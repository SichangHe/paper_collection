# **KAPILOT: LLM-Assisted Generation of Kani Specifications for Unsafe Rust Verification**

MINGHUA WANG\*, Ant Group, China YUXI LING<sup>†</sup>, National University of Singapore, Singapore MINGZHI GAO, Ant Group, China YUWEI LIU, Ant Group, China LIN HUANG, Ant Group, China

Rust's ownership and type system provide strong memory safety guarantees, but unsafe code still presents memory safety risks. Formal verification is crucial for ensuring memory safety, but writing precise specifications for unsafe Rust is challenging and largely manual. Large language models (LLMs) have shown promise in generating formal specifications but are often code-centric, prone to inheriting implementation flaws, and lack systematic quality assessment.

In this paper, we present KAPILOT, a multi-agent framework for automatically generating specifications to verify unsafe Rust memory safety using Kani. The process begins with lightweight program analysis and proof harness generation. The *SafetyReq* agent extracts a concise, refined list of safety requirements from the target Rust function's documentation, which guides the *SpecGenerate* agent in producing initial specifications that specify memory safety concerns. Then, the specifications are iteratively refined through a generate–precheck–verify loop involving *SpecGenerate*, *SpecPrecheck*, and *SpecVerify* agents, which assess quality and feed errors back. By executing this loop multiple times, KAPILOT generates a set of candidate specifications. Finally, the shuffle-and-implication strategy is applied to systematically determine the best specification from these candidates. We evaluated KAPILOT on 54 unsafe Rust functions with ground truth and 70 without. KAPILOT achieved 88.9% and 71.4% specification generation success, respectively, with 57.4% of generated specifications equivalent to or stronger than the ground truth. Compared with AutoSpec, KAPILOT produces 14.8% more verifiable specifications and 25.9% more equivalent-or-better specifications.

#### **ACM Reference Format:**

Minghua Wang, Yuxi Ling, Mingzhi Gao, Yuwei Liu, and Lin Huang. 2026. KAPILOT: LLM-Assisted Generation of Kani Specifications for Unsafe Rust Verification. 1, 1 (July 2026), 22 pages. https://doi.org/10.1145/nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn

#### 1 Introduction

Rust provides strong memory-safety guarantees at compile time through its strict type system and ownership model. However, Unsafe Rust allows programmers to explicitly bypass certain compiler checks in exchange for greater performance or expressiveness. While indispensable in systems programming, unsafe code introduces the risk of undefined behaviour (UB), which can lead to severe memory-safety vulnerabilities. Formal verification offers a principled solution by reasoning exhaustively about program behaviour under precise assumptions, enabling reliable proofs of the

Authors' Contact Information: Minghua Wang, Ant Group, Beijing, China, minghua.wmh@antgroup.com; Yuxi Ling, National University of Singapore, Singapore, yuxiling@u.nus.edu; Mingzhi Gao, Ant Group, Beijing, China, gaomingzhi.gmz@antgroup.com; Yuwei Liu, Ant Group, Hangzhou, Zhejiang, China, lyw458372@antgroup.com; Lin Huang, Ant Group, Beijing, China, linyu.hl@antgroup.com.

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than the author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from permissions@acm.org.

© 2026 Copyright held by the owner/author(s). Publication rights licensed to ACM.

ACM XXXX-XXXX/2026/7-ART

https://doi.org/10.1145/nnnnnn.nnnnnnn

<sup>\*</sup>Corresponding author.

<sup>†</sup>Work done during an internship at Ant Group.

absence of UB. However, formalisation of safety properties, *i.e.*, writing specifications, especially for Unsafe Rust, as the very first step of formal verification, relies heavily on manual effort from human experts, making it time-consuming and error-prone. To make the formal verification scalable, automated specification generation is desired.

Recently, large language models (LLMs) have demonstrated strong capabilities in code-related tasks, motivating LLM-assisted specification generation [1, 6, 23, 25, 34, 35]. For example, AutoSpec [34] generates verifiable ACSL specifications by iteratively interacting with Frama-C, while SpecGen [23] synthesises specifications directly from source code and refines them through mutation strategies when verification fails. Although these LLM-assisted approaches lower the barrier to specification generation, they all share the following challenges in the context of Unsafe Rust: C1: Code-centric specification generation inherits implementation flaws. Existing approaches [23, 34] derive specifications directly from the code. When the implementation contains defects or fails to explicitly expose its safety assumptions, the resulting specifications tend to inherit these limitations, reducing their effectiveness in uncovering missing or violated safety requirements. C2: LLM-generated specifications lack stability. LLMs may produce specifications with inconsistent quality, including incomplete coverage of documented safety concerns, overly restrictive preconditions, overly permissive postconditions, and limited robustness across different instantiations. C3: Specification quality evaluation is hard to automate systematically. Prior works [23, 34, 35] rely on manual inspection to evaluate specification quality. Verification success implies syntactic correctness and verifiability, without ensuring alignment with safety requirements. For example, contradictory preconditions may degenerate into vacuous specifications, allowing verification to succeed without meaningful program behaviour constraints. Moreover, the strength or completeness of specifications lacks objective automated evaluation approaches, leading to subjective and potentially inconsistent assessments.

To address these challenges, we propose KAPILOT, a multi-agent framework of automated specification generation to verify unsafe Rust code in Kani. KAPILOT consists of five specialised agents: Safety Requirement Analysis (*SafetyReq*), Harness Generation (*HarnGen*), Specification Generation (*SpecGenerate*), Specification Precheck (*SpecPrecheck*), and Specification Verification (*SpecVerify*), that collaboratively generate, assess, validate, and refine formal specifications.

KAPILOT takes the documentation, instead of the code, as the primary source to specify safety properties for the target function. Unlike functional correctness, which can be inferred from the code, hidden safety properties are usually revealed by the documentation. By summarising an unstructured description in natural language to a concise list of safety requirements, KAPILOT produces a more structured target for subsequent specification generation (addressing C1).

Guided by this safety requirement list, *SpecGenerate* constructs formal specifications using Kani primitives. Instead of sending them to Kani for verification, *SpecPrecheck* performs a precheck using LLMs, assessing whether they fully cover all documented safety concerns and whether their semantics are aligned with safety requirements, not overly strong or weak. Specifications that fail this precheck are fed back to the *SpecGenerate* agent for refinement and re-assessment, ensuring the stable quality of specifications before the verification (addressing C2).

Finally, KAPILOT invokes Kani to verify the specifications against the target function. A generate–evaluate–verify loop is designed to iteratively repair the specification. Particularly, when verification succeeds, vacuity checks are applied to ensure that postconditions are not trivially satisfied due to contradictory preconditions. After KAPILOT constructs a set of specification candidates, a *shuffle-and-implication* strategy is applied to select optimal preconditions, postconditions, and loop invariants. KAPILOT derives high-quality final specifications (addressing C3).

We evaluate KaPilot on two benchmark datasets: 54 Rust functions with ground-truth specifications (GoldSet) and 70 functions without ground truth (ULSet). On GoldSet, KaPilot achieves an

88.9% specification generation success rate, with 57.4% of the generated specifications being semantically equivalent to or better than the ground truth. On ULSet, KaPilot successfully generates specifications for 71.4% of the functions. Compared with AutoSpec on GoldSet, KaPilot achieves a 14.8% higher success rate in generating verifiable specifications and a 25.9% higher success rate in generating specifications that are semantically equivalent to or better than the ground truth. Apart from that, ablation studies confirmed the effectiveness of KaPilot's components.

Contributions. We summarise the contributions as follows:

- We present and open-source KaPilot[1](#page-2-0) , a fully automated, multi-agent framework for generating Kani specifications to verify memory safety in unsafe Rust code. We design safety requirement extraction that improves LLMs in specifying safety properties. We also introduce a lightweight shuffle-and-implication strategy to KaPilot that further improves the specification quality.
- We design a multi-agent specification generation pipeline that decomposes the verification task into specialised agents. These agents collaborate in a generate-precheck-verify loop, enabling specification generation not only verifiable but also semantically aligned with refined safety requirements and of appropriate strength.
- We conduct an extensive evaluation of KaPilot on GoldSet and ULSet datasets, demonstrating its effectiveness in the safety verification of unsafe Rust code.

## 2 Background

## 2.1 Unsafe Rust and Undefined Behaviour

Rust allows unsafe operations that can potentially violate the memory-safety guarantees of the Rust compiler and transfer the responsibility of ensuring the code safety from the Rust compiler to programmers, that is, unsafe Rust [\[4\]](#page-20-4). The unsafe gives programmers the power to dereference a raw pointer, access or modify a mutable static variable, and access fields of unionS. It is easy to identify unsafe Rust code, since it must be marked with the unsafe keyword, e.g., unsafe fn, unsafe trait, and unsafe {}. [Fig. 1a](#page-3-0) presents an example excerpted from "library/core/src/ffi/c\_str.rs" in the Rust standard library. To calculate the length of a null-terminated string, it dereferences the raw pointer ptr and calls an external function from the C standard library with safety condition statements specified at lines 11 and 19. These safety conditions can be expressed informally, as natural language comments, or formally, as explicit preconditions. The safety of the unsafe Rust code critically depends on these safety conditions being upheld by programmers.

Rust programmers are encouraged to wrap unsafe code within safe abstractions and expose only safe APIs. Such safe abstractions are pervasive in the Rust standard library, where unsafe implementations cover many core functionalities. Within these abstractions, programmers are responsible for ensuring that the calling of unsafe code satisfies its safety condition in the safe abstraction. Otherwise, the violation of safety conditions may lead to undefined behaviour (UB), thereby bringing the regular Rust potential memory safety problems. The Rust Reference [\[30\]](#page-21-3) provides a not exhaustive list of UB, like mutating immutable bytes, producing invalid values, etc.

## <span id="page-2-1"></span>2.2 Safety Verification in Kani

Kani [\[31\]](#page-21-4) is a bit-precise bounded model checker for Rust that supports the verification of unsafe Rust code. It detects memory-safety violations such as null pointer dereferences and use-after-free, as well as runtime panics caused by behaviour including out-of-bounds accesses and arithmetic overflows. Kani performs bounded model checking using proof harnesses with symbolic inputs, exhaustively exploring program executions up to a given bound. Recent versions of Kani provide

<span id="page-2-0"></span><sup>1</sup>https://github.com/MinghuaWang/KaPilot

```
#[requires(!ptr.is null())]
     /// Calculate the length of a nul-terminated string.
                                                                      2
     /// Defers to C's `strlen` when possible.
2
                                                                             let mut next = ptr; let mut found_null = false;
     /// # Safetv
3
                                                                             while kani::mem::can_dereference(next) {
     /// The pointer must point to a valid buffer that
     /// contains a NUL terminator. The NUL must be
/// located within `isize::MAX` from `ptr`.
                                                                      5
                                                                                if unsafe { *next == 0 } {
                                                                                   found_null = true;
                                                                                   break:
     const unsafe fn strlen(ptr: *const c_char) -> usize {
                                                                      8
Q
       const_eval_select!(
                                                                      9
                                                                                next = next.wrapping_add(1);
10
         @capture { s: *const c_char = ptr } -> usize:
                                                                      10
                                                                      11
                                                                             if (next.addr()-ptr.addr()) >= isize::MAX as usize {
         if const {
11
                                                                      12
12
           let mut len = 0;
            // SAFETY: Outer caller has provided
                                                                      13
13
            // a pointer to a valid C string.
                                                                      14
                                                                              found_null
14
                                                                      15
                                                                           3)]
15
            while unsafe { *s.add(len) } != 0 {len += 1;}
                                                                           #[ensures(|&result| result < isize::MAX as usize &&
16
            len
                                                                      16
                                                                      17
                                                                               unsafe { *ptr.add(result) } == 0)]
17
         } else {
            unsafe extern "C" {
18
                                                                      18
                                                                           const unsafe fn strlen(ptr: *const c char) -> usize {
              /// Provided by libc or compiler_builtins.
19
                                                                     19
20
              fn strlen(s: *const c_char) -> usize;
                                                                     20
                                                                          #[kani::proof_for_contract(strlen)]
                                                                      21
21
                                                                     22 #[kani::unwind(33)]
            // SAFETY: Outer caller has provided
22
            // a pointer to a valid C string.
                                                                     23
                                                                           fn check_strlen_contract() {
23
            unsafe { strlen(s) }
                                                                               const MAX_SIZE: usize = 32;
24
                                                                     25
                                                                               let mut string: [u8; MAX_SIZE] = kani::any();
25
         }
                                                                     26
                                                                               let ptr = string.as_ptr() as *const c_char;
26
       )
27
     }
                                                                     27
                                                                               unsafe {strlen(ptr);}
                                                                          }
                                                                     28
             (a) The unsafe Rust function
                                                                               (b) The Kani contract and harness
```

Fig. 1. An unsafe function from the Rust standard library and its Kani verification

specification primitives for writing function contracts and loop invariants, enabling modular verification. Functions can be verified against their specifications and then treated as safe abstractions at call sites, allowing verification results to be composed across the program. This significantly reduces verification cost for code with deep call chains or repeated function invocations.

To illustrate how Kani verifies the safety of an unsafe Rust function, Fig. 1b shows the code added with the Kani contract and harness. The precondition and postcondition with requires and ensures clauses specify the safety requirements given by developers in the function's descriptions. The check\_strlen\_contract harness function at line 23 is the entry point of Kani verification. The annotation kani::proof\_for\_contract specifies that the Kani will verify the function via contracts at lines 1-20. In the Kani harness, it declares an arbitrary string of length 32 as the input parameter of the strlen function and invokes the function within an unsafe block. Then, Kani will perform model checking and check whether the specification is satisfiable.

#### <span id="page-3-1"></span>3 Approach

#### 3.1 Overview

We propose KaPilot, a multi-agent framework to automate the specification generation for unsafe Rust programs in Kani. Fig. 2 shows the overview of KaPilot.

It takes the source code of the target functions and their documentation as inputs. In the preparation stage, it first extracts metadata from the source code via lightweight program analysis, including function signatures, call graph, and function description. Then, agent *HarnGen* constructs a Kani proof harness for the target function (details in Sec. 3.2). Meanwhile, *SafetyReq* extracts safety requirements based on the documentation written in natural language (details in Sec. 3.3). For every processed function, its metadata and safety requirements will be stored in a shared knowledge database for further *HarnGen* and *SpecGenerate*.

With the Kani harness and safety requirements ready, the agent *SpecGenerate* generates formal specifications for the target function consisting of preconditions, postconditions, and loop invariants

<span id="page-4-0"></span>![](_page_4_Figure_2.jpeg)

Fig. 2. The pipeline of KAPILOT.

using Kani primitives (details in Sec. 3.4). Before sending it to Kani to verify, KAPILOT performs a precheck in *SpecPrecheck* to eliminate simple syntax errors and check whether it covers all mentioned safety requirements. If the specification gets a low score, it would be fed back to *SpecGenerate* for refinement. KAPILOT repeats this step till it reaches the maximum iterations or passes the checking of *SpecPrecheck* (details in Sec. 3.5). The passed specification is submitted to the *SpecVerify* agent, which invokes Kani for bounded model checking. Specifications that successfully pass the verification in Kani are marked as candidate specifications (details in Sec. 3.6).

Although candidate specifications have been evaluated and verified by the *SpecPrecheck* and *SpecVerify* agents, their quality may still be suboptimal, for instance, with overly restrictive preconditions or insufficiently precise postconditions. To mitigate this issue, the *specification shuffle* and implication strategy is designed to select the best specification from the candidates (details in Sec. 3.7). Once the final specification is determined, KAPILOT stores it in the shared knowledge database. These high-quality specifications can be retrieved and reused as few-shot examples to guide LLMs in generating specifications for new Rust functions.

#### <span id="page-4-1"></span>3.2 Preparation

The preparation stage here performs preprocessing on the existing codebase and documentation, containing two tasks: 1) metadata extraction; 2) the Kani harness generation.

- 3.2.1 Metadata extraction. In this step, KAPILOT extracts the metadata of the target function via a lightweight static program analysis, including function signature, function descriptions, and available public methods in the code base. When identifying a Rust type, particularly since it can be either concrete or a trait, we record its definition and, additionally, the inherited traits if it is concrete and concrete types implemented from it if it is a trait. Additionally, we extract available public methods for each target function, which can serve as auxiliary functions when constructing preconditions, postconditions, and loop invariants in later specification generation. All metadata is recorded in a shared knowledge database for later specification generation.
- 3.2.2 Harness generation. As mentioned in Sec. 2.2, the Kani harness is essentially a Rust function that invokes the target function with all input parameters initialised in Kani types, such as kani::any(), which serves as the entry point of Kani. The agent HarnGen constructs the proof

harness for the target function using AutoHarness [10]. However, it cannot handle complex scenarios: parameters are not Rust primitive types; parameters require extra implementation of traits beforehand; user-defined data types cannot be directly supported in Kani; *etc.* To make this step fully automatic, *HarnGen* employs LLMs to fill in necessary but missing parameter declarations for failed cases from AutoHarness and checks target function is invoked correctly in the harness.

#### <span id="page-5-0"></span>3.3 Safety Requirements Extraction

Before the specification generation, we need to identify the safety properties to verify for the target function. Unlike functional correctness, safety properties are usually hidden in the code. The most direct source of such properties is the documentation, *i.e.*, function description, which is written in natural language. However, such descriptions are often incomplete, distributed across cross-referenced APIs, or encoded implicitly as behavioural constraints rather than explicitly stated in Safety or Panics sections (e.g., pointer-distance computations must not overflow <code>isize</code>). And descriptions sometimes use variables that are not aligned with function parameters, or safety related description are encoded implicitly as behavioural constraints rather than explicitly stated in Safety or Panics sections (e.g., pointer-distance computations must not overflow <code>isize</code>). For example, in Fig. 3a, the documentation of <code>offset\_from\_unsigned</code> does not fully contain all relevant safety concerns, and highlighted lines require cross-referencing the related function <code>offset\_from</code> elsewhere in the codebase, as shown in Fig. 3b.

In this case, we design an agentic LLM, *SafetyReq*, that iteratively extracts, evaluates, and refines structured safety requirement lists from unstructured and possibly low-quality documentation, which serves as the specification target for subsequent specification generation and verification stages. Fig. 3c presents the resulting safety requirement list distilled by *SafetyReq*.

First, we identify the allowed sources from which safety requirements may be extracted: the *Safety* and *Panics* sections in the target function's preceding documentation, as well as relevant safety-related descriptions introduced through cross-references. Then, the LLM is constrained to generate safety requirements exclusively from these sources and to follow the explicit rules below:

- (R1) Scope. Each requirement must constrain a property related to memory safety or Rust runtime panics of the target function, or the function behaviours related to runtime panics.
- (R2) Atomicity. Each requirement must consist of a single sentence describing exactly one safety property in a precise and concise manner.
- (R3) Variable Reference: A requirement may refer only to the target function's parameters, return values, or generics; if derived from a cross-reference, all referenced variables must be correctly mapped to the target function's interface.
- (R4) Source Traceability: Each requirement must end with a citation in the form <src>--<sec>: <statement>, where <src> denotes either the target function (TF) or a cross reference (CR), <sec> denotes a *Safety* or *Panics* section; <statement> is the original documentation text.
- (R5) Exclusivity. There must be no duplicates between requirements, no logical implications between two requirements, and no contradictions between two requirements.
- (R6) Completeness. They cover all safety constraints from the allowed sources.

Rules R1–R3 ensure that each extracted safety requirement precisely constrains the memory safety behaviour of the target function, while R4 enables subsequent agents to validate the provenance of each requirement. In addition, rules (R5) Exclusivity and (R6) Completeness ensure that different safety requirements describe distinct safety concerns and that the entire set collectively covers all safety-related statements in the documentation.

```
/// # Safety
/// - The distance between the pointers must be
 non-negative (`self >= origin`)
/// - *All* the safety conditions of
[`offset_from`](#method.offset_from) apply to this
method as well; see it for the full details.
/// Importantly, despite the return type of this
method being able to represent a larger offset, it's
still *not permitted* to pass pointers which differ
by more than `isize::MAX` *bytes*. As such, the
result of this method will always be less than or
equal to `isize::MAX as usize`.
/// # Panics
/// This function panics if `T` is a Zero-Sized Type
("ZST").
pub const unsafe fn offset_from_unsigned(self,
subtracted: NonNull<T>) -> usize where T: Sized ...
(a) offset_from_unsigned's safety concerns,
some of which are documented in offset_from.
                                                       /// # Safety
                                                       /// If any of the following conditions are violated, the
                                                       result is Undefined Behavior:
                                                       /// * `self` and `origin` must either
                                                       /// * point to the same address, or
                                                       /// * both be *derived from* a pointer to the same
                                                       [allocated object], and the memory range between the two
                                                       pointers must be in bounds of that object.
                                                       /// * The distance between the pointers, in bytes, must be
                                                       an exact multiple of the size of `T`.
                                                       /// As a consequence, the absolute distance between the
                                                       pointers, in bytes, computed on mathematical integers
                                                       (without "wrapping around"), cannot overflow an `isize`.
                                                       This is implied by the in-bounds requirement, and the fact
                                                       that no allocated object can be larger than `isize::MAX`
                                                       bytes.
                                                       pub const unsafe fn offset_from(self, origin: NonNull<T>)
                                                        -> isize where T: Sized ...
                                                                  (b) offset_from's safety concerns.
1. The distance between `self` and `subtracted` must be non-negative. [TF-Safety]
2. `self` and `subtracted` must either point to the same address, or both be derived from a pointer to the same
allocated object, and the memory range between the two pointers must be in bounds of that object. [CR-Safety]
3. The distance between `self` and `subtracted`, in bytes, must be an exact multiple of the size of `T`.
[CR-Safety]
4. The absolute distance between `self` and `subtracted`, in bytes, computed on mathematical integers without
wrapping around, cannot overflow an `isize`. [CR-Safety]
5. `T` must not be a Zero-Sized Type. [TF-Panics]
                           (c) The safety requirements for offset_from_unsigned
```

Fig. 3. An example of safety requirements extraction in SafetyReq.

After a safety requirement list is generated, the agentic LLM scores it by calculating the harmonic mean of satisfied rules over all rules and plans the next step based on the score. If the score exceeds a predefined threshold, the current requirement list will be accepted as the final result. Otherwise, the per-rule scores will be fed back to the LLM to guide targeted refinement. If the number of iterations exceeds a predefined limit, the agent will return the highest-scoring safety requirement list observed during the process. As for the experiments in [Sec. 4.1,](#page-10-0) the threshold score is set to 6, with a maximum of 3 iterations.

## <span id="page-6-0"></span>3.4 Specification Generation

We design the SpecGenerate agent that generates the specification for the target function based on the following sources: 1) primarily the safety requirement list from SafetyReq; 2) the metadata of the target function; 3) Kani's domain-specific knowledge, including the primitives and APIs for expressing preconditions, postconditions, loop invariants, etc; 4) few-shot examples, if any, from a shared knowledge database; 5) feedback information from the last generation iteration, if any.

