                                                         Autoformalizing Natural Language to First-Order Logic:
                                                                A Case Study in Logical Fallacy Detection

                                                     Abhinav Lalwani1 * Tasha Kim1 * Lovish Chopra1 * Christopher Hahn2 †
                                                                                         ‡                    ‡
                                                                        Zhijing Jin3,4,5, Mrinmaya Sachan4,
                                                                    1
                                                                      Stanford University 2 X, the moonshot factory
                                                  3
                                                    Max Planck Institute for Intelligent Systems 4 ETH Zürich 5 University of Toronto
                                                    {lalwani,tashakim,lovish}@stanford.edu {jinzhi,msachan}@ethz.ch


                                                                   Abstract                         and improving the reasoning capabilities of LLMs
                                                Translating natural language into formal lan-
                                                                                                    has become a critical focus in AI research (Halupt-
                                                guage such as First-Order Logic (FOL) is            zok et al., 2022; Gendron et al., 2024).
arXiv:2405.02318v3 [cs.CL] 6 Mar 2025




                                                a foundational challenge in NLP with wide-
                                                ranging applications in automated reasoning,        In contrast, formal reasoning tools such as Satis-
                                                misinformation tracking, and knowledge val-         fiability Modulo Theory (SMT) solvers excel in
                                                idation. In this paper, we introduce Natural        reasoning, providing rigorous, provable guarantees
                                                Language to First-Order Logic (NL2FOL), a           by leveraging symbolic representations and logi-
                                                framework to autoformalize natural language to      cal calculus (Barrett et al., 2009; De Moura and
                                                FOL step-by-step using Large Language Mod-          Bjørner, 2008). However, a key limitation of for-
                                                els (LLMs). Our approach addresses key chal-        mal solvers is their reliance on structured logical
                                                lenges in this translation process, including the
                                                                                                    input, such as First Order Logic (FOL), which must
                                                integration of implicit background knowledge.
                                                By leveraging structured representations gen-       accurately capture the semantics and context of
                                                erated by NL2FOL, we use Satisfiability Mod-        natural language statements (Beltagy et al., 2016).
                                                ulo Theory (SMT) solvers to reason about the        This presents the challenge of translating unstruc-
                                                logical validity of natural language statements.    tured natural language into a structured form re-
                                                We present logical fallacy detection as a case      quired for formal reasoning while preserving essen-
                                                study to evaluate the efficacy of NL2FOL. Be-       tial context and meaning.
                                                ing neurosymbolic, our approach also provides
                                                interpretable insights into the reasoning pro-      This also brings a unique opportunity: if we can
                                                cess and demonstrates robustness without re-        reliably translate natural language into structured
                                                quiring model fine-tuning or labeled training
                                                                                                    logical forms, we can harness the power of formal
                                                data. Our framework achieves strong perfor-
                                                mance on multiple datasets – on the L OGIC          solvers to reason systematically over natural lan-
                                                dataset, NL2FOL achieves an F1-score of 78%,        guage statements. However, achieving this transla-
                                                while generalizing effectively to the L OGIC -      tion is nontrivial, as it involves accurately capturing
                                                C LIMATE dataset with an F1-score of 80%.1          natural language semantics (Beltagy et al., 2016).
                                                                                                    Moreover, translating to a formal logical form may
                                        1       Introduction                                        cause implicit and external context to be lost, which
                                        In recent years, Large Language Models (LLMs)               must be reintroduced to ensure logical accuracy.
                                        have shown impressive advancements in under-
                                                                                                    To address these challenges, we present NL2FOL,
                                        standing and generating natural language (Brown
                                                                                                    a novel framework that bridges the gap be-
                                        et al., 2020). Despite this progress, their ability
                                                                                                    tween natural language and formal reasoning sys-
                                        to tackle complex reasoning tasks remains limited
                                                                                                    tems. NL2FOL employs a structured, step-by-step
                                        (Bubeck et al., 2023; Wei et al., 2022). These chal-
                                                                                                    pipeline to translate natural language inputs into
                                        lenges are especially prevalent in multistep logical
                                                                                                    first-order logic (FOL) representations, leveraging
                                        deductions, abstract reasoning, and knowledge in-
                                                                                                    large language models (LLMs) at each step for en-
                                        tegration in various domains (Dalvi et al., 2021;
                                                                                                    hanced precision and adaptability. A distinguishing
                                        Chen et al., 2024). Addressing these limitations
                                                                                                    feature of NL2FOL is its seamless integration of
                                            * Equal contribution
                                            †
                                              Work done while at Stanford University
                                                                                                    background knowledge into the generated logical
                                            ‡
                                              Co-supervision                                        forms, overcoming a major limitation of traditional
                                            1
                                              Code available at: github.com/lovishchopra/NL2FOL     formal logic frameworks - the inability to capture
   Fallacy Name            Example                                              Logical Form

   Faulty Generalization   Sometimes flu vaccines don’t work; therefore         (∃x ∈ FluVaccines(DoesntWork(x)) ∧
                           vaccines are useless.                                (FluVaccines ⊆ Vaccines)) ⇒
                                                                                (∀y ∈ Vaccines (DoesntWork(y)))
   False Causality         Every time I wash my car, it rains. Me washing       occuredAfter(washingCar, rain)   ⇒
                           my car has a definite effect on the weather.         caused(washingCar, rain)
   Ad Populum              Everyone should like coffee: 95% of teachers do!     (like(coffee, 95%Teachers))      ⇒
                                                                                (like(coffee, everyone))
   False Dilemma           I don’t want to give up my car, so I don’t think I   ∀(a)(giveUpCar(a)               ∨
                           can support fighting climate change.                 dontSupportFightingClimateChange(a))

Table 1: Sample logical fallacies from Jin et al. (2022) along with examples and their logical forms. For each type
of fallacy, we show one possible logical form.

implicit information embedded in natural language.               guage understanding.
In this paper, we demonstrate the effectiveness of               2    Related Work
NL2FOL through a case study on logical fallacy
                                                                 Logical fallacy detection. Existing work on clas-
detection, showcasing its ability to identify and
                                                                 sifying logical fallacies includes argument suffi-
explain faulty reasoning in natural language argu-
                                                                 ciency classification (Stab and Gurevych, 2017),
ments. Detecting logical fallacies is particularly
                                                                 ad hominem fallacies from Reddit posts (Haber-
challenging as they often rely on reasoning pat-
                                                                 nal et al., 2018b) and dialogues (Habernal et al.,
terns that appear plausible yet are fundamentally
                                                                 2018a), rule parsers (Nakpih and Santini, 2020),
flawed (Jin et al., 2022). To address this, NL2FOL
                                                                 structure-aware Transformers (Jin et al., 2022),
translates logical fallacies from natural language
                                                                 multitask instruction based prompting (Alhindi
into FOL representations, enabling formal solvers
                                                                 et al., 2022), and instance-based reasoning (Sourati
to verify logical validity. These solvers generate
                                                                 et al., 2022). To our knowledge, our work is the
counterexamples and explanations, which are in-
                                                                 first on few-shot classification of logical fallacies
terpreted back into natural language to enhance
                                                                 in a step-by-step, explainable manner. By ensuring
human comprehensibility. By incorporating inter-
                                                                 that the reasoning process is transparent, we allow
mediate natural language outputs, our pipeline im-
                                                                 users to understand and verify the system decision.
proves interpretability, transparency, and debugga-
bility (Bai et al., 2020).                                       Natural language to formal logic. While early
                                                                 work on mapping text to formal logic relied heav-
We show that our framework achieves strong perfor-
                                                                 ily on grammar-based approaches (Purdy, 1991;
mance on the logical fallacy detection benchmarks
                                                                 Angeli and Manning, 2014; MacCartney and Man-
L OGIC and L OGIC C LIMATE (Jin et al., 2022), with
                                                                 ning, 2014), recent advances in deep learning and
F1 scores of 78% and 80%, respectively - out-
                                                                 foundation models have enabled new data-driven
performing existing models by 22% on the chal-
                                                                 techniques for translating natural language to lin-
lenge set, L OGIC C LIMATE. These results high-
                                                                 ear temporal logic (Cosler et al., 2023; Fuggitti and
light NL2FOL as a generalizable and interpretable
                                                                 Chakraborti, 2023; Liu et al., 2022) and first-order
tool for reasoning tasks that demand the precision
                                                                 logic (Singh et al., 2020; Yang et al., 2024; Hahn
of formal reasoning systems. By analyzing the
                                                                 et al., 2022). Neural models for parsing natural lan-
strengths and weaknesses of LLMs at each step of
                                                                 guage to first-order logic (Singh et al., 2020; Yang
the NL2FOL pipeline, we further identify opportu-
                                                                 et al., 2024) and neuro-symbolic approach combin-
nities for improving logical reasoning capabilities.
                                                                 ing language models with first-order logic provers
Even though LLMs prove to be effective in pars-
                                                                 (Olausson et al., 2023) have since been explored.
ing and generating logical representations for struc-
                                                                 However, these approaches still face challenges in
tured inputs, they often struggle with ambiguities in
                                                                 accurately capturing implicit information or trans-
natural language and incorporating nuanced contex-
                                                                 forming complex ambiguous sentences into logical
tual knowledge. The ability to integrate symbolic
                                                                 form, mainly attributed to linguistic ambiguity.
solvers with language models positions NL2FOL
as a powerful neurosymbolic approach, bridging                   Aly et al. (2023) integrated LLMs with logical in-
the gap between formal reasoning and natural lan-                ference for fact verification, and while our method
Figure 1: Overview of the proposed framework used for logical fallacy detection. Module A converts natural
language input to a first-order logic formula merged with contextual relationships, Module B compiles the negation
of a given logical formula to an SMT file with well-defined sorts for variables and predicates, and Module C runs
CVC on the SMT file and if the negation is satisfiable, interprets the counter-model in natural language.

shares the fundamental idea of employing LLMs              the strengths of both to classify logical fallacies.
to construct proofs and analyze relationships be-
                                                           Task formulation. The task input is an argument in
tween textual spans, our task adds a layer of con-
                                                           natural language comprising one or more sentences,
textual reasoning by requiring the incorporation
                                                           which is converted into formal logical form using
of background knowledge and maintaining interde-
                                                           a chain of LLMs. Following this, an SMT solver
pendency between proof steps, which is not present
                                                           processes the logical form and returns whether it is
in approaches where each proof step is treated as
                                                           valid. If invalid, the SMT solver provides a coun-
an independent, isolated process.
                                                           terexample explaining why it is a logical fallacy,
