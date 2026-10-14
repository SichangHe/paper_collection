                                                     Explaining Textual Entailment with Lexical Entailments:
                                                    Using LLMs to Supply Lexical Relations for Formal Proofs

                                                   Jorryt de Jong1       Stefan Morača1 Ettore Cesari1         Lasha Abzianidze2
                                                                          1
                                                                            Utrecht University, the Netherlands
                                                        2
                                                          Institute for Language Sciences, Utrecht University, the Netherlands
                                                               {j.e.j.dejong,s.moraca,e.cesari}@students.uu.nl
                                                                                  Correspondence: l.abzianidze@uu.nl



                                                               Abstract                                                              NLI problem




                                                                                                      Intrinsic evaluation LEX-NLI
                                                                                                                                     P: A zoo keeper holds a chinchilla.
                                             Large Language Models (LLMs) are highly ca-
arXiv:2609.32491v1 [cs.CL] 26 Sep 2026




                                                                                                                                     H: A person holds a small animal.
                                             pable of natural language reasoning and appear
                                             to store a great deal of lexical knowledge, but




                                                                                                                                              predict




                                                                                                                                                                           predict
                                             it is still unclear how much of this knowledge
                                             they actually use when reasoning, and whether
                                             they use it in the right way. On the other                                              Lexical explanation (LEX)
                                             hand, logic-based Natural Language Inference                                                                                Label
                                                                                                                                      zoo keeper ⊑ person              entailment




                                                                                                                                                                                     Extrinsic evaluation
                                             (NLI) systems provide transparent and formally
                                             grounded reasoning, but they need to be sup-                                              chinchilla ⊑ small animal
                                             plied with rich lexical knowledge to prove infer-
                                             ences beyond purely logical ones. In this paper,                                          chinchilla ⊑ animal

                                             we evaluate whether LLMs can identify all lex-
                                             ical knowledge needed to solve NLI problems                                                      Formal proof with LangPro
                                             and how much this knowledge contributes to
                                             proof search in a logic-based NLI system. Our                                                 Inject as KB entries        Run LangPro
                                             research focuses exclusively on structured lexi-                                              zoo keeper ⊑ person
                                                                                                                                           chinchilla ⊑ small animal
                                             cal entailments (e.g., chinchilla ⊑ small animal)                                             chinchilla ⊑ animal
                                                                                                                                           (added to KB)
                                             as a proxy for structured explanations for NLI
                                             problems with an entailment label. First, we
                                             curate a dataset for a new task of explaining                  Figure 1: Overview of the proposed intrinsic and extrin-
                                             sentential entailments with a set of lexical en-               sic evaluation. Given an NLI problem, an LLM is jointly
                                             tailments. The dataset is used to intrinsically                evaluated on the predicted inference label and a struc-
                                             evaluate LLMs on generating structured lexical                 tured lexical explanation (LEX) against human-curated
                                             explanations. Then, we use NLI as an extrinsic                 multi-reference LEX sets. Extrinsically, the generated
                                             evaluation in a simple neuro-symbolic setting,                 lexical relations are supplied to the LangPro theorem
                                             assessing whether LLMs can supply sufficient                   prover, which determines whether they suffice to con-
                                             lexical relations to LangPro, a natural-logic the-             struct a formal proof.
                                             orem prover for natural language. The results
                                             show that the proposed task remains challeng-
                                             ing even for hosted proprietary LLMs, and that
                                             their contribution to theorem proving is mod-
                                                                                                            predict whether a hypothesis sentence is entailed
                                             erate: generated relations are often only par-                 by, contradicted by, or is neutral with respect to a
                                             tially sound and may be tailored to the specific               premise text. While the frontier models have sat-
                                             NLI problem rather than representing generally                 urated common NLI benchmarks, we still do not
                                             valid lexical knowledge.                                       know how sound their reasoning is when arriving
                                                                                                            at correct inference labels.
                                         1   Introduction
                                                                                                               To study how LLMs reason in NLI more closely,
                                         Recent LLM progress has shifted much of NLP re-                    researchers have built simplified synthetic NLI-
                                         search toward downstream tasks. However, Natural                   style datasets (that usually require multi-step rea-
                                         Language Inference (NLI, Dagan et al., 2013), a                    soning) and pursued two related lines of work: (i)
                                         generic reasoning task, remains popular because it                 train and evaluate LLMs on multi-step reasoning in
                                         allows evaluation of models on specific reasoning                  natural language (Clark et al., 2020; Zhong et al.,
                                         phenomena. The NLI task challenges models to                       2022; Saparov and He, 2023; Han et al., 2024),

                                                                                                  1
and (ii) use LLMs to encode sentence meaning in a                   and Vydiswaran, 2021; Carton et al., 2022; Stacey
formal logic formula that is later fed to rule-based                et al., 2022; Ghasemi Madani and Minervini, 2023).
reasoners, such as first-order logic theorem provers                However, the span highlights, which Camburu et al.
(Olausson et al., 2023; Pan et al., 2023; Ryu et al.,               (2018) used to facilitate free-text explanation col-
2025). However, this suggests that the problems                     lection, cannot be regarded as lexical knowledge
from the original NLI datasets1 are too challeng-                   and are too noisy for a gold standard. The second
ing for (i) and (ii), and such valuable datasets are                line of work delegates reasoning to rule-based sys-
unfortunately left out of these research lines.                     tems, while LLMs translate sentences into meaning
   To partially formalize NLI reasoning, we intro-                  representations, often first-order logic (Olausson
duce an explainable task in which models produce                    et al., 2023; Pan et al., 2023; Ryu et al., 2025; No-
structured lexical relations supporting the infer-                  ble et al., 2025). The third line of work constructs
ence label. We also evaluate a neuro-symbolic                       synthetic NLI-style datasets in which the reasoning
pipeline distinct from (ii). Specifically, LLMs gen-                process is represented as a tree, graph, or sequence
erate lexical entailments—not logical formulas—to                   of formally validated inference steps (Clark et al.,
help the natural logic prover LangPro (Abzianidze,                  2020; Zhong et al., 2022; Saparov and He, 2023;
2017a) address scarce KB resources.2 This aligns                    Dalvi et al., 2021; Han et al., 2024). The last two
with work treating LLMs as knowledge bases (KB)                     lines of work rely on simpler language or more
(Petroni et al., 2019; AlKhamissi et al., 2022). Our                restricted reasoning patterns than those found in
evaluation setup is illustrated in Figure 1.                        standard NLI benchmarks such as SNLI (Bowman
   Our contributions are threefold:                                 et al., 2015) and SICK (Marelli et al., 2014).
   (1) We curate a test set of entailment problems                     In contrast, we use existing entailment problems
together with the corresponding lexical entailments                 from SNLI and SICK augmented with structured
that are necessary and sufficient for solving them;                 lexical explanations, formatted as curated multiple-
   (2) We evaluate multiple LLMs against the test                   reference relation sets. We restrict the task to entail-
set on the LEX-NLI task, identifying relevant lexi-                 ment rather than to synthetic sentences or simple
cal entailments for NLI problems, and analyze the                   reasoning patterns, as in the related work.
results with respect to model family and size;                         State-of-the-art rule-based NLI systems (Yanaka
   (3) We select high-performing LLMs and use                       et al., 2018; Abzianidze, 2020) suffer from lexical
them as KB generators for LangPro while the latter                  knowledge sparsity despite using resources such as
is evaluated on its ability to prove NLI problems.                  WordNet (Fellbaum, 1998) and ConceptNet (Speer
Together, these results demonstrate an interpretable                et al., 2017). Consequently, several studies used
integration of LLMs and a symbolic reasoner.                        neural models to supply missing lexical/phrasal
                                                                    knowledge. Yoshikawa et al. (2019) applied the
2    Related Work                                                   ComplEx KB completion model (Trouillon et al.,
                                                                    2016) to generate lexical relations for a theorem
NLI is one of the most widely studied NLP tasks.
                                                                    prover. Tomihari and Yanaka (2023) used vision-
The release of e-SNLI (Camburu et al., 2018) initi-
                                                                    language embeddings to assess phrase-level entail-
ated a research line on explainable NLI by augment-
                                                                    ments selected by a logic-based NLI system. For
ing NLI problems with human-elicited free-text ex-
                                                                    Japanese logic-based NLI, Kobayashi et al. (2026)
planations and span highlights. However, the lack
                                                                    developed a lexical-entailment classifier inspired
of precise and adequate metrics for automatically
                                                                    by hyperbolic embeddings (Ganea et al., 2018).
comparing generated and reference explanations
                                                                    Chen et al. (2021) complemented WordNet and
hinders progress in free-text explainable NLI.
                                                                    ConceptNet with phrasal paraphrases derived from
   Several alternatives to free-text explanations
                                                                    a pretrained language model, while Noble et al.
have therefore been explored. The first line of
                                                                    (2025) used an LLM to generate first-order-logic
work directly stems from e-SNLI and uses its span
                                                                    axioms corresponding to lexical relations for a the-
highlights for training and/or evaluation of explain-
                                                                    orem prover. Aly et al. (2023) and Strong et al.