The safety requirement list and metadata of the target function serve as a structured and precise target for the specification generation in this stage. Each requirement captures an atomic memorysafety or runtime-correctness property of the target function and is explicitly grounded in the function documentation. The SpecGenerate agent required that the generated formal specifications must be aligned with all safety requirements.

Note that we exclude the source code of the target function, because we believe that the actual implementation would interfere with LLMs' understanding of safety properties. Intuitively, the source code does not provide useful information to LLMs on how to formally specify safety properties, while it is helpful for functional correctness verification. Furthermore, LLMs tend to follow the source code to specify safety properties if it exists, in a way that would always lead to wrong results. Thus, we replace the source code with the metadata for LLM in generating specifications. Our experiments also evidence this observation (will be detailed in Sec. 4.1).

The remaining three sources are intended to further improve the performance of *SpecGenerate*. Kani's domain-specific knowledge is injected into LLMs via the shared knowledge database because it helps the LLM select and compose appropriate primitives correctly when constructing specifications. Specifically, this knowledge is mainly Kani specification primitives used in encoding safety properties, including the usage of APIs for expressing pre- and post-conditions, loop invariants, and memory-safety related predicates, such as #[requires()] and #[ensures()].

In addition, we adopt a few-shot in-context learning strategy in *SpecGenerate*. By default, all specifications that are successfully verified in the loop, together with their target functions, will be stored in the shared knowledge database. When *SpecGenerate* has a new target function, it retrieves the top N functions that are most similar in terms of function code and documentation, then constructs pairs of function code and corresponding specifications as few-shot examples. These few-shot examples offer concrete references on writing Kani specifications, thereby improving the quality of the generated specifications further.

## <span id="page-7-0"></span>3.5 Specification Precheck

In this step, we design *SpecPrecheck* agent to perform a precheck on the quality of the specification from *SpecGenerate* before sending it to Kani for verification.

Specifically, *SpecPrecheck* evaluates the generated specifications in two steps. First, it checks whether all safety requirements in the safety requirement list are covered. All uncovered requirements will be fed back to *SpecGenerate*, which is then instructed to generate specifications targeting the missing requirements. This checking helps solve the side effect of LLM's hallucination and nondeterminism from *SpecGenerate*. Second, *SpecPrecheck* asks LLM to assess the strength of the generated specifications by assigning a quantitative score ranging from 1 to 10. It evaluates whether preconditions are overly restrictive with respect to the corresponding safety requirements, and whether postconditions are overly weak and thus insufficient to characterise the function's safety properties. If the assigned score falls below a predefined threshold, *SpecPrecheck* produces concrete refinement suggestions and feeds them back to *SpecGenerate* for the refinement.

The refinement iteration between *SpecGenerate* and *SpecPrecheck* continues until all safety requirements are covered and the evaluation score is higher than the threshold, or it reaches the maximum number of iterations, at which point the highest-scoring specification is returned. In our experiment, we set the threshold score to 6 and the iteration limit to 5.

Note that *SpecPrecheck* is designed as a lightweight semantic-based specification checker rather than a sound verifier, pruning low-quality specifications before verifying them in Kani. Our ablation study (see Sec. 4.3) evidences that this refinement process helps ensure the resulting specifications capture all the safety requirements and improve the overall quality of the final specifications.

#### <span id="page-7-1"></span>3.6 Specification Verification

The *SpecVerify* agent invokes Kani to verify the target function under generated harnesses and specifications, and feeds the verification results back to *SpecGenerate* for refinement when it fails. To improve the specification refinement process, *SpecVerify* constructs contextual feedback for *SpecGenerate* based on the following three kinds of verification results from Kani:

**Syntax errors**. If Kani reports syntax errors in the specifications, *SpecVerify* directly forwards the corresponding error messages to *SpecGenerate*. These errors typically arise from incorrect usage of Kani primitives and can be resolved in the next iteration.

**Verification failures**. When the generated specifications are syntactically valid but fail to satisfy certain safety properties, the contextual feedback contains the following three parts. First, it retrieves counterexamples from Kani for the failed properties. Second, when multiple harnesses are involved for a single target function, both passing and failing harnesses are retrieved for cross-reference. Third, if the failure falls into predefined failure types, the corresponding repair rule will be triggered. For example, when Kani reports violations related to the assigns clause, *SpecGenerate* is explicitly prompted to refine the corresponding <code>#[kani::modifies(...)]</code> annotations for mutable parameters. The full list of failure-specific repair rules can be found in our artefact.

**Vacuous verifications**. A successful Kani verification does not exclude vacuous specifications, such as <code>#[kani::requires(false)]</code>. Kani inherently checks the reachability of each Kani annotation, making vacuous specification detectable. However, it is tedious to check the reachability of all annotations from Kani's running log directly. In our implementation, <code>SpecVerify</code> interpolates a redundant <code>#[kani::ensures(|\_| false)]</code> at the end of Kani postcondition. As long as the verification fails after the interpolation and succeeds before, the specification is considered non-vacuous.

The refinement process, *i.e.*, the *SpecGenerate-SpecPrecheck-SpecVerify* loop, terminates when Kani verification succeeds, or the maximum iteration limit is reached. Then, the current specification is added to the candidate set. KAPILOT allows users to set the target number of candidate specifications.

#### <span id="page-8-0"></span>3.7 Specification Selection

Given a set of specification candidates from *SpecVerify*, although all are valid and not vacuous, it is non-trivial to determine which candidate correctly formalises all desired safety properties, that is, fully satisfies users' intentions. Intuitively, we tend to select the candidate with the weakest precondition and the strongest postcondition as the final result. However, it happens that the weakest precondition and the strongest postcondition are not from the same candidate. For example, suppose we obtain two candidate specifications,  $\{P\}$  C  $\{Q'\}$  and  $\{P'\}$  C  $\{Q\}$ , where P'  $\implies$  P and Q  $\implies$  Q'. The desired specification, however, is  $\{P\}$  C  $\{Q\}$ . Although the two candidates are very close to the target, existing approaches [23, 25, 34, 35] would typically start a new run of the tools, thereby missing the correct result that can be derived from the current candidate set.

To address this challenge, we design a specification *shuffle-and-implication strategy*, which shuffles predicates across candidates and selects the optimal combination of specification predicates. If the best specification is already in the candidate set, the strategy will directly identify and return it in the first iteration. The remainder section introduces how our *shuffle-and-implication strategy* effectively identifies the optimal specification.

**Shuffle and implication strategy**. Algorithm algorithm 1 presents details of the strategy. We take three inputs: the target function F, the maximum iteration times M, and a set of generated specification candidate tuples SP with the index set  $\mathbb{T}$ , where each element consists of a precondition, a postcondition, and a loop invariant. And then, we return the optimal specification tuple  $(P_{best}, Q_{best}, I_{best})$ .

Within the maximum number of iterations, we select the weakest precondition and the strongest postcondition from the current pre- and post-condition sets (lines 4 and 8). If the function F contains no loop, *i.e.* all loop invariants in SP are none, we directly check the satisfiability of the current specification combination in Kani (line 10). If the verification succeeds, we return the current specification (line 11). Otherwise, we discard the current postcondition or precondition and test the next strongest or weakest combination in the subsequent iteration (lines 19 and 22). The two-layer nested loop guarantees that we will cover all possible combinations as long as  $M \geq |SP|$ . In this case, there are at least |SP| satisfiable combinations, corresponding exactly to the original candidates in SP. When no successful verification is found among the tested combinations, we randomly select a candidate from SP (line 23). This fallback occurs only when M < |SP|.

### **Algorithm 1:** Specification Shuffle and Implication Strategy

```
Input: F: target function, M: max iterations, SP = \{(p_k, q_k, i_k) \mid k \in \mathbb{T}\}: Specification set
    Output: (P_{best}, Q_{best}, I_{best}): the optimal specification
 1 i, j \leftarrow 0; \mathbb{P} \leftarrow getPreSet(SP);
 2 while i < M do
         // get the weakest precondition
 3
         p_w, i_w \leftarrow p_k, i_k \text{ s.t. } \exists p_k \in \mathbb{P}, \forall p_m \in \mathbb{P}, (p_m \Rightarrow p_k) \lor (p_k \Rightarrow p_m);
 5
         \mathbb{O} \leftarrow qetPostSet(\mathcal{SP});
         while j < M do
              // get the strongest postcondition
 7
               q_s, i_s \leftarrow q_k, i_k \text{ s.t. } \exists q_k \in \mathbb{Q}, \forall q_m \in \mathbb{Q}, (q_k \Rightarrow q_m) \lor (q_m \Rightarrow q_k);
 8
              if isEmptyInv(SP) then // no loop in F
 9
                    if KANIVERIFY(F, p_w, q_s) == SUCCESS then
10
                     return (p_w, q_s, None);
11
              else // has loop in F
12
                    if KANIVERIFY(F, p_w, q_s, i_w) == SUCCESS then
13
                       return (p_w, q_s, i_w);
                    else if KANIVERIFY(F, p_w, q_s, i_s) == SUCCESS then
15
                       return (p_w, q_s, i_s);
16
                    else if KANIVERIFY(F, p_w, q_s, i_w \wedge i_s) == SUCCESS then
17
                       return (p_w, q_s, i_w \wedge i_s);
18
19
               \mathbb{Q} \leftarrow \mathbb{Q} \setminus \{q_s\};
               j++;
20
         \mathbb{P} \leftarrow \mathbb{P} \setminus \{p_w\};
21
22
23 return random(SP);
```

If the function F contains loops, we test three possible loop invariants:  $i_w$ ,  $i_s$ , and  $i_w \wedge i_s$  for the selected  $p_w$  and  $q_s$  (lines 13-18), where  $i_w$  is the invariant from the candidate tuple containing the current precondition  $p_w$ , and  $i_s$  is from the tuple containing the current postcondition  $q_s$ . If none of these invariants make the verification succeed, we move on to the next iteration. Intuitively, the correct invariant is highly likely to be expressible in one of these three formats, as  $i_w$  captures the assumptions required to enter the loop safely, while  $i_s$  captures the conditions necessary to establish the desired postcondition after loop termination. Below, we provide a more formal explanation.

Consider two candidates  $(P_1,Q_1,I_1)$  and  $(P_2,Q_2,I_2)$ , where  $P_2 \implies P_1$  and  $Q_2 \implies Q_1$ , satisfiability of these candidates means that  $P_1 \implies wp(F,Q_1)$  and  $P_2 \implies wp(F,Q_2)$ . If we focus on the loop in F, we obtain  $P'_1 \implies wp(while\ (b)\ invariant\ I_1\ \{S\},Q'_1)$  and  $P'_2 \implies wp(while\ (b)\ invariant\ I_2\ \{S\},Q'_2)$ , where  $P'_1,P'_2,Q'_1$ , and  $Q'_2$  are predicates immediately before and after the loop, calculated from  $P_1,P_2,Q_1$ , and  $Q_2$ , respectively. By the while and consequence rule, we get  $P'_1 \implies I_1,I_1 \land \neg b \implies Q'_1$ , and  $I_1 \land b \implies wp(S,I_1)$ , together with  $P'_2 \implies I_2$ ,  $I_2 \land \neg b \implies Q'_2$ , and  $I_2 \land b \implies wp(S,I_2)$ .

