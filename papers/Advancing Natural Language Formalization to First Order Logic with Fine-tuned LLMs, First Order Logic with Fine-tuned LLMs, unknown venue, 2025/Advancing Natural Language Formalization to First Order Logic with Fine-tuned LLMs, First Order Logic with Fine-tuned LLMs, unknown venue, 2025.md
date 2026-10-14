                                             Advancing Natural Language Formalization to
                                               First Order Logic with Fine-tuned LLMs

                                          Felix Vossel1[0009−0005−2367−9022] , Till Mossakowski1[0000−0002−8938−5204] , and
                                                                Björn Gehrke1,2[0009−0007−7488−0257]

                                                                  Osnabrück University, Germany
                                                                  1

                                                      {fvossel, till.mossakowski, bjoern.gehrke}@uos.de
arXiv:2509.22338v2 [cs.CL] 30 Nov 2025




                                                               2
                                                                 University of Zurich, Switzerland



                                               Abstract. Automating the translation of natural language to first-order
                                               logic (FOL) is crucial for knowledge representation and formal meth-
                                               ods, yet remains challenging. We present a systematic evaluation of fine-
                                               tuned LLMs for this task, comparing architectures (encoder-decoder vs.
                                               decoder-only) and training strategies. Using the MALLS and Willow
                                               datasets, we explore techniques like vocabulary extension, predicate con-
                                               ditioning, and multilingual training, introducing metrics for exact match,
                                               logical equivalence, and predicate alignment. Our fine-tuned Flan-T5-
                                               XXL achieves 70% accuracy with predicate lists, outperforming GPT-4o
                                               and even the DeepSeek-R1-0528 model with CoT reasoning ability as
                                               well as symbolic systems like ccg2lambda. Key findings show: (1) pred-
                                               icate availability boosts performance by 15-20%, (2) T5 models surpass
                                               larger decoder-only LLMs, and (3) models generalize to unseen logical
                                               arguments (FOLIO dataset) without specific training. While structural
                                               logic translation proves robust, predicate extraction emerges as the main
                                               bottleneck.

                                               Keywords: First Order Logic · Fine-tuning · Formalisation · LLM ·
                                               Natural Language Processing.


                                         1    Introduction

                                         Both knowledge representation and formal specification essentially depend on
                                         formalisation of knowledge as logical theories. The formalisation process is often
                                         a bottleneck, because high-quality formalisation requires manual human effort.
                                         As a result, in many ontologies, annotations in natural language are often much
                                         richer than the formalised logical theory. Likewise, informal requirement speci-
                                         fications in natural language are often much more extensive than formal specifi-
                                         cations. This leads to a limitation of usefulness of formal methods like theorem
                                         proving, model finding and model checking, because the involved logical theory
                                         is often incomplete and only partially captures the informal natural language
                                         specification.
                                             In order to address this problem, we aim to automate the translation from
                                         natural language to formal logic, more specifically, to first-order logic. While
2      F. Vossel et al.

this problem has been solved to a certain extent by different methods, we aim at
improving the quality of existing automated translation methods. Our approach
uses large language models, which are fine-tuned and evaluated for this specific
task, while being simultanesously available as general-purpose LLMs.


2   Related Work

Natural Language to First-Order Logic Translation Translating NL to FOL can
be used to enable logical reasoning with natural language. Early approaches to
this problem relied mainly on symbolic methods. They used rule-based systems
with hand-crafted linguistic rules and syntactic patterns, maping natural lan-
guage structures directly to logical expressions. Pease and Murray developed
an early translator from controlled English to logic for ontology-based knowl-
edge representation [25]. Bos and Markert explored logical inference techniques
for recognizing textual entailment [2]. They used model building from auto-
mated reasoning to approximate entailment relationships. Other systems often
utilize frameworks like Combinatory Categorial Grammar (CCG) to build com-
positional semantic representations which can then be transformed to lambda
expressions, FOL, or other formal languages. For example, ccg2lambda is a com-
positional semantics system generating logical semantic representations by com-
bining semantic formulas bottom-up, guided by CCG parse trees [19].
    Barker-Plummer et al. systematically analysed the difficulties of students
during a translation task. They identified, among other, the ambiguity of natural
language, complex sentence structures, and uninformative automated feedback
as the students key challenges in mapping natural language to formal logic [1].
Cai and Yates addressed the identified scalability by developing techniques for
large-scale semantic parsing [4]. They used schema matching and lexicon ex-
tension to improve performance on database-grounded tasks. Martínez-Gómez
et al. further refined compositional semantics with the ccg2lambda system [19].
This system produces logical semantic representations by composing formulas
bottom-up from CCG parse trees.
    More recently, researchers have explored methods beyond purely symbolic
systems. Lu et al. demonstrated the use of Dual Reinforcement Learning (DRL)
to translate NL to both Propositional and First-Order Logic [18].
    The emergence of large language models (LLMs) offered a new potential
solution. However, LLMs often struggle with complex logical reasoning. Several
recent works approach this limitations in different ways.
    LogicLLaMA, a LLaMA-7B model fine-tuned specifically for NL-FOL trans-
