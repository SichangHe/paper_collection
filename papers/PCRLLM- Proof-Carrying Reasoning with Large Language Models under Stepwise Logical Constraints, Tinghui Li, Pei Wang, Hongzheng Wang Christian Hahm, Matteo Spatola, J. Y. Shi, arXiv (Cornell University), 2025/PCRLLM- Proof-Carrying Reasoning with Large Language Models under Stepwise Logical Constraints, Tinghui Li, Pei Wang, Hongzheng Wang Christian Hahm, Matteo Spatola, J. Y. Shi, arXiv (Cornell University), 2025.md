                                         PCRLLM: Proof-Carrying Reasoning with Large
                                           Language Models under Stepwise Logical
                                                        Constraints

                                         Tangrui Li[0000−0003−3110−8324] , Pei Wang, Hongzheng Wang, Christian Hahm,
                                                       Matteo Spatola, and Justin Shi[0000−0003−3774−2190]
arXiv:2511.08392v1 [cs.CL] 11 Nov 2025




                                                          Temple University, Philadelphia PA 19122, USA
                                             {tuo90515,pei.wang,tuf78197,tun50806,matteo.spatola, shi}@temple.edu



                                                Abstract. Large Language Models (LLMs) often exhibit limited logical
                                                coherence, mapping premises to conclusions without adherence to ex-
                                                plicit inference rules. We propose Proof-Carrying Reasoning with LLMs
                                                (PCRLLM), a framework that constrains reasoning to single-step infer-
                                                ences while preserving natural language formulations. Each output ex-
                                                plicitly specifies premises, rules, and conclusions, thereby enabling verifi-
                                                cation against a target logic. This mechanism mitigates trustworthiness
                                                concerns by supporting chain-level validation even in black-box settings.
                                                Moreover, PCRLLM facilitates systematic multi-LLM collaboration, al-
                                                lowing intermediate steps to be compared and integrated under formal
                                                rules. Finally, we introduce a benchmark schema for generating large-
                                                scale step-level reasoning data, combining natural language expressive-
                                                ness with formal rigor.

                                                Keywords: Non-Axiomatic Logic · Formal LLM Reasoning and Evalu-
                                                ation · LLM Collaboration · LLM Reasoning Benchmark.


                                         1    Introduction

                                         The reasoning ability of large language models (LLMs) has long been a cen-
                                         tral concern, yet their answers often lack stable logical coherence. This stems
                                         from their nature as neural networks, which treat reasoning as a direct mapping
                                         from premises to conclusions according to the training data. Such mapping is
                                         not inherently problematic, but it should be constrained by logical rules and
                                         restricted to the smallest unit of inference (as single-step reasoning). Otherwise,
                                         when LLMs skip steps by leveraging semantic knowledge, we cannot tell whether
                                         they are performing valid logical short-cuts or unjustified leaps (thus losing the
                                         soundness). To this point, having LLMs simulate an existing logical system is a
                                         reasonable choice, since the rules of single-step inference are explicitly defined.
                                             Nevertheless, LLMs’ strength lies not in mechanically reproducing logic sys-
                                         tems, but in their powerful natural language processing ability. Existing ap-
                                         proaches usually emphasize only one side: either broad reasoning ability without
                                         formal soundness (e.g., CoT [17]), or strict formalism at the cost of generality
2      T. Li, P. Wang, et al.

(e.g., neural-symbolic architectures [1], domain-specific loss on formality [19]).
Our approach aims to combine the two: retaining natural language problem de-
scriptions while rephrasing them in formal logical reasoning in the output, which
is a chain reasoning consists of well-formed single steps.

    This design not only addresses the above dilemma but also brings two addi-
tional advantages. First, it produces proof-carrying outputs: the LLM’s answers
include premises, rules, conclusions, and necessary details, which allows each
single-step inference to be checked against the target logic, enabling a chain-
level grading as an automatic judgment of logical soundness. In this way, the
trustworthiness problem can be mitigated: even if the model remains a black
box, its outputs can still be validated on logical grounds.

    Secondly, it enables more systematic multi-LLM collaboration. Prior ap-