Theory solvers. Recent work by Hahn et al. (2022)          which is then interpreted with an LLM.
demonstrated the potential of integrating symbolic
solvers with large language models (LLMs), such            First-order logic. In FOL, propositions are rep-
as tool-augmented LLMs, to combine neural and              resented using predicates that express properties
symbolic reasoning. While such approaches are              or relations over objects in a domain. These predi-
promising, they often struggle to translate natural        cates can be combined with constants, representing
language into symbolic representations and effec-          specific objects and variables that represent unspec-
tively capture background knowledge. Other recent          ified elements in the domain. An Interpretation
approaches (Olausson et al., 2023; Pan et al., 2023)       assigns meaning to these symbols within a given
have used theory solvers to logically reason with          context, while a Sort categorizes objects into differ-
natural language, which we build on with several           ent types, facilitating precise reasoning about their
key advancements. First, we introduce a frame-             properties. Logical connectives of FOL, such as im-
work that handles naturalistic, real-world data and        plication (⇒), universal quantifiers (∀), existential
tasks with ambiguous premises and conclusions.             quantifiers (∃), and operators for conjunction/and
Then, we present a method to incorporate back-             (∧), disjunction/or (∨), and negation/not (¬), allow
ground knowledge into logical formulas. Finally,           for the construction of intricate statements.
we show that our approach introduces interpretabil-        Module A: Natural language to first-order logic.
ity by allowing human verification and modifica-           Our approach for converting given natural lan-
tion throughout the intermediate reasoning steps.          guage sentences into a logical form comprises mul-
                                                           tiple steps involving few-shot prompting of LLMs:
3   Methodology
                                                           (i) decomposing a sentence into multiple smaller
Although powerful, LLMs struggle to detect logical         parts that can be represented in first-order logic,
fallacies in language, as it requires proper logical       (ii) identifying relationships between different sub-
analysis (Jin et al., 2022). On the other hand, SMT        components to merge them and obtain a resultant
solvers can reason over logical formulas with the-         logical formula, and (iii) identifying real-world
oretical guarantees but require the input to be in a       relationships between these sub-components (back-
structured, logical form. This approach combines           ground knowledge) and augmenting them to ob-
tain a FOL formula by incorporating background          the relation between properties and entities. (see
knowledge in the statement. We demonstrate with         Prompt 5). We also find the relationships between
a Logical Fallacy (LF) and a Valid (V) example.         various properties (see Prompt 6). For instance,
                                                        in the LF Example, it can be inferred that Like
 1. LF Example: A Logical Fallacy Input
 I met a tall man who loved to eat cheese, now I        and Love are contextually similar. Similarly, in our
 believe all tall people like cheese.                   valid example, jumping over skateboard implies do-
 2. V Example: A Valid Input                            ing a skateboard trick. These relationships provide
 A boy is jumping on a skateboard in the middle of a    an additional context that is not directly present in
 red bridge. Thus the boy does a skateboarding trick.
                                                        the statement.
Our pipeline begins with a semantic decomposition
                                                        To identify these contextual relationships, we run
module which decomposes natural language argu-
                                                        NLI between each pair of properties, i.e., by setting
ments into respective claims and implications. Gen-
                                                        one property as the hypothesis and the other as the
erally, a sentence can be split into some claims and
                                                        premise as the input to the NLI model. If we find
implications based on those claims (see Prompt 2).
                                                        that any one property entails the other, we add the
 1. LF Example: Claim and Implication Parser            relationship property1 ⇒ property2 to our con-
 Claim: A tall man loved to eat cheese.                 text. Before running the NLI model between a pair
 Implication: All tall people like cheese.
                                                        of properties, we replace the variables in each prop-
 2. V Example: Claim and Implication Parser             erty with the referring expressions that they repre-
 Claim: A boy is jumping on a skateboard in the
 middle of a red bridge.                                sent. This adds additional context that helps the
 Implication: The boy does a skateboarding trick.       NLI model identify relations. For instance, in the
                                                        V Example, the NLI model is unable to find the re-
The claims and implications are split into further
                                                        lation between JumpsOn(x, s) and Does(x, y), but it
sub-components and used to build up the logical
                                                        can identify the relationship between JumpsOn(boy,
form of the sentence. The next step is to identify
                                                        skateboard) and Does(boy, skateboardingTrick).
entities in the sentence. In our work, we treat noun
phrases or surrogates for noun phrases as entities       1. LF Example: Property Extractor + Background
(see Prompt 3). Then, we find the relationship           Knowledge Retriever
                                                         Properties: Tall, Love, Like
between the different entities using Zero-Shot clas-     Property entity relations: Tall(x), Love(x, c)
sification via Natural Language Inference (NLI).         Background knowledge:
These relationships (e.g., subset, equality, not re-        1. ∀x(Like(x, c) ⇒ Love(x, c))
                                                            2. ∀x(Love(x, c) ⇒ Like(x, c))
lated) are generally helpful in deciding appropriate        3. x ⊆ y
quantifiers in the logical form. For example, if the     2. V Example: Property Extractor + Background
entities are man and people, then it can be inferred     Knowledge Retriever
that man is a subset of people and that the man          Properties: JumpsOn, inMiddleOf, Red, Does
                                                         Property entity relations: JumpsOn(b, s),
would be bound by an existential quantifier in the       Red(bridge), inMiddleOf(b, bridge), Does(b, y)
sentence x (see Prompt 4).                               Background knowledge:
                                                           1. ∀x(JumpsOn(b, s) ⇒ Does(b, y))
 1. LF Example: Entity Extractor
 Referring expressions:
     • man: x
                                                        Finally, we combine all of this information using
     • cheese: c                                        the relationships between properties and entities to
     • people: y                                        obtain the FOL form of the sentence with the help
     • x⊆y
                                                        of an LLM (see Prompt 7). For a logical fallacy, the
 2. V Example: Entity Extractor                         negation of the formula is expected to be satisfiable.
 Referring expressions:
     • boy: b                                           On the contrary, for a valid statement, the negation
     • skateboard: s                                    of the formula should be unsatisfiable.
     • bridge
     • skateboardingTrick: y                             1. LF Example: NL2FOL Output
                                                         First-order logic: ((∀x(Like(x, c) ⇒ Love(x, c)))∧
The other set of sub-components are properties,          (∀x(Love(x, c) ⇒ Like(x, c)))∧ (∃x(Tall(x) ∧
which describe a trait of a referring expression or      Love(x, c)))) ⇒ (∀y(Tall(y) ⇒ Like(y, c)))
relationship between multiple referring expressions.     2. V Example: NL2FOL Output
                                                         First-order logic:       (∀x(JumpsOn(x, s)      ⇒
These properties are predicates in first-order logic.    Does(x, y)) ∧ Red(bridge)∧ inMiddleOf(b, bridge) ∧
We use a single module to extract the properties and     JumpsOn(b, s)) ⇒ Does(b, y)
Module B: First-order logic to SMT. The next                   L OGIC C LIMATE (Jin et al., 2022) datasets, origi-
step involves automatically creating an SMT file               nally designed for training models to identify and
for the negation of the first-order logical formula            classify different fallacies. These datasets contain
generated. While one can easily write an SMT                   examples of logical fallacies, each labeled with
file for a logical formula manually, generating one            multiple categories from 13 different categories,
automatically for an arbitrary formula has not been            including faulty generalization, circular claim, and
done before. Thus, we develop a compiler that                  ad hominem. The L OGIC dataset contains 2,449
parses a given logical formula and converts it into            examples of common logical fallacies collected
an SMT file that can be given to CVC as input, as              mostly from quiz websites. The L OGIC C LIMATE
described in Algorithm 1 (See Appendix).                       dataset comprises 1,079 examples of logical falla-
                                                               cies drawn from climate change news articles on
Module C: Interpreting SMT results. To ver-
                                                               the Climate Feedback platform. It is intended to
ify the validity of the logical formulas, we utilize
                                                               test the model’s ability to generalize out-of-domain.
an SMT solver, CVC4 (Barrett et al., 2011). The
solver determines whether the formula is valid or              To test our approach with valid statements, we use
invalid, hence a logical fallacy. In the case of in-           the Stanford Natural Language Inference (SNLI)
validity, the model provides a counterexample to               corpus (Bowman et al., 2015), which supports the
the original logical formula, which shows that the             development of natural language inference sys-
given claim or implication is a logical fallacy.               tems. This dataset features over 570,000 human-
 Example (Module B Output):                                    annotated sentence pairs, where each pair consists
 I met a tall man who loved to eat cheese, now I               of a premise and a hypothesis labeled as entailment,
 believe all tall people like cheese.
                                                               contradiction, or neutral. We focus on the entail-
                             ↓
 First-order logic: ((∀x(Like(x, c) ⇒ Love(x, c)))∧            ment class in this study, extracting over 170,000
 (∀x(Love(x, c) ⇒ Like(x, c)))∧ (∃x(Tall(x) ∧                  sentence pairs where the premise entails the hypoth-
 Love(x, c)))) ⇒ (∀y(Tall(y) ⇒ Like(y, c)))                    esis. We construct valid sentences by combining
                             ↓
                                                               the premise and hypothesis into a single sentence.
 SMT classification: Logical fallacy
 Explanation: Counterexample
                                                               The task is set up as a simple binary classification
                             ↓
     • John is tall (Tall(John) is True). John likes           task, where the input consists of sentences drawn
       cheese (Likes(John, Cheese) is True).                   from the L OGIC or L OGIC C LIMATE datasets la-
     • Jane is tall (Tall(Jane) is True). No constraint        beled as logical fallacies or from the SNLI dataset
       Jane likes cheese.
                                                               labeled as valid sentences. Here, we treat logical
    Therefore, there exists a tall person (John) who likes     fallacies as the positive class. To ensure a balanced
    cheese, but it does not follow that all tall people like   evaluation, we select an equal number of fallacies
    cheese, since Jane serves as a counterexample.
                                                               and valid statements, allowing for a fair comparison
Figure 2: Example of logical fallacy detection using           across both classes. Finally, our model is evaluated
NL2FOL. The resulting classification is explained using        on standard binary classification metrics such as
a counterexample generated by the SMT solver.                  precision, recall, f1 score, and accuracy.
The result of the SMT solver is hard to interpret, as          Models. We compare our method to pretrained
it uses technical terminology generally only well              language models, including Llama2-7B (Touvron
understood by those who are familiar with CVC4                 et al., 2023), GPT4o-mini (OpenAI, 2024), GPT4o
and SMT. To obtain an explanation in natural lan-              (OpenAI et al., 2024a) and OpenAI o1-preview
guage, we prompt an LLM with the claim, impli-                 (OpenAI et al., 2024b) with few-shot in-context
cation, referring expressions, properties, FOL for-            examples (see Prompt 1). We also run NL2FOL
mula, and the counterexample generated by CVC4.                with each of the above models used for the LLM
The model then interprets the counterexample with              prompting stages. Llama2-7B was chosen for our
natural language, as depicted in Figure 2.                     experiments as it had the best performance dur-
                                                               ing testing over an initial subset of the data, out-
4      Experiments
                                                               performing Llama3.1-8B (Grattafiori et al., 2024),
