                                                                           Large Language Model for OWL Proofs
                                                                Hui Yang                                              Jiaoyan Chen                                     Uli Sattler
                                                  The University of Manchester                               The University of Manchester                   The University of Manchester
                                                         Manchester, UK                                            Manchester, UK                                   Manchester, UK
                                                  hui.yang-2@manchetser.ac.uk                              jiaoyan.chen@manchester.ac.uk                    uli.sattler@manchester.ac.uk

                                         Abstract                                                                                asking them to select correct answers from given options or verify
                                         The ability of Large Language Models (LLMs) to perform reasoning                        reasoning processes.
                                         tasks such as deduction has been widely investigated in recent years.                      The more comprehensive and realistic proof construction and
                                         Yet, their capacity to generate proofs—faithful, human-readable                         presentation abilities of LLMs remain underexplored. Specifically,
                                         explanations of why conclusions follow—remains largely under-                           can LLMs effectively perform proof construction when given a con-
                                                                                                                                 clusion and a set of potential premises? This task requires simulta-
arXiv:2601.12444v1 [cs.AI] 18 Jan 2026




                                         explored. In this work, we study proof generation in the context
                                         of OWL ontologies, which are widely adopted for representing                            neously identifying necessary logical information and generating
                                         and reasoning over complex knowledge, by developing an auto-                            correct, interpretable consequences—a significantly more challeng-
                                         mated dataset construction and evaluation framework. Our evalu-                         ing problem than traditional reasoning evaluation. Furthermore,
                                         ation encompassing three sequential tasks for complete proving:                         how do LLMs perform when available premises are incomplete
                                         Extraction, Simplification, and Explanation, as well as an additional                   or only partially specified, reflecting real-world scenarios where
                                         task of assessing Logic Completeness of the premise. Through ex-                        perfect information is rarely available?
                                         tensive experiments on widely used reasoning LLMs, we achieve                              In this work, we investigate this realistic LLM evaluation prob-
                                         important findings including: (1) Some models achieve overall                           lem on proof construction using OWL (Web Ontology Language)
                                         strong results but remain limited on complex cases; (2) Logical                         ontologies [9], a widely adopted formalism for semantic reasoning
                                         complexity, rather than representation format (formal logic lan-                        across domains such as the Semantic Web [21], healthcare [44],
                                         guage versus natural language), is the dominant factor shaping                          and finance [4]. OWL ontologies serve two key purposes: (i) they
                                         LLM performance; and (3) Noise and incompleteness in input data                         provide formal, specific, shared, and machine-readable knowledge
                                         substantially diminish LLMs’ performance. Together, these results                       representations as collections of axioms, and (ii) they enable au-
                                         underscore both the promise of LLMs for explanation with rig-                           tomated reasoning over existing axioms to infer new knowledge,
                                         orous logics and the gap of supporting resilient reasoning under                        underpinned by Description Logic (DL).
                                         complex or imperfect conditions. Code and data are available at                            Different from prior benchmarks that evaluate whether LLMs
                                         https://github.com/HuiYang1997/LLMOwlR.                                                 contain knowledge expressed in ontologies [5, 36, 48, 56], or can
                                                                                                                                 perform deductive inference over ontologies [18, 39, 56], we focus
                                         CCS Concepts                                                                            on evaluating the proving abilities of LLMs over OWL ontologies.
                                                                                                                                 To this end, we define three tasks of increasing difficulty (illustrated
                                         • Computing methodologies → Description logics; Natural
                                                                                                                                 in Figure 1):
                                         language generation.
                                                                                                                                 (1) Extraction. Identify and extract a set of axioms sufficient to
                                         ACM Reference Format:                                                                       infer the target conclusion. This evaluates both completeness
                                         Hui Yang, Jiaoyan Chen, and Uli Sattler. 2026. Large Language Model for
                                                                                                                                     (capturing all necessary supporting axioms) and conciseness
                                         OWL Proofs. In Proceedings of the ACM Web Conference 2026 (WWW ’26),
                                         April 13–17, 2026, Dubai, United Arab Emirates. ACM, New York, NY, USA,
                                                                                                                                     (avoiding irrelevant axioms).
                                         17 pages. https://doi.org/10.1145/XXXXXX.XXXXXX                                         (2) Simplification. For each extracted supporting axiom, rewrite
                                                                                                                                     it into a simplified one by keeping only the essential parts that
                                                                                                                                     contribute to the derivation of the target conclusion.
                                         1    Introduction                                                                       (3) Explanation. Given a conclusion and its supporting axioms,
                                         In recent years, analyzing the logical reasoning capabilities of                            produce a logically valid, coherent, and understandable proof
                                         Large Language Models (LLMs) has attracted considerable attention                           that demonstrates how the conclusion is inferred.
                                         [28, 32, 37]. Prior work has explored multiple facets of reasoning
                                                                                                                                    Moreover, in real-world scenarios, logical information is often
                                         tasks, including deduction [8, 18, 41, 45], induction [43], constraint
                                                                                                                                 written informally in natural language and may be incomplete for
                                         satisfaction problems [29] and combinations of multiple reasoning
                                                                                                                                 inferring the target conclusion. To capture these scenarios, we intro-
                                         paradigms [16, 23, 33, 38, 46, 50, 55]. However, most studies focus
                                                                                                                                 duce two additional evaluation dimensions: formal logic language
                                         narrowly on individual aspects of logical reasoning under idealized
                                                                                                                                 versus natural language and complete versus incomplete premises. In
                                         conditions, such as providing LLMs with complete premise sets and
                                                                                                                                 the case of incomplete premises, a natural question arises: are the
                                                                                                                                 given premises sufficient to derive the target conclusion? We frame
                                                                                                                                 this as a Logic Completeness task within the incomplete-premise
                                         This work is licensed under a Creative Commons Attribution 4.0 International License.   setting.
                                         WWW ’26, Dubai, United Arab Emirates.                                                      In summary, our evaluation goes beyond traditional reasoning
                                         © 2026 Copyright held by the owner/author(s).
                                         ACM ISBN 979-8-4007-2307-0/2026/04                                                      tasks such as extracting relevant axioms and generating proofs.
                                         https://doi.org/10.1145/XXXXXX.XXXXXX                                                   We also investigate more complex, realistic scenarios that classical
WWW ’26, April 13–17, 2026, Dubai, United Arab Emirates.                                                                   Hui Yang, Jiaoyan Chen, and Uli Sattler


                                                                                                    Task 1: Extraction
 Query: Why DomesticDog is subclass of CompanionAni-
                                                                            Extract relevant ontological axioms:
 mal?
 (i.e., prove conclusion: DomesticDog ⊑ CompanionAnimal)                    • DomesticDog ⊑ Mammal (from ontology.org)
                                                                            • CompanionAnimal ≡ Animal ⊓ ∃ hasOwner.Human (petcare.com)
                                                                            • DomesticDog ≡ ∃ hasOwner. Human ⊓ Dog (from biology.edu)
                                 Relevant Web Ontologies

 ontology.org/animal:
 DomesticDog ⊑ Mammal                                                                            Task 2: Simplification
 Mammal ⊑ Animal




                                                                                                                                                                     Increasing Difficulty
                                                                            Simplify axioms of complex ontological expressions:
 ...
                                                                            • CompanionAnimal ≡ Animal ⊓ ∃ hasOwner.Human
                                                                              → Animal ⊓ ∃ hasOwner.Human ⊑ CompanionAnimal
 petcare.com/taxonomy:                                                      • DomesticDog ≡ ∃ hasOwner. Human ⊓ Dog
 CompanionAnimal ≡ Animal ⊓ ∃hasOwner.Human                                   → DomesticDog ⊑ ∃ hasOwner.Human
 Fish ⊑ ∃livesIn. AquaticEnvironment
 ...
                                                                                                  Task 3: Explanation
 biology.edu/species:                                                    Describe reasoning process:
 DomesticDog ≡ ∃hasOwner. Human ⊓ Dog
                                                                         Step 1: DomesticDog ⊑ Animal ⊓ ∃ hasOwner.Human
 Bird ⊑ ∃canPerform. Flying                                                BECAUSE DomesticDog ⊑ Mammal ⊑ Animal AND
 ...                                                                       DomesticDog ⊑ ∃ hasOwner.Human
                                                                         Step 2: DomesticDog ⊑ CompanionAnimal
                                                                           BECAUSE Animal ⊓ ∃ hasOwner.Human ⊑ CompanionAnimal AND Step 1



                                Figure 1: LLMs for proof construction and presentation with Web ontologies


ontology reasoners cannot address—specifically, cases where logical         2     Related Work
information is expressed informally in natural language, or where              LLM Evaluation on Logical Reasoning. Evaluating the logical
the set of premises is incomplete.                                          reasoning capabilities of LLMs has emerged as a central research di-
   To facilitate systematic evaluation, we propose an automatic             rection. Prior work has primarily focused on tasks such as deductive
dataset construction and evaluation framework that can support ar-          reasoning [8, 41, 45], inductive reasoning [43], constraint satisfaction
bitrary OWL ontologies of DL EL, and investigate state-of-the-art           problems [29], and hybrid settings that combine multiple reasoning
reasoning LLMs of different sizes, including the DeepSeek-R1 family,        paradigms (e.g., non-monotonic reasoning) [16, 23, 33, 38, 46, 55].
the Qwen3 family, GPT-o4-mini and Magistral. Through extensive              However, most existing benchmarks assume clean and complete
evaluation across diverse cases on three real-world ontologies, we          premise sets. They are typically constructed by instantiating ab-
gain a deeper understanding of LLMs’ reasoning capabilities with            stract rules from formal logics (e.g., propositional or first-order
several important findings, including:                                      logic) with synthetic symbols or entities1 . While systematic, such
                                                                            approaches abstract away from commonsense and domain-specific
                                                                            knowledge. In contrast, our work leverages real-world ontologies
(1) Some models, such as GPT-o4-mini and Qwen3-32B, achieve                 from diverse domains. Ontologies encode both semantic richness
    strong overall results but remain limited when confronted with          and logical structure, making them a natural resource for evaluating
    conclusions that require complex derivation patterns beyond             LLMs’ ability to reason under incomplete premises while remaining
    transitive closures.                                                    grounded in real-world semantics.
(2) The primary determinant of performance lies in the underlying
    logical complexity of the task, rather than the form of expression         LLMs on Ontologies. The application of LLMs to ontology engi-
    (e.g., formal logic language vs. natural language).                     neering and reasoning has attracted increasing attention. Existing
(3) The greatest challenges arise from noise and incompleteness             research can be broadly divided into two categories: (1) Ontology
    in the input: performance on reasoning tasks can decline con-           construction and validation, which include constructing new ontolo-
    siderably, dropping by up to 47% with substantial irrelevant            gies axioms from text [12, 13, 31, 34], evaluating ontology knowl-
    information and up to 38% with missing premises.                        edge captured by pre-training LLMs [5, 36, 48, 56], and validation
                                                                            of ontology correctness or abilities [30, 40, 47] ; and (2) Subsump-
                                                                            tion prediction and inference, which investigates whether LLMs can
These findings provide valuable insights for future research on             predict subsumptions in zero-shot, few-shot or finetuning settings
complex LLM reasoning problems such as explainable knowledge                and deductive reasoning capabilities [18, 19, 39, 51, 56].
retrieval and generation, which aims to find exactly necessary ma-
                                                                            1 E.g., given the premise in first-order logic {𝑝 (𝑥 ),  ∀𝑥 . 𝑝 (𝑥 ) → 𝑞 (𝑥 ) } , one can
terials from a knowledge base towards requests that require logical
                                                                            derive 𝑞 (𝑥 ) . Replacing 𝑥 by a person (e.g., Tom) and 𝑝, 𝑞 by some attributes (𝑝 : likes
proving (such as answering natural language questions with attri-           apples; 𝑞 : likes oranges), one obtain the natural language form with premise ‘Tom likes
butions [10, 20]).                                                          apples. Anyone who likes apples likes oranges" and conclusion Tom likes oranges".
Large Language Model for OWL Proofs                                                            WWW ’26, April 13–17, 2026, Dubai, United Arab Emirates.


   However, these works devote less attention to the more complex              selection, we introduce a distance measure atomic distance for
proving context highlighted in the introduction. Such contexts in-             each subsumption and select axioms across different distance
volve explanation generation and logical evidence retrieval, both              ranges (details in Section 4.1).
of which are crucial for practical applications. In this work, we          (2) We then introduce noisy axioms based on semantic distances
address this gap by evaluating the proving ability of LLMs over on-            computed using embedding models. These noisy axioms do
tologies, focusing on atomic subsumptions and their corresponding              not belong to any justification for the given conclusion, which
justifications [1, 22, 24, 52].                                                guarantees that the golden answer remains the only correct
                                                                               answer (details in Section 4.2).
3    Preliminaries                                                            During evaluation, we shuffle the order of both the original and
Ontologies represent knowledge using sets of statements, called            noisy axioms, and prompt the LLMs to generate detailed explana-
axioms, which describe concepts (unary predicates) and roles (bi-          tions using prompt learning techniques (for details see Appendix
nary predicates). In this work, we focus on EL-ontologies, which           A).
are based on the Description Logic fragment of EL and are widely
applied in domains such as biomedicine [3]. Let NC = {𝐴, 𝐵, . . .},        4.1    Selecting Conclusions
NR = {𝑟, 𝑡, . . .}, and NI = {𝑎, 𝑏, . . .} denote pairwise disjoint sets   Given an ontology O, our construction method focus on inferred
of concept names, role names, and individual names, respectively.          atomic subsumptions of the form O |= 𝐴 ⊑ 𝐵, where 𝐴 and 𝐵 are
EL-concepts are defined recursively as 𝐶 ::= ⊤ | 𝐴 | 𝐶 ⊓ 𝐷 | ∃𝑟 .𝐶,        atomic concepts (i.e., 𝐴, 𝐵 ∈ N𝐶 ). To ensure that the selected sub-
where 𝐴 ∈ NC , 𝑟 ∈ NR , and 𝐶, 𝐷 are EL-concepts. An EL-ontology           sumptions cover broad cases, we introduce a metric over atomic
O is a finite set of axioms consisting of General Concept Inclusions       subsumptions, denoted as atomic distance, and select them uni-
(GCIs) axioms 𝐶 ⊑ 𝐷, where 𝐶 and 𝐷 are (complex) EL-concepts,              formly across different distance levels. The atomic distance serves
and facts about individuals in NI . In this work, we focus mainly          as a heuristic for estimating the “reasoning length” of an atomic
on the GCIs, by which complex logical relationships are usually            subsumption, measured by the number of intermediate atomic con-
defined.                                                                   cepts involved. Specifically:
   Example 1. Consider a small university EL-ontology with atomic          (1) Distance 1 (Direct Subsumption): A subsumption 𝐴 ⊑ 𝐵 has
