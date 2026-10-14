                                               MathAtlas: A Benchmark for Autoformalization
                                                                in the Wild


                                                       Nilay Patel†*                 Noah Arias                      Davit Babayan
                                                     nilay@ucsc.edu               ngarias@ucsc.edu                 dbabaya1@ucsc.edu

                                                      Victoria Cochran               Timothy Libman                 Hafsah Mahmood
arXiv:2605.14061v1 [cs.AI] 13 May 2026




                                                     vacochra@ucsc.edu              tlibman@ucsc.edu               hzmahmoo@ucsc.edu

                                                       Liam McCarty                    Soli Munoz                     Laurel Willey
                                                     lmccarty@ucsc.edu             mmunoz35@ucsc.edu               lwwilley@ucsc.edu

                                                                                    Jeffrey Flanigan*
                                                                                   jmflanig@ucsc.edu

                                                                            University of California, Santa Cruz
                                                                                     ∗
                                                                                       Primary authors
                                                                                     †
                                                                                       Correspondence



                                                                                         Abstract
                                                      Current autoformalization benchmarks are largely focused on olympiad or under-
                                                      graduate mathematics, while graduate and research-level mathematics remains
                                                      underexplored. In this paper, we introduce MathAtlas, the first large-scale auto-
                                                      formalization benchmark of in the wild graduate-level mathematics, containing
                                                      ∼ 52k theorems, definitions, exercises, examples, and proofs extracted from 103
                                                      graduate mathematics textbooks. MathAtlas is enriched with a mathematical de-
                                                      pendency graph containing ∼ 178k relations, and is the first autoformalization
                                                      benchmark to include such relations, facilitating evaluation and development of
                                                      dependency-aware autoformalization systems. Our extensive experiments show
                                                      that MathAtlas is high quality but extremely challenging: strong baselines achieve
                                                      at most 9.8% correctness on theorem statements and 16.7% on definitions. Fur-
                                                      thermore, we find performance of state-of-the-art models degrades substantially
                                                      with dependency depth: on MA-Hard, a subset of 700 entities with the deepest
                                                      dependency trees, the best model achieves only 2.6% correctness for autoformal-
                                                      ization on this challenging dataset. We release MathAtlas to the community as a
                                                      benchmark set for large-scale autoformalization of graduate-level mathematics in
                                                      the wild.


                                         1    Introduction
                                         The popularity of formal mathematics (computer verifiable mathematics) within the mathematics
                                         community has grown dramatically over recent years [30, 32, 15]. Together with advances in AI,
                                         this has caused a surge of interest in autoformalization [10, 36, 13, 3, 18], the task of automatically
                                         converting natural language math to a formal verifiable language such as Lean [24].
                                         Until recently, autoformalization work has been largely focused on simpler settings such as olympiad
                                         or undergraduate mathematics [3, 36, 41, 1, 2, 12, 19], where mathematical statements require limited

                                         Preprint.
Figure 1: An entity from MathAtlas together with a subgraph of its dependency tree. In yellow
(bottom), we have a target theorem statement to be formalized (Proposition 15). Proposition 15
contains three “object references” to previously defined mathematical concepts: Dedeking ring,
prime ideals, and principal ideal ring, which are dependencies needed to correctly formalize the
theorem. These objects each have their own dependency tree (shown with a red border), and so on.
Formalizations of objects possibly already exist (e.g., in Mathlib), or they need to be synthesized
before the target statement can be formalized.


prerequisite material to properly formalize, much of which already has been formalized by humans in
libraries such as Mathlib [22].
However, in more advanced mathematics, autoformalization becomes increasingly complex. Ad-
vanced mathematics has a large amount of prerequisite theory, much of which has yet to be formalized.
This means an autoformalization system must first retrieve or produce the necessary dependent theory,
correctly formalize it, and then formalize the original target statement.
Additionally, existing benchmarks typically focus on theorem statements, and ignore formalizations
of mathematical definitions. Systems which can only autoformalize theorem statements are limited
in their scope by the level of existing theory because they cannot formalize theorems using math
concepts they do not already have definitions for. Thus, creating scalable autoformalization systems
necessitates the study of definition autoformalization, for which large-scale real-world benchmarks
are lacking [39, 34].
To comprehensively evaluate the performance of autoformalization methods in higher-level math-
ematics, we present MathAtlas 1 , a large-scale, graduate-level benchmark designed to measure
autoformalization performance on mathematics in the wild. MathAtlas contains ∼ 51k informal
entities, divided into statements (theorems, examples, and exercises), definitions, and proofs, which
are extracted from 103 graduate math textbooks. Entities in MathAtlas span 87 areas of mathematics,
including real analysis, differential geometry, category theory, topology, quantum groups, among
others. Some entities in MathAtlas are formalizable on top of Mathlib, but many require additional
formal theory which may not currently exist. To facilitate access to these required dependencies, we
enrich each entity with long-range dependency relations, local variable references, and local context
(see Figure 1).
MathAtlas is the first large-scale, in the wild autoformalization benchmark of graduate-level math-
ematics, the first to include rich contextual and dependency data, and the first to annotate their
inter-entity dependencies. Our extensive experiments show that MathAtlas is very challenging:
strong baseline methods have low overall autoformalization correctness (10.5% on statements and
20.3% on definitions) on MathAtlas. Furthermore, we find this performance is correlated with an
entity’s dependency depth: our strongest baseline has only 2.6% overall correctness on MA-Hard , a
subset of 700 entities with the deepest dependency trees.
Finally, we investigate how well existing semantic faithfulness metrics for autoformalization gen-
eralize to MathAtlas. We present MA-Align 2 , a binary classification benchmark of 200 entities
from MathAtlas. Unlike prior benchmarks such as ConsistencyCheck [7] and CriticLeanBench[28],
MA-Align contains both labeled examples of theorem statements and definitions, and covers a

  1 https://huggingface.co/datasets/MathAtlas/MathAtlas




                                                 2
    Definition 2.7.10 (Invariant bilinear form).: Let V = V0̄ ⊕V1̄ be a superspace and carrying a representation
    of a Lie algebra g. A bilinear form (·|·) is said invariant if, for any homogeneous element X ∈ g and
    v, w ∈ V , (Xv|w) + p(v, X)(v|Xw) = 0. Moreover, if V is the representation space of the adjoint
    representation, then the bilinear form is said adjoint invariant.

    Corollary 3.A.24: Let X be a compact Kahler manifold. Then the inclusion i : (A∗ (X)c , d) ⊂
    (A∗ (X), d) is a dga-quasi-isomorphism.

    Example 5.1.14.: Find two fundamental matrices for the linear homogeneous system in Example 5.1.11.

Figure 2: Several entities from MathAtlas of various types: (1) a definition entity which defines
two terms: “invariant” and “adjoint invariant”. (2) a theorem statement of a corollary from complex
geometry. (3) an example from an ODE textbook.


wide variety of mathematics at the graduate level. Our experiments show that prior baselines have
significant room for improvement on MA-Align.
We organize the rest of the paper as follows: In § 2, we present MathAtlas, its construction, contents
and quality. We then discuss the benchmark’s autoformalization metrics (§ 3), before moving on to
our autoformalization experiments and an analysis of the results (§ 4). Finally, we discuss related
works (§ 5), and conclude (§ 6).

2     MathAtlas Benchmark

MathAtlas is constructed automatically from textbook documents. We discuss the entity and relation
types in MathAtlas, and then discuss our entity and relation extraction pipeline. We also measure the
quality of MathAtlas with a human evaluation.

2.1    Structure of MathAtlas

The structure of MathAtlas is as follows, with some relevant statistics.