proaches mostly rely on debates or answer aggregation, which lack formal con-
straints and obscure the quality of intermediate steps. In our framework, multiple
models’ reasoning steps can be unified through logical rules, so that collabora-
tion improves not only the final result but also the transparency and consistency
of intermediate reasoning.

    Additionally, we also recognize that the complexity of long-chain reasoning
arises from the exponential growth of rule applications over shared premises,
which cannot be captured by existing corpora alone. To address this, we propose
a benchmark schema that generates large-scale training data, allowing LLMs to
better learn complex inference patterns, as well as the testing data.

    To summarize, we propose a methodology that enables LLMs to perform for-
mal reasoning while preserving natural language problem descriptions. The key
idea is to constrain reasoning to single steps so that each step can be verified
against a target logic. This yields proof-carrying outputs that allow automatic
scoring of reasoning chains and provide a new angle to address the trustwor-
thiness problem. Moreover, by expressing reasoning under formal constraints,
our approach supports systematic multi-LLM collaboration, where intermediate
steps can be compared and integrated through logical rules rather than opaque
debates. To further overcome the data scarcity of formal reasoning, we intro-
duce a benchmark schema that generates large-scale step-level training data.
Together, these contributions offer a principled path toward combining LLMs’
natural language understanding with the rigor of formal logic. All the codes and
appendix are in our GitHub repository.

    The remainder of this paper 1) reviews related work, analyzes the scope of
our approach, and 2) introduces the logical system we adopt along with its neces-
sary background. We then 3) describe our data generation strategy, evaluation of
reasoning, and multi-LLM integration, followed by 4) experiments that demon-
strate the effectiveness of our method and discuss the challenges of simulating
reasoning with LLMs.
                                                                 PCRLLM          3

2     Related Work
2.1   Approach Introducing Logic to LLMs
 – CoT and PRM
   CoT (Chain of Thought [17]) was the first approach to explicitly intro-
   duce step-by-step reasoning in LLMs. Its core idea is “reasoning granularity”:
   prompting models to generate intermediate steps and leveraging techniques
   such as self-consistency sampling or process rewards to boost performance.
   However, the underlying mechanism remains closer to semantic pattern map-
   ping than to fully formal reasoning. Even with explicit steps, the transitions
   lack the strict constraints of a logical system. As a result, while CoT improves
   performance on arithmetic and logical tasks [14], its intermediate reasoning
   often suffers from faithfulness issues [10]. PRM (Process Reward Model [9])
   shares some similarity with our approach: it evaluates reasoning steps rather
   than final answers. Yet the reasoning process remains a black box—we can
   only score or select from the outputs, not reshape them. Moreover, PRM
   makes progress by evaluating intermediate steps, but its scoring framework
   is not yet aligned with a formal logical system. As a result, it faces chal-
   lenges in achieving rigor, generality, or in supporting fully validated chains
   of evidence.
 – Reasoning with External Tools
   The key idea is that LLMs can be nudged toward normative outputs such
   as code or JSON, exemplified by approaches like PoT [2], where reasoning
   becomes explicit, step-wise, and programmatic. But these methods lever-
   age programmatic reasoning, which increases explicitness and verifiability,
   though the reliance on program structures may limit flexibility and compli-
   cate cross-model collaboration. A different line of work translates natural
   language into formal representations and delegates reasoning to external
   solvers [8][12]. This, however, faces the semantic ambiguity and uncertainty
   of natural language [7], and large-scale contexts remain difficult to fully for-
   malize.
 – Neural Symbolic Architecture
   This approach encourages neural networks to generate outputs that resemble
   formal reasoning structures, which can improve logical consistency. In many
   implementations, however, the reasoning chains are implicit and difficult
   to validate (with some exceptions [13], though readability and integration
   into feedback or collaboration remain limited). Furthermore, the underlying
   logical formalisms are currently focused on propositional or first-order logic
   [1]. Since symbolization is closely tied to natural language understanding
   (NLU), extending these methods to handle unrestricted natural language
   remains a challenging task.

2.2   LLM Collaboration
LLM collaboration aims to boost performance by combining multiple models.
Without a formal structure, however, multi-agent debates [16][4] can become
4       T. Li, P. Wang, et al.

