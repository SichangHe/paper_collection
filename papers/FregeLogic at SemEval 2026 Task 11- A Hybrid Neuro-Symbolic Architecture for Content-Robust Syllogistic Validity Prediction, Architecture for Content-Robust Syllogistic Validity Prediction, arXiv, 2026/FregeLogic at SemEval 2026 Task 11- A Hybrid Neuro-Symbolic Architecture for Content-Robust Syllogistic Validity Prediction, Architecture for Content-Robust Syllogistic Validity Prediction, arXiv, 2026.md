                                                FregeLogic at SemEval 2026 Task 11: A Hybrid Neuro-Symbolic
                                                 Architecture for Content-Robust Syllogistic Validity Prediction

                                                           Adewale Akinfaderin                                Nafi Diallo
                                                           Amazon Web Services                            Amazon Web Services
                                                               Seattle, WA                                    Seattle, WA
                                                           akinfaa@amazon.com                              nafid@amazon.com



                                                               Abstract                          pre-training, but these are susceptible to contami-
                                                                                                 nation from world knowledge (Kim et al., 2025), a
                                             We present FregeLogic, a hybrid neuro-
arXiv:2604.18328v1 [cs.CL] 20 Apr 2026




                                             symbolic system for SemEval-2026 Task 11
                                                                                                 phenomenon documented across tasks, model fam-
                                             (Subtask 1), which addresses syllogistic valid-     ilies, and domains (Wysocka et al., 2025; Ozeki
                                             ity prediction while reducing content effects       et al., 2024). SemEval-2026 Task 11 (Valentino
                                             on predictions. Our approach combines an            et al., 2026) formalizes this challenge by evaluat-
                                             ensemble of five LLM classifiers, spanning          ing systems on syllogistic validity prediction using
                                             three open-weights models (Llama 4 Maverick,        a combined metric that rewards both accuracy and
                                             Llama 4 Scout, and Qwen3-32B) paired with           low content effect.
                                             varied prompting strategies, with a Z3 SMT
                                             solver that serves as a formal logic tiebreaker.
                                                                                                    In this paper, we describe FregeLogic, a hy-
                                             The central hypothesis is that LLM disagree-        brid neuro-symbolic system that exploits the com-
                                             ment within the ensemble signals likely content-    plementary strengths of LLM ensembles and for-
                                             biased errors, where real-world believability in-   mal logic solvers. We construct a five-member
                                             terferes with logical judgment. By deferring to     ensemble from three open-weight model families
                                             Z3’s structurally-grounded formal verification      (Llama 4 Maverick, Llama 4 Scout, Qwen3-32B)
                                             on these disputed cases, our system achieves        paired with varied prompting strategies, then use
                                             94.3% accuracy with a content effect of 2.85
                                                                                                 the Z3 SMT solver (De Moura and Bjørner, 2008)
                                             and a combined score of 41.88 in nested 5-fold
                                             cross-validation on the dataset (N =960). This      as a tiebreaker when the ensemble produces a nar-
                                             represents a 2.76-point improvement in com-         row 3–2 vote split. The design is motivated by
                                             bined score over the pure ensemble (39.12),         an empirical observation: close votes in the en-
                                             with a 0.9% accuracy gain, driven by a 16% re-      semble disproportionately coincide with content-
                                             duction in content effect (3.39 → 2.85). Adopt-     biased errors, precisely the cases where a content-
                                             ing structured-output API calls for Z3 extrac-      neutral formal verifier can add value (Bayless et al.,
                                             tion reduced failure rates from ∼22% to near
                                                                                                 2025; Ranaldi et al., 2025). In nested 5-fold cross-
                                             zero, and an Aristotelian encoding with exis-
                                             tence axioms was validated against task anno-
                                                                                                 validation on the dataset (N =960), this selective
                                             tations. Our results suggest that targeted neuro-   intervention reduces content effect by 16% (3.39
                                             symbolic integration, applying formal methods       → 2.85) while improving accuracy by 0.9%, yield-
                                             precisely where ensemble consensus is low-          ing a combined score of 41.88 compared to 39.12
                                             est, can improve the combined accuracy-plus-        for the pure ensemble.
                                             content-effect metric used by this task.
                                                                                                 2     Background
                                         1   Introduction
                                         Syllogistic reasoning is a fundamental form of de-      2.1    Task Description and Metrics
                                         ductive inference studied extensively in logic and      SemEval-2026 Task 11 (Valentino et al., 2026) eval-
                                         cognitive science (Eisape et al., 2024; Bertolazzi      uates syllogistic reasoning while disentangling logi-
                                         et al., 2024). A key challenge in evaluating rea-       cal structure from semantic content. We participate
                                         soning capabilities of language models is content       in Subtask 1: binary classification of syllogisms
                                         effects: the tendency for real-world believability to   as valid or invalid. The dataset comprises 960 syl-
                                         interfere with purely logical judgment (Dasgupta        logisms annotated with validity labels and plausi-
                                         et al., 2022). Mechanistic analyses have shown that     bility metadata (believable/unbelievable), balanced
                                         language models develop reasoning circuits during       across four subgroups.
   The task uses a combined score that jointly                                 Input: Syllogism S
                                                                                        ↓
rewards high accuracy and low content effect
                                                                          LLM Ensemble (5 classifiers)
(CE), which measures how much a system’s pre-                    Selected per fold from 12 (model, prompt) pairs
dictions are influenced by believability rather than             across Maverick, Scout, Qwen × 4 prompt types
logical structure. The combined score applies a                                         ↓
                                                                          Vote vector [v1 , v2P
                                                                                              , v3 , v4 , v5 ]