Entities We use the term entity to mean a span of informal text which can be formalized, such as
a theorem in a textbook. In MathAtlas, entities are either definitions, theorems, proofs, examples,
or exercises (see Figure 2). Entities can, but don’t always, have identifiers, such as “Theorem 4.3.”
These identifiers are sometimes referenced by other entities (see Figure 1). Importantly, entities
sometimes contain multiple formalizable items. For example, in Figure 2, Definition 2.7.10 actually
defines two objects, and so it’s formalization may require two definitions.

References Entities can contain references to other entities, dependent mathematical objects, or
local variables which are not explicitly defined in the entity itself. We call these entity references,
object references, and local variable references, respectively.

Relations We also include relations between entity references and the target entity, and object
references and entities which define those objects. For example, an entity emet may define a metric
space, and contain an object reference rtop to a topological space, which is defined in an entity etop .
In this case, we add a relation ⟨emet , etop ⟩ (see Figure 1). We define dependency depth to be the
maximum height of an items dependency tree, where nodes are entities (e.g., definitions or theorems)
and edges are object references. Similarly, we define dependency mass to be the total number of
unique nodes in a particular entity’s dependency tree.

Statistics We now discuss some statistics of MathAtlas. Overall, MathAtlas contains of 52,052
entities, which are comprised of ∼ 18k theorems, ∼ 10k exercises, ∼ 10k definitions, ∼ 10k proofs,
and 5k examples.
    2 https://huggingface.co/datasets/MathAtlas/MA-Align




                                                         3
About 90% of entities contain at least one object reference. In sum, there are ∼193k object references,
for an average of 3.69 per entity. Of these, our relation extraction system found a matching target
entity for 83.7%, for a total of ∼161k total object relations in the full graph. In addition, 20.5% of
entities contain an entity reference, summing to ∼ 17k total entity references. Of these, over 99.8%
were matched with a target entity.
We now briefly present some features of MathAtlas’s dependency graph. Nodes have an average
dependency depth of 30 (median of 17), but range anywhere from 0 to 80. We also find a stark
difference in dependency depth based on the field of mathematics. For example, entities from
textbooks on Lie algebra or Quantum groups had an average depth of ∼ 50, whereas those from
books on set theory and logic had an average depth of ∼ 6. This is in-line with the intuition that
certain fields of mathematics have more prerequisites, and thus deeper dependency trees.



2.2   Construction of MathAtlas

Here we give an overview of our dataset construction pipeline. For additional details, see Appendix A.
To construct MathAtlas, we collect 103 PDFs of math texts from a variety of sources and several
fields of mathematics including subfields of algebra, analysis, geometry, number theory, probability,
quantum theory, category theory, topology, and others. The math texts cover a total of 87 fields
and subfields of mathematics. Following our pipeline (Figure 5), we convert the PDFs to MMD
(mathematical markdown) files and filter out pages containing metadata, such as indices or glossaries.
Then, we run an entity extraction model on the MMDs, which identifies spans of text corresponding
to entity types, along with any identifier found in the entity (e.g., “Example 3.4”). Next, on any
extracted entity, we run a reference extractor to identify any references to other entities, objects, or
local variables. Lastly, on definition entities, we run a name extraction system, which identifies the
name(s) of the defined object(s).
After extracting entities and associated metadata, we construct our dependency graph with a relation
extraction system (see Appendix A for system details). We add “refers-to” relations between entity
references and their target entities, and between an object references and the entity which defines that
object, if present. Finally, we add a “proves” relation between a proof entity and the theorem entity it
proves.



2.3   Quality Analysis of MathAtlas

We measure the intrinsic entity and relation extraction quality of the entities in MathAtlas.
To evaluate entity extraction quality, we annotate a random sample of 250 extracted entities from
MathAtlas, 50 entities of each type, based on whether the entity is valid.3 For an entity to be valid,
it must be complete (e.g., not cut off at the start or end, no missing segments due to improper
PDF-markdown conversion), and have a correctly labeled type. We find that overall, 90.4% of the
annotated entities are correctly extracted (see Table 1).
We also annotate 100 randomly sampled references, comprised of 50 object references and 50 entity
references. Like before, references are considered correct if they are complete and are labeled with
the correct type. We find that 96% of references were properly extracted. Of the four examples with
errors, three were identifiers which were mistaken as entity references, and one was a name mistaken
for an object reference.
Finally, we measure the performance of our relation extraction system. For each of the 100 randomly
sampled references above, we retrieve 10 candidate targets with LeanSearch and annotate which, if
any, are correct. We compute precision, recall, and F1 score of our automated system against the
human annotations. Overall, we find an F1 score of 94.8% (see Table 1a).



  3 Our annotators hold, at minimum, undergraduate math degrees.




                                                         4
                              Table 1: Intrinsic data quality analysis of MathAtlas.
    Ref. type        F1           Recall      Precision                            Entity Type      Valid %
    Entity ref.      94.7%        100%        90%                                  Definition       98.0%
    Object ref.      94.9%        98%         92%                                  Theorem          94.0%
                                                                                   Proof            80.0%
    Overall          94.8%        99%         91%
                                                                                   Example          86.0%
(a) Performance of our relation extraction system on                               Exercise         94.0%
a human-annotated subset of 100 extracted relations                                Overall          90.4%
(50 of each type). To measure recall, we annotate gold
target entities from among the retrieved candidates;               (b) Precision of our entity extraction system on a
if no selected candidate is an appropriate match, we               human-annotated subset of 250 examples (50 of each
assume none exists.                                                type).



3     Autoformalization Metrics for MathAtlas

Following previous work, we use the standard autoformalization metric of compile rate.4 However,
compile rate does not measure faithfulness of the formalization, so we also report semantic faithfulness
(see subsection 3.1 for a full discussion).
We report a combined metric of compile rate and semantic faithfulness which we call correctness. A
formal statement must both compile and be faithful to the informal statement for it to be considered
correct.

3.1    Semantic Faithfulness Metric

Here, we discuss semantic faithfulness as a metric, and present experiments showing limitations of
prior methods and our improvements.
Together with syntactic correctness (compilation rate), semantic correctness, or semantic faithfulness
is a critical metric for autoformalization. Faithfulness measures whether a formal statement has the
same mathematical meaning as its informal source. Prior work on semantic faithfulness [21, 7, 28, 20]
focuses on easier domains (olympiad or undergraduate math), and does not measure alignment of
definitions. MathAtlas highlights this gap in prior work, as it contains both high-level mathematics
and definition entities.
To assess the quality of semantic faithfulness metrics on graduate-level, in the wild mathematics, we
introduce MA-Align, a semantic faithfulness benchmark of syntactically correct 200 statements and
definitions from MathAtlas. Each informal entity is formalized by gpt-oss-120b, and annotated
with a binary label, “aligned” or “misaligned”.5 We evaluate prior LLM-as-judge systems, CriticLean
[28], as well as our few-shot LLM-as-judge on ConsistencyCheck [7] and CriticLeanBench [28], and
MA-Align (see Table 2). 6

3.2    Semantic Faithfulness Results

We now analyze the results of our semantic faithfulness experiments (Table 2). Overall, we find
that CriticLean has strong performance on ConsistencyCheck and CriticLeanBench, but a notable
drop in accuracy on MA-Align. In contrast, the strongest LLM-as-judge system (gpt-5.2 with an
engineered prompt) drops performance on ConsistencyCheck and CriticLeanBench, but improves by
6% on MA-Align for definitions and 5% for statements. We suspect this tradeoff is in part due to the
selected examples, which were selected from MathAtlas and therefore in-domain for MA-Align.

    4We use the software package blv [26] to measure compile rate, compiled against Lean version v4.24.0.
    5We selectively sample 200 such entities to better balance the label distribution.
    6We note that we leave out FormalAlign [21] as a baseline as there is no official implementation, and our reimplementation