lation, achieved performance comparable to GPT-4, but at a much lower compu-
tational cost [30]. During their work they created the dataset MALLS, a dataset
of 34K high-quality NL-FOL pairs generated using GPT-4. Other frameworks
combine LLMs with symbolic reasoners. For example, LogicLM first translates
NL to FOL using LLMs and then applies symbolic reasoning [24]. Experiments
showed this combination performed better than using the LLM directly for rea-
soning. Building on top of that, Lalwani et al. presented NL2FOL [12], a frame-
                          Natural Language to First Order Logic with LLMs          3

work to translate NL to FOL in multiple steps with few-shot prompting of an
LLM. It is designed to detect logical fallacies in natural language statements.
    Thatikonda et al. focused on fine-tuning LLMs for NL to FOL translation
[29]. They explored various fine-tuning strategies and data augmentation tech-
niques. Their results show that fine-tuning significantly improves performance
compared to zero-shot settings. They also found that incrementally translating
premises and conclusions of (natural language) logical arguments can improve
logical inference checking.

Evaluation Metrics For the evaluation of NL to FOL translation tasks, various
metrics are used in the literature. A common method is an exact, character-by-
character match to evaluate whether a prediction of a model is correct [14,18].
However, this metric is very strict as it does not account for syntactic variations
in FOL expressions which do not change the underlying semantics.
    Other approaches use logical equivalence as a more robust metric. Using
automated theorem provers this metric checks whether the predicted FOL ex-
pression is logically equivalent to the ground truth expression, even if they are
syntactically different [3,10]. However, this approach either requires static sig-
natures ensuring that the same predicates are used in both expressions or a
normalization step to align predicate names. Experiments which include NL to
FOL translation only as a subtask of logical entailment use the accuracy of the
entailment task as a metric [29,12].
    Yang et al. defined a new metric called “Logical Equivalence” which is also
used in other experiments [30,16]. In contrast to the previous methods, which
rate a prediction either “correct” or “incorrect”, this metric assigns a score based
on the number of matching propositional valuations. However, it is questionable
whether this metric is suitable for FOL, as it does not account for the complexity
of quantifiers and a prediction which differs in only one valuation can still be
worse than a prediction which differs in many valuations. For example, A ∧ B ∧
                                                                            3
C ∧ D is closer to A ∧ B than to false, but differs from the former for 16     of the
                                       1
valuations, but from latter only for 16 .


3     Methodology
3.1   Model Selection
For our formalization task, we employ both encoder-decoder and decoder-only
large language models (LLMs) with different sizes to enable a systematic com-
parison across architectures and model sizes. Encoder-decoder models, such as
T5-base [26], T5-3B [26], and Flan-T5-XXL [5], are chosen based on their suc-
cessful application to structured prediction tasks like text-to-text translation
and semantic parsing [15], which parallel the formality and compositionality of
natural language to logic translation. For the decoder-only setting, we fine-tune
LLaMA3.1-8B [9], which is widely used in recent research on fine tuning LLMs
for formal language and reasoning tasks [30], as well as Mistral-24B, recognized
for its strong performance and efficiency [20]. Additionally, we include Olmo-32B
4      F. Vossel et al.

[22] as a representative of modern open-source approaches in large-scale language
modeling.
    This selection enables an analysis of architectural influences while spanning a
diverse range of parameter sizes and recent model families. Table 1 summarizes
the models considered in our experiments.


             Model          Architecture Parameters Reference
            T5-base       Encoder-Decoder       220M          [26]
            T5-3B         Encoder-Decoder        3B           [26]
            Flan-T5-XXL Encoder-Decoder          11B           [5]
            Olmo-32B        Decoder-Only         32B          [22]
            Mistral-24B     Decoder-Only         24B          [20]
            LLaMA3.1-8B Decoder-Only              8B           [9]
      Table 1. Large language models used for fine-tuning in our experiments.




3.2   Datasets

For our experiments, we leverage two of the largest publicly available Natural
Language to First-Order Logic (NL-FOL) datasets: MALLS [30] and Willow [8].
These datasets were selected because their considerable size makes them more
suitable for training large models than, for instance, FOLIO [10], and they con-
tain significantly more complex natural language utterances compared to simpler
resources such as Text2Log [14].
    Each instance in both datasets consists of a natural language string paired
with its corresponding FOL string. To ensure consistency and facilitate model
training, we store the combined corpus in a unified json format, where each
record contains both fields. For example:

              "NL": "Not every student is hardworking."
              "FOL": "¬∀x (Student(x) → Hardworking(x))"



3.3   Fine-tuning Procedure

To adapt the selected pre-trained language models to the NL-to-FOL formal-
ization task, we fine-tune each model on the combined training split described
above. For the decoder-only models (LLaMA3.1-8B, Mistral-24B, and Olmo-
32B), we apply Low-Rank Adaptation (LoRA) [11] with rank r = 16, scaling
factor α = 32, a dropout rate of 0.05, and targeting all attention and feed-forward
projection layers, following recommended settings for large-scale language mod-
eling [11]. For Flan-T5-XXL, LoRA was analogously applied to attention and
feed-forward layers. T5-base and T5-3B were trained with full fine-tuning. In all
LoRa settings mixed precision training was enabled.
                         Natural Language to First Order Logic with LLMs         5