subjective. Since natural language is the medium, evaluation often relies on se-
mantic plausibility rather than strict structural validity, which makes guarantees
of soundness challenging. Current methods typically fall into two types: 1) ex-
panding reasoning branches via sampling [16], which can be costly and may yield
intermediate steps that are difficult to verify; or 2) organizing debates among
multiple models [18] (or within the self-talk of a single model [5]), which may
improve accuracy but do not yet provide fully verifiable chains of evidence.
    While multi-agent debate has been shown to outperform single models on
many tasks [6], it remains constrained by natural language as the carrier: larger
debates may yield higher performance [11], but also make it harder to automat-
ically parse or validate intermediate reasoning. Benchmarks such as GSM8K [3]
further reinforce this tendency by evaluating only final answers rather than rea-
soning processes, thus prioritizing correctness of outcomes over explicit scrutiny
of intermediate reasoning.


3     Non-Axiomatic Logic Background

We choose Non-Axiomatic Logic (NAL) as our target logic for two main reasons.
1) NAL offers sufficient expressive ability to represent natural language contents
properly. NAL is defined hierarchically with multiple “layers” and each of them
extends the sets of grammar and inference rules of the lower layers, to increase
the expressive ability and inferential power of the system[15]. The high layers
of NAL can support substantially higher semantic complexity. In the meantime,
NAL is designed based on AIKR (Assumption of Insufficient Knowledge and
Resources) [15], which makes NAL naturally tolerant of the uncertainty and
vagueness in natural language. 2) NAL can be considered as a non-monotonic
logic. New evidence can strengthen, weaken, or overturn previous judgments
through revision. This expands the range of inferences we can draw from LLM
outputs, such as allowing different reasoning paths to yield different judgments
about the same statement. And more importantly, because of the inherent un-
certainty of natural language, judgments from different LLM can rarely share
the same truth-value. NAL can naturally accommodate such discrepancies with
its non-monotonicity when combining the outputs from multiple LLMs.


3.1   Used NAL Rules

NAL is a complex logic, developed on the basis of syllogistic reasoning and
subsequently extended with increasingly powerful expressive capabilities. These
capabilities are organized into eight levels of logic rules, with later levels building
upon the foundations of earlier ones. For example, NAL-4 introduces acquired
relations (including predicates); NAL-5 extends the system to statement-level
inference; NAL-6 enables the representation of variables; NAL-7 incorporates
temporal descriptions and NAL-8 further expands the system to perception and
interaction with the external environment.
                                                                   PCRLLM          5

    In this paper, we restrict our focus to syllogistic inference rules within first-
order NAL. To clarify the rules we employ, it is necessary to introduce the
following basic concepts:
 – Inheritance A copula in NAL, denoted as →. For a judgment s → o, it
   indicates that s is a specialization of o (equivalently, o is a generalization of
   s). A low frequency corresponds to the negation of a judgment.
 – Similarity Another copula, denoted as ↔. s ↔ o indicates that the two
   terms can be interchanged as equivalent in the current context. For example,
   if “Jack” first appears in a sentence and is later referred to as “the one,” then
   at that moment the judgment Jack ↔ the one holds true.
 – Syllogistic reasoning Since NAL is founded on sentences of the form
   “subject-term copula predicate-term” and syllogistic reasoning, the appli-
   cation of any rule requires two premises J1 , J2 , which must share a common
   term M . The other two terms are denoted as S and P .
 – Truth-value A NAL judgment is associated with a two-dimensional truth-
   value (f, c), where f represents the frequency with which a statement is
   confirmed based on accumulated evidence, and c represents the confidence,
   i.e., the stability of f . Formally, given equivalent positive evidence wp and
   equivalent negative evidence wn , we define f = wp /(wp + wn ) and c =
   (wp +wn )/(wp +wn +1). A larger evidence base makes c closer to 1, indicating
   that f is more stable and therefore more reliable for future reasoning.
 – Evidential base In NAL, truth-values are determined by evidence, but
   the system does not track the specific contribution of individual pieces of
   evidence, as evidence accumulates and changes during inference, making it
   difficult to trace independently. To prevent double counting, NAL assigns
   each input statement a unique ID. Any conclusion derived through inference
   must carry all premise IDs (to a maximum capacity), and if overlapping
   IDs are detected, the inference is disallowed. The set of accumulated IDs
   associated with a statement is referred to as its evidential base.
 – Truth functions Since NAL employs continuous truth-values, it is equipped
   with specially designed functions for calculating them. For instance, Fded is
   the truth-value function for deduction rule. Since syllogistic inference distin-
   guishes between major and minor premises, the order of the premises mat-
   ters: the truth-values of J1 and J2 are treated in sequence. When needed,
                ′
   we write Fded   to indicate the function applied after swapping the order of J1
   and J2 . Besides deduction, we also make use of other rules such as abduc-
   tion, induction, comparison, analogy, exemplification, and resemblance. For
   the precise definitions of these rules and their truth functions, please refer
   to Appendix B in [15].
    The following chart summarizes all the inference rules employed in this paper.
