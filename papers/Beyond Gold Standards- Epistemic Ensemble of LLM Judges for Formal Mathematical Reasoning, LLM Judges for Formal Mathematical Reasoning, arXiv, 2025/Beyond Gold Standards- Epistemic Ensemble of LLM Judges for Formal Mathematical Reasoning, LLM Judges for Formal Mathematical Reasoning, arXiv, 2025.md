                                                                 Beyond Gold Standards: Epistemic Ensemble of
                                                                LLM Judges for Formal Mathematical Reasoning
                                                           Lan Zhang1 , Marco Valentino2 , Jordan Meadows3 , André Freitas1,3,4
                                                      1
                                                        Department of Computer Science, University of Manchester, United Kingdom
                                                            2
                                                              School of Computer Science, University of Sheffield, United Kingdom
                                                                            3
                                                                              Idiap Research Institute, Switzerland
                                                         4
                                                           National Biomarker Centre, CRUK Manchester Institute, United Kingdom
                                                                         lan.zhang-6@postgrad.manchester.ac.uk

                                                                   Abstract                               ematics has received growing attention in recent
                                                                                                          years (Jiang et al., 2023b; Xin et al., 2025; Lin
                                                 Statement autoformalization plays a crucial
arXiv:2506.10903v2 [cs.CL] 21 Aug 2026




                                                 role in formal mathematical reasoning by en-             et al., 2025; Ahuja et al., 2025; Poesia et al., 2024;
                                                 abling the automatic translation of natural lan-         Yu et al., 2025; Yang et al., 2024). Autoformal-
                                                 guage statements into formal languages. While            ization, which serves as a bridge between natural
                                                 recent advances using large language models              language and formal language domains, plays a
                                                 (LLMs) have shown promising capability of                critical role in improving accessibility to formal
                                                 autoformalization, methods for automatically             verification tools for formal reasoning (Pan et al.,
                                                 evaluating autoformalization remain underex-
                                                                                                          2023; Quan et al., 2025, 2024b). Despite recent ad-
                                                 plored. LLM-as-a-judge presents a promising
                                                 approach for automating such evaluation, how-            vances in autoformalization with LLMs (Wu et al.,
                                                 ever, existing methods typically employ coarse-          2022; Zhang et al., 2024), its evaluation remains a
                                                 grained and generic evaluation criteria, which           long-standing challenge. While syntactic correct-
                                                 limit their effectiveness for advanced formal            ness (Zhang et al., 2024, 2025a,b) can be rigor-
                                                 mathematical reasoning, where quality hinges             ously verified using theorem provers (TPs) such
                                                 on nuanced, multi-granular dimensions. In this           as Isabelle (Paulson, 2000) or Lean (de Moura
                                                 work, we take a step toward addressing this gap          et al., 2015), assessing semantic alignment or con-
                                                 by introducing a systematic, automatic method
                                                                                                          sistency (Zhang et al., 2024) between natural and
                                                 to evaluate autoformalization tasks. The pro-
                                                 posed method is based on an epistemically and            formal language statements is still a significant
                                                 formally grounded ensemble (EFG) of LLM                  open problem.
                                                 judges, defined on criteria encompassing log-               While human experts can provide direct as-
                                                 ical preservation (LP), mathematical consis-             sessments, formalizations in highly specialized
                                                 tency (MC), formal quality (FQ), and formal              domains are extremely time-consuming to eval-
                                                 validity (FV), resulting in a transparent assess-        uate and prone to errors. Human evaluation be-
                                                 ment that accounts for different contributing
                                                                                                          comes particularly challenging when dealing with
                                                 factors. We validate the proposed framework
                                                 to serve as a proxy for autoformalization as-            increasingly complex and novel mathematical ob-
                                                 sessment within the domain of formal mathe-              jects (Zhang et al., 2025a), where the required back-
                                                 matics. Overall, our experiments demonstrate             ground knowledge grows substantially. This cre-
                                                 that the EFG ensemble of LLM judges is a                 ates a clear scalability bottleneck for autoformal-
                                                 more suitable emerging proxy for evaluation              ization evaluation.
                                                 than a coarse-grained model. These findings                 On the other hand, although reference-based met-
                                                 suggest that LLM-as-judges, especially when              rics (Li et al., 2024; Poiroux et al., 2025a; Liu et al.,
                                                 guided by a well-defined set of atomic proper-
                                                                                                          2025a) enable automatic evaluation, they introduce
                                                 ties, could offer a scalable, interpretable, and
                                                 reliable support for evaluating formal mathe-            several limitations: (i) they require ground-truth
                                                 matical reasoning.1                                      formalizations to be correct, which has already
                                                                                                          been identified as an issue in formal benchmarks
                                                                                                          such as ProofNet (Poiroux et al., 2025a); (ii) they
                                         1       Introduction
                                                                                                          rely on models to infer equivalence, which may in-
                                         With the increasing capabilities of large lan-                   troduce errors that are unrelated to the quality of the
                                         guage models (LLMs), reasoning in formal math-                   formalization itself; and (iii) they depend heavily
                                             1
                                             Code and datasets are available at https://github.com/       on a formal execution environment and thereby are
                                         lanzhang128/autoformalization_evaluation                         constrained by syntactic correctness, even though

                                                                                                      1
                   (1) A Taxonomy for Autoformalization Evaluation                                                                              (2) Autoformalization Task

                                                                            Pre-arg Structure                                                                                                    Formalization:
                                                           Proposition                          NL Statement:
                                                            Structure                                                                                                                            theory aime_1983_p9 imports
                                                                                                Find the minimum value of                 for                                                      Complex_Main
                                                                             Quantification                . Show that it is 012.                                                                begin
                                                                                                                                                                                                 theorem aime_1983_p9:
                                                                  Formula                                                                                                                         ...
                                        Logical                                                                                                        Autoformalization Model
                                      Preservation                                                                                                             (LLM)                                                     Isabelle/Lean
                                                                                Relation
                    Alignment                                                                                                                         (3) Evaluation
                   Faithfulness                              Concept
                                                                                                          Existing Evaluation Paradims
                                      Mathematical                                                                                                                                                                   Scalable
                                                                                Constant
                                      Consistency                                                                                                              Formalization
                                                                                                                                                                                                                  Fine-Grained
   Formalization                                             Operator                                                          Scalable
      Quality
                                                                                                                             Fine-Grained                                                 Epistemic Ensemble of
                                                                                                                                                                                               LLM Judges
                                                           Conciseness                              Human Evaluation
                                                                                                                                                                       Aspect #1
                                                                                                                                                                   Logical Preservation           ...                Aspect #n
                                                                                                                                                                                                               Mathematical Consistency
                                        Formal                                                                                                                      Judgment: False                               Judgement: True
                                        Quality
                   Formalization                             Logical                                                           Scalable
                                                                                                                                                                                           Linear Combination
                    Correctness                            Consistency
                                        Formal                                                                               Fine-Grained
                                        Validity
                                                                                                     Coarse-grained
                                                                                                     LLM-as-a-Judge                                                                       Overall Evaluation




Figure 1: Overview of the proposed framework for automatically evaluating autoformalization. Our method
leverages ensembles of LLM judges based on epistemic criteria organized into a taxonomy, while also providing
explanations for their judgments. A linear evaluation model aggregates the criteria into a single overall assessment
to serve as a proxy for human evaluation.


syntactically incorrect code may still be semanti-                                                       To validate the proposed framework, we conduct
cally meaningful and useful for refinement. These                                                     human evaluations of rankings on Lean4, using
limitations highlight the need for reference-free                                                     both human-written formalizations from existing
evaluation methods for autoformalization.                                                             datasets (Zheng et al., 2022; Azerbayev et al., 2023)
   In this paper, we take a step toward address-                                                      and LLM-generated formalizations. We further an-