Property                       Value Description
Total examples                 49950 NL→FOL pairs in dataset
Training examples              35964 Size of train set
Validation examples             3996 Size of validation set
Test examples                   9990 Size of test set
Unique predicates              62981 Distinct predicates occurring in FOL
Unique constants                2011 Distinct constants (entities/objects) in FOL
Avg. NL length (chars)         86.73 Mean input (NL) string length [characters]
Avg. FOL length (chars)        85.02 Mean FOL string length [characters]
Avg. quantifiers per sample     1.56 Mean number of quantifiers per FOL entry
Avg. formula depth per sample 6.75 Mean parse tree depth per FOL formula
Avg. logical connectives/sample 3.68 Mean number of logical connectives (∧, ∨, ¬, →)
           Table 2. Summary statistics for our unified NL-FOL dataset.




    All models were trained with the AdamW optimizer [17], a maximum of 12
epochs, early stopping (patience 4) based on validation loss, and cosine (Decoder-
Only models)/linear (T5 models) learning rate scheduling with a warmup ratio
of 0.05 and weight decay of 0.01. Batch sizes and learning rates are detailed in
Table 3. Multi-GPU training was used for larger models as required.
    All experiments were conducted on a high-performance computing cluster
equipped with Intel® Xeon® Platinum 8480+ CPUs and either NVIDIA H100
80GB or NVIDIA A100-SXM4-80GB GPUs. The cluster and computational re-
sources were funded by the Deutsche Forschungsgemeinschaft (DFG, German
Research Foundation) – 456666331.
    Except for T5-base and T5-3B (trained in float32), all models were fine-
tuned using bfloat16 precision. Distributed training was performed using the
NCCL backend with unused parameter detection disabled. All experiments lever-
aged the HuggingFace transformers, peft, and trl libraries.
    Table 3 summarizes the main training hyperparameters and hardware used
for each model.


Model           Arch.   LoRA F-FT Batch Size         LR        Max Epochs GPUs
 T5-base         Enc-Dec    –     ✓       8      1 × 10   −3
                                                                12           1
 T5-3B           Enc-Dec    –     ✓        8     1 × 10−4       12           1
 Flan-T5-XXL Enc-Dec        ✓     –        8     1 × 10−4       12           1
 LLaMA3.1-8B Dec-Only ✓           –       16     1 × 10−5       12           1
 Mistral-24B Dec-Only ✓           –       32     1 × 10−5       12           2
 Olmo-32B       Dec-Only ✓        –       32     1 × 10−5       12           2
Table 3. Training hyperparameters and hardware for model fine-tuning. LR denotes
learning rate; LoRA indicates Low-Rank Adaptation; F-FT denotes full fine-tuning.
6       F. Vossel et al.

3.4   Experiment Details

We design a sequence of eight experiments to systematically analyze the impact
of different fine-tuning strategies, data augmentations, and evaluation settings
on the NL-to-FOL formalization task. Each experiment builds on the findings
and methodology of the previous ones, allowing us to isolate and compare the
effects of key choices in model adaptation.

1. Standard fine-tuning We fine-tune all models on pairs of natural language
statements and their corresponding FOL expressions in a standard sequence-to-
sequence or causal language modeling setting. For decoder-only and chat-based
transformer models, we use a ChatML-style prompt structure: each instance is
formatted into system, user, and assistant messages, with the system prompt in-
structing the model to output only the FOL formula (using the set ∀, ∃, ¬, ∧, ∨, →
, ↔, ⊕) and to begin with “Φ =”. For encoder–decoder (T5) models, we use a
simple input–output format, prepending the source with "translate English
natural language statements into first-order logic (FOL): " and set-
ting the target to the corresponding FOL expression. Since T5 models rely on
the SentencePiece tokenizer, they are unable to generate logical operator sym-
bols by default. Consequently, all logical operators were substituted with their
respective textual forms. The prompt templates are automatically converted to
match the input requirements of each model architecture. This baseline serves
as our primary reference point for all subsequent augmentations and curriculum
strategies.
    After fine-tuning, we save the resulting model and evaluate its performance on
the test set. For decoder-only models, text generation is performed with sampling
enabled and a maximum of 250 new tokens; all other generation parameters are
left at their default values. For T5 models, we use beam search with five beams,
a maximum output length of 256 tokens, a length penalty of 2.0, and early
stopping disabled; the remaining settings follow the respective model defaults.

2. Token extension. In this experiment, we augment the model’s vocabulary
with dedicated tokens for all logical connectives and quantifiers used in First-
Order Logic (∀, ∃, ¬, ∧, ∨, →, ↔, ⊕). Each special symbol is represented as a
unique token in the tokenizer and the model’s embedding matrix, ensuring they
are treated as atomic units during both input encoding and output generation.
This direct symbolic mapping facilitates the handling of logical structure and
reduces token fragmentation of FOL expressions.
    A key motivation for this experiment stems from the observation that models
