                                          Reason Popper-ly: Patching In-Context Reasoning with Inductive
                                                               Logic Programming
                                                                               Zirong Chen           Meiyi Ma
                                                           Department of Computer Science, Vanderbilt University, USA
                                                          zirong.chen@vanderbilt.edu        meiyi.ma@vanderbilt.edu

                                                 Accepted at the 20th Conference on Neurosymbolic Learning and Reasoning


                                                                                          Abstract
                                                  Chain-of-thought (CoT) prompting enables large language models (LLMs) to tackle multi-
arXiv:2607.23019v1 [cs.AI] 25 Jul 2026




                                              step reasoning tasks, yet the generated intermediate steps are not guaranteed to be logically
                                              sound. We present Reason Popper-ly, a neurosymbolic framework that uses inductive logic
                                              programming (ILP) to learn relation composition rules from reasoning traces and deploys them
                                              as an online verifier for step-level correction. Given an LLM-generated trace, the method checks
                                              each inferred step against the learned rule table, diagnoses the violation type, rewrites incorrect
                                              steps with symbolically derived repairs, and regenerates the remaining suffix so that the model
                                              can produce its final answer conditioned on a verified trace. We evaluate on CLUTRR, a
                                              multi-hop kinship reasoning benchmark, using five language models over reasoning chains of
                                              2 to 10 hops. Across all models, Reason Popper-ly consistently improves terminal accuracy
                                              over standard CoT, with gains of up to 48 percentage points for small models and 15 points
                                              for frontier models on the longest chains. Compared with a fully exogenous symbolic pipeline,
                                              our method performs better on harder instances by preserving the model’s successful grounding
                                              while correcting only verifiable reasoning failures. In addition, step-level ILP verification yields
                                              a fine-grained error taxonomy that provides diagnostic insight beyond final-answer accuracy.


                                         1    Introduction
                                         Chain-of-thought (CoT) prompting has become a standard approach for eliciting multi-step rea-
                                         soning from large language models (LLMs) Wei et al. [2022]. By generating intermediate reasoning
                                         steps before producing a final answer, LLMs often achieve strong gains on tasks that require com-
                                         position, deduction, and planning. However, stronger end-task performance does not imply that
                                         the generated reasoning trace is logically sound or faithful to the model’s actual decision process.
                                         Prior work shows that CoT explanations can be plausible while remaining unfaithful Turpin et al.
                                         [2023], Lanham et al. [2023], and that reasoning quality degrades substantially as compositional
                                         depth increases Saparov and He [2023]. These findings point to a gap between the surface form
                                         of structured reasoning and its underlying validity. A natural response is to combine LLMs with
                                         symbolic methods. Recent neurosymbolic approaches either translate natural-language problems
                                         into formal representations and delegate reasoning to external solvers Pan et al. [2023], Olausson
                                         et al. [2023], or inject symbolic structure into the reasoning process to improve faithfulness and
                                         controllability Xu et al. [2024], Lyu et al. [2023]. These approaches show that symbolic constraints
                                         can improve reasoning reliability, but they typically operate at the level of the full problem or the
                                         full reasoning trace. In contrast, we study a more targeted setting: using symbolic knowledge as


                                                                                               1
an online guardrail over the model’s own reasoning trace, preserving valid intermediate work while
intervening at steps that violate explicit compositional rules.
    Bridging this gap with symbolic methods raises several open challenges: (1) Rule acquisition.
Symbolic verification requires explicit inference rules. Classical inductive logic programming (ILP)
Muggleton [1991], Cropper and Morel [2021] can learn such rules from examples rather than re-
quiring manual specification, but it has rarely been used as a runtime verifier for LLM-generated
reasoning traces. Existing neurosymbolic approaches either internalize rules through retraining
with logic-informed objectives de Souza et al. [2025], or rely on hand-crafted formal grammars
specified per domain Pan et al. [2023], Chen et al. [2022, 2023]. Neither directly learns verification
rules from model-generated reasoning traces and deploys them for online step-level intervention.
(2) Grounding bottleneck. Symbolic verification operates over structured predicates, whereas CoT
traces are written in natural language. This creates a grounding bottleneck in which extraction
or translation errors can compound with reasoning errors. Logic-LM Pan et al. [2023] partially
addresses this issue by using LLMs as translators from natural language to formal logic, but the
translation stage itself introduces an additional failure mode. More broadly, this bottleneck has
historically limited symbolic reasoning pipelines to relatively narrow and well-formalized domains
Olausson et al. [2023], Lyu et al. [2023]. (3) Error attribution. Current neurosymbolic verifiers
often reduce verification to a binary accept-or-reject decision over the full trace or full solution.
SymbCoT Xu et al. [2024] integrates symbolic expressions into chain-of-thought with an LLM-
based verification stage, but does not localize failures to specific reasoning steps or systematically
classify their types. A practically useful verifier should identify which step failed and why, such as
a wrong composition rule, a missing inversion, a direction reversal, or a hallucinated premise. Such
step-level attribution is important for targeted intervention and aligns with the broader motivation
for process-level reasoning supervision Lightman et al. [2023]. (4) Targeted correction. Retry-based
refinement methods Madaan et al. [2023], Gou et al. [2024] often discard the entire context and
regenerate from scratch, losing correct intermediate work. Replacing a single step is more targeted,
but it also changes the context for all subsequent steps. The corrected trace must therefore re-
main coherent, and the model must condition on the patched prefix in a way that meaningfully
improves the final answer. This is especially important because intrinsic self-correction without
reliable external feedback remains limited for reasoning tasks Huang et al. [2024].
    Targeting these challenges, we propose Reason Popper-ly, a framework that learns relation-