We evaluate our approach on both logical falla-                Llama3.2-11B (AI, 2024a), and Ministral-8B (AI,
cies (positive class) and valid statements (negative           2024b). We evaluate BART (140M parameters)
class). For logical fallacies, we use the L OGIC and           (Lewis et al., 2020) finetuned on MNLI (Williams
                                                         L OGIC                     L OGIC C LIMATE
          Model                Method           Acc.    P.     R.     F1     Acc.      P.    R.       F1
                               End-to-end       0.41   0.45    0.82   0.58   0.31     0.38   0.62     0.47
          Llama-7B
                               NL2FOL (Ours)    0.63   0.58    0.92   0.71   0.66     0.60   0.94     0.73
                               End-to-end       0.91   0.94    0.88   0.91   0.64     0.67   0.55     0.60
          GPT-4o-mini
                               NL2FOL (Ours)    0.70   0.64    0.91   0.75   0.73     0.66   0.93     0.77
                               End-to-end       0.96   0.96    0.96   0.96   0.70     0.95   0.42     0.58
          GPT-4o
                               NL2FOL (Ours)    0.78   0.76    0.82   0.78   0.80     0.80   0.80     0.80
                               End-to-end       0.93   0.89    0.98   0.93   0.73     0.84   0.56     0.67
          OpenAI o1-preview
                               NL2FOL (Ours)      -      -       -      -      -        -      -        -

Table 2: Comparison of few-shot model performance metrics (abbreviations: Acc. = accuracy, P. = precision, R. =
recall, F1 = F1 score) on the L OGIC+SNLI and L OGIC C LIMATE+SNLI datasets using End-to-end vs. NL2FOL
(Ours). Results on NL2FOL with o1-preview are omitted as o1-preview failed to complete the pipeline in most
cases, likely due to its poor instruction following capabilities.

et al., 2018) to analyze the relationships between       alization, the in-context examples we provide to
properties and referring expressions. We ran the         all models are from the L OGIC dataset. NL2FOL
experiments on a V100 GPU, with one run costing          yields results that are highly similar to the results
around 2 GPU hours.                                      from L OGIC, whereas end-to-end classification saw
                                                         a drop in performance. This demonstrates that
Prompt tuning. For prompt tuning, 20 samples
                                                         our system is also robust and adapts well to real-
from the L OGIC dataset were selected and manu-
                                                         world texts, including texts with significant domain-
ally annotated with intermediate and final results.
                                                         specific context. This makes it effective in detect-
They were then split into 10 train and 10 valida-
                                                         ing and mitigating misinformation. Specifically,
tion examples. For each prompt, we start with a
                                                         on this dataset, we find that NL2FOL outperforms
simple description of the task. 4-6 examples were
                                                         direct translation with all LLMs that we tested.
randomly selected from the train set as in-context
examples, with the relevant intermediate outputs         5.1    Quantitative Analysis
depending on the stage. Results were tested on the       Error analysis and interpretability. The pro-
validation examples, and the prompt was updated          posed method is interpretable due to the use of
to address common mistakes. To ensure fairness, a        natural language inputs and outputs at each step
fixed number of 5 improvement iterations was used        of the pipeline. This structure allows for precise
for each prompt, and the one showing best perfor-        identification of the specific module responsible
mance over the validation examples was chosen.           for a failure by examining intermediate results. To
                                                         evaluate this aspect, we performed an in-depth er-
5   Results and Discussion
                                                         ror analysis by annotating the module responsible
As shown in Table 2, our method achieves an              for failure in 100 incorrect predictions made by the
F1 score of 78% when used with GPT-4o on the             model. The results are summarized in Table 4.
L OGIC dataset. When run end-to-end, the Llama-
                                                         Our analysis reveals that the majority of errors oc-
7B model reached an F1 score of only 58%, but
                                                         cur in the ‘Background Knowledge Retriever’, in-
when used with the NL2FOL pipeline, reached
                                                         volving missed or incorrectly added contextual in-
a score of 71%. Although end-to-end classifica-
                                                         formation in the logical form. Other errors typically
tion has shown better performance in other models,
                                                         pertain to incorrect identification of claims, impli-
comparisons can be skewed because they may have
                                                         cations, or properties. In contrast, inaccuracies in
been exposed to the L OGIC dataset and its labels
                                                         the generation of logical forms are relatively infre-
during training because this dataset was compiled
                                                         quent, suggesting that the model performs well in
from publicly accessible web sources. On average,
                                                         constructing accurate logical representations when
NL2FOL demonstrated high recall, whereas end-
                                                         provided with reliable information about the con-
to-end classification demonstrated high precision.
                                                         stituent entities and properties within a sentence.
