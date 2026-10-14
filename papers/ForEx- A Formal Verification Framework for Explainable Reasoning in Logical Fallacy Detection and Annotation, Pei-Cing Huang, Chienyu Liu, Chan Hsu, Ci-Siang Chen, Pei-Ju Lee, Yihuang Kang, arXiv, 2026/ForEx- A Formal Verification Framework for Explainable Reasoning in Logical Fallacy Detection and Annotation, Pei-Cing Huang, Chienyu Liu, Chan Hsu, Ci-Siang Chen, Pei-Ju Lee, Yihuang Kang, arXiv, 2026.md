    ForEx: A Formal Verification Framework for
  Explainable Reasoning in Logical Fallacy Detection
                   and Annotation
          Pei-Cing Huang                                      Chienyu Liu                                        Chan Hsu
Department of Information Management              Department of Information Management             Department of Information Management
   National Sun Yat-Sen University                   National Sun Yat-Sen University                  National Sun Yat-Sen University
         Kaohsiung, Taiwan                                 Kaohsiung, Taiwan                                Kaohsiung, Taiwan
       pcpeicing@gmail.com                               c09010011@gmail.com                               chanshsu@gmail.com

            Ci-Siang Chen                                       Pei-Ju Lee                                    Yihuang Kang
Department of Information Management               Graduate Institute of Data Science &            Department of Information Management
   National Sun Yat-Sen University                       Information Computing                        National Sun Yat-Sen University
          Kaohsiung, Taiwan                          National Chung Hsing University                       Kaohsiung, Taiwan
       cisiang.chen@gmail.com                               Taichung, Taiwan                             ykang@mis.nsysu.edu.tw
                                                            pjlee@nchu.edu.tw

     Abstract—Current evaluations of Large Language Models                 In parallel, recent studies have applied symbolic logic to
 (LLMs) on logical fallacy detection focus on predicted labels,        represent argument structures more explicitly [3].
 but do not establish whether those labels are supported by the        Nevertheless, these efforts formalize the input argument rather
 reasoning the models provide. We propose ForEx (Formal                than the model's generated reasoning chain, and satisfiability
 Verification for Explainable Reasoning), a framework that             checking does not establish that the conclusion follows from
 translates LLM-generated explanations into Lean4 and verifies         stated premises. What remains missing is an evaluation
 whether the translated rationale is derivable under encoded           framework that jointly analyzes predicted labels, generated
 premises, not the logical validity of the original natural language
                                                                       explanations, and formal verification outcomes.
 argument. To distinguish prediction outcomes from the formal
 status of the supporting reasoning, we introduce the LLM                  Beyond methodological limitations, evaluation remains
 Argument Verification Matrix, which separates label                   constrained by dataset construction and annotation.
 consistency from formal verification status. Experiments on           Annotation schemes compress interpretive variation into a
 LOGIC-Climate show that over 90% of LLM outputs can be                limited set of labels, even when the same statement admits
 translated into formal reasoning chains that pass verification,       multiple readings [6], [7]. Label-based evaluation may
 while agreement with human annotations remains around 20%.            therefore fail to capture reasoning that is consistent with an
 These results expose a systematic gap between formal                  interpretation not reflected in the annotation.
 derivability and label agreement, a distinction invisible to
 prediction-based metrics. ForEx moves LLM evaluation beyond               Motivated by these challenges, we propose ForEx (Formal
 label correctness toward machine-checkable analysis of                Verification for Explainable Reasoning), a framework that
 formalized reasoning chains.                                          translates LLM-generated explanations into Lean4 and
                                                                       evaluates the formalized self-consistency of the translated
    Keywords— Logical fallacy detection, Formal verification,
 Lean4, LLM reasoning, Consensus-guided annotation                     rationale under encoded premises, rather than the validity or
                                                                       faithfulness of the original natural language argument. A
                        I. INTRODUCTION                                successful Lean4 verification therefore certifies only that the
                                                                       translated conclusion is derivable from the encoded premises
     Large Language Models (LLMs) excel in natural language
                                                                       within the given formalization. By jointly examining
 understanding, yet their logical reasoning capabilities remain        prediction labels, translated rationales, and verification
 difficult to evaluate [1], [2], [3]. Logical fallacy detection has    outcomes, ForEx provides a structured way to identify cases
 thus emerged as a key benchmark for assessing LLMs' ability           in which formally verified reasoning systematically diverges
 to recognize flawed reasoning [4], [5], as it requires
                                                                       from existing annotations. Such cases may suggest that gold
 identifying faulty argumentative structures rather than merely        labels do not fully capture plausible interpretations of the input,
 parsing semantics.                                                    making ForEx useful not only for reasoning verification but
    Existing research on logical fallacy detection has largely         also for downstream annotation analysis and augmentation. In
 focused on improving classification performance through               summary, the contributions of this paper are as follows:
 prompt engineering, few-shot learning, and related inference-              1.   We introduce ForEx, a framework that translates
 time strategies [6]. While these approaches often yield
                                                                                 LLM-generated explanations into Lean4 and enables
 competitive results, their evaluation remains centered on                       machine-checkable analysis of the resulting
 prediction outcomes rather than on whether the model's                          formalized reasoning chains.
 explanation actually supports its label. As a result, correct
 predictions may derive from superficial correlations, with no              2.   We design the LLM Argument Verification Matrix,
 guarantee that the accompanying explanation provides                            which separates label consistency from formal
 genuine support for the predicted label.                                        verification status and exposes mismatches between
                                                                                 label correctness and formal derivability.



 https://github.com/D3-Laboratory/ForEx
    3.   We develop a consensus-guided annotation pipeline                                       However, these approaches evaluate linguistic coherence,
         that combines human annotation standards, multi-                                        factual consistency, or behavioral correctness, rather than
         LLM agreement, and formal verification to support                                       whether a reasoning chain constitutes a formally valid
         annotation analysis and conservative label                                              derivation. As a result, a fluent but structurally fallacious
         augmentation.                                                                           rationale may still pass behavioral verification.
   The remainder of this paper is organized as follows:                                              Compounding these limitations, annotation construction
