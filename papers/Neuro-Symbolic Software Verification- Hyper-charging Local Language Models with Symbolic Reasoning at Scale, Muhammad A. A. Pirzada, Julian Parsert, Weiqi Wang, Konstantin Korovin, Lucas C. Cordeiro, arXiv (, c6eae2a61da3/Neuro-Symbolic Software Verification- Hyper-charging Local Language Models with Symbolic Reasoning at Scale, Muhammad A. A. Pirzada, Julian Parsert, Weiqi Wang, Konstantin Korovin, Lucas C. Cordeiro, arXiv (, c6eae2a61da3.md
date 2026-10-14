                                         Neuro-Symbolic Software Verification: Hyper-charging Local
                                         Language Models with Symbolic Reasoning at Scale
                                         MUHAMMAD A. A. PIRZADA, The University of Manchester, UK
                                         JULIAN PARSERT, RPTU Kaiserslautern, Germany
                                         WEIQI WANG, The University of Manchester, UK
                                         KONSTANTIN KOROVIN, The University of Manchester, UK
                                         LUCAS C. CORDEIRO, The University of Manchester, UK
arXiv:2606.16886v1 [cs.SE] 15 Jun 2026




                                         Loop invariant synthesis remains a central and pivotal bottleneck in formal software verification. Recent LLM-
                                         based Neuro-Symbolic tools have achieved impressive solve rates. However, these tools rely on proprietary,
                                         often expensive cloud APIs, which constitute a hurdle for privacy-sensitive industrial deployments where the
                                         source code cannot leave the organisation or where cost is a factor. We present VerIbmc, a neuro-symbolic
                                         pipeline that pairs symbolic invariant generation with locally deployable open-weight language models with
                                         the ESBMC verification tool. Our pipeline combines a deterministic symbolic invariant synthesis phase with
                                         an iterative LLM refinement loop driven by structured verifier feedback. In addition, we provide two types of
                                         pipelines that differ in their prompting strategy: Chain-of-Thought vs. Tree-of-Thought.
                                            We conduct an extensive experimental evaluation with five open-weight models (ranging from 7B to
                                         120B parameters) across five benchmark families comprising of 520 problems (499 after excluding 21 with
                                         unavoidable overflow). Overall, the best single configuration (GPT-OSS-120B) solves 431 of 499 problems
                                         (86.4%). Additionally, on the four benchmark suites shared with the strongest cloud-API tools, VerIbmc is
                                         competitive running only on a single local machine. The evaluation shows symbolic invariant synthesis
                                         solves 75 problems without any LLM call and yields up to +35 additional problems for the weakest model.
                                         Importantly, all inference runs entirely on a single local machine using open-weight models – no cloud API
                                         or proprietary model is required. Overall, we demonstrate that a neuro-symbolic approach based on LLMs
                                         can be used effectively for invariant synthesis in a privacy-preserving and energy-efficient manner, without
                                         having to resort to expensive proprietary frontier models locked behind APIs.
                                         CCS Concepts: • Computing methodologies → Artificial intelligence; Natural language processing; •
                                         Software and its engineering → Software verification; • Theory of computation → Invariants.
                                         Additional Key Words and Phrases: Program Verification, Large Language Models, Bounded Model Checking,
                                         Invariant Generation, Neuro-Symbolic AI
                                         ACM Reference Format:
                                         Muhammad A. A. Pirzada, Julian Parsert, Weiqi Wang, Konstantin Korovin, and Lucas C. Cordeiro. 2026.
                                         Neuro-Symbolic Software Verification: Hyper-charging Local Language Models with Symbolic Reasoning at
                                         Scale. 1, 1 (June 2026), 35 pages. https://doi.org/10.1145/nnnnnnn.nnnnnnn

                                         1   Introduction
                                         Software systems increasingly underpin safety-critical and security-sensitive domains, including
                                         but not limited to: transportation [18, 37, 56], healthcare [58], and finance [54]. In these settings,
                                         correctness is not merely desirable but essential. Formal verification provides mathematically
                                         rigorous guarantees that programs satisfy their specifications by reasoning about their behavior for
                                         Authors’ Contact Information: Muhammad A. A. Pirzada, muhammad.pirzada@postgrad.manchester.ac.uk, The University
                                         of Manchester, Manchester, UK; Julian Parsert, julian.parsert@gmail.com, RPTU Kaiserslautern, , Germany; Weiqi Wang,
                                         Weiqi.Wang-2@postgrad.manchester.ac.uk, The University of Manchester, Manchester, UK; Konstantin Korovin, Konstantin.
                                         Korovin@manchester.ac.uk, The University of Manchester, Manchester, UK; Lucas C. Cordeiro, lucas.cordeiro@manchester.
                                         ac.uk, The University of Manchester, Manchester, UK.

                                         2026. ACM XXXX-XXXX/2026/6-ART
                                         https://doi.org/10.1145/nnnnnnn.nnnnnnn


                                                                                                            , Vol. 1, No. 1, Article . Publication date: June 2026.
2                                                                  Pirzada, Parsert, Wang, Korovin, Cordeiro


all possible inputs. Deductive verification, in particular, has become a key approach for reasoning
about real-world software. In this work, we target the problem of loop invariant synthesis, as this
is a central bottleneck for verification. Notably, our techniques are not language specific. However,
its effectiveness depends crucially on the availability of appropriate tooling for loop invariant
verification [38].
   Despite decades of progress in program analysis and not least due to its undecidability, automatic
loop invariant synthesis remains a central bottleneck in formal verification. Symbolic techniques
such as abstract interpretation [26], constraint solving [6, 23, 49], and other methods provide partial
solutions but often struggle with scalability, expressiveness, or the diversity of real-world code.
More recently, data-driven invariant synthesis based on “guess-and-check” methods have become
popular [40, 41, 69, 70, 82, 84, 86].
   Recently, large language models (LLMs) have significantly impacted software engineering prac-
tice [48]. They are now widely used for tasks such as code generation, summarization, debugging,
and test creation [50, 83]. Their ability to learn statistical and semantic regularities from large
code corpora has also made them attractive for formal methods research. In particular, LLMs have
shown promise in generating candidate loop invariants and other verification artifacts by lever-
aging learned patterns of program structure and behavior [17, 51, 80, 81]. This has opened a new
direction in which LLM-based approaches complement traditional symbolic reasoning. However,
many existing approaches rely on proprietary, closed models accessed via external APIs. This
introduces several limitations in the context of formal verification of production software. First,
source code must often be transmitted to third-party services, raising serious confidentiality and
compliance concerns [27, 61, 76]. Second, reliance on external providers reduces reproducibility
and complicates integration into controlled verification pipelines. Third, large-scale models are
computationally and financially expensive and are associated with significant energy consumption
at both training and inference, thereby raising sustainability concerns and limiting their practicality
for continuous or large-scale verification workflows [20, 30].
   These challenges motivate the use of open-weight and open-source language models that can be
deployed locally within an organization’s infrastructure. Such models enable full control over data,
eliminate the need to expose proprietary code externally, and improve reproducibility of verification
results. Importantly, smaller and medium-sized models also offer a significant advantage in energy
efficiency, making them better suited for sustained use in industrial software verification pipelines,
where repeated analysis and iteration are required.
   In this work, we investigate the use of locally deployable, open-weight language models for loop
invariant synthesis in C programs. The pipeline is language-agnostic by design: it interacts with the
verifier only through a loop-invariant-checking interface, and ESBMC supports languages beyond
C/C++ (e.g. Python) through dedicated front-ends. Our evaluation focuses on C for comparability
with existing tools; we do not claim empirical results on other languages. Our goal is to support
formal verification of production software in environments where privacy, reproducibility, and
resource efficiency are critical requirements. By operating entirely on internal infrastructure, our
approach avoids exposing external data while enabling seamless integration into existing deductive
verification toolchains. We present a complete pipeline that integrates locally served LLMs into a
loop invariant synthesis and verification loop. The system generates candidate invariants, validates
them with a formal verification backend, and iteratively refines them in response to counterexamples
or proof failures. When the iteration budget is exhausted without finding a valid invariant, the
pipeline then reports the outcome as unknown and terminates. The method is always sound but
incomplete due to the inherent undecidability of the problem. This structured interaction allows
the verifier to guide the model, improving both precision and robustness of generated invariants.
We evaluate our approach on a representative set of verification benchmarks and demonstrate that

, Vol. 1, No. 1, Article . Publication date: June 2026.
Neuro-Symbolic Software Verification: Hyper-charging Local Language Models with Symbolic Reasoning at Scale           3


locally deployed open-weight models can effectively support loop invariant generation across a
wide range of programs. Our results show that when properly integrated into a formal verification
loop, such models can significantly reduce annotation effort while maintaining strong performance
on verification tasks.
   Overall, this work demonstrates that combining LLMs with symbolic reasoning can be applied
to invariant synthesis with great effect. When using relatively small open-weight models as part of
this neuro-symbolic approach, we can verify programs in a privacy-preserving, energy-efficient
manner, without relying on proprietary cloud-based systems. With these verification pipelines we
take a step toward scalable, reproducible, and industry-ready AI-assisted formal verification of
production software. To summarize, our contributions are:
    • We present a neuro-symbolic method that integrates LLMs with symbolic reasoning using
      ESBMC as a verification oracle for automated loop invariant synthesis in C programs.
    • We design and experiment with inference strategies spanning pure LLM, symbolic-guided,
      and Tree-of-Thoughts (ToT) variants, providing a systematic comparison of neural and
      neuro-symbolic approaches.
    • We demonstrate that symbolic feedback (provable invariant atoms fed as context to the LLM)
      provides consistent gains for weaker models, yielding up to 35 additional solved benchmarks
      over a pure-LLM baseline (Llama-3.1-8B: 307→342).
    • We describe and evaluate the effect of different prompting strategies including, Chain-of-
      Thought (CoT) and ToT prompting on loop invariant synthesis. We also experiment different
      reasoning styles in the prompting stages (Inductive, Hoare Logic, Horn Clause, and direct
      derivation).
    • We conduct a large-scale evaluation across five language models, four inference strategies,
      and five benchmark families (520 problems), including SV-COMP benchmarks, providing a
      comprehensive assessment of LLM-guided invariant synthesis at scale (10,400 per-problem
      outcomes).

2   Theoretical Background
In deductive verification, the correctness problem is reduced to proving logical formulas called
verification conditions (VCs). These conditions encode the semantics of the program together with
its specification. If all generated verification conditions are valid, then the program is considered
correct with respect to the specification. Modern verification frameworks usually translate programs
into an intermediate logical representation based on first-order logic, often extended with theories
such as arithmetic, arrays, bit-vectors, or algebraic data types. Automated reasoning about these
formulas is delegated to Satisfiability Modulo Theories (SMT) solvers. Popular SMT solvers such as
Z3 [28], Boolector [14], MathSAT [21], Yices [32], and Bitwuzla [62] are widely used in program
verification. In the context of deductive verification, the verifier generates formulas representing
correctness obligations and submits them to an SMT solver. If the solver proves the formulas
unsatisfiable under the negation of the specification, then the corresponding verification condition
holds. Additionally, SMT solvers provide efficient reasoning procedures for many theories relevant
to software verification and therefore form the backbone of many modern verification tools.
   Furthermore, model checking [22] is another major verification paradigm. Instead of proving
correctness via symbolic logical derivations alone, model checking systematically explores the
state space of a system to determine whether a specification holds. Bounded Model Checking
(BMC) is a formal verification technique introduced by Biere et al. [9, 10] that systematically
checks whether a system violates a given safety property within a finite number of execution
steps, known as the bound 𝑘. The fundamental idea is to unroll the program’s transition relation 𝑘

                                                                 , Vol. 1, No. 1, Article . Publication date: June 2026.
4                                                                  Pirzada, Parsert, Wang, Korovin, Cordeiro


times, producing a propositional formula that is satisfiable if and only if an error state is reachable
within 𝑘 steps. A central limitation of plain BMC is its inherent incompleteness: a clean result
for bound 𝑘 does not guarantee correctness for 𝑘 + 1 or beyond. To address this, 𝑘-induction [71]
extends BMC with a proof step: if no violation exists within 𝑘 steps and every 𝑘-step execution
prefix that satisfies the invariant candidate also satisfies it at step 𝑘 + 1, the property is proven
for all depths. However, 𝑘-induction only succeeds when the candidate invariant is already strong
enough; for programs with complex loop behaviour, a strong loop invariant must be supplied to
strengthen the inductive hypothesis. This is precisely where invariant inference becomes critical: a
sufficiently strong invariant, when assumed at the loop head, allows the BMC engine to complete a
full inductive proof without requiring deeper unrolling.

2.1    Loop Invariants
First of all, a loop is a control-flow construct that repeatedly executes a body, as long as a guard 𝑔
evaluates to true [45]. Since the number of iterations is either large or unbounded, reasoning about
a loop requires a finite characterization of its behavior – that holds across all iterations. This is
where loop invariants are extremely beneficial. A loop invariant is a predicate 𝜑 that must satisfy
three conditions [36, 45]:

    (1) Initiation: 𝜑 holds before the first iteration (pre ⇒ 𝜑).
    (2) Consecution: 𝜑 is preserved by every iteration ({𝜑 ∧ 𝑔} body {𝜑 }).
    (3) Sufficiency: 𝜑 together with the negated loop guard implies the required post-condition
        (𝜑 ∧ ¬𝑔 ⇒ 𝜓 ).

  A loop invariant satisfying all three conditions is called an inductive loop invariant. A predicate
that merely holds at the loop entry point but is not preserved by the loop body is non-inductive
and therefore insufficient to discharge the associated verification condition.

  The Challenge of Invariant Synthesis. Invariant synthesis is undecidable in general [36, 45, 66]:
no algorithm can, given an arbitrary program and post-condition, always return an adequate loop
invariant. The difficulty is not confined to pathological programs. Even for loops over integer
variables with simple control flow, an adequate invariant may require non-linear arithmetic, con-
junctions of many linear constraints, or ghost variables absent from the original source. Hence,
practical invariant synthesis tools must navigate a search space whose membership problem is itself
undecidable, trading completeness for tractability on the program classes that arise in practice.

   ESBMC. (Efficient SMT-Based Context-Bounded Model Checker) [24, 39, 73] is an industrial-
strength open-source verification tool for C/C++ programs. It front-ends the LLVM/Clang compiler
infrastructure, performs pointer analysis, arithmetic overflow and array bounds checking, and
encodes the resulting verification conditions in SMT-LIB2, discharging them via one of several back-
end solvers (Z3 [28], Boolector [14], MathSAT [21], Yices [32], Bitwuzla [62]). Beyond plain BMC,
ESBMC supports 𝑘-induction and a loop-invariant-checking mode that compiles the program to
ESBMC’s GOTO representation and injects a user-supplied predicate at the loop head, establishing
correctness for all loop iterations when a sufficient invariant is supplied. Throughout this paper,
ESBMC serves as the formal verification back-end for every invariant candidate produced by
the LLM-based components of our approach. We invoke ESBMC exclusively in loop-invariant-
checking mode with 𝑘-induction as the underlying proof rule; we do not rely on plain BMC, and
our soundness argument therefore does not depend on a bounded unrolling.

, Vol. 1, No. 1, Article . Publication date: June 2026.
Neuro-Symbolic Software Verification: Hyper-charging Local Language Models with Symbolic Reasoning at Scale           5


2.2   LLMs
LLMs are deep neural sequence models, trained on web-scale corpora of natural language and
source code via a next-token prediction objective. Popular network types are transformer models,
which allow each token in a sequence to attend to every other token, enabling the model to capture
long-range syntactic and semantic dependencies that earlier recurrent architectures struggled to
represent. Scaling the number of parameters, training tokens, and compute following the empirical
laws described by Kaplan et al. [52] and subsequently refined as chinchilla scaling [47] has produced
a family of increasingly capable models: GPT [1], Claude [3], Gemini [74], Llama [43, 75], and
Alibaba’s Qwen [4, 64] and DeepSeek-Coder [44], among others.
   Furthermore, a defining capability of sufficiently large models is in-context learning (ICL) [13]: by
conditioning the model on a prompt that contains a handful of input-output examples, it generalises
to new inputs in the same format without any gradient update to its parameters. This is distinct from
traditional supervised learning and is particularly valuable in formal verification, where labelled
(program, invariant) pairs are scarce and domain-specific fine-tuning datasets are expensive to
construct. For code-related tasks specifically, LLMs trained on large repositories of open-source
software have internalised the syntactic conventions, common idioms, and proof patterns of widely
used programming languages and verification frameworks. Studies such as HumanEval [19] and
SWE-bench [50] demonstrate that frontier models can solve a significant fraction of competitive
programming and real-world bug-fixing tasks. In the context of loop invariant inference, this prior
exposure to annotated code, SMT-LIB formulae, and formal specification languages means that
LLMs can often produce plausible invariant candidates from program text alone, without requiring
domain-specific training.
   Despite these strengths, LLMs are fundamentally probabilistic predictors and are known to
hallucinate: they produce plausible-sounding but factually or logically incorrect outputs with
non-trivial probability, including syntactically valid but semantically incorrect program assertions.
In a verification context, a hallucinated invariant that is not inductively valid would cause a sound
verifier to reject it, but could also mislead a developer who does not independently check it. This
makes LLMs unsuitable as standalone verifiers. The dominant design pattern in the literature
is therefore a guess-and-check architecture: the LLM acts as a heuristic proposal function that
generates candidate invariants, while a formal tool verifies the given candidate.

2.3   Prompt Engineering: CoT and ToT Reasoning
Prompting describes the presentation of a task description which is given as an input to the LLM.
Standard prompting often fails on tasks that require multi-step reasoning, because the model
is forced to compress all intermediate reasoning into a single generation step. Two prompting
strategies have emerged as principled solutions to this limitation, both of which are directly
applicable to loop invariant inference: CoT and ToT prompting.
  CoT prompting [77]. This elicits explicit intermediate reasoning by including, in the few-shot
prompt, example solutions that demonstrate step-by-step derivation rather than simply showing
input-output pairs. The model is implicitly encouraged to emit a sequence of reasoning steps (i.e. a
chain of thought) before producing its final answer. Wei et al. [77] showed that CoT dramatically
improves performance on arithmetic, commonsense, and symbolic reasoning benchmarks, and that
the benefit is an emergent property of models with sufficiently many parameters (approximately
100B in the original study, though subsequent work has replicated the effect in smaller models with
better training). In the invariant synthesis context, a CoT prompt might instruct the model to: (i)
identify the loop’s modified variables and their ranges; (ii) determine how each variable evolves
across iterations; (iii) derive a relational constraint that is preserved by the loop body; and (iv)

                                                                 , Vol. 1, No. 1, Article . Publication date: June 2026.
6                                                                            Pirzada, Parsert, Wang, Korovin, Cordeiro




                                              Fig. 1. VerIbmc Flow Diagram



express that constraint as a formal assertion. This structured decomposition mirrors the manual
reasoning process of a verification engineer and has been shown to improve the syntactic validity
and semantic correctness of generated invariants compared to direct prompting [78, 80, 81].
   A particularly effective variant is zero-shot CoT [55], in which the model is prompted with the
phrase “Let’s think step by step” (or a domain-appropriate equivalent such as “Let’s derive the
loop invariant step by step”) without providing explicit few-shot examples. This eliminates the
need to curate high-quality example solutions and has been shown to achieve performance close to
few-shot CoT on many reasoning benchmarks, making it practical in settings where annotated
(program, invariant) examples are scarce.
   ToT prompting [85] generalises CoT via maintaining a tree of partial reasoning states rather than
a single linear chain. At each node in the tree, the model generates 𝑘 alternative continuations each
representing a different hypothesis about the next step of the derivation. A state evaluator (which
may be the LLM itself, a symbolic checker, or a learned heuristic) scores each continuation and
determines which branches to expand further, implementing a best-first or breadth-first search over
the space of reasoning paths. ToT was introduced by Yao et al. [85] and demonstrated significant
improvements over CoT on tasks requiring planning and backtracking, such as the Game of 24 and
creative writing with structural constraints.

3    The VerIbmc System
VerIbmc is a neuro-symbolic pipeline for loop invariant synthesis (Figure 1). Its design follows
a single principle: escalate only when necessary. Cheap, symbolic reasoning runs first, and the
LLM is invoked only on the residue that symbolic methods cannot close. Notably, every candidate,
regardless of its origin, is discharged by ESBMC before it is accepted. The pipeline is therefore
sound by construction, and its LLM budget is spent exclusively on the problems that need it.
   The pipeline comprises three phases. Phase 0 runs ESBMC on the unannotated program: if the
program is trivially safe or provably unsafe, the pipeline exits immediately, so no synthesis effort is
spent on problems the verifier already decides. Phase 1 symbolically enumerates candidate invariant
atoms by pairwise comparison of loop-entry variables and constants, retaining those that ESBMC
proves inductive (Section 3.2). This phase is deterministic and requires no LLM call; it establishes
a verified floor of invariant knowledge that every subsequent LLM interaction builds on. Phase 2
is the LLM refinement loop (Section 3.2): candidates are iteratively proposed, verified by ESBMC,
decomposed into atoms, and recombined, with the verifier’s verdicts fed back into subsequent
prompts as structured evidence.

, Vol. 1, No. 1, Article . Publication date: June 2026.
Neuro-Symbolic Software Verification: Hyper-charging Local Language Models with Symbolic Reasoning at Scale           7


   On top of this pipeline we define four inference strategies along two independent design choices
(Section 3.3). The verifier-feedback axis controls whether the LLM receives Phase 1’s symbolic
prior: Basic runs all three phases, whereas LLM-Only skips Phase 1 and, within Phase 2, it also
forgoes the atom-level decomposition, filtering, and recombination that Basic applies to every LLM
proposal – accepting a candidate only when it is inductive as a whole. LLM-Only thus serves as
the ablation baseline that isolates raw LLM capability. The reasoning-structure axis controls prompt
organisation: each base strategy runs either with standard CoT prompting or with a ToT variant
that explores four derivation styles in parallel (Section 3.5). Section 3.3 details the four strategies.

3.1   ESBMC Loop Invariant Checker
Invariant synthesis and invariant checking are separate phases in VerIbmc. The checker is treated
as a black-box primitive: for a program 𝑃 and a candidate invariant 𝜑 (a C Boolean expression
placed at the loop head), it returns provable, disprovable, or unknown. We realise this primitive
using ESBMC’s loop-invariant-checking mode [34].
  Two operating modes. VerIbmc invokes the checker in two structurally different ways. Let 𝑃 be
the annotated program, 𝜓 its post-condition, and 𝜑 a candidate invariant.
  (a) Atomic inductivity test. To classify a single atom, the post-condition 𝜓 is stripped from 𝑃. 𝑔 is
used as a guard which is evaluated to true,and 𝜑 is inserted as the only invariant. ESBMC’s decision
then reduces to the validity of

                           VC𝜑(𝑎) ≡ pre → 𝜑 ∧ 𝜑 ∧ 𝑔 ∧ body → 𝜑 ′ ,                                  (1)
                                                                         

where pre is the formula accumulated up to the loop head and 𝜑 ′ renames each variable in 𝜑 to its
post-body version. A successful verdict witnesses that 𝜑 is inductive; failed exhibits a concrete
countermodel to one of the two conjuncts; timeout or parse error maps Ó    to unknown.
  (b) Whole-program verification. To test whether a conjunction 𝜑 = 𝑖 𝜑𝑖 , where each 𝜑𝑖 is a
provably-inductive atom, closes the proof, 𝜑 is inserted and 𝜓 is kept; ESBMC then discharges both
inductivity obligations together with the post-condition,

                               VC𝜑(𝑏 ) ≡ VC𝜑(𝑎) ∧ 𝜑 ∧ ¬𝑔 → 𝜓 .                                  (2)
                                                                   

A successful verdict terminates the pipeline; failed indicates that 𝜑 is inductive but too weak to
entail 𝜓 —a spurious counter-example in the sense of [63]. VerIbmc treats this as a signal rather than
a defect: the atoms in 𝜑 remain provable, and recombination (Section 3.2) searches for additional
atoms whose conjunction closes VC𝜑(𝑏 ) .

3.2   VerIbmc Phases
As mentioned, VerIbmc consists of 3 main phases. The first phases are simple symbolic reasoning
while the last is an iterative procedure that iteratively queries an LLM and subsequently filters and
symbolically manipulates the feedback.

Phase 0: Baseline Verification
Before any invariant is generated, VerIbmc uses ESBMC to verify the unannotated program 𝑃.
This ensures that we do not waste time on invariant synthesis when the verification conditions
are trivial or ESBMC’s standard methods are already strong enough to discharge them. In case of
success or failure, we terminate immediately; on an unknown result, we proceed to the next phase.
This procedure is deterministic and independent of model or strategy choice: its verdict depends
only on ESBMC and the program.

                                                                 , Vol. 1, No. 1, Article . Publication date: June 2026.
8                                                                                Pirzada, Parsert, Wang, Korovin, Cordeiro


Phase 1: Symbolic Candidate Generation
When Phase 0 returns Unknown, VerIbmc synthesises invariant candidates by symbolically
enumerating atoms without invoking an LLM. For each loop ℓ in 𝑃, let 𝑉ℓ be the set of variables
live at the loop head and 𝐶 ℓ the set of integer constants appearing in the loop body. We enumerate
all atomic candidate atoms of the form
                                  𝑣𝑖 ⊲⊳ 𝑣 𝑗    𝑣𝑖 ⊲⊳ 𝑐      with    ⊲⊳∈ {<, ≤, =, ≠, ≥, >}                             (3)
Each atom is submitted to ESBMC in atomic-inductivity mode (Eq. 1) and    Ó placed in one of three
stores: P (provable), D (disprovable), or U (unknown). The conjunction P is then submitted in
whole-program mode (Eq. 2); if it closes the proof, the pipeline returns Safe without any LLM call.
Otherwise, the populated stores are carried into Phase 2 as prior knowledge and grow monotonically
as further atoms are synthesised and verified.
  Worst-case complexity. For a loop with |𝑉 | live variables and |𝐶 | integer constants, Phase 1
enumerates at most
                                    𝑁 atoms = 6 |𝑉 | 2 + |𝑉 | · |𝐶 |                               (4)
                                                                     
                          2
candidate atoms (the |𝑉 | term covers all ordered variable–variable pairs, including 𝑖=𝑗; self-
comparisons such as 𝑥 ≤ 𝑥 are trivially true and filtered before ESBMC submission). Adding one
extra relation symbol would scale the count by 7/6; adding one constant adds 6|𝑉 | candidates. The
enumeration is therefore linear in |𝐶 | and quadratic in |𝑉 |, remaining tractable for the programs in
our benchmark set; for multi-loop programs, Phase 1 runs independently per loop ℓ ∈ 𝑃.
    Example 3.1. The following example is benchmark from the code2inv set:
int x = 1 , y = nondet ();
while ( x <= 10) { y = 10 - x;                            x ++; }
assert ( y < 10);
We have 𝑉 ={𝑥, 𝑦} and 𝐶={0, 1, 10}; Eq. (4) gives at most 6(4 + 6) = 60 candidate atoms. ESBMC
classifies 𝑥 ≥ 1 and 𝑥 ≥ 0 as provable. Atoms constraining 𝑦 alone—such as 𝑦 ≥ 0—are classified as
disprovable: since 𝑦 is nondeterministic at the first loop entry, no entry-point constraint on 𝑦 holds
unconditionally. The conjunction {𝑥 ≥ 1, 𝑥 ≥ 0} is checked but not strong enough to prove the
assertion 𝑦 < 10. The pipeline enters Phase 2 with P = {𝑥 ≥ 1, 𝑥 ≥ 0}.

Phase 2: LLM Refinement Loop
In this phase VerIbmc iteratively prompts an LLM for an invariant which we parse, check and
in case of failure mutate to verify related invariants. At each iteration, for every loop ℓ in 𝑃, we
construct a prompt that includes the loop’s C source, the current contents of P, D, and U as
feedback, and few-shot examples drawn from the prompting strategy (Section 3.4). Note that the
3 stores that are populated are the only “feedback” we propagate from one iteration to the next.
We also experimented with including concrete ESBMC counterexamples directly in the prompt,
but found this did not improve performance and often degraded it, particularly for smaller models.
We attribute this to the well-documented tendency of LLMs to lose relevant information when the
context grows long [31, 60]: the additional counterexample trace increases prompt length without
providing actionable signal beyond what the disprovable store D already encodes in a compact form.
After submitting the prompt to the LLM we parse the response and for each invariant candidate 𝜑
we:
   (1) Attempt to verify the program using 𝜑. In case of success, we terminate.
   (2) In case of no success, we decompose 𝜑 into its sub-formulas and check individually (cf. Eq. (1))
       and add each to the appropriate store (P, D, U).

, Vol. 1, No. 1, Article . Publication date: June 2026.
Neuro-Symbolic Software Verification: Hyper-charging Local Language Models with Symbolic Reasoning at Scale           9


  (3) Finally, we use P as an invariant to verify the program where in case of success, we
                      Ó
      terminate with a successful verdict. Otherwise, we continue with the next iteration.
In case of parsing errors, we simply continue with the next iteration. In order to improve the
number of parsing errors the prompt also contains instructions and examples of syntactically
correct invariant candidates.
  Example 3.2. Consider the program from Example 3.1. Given P={𝑥 ≥ 1, 𝑥 ≥ 0} the LLM may
generate the invariant:
y == 0 && ( x == 1 || y + x == 11)
Step 1: ESBMC attempts whole-program verification and fails: the conjunct y == 0 is not inductive
since 𝑦 is nondeterministic at loop entry. Step 2: VerIbmc decomposes the formula into its conjuncts
y == 0 and x == 1 || y + x == 11 and checks each individually. ESBMC classifies y == 0
as disprovable (addedÓto D) and x == 1 || y + x == 11 as provable (added to P). Step 3: The
updated conjunction P = {𝑥≥0, 𝑥≥1, 𝑥=1∨𝑦+𝑥=11} is submitted for whole-program verification.
Combined with the negated guard 𝑥 > 10, we obtain 𝑥≥11 and 𝑦+𝑥=11, hence 𝑦 = 11−𝑥 ≤ 0 < 10.
This is sufficient to prove the assertion and VerIbmc terminates successfully.

3.3   Inference Strategies
   Basic Strategy. Basic chains all three phases with a single LLM. Phase 0 first checks whether
ESBMC can decide the program unaided; if not, Phase 1 accumulates provable symbolic atoms and
tests their conjunction. Only if that conjunction is insufficient does Phase 2 invoke the LLM, for up
to 𝑁 iterations; each call contributes atoms to P, which feed forward as context into subsequent
prompts. The LLM is thus never asked to rediscover what the symbolic phase has already established:
it starts from a verified partial invariant and is steered toward the atoms that are still missing.
   LLM-Only Strategy. LLM-Only omits Phase 1: after Phase 0, the pipeline enters Phase 2 with
empty stores. The provable/disprovable/unknown lists are used only for deduplication, preventing
re-submission of previously evaluated candidates, and carry no symbolic prior into the prompt.
This strategy is structurally analogous to ESBMC-ibmc [63] and serves as the primary ablation
baseline: any gap between Basic and LLM-Only is attributable to Phase 1’s symbolic augmentation.
   ToT Variants. Each base strategy has a ToT counterpart (Basic-ToT, LLM-Only-ToT) that replaces
single-strategy prompting in Phase 2 with a two-stage multi-branch search: a scouting stage issues
one LLM call per derivation style (Section 3.4), scores each style by the inductive atoms it yields,
and a refinement stage concentrates the remaining iteration budget on the top-two styles. The
verifier-feedback axis is unaffected: Basic-ToT retains the Phase 1 prior, LLM-Only-ToT does not.
The search algorithm and scoring function are detailed in Section 3.5.

3.4   Prompt Engineering
In the default case, we use a few-shot CoT prompt containing a task instruction, the target C
program, the current invariant store as feedback, and one of four example sets demonstrating
different derivation styles. These prompt strategies are:
    Inductive with Explanation. Each example shows the program, the invariant annotation,
       and a step-by-step inductive proof (base case, inductive step, and sufficiency check). This
       style targets models that benefit from explicit reasoning traces.
    Inductive without Explanation. The same programs and annotations are shown but without
       derivation text. This compact style reduces prompt length and is suited for models sensitive
       to context size.

                                                                 , Vol. 1, No. 1, Article . Publication date: June 2026.
10                                                                  Pirzada, Parsert, Wang, Korovin, Cordeiro


      Hoare Logic Derivation. Each example derives the invariant by constructing and discharging
       the Hoare triple {𝐼 ∧ 𝐵} 𝑆 {𝐼 }, making the consecution obligation explicit. This style anchors
       the model’s generation in the formal semantics of the loop.
      Horn Clause Derivation. Each example encodes the loop as a constrained Horn clause system
       and derives the invariant by logical consequence. This style is particularly effective for non-
       linear arithmetic invariants.
In the basic strategy, a single example set is selected for the entire run. In the ToT variants, all four
sets are explored in parallel and the best two are selected for refinement (Section 3.5).

3.5     ToT Refinement
Firstly, let 𝜋𝑠 (I) denote the prompt template for strategy 𝑠, augmented with the current set of
verified invariant atoms I. Next, let 𝜋𝑠fb (I) denote the feedback-augmented prompt for strategy 𝑠,
which extends 𝜋𝑠 (I) with the counterexample and verification outcome from the previous LLM
candidate.


Algorithm 1 Invariant Synthesis using ToT prompting.
Require: 𝑃, 𝑀, strategies S, 𝑅=10, 𝑇
Ensure: Verification result
 1: if Vfy(𝑃, ∅)=Succ then return Success
 2: if Vfy(𝑃, ∅)=Fail then return Unsolvable
 3: I ← ∅
 4: for all 𝑠 ∈ S do                                           ⊲ Phase 1: one attempt per strategy
 5:     𝐶 ← LLM(𝑀, 𝜋𝑠 (I))
 6:     if 𝐶 verifies then return Success
 7:     add provable atoms of 𝐶 to I
 8:     if I verifies then return Success
 9:     score(𝑠) ← (0.6|P𝑠 | − 0.3|D𝑠 | + 0.1|U𝑠 |)/|P𝑠 ∪ D𝑠 ∪ U𝑠 |
10:     if Elapsed() ≥ 𝑇 then return Timeout
11: end for
12: S ∗ ← top2 (S); 𝑟 ← 0; step[𝑠] ← 0
13: while 𝑟 < 𝑅 and S ∗ ≠ ∅ do                                         ⊲ Phase 2: top-2 refinement
14:     𝑠 ← S ∗ [𝑟 mod |S ∗ |]
15:     if step[𝑠] ≥ 𝐾𝑠 then
16:         S ∗ ← S ∗ \ {𝑠}; continue
17:     end if
18:     𝑟 += 1; step[𝑠] += 1
19:     𝐶 ← LLM(𝑀, 𝜋𝑠fb (I))
20:     if 𝐶 verifies then return Success
21:     add provable atoms of 𝐶 to I
22:     if I verifies then return Success
23:     if 𝑟 mod 6=0 then
24:         S ∗ ← top2 (S); step[·] ← 0                                  ⊲ Re-rank every 6 rounds
25:     end if
26:     if Elapsed() ≥ 𝑇 then return Timeout
27: end while
28: return Failure


, Vol. 1, No. 1, Article . Publication date: June 2026.
Neuro-Symbolic Software Verification: Hyper-charging Local Language Models with Symbolic Reasoning at Scale          11


   We hypothesise that ToT is well-suited to loop invariant inference for multiple reasons. First, the
space of candidate invariants is large and non-monotone: a partial invariant that is not provable
become valid once it is weakened. Second, the symbolic verifier provides a structured evaluation
signal, which can be used directly as the state evaluator to prune branches early. Third, multiple
candidate invariants can be checked in parallel using independent SMT solver processes, aligning
naturally with ToT’s multi-branch search structure. These properties motivate the design of our
ToT-based prompting strategy.
   Algorithm 1 receives: program 𝑃; model 𝑀; strategy set S = {𝑆 1, 𝑆 2, 𝑆 3, 𝑆 4 } corresponding to
the four CoT example sets (Section 3.4); maximum refinement rounds 𝑅=10; and timeout 𝑇 . The
goal is to identify—via a single scored pass over all four strategies in Stage 1—which prompting
style generates the most inductive atoms for the given program, then concentrate the remaining
iteration budget on the top-2 strategies in Stage 2 rather than committing blindly to one from the
start. It proceeds in two stages.
   Stage 1 (strategy scoring). One LLM call is made per strategy 𝑠 ∈ S = {𝑆 1, 𝑆 2, 𝑆 3, 𝑆 4 }, each using
its corresponding example set. For each strategy 𝑠, let P𝑠 , D𝑠 , U𝑠 be the provable, disprovable, and
unknown atom sets accumulated from 𝑠’s Stage 1 response. A score is computed:
                                             0.6 |P𝑠 | − 0.3 |D𝑠 | + 0.1 |U𝑠 |
                              score(𝑠) =                                       .                                    (5)
                                                      |P𝑠 ∪ D𝑠 ∪ U𝑠 |
Provable atoms carry the most signal toward a successful proof; disprovable atoms are penalised
because they contribute no usable invariant content; unknown atoms receive a small positive
weight to encourage exploration of strategies that produce candidates the verifier cannot yet
classify. A strategy achieving whole-program verification short-circuits with score(𝑠) = 1.0; a
strategy producing no atoms receives a fallback score of 0.1.
   Traditionally, ToT prompting asks the LLM to self-evaluate and rank the strategies [85]. However,
in our implementation the actual top-2 selection in Algorithm 1 uses the ESBMC-derived score
(Eq. 5), not the LLM’s self-assessment: the LLM cannot run the verifier and therefore lacks ground
truth to self-evaluate reliably. Although we override the LLM’s preference with the ESBMC-derived
score (Eq. 5), we retain the self-ranking instruction in the prompt. Asking the model to compare
strategies and commit to a preference before generating candidates acts as a think-before-generate
step: empirically, this structured prompt discipline produces more coherent and more frequently
inductive invariant proposals than unstructured generation, even though the expressed preference
itself is not used by the search controller.
   Stage 2 (top-2 refinement). The two highest-scoring strategies proceed to a refinement loop of
up to 𝑅=10 rounds, cycling between the two. Every 6 rounds the scores are recomputed from the
full accumulated evidence and the top-2 selection is refreshed, allowing a previously lower-ranked
strategy to re-enter. This interval was chosen so that, within the 𝑅=10 round budget, each selected
strategy accumulates at least three rounds of evidence before re-evaluation. The per-strategy
counter step[𝑠] caps each strategy’s contribution at 𝐾𝑠 = ⌊𝑅/|S ∗ |⌋ rounds (i.e. an equal share of
the total budget); exhausted strategies are removed from S ∗ .

4   Experimental Evaluation
We conduct an experimental evaluation of VerIbmc to answer the following research questions:
    RQ1: Can symbolic methods combined with locally deployed open-weight models effectively
     synthesise loop invariants?
    RQ2: Does this neuro-symbolic method advance the state of the art in loop invariant synthesis?

                                                                 , Vol. 1, No. 1, Article . Publication date: June 2026.
12                                                                Pirzada, Parsert, Wang, Korovin, Cordeiro


    RQ3: What effect does Tree-of-Thoughts prompting have on the efficacy of neuro-symbolic
       invariant synthesis?
    RQ4: How do the individual pipeline phases contribute to the overall solve rate?
   The experiments involve five LLMs, four inference strategies, and eleven benchmark suites, to-
talling 10 400 per-problem outcomes. A supplementary dual-LLM experiment is reported separately
in Appendix D. The code is available at: https://zenodo.org/records/20690105. We also conduct
experiments to compare with other tools that represent the state-of-the-art (SOTA). These consist of
the following: ESBMC [39, 73], CPAchecker [7], 2ls [68], LaM4Inv [80], Clause2Inv [15], Code2Inv
[72], and LORIS [59].

4.1    Experimental Setup
  Benchmark suites. We evaluate on five benchmark families totalling 520 problems. Four are
established loop-invariant synthesis suites: C2I (133 problems), introduced with Code2Inv [72];
L4I-SVC (99) and L4I-SY (84), introduced with LaM4Inv [80] and drawn from SV-COMP 2024 and
SyGuS 2019 respectively; and NL (50), the non-linear suite introduced with Clause2Inv [15]. The fifth
family, SVC (154), is our own selection from the latest SV-COMP edition [8]: the complete loops,
loops-crafted-1, loop-acceleration, loop-crafted, loop-invariants, loop-new, and loop-
simple subcategories. Unlike the four established suites, which were syntactically restricted to fit
the front-ends of the tools that introduced them, the SVC family is unfiltered: it retains programs
with arrays, nested and multiple loops, pointers, and function calls.
  Of the 520 problems, 21 are unsolvable under machine-integer semantics (ESBMC reports
Verification Failed due to unavoidable overflow), leaving an effective pool of 499 problems.
All solve rates in this section use 499 as the denominator; RQ4 further decomposes this pool by
pipeline phase.
  Hardware and software. All models are served locally via Ollama on a server running Ubuntu
22.04.5 LTS and equipped with four NVIDIA RTX A6000 GPUs (48 GB each). ESBMC v8.2 serves as
the backend verifier throughout all experiments.
  Models. We focus on open-weight models that can be deployed entirely on local infrastructure,
avoiding the need to transmit source code to external services. We evaluate five models spanning
7B to 120B parameters: GPT-OSS-120B [2], GPT-OSS-20B [2], Qwen2.5-32B-Instruct [64], Qwen2.5-
7B-Instruct [64], and Llama-3.1-8B [43]. The GPT-OSS models use their default temperature of 1.0,
while the remaining models use Ollama’s default temperature setting of 0.8.
   Inference strategies. We evaluate four inference strategies built from two independent design
choices. The first is verifier feedback: the LLM-Only strategy enters Phase 2 directly after Phase 0
with empty atom stores, so the LLM receives no symbolic prior and each LLM proposal is accepted
only if it is inductive as a whole; the Basic strategy runs the full three-phase pipeline (Figure 1),
augmenting each LLM call with the provable atoms accumulated in Phase 1 and, in addition,
decomposing every LLM proposal into atoms, discarding the non-inductive ones, and recombining
the provable remainder into the strongest verified invariant. LLM-Only therefore differs from Basic
along two coupled mechanisms—the symbolic prior and this atom-level filtering/recombination
of LLM output—rather than the symbolic prior alone, and serves as the primary ablation baseline
isolating raw LLM capability from symbolic augmentation. The second design choice is reasoning
structure. Each of the two strategies above can be run with standard CoT prompting or with a
ToT variant, denoted by the suffix -tot, which explores all four prompting styles in parallel before
concentrating the iteration budget on the top-two (Section 3.5). This yields four strategies in total:
LLM-Only, Basic, LLM-Only-ToT, and Basic-ToT.

, Vol. 1, No. 1, Article . Publication date: June 2026.
Neuro-Symbolic Software Verification: Hyper-charging Local Language Models with Symbolic Reasoning at Scale          13


                                                         Benchmarks
          LLM Model           Strategy                                                        IR     Total
                                            C2I     L4I-SVC L4I-SY SVC                 NL
                               Basic        127        87      77   85                 41      14      431
         GPT-OSS-120B
                             LLM-Only       127        87      76   82                 42      14      428
                               Basic        125        87      73   85                 40      14      424
         GPT-OSS-20B
                             LLM-Only       124        80      71   82                 38      14      409
                               Basic        111        71      57   69                 22      12      342
          Llama-3.1-8B
                             LLM-Only       98         65      45   68                 18      13      307
                               Basic        112        80      68   76                 34      12      382
          Qwen2.5-32B
                             LLM-Only       113        78      67   75                 34      13      380
                               Basic        104        74      62   73                 28      11      352
          Qwen2.5-7B
                             LLM-Only       101        69      52   71                 26      9       328
Table 1. VerIbmc results across 520 benchmark problems (499 effective). Column headers: C2I = Code2Inv,
L4I-SVC = LaM4Inv-SVCOMP24, L4I-SY = LaM4Inv-SyGuS19, SVC = SV-COMP (full), NL = Non-Linear.
Total = sum of all five benchmark columns plus the IR column (problems solvable only under unbounded-
integer semantics). The phase-level ablation in Table 7 (Appendix) reports only standard-semantics solves; the
difference equals the IR column. Basic results are the best of three independent runs per model (see Table 5)




   Experimental protocol. Each problem is run with a 600 s wall-clock timeout. Outcomes are clas-
sified as success, timeout, failure, or unknown. We further distinguish normal successes from
integer-relaxed (IR) successes: an IR success means ESBMC verifies the property only when integer
widths are modelled as unbounded rather than fixed-width machine integers. The Total column
and all headline solve rates include IR solves. The IR variation across configurations is small (at most
14 out of 499 problems) and does not alter any qualitative ranking in Sections 4.2–4.2. The SOTA
comparison (Section 4.2) includes IR solves to match the unbounded-integer semantics assumed by
all competing tools (see Section 5). When we initially ran VerIbmc, our best performing strategy
was Basic with the LLM GPT-OSS-120B. Since LLM responses are subject to non-determinism,
we ran this strategy three times and report the best-performing run (see Table 5), following the
established pass@k evaluation protocol used in LLM-based code-generation benchmarks [19]. The
variance across the three runs was small (see Table 5), confirming that best and average would
yield equivalent qualitative rankings.

4.2   Results
RQ1: Can symbolic methods combined with locally deployed open-weight models effectively synthesise
loop invariants? We examine overall solve rates across all (model, strategy) pairs, isolating the
contribution of each pipeline phase, and characterising convergence behaviour. The results of the
standard (non-ToT) strategies are shown in Table 1. The Basic strategy is the best-performing for
every model, achieving 1,931 solved instances across 2,600 model–problem pairs (74.3%). For the
strongest model, GPT-OSS-120B, Basic solves 431/499 (86.4%) and outperforms LLM-Only (428/499).
The GPT-OSS-20B model solves 424 problems, only 7 problems fewer than the stronger model. In
contrast, the other models are significantly weaker with Qwen2.5-32B solving 382 problems. Across
all models, the Basic pipeline matches or outperforms the LLM-Only pipeline, indicating that the
addition of symbolic reasoning is advantageous. This effect is most pronounced when using Llama-
3.1-8b and Qwen2.5-7B, indicating that symbolic reasoning can mitigate weaker-model performance.
Across benchmark families, performance varies considerably: C2I is solved to near-completion
under Basic for all five models, whereas L4I-SY and NL are more discriminating. The strongest

                                                                 , Vol. 1, No. 1, Article . Publication date: June 2026.
14                                                                          Pirzada, Parsert, Wang, Korovin, Cordeiro


                                            Shared benchmarks                          SV-COMP
               Tool                                                 Subtotal‡                               Total†
                                      C2I    L4I-SVC L4I-SY NL                   Comp. (43) Full (154)
        ESBMC-Kind                     71       14      13      4     102            5         43             145
               2ls                     85       27      21      4     137           14         57             194
        CPA-Checker                    97       55      46      8     206           19         76             282
           Code2inv                   110       47      53    N/A     210           11         –∗              –∗
          Clause2Inv                  132       98      82     44     356           30         –∗              –∗
           LaM4Inv                    133       95      81     29     338           30         –∗              –∗
       LORIS (GPT-4.1)                131       94      81     45     351           39         –∗              –∗
   VerIbmc (best single cell)         133       94      78     41     346           36         85             431
 VerIbmc* (4 strats × 5 models)       133       94      79     42     348           36         89             437
Table 2. Comparison with state-of-the-art tools. C2I = Code2Inv, L4I-SVC = LaM4Inv-SVCOMP24, L4I-SY =
LaM4Inv-SyGuS19, NL = Non-Linear. Subtotal‡ sums the four shared suites. Total† = Subtotal + Full (154);
the Comp. (43) column is a subset of Full (154) and is therefore excluded from the sum. Tools whose frontend
cannot run the full SV-COMP set have no Full (154) figure and hence no Total (∗ ). ∗ frontend-limited; see
Table 6. Comp. (43) entries for ESBMC-Kind, 2ls, CPA-Checker, and Code2Inv are from our own runs on the
comparable subset (same 600 s timeout). LORIS uses GPT-4.1; VerIbmc uses local models. VerIbmc = best
single (model, strategy) cell; VerIbmc* = union across all configurations.



model (GPT-OSS-120B) shows its largest relative advantage on the non-linear clause2inv_NL suite,
where generating polynomial invariants is beyond the reach of weaker models. In conclusion, the
experiments indicate that VerIbmc can be used for effective invariant synthesis. Furthermore, the
choice of LLM has a significant impact on the results, and the use of symbolic invariants has a
positive impact, especially on weaker models.
RQ2: Does this neuro-symbolic method advance the state of the art in loop invariant synthesis? To
answer this question, we compare VerIbmc against three classes of tools, summarised in Table 2.
Class I (traditional symbolic): CPA-Checker, 2ls, and ESBMC-Kind. Class II (neural): Code2Inv [72],
which learns loop invariants via graph neural networks. Class III (LLM-augmented): Clause2Inv,
LaM4Inv, and LORIS. All Class I and II tools were run directly on our hardware across all benchmarks,
enabling a direct and fair comparison. VerIbmc substantially outperforms every tool in these two
classes: the best single configuration (GPT-OSS-120B, 431/499; 86.4%) and the overall union across
the four single-LLM strategies (All LLMs, 437/499, 87.6%) is significantly more than the state-of-
the-art verifiers, e.g., CPA-Checker’s 282 solved problems, with Code2Inv at 210, 2ls at 194, and
ESBMC-Kind at 145. On the SV-COMP benchmarks VerIbmc solves 85 and 89 problems in the IR
configuration while CPA-Checker solves 76 problems, 2ls 57 and ESBMC-Kind 43.
   Class I and II tools, as well VerIbmc require no external API subscriptions and no transmission
of source code to external servers. In contrast, the Class III LLM-augmented tools rely on external
paid APIs (e.g. OpenAI or Anthropic) that cannot be fully replicated in our setup, requiring a more
nuanced comparison. We therefore report their published figures for the four shared benchmark
suites (C2I, L4I-SVC, L4I-SY, NL). Furthermore, their provided implementations are subject to input-
format constraints: Clause2Inv and LaM4Inv use a clang-fe frontend that encodes only single-loop
scalar integer programs, and LORIS’s front-end enforces the same restriction; comparison on the
SV-COMP problem set is therefore restricted to the 43-program subset that their respective parsers
can handle. Additionally, on the shared benchmark suites, VerIbmc (346–348 solved, union across
the four single-LLM strategies) outperforms LaM4Inv (338), and is competitive with – though
slightly below – Clause2Inv (356) and LORIS (351). Note that these Clause2Inv and LORIS both
require state of the art expensive frontier models run on external servers. On the comparable
SV-COMP subset, LORIS (GPT-4.1) solves 39/43, VerIbmc solves 36/43 using local models, and

, Vol. 1, No. 1, Article . Publication date: June 2026.
Neuro-Symbolic Software Verification: Hyper-charging Local Language Models with Symbolic Reasoning at Scale          15


                                                           Benchmarks
       LLM Model              Strategy                                                           IR     Total
                                               C2I    L4I-SVC L4I-SY SVC                  NL
                            Basic-ToT          123       87      75   83                  39      14      421
      GPT-OSS-120B
                          LLM-Only-ToT         124       87      77   83                  38      14      423
                            Basic-ToT          121       84      73   80                  39      14      411
       GPT-OSS-20B
                          LLM-Only-ToT         122       86      72   82                  38      14      414
                            Basic-ToT           83       62      49   65                  17      9       285
       Llama-3.1-8B
                          LLM-Only-ToT         81        56      41   65                  21      11      275
                            Basic-ToT           98       74      64   72                  28      13      349
       Qwen2.5-32B
                          LLM-Only-ToT         100       69      64   72                  30      12      347
                            Basic-ToT           99       76      58   74                  24      10      341
        Qwen2.5-7B
                          LLM-Only-ToT         90        72      56   74                  24      11      327
Table 3. Results for the ToT strategies. Column abbreviations and IR convention as in Table 1. Shaded cells
indicate where ToT outperforms its non-ToT counterpart in aggregate; ToT additionally reaches exclusive
problems not reflected in these totals (Section 4.2).




Clause2Inv and LaM4Inv each solve 30/43; pure ESBMC solves only 5/43 without invariants, CPA-
Checker verifies 19/43, 2ls verifies 14/43 and Code2inv verifies 11/43, confirming the gain is due
to invariant synthesis. VerIbmc with GPT-OSS-20B (and even an 8B Llama at 33/43) stays at or
above Clause2Inv’s and LaM4Inv’s 30, despite their use of GPT-4o-mini.
    A breakdown of the different problem sets shows that the best single configuration solves all 133
C2I problems (matching LaM4Inv’s perfect score), 94/99 on L4I-SVC (within one of LaM4Inv’s 95,
four below Clause2Inv’s 98), 78/84 on L4I-SY (three below LaM4Inv’s 81, four below Clause2Inv’s
82), and 41/50 on NL (three below Clause2Inv’s 44, four below LORIS’s 45). Note that the Class I and
II tools are clearly beaten by a large margin in every problem set. Non-linear arithmetic is a known
weak point of SMT solvers, the best Class I tool solves only 8 problems here, so LLM-generated
invariants serve as guided lemma selection, enabling ESBMC to discharge polynomial goals it
would otherwise fail on.
    In summary, VerIbmc substantially outperforms all Class I and II tools, is competitive with
the best LLM-augmented tools on the benchmarks they can express, and uniquely scales to the
full range of C programs. Notably, in our experiments Class I and II tools were run on the same
hardware as VerIbmc and without any calls to external servers.

RQ3: What effect does Tree-of-Thoughts prompting have on the efficacy of neuro-symbolic invariant
synthesis? The results of ToT based pipelines are shown in Table 3. Comparing Table 1 with Table 3
reveals that the performance of ToT hinges on the strength of the model. For strong models the
difference to the CoT prompting is negligible while for the weaker models the performance is
lacking. Table 4 summarises the CoT–ToT comparison. ToT’s key contribution is not aggregate
throughput but diversity: its scouting stage explores multiple candidate invariants and reaches 49
(model, problem) pairs that the direct CoT approach cannot, two of which are globally unique across
all models and strategies. The aggregate cost of this diversity depends on model capability: for the
two strongest models the deltas are small (−5 to −13), with GPT-OSS-20B under LLM-Only-ToT the
sole case of a net gain (+5). Weaker models pay a larger price, most severely Llama-3.1-8B (−57
under Basic-ToT). In total, 119 pairs move in the opposite direction under ToT; the failure-mode
decomposition in Section 4.3 explains why.

                                                                 , Vol. 1, No. 1, Article . Publication date: June 2026.
16                                                                          Pirzada, Parsert, Wang, Korovin, Cordeiro


                                            Basic                           LLM-Only              ToT-
     Model
                    CoT                         ToT         𝚫       CoT          ToT           𝚫 unique
     GPT-OSS-120B 431 (5.2 h)                421 (5.9 h)   −10    428 (4.7 h) 423 (5.6 h)     −5   1
     GPT-OSS-20B 424 (5.5 h)                 411 (6.2 h)   −13    409 (6.5 h) 414 (6.2 h)     +5   6
     Llama-3.1-8B 342 (8.6 h)                285 (8.8 h)   −57   307 (10.0 h) 275 (9.3 h)     −32  10
     Qwen2.5-32B  382 (6.3 h)                349 (7.0 h)   −33    380 (6.2 h) 347 (6.8 h)     −33  8
     Qwen2.5-7B   352 (6.6 h)                341 (7.6 h)   −11    328 (5.7 h) 327 (8.0 h)     −1   24
Table 4. CoT versus ToT solve counts and total wall-clock time per model and strategy. Numbers in parentheses
are total wall-clock time across all 11 benchmark families. Δ = ToT − CoT (solve count). ToT-unique: problems
where the model fails under both Basic and LLM-Only but succeeds under at least one ToT strategy.



   Table 4 also shows that ToT incurs a wall-clock overhead over its base counterpart, driven by
the scouting stage; this ranges from negligible (Llama-3.1-8B Basic-ToT, +2%) to 1.40× for LLM-
Only-ToT on Qwen2.5-7B (5.7 h → 8.0 h). Within the non-ToT strategies, Basic and LLM-Only run
in comparable time, confirming that the extra work Basic performs—Phase 1 symbolic enumeration
together with the atom-level filtering and recombination of each LLM proposal—is negligible
relative to the LLM loop, so its accuracy gains in RQ1 come effectively for free.
RQ4: How do the different pipeline phases contribute to the overall solve rate? To see which phases
had what impact on the solve rate we look at the solved problems and look at the which phase of
the pipeline in Figure 1 on page 6 led to a successful verification. Overall, the counts are as follows:
    • 111 (22.2%) are solved by Phase 0 alone under standard semantics, plus 3 (0.6%) under
      unbounded-integer (IR) semantics – 114 Phase 0 solves in total;
    • 75 (15.0%) are solved by symbolic stage in Phase 1;
    • 248 (49.7%) need at least one LLM-generated invariant phase;
    • 62 (12.4%) remain unsolved by every (model, strategy) combination within the 600 s budget.
Figure 2a visualises the breakdown per benchmark family. Phase 0 is strongest in C2I ; SVC shows
the highest proportion of never-solved problems, making it the hardest family. Phase 1 symbolic
candidates contribute a small but fully deterministic share across most suites. The 323 problems
requiring the LLM/symbolic stage are therefore the right denominator for evaluating the LLM’s
contribution—though even within this subset, 75 are resolved by Phase 1’s symbolic candidates
alone, without any LLM call.
   On this 323-problem subset, performance diverges sharply by model: GPT-OSS-120B/Basic solves
314 (97.2%), Llama-3.1-8B/Basic solves 229 (70.9%), and Llama-3.1-8B/Basic-ToT solves only 172
(53.3%).
   Phase 1 symbolic candidates alone resolve exactly 75 problems that Phase 0 cannot decide—a fully
deterministic contribution independent of which LLM is paired with the system. Table 7 (Appendix)
shows the per-phase breakdown for each model. Llama-3.1-8B gains a net +36 problems (75 Phase 1
solves, offset by −39 LLM solves on the harder residual); Qwen2.5-7B gains +22; GPT-OSS-20B
gains +15; GPT-OSS-120B gains zero, as the strong model independently derives the same provable
atoms.

4.3 Discussion
   Convergence behaviour. Figure 2b shows the distribution of refinement rounds required to solve
each problem. Convergence is heavily front-loaded across all models and strategies: 65.1% of LLM-
solved problems are solved on the first iteration, 85.1% within five, and 88% within ten; the maximum
is 171 iterations. Unsurprisingly, stronger models (GPT-OSS-120B, GPT-OSS-20B) converge faster,

, Vol. 1, No. 1, Article . Publication date: June 2026.
Neuro-Symbolic Software Verification: Hyper-charging Local Language Models with Symbolic Reasoning at Scale          17




(a) Per-benchmark breakdown of solved contribution (b) Cumulative Distribution Function (CDF) of refine-
by phase (as a percentage of each family’s total   ment rounds on successful Phase 2 outcomes, broken
problems).                                         down by model. Each curve aggregates all four main
                                                   strategies for that model.

                     Fig. 2. Solve rates by refinement iterations and benchmark family.


with their curves reaching the plateau at lower iteration counts, while weaker models (Llama-3.1-8B,
Qwen2.5-7B) show a longer tail. This front-loading suggests that most problems are either directly
solvable by the model or require only modest refinement; the long tail (rounds > 20) accounts for
fewer than 10% of successful solves and represents structurally harder instances where the LLM
must progressively accumulate provable atoms before closure.
  For GPT-OSS-120B, Basic (431/499) marginally outperforms LLM-Only (428/499) by 3 problems.
Phase 1 symbolic candidates primarily displace LLM solves rather than add new ones for the strong
model: it independently derives the same provable atoms through direct generation that Phase 1
enumerates symbolically, explaining why the scores are nearly identical. Only a small number of
problems genuinely require Phase 1 to succeed where LLM generation alone does not converge
within budget.
   Unique Solves. The four strategies clusters cover between 314 and 318 of the 323 non-trivial
problems, and at most 1 problem is unique to any single strategy. Figure 3 renders the per-cell
pairwise Jaccard similarity on the non-trivial subset across the 20 (model, strategy) cells; median
pairwise Jaccard is ≈ 0.73, confirming strong agreement. Each entry (𝑖, 𝑗) reports |𝑆𝑖 ∩ 𝑆 𝑗 |/|𝑆𝑖 ∪ 𝑆 𝑗 |;
a value of 1.0 denotes identical coverage and 0.0 denotes no overlap. Pairs sharing the same model
(different strategy) exhibit the highest Jaccard values, while pairs sharing only the same strategy
but different models span a wider range. This shows that the solvable frontier is shaped primarily
by model identity: switching from LLM-Only to Basic within the same model yields only marginal
changes in which problems are solved, even when the aggregate count shifts noticeably.
  Failure mode decomposition. We disaggregate failures into timeouts and UNKNOWN outcomes
(UNKNOWN means that either ESBMC could neither prove safety nor find a counterexample or
another system error occurred either in or outside of ESBMC). For the two strong models, UNKNOWN
rates are low (≤ 2%) and change negligibly under ToT (GPT-OSS-120B: 1.8% under both Basic
and Basic-ToT). Qwen2.5-7B’s UNKNOWN rate under LLM-Only is 26.0%, but falls to 6.9% under
LLM-Only-ToT (−19 pp); the solve-count nonetheless decreases (319 → 316) as timeouts rise by
+19.5 pp. Llama-3.1-8B shows the reverse: its UNKNOWN rate rises from 4.5% under Basic to 14.5%
under Basic-ToT (+10 pp).

                                                                 , Vol. 1, No. 1, Article . Publication date: June 2026.
18                                                                        Pirzada, Parsert, Wang, Korovin, Cordeiro




Fig. 3. Pairwise Jaccard similarity of solved-problem sets across the 20 (model, strategy) cells of our evaluation
(5 models × 4 strategies), restricted to the 323 non-trivial problems. Median pairwise Jaccard = 0.73. Strong off-
diagonal agreement (≥ 0.7 in nearly every cell) indicates that the solvable frontier is robust to model/strategy
choice once the Phase 0 baseline is held constant.


   These two weak models thus face qualitatively different bottlenecks. For Qwen2.5-7B, ToT’s
structured output template improves format compliance but exhausts the iteration budget; for
Llama-3.1-8B, the structured template itself exceeds the model’s reliable output capability. In both
cases the binding constraint is not reasoning ability but the interplay between output format and
iteration budget.
   Model capability vs. strategy choice. To understand the relative contributions of model identity
and strategy selection to solve outcomes, we classify each discriminating problem (one where some
(model, strategy) cell succeeds and another fails) by which axis drives most of the variance. Across
the four pre-existing benchmark suites, model-driven variance dominates strategy-driven variance
by a factor of 3–7×: on L4I-SY, 31 of 54 discriminating problems are classified model-dominated,
while only 4 are strategy-dominated (19 mixed); on C2I, the ratio is 39:10 (26 mixed). L4I-SVC is the
closest to balanced (20:4 with 32 mixed), making it the most informative benchmark for isolating

, Vol. 1, No. 1, Article . Publication date: June 2026.
Neuro-Symbolic Software Verification: Hyper-charging Local Language Models with Symbolic Reasoning at Scale          19


strategy effects. The gap between the strongest model (GPT-OSS-120B) and the weakest (Llama-
3.1-8B) on their respective best strategies is 89 problems (431 vs. 342 under Basic), substantially
larger than the within-model strategy span of 67 problems (Basic at 342 vs. LLM-Only-ToT at 275
for Llama-3.1-8B). The within-model maximum gain attributable to strategy alone is +35 (Basic vs.
LLM-Only on Llama-3.1-8B). These numbers confirm that model capability is the primary driver of
accuracy: Phase 1 symbolic feedback provides useful but modest within-model gains, and investing
in a stronger model yields a larger expected accuracy gain than any strategy-level refinement.
   Compute overhead. Table 4 shows that the wall-clock cost of ToT is model-dependent, ranging
from negligible to 1.40×. For the two strongest models the overhead is small (under 15%) and
the diversity gain is correspondingly modest (1 and 6 ToT-unique pairs); the extra compute is
unlikely to be worthwhile in practice unless the specific unsolved problems are known to matter.
For Qwen2.5-7B, the picture is reversed: ToT-unique pairs number 24 and the overhead reaches
1.40× under LLM-Only-ToT, yet the aggregate solve count does not improve, consistent with the
failure-mode analysis above showing that timeouts absorb the scouting budget. In all cases, the
cost of switching from LLM-Only to Basic is negligible: Phase 1 symbolic enumeration together
with the atom-level filtering and recombination of each LLM proposal completes in time that is
small relative to the LLM refinement loop, so the accuracy gains reported in RQ1 come effectively
for free.

5   Threats to Validity
Like the state-of-the-art tools we compare against, our pipeline reasons about programs under a
real-arithmetic (LRA/LIA-over-Z) semantics rather than over C’s fixed-width machine integers.
This makes the head-to-head comparison fair – every system in the evaluation is solving the same
abstract problem on the same benchmarks. For this comparison, we therefore operate under the
same abstract semantics as the competing tools, which means overflow bugs are not checked in
this evaluation. This is a deliberate choice for comparability, not a fundamental limitation: ESBMC
natively supports bit-precise reasoning via SMT bitvector theory, so VerIbmc can detect arithmetic
overflows when configured to do so – a capability that the cloud-API tools we compare against do
not offer.
   Model bias. GPT-OSS-120B and GPT-OSS-20B belong to the same model family [2] and share ar-
chitectural design choices and training provenance; their results are therefore not fully independent.
The scaling trend we observe – larger model yields higher solve rate – may partly reflect shared
inductive biases rather than a universal property of open-weight models in general. All five models
were served through Ollama at default generation parameters; we did not tune temperature or
sampling settings per model or per benchmark family. Decoding configurations that are suboptimal
for a given model may understate its performance, and the relative rankings we report could shift
under different hyperparameter settings. Additionally, all five benchmark families used in this
evaluation are publicly available – C2I, L4I-SVC, L4I-SY, and NL are distributed alongside their
respective tools, and SVC problems are drawn from the public SV-COMP archive. Since all five
models are trained on internet-scale corpora, it is likely that some programs, their invariants, or
the papers introducing them have appeared in pre-training data. This could artificially inflate
per-problem LLM performance on those families, and we did not attempt to detect or quantify
contamination.
   Non-determinism and experimental variance. LLM generation is stochastic. Each (model, strategy,
problem) triple in the full four-strategy grid (Tables 1–3) was evaluated in a single run; this applies
to LLM-Only, Basic, LLM-Only-ToT, and Basic-ToT alike. To quantify sampling sensitivity for the

                                                                 , Vol. 1, No. 1, Article . Publication date: June 2026.
20                                                                           Pirzada, Parsert, Wang, Korovin, Cordeiro


                        Model                             Run 0   Run 1   Run 2   Mean       𝜎
                        GPT-OSS-120B                        428     431     428    429.0    1.7
                        GPT-OSS-20B                         424     423     424    423.7    0.6
                        Qwen2.5-32B-Instruct                382     380     381    381.0    1.0
                        Qwen2.5-7B-Instruct                 352     347     351    350.0    2.6
                        Llama-3.1-8B                        342     332     334    336.0    5.3
                        Grand Total                        1928    1913    1918   1919.7    7.6
Table 5. Solve counts for the Basic strategy across three independent runs (2,600 model–problem pairs per
run; 520 problems × 5 models). 𝜎 is the sample standard deviation across the three runs.



best-performing strategy, we replicated the Basic strategy specifically: in addition to the original
run, we conducted two further independent full runs of Basic across all five models and all eleven
benchmark families (2,600 model–problem pairs per run), giving three runs of Basic in total. We
report the best result across the three runs for each model as the main Basic result in Table 1; for
GPT-OSS-120B this corresponds to Run 1 (431 problems), while all other models achieve their best
in Run 0. Table 5 summarises all three runs. Grand totals across the three runs are 1,928, 1,913, and
1,918; per-model standard deviations range from 𝜎 = 0.6 (GPT-OSS-20B) to 𝜎 = 5.3 (Llama-3.1-8B,
the weakest model and therefore most sensitive to sampling fluctuation). The between-run range
for the strongest model, GPT-OSS-120B, is only 3 problems (428–431), well within the 89-problem
gap between GPT-OSS-120B and GPT-OSS-20B reported in Table 1. All three grand totals fall within
a 15-problem window (1,913–1,928) against a total of 2,600, confirming that the rank ordering
of models and the strategy-level findings are robust to LLM non-determinism. Problems at the
boundary of model capability may still produce different outcomes under different random seeds;
differences of fewer than ten problems between strategies should be treated as indicative rather
than definitive. The 600 s wall-clock timeout introduces a further source of variance: host machine
load during a run can shift which problems are decided within budget.
   Benchmark bias. Three of the four shared benchmark families were curated by or introduced
alongside the tools we compare against: ibmc_code2inv derives from Code2Inv [72], L4I-SVC and
L4I-SY were introduced alongside LaM4Inv [80], and clause2inv_NL was introduced alongside
Clause2Inv [15]. Benchmarks curated by competing tools may implicitly reflect their represen-
tational strengths, potentially giving those tools a distributional advantage on their respective
sets. Furthermore, these benchmarks were, in part, syntactically restricted to conform to the input
format of the tested tools. To mitigate this bias, we also considered a wider range of benchmarks
provided by the SV-COMP that are collected from various sources. Furthermore, these benchmarks
do not fall under the same syntactic restrictions.
   Benchmark representativeness. The majority of benchmark problems in our evaluation are single-
loop programs over scalar integer variables. Notably, the SV-COMP subset includes programs
with multiple loops, arrays, and pointer arithmetic (see Section 4.2). This design choice isolates
arithmetic invariant reasoning but limits generalisability to industrial software. Programs with
heap-allocated data structures, pointer aliasing, concurrency, floating-point arithmetic, or complex
multi-procedure control flow lie outside the current scope. Nevertheless, the SV-COMP subset
substantially relaxes the single-loop and scalar integer restrictions. As a result VerIbmc handles
arrays, nested loops, and function calls. This is enabled through the use of ESBMC’s advanced C
frontend that supports a wide range of C features. In particular, of the 154 SV-COMP programs,

, Vol. 1, No. 1, Article . Publication date: June 2026.
Neuro-Symbolic Software Verification: Hyper-charging Local Language Models with Symbolic Reasoning at Scale          21


36 contain multiple or nested loops that VerIbmc can support but that are inexpressible for some
competing tools (see Table 6). As a result, the SV-COMP problems that fall outside the expressible
fragment of some SOTA tools have no full comparison.
  Cross-tool comparison on SV-COMP. For the SV-COMP set, Clause2Inv and LaM4Inv were run
by us using their required external paid APIs, because their published evaluations did not cover this
benchmark. These runs were conducted at different times, used the API model versions available at
the time of our evaluation, and may have executed on different backend infrastructure from the
runs reported in their respective papers. LLM API outputs are non-deterministic and API model
versions change silently over time; these cross-tool figures should therefore be treated as indicative.
The comparable-subset comparison (Table 2) uses the same 43 programs under identical evaluation
conditions for all three invariant-driven methods and is the most controlled tier of the SV-COMP
comparison.
   ToT scoring function. The ToT strategy-scoring function (Eq. 5) assigns fixed weights of 0.6, −0.3,
and 0.1 to provable, disprovable, and unknown atoms respectively. These weights were chosen
heuristically and were not subjected to ablation. The top-2 strategy selection in Stage 1, and the
re-ranking every six rounds in Stage 2, both depend directly on this scoring function. A different
weighting could change which two strategies are promoted to the refinement loop for a given
program, potentially altering which problems ToT solves or fails on and shifting the diversity–
accuracy trade-off boundary reported in Section 4.2. The reported ToT results should therefore be
understood as specific to this particular scoring configuration rather than as a property of the ToT
architecture in general.

6   Related Work
   Traditional Methods. Abstract interpretation [25] computes sound over-approximations over
abstract domains (intervals, octagons, polyhedra [26]), but precision is domain-limited. Constraint-
based synthesis [23, 67] encodes initiation and consecution as constraints over a fixed template, re-
quiring the user to anticipate the invariant’s form. Houdini [35] computes the largest simultaneously-
inductive subset of a candidate set but cannot synthesise new predicates. IC3/PDR [11, 33] incre-
mentally strengthens reachability over-approximations using counterexamples to inductiveness; it
is complete for finite-state systems and extends to infinite-state via SMT [46].
   Neuro-Symbolic Methods. Neuro-Symbolic approaches pair a neural proposal component (GNN
or LLM) with a symbolic back-end that checks soundness and returns structured feedback (coun-
terexamples, unsat cores). This generate-and-check architecture is sound by construction: any
accepted invariant is logically guaranteed, regardless of how it was generated. Earlier RL-based
work (Code2Inv [72]) required thousands of solver queries during training and suffered from sparse
binary rewards; LLM-based approaches leverage pretrained knowledge to reduce oracle queries
substantially. All five evaluated systems fall within this paradigm, differing in neural architecture,
feedback format, and use of fine-tuning.
   Code2Inv [72] encodes programs as graphs (data-flow, control-flow, syntactic containment),
applies a GNN to produce invariant candidates, and updates via policy-gradient RL using Z3 out-
comes as rewards. It solved 106/133 benchmark programs, outperforming template-based methods,
and established the de facto evaluation suite used by all subsequent work. The tool is limited to
linear arithmetic invariants over scalar integers. IC3Syn [16] combines an IC3/PDR frame-based
controller with LLM-generated blocking clauses to synthesise inductive invariants for distributed
protocols specified in TLA+; unlike VerIbmc, it targets protocol-level transition systems rather
than C loop programs and relies on cloud-hosted frontier models via external APIs.

                                                                 , Vol. 1, No. 1, Article . Publication date: June 2026.
22                                                                Pirzada, Parsert, Wang, Korovin, Cordeiro


   LEMUR [81] is the first framework to provide a formal calculus for integrating LLMs into
automated program verification. Both GPT-3.5-turbo and GPT-4 are supported as oracle backends,
with GPT-4 demonstrating superior performance; the program and any solver counterexample are
included in the prompt, and on failure, a repair step applies backtracking to refine candidates before
re-checking. LEMUR achieved state-of-the-art results on Code2Inv and non-linear benchmarks
with no task-specific fine-tuning.
   ESBMC-ibmc [63] integrates LLM-generated invariants into the ESBMC BMC pipeline by modi-
fying the control flow graph (CFG) rather than unrolling loops. A portion of the CFG representing a
loop is replaced by a node asserting LLM-generated invariants, which are validated by Vampire [57],
a first-order theorem prover, to ensure soundness. This transforms programs into loop-free variants
that ESBMC can then verify. VerIbmc eliminates this external dependency: all invariant checking
is discharged directly through ESBMC’s loop-invariant-checking mode with 𝑘-induction, requiring
no additional theorem prover.
   LaM4Inv [80] integrates LLMs with BMC in a closed-loop query-filter-reassemble strategy. The
LLM generates candidate invariants, which are filtered and fed into the ESBMC BMC pipeline;
counterexamples from failed checks are returned to the LLM to guide refinement. LaM4Inv out-
performs both traditional and prior LLM-based methods; a detailed quantitative comparison with
VerIbmc is given in Section 4.
   Clause2Inv [15] refines the standard guess-and-check framework into a generate-combine-
check framework. An LLM-based clause generator produces atomic clauses (simple expressions
without logical connectives), which are stored and systematically combined by a counterexample-
driven combinator. Each candidate conjunction is verified by an SMT solver; failures trigger further
combination guided by counterexamples. This factorised architecture addresses the observation that
existing approaches struggle with complete invariants due to the complexity of logical connectives,
yet the individual clauses of the correct invariant typically appear in earlier guesses.
   LORIS [59] identify a fundamental limitation of counterexample-based feedback: informing an
LLM that a concrete variable assignment violates its candidate invariant is a blunt signal, because
LLM errors are typically detail mistakes within an otherwise-correct reasoning strategy rather
than global misdirections. LORIS addresses this by prompting the LLM to produce a step-by-step
natural language proof of its proposed invariant, translating each proof step into a first-order logic
implication via a dedicated Formalizer LLM, and checking each implication with Z3 [28]. When a
specific implication fails, the model receives targeted feedback identifying exactly which reasoning
step is invalid – for example, that the claim 𝑗 > 𝑚 ⇒ 𝑗 = 𝑚 + 1 in step 3 does not hold – rather
than a raw counterexample. LORIS achieves strong accuracy on overlapping benchmarks, with
its advantage over clause-based approaches growing with model capability; see Section 4 for a
detailed comparison with VerIbmc.
   VerIbmc and LORIS address complementary deployment scenarios. LORIS requires transmitting
source code to an external API and degrades substantially with weaker models. VerIbmc targets
environments where this is infeasible: all inference runs on locally-deployed open-weight models,
and Phase 1 symbolic augmentation provides a deterministic floor that particularly benefits weaker
models. Phase 1 also resolves a non-trivial fraction of benchmarks without any LLM call, a cate-
gory LORIS cannot address (see Section 4). Li et al. also demonstrate that local-error feedback is
complementary to LaM4Inv-style symbolic conjunct accumulation [80], suggesting that integrating
LORIS-style reasoning feedback into VerIbmc’s Phase 2 prompt is a natural direction for future
work (Section 7).

  LLM-Based Specification Synthesis. The generate-and-check paradigm extends naturally from
loop invariants to broader verification artifacts. AutoSpec [78] augments LLM-based specification

, Vol. 1, No. 1, Article . Publication date: June 2026.
Neuro-Symbolic Software Verification: Hyper-charging Local Language Models with Symbolic Reasoning at Scale          23


synthesis with static analysis and program verification, iteratively refining Frama-C annotations
until a formal checker accepts them. Granberry et al. [42] address a complementary challenge
– what to specify – using symbolic methods to identify under-specified clauses and focus LLM
generation on the predicates that are actually missing. King et al. [53] extend LLM-based generation
to weakest preconditions and quantified array invariants, two classes that fall outside the scalar
linear-arithmetic scope of most loop-invariant tools. The paradigm also transfers to compiler
settings: Magalhaes et al. [29] apply a guess, measure, and edit feedback loop to guide LLM-based
tensor code optimisation, demonstrating that structured neural–symbolic interaction is domain-
agnostic.

7   Conclusion
Overall, we presented VerIbmc, a neuro-symbolic pipeline that pairs locally-deployable open-weight
language models with the ESBMC verification backend for automated loop invariant synthesis in C
programs. The pipeline combines a deterministic symbolic phase with an iterative LLM refinement
loop driven by structured verifier feedback, offering two prompting strategies: CoT and ToT. In
our experimental evaluation, we show that cheap, locally hosted, open weight LLMs can be used
effectively in a neuro-symbolic pipeline for loop invariant synthesis. VerIbmc outperforms all other
tools that run on local infrastructure and is competitive with LLM-based tools that rely on expensive
external APIs and transmit source code to third-party services. Alongside this, our evaluation across
five open-weight models, four inference strategies, and five benchmark families confirms that
the Basic pipeline, which augments LLM refinement with symbolic invariant candidates, is the
strongest strategy across all models. The symbolic phase resolves a significant fraction of problems
without any LLM call and yields consistent gains for weaker models. Also, our ToT-inspired pipelines
reveal a diversity–accuracy trade-off: ToT’s multi-branch exploration reaches problem–model pairs
inaccessible to direct CoT and yields a net gain for stronger models. In aggregate, however, non-
ToT strategies dominate across most comparisons, as the iteration budget consumed by scouting
outweighs the diversity benefit for weaker models, respectively. VerIbmc matches the best prior
LLM-augmented tools on shared benchmark suites and separates from them in generality – handling
the full SV-COMP loop set they cannot express – while operating entirely on local infrastructure.
A small fraction of problems remain unsolved across all pipelines and models, representing the
hard frontier for future work.
   Several directions remain open for the future. First, for ToT, constrained decoding [5, 79] would
reduce malformed outputs and free iteration budget for convergence, while ablating the scor-
ing weights (Eq. 5) could shift the diversity–accuracy trade-off boundary across model tiers. On
soundness, a post-processing pass that re-discharges accepted invariants under ESBMC’s bit-vector
back-end would recover bit-precise semantics without burdening the LLM; extending Phase 1
candidate enumeration to array or separation-logic predicates [12, 65] would open the pipeline to
heap-manipulating programs. Finally, an energy and cost comparison against cloud-API baselines
would empirically ground the efficiency claims that motivate local deployment, and a difficulty-
aware early-stopping policy could make the iteration budget adaptive rather than fixed.

Acknowledgments
We thank Dr. Giles Reger for his advice, code assistance and guidance. We also thank Rafael Menezes
for his support to create a setup to run the experiments. Julian Parsert was funded by the European
Research Council (ERC) project LASD (Grant ID: 101089343).
   The authors of this research disclose that generative AI was used in the development of the
tooling and in the execution of the methodological evaluation. After using these tool(s)/service(s),

                                                                 , Vol. 1, No. 1, Article . Publication date: June 2026.
24                                                            Pirzada, Parsert, Wang, Korovin, Cordeiro


the author(s) reviewed and edited the content as needed and take(s) full responsibility for the
publication’s content.




, Vol. 1, No. 1, Article . Publication date: June 2026.
Neuro-Symbolic Software Verification: Hyper-charging Local Language Models with Symbolic Reasoning at Scale                 25


References
 [1] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida,
     Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. 2023. Gpt-4 technical report. arXiv preprint arXiv:2303.08774
     (2023).
 [2] Sandhini Agarwal, Lama Ahmad, Jason Ai, Sam Altman, Andy Applebaum, Edwin Arbus, Rahul K Arora, Yu Bai,
     Bowen Baker, Haiming Bao, et al. 2025. gpt-oss-120b & gpt-oss-20b model card. arXiv preprint arXiv:2508.10925 (2025).
 [3] AI Anthropic. 2024. Claude 3 model card. Technical documentation, Anthropic (2024).
 [4] Jinze Bai, Shuai Bai, Yunfei Chu, Zeyu Cui, Kai Dang, Xiaodong Deng, Yang Fan, Wenbin Ge, Yu Han, Fei Huang, et al.
     2023. Qwen technical report. arXiv preprint arXiv:2309.16609 (2023).
 [5] Luca Beurer-Kellner, Marc Fischer, and Martin Vechev. 2023. Prompting is programming: A query language for large
     language models. Proceedings of the ACM on Programming Languages 7, PLDI (2023), 1946–1969.
 [6] Dirk Beyer, Thomas A. Henzinger, Rupak Majumdar, and Andrey Rybalchenko. 2007. Invariant Synthesis for Combined
     Theories. In Verification, Model Checking, and Abstract Interpretation, 8th International Conference, VMCAI 2007, Nice,
     France, January 14-16, 2007, Proceedings (Lecture Notes in Computer Science), Byron Cook and Andreas Podelski (Eds.).
     Springer, 378–394. doi:10.1007/978-3-540-69738-1_27
 [7] Dirk Beyer and M Erkan Keremoglu. 2011. CPAchecker: A tool for configurable software verification. In International
     conference on computer aided verification. Springer, 184–190.
 [8] Dirk Beyer and Jan Strejcek. 2026. Evaluating Software Verifiers for C, Java, and SV-LIB - (Report on SV-COMP 2026).
     In Tools and Algorithms for the Construction and Analysis of Systems - 32nd International Conference, TACAS 2026, Held
     as Part of the International Joint Conferences on Theory and Practice of Software, ETAPS 2026, Turin, Italy, April 11-16,
     2026, Proceedings, Part II (Lecture Notes in Computer Science), Sebastian Junges and Guy Katz (Eds.). Springer, 461–502.
     doi:10.1007/978-3-032-22749-2_23
 [9] Armin Biere. 2021. Bounded Model Checking. In Handbook of Satisfiability - Second Edition, Armin Biere, Marijn
     Heule, Hans van Maaren, and Toby Walsh (Eds.). IOS Press, 739–764. doi:10.3233/FAIA201002
[10] Armin Biere, Alessandro Cimatti, Edmund Clarke, and Yunshan Zhu. 1999. Symbolic model checking without BDDs.
     In International conference on tools and algorithms for the construction and analysis of systems. Springer, 193–207.
[11] Aaron R Bradley. 2011. SAT-based model checking without unrolling. In International Workshop on Verification, Model
     Checking, and Abstract Interpretation. Springer, 70–87.
[12] Aaron R Bradley, Zohar Manna, and Henny B Sipma. 2006. What’s decidable about arrays?. In International Workshop
     on Verification, Model Checking, and Abstract Interpretation. Springer, 427–442.
[13] Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan,
     Pranav Shyam, Girish Sastry, Amanda Askell, et al. 2020. Language models are few-shot learners. Advances in neural
     information processing systems 33 (2020), 1877–1901.
[14] Robert Brummayer and Armin Biere. 2009. Boolector: An efficient SMT solver for bit-vectors and arrays. In International
     Conference on Tools and Algorithms for the Construction and Analysis of Systems. Springer, 174–177.
[15] Weining Cao, Guangyuan Wu, Tangzhi Xu, Yuan Yao, Hengfeng Wei, Taolue Chen, and Xiaoxing Ma. 2025. Clause2Inv:
     A Generate-Combine-Check Framework for Loop Invariant Inference. Proc. ACM Softw. Eng. 2, ISSTA (2025), 1009–1030.
     doi:10.1145/3728920
[16] Weining Cao, Guangyuan Wu, Yuan Yao, Hengfeng Wei, Taolue Chen, and Xiaoxing Ma. 2026. Synthesizing Inductive
     Invariants for Distributed Protocols via IC3 and Large Language Models. arXiv preprint arXiv:2605.24619 (2026).
[17] Saikat Chakraborty, Shuvendu K. Lahiri, Sarah Fakhoury, Akash Lal, Madanlal Musuvathi, Aseem Rastogi, Aditya
     Senthilnathan, Rahul Sharma, and Nikhil Swamy. 2023. Ranking LLM-Generated Loop Invariants for Program
     Verification. In Findings of the Association for Computational Linguistics: EMNLP 2023, Singapore, December 6-10, 2023
     (Findings of ACL), Houda Bouamor, Juan Pino, and Kalika Bali (Eds.). Association for Computational Linguistics,
     9164–9175. doi:10.18653/V1/2023.FINDINGS-EMNLP.614
[18] Robert N Charette. 2009. This car runs on code. IEEE spectrum 46, 3 (2009), 3.
[19] Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde De Oliveira Pinto, Jared Kaplan, Harri Edwards,
     Yuri Burda, Nicholas Joseph, Greg Brockman, et al. 2021. Evaluating large language models trained on code. arXiv
     preprint arXiv:2107.03374 (2021).
[20] Andrew A. Chien, Liuzixuan Lin, Hai Nguyen, Varsha Rao, Tristan Sharma, and Rajini Wijayawardana. 2023. Reducing
     the Carbon Impact of Generative AI Inference (today and in 2035). In Proceedings of the 2nd Workshop on Sustainable
     Computer Systems, HotCarbon 2023, Boston, MA, USA, 9 July 2023, George Porter, Tom Anderson, Andrew A. Chien,
     Tamar Eilam, Colleen Josephson, and Jonggyu Park (Eds.). ACM, 11:1–11:7. doi:10.1145/3604930.3605705
[21] Alessandro Cimatti, Alberto Griggio, Bastiaan Joost Schaafsma, and Roberto Sebastiani. 2013. The mathsat5 smt solver.
     In International Conference on Tools and Algorithms for the Construction and Analysis of Systems. Springer, 93–107.
[22] Edmund M. Clarke, Thomas A. Henzinger, Helmut Veith, and Roderick Bloem (Eds.). 2018. Handbook of Model Checking.
     Springer. doi:10.1007/978-3-319-10575-8


                                                                        , Vol. 1, No. 1, Article . Publication date: June 2026.
26                                                                               Pirzada, Parsert, Wang, Korovin, Cordeiro


[23] Michael Colón, Sriram Sankaranarayanan, and Henny Sipma. 2003. Linear Invariant Generation Using Non-linear
     Constraint Solving. In Computer Aided Verification, 15th International Conference, CAV 2003, Boulder, CO, USA, July
     8-12, 2003, Proceedings (Lecture Notes in Computer Science), Warren A. Hunt Jr. and Fabio Somenzi (Eds.). Springer,
     420–432. doi:10.1007/978-3-540-45069-6_39
[24] Lucas Cordeiro, Bernd Fischer, and Joao Marques-Silva. 2012. SMT-based bounded model checking for embedded
     ANSI-C software. IEEE Transactions on Software Engineering 38, 4 (2012), 957–974.
[25] Patrick Cousot and Radhia Cousot. 1977. Abstract interpretation: a unified lattice model for static analysis of programs
     by construction or approximation of fixpoints. In Proceedings of the 4th ACM SIGACT-SIGPLAN symposium on Principles
     of programming languages. 238–252.
[26] Patrick Cousot and Nicolas Halbwachs. 1978. Automatic Discovery of Linear Restraints Among Variables of a
     Program. In Conference Record of the Fifth Annual ACM Symposium on Principles of Programming Languages, Tucson,
     Arizona, USA, January 1978, Alfred V. Aho, Stephen N. Zilles, and Thomas G. Szymanski (Eds.). ACM Press, 84–96.
     doi:10.1145/512760.512770
[27] Badhan Chandra Das, M. Hadi Amini, and Yanzhao Wu. 2025. Security and Privacy Challenges of Large Language
     Models: A Survey. ACM Comput. Surv. 57, 6 (2025), 152:1–152:39. doi:10.1145/3712001
[28] Leonardo De Moura and Nikolaj Bjørner. 2008. Z3: An efficient SMT solver. In International conference on Tools and
     Algorithms for the Construction and Analysis of Systems. Springer, 337–340.
[29] José Wesley de Souza Magalhães, Jackson Woodruff, Jordi Armengol-Estapé, Alexander Brauckmann, Luc Jaulmes,
     Elizabeth Polgreen, and Michael F. P. O’Boyle. 2025. Guess, Measure & Edit: Using Lowering to Lift Tensor Code.
     In 34th International Conference on Parallel Architectures and Compilation Techniques, PACT 2025, Irvine, CA, USA,
     November 3-6, 2025. IEEE, 216–228. doi:10.1109/PACT65351.2025.00029
[30] Yi Ding and Tianyao Shi. 2024. Sustainable LLM Serving: Environmental Implications, Challenges, and Opportunities :
     Invited Paper. In 15th IEEE International Green and Sustainable Computing Conference, IGSC 2024, Austin, TX, USA,
     November 2-3, 2024. IEEE, 37–38. doi:10.1109/IGSC64514.2024.00016
[31] Yufeng Du, Minyang Tian, Srikanth Ronanki, Subendhu Rongali, Sravan Babu Bodapati, Aram Galstyan, Azton Wells,
     Roy Schwartz, Eliu A. Huerta, and Hao Peng. 2025. Context Length Alone Hurts LLM Performance Despite Perfect
     Retrieval. In Findings of the Association for Computational Linguistics: EMNLP 2025, Christos Christodoulopoulos,
     Tanmoy Chakraborty, Carolyn Rose, and Violet Peng (Eds.). Association for Computational Linguistics, Suzhou, China,
     23281–23298. doi:10.18653/v1/2025.findings-emnlp.1264
[32] Bruno Dutertre and Leonardo De Moura. 2006. The yices smt solver. Tool paper at http://yices. csl. sri. com/tool-paper.
     pdf 2, 2 (2006), 1–2.
[33] Niklas Eén, Alan Mishchenko, and Robert Brayton. 2011. Efficient implementation of property directed reachability. In
     2011 Formal Methods in Computer-Aided Design (FMCAD). IEEE, 125–134.
[34] ESBMC Developers. 2026. Loop Invariant Support. https://esbmc.github.io/docs/loop-invariants/ ESBMC Documenta-
     tion.
[35] Cormac Flanagan and K Rustan M Leino. 2001. Houdini, an annotation assistant for ESC/Java. In International
     symposium of formal methods Europe. Springer, 500–517.
[36] Robert W Floyd. 1993. Assigning meanings to programs. In Program Verification: Fundamental Issues in Computer
     Science. Springer, 65–81.
[37] Graham Fraser. 2024. CrowdStrike: What was the impact of the global IT outage. BBC News (24 Sept. 2024). https:
     //www.bbc.co.uk/news/articles/cr54m92ermgo Accessed: 2026-06-14.
[38] Carlo A. Furia, Bertrand Meyer, and Sergey Velder. 2014. Loop invariants: Analysis, classification, and examples. ACM
     Comput. Surv. 46, 3 (2014), 34:1–34:51. doi:10.1145/2506375
[39] Mikhail R Gadelha, Felipe Monteiro, Lucas Cordeiro, and Denis Nicole. 2019. ESBMC v6. 0: Verifying C Programs Using
     k-Induction and Invariant Inference: (Competition Contribution). In International Conference on Tools and Algorithms
     for the Construction and Analysis of Systems. Springer, 209–213.
[40] Pranav Garg, Daniel Neider, P. Madhusudan, and Dan Roth. 2016. Learning invariants using decision trees and
     implication counterexamples. In Proceedings of the 43rd Annual ACM SIGPLAN-SIGACT Symposium on Principles of
     Programming Languages, POPL 2016, St. Petersburg, FL, USA, January 20 - 22, 2016, Rastislav Bodík and Rupak Majumdar
     (Eds.). ACM, 499–512. doi:10.1145/2837614.2837664
[41] Mirco Giacobbe, Daniel Kroening, and Julian Parsert. 2022. Neural termination analysis. In Proceedings of the 30th ACM
     Joint European Software Engineering Conference and Symposium on the Foundations of Software Engineering, ESEC/FSE
     2022, Singapore, Singapore, November 14-18, 2022, Abhik Roychoudhury, Cristian Cadar, and Miryung Kim (Eds.). ACM,
     633–645. doi:10.1145/3540250.3549120
[42] George Granberry, Wolfgang Ahrendt, and Moa Johansson. 2024. Specify What? Enhancing Neural Specification
     Synthesis by Symbolic Methods. In Integrated Formal Methods - 19th International Conference, IFM 2024, Manchester,
     UK, November 13-15, 2024, Proceedings (Lecture Notes in Computer Science), Nikolai Kosmatov and Laura Kovács (Eds.).


, Vol. 1, No. 1, Article . Publication date: June 2026.
Neuro-Symbolic Software Verification: Hyper-charging Local Language Models with Symbolic Reasoning at Scale                 27


     Springer, 307–325. doi:10.1007/978-3-031-76554-4_19
[43] Aaron Grattafiori, Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad Al-Dahle, Aiesha
     Letman, Akhil Mathur, Alan Schelten, Alex Vaughan, et al. 2024. The llama 3 herd of models. arXiv preprint
     arXiv:2407.21783 (2024).
[44] Daya Guo, Qihao Zhu, Dejian Yang, Zhenda Xie, Kai Dong, Wentao Zhang, Guanting Chen, Xiao Bi, Yifan Wu, YK Li,
     et al. 2024. DeepSeek-Coder: when the large language model meets programming–the rise of code intelligence. arXiv
     preprint arXiv:2401.14196 (2024).
[45] Charles Antony Richard Hoare. 1969. An axiomatic basis for computer programming. Commun. ACM 12, 10 (1969),
     576–580.
[46] Kryštof Hoder and Nikolaj Bjørner. 2012. Generalized property directed reachability. In International Conference on
     Theory and Applications of Satisfiability Testing. Springer, 157–171.
[47] Jordan Hoffmann, Sebastian Borgeaud, Arthur Mensch, Elena Buchatskaya, Trevor Cai, Eliza Rutherford, DDL Casas,
     Lisa Anne Hendricks, Johannes Welbl, Aidan Clark, et al. 2022. Training compute-optimal large language models.
     arXiv preprint arXiv:2203.15556 10 (2022).
[48] Xinyi Hou, Yanjie Zhao, Yue Liu, Zhou Yang, Kailong Wang, Li Li, Xiapu Luo, David Lo, John Grundy, and Haoyu
     Wang. 2024. Large Language Models for Software Engineering: A Systematic Literature Review. ACM Trans. Softw.
     Eng. Methodol. 33, 8 (2024), 220:1–220:79. doi:10.1145/3695988
[49] Andreas Humenberger, Maximilian Jaroschek, and Laura Kovács. 2018. Invariant Generation for Multi-Path Loops with
     Polynomial Assignments. In Verification, Model Checking, and Abstract Interpretation - 19th International Conference,
     VMCAI 2018, Los Angeles, CA, USA, January 7-9, 2018, Proceedings (Lecture Notes in Computer Science), Isil Dillig and
     Jens Palsberg (Eds.). Springer, 226–246. doi:10.1007/978-3-319-73721-8_11
[50] Carlos E. Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, and Karthik R. Narasimhan. 2024.
     SWE-bench: Can Language Models Resolve Real-world Github Issues?. In The Twelfth International Conference on
     Learning Representations, ICLR 2024, Vienna, Austria, May 7-11, 2024. OpenReview.net. https://openreview.net/forum?
     id=VTF8yNQM66
[51] Adharsh Kamath, Aditya Senthilnathan, Saikat Chakraborty, Pantazis Deligiannis, Shuvendu K. Lahiri, Akash Lal,
     Aseem Rastogi, Subhajit Roy, and Rahul Sharma. 2023. Finding Inductive Loop Invariants using Large Language
     Models. CoRR abs/2311.07948 (2023). arXiv:2311.07948 doi:10.48550/ARXIV.2311.07948
[52] Jared Kaplan, Sam McCandlish, Tom Henighan, Tom B Brown, Benjamin Chess, Rewon Child, Scott Gray, Alec Radford,
     Jeffrey Wu, and Dario Amodei. 2020. Scaling laws for neural language models. arXiv preprint arXiv:2001.08361 (2020).
[53] Daragh King, Vasileios Koutavas, and Laura Kovács. 2025. Llm-Based Generation of Weakest Preconditions and
     Precise Array Invariants. In 13th IEEE/ACM International Conference on Formal Methods in Software Engineering,
     FormaliSE@ICSE 2025, Ottawa, ON, Canada, April 27-28, 2025. IEEE, 1–5. doi:10.1109/FORMALISE66629.2025.00016
[54] Andrei Kirilenko, Albert S Kyle, Mehrdad Samadi, and Tugkan Tuzun. 2017. The flash crash: High-frequency trading
     in an electronic market. The Journal of Finance 72, 3 (2017), 967–998.
[55] Takeshi Kojima, Shixiang Shane Gu, Machel Reid, Yutaka Matsuo, and Yusuke Iwasawa. 2022. Large language models
     are zero-shot reasoners. Advances in neural information processing systems 35 (2022), 22199–22213.
[56] Philip Koopman and Michael Wagner. 2017. Autonomous vehicle safety: An interdisciplinary challenge. IEEE Intelligent
     Transportation Systems Magazine 9, 1 (2017), 90–96.
[57] Laura Kovács and Andrei Voronkov. 2013. First-order theorem proving and Vampire. In International Conference on
     Computer Aided Verification. Springer, 1–35.
[58] Nancy G Leveson and Clark S Turner. 1993. An investigation of the Therac-25 accidents. Computer 26, 7 (1993), 18–41.
[59] Tianchi Li, Zhenyu Yan, Junhao Liu, Peng Di, and Xin Zhang. 2026. Guiding LLM-based Loop Invariant Synthesis via
     Feedback on Local Reasoning Errors. ACM Trans. Program. Lang. Syst. (April 2026). doi:10.1145/3806652 Just Accepted.
[60] Nelson F Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, and Percy Liang. 2024.
     Lost in the middle: How language models use long contexts. Transactions of the association for computational linguistics
     12 (2024), 157–173.
[61] Niloofar Mireshghallah, Hyunwoo Kim, Xuhui Zhou, Yulia Tsvetkov, Maarten Sap, Reza Shokri, and Yejin Choi. 2024.
     Can LLMs Keep a Secret? Testing Privacy Implications of Language Models via Contextual Integrity Theory. In The
     Twelfth International Conference on Learning Representations, ICLR 2024, Vienna, Austria, May 7-11, 2024. OpenReview.net.
     https://openreview.net/forum?id=gmg7t8b4s0
[62] Aina Niemetz and Mathias Preiner. 2023. Bitwuzla. In International Conference on Computer Aided Verification. Springer,
     3–17.
[63] Muhammad A. A. Pirzada, Giles Reger, Ahmed Bhayat, and Lucas C. Cordeiro. 2024. LLM-Generated Invariants for
     Bounded Model Checking Without Loop Unrolling. In Proceedings of the 39th IEEE/ACM International Conference on
     Automated Software Engineering (Sacramento, CA, USA) (ASE ’24). Association for Computing Machinery, New York,
     NY, USA, 1395–1407. doi:10.1145/3691620.3695512


                                                                        , Vol. 1, No. 1, Article . Publication date: June 2026.
28                                                                                Pirzada, Parsert, Wang, Korovin, Cordeiro


[64] Qwen Team. 2025. Qwen2.5 Technical Report. Technical Report. Alibaba Group. arXiv:2412.15115 https://arxiv.org/
     abs/2412.15115
[65] John C Reynolds. 2002. Separation logic: A logic for shared mutable data structures. In Proceedings 17th annual IEEE
     symposium on logic in computer science. IEEE, 55–74.
[66] Henry Gordon Rice. 1953. Classes of recursively enumerable sets and their decision problems. Transactions of the
     American Mathematical society 74, 2 (1953), 358–366.
[67] Sriram Sankaranarayanan, Henny B Sipma, and Zohar Manna. 2004. Non-linear loop invariant generation using
     Gröbner bases. In Proceedings of the 31st ACM SIGPLAN-SIGACT symposium on Principles of programming languages.
     318–329.
[68] Peter Schrammel and Daniel Kroening. 2016. 2LS for Program Analysis: (Competition Contribution). In International
     Conference on Tools and Algorithms for the Construction and Analysis of Systems. Springer, 905–907.
[69] Rahul Sharma and Alex Aiken. 2016. From invariant checking to invariant inference using randomized search. Formal
     Methods Syst. Des. 48, 3 (2016), 235–256. doi:10.1007/S10703-016-0248-5
[70] Rahul Sharma, Saurabh Gupta, Bharath Hariharan, Alex Aiken, Percy Liang, and Aditya V. Nori. 2013. A Data Driven
     Approach for Algebraic Loop Invariants. In Programming Languages and Systems - 22nd European Symposium on
     Programming, ESOP 2013, Held as Part of the European Joint Conferences on Theory and Practice of Software, ETAPS
     2013, Rome, Italy, March 16-24, 2013. Proceedings (Lecture Notes in Computer Science), Matthias Felleisen and Philippa
     Gardner (Eds.). Springer, 574–592. doi:10.1007/978-3-642-37036-6_31
[71] Mary Sheeran, Satnam Singh, and Gunnar Stålmarck. 2000. Checking safety properties using induction and a SAT-solver.
     In International conference on formal methods in computer-aided design. Springer, 127–144.
[72] Xujie Si, Hanjun Dai, Mukund Raghothaman, Mayur Naik, and Le Song. 2018. Learning loop invariants for program
     verification. Advances in Neural Information Processing Systems 31 (2018).
[73] Rafael Sá Menezes, Mohannad Aldughaim, Bruno Farias, Xianzhiyu Li, Edoardo Manino, Fedor Shmarov, Kunjian
     Song, Franz Brauße, Mikhail R. Gadelha, Norbert Tihanyi, Konstantin Korovin, and Lucas C. Cordeiro. [n. d.]. ESBMC:
     7.4: Harnessing the Power of Intervals. https://github.com/esbmc/esbmc
[74] Gemini Team, Rohan Anil, Sebastian Borgeaud, Jean-Baptiste Alayrac, Jiahui Yu, Radu Soricut, Johan Schalkwyk,
     Andrew M Dai, Anja Hauth, Katie Millican, et al. 2023. Gemini: a family of highly capable multimodal models. arXiv
     preprint arXiv:2312.11805 (2023).
[75] Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timothée Lacroix, Baptiste
     Rozière, Naman Goyal, Eric Hambro, Faisal Azhar, Aurélien Rodriguez, Armand Joulin, Edouard Grave, and Guillaume
     Lample. 2023. LLaMA: Open and Efficient Foundation Language Models. CoRR abs/2302.13971 (2023). arXiv:2302.13971
     doi:10.48550/ARXIV.2302.13971
[76] Alexander Wan, Kevin Klyman, Sayash Kapoor, Nestor Maslej, Shayne Longpre, Betty Xiong, Percy Liang, and Rishi
     Bommasani. 2025. The 2025 Foundation Model Transparency Index. CoRR abs/2512.10169 (2025). arXiv:2512.10169
     doi:10.48550/ARXIV.2512.10169
[77] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou, et al. 2022.
     Chain-of-thought prompting elicits reasoning in large language models. Advances in neural information processing
     systems 35 (2022), 24824–24837.
[78] Cheng Wen, Jialun Cao, Jie Su, Zhiwu Xu, Shengchao Qin, Mengda He, Haokun Li, Shing-Chi Cheung, and Cong Tian.
     2024. Enchanting Program Specification Synthesis by Large Language Models Using Static Analysis and Program
     Verification. In Computer Aided Verification - 36th International Conference, CAV 2024, Montreal, QC, Canada, July
     24-27, 2024, Proceedings, Part II (Lecture Notes in Computer Science, Vol. 14682), Arie Gurfinkel and Vijay Ganesh (Eds.).
     Springer, 302–328. doi:10.1007/978-3-031-65630-9_16
[79] Brandon T Willard and Rémi Louf. 2023. Efficient guided generation for large language models. arXiv preprint
     arXiv:2307.09702 (2023).
[80] Guangyuan Wu, Weining Cao, Yuan Yao, Hengfeng Wei, Taolue Chen, and Xiaoxing Ma. 2024. LLM Meets Bounded
     Model Checking: Neuro-symbolic Loop Invariant Inference. In Proceedings of the 39th IEEE/ACM International Conference
     on Automated Software Engineering, ASE 2024, Sacramento, CA, USA, October 27 - November 1, 2024, Vladimir Filkov,
     Baishakhi Ray, and Minghui Zhou (Eds.). ACM, 406–417. doi:10.1145/3691620.3695014
[81] Haoze Wu, Clark W. Barrett, and Nina Narodytska. 2024. Lemur: Integrating Large Language Models in Automated
     Program Verification. In The Twelfth International Conference on Learning Representations, ICLR 2024, Vienna, Austria,
     May 7-11, 2024. OpenReview.net. https://openreview.net/forum?id=Q3YaCghZNt
[82] Rongchen Xu, Fei He, and Bow-Yaw Wang. 2020. Interval counterexamples for loop invariant learning. In ESEC/FSE ’20:
     28th ACM Joint European Software Engineering Conference and Symposium on the Foundations of Software Engineering,
     Virtual Event, USA, November 8-13, 2020, Prem Devanbu, Myra B. Cohen, and Thomas Zimmermann (Eds.). ACM,
     111–122. doi:10.1145/3368089.3409752



, Vol. 1, No. 1, Article . Publication date: June 2026.
Neuro-Symbolic Software Verification: Hyper-charging Local Language Models with Symbolic Reasoning at Scale                29


[83] John Yang, Carlos E. Jimenez, Alexander Wettig, Kilian Lieret, Shunyu Yao, Karthik Narasimhan, and Ofir Press.
     2024. SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering. In Advances in Neural
     Information Processing Systems 38: Annual Conference on Neural Information Processing Systems 2024, NeurIPS 2024,
     Vancouver, BC, Canada, December 10 - 15, 2024, Amir Globersons, Lester Mackey, Danielle Belgrave, Angela Fan,
     Ulrich Paquet, Jakub M. Tomczak, and Cheng Zhang (Eds.). http://papers.nips.cc/paper_files/paper/2024/hash/
     5a7c947568c1b1328ccc5230172e1e7c-Abstract-Conference.html
[84] Jianan Yao, Gabriel Ryan, Justin Wong, Suman Jana, and Ronghui Gu. 2020. Learning nonlinear loop invariants with
     gated continuous logic networks. In Proceedings of the 41st ACM SIGPLAN International Conference on Programming
     Language Design and Implementation, PLDI 2020, London, UK, June 15-20, 2020, Alastair F. Donaldson and Emina Torlak
     (Eds.). ACM, 106–120. doi:10.1145/3385412.3385986
[85] Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Tom Griffiths, Yuan Cao, and Karthik Narasimhan. 2023. Tree of
     thoughts: Deliberate problem solving with large language models. Advances in neural information processing systems
     36 (2023), 11809–11822.
[86] Shiwen Yu, Ting Wang, and Ji Wang. 2023. Loop Invariant Inference through SMT Solving Enhanced Reinforcement
     Learning. In Proceedings of the 32nd ACM SIGSOFT International Symposium on Software Testing and Analysis, ISSTA
     2023, Seattle, WA, USA, July 17-21, 2023, René Just and Gordon Fraser (Eds.). ACM, 175–187. doi:10.1145/3597926.3598047

A    SV-COMP Frontend Limitations
Table 6 details why 71% of the SV-COMP loop set (110 of 154 programs) cannot be expressed by
the clang-fe frontend used by Clause2Inv, LaM4Inv, and LORIS. Each cause is an architectural
boundary of the frontend or single-loop scalar program graph model, not a tuning gap.

 Reason cannot be expressed                 Count       Inherent cause
 Array                                         41       graph models only scalar integers
 Nested/multi-loop                             36       approach targets single loops
 Pointer                                        5       pointers not modeled
 Frontend crash                                 8       clang-fe hang/segfault
 In-loop assert                                 8       empty post-condition; Horn template cannot encode
 Other VC bug                                  11       malformed/ill-typed VC; function calls, infinite loops
 Bitwise                                        1       not expressible in linear integer arithmetic
 Total limitation                             110       (71% of 154)
Table 6. Breakdown of the 110 SV-COMP loop programs inexpressible by the clang-fe frontend (used by
Clause2Inv, LaM4Inv, and LORIS). Each cause is an architectural boundary, not a tuning gap.




                                                                       , Vol. 1, No. 1, Article . Publication date: June 2026.
30                                                                   Pirzada, Parsert, Wang, Korovin, Cordeiro


B    Additions to Discussion of Experimental Results
  Phase-level ablation. Table 7 shows the per-phase breakdown of solve counts for each model
under the LLM-Only and Basic strategies.

          Model                  Strategy Phase 0 Phase 1 Phase 2                       Total
                                 LLM-Only     111       -     303                         414
          GPT-OSS-120B
                                 Basic        111      75     228              414 (ΔPh1 = 0)
                                 LLM-Only     111       -     284                         395
          GPT-OSS-20B
                                 Basic        111      75     224            410 (ΔPh1 = +15)
                                 LLM-Only     111       -     256                         367
          Qwen2.5-32B
                                 Basic        111      75     184             370 (ΔPh1 = +3)
                                 LLM-Only     111       -     208                         319
          Qwen2.5-7B
                                 Basic        111      75     155            341 (ΔPh1 = +22)
                                 LLM-Only     111       -     183                         294
          Llama-3.1-8B
                                 Basic        111      75     144            330 (ΔPh1 = +36)
Table 7. Phase-level ablation of VerIbmc (single-LLM strategies). Phase 0: problems solved by ESBMC
without any invariant (standard semantics, model-invariant). Phase 1: problems solved by symbolic candidate
conjunction alone (no LLM call, model-invariant at 75 problems). Phase 2: problems requiring at least one
LLM-generated invariant. ΔPh1 = net gain of adding Phase 1 (Basic vs. LLM-Only). Dual-LLM data is in the
remainder of this appendix.



  Figure 2b reports number of iterations required. The long tail past 20 refinement rounds is
universally rare (< 7% of LLM-solved instances), which provides an empirical basis for capping
max_iter at a modest value (e.g., ≤ 20). Without ESBMC Phase 1 feedback (LLM-Only), weaker
models continue to gain solves well past cap = 20, confirming that the symbolic augmentation in
Basic narrows the long tail even without a second LLM.

C    Coverage




, Vol. 1, No. 1, Article . Publication date: June 2026.
Neuro-Symbolic Software Verification: Hyper-charging Local Language Models with Symbolic Reasoning at Scale          31


         Model                Strategy             N      ≤0      ≤1      ≤5       ≤ 10       ≤ 20 p90
                              Basic               236    83.1    91.1    98.7      99.6      100.0   1
                              Basic-ToT           228    69.7    74.6    92.5      99.6      100.0   5
         GPT-OSS-120B
                              LLM-Only            268    72.0    91.8    99.3     100.0      100.0   1
                              LLM-Only-ToT        310    78.1    83.5    94.5     100.0      100.0   5
                              Basic               231    77.5    89.2    97.4      99.6      100.0   1
                              Basic-ToT           218    77.1    78.9    94.5      99.5      100.0   5
         GPT-OSS-20B
                              LLM-Only            295    72.2    88.5   100.0     100.0      100.0   1
                              LLM-Only-ToT        301    81.4    82.7    94.0     100.0      100.0   5
                              Basic               150    26.0    36.0    50.0      62.0       73.3  36
                              Basic-ToT            93    34.4    37.6    66.7      89.2       97.8  11
         Llama-3.1-8B
                              LLM-Only            194    24.7    35.1    50.5      60.8       69.6  38
                              LLM-Only-ToT        162    37.7    43.2    72.8      91.4       96.3  10
                              Basic               189    57.7    67.7    76.2      80.4       86.8  33
                              Basic-ToT           156    57.7    62.8    84.6      91.0       94.9   9
         Qwen2.5-32B
                              LLM-Only            266    49.6    59.0    70.3      74.8       81.2  40
                              LLM-Only-ToT        233    62.2    65.2    84.5      96.6       98.3   9
                              Basic               159    35.8    43.4    54.1      59.7       78.0  17
                              Basic-ToT           148    41.9    45.3    64.9      77.7       83.8  33
         Qwen2.5-7B
                              LLM-Only            214    40.2    47.7    54.7      58.9       72.4  27
                              LLM-Only-ToT        213    50.7    52.6    70.9      85.0       90.6  17
Table 8. Per-cell convergence thresholds. N: number of successfully-solved problems where at least one
LLM call was made; excludes Phase 0-only and Phase 1-only solves, but includes integer-relaxed solves. ≤ 𝑘:
cumulative percentage of those 𝑁 problems solved within 𝑘 LLM refinement rounds (𝑘=0 means first LLM
call succeeded). p90: 90th-percentile round count. Convergence data for the dual-LLM strategies is reported
in Section D.



                Strategy                      Solved Coverage % Unique vs others
                Basic                            317        97.8               1
                Basic-ToT                        315        97.2               1
                LLM-Only                         314        96.9               0
                LLM-Only-ToT                     318        98.1               1
                Union (any strategy)             324      100.0                –
Table 9. Strategy-as-solver coverage of the 323 non-trivial problems reachable by at least one of the four
inference strategies (Phase 0-safe and dual-LLM-exclusive problems excluded). Each strategy = union of
solves across all five models. “Unique vs others” counts problems that no other single-LLM strategy (in its
own union) reaches.



D    Dual-LLM Correction with a Fixed Strong Model
  Strategy description. The Combined strategy follows the same Phase 0–Phase 1 structure as the
Basic strategy but replaces the single LLM in Phase 2 with a dual LLM sequence. In each iteration,
LLM1 receives the standard prompt and generates invariant candidates; its raw textual output
together with the current P, D, U lists is forwarded as context to LLM2 . LLM2 can therefore observe
both what LLM1 proposed and what ESBMC formally verified, enabling semantic-level correction
rather than blind regeneration. Both outputs are independently parsed, verified, and atomically

                                                                 , Vol. 1, No. 1, Article . Publication date: June 2026.
32                                                                    Pirzada, Parsert, Wang, Korovin, Cordeiro


                             LLM1                         Basic   Combined   Δ
                             GPT-OSS-120B (= LLM2 )         428        427 −1
                             GPT-OSS-20B                    424        425 +1
                             Llama-3.1-8B                   342        389 +47
                             Qwen2.5-32B                    382        421 +39
                             Qwen2.5-7B                     352        416 +64
Table 10. Supplementary dual-LLM experiment: Basic vs. Combined solve counts (out of 499 effective prob-
lems). LLM2 = GPT-OSS-120B is fixed for all runs. Δ = combined − basic.



decomposed; a successful outcome may arise from LLM1 alone, LLM2 alone, or the recombination
of atoms from both. The Combined-ToT variant is not a simple extension of Combined; it replaces
the sequential per-iteration correction chain with the Tree-of-Thoughts multi-branch scouting
structure (§3.7). In each ToT stage, both LLM1 and LLM2 are invoked across multiple exploratory
branches, and their accumulated atoms jointly populate the shared stores P, D, U; a top-2 selection
then prunes the branch set before the next stage. The result is that LLM2 no longer acts as a targeted
corrector of LLM1 ’s output within a single iteration—instead, both models contribute to cross-
branch diversity, at the cost of a larger iteration budget. In short, the two strategies differ not
merely in the presence of ToT but in how the two LLMs interact: LLM2 is a sequential corrector in
Combined and a joint explorer in Combined-ToT.
   Setup. Important: the Combined and Combined-ToT strategies each use two LLMs simultaneously
and are not directly comparable to the four single-LLM strategies above. The gains below scale with
the capability gap between LLM1 and GPT-OSS-120B; they should be read as a characterisation of
strong-model post-processing as an optional ceiling, not as evidence that dual-LLM refinement
is a generally effective technique. LLM2 is fixed to GPT-OSS-120B—the strongest model in our
evaluation pool—regardless of which model serves as LLM1 . We report these results separately as a
supplement.
  Aggregate gains. Table 10 shows the gains of Combined over Basic for each LLM1 . When LLM1 =
LLM2 = GPT-OSS-120B, the correction adds zero benefit (Δ = −1); as LLM1 weakens, the gain grows
monotonically to +64 for Qwen2.5-7B. This pattern indicates that the gain tracks the capability gap
between LLM1 and GPT-OSS-120B rather than reflecting any benefit of ESBMC feedback structure,
which explains why the two experimental conditions cannot be compared on equal terms.
   Unique solves. Despite the aggregate gain being largely attributable to LLM2 ’s capability, Com-
bined’s solution trajectory—which begins from LLM1 ’s partial invariant proposals—reaches prob-
lems that no other strategy for the same model can solve. Under Definition A (per-model unique:
solved by Combined for model 𝑀 but by no other strategy for 𝑀), the counts are 27 for Llama-3.1-8B,
16 for Qwen2.5-7B, and 7 for Qwen2.5-32B (50 model–problem pairs in total; Figure 4).
   Under the stricter Definition B—where no other (model, strategy) pair can solve the problem—only
2 problems are globally unique to Combined, both solved by Qwen2.5-7B: lam4inv_sygus19/186.c
and sv-comp_loops-crafted-1/mono-crafted_3.c. These two problems account for the differ-
ence between the union of 437 (four strategies) and 440 (all six configurations).
   Convergence. Under Combined, first-try success rates are uniformly high (≥ 77% across all
models), compared to 24–83% under Basic. This faster convergence is explained by LLM2 (GPT-OSS-
120B) frequently reformatting or correcting LLM1 ’s output on the first pass, reducing the number
of ESBMC re-queries required. Consequently, the low UNKNOWN (parse failure) rate observed for

, Vol. 1, No. 1, Article . Publication date: June 2026.
Neuro-Symbolic Software Verification: Hyper-charging Local Language Models with Symbolic Reasoning at Scale          33




Fig. 4. Per-model unique solves (Definition A): problems solved by Combined for model 𝑀 but not by any
other strategy for the same model 𝑀. Total = 50 (model, problem) pairs.




Fig. 5. Supplementary dual-LLM experiment: Basic (single LLM) vs. Combined (+GPT-OSS-120B as LLM2 ).
Numbers show the Δ (combined − basic). Not directly comparable to the four single-LLM strategies.


weaker models under Combined reflects GPT-OSS-120B’s output quality rather than any structural
benefit of ESBMC feedback.

E   Similar-Size Paired LLM Experiments
   Motivation. The experiment in Section D holds LLM2 fixed to GPT-OSS-120B, the strongest model
in our pool, so the observed gains track the capability gap between LLM1 and GPT-OSS-120B rather
than a structural benefit of dual-LLM correction. To isolate the structural question, we re-run the
Combined and Combined-ToT strategies with four LLM pairs whose two members are drawn from

                                                                 , Vol. 1, No. 1, Article . Publication date: June 2026.
34                                                                           Pirzada, Parsert, Wang, Korovin, Cordeiro


Table 11. Similar-size paired LLM results across all 11 benchmarks (520 problems). C = Combined, CT =
Combined-ToT. IR-mode solves are noted separately in the Total row (not added to per-benchmark columns).
Contrast with Table 10, where LLM2 = GPT-OSS-120B throughout. Pair labels: P1 = Qwen-7B→LLaMA-8B;
P2 = LLaMA-8B→Qwen-7B; P3 = Qwen-32B→GPT-20B; P4 = GPT-20B→Qwen-32B.


                                                Small (≈7–8B)                   Medium (≈20–32B)
                                                P1                P2               P3                    P4
  Benchmark (total)                           C       CT         C     CT       C        CT           C        CT
  loop-acceleration (24)                     17           14    15     15       20         15        19         17
  loop-crafted (8)                            2            2     2      2        2          2         2          2
  loop-invariants (9)                         6            3     6      4        6          6         6          6
  loop-new (11)                               2            2     2      2        2          2         2          2
  loop-simple (6)                             5            5     5      5        5          5         5          5
  loops (50)                                 25           23    23     24       26         25        25         25
  loops-crafted-1 (46)                       15           16    16     13       23         20        24         19
  C2I (133)                                  91           84    84     87     133        126        132        121
  L4I SVC (99)                               78           71    67     59      93         85         93         87
  L4I SY (84)                                57           44    53     35      78         76         76         77
  NL (50)                                    22           15    19     17      38         33         39         38
  Total / 520                             320        279       292    263     426       395        423       399
    of which IR                          (+10)       (+9)      (+9)   (+9)   (+14)     (+13)      (+14)     (+11)
  Solve %                                 61.5       53.7      56.2   50.6    81.9      76.0       81.3      76.7

the same capability tier: two small-model pairs (≈7–8B parameters) and two medium-model pairs
(≈20–32B parameters). LLM2 is not GPT-OSS-120B in any of these runs; the same 520-problem
pool and 600 s timeout are used throughout.
   Important. Combined and Combined-ToT use architecturally different pipelines (see
§D, Strategy distinction) and are not directly comparable to each other or to the four single-LLM
strategies. Results are reported to characterise dual-LLM behaviour in the equal-size regime, not as
a controlled ablation.
   Findings. Three patterns emerge from Table 11. (i) Model size dominates. Medium pairs solve
81–82% of problems versus 56–62% for small pairs—a gap of ≈130 problems—mirroring the main-
paper conclusion that model capability is the primary accuracy driver even in the equal-size regime.
(ii) LLM1/LLM2 order sensitivity is weak. Swapping the two models changes the aggregate by at
most 28 problems for small pairs (P1 Combined: 320 vs. P2 Combined: 292) and at most 3 problems
for medium pairs, indicating that the correction gain depends on the shared capability tier rather
than on which model sees the problem first. (iii) Combined-ToT consistently underperforms
Combined across all four pairs (by 32–54 problems for small pairs, 24–31 for medium pairs),
consistent with the budget-cost analysis in Section D: when neither LLM is large enough to absorb
the iteration overhead of multi-branch scouting, ToT’s diversity benefit does not materialise. Notably,

, Vol. 1, No. 1, Article . Publication date: June 2026.
Neuro-Symbolic Software Verification: Hyper-charging Local Language Models with Symbolic Reasoning at Scale          35


Pair 3 (Qwen2.5-32B + GPT-OSS-20B) achieves 133/133 (100%) on ibmc_code2inv under Combined,
matching the ceiling attained by GPT-OSS-120B alone in the main experiment.




                                                                 , Vol. 1, No. 1, Article . Publication date: June 2026.