composition rules from reasoning traces via ILP and applies them as an online verifier over CoT
reasoning. Given a complete reasoning trace, our method checks each inferred step against an
induced composition table, classifies detected violations, replaces invalid steps with symbolically
grounded corrections, and regenerates only the remaining suffix conditioned on the patched prefix.
This design preserves the model’s own reasoning whenever it is already sound, while introducing
symbolic correction only where it is needed.
    Our contributions are: (1) We propose Reason Popper-ly, an ILP-based pipeline for step-level
verification and in-place repair of LLM reasoning traces. Rather than replacing model reasoning
with a standalone symbolic solver, our method uses learned symbolic rules as an online guardrail
over the model’s own CoT. (2) We introduce an error taxonomy for compositional reasoning fail-
ures that provides fine-grained diagnostic information beyond binary correctness. The taxonomy
is enabled by the structured nature of ILP-based verification and supports localized attribution of
reasoning failures. (3) We evaluate our method on CLUTRR Sinha et al. [2019] across multiple
language models and reasoning depths. The results show that step-level symbolic patching con-
sistently improves terminal accuracy over standard CoT, and becomes increasingly advantageous
over a fully exogenous symbolic pipeline as reasoning depth grows.



                                                  2
2     Background and Preliminaries
We briefly review in-context reasoning and inductive logic programming that are used throughout
the paper.

2.1   In-Context Reasoning
Given a pretrained language model M and an input sequence x consisting of a task description
and optional demonstrations, in-context reasoning refers to the process by which M generates a
response y through conditional next-token prediction, without updating model parameters. The
model relies on the information available within its context window.

Chain-of-thought (CoT). Chain-of-thought prompting Wei et al. [2022] elicits intermediate
reasoning steps s1 , s2 , . . . , sn before a final answer a. We denote the resulting reasoning trace by

                                          τ = (s1 , . . . , sn , a).

Each step si is a natural-language statement that either (i) restates information explicitly given in
the input, which we call a stated step, or (ii) derives new information from previous steps, which
we call an inferred step.

Step soundness. Let R be a set of inference rules. An inferred step si is sound with respect
to R if the conclusion expressed by si follows from its cited premises under some rule r ∈ R. A
reasoning trace τ is sound if every inferred step in τ is sound. Soundness is necessary but not
sufficient for final-answer correctness, since a trace may still begin from incorrectly extracted or
misinterpreted premises.

2.2   Inductive Logic Programming
Inductive Logic Programming (ILP) Muggleton [1991] learns a logic program H from background
knowledge B, positive examples E + , and negative examples E − such that:

                                             B ∪ H |= E +                                            (1)
                                                              −
                                             B ∪ H ̸|= E                                             (2)

That is, the learned hypothesis H together with B should entail all positive examples while re-
maining consistent with all negative examples. In our setting, the learned hypothesis consists of
ground facts over a ternary predicate compose/3. Formally, compose(r1 , r2 , r3 ), where r1 , r2 , r3 ∈ V
are relation symbols drawn from a finite vocabulary V. Each fact states that composing relation
r1 with relation r2 yields relation r3 . Collectively, these facts define a partial composition table
R : V × V ⇀ V.
    We use Popper Cropper and Morel [2021], an ILP system based on learning from failures1 .
Popper follows a generate, test, and constrain loop: it proposes candidate hypotheses using answer
set programming, evaluates them against the examples in Prolog, and derives constraints from
failed candidates to prune subsequent search. In our case, this allows us to induce a compact
symbolic rule table that can later be used for runtime verification of LLM reasoning steps.




                                                      3