Section 2 reviews related work. Section 3 presents the ForEx                                     further highlights the limits of label-based evaluation.
framework, including the LLM Argument Verification Matrix                                        Standard annotation practice typically resolves disagreement
and consensus-guided annotation pipeline. Section 4 reports                                      through aggregation, such as majority voting or adjudication,
experimental results on LOGIC-Climate. Section 5 concludes                                       treating disagreement primarily as noise. CrowdTruth 2.0
with future directions.                                                                          instead argues that disagreement can reflect ambiguity in the
                                                                                                 data and should be modeled as a signal rather than discarded
                     II. RELATED WORK                                                            [6]. Pavlick and Kwiatkowski [7] further show that
    Prior work on logical fallacy detection has largely treated                                  disagreements in natural language inference often reflect
the task as supervised classification. Jin et al. [1] introduced                                 multiple valid interpretations of the same text. This issue is
the LOGIC dataset and LogicClimate challenge set with a                                          especially relevant to fallacy detection, where judgments may
structure-aware classifier. Yeh et al. [4] introduced                                            depend on unstated assumptions and alternative reasoning
CoCoLoFa and showed the effectiveness of supervised                                              paths. Compressing such cases into a single gold label can
models for fallacy detection and classification. Lei and Huang                                   therefore obscure plausible interpretations and make
[8] incorporated logical structure trees into LLMs to improve                                    evaluation overly dependent on label agreement rather than
fallacy detection and classification. Despite these advances,                                    reasoning quality [13], [14]. Overall, existing approaches still
prior work measures performance through label prediction,                                        do not directly evaluate whether a model’s predicted label is
which is insufficient for assessing reasoning quality.                                           supported by a reasoning process that can be explicitly
                                                                                                 represented and formally assessed. To address this gap, ForEx
    Complementing classification approaches, structured and                                      sits at the intersection of fallacy detection, argument
symbolic methods encode fallacy definitions as relational                                        formalization, and annotation-disagreement research: it
graphs [9] or capture compositional argument structures                                          translates model-generated explanations into Lean4 to assess
through logical structure trees [8]. The most directly related is                                formal derivability under encoded premises, while using
NL2FOL, which converts input arguments into first-order                                          systematic mismatches between verification outcomes and
logic and checks satisfiability via SMT solvers [3].                                             human labels to support annotation analysis and augmentation.
Nevertheless, NL2FOL formalizes the input argument rather
than the model’s generated reasoning chain, and satisfiability                                             III.
                                                                                                              FORMAL VERIFICATION FOR EXPLAINABLE
checking does not show that the conclusion follows from the                                                               REASONING
stated premises. These approaches therefore do not assess
                                                                                                     We present ForEx, a framework for assessing LLM-
whether model-generated reasoning can be formally derived
                                                                                                 generated reasoning by linking natural language explanations
from encoded premises.
                                                                                                 to formal representations in Lean4. As illustrated in Figure 1,
    Another line of work targets reasoning reliability through                                   the workflow consists of three stages: Reasoning Candidates,
behavioral verification. Chain-of-Verification (CoVe)                                            Execution Feedback & Lean4 Verification, and Label
prompts models to generate verification questions and revise                                     Consistency Evaluation.
their answers accordingly [10], while EVER performs step-
                                                                                                     The framework begins with the Reasoning Candidates
wise hallucination detection and rectification during
                                                                                                 stage, where the Reasoner receives an input statement and
generation [11]. Generator–verifier studies further show that
                                                                                                 generates up to 𝑘 candidates, where 𝑘 is a tunable upper-
verification effectiveness depends strongly on verifier
                                                                                                 bound hyperparameter. Each candidate is represented as a
