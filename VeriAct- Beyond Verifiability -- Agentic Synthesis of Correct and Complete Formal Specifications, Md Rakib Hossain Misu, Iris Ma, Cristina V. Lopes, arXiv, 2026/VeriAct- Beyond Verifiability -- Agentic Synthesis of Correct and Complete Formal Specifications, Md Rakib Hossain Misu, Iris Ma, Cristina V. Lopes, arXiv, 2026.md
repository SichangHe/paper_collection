# VeriAct: Beyond Verifiability – Agentic Synthesis of Correct and Complete Formal Specifications

[Md Rakib Hossain Misu](https://orcid.org/0000-0002-7931-6782)<sup>∗</sup> University of California, Irvine Irvine, California, USA mdrh@uci.edu

[Iris Ma](https://orcid.org/0009-0003-3699-7981) University of California, Irvine Irvine, California, USA huaiyaom@uci.edu

[Cristina V. Lopes](https://orcid.org/0000-0003-0551-3908) University of California, Irvine Irvine, California, USA lopes@uci.edu

### Abstract

Formal specifications play a central role in ensuring software reliability and correctness. However, automatically synthesizing highquality formal specifications remains a challenging task, often requiring domain expertise. Recent work has applied large language models to generate specifications in Java Modeling Language (JML), reporting high verification pass rates. But does passing a verifier mean that the specification is actually correct and complete? In this work, we first conduct a comprehensive evaluation comparing classical and prompt-based approaches for automated JML specification synthesis. We then investigate whether prompt optimization can push synthesis quality further by evolving prompts through structured verification feedback. While optimization improves verifier pass rates, we find a clear performance ceiling. More critically, we propose Spec-Harness, an evaluation framework that measures specification correctness and completeness through symbolic verification, revealing that a large fraction of verifier-accepted specifications, including optimized ones, are in fact incorrect or incomplete, over- or under-constraining both inputs and outputs in ways invisible to the verifier. To push beyond this ceiling, we propose VeriAct, a verification-guided agentic framework that iteratively synthesizes and repairs specifications through a closed loop of LLM-driven planning, code execution, verification, and Spec-Harness feedback. Our experiments on two benchmark datasets show that VeriAct outperforms both prompt-based and prompt-optimized baselines, producing specifications that are not only verifiable but also correct and complete.

### CCS Concepts

• Software and its engineering → Formal software verification.

### Keywords

Program Verification, LLM, Java, JML

# 1 Introduction

The correctness of software systems increasingly depends on the availability of precise, machine-checkable behavioral contracts. Formal specifications describe the intended behavior of programs using behavioral contracts with precise semantics, typically expressed as method preconditions and postconditions, loop invariants, or assertions at specific program locations. They form the foundation for a wide range of software quality assurance tasks, including testing, model checking, and program verification. In the Java ecosystem, the Java Modeling Language (JML) [\[7,](#page-10-0) [29\]](#page-11-0) provides a standard

notation for writing such behavioral contracts, which tools like OpenJML [\[13\]](#page-10-1) and KeY [\[2\]](#page-10-2) can then verify against the implementation. When these specifications are both correct and complete, they enable exhaustive reasoning about program behavior, detection of boundary violations, and generation of test oracles.

However, writing JML annotations in practice remains demanding since it requires domain specific expertise, deep understanding of program semantics, and significant manual efforts. Traditional rules base approaches have been developed for automated JML synthesis [\[15,](#page-10-3) [16,](#page-10-4) [34\]](#page-11-1). Among them, Houdini [\[16\]](#page-10-4) and Daikon [\[15\]](#page-10-3) being the most prominent for Java programs. Houdini uses a refutationbased approach that starts with a large set of candidate annotations drawn from predefined templates and iteratively removes those that the verifier disproves. Daikon takes a dynamic analysis approach, observing program executions to infer likely invariants over observed variable values. While both tools reduce the manual burden of writing specifications, their output is constrained by fixed templates or grammars and this reliance on predefined patterns produces overly simplistic specifications [\[32\]](#page-11-2) that fails to capture all program semantics and behaviors.

Recent advances in large language models have opened a promising direction for automatically synthesizing meaningful specifications because of their excellent capabilities of code understanding and reasoning. For instance, SpecGen [\[31\]](#page-11-3) introduced a promptdriven pipeline for generating JML specifications from Java method signatures and bodies, demonstrating that contemporary LLMs possess sufficient syntactic and semantic understanding to produce plausible formal annotations. AutoSpec [\[43\]](#page-11-4) combines LLMs with static analysis by decomposing a program into components, generating specifications for each through LLM queries, and composing them into a complete annotation. It iteratively refines the result using verifier feedback until the specification is accepted. Formal-Bench [\[28\]](#page-11-5) subsequently established a systematic benchmark for evaluating LLM performance on formal specification generation tasks, providing standardized evaluation across a curated suite of Java methods with various prompts.

Despite recent advances, existing LLM-based approaches continue to exhibit three major drawbacks. l When an LLM is prompted to generate a specification for a given java code, existing approaches do not validate whether the model has silently altered the original code to fit the specification it produces. l More fundamentally, current approaches largely rely on verifier acceptance as the principal measure of specification quality. However, successful verification does not guarantee that a specification is either correct or complete. For example, a trivial postcondition such as ensures true, will satisfy any verifier, yet it provides no meaningful characterization

<sup>∗</sup>Corresponding author: Md Rakib Hossain Misu (mdrh@uci.edu)

of the code's behavior and would be ineffective in identifying erroneous outputs during testing [14, 26, 27]. Finally, the task of distinguishing substantive specifications from trivial or incomplete ones continues to depend on manual evaluation by human experts. This reliance on human judgment presents a significant scalability challenge, particularly when assessing large benchmark datasets comprising hundreds or thousands of java code snippets.

These shortcomings collectively point to the need for investigating four key aspects: An empirical study of state-of-the-art classical and prompt-based specification synthesis approaches, Prompt optimization techniques that leverage structured verification feedback to improve synthesis quality, An automated evaluation framework that measures specification quality beyond verifier acceptance, and A verification-guided agentic approach that iteratively synthesizes and repairs specifications through closed-loop feedback.

This work investigates all four aspects through a structured, multi-stage analysis: we begin with a broad empirical study of existing approaches, apply prompt optimization to push verifier-based synthesis to its limits, introduce a new evaluation framework that exposes the hidden gap between verifiability and actual specification quality, and finally propose an agentic approach that closes this gap by incorporating specification quality feedback directly into the synthesis loop. In summary, this paper makes the following contributions:

- We conduct a comprehensive evaluation of classical and prompt-based specification synthesis approaches, revealing that high verifier acceptance rates alone do not reflect actual specification quality.
- We demonstrate that GEPA-driven prompt optimization with structured verification feedback improves verifier pass rates but reaches a performance ceiling — and more critically, the resulting specifications still suffer from correctness and completeness deficiencies.
- We propose Spec-Harness, an automated evaluation framework that measures the correctness and completeness of formal specifications beyond verifier pass/fail, using metrics grounded in Hoare-triple reasoning and input/output mutation testing.
- We develop VeriAct, a verification-guided agentic framework that combines closed-loop iterative LLM planning, code execution, verification, and Spec-Harness feedback to synthesize specifications that are verifiable, correct, and complete.

#### 2 Background & Motivation

#### 2.1 IML and Deductive Verification

The Java Modeling Language (JML) is a behavioral specification language that allows developers to annotate Java methods with formal contracts. A JML contract consists of requires clauses, which define preconditions that must hold before a method executes, and ensures clauses, which define postconditions that must hold when the method returns. The keyword \result refers to the method's return value within postconditions. For iterative code, JML provides loop\_invariant and maintaining annotations that express properties preserved across every iteration of a loop, enabling the verifier to reason about loops without unrolling them.

```
SGB_ChangeCase: Change Character Case
1 : public class ChangeCase {
       @ requires c >= 'A' && c <= 'z':
3:
       @ ensures (c >= 'a' && c <= 'z')
4:
5:
                 ==> (\result >= 'A' && \result <= 'Z');
6:
7 :
      public char changeCase (char c) {
          char out = ' ':
8:
          if (c > 'z') { out = c; }
9:
          else if (c >= 'a') { out = (char)(c - 'a' + 'A'); }
10:
          else if (c > 'Z') { out = c; }
11.
          else if (c >= 'A') { out = (char)(c - 'A' + 'a'); }
12:
13.
          else { out = c: }
14:
          return out;
15:
      }
16: }
```

Figure 1: Example of a JML annotated snippet from SpecGen-Bench with formal specification generated by an LLM

Once annotated, a deductive verifier such as OpenJML statically checks whether the implementation satisfies its JML specification. Internally, the verifier translates the annotated program into a set of logical proof obligations and dispatches them to an SMT (Satisfiability Modulo Theories) solver. The SMT solver attempts to prove that each obligation holds across all possible inputs and execution paths. If all obligations are discharged, the specification is considered verified — meaning the implementation does not violate the stated contract. However, successful verification only confirms that the code is consistent with the specification, not that the specification itself is correct or complete.

### 2.2 Motivating Example

Figure 1 illustrates an LLM-annotated JML specification on top of the changeCase method that converts characters between uppercase and lowercase. The precondition on line 3 restricts the input to characters in the range ['A'..'z'], and the postcondition on lines 4-5 states that if the input is a lowercase letter, the result falls within the uppercase range ['A'..'Z']. This specification passes OpenJML verification without any errors. However, passing the verifier does not mean this specification is correct or complete. The postcondition covers only the lowercase-to-uppercase branch and, even for that branch, it only asserts that the result falls somewhere in ['A'..'Z'] rather than equating it to the precise conversion expression (char) (c - 'a' + 'A'). The remaining four branches, uppercase-to-lowercase conversion, identity for non-letter characters, and characters outside ['A'..'z'], are entirely unspecified. Any return value would satisfy the postcondition for these cases. Similarly, the precondition restricts input to c >= 'A' && c <='z', which incorrectly rejects valid printable characters below 'A' such as '!' or digits, and above 'z' such as '|', even though the method handles these correctly through identity assignment. In short, this specification is both too weak in what it guarantees about outputs and too strong in what it demands of inputs.

This example exposes a fundamental limitation of relying on verifier acceptance as a quality measure. A verifier confirms that the implementation does not violate the specification — but if the

specification says very little, there is very little to violate. Trivial or partial specifications pass verification easily, yet they fail to capture the full behavioral contract of the method. This gap between verifiability and actual specification quality motivates the need for an evaluation framework that can systematically measure how correct and how complete a specification truly is, independent of whether a verifier accepts it.

# 2.3 Research Questions

We structure our investigation around four research questions, each building on the findings of the preceding one.

- ⋆ RQ1 [Effectiveness]: How effective are state-of-the-art approaches — classical (Daikon, Houdini) vs. prompt-based (SpecGen, AutoSpec, FormalBench) — in synthesizing verifiable formal specifications? Both classical and LLM-based approaches report varying levels of success in generating JML specifications that pass a verifier. However, no existing study provides a unified comparison across these two families under a common benchmark and evaluation setup. RQ1 establishes this baseline by measuring verifier acceptance rates across all approaches.
- ⋆ RQ2 [Optimization]: Can prompt optimization, leveraging structured verification feedback, improve the effectiveness of LLMdriven formal specification synthesis? Prompt design significantly influences LLM output quality. RQ2 investigates whether systematically evolving prompts, using GEPA-driven optimization with a graduated verification scoring function, can push verifier pass rates beyond what fixed prompt strategies achieve. We apply this optimization across the best, average and the worst prompt types selected from RQ1 results.
- ⋆ RQ3 [Correctness & Completeness]: How correct and complete are verifier-accepted formal specifications, including promptoptimized ones, when evaluated with Spec-Harness? RQ1 and RQ2 measure success by verifier acceptance, but this metric cannot distinguish a meaningful specification from a trivially weak one. RQ3 applies Spec-Harness, a set of metrics, to all verifier-accepted specifications produced across RQ1 and RQ2, exposing the gap between verifiability and actual specification quality.
- ⋆ RQ4 [VeriAct]: Can VeriAct a verification-guided agentic loop combining code execution with Spec-Harness feedback — outperform prompt-based and prompt-optimized approaches in synthesizing correct and complete formal specifications? RQ3 reveals that neither prompt-based nor optimized approaches consistently produce correct and complete specifications. RQ4 investigates whether an agentic framework that incorporates Spec-Harness feedback directly into its synthesis loop can close this gap.

# 3 Empirical Study: Classical vs. Prompt-Based Specification Synthesis

# 3.1 Baselines

We evaluate two families of specification synthesis approaches: classical tools that rely on predefined templates or dynamic analysis, and prompt-based approaches that leverage LLMs for specification generation.

3.1.1 Classical Approaches. We elected two conventional approaches, utilized in JML specification generations.

<span id="page-2-0"></span>![](_page_2_Figure_13.jpeg)

Figure 2: Task category distribution (%) for SpecGenBench and FormalBench.

- Ö Houdini [\[16\]](#page-10-4) is a template-based JML annotation generator. Given a Java method, it populates a set of predefined templates with available variables and operators to produce candidate specifications. It then iteratively invokes a JML verifier, removing any candidate that the verifier refutes, until all remaining annotations are verified.
- Ö Daikon [\[15\]](#page-10-3) is a dynamic invariant detection tool. It instruments the target program to trace variable values during execution, then applies a generate-and-check algorithm over the collected traces to infer likely invariants. Daikon supports multiple output formats including JML.
- 3.1.2 Prompt-Based Approaches. There are three LLM-driven automated JML annotation generation approaches reported in the literature.
- j SpecGen [\[31\]](#page-11-3) uses its own prompt templates to generate JML specifications from Java method signatures and bodies. It employs a mutation-guided conversational pipeline where the LLM iteratively refines its output based on verifier feedback. We evaluate SpecGen with three prompt configurations: zero, two, and four-shot.
- j AutoSpec [\[43\]](#page-11-4) combines LLMs with static analysis by first decomposing a program into components and building a hierarchy graph. It queries the LLM for specifications of each component, composes them, and iteratively refines the result through verifier feedback until the specification is accepted. We evaluate AutoSpec with zero-shot, two-shot, and four-shot prompts.
- j FormalBench [\[28\]](#page-11-5) provides a set of prompting strategies designed for formal specification generation, covering a range of prompting techniques. We evaluate five prompt configurations: zero-shot, two-shot, zero-shot chain-of-thought (zs\_cot), few-shot chain-of-thought (fs\_cot), and few-shot least-to-most (fs\_ltm). It is a benchmark dataset and also include advance prompting approaches to infer and fix JML specification with LLMs.

### 3.2 Dataset

We use two established benchmarks for evaluation. SpecGenBench contains 120 Java method tasks and FormalBench contains 700 Java method tasks. Upon manual review, we found that a small number of methods in FormalBench have no return type (void) or use Object as a parameter or return type. Methods without a return

<span id="page-3-0"></span>Table 1: Summary of Models and Prompt Configurations

| Component             | Configuration                                 |  |  |  |
|-----------------------|-----------------------------------------------|--|--|--|
| Proprietary Models    |                                               |  |  |  |
|                       | gpt-4o-2024-08-06 [35]                        |  |  |  |
|                       | gemini-2.0-flash [17]                         |  |  |  |
|                       | claude-sonnet-4-6 [4]                         |  |  |  |
| Open-Weight Models    |                                               |  |  |  |
|                       | Qwen2.5-Coder-32B-Instruct [22]               |  |  |  |
|                       | deepseek-coder-33b-instruct [20]              |  |  |  |
|                       | CodeLlama-34b-Instruct-hf [39]                |  |  |  |
| Prompt Configurations |                                               |  |  |  |
| SpecGen [31]          | zero-shot (ZS), two-shot (2S), four-shot (4S) |  |  |  |
| AutoSpec [43]         | zero-shot, two-shot, four-shot                |  |  |  |
| FormalBench [28]      | zero-shot, two-shot, zs-cot, fs-cot, fs-ltm   |  |  |  |

value cannot be meaningfully evaluated with postcondition verification, since there is no \result to constrain. Similarly, Objecttyped parameters lack the type specificity needed for meaningful preconditions. We exclude these methods, resulting in 662 tasks from FormalBench. Both benchmarks categorize their tasks into five types based on control-flow structure: branch, multi\_path\_loop, nested, sequential, and single\_path\_loop. Figure [2](#page-2-0) shows the task category distributions across SpecGenBench and FormalBench, revealing that SpecGenBench is proportionally more branch-heavy while FormalBench is skewed toward loop-based (both single-path and multi-path) task categories.

Normalization. To ensure that LLMs rely solely on code reasoning rather than inferring behavior from naming conventions, we normalize all benchmark tasks by renaming class names to Solution and method names to solve(). Without this step, a class named BinarySearch with a method search() would leak semantic hints to the model, allowing it to bypass actual code comprehension. This normalization enforces a uniform evaluation setting across all models and approaches.

Test Suite Extension. The original benchmarks provide only 3–5 test pairs per task. To enable more robust evaluation — particularly for Daikon, which requires execution traces, and for Spec-Harness, which relies on diverse input-output pairs — we extend each task with 100–200 additional test pairs generated through randomly guided automated test generation. These extended test suites also serve to validate task correctness across all approaches.

### 3.3 Experiments

For classical approaches, we run Houdini and Daikon on both benchmarks. For prompt-based approaches, we evaluate 11 prompt configurations (3 from SpecGen, 3 from AutoSpec, and 5 from Formal-Bench) across six LLMs: three frontier proprietary models from major providers (OpenAI [\[36\]](#page-11-8), Google [\[18\]](#page-10-12), Anthropic [\[3\]](#page-10-13)), and three open-weight models at a comparable parameter scale ( 32–34B) to provide a controlled comparison. Table [1](#page-3-0) presents a summary of all configurations that yield 11 prompts × 6 models × 2 benchmarks = 132 prompt-based runs, plus 2 classical runs (Daikon and Houdini),

<span id="page-3-1"></span>Table 2: Summary: Classical vs. Prompt-based Approaches (Best Configurations)

| Approach           | SpecGenBench    | FormalBench     |
|--------------------|-----------------|-----------------|
| Daikon             | 22/120 (18.3%)  | 87/662 (13.1%)  |
| Houdini            | 104/120 (86.7%) | 359/662 (54.2%) |
| SpecGen (best)     | 80/120 (66.7%)  | 200/659 (30.3%) |
| AutoSpec (best)    | 70/120 (58.3%)  | 185/662 (27.9%) |
| FormalBench (best) | 77/120 (64.2%)  | 238/662 (36.0%) |

totaling 134 experimental configurations. All experiments use the same OpenJML version (21-0.21) and Java 21.0.4 to ensure a consistent verification environment. We use the same max\_iterations configuration for each approach as reported in baselines original experiments. For this research question, we measure specification quality using the Verification Rate (VR), defined as the fraction of generated specifications that pass OpenJML verification without errors. This binary pass/fail metric reflects the standard evaluation criterion used by all existing approaches.

# 3.4 Results

RQ1 [Effectiveness]: How effective are state-of-the-art approaches — classical (Daikon, Houdini) vs. prompt-based (SpecGen, AutoSpec, FormalBench) — in synthesizing verifiable formal specifications?

3.4.1 Classical Approaches. The two classical approaches show a wide performance gap. Houdini achieves the strongest results overall — 86.7% on SpecGenBench and 54.2% on FormalBench (Fig. 2) — because it leverages iterative candidate weakening with a fixed verifier, giving it a structural advantage. Daikon, by contrast, performs poorly across both benchmarks (18.3% and 13.1%), as its dynamic invariant inference struggles to produce specifications precise enough to pass static verification. This gap highlights that classical approaches are not uniformly strong, and their effectiveness is tightly coupled to their underlying verification strategy.

3.4.2 Prompt-based Approaches (Best Configurations). Among promptbased approaches, SpecGen leads on SpecGenBench at 66.7%, followed closely by the FormalBench prompts (64.2%) and AutoSpec (58.3%). On FormalBench dataset, the FormalBench prompts achieve the best result at 36.0%, while SpecGen and AutoSpec trail at 30.3% and 27.9% respectively. As seen in Figure [3](#page-4-0) proprietary models (GPT-4o, Gemini, Claude Sonnet 4.6) consistently outperform openweight models under the best configuration, with Claude Sonnet 4.6 reaching 66.7% on SpecGenBench with SpecGen 4-shot. Table [2](#page-3-1) represent the summary of the best configurations result of all prompt based approaches vs classical approaches.

3.4.3 Average vs. Best Configuration Gap. When looking at average verification rates across all configurations, performance drops notably for all prompt-based approaches — SpecGen falls from 66.7% to 43.1% on SpecGenBench, and from 30.3% to 20.1% on Formal-Bench. A similar drop is observed for AutoSpec and FormalBench prompts. This gap between best and average configurations signals that prompt-based methods are sensitive to prompt design choices

<span id="page-4-0"></span>![](_page_4_Figure_2.jpeg)

Figure 3: Verification Rate (VR%) in all prompt based approaches for all LLMs and prompt types.

such as shot count and instruction framing, and do not generalize uniformly across all settings.

3.4.4 Prompt-based vs. Classical. Despite their flexibility, promptbased approaches fall short of Houdini under best configurations (66.7% vs. 86.7% on SpecGenBench; 36.0% vs. 54.2% on Formal-Bench), as shown in Figure [3.](#page-4-0) However, they substantially outperform Daikon and offer broader applicability across diverse method types without requiring instrumented execution.

#### Summary RQ1

Houdini remains the strongest baseline overall, but promptbased approaches — particularly SpecGen and FormalBench prompts with proprietary LLMs — close the gap meaningfully on simpler benchmarks. All prompt-based methods show a significant drop from best to average configuration, pointing to high sensitivity to prompt design.

# 4 GEPA-Driven Prompt Optimization for Specification Synthesis

Prompt optimization is the process of systematically refining the instructions given to an LLM to improve its output quality on a target task [\[1,](#page-10-14) [25,](#page-10-15) [37,](#page-11-9) [40\]](#page-11-10). Rather than relying on manually crafted prompts, optimization techniques automatically search for prompt formulations that maximize a given scoring function. Several prompt optimizers have been proposed in recent literature. COPRO [\[40\]](#page-11-10) iteratively rewrites prompts by sampling candidate variations and selecting the best-performing one based on task accuracy. MIPRO [\[37\]](#page-11-9) extends this idea by jointly optimizing both the instruction text and few-shot example selection using a Bayesian surrogate model. While both approaches are effective for general NLP tasks, they treat the scoring function as a black-box scalar signal and do not leverage structured feedback about why a particular output failed.

GEPA (Genetic-Pareto) [\[1\]](#page-10-14) takes a fundamentally different approach through reflective prompt evolution. Given a set of systemlevel execution traces, including the LLM's reasoning, tool calls, and outputs, GEPA reflects on them in natural language to diagnose problems, propose prompt updates, and combine complementary lessons from the Pareto frontier of its own attempts. This reflective mechanism makes GEPA particularly well-suited for formal specification synthesis, where failure modes are structured and classifiable. When a generated specification fails verification, the error is not arbitrary, it is a syntax error, a postcondition violation, or a type mismatch, each requiring a different repair direction. GEPA can consume both a numerical score and textual feedback explaining what went wrong, giving the optimizer a double signal: the score provides gradient, and the feedback explains the direction.

In contrast, COPRO and MIPRO would receive only a binary or scalar reward without any structured explanation of the failure, limiting their ability to make targeted prompt refinements. For a domain where the difference between a syntax error and a single postcondition violation represents a meaningful quality gap, this distinction is critical. We therefore adopt GEPA as our prompt optimizer for this study.

### 4.1 Approach

From the results of RQ1, we identify three representative prompt types based on their verifier pass rates: zero-shot (worst performing), few-shots least-to-most (average performing) and few-shot chain-of-thought (best performing). We use these three prompts as seed prompts for GEPA optimization, ensuring that the optimizer is evaluated across the full performance spectrum rather than on a single prompting strategy. For the few-shot CoT and few-shot LtM seeds, we include two example tasks drawn from SpecGenBench as in-context demonstrations. We draw a stratified sample from FormalBench based on task categories, resulting in a 100/50/512 split for train, validation, and test sets respectively. Stratification ensures that each task category is proportionally represented across all splits, preventing the optimizer from overfitting to a narrow subset of specification patterns. To provide GEPA with a meaningful optimization signal, we design a graduated scoring function that assigns partial credit based on the severity of verification failures, rather than treating verification as a binary pass/fail outcome:

Equation 1 represents this scoring function, where r is the verification result,  $E_s(r)$  denotes the set of syntax errors, and  $E_v(r)$  denotes the set of verification errors reported by the verifier. The key insight behind this scoring function is that not all failures are equal: a specification with a single postcondition violation is structurally much closer to a correct specification than one with a syntax error, and the optimizer should be able to distinguish between these cases. Combined with GEPA's reflective feedback mechanism, which receives classified error descriptions alongside the score, this gives the optimizer both a gradient to climb and an explanation of the repair direction.

In our implementation, we utilize DSPy's [25] optimizer module with GEPA as the optimization strategy. We use gpt-4o as both the target model (generating specifications) and the reflection model (analyzing failures and proposing prompt updates). The optimization budget is set to the medium in the run configuration.

<span id="page-5-0"></span>
$$Score(r) = \begin{cases} 1.0 & \text{if } r \text{ is verified successfully} \\ 0.3 & \text{if } |E_v(r)| = 1 \land |E_s(r)| = 0 \\ 0.1 & \text{if } |E_v(r)| \ge 2 \land |E_s(r)| = 0 \\ 0.0 & \text{if } |E_s(r)| > 0 \text{ or } r = \emptyset \end{cases}$$
(1)

#### 4.2 Results

**RQ2 [Optimization]:** Can prompt optimization, leveraging structured verification feedback, improve the effectiveness of LLM-driven formal specification synthesis?

We evaluate each GEPA-optimized prompt against its corresponding seed prompt on both the FormalBench test set (512 tasks) and SpecGenBench (118 tasks, with 2 tasks excluded as they were

<span id="page-5-1"></span>Table 3: Verification Rate (VR%) in Seed Prompts vs GEPA Optimized Prompts

| Prompt Type       | Configuration  | SpecGenBench | FormalBench |
|-------------------|----------------|--------------|-------------|
| Zero-Shot / Plain | Seed Prompt    | 39.83.%      | 17.81%      |
|                   | GEPA Optimized | 46.61(+7)%   | 18.59%      |
| Few-Shot LtM      | Seed Prompt    | 45.66%       | 19.90%      |
|                   | GEPA Optimized | 45.70%       | 19.96%      |
| Few-Shot CoT      | Seed Prompt    | 44.07%       | 19.18%      |
|                   | GEPA Optimized | 46.61 (+2)%  | 19.77%      |

used for few-shot examples during optimization). Our initial results reveal an interesting pattern across the three prompt types as presented in Table 3. The zero-shot seed prompt, which had the lowest baseline performance, shows noticeable improvement after GEPA optimization, suggesting that the optimizer successfully identified and incorporated structural cues missing from the minimal seed prompt. The few-shot CoT prompt also benefits from optimization, achieving a slight gains over its seed. However, the few-shot LtM prompt shows negligible improvement after optimization. This suggests that the LtM prompting strategy already captures much of what GEPA's reflective evolution would discover, leaving little room for further gains within the verifier-based scoring regime.

#### **Summary RQ2**

GEPA-driven prompt optimization improves verifier pass rates for weaker prompt strategies but reaches a performance ceiling for already well-performing prompts. This ceiling raises a deeper question: are the optimized specifications actually correct and complete, or has the optimizer simply learned to produce specifications that satisfy the verifier without meaningfully capturing program behavior? We investigate this question in RQ3.

# 5 Spec-Harness: Evaluation Metrics for Specification Quality

The results of RQ1 and RQ2 rely entirely on verifier pass rates, a binary pass/fail signal, but a fundamental question remains: are these verifier-accepted specifications actually correct and complete? Recent studies [26, 27, 41, 45] addressed such questions for verification-aware programming language such as Dafny, proposing various metrics to evaluate LLMs' generated specifications. The key insight we have from these studies is that a correct specification should be consistent with all valid test pairs, while a complete specification should reject mutated outputs, a vacuous postcondition like ensures true would pass correctness but fail completeness, as it accepts every mutant unchallenged.

Inspired by this formulation, we design four Spec-Harness metrics that adapt the Hoare-triple-based symbolic verification procedure to work with OpenJML and Java programs. These metrics evaluate formal specifications along four dimensions — precondition and postcondition correctness and completeness — enabling a

<span id="page-6-0"></span>![](_page_6_Figure_2.jpeg)

Figure 4: Meaningfully Verified Rate (MVR), for the best prompt configurations. MVR% = % of verified task where the Spec-Harness metrics value, PostCorr >= 0.50 and PostComp >= 0.50

comprehensive assessment of both input and output contracts. We formalize them as follows:

#### 5.1 Preliminaries

Let P be a Java method with signature  $m(\mathbf{x})$ :  $\mathbf{y}$ , where  $\mathbf{x}$  denotes the input parameters and  $\mathbf{y}$  the return value. Let  $\varphi(\mathbf{x}, \mathbf{y})$  be an LLM-generated JML postcondition and  $\psi(\mathbf{x})$  an LLM-generated JML precondition for P. Let  $\mathcal{T} = \{(i_1, o_1), \ldots, (i_n, o_n)\}$  be a set of valid input-output test pairs, i.e., pairs produced by a known-correct execution of P.

*Spec harness.* For a postcondition check against test pair  $(i, o) \in \mathcal{T}$ , we construct a harness stub that replaces the method body with the concrete assignments  $\mathbf{x} := i$ ;  $\mathbf{y} := o$  and submits the following Hoare triple to the verifier:

$$\models \{ \text{true} \} \ \mathbf{x} := i; \ \mathbf{y} := o \ \{ \varphi(\mathbf{x}, \mathbf{y}) \}$$
 (2)

For a precondition check against input i, the stub assigns  $\mathbf{x} := i$  only, and the triple becomes:

$$\models \{ \text{true} \} \ \mathbf{x} := i \ \{ \psi(\mathbf{x}) \}$$
 (3)

In both cases the verifier symbolically checks the Hoare triple using an SMT solver, without executing P.

#### 5.2 Postcondition Metrics

Definition 5.1 (Post-Correctness). A postcondition  $\varphi$  is post-correct with respect to  $\mathcal{T}$  if it raises no false alarms on any known-correct execution. Formally:

$$\operatorname{PostCorr}(\varphi, \mathcal{T}) \ = \ \frac{ \left| \left\{ \left. (i, o) \in \mathcal{T} \right| \mid = \left\{ \operatorname{true} \right\} \right. \mathbf{x} := i; \ \mathbf{y} := o \left. \left\{ \varphi(\mathbf{x}, \mathbf{y}) \right\} \right\} \right| }{ |\mathcal{T}|}$$

A score of 1.0 indicates that  $\varphi$  is consistent with every valid execution in  $\mathcal{T}$ . Note that a vacuous postcondition (e.g., ensures true) trivially achieves PostCorr = 1.0, motivating the complementary completeness metric below.

Definition 5.2 (**Post-Completeness**). Post-completeness measures the discriminative strength of  $\varphi$ : its ability to reject incorrect output values. For each pair  $(i,o) \in \mathcal{T}$ , let  $\mu(o) = \{o'_1, \ldots, o'_k\}$  be a fixed-size set of *output mutants* obtained by type-specific perturbation of o (e.g.,  $o \pm \delta$  for integers, element insertion/deletion for arrays). Define the full mutant pool as:

$$\mathcal{T}_1 = \bigcup_{(i,o) \in \mathcal{T}} \left\{ (i,o') \mid o' \in \mu(o) \right\} \tag{5}$$

Let  $\mathcal{T}_2 \subseteq \mathcal{T}_1$  be the subset of mutant pairs that  $\varphi$  correctly *rejects*:

$$\mathcal{T}_2 = \left\{ (i, o') \in \mathcal{T}_1 \mid \not\models \{\mathsf{true}\} \ \mathsf{x} := i; \ \mathsf{y} := o' \left\{ \varphi(\mathsf{x}, \mathsf{y}) \right\} \right\} \tag{6}$$

Post-completeness is then:

$$PostComp(\varphi, \mathcal{T}) = \frac{|\mathcal{T}_2|}{|\mathcal{T}_1|}$$
 (7)

A score of 1.0 means  $\varphi$  distinguishes the correct output from all injected output faults. A vacuous postcondition scores 0.0, as it admits every mutant unchallenged.

### 5.3 Precondition Metrics

Precondition quality is evaluated over two disjoint input sets derived from the test suite. Let  $\mathcal{T}^+$  denote the set of *valid inputs*, i.e., the input components  $\{i \mid (i,o) \in \mathcal{T}\}$ , and let  $\mathcal{T}^-$  denote a set of *invalid inputs*: boundary and edge-case values that violate the intended domain of P (e.g., null references, out-of-range integers, empty arrays where non-empty is required). The elements of  $\mathcal{T}^-$  are provided explicitly in the test suite, not generated heuristically, ensuring that the domain violations are semantically meaningful by construction.

Definition 5.3 (**Pre-Correctness**). A precondition  $\psi$  is pre-correct with respect to  $\mathcal{T}^+$  if it admits every valid input without false rejection:

$$\operatorname{PreCorr}(\psi, \mathcal{T}^{+}) = \frac{\left|\left\{i \in \mathcal{T}^{+} \mid \models \{\operatorname{true}\} \ \mathbf{x} := i \ \{\psi(\mathbf{x})\}\right\}\right|}{|\mathcal{T}^{+}|} \tag{8}$$

<span id="page-7-1"></span>![](_page_7_Figure_2.jpeg)

Figure 5: Verification Rate (VR%) vs. Meaningfully Verified Rate (MVR%) for the Best Configurations Prompts

A score of 1.0 indicates that  $\psi$  imposes no spurious constraints on any valid caller. An overly restrictive precondition (e.g., one that guards against inputs that are in fact safe) is penalised here.

Definition 5.4 (**Pre-Completeness**). A precondition  $\psi$  is precomplete with respect to  $\mathcal{T}^-$  if it correctly guards against every known-invalid input:

$$\operatorname{PreComp}(\psi, \mathcal{T}^{-}) = \frac{\left| \left\{ i' \in \mathcal{T}^{-} \mid \not\models \left\{ \operatorname{true} \right\} \mathbf{x} := i' \left\{ \psi(\mathbf{x}) \right\} \right\} \right|}{|\mathcal{T}^{-}|} \tag{9}$$

A score of 1.0 indicates that  $\psi$  rejects all boundary and edge-case inputs in  $\mathcal{T}^-$ . A vacuous precondition (e.g., requires true) scores 0.0, as it admits every invalid input unchallenged.

Table 4 summarizes our proposed four Spec-Harness metrics. We apply Spec-Harness to evaluate every task that passed the verifier across both RQ1 and RQ2. This includes specifications generated by classical approaches (Daikon, Houdini), all prompt-based approaches (SpecGen, AutoSpec, FormalBench), and the three GEPA-optimized prompt variants. For each verifier-accepted specification, we compute all four metrics using the corresponding input test pairs from the benchmark. This unified evaluation allows us to directly compare the actual specification quality across all approaches on a common scale, independent of their verifier pass rates.

### 5.4 Results

**RQ3** [Correctness & Completeness]: How correct and complete are verifier-accepted formal specifications, including prompt-optimized ones, when evaluated with Spec-Harness?

<span id="page-7-0"></span>**Table 4: Summary of Spec-Harness Evaluation Metrics**

| Metric   | Spec                              | Stub                                 | Test Set                   | Outcome         |
|----------|-----------------------------------|--------------------------------------|----------------------------|-----------------|
| PostCorr | $\varphi(\mathbf{x}, \mathbf{y})$ | $\mathbf{x} := i; \ \mathbf{y} := o$ | $(i,o) \in \mathcal{T}$    | no false alarm  |
| PostComp | $\varphi(\mathbf{x}, \mathbf{y})$ | $\mathbf{x}:=i; \ \mathbf{y}:=o'$    | $(i,o') \in \mathcal{T}_1$ | mutant rejected |
| PreCorr  | $\psi(\mathbf{x})$                | $\mathbf{x}:=i$                      | $i\in\mathcal{T}^+$        | input admitted  |
| PreComp  | $\psi(\mathbf{x})$                | $\mathbf{x} := i'$                   | $i'\in\mathcal{T}^-$       | input rejected  |

5.4.1 Verification Rate Alone is Misleading: A high VR does not mean that a specification is correct or complete. Figure 5 shows a consistent gap between the Verification Rate (VR) and the Meaningfully Verified Rate (MVR), the fraction of tasks where a specification achieves both PostCorrectness  $\geq 0.50$  and PostCompleteness  $\geq 0.50$  under the Spec-Harness evaluation. This gap appears across all approaches on both benchmarks, revealing that many verifier-accepted specifications are too weak to meaningfully capture the intended method behavior, a problem that VR alone cannot detect.

5.4.2 Classical Approaches Collapse Under Spec-Harness. Houdini's VR of 86% on SpecGenBench and 54% on FormalBench drops to just 2% and 0% MVR respectively (Δ84%, Δ54%). This collapse is due to Houdini's predefined templates that produce trivially weak post-conditions the verifier accepts but Spec-Harness correctly rejects as incomplete. Daikon follows the same pattern, falling from 18% to 1% MVR on SpecGenBench, confirming that classical approaches largely produce formally valid but semantically empty specifications.

5.4.3 Prompt-Based Approaches Drop Sharply Too. Prompt-based approaches show a smaller but still significant VR-to-MVR gap. On SpecGenBench, SpecGen drops from 54% VR to 24% MVR ( $\Delta$ 30%), while AutoSpec and FormalBench prompts fall by  $\Delta$ 15% and  $\Delta$ 13% respectively. On FormalBench, all three approaches collapse to near-zero MVR (Figure 5). From the MVR heatmap (Figure 4), Claude Sonnet 4.6 achieves the highest MVR at 50% on SpecGenBench, while open-weight models remain below 20%.

5.4.4 Spec-Harness Reveals the True Quality Gap. On FormalBench, MVR stays below 11% for all models across all prompt-based approaches (Figure 4), far below their corresponding VR scores reported in RQ1. The Spec-Harness metrics , PostCorrectness and PostCompleteness, together expose two failure modes invisible to the verifier: specifications that are too strong and specifications that are too weak. This confirms that Spec-Harness provides a more honest and necessary measure of specification quality.

#### Summary RQ3

VR consistently overstates specification quality across all approaches. Houdini's near-total MVR collapse exposes that high VR can be driven entirely by trivially weak specifications. Prompt-based approaches retain more meaningful specifications but still show large VR-to-MVR gaps.Spec-Harness is essential for distinguishing genuinely correct and complete specifications from those that merely satisfy the verifier.

# 6 Verification-Guided Agentic Specification Synthesis

Our analysis found that LLMs struggle to generate complete and correct specifications. Without a feedback loop they often produce annotations that fail verification or miss important behavioral properties. To address this gap, we propose VeriAct, framing specification synthesis as an iterative, agent-driven task. The agent proposes a specification, checks it automatically, and receives structured feedback to guide its revision. This closed-loop design transforms prompt-based generation into a guided search over the space of valid specifications, where each iteration brings the candidate closer to one that both the verifier and Spec-Harness accept.

### 6.1 VeriAct

We develop VeriAct on the CodeAct [\[42\]](#page-11-13) paradigm, which equips an LLM agent with the ability to write and execute Python code as its action space within a ReAct-style reasoning loop. Rather than selecting from a fixed set of predefined actions, the agent generates executable code at each step, calls domain-specific tools, and observes their output before deciding what to do next. Veri-Act specializes this framework for formal verification by injecting verification-aware tools into the agent's execution environment and guiding the model with a system prompt tailored to JML synthesis. The agent maintains a shared namespace across steps, so variables and intermediate results persist throughout the refinement process. The agent operates with four purpose-built tools:

- verify\_with\_openjml: Runs OpenJML ESC on a JMLannotated class and returns verification results and errors.
- analyze\_openjml\_errors: Parses verifier logs, classifies failures, and suggests targeted specification fixes.
- run\_spec\_harness: Evaluates specification correctness and completeness against test pairs using symbolic verification.
- task\_complete: Terminates the CodeAct loop when specharness metrics value exceed the predefined threshold.

A typical VeriAct run proceeds as follows. The agent reads the Java method, plans its approach, and drafts an initial JML annotation. It calls the verification tool; if OpenJML reports errors, the agent invokes the error analysis tool to understand the failure and revises accordingly. Once verification passes, the agent runs Spec-Harness to measure specification quality. If both postcondition correctness and completeness exceed the predefined threshold, the agent calls task\_complete and the loop terminates. Otherwise, it continues refining. The full trajectory, thought, code action, and tool output are recorded for later analysis, providing complete transparency

into the agent's reasoning process. Since VeriAct requires tight integration between the LLM, the SMT-based verifier, and the Spec-Harness computation, we implement VeriAct as a standalone system without relying on external agents development frameworks.

# 6.2 Results

RQ4 [VeriAct]: Can VeriAct — a verification-guided agentic loop combining code execution with Spec-Harness feedback — outperform prompt-based and prompt-optimized approaches in synthesizing correct and complete formal specifications?

Using GPT-4o as the base model, we evaluate VeriAct on both SpecGenBench and FormalBench under a fixed configurations, allowing up to three full refinement cycles of verify → error analysis → re-verification → Spec-Harness evaluation. Our results show that VeriAct consistently outperforms strong prompt-based baselines. Compared to the best-performing prompt-optimized configurations, VeriAct achieves a +5% improvement in Meaningfully Verified Rate (MVR) on SpecGenBench. The gains are even larger on FormalBench, where VeriAct improves performance by +12%. The improvements of VeriAct comes from its ability to use verification failures as structured guidance. Instead of relying on implicit reasoning alone, the agent incrementally refines specifications based on concrete error signals and correctness checks, leading to higher completeness and fewer invalid annotations, where prompt-based approaches often fails to capture complete behavioral properties.

The gap between the two benchmarks is worth noting. Spec-GenBench methods tend to be shorter and have clearer behavioral contracts, so a well-prompted LLM already gets reasonably close on the first attempt, there is less room for the loop to help. Formal-Bench, on the other hand, includes methods with richer control flow, edge cases around boundary values, and less obvious postconditions. For these cases, the initial specification often passes OpenJML verification but fails the Spec-Harness completeness check, meaning the specification is valid but too loose. The refinement loop catches exactly this kind of gap: the agent sees that its postcondition admits mutated outputs, tightens the ensures clause, and re-checks. This pattern, verify-pass but harness-fail, driving further refinement, accounts for the majority of productive iterations we observe across both benchmarks. It is also worth noting that in most successful VeriAct runs, the first iteration typically resolves syntax-level and type-level issues flagged by OpenJML, while the second addresses specification weakness exposed by Spec-Harness. Cases that still fail after three cycles tend to required complex quantified expressions, exceptional loop invariants, supportive lemmas and axioms that the model struggles to express in JML regardless of feedback. This suggests that while the agentic loop is effective at closing the gap between a rough draft and a tight specification, it does not eliminate the fundamental limitations of the underlying LLM's ability to reason about complex formal properties.

### Summary RQ4

VeriAct shows that iterative Spec-Harness feedback is more effective than prompts to drive targeted refinements for correct and complete JML synthesis. It outperforms prompt-based approaches with a positive gain on the challenging benchmark.

# 7 Threats to Validity

Internal Validity. We re-implemented and refactored all baseline approaches to ensure a fair comparison under a unified execution environment, using the same OpenJML (21-2.21) and Java (21.0.4) versions, the same verification command across all approaches. For GEPA optimization, we used gpt-4o as both the target and reflection model, which may limit the diversity of optimization feedback. However, this choice isolates the effect of prompt optimization from model variation. VeriAct's configurations:max\_steps=12, planning\_interval=4, and max\_pairs=5 for Spec-Harness test pairs — were set based on preliminary experiments balancing cost and performance. Different configurations may yield different results; however, our preliminary experiments showed that increasing these values in configurations led to significantly longer execution times and higher computational costs without a proportional improvement in specification quality.

External Validity. Our evaluation is conducted on two established benchmarks, SpecGenBench (120 tasks) and FormalBench (662 tasks), both consisting of Java method snippets. While these benchmarks cover a range of task categories and complexity levels, our findings may not directly generalize to other programming languages, specification languages, or larger industrial codebases. As presented in Table [1,](#page-3-0) our prompt-based evaluation covers six LLMs that span both proprietary and open-weight models , but the results may differ with other models or future model versions.

Construct Validity. Spec-Harness measures specification quality through four metrics addressing postcondition and precondition correctness and completeness. Although these metrics capture the core dimensions of specification quality grounded in Hoare-triple reasoning, they do not cover all possible specification properties such as frame conditions or exceptional postconditions. The quality of Spec-Harness evaluation also depends on the test pairs and input cases drawn from the benchmarks; richer test suites could surface additional specification deficiencies. We mitigate this by using the benchmark-provided test suites, which were curated to cover various execution paths and boundary conditions reasoning.

### 8 Related Work

### 8.1 Formal Specification Synthesis

Automated specification synthesis has a long history before LLMs. Classical tools such as Daikon [\[15\]](#page-10-3), Houdini [\[16\]](#page-10-4), and DIG [\[33\]](#page-11-14) infer likely invariants from runtime observations using predefined templates. While useful in constrained settings, they often produce trivial invariants (e.g., nums != null) and struggle with complex functional properties [\[31\]](#page-11-3). LLMs have since enabled a shift toward specification synthesis without exhaustive execution. Early work focused on fine-tuning models for invariant inference [\[9,](#page-10-16) [38\]](#page-11-15), primarily targeting loop invariants in isolation. More recent systems such as SpecGen [\[31\]](#page-11-3) generate full JML specifications through iterative, mutation-guided prompting, while AutoSpec [\[43\]](#page-11-4) combines LLMs with static analysis and code decomposition for verifiable specification generation. Related efforts span other languages and contract types: Janssen et al. [\[23\]](#page-10-17) applied ChatGPT to loop invariant inference for C programs, Endres et al. [\[14\]](#page-10-5) introduces metrics for evaluating NL-to-postcondition approaches and finds

that generated postconditions are generally correct and effective at distinguishing incorrect code. Yang et al. [\[46\]](#page-11-16) used LLM agent networks for automated proof generation in Rust, and Chen et al. [\[12\]](#page-10-18) developed a self-evolving synthesis and fine-tuning cycle for the same language. Across all these approaches, specification quality is assessed primarily through verifier acceptance. Our work departs from this by decoupling generation quality from verification success — Spec-Harness independently measures correctness and completeness deficiencies, and VeriAct uses this structured feedback in a closed-loop agent to drive targeted repairs.

# 8.2 Benchmarking LLM-Synthesized Formal Specifications

Existing benchmarks for evaluating LLM code capabilities — HumanEval [\[11\]](#page-10-19), MBPP [\[6\]](#page-10-20), MBXP [\[5\]](#page-10-21), and SWE-bench [\[24\]](#page-10-22) — measure functional correctness through test-suite execution. However, these protocols do not transfer to specification evaluation, since a specification is not an implementation and cannot be tested by running it. Code reasoning benchmarks such as CRUXEval [\[19\]](#page-10-23), CRUXEval-X [\[44\]](#page-11-17), and REval [\[10\]](#page-10-24) come closer by assessing input/output prediction and execution trace simulation, but they still evaluate single-execution behavior rather than the exhaustive contracts that formal specifications must express. Several recent efforts target specification evaluation directly. He et al. [\[21\]](#page-10-25) evaluate LLMs on postcondition generation tasks, while Cao et al. [\[8\]](#page-10-26) study how fine-tuning affects model performance on formal methods benchmarks. SpecEval [\[30\]](#page-11-18) broadens the scope to preconditions, postconditions, and loop invariants, adding counterfactual analysis to probe sensitivity to semantic-preserving code changes. FormalBench [\[28\]](#page-11-5) establishes a standardized benchmark of Java methods that demands reasoning across the full range of execution behaviors, revealing LLM weaknesses in multi-branch and boundary-condition. Despite this progress, all these benchmarks share a common limitation: they assess specifications as correct or incorrect relative to a ground-truth annotation or verifier oracle, producing a binary signal. Spec-Harness addresses this gap by independently measuring postcondition and precondition correctness and completeness through targeted Hoare-triple queries, making specification deficiencies visible and actionable.

# 9 Conclusion & Future Work

In this paper, we investigated the gap between verifiability and actual specification quality in automated formal specification synthesis. Our empirical study (RQ1) established baseline verifier pass rates, while GEPA-driven prompt optimization (RQ2) pushed these rates further but reached a clear performance ceiling. More critically, our proposed Spec-Harness (RQ3) metrics revealed that a significant fraction of verifier-accepted specifications are incorrect or incomplete, demonstrating that verifier acceptance alone is an insufficient measure of specification quality. To address this, we proposed VeriAct, a verification-guided agentic framework that incorporates Spec-Harness feedback directly into its synthesis loop. Our results (RQ4) showed that VeriAct outperforms both promptbased and prompt-optimized baselines across all four Spec-Harness metrics, producing specifications that are not only verifiable but also correct and complete. Together, Spec-Harness and VeriAct shift

the evaluation and synthesis of formal specifications beyond verifiability toward meaningful behavioral contracts. For future work, we plan to extend Spec-Harness to support additional constructs such as loop invariants, class invariants, and exceptional postconditions.

# 10 Data Availability

All artifacts associated with this study are available here in the § [VeriAct](https://github.com/Mondego/VeriAct) GitHub Repository. It includes implementation and execution scripts for all baseline approaches (Daikon, Houdini, Spec-Gen, AutoSpec, and FormalBench), normalized benchmark datasets (SpecGenBench and FormalBench) with extended test suites, our implementations of the GEPA-based prompt optimizer, Spec-Harness, and VeriAct.

### References

- <span id="page-10-14"></span>[1] Lakshya A Agrawal, Shangyin Tan, Dilara Soylu, Noah Ziems, Rishi Khare, Krista Opsahl-Ong, Arnav Singhvi, Herumb Shandilya, Michael J Ryan, Meng Jiang, Christopher Potts, Koushik Sen, Alex Dimakis, Ion Stoica, Dan Klein, Matei Zaharia, and Omar Khattab. 2026. GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning. In The Fourteenth International Conference on Learning Representations.<https://openreview.net/forum?id=RQm2KQTM5r>
- <span id="page-10-2"></span>[2] Wolfgang Ahrendt, Bernhard Beckert, Daniel Bruns, Richard Bubel, Christoph Gladisch, Sarah Grebing, Reiner Hähnle, Martin Hentschel, Mihai Herda, Vladimir Klebanov, et al. 2014. The KeY platform for verification and analysis of Java programs. In Verified Software: Theories, Tools and Experiments: 6th International Conference, VSTTE 2014, Vienna, Austria, July 17-18, 2014, Revised Selected Papers 6. Springer, 55–71.
- <span id="page-10-13"></span>[3] Anthropic. 2026. Claude. [https://docs.anthropic.com/claude/docs.](https://docs.anthropic.com/claude/docs) [Online], [Accessed: 2026-03-20].
- <span id="page-10-9"></span>[4] Anthropic. 2026. Claude Sonnet 4.6 System Card. [https://www.anthropic.com/](https://www.anthropic.com/claude-sonnet-4-6-system-card) [claude-sonnet-4-6-system-card.](https://www.anthropic.com/claude-sonnet-4-6-system-card) [Online], [Accessed: 2026-03-20].
- <span id="page-10-21"></span>[5] Ben Athiwaratkun, Sanjay Krishna Gouda, Zijian Wang, Xiaopeng Li, Yuchen Tian, Ming Tan, Wasi Uddin Ahmad, Shiqi Wang, Qing Sun, Mingyue Shang, Sujan Kumar Gonugondla, Hantian Ding, Varun Kumar, Nathan Fulton, Arash Farahani, Siddhartha Jain, Robert Giaquinto, Haifeng Qian, Murali Krishna Ramanathan, and Ramesh Nallapati. 2023. Multi-lingual Evaluation of Code Generation Models. In The Eleventh International Conference on Learning Representations, ICLR 2023, Kigali, Rwanda, May 1-5, 2023. OpenReview.net. [https:](https://openreview.net/forum?id=Bo7eeXm6An8) [//openreview.net/forum?id=Bo7eeXm6An8](https://openreview.net/forum?id=Bo7eeXm6An8)
- <span id="page-10-20"></span>[6] Jacob Austin, Augustus Odena, Maxwell I. Nye, Maarten Bosma, Henryk Michalewski, David Dohan, Ellen Jiang, Carrie J. Cai, Michael Terry, Quoc V. Le, and Charles Sutton. 2021. Program Synthesis with Large Language Models. CoRR abs/2108.07732 (2021). arXiv[:2108.07732 https://arxiv.org/abs/2108.07732](https://arxiv.org/abs/2108.07732)
- <span id="page-10-0"></span>[7] Jan Boerman, Marieke Huisman, and Sebastiaan J. C. Joosten. 2018. Reasoning About JML: Differences Between KeY and OpenJML. In Integrated Formal Methods - 14th International Conference, IFM 2018, Maynooth, Ireland, September 5-7, 2018, Proceedings (Lecture Notes in Computer Science), Carlo A. Furia and Kirsten Winter (Eds.). Springer, 30–46. [doi:10.1007/978-3-319-98938-9\\_3](https://doi.org/10.1007/978-3-319-98938-9_3)
- <span id="page-10-26"></span>[8] Jialun Cao, Yaojie Lu, Meiziniu Li, Haoyang Ma, Haokun Li, Mengda He, Cheng Wen, Le Sun, Hongyu Zhang, Shengchao Qin, Shing-Chi Cheung, and Cong Tian. 2025. From Informal to Formal - Incorporating and Evaluating LLMs on Natural Language Requirements to Verifiable Formal Proofs. In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), ACL 2025, Vienna, Austria, July 27 - August 1, 2025, Wanxiang Che, Joyce Nabende, Ekaterina Shutova, and Mohammad Taher Pilehvar (Eds.). Association for Computational Linguistics, 26984–27003. [https://aclanthology.org/2025.acl](https://aclanthology.org/2025.acl-long.1310/)[long.1310/](https://aclanthology.org/2025.acl-long.1310/)
- <span id="page-10-16"></span>[9] Saikat Chakraborty, Shuvendu K. Lahiri, Sarah Fakhoury, Akash Lal, Madanlal Musuvathi, Aseem Rastogi, Aditya Senthilnathan, Rahul Sharma, and Nikhil Swamy. 2023. Ranking LLM-Generated Loop Invariants for Program Verification. In Findings of the Association for Computational Linguistics: EMNLP 2023, Singapore, December 6-10, 2023 (Findings of ACL, Vol. EMNLP 2023), Houda Bouamor, Juan Pino, and Kalika Bali (Eds.). Association for Computational Linguistics, 9164–9175. [doi:10.18653/V1/2023.FINDINGS-EMNLP.614](https://doi.org/10.18653/V1/2023.FINDINGS-EMNLP.614)
- <span id="page-10-24"></span>[10] Junkai Chen, Zhiyuan Pan, Xing Hu, Zhenhao Li, Ge Li, and Xin Xia. 2024. Evaluating Large Language Models with Runtime Behavior of Program Execution. CoRR abs/2403.16437 (2024). arXiv[:2403.16437](https://arxiv.org/abs/2403.16437) [doi:10.48550/ARXIV.2403.16437](https://doi.org/10.48550/ARXIV.2403.16437)
- <span id="page-10-19"></span>[11] Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Pondé de Oliveira Pinto, Jared Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, Alex Ray, Raul Puri, Gretchen Krueger, Michael Petrov, Heidy Khlaaf, Girish Sastry, Pamela Mishkin, Brooke Chan, Scott Gray, Nick Ryder, Mikhail Pavlov, Alethea Power, Lukasz Kaiser, Mohammad Bavarian, Clemens Winter,

- Philippe Tillet, Felipe Petroski Such, Dave Cummings, Matthias Plappert, Fotios Chantzis, Elizabeth Barnes, Ariel Herbert-Voss, William Hebgen Guss, Alex Nichol, Alex Paino, Nikolas Tezak, Jie Tang, Igor Babuschkin, Suchir Balaji, Shantanu Jain, William Saunders, Christopher Hesse, Andrew N. Carr, Jan Leike, Joshua Achiam, Vedant Misra, Evan Morikawa, Alec Radford, Matthew Knight, Miles Brundage, Mira Murati, Katie Mayer, Peter Welinder, Bob McGrew, Dario Amodei, Sam McCandlish, Ilya Sutskever, and Wojciech Zaremba. 2021. Evaluating Large Language Models Trained on Code. CoRR abs/2107.03374 (2021). arXiv[:2107.03374 https://arxiv.org/abs/2107.03374](https://arxiv.org/abs/2107.03374)
- <span id="page-10-18"></span>[12] Tianyu Chen, Shuai Lu, Shan Lu, Yeyun Gong, Chenyuan Yang, Xuheng Li, Md Rakib Hossain Misu, Hao Yu, Nan Duan, Peng Cheng, Fan Yang, Shuvendu K. Lahiri, Tao Xie, and Lidong Zhou. 2025. Automated Proof Generation for Rust Code via Self-Evolution. In The Thirteenth International Conference on Learning Representations, ICLR 2025, Singapore, April 24-28, 2025. OpenReview.net. [https:](https://openreview.net/forum?id=2NqssmiXLu) [//openreview.net/forum?id=2NqssmiXLu](https://openreview.net/forum?id=2NqssmiXLu)
- <span id="page-10-1"></span>[13] David R Cok. 2011. OpenJML: JML for Java 7 by extending OpenJDK. In NASA Formal Methods: Third International Symposium, NFM 2011, Pasadena, CA, USA, April 18-20, 2011. Proceedings 3. Springer, 472–479.
- <span id="page-10-5"></span>[14] Madeline Endres, Sarah Fakhoury, Saikat Chakraborty, and Shuvendu K. Lahiri. 2024. Can Large Language Models Transform Natural Language Intent into Formal Method Postconditions? Proc. ACM Softw. Eng. 1, FSE (2024), 1889–1912. [doi:10.1145/3660791](https://doi.org/10.1145/3660791)
- <span id="page-10-3"></span>[15] Michael D. Ernst, Jeff H. Perkins, Philip J. Guo, Stephen McCamant, Carlos Pacheco, Matthew S. Tschantz, and Chen Xiao. 2007. The Daikon system for dynamic detection of likely invariants. Sci. Comput. Program. 69, 1-3 (2007), 35–45. [doi:10.1016/J.SCICO.2007.01.015](https://doi.org/10.1016/J.SCICO.2007.01.015)
- <span id="page-10-4"></span>[16] Cormac Flanagan and K. Rustan M. Leino. 2001. Houdini, an Annotation Assistant for ESC/Java. In FME 2001: Formal Methods for Increasing Software Productivity, International Symposium of Formal Methods Europe, Berlin, Germany, March 12-16, 2001, Proceedings (Lecture Notes in Computer Science, Vol. 2021), José Nuno Oliveira and Pamela Zave (Eds.). Springer, 500–517. [doi:10.1007/3-540-45251-6\\_29](https://doi.org/10.1007/3-540-45251-6_29)
- <span id="page-10-8"></span>[17] Google. 2025. Gemini 2.0 Flash Model Card. [https://modelcards.withgoogle.com/](https://modelcards.withgoogle.com/assets/documents/gemini-2-flash.pdf) [assets/documents/gemini-2-flash.pdf.](https://modelcards.withgoogle.com/assets/documents/gemini-2-flash.pdf) [Online], [Accessed: 2026-03-20].
- <span id="page-10-12"></span>[18] Google. 2026. Gemini. [https://ai.google.dev/.](https://ai.google.dev/) [Online], [Accessed: 2026-03-20].
- <span id="page-10-23"></span>[19] Alex Gu, Baptiste Rozière, Hugh James Leather, Armando Solar-Lezama, Gabriel Synnaeve, and Sida Wang. 2024. CRUXEval: A Benchmark for Code Reasoning, Understanding and Execution. In Forty-first International Conference on Machine Learning, ICML 2024, Vienna, Austria, July 21-27, 2024 (Proceedings of Machine Learning Research, Vol. 235), Ruslan Salakhutdinov, Zico Kolter, Katherine A. Heller, Adrian Weller, Nuria Oliver, Jonathan Scarlett, and Felix Berkenkamp (Eds.). PMLR / OpenReview.net, 16568–16621. [https://proceedings.mlr.press/](https://proceedings.mlr.press/v235/gu24c.html) [v235/gu24c.html](https://proceedings.mlr.press/v235/gu24c.html)
- <span id="page-10-11"></span>[20] Daya Guo, Qihao Zhu, Dejian Yang, Zhenda Xie, Kai Dong, Wentao Zhang, Guanting Chen, Xiao Bi, Y. Wu, Y. K. Li, Fuli Luo, Yingfei Xiong, and Wenfeng Liang. 2024. DeepSeek-Coder: When the Large Language Model Meets Programming – The Rise of Code Intelligence. [https://arxiv.org/abs/2401.14196.](https://arxiv.org/abs/2401.14196) arXiv preprint arXiv:2401.14196 (2024). [Online], [Accessed: 2026-03-20].
- <span id="page-10-25"></span>[21] Fusen He, Juan Zhai, and Minxue Pan. 2024. Beyond Code Generation: Assessing Code LLM Maturity with Postconditions. CoRR abs/2407.14118 (2024). arXiv[:2407.14118](https://arxiv.org/abs/2407.14118) [doi:10.48550/ARXIV.2407.14118](https://doi.org/10.48550/ARXIV.2407.14118)
- <span id="page-10-10"></span>[22] Binyuan Hui, Jian Yang, Zeyu Cui, Jiaxi Yang, Dayiheng Liu, Lei Zhang, Tianyu Liu, Jiajun Zhang, Bowen Yu, Kai Dang, et al. 2024. Qwen2.5-Coder Technical Report. [https://arxiv.org/abs/2409.12186.](https://arxiv.org/abs/2409.12186) arXiv preprint arXiv:2409.12186 (2024). [Online], [Accessed: 2026-03-20].
- <span id="page-10-17"></span>[23] Christian Janßen, Cedric Richter, and Heike Wehrheim. 2024. Can ChatGPT support software verification?. In Fundamental Approaches to Software Engineering - 27th International Conference, FASE 2024, Held as Part of the European Joint Conferences on Theory and Practice of Software, ETAPS 2024, Luxembourg City, Luxembourg, April 6-11, 2024, Proceedings (Lecture Notes in Computer Science, Vol. 14573), Dirk Beyer and Ana Cavalcanti (Eds.). Springer, 266–279. [doi:10.1007/](https://doi.org/10.1007/978-3-031-57259-3_13) [978-3-031-57259-3\\_13](https://doi.org/10.1007/978-3-031-57259-3_13)
- <span id="page-10-22"></span>[24] Carlos E. Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, and Karthik R. Narasimhan. 2024. SWE-bench: Can Language Models Resolve Real-world Github Issues?. In The Twelfth International Conference on Learning Representations, ICLR 2024, Vienna, Austria, May 7-11, 2024. OpenReview.net. <https://openreview.net/forum?id=VTF8yNQM66>
- <span id="page-10-15"></span>[25] Omar Khattab, Arnav Singhvi, Paridhi Maheshwari, Zhiyuan Zhang, Keshav Santhanam, Sri Vardhamanan, Saiful Haq, Ashutosh Sharma, Thomas T. Joshi, Hanna Moazam, Heather Miller, Matei Zaharia, and Christopher Potts. 2023. DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines. CoRR abs/2310.03714 (2023). arXiv[:2310.03714](https://arxiv.org/abs/2310.03714) [doi:10.48550/ARXIV.2310.03714](https://doi.org/10.48550/ARXIV.2310.03714)
- <span id="page-10-6"></span>[26] Shuvendu K. Lahiri. 2024. Evaluating LLM-driven User-Intent Formalization for Verification-Aware Languages. In Formal Methods in Computer-Aided Design, FMCAD 2024, Prague, Czech Republic, October 15-18, 2024, Nina Narodytska and Philipp Rümmer (Eds.). IEEE, 142–147. [doi:10.34727/2024/ISBN.978-3-85448-065-](https://doi.org/10.34727/2024/ISBN.978-3-85448-065-5_19) [5\\_19](https://doi.org/10.34727/2024/ISBN.978-3-85448-065-5_19)
- <span id="page-10-7"></span>[27] Shuvendu K Lahiri. 2026. Intent Formalization: A Grand Challenge for Reliable Coding in the Age of AI Agents. arXiv preprint arXiv:2603.17150 (2026).

- <span id="page-11-5"></span>[28] Thanh Le-Cong, Bach Le, and Toby Murray. 2025. Can LLMs Reason About Program Semantics? A Comprehensive Evaluation of LLMs on Formal Specification Inference. In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), ACL 2025, Vienna, Austria, July 27 - August 1, 2025, Wanxiang Che, Joyce Nabende, Ekaterina Shutova, and Mohammad Taher Pilehvar (Eds.). Association for Computational Linguistics, 21991–22014.<https://aclanthology.org/2025.acl-long.1068/>
- <span id="page-11-0"></span>[29] Gary T Leavens, Albert L Baker, and Clyde Ruby. 2006. Preliminary design of JML: A behavioral interface specification language for Java. ACM SIGSOFT Software Engineering Notes 31, 3 (2006), 1–38.
- <span id="page-11-18"></span>[30] Lezhi Ma, Shangqing Liu, Lei Bu, Shangru Li, Yida Wang, and Yang Liu. 2024. SpecEval: Evaluating Code Comprehension in Large Language Models via Program Specifications. CoRR abs/2409.12866 (2024). arXiv[:2409.12866](https://arxiv.org/abs/2409.12866) [doi:10.48550/ARXIV.2409.12866](https://doi.org/10.48550/ARXIV.2409.12866)
- <span id="page-11-3"></span>[31] Lezhi Ma, Shangqing Liu, Yi Li, Xiaofei Xie, and Lei Bu. 2025. SpecGen: Automated Generation of Formal Program Specifications via Large Language Models. In 47th IEEE/ACM International Conference on Software Engineering, ICSE 2025, Ottawa, ON, Canada, April 26 - May 6, 2025. IEEE, 16–28. [doi:10.1109/ICSE55347.2025.00129](https://doi.org/10.1109/ICSE55347.2025.00129)
- <span id="page-11-2"></span>[32] Facundo Molina, Marcelo d'Amorim, and Nazareno Aguirre. 2022. Fuzzing class specifications. In Proceedings of the 44th International Conference on Software Engineering. 1008–1020.
- <span id="page-11-14"></span>[33] ThanhVu Nguyen, Deepak Kapur, Westley Weimer, and Stephanie Forrest. 2014. DIG: A Dynamic Invariant Generator for Polynomial and Array Invariants. ACM Trans. Softw. Eng. Methodol. 23, 4 (2014), 30:1–30:30. [doi:10.1145/2556782](https://doi.org/10.1145/2556782)
- <span id="page-11-1"></span>[34] Jeremy W Nimmer and Michael D Ernst. 2002. Automatic generation of program specifications. ACM SIGSOFT Software Engineering Notes 27, 4 (2002), 229–239.
- <span id="page-11-6"></span>[35] OpenAI. 2024. GPT-4o. [https://platform.openai.com/docs/models/gpt-4o.](https://platform.openai.com/docs/models/gpt-4o) [Online], [Accessed: 2026-03-20].
- <span id="page-11-8"></span>[36] OpenAI. 2026. OpenAI. [https://platform.openai.com/docs/models.](https://platform.openai.com/docs/models) [Online], [Accessed: 2026-03-20].
- <span id="page-11-9"></span>[37] Krista Opsahl-Ong, Michael J. Ryan, Josh Purtell, David Broman, Christopher Potts, Matei Zaharia, and Omar Khattab. 2024. Optimizing Instructions and Demonstrations for Multi-Stage Language Model Programs. In Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing, EMNLP 2024, Miami, FL, USA, November 12-16, 2024, Yaser Al-Onaizan, Mohit Bansal, and Yun-Nung Chen (Eds.). Association for Computational Linguistics, 9340–9366. [doi:10.18653/V1/2024.EMNLP-MAIN.525](https://doi.org/10.18653/V1/2024.EMNLP-MAIN.525)
- <span id="page-11-15"></span>[38] Kexin Pei, David Bieber, Kensen Shi, Charles Sutton, and Pengcheng Yin. 2023. Can Large Language Models Reason about Program Invariants?. In International Conference on Machine Learning, ICML 2023, 23-29 July 2023, Honolulu, Hawaii, USA (Proceedings of Machine Learning Research, Vol. 202), Andreas Krause, Emma Brunskill, Kyunghyun Cho, Barbara Engelhardt, Sivan Sabato, and Jonathan Scarlett (Eds.). PMLR, 27496–27520. [https://proceedings.mlr.press/v202/pei23a.](https://proceedings.mlr.press/v202/pei23a.html) [html](https://proceedings.mlr.press/v202/pei23a.html)
- <span id="page-11-7"></span>[39] Baptiste Rozière, Jonas Gehring, Fabian Gloeckle, Sten Sootla, Itai Gat, Xiaoqing Ellen Tan, Yossi Adi, Jingyu Liu, Romain Sauvestre, Tal Remez, Jérémy Rapin, Artyom Kozhevnikov, Ivan Evtimov, Joanna Bitton, Manish Bhatt, Cristian Canton Ferrer, Aaron Grattafiori, Wenhan Xiong, Alexandre Défossez, Jade Copet,

- Faisal Azhar, Hugo Touvron, Louis Martin, Nicolas Usunier, Thomas Scialom, and Gabriel Synnaeve. 2023. Code Llama: Open Foundation Models for Code. [https://arxiv.org/abs/2308.12950.](https://arxiv.org/abs/2308.12950) arXiv preprint arXiv:2308.12950 (2023). [Online], [Accessed: 2026-03-20].
- <span id="page-11-10"></span>[40] Bhaskarjit Sarmah, Kriti Dutta, Anna Grigoryan, Sachin Tiwari, Stefano Pasquali, and Dhagash Mehta. 2024. A Comparative Study of DSPy Teleprompter Algorithms for Aligning Large Language Models Evaluation Metrics to Human Evaluation. CoRR abs/2412.15298 (2024). arXiv[:2412.15298](https://arxiv.org/abs/2412.15298) [doi:10.48550/ARXIV.](https://doi.org/10.48550/ARXIV.2412.15298) [2412.15298](https://doi.org/10.48550/ARXIV.2412.15298)
- <span id="page-11-11"></span>[41] Chuyue Sun, Ying Sheng, Oded Padon, and Clark W. Barrett. 2024. Clover: Closed-Loop Verifiable Code Generation. In AI Verification - First International Symposium, SAIV 2024, Montreal, QC, Canada, July 22-23, 2024, Proceedings (Lecture Notes in Computer Science, Vol. 14846), Guy Avni, Mirco Giacobbe, Taylor T. Johnson, Guy Katz, Anna Lukina, Nina Narodytska, and Christian Schilling (Eds.). Springer, 134–155. [doi:10.1007/978-3-031-65112-0\\_7](https://doi.org/10.1007/978-3-031-65112-0_7)
- <span id="page-11-13"></span>[42] Xingyao Wang, Yangyi Chen, Lifan Yuan, Yizhe Zhang, Yunzhu Li, Hao Peng, and Heng Ji. 2024. Executable Code Actions Elicit Better LLM Agents. In Forty-first International Conference on Machine Learning, ICML 2024, Vienna, Austria, July 21-27, 2024 (Proceedings of Machine Learning Research), Ruslan Salakhutdinov, Zico Kolter, Katherine A. Heller, Adrian Weller, Nuria Oliver, Jonathan Scarlett, and Felix Berkenkamp (Eds.). PMLR / OpenReview.net, 50208–50232. [https:](https://proceedings.mlr.press/v235/wang24h.html) [//proceedings.mlr.press/v235/wang24h.html](https://proceedings.mlr.press/v235/wang24h.html)
- <span id="page-11-4"></span>[43] Cheng Wen, Jialun Cao, Jie Su, Zhiwu Xu, Shengchao Qin, Mengda He, Haokun Li, Shing-Chi Cheung, and Cong Tian. 2024. Enchanting Program Specification Synthesis by Large Language Models Using Static Analysis and Program Verification. In Computer Aided Verification - 36th International Conference, CAV 2024, Montreal, QC, Canada, July 24-27, 2024, Proceedings, Part II (Lecture Notes in Computer Science, Vol. 14682), Arie Gurfinkel and Vijay Ganesh (Eds.). Springer, 302–328. [doi:10.1007/978-3-031-65630-9\\_16](https://doi.org/10.1007/978-3-031-65630-9_16)
- <span id="page-11-17"></span>[44] Ruiyang Xu, Jialun Cao, Yaojie Lu, Ming Wen, Hongyu Lin, Xianpei Han, Ben He, Shing-Chi Cheung, and Le Sun. 2025. CRUXEVAL-X: A Benchmark for Multilingual Code Reasoning, Understanding and Execution. In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), ACL 2025, Vienna, Austria, July 27 - August 1, 2025, Wanxiang Che, Joyce Nabende, Ekaterina Shutova, and Mohammad Taher Pilehvar (Eds.). Association for Computational Linguistics, 23762–23779. [https://aclanthology.](https://aclanthology.org/2025.acl-long.1158/) [org/2025.acl-long.1158/](https://aclanthology.org/2025.acl-long.1158/)
- <span id="page-11-12"></span>[45] Chuanhao Yan, Fengdi Che, Xuhan Huang, Xu Xu, Xin Li, Yizhi Li, Xingwei Qu, Jingzhe Shi, Zhuangzhuang He, Chenghua Lin, Yaodong Yang, Binhang Yuan, Hang Zhao, Yu Qiao, Bowen Zhou, and Jie Fu. 2025. Re:Form - Reducing Human Priors in Scalable Formal Software Verification with RL in LLMs: A Preliminary Study on Dafny. CoRR abs/2507.16331 (2025). arXiv[:2507.16331](https://arxiv.org/abs/2507.16331) [doi:10.48550/ARXIV.2507.16331](https://doi.org/10.48550/ARXIV.2507.16331)
- <span id="page-11-16"></span>[46] Chenyuan Yang, Xuheng Li, Md Rakib Hossain Misu, Jianan Yao, Weidong Cui, Yeyun Gong, Chris Hawblitzel, Shuvendu K. Lahiri, Jacob R. Lorch, Shuai Lu, Fan Yang, Ziqiao Zhou, and Shan Lu. 2025. AutoVerus: Automated Proof Generation for Rust Code. Proc. ACM Program. Lang. 9, OOPSLA2 (2025), 3454–3482. [doi:10.](https://doi.org/10.1145/3763174) [1145/3763174](https://doi.org/10.1145/3763174)