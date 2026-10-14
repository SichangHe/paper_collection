                                             Improving Symbolic Translation of Language Models for Logical Reasoning
                                                       Ramya Keerthy Thatikonda1 , Jiuzhou Han1 , Wray Buntine2 , Ehsan Shareghi1
                                                                                  1
                                                                                   Department of Data Science & AI, Monash University
                                                                            2
                                                                                College of Engineering and Computer Science, VinUniversity
                                                                                             ramya.thatikonda1@monash.edu




                                                                    Abstract                                   These scenarios require consistent NL-to-FOL translations
arXiv:2601.09446v1 [cs.CL] 14 Jan 2026




                                           The use of formal language for deductive logical reasoning          across statements (e.g., in predicate naming or the transla-
                                           aligns well with language models (LMs), where translating           tion of logical operators). Existing approaches to reducing
                                           natural language (NL) into first-order logic (FOL) and em-          NL-to-FOL translation errors rely on the LM’s ability to un-
                                           ploying an external solver results in a verifiable and there-       derstand and self-correct the translation inaccuracies based
                                           fore reliable reasoning system. However, smaller LMs often          solely on the error message from an external SMT solver
                                           struggle with this translation task, frequently producing in-       (Pan et al. 2023). However, both interpreting solver feed-
                                           correct symbolic outputs due to formatting and translation er-      back and generating accurate symbolic representations are
                                           rors. Existing approaches typically rely on self-iteration to       capabilities more strongly associated with larger models. In
                                           correct these errors, but such methods depend heavily on            contrast, smaller, more accessible language models — de-
                                           the capabilities of the underlying model. To address this, we
                                                                                                               spite their advantages in cost and accessibility for research
                                           first categorize common errors and fine-tune smaller LMs us-
                                           ing data synthesized by large language models. The evalua-          — continue to face significant challenges in these tasks.
                                           tion is performed using the defined error categories. We in-           A key barrier to improving smaller LMs is the scarcity of
                                           troduce incremental inference, which divides inference into         symbolic data. To bridge this gap, we synthesize additional
                                           two stages, predicate generation and FOL translation, pro-          data for the ProofWriter (Tafjord, Dalvi, and Clark 2021)
                                           viding greater control over model behavior and enhancing            dataset using a large LM, followed by a multi-stage filter-
                                           generation quality as measured by predicate metrics. This de-       ing pipeline that includes format correction, syntax valida-
                                           composition framework also enables the use of a verification        tion, and semantic filtering to ensure high translation quality.
                                           module that targets predicate-arity errors to further improve       This synthesized data, combined with the limited existing
                                           performance. Our study evaluates three families of models
                                           across four logical-reasoning datasets. The comprehensive
                                                                                                               symbolic dataset (Han et al. 2024), helps establish a base-
                                           fine-tuning, incremental inference, and verification modules        line with fewer NL-to-FOL errors (as categorized in our tax-
                                           reduce error rates, increase predicate coverage, and improve        onomy) and enables the study of additional frameworks for
                                           reasoning performance for smaller LMs, moving us closer to          smaller LMs.
                                           developing reliable and accessible symbolic-reasoning sys-             Our fine-tuned models are evaluated under a standard in-
                                           tems.                                                               ference setting in which the model is prompted to first gen-
                                                                                                               erate a list of predicates and then the FOL translations. This
                                         Code — https://github.com/RamyaKeerthy/ProofFOL.git                   design enforces predicate consistency across statements, a
                                                                                                               requirement for semantic correctness (Pan et al. 2023). How-
                                                              1    Introduction                                ever, under next-token prediction, a single token-level error
                                         The tool-augmented paradigm in logical reasoning tasks                can cascade throughout the remainder of the generation. As
                                         with language models (LMs) is to translate statements from            shown in Figure 1, the inference is stuck in repetitive loops
                                         natural language (NL) to predicate first-order logic (FOL).           of generating “IsFavorite(x, y)” (Holtzman et al. 2020). To
                                         These translations are then sent for execution to exter-              mitigate this, we introduce incremental inference, in which
                                         nal solvers such as Z3 (De Moura and Bjørner 2008) and                the model first outputs only the set of predicates and then, in
                                         Prover9 (McCune 2005), where the tool returns ‘True’,                 a separate step, generates the full FOL statements. This de-
                                         ‘False’, ‘Uncertain/Unknown’ as final output (Ye et al. 2023;         composition allows the model to focus on a single subtask
                                         Pan et al. 2023; Olausson et al. 2023). Beyond logical rea-           at a time, enables early stopping, and ensures well-formatted
                                         soning, autoformalisation methods (Yang et al. 2024a; Wu              outputs. While the incremental mode reduces formatting er-
                                         et al. 2022) follow a similar symbolic translation pipeline.          rors, it may still introduce other syntactic issues. The two-
                                            Yang et al. (2024b) highlight systematic errors that even          stage design therefore facilitates the integration of a plug-
                                         the most advanced LLMs make when translating a single                 and-play verifier module, allowing a lightweight LM to cor-
                                         NL statement into its corresponding FOL. Realistic logical-           rect predicate-arity errors and further improve translation ro-
                                         reasoning tasks are substantially more challenging, involv-           bustness.
                                         ing multiple premise statements followed by a conclusion.                We analyze syntactic errors using our error taxonomy, and
Figure 1: Framework used to improve symbolic translations. Standard inference can still exhibit formatting errors like repetitive
loops. Incremental inference mitigates these by stopping predicate generation early and dividing the process into two stages. A
verifier helps address arity error with a predicate “HaveLongVacation” come with arity of 0 and 1 introduced during incremental
predicate generation.


we study semantic issues, those that external tools cannot         to building a complete translation system capable of han-
detect, using two predicate-level metrics: coverage and us-        dling multi-statement inputs using accessible and inexpen-
age. These metrics quantify the alignment between the pre-         sive small LMs, accompanied by a systematic analysis of
dicted predicate set and the predicates appearing in the final     translation errors.
FOL statements. Our experiments show that incremental in-
ference substantially improves predicate coverage relative to      Logical Reasoning Logical reasoning is a critical capa-
standard inference.                                                bility for evaluating the inference performance of large lan-
                                                                   guage models, encompassing three major types: deductive,
                    2   Related Work                               inductive, and abductive reasoning (Xu et al. 2025; Liu et al.
                                                                   2025). Our work focuses specifically on deductive reason-
LMs for Symbolic Translation. Formal language trans-               ing, which requires deriving a logically valid conclusion
lations by large language models (LLMs) was initially at-          from a given set of premises. Several datasets support re-
tempted by Nye et al. (2021), with an intent to emphasize          search in this area, including FOLIO (Han et al. 2024),
the importance of dual-process theory for logical reasoning        ProofWriter (Tafjord, Dalvi, and Clark 2021), ProntoQA
tasks. Subsequent work shifted the reasoning burden to the-        (Saparov and He 2023), ProverQA (Qi et al. 2025a), and
orem provers, with LLMs generating logic programs for de-          JustLogic (Chen, Zhang, and Tao 2025). Among these, FO-
ductive reasoning (Matthew Lam, Thatikonda, and Shareghi           LIO is notable for providing complete symbolic translations
2024; Pan et al. 2023; Ye et al. 2023; Olausson et al. 2023)       with human-annotated FOL sentences, but its utility is lim-
and inference tasks (Liu et al. 2024; Tarau 2024). Research        ited by its relatively small size. As smaller models often
in this direction primarily differs in the choice of formal lan-   struggle to produce meaningful outputs on complex reason-
guage (influenced by the underlying theorem prover) and in         ing tasks, we use both existing symbolic datasets and syn-
the verification or correction mechanisms used to address          thetically generated data to supervise-finetune these models
translation errors. Other methods (Xu et al. 2024a) focus          and instill the desired behavior (Taori et al. 2023; Ouyang
on adapting symbolic structures within reasoning paradigms         et al. 2022).
such as chain-of-thought (Wei et al. 2022), improving rea-
soning fidelity without employing external provers. How-           Knowledge Distillation Leveraging data generated by
ever, these approaches often rely on large, expensive, and         larger, more capable models to train smaller models has been
proprietary models, limiting the deployment of symbolic            widely studied. Early work in this direction focuses on syn-
frameworks in safety-critical or resource-constrained set-         thetic data generation, where outputs from capable models
tings.                                                             are used to train instruction-following models (Taori et al.
   Complementary to work in formal logic, Yang et al.              2023; Wang et al. 2023). With the growing performance