This work does not involve an in-depth discussion of NAL. It is sufficient to
understand only the basic inference forms required to apply these rules. The
table shows which rules can be applied to obtain different conclusions based on
different J1 and J2 . It is worth noting that NAL often uses all available rules
and thus obtains multiple conclusions for a pair of premises.
6         T. Li, P. Wang, et al.




                           Fig. 1. First-order NAL Syllogism.


4      Method
4.1     Data Construction
The data is required to have natural language input as the problem description,
and the JSON output as formal NAL inference. In data generation, we will first
create a logical structure and then convert it into a sufficiently rich natural
language description.

Logical Instance Generation We focus on two-step NAL reasoning in this
paper, as it represents the simplest form of multi-step reasoning. Due to com-
putational constraints, we restrict our experiments to this basic case; however,
we also emphasize that the proposed method has the potential to be extended
to more complex multi-step reasoning tasks when supported by more powerful
hardware and larger models.
    – Step 1: One of the nine inference rules (Fig. 1) is randomly selected to
      determine first two premises (J1, J2) used, as well as the pending conclu-
      sions. Unique terms (e.g., ID3939 ) are assigned to the placeholders S, M , P
      respectively. A random evidential base (within 3 IDs) is attached.
    – Step 2: One conclusion from Step 1 is randomly selected as a premise (J1 or
      J2), thereby fixing the position of Step 2 in the inference chart. Another in-
      dependent premise is generated in the same way. The remaining placeholder
      is assigned a unique term, and one of the possible conclusions of Step 2 is
      chosen as the final goal.
    – Distractors: To increase difficulty and emphasize the NLU ability of LLMs
      in such problems, two additional distractor premises are introduced in Step
      1, which are generated by randomly selecting a rule and assigning distinct
      unique terms with random evidential bases.
    This procedure guarantees that every generated reasoning instance is valid
and sufficiently complex. It can be extended to multi-step reasoning or to con-
sider higher levels of NAL rules to further increase complexity.
                                                                  PCRLLM          7

Natural Language Instance The natural language translation is disclosed to
LLMs thus cannot contain everything in the logic instance. It only contains:
 1. The two premises of Step 1 (without specifying J1, J2 roles).
 2. The independent premise of Step 2 (which is not derived from Step 1).
 3. The two distractor premises for Step 1.
 4. The selected conclusion of Step 2 (as the question asked to LLMs, truth
    values removed).

    In translating NAL sentences, 20 templates are prepared for the inheritance
copula, as well as the similarity copula. For example, inheritance may be rep-
resented as sub is a type of obj; similarity may be represented as sub and obj
are conceptually identical. In describing numerical truth-values, the frequency
(f ) is discretized into five categories (always false, usually false, unknown, usu-
ally true, always true), each with five natural language expressions. Note that
the confidence (c) is omitted here and replaced with the LLM’s answer-level
confidence.
    As a result, each logic instance admits up to (20×5×5)5 ×20 possible natural
language translations, ensuring a high diversity. For all templates used, please
refer to the appendix provided in our GitHub repository.

JSON Representation As the expected reponse from LLMs, the step-by-step
inference process of each logic instance is represented in JSON format with two
top-level keys, which are Step 1 and Step 2.
    In each step, there are 3 keys: Premise 1, Premise 2 and Results. In each a
NAL sentence s cp o.⟨f ; c⟩[eb]{r} is enclosed with keys: s which is the subject;
o which is the object; cp which is the copula; f which is the frequency in the
truth-value; c which is the confidence in the truth-value, here the default value
of 0.9 is used; eb which is the evidential base of the truth-value; r which is the
only applicable for sentences in the results, representing the reasoning rule used.
    This structure preserves the full reasoning process and aligns precisely with