Our target is to find an invariant  $I_{best}$ , such that  $P'_1 \implies wp(while\ (b)\ invariant\ I_{best}\ \{S\}, Q'_2)$  holds. Through the implication rules, we obtain the invariant based on the following rules:

```
• If P'_1 \Rightarrow I_2 holds, as I_2 \land \neg b \Rightarrow Q'_2, select I_{best} = I_2.
```

<sup>•</sup> If  $P'_1 \Rightarrow I_1 \wedge I_2$  holds, as  $I_2 \wedge \neg b \Rightarrow Q'_2$ , select  $I_{best} = I_1 \wedge I_2$ .

<span id="page-10-1"></span>

| Dataset | #Task | Fur | iction I | Lines          | Documentation Lines |    |       |  |
|---------|-------|-----|----------|----------------|---------------------|----|-------|--|
|         |       |     |          | avg            |                     |    | avg   |  |
| GOLDSET | 54    | 3   | 42       | 10.37<br>15.60 | 4                   | 85 | 23.35 |  |
| ULSET   | 70    | 3   | 55       | 15.60          | 4                   | 60 | 15.69 |  |

Table 1. Summary of the benchmarks.

- If  $I_1 \wedge \neg b \Rightarrow Q_2'$  holds, as  $P_1' \Rightarrow I_1$ , select  $i_{best} = I_1$ .
- If none of the above cases apply, skip.

In the actual implementation, since we cannot easily derive  $P'_1$ ,  $P'_2$ ,  $Q'_1$ , and  $Q'_2$ , we instead directly check the satisfiability of the combined specification using each of the three candidate invariants. In our experiments, we set the candidate number to 2 and the maximum iterations to 2.

#### 4 Evaluation

In this section, we evaluate the effectiveness and efficiency of KAPILOT in verifying unsafe Rust code with Kani. In summary, we seek to answer the following research questions:

- RQ1: How effective is KAPILOT at generating specifications in verifying safety properties?
- RQ2: How does KAPILOT compare with state-of-the-art specification generation approaches?
- RQ3: How effective is each component of KAPILOT at generating valid specifications?

Benchmarks. We construct a benchmark of 124 unsafe Rust functions, summarized in Tab. 1. The benchmark consists of two parts: a gold set with ground-truth specifications (GoldSet) and an unlabeled set without such specifications (ULSET).

The GoldSet consists of 54 unsafe Rust functions from the verify-rust-std project [11] (commit: bacd51ca) and serves as the primary evaluation baseline. We select these functions for the following three reasons: 1) the safety of unsafe code in the Rust standard library is of central importance to the Rust community, making it a practically significant target for evaluation; 2) the safety requirements of the Rust standard library are comprehensive and of high quality defined by the *rust-lang* developers; 3) and thanks to this project led by Amazon, where existing solutions provide human-expert-written specifications for these unsafe Rust functions, which perfectly satisfy the requirement of our benchmark as a reliable ground truth.

The ULSET comprises 70 unsafe Rust functions drawn from the Safe4U [22] unsound samples, which collect 97 unsafe Rust functions along with their safety comments from the top 500 most downloaded libraries on crates.io. We exclude 27 functions due to Kani's (1) no support for await and inline assembly, (2) incompatibility with packed\_simd, and (3) inability to express contracts for functions that return mutable references to arguments.

Implementation and Experimental Setup. KAPILOT is implemented in a total of 2470 lines of Python code and 1323 lines of Rust code. KAPILOT verifies programs in Kani 0.62.0. In experiments, we test KAPILOT on three LLMs: GPT-5 (gpt-5-2025-08-07), DeepSeek-v3.2 (2025-12-01), and Claude-Sonnet-4 (claude-sonnet-4-20250514). As these models have been widely used in prior work due to accessibility, moderate cost, and strong performance, ensuring reproducibility without specialized hardware. All experiments are conducted on a server running Ubuntu 24.04.1 LTS, with a 104-core Intel(R) Xeon(R) Gold 6230R CPU, 128 GB of RAM, and 2 TB of disk space.

#### <span id="page-10-0"></span>4.1 RO1: Effectiveness of KAPILOT

Overall results. We evaluate KAPILOT on GOLDSET and ULSET using three LLMs. Since Kani only checks whether a program satisfies the properties described in a specification, a specification that

passes Kani may still be incomplete or even vacuous. Thus, we categorise the result into one of three types: good, bad, or failure. A good indicates that verification passes and the specification captures all safety requirements. A bad indicates that verification passes, but the specification is incomplete or vacuous. A failure means the verification process itself fails (e.g., due to a counterexample or syntax errors). As there is no fully automated approach to distinguish good from bad cases, we manually performed the categorisation for GOLDSET, for which ground truth is available. Two co-authors, each with five years of experience in formal verification, independently evaluated the generated specifications in a blind review process, spending over 30 hours in total. We measured the agreement between their initial annotations using Cohen's  $\kappa$  [7], with values ranging from 0.81 to 0.95 across different LLMs, as summarised in Tab. 2. The high  $\kappa$  values and the few disagreements indicate strong inter-rater agreement. Disagreements were subsequently resolved through discussion until both co-authors reached a consensus. This manual evaluation is facilitated by Kani's concise specification primitives and clear semantics, which allow for a reliable comparison of semantic strength and equivalence. Specifically, we manually assessed whether each generated pre- and post-condition is stronger than, weaker than, different from, or equivalent to the ground truth. A specification is labeled good only if: (1) verification passes, (2) the generated precondition is equivalent to or weaker than the ground truth, and (3) the postcondition is equivalent to or stronger than the ground truth. If verification passes but these semantic criteria are not met, the result is labeled bad. Fig. 4 shows examples of good and bad postconditions, respectively (analogous to the cases for preconditions), where the KAPILOT-generated specification is shown on the left and the ground truth is on the right.

<span id="page-11-0"></span>Table 2. Summary of inter-rater agreement for the independent blind labeling of specifications generated by different LLMs that passed verification on GoldSet. "Both *Good*" and "Both *Bad*" denote the number of specifications labeled as *Good* and *Bad* by both authors. "Author A Only" indicates the number of specifications labeled as *Good* exclusively by Author A. "Author B Only" indicates the number of specifications labeled as *Good* exclusively by Author B.

| Model           | Agree     | ment     | Disagro       | Cohen's K     |      |
|-----------------|-----------|----------|---------------|---------------|------|
|                 | Both Good | Both Bad | Author A Only | Author B Only |      |
| GPT-5           | 28        | 16       | 1             | 3             | 0.82 |
| DeepSeek-v3.2   | 27        | 15       | 0             | 1             | 0.95 |
| Claude-Sonnet-4 | 32        | 14       | 2             | 2             | 0.81 |

Tab. 3 presents the overall results. KAPILOT performs comparable *good* rates across three LLMs on Goldset, ranging from 51.85% to 62.96%, which demonstrates the effectiveness of the overall multi-agent design in KAPILOT. Claude-Sonnet-4 and GPT-5 achieve slightly higher *good* rates than DeepSeek-v3.2 on Goldset. The performance on ULSET follows a similar trend. Note that, due to the lack of ground truth in ULSET, passed cases on this dataset were not further classified into *good* and *bad*. However, the *failure* rate (28.57% to 31.43%) is higher than that on Goldset (7.41% to 20.37%). A possible explanation is that function descriptions in ULSET contain less information than those in Goldset, as shown in Tab. 1. Since function descriptions directly influence the subsequent safety requirements and specification generations, lower-quality descriptions can lead to higher failure rates.

