## StarVerus: LLM-Powered Multi-Agent Collaboration for Industrial Rust Code Verification Automation

Chao Jiang Ding Wang

College of Computer Science and Software Engineering, Shenzhen University Shenzhen, China {2410104016,2510104008}@mails.szu.edu.cn

Cheng Wen Zhong Ming College of Computer Science and Software Engineering, Shenzhen University Shenzhen, China mingz@szu.edu.cn

## Abstract

Creating code specifications is a crucial measure to improve the trustworthiness of many industrial systems implemented in Rust with high security requirements. Because writing specifications requires highly specialized professionals and is time-consuming, the automatic generation of specifications, enabled by large language models (LLMs), has received increasing attention and shown promising results. However, these methods typically focus on partial specification generation (generating proofs after the contract is known) and on extracting dependencies between code modules using predefined relations. This is not suitable for real-world industrial systems where the goal is to generate complete specifications from scratch and where the complex dependencies between code modules are variable. To address this, we propose a multi-agent collaborative framework, StarVerus, to automate the verification of industrial Rust code. Specifically, StarVerus addresses the aforementioned limitations in two ways: 1) In the generation phase, it instructs the LLM to generate all specifications for a given code, and in the repair phase, it uses a cascaded two-stage process of contract alignment and proof repair to correct them; 2) In both the generation and repair phases, it utilizes a function call graph to adaptively obtain bidirectional contextual information (i.e., what it calls and what calls it) for each code module as an additional information source for the LLM. Furthermore, StarVerus introduces a planner-repairer-actor-rewriter multi-agent paradigm to further enhance the proof repair capabilities. Finally, the effectiveness of StarVerus is validated through experiments on benchmark datasets and deployment in a real operating system.

<sup>∗</sup>Corresponding author.

![](_page_0_Picture_7.jpeg)