the natural language input. The overview of the JSON structure can be found
in 2.

Prompt Construction We use the OpenAI User/Assistant format to generate
the full prompt. The overview can be found in Fig. 3.

4.2   Grading
By requiring the LLM to output in JSON format and constraining each infer-
ence step to the minimal granularity, we can systematically evaluate whether
its reasoning follows the target logical rules. Individual steps are first graded
(single-step grading), followed by an assessment of their coherence (inter-step
grading). When ground-truth specifying the correct conclusion(s) is available,
we can further evaluate whether the target outcome is achieved (ground-truth
grading).
8   T. Li, P. Wang, et al.




    Fig. 2. The JSON structure overview of the expected LLM response.




               Fig. 3. The overview of the prompt structure.
                                                                   PCRLLM          9

Single-Step Grading At the step level, we first parse the LLM’s JSON output
to extract Premise 1, Premise 2, and Results. If parsing fails, the minimum grade
(0.1) is given (to retain gradient utility in reinforcement learning, if applicable).
Otherwise, we employ the same reasoning engine used in data construction to
generate all possible conclusions and identify the closest match to the LLM’s
output through bipartite matching.
    When calculating the matching grade, for categorical indicators (s, o, cp, eb,
r), exact matches receive full credit (5 points), otherwise no credit (0 points).
For numerical indicators (f , c), which are central to evaluating whether the LLM
follows the target logic rules, grading depends on the difference from the refer-
ence value: a difference ≤ 0.05 is considered negligible and receives full credit
(25 points); a difference ≥ 0.2 indicates category-level mistakes (since we have
5 categories defined) and receives 0 points. For intermediate cases, we apply the
function (0.1+0.9×(1−(dif f −0.05)/0.15))2 ×25. In which the squaring empha-
sizes penalties for larger deviations, while the 0.1 floor preserves gradient signal
(for reinforcement learning). This design ensures smooth penalization within the
tolerance range.
    The final single-step grade is defined as the proportion of received points over
the maximum possible score. This formulation also supports future extensions
where a single step may yield multiple conclusions. In the following discussions,
we will use the same way on matching different sentences and grade on them.


Inter-Step Grading In multi-step reasoning, each step should build upon
premises from the problem description or conclusions derived from previous
steps. However, since we emphasis the NLU aspect for LLM to understand the
problem and rephrase it into logic sentences, it is difficult to trace the exact
origin of each premise. Therefore, we evaluate LLM outputs by analyzing their
internal chain structure.
    In this work, we focus on two-step reasoning tasks, where the conclusion of the
first step serves as a premise in the second step, the analysis is straightforward.
The same matching and grading strategy is applied on the first-step conclusion
and all second-step premises.


Ground-Truth Grading When ground-truth labels are available, we can addi-
tionally assess whether the question is correctly answered. Specifically, the same
matching and grading strategy is applied on the conclusion of the second and
the label answer, considering all indicators (s, o, cp, f , c, eb, r).


Overall Evaluation The multiplication of the step-wise and inter-step grades
define the formal conformity grade, which is standalone evaluation on whether
the LLM adheres to the target logic without relying on labels. In scenarios
when multiple candidate outputs are available, this grade can be used for prim-
ing structurally coherent answers (soundness). This endows the LLM with a
10     T. Li, P. Wang, et al.

content-agnostic evaluation framework, so when considering answers from mul-
tiple LLMs, there is no longer a need for human inspections or for using debate
among LLMs.
    In testing, the formal conformity grade can further be multiplied with the
ground-truth grade, yielding a comprehensive measure of whether the LLM is
both logically consistent and successful in completing the reasoning task.

4.3   Response combination
Imagine a network of multiple LLMs where the same question may receive differ-
ent answers from different models. Because their training data are highly diverse,
their performance on specific problems often varies. Nevertheless, by leveraging
the structured answering scheme and the previously introduced measure of log-
ical and structural rigor, we can effectively integrate these answers.
    Specifically, when different models generate reasoning steps with identical