logarithmic penalty for content bias: Score =                               Margin m = |2 vi − 5|
Accuracy/(1 + ln(1 + CE)). A content effect of                                          ↓
zero indicates predictions uninfluenced by believ-                              Decision Module
ability. Full metric definitions are in Valentino et al.              If m ≤ 1: use Z3 verdict (if available)
                                                                           Else: use ensemble majority
(2026).                                                                                 ↓
                                                                             Output: Valid / Invalid
2.2   Related Work
Content effects in LLMs. Dasgupta et al. (2022)            Figure 1: FregeLogic system architecture. The ensem-
                                                           ble produces a vote vector; when the margin is low (3–2
demonstrated that large language models exhibit
                                                           split), the system defers to Z3 formal verification.
human-like content effects across syllogism valid-
ity judgments and other reasoning tasks. Eisape
et al. (2024) showed that even the largest models          applying verification selectively only where ensem-
in the PaLM 2 family exhibit systematic biases in-         ble consensus is low, and from activation-steering
cluding sensitivity to variable ordering, a structural     approaches (Valentino et al., 2025; Maraia et al.,
bias related to, but distinct from, semantic content       2026) by requiring no access to model internals.
effects. Bertolazzi et al. (2024) found that pre-
trained LLM behavior can be explained by heuris-
                                                           3     System Overview
tics from cognitive science, and Ozeki et al. (2024)       Our system consists of three components: (1) an
confirmed that LLMs exhibit human-like reasoning           LLM ensemble that provides high-accuracy predic-
biases with primary limitations in the reasoning           tions through diverse model and prompt combina-
process itself.                                            tions, (2) a Z3-based formal verification pipeline
                                                           that provides structurally-grounded logical judg-
Mechanistic interpretations. Kim et al. (2025)
                                                           ments, and (3) a tiebreaker decision module that
uncovered a three-stage reasoning circuit for syllo-
                                                           routes predictions to Z3 only when the ensemble
gistic inference involving middle-term suppression
                                                           produces a narrow vote margin (3–2 split). Figure 1
and information propagation via mover heads. Crit-
                                                           provides an overview of the architecture.
ically, this circuit is susceptible to contamination
from belief biases encoded in additional attention         3.1    LLM Ensemble
heads, providing mechanistic evidence for content
                                                           The ensemble consists of five classifiers, each de-
effects and motivating our use of formal verifica-
                                                           fined by a (model, prompt) pair. We use three open-
tion.
                                                           weight models accessed via Amazon Bedrock:
Neuro-symbolic approaches. Ranaldi et al.                  Llama 4 Maverick (17B active parameters, MoE
(2025) proposed quasi-symbolic chain-of-thought            architecture), Llama 4 Scout (17B), and Qwen3
prompting to improve robustness on reasoning               (32B). These models were selected to maximize
tasks. Bayless et al. (2025) presented a neurosym-         architectural diversity (MoE vs. dense, two distinct
bolic framework for verifying logical correctness          model families) within a practical parameter bud-
using SMT solvers, and Akinfaderin and Subrama-            get (17B–32B active parameters), while remaining
nian (2026) applied similar ideas to financial AI.         accessible through a single inference API. They
Wysocka et al. (2025) showed that zero-shot LLMs           are paired with four prompting strategies to create
achieve between 23% and 70% on biomedical syllo-           diversity across both model family and reasoning
gistic reasoning. Valentino et al. (2025) and Maraia       elicitation method:
et al. (2026) explored activation-level approaches
                                                               • Zero-shot: A direct validity question with no
to mitigate content effects. Our work differs from
                                                                 examples.
pure-LLM approaches by introducing structurally-
grounded formal verification, from pure-formal ap-             • Few-shot: Seven worked examples of valid
proaches by handling paraphrase and extraction                   and invalid syllogisms with explicit validity
failures gracefully, from Bayless et al. (2025) by               rules, balanced across plausibility conditions.
   • Few-shot CoT: Worked examples with step-            ular negative) and its subject and predicate terms.
     by-step reasoning traces demonstrating struc-       We use Amazon Bedrock’s structured output API
     tural analysis, including a believable-invalid      with a JSON schema that enforces well-formed
     example that explicitly names the content           output, reducing extraction failures from approx-
     bias.                                               imately 22% (with free-form prompting) to near
                                                         zero. Extraction is attempted with each of the three
   • Simple CoT: A minimal prompt asking the             models in sequence (Maverick → Qwen → Scout,
     model to identify logical structure before an-      ordered by individual combined score), using the
     swering.                                            first successful parse. In practice, Maverick suc-
                                                         ceeds on 99.5–100% of cases across folds.
   The five configurations are selected per fold
based on combined score on a 200-sample inner            FOL encoding. Each proposition is encoded as a
subset (see Section 4). The selection naturally bal-     first-order formula over a declared sort Thing with
ances model and prompt diversity, following the          unary predicates for each term. Based on diagnos-
principle that ensemble accuracy benefits from un-       tic inspection of Felapton-type syllogisms in the
correlated errors across members (Bertolazzi et al.,     dataset (all labelled valid), we adopt an Aristotelian
2024).                                                   interpretation with existential import, adding ex-
   For each syllogism, all five classifiers produce      istence axioms (∃x : S(x)) for subject terms in
a binary prediction vi ∈ {0, 1}, where 1 indi-           universal propositions:
   P valid. The ensemble majority vote is ŷ =