capability, generator strength, and problem difficulty [12].
                                                                                                 tuple 𝑐! = (𝑓! , 𝑎! , 𝑠! ), where 𝑖 ∈ {1, … , 𝑘}, corresponding

                                             Statement: Now it’s fashionable to blame stalling hurricanes on global warming.

                                                                 𝑪𝒂𝒏𝒅𝒊𝒅𝒂𝒕𝒆𝒔𝒎𝒂𝒙 ≤ 𝒌                                          Reasoning Candidates
                                                                       𝑪𝟏
                                                                       •    Predicted Fallacy (𝑓1 )
                                                                       •    NL Argument (𝑎1 )
                                                                       •    Lean4 Structure (𝑠1 )
                                     Reasoner                                                                                   Modifier
                                                                                        …




                                                                       𝑪𝒌
                                                                        •   Predicted Fallacy (𝑓𝑘 )
                                                                        •   NL Argument (𝑎𝑘 )
                                                                                                                     𝑪𝒊
                                                                        •   Lean4 Structure (𝑠𝑘 )
                                                                                                                             Initial Lean4 Code


                                Execution Feedback ＆ Lean4 Verification                                           Label Consistency Evaluation

                                   NL Argument ( 𝑎𝑖 )    F and 𝒊𝒕𝒆𝒓 ≤ 𝒊𝒕𝒆𝒓𝒎𝒂𝒙                         T or 𝒊𝒕𝒆𝒓 > 𝒊𝒕𝒆𝒓𝒎𝒂𝒙
                                   ＋Error Message



                                                                𝑪𝒊 ′
                                                                                                                                 Checker
                                      Executor                    Revised Lean4 Code (𝑙𝑖𝑖𝑡𝑒𝑟 )




                                         Output: 𝑥, 𝑦 = 𝐿𝑒𝑎𝑛4 𝑉𝑒𝑟𝑖𝑓𝑖𝑐𝑎𝑡𝑖𝑜𝑛, 𝐿𝑎𝑏𝑒𝑙 𝐶𝑜𝑛𝑠𝑖𝑠𝑡𝑒𝑛𝑐𝑦 = 1, 1 → Compilable-Correct


                                                          Fig. 1. Overview of the ForEx Framework



                                                                                           2
 variable {Entity : Type}                                                         TABLE I.      LLM ARGUMENT VERIFICATION MATRIX
 variable (claim evidence : Entity)
                                                                                                            Label Consistency
 variable (is_vague : Entity → Prop)
 variable (lacks_specificity : Entity → Prop)                                                       Match                   Mismatch
 variable (draws_broad_conclusion : Entity → Prop)                                            Compilable-Correct     Compilable-Alternative
                                                                                     Pass
 variable (faulty_generalization : Entity → Prop)                       Lean4                  (Pass & Match)         (Pass & Mismatch)
                                                                        Verifi-
 axiom fg_rule :                                                        cation       Fail    Uncompilable-Correct    Uncompilable-Incorrect
                                                                                                (Fail & Match)         (Fail & Mismatch)
  ∀ {c e : Entity}, is_vague e → lacks_specificity c →
 draws_broad_conclusion c → faulty_generalization c
                                                                       Matrix shown in Table 1. The matrix separates label
 theorem example_fg                                                    consistency from formal verification status, allowing us to
  (h1 : is_vague evidence)                                             analyze whether a model’s predicted label is accompanied by
  (h2 : lacks_specificity claim)                                       a reasoning chain that can be formalized and verified under
  (h3 : draws_broad_conclusion claim) :                                the encoded premises. It is defined by two axes: Lean4
  faulty_generalization claim :=                                       Verification and Label Consistency. Lean4 Verification
  fg_rule h1 h2 h3                                                     indicates whether the revised Lean4 code compiles
                Fig. 2. Example of Lean4 Verification                  successfully in Lean4 (1 = Pass, 0 = Fail). Label Consistency
                                                                       indicates whether the predicted fallacy type matches the
to the Predicted Fallacy, NL Argument, and Lean4 Structure             human annotation (1 = Match, 0 = Mismatch). Importantly, a
shown in Figure 1. Here, 𝑓! denotes the predicted logical              verification pass means that the formalized reasoning chain is
fallacy type, 𝑎! denotes the natural language argument                 derivable under the encoded premises in Lean4; it does not
explaining the reasoning process, and 𝑠! denotes the Lean4
                                                                       by itself guarantee that the formalization fully captures the
structure used to formalize that explanation. These outputs are
                                                                       meaning or logical force of the original natural language
then passed to the Modifier, which converts each 𝑠!
                                                                       statement. The two axes can be represented as a pair [𝑥, 𝑦],
into Initial Lean4 Code for subsequent compilation and
verification.                                                          where 𝑥 denotes Lean4 Verification, and 𝑦 denotes Label
                                                                       Consistency. The four quadrants are defined as follows:
    The second stage, Execution Feedback and Lean4                          • Compilable-Correct Output [1, 1]: The
Verification, attempts to compile the generated Lean4 code.                      formalized reasoning chain compiles successfully in
Let 𝑖𝑡𝑒𝑟 denote the current repair iteration and 𝑖𝑡𝑒𝑟"#$ denote                  Lean4, and the prediction matches the annotation.
the maximum number of permitted repair steps. If the initial                • Compilable-Alternative Output [1, 0]: The
Lean4 code fails to compile (state F), the framework activates
                                                                                 formalized reasoning chain compiles successfully in
