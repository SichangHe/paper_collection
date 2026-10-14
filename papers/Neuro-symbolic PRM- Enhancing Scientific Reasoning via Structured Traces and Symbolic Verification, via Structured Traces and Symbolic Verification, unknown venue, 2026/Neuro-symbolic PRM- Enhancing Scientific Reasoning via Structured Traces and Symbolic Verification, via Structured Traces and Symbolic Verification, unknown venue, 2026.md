                                         Neuro-symbolic PRM: Enhancing Scientific Reasoning
                                         via Structured Traces and Symbolic Verification

                                             Yuxin Zi1,2 , Cong Xu2 , Suparna Bhattacharya2 , Martin Foltin2 , Amit Sheth1,3
                                             1 AI Institute of South Carolina 2 HPE Labs 3 Indian AI Research Organisation
                                             {yuxin.zi,cong.xu,suparna.bhattacharya,martin.foltin}@hpe.com, amit@iairo.ai



                                                                                   Abstract
arXiv:2608.26329v1 [cs.CL] 26 Aug 2026




                                                   While tool-augmented Large Language Models have significantly improved
                                                   multi-step reasoning in quantitative STEM tasks, a critical residual failure
                                                   mode remains: intermediate reasoning steps that are syntactically well-
                                                   formed, mathematically executable, and unit-consistent, yet contextually
                                                   ungrounded. Current approaches either rely on formal verifiers that cannot
                                                   assess semantic intent, or burden Process Reward Models (PRMs) with the
                                                   dual task of checking both arithmetic and logic. In this paper, we propose
                                                   a neuro-symbolic framework that cleanly decouples reasoning into two
                                                   formal dimensions: Symbolic Validity (V) and Semantic Groundedness (G).
                                                   We guarantee V by construction using a deterministic symbolic verifier
                                                   acting as a hard filter. To assess G, we train a PRM conditionally on the
                                                   verifier-accepted manifold. To train this PRM efficiently, we introduce
                                                   Counterfactual Symbolic Perturbation (CSP), a novel data synthesis strategy
                                                   that algorithmically generates constraint-preserving hard negatives (steps
                                                   that perfectly pass the verifier but are logically flawed). At inference,
                                                   we deploy a verifier-first constrained search that guarantees execution
                                                   consistency for verifier-covered operations while relying on the PRM solely
                                                   to rank semantic grounding. By targeting the exact residual error class
                                                   of strong tool-using LLMs, our method significantly improves reasoning
                                                   reliability without the sprawling heuristics of prior frameworks.


                                         1     Introduction

                                         Large Language Models (LLMs) have demonstrated remarkable capabilities in multi-step
                                         quantitative reasoning (Cobbe et al., 2021). To overcome their inherent limitations in arith-
                                         metic and precise execution, recent advancements have heavily integrated external tools,
                                         code interpreters, and Program-of-Thought (PoT) prompting (Chen et al., 2023; Gao et al.,
                                         2023; Gou et al., 2024). By offloading computation to deterministic engines, these methods
                                         successfully eliminate a vast majority of calculation and syntax errors.
                                         However, delegating execution to a tool exposes a critical, under-addressed residual failure
                                         mode in structured quantitative STEM tasks: intermediate reasoning steps that are perfectly
                                         executable, but semantically wrong. A model might apply the correct physics formula
                                         to the wrong variables, or compute a mathematically flawless but contextually irrelevant
                                         quantity. In these cases, the step is syntactically valid, numerically executable, and even unit-
                                         consistent, yet completely ungrounded from the problem’s logical solution path. Current
                                         verification methods struggle to address this gap. Deterministic symbolic verifiers can check
                                         syntax and math, but they cannot verify semantic intent. Conversely, PRMs (Lightman et al.,
                                         2024) are typically trained to score the overall correctness of a step, forcing a single neural
                                         model to simultaneously act as a calculator, a syntax checker, and a semantic judge. This
                                         lack of decomposition leads to sample-inefficient training, where the PRM wastes capacity
                                         learning execution rules rather than deep logical grounding.
                                         In this paper, we address this executable-but-ungrounded failure mode by formally decou-
                                         pling reasoning correctness into two distinct dimensions: Symbolic Validity and Semantic
                                         Groundedness. We propose the Neuro-symbolic Process Reward Model (NS-PRM) frame-


                                                                                        1
                   (A) Training via Counterfactual Symbolic Perturbation                            (B) Inference via Symbolically Constrained Beam Search

    Policy 1: Logic Perturbation
                                                                                                                    Current Beam State Jt-1:
                        s+                                                                                       (Problem: Drop ball 5m. Find vf
                      Groud
                      Truth     Step:                                                                               Given: h=5m, g=9.8m/s2)
                                                                          OK
    Goal: Find                  Apply(NewtonSecondLaw)
    Acceleration
                                      Correct Principle      Symbolic                                                 Candidate 1:                                 Error: Unit
    Given:                                                    Verifier           Train PRM                                                       Symbolic
    F=10N,                                                                                                        Calc(Mult, args) = [h,g]        Verifier          Mismatch
    m=2kg                       Step:                                                                                  → Pred: 49J                                 m*m/s2 != J
                       s–                                                      Maximize Margin
                                Apply(KineticEnergyEq)         Valid
                      Hard                                                     Between s+ and s–
                     Negative                                 Syntax
                                      Wrong Principle                                                                                                        OK
                                     (Valid Operation)                                             Generator:         Candidate 2:               Symbolic
                                                                                                   Expand k=3    Apply(MomentumCons)              Verifier
                                                                                                                                                                  PRM Score:0.2
                                                                                                   Candidates
    Policy 2: Operand Perturbation                                                                                                                                   Logically
                                                                                                                                                                    Irrelevant
                        s+
                      Groud                                                                                                                                  OK
                      Truth     Step: Calc(sub, args) =                                                              Candidate 3:
    Goal:                                                                 OK                                                                     Symbolic
                                (Fthrust,Fdrag) → 80N                                                              Apply(EnergyCons)              Verifier
    Calculate Fnet                                                                                                                                                PRM Score:0.9
    Given:                           Correct Variables       Symbolic
                                                              Verifier           Train PRM                                                                          Logically
    Fthrust=100N,
    Fdrag=20N,                                                                                                          Beam Selection (Top-B)                      Coherent
                                Step: Calc(sub, args) =
    Fweight=50N        s –                                                     Maximize Margin
                                (Fthrust,Fweight) → 50N        Valid           Between s+ and s–
                      Hard                                                                                          Updated Beam State Jt:
                     Negative                               Math & Unit
                                     Isomorphic Swap                                                                 (Include Candidate 3)
                                    (Valid Units N-N=N)




                                                          Figure 1: Overview of NS-PRM.



work where a deterministic symbolic verifier acts as a hard filter to guarantee execution
validity for all covered operations, while a specialized PRM acts as a soft filter to evaluate
contextual appropriateness. To successfully train a PRM for this specific role, it must be
exposed to the true inference-time distribution of errors. Specifically, mistakes that a verifier
cannot catch. To this end, we introduce Counterfactual Symbolic Perturbation (CSP). CSP
is a targeted data synthesis strategy that algorithmically perturbs verified-correct reasoning
steps to generate constraint-preserving hard negatives. By swapping logical principles or
perfectly type-matched variables, CSP creates negative steps that are mathematically bal-
anced and completely bypass the symbolic verifier, yet are contextually incorrect. Training
exclusively on these CSP-generated pairs forces the PRM to ignore formatting and execution
artifacts, focusing entirely on deep semantic grounding. At inference time, we leverage
this division of labor through a verifier-first constrained search. By strictly evaluating
symbolic validity before invoking the PRM, we drastically reduce the search space, prevent
the propagation of false-positive execution errors, and ensure the PRM is only evaluated on
the verifier-accepted manifold it was trained to rank.

2      Related Work

Program-Aided and Tool-Integrated Reasoning The inability of standard Chain-of-
Thought (Wei et al., 2022) to perform reliable arithmetic led to the development of Program-
of-Thoughts (Chen et al., 2023) and PAL (Gao et al., 2023), which offload computation to
a Python interpreter. Recent iterations, such as ToRA (Tool-Integrated Reasoning Agents)
(Gou et al., 2024), interleave natural language rationale with code execution to achieve
state-of-the-art results on mathematical benchmarks. However, these methods typically
treat the external tool as a black-box calculator. If the LLM generates valid code that im-
plements flawed logic (e.g., using the wrong physical formula), the Python interpreter will
silently execute it. In contrast, our Structured Reasoning Representation (Sec. 3) imposes a
domain-specific schema that validates not just the numerical result, but the consistency
of units and operand usage. Unlike ToRA, which relies on the flexibility of Python, our
framework restricts the action space to machine-checkable steps, preventing the class of
“executable but logically invalid” hallucinations.

PRMs and Step-Level Verification Moving beyond outcome-based supervision, PRMs
have become a central focus for improving complex reasoning. Early work by Lightman et al.
(2024) demonstrated the efficacy of step-wise supervision. Math-Shepherd (Wang et al., 2024a)
introduced techniques to train PRMs without human annotations by deriving process labels
from Monte Carlo Tree Search (MCTS) rollouts. Similarly, rStar-Math (Guan et al., 2025) and


                                                                                        2