ing this gap by introducing a systematic reference-                                                   alyze how LLM judges and human differ in the
free method for evaluating autoformalization for                                                      extent to which individual dimensions contribute
formal mathematical reasoning. The proposed                                                           to the final assessment when evaluating flawed for-
method is based on an epistemically and formally                                                      malizations on both Lean4 and Isabelle/HOL. Fi-
grounded (EFG) ensemble2 of LLM Judges (Zheng                                                         nally, we examine whether an ensemble of LLM
et al., 2023), grounded on a taxonomy for multi-                                                      judges (EFG) can reliably produce consistent and
dimensional autoformalization evaluation. We                                                          less biased overall evaluations, thereby supporting
break down the components involved within the                                                         a fully automated evaluation protocol that mini-
context of autoformalization tasks and organize                                                       mizes human involvement while complementing
them into a taxonomy composed of four core as-                                                        human judgment.
pects: logical preservation (LP), mathematical con-                                                      Overall, our experiments demonstrate that fine-
sistency (MC), formal quality (FQ), and formal                                                        grained LLM judges are generally more effective
validity (FV), along with a set of atomic proper-                                                     than coarse-grained LLM judges and achieve rank-
ties that serve as computable estimators of these                                                     ing agreement comparable to that of human eval-
features. We hypothesize that such properties can                                                     uators. Our contributions can be summarized as
serve as an effective proxy for human evaluators in                                                   follows:
mathematical autoformalization settings. Specifi-
                                                                                                          1. We introduce an epistemically and formally
cally, in this framework (Figure 1), LP, MC, and FQ
                                                                                                             grounded (EFG) taxonomy for formal mathe-
are assessed by LLM judges, while FV is verified
                                                                                                             matical reasoning, encompassing key dimen-
using theorem provers. A linear evaluation model
                                                                                                             sions such as logical preservation, mathemati-
that integrates the estimators into a unified, inter-
                                                                                                             cal consistency, formal quality, and formal va-
pretable evaluation outcome, enabling scalable,
                                                                                                             lidity. These dimensions are operationalized
multi-dimensional, and automated assessment.
                                                                                                             through a set of interpretable atomic proper-
    2
     The "ensemble" term used in this paper refers to using the                                              ties serving as estimators.
same backend LLM to assess different aspects, unlike setups
with multiple backend LLMs judging the same aspect. While                                                 2. We develop a fine-grained and interpretable
more diverse models for different aspects could enhance gener-
alizability, our results confirm that a single-backend ensemble                                              framework for automatic evaluation of auto-
suffices for reliable evaluation.                                                                            formalization based on this taxonomy, which

                                                                                                2
    Case 1: miniF2F Isabelle             Case 2: Proofnet Lean4                       Case 3: miniF2F Lean4
    Unpreserved Logic                    Inconsistent Mathematics                     Redundant Hypothesis
    Find     the minimum value of        Let A be a nonempty set of real numbers      Simplify (2 − 2i)(5 + 5i), where
    9x2 sin2 x+4
        x sin x
                  for 0 < x < π. Show    which is bounded below. Let −A be the set    i2 = −1. Show that it is 20.
    that it is 012.                      of all numbers −x, where x ∈ A. Prove that   theorem mathd_algebra_110
    theorem aime_1983_p9:                inf A = − sup(−A).                            (q e : C)
     fixes x::real                       theorem exercise_1_5                          (h0 : q = 2 − 2 * Complex.I)
     assumes "0<x" "x<pi"                 (A minus_A : Set R) (hA : A.Nonempty)        (h1 : e = 5 + 5 * Complex.I) :
     shows "12 ≤ ((9 * (x^2 *             (hA_bdd_below : BddBelow A)                  q * e = 20 := sorry
       (sin x)^2)) + 4) / (x * sin x)"    (hminus_A : minus_A = {x | −x ∈ A}) :
       sorry                              Inf A = Sup minus_A :=sorry

                            Table 1: Typical challenges involved in formalization evaluation.


       aggregates outputs from LLM judges special-               dataset can provide more nuanced insights, but they
       ized in the defined atomic properties via a               require human effort and tend to be tied to the par-
       linear ensemble.                                          ticular combination of dataset, model, and formal
                                                                 language, limiting their generalizability to other
    3. We investigate the impact of coarse-grained
                                                                 settings. To this end, we aim to obtain an autofor-
       versus fine-grained evaluation designs using
                                                                 malization evaluation function that has a twofold
       human evaluation. Our findings show that
                                                                 purpose: (i) serving as an automated proxy for
       smaller LLMs guided by EFG criteria can
                                                                 human evaluators and (ii) providing a qualitative
       outperform larger LLMs relying on coarse-
                                                                 description around a set of formalization properties,
       grained judgments.
                                                                 while being agnostic towards any particular solver.
    4. We empirically validate the effectiveness of                 To illustrate the broader evaluation challenge, we
       EFG ensembles for autoformalization evalu-                present examples from human-validated, ground-
       ation. Results show strong agreement with                 truth formalizations in commonly used datasets in
       human rankings, no evidence of cross-model-               Table 1. In Case 1, the original natural language
       family bias, and robustness to sampling vari-             statement explicitly asks for the minimum value,
       ability, indicating that EFG ensembles serve              but the formalization merely asserts a lower bound
       as reliable proxies for evaluating formaliza-             for the expression, omitting the critical informa-
       tion quality.                                             tion that the minimum is actually attained for some
                                                                 value of x. This highlights a failure to preserve the
2     Methodology
                                                                 underlying logical intent of the natural language.
2.1    Formalization Evaluation                                  In Case 2, the formalization omits a negation on
Mathematical autoformalization is the task of au-                the right-hand side of an equality, contradicting
tomatically transforming an informal mathemati-                  the natural language statement and revealing a se-
cal statement s, expressed in natural language and               mantic inconsistency in the mathematical content.
LaTeX symbols from domain S, into a formal rep-                  In Case 3, while the formalization is semantically
resentation ϕ within a formal language F (Zhang                  correct, it introduces unnecessary variables and hy-
et al., 2024). Formalization evaluation refers to the            potheses, increasing complexity and redundancy,
systematic assessment of the correctness of a can-               an undesirable property for concise and readable
didate formalization (produced either by a human                 formalizations. Motivated by these observations,
or a model) and the assignment of an evaluation                  we propose a fine-grained taxonomy for formaliza-
function (either a score or a binary function). The              tion evaluation that systematically qualifies a set of
conventional evaluation approach relies on human                 target properties that should be satisfied.
judgment of correctness, often based on syntactic
                                                                 2.2 A Taxonomy for Formalization Evaluation
validity within a theorem prover, and typically re-
sults in a binary score (e.g. pass). However, such               We start by introducing a taxonomy which elic-
binary assessment treats all incorrect formaliza-                its the constituting parts entailed by a formaliza-
tions equally and fails to convey a more detailed                tion evaluation framing a set of well-defined com-
qualitative feedback.                                            putable properties (Figure 1):
   Case studies (Wu et al., 2022) of autoformaliza-              Tier 1. A correct candidate formalization ϕ of a
tions produced by a particular model on a specific               natural language statement s should satisfy two key

                                                             3
properties:                                                 weights wLP , wMC , wFQ , wFV > 0 satisfy the con-
1. Alignment Faithfulness (AF): As a representa-            straint wLP + wMC + wFQ + wFV = 1.
tion of s in the formal domain, ϕ must accurately
capture the intended semantics of s from the natural        3     Empirical Validation
language domain.
                                                            3.1     Alignment Between LLM Judges and
2. Formalization Correctness (FC): As a con-
                                                                    Human Rankings
struct within the formal domain, ϕ must be valid,
natural and well-formed within the conventions of           We first evaluate how well LLM judges with dif-
the target formalism.                                       ferent settings can rank formalizations compared
Tier 2 for AF. To ensure that a formalization ϕ             with human evaluation. To this end, we first ran-
faithfully represents a source statement s, it is es-       domly sample 50 natural language statements from
sential that ϕ maintains the logical structure and          the validation split of miniF2F (Zheng et al., 2022)
mathematical intent inherent in s. We introduce             and another 50 from ProofNet (Azerbayev et al.,
two conceptual properties to characterize this align-       2023). We then ask two human evaluators to inde-
ment:                                                       pendently rank 3 formalizations from three sources:
1. Logic Preservation (LP) captures the degree to           human-written ground truth, GPT-4.1 (OpenAI,
which the logical content and inferential structure         2024) zero-shot autoformalization, and Qwen2.5-
of s is preserved within ϕ.                                 7B (Qwen, 2025) few-shot autoformalization (8
2. Mathematical Consistency (MC) reflects how               exemplars), while also providing an overall assess-
coherently and accurately the mathematical objects          ment on a 5-point scale (criteria shown in Table 6
and operations present in s are represented in ϕ.           in Appendix A). We use two accuracy-based met-
Tier 2 for FC. To clarify the intrinsic properties,         rics, exact match (EM) and pairwise match (PM)
which can be assessed independently of any source           of rankings, to measure agreement between the
statement s, of a formalization ϕ, we present the           two human evaluators. The EM and PM scores are
following conceptual properties:                            38.00% and 70.00% on miniF2F, and 22.00% and
                                                            68.67% on ProofNet. From the human evaluations,