Figure 1: Overview of Reason Popper-ly. Left: an LLM-generated reasoning trace may contain
locally plausible but compositionally invalid steps. Right: our method detects violated steps, diag-
noses the error type, patches the offending step, and regenerates the remaining suffix conditioned
on the corrected prefix.


3        Method: Reason Popper-ly
We propose Reason Popper-ly, a framework that uses ILP-learned relation-composition rules to
verify and repair LLM chain-of-thought traces at the step level. The framework has two phases.
In the offline phase, we induce a symbolic composition table from reasoning traces. In the online
phase, we apply this table as a runtime verifier that detects, diagnoses, and repairs invalid inferred
steps in newly generated traces. Figure 1 gives an overview.

3.1       Offline: Learning Composition Rules
This offline phase constructs a frozen composition table R that maps valid relation pairs to their
composed relation. This table is learned once and reused for all test instances.

Trace collection. We prompt each LLM with structured CoT instructions on a training set of
CLUTRR stories. For each instance, the model produces a reasoning trace τ = (s1 , . . . , sn , a),
where each step explicitly indicates whether it is stated or inferred, together with the indices of the
supporting prior steps. We then partition the collected traces by terminal correctness. Traces whose
    1
        Codebase: https://github.com/logic-and-learning-lab/Popper


                                                     4
final answer matches the gold label contribute positive supervision, while traces with incorrect final
answers contribute negative supervision.

Composition extraction. For every inferred step that cites exactly two prior steps, we extract
a composition triple (r1 , r2 , r3 ), which encodes the claim that relation r1 composed with relation
r2 yields relation r3 . This extraction requires direction normalization: relations expressed in the
story may not align with the direction needed by the reasoning chain. We therefore map each
relation into chain-consistent form using a gender-aware inverse map when necessary. For example,
if the story states “Mildred is the daughter of Gerald,” the corresponding relation from Gerald to
Mildred in the reasoning chain is father.

Rule induction. We provide the extracted positive and negative triples to Popper Cropper
and Morel [2021] as examples of the target predicate compose/3. Particularly designed for kinship
reasoning, the hypothesis space is restricted to ground facts of the form compose(r1 , r2 , r3 ), so that
each learned clause corresponds to a single entry in the composition table rather than a higher-order
rule schema. The induced facts are then validated against a gold kinship composition table derived
from CLUTRR Sinha et al. [2019] and supplemented with any missing gold entries. The resulting
table R serves as the symbolic verifier used at inference time.

3.2   Online: Verify, Diagnose, Patch
At inference time, the LLM first produces a complete reasoning trace. We then apply a post-hoc
verification-and-repair procedure to this trace. We do not intervene during autoregressive decoding
itself, which keeps the procedure simple and avoids complications related to hidden-state or key-
value cache manipulation.

Step 1: Verify. Given a trace τ = (s1 , . . . , sn , a), we parse each inferred step into a composition
triple (r1 , r2 , r3 ) using the same extraction and normalization procedure as in the offline phase.
We then check the triple against the learned composition table R. If (r1 , r2 ) ∈ dom(R) but
R(r1 , r2 ) ̸= r3 , the step is marked as a violation. If the relation pair is outside the domain of R,
the step is treated as unverifiable and left unchanged.

Step 2: Diagnose. Once violation is detected, we assign it one of four diagnostic types: (1)
wrong rule: the model uses the correct pair of premise relations but predicts the wrong composed
relation; (2) missing inv: the model fails to invert a premise relation into the chain-consistent
direction before composition; (3) direction rev: the model predicts the inverse of the correct
target relation; (4) hallucinated: the model cites a premise relation that is not supported by
the story or prior stated facts. This classification is obtained by comparing model-produced triple
against rule-table entry together with the inverse-relation map. The resulting taxonomy provides
more information than binary verification alone: it not only identifies that a step is invalid, but
also exposes the structural reason for failure.