like T5, which rely on the SentencePiece tokenizer, cannot represent such sym-
bols by default. In the baseline scenario, logical operators had to be replaced with
textual tokens (e.g., “forall” instead of “∀”), which may introduce ambiguity or
inefficiency. By explicitly extending the vocabulary with the required logic sym-
bols, we aim to assess the impact of direct symbolic encoding on formalization
accuracy and model performance. Training and evaluation procedures otherwise
mirror those of the baseline.
                         Natural Language to First Order Logic with LLMs         7

3. Fixed predicate list. In this experiment, for each NL–FOL pair in the dataset,
the model receives an explicit, alphabetically sorted list of predicates that must
appear in the FOL formalization, encouraging precise and consistent predicate
usage. The list is sorted to ensure that the order of predicates does not reveal
information about the logical structure of the FOL expression. This experimental
setup is motivated by initial evaluation results, which indicated that one of the
main challenges for large language models is correctly identifying the relevant
predicates from the input. To test the hypothesis that predicate selection poses
a greater difficulty than generating the correct logical structure, we provide the
gold predicate list as an additional input to the model. A more detailed analysis
of this issue is presented in our evaluation metrics section.

4. Fixed predicate list with noise. In this experiment, for each NL–FOL pair in
the dataset, the model receives an explicit, alphabetically sorted list of pred-
icates that must appear in the FOL formalization, but this list is augmented
with additional randomly sampled predicates drawn from the predicates used in
five other FOL formulas. This setup requires the model to robustly distinguish
the relevant predicates among distractors when constructing the FOL expres-
sion. Such a scenario is also of practical importance, as in many downstream
applications one may only be able to provide a superset of potentially relevant
predicates, rather than the exact set needed for a particular formalization.

5. Two-step fine-tuning. Building on the practical consideration that gold pred-
icate lists are rarely available in real-world scenarios, we design a two-step cur-
riculum: In the first step, models are trained to extract the relevant predicates
from the natural language input, producing a predicted predicate list. In the
second step, this predicted list is provided as input to the model trained in Ex-
periment 3 (fixed predicate list) for FOL formalization. This approach allows
us to investigate whether intermediate predicate prediction can facilitate more
accurate and robust logic translation when compared to direct end-to-end train-
ing.

6. Three-step curriculum fine-tuning. As an alternative to the two-step fine-
tuning in Experiment 5, we address the predicate prediction challenge through
a curriculum learning scheme with three stages. In the first stage, models are
trained with the exact predicate list provided as input (as in Experiment 3).
In the second stage, the input predicate list is augmented with noisy distrac-
tors (as in Experiment 4), increasing task difficulty. Finally, models are trained
on the standard NL–FOL formalization task without any predicate hints. This
progressive training approach is designed to gradually reduce the model’s re-
liance on explicit predicate information, with the goal of improving its ability to
correctly identify predicates and generate FOL expressions in a more realistic,
unprompted setting.

7. Multilingual fine-tuning. In this experiment, we explore a fundamentally dif-
ferent approach to improving predicate understanding and generalization by
8      F. Vossel et al.

leveraging multilingual training data. Specifically, we use the Mistral model and
translate all natural language statements in the training set into German and
French, two languages that are frequently covered in LLM pretraining alongside
English. The corresponding FOL predicates, however, remain in English, serving
as a consistent formal target language. Training follows the same procedure as
in Experiment 1, but now includes NL–FOL pairs in three languages, while val-
idation and test sets remain in the original English. This setting encourages the
model to capture the semantic meaning of predicates independently of source
language syntax, since predicates can no longer be directly mapped from the NL
input. Our goal is to evaluate the cross-lingual robustness of logical formaliza-
tion and to test whether multilingual exposure improves predicate abstraction
and transfer.

8. Comparison to Other Approaches While previous experiments evaluated the
performance of our models either internally or in comparison to other neu-
ral methods following the same approach, this section extends the analysis by
comparing LLaMA3.1-8B to LLaMA-2 13B [29] and the symbolic system
ccg2lambda. For the comparison with LLaMA-2 13B, we use the eval subset
of the FOLIO dataset, noticing that our model has not been trained on FOLIO.
For the evaluation against ccg2lambda, we preprocessed the natural language
inputs by removing all commas and appending a period to each sentence, in
accordance with the input format expected by the tool.
    Each experiment is designed to isolate a specific methodological or represen-
tational variable, enabling a systematic analysis of model capabilities and the
underlying task. In the following, we present the detailed setup and training
procedure for each experiment; results and discussion are provided in the results
Section.

3.5   Evaluation
With all models and experimental variants in place, we systematically assess per-
formance using three complementary metrics and robust baseline comparisons.

1. Exact match. Exact match evaluates whether the predicted and ground truth
FOL expressions are identical under whitespace-insensitive string comparison,
thereby abstracting away from superficial formatting differences.

2. Logical equivalence. To account for syntactically different but semantically
equivalent expressions, we determine logical equivalence using an automated
theorem proving (ATP) approach. Both predicted and ground truth FOL ex-
pressions are parsed using a context-free grammar that we specifically designed
and implemented with the Lark parsing library [27]. The resulting syntax trees
are then transformed into Z3 format. To check for logical equivalence, we con-
struct a Z3 solver [21] to test the unsatisfiability of the negated bi-implication
¬(φ ↔ ψ), where φ denotes the model output and ψ the ground truth formula.
We use the Z3 solver with a timeout of 10 seconds for each check. If the solver
                         Natural Language to First Order Logic with LLMs        9