concepts Student, Graduate, Course, and role enroll. We can de-                distance 1 if O |= 𝐴 ⊑ 𝐵 and there exists no atomic concept
fine two axioms: Graduate ⊑ Student, Student ⊑ ∃enroll.Course.                 𝐴′ ∉ {𝐴, 𝐵} such that both O |= 𝐴 ⊑ 𝐴′ and O |= 𝐴′ ⊑ 𝐵.
                                                                           (2) Distance 𝑘 (Indirect Subsumption for 𝑘 ≥ 2): More generally,
From an ontology O, new axioms can be inferred through logical                 for an atomic subsumption O |= 𝐴′ ⊑ 𝐵 ′ , the atomic distance
reasoning. For example, given 𝐴 ⊑ 𝐵 and 𝐵 ⊑ 𝐶 in O, one can                    of 𝐴′ ⊑ 𝐵 ′ is defined as the minimal number 𝑘 such that there
derive 𝐴 ⊑ 𝐶, written as O |= 𝐴 ⊑ 𝐶. For formal definition of                  exists a chain of direct subsumptions
entailment “|=” based on interpretations and models, please refer
to [3].                                                                      𝐴0 ⊑ 𝐴1, 𝐴1 ⊑ 𝐴2, . . . , 𝐴𝑘 −1 ⊑ 𝐴𝑘 , where 𝐴0 = 𝐴′, 𝐴𝑘 = 𝐵 ′ .
                                                                              Remark 1. It is worth noting that a subsumption O |= 𝐴 ⊑ 𝐵 with
4    Dataset Construction                                                  a higher atomic distance typically has justifications involving more
Now, we describe the construction of our dataset, designed to eval-        axioms. When the atomic distance coincides with the number of justi-
uate the three tasks introduced earlier. The main idea is based on         fications, the derivation pattern often follows directly from transitive
the concept of justifications for a conclusion, which captures the         closure. For example, in O = {𝐴 ⊑ 𝐴1, 𝐴1 ⊑ 𝐴2, . . . , 𝐴𝑘 −1 ⊑ 𝐴𝑘 },
minimal set of axioms required to entail that conclusion. Intuitively,     the subsumption O |= 𝐴 ⊑ 𝐴𝑘 has both atomic distance and num-
each justification provides the essential premise requirement for          ber of justifications equal to 𝑘, corresponding to the straightforward
inferring the given entailment. The formal definition is given below:      transitive chain 𝐴 ⊑ 𝐴1 ⊑ . . . ⊑ 𝐴𝑘 .
                                                                              In contrast, when the justifications contain more axioms than the
   Definition 1 (Justification). Let O be an ontology and 𝛼 a
                                                                           atomic distance, the derivation usually involves more intricate rea-
conclusion with O |= 𝛼. An axiom subset 𝐽 ⊆ O is a justification for
                                                                           soning patterns, and we classify such cases as complex. For instance,
𝛼 if 𝐽 |= 𝛼, and no proper subset of 𝐽 entails 𝛼 (i.e., no 𝐽 ′ ⊊ 𝐽 such
                                                                           consider O ′ = {𝐴 ⊑ ∃𝑟 .𝐵, 𝐵 ⊑ 𝐵 1, ∃𝑟 .𝐵 1 ⊑ 𝐴1 }. Here, the subsump-
that 𝐽 ′ |= 𝛼).
                                                                           tion O ′ |= 𝐴 ⊑ 𝐴1 has atomic distance 1, since there is no intermediate
   Justifications provide the foundation for the extraction, simpli-       concept 𝐴′ with O ′ |= 𝐴 ⊑ 𝐴′ ⊑ 𝐴1 . However, the number of justifi-
fication, and explanation tasks in our dataset, as they capture the        cations is 3, reflecting the use of more sophisticated reasoning based
minimal set of axioms required to support each conclusion. It is im-       on the existential operator “∃𝑟 ”.
portant to note that a single conclusion may have multiple distinct
justifications. For simplicity, in both the construction of the dataset    4.2    Selecting Noisy Axioms
and our experiments, we consider only the justification of minimal         Since real-world ontologies can be extremely large (e.g., Snomed
size, i.e., the one containing the fewest axioms.                          CT contains over 350,000 axioms) and it is impractical and costly
   The construction of the dataset proceeds in two main steps:             to feed them all into LLMs directly for evaluating the extraction
(1) We first randomly select subsumption axioms as the target              task, we construct the input by adding noisy axioms into the golden
    conclusions along with their corresponding justifications as           justification as follows. We introduce noisy axioms primarily based
    the golden answers for extraction. To ensure a well-distributed        on their semantic interpretations. Specifically, we first translate
WWW ’26, April 13–17, 2026, Dubai, United Arab Emirates.                                                     Hui Yang, Jiaoyan Chen, and Uli Sattler



                                                                               Inference Rules

                                                                               ## Inference Rules
                                                                               1. Subsumption: If A ⊑ B and B ⊑ C, then A ⊑ C
                                                                               2. Conjunction: If A ⊑ B, A ⊑ C, then A ⊑ B ⊓ C
                                                                               3. Existential: If A ⊑ ∃r.C and C ⊑ D, then A ⊑ ∃r.D
                                                                               4. Equivalence: If A ≡ B, then A ⊑ B and B ⊑ A
                                                                               5. Conjunction Inference: If A ⊑ B ⊓ C, then A ⊑ B
                                                                               and A ⊑ C
                                                                               Here, A, B, C, ... means concept, r means roles. ⊑
                                                                               means subclass, ≡ means equivalence, ∃𝑟 .𝐴 means the
                                                                               set of elements in A that have a relationship r with
                                                                               A.


                                                                                  Figure 3: Inference Rules (for EL-ontologies)
Figure 2: Distribution of the selected conclusions (subsump-
tions).
                                                                         our code for generating more sample according to their interest.
                                                                         Specifically, from Snomed CT, we randomly extract 350 conclusions.
both the given conclusion and each axiom in the ontology into            For the other two ontologies, whose logical structures are simpler,
natural language sentences according to their semantic meanings.         we select 70 conclusions from each. All conclusions are chosen with
Then, we select noisy axioms by measuring their semantic distance        an even atomic distance range uniformly spanning from 4 to 16. We
using sentence embedding models, which evaluate the degree of            filter out the non-EL axioms that contains non-EL constructors
semantic similarity between sentences.                                   (e.g., ¬). The distribution of these selected conclusions (subsump-
   In details, following [18], for an axiom of the form 𝐶 ⊑ 𝐷 (resp.     tions), over different atomic-distances and different justification
𝐶 ≡ 𝐷), the corresponding sentence is: V (𝐶) is a subclass of V (𝐷)      sizes (i.e., numbers of axioms) are shown in the Figure 2.
(resp. V (𝐶) is equivalent to V (𝐷)), where V (𝐶) and V (𝐷) denote
the verbalization of the concepts 𝐶 and 𝐷, generated composition-        5 Evaluation Methods and Settings
ally by the following rules:
                                                                         5.1 Methods
          V (𝐶 ⊓ 𝐷) = ”V (𝐶) and V (𝐷)”,
                                                                         We test the performance based on prompt-based method with two
           V (∃𝑟 .𝐶) = ”something that V (𝑟 ) some V (𝐶)”.               options: (1) supplying a set of inference rules to guide reasoning
For instance, we have V (Person ⊓ Student) =“person and student",        over EL-ontologies, as illustrated in Figure 3; or (2) providing
V (∃isParentOf.Person) =“something that is parent of some per-           examples, such as the one in Figure 4 (detailed in Appendix A).
son". Similarly, conclusions 𝐶 ⊑ 𝐷 are transformed into query-like          The evaluated language models span both open-source and com-
sentences of the form: “Why is V (𝐶) a subclass of V (𝐷)?". Finally,     mercial systems: (1) Open-source models: The 32B models com-
noisy axioms are selected based on their embedding distances, with       prise DeepSeek-R1-Distill-Qwen-32B, Qwen3-32B, and Qwen2.5-32B,
embedding vectors computed using the sentence embedding model            the 24B model by Magistral-Small-2506, and the 8B models Qwen3-
BGE [49].                                                                8B, DeepSeek-R1-Distill-Qwen-8B, and DeepSeek-R1-Distill-Llama-
   One could consider extracting noisy axioms based on logical           8B; (2) Commercial baseline: GPT-o4-mini, a cost-effective com-
structures, such as the hypergraph-based representations proposed        mercial model that demonstrates strong performance. This orga-
by [35, 53] or ontology modules [6, 11, 26, 42, 52, 54]. However,        nization enables systematic comparisons across model scale, ar-
this approach requires a more detailed discussion of the selection       chitecture, and source type. For all LLMs tested, the max token
process and additional effort to control the size of the selected        limit is 5,000, with temperature fixed at 0 as convention to ensure
result. For simplicity, we instead rely on semantic meaning, which       reproducibility and enable fair comparison across models.
is more convenient and better suited to our experimental setup. In
particular, our experiments also investigate the impact of the natural   5.2     Metrics
language forms of axioms (Section 6.2.2), rather than focusing solely    Format Correctness Rate This metric measures the percentage
on formal logical expressions.                                           of samples in which the LLM produces outputs that adhere to the
                                                                         required format. That is, the output includes the three sections
4.3     Constructed Dataset                                              AXIOMS_USED, SIMPLIFY, and DERIVE, as illustrated in Figure 4.
We use three widely used, large-scale ontologies—Snomed CT [44],         Note that a high generation success rate indicates that the reasoning
Foodon [15], and GO-Plus [2], which have been used for eval-             LLMs have robust formatting ability or their reasoning processes
uation in many previous works [7]. They may infer millions of            are relatively brief, but it does not guarantee the correctness of the
subsumptions (detailed statistic given by Figure 12 in Appendix).        results.
Due to the computer source limitations, we only select part of them      Extraction We evaluate extraction performance using the Jaccard
in our evaluation. It should be noted that other researchers can use     Similarity, defined as (𝑆 denotes the output axiom set in the section
Large Language Model for OWL Proofs                                                                           WWW ’26, April 13–17, 2026, Dubai, United Arab Emirates.


                                                                                          (2) Overall Accuracy: A derivation is fully correct if all individual
     Example
                                                                                              steps meet the step-level criteria and the target conclusion is
     ## Example                                                                               successfully derived.
     Given the following axioms:                                                          (3) Derivation Steps: This measures the total steps that the output
     [1] A ≡ ∃r.B                                                                             derivations have.
     [2] C ⊑ B ⊓ H ⊓ I                                                                       Remark 2. Most of the metrics introduced above can only be com-
     [3] D ≡∃r.C ⊓ G
                                                                                          puted when the output is in the correct format. To account for outputs
     [4] E ≡ A ⊓ F
     [5] D ⊑ F ⊓ J
                                                                                          with incorrect formatting, we also use a weighted version of each
     [6] D ⊑ K                                                                            metric, obtained by multiplying the format-correctness rate with the
     The desired explanation for deriving the conclusion D
                                                                                          corresponding metric.
     ⊑ E is as follows:
     **AXIOMS_USED**: 1,2,3,4,5                                                           6     Evaluation Results
     **SIMPLIFY**:                                                                        We begin with a standard setting, where the input axioms are
     [1] A ≡ ∃r.B → ∃r.B ⊑ A                                                              expressed in formal logic and contain the complete justification of
     [2] C ⊑ B ⊓ H ⊓ I → C ⊑ B                                                            the output conclusion as well as the same number of noisy axioms as
     [3] D ≡ ∃r.C ⊓ G → D ⊑ ∃r.C                                                          the justification. In Section 6.2, we extend our analysis to the more
     [4] E ≡ A ⊓ F → A ⊓ F ⊑ E
                                                                                          complex settings in which the input contains more noisy axioms,
     [5] D ⊑ F ⊓ J → D ⊑ F
                                                                                          axioms expressed in natural language, or incomplete premises.
     **DERIVE**:
     STEP1: [1,2,3] ⊢ D ⊑ A
     EXPLANATION: D ⊑ ∃r.C ∧ C ⊑ B ⇒ D ⊑ ∃r.B ∧ ∃r.B ⊑ A                                  6.1    Standard Setting
     ⇒ D ⊑ A                                                                              6.1.1 Performance of Different Evaluation Methods. The main re-
     STEP2: [STEP1,4,5] ⊢ D ⊑ E                                                           sults across all datasets are summarized in Table 1. We have the
     EXPLANATION: D ⊑ A ∧ D ⊑ F ⇒ D ⊑ A ⊓ F ∧ A ⊓ F ⊑                                     following observations for the overall best performance. For the
     E ⇒ D ⊑ E                                                                            format correctness rate, we observe that all relatively large mod-
                                                                                          els (≥32B) achieve strong performance, typically above 70% when
Figure 4: An example of the given input and desired output.                               inference rules are provided. Compared to GO-Plus and Foodon, the
The output is supposed to consist of three parts, AXIOMS_USED,                            format correctness on Snomed CT is generally lower, which may be
SIMPLIFY, and DERIVE, correspond to the tasks Extraction,                                 attributed to the comparatively higher complexity of derivations in
Simplification, and Derivation, respectively.                                             Snomed CT. This observation is also supported by the relatively low
                                                                                          accuracy observed on Snomed CT in the extraction, simplification,
                                                                                          and derivation tasks discussed below.
AXIOM_USED and 𝑆 gt denotes the ground-truth set):                                           For the extraction task, GPT-o4-mini and Qwen3-32B achieve
                                                                                          the best performance, with Jaccard similarity scores consistently
                                                   |𝑆 ∩ 𝑆 gt |                            exceeding 95% across different ontologies. In contrast, some mod-
                        Jaccard Similarity =
                                                   |𝑆 ∪ 𝑆 gt |                            els such as Qwen2.5-32B and DeepSeek-R1-Qwen-32B demonstrate