(2024b) applied supervised fine-tuning to LLaMA to im-             gap between large proprietary models and open-source al-
prove natural-language to first-order-logic translations at the    ternatives, knowledge distillation has gained popularity as
sentence level. In contrast, our research shifts the focus         a means of transferring capabilities from larger models to
            Type                  Example
            Missing Quantifier    BerkeleyCollege(x) ∧ResidentialCollegeAt(x, yaleUniversity)
Parsing



            Parenthesis error     BeneficialTo(cherry, people) ⊕On(cherry, warningList)) → ¬RedFruit(cherry)
            Completion error      ∀x(Athlete(x) →¬NeverExercises(x)) Never: does not exist a time

            Quantifier location   ∃y(Own(emily, y) ∧Roommate(y)) → ∃y(Own(emily, y) ∧LiveIn(emily, apartment))
Type




            Missing variable      ∀x∃y(In(indonesia) ∧ Prosecutor(x) ∧ SpecialCrime(y) → InvestigatePersonally(x, y))
Token




            Special token         Endowment(yale, 42.3 billion)
            Unknown Operator      ∀x(Rating(x, y) ∧ y>4→ Listed(x))
Predicate




            Arity Mismatch        Sees(Tiger, Mouse); ∀x(((Visits(x, Rabbit)) ∧ (Sees(Mouse))) → (Visits(x, Tiger)))
            Subject-Predicate     Platypus(platypus) ∧¬Teeth(platypus) ∧Mammal(platypus)
            Conflict

Table 1: Syntax Errors in First-Order Logic translations. This table categorizes errors by their cause, with the underlined text
highlighting the specific cause or location of each error.


more accessible ones (Xu et al. 2024b). Other studies dis-          in syntactic errors, which we discuss in detail in this section.
till rationales from large language models and fine-tune
smaller models to enhance their reasoning abilities (Hsieh          3.1    FOL Representation
et al. 2023; Ho, Schmid, and Yun 2023). However, these              We begin by introducing the notation used throughout this
approaches primarily evaluate effectiveness through down-           work. Let N LP = {N LP1 , N LP2 , . . . , N LPn } denote
stream performance gains after fine-tuning, offering limited        the set of natural-language premises, and let N LC de-
insight into data quality. In contrast, we propose a tool-based     note the natural-language conclusion. Together, they form
symbolic data generation framework that enables external            the natural-language input, S ← {N LP , N LC } which is
verification, ensuring the reliability and correctness of the       passed to a language model (LM) for symbolic transla-
data used for fine-tuning.                                          tion. Before generating FOL expressions, we follow the
Structured Inference with LLMs The use of multiple                  predicate-generation procedure to ensure semantic consis-
prompts distributed across several steps to solve a single          tency. This procedure produces a collection of predicates,
problem has been widely studied in LLM inference across             denoted P = { P (k) | k = 1, . . . , m }, where each P (k) is
domains (Yao et al. 2022). However, these multi-step infer-         a predicate with arity P (k) ∈ N, indicating its number of
ences are typically prompt-induced at each stage. Related           arguments.
work in neurosymbolic and logical reasoning also adopts                The resulting FOL forms of the premises and conclusion
multi-step prompting. For instance, Ryu et al. (2025) first         are written as FOL(S) = {φP1 , φP2 , . . . , φPn , φC }, where
prompts the model to generate step-by-step reasoning and            each φ is expressed using the defined predicates. Based on
subsequently prompts it again to produce translations; sim-         these formulas, the reasoning system produces a final state,
ilarly, Tan et al. (2025) first elicits symbolic instances and      assigned one of the following labels: True, False, or
then performs higher-level inferences over these generated          Uncertain.
symbols for data synthesis. Our work differs from this prior
line of research in that we rely on a fine-tuned model without      3.2    Translation Errors
requiring additional instructions at inference time. Instead,       Large Language Models (LLMs) have demonstrated vary-
we use early stopping with smaller LMs to improve output            ing success in translating natural language into formal rep-
formatting. To the best of our knowledge, ours is the first         resentations. Among these formalism, NL-FOL translation
work to explore this specific form of inference.                    presents unique challenges involving syntactic and semantic
                                                                    interpretations. In this section, we focus solely on categoriz-
                   3   NL-to-FOL Translation                        ing the syntactic errors observed during LM translations1 .
First-order logic (FOL) is a logical framework that uses               1
                                                                         Semantic errors such as incorrect quantifiers, operators, or
predicates, quantifiers, variables, and logical connectives,        predicates conform to formal syntax but misrepresent the intended
enabling automated reasoning grounded in natural language           meaning. Unlike syntactic errors, they are not automatically de-
(NL). Because predicate logic follows strict formal rules           tectable through standard parsers or theorem provers. The proxy
(Russell and Norvig 2020), violations of these rules result         for detecting semantic errors is the final reasoning accuracy.
   Syntactic errors arise from violations of grammatical rules    using Prover9, which supplies explicit feedback for diverse
during translation. For example, the rule “every free vari-       classes of errors. This synthesized data, combined with ex-
able in a predicate must be bound by a quantifier” applied        isting symbolic datasets, serves as the foundation for train-
to the statement “Green people are blue” requires a quanti-       ing LLMs to produce reliable NL-to-FOL translations. Ad-
fier ‘∀’ for the variable x. Missing quantifiers or operators     ditional details on the data generation process are provided
lead to parsing failures, which are often detected by tools       in Appendix B.
such as Prover9 that provide feedback on syntax issues. The
                                                                  Supervised Fine-Tuning We apply Supervised Fine-
most common categories of syntactic errors, summarized in
                                                                  Tuning (SFT) to generate predicates set P, followed by