was unable to match the reported results.


                                                               5
Table 2: Results of various methods on several semantic faithfulness benchmarks. “ReForm prompt”
refers to the faithfulness prompt used by Chen et al. [7], and “Our Prompt” is an engineered, few-shot
prompt optimized for gpt 5.2 with examples taken from MathAtlas.
Model                ConsistencyCheck       CriticLeanBench      MA-Align Defs.      MA-Align Stmts.
                                              CriticLean
CriticLean (14B)            81.7                  84.4                 68.0                 56.0
CriticLean (32B)            82.6                  86.4                 80.0                 75.0
                                           ReForm Prompt
gpt-oss-120b                84.9                85.4                   76.0                 61.0
Qwen3 (14B)                 80.9                82.4                   70.0                 57.0
Qwen3 (32B)                 74.6                71.5                   74.0                 67.0
                                       Our Prompt (Few-shot)
gpt-oss-120b                81.1               83.8                    78.0                 65.0
Qwen3 (14B)                 71.3               59.4                    68.0                 71.0
Qwen3 (32B)                 80.5               72.4                    71.0                 68.0
gpt-5.2                     82.1               79.0                    86.0                 80.0


However, as gpt-5.2 is both proprietary and expensive to use, we elect to use CriticLean (32B) as
our primary semantic faithfulness metric for MathAtlas, as it is still well-correlated with human
evaluations, is open source,


4     Autoformalization Experiments

In this section, we present autoformalization experiments on MathAtlas with several strong baseline
methods. We first detail the various models and settings, followed by an analysis of the results.

4.1   Dataset Splits

MathAtlas is naturally divided into five splits corresponding to each entity type: definitions, theorems,
exercises, examples, and proofs. However, exercises, examples, and theorems are formalized similarly:
that is, as a theorem statement in Lean 4. Thus, we report results on a joint “statement” split comprised
of all exercises, examples, and theorems. Note that only a correct statement is required, not the full
proof. We leave the study of proof and full-theorem formalization for future work.
Additionally, we analyze several variables pertinent to high-level, in the wild autoformalization.
First, we investigate whether an item already existing in Mathlib affects a system’s autoformalization
performance. It is likely that LLMs have seen Mathlib in its training data. Additionally, Mathlib is
constructed bottom-up, meaning entities lower-level fields are more likely to already be formalized.
These reasons suggest that existing items will have a higher average correctness. Secondly, we
determine to what extent max dependency depth affects correctness, as well as dependency mass (i.e.,
the total number of dependencies in the dependency tree).

MA-Hard We select a subset of ∼ 700 examples with the deepest dependency trees, which
we call MA-Hard. This set primarily consists of examples from more advanced graduate-level
mathematics, such as Algebraic Geometry and Lie Theory, and spans 14 subjects. We also note that
MA-Hard consists of both statements (∼ 600) and definitions (∼ 100).

Open Split Approximately 30% of entities in MathAtlas are extracted from Springer textbooks. To
comply with copyright law, we release code to generate MathAtlas in full, which can be run by those
who have access to Springer textbooks. However, to facilitate access to MathAtlas, we release an
open split of the remaining 70% of the data publicly.7 All examples from MA-Hard are in the open
split. Our results on this open subset are reported in the Appendix in Table 5.
    7 https://huggingface.co/datasets/MathAtlas/MathAtlas




                                                   6
Table 3: Results for autoformalization experiments on MathAtlas. “Compiles” measures the percent-
age of examples which successfully compile. “Faithful” measures what percent of the compiling
theorems are faithful. “Correct” indicates the overall percentage of statements which compile and are
faithful.
                                                              Model                Compiles      Faithful    Correct
                                                                           Fine-tuned
                                                        Herald 7B           11.8%         12.7%     1.5%
   Model                Compiles Faithful Correct Kimina 7B                 27.3%         8.4%      2.3%
                                                        ATLAS-L 8B          21.4%         16.4%     3.5%
                        Prompted                        Goedel 8B           20.3%         34.9%     7.1%
   gpt-oss-20b (zs)     10.5%        20.9%        2.2%  Goedel 32B          23.2%         30.6%     7.1%
    +few-shot           18.1%        41.4%        7.5%  ReForm 8B           19.0%         48.4%     9.8%
    +tuned prompt       17.1%        47.4%        8.1%
    +tuned exs.         20.8%        56.3%        11.7%                     Prompted
    +context            16.1%        55.9%        9.0%  gpt-oss-20b (zs)    9.9%          42.4%     4.2%
                                                         +few-shot          16.5%         35.8%     5.9%
   gpt-oss-120b (zs) 13.4%           49.3%        6.6%   +tuned prompt      16.8%         32.7%     5.5%
    +few-shot           24.2%        57.0%        13.8%  +tuned exs.        19.1%         35.1%     6.7%
    +tuned prompt       26.0%        58.8%        15.3%  +local context     18.6%         36.0%     6.7%
    +tuned exs.         28.5%        58.5%        16.7%
    +local context      25.8%        58.9%        15.2% gpt-oss-120b (zs) 14.3%           47.6%     6.8%
                                                         +few-shot          16.8%         43.5%     7.3%
   (a) Autoformalization results for definitions.        +tuned prompt      17.1%         43.9%     7.5%
   We do not evaluate fine-tuned methods for             +tuned exs.        21.7%         35.9%     7.8%
   definitions because there are no prior-work           +local context     20.0%         34.5%     6.9%
   models available for definitions. The best
   performance in each category and column              (b) Autoformalization results for statements (the-
   are bolded.                                          orems, examples, and exercises). The best perfor-
                                                        mance in each category and column are bolded.



4.2   Evaluated Methods

We measure the performance variety of autoformalization baselines, including fine-tuned methods and
prompting methods. We evaluate several strong models with zero and few-shot prompting. We test
zero-shot and few-shot prompting with gpt-oss-120B and gpt-oss-20b [27] (see Appendix B for
full prompts). We supply the target entity text as input, and the expected output is a syntactically and
semantically correct formal representation in Lean 4 (see § 3). This approach has been extensively
studied in prior work, especially on benchmarks such as miniF2F [41] and ProofNet [3]. We
perform an ablation, evaluating zero-shot prompting, few-shot with randomly selected examples from
LeanWorkbook [38], adding an engineered prompt, and using annotated, graduate-level examples.
We use the zero-shot prompt from Zhang et al. [39]. Our engineered prompt is more detailed in its
instructions. Importantly, it instructs the model to synthesize background theory when necessary, and
allows for multiple formal output statements as is sometimes required in MathAtlas.
On statements, we also test fine-tuned methods: Herald Translator [12], Goedel Formalizer v2 [17],
Kimina Autoformalizer [33], Atlas Translator [19], and ReForm [7]. However, for definitions, we
do not include any fine-tuned methods, as our experiments revealed autoformalization methods for
theorems were unable to generalize to definitions in this domain.8

Added Local Context As discussed in subsection 2.1, some entities in MathAtlas require context
to define variables, entities, or otherwise elaborate a mathematical setting. We evaluate a simple
baseline of including the prior 500 tokens in the context window of the LLM. For this setting, we test
only the few-shot prompted systems, as this is out-of-domain for the fine-tuned models.

4.3   Results

In this section we analyze the results of our autoformalization experiments on MathAtlas.
   8We are unable to evaluate some prior definition autoformalization methods such as ARIA [34] or LoC-Decomp [31] due

to unreleased code.


                                                          7
(a) Correctness versus dependency depth of our best       (b) Correctness versus dependency depth of our best
performing system for definitions (gpt-oss-120b).         performing system for statements (ReForm 8B)
Figure 4: Correctness of our strongest models compared with dependency depth on examples in
MathAtlas.