Simplification Performance on the simplification task is evaluated                        high format correctness but very low Jaccard similarity (below
using the following metrics, which assess both logical correctness                        50%). This discrepancy suggests that these models primarily cap-
and efficiency:                                                                           ture structural patterns rather than genuinely understanding the
                                                                                          reasoning process.
(1) Axiom-wise Accuracy: A single-axiom simplification is correct                            For the simplification task, we find that GPT-o4-mini consis-
    if its simplified form is logically entailed by the original axiom                    tently achieves the highest accuracy, exceeding 90% across all the
    (e.g., {𝐴 ≡ 𝐶} |= 𝐶 ⊑ 𝐴).                                                             three datasets. Qwen3-32B ranks second, performing substantially
(2) Overall Accuracy: A simplification is fully correct if all individ-                   better than the remaining models but still lagging by around 40%
    ual axioms are correctly simplified and the target conclusion                         behind GPT-o4-mini in weighted overall accuracy on Snomed CT.
    remains derivable from the simplified forms.                                          However, the performance gap is much smaller (< 10%) on other
(3) Length-drop Percentage: This metric quantifies the efficiency                         two datasets: GO-Plus and Foodon.
    of simplification by measuring the total reduction in axiom                              Moreover, when evaluating simplification efficiency based on
    length2 .                                                                             the length-drop percentage, we find that Snomed CT exhibits sub-
Derivation Analogous to the simplification case, we measure per-                          stantially higher reductions (typically >25%) compared to GO-Plus
formance on the derivation task using:                                                    and Foodon (typically <5%). This is primarily because axioms in
(1) Step-wise Accuracy: A derivation step is correct if the conclusion                    Snomed CT are generally more complex than those in GO-Plus and
    logically follows from its premises and all premises are either                       Foodon, which usually consist of only atomic subsumptions (i.e.,
    given axioms or results of previously validated steps.                                𝐴 ⊑ 𝐵) that cannot be further simplified.
                                                                                             The performance on derivation tasks follows a similar pattern
2 Length is computed by assigning weight 1 to each logical operator, role, and concept,   to simplification: GPT-o4-mini achieves the best results, followed by
and weight 2 to equivalence (≡) .                                                         Qwen3-32B, which lags up to 33% behind GPT-o4-mini in weighted
WWW ’26, April 13–17, 2026, Dubai, United Arab Emirates.                                                                       Hui Yang, Jiaoyan Chen, and Uli Sattler


Table 1: Comparison of model performance (results presented as performance with/withthout inference rules). Format-Correct
denotes Format Correctness Rate of the generated response. The top 3 results for each metric are highlighted in red (1st), blue
(2nd), and orange (3rd).
                                   Format-           Jaccard                    Simplification Acc.                                   Derivation Acc.
  Model
                                   Correct             Avg.         axiom-wise         overall        length-drop     step-wise           overall         #|Steps|
                                                                    Snomed CT
  GPT-o4-mini                   83.43 / 92.26      99.19 / 99.66    98.66 / 97.97    91.78 / 91.93    27.04 / 26.55   97.21 / 93.06     93.49 / 86.02    7.86 / 7.02
  DeepSeek_R1_Llama-8B          58.86 / 60.86      68.18 / 66.21    78.57 / 76.14    34.58 / 29.78    23.85 / 24.90   49.39 / 51.48     14.02 / 14.22    4.59 / 4.20
  DeepSeek_R1_Qwen-32B          97.43 / 86.86      42.23 / 35.63    96.55 / 93.25     8.00 / 6.02     33.29 / 40.21   53.39 / 58.77      7.71 / 7.16     4.89 / 4.95
  DeepSeek_R1_Qwen-8B           15.71 / 16.57      52.63 / 49.34    77.16 / 72.96    40.48 / 29.41    15.82 / 23.91   63.85 / 73.44      8.33 / 7.84     8.17 / 6.90
  Qwen2.5-32B                   99.71 / 100.00     39.81 / 39.41    93.26 / 92.37     5.71 / 6.29     20.33 / 25.57   60.97 / 58.80      6.57 / 7.14     7.07 / 5.68
  Qwen3-32B                     73.71 / 29.71      95.87 / 82.28    97.97 / 97.12    69.47 / 51.33    30.24 / 29.70   94.15 / 88.03     72.14 / 61.95    7.31 / 6.50
  Qwen3-8B                      16.57 / 22.29      86.87 / 86.78    94.32 / 94.72    67.19 / 66.67    25.92 / 31.64   88.71 / 88.64     51.56 / 50.62    9.83 / 7.17
  Magistral-Small-2506          33.71 / 29.14      84.77 / 81.55    87.62 / 89.29    38.56 / 36.96    35.36 / 36.49   78.55 / 88.90     32.68 / 34.78    6.22 / 6.07
                                                                     GO-Plus
  GPT-o4-mini                   100.00 / 100.00   100.00 / 100.00   100.00 / 98.65   98.11 / 98.11     2.24 / 3.23    98.47 / 98.67     98.11 / 94.34    6.15 / 5.66
  DeepSeek_R1_Llama-8B           79.25 / 66.04     84.73 / 69.71     89.21 / 90.59   69.05 / 64.86     2.90 / 4.39    40.00 / 41.77     26.19 / 8.11     3.93 / 4.27
  DeepSeek_R1_Qwen-32B           98.11 / 81.13     47.18 / 36.69     97.04 / 77.87   13.46 / 1.96      1.67 / 7.76    56.67 / 52.07     17.31 / 15.69    4.04 / 3.31
  DeepSeek_R1_Qwen-8B            52.83 / 49.06     54.42 / 61.90     81.51 / 93.29   50.00 / 68.75    12.57 / 7.23    62.48 / 76.40     11.76 / 31.25   14.97 / 12.31
  Qwen2.5-32B                    96.23 / 96.23     45.44 / 46.94     97.51 / 95.35    9.80 / 5.88      0.09 / 3.02    54.73 / 59.57     11.76 / 15.69    6.63 / 4.61
  Qwen3-32B                      73.58 / 35.85     96.73 / 86.39     99.48 / 98.34   95.00 / 80.00     4.00 / 3.03    99.16 / 97.62     92.50 / 60.00    5.97 / 4.20
  Qwen3-8B                       32.08 / 52.83     85.45 / 95.92    98.21 / 100.00   84.21 / 82.76     1.42 / 0.80    94.78 / 98.80     78.95 / 82.76    7.05 / 8.59
  Magistral-Small-2506           54.72 / 54.72     84.08 / 84.00     92.23 / 92.79   55.88 / 65.62    10.30 / 6.78    73.62 / 84.06     44.12 / 37.50    6.91 / 6.47
                                                                      Foodon
  GPT-o4-mini                   100.00 / 100.00   100.00 / 100.00   99.29 / 99.18    100.00 / 97.14    1.91 / 3.55    95.07 / 95.09     88.57 / 91.43    6.96 / 6.40
  DeepSeek_R1_Llama-8B           70.00 / 64.29     87.62 / 76.31    91.07 / 83.45     56.00 / 54.35    1.16 / 1.15    55.51 / 52.63     26.00 / 15.22    5.08 / 4.13
  DeepSeek_R1_Qwen-32B           95.71 / 92.86     43.41 / 38.56    97.67 / 81.18     15.94 / 11.43    2.87 / 6.58    72.73 / 58.27     11.59 / 15.71    5.58 / 3.80
  DeepSeek_R1_Qwen-8B            48.57 / 32.86     42.08 / 58.57    70.70 / 90.74     50.00 / 46.67   12.31 / 10.81   67.30 / 86.40     5.26 / 30.00    20.76 / 9.07
  Qwen2.5-32B                    94.29 / 94.29     39.95 / 39.08    96.65 / 95.06     12.12 / 12.12    3.09 / 2.03    62.66 / 56.62     21.21 / 15.15    6.05 / 4.58
  Qwen3-32B                      74.29 / 37.14     97.58 / 90.11    97.65 / 95.57     90.38 / 73.08    5.29 / 6.91    91.36 / 91.39     90.38 / 65.38    7.79 / 5.81
  Qwen3-8B                       28.57 / 50.00     89.52 / 97.20    87.81 / 96.85     85.71 / 91.43    7.28 / 4.92    88.33 / 84.23     66.67 / 77.14   5.71 / 10.14
  Magistral-Small-2506           51.29 / 44.99     87.64 / 83.85    87.95 / 93.59     58.79 / 61.54    9.36 / 6.48    78.52 / 79.38     53.27 / 51.65    5.85 / 6.53


overall accuracy. Additionally, we find that derivations typically                    6.1.3 Impact of Examples. We investigate the effect of providing
require 7–8 steps on average. However, some models deviate sub-                       examples, still focusing on Qwen3-32B, GPT-o4-mini, and their cor-
stantially (e.g., >20 steps for DeepSeek-R1-Qwen-8B on Foodon),                       responding weighted values. Results are illustrated in Figure 6.
which is not reliable given their low overall derivation accuracy.                       For Qwen3-32B, the no-example setting yields a substantially
                                                                                      higher rate of format correctness compared to the setting with
                                                                                      examples. However, most of the outputs in the no-example case ap-
6.1.2 Impact of Inference Rules. We now examine the effect of
                                                                                      pear to be only formally correct but not logically valid: the case with
incorporating inference rules, focusing on the two best-performing
                                                                                      examples consistently achieves higher overall accuracy across all
models: Qwen3-32B and GPT-o4-mini. The results are presented in
                                                                                      three tasks, as reflected in higher Jaccard similarity, simplification
Figure 5. To ensure a fair comparison that accounts for incorrectly
                                                                                      and derivation overall accuracy. Specifically, for weighted overall
formatted outputs, in the rest of the paper, we focus on the
                                                                                      derivation accuracy, adding examples to the prompt can increase
weighted values (recall Remark 2) rather than the raw values
                                                                                      performance by up to 16-fold (e.g., from 3.82% to 61.95% on Snomed
reported in Table 1, unless stated otherwise.
                                                                                      CT). Interestingly, for axiom-wise simplification accuracy, the case
   For Qwen3-32B, the addition of inference rules yields consistently
                                                                                      without examples performs consistently better than the case with
strong benefits across all ontologies. Both the format correctness
                                                                                      examples. This may be due to the larger number of correctly for-
rate and the task-specific metrics—Jaccard average, simplification
                                                                                      matted outputs in the no-example case, which contribute many
accuracy, and derivation accuracy—improve substantially, with
                                                                                      correct axiom-wise simplifications and thus increase axiom-wise
gains of roughly two- to threefold.
                                                                                      accuracy.
   In contrast, the effect of inference rules on GPT-o4-mini is much
                                                                                         For GPT-o4-mini, the effect of examples is more uniform: per-
smaller. In the Snomed CT dataset, performance even declines
                                                                                      formance improves consistently across all metrics. However, the
across all metrics of success and accuracy. This suggests that GPT-
                                                                                      difference is much smaller than in the case of Qwen3-32B.
o4-mini has largely internalized the relevant inference rules during
training. As a result, explicitly encoding these rules in the prompt                  6.1.4 Performance on Different Conclusions. Figure 7 provides a
may instead degrade performance due to the increased input length.                    fine-grained illustration of the tested conclusions over Snomed
Large Language Model for OWL Proofs                                                                                                                                 WWW ’26, April 13–17, 2026, Dubai, United Arab Emirates.



      100
             Format-Cor   Jaccard Avg.
                                             With IR         Without IR
                                         Simp. Acc.(axiom) Simp. Acc.(overall) Deri. Acc.(step)   Deri. Acc.(overall)                                    Jaccard Avg.                    10019
                                                                                                                                                                                                               Jaccard Avg.              100
                                                                                                                                           19
                                                                                                                                           18                                               18
                                                                                                                                           17                                               17
       80                                                                                                                                  16                                            80 16                                           80
                                                                                                                                           15                                               15




                                                                                                                                                                                   #|Justification|
                                                                                                                        #|Justification|
       60                                                                                                                                  14                                               14
                                                                                                                                           13
                                                                                                                                           12                                            60 13
                                                                                                                                                                                            12                                           60
       40                                                                                                                                  11                                               11
                                                                                                                                           10                                               10
                                                                                                                                            9                                            40 9                                            40
       20                                                                                                                                   8                                                8
                                                                                                                                            7                                                7
                                                                                                                                            6                                            20 65                                           20
        0                                                                                                                                   5
            Qwen    GPT   Qwen    GPT     Qwen     GPT       Qwen     GPT       Qwen     GPT       Qwen      GPT                            4                                                4
                                                 Snomed CT                                                                                  3                                                3                                           0
                                                                                                                                                4    6     8   10   12   14   16         0            4    6     8   10   12   14   16
                                             With IR         Without IR
      100
             Format-Cor   Jaccard Avg.   Simp. Acc.(axiom) Simp. Acc.(overall) Deri. Acc.(step)   Deri. Acc.(overall)
                                                                                                                                                    Simp. Acc.(overall)                  10019
                                                                                                                                                                                                          Simp. Acc.(overall)            100
                                                                                                                                           19
                                                                                                                                           18                                               18
       80                                                                                                                                  17                                               17
                                                                                                                                           16                                            80 16                                           80
                                                                                                                                           15                                               15




                                                                                                                                                                                   #|Justification|
                                                                                                                        #|Justification|
       60                                                                                                                                  14                                               14
                                                                                                                                           13
                                                                                                                                           12                                            60 13
                                                                                                                                                                                            12                                           60
       40                                                                                                                                                                                   11
                                                                                                                                           11
                                                                                                                                           10                                               10
       20                                                                                                                                   9                                            40 9                                            40
                                                                                                                                            8                                                8
                                                                                                                                            7                                                7
        0                                                                                                                                   6                                            20 65                                           20
            Qwen    GPT   Qwen    GPT     Qwen     GPT       Qwen     GPT       Qwen     GPT       Qwen      GPT                            5
                                                   GO-Plus                                                                                  4                                                4
                                                                                                                                            3                                                3                                           0
                                                                                                                                                4    6     8   10   12   14   16         0            4    6     8   10   12   14   16
                                             With IR         Without IR
             Format-Cor   Jaccard Avg.   Simp. Acc.(axiom) Simp. Acc.(overall) Deri. Acc.(step)   Deri. Acc.(overall)
      100
                                                                                                                                                    Deri. Acc.(overall)                  10019
                                                                                                                                                                                                          Deri. Acc.(overall)            100
                                                                                                                                           19
       80                                                                                                                                  18                                               18
                                                                                                                                           17                                               17
       60                                                                                                                                  16                                            80 16                                           80
                                                                                                                                           15                                               15




                                                                                                                                                                                   #|Justification|
                                                                                                                        #|Justification|
                                                                                                                                           14                                               14
       40                                                                                                                                  13
                                                                                                                                           12                                            60 13
                                                                                                                                                                                            12                                           60
                                                                                                                                           11                                               11
       20                                                                                                                                  10                                               10
                                                                                                                                            9                                            40 9                                            40
                                                                                                                                            8                                                8
        0                                                                                                                                   7                                                7
            Qwen    GPT   Qwen    GPT     Qwen     GPT       Qwen     GPT       Qwen     GPT       Qwen      GPT                            6                                            20 65                                           20
                                                   Foodon                                                                                   5
                                                                                                                                            4                                                4
                                                                                                                                            3
                                                                                                                                                4    6     8   10   12   14   16         0 3          4    6     8   10   12   14   16   0
                                                                                                                                                         Atomic Distance                                       Atomic Distance