1. Formal Quality (FQ) captures the structural
                                                            we observe three findings: (1) even human evalua-
clarity and conciseness of ϕ (e.g. non-redundant
                                                            tors can disagree substantially on the exact rankings
statements).
                                                            of formalizations from multiple sources; (2) agree-
2. Formal Validity (FV) refers to whether ϕ is
                                                            ment on pairwise rankings is higher, though notable
syntactically valid within the target formal system.
                                                            disagreement remains; and (3) human evaluators
A formally valid expression conforms to all gram-
                                                            find it more difficult to agree on formalizations of
matical and structural rules of the formal language.
                                                            more complex natural language statements (e.g.,
Tier 3 - Operable Atomic Properties (OAPs).
                                                            from ProofNet) than on formalizations of simpler
The properties previously articulated are then ma-
                                                            statements (e.g., from miniF2F).
terialized into a set of Operable Atomic Properties
(OAPs), which are functions designed to be both in-         3.1.1    Results & Discussions
terpretable and computable. We define a total of 9          We study five LLMs as judges for autoformaliza-
such properties, each capturing a distinct and mea-         tion evaluation: DeepSeek-Math-7B (Shao et al.,
surable aspect of a candidate formalization: Pre-arg        2024), Qwen2.5-Coder-7B (Qwen, 2025), GPT-4.1-
Structure, Quantification, Formula, Relation, Con-          mini, GPT-4.1, and GPT-5.4 (OpenAI, 2025). We
cept, Constant, Operator, Conciseness, and Logical          consider three settings: (OA-TP): LLM judges di-
Consistency. The detailed description of each OAP           rectly provide an overall assessment score based
is provided in Appendix B.                                  on the same criteria used in the human evaluation,
   An evaluation metric for autoformalization can           together with detailed error feedback from the the-
be constructed as a linear combination of Tier-2            orem prover; (DA-T2): LLM judges directly assess
aspects:                                                    the Tier-2 aspects LP, MC, and FQ, while the theo-
                                                            rem prover determines FV, and the resulting scores
  S(s, ϕ) = wLP SLP (s, ϕ) + wMC SMC (s, ϕ)                 are averaged to obtain a final score between 0 and 1;
                  + wFQ SFQ (ϕ) + wFV SFV (ϕ)                  3
                                                                 Equivalence is allowed in the ranking process, as correct
                                                            formalizations can be written in various ways, and even flawed
where SLP , SMC , SFQ , SFV ∈ [0, 1], and the               formalizations may be difficult to distinguish in ranking.


                                                        4
                                              miniF2F                                ProofNet
   LLM                  Setup     EM-H1    EM-H2 PM-H1         PM-H2    EM-H1     EM-H2 PM-H1         PM-H2
   DeepSeek-Math-7B     OA-TP      18.00    16.00     39.33     39.33     6.00     16.00     51.33    46.67
   DeepSeek-Math-7B     DA-T2      18.00    24.00     44.67     45.33    18.00     10.00     46.00    39.33
   DeepSeek-Math-7B     OAP        20.00    16.00     47.33     49.33    20.00      8.00     60.00    48.00
   Qwen2.5-Coder-7B     OA-TP      10.00    22.00     40.00     46.67    10.00     10.00     38.67    39.33
   Qwen2.5-Coder-7B     DA-T2      22.00    22.00     50.67     52.00    12.00     20.00     48.00    56.00
   Qwen2.5-Coder-7B     OAP        16.00    12.00     44.67     46.67    14.00     20.00     56.67    62.00
   GPT-4.1-mini         OA-TP      22.00    26.00     60.00     58.67    22.00     36.00     65.33    68.00
   GPT-4.1-mini         DA-T2      16.00    24.00     57.33     56.67    28.00     24.00     66.00    66.00
   GPT-4.1-mini         OAP        40.00    38.00     72.67     64.00    30.00     26.00     69.33    69.33
   GPT-4.1              OA-TP      32.00    24.00     64.67     53.33    30.00     26.00     68.00    65.33
   GPT-4.1              DA-T2      38.00    34.00     67.33     56.00    30.00     28.00     67.33    67.33
   GPT-4.1              OAP        40.00    32.00     69.33     58.67    32.00     34.00     69.33    72.00
   GPT-5.4              OA-TP      20.00    36.00     59.33     59.33    20.00     22.00     61.33    63.33
   GPT-5.4              DA-T2      36.00    38.00     68.00     62.00    36.00     24.00     70.67    62.00
   GPT-5.4              OAP        34.00    32.00     69.33     60.00    36.00     24.00     75.33    70.67

Table 2: Results of using LLM judges to evaluate Lean4 formalizations from three sources, Human, GPT-4.1 and
Qwen2.5-7B. The metrics include: (EM): the percentage of rankings that exactly match human rankings; (PM): the
percentage of pairwise rankings that match human pairwise rankings. H1 and H2 denote two human annotators.
The evaluation setups are: (OA-TP): overall assessment by an LLM judge with theorem prover feedback injected
into the prompt; (DA-T2): directly assessing the Tier-2 aspects LP, MC, and FQ using LLM judges, and FV using
the theorem prover, then averaging the results; (OAP): independently assessing the OAPs using LLM judges and
synthesizing the Tier-2 aspects LP, MC, and FQ using a weighted average, where each OAP is weighted equally
within each Tier-2 aspect, and FV using the theorem prover, then averaging the results. Bold represents the setup
with the highest score within the same LLM and Underline represents the setup with the highest score overall.


and (OAP): LLM judges independently assess the             evaluation. Comparing results in Table 2 with hu-
OAPs corresponding to the Tier-2 aspects LP, MC,           man agreement scores, with OAP settings, LLM
and FQ, after which the Tier-2 scores are synthe-          judges can reach performance levels that are com-
sized through weighted averaging, with each OAP            parable to human inter-annotator agreement, partic-
weighted equally within its corresponding Tier-2           ularly in pairwise matching where their scores ap-
aspect. FV and the final scores are then obtained in       proach or exceed the agreement between human an-
the same manner as in setting (ii). These scores are       notators on both miniF2F and ProofNet. This indi-
used to rank the formalizations. We compare the            cates that decomposing evaluation into fine-grained
results of the LLM judges with those of the human          aspects enables LLM judges to more closely ap-
evaluators and report the results in Table 2.              proximate human judgment behavior, improving
   Fine-grained LLM judges perform consis-                 consistency and reliability in autoformalization as-
tently better than coarse-grained judges. In Ta-           sessment.
ble 2, across all LLMs, the method of using LLM               Smaller fine-grained LLM judges can exceed
judges with OAPs achieves the highest exact match          the performance of coarse-grained larger LLM
score in 12 cases and the highest pairwise match           judges. Across both miniF2F and ProofNet, we ob-
score in 17 out of 20 cases compared to the other          serve that GPT-4.1-mini equipped with fine-grained
two settings. On miniF2F, all settings with the            OAP-based evaluation consistently outperforms
highest individual scores are achieved via OAPs.           larger models using coarse-grained evaluation se-
On ProofNet, three out of four highest individual          tups. The decomposition of evaluation into in-
scores are also achieved via OAPs. Together, these         terpretable aspects enables smaller judges to bet-
results demonstrate the superiority of the OAP set-        ter capture localized correctness signals, reducing
ting and support our claim that using fine-grained         the ambiguity inherent in single-pass judgments.
aspects in LLM-based judges for autoformalization          These results suggest that evaluation quality is
evaluation is more accurate than coarse-grained            driven not only by model scale, but also by the
approaches.                                                structure of the judging process, with fine-grained
   Fine-grained LLM judges can reach the same              decomposition providing a more effective approach