Overall, we find MathAtlas to be very challenging. On the statement split, our strongest baseline
is ReForm 8B, which achieved an overall correctness of 9.8% (see Table 3). We note the disparity
between compilation rate and correctness, especially in fine-tuned models: Kimina 7B, for example,
achieves 27.3% compilation rate, but just 2.3% of formalizations compile and are faithful. On
the definition split, our strongest system is gpt-oss-120b, with 16.7% correctness, likewise with
a significant 11.8% gap between compilation rate and overall correctness. As shown in Table 4,
MA-Hard poses a significant challenge, with our strongest model achieving only 2.6% correctness.

Local Context Many items in MathAtlas require local context to correctly solve. How-
ever, including 300 tokens of local context seems to confuse prompted systems, and the
input decreases system performance from 20.3% to 17.4% on definitions, and 10.5% to
8.6% on statements for the best model (see Table 3). This drop in performance indicates
further research is necessary on incorporating local context into autoformalization methods.


Object Dependencies Next, we compare correct-
ness versus max dependency depth. In Figure 4, we
notice a clear trend, showing that our best systems is
less likely to correctly formalize deeper targets. We
compute a two-sample Kolmogorov–Smirnov, and
find significant difference between the max depth dis-
tributions for correct and incorrect examples (p <
0.001).

Existence in Mathlib We compare correctness of Figure 3: Correctness of formalized entities
definitions which are and aren’t grounded in Math- from our best models compared with pres-
lib (see Figure 3). We find that 27.9% of definitions ence in Mathlib. Entities which our retrieval
which our linker grounded in Mathlib are correctly system (LeanSearch [11]) found in Mathlib
formalized, whereas only 16.8% of missing defini- are significantly more likely to be correctly
tions are correct, statistically significant difference formalized than otherwise.
(chi-square p < 0.001). This supports intuition, as Mathlib is likely to be in the training data for
modern LLMs like gpt-oss-120b, which may result in inflated autoformalization performance on
those entities.

5   Related Works
LLMs for Autoformalization Large language models (LLMs) have made significant advancements
in autoformalization. Early work with LLMs such as in Wu et al. [36] used naive approaches, but


                                                      8
Table 4: Performance of few-shot prompted models on MA-Hard, which contains both definitions
and statements.
                        Model         Compiling Faithful Correct
                                gpt-oss-20b        14.3%            14.7%         2.1%
                                gpt-oss-120b       14.6%            17.8%         2.6%


showed promise in the methodology. Further refinements with fine-tuning on various data made
significant progress [12, 17, 37, 19, 4] but, as we show in this paper, face similar issues in more
difficult settings. More recently, there has been work on breaking down targets either by decomposing
into subproblems [31] or retrieving dependencies first [34, 23]. These methods have encouraging
results in harder settings [14], but use proprietary and expensive models and are token-inefficient.
ProofFlow [6] introduces a method for formalizing natural language proofs, as well as ProofScore, a
metric for measuring faithfulness to the natural language.

Autoformalization Benchmarks Prior autoformalization benchmarks have largely focused on
formalizing theorem statements [41, 3], primarily on olympiad or undergraduate mathematics. Lea-
nEuclid [25] is a benchmark for autoformalizing geometry from Euclid’s Elements and the UniGeo
dataset [8]. Zhang et al. [39] present two definition-specific benchmark of 100 definitions taken
from arXiv and Wikipedia, and show proprietary LLMs have low performance. The FATE-H and
FATE-X benchmarks [14] consist of 100 problems from commutative and abstract algebra, and pose a
significant challenge compared to previous work. In contrast to the FATE benchmarks, MathAtlas is
much larger, contains multiple entity types, is more varied in topic, andwincludes local and long-range
dependencies which facilitate the study of isolated system components, such as retrieval or synthesis.

Autoformalization Metrics Correctness in autoformalization is measured with two metrics: com-
pilation and semantic faithfulness. The former is simple to measure with the language’s compiler, or
specialized tools such as Kimina Lean Server [29] or blv [26].
More difficult to measure is faithfulness, which measures whether the generated formal language
code is semantically equivalent to the input informal statement. FormalAlign [21] introduces a
methodology for fine-tuning an alignment model for statements. However, the methodology does not
scale well to more difficult domains, and fails to capture the types of mistakes made by more advanced
autoformalization models.9 For benchmarks with gold formal labels, BEq [18] judges semantic
equivalence between two formal statements based on definitional equivalence, and TransTED [20]
presents a tree-based similarity metric. ProofScore [6] as previously mentioned is a faithfulness
metric specifically for proofs. Using an LLM-as-judge approach has been common for measuring
semantic faithfulness [40], and has shown promise as a scalable metric. ConsistencyCheck [7] is a
benchmark for semantic faithfulness metrics, but as we show in subsection 3.2, high performance on
ConsistencyCheck does not necessarily imply high performance in harder domains such as MA-Align.

6     Conclusion
In conclusion, we introduce MathAtlas, a large-scale benchmark for graduate-level autoformalization
of mathematics in the wild. Through extensive experiments, we show that that MathAtlas is very
challenging for existing autoformalization systems.
In contrast to prior benchmarks, MathAtlas with a dependency-graph structure which identifies
prerequisite theory for each entity. Our analysis shows that entities with deeper dependency trees are
substantially less likely to be formalized correctly. To study this difficulty, we construct MA-Hard,
a subset of 700 entities with the deepest dependency trees in MathAtlas, on which our strongest
system achieves only 2.6% correctness. We additionally observe that entities successfully grounded
to existing formalizations in Mathlib are significantly more likely to be formalized correctly.
Finally, we introduce MA-Align, a benchmark for evaluating semantic faithfulness on both mathemat-
ical statements and definitions for MathAtlas. Experiments on MA-Align show that trained metrics
    9 No implementation or model weights have been released as of this paper. Our analysis of these results is based on our

re-implementation, which failed to match reported numbers.


                                                             9
such as CriticLean, as well as strong LLM-as-judge systems, have clear room for improvement in
faithfulness evaluation.
We release MathAtlas, MA-Align, and our experimental code to support future research for in the
wild autoformalization.

Limitations
MathAtlas primarily deals with graduate-level mathematics, and leaves more difficult domains such
as research mathematics for future work. Certain textbooks are also omitted from MathAtlas due to
copyright concerns, which can potentially bias data.

Acknowledgements
This work was supported in part by the National Science Foundation under the Artificial Intelligence,
Formal Methods, and Mathematical Reasoning (AIMing) NSF grant, award #2523479. This work
used resources available through the National Research Platform (NRP) at the University of California,
San Diego. NRP has been developed, and is supported in part, by funding from National Science
Foundation, from awards 1730158, 1540112, 1541349, 1826967, 2112167, 2100237, and 2120019,
as well as additional funding from community partner.