Figure 5: Comparison (weighted) of Qwen3-32B and GPT-o4-
mini with/without Inference Rules (IR).                                                                                                             (a) Qwen3-32B                                           (b) GPT-o4-mini
                                          With Example         No Example                                               Figure 7: Performance (weighted) on Snomed CT across dif-
             Format-Cor   Jaccard Avg.   Simp. Acc.(axiom) Simp. Acc.(overall) Deri. Acc.(step)   Deri. Acc.(overall)
      100                                                                                                               ferent subsumptions grouped by atomic distance and justifi-
       80                                                                                                               cations size (with examples and inference rules).
       60

       40
                                                                                                                        CT, grouped by their atomic distance (𝑦-axis) and the number of
       20                                                                                                               axioms in the corresponding justifications (𝑥-axis). Results on other
        0                                                                                                               datasets are provided in Appendix B.3.
            Qwen    GPT   Qwen    GPT     Qwen     GPT       Qwen     GPT       Qwen     GPT       Qwen      GPT
                                                 Snomed CT                                                                 Recall from Remark 1 that cases in the upper-left region of Fig-
                                          With Example         No Example                                               ure 7—characterized by low atomic distance but large justification
             Format-Cor   Jaccard Avg.   Simp. Acc.(axiom) Simp. Acc.(overall) Deri. Acc.(step)   Deri. Acc.(overall)
      100
                                                                                                                        size—are relatively complex and often require intricate reasoning.
       80
                                                                                                                        We observe that the two best-performing LLMs, GPT-o4-mini and
       60                                                                                                               Qwen3-32B, exhibit limited effectiveness on these cases, even when
       40                                                                                                               provided with examples and inference rules (additional tests for
       20                                                                                                               such difficult cases are reported in Appendix B.1). By contrast, in the
        0
                                                                                                                        diagonal region—where atomic distance and justification size are
            Qwen    GPT   Qwen    GPT     Qwen     GPT       Qwen     GPT       Qwen     GPT       Qwen      GPT
                                                   GO-Plus                                                              roughly equal—both models perform consistently well, regardless
                                          With Example         No Example                                               of justification size.
             Format-Cor   Jaccard Avg.   Simp. Acc.(axiom) Simp. Acc.(overall) Deri. Acc.(step)   Deri. Acc.(overall)
      100

       80                                                                                                               6.2                     Complex Settings
       60                                                                                                               To further identify the main challenges faced by LLMs in the prov-
       40                                                                                                               ing scenario, we investigate the performance of the best-performing
       20
                                                                                                                        model, GPT-o4-mini, under more challenging and realistic condi-
        0
                                                                                                                        tions. These include varying the ratio of noisy axioms, using natural-
            Qwen    GPT   Qwen    GPT     Qwen     GPT       Qwen     GPT       Qwen     GPT       Qwen      GPT        language instead of formal logic representations in the input, and
                                                   Foodon
                                                                                                                        handling incomplete cases where the provided axioms are insuffi-
                                                                                                                        cient to derive the given conclusion. We focus on the Snomed CT
Figure 6: Comparison (weighted) of Qwen3-32B and GPT-o4-
                                                                                                                        case, as its corresponding samples are more complex and therefore
mini with/without examples.
                                                                                                                        more representative than those of Foodon and GO-Plus.
WWW ’26, April 13–17, 2026, Dubai, United Arab Emirates.                                                           Hui Yang, Jiaoyan Chen, and Uli Sattler


Table 2: Performance (not weighted) under different ratios
of justification and noisy axioms (left), and using natural
language forms with a justification-noise ratio of 1:1 (right).
Results are from Snomed CT using GPT-o4-mini without
inference rules or examples.
                                        Ratio                 Nature Lang.
  Metric                       (justification : noise)         (max token)
                          1:1      1:5     1 : 10    1 : 20   5000    10,000
  Format-Correct          91.98   80.57    78.28     61.71    84.00   85.42    Figure 8: F1-scores for recognizing logical completeness (left)
  Jaccard Avg.            99.49   95.49    87.71     78.96    96.00   94.56    and weighted Jaccard similarity for identifying axioms be-
                                                                               longing to justifications (right). Results are from GPT-o4-
  Simp. axiom-wise        90.60   92.86    91.76     89.74      -       -
                                                                               mini without inference rules or examples.
  Acc. overall            80.91   77.99    72.27     69.29      -       -
  Deri. step-wise         92.33   93.87    90.50     88.60      -       -
  Acc. overall            80.30   73.13    64.30     56.00      -       -      interpretation. We consider two tasks: (1) assessing whether the
                                                                               axioms are logically complete with respect to the conclusion (Logic
                                                                               Completeness); and (2) identifying axioms that appear in at least
6.2.1 Different Ratios of Noisy Axioms. We varied the ratio of jus-            one valid justification of the conclusion.
tification and noisy axioms from 1:1 to 1:5, 1:10, and 1:20 and eval-             Incomplete samples are created by removing subsets of axioms
uated the LLMs without examples or inference rules in the prompt.              from their justifications in Snomed CT examples whose conclusions
As shown in Table 2, performance consistently declines as the pro-             have an atomic distance greater than 9. For task (1), the original
portion of noise increases, indicate that noisy axioms have a strong           samples serve as positive instances, while a 1:1 set of negative
negative impact on the model’s final performance. Specifically, as             instances is generated by removing 𝑘 (1 ≤ 𝑘 ≤ 4) axioms from each.
the ratio increases from 1:1 to 1:20, the weighted Jaccard similarity,         Performance is measured by the F1-score. For task (2), we use the
simplification and derivation overall accuracy fall by around 47%,             negative samples above, regard the remaining justification axioms
42%, and 53%, respectively.                                                    as ground truth, and evaluate LLMs using the Jaccard Similarity
                                                                               metric.
6.2.2 Natural Language Form. We next investigate performance                      The results, summarized in Figure 8, reveal two main trends.
when axioms are expressed in natural language rather than for-                 First, the high F1-scores computed across sets with different num-
mal logical notation. For example, instead of the logical statement:           bers of missing axioms in the negative samples (all around 0.93
“Teacher ≡ Person ⊓ ∃teach .Course ⊓ ∃workat .School′′, we use the             when 𝑘 ranges from 1 to 4) indicate that the models are generally
equivalent natural language description: “Teacher is equivalent to             effective at detecting incomplete premises. Second, the ability to
a person who teaches some courses and works at some school.” In                identify the remaining relevant axioms declines sharply up to 38%
this setting, concepts (e.g., Teacher, Person, Course, School) and             as more axioms are removed, as evidenced by the decrease in mean
roles (e.g., teach, workat) are introduced through natural language            Jaccard similarity. This suggests that higher degrees of incomplete-
rather than predefined formal symbols. It is worth noted that in               ness significantly impair the model’s capacity to identify relevant
this case it is no longer possible to automatically verify the logical         information, even when semantic cues are available in the input.
correctness of simplification and derivation steps as all axioms are
expressed in natural language. Instead, we focusing on the format              7   Conclusion and Future Work
correctness rate and Jaccard similarity.
   We compare the standard setting (i.e., a true-to-noisy axiom ratio          We evaluated the use of LLMs for generating proofs in OWL ontolo-
of 1:1) with a variant where axioms are replaced by their natural              gies, including extraction, simplification, and explanation tasks, as
language forms, as described above. The results are shown on the               well as handling challenging cases involving incomplete premises
right-hand side of Table 2, where we also report results with 10,000           or natural language formulations. We developed a method for auto-
max token limit instead of the 5,000 limit by default, since natural-          matic construction of logic proving datasets with different settings
language expressions are substantially longer than formal logic                from OWL ontologies, and evaluated 7 recent reasoning LLMs. Our
ones. Compared with the 1:1 ratio case in the second column of                 findings indicate that while LLMs achieve promising results overall,
Table 2, we find that performance with natural-language forms is               they still struggle in complex scenarios, with substantial perfor-
close to that with formal logic forms (less than an 8% drop), and              mance degradation facing complex logic patterns, noisy axioms or
increasing the token limit has only a minor effect (less than a 2%             incomplete premises.
difference). This suggests that the main bottleneck lies in reasoning             For future work, we aim to extend our evaluation to more com-
complexity rather than representation length or expression form.               plex fragments or the full OWL 2 DL using broader sampling strate-
                                                                               gies, and to more complex reasoning tasks, such as the computation
6.2.3 Incomplete Premises. We evaluate LLM performance in cases                of deductive modules [14, 52] or reasoning beyond subsumption.
where the given axioms are insufficient to derive the conclusion.              With these evaluation results, we are also interested in developing
To fit such incomplete settings, we use natural language formula-              LLM-based frameworks to retrieve explainable knowledge from
tions instead of symbolic representations, enabling richer semantic            OWL ontologies for augmenting generation.
Large Language Model for OWL Proofs                                                                                      WWW ’26, April 13–17, 2026, Dubai, United Arab Emirates.


References                                                                                          Danielle Belgrave, Angela Fan, Ulrich Paquet, Jakub M. Tomczak, and Cheng
 [1] M Fareed Arif, Carlos Mencía, Alexey Ignatiev, Norbert Manthey, Rafael Peñaloza,               Zhang (Eds.).
     and Joao Marques-Silva. 2016. BEACON: An Efficient SAT-Based Tool for Debug-              [20] Nan Hu, Jiaoyan Chen, Yike Wu, Guilin Qi, Hongru Wang, Sheng Bi, Yongrui
     ging E L + Ontologies. In International Conference on Theory and Applications of               Chen, Tongtong Wu, and Jeff Z Pan. 2025. Can LLMs Evaluate Complex Attri-
     Satisfiability Testing. Springer, 521–530.                                                     bution in QA? Automatic Benchmarking using Knowledge Graphs. In The 63rd
 [2] Michael Ashburner, Catherine A Ball, Judith A Blake, David Botstein, Heather                   Annual Meeting of the Association for Computational Linguistics (ACL 2025).
     Butler, J Michael Cherry, Allan P Davis, Kara Dolinski, Selina S Dwight, Janan T          [21] Mate Héder. 2014. From Semantic Web to Semantic Technologies: What’s New?
     Eppig, et al. 2000. Gene ontology: tool for the unification of biology. Nature                 Knowl.-Based Syst. 69 (2014), 18–23.
     genetics 25, 1 (2000), 25–29.                                                             [22] Alexey Ignatiev, Joao Marques-Silva, Carlos Mencıa, and Rafael Peñaloza. [n. d.].
 [3] Franz Baader, Ian Horrocks, Carsten Lutz, and Ulrike Sattler. 2017. An Introduction            Debugging EL Ontologies through Horn MUS Enumeration. ([n. d.]).
     to Description Logic. Cambridge University Press.                                         [23] Jin Jiang, Jianing Wang, Yuchen Yan, Yang Liu, Jianhua Zhu, Mengdi Zhang,
 [4] Markus C. Bennett. 2013. Financial ontology: A knowledge-driven approach to                    Xunliang Cai, and Liangcai Gao. 2025. Do Large Language Models Excel in
     financial data and information. Springer Science & Business Media.                             Complex Logical Reasoning with Formal Language? CoRR abs/2505.16998 (2025).
 [5] Marco Bombieri, Paolo Fiorini, Simone Paolo Ponzetto, and Marco Rospocher.                     arXiv:2505.16998
     2025. Do LLMs Dream of Ontologies? ACM Transactions on Intelligent Systems                [24] Aditya Kalyanpur, Bijan Parsia, Evren Sirin, and James Hendler. 2005. Debugging
     and Technology (2025).                                                                         unsatisfiable classes in OWL ontologies. Journal of Web Semantics 3, 4 (2005),
 [6] Jieying Chen, Michel Ludwig, Yue Ma, and Dirk Walther. 2017. Zooming in on                     268–293.
     Ontologies: Minimal Modules and Best Excerpts. In 16th International Semantic             [25] Yevgeny Kazakov, Markus Krötzsch, and Frantisek Simancik. 2012. ELK reasoner:
     Web Conference, Proceedings, Part I. Springer, 173–189.                                        architecture and evaluation.. In ORE.
 [7] Jiaoyan Chen, Olga Mashkova, Fernando Zhapa-Camacho, Robert Hoehndorf,                    [26] Boris Konev, Carsten Lutz, Dirk Walther, and Frank Wolter. 2008. Semantic
     Yuan He, and Ian Horrocks. 2025. Ontology embedding: a survey of methods,                      Modularity and Module Extraction in Description Logics.. In European Conference
     applications and resources. IEEE Transactions on Knowledge and Data Engineering                on Artificial Intelligence. 55–59.
     (2025).                                                                                   [27] Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng,
 [8] Peter Clark, Oyvind Tafjord, and Kyle Richardson. 2020. Transformers as Soft                   Cody Hao Yu, Joseph E. Gonzalez, Hao Zhang, and Ion Stoica. 2023. Efficient
     Reasoners over Language. In Proceedings of the Twenty-Ninth International Joint                Memory Management for Large Language Model Serving with PagedAttention.
     Conference on Artificial Intelligence, IJCAI 2020, Christian Bessiere (Ed.). ijcai.org,        In Proceedings of the 29th ACM SIGOPS Symposium on Operating Systems Principles.
     3882–3890.                                                                                     vLLM serving system.
 [9] Ann M. Fitz-Gerald and Gregory J. Wilkin. 2010. Knowledge-based approaches                [28] Zhong-Zhi Li, Duzhen Zhang, Ming-Liang Zhang, Jiaxin Zhang, Zengyan Liu,
     to security: An overview of ontology use in security management. Int. J. Inf.                  Yuxuan Yao, Haotian Xu, Junhao Zheng, Pei-Jie Wang, Xiuyi Chen, et al. 2025.
     Manag. 30, 6 (2010), 512–520.                                                                  From system 1 to system 2: A survey of reasoning large language models. arXiv