content (i.e., the same premises and conclusions), one can simply select the
answer with the higher degree of formality (given whether the reasoning process
provided by LLM is consistent with the target logic). When the contents diverge,
single-step reasoning from different models can be combined into a new reasoning
chain, thereby yielding a new answer. For example, in the two-step reasoning
scenario that this paper focuses on, such composition is straightforward: the
final answer can be constructed by pairing the first-step reasoning from one model
with the second-step reasoning from another. In this case, the high-quality single
steps can be picked out individually and then combined. For reasoning tasks
requiring more reasoning steps, however, additional mechanisms are needed to
avoid combinatorial explosion. A practical strategy is to filter out unreliable
intermediate steps using formality scores, thereby reducing the scale of potential
combinations.

5     Experiment
To evaluate our approach, we construct a network of three LLMs that solve the
same task while intentionally differing in capability. The differences are induced
by fine-tuning three clones of the same pretrained backbone on disjoint data
subsets. Specifically, we generate two-step NAL first-order inference instances
under different rules. As shown in Fig. 1, there are nine rule-usage patterns. We
randomly partition them into three non-overlapping subsets and fine-tune each
model on one subset.
    All models are fine-tuned on 100 examples, which is relatively small
dataset to show the feasibility of the work on more complicated backbones. Since
larger models typically require more optimization steps to converge, we adjust
the number of epochs instead of increasing data size, as follows: Qwen 2.5/0.5B
with 1 epoch, Qwen 2.5/1.5B with 2 epochs, Qwen 2.5/3B with 4 epochs.
    Even with more epochs, larger models often produce minor yet fatal format-
ting errors in their JSON outputs (e.g., unclosed brackets). We therefore apply
DeepSeek R1 [5] as a post-processor to repair broken JSON strings.
                                                                   PCRLLM         11

    Although the models are tuned with different data, all three are evaluated on
the same test set of 100 examples that uniformly covers all rules. This design
is deliberate: 1) no single model is sufficient, and 2) it enables us to study the
performance of priming and step-wise recomposition of intermediate reasoning
steps against single-model baselines.


Priming Strategies We consider five priming strategies for using this network
of LLMs to obtain the final answer:

 – Single model, no priming (m1 , m2 , m3 ): use the single answer from
   model 1, 2, 3 as the final output.
 – Priming on 3 base models (model best-3, mb3 ): with light priming,
   select the highest-scoring answer among the three models as the final output.
 – Step-wise recomposition (model best-9, mb9 ): decompose each model’s
   answer into steps and recombine them across models to synthesize a new
   answer (3 first-step possibilities × 3 second-step possibilities).


Scoring and Curves After priming, we evaluate each answer against the la-
bel using a grading method. Given a threshold, an answer is classified as valid
or invalid. The curve reports the ratio of valid answers over the 100 testing
cases. To be comprehensive, we sweep the threshold from 0.1 to 0.9 to show the
performance of the LLM network under increasingly strict conditions.




Fig. 4. Ratio of valid answers under five priming strategies. Model: Qwen2.5–0.5B;
fine-tuned for 1 epoch. Training set: 100 instances (seed = 39). Dashed curves denote
JSON-repaired results.
12      T. Li, P. Wang, et al.

Experiment on Qwen2.5–0.5B Figure 4 shows a monotonic decrease across
all curves, which is expected: stricter thresholds yield lower valid-answer ratios.
Among the three base models, m3 performs best; however, it is still inferior to
mb3 , indicating the effectiveness of priming in our setting. Moreover, mb9 further
improves over m3 , highlighting the additional benefit of step-wise recomposition.
    The dashed curves are close to the solid ones, meaning the JSON-repair step
(DeepSeek-R1 [5]) has limited impact here. This suggests that small-data fine-
tuning is already sufficient for the 0.5B model to produce mostly well-formatted
outputs.
    One potentially confusing point is why the valid-answer ratio of m3 does not
match that of mb3 , even though mb3 selects the best answer among the three
base outputs. This is because mb3 is computed by choosing the per-example
best answer before applying the threshold, whereas m3 reflects a single model’s
distribution of scores; as a result, their averages need not coincide.


Experiment on Qwen2.5–1.5B Compared with the 0.5B results, Figure 5 ex-
hibits similar trends, with smoother curves attributable to the larger backbone.
However, the dashed curves are more separated from the solid ones, underscor-
ing the increased difficulty of enforcing correct output formatting as model size
grows.
   Note that within each model-size experiment, all three base models are eval-