Step 3: Patch. For each step si , we define a verified step s∗i according to whether the step is
constraint-consistent. Let C denote the set of constraint-consistent steps. Then:
                                      (
                                  ∗     si ,             if si ∈ C
                                si =                                                         (3)
                                        Patch(si ; R), otherwise


                                                   5
where Patch(·) is a constraint-aware repair operator that rewrites the relation in si using the
corrected composition R(r1 , r2 ) while preserving the involved entities and step context as much as
                / C and later steps are entailed from such si , we replace si with s∗i and discard all
possible. If si ∈
subsequent steps. The remaining suffix is then regenerated conditioned on the patched prefix and
diagnosed errors, yielding τ ′ = (s1 , . . . , si−1 , s∗i , . . . , s′n ). We apply this repair process iteratively
until no further verifiable violations remain, resulting in a fully verified trace τ ∗ = (s∗1 , . . . , s∗n ).
Finally, the repaired trace τ ∗ is returned to the LLM as context for generating the final answer.
Conceptually, this procedure acts as a local repair operator over the reasoning trace: it preserves the
model’s original reasoning wherever possible, intervenes only at rule-violating steps, and restores
downstream coherence by regenerating only the affected suffix.


4    Evaluation
We evaluate on CLUTRR Sinha et al. [2019], a benchmark for multi-hop kinship reasoning. Each
instance consists of a narrative describing family relations among named characters, a query asking
for relation between two target characters, and a gold relation label. Solving an instance requires
composing a sequence of intermediate kinship relations, for example composing sister and father
to derive aunt. We randomly sample 3,073 instances from CLUTRR, stratified across reasoning
chains of 2 to 10 hops. We reserve 200 held-out 2-hop instances for ILP rule learning and validation.
Longer chains are used only at evaluation time, where the goal is not to learn additional rules but
to test whether the learned local rules can support iterative verification and repair under increasing
reasoning depth.

                                                         Reasoning Chain Length (# of hops)

     Model                Reasoning Setups        Short (2-3)   Medium (4-5)     Long (6-7)    Longer (8-10)

                          Endogenous             56.95±1.73      43.74±3.49      25.91±3.45     19.09±2.00
     Qwen-3.5:4B          Exogenous              75.07±1.33      70.94±2.90      56.67±4.06     46.72±4.35
                          Popper-ly (Ours)       73.23±1.05      72.78±3.87      67.36±4.16     61.93±5.33

                          Endogenous             65.92±1.91      54.05±5.75      38.14±6.13     14.39±3.15
     Gemma-4:E4B          Exogenous              78.35±1.57      71.67±4.33      54.56±4.44     42.22±3.39
                          Popper-ly (Ours)       77.84±1.95      74.68±5.02      66.22±3.93     62.74±3.58

                          Endogenous             39.48±2.79      29.68±1.90      28.67±7.17     18.72±5.26
     LLaMA-3.2:3B         Exogenous              63.93±1.99      54.41±2.19      39.91±5.14     33.48±6.12
                          Popper-ly (Ours)       70.36±1.91      63.67±2.09      52.32±6.16     42.48±7.62

                          Endogenous             86.75±0.88      74.15±6.35      64.93±9.45     56.92±2.83
     Claude-4.6 Sonnet    Exogenous              88.87±1.28      75.91±3.09      71.31±3.01     66.79±6.70
                          Popper-ly (Ours)       89.63±1.59      79.69±3.70      73.33±2.57     71.38±7.71

                          Endogenous             89.23±0.94      78.06±2.69      68.15±4.72     59.91±5.56
     GPT-5.4              Exogenous              92.90±1.39      80.44±3.89      71.75±6.45     69.53±3.45
                          Popper-ly (Ours)       92.59±1.95      85.31±4.41      79.62±7.95     75.09±5.35

Table 1: Terminal accuracy (%) on CLUTRR under multi-fold evaluation. Endogenous: LLM rea-
soning via single-shot CoT. Exogenous: LLM extracts facts and symbolic composition is performed
using the learned rule table. Popper-ly: LLM generates CoT, and ILP-based verification and
repair is applied to violated inferred steps. Best result in each row block is shown in bold.


                                                        6
Research Question. Does step-level ILP-based verification and repair improve terminal rea-
soning accuracy over both endogenous CoT reasoning and fully exogenous symbolic composition,
especially as compositional depth increases?

Models. We evaluate following LLMs: (1) Small local models. Qwen-3.5:4B Qwen Team [2026],
Gemma-4:E4B Google DeepMind [2026], and LLaMA-3.2:3B Touvron et al. [2023], Meta AI [2024].
These models are run locally on an NVIDIA A6000 Ada GPU. (2) Frontier API models. Claude
Sonnet 4.6 Anthropic [2026] and GPT-5.4 OpenAI [2026], accessed through their respective APIs.
All models receive the same structured CoT prompt with explicit formatting instructions. The
final answer is constrained to one of the 21 CLUTRR relation labels, such as father, aunt, and
grandson-in-law, in order to reduce answer-format errors that are unrelated to reasoning quality.

Metric. Our primary metric is terminal accuracy, defined as the fraction of instances for which
the model’s extracted final answer exactly matches the gold relation label. We report terminal
accuracy by model, reasoning configuration, and hop range. Our main quantity of interest is the
accuracy gain of step-level symbolic patching over standard single-shot CoT.

Baselines. We compare Reason Popper-ly against two baselines. (1) Endogenous reasoning
(single-shot CoT). The LLM generates a full chain-of-thought trace and a final answer without any
external verification or intervention. This is the standard CoT setup Wei et al. [2022] and isolates
the model’s native compositional reasoning ability. (2) Exogenous reasoning (symbolic composition
pipeline). The LLM is used only to extract stated facts from the narrative Schick et al. [2023],
Yao et al. [2022]. We then build a relational graph over entities, identify a path between the
query targets using breadth-first search, and compose relations along that path using the learned
rule table R. This baseline removes model-endogenous reasoning after extraction and therefore
isolates the benefit of exact symbolic composition conditional on successful grounding. Its failures
primarily reflect brittleness in fact extraction and graph construction rather than errors in symbolic
composition itself.

Terminal Performance Analysis. Table 1 reports terminal accuracy across five models, three
reasoning configurations, and four hop bins. We highlight three findings. (1) Step-level symbolic
repair consistently improves over endogenous CoT. Across all models and all reasoning depths,
Reason Popper-ly outperforms standard single-shot CoT. The improvements are especially large
for smaller models on long chains. At 8-10 hops, Qwen improves from 19.09% to 61.93%, Gemma
from 14.39% to 62.74%, and LLaMA from 18.72% to 42.48%. Even frontier models benefit ma-
terially: Claude Sonnet improves from 56.92% to 71.38%, and GPT-5.4 improves from 59.91% to
75.09%. These results indicate that a substantial portion of long-chain degradation arises from
verifiable local composition errors that can be corrected after generation. (2) The relative advan-
tage of exogenous symbolic composition decreases as reasoning depth grows. A consistent crossover
pattern appears across models. At short chains, the exogenous pipeline often matches or slightly
exceeds Reason Popper-ly. This is expected: when the required reasoning depth is small, fact
extraction is relatively easy and exact symbolic composition is highly effective. As chain length
increases, however, Reason Popper-ly overtakes the exogenous baseline and the gap widens. At
8-10 hops, the advantage of Reason Popper-ly over exogenous reasoning ranges from 4.59 points
for Claude Sonnet to 20.52 points for Gemma. This pattern suggests a shift in the dominant fail-
ure mode. For short chains, local reasoning mistakes dominate. For longer chains, extraction and
graph-construction errors accumulate, which increasingly harms fully exogenous symbolic pipelines.


                                                  7
In contrast, our method preserves the LLM’s own extraction and intermediate structure whenever
they are already usable, and intervenes only at reasoning steps that violate learned composition
rules. (3) Frontier models remain patchable. Claude Sonnet 4.6 and GPT-5.4 start from much
stronger endogenous CoT baselines than the smaller local models, but both still exhibit substantial
degradation as reasoning depth increases. The fact that step-level symbolic repair yields gains
even at this scale shows that compositional reasoning failures are not restricted to weaker models.
Instead, they remain present, detectable, and actionable even in strong frontier systems. This sup-
ports the broader view that lightweight symbolic guardrails can remain useful even when the base
model is already highly capable.




                 Figure 2: Distribution of diagnosed errors among reasoning hops.


Error Attribution Analysis. Figure 2 shows the distribution of diagnosed error types among all
detected reasoning errors. Two patterns are especially notable. (1) the error taxonomy reveals clear
model-specific failure profiles rather than a single undifferentiated notion of reasoning error. Smaller
local models exhibit a more balanced mix of wrong rule, missing inv, and direction rev, with
wrong rule being the dominant category (43-49%). In contrast, frontier models shift sharply
toward missing inv, which accounts for 75% of GPT-5.4 errors and 78% of Sonnet-4.6 errors,
while wrong rule drops to 16% and 4%, respectively. This suggests that scaling reduces core
composition mistakes but does not eliminate structured reasoning failures; instead, the dominant
failure mode shifts toward relation-direction normalization errors. (2) hallucinated errors are
nearly absent across all models (0-2%), indicating that in this benchmark the main bottleneck
is not unsupported premise invention, but incorrect symbolic composition and direction handling.
These findings support the value of step-level symbolic diagnosis: it not only enables targeted repair,
but also exposes qualitatively different reasoning weaknesses across model scales.


5    Related Work
Chain-of-thought reasoning and failure modes. Chain-of-thought prompting improves perfor-
mance on many multi-step reasoning tasks by eliciting intermediate natural-language steps before


                                                   8
final answer Wei et al. [2022]. At the same time, a growing body of work shows that these inter-
mediate traces should not be taken at face value. Prior studies find that CoT explanations can
be unfaithful to the model’s underlying decision process Turpin et al. [2023], Lanham et al. [2023],
and that compositional reasoning quality deteriorates rapidly as proof depth increases Saparov and
He [2023]. More broadly, process-level supervision has been motivated by the observation that
final-answer correctness alone provides only a weak signal for reasoning quality Lightman et al.
[2023]. Our work builds on this line of evidence, but focuses on different intervention: rather than
supervising reasoning during training, we verify and repair explicit reasoning steps at inference time
using learned rules. Neuro-symbolic reasoning with LLMs. A growing literature combines
LLMs with symbolic reasoning systems to improve faithfulness, controllability, and logical correct-
ness Yang et al. [2023], Hsiang et al. [2025], Cheng et al. [2025], Chen et al. [2025a], An et al. [2026].
Logic-LM Pan et al. [2023] translates natural-language problems into formal logic and delegates in-
ference to an external solver. LINC Olausson et al. [2023] similarly combines LLMs with first-order
logic provers for logical reasoning. SymbCoT Xu et al. [2024] injects symbolic expressions directly
into chain-of-thought traces and adds an LLM-based verification stage, while faithful reasoning ap-
proaches have also explored stronger structural constraints over intermediate reasoning Lyu et al.
[2023]. These methods either rely on symbolic reasoning over the full problem or restructure the
reasoning process globally. Our method operates on the model’s own generated trace and intervenes
only at individual steps that violate induced composition rules, preserving the remaining interme-
diate reasoning whenever possible. Self-correction and iterative refinement. Another related
line of work studies whether LLMs can improve their own outputs through critique and revision.
Self-Refine Madaan et al. [2023] iteratively feeds model-generated feedback back into the model for
refinement, and CRITIC Gou et al. [2024] augments revision with tool-interactive critique. These
methods are general and often effective in practice, but they typically revise outputs through broad
regeneration rather than localized, rule-grounded correction. Moreover, recent evidence suggests
that LLMs cannot reliably self-correct reasoning in the absence of strong external feedback Huang
et al. [2024], Chen et al. [2025b]. Our method uses exactly such external feedback, but in a symbolic
form: the model is not asked to discover its own mistake, only to continue from a corrected prefix
that has been externally verified and repaired. Inductive logic programming. ILP learns logic
programs from examples Muggleton [1991]. Modern systems such as Popper Cropper and Morel
[2021] perform hypothesis-driven search with efficient pruning from failed candidates, making them
practical for learning compact symbolic rule sets. Recent work has also explored interactions be-
tween LLMs and ILP, for example by using LLMs to generate supervision for logical rule induction
de Souza et al. [2025]. Our use of ILP is different in both role and timing. We do not use ILP as a
standalone solver, nor as a training-time signal for updating the language model. Instead, we use
ILP to induce a symbolic composition table offline and deploy the learned rules at inference time
as a step-level verifier and repair mechanism over reasoning traces.


6    Discussion, Limitation, and Future Work
Domain specificity. Our evaluation focuses on kinship reasoning, where relation composition is
well defined and grounding from natural language to structured predicates is relatively tractable
through templated parsing. This makes CLUTRR a useful testbed for studying whether symbolic
verification can improve step-level reasoning, but it also limits the immediate generality of our
findings. In domains with more ambiguous predicate structures, such as legal reasoning or scientific
argumentation, both the grounding process and the induced rule space would be substantially more
complex. Assumptions about explicit reasoning. Our method assumes that the explicit CoT


                                                    9
trace remains causally relevant to the model’s final answer, so that editing an intermediate step
can redirect the downstream conclusion. This assumption is not guaranteed. Prior work has shown
that CoT explanations can function as post-hoc rationalizations rather than faithful accounts of
the model’s underlying computation Turpin et al. [2023], Lanham et al. [2023]. If the model
has effectively committed to an answer before the full reasoning trace is produced, then patching
intermediate steps may have limited influence on the final prediction. Our empirical results suggest
that the assumption is at least partially valid in the evaluated setting, since symbolic patching
yields consistent gains in terminal accuracy.


7    Conclusion
We presented Reason Popper-ly, a framework for improving LLM CoT reasoning through ILP-
based step-level verification and repair. The method learns symbolic relation composition rules
offline, then applies them at inference time to detect violated reasoning steps, diagnose their error
type, patch invalid compositions, and regenerate only the affected suffix of the trace. In this way,
the framework preserves the model’s own reasoning wherever it is already valid while introducing
symbolic correction only where it is needed. Experiments across multiple LLMs and reasoning
depths show that Reason Popper-ly consistently improves terminal accuracy over standard CoT
prompting. The gains become more pronounced as reasoning chains grow longer, where local
composition errors accumulate and increasingly degrade unassisted model reasoning. Overall, these
results suggest that symbolic reasoning support need not fully replace model-generated reasoning
to be useful. In compositional settings, a lightweight verifier that selectively repairs invalid steps
can offer a practical middle ground between unconstrained CoT and full symbolic delegation.




                                                 10
References
Ziyan An, Xia Wang, Hendrik Baier, Zirong Chen, Abhishek Dubey, Taylor T Johnson, Jonathan
  Sprinkle, Ayan Mukhopadhyay, and Meiyi Ma. Logiex: Integrating formal logic and llms for
  explainable transit planning. In 2026 ACM/IEEE 17th International Conference on Cyber-
  Physical Systems (ICCPS), pages 88–99. IEEE, 2026.

Anthropic. Claude 4.6. https://www.anthropic.com/news/claude-sonnet-4-6, 2026. Accessed:
 2026-04-07.

Zirong Chen, Isaac Li, Haoxiang Zhang, Sarah Preum, John A Stankovic, and Meiyi Ma. Cityspec:
  An intelligent assistant system for requirement specification in smart cities. In 2022 IEEE In-
  ternational Conference on Smart Computing (SMARTCOMP), pages 32–39. IEEE, 2022.

Zirong Chen, Isaac Li, Haoxiang Zhang, Sarah Preum, John A Stankovic, and Meiyi Ma. Cityspec
  with shield: A secure intelligent assistant for requirement formalization. Pervasive and Mobile
  Computing, 92:101802, 2023.

Zirong Chen, Ziyan An, Jennifer Reynolds, Kristin Mullen, Stephen Maritini, and Meiyi Ma.
  Logidebrief: A signal-temporal logic based automated debriefing approach with large language
  models integration. In James Kwok, editor, Proceedings of the Thirty-Fourth International Joint
  Conference on Artificial Intelligence, IJCAI-25, pages 9582–9590. International Joint Confer-
  ences on Artificial Intelligence Organization, 8 2025a. doi: 10.24963/ijcai.2025/1065. URL
  https://doi.org/10.24963/ijcai.2025/1065. AI and Social Good.

Zirong Chen, Elizabeth Chason, Noah Mladenovski, Erin Wilson, Kristin Mullen, Stephen Martini,
  and Meiyi Ma. Sim911: towards effective and equitable 9-1-1 dispatcher training with an llm-
  enabled simulation. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 39,
  pages 27896–27904, 2025b.

Fengxiang Cheng, Haoxuan Li, Fenrong Liu, Robert van Rooij, Kun Zhang, and Zhouchen Lin.
  Empowering llms with logical reasoning: A comprehensive survey. In James Kwok, editor,
  Proceedings of the Thirty-Fourth International Joint Conference on Artificial Intelligence, IJCAI-
  25, pages 10400–10408. International Joint Conferences on Artificial Intelligence Organization,
  8 2025. doi: 10.24963/ijcai.2025/1155. URL https://doi.org/10.24963/ijcai.2025/1155.
  Survey Track.

Andrew Cropper and Rolf Morel. Learning programs by learning from failures. Machine Learning,
 110(4):801–856, 2021.

João Pedro Gandarela de Souza, Danilo Carvalho, and André Freitas. Inductive learning of logical
  theories with llms: A expressivity-graded analysis. In Proceedings of the AAAI Conference on
  Artificial Intelligence, volume 39, pages 23752–23759, 2025.

Google DeepMind. Gemma 4: Lightweight open models for reasoning and agentic systems. https:
 //deepmind.google/models/gemma/gemma-4/, 2026. Accessed: 2026-04-07.

Zhibin Gou, Zhihong Shao, Yeyun Gong, yelong shen, Yujiu Yang, Nan Duan, and Weizhu Chen.
  CRITIC: Large language models can self-correct with tool-interactive critiquing. In The Twelfth
  International Conference on Learning Representations, 2024. URL https://openreview.net/
  forum?id=Sx038qxjek.


                                                11
Ryan Hsiang, William Adkisson, Robert Joseph George, and Anima Anandkumar. Leandojo-
  v2: A comprehensive library for AI-assisted theorem proving in lean. In The 5th Workshop
  on Mathematical Reasoning and AI at NeurIPS 2025, 2025. URL https://openreview.net/
  forum?id=tnx1VvrcAn.

Jie Huang, Xinyun Chen, Swaroop Mishra, Huaixiu Steven Zheng, Adams Wei Yu, Xinying Song,
  and Denny Zhou. Large language models cannot self-correct reasoning yet. In The Twelfth
  International Conference on Learning Representations, 2024. URL https://openreview.net/
  forum?id=IkmD3fKBPQ.

Tamera Lanham, Anna Chen, Ansh Radhakrishnan, Benoit Steiner, Carson Denison, Danny Her-
  nandez, Dustin Li, Esin Durmus, Evan Hubinger, Jackson Kernion, et al. Measuring faithfulness
  in chain-of-thought reasoning. arXiv preprint arXiv:2307.13702, 2023.

Hunter Lightman, Vineet Kosaraju, Yuri Burda, Harrison Edwards, Bowen Baker, Teddy Lee, Jan
 Leike, John Schulman, Ilya Sutskever, and Karl Cobbe. Let’s verify step by step. In The twelfth
 international conference on learning representations, 2023.

Qing Lyu, Shreya Havaldar, Adam Stein, Li Zhang, Delip Rao, Eric Wong, Marianna Apidianaki,
  and Chris Callison-Burch. Faithful chain-of-thought reasoning. In Proceedings of the 13th In-
  ternational Joint Conference on Natural Language Processing and the 3rd Conference of the
  Asia-Pacific Chapter of the Association for Computational Linguistics (Volume 1: Long Papers),
  pages 305–329, 2023.

Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler Hallinan, Luyu Gao, Sarah Wiegreffe, Uri
 Alon, Nouha Dziri, Shrimai Prabhumoye, Yiming Yang, et al. Self-refine: Iterative refinement
 with self-feedback. Advances in neural information processing systems, 36:46534–46594, 2023.

Meta AI. Llama 3.2: Open foundation and multimodal models. https://ai.meta.com/llama/,
 2024. Accessed: 2026-04-07.

Stephen Muggleton. Inductive logic programming. New generation computing, 8(4):295–318, 1991.

Theo Olausson, Alex Gu, Ben Lipkin, Cedegao Zhang, Armando Solar-Lezama, Joshua Tenenbaum,
 and Roger Levy. Linc: A neurosymbolic approach for logical reasoning by combining language
 models with first-order logic provers. In Proceedings of the 2023 Conference on Empirical Methods
 in Natural Language Processing, pages 5153–5176, 2023.

OpenAI. Gpt-5.4. https://openai.com/index/introducing-gpt-5-4/, 2026. Accessed: 2026-
 04-07.

Liangming Pan, Alon Albalak, Xinyi Wang, and William Wang. Logic-lm: Empowering large lan-
  guage models with symbolic solvers for faithful logical reasoning. In Findings of the Association
  for Computational Linguistics: EMNLP 2023, pages 3806–3824, 2023.

Qwen Team. Qwen3.5: Accelerating productivity with native multimodal agents, February 2026.
 URL https://qwen.ai/blog?id=qwen3.5.

Abulhair Saparov and He He. Language models are greedy reasoners: A systematic formal analysis
 of chain-of-thought. In The Eleventh International Conference on Learning Representations,
 2023. URL https://openreview.net/forum?id=qFVVBzXxR2V.



                                                12
Timo Schick, Jane Dwivedi-Yu, Roberto Dessı̀, Roberta Raileanu, Maria Lomeli, Eric Hambro, Luke
  Zettlemoyer, Nicola Cancedda, and Thomas Scialom. Toolformer: Language models can teach
  themselves to use tools. Advances in neural information processing systems, 36:68539–68551,
  2023.

Koustuv Sinha, Shagun Sodhani, Jin Dong, Joelle Pineau, and William L Hamilton. Clutrr: A
 diagnostic benchmark for inductive reasoning from text. In Proceedings of the 2019 Conference on
 Empirical Methods in Natural Language Processing and the 9th International Joint Conference
 on Natural Language Processing (EMNLP-IJCNLP), pages 4506–4515, 2019.

Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timothée
 Lacroix, Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal Azhar, et al. Llama: Open and
 efficient foundation language models. arXiv preprint arXiv:2302.13971, 2023.

Miles Turpin, Julian Michael, Ethan Perez, and Samuel Bowman. Language models don’t always
 say what they think: Unfaithful explanations in chain-of-thought prompting. Advances in Neural
 Information Processing Systems, 36:74952–74965, 2023.

Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny
  Zhou, et al. Chain-of-thought prompting elicits reasoning in large language models. Advances in
  neural information processing systems, 35:24824–24837, 2022.

Jundong Xu, Hao Fei, Liangming Pan, Qian Liu, Mong-Li Lee, and Wynne Hsu. Faithful logical
  reasoning via symbolic chain-of-thought. In Proceedings of the 62nd Annual Meeting of the
  Association for Computational Linguistics (Volume 1: Long Papers), pages 13326–13365, 2024.

Kaiyu Yang, Aidan Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing Yu, Saad Godil,
 Ryan J Prenger, and Animashree Anandkumar. Leandojo: Theorem proving with retrieval-
 augmented language models. Advances in Neural Information Processing Systems, 36:21573–
 21612, 2023.

Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik R Narasimhan, and Yuan
  Cao. React: Synergizing reasoning and acting in language models. In The eleventh international
  conference on learning representations, 2022.




                                               13