[10] Tianyu Gao, Howard Yen, Jiatong Yu, and Danqi Chen. 2023. Enabling Large                       preprint arXiv:2502.17419 (2025).
     Language Models to Generate Text with Citations. In Proceedings of the 2023               [29] Bill Yuchen Lin, Ronan Le Bras, Kyle Richardson, Ashish Sabharwal, Radha
     Conference on Empirical Methods in Natural Language Processing. 6465–6488.                     Poovendran, Peter Clark, and Yejin Choi. 2025. ZebraLogic: On the Scaling Limits
[11] William Gatens, Boris Konev, and Frank Wolter. 2014. Lower and Upper Approx-                   of LLMs for Logical Reasoning. CoRR abs/2502.01100 (2025). arXiv:2502.01100
     imations for Depleting Modules of Description Logic Ontologies.. In European              [30] Anna Sofia Lippolis, Mohammad Javad Saeedizade, Robin Keskisärkkä, Aldo
     Conference on Artificial Intelligence. 345–350.                                                Gangemi, Eva Blomqvist, and Andrea Giovanni Nuzzolese. 2025. Large Lan-
[12] Hamed Babaei Giglou, Jennifer D’Souza, and Sören Auer. 2023. LLMs4OL: Large                    guage Models Assisting Ontology Evaluation. CoRR abs/2507.14552 (2025).
     Language Models for Ontology Learning. In The Semantic Web - ISWC 2023                         arXiv:2507.14552
     - 22nd International Semantic Web Conference, Athens, Greece, November 6-10,              [31] Anna Sofia Lippolis, Mohammad Javad Saeedizade, Robin Keskisärkkä, Sara
     2023, Proceedings, Part I (Lecture Notes in Computer Science, Vol. 14265), Terry R.            Zuppiroli, Miguel Ceriani, Aldo Gangemi, Eva Blomqvist, and Andrea Giovanni
     Payne, Valentina Presutti, Guilin Qi, María Poveda-Villalón, Giorgos Stoilos,                  Nuzzolese. 2025. Ontology generation using large language models. In European
     Laura Hollink, Zoi Kaoudi, Gong Cheng, and Juanzi Li (Eds.). Springer, 408–427.                Semantic Web Conference. Springer, 321–341.
[13] Pankaj Kumar Goyal, Sumit Singh, and Uma Shanker Tiwary. 2024. silp_nlp at                [32] Hanmeng Liu, Zhizhang Fu, Mengru Ding, Ruoxi Ning, Chaoli Zhang, Xiaozhang
     LLMs4OL 2024 Tasks A, B, and C: Ontology Learning through Prompts with LLMs.                   Liu, and Yue Zhang. 2025. Logical reasoning in large language models: A survey.
     In LLMs4OL 2024: The 1st Large Language Models for Ontology Learning Challenge,                arXiv preprint arXiv:2502.09100 (2025).
     co-located with ISWC 2024, Vol. 4. Open Conference Proceedings, 31–38.                    [33] Jian Liu, Leyang Cui, Hanmeng Liu, Dandan Huang, Yile Wang, and Yue Zhang.
[14] B Cuenca Grau, Ian Horrocks, Yevgeny Kazakov, and Ulrike Sattler. 2008. Modular                2020. LogiQA: A Challenge Dataset for Machine Reading Comprehension with
     reuse of ontologies: Theory and practice. Journal of Artificial Intelligence Research          Logical Reasoning. In Proceedings of the Twenty-Ninth International Joint Con-
     31 (2008), 273–318.                                                                            ference on Artificial Intelligence, IJCAI 2020, Christian Bessiere (Ed.). ijcai.org,
[15] Emma J. Griffiths, Damion M. Dooley, Pier Luigi Buttigieg, Robert Hoehndorf,                   3622–3628.
     Fiona S. L. Brinkman, and William W. L. Hsiao. 2016. FoodON: A Global Farm-               [34] Andy Lo, Albert Q. Jiang, Wenda Li, and Mateja Jamnik. 2024. End-to-End Ontol-
     to-Fork Food Ontology. In Proceedings of the Joint International Conference on                 ogy Learning with Large Language Models. In Advances in Neural Information
     Biological Ontology and BioCreative, Corvallis, Oregon, United States, August 1-4,             Processing Systems 37 (NeurIPS 2024).
     2016 (CEUR Workshop Proceedings, Vol. 1747), Pankaj Jaiswal, Robert Hoehndorf,            [35] Michel Ludwig and Dirk Walther. 2014. The Logical Difference for ℰℒℋ r -
     Cecilia N. Arighi, and Austin Meier (Eds.). CEUR-WS.org.                                       Terminologies using Hypergraphs. In ECAI 2014 - 21st European Conference on
[16] Simeng Han, Hailey Schoelkopf, Yilun Zhao, Zhenting Qi, Martin Riddell, Wenfei                 Artificial Intelligence, 18-22 August 2014, Prague, Czech Republic - Including Presti-
     Zhou, James Coady, David Peng, Yujie Qiao, Luke Benson, Lucy Sun, Alexander                    gious Applications of Intelligent Systems (PAIS 2014) (Frontiers in Artificial Intelli-
     Wardle-Solano, Hannah Szabó, Ekaterina Zubova, Matthew Burtell, Jonathan Fan,                  gence and Applications, Vol. 263), Torsten Schaub, Gerhard Friedrich, and Barry
     Yixin Liu, Brian Wong, Malcolm Sailor, Ansong Ni, Linyong Nan, Jungo Kasai,                    O’Sullivan (Eds.). IOS Press, 555–560.
     Tao Yu, Rui Zhang, Alexander R. Fabbri, Wojciech Kryscinski, Semih Yavuz, Ye              [36] Huu Tan Mai, Cuong Xuan Chu, and Heiko Paulheim. 2024. Do LLMs really
     Liu, Xi Victoria Lin, Shafiq Joty, Yingbo Zhou, Caiming Xiong, Rex Ying, Arman                 adapt to domains? an ontology learning perspective. In International Semantic
     Cohan, and Dragomir Radev. 2024. FOLIO: Natural Language Reasoning with                        Web Conference. Springer, 126–143.
     First-Order Logic. In Proceedings of the 2024 Conference on Empirical Methods             [37] Philipp Mondorf and Barbara Plank. 2024. Beyond accuracy: evaluating
     in Natural Language Processing, EMNLP 2024, Miami, FL, USA, November 12-16,                    the reasoning behavior of large Language models–A survey. arXiv preprint
     2024, Yaser Al-Onaizan, Mohit Bansal, and Yun-Nung Chen (Eds.). Association                    arXiv:2404.01869 (2024).
     for Computational Linguistics, 22017–22031.                                               [38] Mihir Parmar, Nisarg Patel, Neeraj Varshney, Mutsumi Nakamura, Man Luo,
[17] Yuan He, Jiaoyan Chen, Hang Dong, Ian Horrocks, Carlo Allocca, Taehun Kim,                     Santosh Mashetty, Arindam Mitra, and Chitta Baral. 2024. LogicBench: Towards
     and Brahmananda Sapkota. 2024. DeepOnto: A Python package for ontology                         Systematic Evaluation of Logical Reasoning Ability of Large Language Models.
     engineering with deep learning. Semantic Web 15, 5 (2024), 1991–2004.                          In Proceedings of the 62nd Annual Meeting of the Association for Computational
[18] Yuan He, Jiaoyan Chen, Ernesto Jiménez-Ruiz, Hang Dong, and Ian Horrocks.                      Linguistics (Volume 1: Long Papers), ACL 2024, Bangkok, Thailand, August 11-16,
     2023. Language Model Analysis for Ontology Subsumption Inference (Onto-                        2024, Lun-Wei Ku, Andre Martins, and Vivek Srikumar (Eds.). Association for
     LAMA). In Findings of the Association for Computational Linguistics: ACL 2023.                 Computational Linguistics, 13679–13707.
     3439–3453.                                                                                [39] Angelos Poulis, Eleni Tsalapati, and Manolis Koubarakis. 2023. Reasoning
[19] Yuan He, Moy Yuan, Jiaoyan Chen, and Ian Horrocks. 2024. Language Models                       over Description Logic-based Contexts with Transformers. arXiv preprint
     as Hierarchy Encoders. In Advances in Neural Information Processing Systems 38:                arXiv:2311.08941 (2023).
     Annual Conference on Neural Information Processing Systems 2024, NeurIPS 2024,            [40] Youssra Rebboud, Pasquale Lisena, Lionel Tailhardat, and Raphael Troncy. 2024.
     Vancouver, BC, Canada, December 10 - 15, 2024, Amir Globersons, Lester Mackey,                 Benchmarking llm-based ontology conceptualization: A proposal. In ISWC 2024,
WWW ’26, April 13–17, 2026, Dubai, United Arab Emirates.                                                                         Hui Yang, Jiaoyan Chen, and Uli Sattler


     23rd International Semantic Web Conference.                                            A     Implementation Details
[41] Abulhair Saparov and He He. 2023. Language Models Are Greedy Reasoners: A
     Systematic Formal Analysis of Chain-of-Thought. In The Eleventh International          For the open-source LLMs, we conducted experiments locally on
     Conference on Learning Representations, ICLR 2023, Kigali, Rwanda, May 1-5, 2023.      a machine equipped with a single A100 80 GB GPU, leveraging
     OpenReview.net.
[42] Ulrike Sattler, Thomas Schneider, and Michael Zakharyaschev. 2009. Which kind
                                                                                            the vllm [27] package to accelerate inference. For GPT-o4-mini, we
     of module should I extract? Description Logics 477 (2009), 78.                         accessed the model through the ChatGPT API, with an average
[43] Koustuv Sinha, Shagun Sodhani, Jin Dong, Joelle Pineau, and William L. Hamil-          batch-mode cost of under $0.01 per request. Our implementation
     ton. 2019. CLUTRR: A Diagnostic Benchmark for Inductive Reasoning from Text.
     In Proceedings of the 2019 Conference on Empirical Methods in Natural Language         is based on the DeepOnto package [17]. We use the ELK reasoner
     Processing and the 9th International Joint Conference on Natural Language Process-     [25] to compute justifications and to verify whether each derivation
     ing, EMNLP-IJCNLP 2019, Hong Kong, China, November 3-7, 2019, Kentaro Inui,            step is correct.
     Jing Jiang, Vincent Ng, and Xiaojun Wan (Eds.). Association for Computational
     Linguistics, 4505–4514.
[44] SNOMED International. 2025. SNOMED CT: the comprehensive clinical health-              A.1     Standard Case
     care terminology. Accessed July 2025.
[45] Oyvind Tafjord, Bhavana Dalvi, and Peter Clark. 2021. ProofWriter: Generating          The prompt used for evaluating the performance of LLMs on three
     Implications, Proofs, and Abductive Statements over Natural Language. In Find-         tasks involving explanation and proof generation based on OWL
     ings of the Association for Computational Linguistics: ACL/IJCNLP 2021, Online
     Event, August 1-6, 2021 (Findings of ACL, Vol. ACL/IJCNLP 2021), Chengqing Zong,       ontologies is shown in Figure 9. The input consists of all axioms
     Fei Xia, Wenjie Li, and Roberto Navigli (Eds.). Association for Computational          (each indexed) along with the desired conclusion. The output is
     Linguistics, 3621–3634.                                                                divided into three sections: AXIOMS_USED, SIMPLIFY, and DERIVE:
[46] Jidong Tian, Yitian Li, Wenqing Chen, Liqiang Xiao, Hao He, and Yaohui Jin.
     2021. Diagnosing the First-Order Logical Reasoning Ability Through LogicNLI.           (1) AXIOMS_USED specifies the indices of the axioms required to
     In Proceedings of the 2021 Conference on Empirical Methods in Natural Language
     Processing, EMNLP 2021, Virtual Event / Punta Cana, Dominican Republic, 7-11
                                                                                                derive the given conclusion. In the given example, all axioms
     November, 2021, Marie-Francine Moens, Xuanjing Huang, Lucia Specia, and                    except for the last one are needed.
     Scott Wen-tau Yih (Eds.). Association for Computational Linguistics, 3738–3747.        (2) SIMPLIFY presents the simplified forms of the selected axioms
[47] Nilay Tufek, Aparna Saissre Thuluva, Valentin Philipp Just, Fajar J Ekaputra,
     Tathagata Bandyopadhyay, Marta Sabou, and Allan Hanbury. 2024. Validat-                    that are sufficient for deriving the conclusion. For instance, in
     ing semantic artifacts with large language models. In European Semantic Web                the given example, instead of using the full first axiom 𝐴 ≡ ∃𝑟 .𝐵,
     Conference. Springer, 92–101.                                                              it is sufficient to use the weaker version ∃𝑟 .𝐵 ⊑ 𝐴 to derive the