[This work is licensed under a Creative Commons Attribution 4.0 International License.](https://creativecommons.org/licenses/by/4.0) KDD '26, Jeju Island, Republic of Korea © 2026 Copyright held by the owner/author(s). ACM ISBN 979-8-4007-2259-2/2026/08 <https://doi.org/10.1145/3770855.3818485>

Dugang Liu<sup>∗</sup> Zhiwu Xu

College of Computer Science and Software Engineering, Shenzhen University Shenzhen, China {liudugang,xuzhiwu}@szu.edu.cn

Yuwei Liu Xinyi Wan Lin Huang Ant Research, Ant Group Hangzhou, China {lyw458372,wanxinyi.wxy,linyu.hl}@antgroup.com

## CCS Concepts

• Software and its engineering → Software verification and validation.

## Keywords

Multi-agent collaboration, Code verification, Specification generation, Rust code

#### ACM Reference Format:

Chao Jiang, Ding Wang, Dugang Liu, Zhiwu Xu, Cheng Wen, Zhong Ming, Yuwei Liu, Xinyi Wan, and Lin Huang. 2026. StarVerus: LLM-Powered Multi-Agent Collaboration for Industrial Rust Code Verification Automation. In Proceedings of the 32nd ACM SIGKDD Conference on Knowledge Discovery and Data Mining V.2 (KDD '26), August 09–13, 2026, Jeju Island, Republic of Korea. ACM, New York, NY, USA, [12](#page-11-0) pages[. https://doi.org/10.1145/3770855.3818485](https://doi.org/10.1145/3770855.3818485)

## <span id="page-0-0"></span>1 Introduction

Currently, industrial systems serving high-security domains, such as operating systems (OS), financial systems, and aerospace systems, are gradually migrating to Rust-based architectures due to Rust's superior security features [\[4,](#page-9-0) [14,](#page-9-1) [18,](#page-9-2) [19,](#page-9-3) [22,](#page-9-4) [29\]](#page-9-5). The trustworthiness of these industrial systems can be further guaranteed by writing specifications (consisting of contracts and proofs) for each piece of Rust code to reflect developers' expectations of the code's behavior, and then using verifiers to check the correctness of the code-specification pairs [\[11,](#page-9-6) [30,](#page-9-7) [39\]](#page-9-8). However, writing correct specifications requires a high level of expertise from practitioners and is very time-consuming. Furthermore, different verifiers have different specification syntax constraints, significantly increasing the difficulty. With the rapid development of large language models (LLMs), leveraging their powerful code-generation and logical reasoning capabilities to automate code specification creation and thereby alleviate bottlenecks in the aforementioned practices has attracted increasing attention from both academia and industry [\[10,](#page-9-9) [34,](#page-9-10) [36\]](#page-9-11).

Existing LLM-powered methods for automated specification generation for Rust typically employ a generate-and-repair paradigm, where the generation phase produces an initial specification for

given Rust code, and the repair phase iteratively corrects the specification based on feedback from a verifier [1, 6, 8, 36]. Since generating the correct specifications in a single pass using an LLM is often non-trivial, recent work has focused on improving the repair phase. Despite promising results, generalizing these methods to real-world industrial systems remains very challenging. On the one hand, most methods consider a partial specification generation setting, focusing only on the proof part of the specification and assuming the contract part is given [1, 33]. However, writing contracts for complex, multi-file code in industrial systems in advance is particularly costly. On the other hand, specification generation for industrial systems requires careful consideration and handling of complex structural dependencies among code modules. Although a few methods address system-level code specifications, they rely on predefined sets of relations to extract contextual information, which is then aggregated into a single file for processing (as illustrated in Figure 1) [37, 41]. This operation clearly lacks flexibility and applicability, and may result in missing or redundant information.

<span id="page-1-0"></span>![](_page_1_Figure_3.jpeg)

Figure 1: Examples of existing LLM-based specification generation methods.

To address this, we propose StarVerus, a multi-agent collaborative framework for automated verification of industrial-grade Rust code. Unlike previous methods, StarVerus aims to achieve fully automated specification generation without any predefined manual specifications and to adaptively capture and utilize the complex dependencies among required code modules. Specifically, StarVerus uses LLMs to initialize complete specifications for given code during the generation phase, and introduces a cascaded structure of contract alignment and proof repair during the repair phase to correct them. Contract alignment uses LLMs as judges to promote semantic consistency between contracts and code behavior;

proof repair employs a multi-agent paradigm comprising planner, repairer, actor, and rewriter to enhance performance. In both phases, StarVerus also uses function call graphs [15] to adaptively extract bidirectional contextual information for each code module (i.e., which modules call it and which it calls) to enhance LLM reasoning. Finally, experiments conducted on five benchmarks and deployment on a real OS (Asterinas) validated the effectiveness of StarVerus. We publicly release the code and benchmarks at: https://github.com/Je5s1e/KDD26-ADS-StarVerus.

#### 2 Related Work

This section briefly reviews the literature on the following two research topics: specification and verification in industry, and LLMdriven automated specification generation.

Specification and Verification in Industry. Writing correct specifications for code and verifying them using a verifier, i.e., formal verification, has long been considered the gold standard for ensuring the correctness of safety-critical industrial systems [12]. Landmark projects such as seL4 [19], CertiKOS [16], and IronFleet [17] have demonstrated the feasibility of verifying operating system kernels and distributed systems. These projects typically rely on interactive theorem provers, such as Isabelle/HOL [27] or Cog, but the verification effort is enormous, writing formal specifications and proofs often takes tens of person-years [5, 26]. In recent years, the industry has shifted towards Rust due to its inherent memorysafety guarantees. To further verify the functional correctness of Rust code, verification tools such as Verus [20] and Prusti [2] have emerged. Verus, in particular, has gained widespread use in systems such as the Asterinas OS because it allows developers to write code specifications directly in Rust syntax [28, 40]. However, in complex industrial environments, this manual annotation process becomes a significant bottleneck. For example, the X509-parser project [13] aims to ensure that no runtime errors occur, but its specifications required 5 months of manual effort. Unlike these manual efforts, StarVerus can automatically generate these artifacts, shifting the paradigm in industrial systems from manual writing to AI-generated specifications and proofs.

LLM-Driven Automated Specification Generation. In recent years, there has been widespread interest in leveraging the codegeneration and logical-reasoning capabilities of large language models (LLMs) to significantly reduce the manual effort required to construct proofs across various verification ecosystems. For example, in scenarios involving imperative languages, such as C and Java, the potential for improving specification generation performance using LLM-enabled multi-agent paradigms [9, 32, 34], prompt engineering [7, 21, 24], and reinforcement learning-based fine-tuning [23, 35] has been explored. As high-security industrial systems gradually migrate to Rust, recent work has begun to focus on the Rust verification ecosystem. Most work typically assumes that contracts are manually predefined and expects LLMs to generate the proof [1, 6, 36, 37, 41]; very few works consider the complete specification (i.e., collaborative generation of both the contract and the proof) [8]. However, the former does not meet the expectation of generating complete specifications from scratch in industrial systems; the latter only addresses function-level specification generation and cannot effectively handle the complex dependencies

among code modules in industrial-scale systems. Unlike these approaches, StarVerus is better aligned with the goal of generating system-level specifications and addresses the associated challenges.

#### 3 Problem Formulation

The objective of StarVerus is to achieve autonomous formal verification for system-level code. Given a system-level codebase R consisting of interdependent functions  $\{f_1, f_2, \ldots, f_n\}$ , the framework aims to synthesize a corresponding set of formal function specifications  $S = \{S_1, S_2, \ldots, S_n\}$ . In practice, the verification outcomes of Verus verifier V are denoted as:

$$(x_i, y_i, e_i) = \mathcal{V}(f_i, S_i), \tag{1}$$

where  $x_i$  is the number of verified proof obligations,  $y_i$  is the number of reported errors (e.g., verification results:: 3 verified, 0 errors), and  $e_i$  denotes the corresponding error messages. Following Verus, verification succeeds if and only if  $x_i > 0$  and  $y_i = 0$ . We thus define the Boolean success predicate:

$$\mathsf{Pass}(f_i, S_i) \triangleq (x_i > 0) \land (y_i = 0). \tag{2}$$

The ultimate objective in StarVerus is to ensure that each function  $f_i$  is formally proven correct against its synthesized specification  $S_i$  under Verus, such that:

$$\forall f_i \in R, \ \mathsf{Pass}(f_i, S_i),$$
 (3)

where each function specification  $S_i \in S$  is defined as a tuple  $S_i = (C_i, P_i)$ , comprising two-tier correctness criteria: (1) **Contracts**  $C_i$ , which establish the behavioral boundaries through preconditions and post-conditions, ensuring that a valid input state yields a guaranteed output state. (2) **Proofs**  $P_i$ , which provide internal auxiliary structures such as loop invariants and assertions. These annotations serve as the essential logical scaffolding that enables the underlying SMT solver to prove that the function body strictly adheres to its contracts  $C_i$ .

## 4 The Proposed Framework

#### 4.1 Overview

As illustrated in Figure 2, StarVerus introduces an autonomous, end-to-end framework designed to tackle the complexity of generating formal specifications for industrial Rust code. The framework comprises two core phases: (1) Bottom-up Specification Generation: As the foundational step, this stage constructs the function call graph and establishes a bottom-up layer-wise traversal order, laying the foundation for resolving cross-module dependencies. Following the order, it employs a dual-view context that harmonizes local code semantics with global usage contexts and leverages an LLM to synthesize a set of candidate initial functional specifications. (2) Multi-Agent Collaborative Specification Repair: This phase is triggered when all candidate specifications from the initial synthesis fail verification under the Verus verifier. It employs a multi-agent orchestration framework structured in two stages. First, a dual-agent mechanism is employed to align the synthesized contracts, ensuring consistency with the actual code implementation. Subsequently, a proof repair pipeline consisting of planner, repairer, actor, and rewriter interacts iteratively to resolve specific verification errors in proofs. This hierarchical approach forms a

closed loop, ensuring that every function not only passes local verification but also satisfies system-wide consistency requirements. Figure 10 in Appendix D provides a complete end-to-end case study of the repair process, showcasing the outputs produced at each stage. All prompt templates are shown in Figure 9 in Appendix A.

## 4.2 Bottom-up Specification Generation

The specification generation stage is designed to provide a formal foundation for the codebase through two primary modules: constructing a function call graph and synthesizing initial formal specifications for each identified function.

To handle cross-module interactions in industrial Rust code, StarVerus first performs dependency analysis to turn the unstructured codebase into an ordered verification workflow. It constructs a global function call graph G = (V, E) via static analysis with the open-source SCIP tool [15], where  $V = \{f_1, f_2, \dots, f_n\}$  and  $(f_i, f_i) \in E$  if function  $f_i$  invokes  $f_i$  (Figure 3 shows a real-world call graph generated in our industrial evaluation). After building G, StarVerus derives a bottom-up, layer-wise traversal order: leaf functions (with no callee functions) are processed first, so that when synthesizing specifications for a target function, all its downstream callee function specifications are already available and verified. This leaf-to-root strategy decomposes cross-module verification into locally guided synthesis tasks and provides a deterministic foundation for subsequent generation and repair phases. In the generation phase, StarVerus constructs a dual-view context  $X_i$  for each target function  $f_i$  to ensure globally consistent specification synthesis. Guided by the call graph  $G, X_i$  integrates the contracts of callee functions as boundary constraints and caller-side call-site snippets as usage requirements. Conditioned on  $X_i$ , an LLM  $G_{init}$ generates a set of initial specification candidates:

$$(S_i^{(1)}, S_i^{(2)}, \dots, S_i^{(n)}) = G_{init}(f_i, X_i),$$
 (4)

where n denotes the number of synthesized specification candidates. Upon completion of generation, StarVerus validates all candidates  $(S_i^{(1)}, S_i^{(2)}, \ldots, S_i^{(n)})$  with the Verus verifier  $\mathcal V$  and ranks them by a verification score and then selects the best candidate  $S_i^{(\star)}$  by maximizing  $x_i$  and minimizing  $y_i$ . If  $S_i^{(\star)}$  fully verifies  $f_i$ , the framework writes the specification  $S_i^{(\star)}$  back to the original codebase and proceeds to the next function in the traversal order; otherwise, it transitions to the subsequent repair phase, using  $S_i^{(\star)}$  as the starting point for repair.

# 4.3 Multi-Agent Collaborative Specification Repair

The function specifications generated in the previous phase rarely pass formal verification, as they often harbor residual syntactic errors or logical gaps, i.e.,  $\neg \operatorname{Pass}(f_i, S_i^{(\star)})$ . To address this, StarVerus employs a multi-agent repair pipeline designed for high-efficiency error resolution. The repair phase is decoupled into two steps: contract alignment and multi-agent repair.

4.3.1 Contract Alignment. To effectively guide the repair process, StarVerus must first address the challenge of error attribution in Verus. As Verus specifications comprise contracts and proofs, this

<span id="page-3-0"></span>![](_page_3_Figure_2.jpeg)

Figure 2: StarVerus's workflow includes a generation phase and a repair phase. In the generation phase, contracts and proofs are generated for the given code (i.e., complete specifications); in the repair phase, the contract alignment and proof repair components are used in a cascaded manner to calibrate the contracts and proofs, respectively.

<span id="page-3-1"></span>![](_page_3_Figure_4.jpeg)

Figure 3: A real-world call graph generated by StarVerus from our industrial evaluation.

structure ensures rigor; however, the cascading effects of SMT-based verification often complicate error localization, in which a single defect can trigger multiple misleading diagnostic reports. For instance, an incorrect post-condition may propagate and cause an invariant failure, making it difficult to pinpoint the true source of contradiction. To mitigate this challenge, StarVerus prioritizes contract alignment at the very beginning of the repair pipeline and employs an iterative Judge-Aligner dual-agent paradigm.

**Judge.** Let k denote the iteration index, where the process starts from the best candidate produced in the initial synthesis  $S_i^{(\star)}$ . In each iteration k, the judge  $G_J$  evaluates the contract in  $S_i^{(k)}$  against the implementation  $f_i$  and context  $X_i$  to produce a status–diagnosis pair:

$$(s^{(k)}, d^{(k)}) = G_I(f_i, S_i^{(k)}, \mathcal{X}_i).$$
 (5)

Here,  $s^{(k)} \in \{\text{Aligned}, \text{Misaligned}\}\$ represents the alignment status, indicating whether the current contract semantically captures the intended behavior of the code implementation  $f_i.d^{(k)}$  denotes the diagnostic feedback, a natural language explanation generated by the judge that identifies specific semantic discrepancies and provides actionable refinement suggestions.

**Aligner.** If  $s^{(k)}$  = Misaligned, the aligner  $G_A$  revises the contracts in  $S_i^{(k)}$  following the refinement suggestions in  $d^{(k)}$ :

$$S_i^{(k+1)} = G_A(f_i, S_i^{(k)}, d^{(k)}).$$
 (6)

When  $s^{(k)}$  = Aligned, StarVerus advances to the subsequent multiagent repair pipeline. During contract alignment, StarVerus primarily focuses on refining contracts; however, when necessary to disambiguate error attribution or maintain consistency, it may also apply minor, localized edits to proofs (e.g., adjusting or temporarily weakening invariants) without changing the overall proof intent. This alignment step synchronizes function contracts with the program's execution semantics, enabling later stages to focus on satisfying proofs without the interference of mismatched contracts. To ensure termination within a bounded compute budget, when k reaches the preset limit K, StarVerus proceeds to the subsequent multi-agent repair pipeline.

4.3.2 Proof Repair. After contract alignment (i.e., once  $s^{(k)} = A$  ligned or the budget limit K is reached), StarVerus shifts to repairing the remaining verification failures in proofs. In contrast to contract alignment, this stage primarily focuses on fixing proofs while keeping the contracts unchanged whenever possible. Let  $k^*$  be the final alignment iteration and define the repair-stage initialization as  $S_i^{(0)} := S_i^{(k^*)}$ . Thereafter, we drop the alignment index and

<span id="page-4-1"></span>

| Benchmark Sources      | VerusBench | MBPP  | HumanEval | VeriCoding | DAFNY2VERUS | Overall |
|------------------------|------------|-------|-----------|------------|-------------|---------|
| # Tasks                | 144        | 77    | 38        | 450        | 53          | 762     |
| Avg. Executable LOC    | 23.44      | 18.47 | 23.71     | 20.75      | 17.72       | 20.97   |
| Avg. Specification LOC | 29.94      | 26.45 | 68.16     | 51.49      | 21.51       | 43.63   |

Table 1: Statistics of the benchmarks.

use  $t \in \{0, 1, ..., T\}$  to index the specification state, denoting the evolving specification by  $S_i^{(t)}$ , where T is the total number of repair rounds. The proof repair process starts from  $S_i^{(0)}$  and involves four specialized agents.

**Planner.** The planner  $G_P$  acts as the strategic orchestrator of the proof repair process [31, 38]. Given the function implementation  $f_i$ , the current function specification  $S_i^{(t)}$ , the error messages  $e_i^{(t)}$  checked by the Verus verifier  $\mathcal{V}$ , and context  $X_i$ ,  $G_P$  performs a rootcause analysis to categorize the failure. It selects a repair agent from the pool  $G_R = \{G_{R_1}, G_{R_2}, \ldots, G_{R_n}\}$  whose specialization matches the diagnosed failure. Each agent targets a specific class of proof errors (e.g., syntax errors, invariant violations, or assertion failures), and the complete agent list is provided in Figure 4. This selection is formulated as:

$$G_{R_{\text{sel}}} = G_P(f_i, S_i^{(t)}, e_i^{(t)}, X_i),$$
 (7)

where  $G_{R_{sel}} \in G_R$  denotes the chosen repairer. By delegating tasks to domain-specific modules, the planner effectively narrows the search space and ensures that each error is handled with the appropriate reasoning capability.

<span id="page-4-0"></span>

| Repairer       |                            |                      |  |  |  |
|----------------|----------------------------|----------------------|--|--|--|
| CantFindValue  | UnexpectedToken            | MismatchedType       |  |  |  |
| ArithmeticFlow | <b>ExpectedCurlyBraces</b> | IncompatibleTypes    |  |  |  |
| PreCondFail    | ExpectedComma              | TypeAnnotationNeeded |  |  |  |
| PostCondFail   | TriggerInferenceFail       | TriggerInferenceFail |  |  |  |
| InvFailFront   | BadQuantifierSyntax        | UnknownProver        |  |  |  |
| InvFailEnd     | AssertFail                 | Other                |  |  |  |

Figure 4: Repairer agent list.

**Repairer.** Once the planner  $G_P$  identifies the failure type, the selected repairer  $G_{R_{\text{sel}}}$  generates a natural-language repair blueprint  $\text{Step}_i^{(t)}$ , which is then consumed by the actor  $G_C$  in repair round t to apply the specified edits and produce updated specifications:

$$Step_i^{(t)} = G_{R_{sel}}(f_i, S_i^{(t)}, e_i^{(t)}, \mathcal{H}_i^{(t)}, \mathcal{X}_i).$$
 (8)

We maintain an accumulated repair history  $\mathcal{H}_i^{(t)}$ , which is fed only to the repairer to provide iterative context and discourage repetitive edits. Each record stores the repair action and the verifier feedback obtained after applying it:

$$h_i^{(t)} \triangleq \left( \text{Step}_i^{(t)}, \ e_i^{(t+1)} \right), \qquad \mathcal{H}_i^{(t)} \triangleq \langle h_i^{(0)}, \ \dots, \ h_i^{(t-1)} \rangle, \quad (9)$$

where  $\mathcal{H}_i^{(t)}$  contains the records from rounds 0 to t-1. After round t, if the verification fails (i.e., a new feedback  $e_i^{(t+1)}$  is produced and another repair round is required), we append the new record:

$$\mathcal{H}_i^{(t+1)} = \mathcal{H}_i^{(t)} \oplus h_i^{(t)}. \tag{10}$$

For the repairer specialized in assertion repair, it autonomously determines whether a failing assertion should be promoted to a loop invariant. This promotion is essential for addressing failures caused by insufficient inductive strength; by elevating localized correctness checks to loop invariants, the repairer provides the SMT solver with the requisite inductive hypotheses to preserve logical properties across all iterations.

**Actor.** The actor  $G_C$  serves as the executor, operationalizing the repair plan by applying concrete edits to the specifications. In each repair round t, given the blueprint  $\operatorname{Step}_i^{(t)}$ , the actor samples w candidate updated specifications:

$$(S_{i,1}^{(t+1)}, S_{i,2}^{(t+1)}, \dots, S_{i,w}^{(t+1)}) = G_C(S_i^{(t)}, \operatorname{Step}_i^{(t)}).$$
 (11)

Star Verus then validates all candidates  $(S_{i,1}^{(t+1)},\,S_{i,2}^{(t+1)},\,\dots,\,S_{i,w}^{(t+1)})$  with the Verus verifier  $\mathcal V$  and selects the best candidate as  $S_i^{(t+1)},$  which is consistent with the best-candidate selection used in the initial synthesis stage. If Pass  $(f_i,\,S_i^{(t+1)}),$  Star Verus writes it back and proceeds to the next function in the traversal order; otherwise, it records the verifier feedback as  $e_i^{(t+1)}$  and continues to the next repair round.

**Rewriter.** When the repair process reaches the maximum round T, StarVerus triggers a rewriting phase to mitigate assertion bloat: after many failed iterations, the specification may accumulate redundant assert statements that clutter the proof and hinder SMT solving. Figure 11 in Appendix D provides an intuitive example of assertion bloat. Rewriter  $G_W$  performs a structural reset by pruning non-essential assert statements and re-synthesizing more comprehensive loop invariants that summarize the intended inductive facts. Formally, the rewriter produces a rewritten specification:

$$S_i^{(T')} = G_W(S_i^{(T)}).$$
 (12)

The rewritten specification  $S_i^{(T')}$  is then re-injected into the pipeline as a new starting point (i.e., setting  $S_i^{(0)} := S_i^{(T')}$ ), thereby restarting a fresh repair cycle of up to T rounds. This rewriter is triggered at most once per function; if verification still fails after the restarted T rounds, StarVerus terminates the repair for  $f_i$ .

<span id="page-5-0"></span>

|             |        |        | StarVerus |        |         |        |        |        | Baselines |         |            |                   |           |
|-------------|--------|--------|-----------|--------|---------|--------|--------|--------|-----------|---------|------------|-------------------|-----------|
| Source      | #Tasks | Qwen   | -Coder    | DeepSe | ek-Chat | Lla    | ma     | GP     | Г-4о      | DeepSee | k-Reasoner | AlphaVerus        | AutoVerus |
|             |        | 0-shot | 5-shot    | 0-shot | 5-shot  | 0-shot | 5-shot | 0-shot | 5-shot    | 0-shot  | 5-shot     | (5-shot) (0-shot) |           |
| VerusBench  | 144    | 62     | 111       | 42     | 121     | 18     | 102    | 37     | 98        | 65      | 130        | 48                | 16        |
| MBPP        | 77     | 42     | 61        | 31     | 64      | 15     | 53     | 21     | 62        | 40      | 73         | 19                | 13        |
| HumanEval   | 38     | 4      | 12        | 8      | 15      | 3      | 7      | 6      | 11        | 9       | 17         | 2                 | 0         |
| DAFNY2VERUS | 53     | 36     | 48        | 28     | 45      | 13     | 38     | 17     | 45        | 45      | 51         | 16                | 20        |
| VeriCoding  | 450    | 329    | 360       | 238    | 365     | 152    | 287    | 203    | 343       | 336     | 404        | 120               | 148       |
| Total       | 762    | 62.1%  | 77.7%     | 45.5%  | 80.1%   | 26.4%  | 63.9%  | 37.3%  | 73.4%     | 65.0%   | 88.6%      | 26.9%             | 25.9%     |

Table 2: Overall verification success rates on the benchmarks.

#### 5 Experiments

#### 5.1 Experiment Settings

Dataset. To evaluate the effectiveness of our StarVerus in automated complete-specification synthesis, we conducted a comprehensive evaluation across five widely used benchmarks and a real-world industrial system. For the benchmarks, we derive tasks by transforming five widely used Rust verification datasets: VeriCoding [6], VerusBench [36], MBPP [1], HumanEval [1], and DAFNY2VERUS [1]. Unlike the original tasks that assume predefined contracts, our benchmarks require simultaneously generating both function contracts and proofs from unannotated code; construction details are provided in Appendix B. As summarized in Table 1, the benchmark suite comprises 762 tasks, with an average of 20.97 executable LOC and 43.63 specification LOC per task. For the industrial evaluation, we further evaluate Asterinas [28], an industrial-grade safe OS kernel. We specifically target the FVT (Formal Verification Target) module within vostd [3], which provides high-level safe abstractions for low-level hardware interactions. FVT focuses on the memory-management subsystem, a critical component for kernel safety. Our evaluation covers verification targets including memory region initialization, page lifecycle safety (via ghost state), and page table cursor navigation. These tasks involve complex pointer reasoning and deep invariants, serving as a rigorous testbed for StarVerus in a production-scale systems environment.

Baselines. For the benchmarks evaluation, we use two representative methods, AlphaVerus [1] and AutoVerus [36] as baselines. Since these tools were not originally designed for complete-specification synthesis, we extended them with the necessary adaptations to support operation on unannotated code in our benchmarks. Specifically, we uniformly provide them only with the raw program and add a statement to the baseline prompt requiring that a contract be generated simultaneously. Aside from this, no other modifications were made, thereby minimizing the impact on performance. To ensure a fair comparison, we maintain their default configurations: AlphaVerus uses Llama-3.1-70B, while AutoVerus uses GPT-40.

**Implementation Details.** (1) Bottom-up Specification Generation: For each task, the LLM  $G_{init}$  generates five candidate programs (n=5) at a high temperature (Temp=1.0) to maximize strategy diversity. If all candidates fail verification, the program with the highest score is selected as the seed for subsequent repair. (2) Multi-Agent Collaborative Specification Repair: Repair is performed at a

lower temperature (Temp=0.3) to prioritize stability. In the preceding contract-alignment stage, we perform up to K=3 alignment iterations. In the proof repair stage, we allocate an initial repair budget of T=3 epochs, and the actor generates three repair candidates per epoch (w=3) to explore diverse fix strategies. If verification still fails after these T=3 epochs, we invoke the rewriter to rewrite the core proof structure. We then grant an additional T=3 repair epochs to refine the rewritten specifications. As a result, the repair budget is extended from T=3 to T=6 for such challenging cases. (3) Few-shot Selection Strategy: To provide relevant logical and structural priors, few-shot cases are selected via semantic retrieval. We map all benchmark samples into a semantic vector space using the Qwen-text-embedding model. For each target task, we perform k-NN retrieval based on cosine similarity to identify the top-5 most similar external samples to serve as in-context demonstrations.

**Evaluation Metric.** We evaluate StarVerus across two complementary dimensions: (1) Verification Pass Rate. The absolute count of tasks that successfully pass the Verus verifier following the joint generation and repair phases. This serves as the definitive measure of functional correctness and logical completeness. (2) BLEU Score. The average linguistic similarity between synthesized, fully-annotated programs and the ground-truth in benchmarks. This metric assesses the semantic naturalness and alignment of the generated specifications.

#### 5.2 Benchmarks Evaluation

This section evaluates the overall performance of StarVerus across multiple LLM backends and compares it against established stateof-the-art baselines. Specifically, the Qwen-Coder backend uses the gwen3-coder-480b-a35b-instruct model, and the Llama backend uses the llama-4-maverick-17b-128e-instruct model. (1) Verification Pass Rate. As shown in Table 2, StarVerus consistently outperforms AlphaVerus (26.9%) and AutoVerus (25.9%) across all backends. The 5-shot configuration yields substantial gains, with pass rates ranging from 63.9% to 80.1% across most models and peaking at 88.6% with DeepSeek-Reasoner. These results demonstrate the robustness and superior adaptability of StarVerus across diverse LLM architectures. (2) BLEU Score. Table 3 compares specification quality using the BLEU metric. StarVerus reports the BLEU score averaged across all evaluated backbone LLMs and consistently achieves higher scores than all baselines, reaching 43.67 (0-shot) and 58.99 (5-shot), surpassing AutoVerus (42.71) and AlphaVerus

(56.39), respectively. These results confirm that StarVerus generates specifications that exhibit superior structural and semantic alignment relative to the expert-annotated ground truth. Additional results can be found in Appendix C.

<span id="page-6-0"></span>Table 3: Average BLEU score comparison between StarVerus and baselines.

| Setting             | Average BLEU |
|---------------------|--------------|
| AutoVerus (0-shot)  | 42.71        |
| AlphaVerus (5-shot) | 56.39        |
| StarVerus (0-shot)  | 43.67        |
| StarVerus (5-shot)  | 58.99        |

## 5.3 Ablation Study

To evaluate the contribution of each component, we compare our StarVerus against four variants by systematically disabling core mechanisms on the DAFNY2VERUS benchmark. The results in Figure 5 demonstrate the necessity of each component. (1) w/o Contract Alignment. Removing contract alignment leads to clear performance degradation for most models, indicating that aligning synthesized contracts with the implementation intent is critical for effective downstream proof repair. For example, DeepSeek-Chat drops to 0.65, while Llama suffers the most severe decline (falling to 0.15). This trend suggests that misaligned contracts can quickly propagate inconsistencies and lead to globally inconsistent specifications. (2) w/o Width Exploration. Disabling width exploration in actor (i.e., using w=1) also reduces performance across models. The decline is notable for DeepSeek-Reasoner (0.85) and Llama (0.12), indicating that exploring multiple repair candidates helps avoid brittle local optima. (3) w/o Rewriter. Without the rewriter, all models experience the most substantial drop, e.g., Qwen-Coder decreases to 0.53, DeepSeek-Chat to 0.46, and Llama to 0.08. This result suggests that for complex failures, incremental patching alone is often insufficient and must be complemented by structural proof reorganization. (4) w/o Planner. Removing the planner yields a moderate but consistent decline for several models (e.g., Qwen-Coder to 0.77 and DeepSeek-Chat to 0.65), implying that adaptive error prioritization improves repair efficiency. In contrast, DeepSeek-Reasoner remains close to the baseline 0.96, suggesting that stronger models may be less sensitive to heuristic scheduling in this setting.

#### 5.4 In-depth Analysis

Next, we conduct an in-depth analysis of the full-specification generation task and the characteristics of StarVerus across multiple dimensions, including error distribution, the performance-efficiency trade-off, the specific distribution of the repair phase, convergence, and robustness. Subsequently, we further explore strategies for evaluating specifications. This comprehensive analysis aids in identifying bottlenecks within the task, characterizing the dynamics of the iterative repair process, and validating the effectiveness of StarVerus.

**Error Distribution.** What are the primary challenges associated with the task of full specification generation? Figure 6 highlights

type mismatches and logical failures as primary bottlenecks. The divergent error patterns, ranging from Llama's structural issues to the reasoning models' verification flaws, underscore the need for a robust repair mechanism. By effectively addressing both structural and logical inconsistencies, StarVerus provides a versatile framework that enhances repair efficiency across diverse model architectures.

Performance-Efficiency Trade-off Analysis. Does StarVeurs offer good practical utility? Table 4 provides a detailed quantitative comparison of the cost-efficiency trade-off between StarVerus and the baseline AutoVerus framework, with both utilizing GPT-40 as the underlying LLM backbone. Because StarVerus employs a comprehensive multi-agent collaborative repair pipeline, it inherently requires more iterations and computational resources to thoroughly explore diverse fix strategies. Specifically, the average verification runtime per task increases from 84.75 seconds to 113.9 seconds, representing a 34.4% latency overhead. Similarly, the average token consumption grows from 36,383 tokens in AutoVerus to 45,364 tokens in StarVerus, resulting in a 24.7% token overhead. However, this additional cost yields a 44.0% relative improvement in verification pass rate, demonstrating a favorable trade-off for offline, safety-critical industrial verification.

<span id="page-6-1"></span>Table 4: Cost and performance comparison with AutoVerus.

| Metric     | AutoVerus | StarVerus | Delta  |
|------------|-----------|-----------|--------|
| Avg. Time  | 84.75s    | 113.9s    | +34.4% |
| Avg. Token | 36,383    | 45,364    | +24.7% |
| Pass Rate  | 25.9%     | 37.3%     | +44.0% |

Repair Phase Analysis. To gain a more fine-grained understanding of the repair process, Table 5 quantifies the contribution of each repair phase. Multi-Agent Specification Repair serves as the primary driver: 4,487 triggers yield 62.54% of total successes, underscoring the value of broad multi-agent exploration. Proof Rewrite achieves a 29.15% success-per-trigger rate and contributes 21.54% of total successes, focusing on high-precision logical correction of the target specification. Together, this synergy between broad exploration and targeted refinement enables efficient convergence toward the verified state.

**Convergence Analysis.** Furthermore, Figure 7 illustrates the repair convergence, starting from contract alignment (t=0) followed by sequential proof repair iterations  $(t=1\ \text{to}\ 6)$ : the cumulative success exceeds 90% by t=3, and the largest single-epoch gain occurs at t=3, largely driven by the rewriter. The process stabilizes by t=4, indicating that most solvable cases are resolved with a small repair iteration budget. This means that StarVerus, with a small number of repair cycles, already possesses considerable performance, further reflecting its practicality.

**Robustness Analysis.** What would be the impact on StarVerus if large-scale closed-source LLM backbones were no longer used? To answer this question, Table 6 evaluates StarVerus with lightweight open-source LLMs on DAFNY2VERUS. Even with 7B/8B backbones, StarVerus consistently outperforms the adapted AutoVerus [36] and AlphaVerus [1] baselines: in the 5-shot setting, Qwen2.5-Coder-7B, Meta-Llama-3.1-8B-Instruct, and DeepSeek-R1-Distill-Qwen-7B

<span id="page-7-0"></span>![](_page_7_Figure_2.jpeg)

Figure 5: Ablation study of StarVerus on DAFNY2VERUS. Results are reported as the verification ratio of each configuration relative to the full StarVerus framework across various LLM backends.

<span id="page-7-2"></span>Table 5: Contribution of repair phases. The table distinguishes between the contract alignment, proof repair, and proof rewrite phases, quantifying their respective impacts on final verification success.

| Repair Phase                        | Triggered | Fixed | Success / Trigger | Contrib. |
|-------------------------------------|-----------|-------|-------------------|----------|
| Contract Alignment                  | 1,735     | 129   | 7.44%             | 7.39%    |
| Proof Repair (Before Proof Rewrite) | 4,487     | 1,092 | 24.34%            | 62.54%   |
| Proof Rewrite                       | 1,290     | 376   | 29.15%            | 21.54%   |
| Proof Repair (After Proof Rewrite)  | 914       | 149   | 16.30%            | 8.53%    |

<span id="page-7-1"></span>![](_page_7_Figure_6.jpeg)

Figure 6: Repairer invocations across LLM backends for the top 8 verification error types, highlighting the diverse challenges in automated specification generation.

<span id="page-7-3"></span>![](_page_7_Figure_8.jpeg)

Figure 7: Convergence analysis of StarVerus on benchmarks. Bars and the line plot denote the number of fixed tasks per stage and the cumulative success proportion, respectively. = 0 represents the initial contract alignment.

solve 38, 37, and 39 out of 53 tasks, respectively. These results suggest that the gains come mainly from the StarVerus framework rather than solely from large proprietary backbones.

<span id="page-7-4"></span>Table 6: Generalization results on DAFNY2VERUS with lightweight open-source LLMs.

| Category  | Model                       | 0-shot  | 5-shot  |
|-----------|-----------------------------|---------|---------|
| Baselines | AutoVerus / AlphaVerus      | 20 / 53 | 16 / 53 |
|           | Qwen2.5-Coder-7B            | 22 / 53 | 38 / 53 |
| StarVerus | Meta-Llama-3.1-8B-Instruct  | 23 / 53 | 37 / 53 |
|           | DeepSeek-R1-Distill-Qwen-7B | 22 / 53 | 39 / 53 |

BLEU Semantic Analysis. Next, we shift our focus to specification evaluation. We further evaluate BLEU with an LLM-as-Judge semantic analysis on VerusBench. Specifically, we partition all programs that successfully generated correct specifications into 'high' and 'low' sets based on their BLEU scores; we then feed these programs and their corresponding specifications into an LLM and instruct it to assess the quality of the specifications. As shown in Table [7,](#page-8-0) 90.28% of high-BLEU samples are judged as high-quality specifications, indicating a positive correlation between BLEU and semantic quality. However, 44.44% of low-BLEU samples are still high quality, while 9.72% of high-BLEU samples are low quality, suggesting that BLEU should be treated as a useful but incomplete surface-level metric and complemented by evaluation strategies across different dimensions.

Mutation Testing. Following prior work [\[25\]](#page-9-40), we conducted additional mutation testing to rigorously evaluate the strength and quality of the generated specifications as a complement to BLEU/Pass

<span id="page-8-0"></span>Table 7: Relationship between BLEU and semantic specification quality on VerusBench.

| BLEU Group | High Spec Quality | Low Spec Quality |
|------------|-------------------|------------------|
| High BLEU  | 90.28%            | 9.72%            |
| Low BLEU   | 44.44%            | 55.56%           |

Rate. In this context, a robust specification should reliably identify and reject faulty code; therefore, a lower pass rate on mutated code indicates tighter, higher-quality specifications. As shown in Table 8, StarVerus achieves an exceptionally low mutated pass rate of just 7.56%. This significantly outperforms the baseline frameworks, with AutoVerus allowing a 20.81% pass rate and AlphaVerus achieving 8.78%. These results clearly demonstrate that StarVerus succeeds not only in achieving high overall verification pass rates but also in maintaining strict, semantically rigorous bounds without sacrificing the underlying safety guarantees of formal verification.

<span id="page-8-1"></span>Table 8: Mutation testing results for specification strength.

| Framework  | Mutated Pass Rate |
|------------|-------------------|
| AutoVerus  | 20.81%            |
| AlphaVerus | 8.78%             |
| StarVerus  | 7.56%             |

#### 5.5 Industrial Evaluation

To evaluate the practical applicability of StarVerus, we conduct an industrial evaluation on the *Formal Verification Targets* (FVTs) [3] from the Asterinas OS [28]. As shown in Figure 8, we integrate StarVerus into the verification pipeline as an automated engine for specification synthesis and repair. The FVTs focus on critical memory-management subsystems in the OSTD library, including region initialization, page acquisition/release, safe raw-pointer conversions, fallible VM reader/writer accesses, and multi-level pagetable cursor navigation with guard/locking disciplines. As shown in

<span id="page-8-2"></span>![](_page_8_Figure_9.jpeg)

Figure 8: Integration of StarVerus with FVT for industrial verification in Asterinas

Table 9, the FVTs exhibit a function count ranging from 7 to 53 and Exec LOC spanning 32 to 399. Compared to the five benchmarks discussed earlier, these surface-level metrics significantly understate the FVTs' inherent complexity, driven by three core challenges: (1) All targets involve low-level system operations, which are realized through deep library-call chains that demand interprocedural reasoning over cross-module invariants; (2) Even targets with relatively few executable lines may include functions that span dozens of transitive callees, further amplifying the interprocedural proof burden; (3) From a specification perspective, the FVTs require extensive use of advanced Verus features (e.g., ghost state, quantified invariants, ownership/permission tracking, and pointer proofs) to abstract low-level operations into verifiable logical constructs. StarVerus fully verifies mem-region-init, discharging all conditions (100.00%). On larger targets, it verifies 79.41% conditions on page-acquisitionsafety and 68.42% on into-from-raw. Coverage drops on harder targets, reaching 61.11% on vmreader-and-vmwriter, 50.00% on pt-cursor-navigation, and 44.00% on pt-guards. Overall, StarVerus discharges 112 out of 163 verification conditions (68.7%) across all targets, demonstrating its scalability to production-scale Verus workloads and validating its practical utility for verifying critical kernel subsystems in real-world operating systems.

<span id="page-8-3"></span>Table 9: Verification results on FVT. Functions and Exec LOC indicate, respectively, the number of functions and the total executable lines of code in each target. Verified Num reports the number of proof obligations that are successfully verified (with the pass rate shown in parentheses).

| FVT Target              | Functions | Exec LOC | Verified Num |
|-------------------------|-----------|----------|--------------|
| mem-region-init         | 14        | 185      | 22 (100.00%) |
| page-acquisition-safety | 31        | 233      | 27 (79.41%)  |
| into-from-raw           | 35        | 255      | 26 (68.42%)  |
| vmreader-and-vmwriter   | 53        | 399      | 22 (61.11%)  |
| pt-cursor-navigation    | 7         | 32       | 4 (50.00%)   |
| pt-guards               | 16        | 102      | 11 (44.00%)  |

#### 6 Conclusions

This paper introduces StarVerus, an LLM-powered multi-agent framework that automatically generates and verifies complete specifications for industrial Rust code. By leveraging call-graph-aware context construction and a coordinated multi-agent repair pipeline, StarVerus addresses inter-module dependencies and non-convergent proof repair. Experiments on five benchmarks and real-world industrial systems show that StarVerus improves verification success rates and specification quality over prior work, demonstrating the promise of multi-agent methods for scalable, production-grade formal verification.

## Acknowledgments

This work was supported by the National Natural Science Foundation of China (Nos. 62302310 and 62372304), the Basic Research Foundation of Shenzhen City (No. JCYJ20250604184202003), and Ant Group through CCF-Ant Research Fund (RF20250305).

## References

- <span id="page-9-12"></span>[1] Pranjal Aggarwal, Bryan Parno, and Sean Welleck. 2025. AlphaVerus: Bootstrapping Formally Verified Code Generation through Self-Improving Translation and Treefinement. In Proceedings of the 42st International Conference on Machine Learning. 587–615.
- <span id="page-9-26"></span>[2] Vytautas Astrauskas, Aurel Bíly, Jonáš Fiala, Zachary Grannan, Christoph Math- ` eja, Peter Müller, Federico Poli, and Alexander J Summers. 2022. The prusti project: Formal verification for Rust. In Proceedings of th 14th International Symposium on NASA Formal Methods. 88–108.
- <span id="page-9-39"></span>[3] Asterinas Authors. 2025. Asterinas vostd (verified OS standard library): Fvt (functional verification test) module. [https://github.com/asterinas/vostd/tree/](https://github.com/asterinas/vostd/tree/main-archive-20251225) [main-archive-20251225.](https://github.com/asterinas/vostd/tree/main-archive-20251225)
- <span id="page-9-0"></span>[4] Karthikeyan Bhargavan, Antoine Delignat-Lavaud, Cédric Fournet, Anitha Gollamudi, Georges Gonthier, Nadim Kobeissi, Natalia Kulatova, Aseem Rastogi, Thomas Sibut-Pinote, Nikhil Swamy, et al. 2016. Formal verification of smart contracts: Short paper. In Proceedings of the 2016 ACM Workshop on Programming Languages and Analysis for Security. 91–96.
- <span id="page-9-23"></span>[5] Jean-Louis Boulanger. 2013. Industrial use of formal methods: Formal verification. John Wiley & Sons.
- <span id="page-9-13"></span>[6] Sergiu Bursuc, Theodore Ehrenborg, Shaowei Lin, Lacramioara Astefanoaei, Ionel Emilian Chiosa, Jure Kukovec, Alok Singh, Oliver Butterley, Adem Bizid, Quinn Dougherty, et al. 2025. A benchmark for vericoding: Formally verified program synthesis. arXiv preprint arXiv:2509.22908 (2025).
- <span id="page-9-32"></span>[7] Saikat Chakraborty, Shuvendu Lahiri, Sarah Fakhoury, Akash Lal, Madanlal Musuvathi, Aseem Rastogi, Aditya Senthilnathan, Rahul Sharma, and Nikhil Swamy. 2023. Ranking LLM-generated loop invariants for program verification. In Findings of the 2023 Conference on Empirical Methods in Natural Language Processing. 9164–9175.
- <span id="page-9-14"></span>[8] Tianyu Chen, Shuai Lu, Shan Lu, Yeyun Gong, Chenyuan Yang, Xuheng Li, Md Rakib Hossain Misu, Hao Yu, Nan Duan, Peng Cheng, et al. 2025. Automated proof generation for Rust code via self-evolution. In Proceedings of the 13th International Conference on Learning Representations, Vol. 2025. 71891–71918.
- <span id="page-9-30"></span>[9] Zehan Chen, Long Zhang, Zhiwei Zhang, JingJing Zhang, Ruoyu Zhou, Yulong Shen, JianFeng Ma, and Lin Yang. 2025. SLD-Spec: Enhancement LLM-assisted specification generation for complex loop functions via program slicing and logical deletion. arXiv preprint arXiv:2509.09917 (2025).
- <span id="page-9-9"></span>[10] Matthias Cosler, Christopher Hahn, Daniel Mendoza, Frederik Schmitt, and Caroline Trippel. 2023. nl2spec: Interactively translating unstructured natural language to temporal logics with large language models. In Proceedings of the 35th International Conference on Computer Aided Verification. 383–396.
- <span id="page-9-6"></span>[11] Marcos Cramer and Lucian McIntyre. 2025. Verifying LLM-generated code in the context of software verification with Ada/Spark. arXiv preprint arXiv:2502.07728 (2025).
- <span id="page-9-19"></span>[12] Rolf Drechsler. 2004. Advanced formal verification. Springer.
- <span id="page-9-29"></span>[13] Arnaud Ebalard, Patricia Mouy, and Ryad Benadjila. 2019. Journey to a RTE-free X. 509 parser. In Proceedings of the 2019 Symposium sur la sécurité des technologies de l'information et des communications (SSTIC 2019), Vol. 186.
- <span id="page-9-1"></span>[14] Jincao Feng, Weikai Miao, Hanyue Zheng, Yihao Huang, Jianwen Li, Zheng Wang, Ting Su, Bin Gu, Geguang Pu, Mengfei Yang, et al. 2020. FREPA: An automated and formal approach to requirement modeling and analysis in aircraft control domain. In Proceedings of the 28th ACM Joint Meeting on European Software Engineering Conference and Symposium on the Foundations of Software Engineering. 1376–1386.
- <span id="page-9-18"></span>[15] Beneficial AI Foundation. 2026. Scip-callgraph: A tool for generating call graphs from scip index files. [https://github.com/Beneficial-AI-Foundation/scip](https://github.com/Beneficial-AI-Foundation/scip-callgraph)[callgraph.](https://github.com/Beneficial-AI-Foundation/scip-callgraph)
- <span id="page-9-20"></span>[16] Ronghui Gu, Zhong Shao, Hao Chen, Xiongnan Newman Wu, Jieung Kim, Vilhelm Sjöberg, and David Costanzo. 2016. CertiKOS: An extensible architecture for building certified concurrent OS kernels. In Proceedings of the 12th USENIX Symposium on Operating Systems Design and Implementation. 653–669.
- <span id="page-9-21"></span>[17] Chris Hawblitzel, Jon Howell, Manos Kapritsos, Jacob R Lorch, Bryan Parno, Michael L Roberts, Srinath Setty, and Brian Zill. 2015. IronFleet: Proving practical distributed systems correct. In Proceedings of the 25th Symposium on Operating Systems Principles. 1–17.
- <span id="page-9-2"></span>[18] Gerwin Klein, June Andronick, Kevin Elphinstone, Toby Murray, Thomas Sewell, Rafal Kolanski, and Gernot Heiser. 2014. Comprehensive formal verification of an OS microkernel. ACM Transactions on Computer Systems 32, 1 (2014), 1–70.
- <span id="page-9-3"></span>[19] Gerwin Klein, Kevin Elphinstone, Gernot Heiser, June Andronick, David Cock, Philip Derrin, Dhammika Elkaduwe, Kai Engelhardt, Rafal Kolanski, Michael Norrish, et al. 2009. SeL4: Formal verification of an OS kernel. In Proceedings of the ACM SIGOPS 22nd Symposium on Operating Systems Principles. 207–220.
- <span id="page-9-25"></span>[20] Andrea Lattuada, Travis Hance, Chanhee Cho, Matthias Brun, Isitha Subasinghe, Yi Zhou, Jon Howell, Bryan Parno, and Chris Hawblitzel. 2023. Verus: Verifying Rust programs using linear ghost types. Proceedings of the ACM on Programming Languages 7 (2023), 286–315.

- <span id="page-9-33"></span>[21] Jia Li, Ge Li, Yongmin Li, and Zhi Jin. 2025. Structured chain-of-thought prompting for code generation. ACM Transactions on Software Engineering and Methodology 34, 2 (2025), 1–23.
- <span id="page-9-4"></span>[22] Kang Li, Ronghui Gu, Jun Xu, Zhaofeng Chen, Siwei Wu, Yajin Zhou, Mu Zhang, Xiapu Luo, Yuzhe Tang, Yi Li, et al. 2025. Security analysis and formal verification on blockchain and its applications. Foundations and Trends® in Privacy and Security 8, 1 (2025), 1–121.
- <span id="page-9-35"></span>[23] Chang Liu, Xiwei Wu, Yuan Feng, Qinxiang Cao, and Junchi Yan. 2024. Towards general loop invariant generation: a benchmark of programs with memory manipulation. In Proceedings of the 38th International Conference on Neural Information Processing Systems. 129120–129145.
- <span id="page-9-34"></span>[24] Ruibang Liu, Minyu Chen, Ling-I Wu, Jingyu Ke, and Guoqiang Li. 2025. Enhancing automated loop invariant generation for complex programs with large language models. Science of Computer Programming (2025), 103387.
- <span id="page-9-40"></span>[25] Lezhi Ma, Shangqing Liu, Yi Li, Xiaofei Xie, and Lei Bu. 2025. Specgen: Automated generation of formal program specifications via large language models. In Proceedings of the IEEE/ACM 47th International Conference on Software Engineering. 16–28.
- <span id="page-9-24"></span>[26] Vivek Nigam and Carolyn Talcott. 2019. Formal security verification of industry 4.0 applications. In Proceedings of the 24th IEEE International Conference on Emerging Technologies and Factory Automation. 1043–1050.
- <span id="page-9-22"></span>[27] Tobias Nipkow, Markus Wenzel, and Lawrence C Paulson. 2002. Isabelle/HOL: A proof assistant for higher-order logic. Springer.
- <span id="page-9-27"></span>[28] Yuke Peng, Hongliang Tian, Junyang Zhang, Ruihan Li, Chengjun Chen, Jianfeng Jiang, Jinyi Xian, Xiaolin Wang, Chenren Xu, Diyu Zhou, et al. 2025. Asterinas: A Linux ABI-compatible, Rust-based framekernel OS with a small and sound TCB. In Proceedings of the 2025 USENIX Annual Technical Conference. 307–323.
- <span id="page-9-5"></span>[29] Suneel Sarswat and Abhishek Kr Singh. 2019. Formal verification of trading in financial markets. arXiv preprint arXiv:1907.07885 (2019).
- <span id="page-9-7"></span>[30] Merlijn Sevenhuijsen, Khashayar Etemadi, and Mattias Nyberg. 2025. VeCoGen: Automating generation of formally verified C code with large language models. In Proceedings of the IEEE/ACM 13th International Conference on Formal Methods in Software Engineering. 101–112.
- <span id="page-9-37"></span>[31] Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao. 2023. Reflexion: Language agents with verbal reinforcement learning. In Proceedings of the 37th International Conference on Neural Information Processing Systems. 8634–8652.
- <span id="page-9-31"></span>[32] Wenxian Su, Xi Wu, and Yongxin Zhao. 2025. NL2ACSL: Interactively translating natural language to ANSI C specification language with large language models. Knowledge-Based Systems (2025), 115177.
- <span id="page-9-15"></span>[33] Chuyue Sun, Yican Sun, Daneshvar Amrollahi, Ethan Zhang, Shuvendu Lahiri, Shan Lu, David Dill, and Clark Barrett. 2026. Veristruct: AI-assisted automated verification of data-structure modules in Verus. In Proceedings of the 32nd International Conference on Tools and Algorithms for the Construction and Analysis of Systems. 109–128.
- <span id="page-9-10"></span>[34] Cheng Wen, Jialun Cao, Jie Su, Zhiwu Xu, Shengchao Qin, Mengda He, Haokun Li, Shing-Chi Cheung, and Cong Tian. 2024. Enchanting program specification synthesis by large language models using static analysis and program verification. In Proceedings of the 36th International Conference on Computer Aided Verification. 302–328.
- <span id="page-9-36"></span>[35] Chuanhao Yan, Fengdi Che, Xuhan Huang, Xu Xu, Xin Li, Yizhi Li, Xingwei Qu, Jingzhe Shi, Chenghua Lin, Yaodong Yang, et al. 2025. Re: Form–reducing human priors in scalable formal software verification with RL in LLMs: A preliminary study on Dafny. arXiv preprint arXiv:2507.16331 (2025).
- <span id="page-9-11"></span>[36] Chenyuan Yang, Xuheng Li, Md Rakib Hossain Misu, Jianan Yao, Weidong Cui, Yeyun Gong, Chris Hawblitzel, Shuvendu Lahiri, Jacob R Lorch, Shuai Lu, et al. 2025. Autoverus: Automated proof generation for Rust code. Proceedings of the ACM on Programming Languages 9 (2025), 3454–3482.
- <span id="page-9-16"></span>[37] Chenyuan Yang, Natalie Neamtu, Chris Hawblitzel, Jacob R Lorch, and Shan Lu. 2025. VeruSAGE: A study of agent-based verification for Rust systems. arXiv preprint arXiv:2512.18436 (2025).
- <span id="page-9-38"></span>[38] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik R Narasimhan, and Yuan Cao. 2022. React: Synergizing reasoning and acting in language models. In Proceedings of the 11th International Conference on Learning Representations.
- <span id="page-9-8"></span>[39] Zhe Ye, Zhengxu Yan, Jingxuan He, Timothe Kasriel, Kaiyu Yang, and Dawn Song. 2025. VERINA: Benchmarking verifiable code generation. arXiv preprint arXiv:2505.23135 (2025).
- <span id="page-9-28"></span>[40] Junyang Zhang, Xiangcan Xu, Yonghao Zou, Zhe Tang, Xinyi Wan, Kang Hu, Siyuan Wang, Wenbo Xu, Di Wang, Hao Chen, et al. 2025. Cortenmm: Efficient memory management with strong correctness guarantees. In Proceedings of the 31st ACM Symposium on Operating Systems Principles. 1082–1098.
- <span id="page-9-17"></span>[41] Sicheng Zhong, Jiading Zhu, Yifang Tian, and Xujie Si. 2025. RAG-Verus: Repository-level program verification with LLMs using retrieval augmented generation. arXiv preprint arXiv:2502.05344 (2025).

Prompt Template for Initial Generation

#### <span id="page-10-0"></span>Prompt Template for Repair Agent Prompt Template for Planner Agent [SYSTEM] You are the Verification Architect. Your goal is to design a [SYSTEM] Analyze the code and error message, and IMMEDIATELY [SYSTEM] You are a Verus formal verification expert, proficient in writing specifications and proofs for Rust code to ensure function-level safety, functional correctness, and termination of loops/recursion. provide a structured JSON diagnosis. Do not output any conversational text or step-by-step analysis before the JSON. robust fix strategy. - Treat the following "Knowledge Base" as the primary error-specific functional correctr guidance; extract actionable fix patterns from it. - Carefully review the HISTORY and avoid repeating failed or circular fixes; if a line of attack has already failed, pivot. - In CONTEXT, prioritize the 'requires' / ensures' of called functions: satisfy preconditions at call sites and use postconditions as proof hooks. Knowledge Base for SERROR\_TYPE: SKB ### Structured Diagnosis (JSON) ### Structured Diagnosis (JSON) Provide a JSON object wrapped in a markdown code block. The JSON must contain these fields: "root\_cause\_error\_type": (The true root cause error type. Example: "UnresolvedImport", "MismatchedType") - "fix\_order": (An array of EXACT error type strings from the syster ## lask Description Important: The Code to Fill section below contains only a single function to be verified. Please complete specifications and proofs for that function. If the proof requires it, you may additionally generate auxiliary 'proof fn' (lemmas) and output them after the main function; do not generate the complete file or unrelated functions. prompt list. Example: ["UnresolvedImport", "PreCondFail"]) - "summary": (A concise one-line summary of the issue) Evaluate the following diagnosis from the specialist. If specific syntax fixes are proposed in 'patch\_plan', incorporate them unless they are clearly - "root\_cause": (A short tag, e.g., "missing-precondition", "integer "evidence": (Quote the key lines from the error message or code) DIAGNOSIS JSON (Stage 1): - evidence: (Quote the key lines from the error message or code) -"patch\_plan": (Concise hint for the patcher. Prefer spec/ghost/proo If applicable, mention adding '#[verifier::external\_body]' on the fur -"risk": (Optional warnings) Below are relevant source files from the project. Please read carefully to extract needed properties (pay special att definitions and usage patterns): \${Caller Function Context} SDIAGNOSIS\_JSON HISTORY (Previous Rounds) \${Callee Function Context} GIVEN INFO: [ERROR SUMMARY] Primary observed type: \$ERROR\_TYPE ## Output Requirements CONTEXT (Project): <Output Requ [ERRORS] SERRORS SCONTEXT ## Code to Fill [CODE] SCODE CODE (Current) SCODE [CONTEXT] SCONTEXT TARGET FUNCTION Format your output exactly like this STARGET FUNC OUTPUT FORMAT: "root\_cause\_error\_type' "fix\_order": ["...", "..."], "summary": "...", "root\_cause": "...", "evidence": "...", Output EXACTLY three sections with these labels, in this order: [L1 PLAN] ed plan for history tracking (follow system constraints). IL2 PLANI on plan for the coder (follow system constraints). Prompt Template for Action Agent What to avoid / regression warnings (follow system Start with [L1\_PLAN]. Do not output anything else. Implement the Execution Plan above to fix verification errors Prompt Template for Contract Judge [SYSTEM] You are a Verus specification auditor. Based on the provided Follow the system coding guidelines (scope/anti-cheating/Tracked rules) Prompt Template for Contract Alignment guidelines and context, dete requires/ensures are reasona letermine whether the candidate func-onable. Return JSON only, format: { [SYSTEM] You are a Verus specification rewriter. Your task is to imp the requires/ensures clauses of a candidate function based on audit requires cristices are reasonable. Return 350N only, format. { pass . true/false, "reason": "explanation"}. If GUIDELINE is provided, it is the highest priority and must be followed. Additional Hard Constraints (must follow): the requires/ensures clauses of a candidate function based on additionable feedback. Return ONLY the complete rewritten function code (no explanations, no markdown fences). Make ONLY the changes explicitly required by the Execution Plan; do not add extra specifications/refactors. add extra specifications/refactors. - Do NOT introduce any new identifiers/methods/functions/fields/predicates that do not appear in the ### Preconditions vs Postconditions (Be explicit) ### Preconditions vs Postconditions (Be expicit) - "requires" are preconditions: assumptions about inputs/state before the call; they must be reasonable and not depend on return values. - 'ensures' are postconditions: guarantees after the call; when intent implies\ninput/output relations, they must relate outputs to inputs. - Both must align with the function's semantic intent described in 'GUIDELINE'. ## Guidelines for this function < GUIDELINE> GIVEN CODE/context. Do NOT add new quantifiers ('forall'/'exists') or triggers unless the plan icitly instructs you to. SCONTEXT - If the plan provides a "The modified code should look like:" code block, your output MUST match it exactly (except whitespace). <GUIDELINE> \$PLAN lback (reason for failure) ## Context (Abstract Model, Related Structs, etc.) SAUDIT REASON GIVEN CODE SCODE ## Your Task Rewrite the candidate function to fix the issues mentioned in the audit ## Candidate Function (with specifications) Write the fixed code nov

Figure 9: Prompt templates for specialized agents in StarVerus.

#### <span id="page-10-1"></span>**Prompt Design**

We illustrate the modular prompt templates tailored for different specialized agents in StarVerus in Figure 9.

#### <span id="page-10-2"></span>**Benchmarks Construction.**

The five source benchmarks were originally curated for early, experimental iterations of Verus, which operated under more permissive verification semantics and legacy syntax. To obtain a reliable ground-truth set using the modern toolchain, we manually updated these legacy samples to the latest Verus version to satisfy the current, stricter proof obligations. This modernization primarily adds explicit decreases clauses to recursive functions, enabling Verus to discharge the required termination arguments in a principled, tool-supported way. We further applied careful filtering to improve benchmark quality and relevance. First, we deduplicated tasks, especially within HumanEval-derived subsets used by prior work [1] to avoid evaluation bias from near-duplicate instances. Second, we removed trivial tasks: for datasets such as VeriCoding [6], stripping specifications can reduce some samples to overly simple code

fragments with limited verification value, so we pruned them to retain non-trivial algorithmic reasoning requirements. Finally, we performed suitability filtering on the remaining sources, excluding tasks that are incompatible with the current Verus verifier or deviate from our intended complete specification-synthesis setting.

<span id="page-10-4"></span>Table 10: Verification pass rate comparison with VeruSAGE.

| Framework             | Backbone                       | 0-shot         | 5-shot         |
|-----------------------|--------------------------------|----------------|----------------|
| VeruSAGE<br>StarVerus | Qwen-Coder<br>Qwen-Coder       | 43.6%<br>62.1% | 63.2%<br>77.7% |
| VeruSAGE<br>StarVerus | DeepSeek-Chat<br>DeepSeek-Chat | 25.7%<br>45.5% | 61.4%<br>80.1% |
|                       | Беерзеек-Спат                  | 43.370         | 30.1           |

## <span id="page-10-3"></span>**More Comparison Results**

We further compare StarVerus with VeruSAGE [37], a recent agentbased verification framework for Rust systems. As described in

<span id="page-11-1"></span><span id="page-11-0"></span>![](_page_11_Figure_2.jpeg)

Figure 10: The step-by-step verification and repair trajectory of StarVerus on a vector product task.

Section 1, VeruSAGE employs a predefined set of relationships to extract contextual information and synthesize it into a single file for specification generation. As shown in Table 10, StarVerus consistently achieves higher verification pass rates across various backbone LLMs and metric configurations, improving over VeruSAGE by 14.5–19.8 percentage points. These results highlight the benefit of complete specification generation, call-graph-aware context construction, and cascaded contract/proof repair.

#### <span id="page-11-2"></span>D Case Study

Vector Product Case Study. Figure 10 illustrates StarVerus's execution on a vector product task. Initial synthesis often overlooks safety constraints such as arithmetic overflow and array bounds. During Contract Alignment, StarVerus refines preconditions (e.g., adding product bounds) to bridge the semantic gap with the implementation. While the planner-repairer-actor cycle resolves verification errors via incremental patching, it may introduce redundant local assertions. Finally, the rewriter consolidates these patches into clean, global invariants, eliminating loop-body bloat to achieve a rigorous and concise verification state. Assertion Bloat in LLM-driven Repair. Figure 11 illustrates a common failure mode where LLMs struggle to repair Rust specifications. Rather than rectifying the underlying incorrect loop invariant, LLMs often adopt a "trial-and-error" strategy by inserting dense clusters of redundant or erroneous intermediate assertions. This assertion bloat introduces

significant proof noise and triggers cascading secondary failures. Consequently, the solver becomes overwhelmed by logical contradictions or an excessive search space, causing the repair pipeline to stall before reaching a verified state.

<span id="page-11-3"></span>![](_page_11_Figure_8.jpeg)

Figure 11: Illustration of assertion bloat and resulting proof noise in LLM-based repair.