an execution-feedback loop while 𝑖𝑡𝑒𝑟 ≤ 𝑖𝑡𝑒𝑟"#$ . In each
                                                                                 Lean4, but the prediction differs from the annotation,
iteration, the Executor receives the compilation error message
together with the original explanation 𝑎! and revises the                        indicating a plausible alternative interpretation.
Lean4 code accordingly. To reduce semantic drift, revisions                 • Uncompilable-Correct Output [0, 1]: The
are constrained to rely only on 𝑎! and the Initial Lean4 Code;                   formalized reasoning chain fails to compile in Lean4,
the Executor is not allowed to introduce new logical content                     but the prediction matches the annotation.
or alter the underlying rationale provided by the Reasoner.                 • Uncompilable-Incorrect Output [0, 0]: The
Each repair step produces an updated candidate 𝐶!% with                          formalized reasoning chain fails to compile in Lean4,
Revised Lean4 Code (𝑙!!&'( ). The process continues until the                    and the prediction differs from the annotation.
code compiles successfully (state T) or the repair budget is               Building on the LLM Argument Verification Matrix, we
exhausted. The resulting candidate is then forwarded to the            design a consensus-guided annotation pipeline to identify
Checker, which evaluates label consistency as described in the         plausible additional labels under human-anchored, cross-
following section.                                                     model consensus. Because logical fallacy detection is treated
                                                                       as a multi-label task in our framework, each statement is
     To clarify what “verification” means in our framework, we         represented as a set of fallacy labels rather than a single class
provide a simplified example of how a model-generated                  assignment.
explanation is translated into Lean4. Consider the statement:
“There’s very strange things going on on planet Earth right                For latent behavioral analysis, each model is represented
now.” A model may classify this statement as Faulty                    as a 14-dimensional feature vector over fallacy categories (13
Generalization on the grounds that it draws a broad conclusion         fallacy types and one no-fallacy category). For each statement
from vague and insufficiently specified evidence. This                 and model, a multi-hot vector is constructed in which each
explanation can be formalized in Lean4 as a rule stating that          dimension indicates whether the corresponding label appears
if the cited evidence is vague, the claim lacks specificity, and       among the model’s verified outputs. If multiple verified labels
the claim draws a broad conclusion, then the claim constitutes         are assigned, the corresponding dimensions are each set to 1
a faulty generalization, as shown in Figure 2. If Lean4 accepts        independently. Averaging these vectors across all evaluated
the proof, this means only that the conclusion is derivable            statements yields a normalized behavioral signature for each
from the encoded premises and rule schema, not that the full           model. Human annotations are encoded in the same space by
meaning of the original natural language statement has been            averaging statement-level multi-hot label vectors across
verified.                                                              statements; unlike model predictions, they are not subject to
                                                                       Lean4 verification and thus capture label distribution rather
   We then evaluate candidates in the Label Consistency                than verified prediction behavior. To characterize global
Evaluation stage using the LLM Argument Verification                   behavioral structure, we project these representations into two



                                                                   3
     TABLE II.   CUMULATIVE PASS RATE (%) ACROSS REPAIR                         original annotated labels recovered by the augmented
         ITERATIONS FOR DIFFERENT REASONER MODELS
                                                                                annotation set.
     Model (T/NT)         Modifier        1st  2nd     3rd      4th
 Claude-sonnet-4.5 (T)      14.63       94.31 100.0 100.0 100.0                               IV. EXPERIMENT AND DISCUSSION
 GPT-5 (T)                  47.89       93.07 98.79 99.99 99.99                     We evaluate ForEx on the LOGIC-Climate dataset [1],
 GPT-oss-120b (T)           37.40       94.49 98.82 100.0 100.0                 which contains 1,074 instances across 13 fallacy categories.
 Deepseek-chat-v3.1 (T)     25.00       93.27 97.59 97.59 97.59                 We sample 10% of the data (107 instances) as a representative
 Deepseek-r1 (T)            39.91       92.96 98.59 98.59 98.59                 subset for empirical evaluation, while preserving category
 Kimi-k2 (T)                49.51       94.75 97.70 98.69 99.02                 balance. We tested 15 Reasoner models spanning both
 Gemini 2.5 flash (T)       22.70       81.32 93.68 95.98 96.84                 thinking and non-thinking variants. For non-thinking models,
 Gemini 2.5 flash (NT)      35.09       88.46 96.63 98.55 99.03                 we apply Chain-of-Thought prompting [15] to externalize
 Gemini 2.5 pro (T)         22.70       81.32 93.68 95.98 96.84                 reasoning into a Lean4-verifiable format. To isolate Reasoner
 Gemini 2.5 pro (NT)        24.48       85.31 95.10 96.50 96.85                 performance from Executor variability, we use Claude Sonnet
 Grok 4 fast (T)            38.40       90.72 97.47 98.73 98.73                 4.5 [16] as the Executor across all experiments, selecting it for
 Grok 4 fast (NT)           38.70       92.57 98.14 99.07 99.38                 its strong performance in structured code generation and
 Qwen3 235B (T)             57.63       93.13 95.80 96.95 97.33                 reliable incorporation of compiler feedback. Across all
 Qwen3 235B (NT)            69.86       95.21 97.26 97.94 97.94                 experiments, we set k ≤ 3, corresponding to the maximum
 GPT-4o (NT)                12.83       92.83 99.62 99.99 99.99                 number of fallacy labels observed per instance, and set the
 Average                    36.70       91.11 97.37 98.39 98.65                 maximum number of repair iterations to 4. Although the
Note. Values are percentages. T/NT denote thinking/non-thinking                 dataset is multi-label, most instances contain only one label
models; 1st–4th denote repair iterations.
                                                                                (84.82% original, 71.96% sampled), which retains multi-
dimensions via PCA, selected for simplicity and                                 fallacy cases while keeping the evaluation computationally
interpretability after observing consistent clustering across                   manageable.
PCA, a linear autoencoder, and a non-negative autoencoder.                          Table 2 reports pass rates across repair iterations. On
    In the reduced space, low-consensus models are identified                   average, 36.70% of Modifier outputs compile without repair,
using Mahalanobis distance; those falling outside the 95%                       rising to 91.11% after one iteration and 98.65% by the fourth,
confidence ellipse are excluded from subsequent                                 indicating gains largely saturate after the first repair round.
augmentation. After filtering, we quantify statement-level                      Within each model pair, thinking variants show lower pass
disagreement using pairwise Jaccard distance. For each                          rates than their non-thinking counterparts, likely because they
statement 𝑠, let A = {A) , … , A* } denote the label sets of all 𝑀              generate more complex Lean4 structures that are harder to
annotation sources (retained models and the human                               compile and repair. Remaining failures are categorized as
annotation). The disagreement score is defined as:                              Syntax Failure (SF).
                          )                                                         Table 3 reports model performance under the LLM
          Score(s) = ! ∑-/. JaccardDistJA- , A. K                     (1)
                        +",                                                     Argument Verification Matrix, which distinguishes formal
                                                                                verification status from label correctness. Quadrants are