level of human agreement on autoformalization              for LLM-based assessment.

                                                       5
                                     Isabelle (miniF2F)          Lean4 (miniF2F)        Lean4 (ProofNet)
        Aspect    Judge               GT            ZS           GT          ZS         GT          ZS
        LP        Human Expert     0.24±0.43   0.80±0.40      0.40±0.49   0.80±0.40   0.68±0.47   0.40±0.49
        MC        Human Expert     0.34±0.47   0.74±0.44      0.40±0.49   0.52±0.50   0.68±0.48   0.40±0.49
        FQ        Human Expert     0.76±0.43   0.46±0.50      0.92±0.27   0.56±0.50   0.92±0.27   0.60±0.49
        FV        Theorem Prover   1.00±0.00   0.52±0.50      1.00±0.00   0.20±0.40   1.00±0.00   0.12±0.32
        OA        Human Expert     4.06±0.58   4.00±0.77      4.04±0.53   3.64±0.93   4.48±0.64   3.56±0.57


Table 3: Human evaluation of formalizations on subsets of validation sets. Results are reported in mean± standard
deviation across samples. (GT): Ground-Truth formalization; (ZS): GPT-4.1 Zero-Shot formalization; (LP): Logical
Preservation; (MC): Mathematical Consistency; (FQ): Formal Quality; (FV): Formal Validity; (OA): Overall
Assessment.


   Computational cost can be reduced by select-               malization are evaluated by one human expert and
ing smaller effective LLMs while maintaining                  LLM judges. The human expert and LLM judges
strong performance. On miniF2F, under the OAP                 evaluated the formalizations with respect to LP,
setting, GPT-4.1-mini even outperforms its larger             MC, and FQ using binary judgments, together with
counterpart GPT-4.1 and a more recent model, GPT-             an overall assessment on a 5-point scale (criteria
5.4. On ProofNet, while GPT-4.1-mini is not the               in Table 6 in Appendix A). FV, as verified by the
top-performing model, it still achieves competi-              corresponding theorem prover, was also taken into
tive performance. Since the OAP setting requires              account during the human evaluation and the over-
multiple LLM judge passes, these results suggest              all assessment from LLM judges.
a favorable trade-off between computational cost                 We acknowledge the potential subjectivity inher-
and performance when using smaller LLMs with                  ent in human evaluation, particularly regarding the
OAPs for autoformalization evaluation.                        relative importance assigned to different evaluation
                                                              aspects. Although a multi-annotator study could
3.2   Contribution of Evaluation Aspects in                   provide additional insights by analyzing aspect con-
      LLM and Human Judgments                                 tributions separately for each annotator, conducting
For a perfect formalization, all evaluation aspects           such an analysis would substantially increase the
should receive positive assessments. For formaliza-           complexity of the evaluation procedure and is be-
tions judged to be flawed, however, it is important           yond the scope of this work. We therefore employ
to understand how LLM judges and human eval-                  a single expert evaluator to provide a consistent
uators differ in how individual evaluation aspects            and practically reliable reference for comparison.
contribute to the final assessment. To enable a more          We report the mean and standard deviation of the
detailed comparison between human evaluators and              human assessments in Table 3. As expected, the
LLM judges, we focused on natural language state-             annotated formalizations are not perfect, exhibiting
ments that were likely to result in formalization             errors across all Tier-2 evaluation aspects.
errors, even in human-written formalizations. To
this end, we first used GPT-4.1 to estimate whether           3.2.1   Results & Discussions
the human-written ground-truth formalizations in              We calculate Pearson correlation coefficients be-
the validation datasets correctly represented their           tween Tier-2 aspect evaluations and overall assess-
corresponding natural-language statements. The es-            ments from LLM judges and the human evaluator
timated correctness rates were 76.64% for miniF2F             on flawed formalizations identified by the human
Isabelle/HOL, 82.79% for miniF2F Lean4, and                   evaluator. Results for Lean4 and Isabelle/HOL are
64.84% for ProofNet Lean4. Based on these esti-               reported in Figure 2.
mates, we randomly sampled 50, 25, and 25 natural-               Human and LLM judges exhibit different cor-
language statements from miniF2F Isabelle/HOL,                relation patterns among Tier-2 aspects when
miniF2F Lean4, and ProofNet Lean4, respectively,              evaluating flawed formalizations. As shown in
whose ground-truth formalizations were identified             Figures 2a, 2b, and 2c, LLM judges generally
as potentially incorrect.                                     exhibit moderate positive correlations among the
   For each selected statement, both the ground-              soft aspects, logical preservation (LP), mathemat-
truth formalization and the GPT-4.1 zero-shot for-            ical consistency (MC), and formal quality (FQ),

                                                          6
   / 3                                 / 3                                      / 3                                  / 3                           

  0 &                            0 &                            0 &                            0 &                            

  ) 4                                  ) 4                                       ) 4                                  ) 4                           

  ) 9                                ) 9                                    ) 9                                ) 9                           

  2 $                           2 $                           2 $                           2 $                         
          / 3       0 &       ) 4        ) 9       2 $              / 3       0 &       ) 4        ) 9       2 $                  / 3       0 &       ) 4        ) 9       2 $              / 3      0 &       ) 4       ) 9       2 $
      (a) Qwen2.5-Coder-7B                                            (b) GPT-4.1-mini                                                   (c) GPT-4.1                                               (d) Human

Figure 2: Pearson correlation coefficients between evaluation aspects and overall assessments across judges for
flawed formalizations. LLM judges and human evaluators assess the Tier-2 aspects logical preservation (LP),
mathematical consistency (MC), and formal quality (FQ), while theorem provers assess formal validity (FV). The
lower triangular matrix shows results for Lean4, and the upper triangular matrix shows results for Isabelle/HOL.


whereas human evaluators show weak or slightly                                                                             indicate that evaluators do not rely on a single dom-
negative correlations between these aspects. This                                                                          inant aspect in a uniform manner but instead in-
suggests that LLM judges may have difficulty dis-                                                                          tegrate multiple factors with varying degrees of
tinguishing subtle differences between aspects as                                                                          emphasis depending on the evaluator type and for-
human, leading to more entangled judgments. In                                                                             mal language.
contrast, the hard aspect of formal validity (FV)
shows weak or negative correlations with LP and                                                                            3.3          Distinguishing Performance
MC for both human and LLM judges. This indi-                                                                               We use the GPT-4.1-mini OAP method to as-
cates that semantic alignment issues are largely                                                                           sess the autoformalization performance of mod-
distinct from syntactic correctness: a formally                                                                            els on datasets. We evaluate the zero-shot set-
valid formalization can still be misaligned with                                                                           ting with GPT-4.1, and the few-shot (8 exemplars)
the source mathematics. Both humans and LLMs                                                                               setting with GPT-4.1, Mistral-7B (Jiang et al.,
appear capable of recognizing this distinction. Hu-                                                                        2023a), Deepseek-Math-7B (Shao et al., 2024), and
man evaluators also exhibit a positive correlation                                                                         Qwen2.5-7B (Qwen, 2025). We report scores in
between FQ and FV, reflecting the tendency for                                                                             Table 4.
well-structured formalizations to be both more read-                                                                          GPT-4.1 in the few-shot setting generally demon-
able and more likely to satisfy syntactic require-                                                                         strates better performance compared to the zero-
ments. This relationship is largely absent for LLM                                                                         shot setting. However, this performance gain is
judges, suggesting that humans and LLMs rely on                                                                            primarily driven by improvements in formal va-
different notions of formal quality when assessing                                                                         lidity, indicating that few-shot exemplars mainly
flawed formalizations.                                                                                                     help the model produce syntactically valid for-
   All Tier-2 aspects contribute to the overall as-                                                                        malizations. These findings suggest that our pro-