uated on the same test set. Across different model-size experiments (0.5B, 1.5B,
3B), the test sets may differ.




Fig. 5. Ratio of valid answers under five priming strategies. Model: Qwen2.5–1.5B;
fine-tuned for 2 epochs. Training set: 100 instances (seed = 39). Dashed curves denote
JSON-repaired results.
                                                                   PCRLLM          13

Experiment on Qwen2.5–3B In Figure 6, the dashed curve is clearly sepa-
rated from the solid ones, further illustrating the challenge of maintaining strict
formatting at larger scales. Meanwhile, the performance gap between mb3 and
mb9 narrows. A plausible explanation is that the two-step task is relatively easy
for the 3B model, so individual model outputs are already strong, leaving less
headroom for recomposition gains.




Fig. 6. Ratio of valid answers under five priming strategies. Model: Qwen2.5–3B; fine-
tuned for 4 epochs. Training set: 100 instances (seed = 39). Dashed curves denote
JSON-repaired results.




5.1   Comparison

When plotting the best-performing curves (JSON-repaired mb9 ) across param-
eter scales in Figure 7, we observe a clear improvement with model size. Nev-
ertheless, even on this relatively simple two-step task, many settings still fail to
exceed a valid-answer ratio of 0.2 under relatively loose thresholds, indicating
substantial room for progress in faithfully simulating the target logic.


6     Conclusion

We proposed PCRLLM, which combines the expressive power of natural lan-
guage with the rigor of formal inference rules, enabling transparent, verifiable,
and collaborative reasoning with LLMs while addressing issues of trustworthiness
and data scarcity.
   Although this work is able to scale to more complex multi-step situations,
two open issues remain for future exploration. First, since we rely on the NLU
14      T. Li, P. Wang, et al.




Fig. 7. Comparison of the mb9 valid-answer ratios across models with different param-
eter counts (JSON-repaired).



ability of LLMs, we cannot attribute which premises originate from which prob-
lem description; consequently, hallucination may still occur. While our method
makes these premises transparent and allows users to accept or reject them, this
workflow requires manual intervention and is therefore inconvenient.
    Second, when extending to multi-step reasoning and recomposing answers
from single steps, the search space grows exponentially with the depth of the
NAL extensions and the number of reasoning steps, leading to a combinato-
rial explosion. Although our scoring scheme prunes many low-quality sub-steps
and reduces fruitless search, it does not fundamentally resolve this complexity
bottleneck.
    Future work will focus on automating premise attribution and developing
more efficient search strategies, with the aim of advancing scalable and trust-
worthy reasoning in LLMs.


References

 1. Besold, T.R., Bader, S., Bowman, H., Domingos, P., Hitzler, P., Kühnberger, K.U.,
    Lamb, L.C., Lima, P.M.V., de Penning, L., Pinkas, G., et al.: Neural-symbolic
    learning and reasoning: A survey and interpretation. In: Neuro-symbolic artificial
    intelligence: The state of the art, pp. 1–51. IOS press (2021)
 2. Chen, W., Ma, X., Wang, X., Cohen, W.W.: Program of thoughts prompting:
    Disentangling computation from reasoning for numerical reasoning tasks (2023),
    https://arxiv.org/abs/2211.12588
 3. Cobbe, K., Kosaraju, V., Bavarian, M., Chen, M., Jun, H., Kaiser, L., Plappert,
    M., Tworek, J., Hilton, J., Nakano, R., Hesse, C., Schulman, J.: Training verifiers
    to solve math word problems (2021), https://arxiv.org/abs/2110.14168
                                                                       PCRLLM          15

 4. Du, Y., Li, S., Torralba, A., Tenenbaum, J.B., Mordatch, I.: Improving factuality
    and reasoning in language models through multiagent debate (2023), https://arxiv.
    org/abs/2305.14325
 5. Guo, D., Yang, D., Zhang, H., Song, J., Zhang, R., Xu, R., Zhu, Q., Ma, S.,
    Wang, P., Bi, X., et al.: Deepseek-r1: Incentivizing reasoning capability in llms via
    reinforcement learning (2025), https://arxiv.org/abs/2501.12948
 6. Hegazy, M.: Diversity of thought elicits stronger reasoning capabilities in multi-
    agent debate frameworks (2025), https://arxiv.org/abs/2410.12853
 7. Li, Q., Li, J., Liu, Z., Cheng, M., Zeng, Y., Liu, Q., Liu, T.: Are llms reliable
    translators of logical reasoning across lexically diversified contexts? (2025), https:
    //arxiv.org/abs/2506.04575
 8. Lin, F., Shou, Z., Chen, C.: Using language models for knowledge acquisition in
    natural language reasoning problems (2023), https://arxiv.org/abs/2304.01771
 9. Ma, Q., Zhou, H., Liu, T., Yuan, J., Liu, P., You, Y., Yang, H.: Let’s reward step
    by step: Step-level reward model as the navigators for reasoning (2023), https:
    //arxiv.org/abs/2310.10080