Averaging over all pairs ensures comparability even if the                      ordered by priority: Compilable-Correct (CC) > Compilable-
number of retained models varies. Statements at or below the                    Alternative (CA) > Uncompilable-Correct (UC) >
first quartile are treated as high-consensus and retained for                   Uncompilable-Incorrect (UI). CC+CA serves as the primary
label augmentation.                                                             signal, capturing all predictions accompanied by a compilable
    For each retained statement, a label is added to the                        reasoning chain regardless of label outcome. We evaluate
augmented annotation if at least 50% of retained models                         predictions at the label level, assigning each predicted label to
assign it under verification. Augmented annotations are then                    a matrix category to preserve information in the multi-label
evaluated against the original human annotations using recall                   setting. Because models may output fewer
over statement-label pairs, defined as the proportion of
                     TABLE III.       MODEL PERFORMANCE AND ERROR ANALYSIS UNDER THE ARGUMENT VERIFICATION MATRIX

              Model (T/NT)            Count     CC+CA↑         CC↑         CA↑         UC↓           UI↓          VF↓          NF          SF↓
        Claude-sonnet-4.5 (T)           227       93.84        22.91      70.93        0.88         5.29          2.20         2.64        0.44
        GPT-5 (T)                       290       97.59        17.93      79.66        0.34         2.07          0.69         1.38        0.00
        GPT-oss-120b (T)                234       97.01        20.51      76.50        0.00         2.99          0.00         2.99        0.00
        Deepseek-chat-v3.1 (T)          193       90.16        20.21      69.95        1.04         9.33          1.04         5.70        2.59
        Deepseek-r1 (T)                 201       92.04        22.39      69.65        0.50         7.96          0.00         5.97        1.99
        Kimi-k2 (T)                     276       94.20        18.48      75.72        1.45         5.43          0.72         3.62        1.09
        Gemini 2.5 flash (T)            229       89.52        21.40      68.12        2.62         7.86          6.11         0.44        1.31
        Gemini 2.5 flash (NT)           195       90.77        22.05      68.72        1.03         8.21          3.08         4.10        1.03
        Gemini 2.5 pro (T)              302       91.72        17.88      73.84        0.99         7.62          3.31         0.66        3.64
        Gemini 2.5 pro (NT)             248       91.13        19.76      71.37        2.02         6.85          3.23         0.40        3.23
        Grok 4 fast (T)                 215       90.70        20.93      69.77        0.47         8.84          2.33         5.12        1.40
        Grok 4 fast (NT)                279       96.41        17.92      78.49        1.08         2.87          1.79         0.36        0.72
        Qwen3 235B (T)                  237       92.40        20.25      72.15        0.00         7.59          2.11         2.95        2.53
        Qwen3 235B (NT)                 259       94.59        22.39      72.20        1.16         4.25          1.93         1.16        1.16
        GPT-4o (NT)                     236       96.61        22.88      73.73        0.00         3.39          0.85         2.54        0.00
           Note. Values are percentages. T/NT denote thinking/non-thinking models; ↑ higher is better; ↓ lower is better. Best values are bold.




                                                                            4
                                                                       annotations with 0.77 recall against the original human
                                                                       annotations, indicating that most original labels are preserved
                                                                       by the augmented set. The newly added labels are formally
                                                                       supported and retained through consensus-guided filtering,
                                                                       but their status as gold annotations remains to be confirmed.
                                                                           The following discussion distinguishes observed patterns
                                                                       from their possible interpretations. First, the prevalence of CA
                                                                       outputs suggests that many formally supported predictions
                                                                       may reflect plausible alternative interpretations rather than
                                                                       simple errors (Appendix, Case 1), though this interpretation
                                                                       remains tentative. Second, NF predictions often appear in
                                                                       context-limited cases. Prior analysis of LOGIC-Climate
                                                                       shows that 40% of errors stem from isolated arguments
                                                                       [20], and Appendix Case 2 illustrates how some NF
                                                                       predictions can appear plausible under limited-context reading,
                                                                       possibly because annotators had access to broader discourse
                                                                       context not available to the models. Third, the limited number
                                                                       of consensus augmentations (27 statements) reflects the
       Fig. 3. PCA Model Clustering with Mahalanobis Distance          strictness of our criterion, which retains only interpretations
                                                                       supported by multiple LLMs and the human annotation.