establishes unsatisfiability within this timeframe, the formulas are considered
logically equivalent. Our approach follows the general structure proposed by [3].


3. Predicate matching. To further disentangle errors caused by incorrect predi-
cate naming from structural or logical errors, we introduce a predicate matching
step. For each predicted FOL expression, predicates are mapped to ground truth
predicates using the normalized Levenshtein distance (threshold 0.6) [13]. Once
predicates are aligned, both exact match and logical equivalence are recom-
puted on the normalized formulas. This procedure provides additional insight
into whether errors are due to predicate identification or deeper logical misun-
derstandings.


Baseline comparisons. For Experiment 1, we first establish a baseline by eval-
uating each model on the dataset without any fine-tuning, in order to verify
that fine-tuning indeed improves performance. We further compare the fine-
tuned models to strong proprietary, open-source and reasoning models—namely,
GPT-4o [23], DeepSeek-R1-0528 [7] with a hybrid 2500 tokens CoT setting,
DeepSeek-V3-0324 [6] and LogicLLaMA [30]—for an additional performance
reference. Notably, LogicLLaMA was trained on the MALLS dataset but not
on Willow, providing an informative benchmark for both in-domain and out-of-
domain generalization. In addition, we evaluate the symbolic system ccg2lambda
on the dataset to obtain a symbolic reference point for the neural baselines es-
tablished in this experiment.
    For Experiment 2, the results of Experiment 1 (i.e., fine-tuned model per-
formance) are used as the baseline to assess whether the vocabulary extension
yields further improvements.
    For Experiments 6 and 7, Experiment 1 also serves as the baseline, allowing us
to assess the relative benefits of three-step curriculum learning and multilingual
training, respectively.
    For Experiment 5, we use both the model’s zero-shot or pre-trained perfor-
mance (without any targeted fine-tuning) and the performance from Experi-
ment 1 as baselines, in order to capture the potential gains from intermediate
predicate prediction in addition to direct fine-tuning.
    For Experiments 3 and 4, we compare both to the model’s zero-shot or
pre-trained performance and to the Experiment 1 baseline (i.e., standard fine-
tuning). This allows us to measure not only the incremental benefit of providing
explicit or noisy predicate lists, but also the overall performance gain compared
to conventional fine-tuning without additional predicate information. It is im-
portant to note that zero-shot or pre-trained performance is only evaluated for
the decoder-only models, since the T5 models do not produce meaningful FOL
translations without fine-tuning
    In all cases, this systematic baseline setup enables robust conclusions on the
effectiveness of each method and fair comparisons across experimental condi-
tions.
10      F. Vossel et al.

4     Results

4.1   Results of baselines and standard fine-tunning

Table 4 compares the accuracy of the evaluated LLMs in the baseline setup.
As expected, GPT-4o, DeepSeek-R1-0528, DeepSeek-V3-0324 and Logi-
cLLaMA perform better than the other models, particularly in the few-shot
setting. This can be attributed to significantly larger scale and broader pre-
training corpus, as well as to the fact that LogicLLaMA was trained on a
subset of our dataset, which may overlap with the test set. Overall, the higher
scores for logical equivalence compared to exact match can likely be attributed
to the model’s tendency to produce non-canonical formula representations, as
exemplified in Table 4.1. The results after predicate normalization are particu-
larly insightful, as they provide initial evidence supporting our hypothesis: LLMs
struggle more with correctly reproducing predicate names than with capturing
the underlying logical structure.
    In Table 5, we compare the accuracy of the fine-tuned LLMs in the base-
line fine-tuning setup. Among the evaluated models, Olmo-32B performs the
worst across all metrics. This may be attributed to its relatively limited pre-
training, suggesting that large language models already acquire a rudimentary
understanding of logical structure from pretraining on natural language alone.
    If this hypothesis holds, the performance of the T5 models becomes partic-
ularly noteworthy. Despite being encoder-decoder models—unlike the decoder-
only architecture of the other LLMs—they perform on par with or even outper-
form larger models such as LLaMA3.1-8B and Mistral-24B. This indicates
that T5 models might benefit from their architecture, which explicitly encodes
the input sequence before generating output. Such structural guidance during
encoding could facilitate the mapping from natural language to logical forms,
especially in tasks that require understanding and transformation rather than
open-ended generation.


          Model            Exact Exact (Pred.) Equiv. Equiv. (Pred.)
          T5-base     29.52          44.33     32.71        50.17
          T5-3B       32.96          45.85     36.21        51.54
          Flan-T5-XXL 35.79          49.47     38.83        54.79
          LLaMA3.1-8B 28.46          41.87     32.02        47.90
          Mistral-24B 34.83          48.23     38.18        53.92
          Olmo-32B    24.29          36.49     27.89        42.66
Table 5. Experiment 1: Model accuracy by exact and logical match, before/after
predicate normalization with standard fine tuning. All scores are in %.



  In contrast, ccg2lambda fails to produce correct logical forms for the vast