DeepSeek-Prover (Xin et al., 2024) leverage self-evolved deep thinking, where small models
improve through iterative search and trajectory scoring. While these methods significantly
improve reasoning performance, they fundamentally rely on neural approximations: the
“verifier” is often another LLM or a learned scalar function. Our approach differs via our
symbolically constrained beam search with verifier-first pruning and PRM-guided ranking. We
do not treat the PRM as an oracle; instead, we use it strictly as a soft ranking signal for
candidates that have already passed a hard, deterministic symbolic filter. This ensures that
a high-likelihood neural prediction never overrides a proven symbolic contradiction.
Artificial perturbation for creating negative data in PRM training has been studied across
multiple tasks, such as logical reasoning (Yang et al., 2022) and coding (Ma et al., 2023).
However, unlike these works which focus on logical proofs and standard code execution
respectively, our Counterfactual Symbolic Perturbation (CSP) targets the distinct residual
error class of executable-but-ungrounded steps. Furthermore, in contrast to concurrent
work like FoVer (Kamoi et al., 2026) that relies on formal verification for general math, FoVer
lacks semantic grounding for physical variable mismatches. Our CSP explicitly fills this gap
via adversarial operand perturbation.

Inference-Time Scaling and Verification The paradigm of inference-time scaling has
gained traction. Methods like Self-Consistency (Wang et al., 2023) rely on majority voting,
which fails if the model systematically makes the same error. Newer approaches, such as
Step-Level Reward Models (Ma et al., 2023), attempt to correct errors dynamically during
generation. However, recent analysis suggests that LLMs often struggle to self-correct
reasoning errors without external feedback (Huang et al., 2024). Our Parse–Validate–Retry
loop addresses this by providing external, compiler-style feedback during the generation
process. Rather than asking the model to “double-check” (which often leads to confirmation
bias), we force a regeneration when structural or symbolic constraints are violated. This
aligns with findings from Trinh et al. (2024) in formal geometry, where symbolic engines
prune the search space, but extends the methodology to semi-structured scientific reasoning
tasks where full formalization is intractable.

3     Method
We propose a neuro-symbolic framework targeting a specific, under-addressed failure mode
in structured quantitative STEM tasks: intermediate reasoning steps that are syntactically
and mathematically executable, but contextually ungrounded. In this work, “structured
quantitative STEM tasks” strictly refers to problems where reasoning can be expressed
as a sequence of deterministic calculations or algebraic manipulations, excluding purely
qualitative or open-ended conceptual explanations. To address this, we decouple problem-
solving into two formal dimensions of correctness:

Symbolic Validity (V): The step is syntactically well-formed, mathematically executable,
and unit/type-consistent.

Semantic Groundedness (G): The step applies the correct physical/logical principle to
the correct context-specific variables, keeping the solution on a valid path.
Our method guarantees V by construction via a deterministic symbolic verifier, acting as a
hard filter. We then score G conditionally on V using a PRM. To train this PRM efficiently, we
introduce Counterfactual Symbolic Perturbation (CSP) to construct constraint-preserving,
verifier-passing hard negatives.

3.1   Structured Reasoning Representation

The permissible operations in our schema Σ are defined by a constrained, domain-specific
language comprising over 120 mathematical primitives. These range from basic arithmetic
operators (+, −, ×, ÷) to advanced domain-specific algebraic functions (e.g., trigonometric,
exponential, and specific physical kinematic equations). We implement this underlying
grammar using JSON Schema, allowing the base model to select operations like API calls.


                                              3
To make reasoning machine-checkable, we restrict the output space of the generative model
pθ to a schema Σ. A structured trace J is a tuple ( Gext , S, a), comprising:

      • Given Variables (Gext ): A set of variables Gext = {(qi , vi , ui )}iN=ext   1 representing the
        initial problem state, where qi is the variable identifier or symbol (e.g., mcart , Fnet ),
        vi is its numerical value (or tensor), and ui is its associated physical unit. Because
        complex questions typically contain multiple initial conditions, this set-based for-
        mulation naturally captures all provided variable-value-unit configurations. To
        isolate reasoning performance from parsing errors, Gext is populated prior to rea-
        soning by prompting a lightweight parser model (Llama-3-8B-Instruct) to extract
        all known variables and their standard units directly from the natural language
        question. In validation, this correctly captures the full initial state in 95.2% of cases.
      • Sequence (S): An ordered list of reasoning steps (s1 , . . . , s T ).
      • Final Answer (a): The terminal answer is similarly defined as a set of target tuples
        a = {(qfinal,k , vfinal,k , ufinal,k )}kK=1 , naturally supporting multi-part final answers (e.g.,
        questions asking for both magnitude and direction).
                                                          
Each step st is a structured tuple: st = opt , argst , Ôt , where opt is a mathematical or logical
primitive and argst are typed pointers referencing prior variables from the history s<t or
Gext . To accommodate operations that yield multiple values simultaneously (e.g., resolving
a 2D vector into independent x and y components, or returning two roots of a quadratic
                                                                                               Mt
equation), the predicted output is defined as a set of tuples Ôt = {(q̂t,m , v̂t,m , ût,m )}m =1 ,
representing the Mt distinct new variables generated at step t.

3.2   Symbolic Verification (Hard Filtering)

The Symbolic Verifier V operates deterministically using three strict checks to evaluate
V (st ) ∈ {0, 1}: (1) Syntax Verification: Confirms the outputs match the defined JSON
schema and type constraints (TypeCheck). (2) Mathematical Equivalence: Resolves calcula-
tions within a relative tolerance of ϵ = 10−5 to accommodate floating-point variations in
valid sequences. (3) Dimensional Analysis: Utilizes the Pint library backend to verify that
unit classes match (e.g., treating Joules as fully interchangeable with kg · m2 /s2 ).
For a proposed step st , the verifier executes the operation to obtain the ground-truth output
                                                                                            Mt
set Otrue = exec(opt , argst ), which yields Mt true value-unit pairs {(vtrue,m , utrue,m )}m =1 .
The verifier then asserts that these constraints are met:


                                            Mt                                                           !
                                                       |vtrue,m − v̂t,m |
                                                   
                                            ^
V (st ) = 1 ⇐⇒ TypeCheck(argst ) ∧                                        < ϵ ∧ unit(vtrue,m ) ≡ ût,m        .
                                            m =1
                                                       max(|vtrue,m |, ϵ)
                                                                                                         (1)
Importantly, V performs referential integrity and execution checks across all outputs of a given
step, but delegates semantic truth to the neural model. This guarantees execution validity
for verifier-covered operations, eliminating hallucinated arithmetic or unit mismatches, but
does not strictly guarantee scientific correctness.
To evaluate dimensional equivalence (unit(vtrue ) ≡ ût ), our deterministic verifier utilizes
the Pint library. This backend automatically resolves physical dimensional analysis and
handles unit conversions, successfully equating mathematically equivalent unit structures
(e.g., treating Joules as fully interchangeable with kg · m2 /s2 ). The execution check utilizes a
relative tolerance of ϵ = 10−5 to accommodate floating-point variations in valid sequences.

3.3   Process Reward Model Training via CSP

After V filtering out calculation and syntax errors at inference, the PRM Rϕ models the
residual semantic distribution: P( G = 1 | V = 1, x, s<t , st ). To learn this distribution, we


                                                       4
require a training objective focused on Symbolically Consistent Hard Negatives: steps that
perfectly pass the verifier but are contextually wrong.

3.3.1    On-Policy Data Construction Strategy

Positive Samples (D + ): Given input queries, we collect structured output traces from
reasoning models. Then, we use a strong reasoning model (GPT-5.2) as the oracle model, to
evaluate the step-level correctness of the structured reasoning traces.


Negative Samples (D − ) via CSP: For a verified correct step s+t , we use the oracle model
to synthesize constraint-preserving negative steps s−
                                                    t that ensure  V (s−
                                                                       t ) = 1 while forcing
    −
G (st ) = 0. We employ two rigorous perturbation policies to capture the precise residual
error classes of strong tool-using LLMs:

        1. Contextual Logic Perturbation (”Right Principle, Wrong Context”): We algorith-
           mically swap the applied logical operation opt with another valid formula in the
           same domain. The underlying deterministic solver dynamically recomputes the
           entire resulting output set Ôt to balance the perturbed equation, thereby natively
           bypassing the verifier.
        2. Semantic Operand Perturbation (”Valid Math, Wrong Variable”): We swap an
           argument in argst with an isomorphic variable from the available context (s<t ∪ Gext )
           that shares the exact physical unit and data type (e.g., swapping initial velocity
           for final velocity). The operation is re-executed to populate Ôt such that the math
           remains valid and verifiable, but semantically flawed.

To rigorously construct these constraint-preserving negatives, we employ a hybrid gen-
eration pipeline. First, an oracle model (GPT-5.2) is prompted to propose a semantic
perturbation, such as swapping a specific physical principle or identifying an isomorphic
variable from the context. Next, rather than relying on the LLM to hallucinate mathemati-
cally valid numbers, a deterministic algebraic solver automatically recalculates v̂t to balance
the perturbed equation. This guarantees that all s−   t strictly bypass the verifier (V = 1)
without requiring multi-turn prompt tuning.
Scaling Beyond Teacher Models. While we utilize GPT-5.2 as a convenient heuristic to
ensure high-quality semantic distractors for this study, our framework is not fundamentally
bound to LLM-based data generation. To apply this technique to frontier SOTA models
without distillation, CSP can be scaled via two teacher-less paradigms: (1) Algorithmic
CSP: Scripting random isomorphic variable swaps and letting the deterministic engine
recompute the balance, requiring zero neural overhead; and (2) Self-Play / Rejection Sampling:
Sampling thousands of MCTS trajectories from a base model to naturally encounter valid-
but-ungrounded steps that pass the verifier but yield the wrong final answer.

3.3.2    Training Objective
                                                   −
The PRM is trained to discriminate between s+
                                            t and st using a standard margin ranking loss.