than 𝑘 labels for a given instance, Count denotes the number           Fourth, the low UC rate (<2%) indicates that correct labels
of evaluated label-level predictions for each model rather than        rarely co-occur with unverified reasoning chains in our setting.
the number of instances. The UI category is further                        While these findings provide insights into LLM reasoning,
decomposed into Verification Failure (VF), No Fallacy (NF),            several limitations warrant discussion. The plausibility of CA
and Syntax Failure (SF) to distinguish between distinct failure        predictions cannot be confirmed without clearer evidence
modes.                                                                 about annotator methodology. In addition, formal verification
                                                                       does not guarantee semantic alignment between the
         The combined CC+CA metric is consistently high                formalized reasoning and the original natural language
across models and typically exceeds 90%, with the top value            statement. Under limited context, derivable reasoning chains
reaching 97.59%. In contrast, CC scores show greater                   may still be misaligned with human interpretation. More
variation across models. Claude-sonnet-4.5 (22.91%), GPT-              broadly, because natural language lacks a fully specified
4o (22.88%) [17], and Deepseek-r1 (22.39%) [18] achieve                semantic foundation, formal verification results may overstate
the highest CC scores. This gap between CC and CC+CA                   model capability. Finally, NF errors within UI may arise from
indicates that many formally verified outputs fall into the CA         either insufficient semantic understanding or loss of
category, pointing to plausible readings not captured by the           contextual information, and the current framework does not
annotated labels.                                                      distinguish between these explanations. Regarding the
                                                                       annotation pipeline, cases exhibiting systematic model-human
                                                                       divergence may be filtered out by the augmentation criterion
    UC remains consistently low across models, generally
                                                                       (Appendix, Case 3). The augmentation results should
below 2%, suggesting that correct labels rarely arise without a
                                                                       therefore be interpreted as a demonstration of conservative,
verifiable reasoning chain. Within UI, NF is the dominant
                                                                       consensus-guided label expansion rather than evidence of
failure mode, especially in the Deepseek series [18], [19]. One
                                                                       annotation quality improvement.
possible explanation is that isolated single-sentence inputs
omit contextual information needed for reliable fallacy                   Additional case-level examples, including model
detection, which may also contribute to mismatches with                predictions, Lean4 translations, verification outcomes, and
human annotations. By contrast, VF and SF remain                       annotation-consensus results, are available in the project
comparatively rare, with most values below 3% and 2%,                  repository: https://github.com/D3-Laboratory/ForEx
respectively, indicating that failures are more often associated
with label mismatch than with verification or syntax                                         V. CONCLUSION
breakdown.                                                                 This paper addresses a key challenge in logical fallacy
   Motivated by the prevalence of CA outputs, we apply a               detection: evaluation is typically centered on label correctness,
consensus-guided annotation pipeline to identify additional            while the formal status of the supporting reasoning is rarely
supported labels. Figure 3 shows the PCA projection of the             assessed separately. To address this limitation, we propose
LLMs and the human annotation profile. Most models cluster             ForEx, a framework that links natural language explanations
near the human annotation profile, and no models are                   to Lean4 representations, along with an LLM Argument
identified as outliers under the Mahalanobis distance criterion        Verification Matrix that decouples label correctness from
(95% confidence ellipse).                                              formal verification status. We further introduce a consensus-
                                                                       guided annotation pipeline for analyzing agreement patterns
    We next examine statement-level disagreement using the             between human annotations and multi-LLM predictions.