References
 [1] Exploration of neural machine translation in autoformalization of mathematics in Mizar |
     Proceedings of the 9th ACM SIGPLAN International Conference on Certified Programs and
     Proofs. URL https://dl.acm.org/doi/10.1145/3372885.3373827.
 [2] A. Agrawal, S. Gadgil, N. Goyal, A. Narayanan, and A. Tadipatri. Towards a Mathematics
     Formalisation Assistant using Large Language Models. URL http://arxiv.org/abs/2211.
     07524.
 [3] Z. Azerbayev, B. Piotrowski, and J. Avigad. ProofNet: A Benchmark for Autoformalizing and
     Formally Proving Undergraduate-Level Mathematics Problems.
 [4] Z. Azerbayev, H. Schoelkopf, K. Paster, M. D. Santos, S. McAleer, A. Q. Jiang, J. Deng,
     S. Biderman, and S. Welleck. Llemma: An Open Language Model For Mathematics, Oct. 2023.
 [5] L. Blecher, G. Cucurull, T. Scialom, and R. Stojnic. Nougat: Neural optical understanding for
     academic documents, 2023.
 [6] R. Cabral, T. M. Do, X. Yu, W. M. Tai, Z. Feng, and X. Shen. ProofFlow: A Dependency Graph
     Approach to Faithful Proof Autoformalization, Oct. 2025. URL http://arxiv.org/abs/
     2510.15981. arXiv:2510.15981 [cs].
 [7] G. Chen, J. Wu, X. Chen, W. X. Zhao, R. Song, C. Li, K. Fan, D. Liu, and M. Liao. Reform:
     Reflective autoformalization with prospective bounded sequence optimization, 2026. URL
     https://arxiv.org/abs/2510.24592.
 [8] J. Chen, T. Li, J. Qin, P. Lu, L. Lin, C. Chen, and X. Liang. Unigeo: Unifying geometry logical
     reasoning via reformulating mathematical expression, 2022. URL https://arxiv.org/abs/
     2212.02746.
 [9] R. Escriva, H. Bashir, M. Isom, J. Huber, Macronova, S. Kedia, itaismith, L. Vander-
     Hart, J. Radhakrishnan, tanujnay112, T. Azarov, B. Eggers, K. Diaz, L. Pei, jasonvigil,
     D. Kim, A. Troynikov, P. I. Thomas, R. P, nicolasgere, G. Shahbazian, E. Culver, C. Gam-
     ble, D. Dash, T. Krusinski, W. Gu, swyx.io, M. Keller, R. Him, and naynaly10. chroma-
     core/chroma. https://github.com/chroma-core/chroma, may 7 2026. URL https://github.
     com/chroma-core/chroma.
[10] S. Gadgil, A. R. Tadipatri, A. Agrawal, A. Narayanan, and N. Goyal. Towards automating
     formalisation of theorem statements using large language models.


                                                 10
[11] G. Gao, H. Ju, J. Jiang, Z. Qin, and B. Dong. A semantic search engine for mathlib4, 2025.
     URL https://arxiv.org/abs/2403.13310.
[12] G. Gao, Y. Wang, J. Jiang, Q. Gao, Z. Qin, T. Xu, and B. Dong. Herald: A natural language
     annotated lean 4 dataset, 2025. URL https://arxiv.org/abs/2410.10878.
[13] A. Q. Jiang, W. Li, and M. Jamnik. Multilingual mathematical autoformalization. arXiv preprint
     arXiv: 2311.03755, 2023.
[14] J. Jiang, W. He, Y. Wang, G. Gao, Y. Hu, J. Wang, N. Guan, P. Wu, C. Dai, L. Xiao, and B. Dong.
     Fate: A formal benchmark series for frontier algebra of multiple difficulty levels, 2025. URL
     https://arxiv.org/abs/2511.02872.
[15] A. Kontorovich and T. Tao. Prime Number Theorem and More, Jan. 2024. URL https:
     //github.com/AlexKontorovich/PrimeNumberTheoremAnd.
[16] W. Kwon, Z. Li, S. Zhuang, Y. Sheng, L. Zheng, C. H. Yu, J. E. Gonzalez, H. Zhang, and
     I. Stoica. Efficient memory management for large language model serving with pagedattention.
     In Proceedings of the ACM SIGOPS 29th Symposium on Operating Systems Principles, 2023.
[17] Y. Lin, S. Tang, B. Lyu, Z. Yang, J.-H. Chung, H. Zhao, L. Jiang, Y. Geng, J. Ge, J. Sun, J. Wu,
     J. Gesi, X. Lu, D. Acuna, K. Yang, H. Lin, Y. Choi, D. Chen, S. Arora, and C. Jin. Goedel-
     prover-v2: Scaling formal theorem proving with scaffolded data synthesis and self-correction,
     2025. URL https://arxiv.org/abs/2508.03613.
[18] Q. Liu, X. Zheng, X. Lu, Q. Cao, and J. Yan. Rethinking and improving autoformalization:
     towards a faithful metric and a dependency retrieval-based approach. In The Thirteenth Inter-
     national Conference on Learning Representations, 2025. URL https://openreview.net/
     forum?id=hUb2At2DsQ.
[19] X. Liu, K. Bao, J. Zhang, Y. Liu, Y. Chen, Y. Liu, Y. Jiao, and T. Luo. Atlas: Autoformalizing
     theorems through lifting, augmentation, and synthesis of data, 2025. URL https://arxiv.
     org/abs/2502.05567.
[20] X. Liu, T. Zhu, Z. Dong, Y. Liu, Q. Guo, Z. Liu, Y. Chen, and T. Luo. Assess: A semantic and
     structural evaluation framework for statement similarity, 2026. URL https://arxiv.org/
     abs/2509.22246.
[21] J. Lu, Y. Wan, Y. Huang, J. Xiong, Z. Liu, and Z. Guo. FormalAlign: Automated Alignment
     Evaluation for Autoformalization, Oct. 2024. URL http://arxiv.org/abs/2410.10135.
     arXiv:2410.10135 [cs].
[22] T. mathlib Community. The lean mathematical library. In Proceedings of the 9th ACM SIGPLAN
     International Conference on Certified Programs and Proofs, POPL ’20. ACM, Jan. 2020. doi:
     10.1145/3372885.3373824. URL http://dx.doi.org/10.1145/3372885.3373824.
[23] M. J. Min, Y. Gao, W. Sy, Z. Li, X. Si, and O. Bastani. Divide and abstract: Autoformalization
     via decomposition and abstraction learning. In The Fourteenth International Conference on
     Learning Representations, 2026. URL https://openreview.net/forum?id=NjgaeXNit3.
[24] L. d. Moura and S. Ullrich. The lean 4 theorem prover and programming language, 2021. URL
     https://doi.org/10.1007/978-3-030-79876-5_37.
[25] L. Murphy, K. Yang, J. Sun, Z. Li, A. Anandkumar, and X. Si. Autoformalizing Euclidean
     geometry. In International Conference on Machine Learning (ICML), 2024.
[26] Nilay Patel. offendo/blv. https://github.com/offendo/blv, mar 11 2026. URL https://github.
     com/offendo/blv.
[27] OpenAI, :, S. Agarwal, L. Ahmad, J. Ai, S. Altman, A. Applebaum, E. Arbus, R. K. Arora, Y. Bai,
     B. Baker, H. Bao, B. Barak, A. Bennett, T. Bertao, N. Brett, E. Brevdo, G. Brockman, S. Bubeck,
     C. Chang, K. Chen, M. Chen, E. Cheung, A. Clark, D. Cook, M. Dukhan, C. Dvorak, K. Fives,
     V. Fomenko, T. Garipov, K. Georgiev, M. Glaese, T. Gogineni, A. Goucher, L. Gross, K. G.
     Guzman, J. Hallman, J. Hehir, J. Heidecke, A. Helyar, H. Hu, R. Huet, J. Huh, S. Jain, Z. Johnson,


                                                 11
     C. Koch, I. Kofman, D. Kundel, J. Kwon, V. Kyrylov, E. Y. Le, G. Leclerc, J. P. Lennon,
     S. Lessans, M. Lezcano-Casado, Y. Li, Z. Li, J. Lin, J. Liss, Lily, Liu, J. Liu, K. Lu, C. Lu,
     Z. Martinovic, L. McCallum, J. McGrath, S. McKinney, A. McLaughlin, S. Mei, S. Mostovoy,
     T. Mu, G. Myles, A. Neitz, A. Nichol, J. Pachocki, A. Paino, D. Palmie, A. Pantuliano,
     G. Parascandolo, J. Park, L. Pathak, C. Paz, L. Peran, D. Pimenov, M. Pokrass, E. Proehl,
     H. Qiu, G. Raila, F. Raso, H. Ren, K. Richardson, D. Robinson, B. Rotsted, H. Salman,
     S. Sanjeev, M. Schwarzer, D. Sculley, H. Sikchi, K. Simon, K. Singhal, Y. Song, D. Stuckey,
     Z. Sun, P. Tillet, S. Toizer, F. Tsimpourlas, N. Vyas, E. Wallace, X. Wang, M. Wang, O. Watkins,
     K. Weil, A. Wendling, K. Whinnery, C. Whitney, H. Wong, L. Yang, Y. Yang, M. Yasunaga,
     K. Ying, W. Zaremba, W. Zhan, C. Zhang, B. Zhang, E. Zhang, and S. Zhao. gpt-oss-120b &
     gpt-oss-20b model card, 2025. URL https://arxiv.org/abs/2508.10925.