Our challenge set L OGIC C LIMATE+SNLI contains          This finding underscores the importance of improv-
real-world logical fallacies from climate change         ing the background knowledge retriever module to
news. Since this dataset was used to test gener-         improve overall model performance.
    Type Sentence                 Logical Form                                              Prediction
  1 LF X has been around          (IsNew(a) ∧ ∼ IsNew(b)) ⇒ (IsBetterThan(a,b))             LF: Correct prediction
         for years now. Y is
         new. Therefore, Y
         is better than X.
  2 LF Everyone is doing          (∃ b (∃ a (IsDoing(b,a)))) ⇒ (∃ c (∃ a (IsDo-             V: Incorrect prediction - Wrong
         the Low-Carb Diet.       ing(c,a)))).                                              translation given when no claim
                                                                                            given
  3 V      Two dogs are fight-    (∃ b (∃ a (IsFighting(a, b) ∧ IsInField(b) ∧ IsIn-        LF: Incorrect prediction - Missing
           ing in a field. Con-   Field(b)))) ⇒ (∃ a (IsOutside(a)))                        semantic ground truth claim: ∀ a
           sequently, the two                                                               (IsInField(a) ⇒ IsOutside(a))
           dogs are outside.
  4 V      A baseball player      (∃ a (IsGettingReady(a) ∧ (IsABaseballPlayer(a)           V: Correct Prediction - The method
           gets ready to catch    ∧ IsCatchingFlyBall(a) ∧ IsNearOutfield-                  identifies additional context by es-
           a fly ball near        Fence(a))) ∧ (∀ e ( IsABaseballPlayer(e) ⇒                tablishing relationships such as Is-
           the outfield fence.    IsPlayingBaseball(e))) ∧ (∀ f ( IsPlayingBase-            BaseballPlayer implying IsPlaying-
           Therefore, a person    ball(f) ⇒ IsABaseballPlayer(f))) ∧ (∀ g (                 Baseball, and IsNearOutfieldFence
           is playing baseball    IsNearOutfieldFence(g) ⇒ IsOutdoors(g))))                 implying IsOutdoors.
           outdoors.              ⇒ (∃ c (∃ a (IsPlayingBaseball(a) ∧ IsOut-
                                  doors(c))))
  5 V      A woman sits alone     (IsSittingOn(a, b) ∧ isParkBench(b) ∧ IsIn-               LF: Incorrect prediction - Miss-
           on a park bench in     Sun(a)) ⇒ (IsInPark(a)).                                  ing semantic ground truth claim:
           the sun. Hence, a                                                                ∀a∀b (IsSittingOn(a, b) ∧ isPark-
           woman is in a park.                                                              Bench(b) ⇒ IsInPark(a))
  6 V      A woman is stand-      (∃a∃b (IsStandingAt(b, a)) ∧ ∀f ∀e∀d (IsStandin-          V: Correct prediction - The method
           ing at a podium.       gAt(d,e) ⇒ IsAt(f,e)) ⇒ ∃c∃a (IsAt(c, a))                 identifies additional context by
           Thus, a person is at                                                             establishing the relationship Is-
           a podium.                                                                        StandingAt implying IsAt.

    Table 3: Some example outputs of our model (abbreviations: LF = Logical Fallacy, V = Valid statement)

 Sub-Module with Error               Error Proportion          LLM model with sentence context achieves the
 Claim and Implication Parser                0.19              highest overall performance. This is likely due to
 Incorrect Label                             0.01              the sentence context providing information about
 Property Extractor                          0.13              clauses that are omitted due to the choice of rep-
 Background Knowledge Retriever              0.54              resentation in FOL. This indicates that integrating
 FOL Formulation Engine                      0.13              robust grounding mechanisms is critical to enhanc-
                                                               ing the accuracy and reliability of the method.
Table 4: Categorization of model errors by type on
NL2FOL (GPT-4o), based on a review by domain ex-                                        LOGIC+SNLI            L OGIC C LIMATE +SNLI
perts in the logic of 100 randomly sampled examples             Method               Acc.     P.   R.   F1 Acc.       P.   R.    F1
                                                                (a) No Grounding     0.54    0.52 0.88 0.66   0.57   0.54 0.94   0.69
Impact of adding background knowledge to                        (b) LLM              0.76    0.78 0.74 0.75   0.79   0.80 0.78   0.79
                                                                (c) LLM w/ context   0.78    0.76 0.82 0.78   0.80   0.80 0.80   0.80
NL2FOL. Based on the error analysis, missing or                 (d) BART-MNLI        0.71    0.71 0.70 0.70   0.77   0.81 0.71   0.77
incorrect background knowledge was a significant
contributor to incorrect predictions of our method.            Table 5: Comparison of different grounding methods on
To quantitatively assess the impact of grounding               NL2FOL (GPT4o-mini) across the LOGIC+SNLI and
on model performance, we evaluated several ap-                 LogicClimate+SNLI datasets
proaches for NLI in the Background Relation Ex-
tractor. These included: (a) a pipeline without any            Impact of using an SMT solver. To assess the
background knowledge as a baseline, (b) a model                impact of using an SMT solver in our pipeline, we
without context where the LLM (GPT4o) only pro-                compared its performance against an LLM as a
cesses the input properties, (c) an LLM that incor-            baseline for classifying the logical forms as valid
porates both the input sentence and properties and             or fallacies. The results, summarized in Table 6,
(d) a smaller model specifically fine-tuned for NLI            demonstrate a significant improvement in perfor-
(BART-MNLI). Results are presented in Table 5.                 mance metrics with the integration of the SMT
                                                               solver. Results reveal the SMT-based approach sig-
We see that precision and recall both improve sig-             nificantly outperforms the LLM-based approach
nificantly with better grounding techniques. The               in all metrics across both the L OGIC and L OGIC -
C LIMATE datasets. This underscores the advantage                        L OGIC           L OGIC C LIMATE
of formal reasoning systems like SMT solvers for       Classifier Acc. P.     R.   F1 Acc. P.       R.   F1
tasks requiring precise logical inference and struc-   SMT        0.78 0.76 0.82 0.78 0.80 0.80 0.80 0.80
tured reasoning compared to LLMs, which may            GPT-4o     0.69 0.71 0.62 0.66 0.73 0.72 0.74 0.73
lack systematic consistency in such contexts.
                                                       Table 6: Comparison of classification methods used with
5.2     Qualitative Analysis                           NL2FOL (GPT4o) on L OGIC and L OGIC C LIMATE
5.2.1    Success Modes of NL2FOL                       an incorrectly added clause can cause a fallacy to
S1: Captures implicit information not men-             be identified as valid. One such case is present in
tioned in premises. Previous works that directly       example 3 of the Table 3. In this case, the model
translate natural language to logical forms suffer     is not able to identify the extra context statement
from an inability to capture implicit information      because the NLI model does not identify a required
not mentioned in the premises (Olausson et al.,        ground-truth relation. If this context were to be
2023). Our “Background Knowledge Retriever”            added to the claim of the logical formula, then the
step allows us to capture this information in the      statement would have been predicted to be valid.
final logical form. An illustration of this can be
                                                       F2: Limitations of NLI. Our current approach
found in Example 4 of Table 3.
                                                       is limited to discerning relationships between two
S2: Captures explicit information that is missed       properties at a time rather than handling multiple
in the representation. Our pipeline is also able to    relationships concurrently. For reference, consider
capture information that is explicitly mentioned in    Example 5 in Table 3. Here, the semantic claim
the premises but missed due to the choice of repre-    involves the conjunction of two properties entail-
sentation in logical form. In Example 6, in Table 3,   ing the third, while the ‘Background Knowledge
the fact that the woman is both standing and is at     Retriever’ only checks whether one property en-
the podium is lost due to the choice representation    tails the other. Finding such complex extra context
IsStandingAt. However, the fact that the woman         requires more advanced techniques or additional
is at the podium is recovered in the final logical     human intervention. Including them could further
form due to the identified background knowledge        improve the precision of the model overall.
IsStandingAt implies IsAt.
                                                       F3: Imprecision of LLMs. Among the logical
S3: Comparison to direct translation. To evalu-        fallacies that our model incorrectly predicted to
ate the efficacy of the multi-step LLM pipeline, we    be a valid statement, most of these predictions
compared it against a direct translation approach,     failed due to the imprecision of the LLM, leading to
where natural language inputs were converted into      false translations and incorrect results. Example 2
logical forms with a single LLM call using a few-      demonstrates a case where the input does not have
shot prompt. However, this task proved to be exces-    any claim but instead jumps straight to an implica-
sively complex for LLMs. Llama failed to generate      tion. However, the model is not able to identify that
any output, citing an inability to comprehend the      the example has no claim. As a result, we obtain
prompt. Larger LLMs exhibited significant limi-        an incorrect translation with our technique.
tations, with over 95% of their outputs containing
syntax errors. These findings highlight the inad-      6   Conclusion
equacy of direct translation for complex logical
reasoning tasks and underscore the necessity of a      We present an effective and automatic solution to
structured, multi-step approach to ensure the accu-    detect fallacies and tackle misinformation. We
racy and syntactic correctness of the logical form.    developed a strategy to distinguish logical falla-
                                                       cies from valid statements, involving a chaining
5.2.2    Failure Modes of NL2FOL                       approach to convert a sentence to first-order logic
F1: Misses some background knowledge. As can           using LLMs, followed by using SMT solvers to
be observed in Table 4, incorrect identification of    identify whether the first-order logical statement is
background knowledge is the most common cause          valid or not. If not, we interpret the counter-model
for incorrect classifications. This is because any     generated by the SMT solver in natural language.
gaps in background knowledge can cause a valid         Our proposed technique shows promising results
statement to be identified as a logical fallacy, and   in identifying logical fallacies and valid statements,
as well as good generalizability across domains.           Going beyond first-order logic. It is unknown
                                                           whether our approach would be sufficiently expres-
Ethics Statement                                           sive for reasoning tasks requiring higher-order or
                                                           non-classical logic, as we limit our exploration
While the intended outcome of this research is to
                                                           to first-order logic. Conceptually, extending our
help fight misinformation and promote rational dis-
                                                           method to the aforementioned domains is feasible
course, there are several ethical challenges that we
                                                           but would require modification to the SMT integra-
must consider. First, dependence on AI to identify
                                                           tion and LLM-driven logic translation processes.
logical fallacies could influence how individuals
                                                           Thus, further testing may include translating to
engage in debates and discussions. There is a risk
                                                           logic beyond FOL, such as temporal and higher-
that people may over-rely on AI judgments, po-
                                                           order logic.
tentially stifling complex statements or dissenting
opinions that are essential for a healthy democratic       Computational cost. Using LLMs and SMT
process. Moreover, the use of AI in moderating dis-        solvers can incur high computational costs, such as
cussions, especially in identifying logical fallacies,     high-performance GPUs for LLM inference, CPUs
raises ethical questions about the automation of           optimized for SMT solvers, and high API usage,
content moderation. While it can enhance the qual-         particularly for models like GPT-o1 and Llama-7B.
ity of public discourse by filtering out fallacious
statements, it also risks automating censorship and
impacting the dynamics of online communities. In           References
the wrong hands, logical fallacy detection tools           Meta AI. 2024a. Llama 3.2-11b model card. Accessed:
could be exploited to silence speech or suppress           2025-02-15.
viewpoints under the pretext of promoting rational
                                                           Mistral AI. 2024b. Ministral-8b-instruct-2410 model
discourse. This potentially allows governments or          card. Accessed: 2025-02-15.
organizations to stifle opposition or critique.
                                                           Tariq Alhindi, Tuhin Chakrabarty, Elena Musi, and
To address these issues, we advocate for the devel-        Smaranda Muresan. 2022. Multitask instruction-based
opment of ethical guidelines for AI use that empha-        prompting for fallacy recognition. In Proceedings of
                                                           the 2022 Conference on Empirical Methods in Natural
size transparency, accountability, and active user         Language Processing, pages 8172–8187, Abu Dhabi,
engagement. These measures are crucial in encour-          United Arab Emirates. Association for Computational
aging public literacy in AI and logical fallacies, ulti-   Linguistics.
mately empowering individuals to critically assess         Rami Aly, Marek Strong, and Andreas Vlachos. 2023.
both AI output and arguments they may encounter.           QA-natver: Question answering for natural logic-based
                                                           fact verification. In The 2023 Conference on Empirical
Limitations                                                Methods in Natural Language Processing.

Scope of logical reasoning tasks. Correct iden-            Gabor Angeli and Christopher D Manning. 2014. Natu-
                                                           ralli: Natural logic inference for common sense reason-
tification of background knowledge is crucial for          ing. In Proceedings of the 2014 Conference on Empiri-
our method. While we have shown its potential in           cal Methods in Natural Language Processing (EMNLP),
detecting logical fallacies for short and structured       pages 534–545.
premises, it is important to note that this approach       Bing Bai, Jian Liang, Guanhua Zhang, Hao Li, Kun
may miss complex relational constructs (for exam-          Bai, and Fei Wang. 2020. Why attentions may not be
ple, (a ∧ b) ⇒ (c ∨ d))), in which richer logical          interpretable? Proceedings of the 27th ACM SIGKDD
patterns may often be required in real-world reason-       Conference on Knowledge Discovery & Data Mining.
ing tasks such as those present in multi-paragraph         Clark Barrett, Christopher L. Conway, Morgan Deters,
contexts or Question-Answering (QA) datasets.              Liana Hadarean, Dejan Jovanović, Tim King, Andrew
                                                           Reynolds, and Cesare Tinelli. 2011. Cvc4. In Computer
Generalizability to other tasks and domains. We            Aided Verification, pages 171–177, Berlin, Heidelberg.
have demonstrated promising results of our ap-             Springer Berlin Heidelberg.
proach to logical fallacy detection, but whether           Clark Barrett, Aaron Stump, and Cesare Tinelli. 2009.
the findings generalize to other logical tasks and         Satisfiability modulo theories. Communications of the
domains remains unexplored. The performance of             ACM, 52(9):69–77.
our approach in other languages is untested and            Iz Beltagy, Stephen Roller, Pengxiang Cheng, Katrin
may introduce unforeseen challenges.                       Erk, and Raymond J. Mooney. 2016. Representing
meaning with a combination of logical and distributional      Abhinav Pandey, Abhishek Kadian, Ahmad Al-Dahle,
models. Computational Linguistics, 42(4):763–808.             Aiesha Letman, Akhil Mathur, Alan Schelten, Alex
                                                              Vaughan, Amy Yang, Angela Fan, Anirudh Goyal, An-
Samuel R. Bowman, Gabor Angeli, Christopher Potts,            thony Hartshorn, Aobo Yang, Archi Mitra, Archie Sra-
and Christopher D. Manning. 2015. A large annotated           vankumar, Artem Korenev, Arthur Hinsvark, Arun Rao,
corpus for learning natural language inference. In Pro-       Aston Zhang, Aurelien Rodriguez, Austen Gregerson,
ceedings of the 2015 Conference on Empirical Methods          Ava Spataru, Baptiste Roziere, Bethany Biron, Binh
in Natural Language Processing, pages 632–642, Lis-           Tang, Bobbie Chern, Charlotte Caucheteux, Chaya
bon, Portugal. Association for Computational Linguis-         Nayak, Chloe Bi, Chris Marra, Chris McConnell,
tics.                                                         Christian Keller, Christophe Touret, Chunyang Wu,
Tom B Brown, Benjamin Mann, Nick Ryder, Melanie               Corinne Wong, Cristian Canton Ferrer, Cyrus Niko-
Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind              laidis, Damien Allonsius, Daniel Song, Danielle Pintz,
Neelakantan, Pranav Shyam, Girish Sastry, Amanda              Danny Livshits, Danny Wyatt, David Esiobu, Dhruv
Askell, Sandhini Agarwal, Ariel Herbert-Voss, Gretchen        Choudhary, Dhruv Mahajan, Diego Garcia-Olano,
Krueger, Tom Henighan, Rewon Child, Aditya Ramesh,            Diego Perino, Dieuwke Hupkes, Egor Lakomkin, Ehab
Daniel Ziegler, Jeffrey Wu, Clemens Winter, Chris             AlBadawy, Elina Lobanova, Emily Dinan, Eric Michael
Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott          Smith, Filip Radenovic, Francisco Guzmán, Frank
Gray, Benjamin Chess, Jack Clark, Christopher Berner,         Zhang, Gabriel Synnaeve, Gabrielle Lee, Georgia Lewis
Sam McCandlish, Alec Radford, Ilya Sutskever, and             Anderson, Govind Thattai, Graeme Nail, Gregoire Mi-
Dario Amodei. 2020. Language models are few-shot              alon, Guan Pang, Guillem Cucurell, Hailey Nguyen,
learners. Advances in Neural Information Processing           Hannah Korevaar, Hu Xu, Hugo Touvron, Iliyan Zarov,
Systems, 33:1877–1901.                                        Imanol Arrieta Ibarra, Isabel Kloumann, Ishan Misra,
                                                              Ivan Evtimov, Jack Zhang, Jade Copet, Jaewon Lee, Jan