sessment for both human and LLM judges. All                                                                                posed evaluation method offers more informative
aspects exhibit positive correlations with the over-                                                                       insights into specific areas of improvement.
all assessment, indicating that these dimensions                                                                              Among the 7B models, Qwen2.5-7B achieves
serve as informative signals for formalization qual-                                                                       the best performance across all metrics on
ity. However, the strength of these relationships,                                                                         miniF2F, while on ProofNet, the results are more
as reflected in the correlation coefficients, varies                                                                       varied, with Deepseek-Math-7B achieving the high-
across evaluators and formal languages. For Lean4,                                                                         est overall assessment (OA). Additionally, the per-
both Qwen2.5-Coder-7B and GPT-4.1 assign rela-                                                                             formance of 7B LLMs on miniF2F and ProofNet in
tively higher associations to LP and MC compared                                                                           Lean4 still shows a significant gap in OA, indicat-
to FQ and FV, whereas GPT-4.1-mini and human                                                                               ing that formalizing complex statements remains
evaluators show the strongest association with FQ.                                                                         challenging for these models.
For Isabelle/HOL, Qwen2.5-Coder-7B, GPT-4.1,
and human evaluators place the strongest associ-                                                                           3.3.1             Biases Toward Self-Generated Outputs
ation on FV, while GPT-4.1-mini exhibits a more                                                                            We investigate the use of different LLMs as OAP
uniform pattern across all aspects. These findings                                                                         judges for autoformalization evaluation. Specifi-

                                                                                                                     7
                                                                                                                     
  Prompting    Model             LP       MC         FV         FQ           OA                                                   / 3             0 &                      ) 4             2 $
                                                                                                                     
  miniF2F Isabelle/HOL
                                                                                                                     




                                                                                               6 F R U H    
  Zero-Shot    GPT-4.1          0.939     0.963     0.643      0.953        0.874
  8-Shot       GPT-4.1          0.945     0.986     0.746      0.949        0.906                                    
  8-Shot       Mistral-7B       0.418     0.624     0.201      0.480        0.431                                    
  8-Shot       DS-Math-7B       0.492     0.698     0.324      0.512        0.506
  8-Shot       Qwen2.5-7B       0.651     0.831     0.590      0.740        0.703                                    
  miniF2F Lean4                                                                                                                                                                   
  Zero-Shot    GPT-4.1          0.943     0.986     0.463      0.955        0.837                                                                 7 H P S H U D W X U H
  8-Shot       GPT-4.1          0.924     0.985     0.697      0.957        0.891
  8-Shot       Mistral-7B       0.434     0.634     0.430      0.492        0.498       Figure 3: Error bars of GPT-4.1-mini with OAP setting
  8-Shot       DS-Math-7B       0.522     0.750     0.561      0.641        0.619
  8-Shot       Qwen2.5-7B       0.627     0.842     0.586      0.758        0.703       running with different temperatures.
  ProofNet Lean4

  Zero-Shot    GPT-4.1          0.923     0.980     0.137      0.945        0.746
  8-Shot       GPT-4.1          0.963     0.993     0.423      0.967        0.836       3.3.2                             Randomness in LLM Judges
  8-Shot       Mistral-7B       0.317     0.604     0.082      0.393        0.349
  8-Shot       DS-Math-7B       0.569     0.793     0.192      0.585        0.535       We explore how the randomness introduced during
  8-Shot       Qwen2.5-7B       0.559     0.769     0.099      0.613        0.510
                                                                                        the generation of LLMs influences the scores with
Table 4: Evaluation of autoformalizations on the test                                   GPT-4.1-mini OAP-EW. We randomly select 50
sets with GPT-4.1-mini in OAP setting.                                                  Isabelle/HOL formalizations from the miniF2F test
                                                                                        set using Qwen2.5-7B with 8-shot prompting. We
      AF           Judge           LP        MC           FQ           OA
                                                                                        perform 3 runs for 5 different temperatures (0.2,
      Lean4
                                                                                        0.4, 0.6, 0.8, 1.0) and report the mean and variance
      G-4.1        G-4.1-Mini     0.924     0.985      0.957         0.891
                                                                                        of the scores in Figure 3. In general, the mean of
      Q-7B         G-4.1-Mini     0.627     0.842      0.758         0.703              the MC and FQ scores fluctuates as the temperature
      G-4.1        Q-Coder-7B     0.703     0.757      0.328         0.621              increases, whereas the LP and OA scores remain
      Q-7B         Q-Coder-7B     0.473     0.616      0.170         0.461
      Isabelle/HOL
                                                                                        relatively stable. While LP, MC, and FQ scores
      G-4.1        G-4.1-Mini     0.945     0.986      0.949         0.906
                                                                                        exhibit some variance across multiple runs, the
      Q-7B         G-4.1-Mini     0.651     0.831      0.740         0.703              OA scores show consistent stability.
      G-4.1        Q-Coder-7B     0.847     0.833      0.666         0.773
      Q-7B         Q-Coder-7B     0.666     0.717      0.518         0.623
                                                                                        4         Related Work
Table 5: Using different judges for evaluation on
                                                                                        4.1                    Autoformalization
miniF2F test set. LLM autoformalizer (AF) is used
in few-shot setting. (G): GPT; (Q): Qwen2.5.                                            Autoformalization bridges the gap between nat-
                                                                                        ural and formal languages, enabling natural lan-
                                                                                        guage inputs to be translated into formal repre-
cally, we use GPT-4.1-mini and Qwen2.5-Coder-                                           sentations. This task has seen promising devel-
7B to evaluate the few-shot autoformalizations pro-                                     opments across various domains, such as natural
duced by GPT-4.1 and Qwen2.5-7B on the miniF2F                                          language inference (Quan et al., 2024b,a), and au-
test set. Scores for Tier-2 aspects and overall as-                                     tomated theorem proving (Jiang et al., 2023b; Tar-
sessments are reported in Table 5.                                                      rach et al., 2024). LLMs have shown efficacy in
   Qwen2.5-Coder-7B generally assigns lower                                             Isabelle (Wu et al., 2022), and retrieval-augmented
scores compared to GPT-4.1-mini, suggesting that                                        generation has further enhanced performance in
absolute score values may vary across judge mod-                                        Isabelle (Zhang et al., 2024) and Lean (Yang et al.,
els. Nevertheless, Qwen2.5-Coder-7B consis-                                             2023; Liu et al., 2025a). In parallel, Jiang et al.
tently rates GPT-4.1’s autoformalizations higher                                        (2024) and Liu et al. (2025b) developed data gen-
than those of Qwen2.5-7B across both formal                                             eration pipelines for constructing large-scale paral-
languages, indicating a degree of robustness in                                         lel corpora of theorem statements. On the evalua-
the indicative power of our evaluation approach.                                        tion front, Poiroux et al. (2025b) proposed scalable
The score differences between the two judges are                                        type-check filtering with self-consistency, while Lu
more pronounced on Lean4 than on Isabelle/HOL,                                          et al. (2024) trained a model to assess semantic
which may reflect biases in the training data of                                        alignment between informal and formal statements.
Qwen2.5-Coder-7B. At present, we find no ev-                                            Despite these advances, standardized and compre-
idence that the LLM-as-judges framework fa-                                             hensive evaluation metrics for autoformalization
vors autoformalizations generated by the same                                           remain under-explored. Our work seeks to address
model series.                                                                           this critical gap.

                                                                                    8
4.2    LLM-as-a-Judge                                      expanding the annotation would likely yield more
LLM-as-a-Judge (Zheng et al., 2023) was proposed           robust and generalizable results, we do not expect
for evaluating multi-turn questions and dialogues          it to alter the main findings. Moreover, the set of
and has become an increasingly popular approach            operable atomic properties and LLMs used in our
for assessing NLP tasks using LLMs. In the domain          approach is not exhaustive. Although alternative
of mathematical evaluation, Zhang et al. (2025c)           configurations might yield slightly different results,
explored the use of LLM judges for scoring natural         we believe they would not substantially impact the
language proofs across four dimensions. However,           core conclusions of the study.
limited research has been conducted on employing
LLM-as-a-Judge in the field of formal mathematics.         References
Our work takes a step in this direction.
                                                           Riyaz Ahuja, Jeremy Avigad, Prasad Tetali, and Sean
5     Conclusion                                             Welleck. 2025. Improver: Agent-based automated
                                                             proof optimization. In The Thirteenth International
In this work, we address the under-explored chal-            Conference on Learning Representations.
lenge of evaluating autoformalization by introduc-         Zhangir Azerbayev, Bartosz Piotrowski, Hailey
ing a fine-grained taxonomy that captures multiple           Schoelkopf, Edward W. Ayers, Dragomir Radev, and
aspects of a candidate formalization and propose a           Jeremy Avigad. 2023. Proofnet: Autoformalizing
                                                             and formally proving undergraduate-level mathemat-