[28] Z. Peng, Y. Yao, K. Ma, S. Guo, Y. Li, Y. Zhang, C. Zhang, Y. Zhang, Z. Yu, L. Li, M. Liu,
     Y. Xia, J. Shen, Y. Wu, Y. Cao, Z. Zhang, W. Huang, J. Liu, and G. Zhang. Criticlean:
     Critic-guided reinforcement learning for mathematical formalization, 2025. URL https:
     //arxiv.org/abs/2507.06181.
[29] M. D. Santos, H. Wang, H. de Saxcé, R. Wang, M. Baksys, M. Unsal, J. Liu, Z. Liu, and J. Li.
     Kimina lean server: Technical report, 2025. URL https://arxiv.org/abs/2504.21230.
[30] P. Scholze and K. Buzzard. Liquid tensor experiment, Dec. 2020. URL https://
     xenaproject.wordpress.com/2020/12/05/liquid-tensor-experiment/.
[31] J. Shi, Z. Zhang, B. Ma, S. Zhao, Y. Yuan, and G. Wang. Loc-decomp: LLM autofor-
     malization via logical concept decomposition and iterative feedback correction. In The
     Fourteenth International Conference on Learning Representations, 2026. URL https:
     //openreview.net/forum?id=0KFQ4F9YEH.
[32] T. Tao.    Formalizing the proof of pfr in lean4 using blueprint: a short
     tour, Nov. 2023.         URL https://terrytao.wordpress.com/2023/11/18/
     formalizing-the-proof-of-pfr-in-lean4-using-blueprint-a-short-tour.
[33] H. Wang, M. Unsal, X. Lin, M. Baksys, J. Liu, M. D. Santos, F. Sung, M. Vinyes, Z. Ying,
     Z. Zhu, J. Lu, H. de Saxcé, B. Bailey, C. Song, C. Xiao, D. Zhang, E. Zhang, F. Pu, H. Zhu,
     J. Liu, J. Bayer, J. Michel, L. Yu, L. Dreyfus-Schmidt, L. Tunstall, L. Pagani, M. Machado,
     P. Bourigault, R. Wang, S. Polu, T. Barroyer, W.-D. Li, Y. Niu, Y. Fleureau, Y. Hu, Z. Yu,
     Z. Wang, Z. Yang, Z. Liu, and J. Li. Kimina-prover preview: Towards large formal reasoning
     models with reinforcement learning, 2025. URL https://arxiv.org/abs/2504.11354.
[34] H. Wang, R. Xie, Y. Wang, G. Gao, X. Yu, and B. Dong. Aria: An agent for retrieval and
     iterative auto-formalization via dependency graph, 2025. URL https://arxiv.org/abs/
     2510.04520.
[35] L. Wang, N. Yang, X. Huang, L. Yang, R. Majumder, and F. Wei. Improving text embeddings
     with large language models, 2024. URL https://arxiv.org/abs/2401.00368.
[36] Y. Wu, A. Q. Jiang, W. Li, M. N. Rabe, C. Staats, M. Jamnik, and C. Szegedy. Autoformalization
     with Large Language Models. URL http://arxiv.org/abs/2205.12615.
[37] Y. Wu, D. Huang, R. Wan, Y. Peng, S. Shang, C. Cao, L. Qi, R. Zhang, Z. Du, J. Yan, and X. Hu.
     Stepfun-formalizer: Unlocking the autoformalization potential of llms through knowledge-
     reasoning fusion, 2025. URL https://arxiv.org/abs/2508.04440.
[38] H. Ying, Z. Wu, Y. Geng, J. Wang, D. Lin, and K. Chen. Lean workbook: A large-scale
     lean problem set formalized from natural language math problems. arXiv preprint arXiv:
     2406.03847, 2024.
[39] L. Zhang, M. Valentino, and A. Freitas. Autoformalization in the wild: Assessing LLMs on real-
     world mathematical definitions. In C. Christodoulopoulos, T. Chakraborty, C. Rose, and V. Peng,
     editors, Proceedings of the 2025 Conference on Empirical Methods in Natural Language
     Processing, pages 1720–1738, Suzhou, China, Nov. 2025. Association for Computational
     Linguistics. ISBN 979-8-89176-332-6. doi: 10.18653/v1/2025.emnlp-main.90. URL https:
     //aclanthology.org/2025.emnlp-main.90/.


                                                12
[40] L. Zhang, M. Valentino, and A. Freitas. Beyond Gold Standards: Epistemic Ensemble of LLM
     Judges for Formal Mathematical Reasoning, June 2025.
[41] K. Zheng, J. M. Han, and S. Polu. MiniF2F: A cross-system benchmark for formal Olympiad-
     level mathematics. URL https://arxiv.org/abs/2109.00110v2.




                                             13
Figure 5: MathAtlas creation pipeline. For visual convenience, we combine the “name” and
“reference” extractors into one step called “identifier extractor.”

    Text:
    "M is compact iff G is abelian."

    Reasoning:
    - M not introduced → include local_variable_reference
    - G not introduced → include local_variable_reference
    - compact is a named property → include object_reference
    - abelian is a named property → include object_reference

    Output:
    [
      {"term": "M", "reference_type": "local_variable_reference"},
      {"term": "G", "reference_type": "local_variable_reference"},
      {"term": "compact", "reference_type": "object_reference"},
      {"term": "abelian", "reference_type": "object_reference"}
    ]

                Figure 6: Example of reference extraction system input and output.


A    Extraction Pipeline

Our extraction pipeline starts with 103 selected textbooks covering a wide range of mathematics.
We use Nougat [5] to convert PDFs into Mathematical Markdown (MMD). We then run our entity
extraction system, followed by our reference extraction and name extraction systems, and finally our
relation extraction system. We detail each below.

Entity Extraction Our entity extraction system is a few-shot, prompt-engineered gpt-oss-120b.
We prompt the model to generate an array of JSON objects with keys “type” indicating the entity’s
type, optionally an “identifier”, which are spans such as Definition 3.9 or Theorem 15, and “text”,
which is the actual text of the entity. We enforce this structure with a JSON schema using structured
decoding, a temperature of 0.3, and otherwise default sampling parameters.
We then run our reference extractor system, likewise a prompted gpt-oss-120b model. The reference
extractor takes as input an extracted entity, and outputs a list of JSON objects with keys “term,”
indicating the text of the reference, and “reference_type,” which is one of object_reference,
entity_reference, or local_variable_reference. This is likewise enforced with JSON
schema, and uses a temperature of 0.3.
Then, we run the name extractor, also a prompted gpt-oss-120b, prompted to output the names of
objects defined in the entity. The output a JSON array of strings, again enforced with a schema and
structured decoding. We likewise use a temperature of 0.3.


                                                 14