Sébastien Bubeck, Varun Chandrasekaran, Ronen Eldan,          Geffert, Jana Vranes, Jason Park, Jay Mahadeokar, Jeet
Johannes Gehrke, Eric Horvitz, Ece Kamar, Peter Lee,          Shah, Jelmer van der Linde, Jennifer Billock, Jenny
Yin Tat Lee, Yuanzhi Li, Scott Lundberg, Harsha Nori,         Hong, Jenya Lee, Jeremy Fu, Jianfeng Chi, Jianyu
Hamid Palangi, Marco Tulio Ribeiro, and Yi Zhang.             Huang, Jiawen Liu, Jie Wang, Jiecao Yu, Joanna Bit-
2023. Sparks of artificial general intelligence: Early        ton, Joe Spisak, Jongsoo Park, Joseph Rocca, Joshua
experiments with gpt-4.                                       Johnstun, Joshua Saxe, Junteng Jia, Kalyan Vasuden
                                                              Alwala, Karthik Prasad, Kartikeya Upasani, Kate Plaw-
Zixiang Chen, Yihe Deng, Huizhuo Yuan, Kaixuan Ji,            iak, Ke Li, Kenneth Heafield, Kevin Stone, Khalid
and Quanquan Gu. 2024. Self-play fine-tuning converts         El-Arini, Krithika Iyer, Kshitiz Malik, Kuenley Chiu,
weak language models to strong language models.               Kunal Bhalla, Kushal Lakhotia, Lauren Rantala-Yeary,
                                                              Laurens van der Maaten, Lawrence Chen, Liang Tan,
Matthias Cosler, Christopher Hahn, Daniel Mendoza,
                                                              Liz Jenkins, Louis Martin, Lovish Madaan, Lubo Malo,
Frederik Schmitt, and Caroline Trippel. 2023. nl2spec:
                                                              Lukas Blecher, Lukas Landzaat, Luke de Oliveira,
Interactively translating unstructured natural language
                                                              Madeline Muzzi, Mahesh Pasupuleti, Mannat Singh,
to temporal logics with large language models. In Com-
                                                              Manohar Paluri, Marcin Kardas, Maria Tsimpoukelli,
puter Aided Verification. CAV 2023. Lecture Notes in
                                                              Mathew Oldham, Mathieu Rita, Maya Pavlova, Melanie
Computer Science, volume 13965, Cham. Springer.
                                                              Kambadur, Mike Lewis, Min Si, Mitesh Kumar Singh,
Bhavana Dalvi, Peter Jansen, Oyvind Tafjord, Zheng-           Mona Hassan, Naman Goyal, Narjes Torabi, Nikolay
nan Xie, Hannah Smith, Leighanna Pipatanangkura, and          Bashlykov, Nikolay Bogoychev, Niladri Chatterji, Ning
Peter Clark. 2021. Explaining answers with entailment         Zhang, Olivier Duchenne, Onur Çelebi, Patrick Al-
trees. In Proceedings of the 2021 Conference on Em-           rassy, Pengchuan Zhang, Pengwei Li, Petar Vasic, Peter
pirical Methods in Natural Language Processing, pages         Weng, Prajjwal Bhargava, Pratik Dubal, Praveen Krish-
7358–7370, Online and Punta Cana, Dominican Repub-            nan, Punit Singh Koura, Puxin Xu, Qing He, Qingx-
lic. Association for Computational Linguistics.               iao Dong, Ragavan Srinivasan, Raj Ganapathy, Ra-
                                                              mon Calderer, Ricardo Silveira Cabral, Robert Stojnic,
Leonardo De Moura and Nikolaj Bjørner. 2008. Z3: an           Roberta Raileanu, Rohan Maheswari, Rohit Girdhar, Ro-
efficient smt solver. In Proceedings of the Theory and        hit Patel, Romain Sauvestre, Ronnie Polidoro, Roshan
Practice of Software, 14th International Conference on        Sumbaly, Ross Taylor, Ruan Silva, Rui Hou, Rui Wang,
Tools and Algorithms for the Construction and Analy-          Saghar Hosseini, Sahana Chennabasappa, Sanjay Singh,
sis of Systems, TACAS’08/ETAPS’08, page 337–340,              Sean Bell, Seohyun Sonia Kim, Sergey Edunov, Shao-
Berlin, Heidelberg. Springer-Verlag.                          liang Nie, Sharan Narang, Sharath Raparthy, Sheng
                                                              Shen, Shengye Wan, Shruti Bhosale, Shun Zhang,
Francesco Fuggitti and Tathagata Chakraborti. 2023.           Simon Vandenhende, Soumya Batra, Spencer Whit-
Nl2ltl - a python package for converting natural lan-         man, Sten Sootla, Stephane Collot, Suchin Gururan-
guage (nl) instructions to linear temporal logic (ltl) for-   gan, Sydney Borodinsky, Tamar Herman, Tara Fowler,
mulas. In AAAI Conference on Artificial Intelligence.         Tarek Sheasha, Thomas Georgiou, Thomas Scialom, To-
Gaël Gendron, Qiming Bao, Michael Witbrock, and               bias Speckbacher, Todor Mihaylov, Tong Xiao, Ujjwal
Gillian Dobbie. 2024. Large language models are not           Karn, Vedanuj Goswami, Vibhor Gupta, Vignesh Ra-
strong abstract reasoners.                                    manathan, Viktor Kerkez, Vincent Gonguet, Virginie
                                                              Do, Vish Vogeti, Vítor Albiero, Vladan Petrovic, Wei-
Aaron Grattafiori, Abhimanyu Dubey, Abhinav Jauhri,           wei Chu, Wenhan Xiong, Wenyin Fu, Whitney Meers,
Xavier Martinet, Xiaodong Wang, Xiaofang Wang, Xi-          Nikolay Pavlovich Laptev, Ning Dong, Norman Cheng,
aoqing Ellen Tan, Xide Xia, Xinfeng Xie, Xuchao Jia,        Oleg Chernoguz, Olivia Hart, Omkar Salpekar, Ozlem
Xuewei Wang, Yaelle Goldschlag, Yashesh Gaur, Yas-          Kalinli, Parkin Kent, Parth Parekh, Paul Saab, Pavan
mine Babaei, Yi Wen, Yiwen Song, Yuchen Zhang, Yue          Balaji, Pedro Rittner, Philip Bontrager, Pierre Roux,
Li, Yuning Mao, Zacharie Delpierre Coudert, Zheng           Piotr Dollar, Polina Zvyagina, Prashant Ratanchan-
Yan, Zhengxing Chen, Zoe Papakipos, Aaditya Singh,          dani, Pritish Yuvraj, Qian Liang, Rachad Alao, Rachel
Aayushi Srivastava, Abha Jain, Adam Kelsey, Adam            Rodriguez, Rafi Ayub, Raghotham Murthy, Raghu
Shajnfeld, Adithya Gangidi, Adolfo Victoria, Ahuva          Nayani, Rahul Mitra, Rangaprabhu Parthasarathy, Ray-
Goldstand, Ajay Menon, Ajay Sharma, Alex Boesen-            mond Li, Rebekkah Hogan, Robin Battey, Rocky Wang,
berg, Alexei Baevski, Allie Feinstein, Amanda Kallet,       Russ Howes, Ruty Rinott, Sachin Mehta, Sachin Siby,
Amit Sangani, Amos Teo, Anam Yunus, Andrei Lupu,            Sai Jayesh Bondu, Samyak Datta, Sara Chugh, Sara
Andres Alvarado, Andrew Caples, Andrew Gu, Andrew           Hunt, Sargun Dhillon, Sasha Sidorov, Satadru Pan,
Ho, Andrew Poulton, Andrew Ryan, Ankit Ramchan-             Saurabh Mahajan, Saurabh Verma, Seiji Yamamoto,
dani, Annie Dong, Annie Franco, Anuj Goyal, Apara-          Sharadh Ramaswamy, Shaun Lindsay, Shaun Lind-
jita Saraf, Arkabandhu Chowdhury, Ashley Gabriel,           say, Sheng Feng, Shenghao Lin, Shengxin Cindy Zha,
Ashwin Bharambe, Assaf Eisenman, Azadeh Yazdan,             Shishir Patil, Shiva Shankar, Shuqiang Zhang, Shuqiang
Beau James, Ben Maurer, Benjamin Leonhardi, Bernie          Zhang, Sinong Wang, Sneha Agarwal, Soji Sajuyigbe,
Huang, Beth Loyd, Beto De Paola, Bhargavi Paranjape,        Soumith Chintala, Stephanie Max, Stephen Chen, Steve
Bing Liu, Bo Wu, Boyu Ni, Braden Hancock, Bram              Kehoe, Steve Satterfield, Sudarshan Govindaprasad,
Wasti, Brandon Spence, Brani Stojkovic, Brian Gamido,       Sumit Gupta, Summer Deng, Sungmin Cho, Sunny Virk,
Britt Montalvo, Carl Parker, Carly Burton, Catalina         Suraj Subramanian, Sy Choudhury, Sydney Goldman,
Mejia, Ce Liu, Changhan Wang, Changkyu Kim, Chao            Tal Remez, Tamar Glaser, Tamara Best, Thilo Koehler,
Zhou, Chester Hu, Ching-Hsiang Chu, Chris Cai, Chris        Thomas Robinson, Tianhe Li, Tianjun Zhang, Tim
Tindal, Christoph Feichtenhofer, Cynthia Gao, Damon         Matthews, Timothy Chou, Tzook Shaked, Varun Von-
Civin, Dana Beaty, Daniel Kreymer, Daniel Li, David         timitta, Victoria Ajayi, Victoria Montanez, Vijai Mohan,
Adkins, David Xu, Davide Testuggine, Delia David,           Vinay Satish Kumar, Vishal Mangla, Vlad Ionescu, Vlad
Devi Parikh, Diana Liskovich, Didem Foss, Dingkang          Poenaru, Vlad Tiberiu Mihailescu, Vladimir Ivanov,
Wang, Duc Le, Dustin Holland, Edward Dowling, Eissa         Wei Li, Wenchen Wang, Wenwen Jiang, Wes Bouaziz,
Jamil, Elaine Montgomery, Eleonora Presani, Emily           Will Constable, Xiaocheng Tang, Xiaojian Wu, Xiaolan
Hahn, Emily Wood, Eric-Tuan Le, Erik Brinkman,              Wang, Xilun Wu, Xinbo Gao, Yaniv Kleinman, Yanjun
Esteban Arcaute, Evan Dunbar, Evan Smothers, Fei            Chen, Ye Hu, Ye Jia, Ye Qi, Yenda Li, Yilin Zhang, Ying
Sun, Felix Kreuk, Feng Tian, Filippos Kokkinos, Firat       Zhang, Yossi Adi, Youngjin Nam, Yu, Wang, Yu Zhao,
Ozgenel, Francesco Caggioni, Frank Kanayet, Frank           Yuchen Hao, Yundi Qian, Yunlu Li, Yuzi He, Zach Rait,
Seide, Gabriela Medina Florez, Gabriella Schwarz,           Zachary DeVito, Zef Rosnbrick, Zhaoduo Wen, Zhenyu
Gada Badeer, Georgia Swee, Gil Halpern, Grant Her-          Yang, Zhiwei Zhao, and Zhiyu Ma. 2024. The llama 3
man, Grigory Sizov, Guangyi, Zhang, Guna Lakshmi-           herd of models.
narayanan, Hakan Inan, Hamid Shojanazeri, Han Zou,
Hannah Wang, Hanwen Zha, Haroun Habeeb, Harrison            Ivan Habernal, Henning Wachsmuth, Iryna Gurevych,
Rudolph, Helen Suk, Henry Aspegren, Hunter Gold-            and Benno Kiesel. 2018a. "dummy, grandpa, do you
man, Hongyuan Zhan, Ibrahim Damlaj, Igor Molybog,           know anything?": Identifying and characterizing ad
Igor Tufanov, Ilias Leontiadis, Irina-Elena Veliche, Itai   hominem fallacies in the wild. In Proceedings of the
Gat, Jake Weissman, James Geboski, James Kohli, Jan-        12th International AAAI Conference on Web and Social
ice Lam, Japhet Asher, Jean-Baptiste Gaya, Jeff Mar-        Media (ICWSM), pages 206–215.
cus, Jeff Tang, Jennifer Chan, Jenny Zhen, Jeremy
Reizenstein, Jeremy Teboul, Jessica Zhong, Jian Jin,        Ivan Habernal, Henning Wachsmuth, Iryna Gurevych,
Jingyi Yang, Joe Cummings, Jon Carvill, Jon Shep-           and Benno Stein. 2018b. Before name-calling: Dynam-
ard, Jonathan McPhie, Jonathan Torres, Josh Ginsburg,       ics and triggers of ad hominem fallacies in web argu-
Junjie Wang, Kai Wu, Kam Hou U, Karan Saxena, Kar-          mentation. In Proceedings of the 2018 Conference of
tikay Khandelwal, Katayoun Zand, Kathy Matosich,            the North American Chapter of the Association for Com-
Kaushik Veeraraghavan, Kelly Michelena, Keqian Li,          putational Linguistics: Human Language Technologies,
Kiran Jagadeesh, Kun Huang, Kunal Chawla, Kyle              Volume 1 (Long Papers), pages 386–396, New Orleans,
Huang, Lailin Chen, Lakshya Garg, Lavender A, Le-           Louisiana. Association for Computational Linguistics.
andro Silva, Lee Bell, Lei Zhang, Liangpeng Guo,            Christopher Hahn, Frederik Schmitt, Julia J. Tillman,
Licheng Yu, Liron Moshkovich, Luca Wehrstedt, Ma-           Niklas Metzger, Julian Siber, and Bernd Finkbeiner.
dian Khabsa, Manav Avalani, Manish Bhatt, Marty-            2022. Formal specifications from natural language.
nas Mankus, Matan Hasson, Matthew Lennie, Matthias
Reso, Maxim Groshev, Maxim Naumov, Maya Lathi,              Patrick M. Haluptzok, Matthew Bowers, and Adam Tau-
Meghan Keneally, Miao Liu, Michael L. Seltzer, Michal       man Kalai. 2022. Language modexrls can teach them-
Valko, Michelle Restrepo, Mihir Patel, Mik Vyatskov,        selves to program better. ArXiv, abs/2207.14502.
Mikayel Samvelyan, Mike Clark, Mike Macey, Mike
Wang, Miquel Jubert Hermoso, Mo Metanat, Moham-             Zhijing Jin, Abhinav Lalwani, Tejas Vaidhya, Xiaoyu
mad Rastegari, Munish Bansal, Nandhini Santhanam,           Shen, Yiwen Ding, Zhiheng Lyu, Mrinmaya Sachan,
Natascha Parks, Natasha White, Navyata Bawa, Nayan          Rada Mihalcea, and Bernhard Schoelkopf. 2022. Logi-
Singhal, Nick Egebo, Nicolas Usunier, Nikhil Mehta,         cal fallacy detection. In Findings of the Association for
Computational Linguistics: EMNLP 2022, pages 7180–         Chelsea Voss, Chen Ding, Cheng Lu, Chong Zhang,
7198, Abu Dhabi, United Arab Emirates. Association         Chris Beaumont, Chris Hallacy, Chris Koch, Chris-
for Computational Linguistics.                             tian Gibson, Christina Kim, Christine Choi, Chris-
                                                           tine McLeavey, Christopher Hesse, Claudia Fischer,