majority of inputs (0.00% on not/predicate matched exact match and 0.43%
                          Natural Language to First Order Logic with LLMs         11


       Model                 Exact Exact (Pred.) Equiv. Equiv. (Pred.)
       LLaMA3.1-8B*          2.37         4.10         4.17        6.83
       Mistral-24B*          7.24        10.73        11.44       17.57
       Olmo-32B*             1.91         3.44         4.37        8.58
       GPT-4o*               8.16        11.92        13.02       20.28
       LogicLLaMA*           0.97         1.16         3.06        5.27
       GPT-4o**             10.98        16.60        18.22       29.08
       LogicLLaMA**         16.05        24.79        18.71       29.45
       DeepSeek-V3-0324**   10.33        15.33        15.53       23.17
       DeepSeek-R1-0528**** 8.27         12.87        18.11       30.53
       ccg2lambda***         0.00         0.00         0.27        0.43
Table 4. Baseline: Model accuracy by exact and logical match, before/after predicate
normalization without fine tuning. *zero-shot **few-shot *** only 8225 NL sentences
could be parsed. ****CoT reasoning was used in a few-shot scenario. All scores are in
%.


      NL (Input)        Tomatoes are red and round, while cucumbers are green
                        and elongated.
      FOL_PRED          ∀x (Tomato(x) → (Red(x) ∧ Round(x)))
                        ∧ ∀y (Cucumber(y) → (Green(y) ∧ Elongated(y)))
      FOL_GT          ∀x ∀y (Tomato(x) → (Red(x) ∧ Round(x)))
                      ∧ (Cucumber(y) → (Green(y) ∧ Elongated(y)))
Table 6. Equivalent but not identical FOL translations. FOL_PRED is the formula
predicted by the FLAN-T5-XXL model and FOL_GT is the ground-truth formula.




on predicate matched equivalence match). Its performance is severely con-
strained by the rigidity of its manually constructed grammar, which lacks the
flexibility to handle the syntactic and semantic variety present in natural lan-
guage. These findings highlight the superiority of neural approaches over purely
symbolic systems in the task of semantic parsing.


4.2    Results of further experiments

Adding explicit tokens for logical symbols yielded only marginal improvements
for Olmo-32B and T5-base (less than one percentage point), while other mod-
els showed slight performance drops. This suggests that representing logical sym-
bols using multiple subword tokens does not substantially hinder model under-
standing, and dedicated tokens offer no consistent performance benefit.
    Models fine-tuned with ground-truth predicate names substantially outper-
form all other configurations. The best-performing model (Flan-T5-XXL) achieves
63.45% on the exact match and 70.27% on the equivalence match with only
marginal improvements if predicate matching (63.54% on exact match) was ap-
plied. Adding noise to predicate names leads to a slight performance drop, but
12      F. Vossel et al.

the effect is marginal, confirming that the main benefit stems from access to
correct predicate structure rather than stability under perturbations (Table 7).
     By contrast, initial training for predicate name prediction yields consider-
ably worse results. For example, FLAN-T5-XXL reaches only 25.96% on the
exact match and 28.26% on the equivalence match. If predicate matching was
applied FLAN-T5-XXL reaches 35.11% on the exact match and 38.95% on
the equivalence match. This confirms our hypothesis that exact predicate align-
ment presents a hard constraint. Given the more than 60,000 unique predicates
in the dataset and substantial variation in predicate usage, models struggle to
generalize under these strict conditions.
     The stepwise training procedure—starting with gold predicates, followed by
noisy and then free-form formulas—also underperforms relative to the baseline,
despite access to complete target structures during early training. FLAN-T5-
XXL achieves just 33.83% on the exact match and 36.69% on the equivalence
match, suggesting that training on ground-truth predicates might lead to over-
fitting on the given predicates which then reduces final performance.
     Multilingual training leads to only minor degradation compared to mono-
lingual models. T5-3B achieves 30.33% on the exact match and 32.90% on
the equivalence match, demonstrating that multilingual inputs are compatible
with consistent logical form generation and may support future cross-lingual
extensions.


          Model            Exact Exact (Pred.) Equiv. Equiv. (Pred.)
          T5-base     57.02           57.92       63.22        64.34
          T5-3B       60.04           60.35       66.28        66.66
          Flan-T5-XXL 62.39           62.53       69.06        69.23
          LLaMA3.1-8B 43.76           43.91       53.68        53.95
          Mistral-24B 50.80           50.89       59.93        60.07
          Olmo-32B    36.58           36.90       46.15        46.65
Table 7. Experiment 4: Model accuracy by exact and logical match, before/after
predicate normalization with fine-tuning on fixed predicate list with noise. All scores
are in %.



4.3   Results for logical arguments
[29] argue that with traditional datasets, it is difficult to assess the quality of NL
to FOL translations automatically. As an automated santiy check, they suggest
to use hand-crafted sets of natural language logical arguments, whose (in)validity
is known. Then, after translation to FOL, (in)validity of the argument can be
checked with an automated theorem prover, and if the validity disagrees with the
manually annoteted one, an error in the translation has been spotted. FOLIO [10]
is such a dataset of NL arguments.
    Our model achieves competitive results (39.70% valid conclusions) com-