Table 1, are described below:
                                                                  the FOL representations of the premises and conclusion
 • Parsing errors: These are caused by structural inconsis-       FOL(S). The model input during training is the concate-
   tencies, such as                                               nation X = S ∥ P ∥ FOL(S), enabling it to learn the
   – Missing quantifier – a variable not bound by ∀ or ∃;         structured-form generation pattern. The resulting fine-tuned
                                                                  model is denoted pθ .
   – Parenthesis error – unmatched or missing parentheses
     render a formula invalid;                                    4.2   Inference
   – Completion error – incomplete formulas or interrup-
                                                                  In standard inference, the model receives the natural-
     tions by extraneous text.
                                                                  language statement S and directly generates both P and
 • NoneType errors: These arise from higher-level struc-          FOL(S). However, due to the degenerative nature of greedy
   tural issues, including                                        decoding, where a single error can propagate through the se-
   – Quantifier location – quantifiers placed incorrectly or      quence, leading to repetitive or malformed outputs, this ap-
     redundantly;                                                 proach is brittle. To address this, we introduce incremental
   – Missing variable – quantifier applied to constant facts      inference, a two-stage inference procedure.
     with no free variables.                                         In the first stage, the model receives the natural-language
                                                                  premises and conclusion and generates a predicate set:
 • Token errors: These involve invalid lexical elements,
   such as                                                                         P
                                                                                   b = arg max pθ (y | S) .
                                                                                               y
   – Special token – unsupported special characters in the
     input;                                                         In the second stage, the model receives the augmented in-
   – Unknown operator – operators not belonging to the            put S ∥ P
                                                                          b and produces the FOL representation:
     valid set of logical connectives.                                                                          
                                                                             FOL(S)
                                                                              [        = arg max pθ y | S, P   b .
 • Predicate errors: These occur when predicates are used                                          y
   inconsistently, including                                         This incremental procedure reduces error propagation and
   – Arity mismatch – using the same predicate with differ-       yields more syntactically and semantically coherent FOL
     ent numbers of arguments;                                    outputs. Since the output is decomposed into two stages, any
   – Subject–predicate conflict – treating an entity as both      additional latency introduced by incremental inference is at-
     a constant and a predicate.                                  tributable to the increased number of output tokens. With an
                                                                  appropriate allocation of output tokens, incremental infer-
  For additional details, see Appendix A.                         ence does not incur additional inference time.

                    4    Methodology                              Predicate Evaluation To analyze the role of predicate
                                                                  generation in NL-to-FOL translation, we use two metrics:
4.1   Data synthesis for Finetuning                               coverage, analogous to recall, and usage, analogous to preci-
The alignment of a language model to follow instructions for      sion. The model first generates a set of candidate predicates
a specific task can be accomplished by fine-tuning on suf-        P§ = { P (k) | k = 1, . . . , m }, followed by the composition
ficiently large and representative datasets. Translating nat-     of FOL statements. Let the set of predicates that appear in
ural language into FOL, however, requires capturing for-          FOL(S) be P† = { P (k) | k = 1, . . . , n }
mal semantics at the passage level rather than the sentence          Coverage measures the fraction of predicates used in the
level, making it challenging for a model to consistently ad-      FOL statements that were present in the initial generated
here to the required format. To obtain high-quality passage-      set, while usage measures the fraction of initially generated
level translations, we employ a streamlined pipeline for gen-     predicates that were actually used:
erating FOL data. Our data-generation process builds on
ProofWriter, which provides a large number of training in-                                      |P§ ∩ P† |
                                                                                    Coverage =             ,
stances consisting of multiple premises, a conclusion, and                                        |P† |
varying reasoning depths. Following Pan et al. (2023), we                                       |P§ ∩ P† |
first generate the set of predicates and then derive the corre-                         Usage =            .
                                                                                                  |P§ |
sponding FOL statements for each sentence. We standardize
the target formal language to Prover9 and apply it consis-          These predicates from FOL generation can be obtained
tently across all translations. Syntax validation is performed    only if the final output follows a standard format, where it
                                                 Gemma-3-4B          Phi-4-mini       Qwen-2.5-3B         Qwen-3-4B
                                  Inference Type ExcRate   Acc     ExcRate    Acc    ExcRate     Acc    ExcRate    Acc
                                  ICL            74.50     58.33    87.00    68.67     36.67    25.50    42.67    35.50


                    PW
                                  SFT+           98.83     96.83     100     97.83     96.83    93.33    95.00    92.83
                                    Increment    98.50     96.50     100     97.83     96.50    93.00    96.50    94.17
                    FO            ICL            58.13     33.00    45.32    28.08     27.59    19.21     6.40     3.45
                                  SFT+           66.00     36.95    61.08    38.92     57.63    30.05    60.10    40.39
                                    Increment    69.95     40.89    62.07    38.92     55.17    30.54    58.13    38.42
                                                                   OOD Datasets
                                  ICL             5.60      0.80     6.40     2.60      4.40     0.40     2.80     1.20
                    PrvQA PrnQA




                                  SFT+           51.80     23.20    44.60    30.60     55.60    21.60    62.20    51.60
                                    Increment    50.80     23.60    52.40    34.80     54.40    19.20    80.60    64.40
                                  ICL            28.40      9.40    48.40    18.20      7.60     3.00     0.00     0.00
                                  SFT+           65.80     33.60    42.20    24.40     50.40    22.20    64.80    40.80
                                    Increment    69.40     35.60    53.40    31.00     50.20    20.20    70.40    43.00

Table 2: Comparison of models’ deductive reasoning accuracy under FOL-based output prediction and the execution rate
(%) of the FOLs by the tool. ICL denotes in-context learning (5-shots); SFT+ denotes SFT on symbolic ProofWriter and
FOLIO combined; Increment denotes incremental inference on top of the SFT+ model. The values in bold represent the best
performance for each model–dataset pair.


first generates translations for each statement in the premise,              as SFT+ . All models were trained for three epochs using
and then for the conclusion. We therefore track the validity                 supervised fine-tuning with LoRA (Hu et al. 2022). For
of generations, which measures adherence to this expected                    inference, we applied 8-bit quantization with a temperature
format and differs from solver-based execution rates. Our                    of 0.1 and a maximum generation limit of 1,000 tokens.
objective is to maximize coverage to ensure accurate predi-
cate dependencies.
Verification Because predicate generation is separated                       Benchmarks. We report the downstream accuracy of
from full-statement generation, we additionally explore in-                  the fine-tuned models on four deductive logical reasoning
tegrating a predicate verifier before passing the augmented                  benchmarks: ProofWriter (Tafjord, Dalvi, and Clark 2021),
input to the model for FOL generation.                                       ProntoQA (Saparov and He 2023), ProverQA (Qi et al.
   We define a verifier V that checks predicate validity and                 2025b), and FOLIO (Han et al. 2024). Notably, ProverQA
                                                                             does not include FOL translations in its training data, and
arity consistency. For the generated predicates P   b in the first
                                                                             ProntoQA is a test-only benchmark, making inference on
stage of incremental inference, the verifier outputs either the              these two datasets out-of-distribution (OOD) for our models.
original set or a corrected version:                                         For ProofWriter and ProntoQA, we use the test set provided
                                                                             by Pan et al. (2023), consisting of 600 and 500 records, re-
            (
            P,
               b       if predicates satisfy arity consistency,
 V P =
     b                                                                       spectively. For FOLIO, we used 203 development records
              P ver , otherwise,                                             for test. For ProverQA, we used 500 records of the ‘hard’
where P ver is the corrected predicate set produced by the                   subset of the test set.
verifier.
  The final FOL representation is then obtained in the sec-
ond stage:                                                                   Evaluation. We evaluate models using two metrics: exe-
                                                                         cution rate and accuracy. Execution rate is defined as the
          FOL(S)
          [        = arg max pθ y | S, V P   b .                             percentage of valid FOL statements that successfully parse
                                      y                                      through the tool. We use In-Context Learning (ICL) as a
                                                                             baseline and compare it against SFT for NL-to-FOL trans-
                         5         Experiments                               lation. In both settings, models generate FOL translations
We fine-tuned four small-scale models of size 3–4B                           from natural language inputs, and the final logical outcomes
— Gemma-3-4B-Instruct (Kamath et al. 2025),                                  are obtained using Prover9. For ProntoQA, which is a test-
Phi-4-mini-Instruct (Abouelenin et al. 2025),                                only dataset, we use demonstrations from ProofWriter for
Qwen2.5-3B-Instruct (Hui et al. 2024), and                                   ICL inference, while all other datasets use in-domain few-
Qwen3-4B-Instruct-2507 (Team 2025) — on FOL                                  shot examples. We report results using 5-shot examples for
translations from ProofWriter and FOLIO (the latter offer-                   the ICL baseline in our main experiments. Results for differ-
ing only a limited number of available translations), denoted                ent numbers of shots are provided in §6.4.
                        Figure 2: Heatmap of error types counts across datasets, models, and methods.


                                                                             Mode    Gemma-3         Phi-mini       Qwen-2.5       Qwen-3




                                                                  FOLIO ProofW
                                                                             Vanilla 99 / 99 / 100 100 / 100 / 100 99 / 99 / 100 100 / 100 / 100
                                                                             Incr 99 / 99 / 100 100 / 100 / 100 99 / 99 / 100 100 / 100 / 100
                                                                             ∆         0/0/0          0/0/0          0/0/0          0/0/0
                                                                             Std     88 / 85 / 93   86 / 82 / 91   76 / 81 / 97 88 / 84 / 96
                                                                             Incr    91 / 86 / 96   92 / 87 / 97   78 / 83 / 97 90 / 86 / 100
                                                                             ∆       +3 / +1 / +3   +6 / +5 / +6   +2 / +2 / 0 +2 / +2 / +4
                                                                             Std    80 / 94 / 100 49 / 53 / 61 72 / 83 / 99 69 / 73 / 78
                                                                  Pronto


                                                                             Incr   81 / 94 / 100 53 / 59 / 71 72 / 84 / 99 75 / 81 / 100
                                                                             ∆       +1 / 0 / 0 +4 / +6 / +10 0 / +1 / 0 +6 / +8 / +22
                                                                             Std     74 / 82 / 91 46 / 46 / 53 61 / 77 / 92       74 / 75 / 87
                                                                  Prover




                                                                             Incr    78 / 85 / 96 62 / 62 / 76 63 / 81 / 97       78 / 79 / 95
                                                                             ∆       +4 / +3 / +5 +16 / +16 / +23 +2 / +4 / +5    +4 / +4 / +8

                                                                 Table 3: Predicate analysis across datasets and models. Each
                                                                 entry reports Coverage / Usage / Validity (%). Incr (Incre-
Figure 3: Change in total errors with and without incre-         mental) indicates the proposed inference method; ∆ reports
mental inference across all models and datasets. Blue mark-      (Incr − Vanilla).
ers denote in-distribution datasets, while olive green mark-
ers denote out-of-distribution (OOD) datasets. Refer to Ap-
pendix D for the numerical values corresponding to this plot.    on mixed data is particularly conducive to generalization.
                                                                 This further reinforces the effectiveness of our data synthe-
                                                                 sis pipeline.
             6    Results and Discussion                            Beyond accuracy, Figure 2 shows the distribution of er-
We evaluate results using accuracy and previously defined        ror categories across all benchmarks. ProntoQA exhibits a
error categories. Because the models come from different         large number of arity and type errors under ICL; SFT sub-
families and have been trained under distinct settings, we       stantially reduces these errors, with type errors reduced more
encourage interpreting the results as model-specific and sen-    consistently than arity errors. We attribute this difference to
sitive to the particular data types used.                        the dataset’s use of fictional abstractions such as “jumpus,”
                                                                 which appear to confuse models during predicate genera-
6.1   Logical Reasoning with SFT                                 tion.
Table 2 presents initial results on logical-reasoning datasets      There are a few cases in which certain error categories
using both ICL and SFT, comparing performance across             increase slightly under SFT, but these do not include for-
small-scale model families on multiple benchmarks. A             matting errors, which are effectively corrected through fine-
consistent and expected trend emerges: fine-tuning on in-        tuning. The reduction in formatting issues can, in turn, lead
domain datasets improves performance. All models show            to a slight increase in other types of errors. Further de-
clear gains in both execution rate and accuracy when fine-       tails are provided in Appendix D. Figure 3 provides an
tuned, correcting the relatively low performance observed        overall comparison of SFT error reductions relative to the
under ICL. Notably, fine-tuned models also achieve substan-      baseline. We observe decreases across nearly all condi-
tial improvements on OOD datasets, suggesting that training      tions: ProofWriter shows a 100% reduction in errors for
Phi-4-mini-Instruct; FOLIO shows the largest drop                 6.3   Arity Verification during Inference
of 57.4% using Qwen3-4B-Instruct-2507; ProntoQA                   Given the two-stage generation structure and the explicit
and ProverQA show 61% and 64% reductions, respectively,           predicate decoding enabled by incremental inference, we
using Qwen3-4B-Instruct-2507.                                     also explore integrating a verification mechanism directly
   One exception, highlighted in red, is a 12% increase in        into the inference pipeline. We use the term verifier to refer
error rate on ProverQA using Phi-4-mini. In this case, the        to a model that takes natural language statements (premises
model struggles to maintain the intended output format due        and conclusion) along with LM-generated predicates and
to the large number of premises per query, causing it to lose     outputs either (i) a corrected set of predicates aligned with
context during generation. This motivates us to use incre-        the NL statements or (ii) the token ‘correct’ to indicate that
mental inference.                                                 the predicates are valid.




Figure 4: The gain from adding ICL verifier on top of Incre-
mental inference. We use the Gemma-3-4B-Instruct as
an ICL verifier with 3-shot examples that include arity per-
turbations from the respective training data.


Incremental Inference A two-stage generation process
enables stricter adherence to the required output format
compared to standard inference. Figure 3 illustrates this ef-
fect: the arrows fall further below the diagonal, indicating
roughly a 10% additional reduction in errors relative to the
increase observed under standard inference. Although this
improvement is modest, it demonstrates the effectiveness of
the method. We anticipate that higher-level or multi-stage
forms of incremental inference may yield stronger gains, and      Figure 5: The comparison of reasoning accuracy achieved by
we leave such extensions for future work.                         using between different number of shots in the translation.
                                                                  The red horizontal lines are for reference: the dashed line
6.2   Predicate Analysis                                          reports the results under incremental decoding, and the solid
Because our earlier evaluation primarily focused on accu-         line reports the results with the verification on top.
racy and tool-detected errors, we introduce an additional
analysis targeting the semantic consistency of predicates in         We employ Gemma-3-4B-Instruct as the verifier
the generated FOL translations. In particular, we measure         and construct 3-shot demonstrations that include arity errors
how well the predicates predicted in the first stage corre-       curated from the training data. Figure 4 shows that using
spond to those used in the final FOL statements. Table 3 re-      a small LM for predicate verification further improves per-
ports predicate coverage and usage, along with the validity       formance over incremental inference alone. As noted ear-
rate of the generated FOL expressions.                            lier, ProntoQA continues to struggle with arity errors due to
   This analysis highlights how incremental inference influ-      its semantic abstractions; more tailored in-context examples
ences predicate fidelity. We find that incremental inference      may help alleviate this gap. This verification approach can
consistently improves predicate coverage, with a 16% in-          naturally be extended to other types of errors. Full imple-
crease on OOD data, as predicates are explicitly generated        mentation details are provided in Appendix E.
in the first stage rather than inferred implicitly during full-
sequence decoding. The validity (an adherence to the re-          6.4   Number of Shots
quired format) of FOL statements also improves by a high of       We conduct ICL with varying numbers of few-shot ex-
23% under this setup. ProofWriter, which already achieves         amples randomly sampled from the training sets (3, 5,
high predicate stability, shows no change, indicating that        and 7) to determine the optimal count of demonstra-
incremental inference does not disrupt performance when           tions. The reasoning accuracy results presented in Fig-
models already behave consistently.                               ure 5 show that the performance of smaller language mod-
els degrades as more demonstrations are added, partic-                                      References
ularly for Qwen2.5-3B-Instruct and Phi4-mini                        Abouelenin, A.; Ashfaq, A.; Atkinson, A.; Awadalla, H.;
Instruct. Although in a few cases accuracy improves                 Bach, N.; Bao, J.; Benhaim, A.; Cai, M.; Chaudhary, V.;
with additional few-shots, the gains are negligible compared        Chen, C.; et al. 2025. Phi-4-mini technical report: Compact
to the fine-tuned models. The two red horizontal reference          yet powerful multimodal language models via mixture-of-
lines in each plot indicate the performance achieved by the         loras. arXiv preprint arXiv:2503.01743.
SFT+ with incremental inference (dashed line), and the ad-
                                                                    Chen, M. K.; Zhang, X.; and Tao, D. 2025. Justlogic: A com-
dition of the verifier on top (solid line). See Appendix C
                                                                    prehensive benchmark for evaluating deductive reasoning in
for further ICL results on execution rates as well as the
                                                                    large language models. arXiv preprint arXiv:2501.14851.
ProofWriter results.
                                                                    De Moura, L.; and Bjørner, N. 2008. Z3: An efficient
                                                                    SMT solver. In International conference on Tools and Algo-
                      7    Conclusion                               rithms for the Construction and Analysis of Systems, 337–
                                                                    340. Springer.
In this paper, we provide a systematic analysis of com-             Han, S.; Schoelkopf, H.; Zhao, Y.; Qi, Z.; Riddell, M.; Zhou,
mon translation errors made by LMs when performing nat-             W.; Coady, J.; Peng, D.; Qiao, Y.; Benson, L.; Sun, L.;
ural language to first-order logic translation. Using small         Wardle-Solano, A.; Szabó, H.; Zubova, E.; Burtell, M.; Fan,
LMs fine-tuned on an expanded set of symbolic data, we              J.; Liu, Y.; Wong, B.; Sailor, M.; Ni, A.; Nan, L.; Kasai,
compare their error patterns against in-context learning and        J.; Yu, T.; Zhang, R.; Fabbri, A.; Kryscinski, W. M.; Yavuz,
highlight the limitations of small models under standard            S.; Liu, Y.; Lin, X. V.; Joty, S.; Zhou, Y.; Xiong, C.; Ying,
inference. We introduce an incremental inference frame-             R.; Cohan, A.; and Radev, D. 2024. FOLIO: Natural Lan-
work and demonstrate that decomposing the generation pro-           guage Reasoning with First-Order Logic. In Proceedings of
cess improves symbolic outputs due to the structured na-            the 2024 Conference on Empirical Methods in Natural Lan-
ture of the task. This method substantially improves pred-          guage Processing, 22017–22031.
icate generation and reduces formatting errors, including on        Ho, N.; Schmid, L.; and Yun, S.-Y. 2023. Large language
out-of-distribution datasets. Additionally, we incorporate a        models are reasoning teachers. In Proceedings of the 61st
lightweight verifier into the first stage of the incremental        annual meeting of the association for computational linguis-
pipeline, illustrating its potential for further improving trans-   tics (volume 1: long papers), 14852–14882.
lation robustness. Future work may focus on strengthening           Holtzman, A.; Buys, J.; Du, L.; Forbes, M.; and Choi, Y.
the verification module for both predicate and FOL genera-          2020. The Curious Case of Neural Text Degeneration.
tion, guided by error classification, to further enhance trans-     In 8th International Conference on Learning Representa-
lation accuracy.                                                    tions, ICLR 2020, Addis Ababa, Ethiopia, April 26-30, 2020.
                                                                    OpenReview.net.
                          Limitations                               Hsieh, C.-Y.; Li, C.-L.; Yeh, C.-K.; Nakhost, H.; Fujii, Y.;
                                                                    Ratner, A.; Krishna, R.; Lee, C.-Y.; and Pfister, T. 2023. Dis-
The dataset constructed from ProofWriter inherits limita-           tilling step-by-step! outperforming larger language models
tions in the diversity and complexity of its statements. In         with less training data and smaller model sizes. In Find-
addition, the silver data generated using GPT-4o, while             ings of the Association for Computational Linguistics: ACL
carefully curated, may contain minor inconsistencies that           2023, 8003–8017.
we correct to the best of our ability. Fine-tuning per-             Hu, E. J.; yelong shen; Wallis, P.; Allen-Zhu, Z.; Li, Y.;
formance on logical reasoning tasks is highly dependent             Wang, S.; Wang, L.; and Chen, W. 2022. LoRA: Low-Rank
on the underlying model, yet direct behavioral compar-              Adaptation of Large Language Models. In International
isons are difficult due to the lack of transparency in pre-         Conference on Learning Representations.
training data. For example, Qwen models—particularly the            Hui, B.; Yang, J.; Cui, Z.; Yang, J.; Liu, D.; Zhang, L.; Liu,
4B variant—emphasize “thinking” during training but per-            T.; Zhang, J.; Yu, B.; Dang, K.; Yang, A.; Men, R.; Huang,
form poorly under in-context learning and tend to generate          F.; Ren, X.; Ren, X.; Zhou, J.; and Lin, J. 2024. Qwen2.5-
excessively long reasoning chains during inference, a be-           Coder Technical Report. CoRR, abs/2409.12186.
havior that becomes more pronounced after fine-tuning and           Kamath, A.; Ferret, J.; Pathak, S.; Vieillard, N.; Merhej,
leads to additional computational overhead.                         R.; Perrin, S.; Matejovicova, T.; Ramé, A.; Rivière, M.;
   While the proposed framework ensures coverage between            Rouillard, L.; Mesnard, T.; Cideron, G.; Grill, J.; Ramos,
explicitly stated predicates and their symbolic translations, it    S.; Yvinec, E.; Casbon, M.; Pot, E.; Penchev, I.; Liu, G.;
does not fully address semantic correctness, as symbolic rep-       Visin, F.; Kenealy, K.; Beyer, L.; Zhai, X.; Tsitsulin, A.;
resentations may not capture the complete intended meaning          Busa-Fekete, R.; Feng, A.; Sachdeva, N.; Coleman, B.;
of the original natural language statements. Finally, incor-        Gao, Y.; Mustafa, B.; Barr, I.; Parisotto, E.; Tian, D.; Eyal,
porating a verification module introduces additional infer-         M.; Cherry, C.; Peter, J.; Sinopalnikov, D.; Bhupatiraju, S.;
ence latency, as it adds an extra processing step, although         Agarwal, R.; Kazemi, M.; Malkin, D.; Kumar, R.; Vilar, D.;
the incremental inference procedure itself does not increase        Brusilovsky, I.; Luo, J.; Steiner, A.; Friesen, A.; Sharma,
latency.                                                            A.; Sharma, A.; Gilady, A. M.; Goedeckemeyer, A.; Saade,
A.; Kolesnikov, A.; Bendebury, A.; Abdagic, A.; Vadi, A.;       Qi, C.; Ma, R.; Li, B.; Du, H.; Hui, B.; Wu, J.; Laili, Y.;
György, A.; Pinto, A. S.; Das, A.; Bapna, A.; Miech, A.;       and He, C. 2025b. Large Language Models Meet Symbolic
Yang, A.; Paterson, A.; Shenoy, A.; Chakrabarti, A.; Piot,      Provers for Logical Reasoning Evaluation. In The Thirteenth
B.; Wu, B.; Shahriari, B.; Petrini, B.; Chen, C.; Lan, C. L.;   International Conference on Learning Representations.
Choquette-Choo, C. A.; Carey, C.; Brick, C.; Deutsch, D.;       Russell, S.; and Norvig, P. 2020. Artificial Intelligence:
Eisenbud, D.; Cattle, D.; Cheng, D.; Paparas, D.; Sreepathi-    A Modern Approach (4th Edition).            Pearson.    ISBN
halli, D. S.; Reid, D.; Tran, D.; Zelle, D.; Noland, E.;        9780134610993.
Huizenga, E.; Kharitonov, E.; Liu, F.; Amirkhanyan, G.;         Ryu, H.; Kim, G.; Lee, H. S.; and Yang, E. 2025. Divide
Cameron, G.; Hashemi, H.; Klimczak-Plucinska, H.; Singh,        and Translate: Compositional First-Order Logic Translation
H.; Mehta, H.; Lehri, H. T.; Hazimeh, H.; Ballantyne, I.;       and Verification for Complex Logical Reasoning. In The
Szpektor, I.; and Nardini, I. 2025. Gemma 3 Technical Re-       Thirteenth International Conference on Learning Represen-
port. CoRR, abs/2503.19786.                                     tations, ICLR 2025, Singapore, April 24-28, 2025. OpenRe-
Liu, H.; Fu, Z.; Ding, M.; Ning, R.; Zhang, C.; Liu, X.;        view.net.
and Zhang, Y. 2025. Logical Reasoning in Large Language         Saparov, A.; and He, H. 2023. Language Models Are
Models: A Survey. CoRR, abs/2502.09100.                         Greedy Reasoners: A Systematic Formal Analysis of Chain-
Liu, M.; Ueda, R.; Wan, Z.; Inoue, K.; and Willcocks, C. G.     of-Thought. In The Eleventh International Conference on
2024. Neuro-Symbolic Contrastive Learning for Cross-            Learning Representations, ICLR 2023, Kigali, Rwanda, May
domain Inference. In Cabalar, P.; Fabiano, F.; Gebser, M.;      1-5, 2023. OpenReview.net.
Gupta, G.; and Swift, T., eds., Proceedings 40th Interna-       Tafjord, O.; Dalvi, B.; and Clark, P. 2021. ProofWriter: Gen-
tional Conference on Logic Programming, ICLP 2024, vol-         erating Implications, Proofs, and Abductive Statements over
ume 416 of EPTCS, 78–94.                                        Natural Language. In Findings of the Association for Com-
Matthew Lam, L. H.; Thatikonda, R. K.; and Shareghi, E.         putational Linguistics: ACL/IJCNLP 2021, Online Event,
2024. A Closer Look at Tool-based Logical Reasoning             August 1-6, 2021, volume ACL/IJCNLP 2021 of Findings of
with LLMs: The Choice of Tool Matters. In Baldwin, T.;          ACL, 3621–3634. Association for Computational Linguis-
Rodrı́guez Méndez, S. J.; and Kuo, N., eds., Proceedings       tics.
of the 22nd Annual Workshop of the Australasian Language        Tan, X.; Valentino, M.; Akhter, M. E.; Liakata, M.; and
Technology Association, 41–63. Canberra, Australia: Asso-       Aletras, N. 2025. Enhancing logical reasoning in language
ciation for Computational Linguistics.                          models via symbolically-guided monte carlo process super-
                                                                vision. In Proceedings of the 2025 Conference on Empirical
McCune, W. 2005. Release of Prover9. In Mile high con-
                                                                Methods in Natural Language Processing, 31874–31888.
ference on quasigroups, loops and nonassociative systems,
Denver, Colorado.                                               Taori, R.; Gulrajani, I.; Zhang, T.; Dubois, Y.; Li, X.;
                                                                Guestrin, C.; Liang, P.; and Hashimoto, T. B. 2023. Alpaca:
Nye, M. I.; Tessler, M. H.; Tenenbaum, J. B.; and Lake,         A Strong, Replicable Instruction-Following Model. GitHub
B. M. 2021. Improving Coherence and Consistency in Neu-         repository. https://github.com/tatsu-lab/stanford alpaca.
ral Sequence Models with Dual-System, Neuro-Symbolic
                                                                Tarau, P. 2024. On LLM-generated Logic Programs and
Reasoning. In Advances in Neural Information Processing
                                                                their Inference Execution Methods. In Proceedings 40th In-
Systems 34: Annual Conference on Neural Information Pro-
                                                                ternational Conference on Logic Programming, ICLP, vol-
cessing Systems, NeurIPS, 25192–25204.
                                                                ume 416 of EPTCS, 1–14.
Olausson, T.; Gu, A.; Lipkin, B.; Zhang, C. E.; Solar-          Team, Q. 2025.                 Qwen3 Technical Report.
Lezama, A.; Tenenbaum, J. B.; and Levy, R. 2023. LINC: A        arXiv:2505.09388.
Neurosymbolic Approach for Logical Reasoning by Com-
                                                                Wang, Y.; Kordi, Y.; Mishra, S.; Liu, A.; Smith, N. A.;
bining Language Models with First-Order Logic Provers.
                                                                Khashabi, D.; and Hajishirzi, H. 2023. Self-instruct: Align-
In Proceedings of the Conference on Empirical Methods in
                                                                ing language models with self-generated instructions. In
Natural Language Processing, EMNLP, 5153–5176.
                                                                Proceedings of the 61st annual meeting of the associa-
Ouyang, L.; Wu, J.; Jiang, X.; Almeida, D.; Wainwright, C.;     tion for computational linguistics (volume 1: long papers),
Mishkin, P.; Zhang, C.; Agarwal, S.; Slama, K.; Ray, A.;        13484–13508.
et al. 2022. Training language models to follow instructions    Wei, J.; Wang, X.; Schuurmans, D.; Bosma, M.; Xia, F.;
with human feedback.                                            Chi, E.; Le, Q. V.; Zhou, D.; et al. 2022. Chain-of-thought
Pan, L.; Albalak, A.; Wang, X.; and Wang, W. 2023. Logic-       prompting elicits reasoning in large language models.
LM: Empowering Large Language Models with Symbolic              Wu, Y.; Jiang, A. Q.; Li, W.; Rabe, M.; Staats, C.; Jamnik,
Solvers for Faithful Logical Reasoning. In Findings of the      M.; and Szegedy, C. 2022. Autoformalization with large
Association for Computational Linguistics: EMNLP, 3806–         language models. In Advances in Neural Information Pro-
3824. Singapore.                                                cessing Systems, volume 35, 32353–32368.
Qi, C.; Ma, R.; Li, B.; Du, H.; Hui, B.; Wu, J.; Laili, Y.;     Xu, F.; Lin, Q.; Han, J.; Zhao, T.; Liu, J.; and Cambria,
and He, C. 2025a. Large language models meet symbolic           E. 2025. Are Large Language Models Really Good Log-
provers for logical reasoning evaluation. arXiv preprint        ical Reasoners? A Comprehensive Evaluation and Beyond.
arXiv:2502.06563.                                               IEEE Trans. Knowl. Data Eng., 37(4): 1620–1634.
Xu, J.; Fei, H.; Pan, L.; Liu, Q.; Lee, M.-L.; and Hsu, W.         a output token length of 1,000 for each generation. We ran
2024a. Faithful Logical Reasoning via Symbolic Chain-of-           a small scale experiment through GPT-4o for various few-
Thought.                                                           shot combinations. We selected the most optimal demon-
Xu, X.; Li, M.; Tao, C.; Shen, T.; Cheng, R.; Li, J.; Xu,          strations with the least format and translation issues. We
C.; Tao, D.; and Zhou, T. 2024b. A survey on knowl-                use url = /v1/chat/completions format for batch gen-
edge distillation of large language models. arXiv preprint         erations of GPT4o (see Figure 7 for prompt details). The
arXiv:2402.13116.                                                  logical solver is Prover 9, a theorem prover suitable to run in
                                                                   python environment with nltk library, that uses CNF conver-
Yang, K.; Poesia, G.; He, J.; Li, W.; Lauter, K.; Chaudhuri,
                                                                   sions, quantifier operations, and skolemization to transform
S.; and Song, D. 2024a. Formal mathematical reasoning: A
                                                                   the clauses into a tree format. Parsing errors by Prover 9
new frontier in ai. In arXiv preprint arXiv:2412.16075.
                                                                   occur when the FOL formula cannot be converted to a tree
Yang, Y.; Xiong, S.; Payani, A.; Shareghi, E.; and Fekri, F.       structure because it does not follow specific grammar rules.
2024b. Harnessing the Power of Large Language Models for           After filter and parsing stages, we get 10,424 records with
Natural Language to First-Order Logic Translation. In Pro-         FOL statements with a fair distribution of labels. Syntax er-
ceedings of the 62nd Annual Meeting of the Association for         rors are the errors thrown by the tool and semantic errors
Computational Linguistics (Volume 1: Long Papers), 6942–           are measured by comparing the ground truth label with the
6959. Association for Computational Linguistics.                   solver output.
Yao, S.; Zhao, J.; Yu, D.; Du, N.; Shafran, I.; Narasimhan,        Quality Evaluation. We manually evaluated a random
K.; and Cao, Y. 2022. React: Synergizing reasoning and             sample of 50 records from the dataset (containing 1,018 in-
acting in language models.                                         dividual statements) for which Prover9 confirmed correct-
Ye, X.; Chen, Q.; Dillig, I.; and Durrett, G. 2023. SatLM:         ness of the final outputs. Among these 1,018 translations,
Satisfiability-Aided Language Models Using Declarative             we found only 22 errors (approximately 2%), half of which
Prompting. In Advances in Neural Information Processing            were minor and did not affect the semantic interpretation of
Systems 36: Annual Conference on Neural Information Pro-           the FOL statements. We also extracted predicates and per-
cessing Systems, NeurIPS.                                          formed arity checks and similarity analysis on lemmatized
                                                                   predicate forms across all records, identifying no errors in
                                                                   predicate construction.
              A    Error Categorization.
The error categories are derived from the feedback provided
by the tool. We categorize these errors based on common
patterns observed in language model generations (Table 4).
Formatting errors are grouped together as cases where the
FOL statements never reach the tool, as these generations
have incompatible or invalid FOL formatting. These are usu-
ally the ones with no feedback from the tool, but fail at pars-
ing stage.

     Error Category        Representative Pattern                  Figure 6: Overview of the Data Generation Pipeline and Key
     NoneType Error        ’N ONE T YPE ’ OBJECT HAS               Statistics.
                           NO ATTRIBUTE ’ RSTRIP ’
     Arity Error           T HE FOLLOWING SYM -
                           BOLS ARE USED WITH                                    C     In-Context Learning
                           MULTIPLE ARITIES
                                                                   Figure 7 shows the format of the few-shot example for gen-
     Parsing Error         A TERM CANNOT BE                        eration of FOLs using data synthesis. It includes an instruc-
                           CONSTRUCTED FROM THE
                                                                   tion followed by examples which show a sequential genera-
                           MARKED STRING
                                                                   tion of predicates, FOL for premise and conclusion. Table 5
     Token Error           U NEXPECTED TOKEN :’-’                  reports the detailed accuracy and execution rates for each
                                                                   models and datasets under different number of shots. The
Table 4: Common error categories and representative pat-           Qwen-3-4B model fails to follow the formatting instruc-
terns used to extract LM-generated errors                          tions, specifically for ProverQA dataset.
                                                                      The prompt for the ICL FOL generation from LMs is pre-
                                                                   sented in Figure 8. The FOL syntax is fixed to represent
                   B    Data Synthesis                             Prover9 format.
The data pipeline applied for generating the FOL transla-
tions is detailed in Fig 6. The train data is 15,000 data points     D    Error Distribution in FOL Generations
with depth-5 from ProofWriter dataset. The 15k records are         Table 6 reports the statistics of syntax errors in detail.
sampled randomly ensuring a fair distribution of the labels;       Smaller LMs are more prone to formatting errors, as they
True, False, and Uncertain. The LLM here is GPT4o with             often get stuck in a loop of greedy decoding—repeatedly
                                                      Gemma-3-4B          Phi-4-mini           Qwen-2.5-3B             Qwen-3-4B
                                             Type     ExcRate   Acc     ExcRate   Acc         ExcRate     Acc    ExcRate      Acc




                       Pronto FOLIO ProofW
                                             3-shot    66.33    59.68    74.50    57.67        57.83     39.67      1.33       0.83
                                             5-shot    74.50    58.33    87.00    68.67        36.67     25.50     42.67      35.50
                                             7-shot    83.00    64.67    26.67    23.67        15.17     10.17     62.83      53.83
                                             3-shot    46.79    27.09    42.85    30.05        22.16     12.81         1.97   1.48
                                             5-shot    58.13    33.00    45.32    28.08        27.59     19.21         6.40   3.45
                                             7-shot    51.72    30.05    43.84    27.59        22.17     14.78         6.40   3.94
                                             3-shot    13.60    1.80     6.00     2.60          6.80      0.60         0.00   0.00
                                             5-shot     5.60    0.80     6.40     2.60          4.40      0.40         2.80   1.20
                                             7-shot     3.00    0.20      1.6     1.00          7.00      0.40         9.40   4.20
                                             3-shot    30.80     9.40    47.20    18.40         0.20      0.20         0.00   0.00
                       Prover




                                             5-shot    28.40     9.40    48.40    18.20         7.60      3.00         0.00   0.00
                                             7-shot    35.80    13.00    46.20    17.00         3.40      2.00         0.00   0.00

       Table 5: Performance of smaller language models using in-context learning of varying sizes of demonstrations.


choosing the same next prediction—which makes the trans-                               Hugging     Face2 :  Qwen/Qwen2.5-3B-Instruct,
lation invalid. After fine-tuning the LMs, we observe a sig-                           Qwen/Qwen3-4B-Instruct-2507,
nificant reduction in these formatting errors.                                         google/gemma-3-4b-it,                              and
                                                                                       microsoft/Phi-4-mini-instruct. The Q WEN
              E    Verification with LM                                                models have 3B and 4B parameters, while G EMMA and P HI
                                                                                       each have 4B parameters.
We apply a simple plug-and-play verification module on top
of incremental inference using 3-shot examples. One exam-
ple demonstrates the ‘correct’ value, while the other two il-
lustrate different forms of arity errors. These include per-
turbed arity forms, where an additional variable is inserted
into a predicate, with the target correction being the cor-
responding single predicate. For FOLIO, we use examples
generated by passing the training data to an LLM, extract-
ing and reusing specifically the arity errors. For ProntoQA,
which is a test-only dataset, we use data from ProofWriter.
For ProverQA, arity errors are manually constructed. An ex-
ample prompt is shown in Figure 9.

   F    Further Details of SFT and Inference
The models are fine-tuned for three epochs with a fixed batch
size of 64, a learning rate of 1 × 10−4 , a weight decay of
0.01, and a LoRA configuration (Hu et al. 2022) adapted to
the language model on a single A100 GPU. Training uses
a causal language modeling loss applied to inputs format-
ted as {NL \n\n Predicates; FOL}, with gradients
computed over the entire input.
   Inference is performed using 8-bit quantization with the
trained LoRA adapter, a temperature of 0.1, and a variable
maximum new tokens value depending on the dataset.
P ROOF W RITER and P ROVER QA require a larger number
of tokens during inference compared to FOLIO and P RON -
TO QA due to their longer input sizes.


   G     Further details on Language Models
We use four instruction-tuned language models from differ-
                                                                                          2
ent model families. All model weights are downloaded from                                     https://huggingface.co
Few-shot Example with Instruction for Data Generation Process

Instruction: You are an expert who works with theorem provers. Given some context and a question, generate the
predicates and the first-order logic formula for contexts and question. Here is an example.
—
Context:
Anne is quiet. Erin is furry. Erin is green. Fiona is furry. Fiona is quiet. Fiona is red. Fiona is rough. Fiona is white.
Harry is furry. Harry is quiet. Harry is white. Young people are furry. If Anne is quiet then Anne is red. Young, green
people are rough. If someone is green then they are white. If someone is furry and quiet then they are white. If someone
is young and white then they are rough. All red people are young.
Question:
Anne is white.
###
Predicates:
Quiet(x) ::: x is quiet
Furry(x) ::: x is furry
Green(x) ::: x is green
Red(x) ::: x is red
Rough(x) ::: x is rough
White(x) ::: x is white
Young(x) ::: x is young
Premises:
Quiet(Anne) ::: Anne is quiet.
Furry(Erin) ::: Erin is furry.
Green(Erin) ::: Erin is green.
Furry(Fiona) ::: Fiona is furry.
Quiet(Fiona) ::: Fiona is quiet.
Red(Fiona) ::: Fiona is red.
Rough(Fiona) ::: Fiona is rough.
White(Fiona) ::: Fiona is white.
Furry(Harry) ::: Harry is furry.
Quiet(Harry) ::: Harry is quiet.
White(Harry) ::: Harry is white.
∀x (Young(x) → Furry(x)) ::: Young people are furry.
Quiet(Anne) → ¬Red(Anne) ::: If Anne is quiet then Anne is not red.
∀x (Young(x) ∧ Green(x) → Rough(x)) ::: Young, green people are rough.
∀x (Green(x) → White(x)) ::: If someone is green then they are white.
∀x (Furry(x) ∧ Quiet(x) → ¬White(x)) ::: If someone is furry and quiet then they are not white.
∀x (Young(x) ∧ White(x) → Rough(x)) ::: If someone is young and white they are rough.
∀x (Red(x) → Young(x)) ::: All red people are young.
Conclusion:
White(Anne) ::: Anne is white.
—
<INPUT>
###



            Figure 7: Few shot example and instruction for FOL generation of FOL dataset using gpt4o.
Prompt and a Few-shot Example for ICL FOL Generation

System:
Given a set of premises and a conclusion, generate the predicates and first-order logic representation of both the
premises and the conclusion.

User:
Premise:
Braden advances medical knowledge. If Braden pursues science, then he can either make a groundbreaking discovery
or advance medical knowledge, but not both. Braden pursues science.
Conclusion:
Braden makes a groundbreaking discovery.
Assistant:
Predicates:
AdvancesMedicalKnowledge(x);
PursuesScience(x);
MakesDiscovery(x);
Premise First-order:
AdvancesMedicalKnowledge(Braden) ::: Braden advances medical knowledge.;
PursuesScience(Braden) → ( MakesDiscovery(Braden) ⊕ AdvancesMedicalKnowledge(Braden)) ::: If Braden pursues
science, then he can either make a groundbreaking discovery or advance medical knowledge, but not both.;
PursuesScience(Braden) ::: Braden pursues science.
Conclusion First-order:
MakesDiscovery(Braden) ::: Braden makes a groundbreaking discovery.

Other Few-Shot Examples

User:
Premises:
Lennon has feathers. If Lennon either eats pollen or sips sap (but not both), then he collects nectar. Lennon does not
locate food. Lennon does not avoid predators. Any insect that finds shelter either avoids predators or locates food (or
both). If Lennon has feathers, then he spreads seeds and flies efficiently. If Lennon hibernates during winter, then
he migrates seasonally. Louisa does not avoid predators. Lennon finds shelter or migrates seasonally. If Karim has
feathers, then he spreads seeds and flies efficiently. Lennon either collects nectar or spreads seeds, but not both.
Conclusion:
Lennon does not pollinate flowers.



                     Figure 8: Prompt for FOL Generation in an ICL setting for Instruct models.
Dataset       Model                 Config        Token   Arities   Type   Parsing    Formatting
ProofWriter   Gemma3 4B Instruct    ICL              0        17      7           0         178
ProofWriter   Gemma3 4B Instruct    SFT+             0         1      0           0           6
ProofWriter   Gemma3 4B Instruct    Incremental      0         1      0           0           8
ProofWriter   Phi4 mini Instruct    ICL              0        62     14           0          77
ProofWriter   Phi4 mini Instruct    SFT+             0         0      0           0           0
ProofWriter   Phi4 mini Instruct    Incremental      0         0      0           0           0
ProofWriter   Qwen2.5 3B Instruct   ICL              8         9     12           0         224
ProofWriter   Qwen2.5 3B Instruct   SFT+             0         0      0           0          19
ProofWriter   Qwen2.5 3B Instruct   Incremental      0         0      0           0          21
ProofWriter   Qwen3 4B Instruct     ICL              0         0      0           0         344
ProofWriter   Qwen3 4B Instruct     SFT+             0         0      0           0          30
ProofWriter   Qwen3 4B Instruct     Incremental      0         0      0           0          21
FOLIO         Gemma3 4B Instruct    ICL              1        13      9           1          84
FOLIO         Gemma3 4B Instruct    SFT+             0        14     10           1          44
FOLIO         Gemma3 4B Instruct    Incremental      0         9     12           0          40
FOLIO         Phi4 mini Instruct    ICL              2        28     30           0          56
FOLIO         Phi4 mini Instruct    SFT+             1        18     13           0          47
FOLIO         Phi4 mini Instruct    Incremental      2        17     18           1          39
FOLIO         Qwen2.5 3B Instruct   ICL              0         3      7           0         148
FOLIO         Qwen2.5 3B Instruct   SFT+             0        14      6           0          66
FOLIO         Qwen2.5 3B Instruct   Incremental      0        14      6           0          71
FOLIO         Qwen3 4B Instruct     ICL              0         0      0           2         188
FOLIO         Qwen3 4B Instruct     SFT+             0         6     12           2          61
FOLIO         Qwen3 4B Instruct     Incremental      0         8     11           1          65
ProntoQA      Gemma3 4B Instruct    ICL              0       187    127         0           118
ProntoQA      Gemma3 4B Instruct    SFT+             6       106     16        10           103
ProntoQA      Gemma3 4B Instruct    Incremental      6       116     11        12           101
ProntoQA      Phi4 mini Instruct    ICL              0       244     21         0           205
ProntoQA      Phi4 mini Instruct    SFT+             0        73      3         0           201
ProntoQA      Phi4 mini Instruct    Incremental      0        87      2         3           146
ProntoQA      Qwen2.5 3B Instruct   ICL              6       184     84         0           192
ProntoQA      Qwen2.5 3B Instruct   SFT+             0        85      8         1           128
ProntoQA      Qwen2.5 3B Instruct   Incremental      0        96      5         0           127
ProntoQA      Qwen3 4B Instruct     ICL              0         3      0         0           483
ProntoQA      Qwen3 4B Instruct     SFT+             0        32      2         0           155
ProntoQA      Qwen3 4B Instruct     Incremental      0        50      1         0            46
ProverQA      Gemma3 4B Instruct    ICL             95         0      0           0         251
ProverQA      Gemma3 4B Instruct    SFT+             4        24      6           0         137
ProverQA      Gemma3 4B Instruct    Incremental      3        26      5           0         119
ProverQA      Phi4 mini Instruct    ICL              3         1      3           0         257
ProverQA      Phi4 mini Instruct    SFT+             2        14      2           0         271
ProverQA      Phi4 mini Instruct    Incremental      5        23      3           0         202
ProverQA      Qwen2.5 3B Instruct   ICL             52         0      0           0         447
ProverQA      Qwen2.5 3B Instruct   SFT+             3        13      1           3         228
ProverQA      Qwen2.5 3B Instruct   Incremental      2        15      2           3         227
ProverQA      Qwen3 4B Instruct     ICL              0         0      0           0         500
ProverQA      Qwen3 4B Instruct     SFT+             1        19      4           0         152
ProverQA      Qwen3 4B Instruct     Incremental      1        24      5           0         118

               Table 6: Error type counts across datasets, models, and methods.
Prompt and a Few-shot Example for ICL Predicate Verification

System:
You are given a premise, a conclusion, and a list of predicates. Check if the predicates correctly represent the premise
and conclusion.
Rules:Watch for arity errors: this happens when the same predicate symbol is used with different numbers of arguments.
Example: Parent(x, y) (2 arguments) vs. Parent(x) (1 argument) → arity error.
If all predicates are correct, output:”correct”
If there are errors, output the corrected list of predicates only

User:
Premise:
If a class has prerequisites, the student must take the prerequisites to take the class. If a class has no prerequisites, then
the student can take the class CPSC 201 and CPSC 223 are prerequisites for CPSC 323. Intro Microeconomics is the
only prerequisite for Intermediate Microeconomics. Intro Geology has no prerequisites.
Conclusion:
Intermediate Microeconomics has one prerequisite.
Predicates:
CanTake(x); CanTake(x, y); Class(x); Prereq(x, y); Student(x); Take(x); Taken(x)
Assistant:
Predicates:
Class(x); Prereq(x, y); Student(x); Take(x, y); CanTake(x, y)

Other Few-Shot Examples

User:
Premises:
Yale University is a private Ivy League research university. Yale University moved to New Haven in 1716. Yale
university’s endowment was valued at 42.3 billion. A list of residential colleges at Yale: Benjamin Franklin College,
Berkeley College, Branford College, Davenport College, Ezra Stiles College, Grace Hopper College, Jonathan Edwards
College, Morse College, Pauli Murray College, Pierson College, Saybrook College, Silliman College, Timothy Dwight
College, and Trumbull College.
Conclusion:
Yale University has the largest university endowment of any educational institution.
Predicates:
Is(x, y); Endowment(x, y); ResidentialCollege(x); ResearchUniversity(x); IvyLeague(x); MoveTo(x, y); List(x, y);
Value(x, y)



              Figure 9: Prompt for Predicate Verification in an ICL setting for Gemma4B Instruct model.