Mike Lewis, Yinhan Liu, Naman Goyal, Marjan                Clemens Winter, Coley Czarnecki, Colin Jarvis, Colin
Ghazvininejad, Abdelrahman Mohamed, Omer Levy,             Wei, Constantin Koumouzelis, Dane Sherburn, Daniel
Veselin Stoyanov, and Luke Zettlemoyer. 2020. BART:        Kappler, Daniel Levin, Daniel Levy, David Carr, David
Denoising sequence-to-sequence pre-training for natu-      Farhi, David Mely, David Robinson, David Sasaki,
ral language generation, translation, and comprehension.   Denny Jin, Dev Valladares, Dimitris Tsipras, Doug Li,
In Proceedings of the 58th Annual Meeting of the Associ-   Duc Phong Nguyen, Duncan Findlay, Edede Oiwoh,
ation for Computational Linguistics, pages 7871–7880,      Edmund Wong, Ehsan Asdar, Elizabeth Proehl, Eliz-
Online. Association for Computational Linguistics.         abeth Yang, Eric Antonow, Eric Kramer, Eric Peter-
Jason Xinyu Liu, Ziyi Yang, Benjamin Schornstein,          son, Eric Sigler, Eric Wallace, Eugene Brevdo, Evan
Sam Liang, Ifrah Idrees, Stefanie Tellex, and Ankit        Mays, Farzad Khorasani, Felipe Petroski Such, Fil-
Shah. 2022. Lang2LTL: Translating natural language         ippo Raso, Francis Zhang, Fred von Lohmann, Fred-
commands to temporal specification with large language     die Sulit, Gabriel Goh, Gene Oden, Geoff Salmon,
models. In CoRL Workshop on Language and Robot             Giulio Starace, Greg Brockman, Hadi Salman, Haiming
Learning.                                                  Bao, Haitang Hu, Hannah Wong, Haoyu Wang, Heather
                                                           Schmidt, Heather Whitney, Heewoo Jun, Hendrik Kirch-
B. MacCartney and C. D. Manning. 2014. Natural logic       ner, Henrique Ponde de Oliveira Pinto, Hongyu Ren,
and natural language inference. In H. Bunt, J. Bos,        Huiwen Chang, Hyung Won Chung, Ian Kivlichan,
and S. Pulman, editors, Computing Meaning: Volume 4,       Ian O’Connell, Ian O’Connell, Ian Osband, Ian Silber,
pages 129–147. Springer Netherlands, Dordrecht.            Ian Sohl, Ibrahim Okuyucu, Ikai Lan, Ilya Kostrikov,
                                                           Ilya Sutskever, Ingmar Kanitscheider, Ishaan Gulrajani,
Callistus Ireneous Nakpih and Simone Santini. 2020.        Jacob Coxon, Jacob Menick, Jakub Pachocki, James
Automated discovery of logical fallacies in legal argu-    Aung, James Betker, James Crooks, James Lennon,
mentation. International Journal of Artificial Intelli-    Jamie Kiros, Jan Leike, Jane Park, Jason Kwon, Ja-
gence & Applications.                                      son Phang, Jason Teplitz, Jason Wei, Jason Wolfe, Jay
                                                           Chen, Jeff Harris, Jenia Varavva, Jessica Gan Lee, Jes-
Theo Olausson, Alex Gu, Ben Lipkin, Cedegao Zhang,         sica Shieh, Ji Lin, Jiahui Yu, Jiayi Weng, Jie Tang,
Armando Solar-Lezama, Joshua Tenenbaum, and Roger          Jieqi Yu, Joanne Jang, Joaquin Quinonero Candela,
Levy. 2023. LINC: A neurosymbolic approach for logi-       Joe Beutler, Joe Landers, Joel Parish, Johannes Hei-
cal reasoning by combining language models with first-     decke, John Schulman, Jonathan Lachman, Jonathan
order logic provers. In Proceedings of the 2023 Con-       McKay, Jonathan Uesato, Jonathan Ward, Jong Wook
ference on Empirical Methods in Natural Language           Kim, Joost Huizinga, Jordan Sitkin, Jos Kraaijeveld,
Processing, pages 5153–5176, Singapore. Association        Josh Gross, Josh Kaplan, Josh Snyder, Joshua Achiam,
for Computational Linguistics.                             Joy Jiao, Joyce Lee, Juntang Zhuang, Justyn Harri-
OpenAI. 2024. Gpt-4o mini: Advancing cost-efficient        man, Kai Fricke, Kai Hayashi, Karan Singhal, Katy Shi,
intelligence. Accessed: 2025-02-15.                        Kavin Karthik, Kayla Wood, Kendra Rimbach, Kenny
                                                           Hsu, Kenny Nguyen, Keren Gu-Lemberg, Kevin But-
OpenAI, Aaron Hurst, Adam Lerer, Adam P. Goucher,          ton, Kevin Liu, Kiel Howe, Krithika Muthukumar, Kyle
Adam Perelman, Aditya Ramesh, Aidan Clark, AJ Os-          Luther, Lama Ahmad, Larry Kai, Lauren Itow, Lau-
trow, Akila Welihinda, Alan Hayes, Alec Radford, Alek-     ren Workman, Leher Pathak, Leo Chen, Li Jing, Lia
sander Madry,
           ˛    Alex Baker-Whitcomb, Alex Beutel,          Guy, Liam Fedus, Liang Zhou, Lien Mamitsuka, Lilian