Jaccard-based score. The median distance across all
statements is 0.63 (Q1: 0.56, Q3: 0.71). Statements at or below            Experiments demonstrate that formal verification can be
the first quartile threshold are treated as high-consensus and         used to assess whether model-generated reasoning chains are
comprise approximately 25% of the dataset. Applying the                derivable under encoded premises. The results also reveal a
50% support criterion within this subset yields augmented              substantial gap between verification outcomes and agreement
                                                                       with existing human labels. These findings suggest that label-


                                                                   5
based evaluation and formal verification capture different                         [13] Z. Liu et al., “Self-contradictory reasoning evaluation and detection,”
aspects of model behavior. Future work will focus on                                     in Findings of the Association for Computational Linguistics: EMNLP
                                                                                         2024, Miami, Florida, USA: Association for Computational
improving the alignment between formal verification                                      Linguistics, 2024, pp. 3725–3742. doi: 10.18653/v1/2024.findings-
outcomes and semantic correctness by extending the                                       emnlp.213.
framework to richer argument structures, incorporating                             [14] F. M. Molfese, L. Moroni, L. Gioffré, A. Scirè, S. Conia, and R.
contextual information, and integrating semantic consistency                             Navigli, "Right Answer, Wrong Score: Uncovering the Inconsistencies
checks.                                                                                  of LLM Evaluation in Multiple-Choice Question Answering," in
                                                                                         Findings of the Association for Computational Linguistics: ACL 2025,
                       ACKNOWLEDGEMENT                                                   Vienna, Austria: Association for Computational Linguistics, 2025, pp.
                                                                                         18477–18494. doi: 10.18653/v1/2025.findings-acl.950.
      This work was supported by the Taiwan Comprehensive                          [15] J. Wei, X. Wang, D. Schuurmans, M. Bosma, B. Ichter, F. Xia, E. Chi,
                   University System (TCUS).                                             Q. Le, and D. Zhou, "Chain-of-Thought Prompting Elicits Reasoning
                                                                                         in Large Language Models," Jan. 28, 2022, arXiv: arXiv:2201.11903.
                                REFERENCE                                                doi: 10.48550/arXiv.2201.11903.
                                                                                   [16] “Introducing Claude Sonnet 4.5.” Accessed: Nov. 24, 2025. [Online].
[1]  Z. Jin, A. Lalwani, T. Vaidhya, X. Shen, Y. Ding, Z. Lyu, M. Sachan,                Available: https://www.anthropic.com/news/claude-sonnet-4-5
     R. Mihalcea, and B. Schölkopf, "Logical Fallacy Detection," in                [17] OpenAI et al., “GPT-4o System Card,” Oct. 25, 2024, arXiv:
     Findings of the Association for Computational Linguistics: EMNLP                    arXiv:2410.21276. doi: 10.48550/arXiv.2410.21276.
     2022, Abu Dhabi, United Arab Emirates: Association for                        [18] DeepSeek-AI et al., “DeepSeek-R1: Incentivizing Reasoning
     Computational      Linguistics,    2022,    pp.    7180–7198.      doi:             Capability in LLMs via Reinforcement Learning,” Jan. 22, 2025, arXiv:
     10.18653/v1/2022.findings-emnlp.532.                                                arXiv:2501.12948. doi: 10.48550/arXiv.2501.12948.
[2] G. Lim and S. T. Perrault, “Evaluation of an LLM in Identifying                [19] deepseek-ai/DeepSeek-V3. (Nov. 23, 2025). Python. DeepSeek.
     Logical Fallacies: A Call for Rigor When Adopting LLMs in HCI                       Accessed:       Nov.      24,      2025.     [Online].     Available:
     Research,” Apr. 09, 2024, arXiv: arXiv:2404.05213. doi:                             https://github.com/deepseek-ai/DeepSeek-V3
     10.48550/arXiv.2404.05213.                                                    [20] T. Calamai, O. Balalau, and F. M. Suchanek, "Benchmarking the
[3] A. Lalwani, T. Kim, L. Chopra, C. Hahn, Z. Jin, and M. Sachan,                       Benchmarks: Reproducing Climate-Related NLP Tasks," in
     “Autoformalizing natural language to first-order logic: A case study in             Proceedings of the 63rd Annual Meeting of the Association for
     logical fallacy detection,” in Proc. 14th Int. Joint Conf. Natural                  Computational Linguistics, Vienna, Austria: Association for
     Language Process. and 4th Conf. Asia-Pacific Chapter Assoc. Comput.                 Computational Linguistics, Jul. 2025.
     Linguistics, Mumbai, India, 2025, pp. 132–147, doi:
     10.18653/v1/2025.findings-ijcnlp.8.                                                          APPENDIX. CASE ANALYSIS EXAMPLES