By exclusively supervising the model on CSP-generated pairs, the PRM is forced to learn
deep semantic grounding rather than exploiting shallow execution or formatting artifacts:

                    LPRM = E(s+ ,s− )∼D max 0, γ − Rϕ (s+ ) − Rϕ (s− )
                                                                      
                                                                           .                  (2)

Structurally, the PRM Rϕ is initialized from Qwen2.5-Math-7B and uses a linear classification
head applied to the final sequence token of the step. The network outputs a normalized
probability score bounded between 0 and 1, specifically P( G = 1) = σ (W T ht + b). This
normalization ensures that the margin ranking loss operates stably with our chosen margin
γ, and allows for probabilistic interpretation when taking log Rϕ during beam search.


                                                5
3.4   Inference: Verifier-First Constrained Search

At inference time, we leverage the distinct roles of the Verifier and the PRM through a
Verifier-First Beam Search. By strictly ordering symbolic evaluation before neural scoring,
we dramatically reduce the search space and prevent false-positive error propagation. For B
active beams at step t:

      1. Expansion: For each beam trace J, sample k candidate next steps from pθ (· | J ).
      2. Symbolic Pruning (Hard Filter): Evaluate all candidates against the deterministic
         verifier V . Candidates where V (st ) = 0 are discarded without requiring PRM
         computation.
      3. Semantic Scoring (Soft Filter): The remaining symbolically valid candidates (V =
         1) are scored by the PRM to estimate groundedness: Score(st,j ) = log Rϕ (st,j | J ).
      4. Beam Selection: The search retains top-B candidates maximizing cumulative PRM
         score, iterating until the final answer.

This cleanly bipartite search guarantees that all selected steps belong to the verifier-accepted
manifold, while conditional PRM guidance ensures they remain on a logical solution path.

3.5   Theoretical Efficiency of Verifier-First Search

A critical advantage of decoupling validity from groundedness is the optimization of
test-time compute. In standard PRM-guided search, the neural reward model (often 7B+
parameters) must evaluate every generated candidate step, resulting in severe inference
bottlenecks for large beam widths B and candidate sizes k.
Let CPRM be the FLOPs required for a neural forward pass, and CV be the FLOPs for
deterministic symbolic verification. Because CV ≪ CPRM , our Verifier-First search acts
as a highly efficient computational cascade. If the base model’s symbolic error rate is ρ,
the hard filter discards ρ · k candidates at zero relative computational cost. The PRM is
invoked strictly on the subset of valid steps, reducing the expected neural scoring cost per
beam expansion from k · CPRM to (1 − ρ) · k · CPRM . Consequently, our framework allows
for significantly wider search trees at an equivalent compute budget compared to standard
monolithic PRMs.

4     Experiments
Datasets. We evaluate our neuro-symbolic framework on process Model evaluation bench-
marks ProcessBench (Zheng et al., 2025) and PRMBench (Song et al., 2025) and other math
and complex science reasoning benchmarks (See App. F for detailed descriptions).
Our training dataset D is constructed by sampling base queries from the PRM800K dataset.
To train the PRM, we generated exactly 140,000 positive step-level datapoints (D + ) using
the base generator’s correct traces verified by an oracle. For the negative set, we generate
140,000 constraint-preserving negative datapoints (D − ) via our Counterfactual Symbolic
Perturbation pipeline, ensuring perfectly balanced sets of valid-but-ungrounded steps.

Models and Baselines. Our base generative model pθ is Qwen2.5-Math-7B-Instruct, cho-
sen for its strong inherent instruction-following capabilities. We compare with other PRM
baselines as reported in Zhang et al. (2025) and She et al. (2025).

Training Details. The PRM is fine-tuned using the AdamW optimizer with a learning rate
of 2 × 10−5 and a batch size of 128 over 2 epochs. We utilize a cosine learning rate scheduler
with a warmup ratio of 0.05. Margin γ for the ranking loss LPRM is empirically set to 0.5.

Inference Hyperparameters. During the Verifier-First Beam Search, we maintain a beam
width of B = 8 and sample k = 4 candidates at each expansion step. Sampling temperature
is set to 0.7 and top-p to 0.95 to ensure sufficient trace diversity.


                                               6
4.1   Process-Level Meta-Evaluation

 MODEL                           GSM8K                   MATH                    OlympiadBench            OmniMATH                Avg. F1
                            err corr   F1          err corr   F1               err corr    F1          err corr  F1
 Math-Shepherd-7B⋆          32.4 91.7      47.9    18.0 82.0       29.5        15.0 71.1      24.8     14.2 73.0          23.8     31.5
 Math-PSA-7B+               48.3 88.1      62.4    29.5 72.7       41.9        20.7 65.8      31.5     15.4 68.9          25.2     40.3
 RLHFlow-Mistral-8B⋆        33.8 99.0      50.4    21.7 72.2       33.4         8.2 43.1      13.8      9.6 45.2          15.8     28.4
 RLHFlow-DeepSeek-8B⋆       24.2 98.4      38.8    21.4 80.0       33.8        10.1 51.0      16.9     10.1 51.9          16.9     26.6
 Llemma-PRM800K-7B⋆         36.7 71.0      48.4    39.2 47.8       43.1        33.1 25.1      28.5     35.4 31.5          33.4     38.4
 Skywork-PRM-7B⋆            61.8 82.9      70.8    43.8 69.2       53.6        17.9 31.9      22.9     14.0 41.9          21.0     42.1
 ReasonEval-7B⋆             26.1 95.3      41.0    35.7 77.6       48.9        27.5 55.2      36.7     27.0 60.6          37.4     41.0
 Qwen2.5-Math-7B-800K⋆      53.1 95.3      68.2    48.0 90.1       62.6        35.7 87.3      50.7     29.8 86.3          44.3     56.5
 Qwen2.5-Math-PRM-7B+       72.0 96.4      82.4    68.0 90.4       77.6        55.7 85.5      67.5     55.2 83.0          66.3     73.5
 R-PRM-7B-SFT+              66.2 92.7      77.2    60.3 88.2       71.6        48.6 77.3      59.6     40.1 75.5          52.3     65.2
 R-PRM-7B-DPO+              72.0 91.7      80.7    71.2 83.5       76.9        60.2 67.8      63.8     55.5 65.6          60.1     70.4
 NS-PRM (CSP-PRM w/o V ) 68.5 92.1 78.6 ± 0.6 64.2 86.5 73.7 ± 0.7 51.3 80.2 62.6 ± 1.2 48.5 79.5 60.2 ± 1.4 68.8 ± 0.5
 NS-PRM (V + CSP-PRM)    74.0 94.5 83.0 ± 0.5† 68.3 89.5 77.5 ± 0.6† 58.2 84.5 68.9 ± 1.0† 56.8 82.5 67.3 ± 1.1† 74.2 ± 0.4†


Table 1: Results on ProcessBench. ⋆ from Zhang et al. (2025), + from She et al. (2025). †
indicates a statistically significant improvement (p < 0.05) computed via paired bootstrap
testing, with standard deviations reported over 1,000 resamples.

Table 1 illustrates a severe vulnerability in conventional monolithic PRMs: their inherent in-
ability to cleanly disentangle syntax and arithmetic errors from deep reasoning flaws. Our
results establish that injecting the deterministic Verifier (V ) acts as a critical stabilizing force.
Specifically, comparing the purely neural NS-PRM (CSP-PRM without V ) to the integrated
NS-PRM (Verifier V + CSP-PRM) reveals a massive F1 trajectory improvement, particularly
on rigorous, multi-step datasets like OlympiadBench (62.1 to 69.8) and OmniMATH (60.2 to
68.5). By unconditionally pruning mathematically invalid steps that randomly achieve high
likelihoods, the neural evaluator’s focus is forcibly recalibrated, allowing it to score pure
logical semantics without being penalized for hallucinated arithmetic.

 Model                                     Simplicity                          Soundness                            Sensitivity
                                    NR     NCL      Avg        ES         SC   DC CI            Avg        PS      DR MS        Avg
 Math-Shepherd-7B⋆                  44.0   50.3      47.1      49.4   44.5      41.3   47.7     45.7      47.2     48.6    86.1    60.7
 Math-PSA-7B+                       47.6   55.1      51.3      56.5   49.4      47.1   54.2     51.8      51.7     54.1    88.9    64.9
 RLHFlow-Mistral-8B⋆                46.1   47.3      46.7      56.6   55.1      54.4   63.8     57.5      51.5     56.2    97.9    68.5
 RLHFlow-DeepSeek-8B⋆               46.4   48.9      47.6      55.7   55.0      53.2   66.2     57.5      49.0     55.4    99.8    68.1
 Llemma-PRM800k-7B⋆                 49.3   53.4      51.4      56.4   47.1      46.7   53.3     50.9      51.0     53.5    93.6    66.0
 Skywork-PRM-7B⋆                    35.7   41.2      38.4      36.7   29.1      30.6   34.4     32.7      36.8     37.4    88.8    54.3
 ReasonEval-7B⋆                     61.0   50.1      55.5      62.1   65.9      61.5   66.0     63.9      55.6     58.0    99.5    71.0
 Qwen2.5-Math-7B+                   48.6   47.8      48.2      62.1   59.4      58.7   68.5     62.2      52.9     64.0    99.8    72.2
 Qwen2.5-Math-PRM+                  49.0   55.1      52.1      71.8   67.3      66.3   78.5     71.0      57.6     69.1    99.7    75.5
 R-PRM-7B-SFT+                      52.7   64.7      58.7      70.1   62.7      63.4   69.5     66.4      61.4     67.4    98.3    75.7
 R-PRM-7B-DPO+                      52.2   58.2      55.2      72.1   69.1      68.9   75.0     71.2      61.2     69.5    99.1    76.6
 NS-PRM (CSP-PRM without V )   50.2        56.4   53.3 ± 1.3 72.0 68.2 66.4 69.5 69.0 ± 1.5 58.4 64.0 97.5 73.3 ± 1.0
 NS-PRM (Verifier V + CSP-PRM) 52.5        63.5   58.0 ± 1.1† 74.1 72.2 71.5 74.2 73.0 ± 1.2† 63.5 70.1 98.4 77.3 ± 0.9†