10. Manuvinakurike, R., Moss, E., Watkins, E.A., Sahay, S., Raffa, G., Nachman,
    L.: Thoughts without thinking: Reconsidering the explanatory value of chain-of-
    thought reasoning in llms through agentic pipelines (2025), https://arxiv.org/abs/
    2505.00875
11. Pan, J., Zhang, J., Wang, X., Yuan, L., Peng, H., Suhr, A.: Tinyzero (2025),
    https://github.com/Jiayi-Pan/TinyZero, accessed: 2025-01-24
12. Qin, B., Hui, B., Wang, L., Yang, M., Li, J., Li, B., Geng, R., Cao, R., Sun, J.,
    Si, L., Huang, F., Li, Y.: A survey on text-to-sql parsing: Concepts, methods, and
    future directions (2022), https://arxiv.org/abs/2208.13629
13. Rocktäschel, T., Riedel, S.: End-to-end differentiable proving. In: Guyon, I.,
    Luxburg, U.V., Bengio, S., Wallach, H., Fergus, R., Vishwanathan, S., Garnett,
    R. (eds.) Advances in Neural Information Processing Systems. vol. 30. Curran As-
    sociates, Inc. (2017), https://proceedings.neurips.cc/paper_files/paper/2017/file/
    b2ab001909a8a6f04b51920306046ce5-Paper.pdf
14. Sprague, Z., Yin, F., Rodriguez, J.D., Jiang, D., Wadhwa, M., Singhal, P., Zhao,
    X., Ye, X., Mahowald, K., Durrett, G.: To cot or not to cot? chain-of-thought helps
    mainly on math and symbolic reasoning (2025), https://arxiv.org/abs/2409.12183
15. Wang, P.: Non-axiomatic logic: A model of intelligent reasoning. World Scientific
    (2013)
16. Wang, X., Wei, J., Schuurmans, D., Le, Q., Chi, E., Narang, S., Chowdhery, A.,
    Zhou, D.: Self-consistency improves chain of thought reasoning in language models
    (2023), https://arxiv.org/abs/2203.11171
17. Wei, J., Wang, X., Schuurmans, D., Bosma, M., Xia, F., Chi, E., Le, Q.V., Zhou,
    D., et al.: Chain-of-thought prompting elicits reasoning in large language models.
    Advances in neural information processing systems 35, 24824–24837 (2022)
18. Zheng, L., Chiang, W.L., Sheng, Y., Zhuang, S., Wu, Z., Zhuang, Y., Lin,
    Z., Li, Z., Li, D., Xing, E., Zhang, H., Gonzalez, J.E., Stoica, I.: Judging
    llm-as-a-judge with mt-bench and chatbot arena. In: Oh, A., Naumann, T.,
    Globerson, A., Saenko, K., Hardt, M., Levine, S. (eds.) Advances in Neu-
    ral Information Processing Systems. vol. 36, pp. 46595–46623. Curran Asso-
    ciates, Inc. (2023), https://proceedings.neurips.cc/paper_files/paper/2023/file/
    91f18a1287b398d378ef22505bf41832-Paper-Datasets_and_Benchmarks.pdf
19. Zhou, Z., Kearnes, S., Li, L., Zare, R.N., Riley, P.: Optimization of molecules via
    deep reinforcement learning. Scientific Reports 9(1) (Jul 2019). https://doi.org/
    10.1038/s41598-019-47148-x