linear evaluation model to synthesize core proper-
                                                             ics. Preprint, arXiv:2302.12433.
ties into a single overall assessment score.
   Through human evaluation and empirical anal-            Leonardo de Moura, Soonho Kong, Jeremy Avigad,
ysis, we demonstrate that this automatic evalua-             Floris van Doorn, and Jakob von Raumer. 2015. The
                                                             lean theorem prover (system description). In Auto-
tion model provides meaningful indication on for-            mated Deduction - CADE-25, pages 378–388, Cham.
malization performance. Furthermore, we show                 Springer International Publishing.
the feasibility of EFG ensemble of LLM-as-a-
                                                           Albert Q. Jiang, Wenda Li, and Mateja Jamnik. 2024.
Judge, both directly and via OAPs. Our experi-               Multi-language diversity benefits autoformalization.
ments reveal that fine-grained LLM-based judg-               In Advances in Neural Information Processing Sys-
ments are more closely with human assessments                tems, volume 37, pages 83600–83626. Curran Asso-
than coarse-grained judgements in terms of rank-             ciates, Inc.
ing. Lightweight LLMs like GPT-4.1-mini, when              Albert Q. Jiang, Alexandre Sablayrolles, Arthur Men-
guided by OAPs, can serve as effective and cost-             sch, Chris Bamford, Devendra Singh Chaplot, Diego
efficient judges.                                            de las Casas, Florian Bressand, Gianna Lengyel, Guil-
   Our findings contribute new insights and tools            laume Lample, Lucile Saulnier, Lélio Renard Lavaud,
                                                             Marie-Anne Lachaux, Pierre Stock, Teven Le Scao,
for automatic and fine-grained evaluation of aut-            Thibaut Lavril, Thomas Wang, Timothée Lacroix,
oformalization systems, paving the way for more              and William El Sayed. 2023a. Mistral 7b. Preprint,
systematic benchmarking and future improvements              arXiv:2310.06825.
in this emerging area. Further directions could            Albert Qiaochu Jiang, Sean Welleck, Jin Peng Zhou,
focus on fine-tuning smaller open-sourced LLMs               Timothee Lacroix, Jiacheng Liu, Wenda Li, Mateja
specialized as judges for autoformalization evalua-          Jamnik, Guillaume Lample, and Yuhuai Wu. 2023b.
tion and using LLM explanations of judgments to              Draft, sketch, and prove: Guiding formal theorem
                                                             provers with informal proofs. In The Eleventh Inter-
improve autoformalization performance.                       national Conference on Learning Representations.
Limitations                                                Zenan Li, Yifan Wu, Zhaoyu Li, Xinming Wei, Xian
                                                             Zhang, Fan Yang, and Xiaoxing Ma. 2024. Autofor-
As in different studies involving human annota-              malize mathematical statements by symbolic equiva-
tions, some of our results may be partially affected         lence and semantic consistency. In The Thirty-eighth
by subjective biases. However, we attempt to limit           Annual Conference on Neural Information Process-
                                                             ing Systems.
subjectivity by leveraging the annotators with back-
ground knowledge in both AI and formal languages,          Yong Lin, Shange Tang, Bohan Lyu, Jiayun Wu,
capable of articulating the rationale behind the an-         Hongzhou Lin, Kaiyu Yang, Jia Li, Mengzhou
                                                             Xia, Danqi Chen, Sanjeev Arora, and Chi Jin.
notation’s decisions. Additionally, the scale of             2025. Goedel-prover: A frontier model for open-
human-annotated samples is relatively small due to           source automated theorem proving.     Preprint,
the complexity involved in the annotation. While             arXiv:2502.07640.


                                                       9
Qi Liu, Xinhao Zheng, Xudong Lu, Qinxiang Cao, and                 theorem proving. In Proceedings of the 2024 Con-
  Junchi Yan. 2025a. Rethinking and improving auto-                ference on Empirical Methods in Natural Language
  formalization: towards a faithful metric and a depen-            Processing, pages 2933–2958, Miami, Florida, USA.
  dency retrieval-based approach. In The Thirteenth                Association for Computational Linguistics.
  International Conference on Learning Representa-
  tions.                                                         Xin Quan, Marco Valentino, Louise A Dennis, and An-
                                                                   dré Freitas. 2025. Faithful and robust llm-driven
Xiaoyang Liu, Kangjie Bao, Jiashuo Zhang, Yunqi                    theorem proving for nli explanations. arXiv preprint
  Liu, Yuntian Liu, Yu Chen, Yang Jiao, and Tao Luo.               arXiv:2505.24264.
  2025b. Atlas: Autoformalizing theorems through
  lifting, augmentation, and synthesis of data. Preprint,        Team Qwen. 2025. Qwen2.5 technical report. Preprint,
  arXiv:2502.05567.                                                arXiv:2412.15115.

Jianqiao Lu, Yingjia Wan, Yinya Huang, Jing Xiong,               Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu,
   Zhengying Liu, and Zhijiang Guo. 2024. For-                     Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan
   malalign: Automated alignment evaluation for auto-              Zhang, Y. K. Li, Y. Wu, and Daya Guo. 2024.
   formalization. Preprint, arXiv:2410.10135.                      Deepseekmath: Pushing the limits of mathemati-
                                                                   cal reasoning in open language models. Preprint,
OpenAI. 2024. Gpt-4 technical report.          Preprint,           arXiv:2402.03300.
  arXiv:2303.08774.
                                                                 Guillem Tarrach, Albert Q. Jiang, Daniel Raggi, Wenda
OpenAI. 2025. Openai gpt-5 system card. Preprint,                  Li, and Mateja Jamnik. 2024. More details, please:
  arXiv:2601.03267.                                                Improving autoformalization with more detailed
                                                                   proofs. In AI for Math Workshop @ ICML 2024.
Liangming Pan, Alon Albalak, Xinyi Wang, and
  William Wang. 2023. Logic-LM: Empowering large                 Yuhuai Wu, Albert Qiaochu Jiang, Wenda Li,
  language models with symbolic solvers for faithful               Markus Norman Rabe, Charles E Staats, Mateja Jam-
  logical reasoning. In Findings of the Association                nik, and Christian Szegedy. 2022. Autoformalization
  for Computational Linguistics: EMNLP 2023, pages                 with large language models. In Advances in Neural
  3806–3824, Singapore. Association for Computa-                   Information Processing Systems.
  tional Linguistics.
                                                                 Huajian Xin, Z.Z. Ren, Junxiao Song, Zhihong Shao,
Lawrence C. Paulson. 2000. Isabelle: The next 700                  Wanjia Zhao, Haocheng Wang, Bo Liu, Liyue Zhang,
  theorem provers. Preprint, arXiv:cs/9301106.                     Xuan Lu, Qiushi Du, Wenjun Gao, Haowei Zhang,
                                                                   Qihao Zhu, Dejian Yang, Zhibin Gou, Z.F. Wu, Fuli
Gabriel Poesia, David Broman, Nick Haber, and Noah                 Luo, and Chong Ruan. 2025. Deepseek-prover-v1.5:
  Goodman. 2024. Learning formal mathematics from                  Harnessing proof assistant feedback for reinforce-
  intrinsic motivation. In The Thirty-eighth Annual                ment learning and monte-carlo tree search. In The
  Conference on Neural Information Processing Sys-                 Thirteenth International Conference on Learning
  tems.                                                            Representations.

Auguste Poiroux, Gail Weiss, Viktor Kunčak, and An-             Kaiyu Yang, Gabriel Poesia, Jingxuan He, Wenda Li,
  toine Bosselut. 2025a. Reliable evaluation and bench-            Kristin Lauter, Swarat Chaudhuri, and Dawn Song.
  marks for statement autoformalization. In Proceed-               2024. Formal mathematical reasoning: A new fron-
  ings of the 2025 Conference on Empirical Methods in              tier in ai. Preprint, arXiv:2412.16075.
  Natural Language Processing, pages 17947–17969,
  Suzhou, China. Association for Computational Lin-              Kaiyu Yang, Aidan M. Swope, Alex Gu, Rahul Chala-
  guistics.                                                        mala, Peiyang Song, Shixing Yu, Saad Godil, Ryan
                                                                   Prenger, and Anima Anandkumar. 2023. Leandojo:
Auguste Poiroux, Gail Weiss, Viktor Kunčak, and An-               Theorem proving with retrieval-augmented language
  toine Bosselut. 2025b. Improving autoformalization               models. Preprint, arXiv:2306.15626.
  using type checking. Preprint, arXiv:2406.07222.
                                                                 Zhouliang Yu, Ruotian Peng, Keyi Ding, Yizhe Li,
Xin Quan, Marco Valentino, Louise Dennis, and An-                  Zhongyuan Peng, Minghao Liu, Yifan Zhang, Zheng
  dre Freitas. 2024a. Enhancing ethical explanations               Yuan, Huajian Xin, Wenhao Huang, Yandong Wen,
  of large language models through iterative symbolic              Ge Zhang, and Weiyang Liu. 2025. Formalmath:
  refinement. In Proceedings of the 18th Conference of             Benchmarking formal mathematical reasoning of
  the European Chapter of the Association for Compu-               large language models. Preprint, arXiv:2505.02735.
  tational Linguistics (Volume 1: Long Papers), pages
  1–22, St. Julian’s, Malta. Association for Computa-            Lan Zhang, Xin Quan, and Andre Freitas. 2024. Consis-
  tional Linguistics.                                              tent autoformalization for constructing mathematical
                                                                   libraries. In Proceedings of the 2024 Conference on
Xin Quan, Marco Valentino, Louise A. Dennis, and An-               Empirical Methods in Natural Language Processing,
  dre Freitas. 2024b. Verification and refinement of nat-          pages 4020–4033, Miami, Florida, USA. Association
  ural language explanations through LLM-symbolic                  for Computational Linguistics.


                                                            10
Lan Zhang, Marco Valentino, and Andre Freitas. 2025a.            2. Quantification: ϕ accurately formalizes all
  Autoformalization in the wild: Assessing LLMs on                  quantifiers, such as universal and existential,
  real-world mathematical definitions. In Proceed-
                                                                    present in s.
  ings of the 2025 Conference on Empirical Methods
  in Natural Language Processing, pages 1720–1738,
  Suzhou, China. Association for Computational Lin-
                                                                 3. Formula: All mathematical formulas and ex-
  guistics.                                                         pressions in s, such as equations and inequali-
                                                                    ties, are correctly and completely represented
Lan Zhang, Marco Valentino, and Andre Freitas. 2025b.               in ϕ.
  MASA: LLM-driven multi-agent systems for auto-
  formalization. In Proceedings of the 2025 Confer-
                                                                 4. Relation: The logical and mathematical re-
  ence on Empirical Methods in Natural Language
  Processing: System Demonstrations, pages 615–624,                 lationships between propositions in s are pre-
  Suzhou, China. Association for Computational Lin-                 served in ϕ.
  guistics.
                                                                 5. Concept: All mathematical concepts men-
Ziyin Zhang, Jiahao Xu, Zhiwei He, Tian Liang, Qi-                  tioned in s, such as integers, fractions, real or
  uzhi Liu, Yansi Li, Linfeng Song, Zhenwen Liang,
  Zhuosheng Zhang, Rui Wang, Zhaopeng Tu, Haitao                    complex numbers, derivatives, integrals, vec-
  Mi, and Dong Yu. 2025c. Deeptheorem: Advanc-                      tors, matrices, probabilities, expectations, and
  ing llm reasoning for theorem proving through nat-                variances, are correctly formalized in ϕ.
  ural language and reinforcement learning. Preprint,
  arXiv:2505.23754.                                              6. Constant: All mathematical constants men-
Kunhao Zheng, Jesse Michael Han, and Stanislas Polu.                tioned in s, such as 1, 23 , π, e, are properly
  2022. minif2f: a cross-system benchmark for for-                  included in ϕ.
  mal olympiad-level mathematics. In International
  Conference on Learning Representations.                        7. Operator: All mathematical operators used
                                                                    in s, such as addition, subtraction, multipli-
Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan
  Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin,                      cation, division, summation, exponentiation,
  Zhuohan Li, Dacheng Li, Eric Xing, Hao Zhang,                     and product, are correctly represented in ϕ.
  Joseph E. Gonzalez, and Ion Stoica. 2023. Judging
  LLM-as-a-judge with MT-bench and chatbot arena.                8. Conciseness: ϕ is expressed in a minimal,
  In Thirty-seventh Conference on Neural Information                non-redundant form, avoiding unnecessary
  Processing Systems Datasets and Benchmarks Track.                 repetition or complexity.
A     Human Annotation Criteria and LLM                          9. Logical Consistency: ϕ is internally coher-
      Prompts                                                       ent and contains no contradictions under the
We provide the detailed human annotation criteria                   logical rules of the formal system.
in Table 6. A binary scheme is used for logical              C     Examples of Incorrect LLM Judgments
preservation, mathematical consistency, and for-
mal quality, while overall assessment is rated on a          We conduct a qualitative study on cases where GPT-
5-point scale. Since mathematics is a rigorous dis-          4.1 misjudges logical preservation and mathemati-
cipline and formal languages are designed to reflect         cal consistency in formalizations. We provide two
this rigor, any human with sufficient knowledge of           examples of misjudged logical preservation and
mathematics and formal language should be able to            two examples of misjudged mathematical consis-
apply these criteria consistently and reach similar          tency by GPT-4.1 in Table 7 and Table 8, and in
judgments. We provide the prompts in Table 11.               Table 9 and Table 10, respectively. GPT-4.1 of-
                                                             ten provides reasonable and correct explanations
B     Operable Atomic Properties                             of the formalizations, and its judgments generally
With the notation of s as the original natural lan-          align with those explanations. The primary rea-
guage statement and ϕ as a candidate formalization,          son for incorrect judgments is the overlap between
we define operable atomic properties as the follow-          the logical and mathematical aspects of formal-
ing:                                                         izations, which makes it difficult for GPT-4.1 to
                                                             clearly distinguish the subtle differences between
    1. Pre-arg Structure: ϕ reflects the inherent            them through prompt-based interaction.
       predicate-argument structure of the statement
       s.

                                                        11
Logical Preservation (LP)
From your point of view, does the formal code capture the logical structure and content of the natural language statement?
1: Yes 0: No
Mathematical Consistency (MC)
From your point of view, does the formal code accurately represent mathematical objects and operations present in the
natural language statement?
1: Yes 0: No
Formal Quality (FQ)
From your point of view, does the formalized code alone demonstrate high quality in terms of structural clarity, readability,
and usefulness?
1: Yes 0: No
Overall Assessment (OA)
What would you rate this formal code as the formalization of the natural language statement?
5: Perfect formalization – fully accurate and complete with no issues.
4: Good formalization – minor flaws are present, but they are easy to fix.
3: Acceptable formalization – captures the intent but may require some time and effort to correct.
2: Flawed formalization – contains major issues that require significant time and effort to correct.
1: Poor formalization – completely fails to reflect the intended meaning of the natural language statement.


                                              Table 6: Annotation criteria




NL Statement        Let                                            (
                                                                       x2 + 9 ifx < −5,
                                                         f (x) =
                                                                       3x − 8 ifx ≥ −5.

                    If f (x) = 10, find the sum of all possible values of x. Show that it is 6.
Human               theorem mathd_algebra_149:
Formalization        fixes f :: "real ⇒ real"
                     assumes "∀ x < −5. f x = x^2 + 5"
                       and "∀ P x ≥ −5. f x = 3 * x −8"
                     shows "( k ∈ (f −` {10}). k) = 6"
                     sorry
Aspect              Logical Preservation
Human               Judgment: True
                    Explanation: The issue of having ‘+5’ instead of ‘+9’ in the formalization does not indicate that
                    the formalization fails to capture the logic of the natural language statement; rather, it suggests a
                    misrepresentation of a mathematical constant.
GPT-4.1             Explanation: The formal code does not fully capture the logical structure and content of the natural
                    language statement. The natural language statement defines a piecewise function f (x) with f (x) =
                    x2 + 9 for x < −5 and f (x) = 3x − 8 for x ≥ −5. However, in the formal code, the first case is
                    written as f x = x2 + 5 instead of x2 + 9, which is a critical error. This changes the function being
                    analyzed and thus the set of solutions to f (x) = 10. The rest of the structure, including the use of the
                    preimage and summing over the solutions, is correct, but the incorrect function definition means the
                    code does not faithfully represent the original problem.
                    Judgment: False


                              Table 7: Example 1 of incorrect LLM in Isabelle/HOL.




                                                            12
NL Statement    How many distinct, non-equilateral triangles with a perimeter of 60 units have integer side lengths a, b,
                and c such that a, b, c is an arithmetic sequence? Show that it is 9.
GPT-4.1         lemma count_non_equilateral_triangles_arith_seq:
Formalization    "card { (a, b, c) :: nat × nat × nat.
                   a<b∧b<c∧
                   a + b + c = 60 ∧
                   (∃d::nat. d > 0 ∧ b = a + d ∧ c = a + 2*d) ∧
                   ¬ (a = b ∨ b = c ∨ a = c) ∧
                   a+b>c∧a+c>b∧b+c>a
                  } = 9"
                 sorry