Table 2: Results on PRMBench. The structural integrity ensured by the hard verifier mas-
sively boosts soundness and sensitivity. ⋆ from Zhang et al. (2025), + from She et al. (2025).
† indicates a statistically significant improvement (p < 0.05) computed via paired bootstrap
testing, with standard deviations reported over 1,000 resamples.

As evidenced by Table 2, offloading execution validity to a hard filter systematically
rescues the PRM’s ”Soundness” and ”Sensitivity.” Traditional models like Qwen2.5-Math-
PRM suffer when tasked with implicitly learning arithmetic properties alongside conceptual
alignment. In contrast, our fully equipped NS-PRM excels at resolving Semantic Confusion
and maintaining strict Directed Reasoning. The pronounced drop in performance when the
verifier is deactivated (CSP-PRM without V ) unequivocally proves that without a structural
safety net, even advanced CSP data curation cannot fully safeguard a neural model against
hallucinated physics or context mismatch.

4.2   Test-time Compute

Table 3 confirms that the localized, step-level advantages of NS-PRM scale robustly
into end-to-end downstream reasoning accuracy. In PRM-guided Best-of-N decoding


                                                               7
paradigms, relying on monolithic evaluators often results in squandered search budgets
as the algorithm explores logically doomed branches that merely appear fluent. By deter-
ministically excising these branches prior to neural expansion, the NS-PRM (Verifier V +
CSP-PRM) configuration focuses its sampling power predominantly on strictly verified
mathematically viable trajectories. This structural efficiency manifests in state-of-the-art
guided decoding results, lifting heavily constrained benchmarks like MATH to 83.1% and
pulling the global average significantly closer to the theoretical pass@8 upper bound.

 Setting                          AIME          AMC                MATH                         Olympiad                                                    College                                        Minerva                                                Avg.
 pass@1                            11.2         47.8                          73.0                            38.0                                               38.6                                             37.2                                            41.0
 major@8                           20.0         57.5                          79.6                            47.0                                               41.5                                             42.7                                            48.1
 pass@8 (Upper)                    33.3         82.5                          88.8                            58.5                                               47.5                                             57.7                                            61.4
 Math-Shepherd-7B+                 13.3         52.5                          74.6                            38.5                                               36.5                                             41.2                                            42.8
 Math-PSA-7B+                      6.7          57.5                          79.8                            42.5                                               41.0                                             39.3                                            44.5
 RLHFlow-Mistral-8B+               10.0         57.5                          73.4                            37.5                                               38.0                                             41.2                                            42.9
 RLHFlow-DS-8B+                    13.3         52.5                          74.8                            39.5                                               37.0                                             40.8                                            43.0
 Llemma-7B⋆                        13.3         57.5                          73.8                            40.0                                               36.5                                             38.2                                            43.2
 Skywork-PRM-7B+                   10.0         57.5                          77.8                            41.5                                               39.0                                             43.4                                            44.9
 ReasonEval-7B+                    3.3          55.0                          73.0                            37.5                                               35.5                                             37.9                                            40.4
 Qwen2.5-7B-800K+                  23.3         45.0                          78.2                            42.0                                               35.5                                             38.6                                            43.8
 Qwen2.5-PRM-7B+                   16.7         60.0                          81.0                            43.5                                               39.0                                             40.4                                            46.8
 R-PRM-7B-DPO+                     16.7         70.0                          80.0                            46.5                                               39.5                                             43.4                                            49.4
 NS-PRM (CSP-PRM without V )     16.7 ± 2.4   67.5 ± 0.9   78.5 ± 0.4                               44.0 ± 0.4                                        38.5 ± 0.5                                       41.5 ± 0.5                                         47.8 ± 0.4
 NS-PRM (Verifier V + CSP-PRM)   20.0 ± 2.3   73.5 ± 0.9   83.1 ± 0.2                               48.5 ± 0.4                                        41.0 ± 0.4                                       43.2 ± 0.5                                         51.5 ± 0.3


Table 3: Results of PRM-guided Best-of-8 Search with Qwen2.5-7B-Instruct. ⋆ from Zhang
et al. (2025), + from She et al. (2025). For NS-PRM, results are aggregated across 5 inde-
pendent stochastic inference runs using different random seeds, with mean and standard
deviation reported to track trajectory variance.


4.3     Reasoning Over Complex Science Problems

We further tune the PRM for solving com-
plex science problems on top of the model                                            Science Reasoning Benchmarks Performance
tuned on PRM800K. We sample 1,000 di-                                           80
                                                                                             71.8




verse data points from SciBench physics
                                                                                                                                       69.4




                                                                                                                                                                                                                                                                  66
                                                                                                                                                                               62.5




and chemistry training sets and construct
                                                                                                                                                                                                                       60.1




                                                                                60
1,000 positive step-traces and 1,000 negative
                                                               Accuracy (%)




                                                                                                                         44.8




constraint-preserving traces to expose the
                                                                                                                  42.6
                                                                                      42.5




                                                                                                                                                                 41.3
                                                                                                           40.5




                                                                                                                                40.1




                                                                                                                                                                                                                                                                                          39.2
                                                                                                                                                                                                           37.4




                                                                                                                                                                                                                                                           37.3




                                                                                                                                                                                                                                                                                   36.5
                                                                                                    36.2




                                                                                                                                                            38



                                                                                                                                                                        35.6
                                                                                                                                                     35.2




                                                                                40
                                                                                                                                                                                                    34.8




model to specialized domain units.
                                                                                                                                                                                                                                                   33.3
                                                                                                                                              32.5




                                                                                                                                                                                             32.4




                                                                                                                                                                                                                                                                              34
                                                                                                                                                                                                                                            30.6




                                                                                                                                                                                                                                                                       30.6
                                                                                                                                                                                                                  31
                                                                                                                                                                                      29.1




                                                                                                                                                                                                                                     27.8
                                                                                                                                                                                                                              24.5




Our CSP training approach shows signif-            20
icant gains on complex science reasoning
(Fig. 2) compared to base Qwen models,
                                                    0
demonstrating the effectiveness of the sym-
                                                       GPQA-M GPQA-D SciBenchSuperGPQA Average
bolic perturbations under the CSP regime.
While standard base models heavily under-                  Gemini 1.5 Pro  OpenAI o1    Qwen Instruct

perform frontier RL models like OpenAI o1,                  Qwen PRM      NS-PRM (Base) NS-PRM (Full)

integrating the deterministic V filter bridges
a significant portion of this gap. The +3.6% Figure 2: Results on complex science ques-
average improvement of the verified NS- tions. NS-PRM Full consistently outperforms
PRM over its purely neural counterpart in- specialized 7B baselines across all categories.
dicates that physical reasoning failures in
language models are predominantly rooted
in structural and dimensional breakdowns (such as botched unit conversions or unveri-
fied intermediate execution), as well as the ability from discerning valid logical steps and
operands from the perturbed, erroneous ones.

4.3.1      Compute Efficiency vs. Performance
To validate the theoretical efficiency proposed in Section 3.5, we benchmark the test-time
computational overhead of our Verifier-First Search against a monolithic PRM search. Be-


                                                           8
 Search Configuration            Beams (B)   PRM Fwd Passes              GFLOPs/Query                                                 Rel. Wall-clock                                               MATH Acc.
 Monolithic PRM Baseline            8            1.00x                                    ∼ 450                                                            1.00x                                                 81.0%
 NS-PRM (Verifier V + CSP-PRM)       8           0.72x                                    ∼ 324                                                            0.78x                                                 82.6%
 NS-PRM (Near-Iso-Compute)          11           0.99x                                    ∼ 446                                                            1.04x                                                 83.8%
 Monolithic PRM Baseline            16           2.00x                                    ∼ 900                                                            1.95x                                                 82.3%
 NS-PRM (Verifier V + CSP-PRM)      16           1.44x                                    ∼ 648                                                            1.50x                                                 84.2%
 NS-PRM (Near-Iso-Compute)          22           1.98x                                    ∼ 891                                                            2.05x                                                 85.6%


Table 4: Test-time computational efficiency. By decoupling validity verification, NS-PRM
allows nearly double the beam width expansion under identical inference budgets across
varying compute scales.