[4] M.-H. Yeh, R. Wan, and T.-H. K. Huang, “CoCoLoFa: A Dataset of
     News Comments with Common Logical Fallacies Written by LLM-                   Case 1. Label Mismatch Under Limited Context
     Assisted Crowds,” in Proceedings of the 2024 Conference on                    -   Statement: For good reason: In the U.S., and for much of the world, the
     Empirical Methods in Natural Language Processing, Miami, Florida,                 most dangerous environmental pollutants have been cleaned up. U.S.
     USA: Association for Computational Linguistics, 2024, pp. 660–677.                emissions of particulates, metals, and varied gases, all of these: ozone,
     doi: 10.18653/v1/2024.emnlp-main.39.                                              lead, carbon monoxide, oxides of nitrogen, and sulfur, fell almost 70 %
[5] Y. Li et al., “Reason from Fallacy: Enhancing Large Language Models’               between 1970 and 2014.
     Logical Reasoning through Logical Fallacy Understanding,” in                  -   Model Prediction: Faulty Generalization (15/15 models)
     Findings of the Association for Computational Linguistics: NAACL              -   Human Annotation: Ad Hominem
     2024, Mexico City, Mexico: Association for Computational                      -   Analysis: All models predicted Faulty Generalization based on the
     Linguistics, 2024, pp. 3053–3066. doi: 10.18653/v1/2024.findings-                 isolated statement. The human annotation reflects a different
     naacl.192.                                                                        interpretation from the model predictions. One possible explanation is
[6] A. Dumitrache, O. Inel, L. Aroyo, B. Timmermans, and C. Welty,                     that the isolated sentence omits contextual information relevant to
     “CrowdTruth 2.0: Quality Metrics for Crowdsourcing with                           fallacy identification, suggesting that single-sentence inputs may
     Disagreement,” Aug. 18, 2018, arXiv: arXiv:1808.06080. doi:                       provide insufficient cues for reliable classification.
     10.48550/arXiv.1808.06080.
[7] E. Pavlick and T. Kwiatkowski, "Inherent Disagreements in Human                Case 2. No Fallacy (NF)
     Textual Inferences," Transactions of the Association for                      -   Statement: Barrie now works for the Climate Change Institute at
     Computational Linguistics, vol. 7, pp. 677–694, 2019, doi:                        Australian National University, Canberra.
     10.1162/tacl_a_00293.                                                         -   Model Prediction: No Fallacy (14/15 models)
[8] Y. Lei and R. Huang, “Boosting Logical Fallacy Reasoning in LLMs               -   Human Annotation: Intentional Fallacy
     via Logical Structure Tree,” in Proceedings of the 2024 Conference on         -   Analysis: The statement appears factually neutral in isolation, leading
     Empirical Methods in Natural Language Processing, Miami, Florida,                 most models to predict No Fallacy. The mismatch with the human
     USA: Association for Computational Linguistics, 2024, pp. 13157–                  annotation suggests that the assigned label may depend on information
     13173. doi: 10.18653/v1/2024.emnlp-main.730.                                      not recoverable from the single sentence alone, illustrating the difficulty
[9] O. P. Wang, T. Bansal, R. Bai, E. M. Chui, and L. H. Gilpin, "Follow               of fallacy detection under limited context.
     My Lead: Logical Fallacy Classification with Knowledge-Augmented
     LLMs," Oct. 11, 2025, arXiv: arXiv:2510.09970. doi:                           Case 3. Systematic Label Mismatch Under Argument-Level
     10.48550/arXiv.2510.09970.                                                    Reasoning
[10] S. Dhuliawala et al., “Chain-of-Verification Reduces Hallucination in         -   Statement: There are no carbon emissions, because carbon is a solid
     Large Language Models,” in Findings of the Association for                        and most carbon is black and soot, which are solids.
     Computational Linguistics ACL 2024, Bangkok, Thailand and virtual             -   Model Prediction: Equivocation (12/15 models), False Causality
     meeting: Association for Computational Linguistics, 2024, pp. 3563–               (11/15 models)
     3578. doi: 10.18653/v1/2024.findings-acl.212.                                 -   Human Annotation: Fallacy of Logic
[11] H. Kang, J. Ni, and H. Yao, “Ever: Mitigating Hallucination in Large          -   Analysis: Most models predicted Equivocation or False Causality based
     Language Models through Real-Time Verification and Rectification,”                on local cues such as the repeated use of “carbon” or the apparent causal
     Feb.       25,     2024,       arXiv:     arXiv:2311.09114.        doi:           structure. In contrast, the human label, Fallacy of Logic, reflects a
     10.48550/arXiv.2311.09114.                                                        broader argument-level judgment that the inference is invalid. This
[12] Y. Zhou, A. Xu, Y. Zhou, J. Singh, J. Gui, and S. Joty, “Variation in             suggests that models may rely on local cues rather than assessing overall
     Verification: Understanding Verification Dynamics in Large                        argument validity. The case was excluded from label augmentation due
     Language Models,” Sep. 22, 2025, arXiv: arXiv:2509.17995. doi:                    to high Jaccard disagreement, showing that the pipeline can filter out
     10.48550/arXiv.2509.17995.                                                        high-divergence model–human mismatches.




                                                                               6