able NLI models (DeYoung et al., 2020; Zhao
                                                                    (2024) on natural-logic-based fact verification use
    1
      For instance, RTE (Dagan et al., 2006), SICK (Marelli         instruction-tuned LLMs to predict short-phrase re-
et al., 2014), and SNLI (Bowman et al., 2015).                      lations for a version of natural logic.
    2
      Unlike ours, the works in (i) and (ii) do not use LLMs
to produce lexical knowledge because their synthetic datasets          Our work instead formulates lexical KB predic-
require little covert lexical knowledge.                            tion as an independent explainable task. Reference

                                                                2
lexical relations are not tied to third-party systems                     We use the term lexical broadly enough to
or their representation language. We judge them                        include both single- and multi-word concepts.
by whether they explain the NLI inference, not by                      Lexical items are essentially similar to those
whether a given reasoning system can import them                       found in lexical databases such as WordNet,
and successfully use them in its proofs.                               but extending beyond their incomplete cover-
                                                                       age. Single-word relations include cap ⊑ hat
3       Structured Explanation with Lexical                            and obese ⊑ fat, whereas multi-word relations in-
        Entailments                                                    clude female swimmer ⊑ woman and little boy ⊑ child.
We     use lexical entailments,            such as                     Multi-word expressions are included when us-
guitar ⊑ musical instrument, as structured NLI
                                                                       ing only one of their components would pro-
explanations. We first motivate our focus on                           duce an invalid or insufficient relation. For
entailment problems and then show how lexical                          instance, swimmer ⊑ woman is false, whereas
                                                                       female swimmer ⊑ woman is acceptable. Similarly,
entailments can serve as a key component of the
                                                                       chinchilla ⊑ animal is insufficient for a hypothesis
underlying reasoning. Finally, we define the kinds
of words and short phrases that may occur in                           referring to a “small animal”, as the more informa-
lexical entailments.                                                   tive relation chinchilla ⊑ small animal is required.
   Earlier formulations of Recognizing Textual En-                        For consistency and comparability, expressions
tailment (Dagan et al., 2006) distinguished between                    in a relation are normalized to their lemmatized
entailment and non-entailment, whereas contempo-                       forms and exclude determiners, auxiliary verbs, the
rary NLI datasets typically divide non-entailment                      infinitival marker “to”, and prepositional phrases.
into contradiction and neutral. The distinction be-                    We also exclude relations that are merely obtained
tween contradiction and neutral, however, is not al-                   by dropping modifiers: tall man ⊑ man is uninfor-
ways straightforward.3 Moreover, non-entailment                        mative because entailment follows from the com-
cases are generally more difficult to explain using                    positionality by discarding tall.
only word- or phrase-level relations. A neutral                           We call a set of lexical entailments that serves
label usually results from the absence of certain                      as a lexical basis of explanations for an NLI prob-
semantic relations, and contradictions sometimes                       lem a LEX set, or LEX. Some entailment prob-
depend only on negation, which doesn’t require                         lems don’t require lexical entailments. When the
relations. In contrast, word- or phrase-level rela-                    hypothesis follows through syntactic and compo-
tions frequently represent knowledge needed to ex-                     sitional reasoning, the LEX set is empty. For ex-
plain entailment NLI problems, e.g., “a zoo keeper                     ample, “A zoo keeper holds a chinchilla” entailing
holds a chinchilla” entailing “a person holds a                        “A chinchilla is held” doesn’t require lexical rela-
small animal” is explained with zoo keeper ⊑ person                    tions but is licensed by passive alternation and sub-
and chinchilla ⊑ small animal entailment relations.                    categorization of “hold”, which omits the agent.
We therefore currently focus only on entailment                           LEX sets are not intended to constitute complete
problems and lexical entailment relations between                      formal proofs of entailment. Instead, they serve as
words and multi-word lexical items.                                    structured proxies for the lexical knowledge that
   A lexical entailment is a directed binary relation,                 licenses an entailment. When non-empty, they rep-
e.g., guitar ⊑ musical instrument, where the first ar-                 resent the lexical component that a complete formal
gument is semantically more specific than or equal                     or structured explanation must account for.
to the second. It is structured because it represents
the knowledge in an explicit format. This makes                        4    Curating a Test Set
the explanations easier to compare across anno-
                                                                       To evaluate models on explainable NLI from a lex-
tators and models and allows them to be directly
                                                                       ical perspective, we curate a set of NLI problems
supplied to a symbolic reasoning system.4
                                                                       paired with reference LEX sets. We constructed
    3
      This was already discussed by Marelli et al. (2014). Con-        a manually annotated test set of entailment prob-
sider a premise-hypothesis pair from SICK: “A couple is not
looking at a map” and “A couple is looking at a map”. The
                                                                       lems drawn from SICK and SNLI, as these datasets
inference label depends on the interpretation of indefinite NPs:       heavily depend on lexical knowledge. All four au-
if “a couple” and “a map” co-refer across sentences, then the          thors served as both data curators and annotators.
NLI problem is contradiction, otherwise neutral.
    4
      In contrast, a free-text explanation doesn’t make the com-       means musical instrument” and “a guitar is a type of a musical
parison straightforward: detecting equality between “guitar            instrument” is not trivial.


                                                                   3
                           NLI problem with three LEX annotations and an optional 4th alternative LEX
     P: A man in a bright yellow shirt juggles while riding a unicycle.                                   ∅            ∅            ∅
     H: A man performs a juggling act on a unicycle.
     P: A young boy wearing safety swimming gear and goggles is in a pool.            H: A kid uses eye protection while in the water.
          goggles ⊑ eye protection;                   goggles ⊑ eye protection;                       goggles ⊑ eye protection;
          pool ⊑ water; young boy ⊑ kid               pool ⊑ water;    young boy ⊑ kid                pool ⊑ water; young boy ⊑ kid

     P: A woman observes a rusted antique car.      H: A woman looks at an old car.
             antique ⊑ old;               antique car ⊑ old car;                 antique ⊑ old;                 antique car ⊑ old car;
             observe ⊑ look               observe ⊑ look                         observe ⊑ look at              observe ⊑ look at

     P: A person rides his bicycle in the sand beside the ocean.                                     sand ⊑ beach      ∅            ∅
     H: A person is on a beach.
     P: A black and white dog is carrying a huge stick on the green grass.                                             grass ⊑ field;
     H: A black and white dog with a large branch is running in the field.               green grass ⊑ field;          huge ⊑ large;
           huge stick ⊑ large branch                  huge ⊑ large                       huge ⊑ large                  stick ⊑ branch



Table 1: Examples of agreement and variation among three independently produced LEX annotations. An additional
4th LEX, if introduced during adjudication, is marked with a dashed borderline. ∅ stands for an empty LEX. The
first two problems have unanimous agreement in LEX annotations.


Each annotator initially selected 70-100 entailment                       to distinguish annotation mistakes from legitimate
problems from the two datasets and assigned a LEX                         explanatory variation. As a result, we obtained
set to each selected problem. During this selection                       unanimous agreement for 223 (62%) problems (see
process, the annotators aimed for approximately 20-                       Table 2).5 When a disagreement could be resolved
30% of the problems to have an empty LEX. This                            into a single adjudicated annotation, one annotator
ensured that the test set contained both problems                         proposed the revised LEX. The revised annota-
requiring non-trivial lexical knowledge and prob-                         tion was subsequently checked by the annotators
lems whose entailment could be explained through                          whose original LEX sets had been modified. This
syntactic and compositional reasoning alone. All                          process ensured that changes were not introduced
annotations were produced according to the guide-                         unilaterally and that the final annotation reflected
lines presented in Appendix B. The selected NLI                           agreement among the affected annotators.
problems were subsequently pooled into a single                              When disagreement couldn’t be reduced to a
collection. Each problem was then independently                           single canonical LEX (in total 139), several LEX
annotated by two additional annotators, besides its                       variants were retained as a reference answer for
original annotator. Consequently, every problem                           the same problem. In several instances, adjudica-
received three independently produced LEX anno-                              5
                                                                              Three SNLI problems were excluded from the final
tations. This procedure allowed us to assess both                         dataset: one contained an incomplete sentence, and two had
the reproducibility of the task and the extent to                         entailment labels that were judged unreliable.
which different annotators identify the same lexical
knowledge as explanatory.                                                  Dataset statistics
   We considered the annotations to be in unani-                           Total NLI problems                                      362
                                                                           SNLI problems / SICK problems                      280 / 82
mous agreement when all three annotators assigned                          Problems w/ unique LEX (unanimous agreement) 223 (61.6%)
the same LEX set. During the first phase, out of                           Problems with an alternative (4th) LEX           22 (6.1%)
                                                                           Total LEX (incl. the added 4th LEX)                   1108
the 365 annotated problems, 161 (44%) received                             LEX size distribution: 0, 1, 2, 3+        29 / 51 / 14 / 6%
unanimous LEX annotations. The remaining cases                             Annotator performance          n         Exact Match         micro-F1
exhibited variation in the selected relations, their                       Annotator-1 vs. rest         271            75.7                 81.5
granularity, or the amount of lexical knowledge                            Annotator-2 vs. rest         271            84.5                 86.0
                                                                           Annotator-3 vs. rest         271            80.8                 85.9
considered necessary for explaining the inference.                         Annotator-4 vs. rest         273            82.8                 86.2
These disagreements do not always indicate anno-                           Mean                           –            80.9                 84.9
tation errors, since more than one set of lexical
entailments may provide an acceptable explanation                         Table 2: Statistics of the final dataset and annotator
for the same NLI problem (see Table 1).                                   performance after the adjudication. Annotator-N vs rest
   We therefore conducted an adjudication phase                           is based on the problems annotated by Annotator-N.


                                                                     4
tion also resulted in the creation of a fourth LEX                     rive the intended inference. For instance, our run-
variant that captured an acceptable explanation not                    ning NLI example requires relations corresponding
represented by any of the three original annotations.                  to zoo keeper ⊑ person and chinchilla ⊑ small animal,
This outcome indicates that variation is, to some                      neither of which is available in WordNet.7
extent, inherent to the task rather than being solely                     We use LLMs to supplement LangPro with lex-
a consequence of inconsistent annotation. The ex-                      ical knowledge that is missing from WordNet.
amples from the final dataset are given in Table 1.                    Rather than asking an LLM to predict the NLI la-
   The resulting test set attaches one to four refer-                  bel, construct the proof itself, or translate sentences
ence LEX sets (possibly empty LEX) to each NLI                         into logic formulas, we use it only to propose rel-
problem. 20% of the LEX annotations contain more                       evant lexical knowledge. After receiving lexical
than one relation, while 29% are empty. Overall an-                    KB from an LLM, LangPro remains solely respon-
notator performance is 80.9% for exact match and                       sible for determining whether the supplied KB is
84.9% for micro-F1, computed as the mean of the                        sufficient to find a proof. Thus, LangPro provides
four annotator-level scores. For each annotator, we                    an extrinsic test of whether LLMs generate lexical
calculate the scores by comparing the annotator’s                      entailments relevant for formal proof construction.
LEX to the other two or three LEX s (depending on
the presence of the 4th LEX).                                          6       Experiments
                                                                       We conduct two groups of experiments: evaluating
5       Lexical Entailments for Formal Proofs
                                                                       LLMs intrinsically on the new task of predicting
The lexical entailments introduced in Section 3                        LEX sets and extrinsically on how much those pre-
can be converted directly into KB entries                              dictions help LangPro prove NLI problems.8
for logic-based NLI systems. For example,
chinchilla ⊑ small animal can be represented as a sub-
                                                                       6.1      Predicting Lexical Explanations
sumption relation stating that every chinchilla is                     We evaluate eight instruction-following LLMs
a small animal. Such relations complement the                          from four model families: GPT-5.4 and GPT-5.4
logical rules of a prover with the lexical knowl-                      Mini, Claude Sonnet 4.5 and Claude Haiku 4.5,
edge required to connect predicates occurring in                       Gemini 3.5 Flash and Gemini 3.1 Flash-Lite, GPT-
the premise and hypothesis. A LEX set can there-                       OSS-20B, and Gemma 3 4B. The selection com-
fore be viewed not only as a structured explanation                    bines higher-capability hosted models with smaller,
of an inference, but also as a small problem-specific                  cheaper alternatives from the same families, allow-
KB that may lead to a formal proof.                                    ing us to examine whether LEX prediction requires
   One logic-based NLI system that can use such                        a frontier model or can be handled by cheaper mod-
knowledge is LangPro, a natural language theo-                         els. It also reduces dependence on a single devel-
rem prover based on natural logic and semantic                         oper. Additionally, GPT-OSS-20B and Gemma 3
tableaux (Abzianidze, 2017a,b).6 In addition to                        4B provide open-weight comparison points.
its logical rules, LangPro relies on a lexical KB                         Each model is evaluated five times using the
containing relations such as synonymy, hypernymy,                      same prompt. Only relations extracted from raw
and semantic incompatibility. A large part of this                     model responses are evaluated: no automatic post-
knowledge is obtained from WordNet. However,                           processing was used to correct word forms or dis-
WordNet does not contain every relation required                       card relations based on the vocabulary of an NLI
by NLI problems. Consequently, a tableau may                           problem. LLM inference details are provided in
remain open even when LangPro’s linguistic anal-                       Appendix A. The prompts follow the annotation
ysis and proof rules are otherwise sufficient to de-                   guidelines (see Appendix B). Prompt selection
    6
                                                                       details are in Appendix C.
     LangPro analyzes the linguistic structures of the premise
and hypothesis and converts them into logical forms that re-
                                                                          Predictions are evaluated against all reference
main relatively close to the original sentences. To test whether       LEX sets, and the best match determines the final
the premise entails the hypothesis, it attempts to construct a
                                                                           7
tableau from the premise together with the negation of the                  Feeding LangPro with lexical relations is straightfor-
hypothesis. The prover repeatedly applies logical, lexical, and        ward because multi-word expressions such as zoo keeper and
monotonicity-based inference rules, and the entailment is es-          small animal are already terms in its higher-order logic, without
tablished when every branch of the resulting tableau is closed         need to represent them as, for example, small(x) ∧ animal(x).
                                                                          8
by a contradiction. The resulting tableau constitutes a formal              The dataset and codebase are available from https://
proof whose individual inference steps can be inspected.               github.com/jorrytdejong/kbprojection.


                                                                   5
score. We use two scores to evaluate models on                         which LangPro attempts the proof again. The ex-
labeling entailment problems and generating LEX                        periment therefore tests whether feedback from the
sets. Exact Match (EM) counts a predicted LEX set                      symbolic prover, followed by a critical reassess-
correct when it is equal to one of the reference LEX                   ment of the generated KB, can improve the use-
sets. Because EM ignores the size of LEX, we addi-                     fulness of LLM-generated lexical knowledge on a
tionally use micro-F1 for finer-grained matching.9                     second attempt.
   Mismatch between lexical entailment relations
can be roughly divided into normalization, struc-                      7     Results
ture, and semantic errors. Normalization errors                        7.1    Predicting Lexical Explanations
concern wrong lemmatization of words in the rela-
tions. Structure errors include cases where two cor-                   The evaluation results of the eight models on the
rectly extracted arguments are placed in the wrong                     curated 362 problems are given in Table 3. The
order in a relation, i.e., in a swapped order for the                  evaluation is averaged over five runs, and the scores
entailment relation. Semantic errors cover mis-                        (with micro-F1 regarded as primary) are computed
takes that do not belong to the two aforementioned                     based on the best reference LEX sets. Since the
classes. To assess how much models struggle with                       proposed explainable NLI task requires models to
normalization, we use lemmatized F1 that elimi-                        predict an inference label together with a LEX set,
nates this type of error by lemmatizing LEX sets be-                   any LEX set paired with a non-entailment predic-
fore matching.10 We also use argument-unordered                        tion is considered distinct from a gold empty LEX.
F1, which ignores relation direction during match-                     However, if a model’s prediction for a problem is
ing, so that guy ⊑ man matches man ⊑ guy.                              not available due to an error in the API call, we
                                                                       ignore such problems from the model evaluation
6.2    Supplying Knowledge to LangPro                                  (indicated in the support column).
                                                                          In addition to the eight LLMs, we report results
For the extrinsic evaluation, we use an LLM to
                                                                       for three baselines. Empty LEX always returns
supply lexical entailments as a KB to LangPro
                                                                       an empty LEX set and serves as the simplest base-
while it searches for proofs of entailment problems.
                                                                       line. WordNet & Rules returns relations of the form
1,000 randomly sampled entailment problems from
                                                                       sp ⊑ sh that are found in WordNet, where sp and sh
the SNLI training set are used for this evaluation.
                                                                       are single- or multi-word lemma spans that occur
We compare five ways of assisting LangPro with
                                                                       only in the premise and hypothesis, respectively.11
lexical KBs: only WordNet, only LLM-generated
                                                                       WordNet & Oracle peeks at the reference LEX sets
knowledge, and WordNet with LLM-generated
                                                                       and selects all and only those relations that are val-
knowledge, with the latter two settings evaluated
                                                                       idated by WordNet lookup. It therefore represents
both in one-shot and agentic use of LLMs.
                                                                       a baseline that is perfect in selection of arguments,
   In the one-shot setting, the LLM generates a                        but limited by WordNet coverage.
KB once and LangPro attempts a proof using the
                                                                          Model performance ranking generally follows a
KB. In the agentic setting, a failed proof triggers
                                                                       simple size-based pattern, except for Gemini 3.1
one refinement cycle. A critic prompt receives the
                                                                       Flash-Lite which achieves better scores than Gem-
premise-hypothesis pair together with LangPro’s
                                                                       ini 3.5 Flash. Interestingly, Gemini 3.1 Flash-Lite
proof outcome, tableau closure information, and
                                                                       also substantially outperforms Claude Haiku 4.5
the attempted KB, and diagnoses possible missing
                                                                       and GPT-5.4 Mini, from a comparable product tier.
or inappropriate relations. A subsequent LLM call
                                                                       GPT-5.4 Mini, GPT-OSS-20B, and Gemma 3 4B
uses this diagnosis to generate a revised KB, after
                                                                       scored substantially lower than the remaining mod-
   9
      We opt for micro-F1 because it gives greater weight to           els, with Gemma 3 4B performing worst overall
larger LEX sets and is less influenced by the 29% of examples          and falling below the WordNet & Rules baseline on
with empty LEX sets than macro-F1.
   10                                                                     11
      We POS-tag the original premise and hypothesis and lo-                 WordNet & Rules represents a realistic rule-based base-
cate words of each argument in either sentence. The corre-             line using the heuristic that the first and second components
sponding tags are mapped to WordNet’s noun, verb, adjective,           of a relation typically come from the premise and hypothesis,
or adverb categories, and NLTK’s WordNet lemmatizer is used            respectively, while words shared by the premise and hypothe-
to get the lemma for a word-tag pair. Tokens for which this            sis are rarely part of such relations. It uses spaCy (Honnibal
procedure fails remain unchanged. We also apply lemmatiza-             et al., 2020) for lemmatization and POS tagging, with POS
tion to the reference relations because they contain plural-only       tags used to select the corresponding WordNet senses. During
nouns such as “glasses”, “pants”, and “shades”, and this might         WordNet lookup, we use the transitive closure of hypernymy,
increase the chance of a match.                                        entailment, and similarity relations.


                                                                   6
                                     Exact                              Micro-F1                         Micro-         Micro-
 Model                   Support     match                                                              Precision       Recall
                                                    Raw ↓            ∆ Lem.    ∆ Un.   ∆ Lem.+Un.
 Claude Sonnet 4.5       100.0     58.2 (± 0.2)   73.1 (± 0.2)       +0.9       +0.6       +1.5        64.5 (± 0.2)   84.2 (± 0.3)
 Gemini 3.1 Flash-Lite   100.0     57.9 (± 0.4)   72.3 (± 0.5)       +0.4       +0.0       +0.4        64.4 (± 0.4)   82.6 (± 0.6)
 Gemini 3.5 Flash        100.0     58.1 (± 0.4)   71.9 (± 0.4)       +1.0       +0.4       +1.4        63.6 (± 0.4)   82.6 (± 0.5)
 ■ WordNet & Oracle      100.0     64.1           70.5                 –         –           –        100.0           54.4
 GPT-5.4                 100.0     57.5 (± 1.0)   69.3 (± 0.4)       +0.7       +0.4       +1.1        61.0 (± 0.4)   80.2 (± 0.7)
 Claude Haiku 4.5        100.0     50.6 (± 0.0)   67.2 (± 0.0)       +1.6       +0.0       +1.6        57.1 (± 0.0)   81.8 (± 0.0)
 GPT-5.4 Mini            100.0     38.7 (± 1.2)   56.0 (± 1.1)       +7.3       +0.3       +7.8        46.3 (± 0.9)   71.0 (± 1.5)
 GPT-OSS-20B              99.8     44.0 (± 1.1)   55.0 (± 0.9)       +4.5       +0.2       +4.7        48.8 (± 0.7)   63.0 (± 1.3)
 ■ WordNet & Rules       100.0     50.0           51.0                 –         –           –         70.2           40.0
 Gemma 3 4B               98.1     14.1 (± 0.3)   30.6 (± 0.3)       +11.5      +0.1       +12.1       21.4 (± 0.2)   53.8 (± 0.3)
 ■ Empty LEX             100.0     37.0            0.0                 –         –           –        100.0            0.0

Table 3: LLMs’ results on the LEX-NLI task. Values are reported as the mean (± sample standard deviation) across
five runs. Results are sorted by raw Micro-F1, computed without post-processing. ∆ Lem., ∆ Un., and ∆ Lem.+Un.
report gains over raw Micro-F1 under lemmatized, argument-order-agnostic (A ⊑ B matches B ⊑ A), and combined
scoring, respectively. Support is the percentage of problems evaluated; exclusions are due to error responses from
API calls. ■ denotes baseline and oracle systems.


both EM and micro-F1, as well as below the Empty                        Overall, the results show substantial room for
LEX baseline on EM.                                                  improvement on the LEX-NLI task. The best model
   The substantially higher recall than precision                    trails annotator performance by 22.7 points in EM
suggests systematic overgeneration. Across the                       and 11.8 points in micro-F1. Even under the more
top five models, predicted LEX sets average 1.4                      model-friendly evaluation, where problems classi-
relations, compared with 1.0 for the reference LEX                   fied as non-entailment are excluded rather than pe-
sets. Relative to the references, models produce                     nalized (see Table 5 in Appendix D), the best scores
fewer empty sets (15% vs 29%) and more sets of                       remain below average annotator performance, with
size 2 (25% vs 14%) and 3+ (11% vs 6%). Due                          gaps of 13.9 percentage points in EM and 7.1 in
to the models’ tendency to overgenerate relations,                   micro-F1.12
WordNet & Oracle provides a strong baseline. This
                                                                     7.2      Using LEX to Prove Entailments
suggests that selecting the correct lexical spans is a
major challenge of the task.                                         Table 4 reports the number of entailment proofs
   Table 3 also reports micro-F1 under lemmatized                    constructed by LangPro for 1,000 SNLI entailment
and/or argument-order-agnostic matching. Ignor-                      problems. When using only WordNet as its lex-
ing inflectional differences increases micro-F1 for                  ical KB, LangPro proves 157 problems. We ad-
all models, but the gain is small for the top five                   ditionally evaluate four configurations in which
models (≤1.6 points) and substantially larger for                    the lexical KB is generated by an LLM either in
the remaining models (≥4.5 points). This suggests                    one-shot mode (LLM1 ) or agentic mode (LLMa ),
that producing lemmatized arguments is not a ma-                     with the generated KB optionally complemented by
jor difficulty for the better-performing models.                     WordNet (LLMWN              WN
                                                                                     1 and LLMa , respectively). Due
                                                                     to budget constraints, we conduct this experiment
   Ignoring argument order has a much smaller ef-
                                                                     with five small models.
fect (≤0.6 points). We hypothesize that this reflects
                                                                        The extrinsic evaluation results show that the
a combination of models distinguishing more spe-
                                                                     model ranking differs from that observed on the
cific from more general concepts and exploiting the
                                                                     LEX -NLI task. While Gemini 3.1 Flash-Lite and
heuristic that the specific concepts usually occur in
                                                                     Claude Haiku 4.5 remain the strongest models in
the premise and the general ones in the hypothesis.
                                                                     the LLM1 setting, they are outperformed by other
Note that among the eight entailment examples in
                                                                     models in the remaining three configurations.
the nine-shot prompt, we deliberately included one
                                                                        The relatively small gains of LLM1 over the
example that violates this heuristic (Example 7 in
                                                                     LangPro+WordNet baseline (see ∆WN values in
Appendix B). However, because entailment NLI
problems rarely include such adversarial cases, we                      12
                                                                          Additionally, while prompt engineering was not extensive,
included only one example in the prompt.                             the selection was biased toward the test set; see Appendix C.


                                                                 7
                                      LLM1               LLMa                LLMWN
                                                                                1         LLMWN
                                                                                             a
             Model
                                       ∆WN           ∆WN          ∆a          ∆WN         ∆WN       ∆a

             Gemini 3.1 Flash-Lite   165   +8     180    +23       +15      179   +22   193   +36    +14
             Claude Haiku 4.5        165   +8     176    +19       +11      179   +22   190   +33    +11
             GPT-5.4 Mini            162   +5     183    +26       +21      178   +21   199   +42    +21
             GPT-OSS-20B             158   +1     194    +37       +36      174   +17   212   +55    +38
             Gemma 3 4B              163   +6     163        +6        +0   182   +25   182   +25        +0


Table 4: LangPro proof coverage on 1,000 SNLI entailment problems when using various sources of the lexical KB.
LLM1 and LLMa denote one-shot and agentic LLM-generated LEX, while LLMWN                       WN
                                                                                    1 and LLMa are the former
two coupled with WordNet, respectively. Values indicate the number of problems proved as entailment. The
LangPro+WordNet baseline proves 157 problems. The boxed ∆WN values indicate gains over LangPro+WordNet,
while ∆a values indicate the additional gains from agentic inference over the corresponding non-agentic LLM.


LLM1 ) do not appear to arise simply because the             8         Analysis
LLM-generated relations are largely subsumed by
WordNet. When combined with WordNet, each                    8.1        Predicting Lexical Explanations
model still generates relations enabling additional          We examine the NLI problems and the predicted
proofs, see the ∆WN values in the LLMWN      1 and           LEX sets to understand the type of mistakes models
LLMWN a   columns.    In  the one-shot setting with          make. For 33 problems (9%), no model predicts
                 WN
WordNet (LLM1 ), Gemma 3 4B performs best,                   any of the reference LEX sets exactly. Our analysis
with 182 proofs, whereas GPT-OSS-20B performs                of these cases yields three main observations.
best in the agentic setting LLMWN
                                a , with 212 proofs.            Overgeneration of variants: Models fre-
                                                             quently overgenerate variants of the same semantic
                                                             relation (in roughly half of the cases), most
   Agentic generation improves proof coverage for
                                                             often differing only in inflection. Examples
all models except Gemma 3 4B, indicating that
                                                             include shades ⊑ glasses alongside shade ⊑ glass,
Gemma cannot successfully revise the relations
                                                             cartoon ⊑ animated alongside cartoon ⊑ animate,
produced in its initial attempt. GPT-OSS-20B ben-
                                                             and stereo equipment ⊑ audio equipment alongside
efits most from agentic generation, improving over
                                                             stereo ⊑ audio. Such overgeneration lowers pre-
the corresponding one-shot configurations by 36
                                                             cision and micro-F1 but does not affect recall.
proofs without WordNet and 38 proofs with Word-
                                                             The extent of this penalty is reflected in the
Net. It consequently achieves the best overall result,
                                                             improvement obtained with lemmatized micro-F1
with 212 proofs in the LLMWN  a configuration.
                                                             (Table 3). Additional prompt instructions could
                                                             likely reduce variant overgeneration, although this
  We also conducted an extrinsic evaluation on the           would not improve recall.
LEX test set (see Table 6 in Appendix D). The per-              Overgeneration of phrasal relations: LEX-
formance gaps between models are substantially               NLI specifically targets lexical relations and ex-
narrower than on LEX-NLI, indicating that the ex-            cludes phrasal ones. For example, for the en-
trinsic evaluation is coarser-grained and captures a         tailment snippets “man painting a picture” and
different aspect of model quality. The LEX test              “man is creating art”, it expects the explanation
set also appears easier: proof coverage is typi-             {paint ⊑ create, picture ⊑ art}. However, no model
cally around 1.5-1.9 times as high as on the 1,000-          predicted either relation, often opting instead
problem SNLI sample, while gains over the Word-              for phrasal relations such as paint ⊑ create art or
Net baseline are substantially larger. In the LLMWN
                                                 a           paint picture ⊑ create art, more natural in this case.
setting, all but one model exceed the 34% accuracy           Although the lexical-phrasal distinction is relatively
of the LangPro-LEX oracle, where LangPro is sup-             clear from a syntactic perspective, the annotation
plied with the union of the reference LEX sets. This         guidelines, which were also used as the prompt,
suggests that, despite suboptimal intrinsic perfor-          deliberately avoided syntax-heavy terminology.
mance on LEX-NLI, LLM-generated lexical knowl-                  Issues with references: Several correct predic-
edge can have an extrinsic effect comparable to the          tions were unfairly penalized because the refer-
curated reference LEX sets.                                  ences contained wrong relations instead of correct

                                                         8
ones (look out ⊑ view instead of look out over ⊑ view),       LLMs can recover much of the required lexical
omitted valid ones (make ⊑ cause as in “make                  knowledge, but the task remains challenging. Un-
laugh” and “cause to be merry”), or lacked ac-                der the primary evaluation, the best-performing
ceptable variants (having decorated ⊑ nice, but not           LLM reaches 73.1 micro-F1 and 58.2 EM (Table 3),
highly decorated ⊑ nice).                                     trailing average annotator performance by 11.8 and
                                                              22.7 points, respectively. Under the more model-
8.2    Supplying Knowledge to LangPro                         friendly evaluation, which excludes problems pre-
To assess the additional contribution of the agen-            dicted as non-entailment, the best per-metric scores
tic mode over one-shot generation, we manually                increase to 77.8 micro-F1 and 67.0 EM (Table 5),
analyzed the 15/14 additional problems solved by              reducing the corresponding gaps to 7.1 and 13.9
LLMa /LLMWN                                  WN               points. Models particularly struggle with overgen-
             a compared with LLM1 /LLM1 for
Gemini 3.1 Flash-Lite. The added relations for                erating relations, including inflectional variants,
these problems are shown in Table 8 and Table 7,              and with selecting minimal argument spans that
respectively, in Appendix D. Only five of the an-             constitute valid lexical entities.
alyzed problems contain at least one relation we                 Our extrinsic evaluation shows that LLM-
judged semantically reasonable in isolation. In               generated KBs can enable LangPro, a natural-logic
the remaining cases, the additional relations help            theorem prover, to find additional formal proofs.
LangPro prove the problem either by compensat-                LLMs can supply lexical relations that are absent
ing for errors introduced by the CCG parser or                from WordNet, while the agentic setting, which
by exploiting weaknesses in LangPro’s represen-               revises an initial KB once, further improves proof
tation or proof procedure. For example, for the               coverage. However, much of this additional gain
problem P: “Two skiers stand near a snowy moun-               comes from semantically unsound relations that
tain.” and H: “Some humans standing.”, LangPro                compensate for errors in the syntactic analysis of
fails to construct a proof even when LLMWN                    the input. On the LEX test set, the agentic set-
                                            1 pro-
vides skier ⊑ human. This is because “standing” in            ting even surpasses LangPro supplied with oracle
the hypothesis is analyzed as a noun with lemma               reference relations, illustrating that higher proof
“standing” by the NLP tools used in LangPro’s syn-            coverage does not necessarily imply better lexical
tactic pipeline. When LLMWN                                   knowledge.
                              a additionally pro-
poses stand ⊑ standing and standing ⊑ stand, Lang-               Overall, the results support a neuro-symbolic
Pro succeeds; the resulting proof requires only               division of labor in which LLMs supply flexible
stand ⊑ standing together with skier ⊑ human. An-             lexical knowledge and symbolic systems perform
other type of tool error that these relations can             explicit reasoning, while structured lexical evalua-
compensate for involves confusing particles and               tion provides an independent check on whether the
prepositions. Such cases illustrate that the agen-            supplied knowledge genuinely explains the infer-
tic mode can improve proof success by repairing               ence.
parser-induced lexical mismatches when supplying                 As future work, we plan to scale up the LEX-NLI
reasonable lexical knowledge is not enough.                   task to cover all SICK problems and a larger por-
                                                              tion of SNLI. To make this feasible, we will com-
9     Conclusion & Future Work                                bine manual validation with automatic candidate-
                                                              LEX detection using LangPro supplied with LLM-
To our knowledge, this is the first work that aug-            generated lexical knowledge. As the analysis of
ments existing naturalistic NLI problems with                 model outputs in § 8.1 reveals, a few overgenerated
structured lexical explanations of the knowledge re-          relations are in fact valid; we therefore plan to use
quired for their reasoning. Unlike prior lexical rela-        them to refine the reference annotations and im-
tion detection work (Vulić et al., 2017; Schmitt and         prove their completeness as we develop the dataset.
Schütze, 2019; Shwartz and Dagan, 2016), among                In the longer term, we aim to extend structured NLI
others, our task requires identifying only the rela-          explanations beyond entailment to other NLI labels
tions needed to explain a particular inference. We            and to richer explanatory structures that capture
operationalize these explanations as LEX sets and             reasoning beyond lexical entailment as outlined in
construct a manually annotated test set that retains          Abzianidze (2025).
multiple references when necessary.
   Our intrinsic evaluation on LEX-NLI shows that

                                                          9
Limitations                                                    Lasha Abzianidze. 2020. Learning as abduction: Train-
                                                                 able natural logic theorem prover for natural language
Our study is restricted to NLI problems with an                  inference. In Proceedings of the Ninth Joint Confer-
entailment label. This choice allows us to study lex-            ence on Lexical and Computational Semantics, pages
ical entailments in a relatively well-defined setting,           20–31, Barcelona, Spain (Online). Association for
                                                                 Computational Linguistics.
but leaves contradiction and neutral cases unex-
plored. Extending structured explanations to these             Lasha Abzianidze. 2025. Formal proofs as struc-
labels is less straightforward, as their reasoning               tured explanations: Proposing several tasks on ex-
may depend on incompatibility, negation, missing                 plainable natural language inference. Preprint,
                                                                 arXiv:2311.08637.
information, or pragmatic assumptions rather than
directed lexical entailments alone.                            Badr AlKhamissi, Millicent Li, Asli Celikyilmaz, Mona
   We also deliberately restrict explanations to lex-            Diab, and Marjan Ghazvininejad. 2022. A review
ical entailments over words and multi-word con-                  on language models as knowledge bases. Preprint,
                                                                 arXiv:2204.06031.
cepts. Such relations often constitute an impor-
tant component of entailment reasoning, but they               Rami Aly, Marek Strong, and Andreas Vlachos. 2023.
do not provide a complete account of the infer-                  QA-NatVer: Question answering for natural logic-
                                                                 based fact verification. In Proceedings of the 2023
ence. LEX sets abstract away from syntactic rea-                 Conference on Empirical Methods in Natural Lan-
soning, argument structure, quantification, corefer-             guage Processing, pages 8376–8391, Singapore. As-
ence, event relations, and other compositional or                sociation for Computational Linguistics.
world-knowledge phenomena. Our results should
                                                               Samuel R. Bowman, Gabor Angeli, Christopher Potts,
therefore be interpreted as evaluating one crucial               and Christopher D. Manning. 2015. A large anno-
structured component of explanation rather than                  tated corpus for learning natural language inference.
complete explanations of NLI reasoning.                          In Proceedings of the 2015 Conference on Empiri-
   Finally, the annotation task itself also admits gen-          cal Methods in Natural Language Processing, pages
                                                                 632–642, Lisbon, Portugal. Association for Compu-
uine explanatory variation, as evidenced by cases
                                                                 tational Linguistics.
in which several LEX variants remained valid after
adjudication. Although our multi-reference evalua-             Oana-Maria Camburu, Tim Rocktäschel, Thomas
tion (with the 4th LEX added during the annotation               Lukasiewicz, and Phil Blunsom. 2018. e-snli: natu-
                                                                 ral language inference with natural language expla-
adjudication phase) accounts for the retained al-                nations. In Proceedings of the 32nd International
ternatives, the reference set may not exhaust all                Conference on Neural Information Processing Sys-
semantically acceptable explanations.                            tems, NIPS’18, page 9560–9572, Red Hook, NY,
                                                                 USA. Curran Associates Inc.
Acknowledgments
                                                               Samuel Carton, Surya Kanoria, and Chenhao Tan. 2022.
We thank the three anonymous reviewers for their                 What to learn, and how: Toward effective learning
constructive feedback and helpful suggestions.                   from rationales. In Findings of the Association for
                                                                 Computational Linguistics: ACL 2022, pages 1075–
This work was supported by the Dutch Research                    1088, Dublin, Ireland. Association for Computational
Council (NWO) through the project Towards Ex-                    Linguistics.
plainable Natural Language Reasoning for Artifi-
cial Intelligence (project number DXQIL95775).                 Zeming Chen, Qiyue Gao, and Lawrence S. Moss. 2021.
                                                                 NeuralLog: Natural language inference with joint
This paper grew out of a student project conducted               neural and logical reasoning. In Proceedings of
within the course Reasoning with Natural Lan-                    *SEM 2021: The Tenth Joint Conference on Lexical
guage (TLMV25020) at Utrecht University.                         and Computational Semantics, pages 78–88, Online.
                                                                 Association for Computational Linguistics.

                                                               Peter Clark, Oyvind Tafjord, and Kyle Richardson. 2020.
References                                                       Transformers as soft reasoners over language. In
Lasha Abzianidze. 2017a. Langpro: Natural language               Proceedings of the Twenty-Ninth International Joint
  theorem prover. In Proceedings of the 2017 Con-                Conference on Artificial Intelligence, IJCAI’20.
  ference on Empirical Methods in Natural Language
  Processing: System Demonstrations, pages 115–120,            Ido Dagan, Oren Glickman, and Bernardo Magnini.
  Copenhagen, Denmark. Association for Computa-                  2006. The pascal recognising textual entailment chal-
  tional Linguistics.                                            lenge. In Proceedings of the PASCAL Challenges
                                                                 Workshop on Recognising Textual Entailment, Re-
Lasha Abzianidze. 2017b. A natural proof system for              search in Computational Semantics, pages 177–190.
  natural language. Ph.D. thesis, Tilburg University.            Springer-Verlag.


                                                          10
Ido Dagan, Dan Roth, Mark Sammons, and Fabio Mas-             Marco Marelli, Stefano Menini, Marco Baroni, Luisa
   simo Zanzotto. 2013. Recognizing Textual Entail-            Bentivogli, Raffaella Bernardi, and Roberto Zampar-
   ment: Models and Applications. Synthesis Lectures           elli. 2014. A sick cure for the evaluation of compo-
   on Human Language Technologies. Morgan & Clay-              sitional distributional semantic models. In Proceed-
   pool Publishers.                                            ings of the Ninth International Conference on Lan-
                                                               guage Resources and Evaluation (LREC’14), pages
Bhavana Dalvi, Peter Jansen, Oyvind Tafjord, Zhengnan          216–223, Reykjavik, Iceland. European Language
  Xie, Hannah Smith, Leighanna Pipatanangkura, and             Resources Association (ELRA).
  Peter Clark. 2021. Explaining answers with entail-
  ment trees. In Proceedings of the 2021 Conference           Bill Noble, Rasmus Blanck, and Gijs Wijnholds. 2025.
  on Empirical Methods in Natural Language Process-              In the mood for inference: Logic-based natural lan-
  ing, pages 7358–7370, Online and Punta Cana, Do-               guage inference with large language models. In
  minican Republic. Association for Computational               Proceedings of the 5th Workshop on Natural Logic
  Linguistics.                                                  Meets Machine Learning (NALOMA), pages 33–47,
                                                                 Bochum, Germany. Association for Computational
Jay DeYoung, Sarthak Jain, Nazneen Fatema Rajani,                Linguistics.
  Eric Lehman, Caiming Xiong, Richard Socher, and
  Byron C. Wallace. 2020. ERASER: A benchmark to              Theo Olausson, Alex Gu, Ben Lipkin, Cedegao Zhang,
  evaluate rationalized NLP models. In Proceedings              Armando Solar-Lezama, Joshua Tenenbaum, and
  of the 58th Annual Meeting of the Association for             Roger Levy. 2023. LINC: A neurosymbolic approach
  Computational Linguistics, pages 4443–4458, Online.           for logical reasoning by combining language models
  Association for Computational Linguistics.                    with first-order logic provers. In Proceedings of the
                                                                2023 Conference on Empirical Methods in Natural
C. Fellbaum. 1998. WordNet: An Electronic Lexical               Language Processing, pages 5153–5176, Singapore.
  Database. Language, Speech and Communication.                 Association for Computational Linguistics.
  Mit Press.
                                                              Liangming Pan, Alon Albalak, Xinyi Wang, and
Octavian Ganea, Gary Becigneul, and Thomas Hof-
                                                                William Wang. 2023. Logic-LM: Empowering large
  mann. 2018. Hyperbolic entailment cones for learn-
                                                                language models with symbolic solvers for faithful
  ing hierarchical embeddings. In Proceedings of the
                                                                logical reasoning. In Findings of the Association
  35th International Conference on Machine Learn-
                                                                for Computational Linguistics: EMNLP 2023, pages
  ing, volume 80 of Proceedings of Machine Learning
                                                                3806–3824, Singapore. Association for Computa-
  Research, pages 1646–1655. PMLR.
                                                                tional Linguistics.
Mohammad Reza Ghasemi Madani and Pasquale Min-
 ervini. 2023. REFER: An end-to-end rationale ex-             Fabio Petroni, Tim Rocktäschel, Sebastian Riedel,
 traction framework for explanation regularization. In          Patrick Lewis, Anton Bakhtin, Yuxiang Wu, and
 Proceedings of the 27th Conference on Computa-                 Alexander Miller. 2019. Language models as knowl-
 tional Natural Language Learning (CoNLL), pages                edge bases? In Proceedings of the 2019 Confer-
 587–602, Singapore. Association for Computational              ence on Empirical Methods in Natural Language Pro-
 Linguistics.                                                   cessing and the 9th International Joint Conference
                                                                on Natural Language Processing (EMNLP-IJCNLP),
Simeng Han, Hailey Schoelkopf, Yilun Zhao, Zhent-               pages 2463–2473, Hong Kong, China. Association
  ing Qi, Martin Riddell, Wenfei Zhou, James Coady,             for Computational Linguistics.
  David Peng, Yujie Qiao, Luke Benson, Lucy Sun,
  Alexander Wardle-Solano, Hannah Szabó, Ekaterina            Hyun Ryu, Gyeongman Kim, Hyemin S. Lee, and
  Zubova, Matthew Burtell, Jonathan Fan, Yixin Liu,             Eunho Yang. 2025. Divide and translate: Composi-
  Brian Wong, Malcolm Sailor, and 16 others. 2024.              tional first-order logic translation and verification for
  FOLIO: Natural language reasoning with first-order            complex logical reasoning. In The Thirteenth Inter-
  logic. In Proceedings of the 2024 Conference on               national Conference on Learning Representations.
  Empirical Methods in Natural Language Processing,
  pages 22017–22031, Miami, Florida, USA. Associa-            Abulhair Saparov and He He. 2023. Language models
  tion for Computational Linguistics.                           are greedy reasoners: A systematic formal analysis
                                                                of chain-of-thought. In The Eleventh International
Matthew Honnibal, Ines Montani, Sofie Van Lan-                  Conference on Learning Representations.
 deghem, and Adriane Boyd. 2020. spaCy: Industrial-
 strength Natural Language Processing in Python.              Martin Schmitt and Hinrich Schütze. 2019. SherLIiC: A
                                                                typed event-focused lexical inference benchmark for
Honoka Kobayashi, Hinari Daido, and Daisuke Bekki.              evaluating natural language inference. In Proceed-
  2026. Neural DTS: Integrating hyperbolic classifiers          ings of the 57th Annual Meeting of the Association for
  into natural language inference systems. In Proceed-         Computational Linguistics, pages 902–914, Florence,
  ings of the 6th Workshop on Natural Language Meets            Italy. Association for Computational Linguistics.
  Logic and Machine Learning (NALOMA), pages 9–
  18, Prague, Czechia. Association for Computational          Vered Shwartz and Ido Dagan. 2016. Adding context to
  Linguistics.                                                  semantic data-driven paraphrasing. In Proceedings


                                                         11
  of the Fifth Joint Conference on Lexical and Compu-           Wanjun Zhong, Siyuan Wang, Duyu Tang, Zenan Xu,
  tational Semantics, pages 108–113, Berlin, Germany.            Daya Guo, Yining Chen, Jiahai Wang, Jian Yin, Ming
  Association for Computational Linguistics.                     Zhou, and Nan Duan. 2022. Analytical reasoning of
                                                                 text. In Findings of the Association for Computa-
Robyn Speer, Joshua Chin, and Catherine Havasi. 2017.            tional Linguistics: NAACL 2022, pages 2306–2319,
  Conceptnet 5.5: An open multilingual graph of gen-             Seattle, United States. Association for Computational
  eral knowledge. In AAAI Conference on Artificial               Linguistics.
  Intelligence, pages 4444–4451.
Joe Stacey, Pasquale Minervini, Haim Dubossarsky, and
   Marek Rei. 2022. Logical reasoning with span-level
   predictions for interpretable and robust NLI models.
   In Proceedings of the 2022 Conference on Empiri-
   cal Methods in Natural Language Processing, pages
   3809–3823, Abu Dhabi, United Arab Emirates. As-
   sociation for Computational Linguistics.
Marek Strong, Rami Aly, and Andreas Vlachos. 2024.
 Zero-shot fact verification via natural logic and large
 language models. In Findings of the Association
 for Computational Linguistics: EMNLP 2024, pages
 17021–17035, Miami, Florida, USA. Association for
 Computational Linguistics.
Akiyoshi Tomihari and Hitomi Yanaka. 2023. Logic-
  based inference with phrase abduction using vision-
  and-language models. IEEE Access, 11:45645–
  45656.
Théo Trouillon, Johannes Welbl, Sebastian Riedel, Éric
  Gaussier, and Guillaume Bouchard. 2016. Complex
  embeddings for simple link prediction. In Proceed-
  ings of the 33rd International Conference on Interna-
  tional Conference on Machine Learning - Volume 48,
  ICML’16, page 2071–2080. JMLR.org.
Ivan Vulić, Daniela Gerz, Douwe Kiela, Felix Hill, and
   Anna Korhonen. 2017. HyperLex: A large-scale eval-
   uation of graded lexical entailment. Computational
   Linguistics, 43(4):781–835.
Hitomi Yanaka, Koji Mineshima, Pascual Martínez-
  Gómez, and Daisuke Bekki. 2018. Acquisition
  of phrase correspondences using natural deduction
  proofs. In Proceedings of the 2018 Conference of
  the North American Chapter of the Association for
  Computational Linguistics: Human Language Tech-
  nologies, Volume 1 (Long Papers), pages 756–766,
  New Orleans, Louisiana. Association for Computa-
  tional Linguistics.
Masashi Yoshikawa, Koji Mineshima, Hiroshi Noji, and
  Daisuke Bekki. 2019. Combining axiom injection
  and knowledge base completion for efficient natural
  language inference. In Proceedings of the Thirty-
 Third AAAI Conference on Artificial Intelligence and
 Thirty-First Innovative Applications of Artificial In-
  telligence Conference and Ninth AAAI Symposium
  on Educational Advances in Artificial Intelligence,
 AAAI’19/IAAI’19/EAAI’19. AAAI Press.
Xinyan Zhao and V. G. Vinod Vydiswaran. 2021. Lirex:
  Augmenting language inference with relevant expla-
  nations. In Proceedings of the AAAI Conference
  on Artificial Intelligence, volume 35, pages 14532–
  14539.


                                                           12
A      LLM Inference Setup                                          hypothesis sentence.
                                                                    You will reason carefully and decide whether the premise
The models were accessed through the OpenRouter                     entails the hypothesis. Entailment means that if the
Chat Completions interface. The model identifiers                   premise is true, then the hypothesis must also be true
                                                                    under ordinary English meaning and widely accepted
record the versions requested from OpenRouter, but                  background knowledge.
they are not pinned provider snapshots. The under-                  If the answer is entailment, output a structured ex-
lying snapshots were not retained in the response                   planation consisting of a set of lexical entailment re-
                                                                    lations over short phrases that explain why the hy-
metadata. In the final model comparison, every                      pothesis is entailed by the premise. A lexical entail-
model was evaluated on the test data five times us-                 ment must be defined over short phrases that are lem-
ing the same nine-example few-shot prompt (see                      matized or normalized versions of expressions occur-
                                                                    ring in the premise and hypothesis. Use the format
Appendix B). Repetition was used to quantify                        phrase_1 ⊑ phrase_2. The relation means that phrase_1
variation caused by nondeterministic model and                      is a type of, or semantically entails, phrase_2. Ex-
                                                                    amples include woman ⊑ person, dog ⊑ domestic animal,
provider behaviour. A temperature of 0 was re-                      huge ⊑ very big, and run ⊑ move fast.
quested, but this did not guarantee identical out-                  Use lexical entailment relations only when they are
puts because temperature support was not uniform                    needed to explain the entailment. If the entailment fol-
                                                                    lows without any non-trivial lexical relation, output an
across the evaluated OpenRouter routes and the set-                 empty set.
ting could be ignored by a provider. Requests were
                                                                    Relation-formatting rules
issued with a concurrency of four, a 120-second
                                                                    1. The meaning of a lexical entailment relation must
timeout, and at most two retries. No common                            be acceptable according to ordinary common-sense
top_p, random seed, reasoning-effort setting, stop                     knowledge. For example, woman ⊑ blond person is
sequence, or explicit output-token limit was sup-                      not acceptable.
plied. The total budget of the experiments was                      2. A lexical entailment may not express a trivial relation
under $80.                                                             that can be obtained simply by discarding modifiers.
                                                                       For example, blond woman ⊑ woman is not acceptable.

B      Annotation Guidelines and LLM                                3. A lexical entailment may not contain redundant
                                                                       words such as auxiliary verbs or the infiniti-
       Prompt                                                          val marker to. For example, will walk ⊑ will move,
                                                                       is red ⊑ is colored, and to walk ⊑ to move are not ac-
The following instructions were used both as anno-                     ceptable.
tation guidelines for constructing the gold-standard                4. The words in each phrase must be lemmatized. For
structured explanations and as the prompt given to                     example, dogs ⊑ domestic animals is not acceptable.
the evaluated LLMs. The placeholders $PREMISE                       5. Phrases may not contain determiners. For example,
and $HYPOTHESIS were replaced with the premise                         a dog ⊑ a domestic animal is not acceptable.
and hypothesis of each NLI problem.                                 6. Phrases may not contain prepositional phrases. For
   Following § 3, the guidelines define a LEX as                       example, dog with spots ⊑ domestic animal is not ac-
the smallest set of directed lexical entailment rela-                  ceptable.
tions needed to explain how the hypothesis follows                  Example 1
from the premise, when it does. The instructions re-                Premise: Young ladies are playing the guitar.
quire short, factually acceptable argument phrases                  Hypothesis: A musical instrument is being played by
                                                                    girls.
and emphasize four properties: (a) minimality re-                   Correct output:
quires the model to omit relations unnecessary for                  Answer: entailment
                                                                    Relations:                             {young lady ⊑ girl,
the inference or that follow merely by discarding                   guitar ⊑ musical instrument}
a modifier. (b) lemmatization requires canonical                    Unwanted output:
word forms without determiners, auxiliary verbs,                    Relations:                           {young ladies ⊑ girls,
                                                                    the guitar ⊑ a musical instrument}
or the infinitival marker to. (c) relation direction                Explanation: Phrases in relations may not contain deter-
requires the first argument to license the second                   miners such as a and the. The words ladies and girls must
in the direction needed for the inference. (d) out-                 be replaced by their lemmas, lady and girl, respectively.
put formatting requires the prescribed format for                   Example 2
non-empty relation sets.                                            Premise: A female swimmer getting out of the pool still
                                                                    dripping wet.
                                                                    Hypothesis: A woman gets out of the pool.
     Lexical-entailment annotation prompt                           Correct output:
    You are an expert in linguistic semantics and logic. You        Answer: entailment
    will receive a Natural Language Inference (NLI) prob-           Relations: {female swimmer ⊑ woman}
    lem in English, consisting of a premise sentence and a          Unwanted output:



                                                               13
Relations: {swimmer ⊑ woman}                                              because it does not account for the adjective small, which
Explanation: The proposed relation is factually incor-                    is crucial in the hypothesis.
rect because not every swimmer is a woman.
                                                                          Example 9
Example 3                                                                 Premise: A little boy is laughing and happily bouncing
Premise: A young girl wearing a pink coat plays with a                    on a trampoline outside.
yellow toy.                                                               Hypothesis: The child is jumping outdoors.
Hypothesis: A kid is swinging a toy golf club.                            Correct output:
Correct output:                                                           Answer: entailment
Answer: non-entailment                                                    Relations: {little boy ⊑ child, bounce ⊑ jump,
                                                                          outside ⊑ outdoors}
Example 4
                                                                          Unwanted output:
Premise: A black race car starts up in front of a crowd
                                                                          Relations: {boy ⊑ child, outdoors ⊑ outside}
of people.
                                                                          Explanation: The relation bounce ⊑ jump is missing.
Hypothesis: A car is running.
                                                                          The relation little boy ⊑ child is preferred to boy ⊑ child be-
Correct output:
                                                                          cause the former provides a more precise correspondence
Answer: entailment
                                                                          between the expressions in the premise and hypothesis.
Relations: {start up ⊑ run}
                                                                          The arguments of outdoors ⊑ outside must be reversed to
Unwanted output:
                                                                          align the relation with the direction of the inference.
Relations: {starts up ⊑ is running}
Explanation: The expressions starts up and is running                     Additional calibration while preserving all rules
are not lemmatized. The auxiliary verb is is also unnec-                  above:
essary.
                                                                           • Only output lexical entailment relations that are both
Example 5                                                                    factually acceptable and needed to explain the entail-
Premise: A woman dressed in red clothing is dancing                          ment.
inside a crowd of people.
Hypothesis: A woman in red is dancing in a crowd.                          • Do not output relations for entailments that follow
Correct output:                                                              without a non-trivial lexical bridge.
Answer: entailment                                                         • Do not use event or social implications as lexical
Relations: {}                                                                entailment unless the phrase relation is a direct para-
Unwanted output:                                                             phrase.
Relations: {in red clothing ⊑ in red}
Explanation: The arguments of a relation may not con-                      • Do not output modifier-dropping relations such as
tain prepositional phrases such as in red clothing.                          old woman → woman or military men → men.
Example 6                                                                  • Do not output both an inflected form and a lemma-
Premise: A tall man with a cap is climbing a cord.                           tized form for the same relation.
Hypothesis: The man in a hat is climbing a rope.
Correct output:                                                            • If the best relation would violate any existing format-
Answer: entailment                                                           ting rule, omit it instead of approximating it.
Relations: {cap ⊑ hat, cord ⊑ rope}
Unwanted output:                                                          Now process the following input while strictly following
Relations: {cap ⊑ hat, tall man ⊑ man}                                    the above instructions and formatting.
Explanation: The relation cord ⊑ rope is missing. The                     Output exactly in one of the following formats:
relation tall man ⊑ man is trivial because it only discards
the modifier tall.                                                              Answer: entailment
                                                                                Relations: { . . . }
Example 7                                                                       or
Premise: No person is cooking.                                                  Answer: non-entailment
Hypothesis: No cook is cooking in the kitchen.
Correct output:                                                           Input:
Answer: entailment
Relations: {cook ⊑ person}                                                      Premise: $PREMISE
Unwanted output:                                                                Hypothesis: $HYPOTHESIS
Relations: {person ⊑ cook}
Explanation: The unwanted relation does not explain                       Correct output:
the inference because negation reverses the permitted
direction of lexical substitution. It is also factually incor-
rect because not every person is a cook.
                                                                      C      Prompt Selection
Example 8
Premise: A person who is obese is holding a chinchilla.               Preliminary prompt-selection experiments com-
Hypothesis: A fat person is holding a small animal.
Correct output:                                                       pare four controlled variants on the unanimously
Answer: entailment                                                    agreed samples (223 out of 362) using four mod-
Relations: {chinchilla ⊑ small animal, obese ⊑ fat}
Unwanted output:
                                                                      els: GPT-5.4 mini, Claude Haiku 4.5, Gemini 3.1
Relations: {fat ⊑ obese, chinchilla ⊑ animal}                         Flash-Lite, and GPT-OSS-20B. Prompt variants are
Explanation: The arguments of fat ⊑ obese must be re-                 constructed by adding sections to the same base
versed to align the relation with the direction of the in-
ference. The relation chinchilla ⊑ animal is insufficient
                                                                      prompt. The zero-shot base condition contains only
                                                                      the task definition. The zero-shot constrained con-

                                                                 14
dition adds the relation-formatting rules from the
annotation guidelines. The few-shot base condi-
tion further adds nine worked examples, including
correct and unwanted outputs. Finally, the few-
shot precision condition adds a calibration block
discouraging speculative or unnecessary relations,
modifier deletion, and duplicate surface and lemma
forms. For each prompt-model combination, we
calculate multi-reference micro-F1. We then com-
pute the unweighted mean of the four model-level
micro-F1 scores for each prompt condition: 43.8
for zero-shot base, 53.5 for zero-shot constrained,
65.2 for few-shot base, and 69.2 for few-shot preci-
sion. Based on these results, we select the few-shot
precision prompt for the final experiments.

D   Mixture of Figures and Tables




                                                       15
                                     Exact                                 Micro-F1                         Micro-              Micro-
 Model                   Support     match                                                                 Precision            Recall
                                                    Raw ↓         ∆ Lem.          ∆ Un.    ∆ Lem.+Un.
 Gemini 3.1 Flash-Lite    89.0     65.1 (± 0.5)   77.8 (± 0.6)        +0.4        +0.0          +0.4      70.7 (± 0.5)     86.6 (± 0.7)
 Claude Sonnet 4.5        91.7     63.5 (± 0.2)   76.9 (± 0.2)        +1.0        +0.6          +1.5      69.2 (± 0.2)     86.7 (± 0.3)
 GPT-5.4                  85.7     67.0 (± 0.9)   76.6 (± 0.2)        +0.8        +0.4          +1.2      68.8 (± 0.4)     86.4 (± 0.2)
 Gemini 3.5 Flash         95.2     61.0 (± 0.5)   74.3 (± 0.5)        +1.1        +0.4          +1.5      66.0 (± 0.5)     85.0 (± 0.5)
 Claude Haiku 4.5         89.0     56.8 (± 0.0)   72.1 (± 0.0)        +1.7        +0.0          +1.7      62.2 (± 0.0)     85.8 (± 0.0)
 ■ WordNet & Oracle      100.0     64.1           70.5                  –          –              –      100.0             54.4
 GPT-OSS-20B              77.5     56.7 (± 1.2)   66.9 (± 0.7)        +5.5        +0.2          +5.7      60.1 (± 0.8)     75.3 (± 0.9)
 GPT-5.4 Mini             86.9     44.5 (± 1.1)   60.9 (± 0.8)        +7.9        +0.3          +8.4      50.8 (± 0.7)     75.8 (± 1.0)
 ■ WordNet & Rules       100.0     50.0           51.0                  –          –              –       70.2             40.0
 Gemma 3 4B               92.5     14.9 (± 0.4)   31.3 (± 0.3)        +11.8       +0.1          +12.4     21.9 (± 0.2)     55.0 (± 0.3)
 ■ Empty LEX             100.0     37.0            0.0                  –          –              –      100.0              0.0

Table 5: LLMs’ results on the LEX-NLI task. These scores are more favorable to the models, as examples assigned
a non-entailment label are omitted from evaluation; in contrast, Table 3 penalizes predictions on those examples.
Support is the percentage of problems evaluated; exclusions mostly result from models labeling problems as
non-entailment. ■ denotes baseline and oracle systems.




                                    LLM1 %                LLMa %                      LLMWN
                                                                                         1 %               LLMWN
                                                                                                              a %
         Model
                                       ∆WN                 ∆WN        ∆a                  ∆WN              ∆WN     ∆a

         Claude Sonnet 4.5         25.4   +7.2        32.0   +13.8         +6.6     30.1    +11.9       35.4   +17.1     +5.2
         Gemini 3.1 Flash-Lite     24.9   +6.6        31.8   +13.5         +6.9     29.3    +11.0       34.8   +16.6     +5.5
         Gemini 3.5 Flash          23.5   +5.2        33.4   +15.2         +9.9     28.2    + 9.9       37.0   +18.8     +8.8
         GPT-5.4                   24.3   +6.1        30.7   +12.4         +6.4     29.3    +11.0       35.6   +17.4     +6.4
         Claude Haiku 4.5          25.7   +7.5        31.2   +13.0         +5.5     30.9    +12.7       35.6   +17.4     +4.7
         GPT-5.4 Mini              23.8   +5.5        29.3   +11.0         +5.5     29.8    +11.6       34.8   +16.6     +5.0
         Gemma 3 4B                25.1   +6.9        25.1   + 6.9         +0.0     30.7    +12.4       30.7   +12.4     +0.0


Table 6: LangPro proof coverage on the test set (of 362 entailment problems) when using various sources of
the lexical KB. LLM and LLMa denote one-shot and agentic LLM-generated LEX, while LLMWN           1 and LLMa
                                                                                                               WN

are the former two coupled with WordNet, respectively. Values indicate the percentage of problems proved as
entailment. The LangPro+WordNet baseline proves 66 problems (18.2%). The boxed ∆WN values indicate gains
over LangPro+WordNet, while ∆a values indicate the additional gains from agentic inference over the corresponding
non-agentic LLM. GPT-OSS-20B is omitted because the model host was unresponsive when the experiments were
conducted.




                                                                 16
  Premise                                   Hypothesis                    Added/changed relations               Judgment
  Two skiers stand near a snowy             Some humans standing.         stand ⊑ standing; standing ⊑ stand Poor: inflection only; no new lexical
  mountain.                                                                                                  knowledge
                                                                          black dog ⊑ dog; running along ⊑
  A black dog is running along the          a dog is running on the       running on; run along ⊑ run on;    Poor: modifier dropping plus invalid
  beach.                                    beach                         along ⊑ on                         general substitution
                                                                          standing outside ⊑ outdoors;
  Safety officers standing outside.         Safety officers outdoors.                                        Poor: semantically plausible but
                                                                          stand outside ⊑ outdoors
                                                                                                             non-minimal
  A female is wearing a big purple          a girl with a flower in her   wear ⊑ with; have ⊑ with           Good: unusual pairs but specific to
  flower in her hair and has some beads     hair                                                             SNLI & SICK datasets
  around her neck.
  A man wearing a black hat, white          A man is performing.          swallow ⊑ perform                     Poor: valid only in the staged context
  shirt, red vest, black tie, and face
  makeup is swallowing a sword, while
  a man wearing a cowboy hat behind
  him is watching.
                                                                          little girl ⊑ girl; petting ⊑ has;
  A little girl is petting her white, fluffy The girl has a pet.                                                Poor: modifier dropping plus false
                                                                          pet ⊑ have
  cat.                                                                                                          possession inference
                                                                          little kids ⊑ children; little
  Little kids are on an amusement park      Children are on a ride.       kid ⊑ children; amusement park        Poor: unnormalized, non-minimal
  ride.                                                                   ride ⊑ ride                           modifier dropping
  Man in blue shirt playing water           The man is wearing blue       in ⊑ wearing; in ⊑ wear               Poor: valid only in a clothing
  instrument in an orchestra.                                                                                   construction
                                                                          on ⊑ in; mirror on the wall ⊑
  A man on an elevator looks at the         A person in the elevator                                            Poor: invalid preposition change plus
                                                                          mirror
  mirror on the wall.                       looks at a mirror.                                                  modifier dropping
  A child wearing a rainbow striped         A child has a toy.            push ⊑ have                           Poor: pushing does not entail possession
  shirt is pushing a toy cart.
  Young blond woman putting her foot        A person is dipping her       put into ⊑ dip into; put ⊑ dip        Poor: valid only for the foot–water
  into a water fountain                     foot into water.                                                    context
                                                                          tennis player ⊑ tennis playing;
  The blonde tennis player is wearing a     The tennis playing is         tennis player ⊑ tennis play;          Poor: participant–event category
  white shirt and a green tennis skirt.     wearing a green skirt.        player ⊑ playing                      mismatch
                                                                          adjusting ⊑ fixing; adjusting for
  Adjusting a tie for accuracy.             Fixing a tie.                 accuracy ⊑ fixing; adjust for         Poor: unnormalized and
                                                                          accuracy ⊑ fix                        context-dependent
  The bird’s feet are grasping the          there is a bird resting       grasp ⊑ rest                          Poor: grasping does not entail resting
  window tightly.


Table 7: Quality judgments for the 14 additional problems obtained by Gemini 3.1 Flash-Lite in LLMWN
                                                                                                  a  agentic
refinement over LLMWN1  . We  judge 1 case good,  0 mixed, and 13 poor.




                                                                              17
  Premise                                  Hypothesis                Added/changed relations                Judgment
  A black dog is walking through a         An animal is walking      black dog ⊑ animal; stream ⊑ water Good: both relations are generally valid;
  stream of water.                         through water.                                               black dog ⊑ animal is non-minimal
                                                                                                        but sound
  Two skiers stand near a snowy            Some humans standing.     stand ⊑ standing; standing ⊑ stand Poor: inflection only; no new lexical
  mountain.                                                                                             knowledge
                                                                     black dog ⊑ dog; running along ⊑
  A black dog is running along the         a dog is running on the   running on; run along ⊑ run on;    Poor: modifier dropping plus invalid
  beach.                                   beach                     along ⊑ on                         general substitution
                                                                     woman ⊑ women; women ⊑ woman; in ⊑
                                                                     wear; floral wedding dress ⊑
  An Asian woman in a floral wedding      An asian women is                                             Poor: inflection, context dependence,
                                                                     wedding dress; floral wed dress ⊑
  dress poses on a bridge close to her    wearing a wedding dress.                                      modifier dropping, and malformed forms
                                                                     wed dress
  bridesmaids.
  A lady walking down stairs with a        A woman walking down         lady ⊑ woman                        Good: generally valid lexical entailment
  green poster pod on her back.            stairs with a green thing on
                                           her back.
                                                                        standing outside ⊑ outdoors;
  Safety officers standing outside.        Safety officers outdoors.                                        Poor: semantically plausible but
                                                                        stand outside ⊑ outdoors
                                                                                                            non-minimal
                                                                     swallowing ⊑ performing; swallow
  A man wearing a black hat, white           A man is performing.                                           Poor: context-dependent and partly
                                                                     ⊑ perform
  shirt, red vest, black tie, and face                                                                      unlemmatized
  makeup is swallowing a sword, while
  a man wearing a cowboy hat behind
  him is watching.
  A black dog runs in the grass, its         The dog is outdoors.    run ⊑ outdoors                         Poor: running does not entail being
  tongue hanging out.                                                                                       outdoors
  A little girl is petting her white, fluffy The girl has a pet.     petting ⊑ having; pet ⊑ have           Poor: petting does not entail possession
  cat.
                                                                     little kids ⊑ children; little
  Little kids are on an amusement park     Children are on a ride.   kid ⊑ children; amusement park         Poor: unnormalized, non-minimal
  ride.                                                              ride ⊑ ride                            modifier dropping
  A child wearing a rainbow striped        A child has a toy.        push ⊑ have                            Poor: pushing does not entail possession
  shirt is pushing a toy cart.
  A guy kneeling down in front of a        A man bending down in     desk ⊑ furniture                       Good: valid normalized hypernym, but
  desk.                                    front of a piece of                                              not new semantic knowledge over
                                           furniture.                                                       one-shot
                                                                     lady ⊑ woman; making ⊑ cooking;
  An asian lady in a brown shirt with      A woman is cooking                                               Mixed: one valid relation; two
                                                                     make ⊑ cook
  glasses is making some food.                                                                              food-context-dependent mappings
                                                                     adjusting ⊑ fixing; adjusting for
  Adjusting a tie for accuracy.            Fixing a tie.             accuracy ⊑ fixing; adjust for          Poor: unnormalized and
                                                                     accuracy ⊑ fix                         context-dependent
  The bird’s feet are grasping the         there is a bird resting   grasp ⊑ rest                           Poor: grasping does not entail resting
  window tightly.


Table 8: Quality judgments for the 15 additional problems obtained by Gemini 3.1 Flash-Lite in LLMa agentic
refinement over LLM1 . We judge 3 cases good, 1 mixed, and 11 poor.




                                                                         18