Alex Borzunov, Alex Carney, Alex Chow, Alex Kirillov,      Weng, Lindsay McCallum, Lindsey Held, Long Ouyang,
Alex Nichol, Alex Paino, Alex Renzin, Alex Tachard         Louis Feuvrier, Lu Zhang, Lukas Kondraciuk, Lukasz
Passos, Alexander Kirillov, Alexi Christakis, Alexis       Kaiser, Luke Hewitt, Luke Metz, Lyric Doshi, Mada
Conneau, Ali Kamali, Allan Jabri, Allison Moyer, Alli-     Aflak, Maddie Simens, Madelaine Boyd, Madeleine
son Tam, Amadou Crookes, Amin Tootoochian, Amin            Thompson, Marat Dukhan, Mark Chen, Mark Gray,
Tootoonchian, Ananya Kumar, Andrea Vallone, Andrej         Mark Hudnall, Marvin Zhang, Marwan Aljubeh, Ma-
Karpathy, Andrew Braunstein, Andrew Cann, Andrew           teusz Litwin, Matthew Zeng, Max Johnson, Maya
Codispoti, Andrew Galu, Andrew Kondrich, Andrew            Shetty, Mayank Gupta, Meghan Shah, Mehmet Yatbaz,
Tulloch, Andrey Mishchenko, Angela Baek, Angela            Meng Jia Yang, Mengchao Zhong, Mia Glaese, Mianna
Jiang, Antoine Pelisse, Antonia Woodford, Anuj Gos-        Chen, Michael Janner, Michael Lampe, Michael Petrov,
alia, Arka Dhar, Ashley Pantuliano, Avi Nayak, Avi-        Michael Wu, Michele Wang, Michelle Fradin, Michelle
tal Oliver, Barret Zoph, Behrooz Ghorbani, Ben Le-         Pokrass, Miguel Castro, Miguel Oom Temudo de Cas-
imberger, Ben Rossen, Ben Sokolowsky, Ben Wang,            tro, Mikhail Pavlov, Miles Brundage, Miles Wang, Mi-
Benjamin Zweig, Beth Hoover, Blake Samic, Bob Mc-          nal Khan, Mira Murati, Mo Bavarian, Molly Lin, Mu-
Grew, Bobby Spero, Bogo Giertler, Bowen Cheng,             rat Yesildal, Nacho Soto, Natalia Gimelshein, Natalie
Brad Lightcap, Brandon Walkin, Brendan Quinn, Brian        Cone, Natalie Staudacher, Natalie Summers, Natan La-
Guarraci, Brian Hsu, Bright Kellogg, Brydon Eastman,       Fontaine, Neil Chowdhury, Nick Ryder, Nick Stathas,
Camillo Lugaresi, Carroll Wainwright, Cary Bassin,         Nick Turley, Nik Tezak, Niko Felix, Nithanth Kudige,
Cary Hudson, Casey Chu, Chad Nelson, Chak Li,              Nitish Keskar, Noah Deutsch, Noel Bundick, Nora
Chan Jun Shern, Channing Conger, Charlotte Barette,        Puckett, Ofir Nachum, Ola Okelola, Oleg Boiko, Oleg
Murk, Oliver Jaffe, Olivia Watkins, Olivier Godement,        chocki, James Lennon, Jason Wei, Jean Harb, Jerry
Owen Campbell-Moore, Patrick Chao, Paul McMillan,            Twore, Jiacheng Feng, Jiahui Yu, Jiayi Weng, Jie Tang,
Pavel Belov, Peng Su, Peter Bak, Peter Bakkum, Pe-           Jieqi Yu, Joaquin Quiñonero Candela, Joe Palermo,
ter Deng, Peter Dolan, Peter Hoeschele, Peter Welin-         Joel Parish, Johannes Heidecke, John Hallman, John
der, Phil Tillet, Philip Pronin, Philippe Tillet, Prafulla   Rizzo, Jonathan Gordon, Jonathan Uesato, Jonathan
Dhariwal, Qiming Yuan, Rachel Dias, Rachel Lim,              Ward, Joost Huizinga, Julie Wang, Kai Chen, Kai Xiao,
Rahul Arora, Rajan Troll, Randall Lin, Rapha Gontijo         Karan Singhal, Karina Nguyen, Karl Cobbe, Katy Shi,
Lopes, Raul Puri, Reah Miyara, Reimar Leike, Renaud          Kayla Wood, Kendra Rimbach, Keren Gu-Lemberg,
Gaubert, Reza Zamani, Ricky Wang, Rob Donnelly, Rob          Kevin Liu, Kevin Lu, Kevin Stone, Kevin Yu, Lama
Honsby, Rocky Smith, Rohan Sahai, Rohit Ramchan-             Ahmad, Lauren Yang, Leo Liu, Leon Maksin, Ley-
dani, Romain Huet, Rory Carmichael, Rowan Zellers,           ton Ho, Liam Fedus, Lilian Weng, Linden Li, Lindsay
Roy Chen, Ruby Chen, Ruslan Nigmatullin, Ryan Cheu,          McCallum, Lindsey Held, Lorenz Kuhn, Lukas Kon-
Saachi Jain, Sam Altman, Sam Schoenholz, Sam Toizer,         draciuk, Lukasz Kaiser, Luke Metz, Madelaine Boyd,
Samuel Miserendino, Sandhini Agarwal, Sara Culver,           Maja Trebacz, Manas Joglekar, Mark Chen, Marko
Scott Ethersmith, Scott Gray, Sean Grove, Sean Metzger,      Tintor, Mason Meyer, Matt Jones, Matt Kaufer, Max
Shamez Hermani, Shantanu Jain, Shengjia Zhao, Sher-          Schwarzer, Meghan Shah, Mehmet Yatbaz, Melody Y.
win Wu, Shino Jomoto, Shirong Wu, Shuaiqi, Xia, Sonia        Guan, Mengyuan Xu, Mengyuan Yan, Mia Glaese, Mi-
Phene, Spencer Papay, Srinivas Narayanan, Steve Cof-         anna Chen, Michael Lampe, Michael Malek, Michele
fey, Steve Lee, Stewart Hall, Suchir Balaji, Tal Broda,      Wang, Michelle Fradin, Mike McClay, Mikhail Pavlov,
Tal Stramer, Tao Xu, Tarun Gogineni, Taya Chris-             Miles Wang, Mingxuan Wang, Mira Murati, Mo Bavar-
tianson, Ted Sanders, Tejal Patwardhan, Thomas Cun-          ian, Mostafa Rohaninejad, Nat McAleese, Neil Chowd-
ninghman, Thomas Degry, Thomas Dimson, Thomas                hury, Neil Chowdhury, Nick Ryder, Nikolas Tezak,
Raoux, Thomas Shadwell, Tianhao Zheng, Todd Un-              Noam Brown, Ofir Nachum, Oleg Boiko, Oleg Murk,
derwood, Todor Markov, Toki Sherbakov, Tom Rubin,            Olivia Watkins, Patrick Chao, Paul Ashbourne, Pavel Iz-
Tom Stasi, Tomer Kaftan, Tristan Heywood, Troy Pe-           mailov, Peter Zhokhov, Rachel Dias, Rahul Arora, Ran-
terson, Tyce Walters, Tyna Eloundou, Valerie Qi, Veit        dall Lin, Rapha Gontijo Lopes, Raz Gaon, Reah Miyara,
Moeller, Vinnie Monaco, Vishal Kuo, Vlad Fomenko,            Reimar Leike, Renny Hwang, Rhythm Garg, Robin
Wayne Chang, Weiyi Zheng, Wenda Zhou, Wesam Man-             Brown, Roshan James, Rui Shu, Ryan Cheu, Ryan
assra, Will Sheu, Wojciech Zaremba, Yash Patil, Yilei        Greene, Saachi Jain, Sam Altman, Sam Toizer, Sam
Qian, Yongjik Kim, Youlong Cheng, Yu Zhang, Yuchen           Toyer, Samuel Miserendino, Sandhini Agarwal, Santi-
He, Yuchen Zhang, Yujia Jin, Yunxing Dai, and Yury           ago Hernandez, Sasha Baker, Scott McKinney, Scottie
Malkov. 2024a. Gpt-4o system card.                           Yan, Shengjia Zhao, Shengli Hu, Shibani Santurkar,
                                                             Shraman Ray Chaudhuri, Shuyuan Zhang, Siyuan Fu,