cates
                                                            • Type A (“All S are P”): ∀x : S(x) → P (x) ∧
⊮[ i vi > 2.5].
                                                              ∃x : S(x)
   All models are called with temperature 0.0 to
maximize output reproducibility. Responses are              • Type E (“No S are P”): ∀x : S(x) →
parsed using a multi-stage regex pipeline that                ¬P (x) ∧ ∃x : S(x)
checks for explicit answer patterns (e.g., “AN-
SWER: true”), last-line heuristics, and fallback to         • Type I (“Some S are P”): ∃x : S(x) ∧ P (x)
the last occurrence of “true”, “false”, “valid”, or         • Type O (“Some S are not P”): ∃x : S(x) ∧
“invalid” in the response. Parse failures default to          ¬P (x)
invalid.
                                                         Satisfiability check. Validity is determined by a
3.2   Z3 Formal Verification                             two-step procedure. First, we verify premise con-
The Z3 component (De Moura and Bjørner, 2008)            sistency: if P1 ∧P2 is UNSAT (e.g., a Type I premise
provides structurally-grounded validity checking         paired with a contradicting Type E premise over
by encoding syllogisms in first-order logic (FOL)        the same terms), the premises are mutually incon-
and testing satisfiability. We select Z3 over alter-     sistent and Z3 returns ⊥, deferring to the ensemble.
native provers for three reasons: (1) its native sup-    This guards against ex contradictione quodlibet
port for quantifiers and uninterpreted sorts allows      false positives, where any conclusion would be triv-
direct encoding of syllogistic propositions with-        ially entailed by inconsistent premises. Otherwise,
out conversion to conjunctive normal form, unlike        validity is checked in the standard way:
resolution-based provers such as Prover9 (Olaus-
                                                           valid(S) ⇐⇒ (P1 ∧ P2 is SAT) ∧ (P1 ∧ P2 ∧ ¬C is UNSAT)
son et al., 2023); (2) its mature Python API enables
                                                                                                            (1)
tight integration with our LLM pipeline; and (3)
                                                            If the second check returns UNSAT, the syllogism
its proven effectiveness in neuro-symbolic NLP,
                                                         is valid; if SAT, it is invalid; if UNKNOWN (timeout
where it has been used alongside other solvers for
                                                         at 5000ms), the result is undefined (⊥). When
faithful logical reasoning (Pan et al., 2023; Bayless
                                                         structure extraction fails or produces malformed
et al., 2025). The pipeline consists of three stages.
                                                         output, Z3 also returns ⊥.