[48] Weiqi Wu, Chengyue Jiang, Yong Jiang, Pengjun Xie, and Kewei Tu. 2023. Do
     PLMs Know and Understand Ontological Knowledge?. In The 61st Annual Meeting                given conclusion, which is a direct consequence of the original
     Of The Association For Computational Linguistics.                                          form.
[49] Shitao Xiao, Zheng Liu, Peitian Zhang, and Niklas Muennighoff. 2023. C-
     Pack: Packaged Resources To Advance General Chinese Embedding. CoRR
                                                                                            (3) DERIVE provides a step-by-step explanation of the reasoning
     abs/2309.07597 (2023). arXiv:2309.07597                                                    process. The derivation is split into distinct stages, with each
[50] Fangzhi Xu, Qika Lin, Jiawei Han, Tianzhe Zhao, Jun Liu, and Erik Cambria.                 stage ending in an crucial intermediate result for inferring the
     2025. Are large language models really good logical reasoners? a comprehensive
     evaluation and beyond. IEEE Transactions on Knowledge and Data Engineering                 final conclusion. For example, in the given case, 𝐷 ⊑ 𝐴 is
     (2025).                                                                                    chosen as the key intermediate result, and the derivation is
[51] Hui Yang, Jiaoyan Chen, Yuan He, Yongsheng Gao, and Ian Horrocks.                          correspondingly divided into two steps.
     2025. Language Models as Ontology Encoders. CoRR abs/2507.14334 (2025).
     arXiv:2507.14334                                                                          Note that we output all three tasks simultaneously rather than
[52] Hui Yang, Patrick Koopmann, Yue Ma, and Nicole Bidoit. 2023. Efficient Compu-          handling them one by one, since their underlying requirement is
     tation of General Modules for ALC Ontologies. In Proceedings of the Thirty-Second
     International Joint Conference on Artificial Intelligence, IJCAI 2023, 19th-25th Au-   the same: each demands a detailed analysis of the reasoning pro-
     gust 2023, Macao, SAR, China. ijcai.org, 3356–3364.                                    cess needed to derive the given conclusion. However, the difficulty
[53] Hui Yang, Yue Ma, and Nicole Bidoit. 2022. Hypergraph-Based Inference Rules
     for Computing EL+ -Ontology Justifications. In Automated Reasoning - 11th Inter-
                                                                                            increases progressively across the tasks. First, we ask only for the
     national Joint Conference, IJCAR 2022, Haifa, Israel, August 8-10, 2022, Proceedings   indices of the axioms required. Next, we require the LLM to iden-
     (Lecture Notes in Computer Science, Vol. 13385), Jasmin Blanchette, Laura Kovács,      tify the relevant portions of those axioms that are actually useful.
     and Dirk Pattinson (Eds.). Springer, 310–328.
[54] Hui Yang, Yue Ma, and Nicole Bidoit. 2023. Efficient extraction of E L -Ontology       Finally, we ask for a complete derivation process, structured as an
     deductive modules. In The 37th AAAI Conference on Artificial Intelligence, AAAI.       explanation segmented by crucial intermediate results.
     Accepted.
[55] Weihao Yu, Zihang Jiang, Yanfei Dong, and Jiashi Feng. 2020. ReClor: A Reading
     Comprehension Dataset Requiring Logical Reasoning. In 8th International Con-           A.2     Incomplete case
     ference on Learning Representations, ICLR 2020, Addis Ababa, Ethiopia, April 26-30,
     2020. OpenReview.net.
                                                                                            In the incomplete case, where the input axioms may not sufficient
[56] Xiao Zhang, Huiyuan Lai, Qianru Meng, and Johan Bos. 2025. OntoURL: A Bench-           to infer the given conclusion, we focus on the natural language
     mark for Evaluating Large Language Models on Symbolic Ontological Under-               forms and therefore omit the SIMPLIFY and DERIVE parts from the
     standing, Reasoning and Learning. CoRR abs/2505.11031 (2025). arXiv:2505.11031
                                                                                            standard case, as well as the inference rules and examples. The
                                                                                            adjusted prompt is presented in Figure 10, with the differences in
                                                                                            the required output and instructions highlighted in red.

                                                                                            B Other results
                                                                                            B.1 Hard case with GPT-o4-mini
                                                                                            The number of hard cases—i.e., subsumptions with large atomic
                                                                                            distance but small justification size—in the original dataset is rela-
                                                                                            tively small. To enable more reliable analysis, we further analyzed
                                                                                            the hard cases, comprising 261 additional subsumptions in Snomed
Large Language Model for OWL Proofs                                                           WWW ’26, April 13–17, 2026, Dubai, United Arab Emirates.



    Logic Inference Prompt                                                    Logic Inference Prompt

    # Explanation of Logic Inference                                          # Logical Inference Task
    You are an expert in logical reasoning. Your task is to                   You are an expert in logical reasoning. Your task is to
    produce a clear and easily understandable explanation that                assess whether the target conclusion logically follows from
    demonstrates how the conclusion logically follows from the                the provided axioms, and to identify any potentially missing
    given axioms.                                                             axioms if it does not.
    (Inference rules here if applied)                                         ## Required Output Format
                                                                              Your response MUST strictly follow this format:
    ## Output Format Requirements
    Your response MUST follow this exact format:                              MISSING: [YES/NO]
                                                                              AXIOMS_USEFUL: [list of relevant axiom identifiers]
    AXIOMS_USED: {list of axiom identifiers}                                  SUSPECTED_MISSING_PARTS: NONE / [potential missing knowledge
    SIMPLIFY:                                                                 in natural language]
    [axiom_id]: [original_axiom] → [simplified_form]
                                                                              ## Input Data
    ...
                                                                              Consider the following axioms:
                                                                               (0) Axiom 0
    DERIVE:                                                                    (1) Axiom 1
    STEP[n]: [premise_list] ⊢ [conclusion]                                    ...
    EXPLANATION: [a simple explanation of the derivation]
    ...                                                                     **Target Conclusion**: {conclusion}

    (An example here if applied)                                            ## Instructions
                                                                            1. Decide whether the axioms are sufficient to derive the
    ## Task                                                                 target conclusion.
    Given the following axioms:                                             2. In AXIOMS_USEFUL, include only the axioms that contribute
        (0) Axiom 0                                                         to the derivation of the target conclusion.
        (1) Axiom 1                                                         3. If MISSING = YES, provide the suspected missing axioms in
        ...                                                                 SUSPECTED_MISSING_PARTS.
                                                                            4. End your response with exactly the three required fields
    **Target Conclusion**: {conclusion}                                     (MISSING, AXIOMS_USEFUL, SUSPECTED_MISSING_PARTS) and nothing
    **Instructions:**                                                       else.
    (1) Identify and list only the axioms that are essential for
        deriving the conclusion. Note that only half of the given
        axioms are necessary for the derivation.
    (2) Simplify each selected axiom by extracting only the             Figure 10: Prompt for the incomplete case, with inputs shown
        logically relevant components.                                  in blue and differences from the standard case highlighted
    (3) Present your response using the required DSL format,
        with clearly defined AXIOMS_USED, SIMPLIFY, and DERIVE
                                                                        in orange.
        sections.
    (4) In the DERIVE section, break the reasoning into meaningful
        steps. Each STEP should capture a key intermediate              Table 3: Unweighted performance of GPT-o4-mini (without
        result that contributes to the overall derivation, while        inference rules or examples) on the SNOMED CT dataset.
        maintaining logical clarity and completeness.                   “Original” refers to the SNOMED CT data used in Table 1,
                                                                        differences computed by weighted values are indicated by ∗ .

Figure 9: Prompt for logical explanation and proof (input
                                                                          Metric                            Original       Hard      Difference
shown in blue; placeholders for inference rules or examples
shown in red).                                                            Format-Correct                       91.98       51.72       −43.77%
                                                                          Jaccard Avg.                         99.49       94.39      −42.70%∗
                                                                          Simp. Acc. (axiom-wise)              90.60       87.62      −38.01%∗
                                                                          Simp. Acc. (overall)                 80.91       40.14      −53.66%∗