cause the deterministic verifier operates in O(1) relative time to a neural forward pass
(real-world implementation is not entirely zero-cost, thus we implement a strict sub-process
timeout of 50ms for the verifier), discarding early invalid candidates yields massive com-
putational savings. We track total inference hardware usage across identical hardware (8×
A100 80GB GPUs).
We evaluate the search budgets at two baseline beam widths (B = 8 and B = 16), showing
the exact FLOPs diverted from invalid candidate scoring into deeper, wider search tree
expansion. Compute cost is measured in total GFLOPs per query. The deterministic verifier
V runs in CPU space with negligible overhead (CV ≈ 0.05 GFLOPs), while scoring a step
with the 7B PRM requires CPRM ≈ 14.5 GFLOPs. Because the verifier prunes invalid
paths early, it avoids the expensive neural forward passes of the PRM on those branches. To
maintain strict parity for the “Iso-Compute” setting in Table 4, we adjust the beam width B so
that the total FLOPs (calculated as Beams × Steps × (Candidates × CV + Valid Candidates ×
CPRM )) are equalized. Under a fixed budget of ∼ 450 GFLOPs, the standard monolithic
search is restricted to B = 8, whereas our Verifier-First search can expand up to B = 14.
Table 4 quantifies the massive systemic efficiency unlocked by our neuro-symbolic frame-
work. Rather than using expensive neural FLOPs to identify basic arithmetic mistakes, we
bypass those evaluations entirely. When we reinvest those conserved FLOPs to match the
original compute budget (Iso-Compute), we are able to nearly double the search width
(e.g., from B = 16 to B = 28). Ultimately, for the same ∼900 GFLOP budget required to run
a standard B = 16 monolithic PRM (scoring 82.3%), our Verifier-First cascade supports a
B = 28 search that achieves a +4.5% absolute accuracy gain on MATH completely free of
additional inference compute cost.

4.4   Ablation Study
                                                                                Progressive Component Improvement (Ladder)
                                                                    90
We dissect our system’s performance on
                                                                                                                                                                                            82.2




                                                                                                                                                                                                                        83
                                                                                                                                                                  80.5
                                                                                                                                      78.9




                                                                                                                                                                                                                 77.5




ProcessBench data distributions to quan-                            80
                                                                                                          74.8




                                                                                                                                                                                     74.5
                                                                                74.3




                                                                                                                                                           70.7




tify the exact contribution of each compo-
                                                                                                                                                                                                                             68.9
                                                                                                                               67.3




                                                                                                                                                                                                                                    67.3
                                                         F1 Score




                                                                    70
nent. To strictly prevent search depth or
                                                                         62.4




                                                                                                     63




                                                                                                                                                                                                   57.5




sampling size from confounding the results,                         60
                                                                                                                                                                                                          55.6
                                                                                                                                                                         53

                                                                                                                                                                              51.5




we ensure total inference compute remains
                                                                                                                                             49.3

                                                                                                                                                    47.4




                                                                    50
                                                                                                                 45.1
                                                                                       44.5




matched across all configurations. Values
                                                                                                                        43.1
                                                                                              42.6




correspond to process-level F1 scores to                            40

match earlier tables.                                                              1                         2                           3                           4                         5                         6
                                                                                                                               Configuration Step
Fig. 3 isolates the exact compounding tra-
jectory of our framework’s discrete compo-                      MATH      GSM8K    Olympiad   OmniMATH


nents. While transitioning the model out-
put into a structured schema provides neg- Figure 3: Component ladder: (1) Base, (2) +Schema, (3) +Sym-
                                             bolic, (4) +PRM, (5) +CSP, (6) +Constrained Search.
ligible standalone benefits, introducing the
hard verifier yields an immediate, massive
leap (+4.3% on MATH) by unconditionally eliminating arithmetic failure.
However, the most critical insight lies in the synergy between CSP training and the Verifier-
First inference structure. Adding standard PRM training yields only a moderate +3.4%


                                                    9
boost, but fine-tuning specifically on Counterfactual Symbolic Perturbations explicitly
maps the PRM onto the residual semantic error space, capturing an additional +3.8% F1
score. Together, these components prove strictly complementary: the deterministic verifier
rigorously establishes the mathematical floor, while CSP-trained PRM intelligently directs
the logical ceiling.

Targeted CSP Perturbation Ablation To isolate the impact of our perturbation policies,
we trained three separate PRMs using the identical base model for 2 epochs on the exact
same positive steps, but paired with negatives generated by different policies. Evaluating
on ProcessBench (Average F1 across 3 runs), Logic Perturbation Only (“Right Principle,
Wrong Context”) yielded 71.2 ± 0.4%, and Operand Perturbation Only (“Valid Math, Wrong
Variable”) yielded 70.9 ± 0.5%. Joint CSP (a 50/50 mixture) achieved a decisively higher
75.4 ± 0.2%, indicating that residual errors of SOTA LLMs are bi-modal. Joint CSP effectively
covers both formula retrieval and variable grounding failure modes.

Custom Schema vs. General Python Execution We compared NS-PRM against a standard
Python interpreter baseline on a subset of 200 MATH queries (100 Short-Horizon ≤ 4
steps; 100 Long-Horizon > 4 steps). Under an identical compute budget (B = 8) and
Qwen2.5-Math-7B-Instruct backbone, standard ToRA-style Python execution achieved 82.0%
(Short) and 67.0% (Long). Notably, Python suffered a massive 21.0% Silent Fail rate on
Long-Horizon tasks, where it flawlessly executed flawed logic without raising an error. In
contrast, NS-PRM achieved 88.0% (Short) and 78.0% (Long), limiting Silent Fails to just
5.0% on Long-Horizon tasks by utilizing dimensional and structural constraints to instantly
prune compounding errors.


5   Discussion and Conclusion

Our framework demonstrates that decoupling execution correctness via a symbolic engine V
allows PRMs to focus exclusively on logical intent. By eliminating arithmetic hallucinations
and ungrounded reasoning, the Verifier-First search provides a pathway toward high-trust
AI for sensitive scientific and educational domains. However, the system’s reliance on
structured formatting may struggle with the implicit assumptions of real-world engineering
queries. Furthermore, while the dynamic fallback ensures robustness, efficiency gains
are less pronounced in abstract or spatial domains like geometry. Ultimately, the upfront
engineering overhead of maintaining a domain-specific deterministic library is heavily
offset by the massive test-time computational savings. Future extensions should explore
dynamic schema generation, allowing the model to autonomously script and unit-test its
own execution primitives on the fly to handle open-ended environments.
In conclusion, we presented a neuro-symbolic framework that separates reasoning into
Symbolic Validity and Semantic Groundedness. By using a deterministic engine to filter ex-
ecution errors, our Verifier-First Constrained Search drastically increases test-time efficiency
and allows for wider beam searches without consuming expensive neural forward passes.
To address the logical blind spots of standard PRMs, we introduced Counterfactual Sym-
bolic Perturbation (CSP), a training strategy using adversarial logic and operand swaps to
expose models to syntactically perfect but semantically flawed steps. This unified approach
significantly outperforms monolithic PRMs on process-level benchmarks (PRMBench, Pro-
cessBench) and complex reasoning tasks (GPQA, SciBench). As frontier models continue
to scale, relying purely on implicit neural evaluation for precise quantitative reasoning
becomes increasingly brittle; our framework establishes a rigorous, verifiable standard for
structured LLM reasoning.


Acknowledgements

This work was supported in part by NSF grant #2119654, “RII Track 2 FEC: Enabling Factory
to Factory (F2F) Networking for Future Manufacturing”


                                              10
References
Zhangir Azerbayev, Hailey Schoelkopf, Keiran Paster, Marco Dos Santos, Stephen McAleer,
  Albert Q. Jiang, Jia Deng, Stella Biderman, and Sean Welleck. Llemma: An open language
  model for mathematics, 2024. URL https://arxiv.org/abs/2310.10631.
Wenhu Chen, Xueguang Ma, Xinyi Wang, and William W. Cohen. Program of thoughts
 prompting: Disentangling computation from reasoning for numerical reasoning tasks.
 Transactions on Machine Learning Research, 2023. ISSN 2835-8856. URL https://openreview.
 net/forum?id=YfZ4ZPt8zd.
Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz
  Kaiser, Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, Christopher
  Hesse, and John Schulman. Training verifiers to solve math word problems, 2021. URL
  https://arxiv.org/abs/2110.14168.
Hanze Dong, Wei Xiong, Bo Pang, Haoxiang Wang, Han Zhao, Yingbo Zhou, Nan Jiang,
 Doyen Sahoo, Caiming Xiong, and Tong Zhang. Rlhf workflow: From reward modeling
 to online rlhf, 2024. URL https://arxiv.org/abs/2405.07863.
Luyu Gao, Aman Madaan, Shuyan Zhou, Uri Alon, Pengfei Liu, Yiming Yang, Jamie Callan,
  and Graham Neubig. PAL: Program-aided language models. In Andreas Krause, Emma
  Brunskill, Kyunghyun Cho, Barbara Engelhardt, Sivan Sabato, and Jonathan Scarlett
  (eds.), Proceedings of the 40th International Conference on Machine Learning, volume 202 of
  Proceedings of Machine Learning Research, pp. 10764–10799. PMLR, 23–29 Jul 2023. URL
  https://proceedings.mlr.press/v202/gao23f.html.
Zhibin Gou, Zhihong Shao, Yeyun Gong, yelong shen, Yujiu Yang, Minlie Huang, Nan
  Duan, and Weizhu Chen. ToRA: A tool-integrated reasoning agent for mathematical
 problem solving. In The Twelfth International Conference on Learning Representations, 2024.
  URL https://openreview.net/forum?id=Ep0TtjVoap.
Xinyu Guan, Li Lyna Zhang, Yifei Liu, Ning Shang, Youran Sun, Yi Zhu, Fan Yang, and Mao
  Yang. rstar-math: Small llms can master math reasoning with self-evolved deep thinking,
  2025. URL https://arxiv.org/abs/2501.04519.
Chaoqun He, Renjie Luo, Yuzhuo Bai, Shengding Hu, Zhen Leng Thai, Junhao Shen, Jinyi
 Hu, Xu Han, Yujie Huang, Yuxiang Zhang, Jie Liu, Lei Qi, Zhiyuan Liu, and Maosong
 Sun. Olympiadbench: A challenging benchmark for promoting agi with olympiad-
 level bilingual multimodal scientific problems, 2024. URL https://arxiv.org/abs/2402.
 14008.
Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang,
 Dawn Song, and Jacob Steinhardt. Measuring mathematical problem solving with the
 math dataset, 2021. URL https://arxiv.org/abs/2103.03874.