Structure extraction. An LLM is prompted to                 The Z3 solver is content-neutral by construction,
extract the logical structure of the syllogism as        since the formal encoding strips away all semantic
a JSON object containing the three terms, two            content. However, the end-to-end pipeline’s con-
premises, and conclusion, each annotated with its        tent independence is contingent on the extraction
proposition type (A: universal affirmative, E: uni-      step. Our extraction failure disaggregation (Sec-
versal negative, I: particular affirmative, O: partic-   tion 5) confirms that failure rates are uniform across
plausibility subgroups. Pipeline accuracy depends      Strategy             Acc          CE            Score
                                                       Ensemble (pure)    93.4±1.5    3.39±1.30     39.12±5.37
entirely on correct structure extraction, which can    + Z3 Tiebreaker    94.3±0.9   2.85±1.23      41.88±5.97
fail when the LLM misidentifies proposition types      + Z3 Weighted      93.4±1.5    3.39±1.30     39.12±5.37
or term boundaries.                                    + Z3 Veto          74.1±2.1   26.70±2.97     17.18±0.84
                                                       Confidence + Z3    91.7±1.1    6.15±2.00     31.77±3.82
                                                       Top 3 + Z3         92.2±2.0    5.08±2.25     34.11±4.36
3.3    Tiebreaker Decision Fusion                      Z3 Only            74.7±2.0   26.28±2.88     17.39±0.87

The decision module combines ensemble and Z3          Table 1: Comparison of fusion strategies (mean ± std
predictions based on vote consensus, measured by      across 5 outer folds). The tiebreaker strategy achieves
the vote margin:                                      the best combined score. Bold indicates the best result.

                           P
             m(S) = |2 ·       i vi − n|        (2)
                                                      Existential import. To determine the correct
                                                      FOL encoding, we inspected the dataset for
where n = 5 is the number of classifiers. For         Darapti-type (AAI-3) and Felapton-type (EAO-3)
n = 5, the margin is 5 (unanimous), 3 (4–1 split),    syllogisms, whose validity depends on whether ex-
or 1 (3–2 split).                                     istential import is assumed. No Darapti candidates
   The final prediction is:                           were found; seven Felapton candidates were found,
              (                                       all labelled valid. This confirms an Aristotelian
               z(S) m(S) ≤ 1 ∧ z(S) ̸= ⊥              interpretation, and we add existence axioms ac-
    pred(S) =
               ŷ(S) otherwise                        cordingly (Section 3.2).
                                              (3)
where z(S) is the Z3 verdict and ŷ(S) is the en-     5     Results and Analysis
semble majority vote. The threshold τ = 1 means       5.1    Individual Model Performance
Z3 is consulted only on 3–2 splits, which we hy-
pothesize correspond to cases where content bias      Table 5 (Appendix D) presents results for all 12
causes disagreement among the LLMs.                   model-prompt combinations from a representative
                                                      Phase 1 inner fold. Accuracy varies modestly
4     Experimental Setup                              across configurations (79.5–89.0%), but content ef-
                                                      fect varies substantially (3.49–13.71), driving large
The dataset provided by the task organizers           differences in combined score. The best prompt
(Valentino et al., 2026) contains N =960 syllo-       strategy differs by model: Maverick favours zero-
gisms annotated with validity labels and plausi-      shot and few-shot, while Qwen benefits from chain-
bility metadata, balanced across four subgroups:      of-thought. Notably, Simple CoT achieves the low-
valid-believable (240), valid-unbelievable (240),     est average content effect (5.24) despite being the
invalid-believable (234), and invalid-unbelievable    most under-specified prompt, suggesting that min-
(246). No separate development set was provided.      imal instructions may allow models to engage in-
   We adopt a nested 5-fold cross-validation pro-     ternal structural reasoning rather than anchoring to
tocol to separate model selection from evaluation.    example content. Chain-of-thought does not uni-
In each outer fold, 768 syllogisms are used for       formly reduce content effects; for Maverick, few-
calibration and 192 for evaluation. Within each       shot CoT increases CE from 3.83 to 10.11 com-
calibration set, a 200-sample inner subset is ran-    pared to plain few-shot.
domly drawn for Phase 1 model selection, where
all 12 combinations of 3 models and 4 prompts         5.2    Ensemble and Hybrid Strategies
are scored. Two additional OpenAI models (GPT-        Table 1 compares six fusion strategies aggregated
OSS-120B and GPT-OSS-20B) were evaluated in           across the five outer folds. The pure ensemble
preliminary experiments but excluded due to low       achieves 93.4% accuracy but a content effect of
combined scores (14.7–21.0; see Appendix C). The      3.39. The Z3-only baseline achieves low accuracy
top five configurations by combined score are se-     (74.7%) with a high content effect (26.28), driven
lected per fold to form the ensemble. All LLM         by systematic over-prediction of invalidity.
calls use Amazon Bedrock with temperature 0.0.           The tiebreaker strategy achieves the best com-
The Z3 solver uses the Python API with a 5000ms       bined score (41.88) by reducing the content effect
timeout. Full prompts are in Appendix A.              from 3.39 to 2.85, a 16% reduction, while also im-
      Strategy          VB     VU      IB     IU                 Metric                              Count     %
      Ensemble (pure)   95.9   96.0   90.2   91.9                Total evaluation instances            960    100
      + Z3 Tiebreaker   95.6   93.8   94.5   93.5                5–0 or 4–1 splits                     884    92.1
      Z3 Only           50.5   53.9   98.0   97.2                3–2 splits (tiebreaker triggered)      76    7.9
                                                                   Z3 available on splits               76   100.0
Table 2: Subgroup accuracy (%) for key strategies, aver-           Degenerate premises                   1    0.1
aged across folds. VB = Valid-Believable, VU = Valid-            Z3 override decisions                  30
                                                                   Correct flips                        19
Unbelievable, IB = Invalid-Believable, IU = Invalid-               Wrong flips                          11
Unbelievable.
                                                           Table 3: Tiebreaker behavior aggregated across all five
                                                           outer folds.
proving accuracy by 0.9 percentage points. This is
consistent with our hypothesis that ensemble dis-
agreements correspond to content-biased cases that         76), above the 40% expected by chance, suggesting
Z3 can help correct.                                       greater susceptibility to content bias. Conversely,
   Table 2 provides subgroup accuracy for the key          Maverick+FS appears in the minority least often
strategies. The tiebreaker achieves more balanced          (28.9%, 22 of 76), well below the 40% chance base-
accuracy across all four subgroups than either the         line, indicating the strongest resistance to content
pure ensemble or Z3 alone. The pure ensemble               effects among the five classifiers.
shows a gap between valid subgroups (95.9–96.0%)
and invalid subgroups (90.2–91.9%); the tiebreaker         5.4    Z3 Invalidity Bias
narrows this gap (93.5–95.6%), with the largest            The Z3-only baseline exhibits a pronounced invalid-
gains on invalid-believable cases (90.2% → 94.5%)          ity bias: it achieves 97.6% accuracy on invalid syl-
where content bias is strongest.                           logisms (IB: 98.0%, IU: 97.2%) but only 52.2% on
   The remaining strategies perform worse: Z3 veto         valid ones (VB: 50.5%, VU: 53.9%). Because the
(score 17.18) overrides correct high-consensus pre-        Z3 solver itself is deterministically correct given
dictions, the weighted strategy never flips a ma-          well-formed input, this asymmetry originates in
jority, and the confidence-based strategy (91.7%)          the extraction step. When the LLM misidentifies
trusts Z3 on both 3–2 and 4–1 splits (effectively          a proposition type or term boundary in a valid syl-
lowering the margin threshold to τ =3), overriding         logism, the resulting FOL encoding almost always
the ensemble on 37–52 cases per fold compared to           breaks the entailment chain, causing Z3 to cor-
13–19 for the tiebreaker. Because Z3 accuracy on           rectly report unsatisfiability of the (now-corrupted)
valid syllogisms is low (48.6% on 3–2 split cases;         logical structure. Extraction errors on invalid syl-
see Section 5.4), extending Z3 authority to higher-        logisms are less consequential: the syllogism is
consensus cases where the ensemble is typically            already non-entailing, so a different structural error
correct degrades overall performance.                      is unlikely to accidentally produce a valid deriva-
                                                           tion. This directional asymmetry explains both
5.3   Analysis of Tiebreaker Behavior                      the Z3-only subgroup collapse on valid cases and
Table 3 summarizes the tiebreaker mechanism’s              why the tiebreaker restricts Z3 authority to low-
behavior aggregated across all five folds. The 3–2         consensus cases, where the benefit of correcting
vote split occurs in 7.9% of cases (76 of 960). Z3         content-biased ensemble errors outweighs the risk
produces a usable verdict on all 76 cases, enabled         of extraction-induced false invalidity verdicts.
by structured-output extraction which reduced fail-
ures to near zero. Of the 30 cases where Z3 over-          5.5    Error Analysis
rides the ensemble majority, 19 are correct flips          Three main error sources remain: (1) Z3 extraction
and 11 are wrong flips, yielding a net improvement         errors, where incorrect structure extraction (e.g.,
of 8 correct predictions.                                  misidentified proposition types) produces wrong
   When all five LLMs agree, the logical signal is         Z3 verdicts, accounting for 11 wrong flips across
typically strong enough to overcome content bias.          all folds; (2) unanimous ensemble errors, where
The 3–2 splits indicate cases where some models            all five LLMs agree incorrectly on syllogisms with
are swayed by content while others are not; Z3             strong content bias, preventing tiebreaker interven-
resolves these independently of semantic content.          tion; and (3) degenerate premises, where mutually
Coalition analysis reveals that Scout appears in the       inconsistent premises trigger the consistency check
minority coalition on 53.9% of 3–2 splits (41 of           and Z3 defers to the ensemble (1 case across all
     (a) Proposition type error        AAI-1, unbelievable      reduced Z3 failure rates from approximately 22%
    “There are no humans that are not made of glass. Every      to near zero, and a two-step satisfiability check
     single thing made of glass is indestructible. ∴ some
     indestructible things are humans.”
                                                                with Aristotelian existential import was validated
     True: Valid Z3: Invalid Cause: Double negative             against task annotations. Future work includes
    “no . . . not” → type E instead of A                        investigating whether the tiebreaker mechanism
                                                                generalizes to other reasoning tasks and exploring
     (b) Term boundary error Darii IAI-3, unbelievable          adaptive thresholds for the vote margin cutoff.
    “Some fish are penguins. All penguins belong to the
     class of birds. ∴ some birds are fish.”
                                                                Limitations
     True: Valid Z3: Invalid Cause: “belong to the
     class of” → splits “class of birds” as compound term       While our approach involves no parameter updates,
                                                                model and prompt selection, fusion strategy selec-
     (c) Non-standard quantifier            Felapton EAO-1,
     believable                                                 tion, and the tiebreaker threshold (τ =1) were all
    “Anything that is a rose is a flower. Under no circum-      tuned via nested cross-validation on the provided
     stances is a flower a tree. ∴ some trees are not roses.”   dataset; no independent test set was used. This
     True: Valid Z3: Invalid Cause: “Under no cir-              selection procedure adds non-trivial setup com-
     cumstances” → may invert subject-predicate or miss
     E-type                                                     plexity: each fold requires scoring all 12 (model,
                                                                prompt) combinations on a 200-sample inner sub-
Figure 2: Three representative wrong flips. All 11 go in        set before the top-five ensemble is fixed, and the
the same direction: Z3 falsely rejects valid syllogisms         optimal configuration differs across folds (Ap-
due to extraction errors, not encoding errors.                  pendix D), so the approach does not reduce to a sin-
                                                                gle off-the-shelf recipe. The Z3 pipeline depends
folds).                                                         on LLM-based structure extraction, which, despite
   Extraction failure disaggregation confirms that              structured-output enforcement, can still produce se-
the structured-output pipeline is content-neutral:              mantically incorrect extractions (e.g., misidentified
failure rates are 0.0% for VB, IB, and IU subgroups,            proposition types), accounting for the 11 wrong
and 0.4% for VU (1 of 241 cases), consistent with               flips observed. Our system requires six LLM API
uniform distribution.                                           calls per syllogism (five ensemble plus one extrac-
                                                                tion) and one Z3 solve, totalling approximately
   All 11 wrong flips share the same direction: Z3
                                                                4,300 tokens and 12.1 seconds of sequential la-
falsely rejects a valid syllogism. Eight involve
                                                                tency per instance (2.8 seconds with parallel en-
unbelievable content, where absurd premises may
                                                                semble calls); Z3 solving adds under 10ms. Full
compound extraction difficulty. Figure 2 presents
                                                                cost profiling over 18,722 API calls is reported in
three representative cases. In each, the Z3 solver
                                                                Appendix G. We did not compare against larger
produces a correct verdict given the (incorrectly)
                                                                single dense models (e.g., 70B+); whether architec-
extracted structure, confirming that the bottleneck
                                                                tural diversity at smaller scale outperforms a single
is extraction fidelity, not logical encoding.
                                                                larger model on this task remains an open question
   Additional analysis of prompt strategies is in
                                                                for future work.
Appendix E.
                                                                Acknowledgments
6     Conclusion
                                                                We thank the SemEval-2026 Task 11 organizers
We presented FregeLogic, a hybrid neuro-symbolic
                                                                for designing a task that foregrounds the important
system that combines an LLM ensemble with Z3
                                                                challenge of content effects in reasoning evalua-
formal verification via a tiebreaker mechanism for
                                                                tion.
syllogistic validity prediction. Our results support
the hypothesis that ensemble disagreement signals
content-biased predictions, which formal logic can              References
help correct. In nested 5-fold cross-validation on              Adewale Akinfaderin and Shreyas Subramanian. 2026.
the dataset (N =960), the tiebreaker achieves a                   VERAFI: Verified agentic financial intelligence
combined score of 41.88, a 2.76-point improve-                    through neurosymbolic policy generation. In AAAI
ment over the pure ensemble driven by a 16% re-                   2026 Workshop on Agentic AI in Financial Services.
duction in content effect and a 0.9% accuracy gain.             Sam Bayless, Stefano Buliani, Darion Cassel, Byron
Adopting structured-output API calls for extraction               Cook, Duncan Clough, R’emi Delmas, Nafi Diallo,
  Ferhat Erata, Nick Feng, Dimitra Giannakopoulou,         Leonardo Ranaldi, Marco Valentino, and Andr’e Fre-
  and 1 others. 2025. A neurosymbolic approach to nat-       itas. 2025. Improving chain-of-thought reasoning via
  ural language formalization and verification. arXiv        quasi-symbolic abstractions. In Proceedings of the
  preprint arXiv:2511.09008.                                 63rd Annual Meeting of the Association for Compu-
                                                             tational Linguistics.
Leonardo Bertolazzi, Albert Gatt, and Raffaella
  Bernardi. 2024. A systematic analysis of large lan-      Marco Valentino, Geonhee Kim, Dhairya Dalal, Zhixue
  guage models as soft reasoners: The case of syllo-         Zhao, and Andr’e Freitas. 2025. Mitigating con-
  gistic inferences. In Proceedings of the 2024 Con-         tent effects on reasoning in language models through
  ference on Empirical Methods in Natural Language           fine-grained activation steering. arXiv preprint
  Processing, pages 13882–13905.                             arXiv:2505.12189.

Ishita Dasgupta, Andrew K Lampinen, Stephanie CY           Marco Valentino, Leonardo Ranaldi, Giulia Pucci, Fed-
   Chan, Hannah R Sheahan, Antonia Creswell, Dhar-          erico Ranaldi, and André Freitas. 2026. SemEval-
   shan Kumaran, James L McClelland, and Felix              2026 task 11: Disentangling content and formal rea-
   Hill. 2022. Language models show human-like              soning in large language models. In Proceedings of
   content effects on reasoning tasks. arXiv preprint       the 20th International Workshop on Semantic Evalu-
   arXiv:2207.07051.                                        ation (SemEval-2026).

Leonardo De Moura and Nikolaj Bjørner. 2008. Z3: An        Magdalena Wysocka, Danilo Carvalho, Oskar Wysocki,
  efficient SMT solver. In Proceedings of the 14th In-      Marco Valentino, and Andr’e Freitas. 2025.
  ternational Conference on Tools and Algorithms for        SylloBio-NLI: Evaluating large language models on
  the Construction and Analysis of Systems (TACAS),         biomedical syllogistic reasoning. In Proceedings of
  pages 337–340. Springer.                                  the 2025 Conference of the Nations of the Ameri-
                                                            cas Chapter of the Association for Computational
Tiwalayo Eisape, Michael Tessler, Ishita Dasgupta, Fei      Linguistics, pages 7235–7258.
  Sha, Sjoerd van Steenkiste, and Tal Linzen. 2024.
  A systematic comparison of syllogistic reasoning in      A     Prompt Templates
  humans and language models. In Proceedings of the
  2024 Conference of the North American Chapter of         We provide the four prompt templates used in our
  the Association for Computational Linguistics.           system. In each template, {syllogism} is replaced
                                                           with the input syllogism text.
Geonhee Kim, Marco Valentino, and Andr’e Freitas.
  2025. Reasoning circuits in language models: A           A.1    Zero-Shot Prompt
  mechanistic interpretation of syllogistic inference.
  In Findings of the Association for Computational               Determine if this syllogism is VALID.
  Linguistics: ACL 2025, pages 10074–10095.                      VALID means: IF the premises were true,
                                                                 the conclusion MUST be true. Ignore
Giovanni Maraia, Marco Valentino, Fabio Massimo Zan-             whether premises are actually true in
  zotto, and Leonardo Ranaldi. 2026. Abstract activa-            the real world.
  tion spaces for content-invariant reasoning in large           Syllogism: {syllogism}
  language models. arXiv preprint arXiv:2602.02462.              Answer with exactly one word: true or
                                                                 false
Theo X. Olausson, Alex Gu, Benjamin Lipkin, Cede-
  gao E. Zhang, Armando Solar-Lezama, Joshua B.
                                                           A.2    Few-Shot Prompt
  Tenenbaum, and Roger Levy. 2023. LINC: A neu-
  rosymbolic approach for logical reasoning by com-              Determine if this syllogism is VALID
  bining language models with first-order logic provers.         (conclusion necessarily follows from
                                                                 premises).
  In Proceedings of the 2023 Conference on Empiri-
  cal Methods in Natural Language Processing, pages              VALIDITY RULES:
  5153–5176.                                                     - “All A are B” + “All B are C” -> “All
                                                                 A are C” (valid)
Kazuki Ozeki, Risako Ando, Takuro Morishita, Hiro-               - “No A are B” + “All C are A” -> “No C
  hiko Abe, Koji Mineshima, and Mitsuhiro Okada.                  are B” (valid)
                                                                 - “All A are B” + “Some C are A” -> “Some
  2024. Exploring reasoning biases in large lan-                  C are B” (valid)
  guage models through syllogism: Insights from the              - “All A are B” + “All C are B” -> “All A
  NeuBAROCO dataset. In Findings of the Association               are C” (invalid, undistributed middle)
  for Computational Linguistics: ACL 2024.                       - “Some A are B” does NOT guarantee “All
                                                                 A are B”
Liangming Pan, Alon Albalak, Xinyi Wang, and                     EXAMPLES:
  William Yang Wang. 2023. LOGIC-LM: Empow-                      “All dogs are mammals.    All mammals
  ering large language models with symbolic solvers              are animals. Therefore, all dogs are
  for faithful logical reasoning. In Findings of the As-         animals.” -> true
  sociation for Computational Linguistics: EMNLP                 “All birds are dinosaurs. All sparrows
  2023, pages 3806–3824.                                         are birds. Therefore, all sparrows are
      dinosaurs.” -> true                                Example 5: “All cats are pets. All dogs
      “No fish are mammals. All sharks are               are pets. Therefore, all cats are dogs.”
      fish. Therefore, no sharks are mammals.”          - Both subsets of pets, but could be
      -> true                                            separate
      “All reptiles are cold-blooded. Some              - Undistributed middle. ANSWER: false
      lizards are reptiles. Therefore, some              Example 6: “Some birds can fly. All
      lizards are cold-blooded.” -> true                 penguins are birds. Therefore, some
      “All lawyers are professionals.      All           penguins can fly.”
      doctors are professionals. Therefore,             - “Some birds” doesn’t tell us WHICH
      all lawyers are doctors.” -> false                 birds
      “Some politicians are corrupt.       All          - Cannot guarantee any penguin is in the
      senators are politicians.     Therefore,           flying subset. ANSWER: false
      some senators are corrupt.” -> false
      “All rocks are edible.      Some clouds           Syllogism: {syllogism}
      are rocks. Therefore, all clouds are              Think through the structure briefly,
      edible.” -> false                                 then write your final answer as: ANSWER:
      Syllogism: {syllogism}                            true or ANSWER: false
      Answer with exactly one word: true or
      false                                       A.4    Simple Chain-of-Thought Prompt
                                                        Is this syllogism logically VALID? (If
A.3    Few-Shot Chain-of-Thought Prompt                 premises were true, must conclusion be
                                                        true?)
      Analyze   this     syllogism’s   logical
      VALIDITY.                                         Syllogism: {syllogism}
                                                        First, identify the logical structure.
      IMPORTANT: VALID = conclusion MUST
                                                        Then determine if the conclusion
      follow IF premises are assumed true.
                                                        necessarily follows.
      Ignore real-world facts.
                                                        End your response with exactly: ANSWER:
      RULES:
                                                        true or ANSWER: false
      - “All A are B” + “All B are C” -> “All
      A are C” (valid chain)
      - “No A are B” + “All C are A” -> “No C     B     Z3 Structure Extraction Prompt
      are B” (valid exclusion)
      - “All A are B” + “Some C are A” -> “Some   The following prompt is used to extract syllogis-
      C are B” (Darii)                            tic structure for Z3 encoding. When supported,
      - “All A are B” + “All C are B” -> “All A
      are C” (invalid, undistributed middle)      extraction uses Bedrock’s structured output API
      - “Some A are B” means ONLY SOME, not all   with a JSON schema enforcing the expected for-
      WORKED EXAMPLES:                            mat; otherwise, the model’s free-form response is
      Example 1: “All cats are mammals. All       parsed.
      mammals are animals. Therefore, all cats
      are animals.”                                     Extract the logical structure of this
      - Structure: cats ⊆ mammals ⊆ animals             syllogism.
      - Chain is complete. ANSWER: true                 SYLLOGISM: {syllogism}
      Example 2: “All unicorns fly. All pegasi           Proposition types:
      are unicorns. Therefore, all pegasi               - A: “All S are P” / “Every S is P”
      fly.”                                             - E: “No S are P”
      - Premises are fantasy but structure is:          - I: “Some S are P” / “At least one S is
      pegasi ⊆ unicorns ⊆ fly                            P”
      - Valid chain regardless of real-world            - O: “Some S are not P”
      truth. ANSWER: true
                                                        The          CONCLUSION         follows
      Example 3: “All athletes are healthy.             “therefore/hence/thus/consequently/so”.
      All healthy people exercise. Therefore,
                                                        Output ONLY this JSON (replace t1/t2/t3
      all athletes exercise.”
                                                        with the exact term WORDS from the
      - Chain: athletes -> healthy -> exercise
                                                        syllogism text):
      - Chain is complete. ANSWER: true
                                                        {"terms": ["t1", "t2", "t3"],
      Example    4:     “All    doctors   are           "premise1": {"type": "A/E/I/O",
      professionals.       All lawyers are              "subject": "term <- exact word(s) from
      professionals. Therefore, all doctors             text",
      are lawyers.”                                     "predicate": "term <- exact word(s) from
      - “Professionals” appears as PREDICATE            text"},
      in both premises.                                 "premise2": {"type": "A/E/I/O",
      - Middle term is undistributed: we only           "subject": "term <- exact word(s) from
      know both are subsets of professionals,           text",
      not that they overlap.                            "predicate": "term <- exact word(s) from
      - Despite the believable surface, the             text"},
      structure is invalid. ANSWER: false               "conclusion": {"type": "A/E/I/O",
    Model        Prompt        Acc     CE      Score        ing it for Qwen, indicating an interaction between
    GPT-120B     Zero-Shot     80.0   15.71    20.96
    GPT-120B     Few-Shot      78.0   18.64    19.61        model architecture and reasoning elicitation. This
    GPT-120B     FS-CoT        76.0   20.32    18.72        suggests that minimal reasoning prompts may be
    GPT-120B     Simple CoT    75.5   19.88    18.69        preferable to elaborate demonstrations when the
    GPT-20B      Zero-Shot     79.0   13.67    21.43
    GPT-20B      Few-Shot      78.5   14.71    20.91        goal is content-independent reasoning.
    GPT-20B      FS-CoT        73.0   18.92    18.29
    GPT-20B      Simple CoT    65.5   31.14    14.65            Prompt Type     Avg Acc   Avg CE     Avg Score
                                                                Zero-Shot        82.50     8.69        26.94
Table 4: Results for excluded models on a 200-sample            Few-Shot         85.50     7.37        28.60
evaluation set. These models exhibited higher content           Few-Shot CoT     88.67     8.84        27.59
                                                                Simple CoT       85.67     5.24        30.31
effects on average than the selected models, particularly
for chain-of-thought prompts, resulting in lower com-       Table 6: Average metrics by prompt type across three
bined scores across all four prompt types.                  models on a representative 200-sample inner fold.
    Model       Prompt        Acc      CE     Score
    Maverick    Zero-Shot     86.0     3.49   34.38
    Maverick    Few-Shot      88.0     3.83   34.17         F   Strategy Trade-offs
    Maverick    FS-CoT        88.5    10.11   25.97
    Maverick    Simple CoT    84.0     5.86   28.71         Figure 3 shows subgroup accuracy for the three key
    Scout       Zero-Shot     81.0    13.71   21.96         strategies. The tiebreaker (solid green) achieves the
    Scout       Few-Shot      89.0     6.92   29.00
    Scout       FS-CoT        88.5    11.21   25.27
                                                            most symmetric profile, while the pure ensemble
    Scout       Simple CoT    85.0     4.79   30.84         (dashed blue) favours valid subgroups and Z3 Only
    Qwen        Zero-Shot     80.5     8.86   24.48         (dotted red) favours invalid subgroups.
    Qwen        Few-Shot      79.5    11.37   22.62
    Qwen        FS-CoT        89.0     5.20   31.52
    Qwen        Simple CoT    88.0     5.07   31.39

Table 5: Individual model-prompt results from a rep-
resentative Phase 1 inner fold (200 samples). Acc =
Accuracy (%), CE = Content Effect, Score = Combined
Score. FS-CoT = Few-Shot Chain-of-Thought.


     "subject": "term <- exact word(s) from
     text",
     "predicate": "term <- exact word(s) from
     text"}}

C    Excluded Models
Table 4 reports results for GPT-OSS-120B and
GPT-OSS-20B, which were evaluated but excluded
from the final ensemble due to low combined scores
driven by high content effects.
                                                            Figure 3: Subgroup accuracy by strategy. The tiebreaker
                                                            achieves the most balanced profile across all four sub-
D    Individual Model Results
                                                            groups.
Table 5 presents results for all 12 model-prompt
configurations from a representative Phase 1 inner
fold (200 samples).                                         G    Computational Cost
                                                            Table 7 reports per-component cost profiling from
E    Prompt Strategy Analysis
                                                            the full nested cross-validation run (18,722 API
Table 6 shows average metrics by prompt type                calls across model selection and evaluation phases).
across the three selected models on a representa-           Qwen3-32B is the fastest model per call (median
tive 200-sample inner fold. Simple CoT achieves             1.1s), while Maverick and Scout average 2.5–2.8s
the best average combined score (30.31) due to              at the median. Z3 solving is negligible: 960 calls
its low content effect (5.24), despite not having           complete in 8.5 seconds total (median 7ms). At
the highest accuracy. Few-shot CoT increases con-           inference time, each syllogism requires five ensem-
tent effect for Maverick and Scout while decreas-           ble calls, one extraction call, and one Z3 solve,
Figure 4: Per-call cost distributions across the full cross-validation run (18,722 calls). (a) LLM ensemble latency,
(b) Z3 solver latency (note the millisecond scale), (c) input tokens per call, (d) output tokens per call. Outliers
suppressed for readability. The computational bottleneck is LLM inference, not formal verification.


 Component                n    p50 (s)   p95 (s)   Tokens   times are three orders of magnitude smaller than
 Maverick (ens.)      7,264      2.55      5.25     5.84M
 Scout (ens.)         4,576      2.82      5.26     3.69M   any LLM call, confirming that the formal verifica-
 Qwen3-32B (ens.)     5,920      1.11      1.86     3.35M   tion step adds negligible overhead.
 Qwen3-32B (extr.)        2     0.49      0.49       1.4K
 Z3 Solver              960     0.007     0.009       —
 Total               18,722                        12.87M

Table 7: Per-component cost profiling across the full
nested 5-fold cross-validation run. n = number of calls,
p50/p95 = median and 95th-percentile latency, Tokens
= total input + output tokens. Extraction calls are rare
because Maverick succeeds on >99.5% of cases.



consuming approximately 2,200 input tokens and
2,100 output tokens.
   Figure 4 shows per-call distributions across all
four dimensions. LLM ensemble calls range from
1 to 5 seconds, with Qwen3-32B consistently faster
than the Llama 4 models but consuming more in-
put tokens due to longer prompt encodings. Mav-
erick and Scout produce more output tokens on
average (488 and 480 vs. 228 for Qwen), reflecting
more verbose chain-of-thought responses. Z3 solve