CT, where the justification size exceeds their atomic distance by
at least 3. Specifically, we considered 300 subsumptions for each         Deri. Acc. (step-wise)               92.33       79.69      −43.70%∗
subsumption group with fixed atomic distance k, where k ranging           Deri. Acc. (overall)                 80.30       32.39      −57.11%∗
from 4 to 20, and then selected only those whose justification size
exceeds atomic distance at least 3. To further control the distribu-
tion, we limited the sampling to at most 10 subsumptions for each       B.2      Statistics of Subsumptions
(atomic distance, #|Justification|) group. The detailed statistics of   Here, in Figure 12, we present detailed statistics of the subsump-
these hard cases are presented in Figure 13.                            tions derived from the Snomed CT, GO-Plus, and Foodon ontologies.
   We then evaluated GPT-o4-mini under the base setting (i.e., with-    The distribution of atomic distance ranges from 0 to 38, with up to
out inference rules or in-context examples) on this dataset. The        millions of distinct subsumptions sharing the same atomic distance
overall results are summarized in Table 3. We observed a substan-       value. Moreover, for atomic distance values below 15, there are
tial drop in both the format correctness rate and overall accuracy      consistently at least several thousand corresponding subsumptions.
by nearly half, which prove the limitation of LLMs on those hard        This provides a rich resource for further evaluations, as well as po-
cases. The detailed performance across different (atomic distance,      tential investigations or implementations beyond the few hundred
#|Justification|) groups is shown in Figure 11d.                        samples examined in our study.
WWW ’26, April 13–17, 2026, Dubai, United Arab Emirates.                                                                                                                                                                                                                                    Hui Yang, Jiaoyan Chen, and Uli Sattler



                                   19
                                                     Jaccard Avg.              100                                                           Jaccard Avg.                 100                                                    Jaccard Avg.                100                                Jaccard Avg.           100
                                                                                                                                                                                                                                                                                      22




                                                                                                    3 4 5 6 7 8 9 10 11 12 14 16




                                                                                                                                                                                           3 4 6 7 8 9 10 11 12 14 16
                                   18                                                                                                                                                                                                                                                 20
                                   17                                                                                                                                                                                                                                                 19
                                   16                                          80                                                                                         80                                                                                 80                       18                               80
                                   15
                #|Justification|




                                                                                         #|Justification|




                                                                                                                                                                                #|Justification|




                                                                                                                                                                                                                                                                   #|Justification|
                                   14                                                                                                                                                                                                                                                 17
                                   13                                          60                                                                                         60                                                                                 60                       16                               60
                                   12                                                                                                                                                                                                                                                 15
                                   11                                                                                                                                                                                                                                                 14
                                   10                                                                                                                                                                                                                                                 13
                                    9                                          40                                                                                         40                                                                                 40                       12                               40
                                    8                                                                                                                                                                                                                                                 11
                                    7                                                                                                                                                                                                                                                 10
                                    6                                          20                                                                                         20                                                                                 20                        9                               20
                                    5
                                    4                                                                                                                                                                                                                                                  8
                                    3                                          0                                                                                          0                                                                                  0                         7                               0
                                            4    6     8   10   12   14   16                                                       4     6     8    10    12    14   16                                                 4    6     8   10   12     14   16                                 4 5 6 7 8 9 10 11 12 13


                                   19
                                                Simp. Acc.(overall)            100                                                      Simp. Acc.(overall)               100                                               Simp. Acc.(overall)              100                      22
                                                                                                                                                                                                                                                                                             Simp. Acc.(overall)       100


                                                                                                    3 4 5 6 7 8 9 10 11 12 14 16




                                                                                                                                                                                           3 4 6 7 8 9 10 11 12 14 16
                                   18                                                                                                                                                                                                                                                 20
                                   17                                                                                                                                                                                                                                                 19
                                   16                                          80                                                                                         80                                                                                 80                       18                               80
                                   15
                #|Justification|




                                                                                         #|Justification|




                                                                                                                                                                                #|Justification|




                                                                                                                                                                                                                                                                   #|Justification|
                                   14                                                                                                                                                                                                                                                 17
                                   13                                          60                                                                                         60                                                                                 60                       16                               60
                                   12                                                                                                                                                                                                                                                 15
                                   11                                                                                                                                                                                                                                                 14
                                   10                                                                                                                                                                                                                                                 13
                                    9                                          40                                                                                         40                                                                                 40                       12                               40
                                    8                                                                                                                                                                                                                                                 11
                                    7                                                                                                                                                                                                                                                 10
                                    6                                          20                                                                                         20                                                                                 20                        9                               20
                                    5
                                    4                                                                                                                                                                                                                                                  8
                                    3                                          0                                                                                          0                                                                                  0                         7                               0
                                            4    6     8   10   12   14   16                                                       4     6     8    10    12    14   16                                                 4    6     8   10   12     14   16                                 4 5 6 7 8 9 10 11 12 13


                                   19
                                                Deri. Acc.(overall)            100                                                      Deri. Acc.(overall)               100                                               Deri. Acc.(overall)              100                      22
                                                                                                                                                                                                                                                                                              Deri. Acc.(overall)      100
                                                                                                    3 4 5 6 7 8 9 10 11 12 14 16




                                                                                                                                                                                           3 4 6 7 8 9 10 11 12 14 16
                                   18                                                                                                                                                                                                                                                 20
                                   17                                                                                                                                                                                                                                                 19
                                   16                                          80                                                                                         80                                                                                 80                       18                               80
                                   15
                #|Justification|




                                                                                         #|Justification|




                                                                                                                                                                                #|Justification|




                                                                                                                                                                                                                                                                   #|Justification|
                                   14                                                                                                                                                                                                                                                 17
                                   13                                          60                                                                                         60                                                                                 60                       16                               60
                                   12                                                                                                                                                                                                                                                 15
                                   11                                                                                                                                                                                                                                                 14
                                   10                                                                                                                                                                                                                                                 13
                                    9                                          40                                                                                         40                                                                                 40                       12                               40
                                    8                                                                                                                                                                                                                                                 11
                                    7                                                                                                                                                                                                                                                 10
                                    6                                          20                                                                                         20                                                                                 20                        9                               20
                                    5
                                    4                                                                                                                                                                                                                                                  8
                                    3                                          0                                                                                          0                                                                                  0                         7                               0
                                            4    6     8   10   12   14   16                                                       4     6     8    10    12    14   16                                                 4    6     8   10   12     14   16                                 4 5 6 7 8 9 10 11 12 13
                                                     Atomic Distance                                                                         Atomic Distance                                                                     Atomic Distance                                                Atomic Distance

                                            (a) Snomed CT (avg.)                                                                        (b) Foodon (avg.)                                                                   (c) GO-Plus (avg.)                                             (d) Hard (GPT-o4-mini)

Figure 11: Average performance (weighted) of all methods on Foodon and GO-Plus, and the performance of GPT-o4-mini
(without example or inference rules) on the Hard dataset, measured across subsumption distance and justification size.


                     106                                                                                                                                 Foodon
                                                                                                                                                         Go-Plus
                                                                                                                                                         Snomed CT
                     105

                     104
   #|Subsumptions|




                     103

                     102

                     101

                     100
                                        0             5         10        15        20                                             25          30          35
                                                                          Atomic Distance                                                                                                                          Figure 13: Statistics of the hard cases extracted from Snomed
                                                                                                                                                                                                                   CT.
Figure 12: Number of all subsumptions with different atomic
distance.


B.3                        Average Results Across LLMs
Figure 11 presents the overall results for the SNOMED CT, FoodOn,                                                                                                                                                these ontologies are simple subsumption axioms of the form 𝐴 ⊑ 𝐵,
and GO-Plus ontologies. The FoodOn and GO-Plus datasets appear                                                                                                                                                   with 𝐴 and 𝐵 being atomic concepts. Consequently, the average per-
to be relatively easier in terms of logical explanation complexity, as                                                                                                                                           formance of all LLMs across different settings is higher for FoodOn
most instances lie near the diagonal where atomic distance equals                                                                                                                                                and GO-Plus than for SNOMED CT, further supporting our claim
the justification size. This is primarily because most EL axioms in                                                                                                                                              that the SNOMED CT data are comparatively more challenging.
Large Language Model for OWL Proofs                                            WWW ’26, April 13–17, 2026, Dubai, United Arab Emirates.


                                                          B.4     Effect of Example and Input in Prompt
    Example
                                                          We examine two aspects to analyze its sensitivity of prompt to the
    ## Example                                            example and input axioms as follows. We focus on Qwen3-32B as
    Given the following axioms:                           the primary case study.
    [1] A ≡ ∃r.B
                                                              Example modes. We compare three modes:
    [2] C ⊑ B ⊓ H ⊓ I
    [3] D ≡∃r.C ⊓ G                                             • adding the standard example (Simp.),
    [4] E ≡ A ⊓ F                                               • a version with detailed derivation (Detail; see Figure 14),
    [5] D ⊑ F ⊓ J                                               • no example (None),
                                                          The main results for Qwen3-32B on SNOMED CT are presented
    The desired explanation for deriving            the   in Figure 15a. Omitting examples increases format correctness but
    conclusion D ⊑ E is as follows:                       leads to substantial drops in result accuracy. In contrast, when
                                                          no inference rules are provided, detailed examples consistently
    AXIOMS_USED: 1,2,3,4,5                                improve all performance metrics. However, when inference rules
    SIMPLIFY:                                             are included, providing detailed examples can slightly reduce result
    [1] A ≡ ∃r.B → ∃r.B ⊑ A                               accuracy, likely due to the longer context, and the fact that the
    [2] C ⊑ B ⊓ H ⊓ I → C ⊑ B                             additional information in the detailed examples is already captured
    [3] D ≡ ∃r.C ⊓ G → D ⊑ ∃r.C                           by the inference rules.
    [4] E ≡ A ⊓ F → A ⊓ F ⊑ E
    [5] D ⊑ F ⊓ J → D ⊑ F                                     Input modes. We evaluate three modes:
                                                                • the default noise setting with a balanced mix of true and
    DERIVE:
                                                                  noisy axioms,
                                                                • the just-only setting where only true axioms are included,
    STEP1: [1] ⊢ ∃r.B ⊑ A
                                                                • the naming setting where natural-language names or de-
    EXPLANATION: From equivalence A ≡ ∃r.B, we get
                                                                  scriptions are added alongside axioms (e.g., 𝐴 : name/descrip-
    ∃r.B ⊑ A
                                                                  tion of 𝐴).
    STEP2: [2] ⊢ C ⊑ B                                    Results on SNOMED CT (Figure 16a) show that the just-only mode
    EXPLANATION: From conjunction C ⊑ B ⊓ H ⊓ I, we       consistently improves performance across all tasks, which is as
    get C ⊑ B                                             expected since all noise axioms have been removed. In contrast,
    STEP3: [3] ⊢ D ⊑ ∃r.C                                 the naming mode provides no improvements in the absence of in-
    EXPLANATION: From equivalence D ≡ ∃r.C ⊓ G, we        ference rules and usually decreases performance when rules are
    get D ⊑ ∃r.C                                          included, indicating that although linguistic annotations could en-
                                                          hance performance, they are less effective than explicit logical rules
    STEP4: [STEP2, STEP3] ⊢ D ⊑ ∃r.B
                                                          in this case. Note that in just-only mode, the Jaccard average does
    EXPLANATION: From D ⊑ ∃r.C and C ⊑ B, we get
                                                          not make sense, since all axioms are justifications; therefore, we
    D ⊑ ∃r.B
                                                          omit it from the figures.
    STEP5: [STEP1, STEP4] ⊢ D ⊑ A                            The illustration of other models like DeepSeek-R1-Qwen-8B and
    EXPLANATION: From ∃r.B ⊑ A and D ⊑ ∃r.B, we get       Mistral-Small can be found in Figures 17 and 18, respectively.
    D⊑A
    STEP6: [5] ⊢ D ⊑ F                                    C     Case Studies
    EXPLANATION: From conjunction D ⊑ F ⊓ J, we get       In this section, we present several case studies covering both simple
    D⊑F                                                   and complex scenarios. All samples are obtained using Qwen3-32B
    STEP7: [STEP5, STEP6] ⊢ D ⊑ A ⊓ F                     with examples and inference rules provided in the prompt, and
    EXPLANATION: From D ⊑ A and D ⊑ F, we get D ⊑ A⊓F     extracted from Snomed CT.
                                                             In the relatively simple case shown in Figure 19, most input ax-
    STEP8: [4] ⊢ A ⊓ F ⊑ E                                ioms are atomic subsumptions, except for axiom 6. In this example,
    EXPLANATION: From equivalence E ≡ A ⊓ F, we get       both the atomic distance to the given target and the justification size
    A⊓F ⊑ E                                               are 6. The LLM accurately selects the relevant justification axioms,
    STEP9: [STEP7, STEP8] ⊢ D ⊑ E                         as shown in the AXIOMS_USED section, and correctly simplifies ax-
    EXPLANATION: From D ⊑ A ⊓ F and A ⊓ F ⊑ E, we get     iom 6 by preserving only the essential part, 𝐴11 ⊑ 𝐴9 . Furthermore,
    D⊑E                                                   the explanation provided in the DERIVE section is fully correct.
                                                             Figure 20 illustrates a more complex case, where the input axioms
                                                          include compound expressions such as 𝐴20 ≡ 𝐴6 ⊓∃𝑟 3 .𝐴10 . Deriving
     Figure 14: Example with detailed derivation steps.   the target conclusion requires inference patterns beyond simple
                                                          transitive subsumptions. In this scenario, the LLM correctly identi-
                                                          fies the justification axioms, but the simplification process is less
WWW ’26, April 13–17, 2026, Dubai, United Arab Emirates.                                                                                                                                                                                                              Hui Yang, Jiaoyan Chen, and Uli Sattler

                            With IR         Without IR            Original     Weighted                                                       With IR         Without IR            Original     Weighted                                                       With IR         Without IR            Original     Weighted

100
              Format-Cor              100
                                                Simp. Acc.(step)              100
                                                                                       Deri. Acc.(step)           100
                                                                                                                                Format-Cor              100
                                                                                                                                                                  Simp. Acc.(step)              100
                                                                                                                                                                                                         Deri. Acc.(step)           100
                                                                                                                                                                                                                                                  Format-Cor              100
                                                                                                                                                                                                                                                                                    Simp. Acc.(step)              100
                                                                                                                                                                                                                                                                                                                           Deri. Acc.(step)

 80                                    80                                      80                                 80                                     80                                      80                                 80                                     80                                      80

 60                                    60                                      60                                 60                                     60                                      60                                 60                                     60                                      60

 40                                    40                                      40                                 40                                     40                                      40                                 40                                     40                                      40

 20                                    20                                      20                                 20                                     20                                      20                                 20                                     20                                      20

 0                                     0                                        0                                  0                                     0                                        0                                  0                                     0                                        0
      Simp.     Detail     None              Simp.       Detail     None            Simp.    Detail    None             Simp.     Detail     None              Simp.       Detail     None            Simp.    Detail    None             Simp.     Detail     None              Simp.       Detail     None            Simp.    Detail    None

100
           Jaccard Avg.               100
                                              Simp. Acc.(overall)             100
                                                                                      Deri. Acc.(overall)         100
                                                                                                                             Jaccard Avg.               100
                                                                                                                                                                Simp. Acc.(overall)             100
                                                                                                                                                                                                        Deri. Acc.(overall)         100
                                                                                                                                                                                                                                               Jaccard Avg.               100
                                                                                                                                                                                                                                                                                  Simp. Acc.(overall)             100
                                                                                                                                                                                                                                                                                                                          Deri. Acc.(overall)

 80                                    80                                      80                                 80                                     80                                      80                                 80                                     80                                      80

 60                                    60                                      60                                 60                                     60                                      60                                 60                                     60                                      60

 40                                    40                                      40                                 40                                     40                                      40                                 40                                     40                                      40

 20                                    20                                      20                                 20                                     20                                      20                                 20                                     20                                      20

 0                                     0                                        0                                  0                                     0                                        0                                  0                                     0                                        0
      Simp.     Detail     None              Simp.       Detail     None            Simp.    Detail    None             Simp.     Detail     None              Simp.       Detail     None            Simp.    Detail    None             Simp.     Detail     None              Simp.       Detail     None            Simp.    Detail    None


                                      (a) SNOMED CT                                                                                                       (b) FoodOn                                                                                                        (c) GO-Plus

Figure 15: Performance of Qwen3-32B on different datasets with different example in the prompt. Weighted values are in color.

                           With IR          Without IR            Original      Weighted                                                     With IR          Without IR            Original      Weighted                                                     With IR          Without IR            Original      Weighted


100
              Format-Cor              100
                                                Simp. Acc.(step)              100
                                                                                       Deri. Acc.(step)           100
                                                                                                                                Format-Cor              100
                                                                                                                                                                  Simp. Acc.(step)              100
                                                                                                                                                                                                         Deri. Acc.(step)           100
                                                                                                                                                                                                                                                  Format-Cor              100
                                                                                                                                                                                                                                                                                    Simp. Acc.(step)              100
                                                                                                                                                                                                                                                                                                                           Deri. Acc.(step)

 80                                    80                                     80                                   80                                   80                                      80                                   80                                   80                                      80

 60                                    60                                     60                                   60                                   60                                      60                                   60                                   60                                      60

 40                                    40                                     40                                   40                                   40                                      40                                   40                                   40                                      40

 20                                    20                                     20                                   20                                   20                                      20                                   20                                   20                                      20

  0                                    0                                       0                                    0                                    0                                       0                                    0                                    0                                       0
      Naming     Noise   Just-only          Naming       Noise    Just-only         Naming   Noise    Just-only         Naming     Noise   Just-only          Naming       Noise    Just-only         Naming   Noise    Just-only         Naming     Noise   Just-only          Naming       Noise    Just-only         Naming   Noise    Just-only

100
           Jaccard Avg.               100
                                              Simp. Acc.(overall)             100
                                                                                      Deri. Acc.(overall)         100
                                                                                                                             Jaccard Avg.               100
                                                                                                                                                                Simp. Acc.(overall)             100
                                                                                                                                                                                                        Deri. Acc.(overall)         100
                                                                                                                                                                                                                                               Jaccard Avg.               100
                                                                                                                                                                                                                                                                                  Simp. Acc.(overall)             100
                                                                                                                                                                                                                                                                                                                          Deri. Acc.(overall)

 80                                    80                                     80                                   80                                   80                                      80                                   80                                   80                                      80

 60                                    60                                     60                                   60                                   60                                      60                                   60                                   60                                      60

 40                                    40                                     40                                   40                                   40                                      40                                   40                                   40                                      40

 20                                    20                                     20                                   20                                   20                                      20                                   20                                   20                                      20

  0                                    0                                       0                                    0                                    0                                       0                                    0                                    0                                       0
      Naming     Noise   Just-only          Naming       Noise    Just-only         Naming   Noise    Just-only         Naming     Noise   Just-only          Naming       Noise    Just-only         Naming   Noise    Just-only         Naming     Noise   Just-only          Naming       Noise    Just-only         Naming   Noise    Just-only


                                      (a) SNOMED CT                                                                                                       (b) FoodOn                                                                                                        (c) GO-Plus

Figure 16: Performance of Qwen3-32B on different datasets under different input data modes (with standard example in the
prompt).


satisfactory: axioms 13 and 15 are split into simpler forms, yet not                                                                                                                Step3 [Step 2, Axiom 15] ⊢ 𝐴23 ⊑ ∃𝑟 3 .𝐴10
all non-essential parts are removed. For instance, only the compo-                                                                                                                  Step4 [Step 1, Step 3, Axiom 13] ⊢ 𝐴23 ⊑ 𝐴20
nent A6 𝐴6 ⊓ ∃𝑟 3 .𝐴10 ⊑ 𝐴20 from axiom 13 is required. Additionally,                                                                                                                  Although the DERIVE output is almost correct, it has the small
the derivation process contains errors. In the first derivation step,                                                                                                               mistake: the omission of axiom 15 in the premise set for Step 1,
one cannot derive 𝐴23 ⊑ 𝐴6 from axioms 3, 9, and 1. The correct                                                                                                                     despite being mentioned in the explanation.
derivation steps are:                                                                                                                                                                  Finally, Figure 21 presents an even more complex example. In
Step1 [Axioms 15, 3, 9, 1] ⊢ 𝐴23 ⊑ 𝐴6                                                                                                                                               this case, the axioms are highly nested and intricate, and the LLM
Step2 [Axioms 12, 10, 4] ⊢ 𝐴19 ⊑ 𝐴10                                                                                                                                                is unable to produce the result within the token limits.
Large Language Model for OWL Proofs                                                                                                       WWW ’26, April 13–17, 2026, Dubai, United Arab Emirates.


                            With IR         Without IR            Original    Weighted                                               With IR         Without IR           Original      Weighted


100
              Format-Cor              100
                                               Simp. Acc.(step)              100
                                                                                      Deri. Acc.(step)     100
                                                                                                                      Format-Cor               100
                                                                                                                                                         Simp. Acc.(step)             100
                                                                                                                                                                                               Deri. Acc.(step)

 80                                   80                                     80                            80                                  80                                     80

 60                                   60                                     60                            60                                  60                                     60

 40                                   40                                     40                            40                                  40                                     40

 20                                   20                                     20                            20                                  20                                     20

  0                                    0                                      0                             0                                   0                                      0
      Simp.     Detail     None              Simp.       Detail     None           Simp.   Detail   None         Naming   Noise   Just-only          Naming       Noise   Just-only         Naming   Noise   Just-only

100
          Jaccard Avg.                100
                                              Simp. Acc.(overall)            100
                                                                                    Deri. Acc.(overall)    100
                                                                                                                      Jaccard Avg.             100
                                                                                                                                                       Simp. Acc.(overall)            100
                                                                                                                                                                                              Deri. Acc.(overall)

 80                                   80                                     80                            80                                  80                                     80

 60                                   60                                     60                            60                                  60                                     60

 40                                   40                                     40                            40                                  40                                     40

 20                                   20                                     20                            20                                  20                                     20

  0                                    0                                      0                             0                                   0                                      0
      Simp.     Detail     None              Simp.       Detail     None           Simp.   Detail   None         Naming   Noise   Just-only          Naming       Noise   Just-only         Naming   Noise   Just-only

                                       (a) Example mode                                                                                              (b) Data mode

                         Figure 17: Performance of Mistral-Small on SNOMED CT under different data and example modes.

                            With IR         Without IR            Original    Weighted                                               With IR         Without IR           Original      Weighted


100
              Format-Cor              100
                                               Simp. Acc.(step)              100
                                                                                      Deri. Acc.(step)     100
                                                                                                                      Format-Cor               100
                                                                                                                                                         Simp. Acc.(step)             100
                                                                                                                                                                                               Deri. Acc.(step)

 80                                   80                                     80                            80                                  80                                     80

 60                                   60                                     60                            60                                  60                                     60

 40                                   40                                     40                            40                                  40                                     40

 20                                   20                                     20                            20                                  20                                     20

  0                                    0                                      0                             0                                   0                                      0
      Simp.     Detail     None              Simp.       Detail     None           Simp.   Detail   None         Naming   Noise   Just-only          Naming       Noise   Just-only         Naming   Noise   Just-only

100
          Jaccard Avg.                100
                                              Simp. Acc.(overall)            100
                                                                                    Deri. Acc.(overall)    100
                                                                                                                      Jaccard Avg.             100
                                                                                                                                                       Simp. Acc.(overall)            100
                                                                                                                                                                                              Deri. Acc.(overall)

 80                                   80                                     80                            80                                  80                                     80

 60                                   60                                     60                            60                                  60                                     60

 40                                   40                                     40                            40                                  40                                     40

 20                                   20                                     20                            20                                  20                                     20

  0                                    0                                      0                             0                                   0                                      0
      Simp.     Detail     None              Simp.       Detail     None           Simp.   Detail   None         Naming   Noise   Just-only          Naming       Noise   Just-only         Naming   Noise   Just-only

                                       (a) Example mode                                                                                              (b) Data mode

               Figure 18: Performance of DeepSeek-R1-Qwen-8B on SNOMED CT under different data and example modes.
WWW ’26, April 13–17, 2026, Dubai, United Arab Emirates.                                                           Hui Yang, Jiaoyan Chen, and Uli Sattler


                                                           Output Data

                                                           ## AXIOMS_USED
                                                           [2, 4, 6, 7, 8, 9]
     Input Data                                            ## SIMPLIFY
                                                           [8] A2 ⊑ A4 → A2 ⊑ A4
     ## Axioms                                             [7] A4 ⊑ A11 → A4 ⊑ A11
     Axiom 0: A1 ⊑ A2                                      [6] A11 ⊑ A12 ⊓ A13 ⊓ A9 ⊓ A14 ⊓ A15 → A11 ⊑ A9
     Axiom 1: A3 ⊑ A4                                      [4] A9 ⊑ A5 → A9 ⊑ A5
     Axiom 2: A5 ⊑ A6                                      [2] A5 ⊑ A6 → A5 ⊑ A6
     Axiom 3: A7 ⊑ A8                                      [9] A6 ⊑ A7 → A6 ⊑ A7
     Axiom 4: A9 ⊑ A5
                                                           ## DERIVE
     Axiom 5: A10 ⊑ A7
                                                           STEP 1: [8, 7] → A2 ⊑ A11
     Axiom 6: A11 ⊑ A12 ⊓ A13 ⊓ A9 ⊓ A14 ⊓ A15
                                                           EXPLANATION: A2 ⊑ A4 and A4 ⊑ A11 imply A2 ⊑ A11 via subsumption (rule 1).
     Axiom 7: A4 ⊑ A11
                                                           STEP 2: [A2 ⊑ A4, 6] → A2 ⊑ A9
     Axiom 8: A2 ⊑ A4
                                                           EXPLANATION: A2 ⊑ A11 and A11 ⊑ A9 imply A2 ⊑ A9 via subsumption (rule 1).
     Axiom 9: A6 ⊑ A7
                                                           STEP 3: [A2 ⊑ A9, 4] → A2 ⊑ A5
     Axiom 10: A16 ⊑ A17
                                                           EXPLANATION: A2 ⊑ A9 and A9 ⊑ A5 imply A2 ⊑ A5 via subsumption (rule 1).
     Axiom 11: A18 ⊑ A6
                                                           STEP 4: [A2 ⊑ A5, 2] → A2 ⊑ A6
                                                           EXPLANATION: A2 ⊑ A5 and A5 ⊑ A6 imply A2 ⊑ A6 via subsumption (rule 1).
     ## Target Conclusion                                  STEP 5: [A2 ⊑ A6, 9] → A2 ⊑ A7
     A2 ⊑ A7                                               EXPLANATION: A2 ⊑ A6 and A6 ⊑ A7 imply A2 ⊑ A7 via subsumption (rule 1).


      (a) Input axioms and target conclusion                               (b) Output axioms used, simplification, and derivation
                                 Figure 19: A simple example with Atomic distance 6 and Justification size 6

                                                           Output Data
     Input Data
                                                           ## AXIOMS_USED
     ## Axioms                                             1, 3, 4, 9, 10, 12, 13, 15
     Axiom 0: A1 ⊑ A2 ⊓ ∃r3.A4                             ## SIMPLIFY
     Axiom 1: A5 ⊑ A6                                      [1] A5 ⊑ A6 → A5 ⊑ A6
     Axiom 2: A7 ⊑ A2 ⊓ ∃r3.A4                             [3] A2 ⊑ A8 → A2 ⊑ A8
     Axiom 3: A2 ⊑ A8                                      [4] A9 ⊑ A10 → A9 ⊑ A10
     Axiom 4: A9 ⊑ A10                                     [9] A8 ⊑ A5 ⊓ A17 → A8 ⊑ A5
     Axiom 5: A11 ⊑ A2 ⊓ ∃r3.A12                           [10] A12 ⊑ A9 → A12 ⊑ A9
     Axiom 6: A13 ⊑ A2 ⊓ ∃r3.A4                            [12] A19 ⊑ A12 → A19 ⊑ A12
     Axiom 7: A14 ⊑ A2 ⊓ ∃r3.A15                           [13] A20 ≡ A6 ⊓ ∃r3.A10 → A20 ⊑ A6, A20 ⊑ ∃r3.A10, A6 ⊓ ∃r3.A10 ⊑ A20
     Axiom 8: A16 ⊑ A2 ⊓ ∃r3.A4                            [15] A23 ⊑ A2 ⊓ ∃r3.A19 → A23 ⊑ A2, A23 ⊑ ∃r3.A19
     Axiom 9: A8 ⊑ A5 ⊓ A17
                                                           ## DERIVE
     Axiom 10: A12 ⊑ A9
                                                           STEP 1: [3, 9, 1] → A23 ⊑ A6
     Axiom 11: A18 ⊑ A2 ⊓ ∃r3.A4
                                                           EXPLANATION: A23 ⊑ A2 (Axiom 15) ∧ A2 ⊑ A8 (Axiom 3) ∧ A8 ⊑ A5 (Axiom 9) ∧ A5
     Axiom 12: A19 ⊑ A12
                                                           ⊑ A6 (Axiom 1) ⊢ A23 ⊑ A6 via transitive subsumption (rule 1)
     Axiom 13: A20 ≡ A6 ⊓ ∃r3.A10
                                                           STEP 2: [15, 12, 10, 4] → A23 ⊑ ∃r3.A10
     Axiom 14: A21 ⊑ A22
                                                           EXPLANATION: A23 ⊑ ∃r3.A19 (Axiom 15) ∧ A19 ⊑ A12 (Axiom 12) ∧ A12 ⊑ A9 (Axiom
     Axiom 15: A23 ⊑ A2 ⊓ ∃r3.A19
                                                           10) ∧ A9 ⊑ A10 (Axiom 4) ⊢ A23 ⊑ ∃r3.A10 via existential rule (rule 3)
                                                           STEP 3: [STEP1, STEP2, 13] → A23 ⊑ A20
     ## Target Conclusion                                  EXPLANATION: A23 ⊑ A6 ∧ A23 ⊑ ∃r3.A10 ∧ A6 ⊓ ∃r3.A10 ⊑ A20 (Axiom 13) ⊢ A23 ⊑
     A23 ⊑ A20                                             A20 via conjunction (rule 2)


      (a) Input axioms and target conclusion                               (b) Output axioms used, simplification, and derivation
         Figure 20: A complex example with Atomic distance 4 and Justification size 8, split into input and output boxes
Large Language Model for OWL Proofs                                                      WWW ’26, April 13–17, 2026, Dubai, United Arab Emirates.



    Reasoning for Target Conclusion

    ## Axioms
    Axiom 0: A1 ≡ A2 ⊓ ∃r3.( ∃r4.A5 ⊓ ∃r6.A7 ) ⊓ ∃r3.( ∃r4.A5 ⊓ ∃r6.A8 )
    Axiom 1: A9 ⊑ A10 ⊓ A11
    Axiom 2: A12 ≡ A13 ⊓ ∃r3.∃r6.A14
    Axiom 3: A15 ≡ A2 ⊓ ∃r3.( ∃r4.A5 ⊓ ∃r6.A16 )
    Axiom 4: A17 ≡ A2 ⊓ ∃r3.( ∃r4.A5 ⊓ ∃r6.A18 )
    Axiom 5: A19 ⊑ A20 ⊓ ∃r3.∃r6.A21
    Axiom 6: A22 ≡ A23 ⊓ ∃r24.A25
    Axiom 7: A26 ⊑ A9 ⊓ A27
    Axiom 8: A28 ≡ A2 ⊓ ∃r3.( ∃r4.A5 ⊓ ∃r6.A18 ) ⊓ ∃r3.( ∃r4.A5 ⊓ ∃r6.A29 )
    Axiom 9: A30 ⊑ A2 ⊓ ∃r3.∃r6.A21
    Axiom 10: A31 ≡ A2 ⊓ ∃r3.( ∃r4.A5 ⊓ ∃r6.A32 )
    Axiom 11: A33 ⊑ A2
    Axiom 12: A34 ⊑ A35 ⊓ A36
    Axiom 13: A37 ≡ A2 ⊓ ∃r3.( ∃r4.A5 ⊓ ∃r6.A38 ) ⊓ ∃r3.( ∃r4.A5 ⊓ ∃r6.A22 )
    Axiom 14: A39 ≡ A2 ⊓ ∃r3.( ∃r4.A5 ⊓ ∃r6.A29 )
    Axiom 15: A20 ⊑ A13
    Axiom 16: A40 ≡ A20 ⊓ ∃r3.( ∃r4.A41 ⊓ ∃r6.A42 ) ⊓ ∃r3.( ∃r4.A41 ⊓ ∃r6.A43 )
    Axiom 17: A23 ⊑ A34 ⊓ A16
    Axiom 18: A44 ⊑ A45 ⊓ A26 ⊓ A46
    Axiom 19: A36 ⊑ A44
    Axiom 20: A2 ⊑ A47 ⊓ A19 ⊓ ∃r3.∃r6.A21
    Axiom 21: A48 ≡ A2 ⊓ ∃r3.( ∃r4.A5 ⊓ ∃r6.A8 )
    Axiom 22: A49 ⊑ A14
    Axiom 23: A50 ⊑ A51 ⊓ A52
    Axiom 24: A53 ⊑ A49 ⊓ A54
    Axiom 25: A55 ⊑ A56 ⊓ ∃r3.( ∃r4.A57 ⊓ ∃r6.A21 )
    Axiom 26: A58 ≡ A20 ⊓ ∃r3.( ∃r4.A59 ⊓ ∃r60.A61 ⊓ ∃r6.A62 ⊓ ∃r63.A64 )
    Axiom 27: A65 ≡ A2 ⊓ ∃r3.( ∃r4.A66 ⊓ ∃r6.A44 )
    Axiom 28: A67 ≡ A2 ⊓ ∃r3.( ∃r4.A5 ⊓ ∃r6.A23 )
    Axiom 29: A10 ⊑ A53
    ## Target Conclusion
    A37 ⊑ A12


                               Figure 21: A hard example with atomic distance 8 and justification size 15.