Aspect          Logical Preservation
Human           Judgment: False
                Explanation: Non-equilateral triangle should be ¬(a = b ∧ b = c ∧ a = c) rather than ¬(a = b ∨ b =
                c ∨ a = c) which represent non-isosceles triangle.
GPT-4.1         Explanation: The formalization captures most of the logical structure and content of the natural
                language statement. It defines the set of triples (a, b, c) of natural numbers such that a < b < c, the
                perimeter is 60, the sides form an arithmetic sequence (with b = a + d, c = a + 2d, d > 0), the
                triangle is non-equilateral (¬(a = b ∨ b = c ∨ a = c)), and the triangle inequalities are satisfied. The
                cardinality of this set is asserted to be 9, matching the "show that it is 9" part. The only minor issue
                is that the triangle inequalities are redundant given a < b < c and the arithmetic sequence, but their
                inclusion does not harm correctness. The formalization does not miss any logical aspect of the natural
                language statement.
                Judgement: True


                   Table 8: Example 2 of incorrect LLM judgment in Isabelle/HOL.




NL Statement    Let H ≤ K ≤ G. Prove that |G : H| = |G : K| · |K : H| (do not assume G is finite).
GPT-4.1         import Mathlib.GroupTheory.Index
Formalization
                variable {G : Type*} [Group G] (H K : Subgroup G) (hHK : H ≤ K)

                theorem index_mul_index_eq_index (hHK : H ≤ K) :
                 Subgroup.index H * Subgroup.index K = Subgroup.index H :=
                sorry
Aspect          Mathematically Consistency
Human           Judgment: True
                Explanation: The issue with using ‘Subgroup.index H’ on the right-hand side indicates that the
                formalization does not fully capture the logic that H is a subgroup of K, and that the index should be
                taken relative to K. This is more of a logical modeling issue than a purely mathematical one.
GPT-4.1         Explanation: The formalization does not accurately represent the mathematical objects and operations
                present in the natural language statement. The natural language statement involves three subgroups
                H ≤ K ≤ G and asserts the equality |G : H| = |G : K| · |K : H|, where |G : H| denotes the index
                of H in G, |G : K| the index of K in G, and |K : H| the index of H in K. In the Lean code, the
                theorem is stated as ‘Subgroup.index H * Subgroup.index K = Subgroup.index H‘, which is incorrect:
                it should be ‘Subgroup.index K * Subgroup.index H = Subgroup.index H‘ if following the code’s order,
                but even then, the left-hand side should be ‘Subgroup.index K * Subgroup.index H‘ only if the indices
                are taken in the correct groups. More importantly, the code uses ‘Subgroup.index H‘, which is the
                index of H in G, and ‘Subgroup.index K‘, which is the index of K in G, but it does not represent
                |K : H| (the index of H in K). There is no mention or calculation of the index of H in K in the code.
                Therefore, the code does not accurately formalize the mathematical objects and operations (specifically,
                the indices involved) as described in the natural language statement.
                Judgment: False


                        Table 9: Example 3 of incorrect LLM judgment in Lean4.




                                                       13
NL Statement    Prove that for every natural number n, and for every real number x ̸= kπ
                                                                                      2t
                                                                                         (t = 0, 1, . . . , n; k any
                integer) sin12x + sin14x + · · · + sin 12n x = cot x − cot 2n x
GPT-4.1         theorem sum_reciprocal_sin_eq_cot_diff
Formalization    (n : N) (x : R)
                 (hx : ∀ (t : N), t ≤ n → ∀ (k : Z), x ̸= (k * Real.pi) / (2^t : R)) :
                 (Σ i in Finset.range n.succ, 1 / Real.sin (2^(i+1) * x))
                 = Real.cot x − Real.cot (2^n * x) :=
                sorry
Aspect          Mathematical Consistency
Human           Judgment: False
                Explanation: ‘Finset.range n.succ’ gives the set 0, 1, . . . , n; however, the summation should be over
                0, 1, . . . , n − 1 when the summand is sin(21i+1 x) . This indicates a mathematical inconsistency in the
                indexing.
GPT-4.1         Explanation: The formalized Lean4 code accurately represents the mathematical objects and operations
                in the natural language statement. Specifically: -The quantification over n ∈ N and x ∈ R is captured. -
                The condition x ̸= kπ  2t
                                           for t = 0, 1, ..., n and any integer k is represented by the hypothesis. - The sum
                    1
                 sin 2x
                        +    1
                          sin 4x
                                 +· · ·+     1
                                          sin 2n x
                                                   is formalized correctly iterates i from 0 to n and computes 1/ sin(2i+1 x).
                - The right-hand side cot x − cot 2n x is formalized. All mathematical objects (natural numbers, real
                numbers, integers, sine, cotangent, summation) and their operations are correctly represented in the
                code.
                Judgment: True


                        Table 10: Example 4 of incorrect LLM judgment in Lean4.




                                                          14
Purpose                Content
Basic                  You are an expert in formal language {formal_language}.
                       You will be given a mathematical statement written in natural language and LaTeX symbols.
                       You will also be given a formal code which attempted to describe the given mathematical statement
                       in {formal_language}.
                       Your task is to evaluate a specific aspect of the formal code.
                       The description of the aspect is: {{aspect_description}}
                       Your need to give two things about your evaluation:
                       1. the judgement of whether the formal code satisfies this aspect. This should be a binary value in
                       "True" or "False".
                       2. the detailed explanation of your judgement.
                       You should wrap your final results in a way illustrated as the following:
                       %%%%%%%%%%
                       Explanation: Your Detailed Explanation
                       Judgement: Your Binary Judgement
                       %%%%%%%%%%
                       Strictly follow the instructions that have been claimed.
Overall                Is the formalized code a correct formalization of the natural language statement?
Logical Preservation   Does the formalized code capture the logical structure and content of the natural language statement?
Mathematical Con-      Does the formalized code accurately represent mathematical objects and operations present in the
sistency               natural language statement?
Formal Quality         Does the formalized code demonstrate high quality in terms of structural clarity and usefulness?
Pre-arg Structure      Does the formalized code reflect the inherent predicate-argument structure of the natural language
                       statement?
Quantification         Does the formalized code accurately formalize all quantifiers, such as universal and existential,
                       present in the natural language statement?
Formula                Are all mathematical formulas and expressions in the natural language statement, such as equations
                       and inequalities, correctly and completely represented in the formalized code?
Relation               Are the logical and mathematical relationships between propositions in the natural language state-
                       ment preserved in the formalized code?
Concept                Are all mathematical concepts mentioned in the natural language statement, such as integers,
                       fractions, real numbers, complex numbers, derivatives, integrals, vectors, matrices, probabilities,
                       expectations, and variances, are correctly formalized in the formalized code?
Constant               Are all mathematical constants mentioned in the natural language statement, such as 1, 23 , π, e, are
                       properly included in the formalized code?
Operator               Are all mathematical operators used in the natural language statement, such as addition, subtraction,
                       multiplication, division, summation, exponentiation, and product, are correctly represented in the
                       formalized code?
Conciseness            Is the formalized code expressed in a minimal, non-redundant form, avoiding unnecessary repetition
                       or complexity?
Logical Consistency    Is the formalized code internally coherent and contains no contradictions under the logical rules of
                       the relevant formal system?


                                         Table 11: LLM-as-a-judge prompts




                                                           15
