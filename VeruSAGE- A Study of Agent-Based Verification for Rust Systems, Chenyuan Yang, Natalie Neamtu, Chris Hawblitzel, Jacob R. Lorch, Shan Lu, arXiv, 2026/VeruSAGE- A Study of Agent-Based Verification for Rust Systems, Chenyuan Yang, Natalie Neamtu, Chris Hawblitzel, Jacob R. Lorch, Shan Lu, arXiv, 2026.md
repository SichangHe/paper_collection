# VeruSAGE: A Study of Agent-Based Verification for Rust Systems

Chenyuan Yang<sup>⋆</sup> Natalie Neamtu♦ Chris Hawblitzel■ Jacob R. Lorch■ Shan Lu▲■ <sup>⋆</sup>*University of Illinois Urbana-Champaign* ♦*Carnegie Mellon University* ■*Microsoft Research* ▲*University of Chicago*

### Abstract

Large language models (LLMs) have shown impressive capability to understand and develop code. However, their capability to rigorously reason about and prove code correctness remains in question. This paper offers a comprehensive study of LLMs' capability to develop correctness proofs for system software written in Rust. We curate a new system-verification benchmark suite, VeruSAGE-Bench, which consists of 849 proof tasks extracted from eight open-source Verus-verified Rust systems. Furthermore, we design different agent systems to match the strengths and weaknesses of different LLMs (o4 mini, GPT-5, Sonnet 4, and Sonnet 4.5). Our study shows that different tools and agent settings are needed to stimulate the system-verification capability of different types of LLMs. The best LLM-agent combination in our study completes over 80% of system-verification tasks in VeruSAGE-Bench. It also completes over 90% of a set of system proof tasks not part of VeruSAGE-Bench because they had not yet been finished by human experts. This result shows the great potential for LLM-assisted development of verified system software.

## 1 Introduction