Tab. 4 summarises the pre-/post-condition and loop-invariant generation results across three LLMs on two datasets. GPT-5 consistently produces the largest specifications, averaging 18.44 lines per function for Goldset and 26.43 lines per function for ULSet, while DeepSeek-v3.2 and Claude-Sonnet-4 generate shorter specifications on average (9.56 and 11.96 lines for Goldset,

```
#[kani::ensures(|result: &&CStr| {
                                                         // below shows the implementation of `is safe`:
 result.len() > 0 && result[result.len() - 1] == 0
                                                         //impl Invariant for &CStr {
 && (|| { let mut i: usize = 0;
                                                             fn is_safe(&self) -> bool {
   let mut ok: bool = true;
                                                         11
                                                                   let bytes: &[c_char] = &self.inner;
                                                         //
   while i + 1 < result.len() {
                                                                   let len = bytes.len();
    if result[i] == 0 { ok = false; break; }
                                                         //
                                                                   !bytes.is_empty() && bytes[len - 1] == 0 &&
                                                                   !bytes[..len - 1].contains(&0)
    i += 1;
                                                         //
                                                         //
   ok })()
                                                         //}
                                                         #[ensures(|result| result.is_safe())]
3)]
fn from_bytes_with_nul_unchecked(bytes:&[u8])->&CStr..
                                                         fn from_bytes_with_nul_unchecked(bytes:&[u8])->&CStr..
                           (a) Good postcondition, equivalent to the ground truth.
#[kani::ensures(|result: &&'a mut T| {
core::ptr::eq::<T>(*result, self.as_ptr())
 && kani::mem::can_dereference::<T>(core::ptr::addr_of!(**result)) #[kani::ensures(|result: &&mut T|
                                                                       core::ptr::eq(*result, self.as_ptr()))
&& kani::mem::can_write::<T>(core::ptr::addr_of!(**result))
fn as_mut<'a>(&mut self) -> &'a mut T{..}
                                                                    fn as_mut<'a>(&mut self) -> &'a mut T{..}
                           (b) Good postcondition, stronger than the ground truth.
#[kani::ensures(|result: &Self|
                                                      #[kani::ensures(|result: &Self|
                                                        !result.as_ptr().is_null() && result.addr() == addr)]
 !result.as_ptr().is_null())]
fn with_addr(self, addr: NonZero<usize>) -> Self{..} fn with_addr(self, addr: NonZero<usize>) -> Self{..}
                            (c) Bad postcondition, weaker than the ground truth.
 #[kani::ensures(|_result: &isize| {
                                                               #[kani::ensures(|result|
 let size = core::mem::size_of::<T>(); let a = (self as
                                                                 core::mem::size_of::<T>() == 0 ||
 *const T) as usize; let b = origin as usize;
                                                                 (*result == (self as isize - origin as isize) /
 let d = if a >= b { a - b } else { b - a };
                                                                (mem::size_of::<T>() as isize)))
 size > 0 && d <= core::isize::MAX as usize
                                                               fn offset_from(self, origin: *const T) -> isize
fn offset_from(self, origin: *const T) -> isize
```

<span id="page-12-1"></span>Table 3. Number of tasks verified by KAPILOT across different LLMs. *Pass* means that Kani verification passes, while *Failure* means that Kani verification fails to pass due to counterexamples or syntax errors. *Good* means that Kani verification passes and the specification captures all safety requirements. *Bad* means that the verification passes but the specification is incomplete or vacuous.

(d) Bad postcondition, different from the ground truth.

Fig. 4. Examples of good and bad postconditions: KAPILOT-generated (left) vs. ground truth (right).

| Model           | (           | COLDSET Resu | ULSET Result |             |             |
|-----------------|-------------|--------------|--------------|-------------|-------------|
| Model           | Good        | Bad          | Failure      | Pass        | Failure     |
| GPT-5           | 31 (57.41%) | 17 (31.48%)  | 6 (11.11%)   | 50 (71.43%) | 20 (28.57%) |
| DeepSeek-v3.2   | 28 (51.85%) | 15 (27.78%)  | 11 (20.37%)  | 48 (68.57%) | 22 (31.43%) |
| Claude-Sonnet-4 | 34 (62.96%) | 16 (27.78%)  | 4 (7.41%)    | 48 (68.57%) | 22 (31.43%) |

respectively). Across both datasets, all models generate a few number of loop invariants. This arises for two reasons. First, LLMs may choose to generate only pre-/post-conditions even for functions containing loops, and Kani can still verify these functions via unwinding. Second, Kani currently supports loop-invariant primitives only for while loops. Other loop forms must be manually rewritten in a consistent manner, which is error-prone. In our experiments, we let Kani perform full unwinding for non-while loops by default, and impose a bounded unwind only when full unwinding would be too costly.

<span id="page-13-0"></span>

| Dataset         |      | GOLDSET |              |                                          |     |      | ULSET           |     |       |     |     |      |
|-----------------|------|---------|--------------|------------------------------------------|-----|------|-----------------|-----|-------|-----|-----|------|
| Lines           | pre- | and pos | t-conditions | loop invariants pre- and post-conditions |     |      | loop invariants |     |       |     |     |      |
|                 | min  | max     | avg          | min                                      | max | avg  | min             | max | avg   | min | max | avg  |
| GPT-5           | 1    | 68      | 18.44        | 0                                        | 2   | 0.04 | 1               | 97  | 26.43 | 0   | 15  | 1.20 |
| DeepSeek-v3.2   | 2    | 21      | 9.56         | 0                                        | 2   | 0.07 | 1               | 69  | 13.54 | 0   | 7   | 0.73 |
| Claude-Sonnet-4 | 1    | 48      | 11.96        | 0                                        | 8   | 0.15 | 1               | 60  | 15.56 | 0   | 12  | 1.04 |

Table 4. Summary of generated specifications in KAPILOT across different LLMs.

*Invocation Times.* Fig. 5 shows the invocation times of each component in KAPILOT on GOLDSET and ULSET. As mentioned in Sec. 3, we set the maximum invocation times of SafetyReq to 3, SpecGenerate-SpecPrecheck loop to 5, and SpecVerify to 3. Overall, Claude-Sonnet-4 has the lowest median invocation times and the smallest variance across all stages. For SpecGenerate and SpecPrecheck, although the highest invocation times reach the predefined threshold in GPT-5, more than 50% Fig. 5. Invocation times of KaPilot components of tasks terminate in 5 iterations across all three models.

![](_page_13_Figure_5.jpeg)

<span id="page-13-1"></span>

Money Costs. Tab. 5 shows the money and token cost on GOLDSET and ULSET using different LLM models. At the time of our experiments, the cost per 1 million input (output) tokens is \$1.25 (\$10) for GPT-5, \$0.29 (\$1.14) for DeepSeek-v3.2, and \$3 (\$15) for the Claude-4-Sonnet. DeepSeek-v3.2 incurred the lowest overall cost due to its very low per-token price. Claude-4-Sonnet, despite having a higher per-token cost than GPT-5, had a lower overall cost because its invocation times were fewer. Apart from that, Claude-Sonnet-4 maintains the most concise token profile. This high efficiency in token usage effectively compensates for its premium unit pricing, resulting in higher cost-effectiveness compared to GPT-5.

<span id="page-13-2"></span>Table 5. Comparison of average money and token cost per function.

| LLMs            | GPT-5   | DeepSeek-v3.2 | Claude-Sonnet-4 |
|-----------------|---------|---------------|-----------------|
| Avg. Cost (USD) | 0.41    | 0.02          | 0.26            |
| Avg. Tokens     | 219,218 | 90,116        | 82,424          |

#### **RQ2: Comparisons**

Since there is no prior work on using LLMs to generate specifications for unsafe Rust verification in Kani, we select AutoSpec [34] as the closest point of comparison. We delay the detailed discussion of the reason for choosing AutoSpec for comparison to Sec. 5.

To enable a fair comparison, we adapt AutoSpec from Frama-C to Kani through three steps. First, we convert all Frama-C-specific prompts into Kani-compatible prompts. For example, we replace "assuming you are a Frama-C expert" with "assuming you are a Kani expert", replace Frama-C-based examples with Kani examples that we have in KAPILOT, etc. Second, we replace Frama-C API calls with Kani commands that invoke the verifier to check generated specifications and collect running results. Third, we adapt the whole error message processing component to make it compatible with Kani's outputs. Throughout this adaptation, we preserve AutoSpec's overall pipeline, including its

<span id="page-14-1"></span>

| T1 #T1      |      | Results |         |        | Precondition |       |          |          | Postcondition |        |       |    |
|-------------|------|---------|---------|--------|--------------|-------|----------|----------|---------------|--------|-------|----|
| Tool #Tasks | Good | Bad     | Failure | Weaker | Equiv        | Wrong | Stronger | Stronger | Equiv         | Weaker | Wrong |    |
| KaPilot     | 54   | 31      | 17      | 6      | 3            | 38    | 0        | 7        | 16            | 18     | 13    | 1  |
| AutoSpec    | 54   | 17      | 23      | 14     | 3            | 24    | 13       | 14       | 28            | 8      | 11    | 7  |
| Surpass     | -    | ↑ 82%   | ↓ 26%   | ↓ 57%  | <b>↑</b> 52  | 2%    | \ \      | 74%      | ↓ 69          | %      | ↓2    | 2% |

Table 6. Performance of KAPILOT against AutoSpec (direct prompting) under GPT-5.

use of LLMs to generate candidate specifications, its iterative construction of specifications, and its specification repair approach based on error-message types.

Tab. 6 shows the performance of KAPILOT against AutoSpec in terms of specification quality on GoldSet benchmark. Overall, KAPILOT produced approximately 82% more *good* specifications than AutoSpec, reflecting the effectiveness of its specification evaluation and logical implication—based selections in eliminating low-quality candidates. In particular, KAPILOT substantially reduced unsuitable preconditions, which include both incorrect and overly restrictive ones, by about 74% compared with AutoSpec. A similar trend was observed for postconditions. KAPILOT generated around 22% fewer incorrect or overly weak postconditions, indicating better semantic alignment with the intended safety requirements.

Moreover, during specification verification, KAPILOT provides LLMs with counterexamples as well as both failing and successful harnesses, together with error-specific fixing strategies, enabling issues to be identified and repaired early in the pipeline. As a result, KAPILOT reduced verification failures by approximately 57% relative to AutoSpec. These results demonstrate that KAPILOT not only increases the overall success rate of specification generation, but also significantly improves the semantic quality and reliability of the generated specifications.

### <span id="page-14-0"></span>4.3 RQ3: Ablation Study

To understand the effectiveness of each essential component in KAPILOT, we conduct three ablation studies, and the results are shown in Tab. 7. In this study, we compare the full KAPILOT with variants that respectively exclude the *SafetyReq*, *SpecPrecheck*, *SpecVerify* agents, as well as the few-shot examples in *SpecGenerate*. Furthermore, we compare KAPILOT against a naive LLM prompting baseline (i.e., removing all agents). We record the *good* rate, *pass* rate, *bad* rate, and *failure* rate over the same set of 54 verification tasks that we used in Sec. 4.1 for the comparison with AutoSpec. For simplicity, we perform the ablation study under GPT-5.

**KAPILOT w/o SafetyReq.** We replaced the *SafetyReq* agent with a simple LLM that generates the safety requirement list directly from the function's documentation, which is then passed to subsequent agents. Without quality checks and feedback-driven refinement, the resulting safety requirement lists were often misaligned with the original safety concerns of the function, making it difficult to produce specifications with appropriate strength. Experimental results show that this simplification reduced the *good* rate of specification generation by approximately 46.30%, and the *bad* rate increased by around 3.70%.

KAPILOT w/o *SpecPrecheck*. We removed the *SpecPrecheck* agent from KAPILOT, delivering the specifications generated by *SpecGenerate* directly to *SpecVerify*. Without the quality control provided by *SpecPrecheck*, the generated specifications are more likely to be inaccurate and misaligned with the intended safety requirements. The experimental results confirm that removing this agent increased the proportion of specifications with inappropriate strength, such as overly strong preconditions or overly weak postconditions, by 12.96%, and the *good* rate dropped by 35.19%.

<span id="page-15-0"></span>

| NO. | Setting                  | Good        | Bad         | Pass        | Failure     |
|-----|--------------------------|-------------|-------------|-------------|-------------|
| 1   | Full KaPilot             | 31 57.41%   | 17 31.48%   | 48 88.89%   | 6 11.11%    |
| 2   | KaPilot w/o SafetyReq    | 6 ↓ 46.30%  | 19 ↑ 3.70%  | 25 \ 42.59% | 29 ↑ 42.59% |
| 3   | KaPilot w/o SpecPrecheck | 12 ↓ 35.19% | 24 ↑ 12.96% | 36 ↓ 22.22% | 18 ↑ 22.22% |
| 4   | KaPilot w/o SpecVerify   | 12 ↓ 35.19% | 20 ↑ 5.56%  | 32 ↓ 29.63% | 22 ↑ 29.63% |
| 5   | KaPilot w/o few-shots    | 11 ↓ 37.04% | 30 ↑ 24.07% | 41 ↓ 12.96% | 13 ↑ 12.96% |
| 6   | Naive LLM prompt         | 8 ↓ 42.59%  | 20 ↑ 5.56%  | 28 ↓ 37.04% | 26 ↑ 37.04% |

Table 7. Ablation study in GPT-5.

**KAPILOT w/o** *SpecVerify*. We replace the *SpecVerify* agent with a simplified agent that forwards pure Kani error messages to *SpecGenerate* for the refinement, without contextual feedback mentioned in Sec. 3.6, including counterexamples, failing and successful harnesses, error-specific fixing strategies, and the specification selection strategy in Sec. 3.7. The experimental results show that removing these components substantially degrades performance. The *failure* rate increased by 29.63%, and the *good* rate decreased by 35.19%. Without this detailed feedback, errors in Kani specifications cannot be corrected effectively, leading to more iterations in the generate–evaluate–verify loop and, ultimately, exceeding the maximum iteration limit, which causes generation to fail.

**KAPILOT w/o few-shots.** We removed the few-shot examples from *SpecGenerate*, meaning that the agent could no longer retrieve similar function-specification pairs to serve as in-context references. Without these few-shot examples, the agent lacks concrete demonstrations of how to map specific safety requirements and code patterns to Kani's primitives, making it difficult to maintain the required precision and syntax for various safety properties. Removing few-shot examples increases *failure* rate by 12.96% and reduces *good* rate by 37.04%, showing that few-shot examples are critical guidance for encoding Kani-specific safety constraints, enabling more accurate specifications.

Naive LLM prompting. We also implement a baseline prompting strategy for comparison. Specifically, we replace KAPILOT's multi-agent architecture with a direct prompting approach, using Kani as an oracle to provide error feedback for iterative refinement (up to 10 rounds). Experimental results show that this simplified approach significantly degrades performance. The *failure* rate increases by 37.04%, while the *good* rate drops by 42.59%. These results confirm that KAPILOT's performance gains stem from its specialized multi-agent design rather than iterative prompting alone.

## 4.4 Case Study

Case Study 1. This case study compares KAPILOT and AutoSpec [34] on generating specifications for the same function, offset, whose signature and documentation are shown in Fig. 6. AutoSpec generates specifications directly from the function implementation and produces preconditions as shown in Fig. 7. Although syntactically correct, these preconditions are semantically redundant, all expressing the same constraint that "the computed offset count \* size\_of::<T>() must not overflow isize". But Kani verification fails with the error "Offset result and original pointer must point to the same allocation", revealing a missing safety property that "the entire memory range between the original pointer and the resulting pointer must lie within the bounds of the same allocated object" in the specification. Since this constraint is not explicitly stated in the description, AutoSpec cannot capture this safety requirement for the pointer computation.

In contrast, KAPILOT derives specifications from a structured safety requirement list extracted from the function documentation, as shown in Fig. 6. The *SafetyReq* agent iteratively refines this list to ensure that all relevant safety concerns are covered while avoiding redundant or overlapping requirements. Guided by this refined list, KAPILOT generates a Kani specification

```
/// # Safety
                                                             1. The computed offset. `count * size of::<T>()`
/\!/\!/ If any of the following conditions are violated, the
                                                             bytes, must not overflow isize.
result is Undefined Behavior:
                                                             2.If `count * size_of::<T>()` bytes is non-zero,
/// * The computed offset, `count * size_of::<T>()` bytes.
                                                             then self must be derived from a pointer to some
must not overflow 'isize'
                                                             allocated object.
/// * If the computed offset is non-zero, then `self` must
                                                             3.If `count * size_of::<T>()` bytes is non-zero,
                                                             then the entire memory range between self and the
be derived from a pointer to some [allocated object], and
the entire memory range between 'self' and the result must
                                                             result must be within the bounds of that allocated
be in bounds of that allocated object. In particular, this
range must not "wrap around" the edge of the address
                                                             4.If `count * size_of::<T>()` bytes is non-zero,
                                                             then the memory range between self and the result
space.
pub const unsafe fn offset(self, count: isize) -> Self ...
                                                             must not wrap around the edge of the address space.
```

Fig. 6. offset's description (left) and SafetyReq-generated safety requirement list (right).

```
#[kani::requires({
  let stride = crate::mem::size_of::<T>();
                                                          #[kani::requires({
                                                            let size = core::mem::size_of::<T>();
  let abs_count = count.unsigned_abs() as usize;
                                                            let nonzero = (count != 0) && (size != 0);
 abs_count.checked_mul(stride).map_or(false, |bytes|
                                                            let count_abs = count.unsigned_abs() as usize;
bytes <= isize::MAX as usize)</pre>
                                                            let byte_off_opt = count_abs.checked_mul(size);
3)]
#[kani::requires({
                                                            let req1 = byte_off_opt.is_some_and(|bo| bo <=</pre>
                                                              core::isize::MAX as usize);
  let stride = core::mem::size_of::<T>();
  if stride == 0 { true }
                                                            let req2 = !nonzero || (size > 0 &&
                                                              kani::mem::same_allocation::<T>(self.as_ptr(),
 else {
                                                                  self.as_ptr()));
   let abs = if count >= 0 { count as usize }
                                                            let reg3 = !nonzero || (size > 0 &&
          else { (-count) as usize);
   abs.checked_mul(stride).map_or(false, |bytes| bytes
                                                               kani::mem::same_allocation::<T>(self.as_ptr(),
     <= isize::MAX as usize)
                                                               self.as_ptr().wrapping_offset(count)));
                                                            let req4 = !nonzero || (match byte_off_opt {
                                                              Some(bo) => {
})]
                                                                let addr = self.addr().get();
#[kani::requires({
 let stride = core::mem::size_of::<T>();
                                                                if count >= 0 { (addr <= usize::MAX - bo) && (addr
                                                                   + bo == (dest as *const () as usize))}
 if stride == 0 { true }
                                                                else { (addr \geq bo) && (addr - bo == (dest as
 else {
   let limit = (isize::MAX as usize) / stride;
                                                                   *const () as usize)) }
    let mag = if count >= 0 { count as usize } else {
        count.wrapping_neg() as usize };
                                                              None => false.
   mag <= limit
                                                            });
                                                            req1 && req2 && req3 && req4
})]
```

Fig. 7. Preconditions generated by AutoSpec (left) and KAPILOT (right).

that explicitly encodes the missing constraint using kani::mem::same\_allocation as highlighted in Fig. 7, accurately capturing the requirement that both pointers belong to the same allocation. As a result, the generated specification successfully passes Kani verification.

This case study highlights a key limitation of code-centric specification generation. Safety constraints that are implicit in documentation but not directly reflected in code are easily overlooked. By contrast, grounding specification generation in a comprehensive and non-redundant set of documentation-derived safety requirements enables KAPILOT to produce accurate specifications. **Case Study 2.** This case study demonstrates how KAPILOT identifies and repairs subtle specification defects in *SpecVerify*. The Rust function as\_flattened, as shown in Fig. 8, is parameterised by a generic type T, which may be either zero-sized (ZST) or non-zero-sized. Fig. 6 shows the safety requirement list extracted by the *SafetyReq* agent. In the first specification generation attempt, the LLM-produced precondition is shown in Fig. 8 line 2. This precondition implicitly assumed T to be zero-sized and failed to account for the non-ZST case. Consequently, when T is non-zero-sized, the precondition evaluates to false, causing postconditions to be vacuous, allowing verification to succeed without imposing any meaningful behavioural constraints.

To automatically detect such vacuous specifications, KAPILOT applies a vacuity check by appending #[kani::ensures(|\_| false)] to the postcondition. If the precondition collapses to false,

```
// safety regs: 1. If T is a zero-sized type, then self.len() * N must not overflow usize.
     #[kani::requires(T::IS_ZST && self.len().checked_mul(N).is_some()))]
     + #[kani::requires(!T::IS_ZST || self.len().checked_mul(N).is_some())]
    #[kani::ensures(|result: &&[T]| result.len() == if T::IS_ZST { self.len().checked_mul(N).unwrap() } else {
5
    self.len() * N }))]
     #[kani::ensures(|result: &&[T]| core::ptr::eq(result.as_ptr(), self.as_ptr().cast())))]
    #[kani::ensures(|r_post| false)]
     pub const fn as_flattened(&self) -> &[T] {
         let len = if T::IS_ZST {
            self.len().checked_mul(N).expect("slice len overflow")
10
11
         } else {
             // SAFETY: `self.len() * N` cannot overflow because `self` is already in the address space.
12
             unsafe { self.len().unchecked_mul(N) }
13
14
         };
// SAFETY: `[T]` is layout-identical to `[T; N]`
15
         unsafe { from_raw_parts(self.as_ptr().cast(), len) }
16
     }
17
```

Fig. 8. Specifications generated for as\_flattened based on the safety requirements. The prefixes "-" and "+" denote, respectively, an incorrect precondition generated first and a correct one generated after correction.

this new postcondition is incorrectly verified as true, signaling the presence of vacuity. Using this mechanism, KaPilot identifies the flawed precondition and feeds explicit feedback to *SpecGenerate* agent. The LLM is then instructed to regenerate the precondition while accounting for both ZST and non-ZST cases. The corrected precondition from the second iteration is shown in Fig. 8 line 3.

This case highlights that syntactically correct and verified specifications from LLMs may still be semantically meaningless due to vacuous assumptions. It is difficult to detect via manual inspection. By systematically enforcing vacuity checks, KAPILOT ensures that generated specifications are non-trivial, significantly improving the reliability of automated specification generation.

#### <span id="page-17-0"></span>5 Discussion

Why comparing with AutoSpec. AutoSpec is a similar LLM-based specification generation framework designed for Frama-C [9], an automated verification tool whose interface is similar to Kani. In both frameworks, specifications are expressed as annotations embedded in the source code. Moreover, AutoSpec has a classical and representative pipeline for specification generation tasks that recursively invokes LLMs till the verification succeeds. Although prior works [1, 35] have utilised LLM in Rust verification on Verus, the workflow for Verus automation cannot be directly adapted to Kani. Thus, we choose AutoSpec for comparison.

**Evaluating specification quality.** An important question is whether a specification that successfully passes Kani verification truly and precisely captures the intended safety properties. In our evaluation, assessing this aspect still partially relies on manual inspection, and we do not yet provide a fully automated solution. However, KAPILOT incorporates three design choices to improve specification quality. First, *SpecPrecheck* uses LLMs to validate alignment between generated specifications and documented safety requirements. Second, *SpecVerify* explicitly filters out unreachable results, preventing vacuous proofs caused by overly restrictive preconditions. Third, shuffle-and-implication re-evaluates pre- and post-conditions across candidates to explore a broader constraint space, increasing the likelihood that the resulting specification captures a wider range of critical memory-safety properties.

Prior work [18] evaluates the correctness and completeness for post-conditions by mutating implementation code or input-output pairs [18]. These mutations are intended to alter functional results, and if the post-conditions still hold, they are considered too weak. However, our focus is on panic and memory safety properties rather than pure functional correctness. Changes in functional results do not necessarily indicate memory safety violations or runtime panics. The specification

ranking [\[16\]](#page-20-11) approach designs four rating criteria, but they are for P models [\[8\]](#page-20-12). Therefore, existing approaches are not well-suited to our setting.

Effects of documentation quality. Poor documentation may lead to missing or underspecified constraints, potentially resulting in bad specifications. Failures stem from (i) reliance on incomplete examples omitting corner cases, exceptional paths, or implicit assumptions, and (ii) ambiguities and inconsistencies across cross-referenced documentation. These are orthogonal to KaPilot and can be mitigated by preprocessing steps such as LLM-based ambiguity resolution [\[3,](#page-20-13) [36\]](#page-21-5) or extracting precise structured constraints [\[26\]](#page-20-14). We leave this as future work.

Expressiveness of specifications. KaPilot relies on Kani to express specifications. Although Kani provides specification primitives for memory safety and runtime correctness, its expressiveness is limited for certain natural-language safety requirements. For instance, lifetime-related properties (e.g., "For the entire lifetime 'a of the returned &'a CStr, the memory region starting at ptr and spanning the C string must not be mutated.") lack direct support, forcing approximation of the intended semantics in specifications. In addition, semantic overlap exists among Kani primitives. For instance, both mem::checked\_align\_of\_raw and mem::can\_dereference capture alignment properties, which may lead LLMs to generate redundant constraints and introduce unnecessary specification verbosity. The performance of KaPilot is bounded by the expressiveness of Kani primitives.

Bounded verification in Kani. Kani is based on bounded model checking and is limited to provide fully unbounded proof. While recent support for loop invariants improves scalability, it is currently restricted to while loops, requiring manual rewriting for other loop forms. Moreover, nondeterministic modelling of vector-like data structures still relies on concrete capacity bounds, limiting the expressiveness of unbounded abstractions. Addressing these limitations is an important direction for future work.

Threat to validity. The ULSet dataset poses no risk of data leakage, as it contains no existing specifications. For the functions in GoldSet with human-written ground truth, a potential risk exists because the models' training data are undisclosed. However, the knowledge cutoffs of GPT-5, Claude-Sonnet-4 and DeepSeek-v3.2 are September 2024, March and September 2025, respectively, at which time Kani specifications were scarce. Moreover, during our evaluation, we did not observe any non-trivial cases where the generated specifications are the same as the ground truth. We therefore believe the threat is minimal.

## 6 Related Work

## 6.1 Verification of unsafe Rust code

Several studies have focused on unsafe Rust verification. RustBelt [\[17\]](#page-20-15) establishes a semantic typing framework in Coq [\[12\]](#page-20-16) based on lifetime logic to prove the type soundness of a core subset of Rust and ensure that safe APIs correctly encapsulate unsafe code. RustHornBelt [\[24\]](#page-20-17) extends this foundation with parametric prophecies to enable functional correctness verification using first-order logic specifications. RefinedRust [\[14\]](#page-20-18) builds on refined ownership types to support automated reasoning for both safe and unsafe Rust and produces machine-checkable proofs. GillianRust [\[2\]](#page-20-19) combines lifetime logic with SMT-based symbolic execution to reason about unsafe code. These approaches typically require substantial manual effort, including modeling and auxiliary proof construction. Verus [\[19\]](#page-20-20) adopts an SMT-based verification approach over Rust-like programs, supporting safe Rust and limited unsafe constructs, but still relies on user-provided proof annotations. Automated approaches based on bounded model checking [\[15,](#page-20-21) [29,](#page-21-6) [31\]](#page-21-4) and symbolic execution [\[13,](#page-20-22) [28,](#page-20-23) [37\]](#page-21-7) have also been applied to unsafe Rust. Kani [\[31\]](#page-21-4) uses bit-precise bounded model checking to verify both safe and unsafe Rust, supporting function contracts and loop invariants for modular verification. UnsafeCop [\[33\]](#page-21-8) extends Kani with loop bound inference, loop stubbing, and scheduling strategies

to improve scalability. SMACK [\[29\]](#page-21-6) translates LLVM bitcode into Boogie IR [\[20\]](#page-20-24) to detect memory safety violations. Seahorn [\[15\]](#page-20-21) performs model checking and abstract interpretation at the LLVM IR level, while RVT [\[13\]](#page-20-22) extends KLEE to identify memory safety bugs via symbolic execution.

## 6.2 LLM for formal verification

Several studies [\[5,](#page-20-25) [23,](#page-20-2) [27,](#page-20-26) [34\]](#page-21-1) focus on automatically generating formal specifications using LLMs. AutoSpec [\[34\]](#page-21-1) takes the source code as input, employing a call-graph-based hierarchical decomposition and strategically inserts placeholders into the code to guide LLMs in generating candidate specifications through iterative, bottom-up inference. These candidates are then formally validated by a prover, with invalid ones being filtered out. The framework repeats this generate-validate cycle, progressively refining the specification set until verification succeeds or an iteration limit is reached. SpecGen [\[23\]](#page-20-2) is another LLM-driven approach for specification generation. It first engages the LLM to produce candidate specifications. When the initial candidates fail verification, it applies mutations and employs a weighted heuristic to select promising variants for validation. Similar to AutoSpec, it derives specifications directly from the source code. Beyond direct generation, several studies address challenges in improving the quality and selection of LLM-generated invariants. Pei et al. [\[27\]](#page-20-26) fine-tune LLMs using a scratchpad-style prompting strategy to enable stepwise reasoning for invariant inference, achieving performance comparable to dynamic analysis tools without relying on execution traces. Chakraborty et al. [\[5\]](#page-20-25) propose a learning-based ranking approach that prioritises inductive loop invariants based on semantic similarity to the verification task, reducing the number of expensive verifier invocations.

Another category of work integrates LLMs with verification tools to generate proof annotations and verified code. AutoVerus [\[35\]](#page-21-2) combines domain expertise with formal methods to assist LLM agents in generating, refining and debugging proof annotations for Verus programs. By iteratively leveraging verification feedback, it achieves a high success rate in producing correct proofs. SAFE [\[6\]](#page-20-1) addresses data scarcity in verified code generation through a self-evolving framework that combines synthetic data generation with model fine-tuning, demonstrating improved efficiency and accuracy compared to approaches that rely solely on general-purpose LLMs. AlphaVerus [\[1\]](#page-20-0) extends this idea by introducing a fully automated self-improvement loop that integrates candidate exploration, tree-search-based repair, and specification critique, enabling the system to bootstrap its verification capabilities without human intervention. Similarly, the work [\[25\]](#page-20-3) synthesises Dafny [\[21\]](#page-20-27) implementations together with formal specifications from concise functional descriptions using multiple prompting strategies, and evaluates the results using the Dafny verifier. These approaches primarily target functional correctness, rather than the low-level memory safety constraints required for verifying unsafe Rust code.

## 7 Conclusions

We presented KaPilot, a fully automated multi-agent LLM framework for generating Kani specifications to verify unsafe Rust code. KaPilot distills documented safety concerns into structured safety requirements that guide specification generation, and refines candidate specifications through a generate–precheck–verify loop, followed by a shuffle and implication strategy to determine the final specifications. We evaluated KaPilot on 124 Rust functions. It successfully generated specifications for 71.4% of functions without ground truth and for 88.9% of functions with ground-truth specifications, with 57.4% of the generated specifications being semantically equivalent to or better than the ground truth. Compared with AutoSpec, KaPilot improves the success rate of generating verifiable specifications by 14.8% and equivalent-or-better specifications by 25.9%.

### 8 Data Availability

All data and scripts are publicly available at [32].

#### References

- <span id="page-20-0"></span> Pranjal Aggarwal, Bryan Parno, and Sean Welleck. 2024. AlphaVerus: Bootstrapping Formally Verified Code Generation through Self-Improving Translation and Treefinement. arXiv:2412.06176 [cs.LG] https://arxiv.org/abs/2412.06176
- <span id="page-20-19"></span>[2] Sacha-Élie Ayoun, Xavier Denis, Petar Maksimović, and Philippa Gardner. 2025. A hybrid approach to semi-automated Rust verification. Proceedings of the ACM on Programming Languages 9, PLDI (2025), 970–992. doi:10.5281/zenodo.15183201
- <span id="page-20-13"></span>[3] Sarmad Bashir, Alessio Ferrari, Abbas Khan, Per Erik Strandberg, Zulqarnain Haider, Mehrdad Saadatmand, and Markus Bohlin. 2025. Requirements ambiguity detection and explanation with llms: An industrial study. In 2025 IEEE International Conference on Software Maintenance and Evolution (ICSME). IEEE, 620–631. doi:10.1109/ICSME64153.2025.00063
- <span id="page-20-4"></span>[4] The Rust Book. 2026. The Rust Book - Unsafe Rust. Retrieved January 20, 2026 from https://doc.rust-lang.org/book/ch20-01-unsafe-rust.html
- <span id="page-20-25"></span>[5] Saikat Chakraborty, Shuvendu Lahiri, Sarah Fakhoury, Akash Lal, Madanlal Musuvathi, Aseem Rastogi, Aditya Senthilnathan, Rahul Sharma, and Nikhil Swamy. 2023. Ranking llm-generated loop invariants for program verification. In Findings of the Association for Computational Linguistics: EMNLP 2023. 9164–9175. doi:10.18653/v1/2023.findings-emnlp.614
- <span id="page-20-1"></span>[6] Tianyu Chen, Shuai Lu, Shan Lu, Yeyun Gong, Chenyuan Yang, Xuheng Li, Md Rakib Hossain Misu, Hao Yu, Nan Duan, Peng Cheng, Fan Yang, Shuvendu K Lahiri, Tao Xie, and Lidong Zhou. 2026. Automated Proof Generation for Rust Code via Self-Evolution. arXiv:2410.15756 [cs.SE] https://arxiv.org/abs/2410.15756
- <span id="page-20-8"></span>[7] Jacob Cohen. 1960. A Coefficient of Agreement for Nominal Scales. Educational and Psychological Measurement 20, 1 (1960), 37–46. doi:10.1177/001316446002000104
- <span id="page-20-12"></span>[8] Ankush Desai, Vivek Gupta, Ethan K. Jackson, Shaz Qadeer, Sriram K. Rajamani, and Damien Zufferey. 2013. P: safe asynchronous event-driven programming. In ACM SIGPLAN Conference on Programming Language Design and Implementation, PLDI '13, Seattle, WA, USA, June 16-19, 2013, Hans-Juergen Boehm and Cormac Flanagan (Eds.). ACM, 321-332. doi:10.1145/2491956.2462184
- <span id="page-20-9"></span>[9] "Frama-C developers". 2026. "Frama-C". Retrieved January 20, 2026 from https://frama-c.com/
- <span id="page-20-5"></span>[10] "Kani developers". 2026. "Automatic Harness Generation". Retrieved Januarry 20, 2026 from https://model-checking.github.io/kani/reference/experimental/autoharness.html
- <span id="page-20-6"></span>[11] "Kani developers". 2026. "Verify Rust Standard Library Effort". Retrieved January 20, 2026 from https://model-checking.github.io/verify-rust-std
- <span id="page-20-16"></span>[12] The Coq developers. 2026. The Coq proof assistant. Retrieved January 20, 2026 from https://rocq-prover.org
- <span id="page-20-22"></span>[13] "The RVT developers". 2026. "Rust Verification Tools". Retrieved Januarry 20, 2026 from https://project-oak.github.io/rust-verification-tools/about.html
- <span id="page-20-18"></span>[14] Lennard Gäher, Michael Sammler, Ralf Jung, Robbert Krebbers, and Derek Dreyer. 2024. Refinedrust: A type system for high-assurance verification of Rust programs. Proceedings of the ACM on Programming Languages 8, PLDI (2024), 1115–1139. doi:10.1145/3656422
- <span id="page-20-21"></span>[15] Arie Gurfinkel, Temesghen Kahsai, and Jorge A Navas. 2015. SeaHorn: A framework for verifying C programs (competition contribution). In International Conference on Tools and Algorithms for the Construction and Analysis of Systems. Springer, 447–450. doi:10.1007/978-3-662-46681-0. 41
- <span id="page-20-11"></span>[16] Mike He, Zhendong Ang, Ankush Desai, and Aarti Gupta. 2025. Ranking Formal Specifications using LLMs. In Proceedings of the 1st ACM SIGPLAN International Workshop on Language Models and Programming Languages. 51–56. doi:10.1145/3759425.3763386
- <span id="page-20-15"></span>[17] Ralf Jung, Jacques-Henri Jourdan, Robbert Krebbers, and Derek Dreyer. 2017. RustBelt: Securing the foundations of the Rust programming language. Proceedings of the ACM on Programming Languages 2, POPL (2017), 1–34. https://dl.acm.org/doi/10.1145/3158154
- <span id="page-20-10"></span>[18] Shuvendu K. Lahiri. 2024. Evaluating LLM-driven User-Intent Formalization for Verification-Aware Languages. doi:10.34727/2024/ISBN. 978-3-85448-065-5\_19
- <span id="page-20-20"></span>[19] Andrea Lattuada, Travis Hance, Chanhee Cho, Matthias Brun, Isitha Subasinghe, Yi Zhou, Jon Howell, Bryan Parno, and Chris Hawblitzel. 2023. Verus: Verifying rust programs using linear ghost types. Proceedings of the ACM on Programming Languages 7, OOPSLA1 (2023), 286–315. https://dl.acm.org/doi/10.1145/3586037
- <span id="page-20-24"></span>[20] K Rustan M Leino. 2008. This is boogie 2. manuscript KRML 178, 131 (2008), 9. https://www.microsoft.com/en-us/research/wp-content/uploads/2016/12/krml178.pdf
- <span id="page-20-27"></span>[21] K Rustan M Leino. 2010. Dafny: An automatic program verifier for functional correctness. In International conference on logic for programming artificial intelligence and reasoning. Springer, 348–370. https://link.springer.com/chapter/10.1007/978-3-642-17511-4\_20
- <span id="page-20-7"></span>[22] Huan Li, Bei Wang, Xing Hu, and Xin Xia. 2025. Safe4U: Identifying Unsound Safe Encapsulations of Unsafe Calls in Rust using LLMs. Proc. ACM Softw. Eng. 2, ISSTA (2025), 457–480. doi:10.1145/3728890
- <span id="page-20-2"></span>[23] Lezhi Ma, Shangqing Liu, Yi Li, Xiaofei Xie, and Lei Bu. 2025. SpecGen: Automated Generation of Formal Program Specifications via Large Language Models. In 2025 IEEE/ACM 47th International Conference on Software Engineering (ICSE). IEEE Computer Society, 666–666. https://dl.acm.org/doi/10.1109/ICSE55347.2025.00129
- <span id="page-20-17"></span>[24] Yusuke Matsushita, Xavier Denis, Jacques-Henri Jourdan, and Derek Dreyer. 2022. RustHornBelt: a semantic foundation for functional verification of Rust programs with unsafe code. In Proceedings of the 43rd ACM SIGPLAN International Conference on Programming Language Design and Implementation. 841–856. https://dl.acm.org/doi/10.1145/3519939.3523704
- <span id="page-20-3"></span>[25] Md Rakib Hossain Misu, Cristina V Lopes, Iris Ma, and James Noble. 2024. Towards ai-assisted synthesis of verified dafny methods. Proceedings of the ACM on Software Engineering 1, FSE (2024), 812–835. https://dl.acm.org/doi/10.1145/3643763
- <span id="page-20-14"></span>[26] Lahbib Naimi, Abdeslam Jakimi, Rachid Saadane, Abdellah Chehri, et al. 2024. Automating software documentation: Employing Ilms for precise use case description. Procedia Computer Science 246 (2024), 1346–1354. doi:10.1016/j.procs.2024.09.568
- <span id="page-20-26"></span>[27] Kexin Pei, David Bieber, Kensen Shi, Charles Sutton, and Pengcheng Yin. 2023. Can Large Language Models Reason about Program Invariants?. In Proceedings of the 40th International Conference on Machine Learning (Proceedings of Machine Learning Research, Vol. 202), Andreas Krause, Emma Brunskill, Kyunghyun Cho, Barbara Engelhardt, Sivan Sabato, and Jonathan Scarlett (Eds.). PMLR, 27496–27520. https://proceedings.mlr.press/v202/pei23a.html
- <span id="page-20-23"></span>[28] Stuart Pernsteiner, Iavor S. Diatchki, Robert Dockins, Mike Dodds, Joe Hendrix, Tristan Ravich, Patrick Redmond, Ryan Scott, and Aaron Tomb. 2024. Crux, a Precise Verifier for Rust and Other Languages. arXiv:2410.18280 [cs.PL] https://arxiv.org/abs/2410.18280

- <span id="page-21-6"></span><span id="page-21-0"></span>[29] Zvonimir Rakamarić and Michael Emmi. 2014. SMACK: Decoupling source language details from verifier implementations. In Computer Aided Verification: 26th International Conference, CAV 2014, Held as Part of the Vienna Summer of Logic, VSL 2014, Vienna, Austria, July 18-22, 2014. Proceedings 26. Springer, 106–113. doi:10.1007/978-3-319-08867-9
- <span id="page-21-3"></span>[30] The Rust Reference. 2026. The Rust Reference. Retrieved Januarry 20, 2026 from https://doc.rust-lang.org/reference/behavior-considered-undefined.html
- <span id="page-21-4"></span>[31] Alexa VanHattum, Daniel Schwartz-Narbonne, Nathan Chong, and Adrian Sampson. 2022. Verifying dynamic trait objects in rust. In Proceedings of the 44th International Conference on Software Engineering: Software Engineering in Practice (Pittsburgh, Pennsylvania) (ICSE-SEIP '22). Association for Computing Machinery, New York, NY, USA, 321–330. doi:10.1145/3510457.3513031
- <span id="page-21-9"></span>[32] Minghua Wang, Yuxi Ling, Mingzhi Gao, Yuwei Liu, and Lin Huang. 2026. KaPilot Artifact. doi:10.6084/m9.figshare.32834699.v3
- <span id="page-21-8"></span>[33] Minghua Wang, Jingling Xue, Lin Huang, Yuan Zi, and Tao Wei. 2025. UnsafeCop: Towards Memory Safety for Real-World Unsafe Rust Code with Practical Bounded Model Checking. In *Formal Methods*, Andre Platzer, Kristin Yvonne Rozier, Matteo Pradella, and Matteo Rossi (Eds.). Springer Nature Switzerland, Cham, 307–324. https://link.springer.com/chapter/10.1007/978-3-031-71177-0 19
- <span id="page-21-1"></span>[34] Cheng Wen, Jialun Cao, Jie Su, Zhiwu Xu, Shengchao Qin, Mengda He, Haokun Li, Shing-Chi Cheung, and Cong Tian. 2024. Enchanting program specification synthesis by large language models using static analysis and program verification. In *International Conference on Computer Aided Verification*. Springer, 302–328. https://doi.org/10.1007/978-3-031-65630-9 16
- <span id="page-21-2"></span>[35] Chenyuan Yang, Xuheng Li, Md Rakib Hossain Misu, Jianan Yao, Weidong Cui, Yeyun Gong, Chris Hawblitzel, Shuvendu Lahiri, Jacob R Lorch, Shuai Lu, et al. 2025. Autoverus: Automated proof generation for rust code. Proceedings of the ACM on Programming Languages 9, OOPSLA2 (2025), 3454–3482. https://dl.acm.org/doi/abs/10.1145/3763174
- <span id="page-21-5"></span>[36] Mohammad Amin Zadenoori, Jacek Dabrowski, Waad Alhoshan, Liping Zhao, and Alessio Ferrari. 2025. Large Language Models (LLMs) for Requirements Engineering (RE): A Systematic Literature Review. arXiv:2509.11446 [cs.SE] https://arxiv.org/abs/2509.11446
- <span id="page-21-7"></span>[37] Ying Zhang, Peng Li, Yu Ding, Lingxiang Wang, Dan Williams, and Na Meng. 2024. Broadly Enabling KLEE to Effortlessly Find Unrecoverable Errors in Rust. In Proceedings of the 46th International Conference on Software Engineering: Software Engineering in Practice (Lisbon, Portugal) (ICSE-SEIP '24). Association for Computing Machinery, New York, NY, USA, 441–451. doi:10.1145/3639477.3639714