Relation Extraction Each entity is embedded into a ChromaDB instance [9] together with all its
metadata, using the Mistral E5 model from Wang et al. [35]. Then, our relation extraction system
works in two stages. First, we use the same model to retrieve candidate matches from the entity
database. Secondly, we prompt gpt-oss-120b to determine which, if any, is the correct match,
accounting for usage and context. If there are multiple matches, we prioritize those from the same
textbook, or otherwise those with the highest matching score.

Grounding in Mathlib We use LeanSearch [11] to link definitions in MathAtlas to formal def-
initions in Mathlib. We query the definition text to get 10 candidate matches, and select from the
matches using a prompted “gpt-oss-120b.” Unlike the authors however, we find that augmenting the
query degrades performance, so we skip that step in our final run. We suspect this is because our
queries are already fully-formed definitions rather than keywords or phrases. We include the selected
matches as well as all 10 candidates for each definition in the released dataset.

B      Prompts
   ## Task
You are given a block of markdown mathematical text .
Your task is to identify and extract all contiguous snippets that correspond to any of the following
     mathematical entity types :

-   Definition
-   Theorem ( this includes propositions , lemmas , corollaries )
-   Example
-   Exercise
-   Proof

Only extract genuine mathematical content of these types .
Ignore and do NOT extract :

-   General exposition or narrative explanation
-   Chapter titles , section headings , or indexes
-   Transitional text or motivation
-   References to earlier or later results without stating them


## What qualifies as an entity

### 1. Definitions ( very important )

A definition does NOT require a heading or numbering .

You must extract a block as a definition if its primary purpose is to introduce , name , or precisely
     describe a mathematical object or concept , even if it appears inline in the text .

Treat a block as a definition if it contains definitional language , including but not limited to :

-   " is called "
-   " is defined as "
-   " we call "
-   " is said to be "
-   " the ... of ... is "
-   " an element ... is "
-   an emphasized or italicized term followed by an explanation
-   a mathematical object followed by a copular verb (" is " , " are ") and a precise condition

If a paragraph answers the question " What is X ?" , it is a definition .

A single paragraph may introduce multiple concepts ( e . g . , minimum polynomial and conjugate ) .
If so , extract the entire paragraph as one definition entity .

Unlabeled definitions are mandatory .
Failure to extract them is considered an incorrect output .


### 2. Theorems

Extract any explicitly stated mathematical claim intended to be true , including :

-   Theorem
-   Proposition
-   Lemma
-   Corollary

Treat all of these as type " theorem ".

The entity must assert a result , not merely mention one .


### 3. Proofs

Extract a proof only when :




                                                        15
- It is explicitly labeled ( e . g . , " Proof ." , " Proof of Proposition 3.2.") , and
- It contains actual mathematical reasoning or argument

Special rule :
If a proof appears only as part of an exercise prompt ( e . g . , " Prove that ...") and contains no
     mathematical argument beyond the statement itself , do NOT extract a separate proof entity .

Caution :
Be careful to extract a full proof , and do not cut off any information halfway through .


### 4. Examples