In the past few years, two contrasting code and system development methodologies have progressed. On the one hand, AI coding agents [\[37,](#page-13-0) [43\]](#page-14-0) are becoming popular. They are very good at quickly producing a large amount of code with little human support. Their weakness is the lack of a correctness guarantee, which is particularly problematic for reliabilitycritical software, including most system software. On the other hand, system verification techniques are getting mature after decades of research. Recent work [\[6,](#page-12-0) [10,](#page-12-1) [17,](#page-12-2) [19,](#page-13-1) [46\]](#page-14-1) has demonstrated the feasibility for human experts to develop large-scale system software in a popular system programming language (i.e., Rust), together with formal correctness specifications and proofs that can be mathematically verified by tools such as Verus [\[17,](#page-12-2) [18\]](#page-13-2). However, the speed of such code and proof development and the accessibility of such verification techniques to general developers remains questionable. We naturally wonder whether these two methodologies can complement each other. Specifically, can large language models (LLMs) help write correctness proofs for system software?

Several research projects have explored using LLMs for proof writing, but none of them offered an answer to our question. Some of them focused on verification that requires special proof-oriented languages, instead of general programming languages [\[7\]](#page-12-3); the others focused on small programming problems like binary search [\[1,](#page-12-4) [9,](#page-12-5) [23,](#page-13-3) [40,](#page-13-4) [48\]](#page-14-2). For example, the AutoVerus project [\[40\]](#page-13-4) designed a benchmark suite of 150 small Rust programs with Verus specifications, called VerusBench. It also designed an agent system that empowers GPT-4o [\[14\]](#page-12-6) to prove 90% of the tasks in VerusBench. Most recently, RagVerus [\[48\]](#page-14-2) tried AutoVerus plus Retrieval Augmented Generation (RAG), i.e., providing LLMs with example proofs from the same project. They did this for four system projects: VeriSMo [\[49\]](#page-14-3), Vest [\[6\]](#page-12-0), IronKV [\[17\]](#page-12-2), and a small part of Anvil [\[32\]](#page-13-5). Unfortunately, they report a depressing result: only 20% or less of the proof tasks in VeriSMo, IronKV, and Vest could be proved by GPT-4o.

These recent research efforts bring up several natural questions: How do real-world system proof tasks fundamentally differ from small programming problems? Is the poor performance due to limitations in the agent architecture (e.g., AutoVerus + RAG) or the underlying model capabilities (e.g., GPT-4o)? And, ultimately, can state-of-the-art LLMs, paired with specialized agentic designs, effectively tackle the complexity of real-world system verification?

To answer these questions, we curate VeruSAGE-Bench, a comprehensive Verus system verification benchmark suite. It consists of 849 proof tasks extracted from eight open-source Verus-verified system projects authored by different research groups. These projects cover various domains, including operating systems, memory allocators, storage systems, distributed systems, etc. Every task corresponds to one proof function or executable Rust function in the original project, with all the dependencies extracted into a stand-alone Rust file that can be individually compiled and verified. Each task file contains no proof bodies from the original project (i.e., no proof example for LLMs), and hence brings us closer to testing LLMs' real system-proof-writing capabilities.

With this benchmark suite, we can quantitatively measure the makeup of system proofs, and the differences between them and proofs for small programming tasks. Table [1](#page-1-0) lists some of these measurements. It clearly demonstrates that

<span id="page-1-0"></span>

| Per-task characteristic |      | VerusBench VeruSAGEBench |
|-------------------------|------|--------------------------|
| Total LoC               | 32   | 947                      |
| Spec LoC                | 8    | 496                      |
| Proof LoC               | 10   | 50                       |
| Loop invariant proof    | 8    | 1                        |
| Non-loop-inv. proof     | 2    | 49                       |
| # of loops              | 1.6  | 0.08                     |
| # of helper lemmas      | 0.07 | 2.4                      |

Table 1: Proof characteristics, averaged across all benchmark tasks (verified version) in two different benchmark suites. Total lines of code include the target function to prove and all its dependencies.

system proofs are far more complex, with much (over 50×) more lines of specification, code dependencies, proof annotations, and helper lemmas. Furthermore, some code structures that are central to previous benchmarks and proof-synthesis research, such as loops and loop invariants, are rare or even non-existent in the system projects that we studied. [§3](#page-1-1) has details of our methodology and more results.

Using this benchmark suite, we explore what agent systems can produce the best system-proof capability for a range of LLMs. First, we design a *hands-on* agent system VeruSAGE ([§4.2\)](#page-4-0) that greatly improves the system-verification capability of "small" models like o4-mini [\[29\]](#page-13-6) over the state-of-the-art LLM-for-Verus framework, AutoVerus. The complexity of system verification requires us to greatly expand AutoVerus, adding many more agents to "teach" LLMs various aspects of system-verification knowledge and strategy, extending the algorithm to select which of many incomplete proof candidates to refine based on factors like what proof strategy each uses, and forcing LLMs to first plan and then act.

Second, we consider a *hands-off* approach ([§4.1\)](#page-3-0), suitable for strong coding models such as Claude Sonnet 4/4.5 [\[2,](#page-12-7) [3\]](#page-12-8). In this approach, we simply use a generic coding agent, such as GitHub Copilot CLI [\[12\]](#page-12-9), and prompt it to give the LLM access to the Verus standard library and two tools, Verus and a Verus cheating checker. Surprisingly, we find that this produces even better proof capability for Claude Sonnet 4/4.5 than the hands-on approach!

We conduct extensive experiments ([§5\)](#page-5-0) on various combinations of LLMs, agent systems, and system-verification tasks, and test various hypotheses along the way. Most excitingly, the best LLM-agent combination correctly synthesizes proofs for over 80% of VeruSAGE-Bench tasks, with only 7.2 minutes spent on each task on average. This includes an 83% success rate on 157 tasks extracted from Atmosphere [\[10\]](#page-12-1), a project that has not been released online until November 2025 and hence is definitely not in the training data of any models. In addition, LLMs even proved 33 tasks that have not yet been finished by human experts in Atmosphere.

The benchmark and code implementation of VeruSAGE are released at [microsoft/verus-proof-synthesis](https://github.com/microsoft/verus-proof-synthesis/) .

```
1 pub fn MAX_PHYADDR(max_width:u64) -> ( ret : u64)
2 requires 32 <= max_width <= 52,
3 ensures ret < 0x10_0000_0000_0000u64,
4 {
5 assert(1u64 << max_width > 1) by(bit_vector)
6 requires 32 <= max_width <= 52;
7 assert(1u64 << max_width <= 0x10_0000_0000_0000u64)
         by(bit_vector)
8 requires 32 <= max_width <= 52;
9 (1u64 << max_width) - 1u64
10 }
```

Figure 1: A Verus-verified function simplified from NRKernel

### 2 Background

*Verus* [\[17,](#page-12-2) [18\]](#page-13-2) is a tool designed to offer high-performance verification for system software written in Rust. Verus lets a developer give a *specification* for each function, as in the example function in Figure [1.](#page-1-2) A specification can include *pre-conditions* (e.g., line 2), which the function can assume because its callers will be obliged to establish them. A specification can include *post-conditions* (e.g., line 3), which the function is obliged to prove so that its callers can rely on them. Developers can provide *proof annotations* (e.g., lines 5–8) to aid the Verus verifier in proving those obligations. In this case, the proof annotations tell Verus to use bit-vector reasoning to prove that line 9 will not underflow and that it will satisfy the post-condition. To verify the function, Verus turns the executable code, specification, and proof annotations into a query for Verus's underlying theorem prover.

*Large Language Models.* We evaluate four state-of-the-art LLMs. From OpenAI, we consider o4-mini (April 2025) [\[29\]](#page-13-6) and GPT-5 (August 2025) [\[28\]](#page-13-7): o4-mini, from the o-series, is designed to think longer than GPT-4/4o, while GPT-5 aims for further gains in reasoning capability. From Anthropic, we include two Claude models, Sonnet 4 (May 2025) [\[2\]](#page-12-7), and Sonnet 4.5 (September 2025) [\[3\]](#page-12-8); at release, Anthropic described Sonnet 4.5 as the "best coding model in the world" [\[3\]](#page-12-8).

### <span id="page-1-1"></span>3 VeruSAGE-Bench Setup and Study

### <span id="page-1-3"></span>3.1 VeruSAGE-Bench Construction

Our goal is to choose large-scale Verus-verified systems and turn each function with proof into a stand-alone task.

*Project selection.* We select the eight open-source Verusverified system projects shown in Table [2.](#page-2-0) Among these eight projects, five are the projects presented in the Verus paper [\[17\]](#page-12-2) (IronKV, Memory Allocator, Node Replication, NR Kernel, and Storage). Anvil [\[32\]](#page-13-5) uses Verus to prove not only safety properties but also liveness properties of Kubernetes controllers, and is done by authors mostly outside those of the Verus paper. Vest [\[6\]](#page-12-0) is a more recent project about a verified parser and serializer. Finally, Atmosphere [\[10\]](#page-12-1) is a verified operating system. It is the only project that had not yet been released to the public when we received the code from its authors and started our experiments. We do not use

<span id="page-2-0"></span>

| System           | Abbr. | System Description                  |
|------------------|-------|-------------------------------------|
| Anvil Lib        | AL    | Temporal-logic library              |
| Anvil Controller | AC    | A Kubernetes controller             |
| IronKV           | IR    | Sharded key-value store             |
| Memory Allocator | MA    | Mimalloc in Rust                    |
| Node Replication | NO    | Data-structure replication library  |
| NRKernel         | NR    | Operating Systems Page Table        |
| Atmosphere       | OS    | Operating Systems                   |
| Storage          |       | ST Persistent memory storage system |
| Vest             | VE    | Binary parser & serializer          |

Table 2: Open-source Verus verified Rust systems in our study.

the VeriSMo [\[49\]](#page-14-3) project, heavily featured in RagVerus [\[48\]](#page-14-2), because VeriSMo uses a fork of a very old version of Verus.

Together, these projects implement a wide range of systems, are developed by many different authors, and have all been featured in recent systems research papers [\[6,](#page-12-0) [10,](#page-12-1) [17,](#page-12-2) [19,](#page-13-1) [32\]](#page-13-5). They offer a great target for us to understand the systemverification capability of LLMs.

In most cases, every piece of verified code in a project is the target of our benchmark setup. Here are a few exceptions. First, Anvil is by far the largest Verus-verified system, consisting of multiple verified Kubernetes controllers. The Anvil authors suggest we focus on one recently verified controller, vreplicaset, which we refer to as Anvil Controller (AC) in VeruSAGE-Bench. In addition, Anvil has two lemma libraries that are leveraged by various controllers' verification, temporal\_logic and vstd\_ext. We cover them in our benchmark as Anvil Library (AL). For simplicity, for the remainder of this paper, we refer to AC and AL as *two different projects*, and we say VeruSAGE-Bench contains *9 projects*.

Second, on the advice of Verus experts, we skip functions involving a few specific Verus features: permissioned APIs for unsafe Rust datatypes, state\_machine and tokenized\_state\_machine macros. Each of these is extremely complex and rarely used, and we leave them to future study. Excluding proofs that involve these features only affects two projects: Memory Allocator (MA) and Node Replication (NO). Several projects (e.g., Anvil and NRkernel) implement state machines without using Verus state\_machine macros; they are still included in our study. *Benchmark extraction.* Once a Verus-verified system project is selected, our benchmark extraction goes through the following steps. First, we manually filter out *trivial* functions that do not require proof annotations. This can happen either because a function has a special tag that allows the verifier to skip it (e.g., axiom, external\_body), or because Verus can verify the proof without any annotations. Since Verus has evolved greatly in the past 2–3 years, many functions that contain human-written proof annotations in these projects have since become trivial, requiring us to filter them out.

Next, we extract each non-trivial function F, together with all its code dependencies, into a stand-alone verified Rust file F\_verified.rs. To accomplish this, we run Verus

<span id="page-2-1"></span>

|      |    | #Tasks | Spec | Proof | Other  | Total |      |  |
|------|----|--------|------|-------|--------|-------|------|--|
|      |    |        |      | Lemma | Target |       |      |  |
|      | AL | 104    | 28   | 10    | 9      | 37    | 84   |  |
|      | AC | 63     | 2037 | 39    | 69     | 1871  | 4016 |  |
|      | IR | 118    | 140  | 10    | 37     | 227   | 414  |  |
|      | MA | 89     | 32   | 6     | 10     | 33    | 81   |  |
|      | NO | 29     | 40   | 11    | 16     | 32    | 99   |  |
|      | NR | 204    | 675  | 25    | 31     | 459   | 1190 |  |
|      | OS | 157    | 730  | 40    | 33     | 499   | 1302 |  |
|      | ST | 63     | 246  | 20    | 13     | 259   | 538  |  |
|      | VE | 22     | 28   | 7     | 11     | 53    | 99   |  |
| Avg. |    | 496    | 23   | 27    | 401    | 947   |      |  |
|      |    |        |      |       |        |       |      |  |

Table 3: Average line-of-code statistics for VeruSAGE-Bench tasks. (The LoC of proof lemmas only counts signatures that remain in the benchmark, not the original proof bodies.)

with log-all mode, which enables Verus to log the abstract syntax trees (ASTs) of all the code structures that Verus uses to prove a target function. We then process that log file to produce a stand-alone Verus-verified Rust file.

Specifically, F\_verified.rs contains all the data structures, spec functions, and the signatures of all the proof/executable functions F depends on. We do not keep the body of all the dependent functions. If the proof in F calls a proof function F', the Verus log-all log for F only contains the signature of F', including its pre- and post-conditions, as that is all Verus needs to finish the proof. Consequently, in F\_verified.rs, we keep the signature of F', but replace its body with unimplemented!() and tag it with verifier::external\_body so that Verus will skip verifying it and its signatures can still be leveraged by its callers. Excluding the body of F' helps minimize the size of such stand-alone files; keeping the body would necessitate many more code dependencies. This strategy also prevents LLMs from copying the code or mimicking the style of dependent functions, thus mitigating plagiarism and aiding evaluation of the *true* inherent system-verification capability of LLMs.

Finally, we manually go through every F\_verified.rs file and remove all the proof annotations inside F, producing an F\_unverified.rs that will be used to evaluate LLMs. In general, if F is a proof function, its function body becomes empty; if F is an executable function, its function body becomes only the original Rust executable code. In all cases, we do not change the pre- and post-conditions of F.

#### <span id="page-2-2"></span>3.2 VeruSAGE-Bench Analysis

The F\_verified.rs files in VeruSAGE-Bench offer a good opportunity to understand what it takes for human experts to prove a function in a system project.

*The total size of proof tasks.* We measure the size of a *proof* as the lines of code of its F\_verified.rs file. As shown in Table [3,](#page-2-1) even with the body of most dependent functions removed, the total size of a system proof is still large, averaging almost 1000 lines of code. Even in a library project like AL, the average proof size is still over 80 lines of code, more than twice of that in VerusBench.

Different projects differ a lot in average proof size. §5.3 will show that LLM proof-development difficulty is negatively correlated with human-proof size.

*Very few loop invariants.* As highlighted in Table 1, system projects contain many fewer loops than small benchmark programs. Three projects (AC, NO, and NR) contain no loops in their code, and hence no loop invariants in their proofs. Two projects (AL and ST) contain only one loop. In contrast, only four of the 150 VerusBench proof tasks lack loops.

However, in terms of the complexity of loop invariants, the winner is VeruSAGE-Bench. The average lines of code of a loop-invariant block is 5.0 in VerusBench, and 14.6 in VeruSAGE-Bench. Only 4 loops in VerusBench are associated with more than 10 lines of loop invariants. In contrast, three loops in Atmosphere (OS) each contains more than 100 lines of loop invariants! Particularly, a function inside the kernel model contains a loop that iterates through all the virtual-address ranges, and is associated with 149 lines of loop invariants.

Specs are huge. As also highlighted in Table 1, every system proof contains much more specification than the ones in VerusBench. Anvil Controller (AC) particularly stands out, averaging 2037 lines and 235 functions of specification per task. For instance, often the specification includes an entire system state machine, to state the property that the state machine has a certain invariant. And even if we exclude AC from VeruSAGE-Bench, the remaining proof tasks still each contains an average of 37 functions and over 300 lines of specification.

Reading and understanding the entire specification is a challenge for proof development in system projects!

**Reliance on lemmas.** Developers often decompose a complicated proof task into smaller pieces, with each piece being a helper lemma — a proof function called to help the proof in another function F is a (helper) lemma with regard to F. That is why system proofs rely on helper lemmas much more than VerusBench proofs (2.4 versus 0.07 lemmas per task). In VeruSAGE-Bench, 43 proof tasks each use ten or more helper lemmas; in VerusBench, the largest number of helper lemmas used in a proof task is three.

In Table 3, we split the total lines of proof annotations in each task into two parts, those of helper lemmas and those in the target function. Since we have replaced the body of every lemma function with unimplemented! (), the size of lemma functions here is under-represented.

Different styles. The heat maps in Figure 2 demonstrate how different proof strategies/features are covered by different projects. We use a combination of keyword search and manual inspection to count features like high-level strategies (proof by induction, proof by contradiction), quantifier-related features (assert-forall, choose/exists), verifier modes (bit-vector prover,

non-linear prover, by-compute prover), and Verus standard library usage (vstd::arithmetic).

As we can see in Figure 2a and 2b, all the proof strategies/features are well represented in VeruSAGE-Bench, no matter in human-written proof or proof synthesized by Sonnet 4.5 LLM (we will explain how the proof is synthesized later). Popular features like assert forall, which is used to prove a universally-quantified fact, are widely used in almost all projects, while the usage of many other features varies greatly across projects. For example, the bit-vector prover is rarely used in most projects. But it is used in more than half of the proof tasks in the NRKernel (NR), because bit-operations are widely used in page table implementation.

For comparison, these proof strategies/features are rarely or never used in VerusBench, as shown in Figure 2c.

<span id="page-3-1"></span>![](_page_3_Figure_12.jpeg)

Figure 2: Fraction of proof tasks with certain features

#### 4 Agentic System Designs

In building/using agentic systems to support LLMs on proof tasks, we take two different approaches, which we call *hands-off* (§4.1) and *hands-on* (§4.2).

### <span id="page-3-0"></span>4.1 Hands-Off Approach

The hands-off approach uses a generic coding agent and a simple prompt listed below, which focuses on warning the LLM not to cheat, with little information about verification in general or Verus in particular. The LLM is merely given the option of (1) running Verus, (2) running a Verus cheat checker that reports whether a proof features cheating, and (3) inspecting the contents of a folder containing the Verus standard library (vstd).

The file X.rs cannot be verified by Verus, a verification tool for Rust programs, yet. Please add proof annotations to X.rs so that it can be successfully verified by Verus, and write the resulting code with proof into a new file, X\_verified.rs. Please invoke Verus to check the proof annotation you added. The vstd folder in the current directory is a copy of Verus' vstd definitions and helper lemmas; please feel free to check it when needed. You should KEEP editing your proof annotations until Verus shows there is no error. You should NOT change existing functions' preconditions or post-conditions; you should NOT change any executable Rust code; and you should NEVER use admit(...) or assume(...) in your code. You are also NOT allowed to create unimplemented, external-body lemma functions --- for any new lemma functions you add, you should provide complete proof. You are NOT allowed to create new axiom functions or change the pre/post conditions of existing axiom functions, and you should NEVER add external\_body tag to any existing non-external-body functions. I have installed Verus locally; you can just run Verus. Before you are done, MAKE SURE to run verus-checker X\_verified.rs to double check whether you have made any illegal changes to X. rs (fix those if you did).

*Setup* To run this hands-off approach, we use GitHub Copilot Command-Line Interface (CLI) [\[12\]](#page-12-9) for all the models that it supports (GPT-5, Sonnet 4, Sonnet 4.5), and OpenAI Codex CLI [\[27\]](#page-13-8) for o4-mini. We use Copilot's allow-all-tools and Codex's all-auto option, so that the agent can run Verus or any command-line tools without prompting human users for confirmation. In the remainder of the paper, we refer to all these agent systems as *hands-off* and/or as *CLI agents*.

To make sure that the LLM does not find "answers" somewhere in the file system, we run all experiments in containers. When we evaluate tasks from a project P, we ensure that no proof bodies from P exist in that container. Each run of a CLI agent produces two files: its standard output log and the verified file. As we will see later in Figure [5,](#page-6-0) the CLI log is very informative, indicating which files the agent reads, what commands, including Verus, it executes, etc.

### <span id="page-4-0"></span>4.2 Hands-On Approach

A hands-on approach, in contrast, prompts the LLM with detailed and comprehensive domain knowledge about Verus syntax, verification-error debugging strategies, and various other support. It also guides and enforces a proof development methodology, rather than relying on the LLM to drive the development process through self-driven tool invocations.

We do not use the state-of-the-art hands-on approach AutoVerus [\[40\]](#page-13-4) directly, as it performs poorly on system tasks. As shown in Table [4,](#page-4-1) it has only 20% success rate on VeruSAGE-Bench, matching the findings in RagVerus [\[48\]](#page-14-2).

To improve AutoVerus for system tasks, we did a deep dive on two projects, Memory Allocator (MA) and Storage (ST). We interviewed their authors and examined their human-written proof to learn how human experts developed

<span id="page-4-2"></span>![](_page_4_Figure_8.jpeg)

Figure 3: Architecture of VeruSAGE

<span id="page-4-1"></span>

| AL  | AC | IR  | MA  | NO  | NR  | OS  | ST  | VE  | Tot. |
|-----|----|-----|-----|-----|-----|-----|-----|-----|------|
| 30% | 6% | 24% | 32% | 34% | 15% | 13% | 19% | 23% | 20%  |

Table 4: Success rate of AutoVerus on VeruSAGE-Bench

the proofs therein and what parts of this methodology are missing from the AutoVerus agent system. This understanding then led to the following design of VeruSAGE. (Note that the design of VeruSAGE is not influenced by the benchmark study presented in [§3.2.](#page-2-2) MA and ST were the first two system projects that we looked into and extracted proof tasks from; most studies and benchmark extraction presented in [§3.2](#page-2-2) were conducted after the design of VeruSAGE.)

As illustrated in Figure [3,](#page-4-2) for every task, the proofdevelopment of VeruSAGE goes through *steps*. Each step starts with Verus reporting verification errors, if any, of the Rust program with the most up-to-date proof candidate; the candidate selector then decides whether to take this proof candidate or revert to an earlier one; then, the planning agent examines the errors and the context history to select an action agent, which then proposes an updated proof candidate. VeruSAGE differs from AutoVerus with (1) many more action agents; (2) a two-phase plan-then-act LLM procedure; (3) more sophisticated candidate selector; and (4) more context management.

*What action agents are missing in AutoVerus?* AutoVerus contains a network of action agents, each designed to refine loop invariants in a particular way or to fix one type of verification errors, such as pre-/post-condition errors and loop-invariant errors. However, our analysis reveals that AutoVerus' error-driven agents lack the knowledge about high-level proof strategies (e.g., divide-and-conquer, induction), specialized solvers (e.g., bit-vector solver, nonlinear solvers), and other verification techniques beyond those for loops. To support this, VeruSAGE is equipped with many more action agents, including: *Logical Reasoning* agents (e.g., case-analysis, induction), *Arithmetic & Solvers* agents (e.g., nonlinear-arithmetic, bit-vector, integer-ring), *Proof Context* agents (e.g., reveal-opaque, use-lemma), *Quantifier* agents (e.g., instantiate-forall, instantiate-exists), etc.

*Why do LLMs need to plan before act?* AutoVerus does not have a planning phase, as it simply dispatches an action agent based on the verification error type. In more complicated proof tasks, one type of error might be fixed by different strategies/techniques. For example, VeruSAGE has 16 specialized action agents to help fix assertion errors. One needs to analyze the code context and failure history to select the most promising strategy or technique, rather than blindly trying one. To support this, VeruSAGE has a dedicated planning agent that is equipped with the high-level description of every action agent, as well as a when-to-use-what tutorial.

Furthermore, to help the planning agent, VeruSAGE performs a static analysis of the codebase before invoking the planning agent to identify available resources such as lemmas, recursive functions, and opaque functions. Based on this analysis, VeruSAGE filters the available actions to exclude those that are not applicable (e.g., disabling use-lemma if no lemmas are present in the task file) and prioritize relevant ones (e.g., boosting agents that are good at handling recursion if recursive functions are detected). This reduces the search space and guides the model towards more promising actions. *When do we accept a proof candidate?* Before the proof is finalized, many versions of intermediate proof, referred to as *proof candidates*, are usually proposed and judged by the verifier as incorrect. It is important to identify which proof candidates have made useful progress and accept them for further exploration. In simple tasks, this can be easily decided by identifying the proof candidate with the fewest verification errors — this is the strategy of AutoVerus. Unfortunately, this strategy does not work for complicated proof tasks. For example, converting one difficult-to-prove property into multiple easier properties would temporarily increase the number of errors but is often the right way to move forward.

VeruSAGE proposes more types of acceptance criteria and uses different criteria for different actions. For example, its case-analysis action implements the divide-andconquer strategy by splitting a proof into multiple branches. VeruSAGE applies an acceptance criterion that allows the number of verification errors to increase as long as the original assertion error targeted by this action is resolved and no errors are introduced outside the split block. In contrast, for actions like nonlinear-arithmetic, which invokes a specialized solver to prove a specific arithmetic property, we enforce a stricter criterion: a candidate is accepted only if it strictly reduces the total number of verification errors.

*Context management.* VeruSAGE aims to provide sufficient context information to the LLM planning agent in several ways. (1) *Comprehensive History Tracking*: VeruSAGE maintains a log of past proof attempts, recording what action agent was used, what is the synthesized code diff, and what is the outcome — whether the proof candidate was accepted, what are the verification errors, etc. This log is included in the prompt for subsequent invocations of the planning agent, allowing the agent to learn from past mistakes and refine its overall strategy. (2) *Concise Code Context*: Not to overwhelm the model with the entire codebase, we provide a focused view containing only the relevant code surrounding

<span id="page-5-2"></span>

| Project | # Tasks |     |     |     | o4-mini GPT-5 Sonnet 4 Sonnet 4.5 |
|---------|---------|-----|-----|-----|-----------------------------------|
| AL      | 104     | 48% | 79% | 86% | 100%                              |
| AC      | 63      | 19% | 32% | 24% | 37%                               |
| IR      | 118     | 35% | 44% | 69% | 84%                               |
| MA      | 89      | 62% | 72% | 75% | 90%                               |
| NO      | 29      | 72% | 83% | 86% | 100%                              |
| NR      | 204     | 30% | 48% | 55% | 74%                               |
| OS      | 157     | 37% | 45% | 62% | 83%                               |
| ST      | 63      | 49% | 62% | 70% | 78%                               |
| VE      | 22      | 68% | 73% | 82% | 100%                              |
| All     | 849     | 41% | 55% | 64% | 81%                               |

Table 5: % of VeruSAGE-Bench tasks correctly proved by each model from each project (each model under its best agent setting)

the failure and the specific error message. Furthermore, to minimize token usage and focus the model on the specific changes, we instruct action agents to output proof candidates as concise code diffs (specifically, search-and-replace blocks) rather than rewriting entire files. Crucially, this context is *dynamic*: the history evolves, allowing the planning to adapt its strategy in real-time and avoid repeating past mistakes.

*Setup.* We implemented VeruSAGE by adding about 15,600 lines of Python code into AutoVerus for the design changes mentioned above. VeruSAGE uses Azure OpenAI APIs to access OpenAI and Claude models directly.

To ensure a controlled evaluation, we enforce a stopping criterion: VeruSAGE terminates only when (1) the code is successfully verified by Verus, (2) the total execution time exceeds 20 minutes, or (3) 20 proof steps have been conducted. This policy ensures the agent has sufficient opportunity to explore complex strategies but does not run indefinitely.

### <span id="page-5-0"></span>5 Experimental Results

In this section, we answer these key experimental questions:

- How often do LLMs succeed on system tasks? ([§5.1\)](#page-5-1)
- Can LLMs help with tasks that human experts have not yet finished? ([§5.2\)](#page-6-1)
- When and how do LLMs succeed? ([§5.3\)](#page-7-0)
- When and why do LLMs fail? ([§5.4\)](#page-7-1)
- How much time and money does it take to have LLMs complete verification tasks? ([§5.5\)](#page-8-0)
- How do results change with alternative settings? ([§5.6\)](#page-9-0)
- Miscellaneous questions in [§5.7.](#page-9-1)

#### <span id="page-5-1"></span>5.1 How often do LLMs succeed on VeruSAGE-Bench?

The detailed results about every model's success rate for tasks in every project under Hands-Off mode and Hands-On mode are shown later (Tables [6](#page-10-0) and [7\)](#page-10-1). Not to overwhelm the readers with all the detailed numbers, Table [5](#page-5-2) offers an overview of each model's proof success rate under its best agent-system setting (i.e., Hands-On for o4-mini and GPT-5; Hands-Off for Sonnet 4 and Sonnet 4.5).

*Sonnet 4.5 is great at system verification!* The most surprising result to us is that the best model-agent combination, Sonnet 4.5 + Hands-Off, successfully proved 81% of the 849 proof tasks without any help from human beings! This is a huge improvement and contrast from previous results about LLM-for-system-proof.

As we can see in Table [5,](#page-5-2) Sonnet 4.5 offers the highest success rate among all models for proof tasks extracted from every project, reaching 100% for three projects: Anvil Library (AL), Node Replication (NR), and Vest (VE).

Keep in mind that Sonnet 4.5 did well not because it has memorized the human proof from its training data. In proof tasks that we sampled from every project, the LLM proof is different from the human proof. Furthermore, as mentioned in [§3.1,](#page-1-3) the whole Atmosphere (OS) codebase was not released online until we reached out to the developers in November 2025, way after the release date of all the models. And yet, Sonnet 4.5 still reached an 83% success rate for Atmosphere. *Even o4-mini can write system proofs, by VeruSAGE.* The 41% success rate for o4-mini with VeruSAGE more than doubles that of the previous hands-on agent system AutoVerus (20% success rate) and that of the hands-off agent Codex (17% success rate). Although VeruSAGE's design was based on our study of MA and ST, the average success rate of o4-mini under VeruSAGE has outperformed that under AutoVerus and Codex for *every* project. However, agent systems alone cannot fully overcome the inherent difference between models: even with the heavy hands-on help, o4-mini still failed many more tasks than the two Sonnet models.

*Different projects offer consistent and different challenges.* The difficulty levels of different projects seem consistent across models. Anvil Controller (AC) is the most difficult for all models, with fewer than 40% of its proof tasks proved by any model. Projects NO and VE seem the easiest, producing top-three proof-success rates for all four models. The success-rate ranking of different models is also consistent across projects. In all but one project, the ranking remains Sonnet 4.5, Sonnet 4, GPT-5, and finally o4-mini.

#### <span id="page-6-1"></span>5.2 Can LLMs help tasks not yet finished by humans?

We next evaluate whether the best agent-LLM combination (Hands-Off Sonnet 4.5) can help with proof tasks human experts have not yet finished. The Atmosphere (OS) project offers us this opportunity: being a very recent system project, a small part of it is still under proof development.

We first consider Atmosphere's lemma\_u.rs file. Among the 13 lemmas, 10 have not yet been proved. After 12 minutes and at a cost of \$11 (USD), Sonnet 4.5 produces a fully verified file. Notably, Sonnet 4.5 points out five lemmas whose specification requires adjustment, with all five confirmed by human experts. Figure [4](#page-6-2) shows one such adjustment. The original specification of seq\_skip\_lemma states that for any non-empty sequence s, once its first element s[0] is skipped, the remaining sequence contains no

```
pub proof fn seq_skip_lemma<A>()
  ensures
    forall|s: Seq<A>| s.len() > 0
+ && s.no_duplicates()
     ==> !s.skip(1).contains(s[0]),
```

Figure 4: A specification adjustment suggested by an LLM

```
• Wait, let me reconsider. Looking at the post-
condition again - actually it might be wrong. Let me
check the original file to see if this postcondition
is needed elsewhere. ...
• I see - the postcondition says 's.len() > 0 ==> !s.
skip(1).contains(s[0])'. This can't be true in general
! If s = [1, 1], then s.skip(1) = [1] which contains s
[0] = 1. Let me think... Maybe this postcondition
needs no_duplicates too? Or maybe I'm misunderstanding
 skip(1). Let me check the implementation of skip more
 carefully and test:
✓ Check skip definition
   $ cd /xxx/verified && grep -A3 "fn skip" vstd/seq.
   rs | head -10
• So skip(1) = subrange(1, len) which is the tail of
the sequence. Now I see-this DOES need no_duplicates!
```

Figure 5: The monologue of Sonnet 4.5 for seq\_skip\_lemma.

element whose value equals that of the original s[0]. As the log indicates (Figure [5\)](#page-6-0), after multiple proof attempts rejected by Verus, Sonnet 4.5 starts to doubt the correctness of this specification. After some investigation, it proposes the correct adjustment; see Figure [4.](#page-6-2) (Note that OS is not the only project where we see LLMs propose useful specification adjustments. We have seen another example in ST, and the developers have accepted the resulting usability-improving suggestion [\[22\]](#page-13-9).)

In other parts of the project, we find 25 functions in various files that have specifications but incomplete proofs. Eight of these functions have comments indicating the proof will be developed later. The remaining 17 each contain a large amount of proof material, but the proof is incomplete because it includes one or two instances of assume. In Verus, using assume(P) is common practice in proof development; it indicates that property P is not yet verified but allows it to be used (i.e., assumed) in the remainder of the proof. We extract these 25 functions as 25 tasks, just as we do for VeruSAGE-Bench. Sonnet 4.5 generates complete proofs for 23 of them, taking on average 13.5 minutes and \$8.45.

Importantly, we have found human experts and Sonnet 4.5 to be effective *collaborators*! For this, we consider the 17 functions that each contain an incomplete proof developed by human experts. Sonnet 4.5 can prove 16 of these when provided with the partial human proofs, but can prove only six when starting from an empty proof. Even for those six tasks, starting from human experts' partial proofs allows Sonnet 4.5 to reduce its average proof development time from 7.3 minutes to 4.7 minutes.

<span id="page-7-2"></span>![](_page_7_Figure_0.jpeg)

Figure 6: The success rate among tasks with different sizes

#### <span id="page-7-0"></span>5.3 When do LLMs succeed and how?

What correlates with LLMs' success? We hypothesize that the success of LLMs could be correlated with the size of a proof task, the lines of code of F\_unverified.rs. After all, usually a larger task involves more complicated code with more specifications. We calculate the Point-Biserial Correlation Coefficient [36] to test this hypothesis. For all models, o4-mini (Hands-on), GPT-5 (Hands-On), Sonnet 4 and Sonnet 4.5 (Hands-Off), the correlation coefficients are negative values (ranges from -0.28 to -0.50), indicating a correlation between smaller task size and task success; each P-value (which indicates, if no correlation exists, the probability of observing one of this magnitude) is small (the largest is 2.98e-16), indicating high statistical significance of the correlation. This trend can also be seen visually in Figure 6, which shows the success rate among tasks within certain size bucket.

*How do LLM and human proofs differ?* We focus the comparison on proofs developed by Hands-Off Sonnet 4.5.

Strategy difference. As shown in the heatmaps of Figure 2 in § 3.2, human proof and LLM proof use similar but not exactly the same features and strategies. For example, the LLM uses proof by contradiction more, the non-linear prover less, and vstd::arithmetic more. Interestingly, the latter two differences seem to explain each other. Taking project MA as an example, among the 11 tasks that developers use the non-linear prover and yet Sonnet 4.5 does not, Sonnet 4.5 fails 4 tasks and leverages vstd::arithmetic (helper lemmas in Verus's standard arithmetic library) to prove the others. This seems to indicate that Sonnet 4.5 has a weakness in conducting non-linear arithmetic proof by itself. On the positive side, supported by GitHub Copilot CLI, Sonnet 4.5 is very good at searching and identifying relevant helper lemmas, which could be a valuable asset for human proof developers.

<u>Proof length difference.</u> This difference is huge. Across the 688 tasks where Sonnet 4.5 (Hands-Off) succeeds, the lines of proof added by human experts have a median (average) size of 9 (17.3). In contrast, the median (average) lines of proof added by Sonnet 4.5 are 24 (44.2). This trend persists across all projects. Very rarely, the human proof is longer

```
assert forall|s: Seq<A>, v: A|
    s.len() > 0 && s[0] != v implies
    s.skip(1).contains(v) == s.contains(v) by {
    broadcast use vstd::seg lib::lemma seg skip contains
    if s.skip(1).contains(v) {
      assert(exists|i: int| 1 <= i < s.len()
                   && s[i] == v);
       assert(s.contains(v));
10
    if s.contains(v) {
      let i = choose|i: int| 0 <= i < s.len()</pre>
12
                   && s[i] == v;
      if i == 0 {
13
         assert(s[0] == v);
14
15
         assert(false); // a contradiction
16
      } else {
         assert(1 <= i < s.len() && s[i] == v);
         assert(s.skip(1).contains(v));
18
19
    }
20
21 }
```

Figure 7: In this proof written by Sonnet 4.5 for a lemma function in Atmosphere (OS), the gray lines are unnecessary.

than the LLM proof, which typically happens when the LLM finds a vstd lemma to replace many lines of human proof.

Figure 7 shows a concrete example. Here, Sonnet 4.5 successfully proves the property stated in the assert (lines 1–3) using 17 lines of proof annotations (lines 4–20). However, except for the call to the Verus standard library lemma lemma\_seq\_skip\_contains on line 4, all other proof annotations are correct but unnecessary. That is, Verus verification would succeed even without lines 5–20.

In Verus, proof annotations are needed only when the target property cannot be automatically proved by the underlying theorem prover. LLMs tend to write long proofs maybe because they do not fully understand what can(not) be proved by theorem provers. Such chatty proofs can be automatically shrunk by repeatedly running Verus on subsets of the proof. However, since chattiness has a negative impact on the LLM token cost, it is a good target for future improvement.

#### <span id="page-7-1"></span>5.4 When do LLMs fail?

Why does Sonnet 4.5 fail? The projects for which Sonnet 4.5 (Hands-Off) has its highest failure rates are AC, ST, and NR. Some of these failures are random: when we re-run the experiment, Sonnet succeeds in about 10% of the initial failure cases. Here, we do a deep dive on the remaining cases to understand the limits of Sonnet 4.5.

We find that often, when Sonnet fails to complete an Anvil Controller (AC) proof, the corresponding human-written proof uses an inductive invariant. That is, it establishes that a state machine has a certain invariant by stating a stronger invariant and proving that the stronger one is inductive. Automatically finding an inductive invariant is an area of active research [24, 44, 45, 47]. Unfortunately, this capability seems still out of the reach of Sonnet.

We find that often, when Sonnet fails to complete a storage (ST) proof, the corresponding human-written proof lever-

<span id="page-8-1"></span>![](_page_8_Figure_0.jpeg)

Figure 8: Tradeoff among different models and agent systems

ages knowledge of code synthesized by a procedural macro. Specifically, the ST project has a procedural macro for synthesizing functions describing the size and alignment of data structures using # [repr(C)]. Although Sonnet is given access to the directory containing the macro's definition, it seemingly cannot use that access to expand the macro and learn the resulting function definitions. So, it fails.

The NRKernel (NR) project is large and complex enough that the authors employ a considerable amount of abstraction to help manage the complexity of the proof. In particular, they define abstract definitions using closed spec functions (ones whose declarations are visible but whose bodies are hidden from other modules) and lemmas about the properties of those spec functions, rather than just making all the definitions in the spec function bodies directly visible to all modules. In this case, the proof in another module must rely on those lemmas to supply the necessary information about the hidden definitions. We find that Sonnet fails many tasks because it fails to understand and deal with this abstraction in a large project. It tends to insist on seeing the hidden definitions and to claim that the proof cannot be finished without them, failing to see that the available lemmas can be used to complete the proof. Admittedly, this is hard even for humans.

Why does o4-mini fail so often? For o4-mini, we see broad struggles with the syntax of both Rust and Verus, and more hallucinations about which lemma functions actually exist. In the Hands-On mode, the proof candidates synthesized by o4-mini often contain syntax errors according to Rust/Verus compilers (7.8 times per task on average). Common syntax errors include "unexpected token" (reported in 21% tasks), "cannot find value/function" (33% task), and "unresolved import" (8% of tasks). In comparison, for only 10% of tasks did Sonnet 4.5, also Hands-On, ever generated a proof candidate that contains either one of such syntax errors.

<span id="page-8-2"></span>![](_page_8_Figure_5.jpeg)

Figure 9: % of tasks accomplished within a certain time (min)

#### <span id="page-8-0"></span>5.5 How much time and money do LLMs spend?

Money cost. The money cost here is determined by the total input/output tokens consumed by the model and different models' token pricing. As shown in Figure 8 (upper half), the Hands-On approach (circles) costs less than the Hands-Off approach (dashed boxes), mainly because VeruSAGE is strict about what the model should do at each step with focused prompts and concise output format. This leaves little room for random chat, which is common for Sonnet 4 and 4.5 in Hands-Off mode. For both Hands-On and Hands-Off, o4-mini (red in figure) and GPT-5 (yellow in figure) cost less, mainly due to their competitive pricing. At the time of our experiments, the cost per 1 million input (output) tokens is \$1.25 (\$10) for GPT-5 and \$1.1 (\$4.4) for o4-mini, compared to \$3 (\$15) for the Sonnet models.

*Time cost* is affected by two factors: how quickly one succeeds and how quickly one gives up on a task. Considering only successes, Sonnet 4.5 is the fastest. As shown in Figure 9, Sonnet 4.5 (Hands-On) proves 40% of tasks in under 2 minutes each, and Sonnet 4.5 (Hands-Off) proves 60% of tasks in under 6 minutes each, faster than any other settings.

Speed of giving up, on the other hand, depends on both agent setting and model. The Hands-On setting (VeruSAGE) forces the model to try at least 20 steps or 20 minutes, preventing giving up early. In contrast, the Hands-Off setting has no guideline, let alone enforcement, of when the model should give up, leaving this decision to the model. In the latter case, o4-mini and GPT-5 give up *much* more easily than Sonnet models. Take the most difficult project AC as an example. As shown in Table 6, Sonnet 4.5 runs Verus 13.6 times per AC task, proposing various proof candidates, and spends on average 12.5 minutes on each task. In contrast, o4-mini runs Verus least frequently in AC among all projects (2.6 times per task) and *finishes* (i.e., gives up on) each task in less than 3 minutes. GPT-5 behaves similarly to o4-mini.

With these two factors, as shown in the bottom half of Figure [8,](#page-8-1) the Hands-On mode of o4-mini and GPT-5 are the slowest, averaging more than 12 minutes per task, as they are slow in producing correct proofs and cannot give up easily. The Hands-Off mode of o4-mini and GPT-5 are the fastest, averaging less than 4 minutes per task, as they give up quickly. The two Sonnet models, no matter Hands-On or Hands-Off, stay in the middle. Note that, in Hands-Off mode, Sonnet 4.5 is the fastest for projects that it deems easy (i.e., 100% success rate), namely AL, NO, and VE, as shown in Table [6.](#page-10-0)

*Which setting should one use?* The Hands-Off mode of Sonnet 4.5 has a clear advantage for success rate. Its response time is also acceptable—a recent user study shows that it often takes human experts more than 10 minutes to develop Verus proof for a benchmark-style proof task [\[15\]](#page-12-10). If money cost is an issue, the Hands-On modes of Sonnet 4.5, o4-mini and GPT-5 are good choices.

### <span id="page-9-0"></span>5.6 What about alternative settings?

*The Hands-on approach does not suit everybody!* It came as a surprise to us that VeruSAGE did not help every model. The x-axis of Figure [8](#page-8-1) shows a visual comparison of success rates: the hands-on approach (circles) helped o4-mini a lot and GPT-5 somewhat, but became detrimental for Sonnet models, compared with the hands-off approach (lighter squares).

One indication that o4-mini and GPT-5 need hands-on support is how often their Hands-Off mode's *final* proof contains syntax errors. This error rate is 38% for o4-mini and 16% for GPT-5, and is only 1.3% for Sonnet 4 and 0.9% for Sonnet 4.5. It is not a surprise that o4-mini and GPT-5 benefit from the Hands-On approach, which contains a detailed "tutorial" about Verus and dedicated syntax-repair agents.

We suspect a key reason the hands-on approach is detrimental for Sonnet is that VeruSAGE forces the model to develop proof at small steps, working on one verification error with one action agent at a time. This strategy can slow down a capable model. For example, in segment\_start\_mult\_commit\_size from MA, when Sonnet 4.5 finally found the correct proof after 10 VeruSAGE steps, it was already over the 20-minute cut-off and hence was counted as a failure. In contrast, the Hands-Off mode allows Sonnet 4.5 to try big changes quickly — the first proof candidate proposed by Sonnet 4.5 added 53 lines to the 52-line input file; within 3 tries and 2.5 minutes, it was all done.

Occasionally, the hard-coded policies in VeruSAGE could make worse choices than the Sonnet models could on their own, causing some tasks to fail in Hands-On mode but succeed in Hands-Off. For example, the proof-candidate selection algorithm cannot always be optimal, as the potential of an incomplete proof candidate cannot always be measured by quantitative metrics. Similarly, the static-analysis based cheat checker in VeruSAGE can produce false positives, causing correct or promising proof to be rejected.

*Even Hands-Off LLMs still benefit from tool support!* First, LLMs need the feedback of Verus. As shown in Table [6,](#page-10-0) even in the Hands-Off mode, LLMs still repeatedly invoke Verus. Across different models, GPT-5 uses Verus the least often, but still averages 6.4 Verus runs per task. Although every model runs Verus to see if its proof is correct, Sonnet 4.5 starts every proof development by running Verus on the input task file, while GPT-5 often starts writing proof without knowing what errors Verus reports on the input file. Sonnet 4.5 takes at least two runs of Verus in a successful task, which happens to only 21 tasks — 3% of all the tasks it succeeded. Once, Sonnet 4.5 ran Verus 50 times before it succeeded! In contrast, although it succeeded in fewer than two-thirds of what Sonnet 4.5 did, GPT-5 proved 111 tasks with just one run of Verus.

Second, the cheat checker has helped LLMs reduce their cheat rate. Without the cheat checker, Sonnet 4 has cheated in 14% of the proof tasks! Sonnet 4.5 and GPT-5 are more honest, but still cheated in 7% and 2% of tasks, respectively. The way models cheat includes (1) using assume() or admit() to assume a specific property being verified without actual proof, (2) using external\_body and axiom tags to assume a whole function being verified without proof, (3) changing the function pre- and/or post-conditions to make the proof easier, etc. Once we suggest LLMs to use the cheat checker in our prompt, the cheat rate decreases to less than 1.5% for all models. The cheat rate did not drop to 0, as when the LLMs really cannot figure out the proof, they tend to use assume(), admit(), or axiom functions to represent their partial proof.

Finally, we ran a full ablation study of the Hands-Off mode without providing LLMs with Verus standard library (vstd) and cheat-checker. The results show that vstd plus cheat checker has allowed GPT-5, Sonnet 4, and Sonnet 4.5 to prove 26%, 24%, and 9% more VeruSAGE-Bench tasks than not using them. We have observed that the models search the vstd library to not only identify relevant helper lemmas, but also to learn Verus syntax. Of course, the use of vstd and cheat-checker also increased the average time per task by 53% for GPT-5, 21% for Sonnet 4, and only 0.4% for Sonnet 4.5. We observed that vstd and cheat-checker have often helped GPT-5 and Sonnet 4 to work harder and not give up early, and have often helped Sonnet 4.5 to find the correct proof faster.

#### <span id="page-9-1"></span>5.7 More detailed investigations (What if?)

Given the resource constraints, we conducted case studies for the following questions.

*What if we remove all the helper lemmas?* We sampled two projects, Vest (VE) and Storage (ST), to evaluate whether Sonnet 4.5 (Hands-Off) can still prove some of the proof tasks when it is not provided with the helper lemmas used by human experts to prove those tasks. There are 4 and 30 tasks in VE and ST, respectively, that were proved by human experts using helper lemmas. In the default, with-lemma, setting, Sonnet 4.5 proved all 4 in VE and 18 in ST. Without helper lemmas in the input file, Sonnet 4.5 still proved the 4

<span id="page-10-0"></span>

|         |         | % Successful Tasks | Time per Task (min) |      |         |       | Cost per Task (\$) |      |         |       | # Verus Runs per Task |       |         |       |      |      |
|---------|---------|--------------------|---------------------|------|---------|-------|--------------------|------|---------|-------|-----------------------|-------|---------|-------|------|------|
| Project | o4-mini | GPT-5              | S4                  | S4.5 | o4-mini | GPT-5 | S4                 | S4.5 | o4-mini | GPT-5 | S4                    | S4.5  | o4-mini | GPT-5 | S4   | S4.5 |
| AL      | 25%     | 77%                | 86%                 | 100% | 3.8     | 3.3   | 3.9                | 3.1  | 1.00    | 0.81  | 2.57                  | 1.86  | 10.4    | 6.6   | 9.0  | 7.0  |
| AC      | 11%     | 16%                | 24%                 | 37%  | 2.1     | 2.7   | 14.5               | 12.5 | 0.57    | 1.96  | 15.80                 | 12.31 | 2.6     | 4.8   | 17.0 | 13.6 |
| IR      | 25%     | 62%                | 69%                 | 84%  | 4.3     | 3.9   | 7.4                | 6.7  | 0.91    | 1.09  | 5.10                  | 4.56  | 10.7    | 6.3   | 10.3 | 9.5  |
| MA      | 15%     | 60%                | 75%                 | 90%  | 4.9     | 3.2   | 8.3                | 5.2  | 0.85    | 1.14  | 6.00                  | 3.81  | 9.8     | 8.2   | 11.6 | 9.6  |
| NO      | 48%     | 93%                | 86%                 | 100% | 3.9     | 2.6   | 4.5                | 2.0  | 1.17    | 0.46  | 2.18                  | 0.85  | 11.3    | 4.5   | 7.6  | 4.9  |
| NR      | 14%     | 39%                | 55%                 | 74%  | 2.9     | 3.7   | 12.3               | 8.9  | 0.78    | 1.48  | 4.50                  | 6.35  | 6.2     | 5.9   | 11.2 | 11.0 |
| OS      | 9%      | 43%                | 62%                 | 83%  | 2.4     | 3.8   | 9.9                | 8.3  | 0.66    | 1.33  | 6.79                  | 7.15  | 6.0     | 5.6   | 9.6  | 12.8 |
| ST      | 9.5%    | 33%                | 70%                 | 78%  | 2.0     | 4.9   | 9.1                | 7.4  | 0.42    | 1.57  | 5.90                  | 5.84  | 2.1     | 8.0   | 10.5 | 9.9  |
| VE      | 27%     | 64%                | 82%                 | 100% | 4.3     | 5.7   | 5.2                | 2.4  | 1.32    | 1.51  | 4.00                  | 1.50  | 13.3    | 10.0  | 10.9 | 7.1  |
| Avg     | 17%     | 50%                | 64%                 | 81%  | 3.3     | 3.7   | 9.2                | 7.2  | 0.81    | 1.30  | 6.65                  | 5.61  | 7.4     | 6.4   | 10.9 | 10.4 |

Table 6: Detailed results for every model (hands-off). Best and worst results are highlighted; bold indicates better than Table [7](#page-10-1) best.

<span id="page-10-1"></span>

|         |         | % Successful Tasks |      |      |         | Time per Task (min) | Cost per Task (\$) |      |         |       | # Verus Runs per Task |      |         |       |      |      |
|---------|---------|--------------------|------|------|---------|---------------------|--------------------|------|---------|-------|-----------------------|------|---------|-------|------|------|
| Project | o4-mini | GPT-5              | S4   | S4.5 | o4-mini | GPT-5               | S4                 | S4.5 | o4-mini | GPT-5 | S4                    | S4.5 | o4-mini | GPT-5 | S4   | S4.5 |
| AL      | 48%     | 79%                | 69%  | 83%  | 12.4    | 8.7                 | 6.7                | 4.6  | 0.45    | 0.31  | 0.60                  | 0.51 | 32.9    | 10.0  | 25.4 | 20.3 |
| AC      | 19%     | 32%                | 21%  | 37%  | 16.9    | 16.5                | 14.6               | 13.1 | 1.35    | 0.86  | 6.09                  | 5.20 | 36.8    | 13.3  | 31.6 | 25.5 |
| IR      | 35%     | 44%                | 53%  | 67%  | 13.8    | 14.1                | 7.5                | 7.1  | 0.54    | 0.48  | 1.03                  | 0.92 | 45.7    | 17.0  | 35.3 | 28.5 |
| MA      | 62%     | 72%                | 75%  | 84%  | 9.9     | 10.2                | 4.4                | 3.9  | 0.37    | 0.35  | 0.53                  | 0.40 | 30.9    | 13.2  | 26.5 | 20.3 |
| NO      | 72%     | 83%                | 100% | 97%  | 9.2     | 7.6                 | 1.2                | 1.6  | 0.29    | 0.25  | 0.19                  | 0.18 | 31.0    | 9.4   | 25.1 | 19.4 |
| NR      | 30%     | 48%                | 56%  | 60%  | 14.0    | 13.2                | 7.8                | 8.2  | 0.79    | 0.60  | 2.01                  | 1.84 | 41.0    | 13.4  | 32.3 | 26.3 |
| OS      | 37%     | 45%                | 54%  | 62%  | 12.7    | 14.6                | 7.0                | 7.7  | 0.81    | 0.62  | 2.10                  | 1.69 | 36.1    | 14.4  | 30.6 | 24.3 |
| ST      | 49%     | 62%                | 54%  | 71%  | 11.2    | 12.7                | 5.4                | 5.9  | 0.53    | 0.51  | 1.31                  | 1.03 | 31.6    | 13.0  | 29.6 | 23.4 |
| VE      | 68%     | 73%                | 64%  | 77%  | 9.0     | 11.7                | 3.8                | 4.5  | 0.38    | 0.48  | 0.65                  | 0.58 | 46.1    | 20.5  | 34.2 | 25.8 |
| Avg     | 41%     | 55%                | 58%  | 67%  | 12.8    | 12.7                | 7.1                | 6.9  | 0.67    | 0.52  | 1.72                  | 1.47 | 37.7    | 13.7  | 30.3 | 24.1 |

Table 7: Detailed results for every model (hands-on). Best and worst results are highlighted; bold indicates better than Table [6](#page-10-0) best.

out of 4 in VE, with slightly more time (3.4 vs. 3.2 minutes), and 16 out of 30 tasks in ST. These case studies indicate that LLMs remain capable even without helper lemmas.

*Can LLMs work directly in a multi-file project instead of on an extracted task file?* Throughout this study, we always extract a proof task from a multi-file project into one standalone file and let LLMs work on this single file. We did a case study to see if LLMs can directly work in a multi-file project, without the extraction. The results showed that at this point, extracting dependencies into one file is still the preferred way.

We first tried three tasks in IronKV, each with multi-file dependencies. We removed all the proof in the local file, so that there is no easy target for LLM to copy from. Then, when we asked the LLM to prove these tasks, we simply provided the LLM with the path to the IronKV folder and the script to verify the whole project. Sonnet 4.5 (Hands-Off) managed to prove all three tasks in this whole-project setting, taking 1.6X as long and 2.2X as much money as the single-file setting. We then tried a more complicated project, Atmosphere, which contains 10 folders and more than 150 Rust files in its verified component. We randomly picked two tasks that Sonnet 4.5 succeeded in its default single-file setting. In the whole-project setting, the first task got verified, but the proof attempt for the second task add\_mapping\_4k kept going and was killed by Github Copilot CLI after 1 hour

due to exceeding the Copilot token usage limit. This failed attempt cost more than 40 dollars (> 13.8 million tokens)!

*Can different models collaborate?* One way of collaboration is to "union" the proof attempt of every model: if one model succeeds on a task, we declare success. Unfortunately, doing so does not improve the overall VeruSAGE-Bench success rate much: the Hands-Off mode has a union success rate of 82.3%, only 1.4% higher than Sonnet 4.5's 80.9% success rate. Another way of collaboration is to have a more expensive model, Sonnet 4.5, to start from an incomplete proof developed by a cheaper model, o4-mini. In theory, this could lower the money cost of Sonnet 4.5. However, this hypothesis is not confirmed, when we tried it on two randomly sampled tasks from MA. When Sonnet 4.5 started its proof development from the incomplete proof o4-mini produced after 10 VeruSAGE steps, it was quite slow and costly, taking 20 minutes (\$13.7) and 39 minutes (\$18.2) to finally prove these two tasks. In comparison, when Sonnet 4.5 started from scratch, it only took 2 minutes (\$0.81) and 16 minutes (\$14.7) each.

*What if the LLM runs for multiple times?* Given the randomness of LLMs, allowing them to make more attempts could lead to more success. As mentioned earlier, in a second run, Sonnet 4.5 (Hands-Off) succeeded about 10% of the tasks it initially failed in AC, NR, and ST (4/40 failed AC tasks, 2/24 failed ST tasks, and 7/53 failed NR tasks). A similar trend

exists for the Hands-On setting. We ran VeruSAGE + o4-mini on a randomly sampled set of 100 VeruSAGE-Bench tasks for three times. The accumulated success rate goes from 41% after the first run to 56% at three runs. However, the success rate of each individual run remains stable: 41%, 39%, 39%.

### 6 Related Work

*Verification for Rust.* The Rust verification landscape can be broadly categorized by the trade-off between automation and expressiveness. On one end, fully automated tools like Kani [\[33\]](#page-13-12) leverage model checking to verify properties like crash safety with minimal user intervention. While highly accessible, they often face scalability challenges or limitations in expressing complex functional correctness properties for large-scale systems. On the other end, deductive verification tools like Verus [\[17,](#page-12-2) [18\]](#page-13-2), Creusot [\[11\]](#page-12-11), Prusti [\[4\]](#page-12-12), and Aeneas [\[13\]](#page-12-13) offer the expressiveness needed to verify complex system software [\[32,](#page-13-5) [49\]](#page-14-3), handling challenges like concurrency and pointer manipulation via Rust's type system. However, this power comes with a significant *proof burden*: developers must write extensive manual annotations (specifications, loop invariants, lemmas) to guide the verifier. VeruSAGE targets this specific bottleneck, aiming to automate the labor-intensive process of writing these proofs for deductive verifiers, thereby bridging the gap between highassurance verification and developer productivity.

*LLM-based code verification.* LLMs have been revolutionizing software engineering [\[35,](#page-13-13) [38,](#page-13-14) [39,](#page-13-15) [41,](#page-14-7) [42\]](#page-14-8), sparking interest in automating formal proof synthesis [\[20,](#page-13-16) [40,](#page-13-4) [48\]](#page-14-2). Early work focused on prompting or simple RAG for prooforiented languages like Dafny [\[23,](#page-13-3) [25,](#page-13-17) [26,](#page-13-18) [30\]](#page-13-19) and F<sup>∗</sup> [\[7\]](#page-12-3). Recent work like Rango [\[34\]](#page-13-20) for Coq improves RAG by dynamically retrieving relevant proofs to guide the solver. For Verus, AutoVerus [\[40\]](#page-13-4) establishes a baseline workflow using few-shot prompting and error feedback. Most recently, RagVerus [\[48\]](#page-14-2) extends AutoVerus by using RAG to fetch dependencies and similar proof examples from the target project repository. RagVerus evaluates its technique on four Verusverified projects (Verismo [\[49\]](#page-14-3), IronKV [\[17\]](#page-12-2), Vest [\[6\]](#page-12-0), and a small part of Anvil [\[32\]](#page-13-5)) with the original multi-file structure unchanged, referred to as RvBench. The methodology of VeruSAGE-Bench differs from RvBench in that we leverage Verus' built-in log support to extract all the code dependencies out to establish single-file, individually verifiable task files. VeruSAGE-Bench is also based on a more diverse set of 8 open-source systems. RagVerus's low success rate (< 20%) on system projects indicates that RAG alone is insufficient to enable AutoVerus and GPT-4o to tackle system-level proof.

Another direction is model fine-tuning and bootstrapping. SAFE [\[9\]](#page-12-5) employs "self-evolution" to synthesize training data and fine-tune models for Verus proof generation. Similarly, AlphaVerus [\[1\]](#page-12-4) bootstraps verified code generation by translating from Dafny and refining candidates via tree search. Both approaches so far mainly have small programs in their

training set, mainly focus on fine-tuning small models (e.g., DeepSeekCoder-33B), and are evaluated on small programs (VerusBench [\[40\]](#page-13-4), HumanEval-Verus [\[1\]](#page-12-4)), originated from single-file coding benchmarks [\[5,](#page-12-14) [8\]](#page-12-15). While promising, their scalability to large-scale system verification remains to be seen. Our work provides benchmark resources and various lessons for these approaches to scale their future efforts to system-level verification. Plus, current approaches, whether prompting, RAG, or fine-tuning, mainly rely on the model's static knowledge, retrieved context, or translation from other languages. They often lack the dynamic, multi-step reasoning required to debug complex verification failures, which is offered by more advanced agents.

*Agentic and planning-based verification.* To address these limitations, recent research has shifted towards agentic workflows that "think" before act. VeriStruct [\[31\]](#page-13-21) introduces a planner specifically for verifying data structure modules in Verus, orchestrating the generation of class invariants and proofs. Similarly, in the hardware domain, Saarthi [\[16\]](#page-12-16) proposes an autonomous "AI Engineer" for end-to-end RTL verification. VeriPlan [\[21\]](#page-13-22) applies formal verification to validate LLM-generated plans for general tasks. VeruSAGE advances this agentic paradigm for general Rust system verification. Unlike VeriStruct's focus on data structures (e.g., RingBuffer), VeruSAGE employs a diverse set of specialized agents (handling logic, arithmetic, and proof context) and dynamic context management. This allows it to plan and execute complex proof strategies for a wide range of system proof tasks.

# 7 Discussion and Conclusion

The main lesson from our study is that modern reasoning LLMs are dramatically capable of writing proofs of important properties of real-world systems. People who build verified systems would greatly benefit from incorporating LLMs into their workflow. This, in turn, should allow for faster and more frequent development of large-scale verified systems.

Our study also reveals the limitations of the state-of-the-art LLMs and agent systems in proof development, both in terms of proof capability, such as how to devise inductive invariants, how to handle the abstraction in large systems, and how to write concise proofs, and in terms of time and money cost.

Note, there are more challenges in system verification than what was studied in this paper. Our experiment setting provides the LLMs with well-structured Rust programs that are already verified to be correct, and fully defined spec functions and pre- and post-conditions of all executable and proof functions. Although LLMs are good at proving individual functions in our setting, we have no evidence that they are good at breaking down the project-level verification goal into the right specification at the level of every executable function, and into the appropriate set of manageable proof (lemma) functions. In practice, developing a verified system is often a matter of iterating through various code and proof designs, which often involves updating code structures to make them

easier to prove, and adjusting pre- and post-conditions of functions as one discovers that they were initially too weak or too strong to be provable, callable, and useful. With all these factors considered, while we believe that LLMs will be of great help to verified-system builders, we do not expect them to supplant those builders any time soon.

When we change the perspective from system verification to AI coding agents, we believe proof writing is an ideal fit for unreliable LLMs because, once the LLMs start to write not only code but also code proof, the verifier can act as an oracle for determining whether AI-generated code can be trusted.

### Acknowledgement

This material is based on work supported by the National Science Foundation CISE Graduate Fellowships under Grant No. 2313998. Any opinions, findings, and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the National Science Foundation.

### References

- <span id="page-12-4"></span>[1] P. Aggarwal, B. Parno, and S. Welleck. Alphaverus: Bootstrapping formally verified code generation through self-improving translation and treefinement. *arXiv preprint arXiv:2412.06176*, 2024.
- <span id="page-12-7"></span>[2] Anthropic. Introducing claude 4: Claude opus 4 and claude sonnet 4. [https://www.anthropic.co](https://www.anthropic.com/news/claude-4) [m/news/claude-4](https://www.anthropic.com/news/claude-4), May 2025. Introduces the Claude Sonnet 4 model.
- <span id="page-12-8"></span>[3] Anthropic. Introducing claude sonnet 4.5. [https:](https://www.anthropic.com/news/claude-sonnet-4-5) [//www.anthropic.com/news/claude-son](https://www.anthropic.com/news/claude-sonnet-4-5) [net-4-5](https://www.anthropic.com/news/claude-sonnet-4-5), Sept. 2025. Describes the Claude Sonnet 4.5 model.
- <span id="page-12-12"></span>[4] V. Astrauskas, P. Müller, F. Poli, and A. J. Summers. Leveraging rust types for modular specification and verification. *Proc. ACM Program. Lang.*, 3(OOPSLA):147:1–147:30, 2019.
- <span id="page-12-14"></span>[5] J. Austin, A. Odena, M. I. Nye, M. Bosma, H. Michalewski, D. Dohan, E. Jiang, C. J. Cai, M. Terry, Q. V. Le, and C. Sutton. Program synthesis with large language models. *CoRR*, abs/2108.07732, 2021.
- <span id="page-12-0"></span>[6] Y. Cai, P. Singh, Z. Lin, J. Bosamiya, J. Gancher, M. Surbatovich, and B. Parno. Vest: Verified, secure, highperformance parsing and serialization for Rust. In *Proceedings of the USENIX Security Symposium*, August 2025.
- <span id="page-12-3"></span>[7] S. Chakraborty, G. Ebner, S. Bhat, S. Fakhoury, S. Fatima, S. K. Lahiri, and N. Swamy. Towards neural synthesis for smt-assisted proof-oriented programming. In *IEEE/ACM 47th International Conference on Software Engineering (ICSE)*, 2025.

- <span id="page-12-15"></span>[8] M. Chen, J. Tworek, H. Jun, Q. Yuan, H. de Oliveira Pinto, J. Kaplan, H. Edwards, Y. Burda, N. Joseph, G. Brockman, A. Ray, R. Puri, M. Krueger, H. Petrov, I. Khattam, C. Hesse, S. Agarwal, G. Sastry, P. Mishkin, B. Chan, S. Gray, N. Ryder, M. Pavlov, B. Power, L. Kaiser, M. Bavarian, C. King, T. Kerr, S. McCandlish, A. Radford, I. Sutskever, and W. Zaremba. Evaluating large language models trained on code. *arXiv preprint arXiv:2107.03374*, 2021.
- <span id="page-12-5"></span>[9] T. Chen, S. Lu, S. Lu, Y. Gong, C. Yang, X. Li, M. R. H. Misu, H. Yu, N. Duan, P. Cheng, F. Yang, S. K. Lahiri, T. Xie, and L. Zhou. Automated proof generation for rust code via self-evolution. In *Proceedings of the 13th International Conference on Learning Representations (ICLR)*, 2025.
- <span id="page-12-1"></span>[10] X. Chen, Z. Li, J. Zhang, V. Narayanan, and A. Burtsev. Atmosphere: Practical verified kernels with rust and verus. In *Proceedings of the ACM Symposium on Operating Systems Principles (SOSP)*. Association for Computing Machinery, 2025.
- <span id="page-12-11"></span>[11] X. Denis, J. Jourdan, and C. Marché. Creusot: A foundry for the deductive verification of rust programs. In *Formal Methods and Software Engineering - 23rd International Conference on Formal Engineering Methods, ICFEM 2022, Madrid, Spain, October 24-27, 2022, Proceedings*, volume 13478 of *Lecture Notes in Computer Science*, pages 90–105. Springer, 2022.
- <span id="page-12-9"></span>[12] GitHub. Github copilot cli. [https://github.com](https://github.com/github/copilot-cli) [/github/copilot-cli](https://github.com/github/copilot-cli), Sept. 2025. Commandline interface for GitHub Copilot.
- <span id="page-12-13"></span>[13] S. Ho and J. Protzenko. Aeneas: Rust verification by functional translation. *Proc. ACM Program. Lang.*, 6(ICFP):711–741, 2022.
- <span id="page-12-6"></span>[14] A. Hurst, A. Lerer, and OpenAI. GPT-4o System Card. *arXiv preprint arXiv:2410.21276*, 2024.
- <span id="page-12-10"></span>[15] R. Jain, S. Barke, G. Ebner, M. R. H. Misu, S. Lu, and S. Fakhoury. What's in a proof? analyzing expert proof-writing processes in f\* and verus. *arXiv preprint arXiv:2508.02733*, 2025.
- <span id="page-12-16"></span>[16] A. Kumar, D. N. Gadde, K. K. Radhakrishna, and D. Lettnin. Saarthi: The first ai formal verification engineer. *CoRR*, abs/2502.16662, 2025.
- <span id="page-12-2"></span>[17] A. Lattuada, T. Hance, J. Bosamiya, M. Brun, C. Cho, H. LeBlanc, P. Srinivasan, R. Achermann, T. Chajed, C. Hawblitzel, et al. Verus: A practical foundation for systems verification. In *Proceedings of the ACM SIGOPS 30th Symposium on Operating Systems Principles*, pages 438–454, 2024.

- <span id="page-13-2"></span>[18] A. Lattuada, T. Hance, C. Cho, M. Brun, I. Subasinghe, Y. Zhou, J. Howell, B. Parno, and C. Hawblitzel. Verus: Verifying rust programs using linear ghost types. *Proc. ACM Program. Lang.*, 7(OOPSLA1):286–315, 2023.
- <span id="page-13-1"></span>[19] H. LeBlanc, J. R. Lorch, C. Hawblitzel, C. Huang, Y. Tao, N. Zeldovich, and V. Chidambaram. Power never corrupts: Tool-agnostic verification of crash consistency and corruption detection. *OSDI (to appear)*, 2025.
- <span id="page-13-16"></span>[20] Z. Li, J. Sun, L. Murphy, Q. Su, Z. Li, X. Zhang, K. Yang, and X. Si. A survey on deep learning for theorem proving. *CoRR*, abs/2404.09939, 2024.
- <span id="page-13-22"></span>[21] Y. Liu and et al. Veriplan: Integrating formal verification and llms into end-user planning. *CoRR*, abs/2502.17898, 2025.
- <span id="page-13-9"></span>[22] J. R. Lorch. Fix usability issue with unused subregions library. https://github.com/microsoft/verifiedstorage/pull/39.
- <span id="page-13-3"></span>[23] C. Loughridge, Q. Sun, S. Ahrenbach, F. Cassano, C. Sun, Y. Sheng, A. Mudide, M. R. H. Misu, N. Amin, and M. Tegmark. Dafnybench: A benchmark for formal software verification. *CoRR*, abs/2406.08467, 2024.
- <span id="page-13-11"></span>[24] H. Ma, A. Goel, J.-B. Jeannin, M. Kapritsos, B. Kasikci, and K. A. Sakallah. I4: incremental inference of inductive invariants for verification of distributed protocols. In *Proceedings of the 27th ACM Symposium on Operating Systems Principles (SOSP)*, pages 370–384, 2019.
- <span id="page-13-17"></span>[25] M. R. H. Misu, C. V. Lopes, I. Ma, and J. Noble. Towards ai-assisted synthesis of verified dafny methods. *Proc. ACM Softw. Eng.*, 1(FSE):812–835, 2024.
- <span id="page-13-18"></span>[26] E. Mugnier, E. A. Gonzalez, R. Jhala, N. Polikarpova, and Y. Zhou. Laurel: Generating dafny assertions using large language models. *CoRR*, abs/2405.16792, 2024.
- <span id="page-13-8"></span>[27] OpenAI. Codex. <https://openai.com/codex/>, 2025. OpenAI's coding agent for software development.
- <span id="page-13-7"></span>[28] OpenAI. Gpt-5 system card. Technical report, OpenAI, Aug. 2025. Describes the GPT-5 model series.
- <span id="page-13-6"></span>[29] OpenAI. Openai o3 and o4-mini system card. Technical report, OpenAI, Apr. 2025. Describes the OpenAI o4 mini reasoning model.
- <span id="page-13-19"></span>[30] C. Sun, Y. Sheng, O. Padon, and C. W. Barrett. Clover: Closed-loop verifiable code generation. In *AI Verification - First International Symposium, SAIV 2024, Montreal, QC, Canada, July 22-23, 2024, Proceedings*, volume 14846 of *Lecture Notes in Computer Science*, pages 134–155. Springer, 2024.

- <span id="page-13-21"></span>[31] C. Sun, Y. Sun, D. Amrollahi, E. Zhang, S. Lahiri, S. Lu, D. Dill, and C. Barrett. Veristruct: Ai-assisted automated verification of data-structure modules in verus. *arXiv preprint arXiv:2510.25015*, 2025.
- <span id="page-13-5"></span>[32] X. Sun, W. Ma, J. T. Gu, Z. Ma, T. Chajed, J. Howell, A. Lattuada, O. Padon, L. Suresh, A. Szekeres, and T. Xu. Anvil: Verifying liveness of cluster management controllers. In *18th USENIX Symposium on Operating Systems Design and Implementation, OSDI 2024, Santa Clara, CA, USA, July 10-12, 2024*, pages 649–666. USENIX Association, 2024.
- <span id="page-13-12"></span>[33] T. K. Team. How open source projects are using kani to write better software in rust. [https://aws.amaz](https://aws.amazon.com/blogs/opensource/how-open-source-projects-are-using-kani-to-write-better-software-in-rust/) [on.com/blogs/opensource/how-open-sou](https://aws.amazon.com/blogs/opensource/how-open-source-projects-are-using-kani-to-write-better-software-in-rust/) [rce-projects-are-using-kani-to-write](https://aws.amazon.com/blogs/opensource/how-open-source-projects-are-using-kani-to-write-better-software-in-rust/) [-better-software-in-rust/](https://aws.amazon.com/blogs/opensource/how-open-source-projects-are-using-kani-to-write-better-software-in-rust/), 2024. [Online], [Accessed: 2024-09-01].
- <span id="page-13-20"></span>[34] K. Thompson, N. Saavedra, P. Carrott, K. Fisher, A. Sanchez-Stern, Y. Brun, J. F. Ferreira, S. Lerner, and E. First. Rango: Adaptive retrieval-augmented proving for automated software verification. *arXiv preprint arXiv:2412.14063*, 2024.
- <span id="page-13-13"></span>[35] R. Tian, Y. Ye, Y. Qin, X. Cong, Y. Lin, Y. Pan, Y. Wu, H. Hui, W. Liu, Z. Liu, and M. Sun. Debugbench: Evaluating debugging capability of large language models. pages 4173–4198, 2024.
- <span id="page-13-10"></span>[36] Wikipedia contributors. Point-biserial correlation coefficient — Wikipedia, the free encyclopedia, 2025. [Online; accessed 10-December-2025].
- <span id="page-13-0"></span>[37] C. S. Xia, Z. Wang, Y. Yang, Y. Wei, and L. Zhang. Liveswe-agent: Can software engineering agents self-evolve on the fly? *arXiv preprint arXiv:2511.13646*, 2025.
- <span id="page-13-14"></span>[38] C. S. Xia and L. Zhang. Keep the conversation going: Fixing 162 out of 337 bugs for \$0.42 each using chatgpt. *CoRR*, abs/2304.00385, 2023.
- <span id="page-13-15"></span>[39] C. Yang, Y. Deng, R. Lu, J. Yao, J. Liu, R. Jabbarvand, and L. Zhang. Whitefox: White-box compiler fuzzing empowered by large language models. *Proceedings of the ACM on Programming Languages*, 8(OOPSLA2):709–735, 2024.
- <span id="page-13-4"></span>[40] C. Yang, X. Li, M. R. H. Misu, J. Yao, W. Cui, Y. Gong, C. Hawblitzel, S. K. Lahiri, J. R. Lorch, S. Lu, F. Yang, Z. Zhou, and S. Lu. Autoverus: Automated proof generation for rust code. *Proceedings of the ACM on Programming Languages*, 9(OOPSLA2), 2025.

- <span id="page-14-7"></span>[41] C. Yang, Z. Zhao, Z. Xie, H. Li, and L. Zhang. Knighter: Transforming static analysis with llm-synthesized checkers. In *Proceedings of the ACM SIGOPS 31st Symposium on Operating Systems Principles*, SOSP '25, New York, NY, USA, 2025. Association for Computing Machinery.
- <span id="page-14-8"></span>[42] C. Yang, Z. Zhao, and L. Zhang. Kernelgpt: Enhanced kernel fuzzing via large language models. In *Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems, Volume 2*, pages 560–573, 2025.
- <span id="page-14-0"></span>[43] J. Yang, C. E. Jimenez, A. Wettig, K. Lieret, S. Yao, K. Narasimhan, and O. Press. Swe-agent: Agentcomputer interfaces enable automated software engineering. *Advances in Neural Information Processing Systems*, 37:50528–50652, 2024.
- <span id="page-14-4"></span>[44] J. Yao, R. Tao, R. Gu, and J. Nieh. DuoAI: Fast, automated inference of inductive invariants for verifying distributed protocols. In *Proceedings of the USENIX Symposium on Operating Systems Design and Implementation (OSDI)*, 2022.
- <span id="page-14-5"></span>[45] J. Yao, R. Tao, R. Gu, J. Nieh, S. S. Jana, and G. Ryan. DistAI: Data-driven automated invariant learning for distributed protocols. In *Proceedings of the USENIX*

- *Symposium on Operating Systems Design and Implementation (OSDI)*, 2021.
- <span id="page-14-1"></span>[46] J. Zhang, X. Xu, Y. Zou, Z. Tang, X. Wan, K. Hu, S. Wang, W. Xu, D. Wang, H. Chen, et al. Cortenmm: Efficient memory management with strong correctness guarantees. In *Proceedings of the ACM SIGOPS 31st Symposium on Operating Systems Principles*, pages 1082–1098, 2025.
- <span id="page-14-6"></span>[47] T. N. Zhang, K. Singh, T. Chajed, M. Kapritsos, and B. Parno. Basilisk: using provenance invariants to automate proofs of undecidable protocols. In *Proceedings of the 19th USENIX Conference on Operating Systems Design and Implementation (OSDI)*, 2025.
- <span id="page-14-2"></span>[48] S. C. Zhong and X. Si. Towards repository-level program verification with large language models. In *Proceedings of the 1st ACM SIGPLAN International Workshop on Language Models and Programming Languages (LMPL)*, 2025.
- <span id="page-14-3"></span>[49] Z. Zhou, Anjali, W. Chen, S. Gong, C. Hawblitzel, and W. Cui. Verismo: A verified security module for confidential vms. In *18th USENIX Symposium on Operating Systems Design and Implementation, OSDI 2024, Santa Clara, CA, USA, July 10-12, 2024*, pages 599–614. USENIX Association, 2024.