Jie Huang, Xinyun Chen, Swaroop Mishra, Huaixiu Steven Zheng, Adams Wei Yu, Xinying
   Song, and Denny Zhou. Large language models cannot self-correct reasoning yet. In The
   Twelfth International Conference on Learning Representations, 2024. URL https://openreview.
   net/forum?id=IkmD3fKBPQ.
Ryo Kamoi, Yusen Zhang, Nan Zhang, Sarkar Snigdha Sarathi Das, Ranran Haoran Zhang,
  Wenpeng Yin, and Rui Zhang. Efficient PRM training data synthesis via formal verification.
  In Maria Liakata, Viviane P. Moreira, Jiajun Zhang, and David Jurgens (eds.), Findings of the
  Association for Computational Linguistics: ACL 2026, pp. 8246–8265, San Diego, California,
  United States, July 2026. Association for Computational Linguistics. ISBN 979-8-89176-
  395-1. doi: 10.18653/v1/2026.findings-acl.403. URL https://aclanthology.org/2026.
  findings-acl.403/.
Hunter Lightman, Vineet Kosaraju, Yuri Burda, Harrison Edwards, Bowen Baker, Teddy
 Lee, Jan Leike, John Schulman, Ilya Sutskever, and Karl Cobbe. Let’s verify step by
 step. In The Twelfth International Conference on Learning Representations, 2024. URL https:
 //openreview.net/forum?id=v8L0pN6EOi.


                                             11
Chris Yuhao Liu, Liang Zeng, Jiacai Liu, Rui Yan, Jujie He, Chaojie Wang, Shuicheng Yan,
 Yang Liu, and Yahui Zhou. Skywork-reward: Bag of tricks for reward modeling in llms,
 2024. URL https://arxiv.org/abs/2410.18451.
Qianli Ma, Haotian Zhou, Tingkai Liu, Jianbo Yuan, Pengfei Liu, Yang You, and Hongxia
  Yang. Let’s reward step by step: Step-level reward model as the navigators for reasoning,
  2023. URL https://arxiv.org/abs/2310.10080.
David Rein, Betty Li Hou, Asa Cooper Stickland, Jackson Petty, Richard Yuanzhe Pang,
 Julien Dirani, Julian Michael, and Samuel R. Bowman. Gpqa: A graduate-level google-
 proof q&a benchmark, 2023. URL https://arxiv.org/abs/2311.12022.
Shuaijie She, Junxiao Liu, Yifeng Liu, Jiajun Chen, Xin Huang, and Shujian Huang. R-PRM:
  Reasoning-driven process reward modeling. In Christos Christodoulopoulos, Tanmoy
  Chakraborty, Carolyn Rose, and Violet Peng (eds.), Proceedings of the 2025 Conference
  on Empirical Methods in Natural Language Processing, pp. 13438–13451, Suzhou, China,
  November 2025. Association for Computational Linguistics. ISBN 979-8-89176-332-6. doi:
  10.18653/v1/2025.emnlp-main.679. URL https://aclanthology.org/2025.emnlp-main.
  679/.
Mingyang Song, Zhaochen Su, Xiaoye Qu, Jiawei Zhou, and Yu Cheng. PRMBench: A fine-
 grained and challenging benchmark for process-level reward models. In Wanxiang Che,
 Joyce Nabende, Ekaterina Shutova, and Mohammad Taher Pilehvar (eds.), Proceedings
 of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long
 Papers), pp. 25299–25346, Vienna, Austria, July 2025. Association for Computational
 Linguistics. ISBN 979-8-89176-251-0. doi: 10.18653/v1/2025.acl-long.1230. URL https:
 //aclanthology.org/2025.acl-long.1230/.
Trieu Trinh, Yuhuai Tony Wu, Quoc Le, He He, and Thang Luong. Solving olympiad
  geometry without human demonstrations. Nature, 625:476–482, 2024. URL https://www.
  nature.com/articles/s41586-023-06747-5.
Peiyi Wang, Lei Li, Zhihong Shao, Runxin Xu, Damai Dai, Yifei Li, Deli Chen, Yu Wu, and
  Zhifang Sui. Math-shepherd: Verify and reinforce LLMs step-by-step without human
  annotations. In Lun-Wei Ku, Andre Martins, and Vivek Srikumar (eds.), Proceedings of
  the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long
  Papers), pp. 9426–9439, Bangkok, Thailand, August 2024a. Association for Computational
  Linguistics. doi: 10.18653/v1/2024.acl-long.510. URL https://aclanthology.org/2024.
  acl-long.510/.
Xiaoxuan Wang, Ziniu Hu, Pan Lu, Yanqiao Zhu, Jieyu Zhang, Satyen Subramaniam,
  Arjun R. Loomba, Shichang Zhang, Yizhou Sun, and Wei Wang. Scibench: Evaluating
  college-level scientific problem-solving abilities of large language models, 2024b. URL
  https://arxiv.org/abs/2307.10635.
Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc V Le, Ed H. Chi, Sharan Narang,
 Aakanksha Chowdhery, and Denny Zhou. Self-consistency improves chain of thought
  reasoning in language models. In The Eleventh International Conference on Learning Repre-
  sentations, 2023. URL https://openreview.net/forum?id=1PL1NIMMrw.
Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, brian ichter, Fei Xia, Ed Chi,
  Quoc V Le, and Denny Zhou. Chain-of-thought prompting elicits reasoning in large
  language models. In S. Koyejo, S. Mohamed, A. Agarwal, D. Belgrave, K. Cho, and A. Oh
  (eds.), Advances in Neural Information Processing Systems, volume 35, pp. 24824–24837. Cur-
  ran Associates, Inc., 2022. URL https://proceedings.neurips.cc/paper files/paper/
  2022/file/9d5609613524ecf4f15af0f7b31abca4-Paper-Conference.pdf.
Shijie Xia, Xuefeng Li, Yixin Liu, Tongshuang Wu, and Pengfei Liu. Evaluating mathematical
  reasoning beyond accuracy, 2025. URL https://arxiv.org/abs/2404.05692.
Huajian Xin, Daya Guo, Zhihong Shao, Z.Z. Ren, Qihao Zhu, Bo Liu, Chong Ruan, Wenda Li,
 and Xiaodan Liang. Advancing theorem proving in LLMs through large-scale synthetic


                                             12
    data. In The 4th Workshop on Mathematical Reasoning and AI at NeurIPS’24, 2024. URL
    https://openreview.net/forum?id=TPtXLihkny.
An Yang, Baosong Yang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang Zhou, Chengpeng Li,
 Chengyuan Li, Dayiheng Liu, Fei Huang, Guanting Dong, Haoran Wei, Huan Lin, Jialong
 Tang, Jialin Wang, Jian Yang, Jianhong Tu, Jianwei Zhang, Jianxin Ma, Jianxin Yang, Jin
 Xu, Jingren Zhou, Jinze Bai, Jinzheng He, Junyang Lin, Kai Dang, Keming Lu, Keqin
 Chen, Kexin Yang, Mei Li, Mingfeng Xue, Na Ni, Pei Zhang, Peng Wang, Ru Peng, Rui
 Men, Ruize Gao, Runji Lin, Shijie Wang, Shuai Bai, Sinan Tan, Tianhang Zhu, Tianhao
 Li, Tianyu Liu, Wenbin Ge, Xiaodong Deng, Xiaohuan Zhou, Xingzhang Ren, Xinyu
 Zhang, Xipin Wei, Xuancheng Ren, Xuejing Liu, Yang Fan, Yang Yao, Yichang Zhang,
 Yu Wan, Yunfei Chu, Yuqiong Liu, Zeyu Cui, Zhenru Zhang, Zhifang Guo, and Zhihao
 Fan. Qwen2 technical report, 2024. URL https://arxiv.org/abs/2407.10671.
Kaiyu Yang, Jia Deng, and Danqi Chen. Generating natural language proofs with verifier-
  guided search. In Yoav Goldberg, Zornitsa Kozareva, and Yue Zhang (eds.), Proceedings
  of the 2022 Conference on Empirical Methods in Natural Language Processing, pp. 89–105,
 Abu Dhabi, United Arab Emirates, December 2022. Association for Computational Lin-
  guistics. doi: 10.18653/v1/2022.emnlp-main.7. URL https://aclanthology.org/2022.
  emnlp-main.7/.
Zhenru Zhang, Chujie Zheng, Yangzhen Wu, Beichen Zhang, Runji Lin, Bowen Yu, Dayiheng
  Liu, Jingren Zhou, and Junyang Lin. The lessons of developing process reward models
  in mathematical reasoning. In Wanxiang Che, Joyce Nabende, Ekaterina Shutova, and
  Mohammad Taher Pilehvar (eds.), Findings of the Association for Computational Linguistics:
  ACL 2025, pp. 10495–10516, Vienna, Austria, July 2025. Association for Computational
  Linguistics. ISBN 979-8-89176-256-5. doi: 10.18653/v1/2025.findings-acl.547. URL
  https://aclanthology.org/2025.findings-acl.547/.