Extract examples that demonstrate or instantiate a mathematical concept , whether labeled (" Example
     2.3") or clearly signposted in the text .


### 5. Exercises

Extract exercises or problems intended for the reader to solve , whether labeled or clearly formatted as
      such .


## Output format

For each extracted entity , produce a JSON object with the following keys :

- " type ": one of " definition " , " theorem " , " example " , " exercise " , " proof " ( always lowercase )
- " identifier ": a concise label taken verbatim from the text introducing the entity
  ( e . g . , " Definition 6.9." , " Proposition 6.11." , " Proof ." , " Exercise 7( b ) ")
  If no explicit label , number , or name is present , set this to null .
- " text ": the exact text of the entity , copied verbatim .
  Do NOT summarize , paraphrase , normalize spacing , or rewrite mathematics .


## Ordering rules

-   Preserve the original order of appearance .
-   Each entity must be its own JSON object .
-   Do not merge separate entities .
-   Do not invent or infer missing text .


## Reasoning step ( required )

Before producing the final output :

1. Scan the text systematically from start to end .
2. Actively search for :
   - Explicit labels ( Definition , Theorem , Proof , etc .)
   - Implicit definitions using definitional language
3. For each candidate block :
   - Decide whether it is genuine mathematical content
   - Confirm it matches one of the allowed entity types
4. Exclude all non - mathematical exposition .

Only after completing this identification and segmentation should you produce the output .


## Output constraints

-   Respond with a JSON list only
-   Do NOT wrap the JSON in code fences
-   Do NOT include explanations , commentary , or reasoning in the output
-   If no valid entities are found , return an empty list : []


## Priority reminder

If a block introduces or defines a mathematical object - even without a heading - it MUST be extracted
     as a " definition ".



                                      Figure 7: Prompt for entity extraction
You are given a mathematical definition written in textbook style .

Your task is to extract the names of the mathematical objects , concepts , or properties being defined .

### Rules :
- Return only the names of the items being defined .
- Do not include symbols , formulas , or explanations .
- If multiple items are defined , return all of them .
- If a definition gives multiple synonymous names ( e . g . " X ( or Y ) ") , include the most standard or
     commonly used name .
- Ignore purely notational conventions unless they define a commonly named concept .
- Normalize names to lowercase unless capitalization is standard .
- Output the result as a JSON - style list of strings .

Definition :
{{ DEFINITION_TEXT }}




                                                            16
Output format :
[" name 1" , " name 2" , ...]

### Examples :

Example 1:
Definition :
** Definition 0.3.4**.:
1. A _union_ of two sets \( A \) and \( B \) is defined as \[ A \ cup B \ coloneqq \{{ x : x \ in A \ text {{ or }} x \ in B
      \}}.\]
2. An _intersection_ of two sets \( A \) and \( B \) is defined as \[ A \ cap B \ coloneqq \{{ x : x \ in A \ text {{ and
       }} x \ in B \}}.\]
3. A _complement of \( B \) relative to \( A \) _ ( or _set - theoretic difference_ of \( A \) and \( B \) ) is
      defined as \[ A \ setminus B \ coloneqq \{{ x : x \ in A \ text {{ and }} x \ notin B \}}.\]
4. We say _complement_ of \( B \) and write \( B ^{{ c }}\) instead of \( A \ setminus B \) if the set \( A \) is
      either the entire universe or if it is the obvious set containing \( B \) , and is understood from
      context .
5. We say sets \( A \) and \( B \) are _disjoint_ if \( A \ cap B =\ emptyset \)

Output :
[" union " , " intersection " , " set - theoretic difference " , " complement " , " disjoint "]

Example 2:
Definition :
** Definition 6.1** (\(\ mathsf {{ RCA }} _ {{0}}\) ) .: An _integral domain_ is a ring \( R \) with no nonzero
      zero - divisors

Output :
[" integral domain "]



                                      Figure 8: Prompt for name extraction
You are an expert mathematician and a specialist in formal mathematics , especially Lean 4 and mathlib4 .

Your task is to identify all mathematical references that appear in a given mathematical definition ,
     theorem , lemma , or statement .

A reference is any term , symbol , or phrase whose meaning depends on a previously defined mathematical
     object , entity , or external context .

You must classify each reference into exactly one of the following categories .

--------------------------------------------------
REFERENCE TYPES
--------------------------------------------------

1. " object_reference "

A standard , named mathematical object , structure , property , or concept whose definition exists
     independently of the current text .

Examples :
- group
- topological space
- metric space
- compact space
- real number
- real vector space
- group homomorphism
- general linear group
- continuous function
- prime number
- finite set

Include :
- Named mathematical structures
- Named mathematical properties if they have formal definitions
- Standard named constructions

Do NOT include :
- Generic words like " element " , " set " , " function " , " number "
- Logical words like " if " , " then " , " and " , " exists "
- Less specific forms of an object . I . e . , in the sentence " Let G be an abelian group " , you should
     include " abelian group " , NOT " group ".

--------------------------------------------------

2. " entity_reference "

A reference to a specific previously defined , labeled , or numbered mathematical item .

Examples :
- Definition 3.4
- Theorem 2.1
- Lemma 5
- Proposition 4.2
- Corollary 1.3
- previous lemma
- above theorem
- following definition




                                                            17
These refer to specific formal entities in the document structure .

--------------------------------------------------

3. " l o c a l _ v a r i a b l e _ r e f e r e n c e "

A symbol that refers to a mathematical object but is NOT explicitly introduced in the current text .

A symbol is explicitly introduced if the current text declares it using phrases such as :

-    let M be ...
-    suppose M is ...
-    fix M ...
-    given M ...
-    where M is ...
-    for M a ...
-    denote by M ...
-    let M := ...
-    assume M is ...
-    take M ...
-    any equivalent explicit declaration

If a symbol is explicitly introduced in the current text , DO NOT include it .

Only include symbols that are used WITHOUT being introduced .

EXAMPLES

Example :

Text :
" Let G be a group . Then G is abelian iff the center of G equals G ."

Reasoning :
- G is explicitly introduced -> exclude
- group is a named object -> include
- abelian is a named property -> include
- center is a named construction -> include

Output :
[
  {" term ": " group " , " reference_type ": " object_reference "} ,
  {" term ": " abelian " , " reference_type ": " object_reference "} ,
  {" term ": " center " , " reference_type ": " object_reference "}
]

--------------------------------------------------

Example :

Text :
" M is compact iff G is abelian ."

Reasoning :
- M not introduced -> include                            local_variable_reference
- G not introduced -> include                            local_variable_reference
- compact is a named property                            -> include object_reference
- abelian is a named property                            -> include object_reference

Output :
[
  {" term ":        " M " , " reference_type ": " l o c a l _ v a r i a b l e _ r e f e r e n c e "} ,
  {" term ":        " G " , " reference_type ": " l o c a l _ v a r i a b l e _ r e f e r e n c e "} ,
  {" term ":        " compact " , " reference_type ": " object_reference "} ,
  {" term ":        " abelian " , " reference_type ": " object_reference "}
]

--------------------------------------------------

If no references exist , output :

[]



                                                         Figure 9: Prompt for reference extraction
You are a meticulous expert in Lean 4 and ‘ mathlib4 ‘.

Your task is to act as a " grounding " reasoner for a formalization agent . Your goal is to determine
     whether a given mathematical concept has a canonical formal definition in ‘ mathlib ‘ , based on a
     list of search candidates .

--------------------------------------------------
Your Task ( Follow These Steps PRECISELY )
--------------------------------------------------

--------------------------------------------------
Step 1: Direct Match Analysis
--------------------------------------------------

- First , look for a ** direct , canonical definition ** among the candidates .




                                                                                   18
- A direct match is typically a ‘ class ‘ , ‘ structure ‘ , or ‘def ‘ whose name is very similar to the
     concept name .

  Example :
  - Concept : " local ring "
  - Match : ‘ class IsLocalRing ‘

- If you find a clear , direct match , use that as your primary answer .

--------------------------------------------------
Step 2: Deduction from Usage Patterns
( Only if no direct match is found in Step 1)
--------------------------------------------------

- If no direct match was found in Step 1 , your task is to ** deduce ** the canonical name by finding a **
     consistent usage pattern ** across multiple ‘ theorem ‘ and ‘ instance ‘ candidates .

- ** Analyze the signatures :**
  Look for a common identifier that is consistently used as a ** type ** or ** typeclass ** across multiple
         candidates .

- ** Example :**
  If you are looking for " CharZero " and the search results include :
  - ‘ instance : CharZero N ‘
  - ‘ instance : CharZero Z ‘
  - ‘ theorem my_thm [ CharZero R ] ‘

  Then the identifier ‘ CharZero ‘ appears repeatedly as a typeclass . This is overwhelming evidence that
       the canonical definition is named ‘ CharZero ‘.

- ** Strict Rule :**
  The name you select ** must ** be an identifier that is explicitly present in the candidate list .

  - Do ** not ** invent , combine , or guess a new name .
  - If no single , consistent pattern emerges from the candidates , you must conclude that no confident
       match can be found .

--------------------------------------------------
Step 3: Final Decision
--------------------------------------------------

- Based on your analysis from Step 1 and Step 2 , determine the single best candidate for the concept .

- Your answer MUST be a single , valid JSON object with the following keys :

  - ‘" best_match " ‘:
    The ** list index ** of the candidate which precisely matches the search query . If no confident match
           can be found through either direct matching or inference , the value must be ‘ null ‘.

  - ‘" reasoning " ‘:
    An explanation of why you chose a match , or didn ’ t choose any match .



Figure 10: Prompt for grounding entities to mathlib. 10 candidate results are fed into this prompt,
and the output is an index of the best match and a reasoning.

C    Additional Experimental Details
We use vLLM [16] as an efficient inference server for all of our dataset construction, autoformalization,
and evaluation. If specified, we use the author’s recommended sampling parameters. Otherwise, we
use a temperature of 0.5, a top-p of 0.95, and otherwise default parameters for all autoformalization
experiments. We use deterministic sampling for our semantic faithfulness systems.
All experiments were run on a single H200 GPU. Depending on the model, full-benchmark runs
run from 1-10 hours. Checking compilation runs on 10 cpu workers for approximately 5 minutes.
Measuring faithfulness runs for ∼1-2 hours, depending on the number of successfully compiling
examples.

D    Broader impacts
We release MathAtlas with the hope to advance the field of autoformalization, and with it, AI and
mathematics in general. This outcome can potentially have larger societal impact as AI becomes
more powerful and more widely used. However, it is unlikely that this contribution in particular will
have large-scale negative ramifications.




                                                      19
Table 5: Autoformalization results on the “open” split of MathAtlas. The results listed here are
similar to those in Table 3, but restricted to a subset of the data.
                                                        Model               Compiles     Faithful   Correct
                                                                            Fine-tuned
                                                       Herald 7B            11.8%      14.4%        1.7%
  Model               Compiles Faithful Correct Kimina 7B                   27.1%      8.1%         2.2%
                                                       ATLAS-L 8B           20.1%      16.9%        3.4%
                      Prompted                         Goedel 8B            18.9%      37.6%        7.1%
  gpt-oss-20b (zs)    9.5%          48.4%        4.6%  Goedel 32B           22.3%      32.7%        7.3%
   +few-shot          16.3%         47.2%        7.7%  ReForm 8B            18.1%      50.8%        9.2%
   +tuned prompt      16.8%         47.6%        8.0%
   +tuned exs.        19.9%         60.3%        12.0%                      Prompted
                                                       gpt-oss-20b (zs)     9.3%         49.5%      4.6%
  gpt-oss-120b (zs) 13.0%           49.2%        6.4%   +few-shot           16.5%        35.8%      5.9%
   +few-shot          24.2%         57.0%        13.8%  +tuned prompt       16.8%        32.7%      5.5%
   +tuned prompt      26.0%         58.8%        15.3%  +tuned exs.         19.1%        35.1%      6.7%
   +tuned exs.        27.4%         62.0%        17.0%
                                                       gpt-oss-120b (zs)    15.5%        43.2%      6.7%
  (a) Autoformalization results for definitions.        +few-shot           16.3%        44.2%      7.2%
  The best performance in each category and             +tuned prompt       17.1%        43.9%      7.5%
  column are bolded.                                    +tuned exs.         20.7%        38.6%      8.0%

                                                        (b) Autoformalization results for statements (the-
                                                        orems, examples, and exercises). The best perfor-
                                                        mance in each category and column are bolded.




                                                   20