OpenAI, Aaron Jaech, Adam Kalai, Adam Lerer, Adam            Spencer Papay, Steph Lin, Suchir Balaji, Suvansh San-
Richardson, Ahmed El-Kishky, Aiden Low, Alec Hel-            jeev, Szymon Sidor, Tal Broda, Aidan Clark, Tao Wang,
yar, Aleksander Madry, Alex Beutel, Alex Carney, Alex        Taylor Gordon, Ted Sanders, Tejal Patwardhan, Thibault
Iftimie, Alex Karpenko, Alex Tachard Passos, Alexan-         Sottiaux, Thomas Degry, Thomas Dimson, Tianhao
der Neitz, Alexander Prokofiev, Alexander Wei, Alli-         Zheng, Timur Garipov, Tom Stasi, Trapit Bansal, Trevor
son Tam, Ally Bennett, Ananya Kumar, Andre Saraiva,          Creech, Troy Peterson, Tyna Eloundou, Valerie Qi, Vi-
Andrea Vallone, Andrew Duberstein, Andrew Kon-               neet Kosaraju, Vinnie Monaco, Vitchyr Pong, Vlad
drich, Andrey Mishchenko, Andy Applebaum, An-                Fomenko, Weiyi Zheng, Wenda Zhou, Wes McCabe,
gela Jiang, Ashvin Nair, Barret Zoph, Behrooz Ghor-          Wojciech Zaremba, Yann Dubois, Yinghai Lu, Yining
bani, Ben Rossen, Benjamin Sokolowsky, Boaz Barak,           Chen, Young Cha, Yu Bai, Yuchen He, Yuchen Zhang,
Bob McGrew, Borys Minaiev, Botao Hao, Bowen                  Yunyun Wang, Zheng Shao, and Zhuohan Li. 2024b.
Baker, Brandon Houghton, Brandon McKinzie, Brydon            Openai o1 system card.
Eastman, Camillo Lugaresi, Cary Bassin, Cary Hud-
son, Chak Ming Li, Charles de Bourcy, Chelsea Voss,          Liangming Pan, Alon Albalak, Xinyi Wang, and
Chen Shen, Chong Zhang, Chris Koch, Chris Orsinger,          William Wang. 2023. Logic-LM: Empowering large lan-
Christopher Hesse, Claudia Fischer, Clive Chan, Dan          guage models with symbolic solvers for faithful logical
Roberts, Daniel Kappler, Daniel Levy, Daniel Sel-            reasoning. In Findings of the Association for Compu-
sam, David Dohan, David Farhi, David Mely, David             tational Linguistics: EMNLP 2023, pages 3806–3824,
Robinson, Dimitris Tsipras, Doug Li, Dragos Oprica,          Singapore. Association for Computational Linguistics.
Eben Freeman, Eddie Zhang, Edmund Wong, Elizabeth            William C Purdy. 1991. A logic for natural language.
Proehl, Enoch Cheung, Eric Mitchell, Eric Wallace, Erik      Notre Dame Journal of Formal Logic, 32(3):409–425.
Ritter, Evan Mays, Fan Wang, Felipe Petroski Such,
Filippo Raso, Florencia Leoni, Foivos Tsimpourlas,           Hrituraj Singh, Milan Aggarwal, and Balaji Krish-
Francis Song, Fred von Lohmann, Freddie Sulit, Ge-           namurthy. 2020. Exploring neural models for pars-
off Salmon, Giambattista Parascandolo, Gildas Chabot,        ing natural language into first-order logic. ArXiv,
Grace Zhao, Greg Brockman, Guillaume Leclerc, Hadi           abs/2002.06544.
Salman, Haiming Bao, Hao Sheng, Hart Andrin, Hes-
sam Bagherinezhad, Hongyu Ren, Hunter Lightman,              Zhivar Sourati, Vishnu Priya Prasanna Venkatesh, Dar-
Hyung Won Chung, Ian Kivlichan, Ian O’Connell, Ian           shan Deshpande, Himanshu Rawlani, Filip Ilievski,
Osband, Ignasi Clavera Gilaberte, Ilge Akkaya, Ilya          Hông-Ân Sandlin, and Alain Mermoud. 2022. Robust
Kostrikov, Ilya Sutskever, Irina Kofman, Jakub Pa-           and explainable identification of logical fallacies in nat-
ural language arguments. Knowledge Based Systems,
266:110418.
Christian Stab and Iryna Gurevych. 2017. Recogniz-
ing insufficiently supported arguments in argumentative
essays. In Proceedings of the 15th Conference of the
European Chapter of the Association for Computational
Linguistics: Volume 1, Long Papers, pages 980–990,
Valencia, Spain. Association for Computational Lin-
guistics.
Hugo Touvron, Louis Martin, Kevin Stone, Peter Al-
bert, Amjad Almahairi, Yasmine Babaei, Nikolay Bash-
lykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhos-
ale, Dan Bikel, Lukas Blecher, Cristian Canton Fer-
rer, Moya Chen, Guillem Cucurull, David Esiobu, Jude
Fernandes, Jeremy Fu, Wenyin Fu, Brian Fuller, Cyn-
thia Gao, Vedanuj Goswami, Naman Goyal, Anthony
Hartshorn, Saghar Hosseini, Rui Hou, Hakan Inan,
Marcin Kardas, Viktor Kerkez, Madian Khabsa, Is-
abel Kloumann, Artem Korenev, Punit Singh Koura,
Marie-Anne Lachaux, Thibaut Lavril, Jenya Lee, Di-
ana Liskovich, Yinghai Lu, Yuning Mao, Xavier Mar-
tinet, Todor Mihaylov, Pushkar Mishra, Igor Moly-
bog, Yixin Nie, Andrew Poulton, Jeremy Reizenstein,
Rashi Rungta, Kalyan Saladi, Alan Schelten, Ruan
Silva, Eric Michael Smith, Ranjan Subramanian, Xiao-
qing Ellen Tan, Binh Tang, Ross Taylor, Adina Williams,
Jian Xiang Kuan, Puxin Xu, Zheng Yan, Iliyan Zarov,
Yuchen Zhang, Angela Fan, Melanie Kambadur, Sharan
Narang, Aurelien Rodriguez, Robert Stojnic, Sergey
Edunov, and Thomas Scialom. 2023. Llama 2: Open
foundation and fine-tuned chat models.
Jason Wei, Xuezhi Wang, Dale Schuurmans, et al. 2022.
Chain of thought prompting elicits reasoning in large
language models. Advances in Neural Information Pro-
cessing Systems.
Adina Williams, Nikita Nangia, and Samuel Bowman.
2018. A broad-coverage challenge corpus for sentence
understanding through inference. In Proceedings of
the 2018 Conference of the North American Chapter of
the Association for Computational Linguistics: Human
Language Technologies, Volume 1 (Long Papers), pages
1112–1122, New Orleans, Louisiana. Association for
Computational Linguistics.
Yuan Yang, Siheng Xiong, Ali Payani, Ehsan Shareghi,
and Faramarz Fekri. 2024. Harnessing the power of
large language models for natural language to first-
order logic translation. In Proceedings of the 62nd
Annual Meeting of the Association for Computational
Linguistics (Volume 1: Long Papers), pages 6942–6959,
Bangkok, Thailand. Association for Computational Lin-
guistics.
     Appendix                                                   Algorithm 2: UnifySort for Predicate A(x, y)
     A      Algorithms                                          Input: Predicate A(x, y) with arguments and potential
                                                                       instances
                                                                Output: Unified sort for predicate A or an error if sorts
     Algorithm 1: Compiling Logical Formula to                           are incompatible
     SMT                                                   1    Step 1: Declare the Current Sort Initialize the current
     Input: Logical formula L in natural language or             sort of A: (NULL, NULL, Bool)
            First-Order Logic (FOL)
                                                           2    Step 2: Process Each Instance of Predicate A foreach
     Output: SMT file S formatted for formal solvers
                                                                 instance of predicate A do
 1   Step 1: Tokenize Formula                              3        Step 2.1: Determine Instance Sorts foreach
 2   T ← Tokenize(L) // Split L into tokens based                    argument xi in the instance do
        on operators, parentheses, and commas              4            if xi is a formula then
 3 Step 2: Process Tokens                                   5                Set sort(xi ) = Bool
 4 P ← ∅ // Initialize processed tokens set
                                                            6           else if xi is a variable then
 5 foreach token t ∈ T do
                                                            7                Set sort(xi ) = sort(variable) // May be
 6     if t is a predicate then                                                   NULL
 7           Identify arguments of t
                                                           8        Step 2.2: Unify Current Sort with Instance Sort
 8           Recursively ProcessTokens() for arguments
                                                                     foreach statement sort in current and instance
 9     else if t is an operator or variable then                     sorts do
10           Add t to P                                    9            if sorts are not NULL and different then
11 Step 3: Convert Formula to Prefix Notation              10                Raise an error: Incompatible sorts
12 Fprefix ← InfixToPrefix(P) // Transform logical         11           else if current sort is NULL and instance sort is
       formula from infix to prefix notation                              not NULL then
13 Recursively apply InfixToPrefix() for predicate
                                                           12                Update current sort:
    arguments                                                                  current_sort ← instance_sort
                                                           13           else if instance sort is NULL and current sort is
14 Step 4: Determine Sorts                                                not NULL then
15 Ssorts ← UnifySort(Fprefix ) // Assign sorts for        14                Update variable sort to match current sort
       variables and predicates
16   Step 5: Format Formula for SMT
17   FSMT ← Parenthesize Fprefix according to SMT-LIB
      syntax
18 Step 6: Generate SMT File
19 S ← GenerateSMT(Ssorts , FSMT )
20 Include
       • (declare-sort) statements for sorts.
       • (declare-fun) statements for variables and
         predicates.
       • Negation of FSMT .
       • (check-sat) and (get-model) commands.
     return S // Return the SMT file for use in
         formal solvers
                                                                    Here are some examples of classifying sen-
                                                                    tences as logical fallacies or valid sentences:
     B     Prompt Examples
     Note: Additional in-context examples were re-                  Example 1:
     moved for brevity and denoted ‘[...]’ in the fol-
     lowing prompts.                                                Input: "I met a tall man who loved to eat
                                                                    cheese, now I believe all tall people like
     B.1     End-to-end LLM Prompts                                 cheese"
           Prompt 1. Classifying with in-context ex-                Answer: Logical Fallacy
           amples (Few-shot)
                                                                    [...]
           Logical fallacies are common errors in
           reasoning that undermine the logic of an                 Now, classify the following sentence.
           argument.                                                Answer with either "Logical Fallacy" or
                                                                    "Valid" at the start of your answer.
         A sentence is logically valid if and only if it
         is not possible for it to be false.                        Input:
B.2      Intermediate NL2FOL Prompts
                                                    2. "[Entity A]" is a subset of "[Entity B]".
      Prompt 2. Extracting claim and implication    3. "[Entity B]" is a subset of "[Entity A]".
                                                    4. "[Entity A]" is not related to "[Entity B]".
      Here are some examples of extracting
      claims and implications from an input          Instructions:
      paragraph. There can be multiple claims       - Equality check: If the two entities are equal
      but only one implication.                     (case-insensitive after stripping whitespace),
                                                     select statement 1.
      Input: "I met a tall man who loved to eat     - Subset determination: If they are not equal,
      cheese, now I believe all tall people like     assess whether one entity is a subset of the
      cheese."                                       other based on general knowledge and logi-
      Output:                                        cal reasoning.
      Claim: "A tall man loves cheese."                    - If "[Entity A]" is a subset of "[Entity
      Implication: "All tall people like cheese."          B]", select statement 2.
                                                           - If "[Entity B]" is a subset of "[Entity
      [...]                                                A]", select statement 3.
                                                    - Unrelated entities: If none of the above
      Do not use any subordinating conjunctions      statements accurately describes the relation-
      in the implication. Replace pronouns with      ship.
      the appropriate nouns so that there are
      no pronouns. Now extract the claim and        Here are some examples:
      implication for the following input.
                                                    Example 1:
      Input:
                                                    Entity A: "dogs"
      Prompt 3. Getting referring expressions       Entity B: "animals"
                                                    Analysis: All dogs are animals, so "dogs"
  You are given a sentence. Referring               is a subset of "animals".
  expressions are noun phrases, pronouns,           Answer: 2
  and proper names that refer to some
  individual objects that have some properties      [...]
  associated with them. Here are some
  examples of finding referring expressions         Entities:
  in a sentence:                                    - Entity A:
                                                    - Entity B:
      Input: "A tall man loved cheese"
      Referring expressions: A tall man             Your Task:
                                                    - Analyze the relationship between "Entity
      [...]                                         A" and "Entity B" based on the instructions.
                                                    - Provide only the number (1, 2, 3, or 4)
      Now, find the referring expressions for the   that corresponds to the statement you have
      following input:                              selected.

      Prompt 4. Getting entity relations
                                                    Prompt 5. Getting properties (claim)
      Please determine the relationship between
      the two entities provided below. Choose the   Given a sentence, and the referring
      number corresponding to the statement that    expressions of that sentence. Properties
      best describes their relationship:            are anything that describes a relationship
                                                    between two referring expressions, or
  1. "[Entity A]" is equal to "[Entity B]".         they may describe a trait of a referring
expression. These properties are essentially       sentence into a first-order logical form. Use
predicates in first-order logic.                  -> to represent implies, & to represent and, |
                                                   to represent or and to represent negations.
Here are some examples of finding proper-
ties in a sentence:                               Example 1:

Example 1:                                        Input Sentence: A tall man loves cheese
                                                  Referring Expressions: A tall man: x
Input sentence: A tall man loves cheese           Properties: IsTall(x), LovesCheese(x)
Referring expressions: tall man: a, cheese:       Logical Form: IsTall(x) & LovesCheese(x)
b
Properties: IsTall(x), LovesCheese(x)             [...]

[...]                                          The complete set of prompt examples is available
                                               in our public code repository at https://github.
Now extract the properties for the following   com/lovishchopra/NL2FOL. We encourage read-
input:                                         ers to visit the repository for details and latest up-
                                               dates.

Prompt 6. Getting property relations

You are given two logical clauses. Your
task is to identify whether or not the
first clause entails the second clause,
taking into account external knowl-
edge or ’common sense’. Also, take into
account the context from the input sentence.

Here are some examples:

Example 1:

Input sentence: A boy is jumping on skate-
board in the middle of a red bridge. Thus,
the boy does a skateboarding trick.
Clause 1: JumpsOn(boy,skateboard)
Clause 2: Does(boy, skateboarding_trick)
Answer: ENTAILMENT

[...]

Now given the following clauses. identify
whether the first clause entails the second
clause.


Prompt 7. Retrieving FOL expression

Given a sentence, the referring expressions
of that sentence, and properties which are
associated with the referring expressions.
Use the given properties to convert the