pared to the best version of LLaMA-2 13B (37.44% valid conlsusions with
                         Natural Language to First Order Logic with LLMs        13

inkremental fine-tuning and predicate verifier), even though it was not trained
on the FOLIO dataset. This suggests that the iterative fine-tuning procedure
on FOLIO proposed by previous work [29] is not strictly required to attain
strong performance. Additionally, our model exhibits robust behavior in multi-
premise inference settings, where earlier premises are provided as contextual
input—despite such scenarios not being part of the training data. This points
to the model’s capacity to generalize to more complex reasoning setups without
explicit supervision.


5   Conclusion
For the task of translating natural language into first-order logic, we have fined-
tuned several large language models using the MALLS and Willow datasets,
and have conducted experiments with several settings. An important aspect was
the provision or learning of a list of predicate names that shall occur in the
translation. While the provision of ground-truth predicate names greatly helps,
learning them in a two-step process did not lead to good results. Our fine-
tuned Flan-T5-XXL model with 11 billion parameters, can outperform baselines
like GPT-4o, LogicLLaMA and even DeepSeek-R1-0528, as well as a symbolic
baseline. The accuracy of translations of natural language arguments from the
FOLIO dataset is comparable to the baseline (note that here only (in)validity
of the translated argument is considered). The source code for our fine-tuned
models is available on GitHub, and the models themselves can be accessed on
Hugging Face. A common mistake in NL to FOL translation that is also present
in the MALLS dataset is the confusion of hard-to-recognise Aristotelian forms:
“A pineapple is a fruit with spiky skin” is translated to
                 ∃x(P ineapple(x) ∧ F ruit(x) ∧ SpikySkin(x)).
Despite being trained with MALLS, our model correctly translates this to
             ∀x(P ineapple(x) → (F ruit(x) ∧ HasSpikySkin(x)))),
which can be explained with the usage of the Willow dataset that translates such
situations correctly.
    We observe that reasoning strategies such as CoT can sometimes degrade
performance in NL-to-FOL translation, as initially correct outputs are over-
written during the reasoning process. This aligns with the illusion of thinking
phenomenon described by Apple [28]. Future work may benefit from a two-stage
approach, where base model outputs are first generated and then verified or
refined using a reasoning model, as suggested by Thatikonda et al [29].
    Flan-T5-XXL achieves 55% accuracy without a predicate list and 70% with
a noisy one, as is realistic in practice. A correlation of −0.318 between sen-
tence length and exact match further suggests that shorter sentences are trans-
lated more accurately. Future work includes improving predicate extraction—
e.g., splitting composite names like ProtectFromRain, tokenizing given predicate
names, and correcting errors in the MALLS dataset to boost accuracy.
14      F. Vossel et al.

    Furthermore, we plan to correct the errors in the MALLS dataset, in order
to improve accuracy.
    As another line of future work, we plan to cover also less and more expressive
logics used for specification and ontology development.

Acknowledgments. The authors want to thank Christoph Benzmüller, Dave Barker-
Plummer and İbrahim Ethem Deveci for helpful discussions.
   This work was supported by the Deutsche Forschungsgemeinschaft (DFG, German
Research Foundation) – 456666331.

Disclosure of Interests. The authors have no competing interests to declare that
are relevant to the content of this article.


References
 1. Barker-Plummer, D., Cox, R., Dale, R.: Dimensions of difficulty in translating
    natural language into first order logic. International Working Group on Educational
    Data Mining (2009)
 2. Bos, J., Markert, K.: Recognising textual entailment with logical inference. In: HLT
    ’05. pp. 628–635. Association for Computational Linguistics, Vancouver, British
    Columbia, Canada (2005). https://doi.org/10.3115/1220575.1220654
 3. Brunello, A., et al.: Evaluating LLMs Capabilities at Natural Language to
    Logic Translation: A Preliminary Investigation. In: CEUR workshop proceedings.
    vol. 3904, pp. 103–110 (2025)
 4. Cai, Q., Yates, A.: Large-scale Semantic Parsing via Schema Matching and Lexi-
    con Extension. In: Proceedings of the 51st Annual Meeting of the Association for
    Computational Linguistics (Volume 1: Long Papers). pp. 423–433 (2013)
 5. Chung, H.W., Hou, L., Longpre, S., Zoph, B., Tay, Y., Fedus, W., Li, Y., Wang, X.,
    Dehghani, M., Brahma, S., et al.: Scaling instruction-finetuned language models.
    Journal of Machine Learning Research 25(70), 1–53 (2024)
 6. DeepSeek-AI: Deepseek-v3 technical report (2024), https://arxiv.org/abs/2412.
    19437
 7. DeepSeek-AI: Deepseek-r1: Incentivizing reasoning capability in llms via reinforce-
    ment learning (2025), https://arxiv.org/abs/2501.12948
 8. Deveci, I.E.: Transformer Models for Translating Natural Language Sentences into
    Formal Logical Expressions. Master’s thesis, Middle East Technical University
    (Turkey) (2024)
 9. Grattafiori, A., et al.: The LLama 3 herd of models. arXiv preprint
    arXiv:2407.21783 (2024)