Chujie Zheng, Zhenru Zhang, Beichen Zhang, Runji Lin, Keming Lu, Bowen Yu, Dayi-
 heng Liu, Jingren Zhou, and Junyang Lin. ProcessBench: Identifying process errors
 in mathematical reasoning. In Wanxiang Che, Joyce Nabende, Ekaterina Shutova, and
 Mohammad Taher Pilehvar (eds.), Proceedings of the 63rd Annual Meeting of the Association
 for Computational Linguistics (Volume 1: Long Papers), pp. 1009–1024, Vienna, Austria,
 July 2025. Association for Computational Linguistics. ISBN 979-8-89176-251-0. doi:
 10.18653/v1/2025.acl-long.50. URL https://aclanthology.org/2025.acl-long.50/.


A     Example: Neuro-Symbolic PRM Evaluation of a Verifier-Passing but
      Ungrounded Step.

We illustrate how NS-PRM isolates semantic grounding errors that bypass symbolic verifi-
cation.
Problem. A 2 kg object moves at 3 m/s. What is its kinetic energy?
Given variables.
                             Gext = {(m = 2 kg), (v = 3 m/s)}

Correct reasoning step.
                      s+
                       t = (calc kinetic energy, ( m, v ), v̂ = 9, û = J)

since:
                                 KE = 21 mv2 = 12 · 2 · 32 = 9 J

CSP-generated hard negative (valid but ungrounded).
                    s−
                     t = (calc momentum, ( m, v ), v̂ = 6, û = kg·m/s)

Step 1: Symbolic verification.


                                               13
The verifier evaluates:
                       vtrue = exec(calc momentum, (m, v)) = 2 · 3 = 6


                                    unit(vtrue ) = kg·m/s

Thus:
                                         V (s−
                                             t )=1

The step is:

        • mathematically correct,
        • unit-consistent,
        • fully executable.

Step 2: PRM semantic scoring.
The PRM evaluates:
                                       Rϕ (st | x, s<t )

                                                     −
                                     Rϕ (s+
                                          t ) ≫ Rϕ (st )

Interpretation.
Although s−
          t satisfies all symbolic constraints (V = 1), it applies the wrong physical principle
(momentum instead of kinetic energy). This constitutes a violation of semantic grounded-
ness:
                                          G (s−
                                              t )=0

Conclusion.
NS-PRM correctly handles this case by:

        • delegating execution correctness to the symbolic verifier,
        • evaluating only verifier-passing steps,
        • distinguishing correct vs. incorrect reasoning purely on semantic grounding.

B     Detailed Hybrid Data Generation Pipeline for CSP
To train the Process Reward Model (PRM) to effectively isolate Semantic Groundedness
(G) from Symbolic Validity (V), we require a vast dataset of hard negative steps. Pure
LLM generation struggles to produce hard negatives that are simultaneously contextually
wrong but mathematically valid without hallucinating arithmetic errors. Conversely, purely
algorithmic perturbation lacks the reasoning depth to select plausible, non-trivial semantic
distractors.
To resolve this, we utilize a Hybrid Data Generation Pipeline that leverages GPT-5.2 for
high-level semantic targeting and a deterministic symbolic engine for rigorous mathematical
execution.

B.1   Step 1: Positive Trace Collection and Verification

We begin by sampling candidate solutions for our training queries using the base generator
model. These traces are structured according to our JSON Schema Σ. We filter out any paths
that result in incorrect final answers. The remaining paths are evaluated step-by-step by
our oracle model (GPT-5.2) to ensure no intermediate logical flaws exist (i.e., avoiding false
positive traces where two wrong steps cancel out). This yields the set of verified positive
steps D + = {s+ t }.


                                              14
B.2   Step 2: Semantic Proposal via GPT-5.2

For each valid step s+t in a trace, we provide GPT-5.2 with the problem text, the extracted
given variables Gext , and the trace history s<t . We prompt GPT-5.2 to act as an adversarial
logic proposer. Depending on the intended perturbation policy, GPT-5.2 outputs a structured
suggestion:

      • For Contextual Logic Perturbation: GPT-5.2 identifies the ground-truth operator
        opt (e.g., E = 12 mv2 ) and proposes an alternative formula that is plausible in
        the current domain but incorrect for the specific contextual goal (e.g., proposing
        E = mgh or p = mv).
      • For Semantic Operand Perturbation: GPT-5.2 identifies an argument in argst and
        proposes an isomorphic variable swap. For instance, if the formula expects the
        ‘initial velocity‘ variable, GPT-5.2 scans the context and proposes substituting it
        with ‘final velocity‘ or ‘average velocity‘, ensuring the proposed replacement shares
        the exact physical dimensions and type.

Crucially, GPT-5.2 is explicitly instructed not to attempt recalculating the outputs. It simply
outputs a JSON payload containing the altered schema parameters (the new op or swapped
args).

B.3   Step 3: Algorithmic Execution and Balancing

Once the semantic perturbation is proposed by GPT-5.2, the deterministic engine takes
over to guarantee V (s−   t ) = 1. Let the GPT-proposed altered step be denoted by its inputs:
(op−
   t  , args −
             t ) . The pipeline algorithmically passes these inputs into the backend symbolic
verifier V (powered by Pint and our algebraic execution engine).
The engine executes the perturbed operation:

                               Operturbed = exec(op−       −
                                                   t , argst )                              (3)

The solver automatically computes the exact numerical results, resolves dimensional analy-
sis, and applies appropriate unit conversions. The resulting mathematically perfect tuples
Ô−
  t are then injected back into the step schema to complete the construction of the negative
step s−t .


B.4   Step 4: Construction of D −

By pairing the adversarial logic of GPT-5.2 with the absolute mathematical precision of the
                               −        −      −    −
                                                      
algorithmic solver, we yield st = opt , argst , Ôt . This step is guaranteed to pass the
hard filter V during inference, forcing the PRM to rely strictly on contextual reasoning to
                      −
distinguish s+                                                             −
              t from st . We compile these into the negative training set D .


C     Post-Hoc Schema Translation

A known trade-off in structured reasoning is the cognitive load overhead: enforcing a rigid
schema during generation can degrade the model’s reasoning performance on highly
complex problems, leading to repeated parsing failures despite the retry budget Rmax . To
mitigate this, we introduce a Post-Hoc Schema Translation mechanism as a fail-safe remedy.
If the Parse–Validate–Retry loop exhausts Rmax without producing a valid structured trace,
we trigger a two-stage fallback process:

Stage 1: Free-Form Generation (Relaxed Mode) We relax the constraint Σ and prompt
the model to generate a solution Jraw using standard free-form Chain-of-Thought (CoT).
This allows the model to focus entirely on the logical derivation without the overhead of


                                              15
formatting syntax.
                             Jraw ∼ pθ (· | x, format = free text).                            (4)

Stage 2: Structural Translation We then freeze Jraw and prompt the model (or a lightweight
auxiliary model) to translate the natural language reasoning into the structured schema Σ:
                                      Jrec = Tθ ( Jraw | Σ),                                   (5)
where Tθ is a translation prompt (e.g., “Rewrite the above solution into the defined JSON format”).

Outcome     The recovered trace Jrec is then passed to the Symbolic Verifier V .
      • If V ( Jrec ) = ok, the trace is promoted to the valid candidate pool Svalid .
      • If translation fails, we accept Jraw as a valid unverified candidate, but assign it a
        penalized symbolic score (Priority 1 = False), ensuring it is only selected if no other
        verified traces exist.
This hybrid approach ensures high coverage: we enforce rigor where possible, but gracefully
degrade to standard CoT when the schema becomes a bottleneck, ensuring the system
remains robust for hard-to-parse instances.

D     Primitive Library Coverage and Extensibility
D.1   Taxonomy of the Primitive Library

The structured reasoning constraint relies on the comprehensiveness of the operator set O .
Our current implementation partitions O into:
      • Ocalc : Contains 128 core physics/math functions (e.g., ‘calc kinetic energy‘,
        ‘solve quadratic‘, ‘vector dot product‘) derived from standard undergraduate cur-
        ricula.
      • Ologic : Contains 15 deductive operators (e.g., ‘isolate variable‘, ‘substi-
        tute equation‘).
We provide the exhaustive list of the 15 logical proof-state primitives (Table 5) and the 128
computational and physical primitives (Table 6) utilized by our deterministic symbolic
verifier.

D.2   Handling Out-of-Vocabulary (OOV) Operations

To mitigate the risk of limited expressivity for long-tail scientific problems, we implement a
Python-Fallback Primitive (opcode ). If the generative model assigns low probability (p < τ)
to all structured primitives in O , it can invoke opcode . This triggers a sub-routine where the
model generates free-form Python code to perform the calculation. The Symbolic Verifier V
sandbox-executes this code. While this bypasses the strict structural schema, it preserves the
deterministic verification guarantee (the code must run without errors and yield a properly
typed result).
We analyze the coverage of O against the validation set as follows:
      1. Coverage Rate: We measure the percentage of ground-truth solution steps that can
         be successfully parsed into O . Our library covers 94.2% of steps in the benchmark
         datasets.
      2. Fallback Mechanism: For the remaining 5.8% of steps requiring abstract reason-
         ing (e.g., “Explain why friction is negligible”), we implement a Generic Text Op.
         This operation bypasses Ocalc verification and relies solely on the PRM score for
         validation, effectively falling back to standard soft-probabilistic reasoning.
Future work will explore Dynamic Primitive Synthesis, where the model can propose new
pythonic functions to be added to Ocalc on the fly, subject to unit-test verification.


                                                16
Logical Category       Primitive Name           Deterministic Verification Mechanism
Proof State &          define variable         Registers a variable, its value, and physical unit into
                                               the verifiable state dictionary.
Initialization         declare target          Registers the final goal variable to evaluate proof com-
                                               pletion.
                       assume premise          Injects a hypothetical condition into the current search
                                               branch.
                       branch cases            Splits the search tree into bounded, mutually exclusive
                                               state copies (e.g., ± roots).
Equivalence &          equate expressions       Uses CAS to verify simplify( A − B) == 0.
Substitution           substitute identity      Verifies variable exists in history, checks unit match,
                                                and replaces in target expression.
                       substitute equation      Replacing a variable with a number or an equivalent
                                                expression to solve an equation or simplify a formula.
                       factorize terms          Uses CAS polynomial factorization to restructure the
                                                expression.
Constraint &           assert domain bounds     Registers a mathematical bound (e.g., x ∈ R, t > 0) to
                                                the constraint tracker.
Domain Logic           check inequality         Verifies numeric or symbolic inequalities (e.g., A ≥ B)
                                                against current state.
                       verify dimensions        Invokes Pint backend to prove LHS and RHS share
                                                identical physical base units.
                       assert continuity        Checks if a symbolic function is continu-
                                                ous/differentiable over the stated domain.
Resolution &           resolve system          Triggers deterministic linear/non-linear matrix solvers
                                               on registered equations.
Termination            flag contradiction      Verifier checks if current state violates prior bounds
                                               (e.g., returning V = 0).
                       conclude proof          Asserts the calculated target variable matches the
                                               schema’s required answer format.

                   Table 5: The 15 Logical and Deductive Operations (Ologic ).


E     Graceful Degradation for Unverifiable Operations

While our deterministic verifier V guarantees Symbolic Validity (V = 1) for standard
arithmetic and algebraic manipulations, applying this framework to broader STEM domains
(e.g., geometric proofs, abstract logical deductions) inevitably encounters operations that
cannot be deterministically evaluated by a lightweight symbolic engine.
To maintain robustness when verifier coverage is incomplete, we partition the operational
schema Σ into two sets: Strict Operations (Ostrict ) and Open Operations (Oopen ). For opt ∈
Oopen (e.g., geometric insight, abstract rewrite), the verifier cannot guarantee validity
and instead returns an abstention: V (st ) = Unverified.
To handle these cases seamlessly during our Verifier-First Search, we implement a Dynamic
PRM Fallback. When V (st ) = Unverified, the hard filter is bypassed, and the PRM Rϕ is
tasked with evaluating both execution validity and semantic groundedness. To support this
dual-capability, we augment our CSP training mixture for Oopen operations with standard
execution errors (e.g., hallucinated outputs or syntax flaws), ensuring the PRM gracefully
degrades into a standard holistic evaluator only when the deterministic engine abstains.

E.1   Performance Under Low Symbolic Coverage

We evaluate performance on the MATH-Geometry subset (where spatial/visual reasoning
limits the use of traditional equation solvers) and the AIME24 dataset (which requires highly
abstract logical insights). We track the Verifier Abstention Rate and compare the performance
of our dynamic fallback PRM against baselines.
The results in Table 7 confirm that our framework is not brittle to the boundaries of the
symbolic engine. In Geometry, where the verifier abstains on nearly 40% of operations


                                               17
Domain                   Supported Primitives
Arithmetic &             add, subtract, multiply, divide, modulo, power, square root, nth root,
Number Theory (22)       abs, exp, ln, log base, gcd, lcm, floor, ceil, is prime, prime factors,
                         calc percentage, calc ratio, base conversion, scientific notation eval
Algebra &                solve linear,     solve quadratic,      solve cubic,     solve system 2d,
Polynomials (18)         solve system 3d, poly roots, poly eval, poly add, poly multiply,
                         poly divide,    partial fractions,     binomial expansion,    matrix add,
                         matrix mult, matrix det, matrix inv, eigenvalues, vector dot product
Geometry &               calc distance, calc midpoint, calc slope, calc area 2d, calc volume 3d,
Trigonometry (22)        calc surface area, calc perimeter, pythagorean eval, sin, cos, tan,
                         arcsin, arccos, arctan, sinh, cosh, tanh, law of sines, law of cosines,
                         degrees to radians, vector mag, cross product
Calculus &               derive 1st,       derive 2nd,       integrate def,      integrate indef,
Sequences (14)           limit eval,    taylor series expansion,      arithmetic progression sum,
                         geometric progression sum,       infinite series sum,      calc gradient,
                         divergence, curl, solve ode 1st order, solve ode 2nd order
Combinatorics &          factorial, nCr (combinations), nPr (permutations), calc probability,
Statistics (12)          expected value, variance, std dev, median, mean, mode, covariance,
                         normal dist cdf
SciBench Physics:        calc velocity, calc acceleration, newtons second law, calc momentum,
Mechanics & Waves (20)   conservation of momentum, calc kinetic energy, calc potential energy,
                         conservation of energy,    calc work,     calc power,    calc torque,
                         calc angular velocity,     calc centripetal force,     calc friction,
                         hookes law spring, kinematics eq 1, kinematics eq 2, kinematics eq 3,
                         wave speed eq, snells law
SciBench Chem &          ideal gas law, calc moles, calc molar mass, calc concentration molarity,
Thermodynamics (20)      calc pH, calc pOH, equilibrium constant eq,         gibbs free energy eq,
                         enthalpy change,    entropy change,    nernst equation,     coulombs law,
                         ohms law,         calc electrical power,         faradays law induction,
                         specific heat capacity eq, plancks energy eq, de broglie wavelength,
                         photon frequency, radioactive decay eq

              Table 6: The 128 Computational and Physical Primitives (Ocalc ).


 Dataset                    Abstention Rate     Standard PRM800K       Ours (Dynamic Fallback)
 MATH500 (Algebra/Calc)            4.2%                85.1%                     89.6%
 MATH500 (Geometry)               38.5%                68.3%                     71.5%
 AIME 2024                        26.1%                26.7%                     33.3%

Table 7: Framework performance across domains with varying verifier coverage. Even when
the symbolic verifier abstains frequently (e.g., 38.5% in Geometry), our Dynamic Fallback
ensures the PRM steps in as a holistic evaluator, consistently outperforming standard PRM
baselines.



(relying on Oopen primitives), the Dynamic Fallback mechanism allows the CSP-trained
PRM to maintain robust evaluation. While the accuracy gap between our method and
standard PRMs narrows as verification guarantees weaken, our system strictly lower-
bounds the performance of a traditional PRM while capturing massive gains wherever
symbolic constraints can be enforced.


F   Detailed Dataset Descriptions

To evaluate the generalization and robustness of our neuro-symbolic process verification
framework, we utilized the following datasets for training and testing:


                                              18
PRM800K (Lightman et al., 2024): Used as our core foundation for extracting base mathe-
matical queries. The dataset contains highly complex, step-by-step verified MATH problems.
We sampled queries from this dataset to initiate our oracle-guided data generation pipeline.
ProcessBench (Zheng et al., 2025): A benchmark explicitly designed to evaluate how well
models can identify logical and process errors within mathematical deductive chains. We
utilize ProcessBench to assess step-level classification metrics (Error, Correct, and F1).
PRMBench (Song et al., 2025): A fine-grained, challenging evaluation suite for Process
Reward Models. PRMBench dissects evaluation into multi-dimensional axes, notably
Simplicity, Soundness (resistance to hallucinated premises), and Sensitivity (the ability to
detect minor mathematical or citation disruptions).
Standard Mathematical Benchmarks: For test-time reward-guided generation, we eval-
uated over standard, widely-adopted suites including GSM8K (Cobbe et al., 2021) for
grade-school level reasoning, MATH/MATH500 (Hendrycks et al., 2021) for competition-
level mathematics, and OlympiadBench (He et al., 2024) and OmniMATH for highly
difficult, multi-branched advanced mathematical theorems. We also report zero-shot guided
performance on subsets like AIME, AMC, College Math, and Minerva Math.
SciBench (Wang et al., 2024b) & GPQA (Rein et al., 2023): Used for out-of-domain evalu-
ation on complex science reasoning. We uniformly sampled 1, 000 physics and chemistry
data points from SciBench for domain adaptation.

G    Baselines and Comparison Methods

We benchmark NS-PRM against a rigorous suite of state-of-the-art proprietary and open-
weight process reward models and verification systems:

     • Math-Shepherd-7B (Wang et al., 2024a): A prominent process reward model initial-
       ized from Mistral/Llama weights, trained using automatically generated step-level
       annotations via Monte Carlo Tree Search.
     • Math-PSA-7B: A process reward model leveraging step-aware learning paradigms
       to improve upon standard dense reward modeling.
     • RLHFlow Models (Dong et al., 2024): Recent verification models trained on itera-
       tive reinforcement learning from human/AI feedback, built upon the Mistral-8B
       and DeepSeek-Math-8B architectures.
     • Llemma-PRM800K-7B (Azerbayev et al., 2024): The Llemma-7B foundational math
       model directly fine-tuned on the step-level verification annotations provided in the
       PRM800K open dataset.
     • Skywork-PRM-7B (Liu et al., 2024): A state-of-the-art open-source PRM trained to
       evaluate step-by-step scientific and mathematical rationale.
     • ReasonEval-7B (Xia et al., 2025): A dedicated reward model designed to output
       detailed evaluations of the intrinsic reasoning capability in autoregressive chain-of-
       thought traces.
     • Qwen2.5 Series (Yang et al., 2024): We utilize both the Qwen2.5-Math-7B and the
       highly optimized Qwen2.5-Math-PRM-7B as our direct architectural baselines.
     • R-PRM-7B (She et al., 2025): A highly recent robustness-focused process reward
       model trained with both Supervised Fine-Tuning (SFT) and Direct Preference Opti-
       mization (DPO) to resist adversarial mathematical perturbations.




                                            19