10. Han, S., et al.: Folio: Natural language reasoning with first-order logic. arXiv
    preprint arXiv:2209.00840 (2022)
11. Hu, E.J., Shen, Y., Wallis, P., Allen-Zhu, Z., Li, Y., Wang, S., Wang, L., Chen, W.,
    et al.: Lora: Low-rank adaptation of large language models. ICLR 1(2), 3 (2022)
12. Lalwani, A., et al.: Nl2fol: translating natural language to first-order logic for logical
    fallacy detection. arXiv preprint arXiv:2405.02318 (2024)
13. Levenshtein, V.I., et al.: Binary codes capable of correcting deletions, insertions,
    and reversals. In: Soviet physics doklady. pp. 707–710. No. 10 in 8, Soviet Union
    (1966)
                           Natural Language to First Order Logic with LLMs           15

14. Levkovskyi, O., Li, W.: Generating Predicate Logic Expressions from Natural Lan-
    guage. In: SoutheastCon 2021. pp. 1–8. IEEE, Atlanta, GA, USA (Mar 2021).
    https://doi.org/10.1109/SoutheastCon45413.2021.9401852
15. Li, Y., Su, Z., Li, Y., Zhang, H., Wang, S., Wu, W., Zhang, Y.: T5-sr: A unified
    seq-to-seq decoding strategy for semantic parsing. In: ICASSP 2023-2023 IEEE
    International Conference on Acoustics, Speech and Signal Processing (ICASSP).
    pp. 1–5. IEEE (2023)
16. Liu, J.: Few-shot natural language to first-order logic translation via code genera-
    tion. In: Proceedings of the 2025 Conference of the Nations of the Americas Chapter
    of the Association for Computational Linguistics: Human Language Technologies
    (Volume 1: Long Papers). pp. 10939–10960 (2025)
17. Loshchilov, I., Hutter, F.: Decoupled weight decay regularization. arXiv preprint
    arXiv:1711.05101 (2017)
18. Lu, X., Liu, J., Gu, Z., Tong, H., Xie, C., Huang, J., Xiao, Y., Wang, W.: Parsing
    natural language into propositional and first-order logic with dual reinforcement
    learning. In: Proceedings of the 29th International Conference on Computational
    Linguistics. pp. 5419–5431 (2022)
19. Martínez-Gómez, P., Mineshima, K., Miyao, Y., Bekki, D.: Ccg2lambda: A Compo-
    sitional Semantics System. In: Proceedings of ACL-2016 System Demonstrations.
    pp. 85–90. Association for Computational Linguistics, Berlin, Germany (2016).
    https://doi.org/10.18653/v1/P16-4015
20. Mistral AI Team: Mistral small 3: Apache 2.0, 81% mmlu, 150 tokens/s (Jan 2025),
    https://mistral.ai/news/mistral-small-3, accessed on June 7, 2025
21. de Moura, L., et al.: Z3 Theorem Prover. https://github.com/Z3Prover/z3 (2024),
    accessed: 2025-06-07
22. OLMo, T., Walsh, P., Soldaini, L., Groeneveld, D., Lo, K., Arora, S., Bhagia,
    A., Gu, Y., Huang, S., Jordan, M., et al.: 2 olmo 2 furious. arXiv preprint
    arXiv:2501.00656 (2024)
23. OpenAI: Gpt-4o: Openai’s new flagship model. https://openai.com/index/gpt-4o
    (2024), accessed: 2025-06-07
24. Pan, L., Albalak, A., Wang, X., Wang, W.Y.: Logic-LM: Empowering large lan-
    guage models with symbolic solvers for faithful logical reasoning (2023), https:
    //arxiv.org/abs/2305.12295
25. Pease, A., Murray, W.: An english to logic translator for ontology-based knowl-
    edge representation languages. In: International Conference on Natural Language
    Processing and Knowledge Engineering,. pp. 777–783. IEEE (2003)
26. Raffel, C., Shazeer, N., Roberts, A., Lee, K., Narang, S., Matena, M., Zhou, Y., Li,
    W., Liu, P.J.: Exploring the limits of transfer learning with a unified text-to-text
    transformer. Journal of machine learning research 21(140), 1–67 (2020)
27. Shinan, E., et al.: Lark: A modern parsing library for Python. https://github.com/
    lark-parser/lark (2024), accessed: 2025-06-07
28. Shojaee, P., et al.: The illusion of thinking: Understanding the strengths and lim-
    itations of reasoning models via the lens of problem complexity (2025), https:
    //ml-site.cdn-apple.com/papers/the-illusion-of-thinking.pdf
29. Thatikonda, R.K., Han, J., Buntine, W., Shareghi, E.: Strategies for improving
    NL-to-FOL translation with LLMs: Data generation, incremental fine-tuning, and
    verification. arXiv:2409.16461 (2024)
30. Yang, Y., Xiong, S., Payani, A., Shareghi, E., Fekri, F.: Harnessing the Power of
    Large Language Models for Natural Language to First-Order Logic Translation.
    In: Proceedings of the 62nd Annual Meeting of the Association for Computational
    Linguistics. pp. 6942–6959 (2024). https://doi.org/10.18653/v1/2024.acl-long.375
