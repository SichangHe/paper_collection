                                             Characterizing Paraphrase-Induced Failures in Lean 4 Autoformalization


                                                                              William Feng * 1 Ethan Lou * 1 Aryan Sharma * 1


                                                                   Abstract                                      would allow for targeted training-time interventions, effec-
                                                                                                                 tively improving the reliability of generated autoformaliza-
                                              Lean 4 autoformalization has become increas-
                                                                                                                 tions.
                                              ingly popular in recent years, with frontier lan-
arXiv:2604.23135v2 [cs.LG] 17 May 2026




                                              guage models and open-weight autoformalizers                       We study this gap in Lean 4 by using a controlled suite of
                                              now producing valid formalizations of mathemat-                    60 deterministic paraphrase rules applied to ProofNet# (a
                                              ical theorems. However, these evaluations often                    dataset of 185 formalized undergraduate-level theorems)
                                              rely on single canonical phrasings of theorems                     and miniF2F (a dataset of 244 formalized Olympiad-level
                                              and rarely probe whether outputs are robust to                     problems). Each rule is implemented as a regex-based sur-
                                              natural variation in inputs, while prior work has                  face trigger preserving semantic meaning. Rules only edit a
                                              shown that semantically equivalent paraphrases                     single, named linguistic axis, e.g., conditional restructuring,
                                              often induce divergent formal outputs. We study                    concept renaming, or quantifier rephrasing — this design
                                              the structure of these divergences in Lean 4 by ap-                lets us attribute paraphrase-driven variance to specific in-
                                              plying deterministic paraphrase rules to datasets                  put features and measure consistency rates by category, in
                                              of undergraduate and Olympiad-level math prob-                     contrast to LLM-paraphrased perturbations (Moore & Shah,
                                              lems. Across four frontier models and three open-                  2025), which combine multiple linguistic axes into single
                                              weight autoformalizers, we find that paraphrase                    edits. We evaluate four frontier models (o3, GPT-5.4, o1,
                                              sensitivity is dominated by failures at the code-                  o4-mini) and three open-weight 7B autoformalizers (Kim-
                                              generation layer, and that these failures are typed                ina, Herald, DeepSeek-Prover-V2) on our suite of rules, and
                                              differently by dataset. Furthermore, these patterns                score their paired outputs using BEq+ (Poiroux et al., 2025)
                                              generalize to open-weight models, showing that                     for semantic equivalence and GTED (Liu et al., 2025c) for
                                              state-of-the-art autoformalizers still struggle to                 structural similarity.
                                              generate valid Lean code. Our results provide a
                                                                                                                 Our main finding is that paraphrase sensitivity in Lean 4
                                              failure-mode taxonomy for autoformalization and
                                                                                                                 autoformalization is dominated by code-generation failures,
                                              motivate training-time interventions targeted at
                                                                                                                 rather than by semantic disagreement among compiling
                                              specific compilation failures.
                                                                                                                 outputs. Surface consistency (i.e., pairs whose baseline
                                                                                                                 and perturbed outputs are equivalent as per BEq+) rates
                                                                                                                 are low (19–56% across models), and most inconsistency
                                         1. Introduction                                                         arises from pairs where at least one output fails to compile.
                                         Lean 4 autoformalization has matured rapidly in recent                  Moreover, these failures are typed differently by dataset:
                                         years, with frontier language models and open-weight auto-              on ProofNet#, models hallucinate Mathlib API identifiers
                                         formalizers (Wang et al., 2025; Gao et al., 2025; Ren et al.,           that do not exist (34–50% of failures); on miniF2F, they
                                         2025) now producing valid formalizations on a meaningful                produce malformed syntax or fail elaboration (47–70% of
                                         fraction of standard benchmarks (Azerbayev et al., 2023;                failures). These same patterns appear on the open-weight
                                         Zheng et al., 2022). However, these benchmarks evaluate                 panel, indicating that state-of-the-art autoformalizers still
                                         theorems on single natural-language phrasings, and rarely               struggle to generate valid Lean code.
                                         probe whether outputs are stable under input variations.                Together, these results contribute (i) a failure-mode taxon-
                                         Prior work has shown that semantically equivalent para-                 omy for Lean 4 autoformalization under paraphrases, (ii) an
                                         phrases of the same theorem can induce divergent formal                 empirical characterization of the failures across frontier and
                                         outputs (Moore & Shah, 2025), but it remains unclear how                autoformalizer models, and (iii) evidence that paraphrase ro-
                                         these failures are structured. Characterizing this structure            bustness in autoformalization is primarily a code-generation
                                           *
                                             Equal contribution 1 Yale University, New Haven, Connecticut,       problem. Finally, they motivate training-time interven-
                                         USA. Correspondence to: Ethan Lou <ethan.lou@yale.edu>.                 tions targeted at specific compilation-failure modes, such as
                                                                                                                 retrieval-augmented identifier resolution for ProofNet#-style
                                         Preprint.

                                                                                                             1
                          Characterizing Paraphrase-Induced Failures in Lean 4 Autoformalization

failures and compiler-feedback fine-tuning for miniF2F-             tablishing meaning preservation (Appendix B.1). Of these,
style failures, rather than generic robustness measures.            14 rules apply on ProofNet# and 37 on miniF2F. These are
                                                                    dataset-specific coverage counts rather than a partition of
2. Related Work                                                     the 60-rule suite: a rule is applied only when its trigger
                                                                    matches and its guards pass on that corpus.1 For each theo-
Autoformalization refers to the translation of natural-             rem, we refer to the original natural language phrasing as
language mathematics into a machine-verifiable formal lan-          the baseline and its rule-rewritten version as the perturbed
guage (Wu et al., 2022; de Moura & Ullrich, 2021). Recent           input. A paraphrase pair consists of the model’s baseline
work has substantially improved closed- and open-weight             and perturbed Lean outputs for a given theorem and rule.
autoformalizers, including Lean-oriented systems (Lu et al.,
2024; Gao et al., 2025; Liu et al., 2025b; Wang et al., 2025;       Datasets. ProofNet# contributes 185 undergraduate the-
Ren et al., 2025) and retrieval-augmented approaches for            orems that often require nontrivial Mathlib API naviga-
premise selection over Mathlib (Yang et al., 2023).                 tion to formalize, while miniF2F contributes 244 olympiad
                                                                    problems paired with standardized Lean formalizations that
Despite this progress, autoformalization benchmarks (Azer-
                                                                    closely mirror their natural language statements. This con-
bayev et al., 2023; Zheng et al., 2022; Poiroux et al., 2025)
                                                                    trast lets us test two different sources of fragility: whether
typically evaluate models on a single canonical natural-
                                                                    models can find the correct existing definitions and lemmas
language phrasing per theorem. Recent work has shown
                                                                    in a large formal library, and whether they can preserve the
that paraphrases in theorems significantly affect autoformal-
                                                                    intended mathematical content when the target formaliza-
izer output (Moore & Shah, 2025), yet it has not been shown
                                                                    tion is more directly reflected in the problem statement.
whether such perturbations reflect semantic disagreement or
shallower code-generation issues. Furthermore, since gener-
ated formalizations can differ syntactically from benchmark         Models. We evaluate four frontier models (o3, GPT-5.4,
references while expressing the same theorem, evaluation            o1, o4-mini) and three open-weight 7B autoformalizers
also requires equivalence metrics such as BEq+ bidirectional        (Kimina (Wang et al., 2025), Herald (Gao et al., 2025), and
proof search (Poiroux et al., 2025), FormalAlign contrastive        DeepSeek-Prover-V2 (Ren et al., 2025)). Serving details for
scoring (Lu et al., 2025), and GTED AST edit distance (Liu          the open-weight models are in Appendix B.2.
et al., 2025c).
                                                                    Evaluation metrics. We use BEq+ (Poiroux et al., 2025)
Our work relates to studies of surface robustness under             as the primary equivalence metric, which declares two for-
semantically equivalent input variation in informal math-           mal statements equivalent when bidirectional proof search
ematical reasoning (Huang et al., 2025; Hao et al., 2025)           succeeds in both directions. As an independent structural
and natural-language-to-code translation (Mastropaolo et al.,       cross-check, we use GTED (Liu et al., 2025c), which mea-
2023; Chen et al., 2024). However, autoformalization dif-           sures tree edit distance over Lean abstract syntax trees nor-
fers because correctness is compiler-verified, meaning that         malized to [0, 1] (where 1.0 indicates byte-identical struc-
inconsistencies may arise not only from semantic differ-            ture). We say a paraphrase pair is compile-both when both
ences but also from failures to produce syntactically valid         Lean outputs successfully elaborate, while compile rate
code. Closest to our setting, Moore & Shah (2025) shows             denotes the fraction of predictions that elaborate. Non-
that LLM-generated paraphrases of miniF2F and ProofNet              compiling predictions count as non-equivalent. We define
can change whether outputs compile, and Liu et al. (2025a)          surface consistency as the fraction of paraphrase pairs whose
documents identifier hallucination as a major failure mode          baseline and perturbed Lean outputs are BEq+-equivalent.
in undergraduate-level autoformalization. We build upon
this by using a controlled suite of deterministic paraphrases       Implementation. We patch BEq+ for models that emit
across seven models, helping us localize failures and demon-        their own Lean preamble (Appendix B.3) and report 95%
strate that sensitivity largely stems from compilation errors       bootstrap confidence intervals throughout. For each GPT
rather than differences in mathematical meaning.                    model, we issue 50 paired requests with identical inputs
                                                                    and observe byte-identical outputs in all cases, confirming
3. Methods                                                          deterministic behavior at the API layer. Open-weight mod-
                                                                    els are deterministic by construction, as we serve them at
Perturbations. We apply 60 named rules to theorem-                  temperature 0.
statement natural language prose across 11 categories (con-
cept rename, conditional, discourse, quantifier, verbosity,
and others). Math spans ($...$) are masked so LaTeX
formulas and identifiers are never altered. Every rule has an         1
                                                                        All code is available at https://anonymous.4open.
input pattern, context guards, and a textbook reference es-         science/r/F232/.

                                                                2
                                         Characterizing Paraphrase-Induced Failures in Lean 4 Autoformalization

                                                                                                           ProofNet#           miniF2F
                              (a)                                                             (b)
                        70%
                                                            ProofNet#   Concept rename              5.0%
                                  56%       55%             miniF2F
                        60%    50%
                                                                               Definitional                            25.0%
                                                                 45%
  Surface consistency




                        50%                           44%
                                                                               Conditional                             25.1%
                                         33%
                        40%
                                                                                Discourse                                  30.6%
                        30%                        20%
                                                              19%                Verbosity                                 30.8%

                        20%
                                                                                Quantifier                                      36.0%

                        10%
                                                                         Type / notation                                           40.2%

                        0%
                               GPT-5.4    o3         o1       o4-mini                     0%         10%    20%      30%    40%            50%
                                                                                                      BEq+ rate (4 models pooled)
Figure 1. (a) Per-model surface consistency under paraphrased inputs on ProofNet# (teal) and miniF2F (orange). Pair agreement ranges
from 19–56% across the GPT panel. Error bars are 95% bootstrap CIs. (b) Per-category BEq+ surface consistency, pooled across the
GPT panel, with ProofNet# categories (teal) and miniF2F categories (orange) shown together.


4. Results                                                                     tions. These formulations are mathematically equivalent,
                                                                               but BEq+’s bidirectional proof search fails to bridge them.
4.1. Surface Consistency                                                       Such cases illustrate that BEq+-based non-equivalence
Surface consistency is low across the panel. Across the                        should be read as a conservative floor, consistent with the
four frontier models, surface consistency ranges from 19.1–                    metric’s known incompleteness (Liu et al., 2025a; Poiroux
49.5% on ProofNet# and 44.5–55.5% on miniF2F (Fig-                             et al., 2025).
ure 1(a)), well below the 100% byte-identical agreement on
repeated identical inputs (§3). Additionally, compile rates                    4.2. Failure Modes Are Typed by Dataset
per direction are 11–24%, meaning most of the inconsis-
                                                                               Compile failures dominate, with dataset-specific error
tency arises from pairs where at least one Lean output fails
                                                                               types. On ProofNet#, 34–50% of compile failures across
to compile.
                                                                               the models are from unknown-identifier errors: specifically,
                                                                               the model emits a Mathlib API name that does not exist in
Compile-both pairs are largely equivalent. Among
                                                                               the pinned version, such as using SimpleGroup where
pairs where both outputs compile, BEq+-equivalence is
                                                                               the correct identifier is IsSimpleGroup. On miniF2F,
high across the panel. Cross-checking with GTED, we find
                                                                               22–48% of compile failures are syntax errors and 25–39%
a median of at least 0.943 across all four frontier models
                                                                               are elaboration failures (Appendix A.3). This is because
on ProofNet#, with the majority of pairs at GTED = 1.000.
                                                                               miniF2F theorems are formalized from scratch, so failures
This confirms that compile-both pairs are structurally near-
                                                                               often surface as malformed Lean code rather than wrong li-
identical, meaning the low surface consistency is not driven
                                                                               brary names. In both cases, perturbations push the model to-
by semantic disagreement among compiling outputs. We
                                                                               ward a made-up identifier or malformed construction, which
provide full GTED metrics across frontier models in Ap-
                                                                               Lean then rejects.
pendix A.7.
                                                                               The most harmful perturbation axis is dataset-specific.
BEq+ incompleteness affects a small subset. A small
                                                                               The most destabilizing category differs across datasets (Fig-
subset of BEq+ failures on our compile-both subset arises
                                                                               ure 1(b)). On ProofNet#, conditional restructuring (“if
from BEq+’s known incompleteness. For example, on
                                                                               . . . then” → “whenever”) causes the largest drop in surface
our discourse exists style perturbation, o4-mini
                                                                               consistency, with paired outputs equivalent in only 25.1% of
maps “there is an infinite number” to a Set.Infinite
                                                                               cases. On miniF2F, concept renaming is the most damaging
formulation and “there exists an infinite number” to an
                                                                               category, with around 5% of pairs equivalent. Per-category
explicit injective map from N into the quaternion solu-

                                                                           3
                            Characterizing Paraphrase-Induced Failures in Lean 4 Autoformalization

  o4-mini                   19%                           GPT-family           5. Discussion
                                                          Open-weight
  Herald                     20%                                               We study paraphrase sensitivity in Lean 4 autoformaliza-
      o1                     20%
                                                                               tion across seven models and find that paraphrase-induced
                                                                               failures are dominated by the code-generation layer rather
DeepSeek                          22%
                                                                               than by semantic disagreement about mathematical content.
      o3                                  33%                                  Overall, we find surface consistency to be low across the
  GPT-5.4                                               50%
                                                                               panel (19–56% across models), with failures typed differ-
                                                                               ently by dataset: on ProofNet#, models hallucinate Mathlib
  Kimina                                                       56%
                                                                               identifiers (34–50% of failures); on miniF2F, they produce
        0%    10%     20%     30%       40%       50%    60%         70%       malformed syntax or fail elaboration (47–70% combined).
                            Surface consistency
                                                                               Similar patterns appear on the open-weight panel. These
Figure 2. ProofNet# surface consistency on the 10 rules shared                 findings indicate that state-of-the-art autoformalizers still
across both panels (95% bootstrap confidence intervals over 5,000              struggle to consistently generate valid Lean code under real-
iterations).                                                                   istic input variation, and that their failure modes are dataset-
                                                                               specific in classifiable ways. Practically, this suggests that
                                                                               autoformalization evaluations should report not only final
breakdowns for miniF2F are in Appendix A.4, while a per-
                                                                               equivalence or accuracy, but also where failures occur in the
rule heatmap for the frontier panel is in Appendix A.2.
                                                                               formalization pipeline, since identifier hallucinations, syn-
We note that these differences reflect each dataset’s formal-                  tax errors, and elaboration failures point to different repair
ization path. ProofNet# formalizations depend on hypothe-                      strategies.
sis structure, which requires navigating Mathlib’s typeclass
hierarchy to select the correct API entry point. Therefore,                    5.1. Limitations
surface edits that restructure logical form change which API
path the model takes. In contrast, miniF2F formalizations                      Our equivalence claims depend on BEq+ as the primary
depend on vocabulary, because they map phrases like “sum                       checker. We note that BEq+ is sound but not complete by
of the first n integers” onto specific Lean identifiers. There-                construction (Liu et al., 2025a; Poiroux et al., 2025), and our
fore, surface edits that rename concepts directly disrupt this                 incompleteness example shows a case where bidirectional
lookup.                                                                        proof search fails on a mathematically valid equivalence.
                                                                               For this reason, non-equivalence on BEq+ should be read
Two concrete examples of surface-induced failures are pre-                     as a conservative floor rather than as definitive evidence of
sented in Appendix A.5. In each case, the baseline formal-                     semantic difference. Additionally, our perturbation suite
ization is BEq+-equivalent to the ground-truth reference,                      primarily consists of conventional English mathematical
while the perturbed one is not, despite the underlying math-                   paraphrases, while underrepresenting notational and multi-
ematical content remaining unchanged.                                          lingual edits. Finally, our open-weight panel is limited to
                                                                               three 7B autoformalizers, and whether larger or differently-
4.3. Open-Weight Models Exhibit the Same Patterns                              trained models show the same dissociation is left for future
                                                                               work.
We additionally test three open-weight 7B autoformalizers
(Kimina, Herald, DeepSeek-Prover-V2) on the ProofNet#
rules shared with the frontier panel and find consistency                      5.2. Future Work
rates of 19.8–55.6% (Figure 2), overlapping the frontier-                      Our failure-mode characterization makes targeted training-
panel range of 19.1–49.5%. This indicates that the failure                     time interventions feasible, since the dominant failure
modes characterized above are not limited to frontier models.                  modes are classifiable from compiler output. Unknown-
We note that Kimina and DeepSeek-Prover-V2 have training                       identifier errors on ProofNet# are naturally addressable by
data overlap with ProofNet (Wang et al., 2025; Ren et al.,                     retrieval-augmented identifier resolution, while syntax er-
2025), so their performance partly reflects training exposure                  rors on miniF2F can be targeted via fine-tuning on com-
rather than generalization to unseen theorems. Nevertheless,                   piler feedback. We expect interventions narrowly targeted
they still show substantial paraphrase sensitivity, indicat-                   at these specific failure modes to close the gap between
ing that failure is fundamentally caused by instability in                     paraphrase-sensitive surface consistency and paraphrase-
code-generation. We provide full per-rule breakdowns in                        invariant semantic capability more effectively than generic
Appendix A.6.                                                                  robustness measures. We view this as a natural next step.




                                                                           4
                            Characterizing Paraphrase-Induced Failures in Lean 4 Autoformalization

References                                                                autoformalization. In The Thirteenth International Con-
                                                                          ference on Learning Representations, 2025.
Azerbayev, Z., Piotrowski, B., Schoelkopf, H., Ayers, E. W.,
  Radev, D., and Avigad, J. Proofnet: Autoformalizing                   Mastropaolo, A., Pascarella, L., Guglielmi, E., Ciniselli,
  and formally proving undergraduate-level mathematics.                  M., Scalabrino, S., Oliveto, R., and Bavota, G. On the
  CoRR, abs/2302.12433, 2023.                                            robustness of code generation techniques: An empirical
                                                                         study on GitHub Copilot. In Proceedings of the 45th In-
Chen, J., Li, Z., Hu, X., and Xia, X. NLPerturbator: Study-
                                                                         ternational Conference on Software Engineering (ICSE),
  ing the robustness of code LLMs to natural language
                                                                         pp. 2149–2160, 2023.
  variations. arXiv preprint arXiv:2406.19783, 2024.
                                                                        Moore, H. and Shah, A. Evaluating autoformalization ro-
de Moura, L. and Ullrich, S. The Lean 4 theorem prover
                                                                         bustness via semantically similar paraphrasing. CoRR,
  and programming language. In Automated Deduction –
                                                                         abs/2511.12784, 2025.
  CADE 28: 28th International Conference on Automated
  Deduction, pp. 625–635. Springer, 2021.                               Poiroux, A., Weiss, G., Kunčak, V., and Bosselut, A. Re-
                                                                          liable evaluation and benchmarks for statement autofor-
Gao, G., Wang, Y., Jiang, J., Gao, Q., Qin, Z., Xu, T., and
                                                                          malization. In Proceedings of the 2025 Conference on
  Dong, B. Herald: A natural language annotated lean 4
                                                                          Empirical Methods in Natural Language Processing, pp.
  dataset. In The Thirteenth International Conference on
                                                                          17958–17980, 2025.
  Learning Representations, 2025.
                                                                        Ren, Z. Z., Shao, Z., Song, J., Xin, H., Wang, H., Zhao,
Hao, Y., Wan, X., and Zhai, C. An investigation of robust-                W., Zhang, L., Fu, Z., Zhu, Q., Yang, D., Wu, Z. F.,
  ness of LLMs in mathematical reasoning: Benchmark-                      Gou, Z., Ma, S., Tang, H., Liu, Y., Gao, W., Guo, D.,
  ing with mathematically-equivalent transformation of ad-                and Ruan, C. DeepSeek-Prover-V2: Advancing formal
  vanced mathematical problems. CoRR, abs/2508.08833,                     mathematical reasoning via reinforcement learning for
  2025.                                                                   subgoal decomposition. CoRR, abs/2504.21801, 2025.
Huang, K., Guo, J., Li, Z., Ji, X., Ge, J., Li, W., Guo, Y., Cai,       Wang, H., Unsal, M., Lin, X., Baksys, M., Liu, J., Dos San-
  T., Yuan, H., Wang, R., Wu, Y., Yin, M., Tang, S., Huang,              tos, M., Sung, F., Vinyes, M., Ying, Z., Zhu, Z., Lu, J.,
 Y., Jin, C., Chen, X., Zhang, C., and Wang, M. MATH-                    de Saxcé, H., et al. Kimina-Prover Preview: Towards
  Perturb: Benchmarking LLMs’ math reasoning abilities                   large formal reasoning models with reinforcement learn-
  against hard perturbations. CoRR, abs/2502.06453, 2025.                ing. arXiv preprint arXiv:2504.11354, 2025.
Liu, Q., Zheng, X., Lu, X., Cao, Q., and Yan, J. Rethinking             Wu, Y., Jiang, A. Q., Li, W., Rabe, M. N., Staats, C., Jam-
  and improving autoformalization: Towards a faithful met-               nik, M., and Szegedy, C. Autoformalization with large
  ric and a dependency retrieval-based approach. In The                  language models. In Advances in Neural Information
  Thirteenth International Conference on Learning Repre-                 Processing Systems, 2022.
  sentations, 2025a.
                                                                        Yang, K., Swope, A., Gu, A., Chalamala, R., Song, P., Yu,
Liu, X., Bao, K., Zhang, J., Liu, Y., Chen, Y., Liu, Y.,                  S., Godil, S., Prenger, R., and Anandkumar, A. Lean-
  Jiao, Y., and Luo, T. ATLAS: Autoformalizing theo-                      Dojo: Theorem proving with retrieval-augmented lan-
  rems through lifting, augmentation, and synthesis of data.              guage models. In Advances in Neural Information Pro-
  In Advances in Neural Information Processing Systems,                   cessing Systems, 2023.
  2025b.
                                                                        Zheng, K., Han, J. M., and Polu, S. minif2f: A cross-system
Liu, Y., Zhu, T., Liu, X., Chen, Y., Liu, Z., Guo, Q., Zhang,             benchmark for formal olympiad-level mathematics. In
  J., Bao, K., and Luo, T. Generalized tree edit distance                 International Conference on Learning Representations,
  (GTED): A faithful evaluation metric for statement auto-                2022.
  formalization. CoRR, abs/2507.07399, 2025c. Presented
  at AI4Math@ICML 2025.
Lu, J., Wan, Y., Liu, Z., Huang, Y., Xiong, J., Liu, C.,                A. Additional Results
  Shen, J., Jin, H., Zhang, J., Wang, H., Yang, Z., Tang, J.,           A.1. Compile Rates
  and Guo, Z. Process-driven autoformalization in lean 4.
  CoRR, abs/2406.01940, 2024.                                           Table 1 reports compile rates underlying the subset analyzed
                                                                        in §4.1. The Both column gives the number of pairs where
Lu, J., Wan, Y., Huang, Y., Xiong, J., Liu, Z., and Guo,                both baseline and perturbed predictions type-check. Base-
  Z. FormalAlign: Automated alignment evaluation for                    line and perturbed compile rates are similar within each

                                                                    5
                                       Characterizing Paraphrase-Induced Failures in Lean 4 Autoformalization

cell, meaning perturbations do not uniformly destroy com-                          Table 3. Per-category BEq+ surface consistency on miniF2F, with
                                                                                   95% bootstrap confidence intervals.
pilability. Instead, the inconsistency comes from the subset
of pairs where a surface change triggers a code generation                                 Category              Equiv Rate          N
failure.
                                                                                           Concept rename       5.0% [0.0, 15.0]     20
Table 1. Compile rates across all frontier models and datasets. PN#
                                                                                           Definitional        25.0% [8.3, 41.7]    24
= ProofNet#, MF2F = miniF2F.
                                                                                           Type / notation    40.2% [31.6, 48.7]    117
                                                                                           Organization       44.9% [34.7, 55.1]     98
      Dataset      Model           N        Base      Pert      Both
                                                                                           Conditional        45.7% [38.6, 52.7]    184
                   GPT-5.4         299      11.7%    11.4%    9.7% (29)                    Verbosity          50.0% [47.4, 52.7]   1,368
                   o3              237      18.1%    19.0%    14.3% (34)
      PN#
                   o1              249      13.3%    12.0%     8.4% (21)
                                                                                           Discourse          52.0% [48.8, 55.2]    904
                   o4-mini         324      12.3%    12.0%    6.8% (22)                    Equivalence        57.1% [28.6, 78.6]     14
                                                                                           Quantifier         58.6% [51.0, 66.2]    157
                   GPT-5.4         827      15.8%    16.1%   14.6% (121)
                   o3              582      23.7%    23.9%   20.6% (120)
      MF2F
                   o1              723      24.2%    24.1%   19.9% (144)           to the ground-truth reference, while the perturbed one is
                   o4-mini         658      21.7%    21.6%   16.9% (111)
                                                                                   not, despite the underlying mathematical content remaining
                                                                                   unchanged.
A.2. Per-Rule GPT-Panel Heatmap on ProofNet#
Figure 3 gives the BEq+ equivalence rates for the frontier                         A.6. Per-Rule Open-Weight Surface Consistency
model panel on ProofNet#. Empty cells indicate rules with                          Table 5 expands Figure 2 from the main paper to explore
zero paired predictions where both outputs compiled.                               surface consistency on the ProofNet# rules common to both
                                                                                   the GPT and open-weight evaluations. Kimina achieves a
A.3. Compile Failure Taxonomy                                                      surface consistency of 0% on certain rules, unlike any of the
We classify all non-equivalent predictions by Lean error                           other models. We leave exploring this to future work.
type. The error distribution differs significantly across
datasets (Table 2). On ProofNet#, unknown-identifier er-                           A.7. Panel-Wide GTED Results
rors account for 34–50% of failures across models, with                            Table 6 reports GTED on compile-both pairs across all fron-
the model emitting a Mathlib API name that does not ex-                            tier and open-weight models. Pooled across 401 pairs, the
ist in the pinned Mathlib version (e.g., SimpleGroup                               median GTED is 1.000 and the mean is 0.934. Furthermore,
instead of IsSimpleGroup). On miniF2F, syntax errors                               eight of the eleven cells have a per-cell median of exactly
are the largest or second-largest category for every model                         1.000, confirming that baseline and perturbed Lean outputs
(22–48%), followed by elaboration failures (25–39%). We                            are near-identical on the compile-both subset.
discuss the dataset-specific structure of these failure modes
in §4.2.
Table 2. Compile error taxonomy across all non-equivalent predic-
tions. The Other column aggregates type, import, and miscella-
neous errors.

   Dataset      Model         N          Unk. ID    Syntax   Elab.     Other
                GPT-5.4      151          34.4%     11.9%    23.2%     30.5%
                o3           159          50.3%     14.5%    14.5%     20.8%
   PN#
                o1           198          44.9%     19.2%    10.1%     25.8%
                o4-mini      262          46.2%     13.4%    12.6%     27.9%
                GPT-5.4      368          10.1%     48.4%    28.5%     13.0%
                o3           265          21.1%     21.9%    39.2%     17.7%
   MF2F
                o1           401          20.2%     34.2%    24.7%     20.9%
                o4-mini      416          18.5%     31.0%    28.4%     22.1%


A.4. Per-Category Surface Consistency on miniF2F
Figure 1(b) in §4.2 reports per-category surface consistency
on ProofNet#, while Table 3 gives the corresponding break-
down on miniF2F.

A.5. Example Surface-Induced Failures
Table 4 shows two concrete surface-induced failures. In
each case, the baseline formalization is BEq+-equivalent

                                                                               6
                                         Characterizing Paraphrase-Induced Failures in Lean 4 Autoformalization

                                                                                                                                                                                                        100

GPT-5.4         39           33          50             46         43           53           47            100            47         48               40           67           60            69
                                                                                                                                                                                                        80




                                                                                                                                                                                                              BEq+ equivalence (%)
    o3          –            33          21             25         23           32           37            –              41          –               45           35           40            31        60


    o1          17           –           –              –          23           17           17             0             20         26               20           30           17            –         40


                                                                                                                                                                                                        20
o4-mini         6            0           7              11         17           10           20             0             33         35               17           41           17            19

                                                                                                                                                                                                        0
                  r




                                                                   e



                                                                              ow
                            e




                                                       le
                                        e




                                                                                             e



                                                                                                           e



                                                                                                                      op




                                                                                                                                     le



                                                                                                                                                     ies




                                                                                                                                                                    g




                                                                                                                                                                                           ds
                                                                                                                                                                                e
               ve




                                                                  ov
                            ut



                                       um




                                                                                          ot



                                                                                                         or




                                                                                                                                                                  in



                                                                                                                                                                                bl
                                                      sty




                                                                                                                                    ty




                                                                                                                                                                                         or
                                                                                                                    dr




                                                                                                                                                  pl
                                                                              sh
            ne




                                                                                                                                                               as



                                                                                                                                                                              am
                           m




                                                                                        en



                                                                                                       ef
                                                                 pr




                                                                                                                                ss




                                                                                                                                                                                          w
                                    ss




                                                                                                                                                im
                                                  at




                                                                                                   er
                       m




                                                                                                                   ow




                                                                                                                                                              hr
         e




                                                                                       td
                                                                            o




                                                                                                                               ist
                                                              to




                                                                                                                                                                          re
                                  ea




                                                                                                                                                                                       al
      wh




                                              th




                                                                                                  th
                                                                          et
                      co




                                                                                                                                                              lp
                                                                                                                                            al
                                                                                                                 sh




                                                                                                                                                                         kp
                                                                                      le




                                                                                                                               ex




                                                                                                                                                                                      er
                                                             ow
                                  os




                                                                                                                                          on
                                                                        ov
                                              ch




                                                                                                  en




                                                                                                                                                           rsa
     o



                     sis




                                                                                                                                                                                   m
                                                                                                                                                                    oo
   if t




                              pp




                                                            sh



                                                                       pr
                                             su




                                                                                              th




                                                                                                                                          iti




                                                                                                                                                                                 nu
                                                                                                                                                       ive
                   e




                                                                                                                                                                   xtb
                th




                                                                                                                                      nd
                            su




                                                                                                                                                     un
              po




                                                                                                                                    co




                                                                                                                                                                   te
            hy




                             Conditional                                                      Discourse                                                Quantifier                Verbosity

Figure 3. Per-(rule, model) BEq+ equivalence on ProofNet# (GPT panel). Rows sorted by panel-mean ascending. Dots denote cells with
no paired predictions.

Table 4. Two meaning-preserving paraphrases that flip a baseline-correct formalization to an incorrect or non-compiling Lean output.
Each row shows the natural language edit and the resulting change in Lean output.

Rule / Model                             NL input                                                                               Lean output

quant                                    Original: Prove that if |G| = 132 then G is not                                        Baseline: (h : Fintype.card G = 132)
conditional                              simple.                                                                                : ¬ IsSimpleGroup G
implies                                  Perturbed: Prove that |G| = 132 implies G is not                                       Perturbed: (h : Fintype.card G = 132)
(o1)                                     simple.                                                                                : ¬ SimpleGroup G
                                                                                                                                SimpleGroup is not a Mathlib identifier.

discourse prove                          Original: Prove that for all n>1, Z/nZ is not a                                        Baseline:   (h : 1 < n) : ¬ Nonempty
to show                                  group under multiplication of residue classes.                                         (Group (ZMod n))
(o3)                                     Perturbed: We show that for all n>1, Z/nZ is not                                       Perturbed: (h : 1 < n) : ∃ a : ZMod
                                         a group under multiplication of residue classes.                                       n, ∀ b, a * b ̸= 1
                                                                                                                                Perturbed claim is strictly weaker: one element lacks a right-inverse
                                                                                                                                vs. no group structure exists.




Table 5. Per-rule BEq+ surface consistency on the 10 ProofNet#                                             Table 6. Panel-wide GTED on compile-both pairs. Median TED
rules common to the GPT and open-weight evaluations.                                                       = 0 in 8/11 cells, confirming structural identity is typical on
                                                                                                           compile-both pairs across the frontier and open-weight panels.
    Cat.      Rule                                N     Herald     Kimina       DeepSeek
                                                                                                                 Model         Dataset          N     Median            p25     p75     Mean       count@1.0
              if to whenever                      18     16.7%         0.0%          27.8%
    cond      such that style                     28     25.0%         0.0%           0.0%                       GPT-5.4       PN#              40         1.000    1.000      1.000    0.961        31/40
              suppose assume                      28     14.3%         0.0%           0.0%                       o3            PN#              40         1.000    0.885      1.000    0.901        22/40
                                                                                                                 o1            PN#              40         0.943    0.842      1.000    0.914        14/40
              exists style                     23        26.1%        91.3%          21.7%                       o4-mini       PN#              40         1.000    0.846      1.000    0.898        25/40
              let denote                        36       13.9%        61.1%          19.4%                       Kimina        PN#              30         1.000    1.000      1.000    0.970        27/30
    disc.     prove to show                    121       20.7%        65.3%          24.8%                       DeepSeek      PN#              30         1.000    1.000      1.000    0.978        24/30
              show drop                         78       23.1%        55.1%          26.9%                       Herald        PN#              21         1.000    1.000      1.000    1.000        21/21
              show to prove                     53       24.5%        67.9%          28.3%                       GPT-5.4       MF2F             40         1.000    0.969      1.000    0.954        29/40
                                                                                                                 o3            MF2F             40         1.000    0.936      1.000    0.932        26/40
              numeral words                     16       31.2%        62.5%          25.0%
    verb.                                                                                                        o1            MF2F             40         0.977    0.855      1.000    0.891        19/40
              textbook preamble                104       13.5%        67.3%          25.0%
                                                                                                                 o4-mini       MF2F             40         1.000    0.958      1.000    0.927        28/40
    Pooled                                     505       19.8%        55.6%          22.4%
                                                                                                                 Pooled        —            401            1.000    0.929      1.000    0.934       266/401




                                                                                                       7
                          Characterizing Paraphrase-Induced Failures in Lean 4 Autoformalization

B. Methodology Details                                               Table 7. Three representative entries from the construction-
                                                                     correctness spec. References: cond if to whenever is a stan-
B.1. Construction                                                    dard logical rewrite; discourse prove to show is a proof-
                                                                     prose convention; concept rename synonym follows Dum-
Each perturbation rule specifies an input pattern, transforma-       mit & Foote, Abstract Algebra, §1.2.
tion, context guards, and a reference establishing meaning
                                                                     Rule / Pattern                Output               Guard
preservation. Rules do not modify content inside math spans
                                                                     cond if to whenever:           “whenever P , Q”    P , Q contain no nested
($...$). We mask spans before matching and restore them              “if P then Q” (sentence start)                     conditionals
after substitution, ensuring LaTeX formulas and variable             discourse prove to           “We show that” (or in- Theorem-statement bound-
names remain unchanged. Rules that fail their guard condi-           show: “Prove that” (sentence verse)                 ary; ignores embedded
                                                                     start)                                              quotes
tions are skipped. Table 7 shows three representative rules
(conditional, discourse, concept rename).                            concept rename           “commutative group”       Outside math spans; not
                                                                     synonym: “abelian group”                           AbelianGroup
                                                                     (token, outside math)
B.2. Open-Weight Inference Setup
                                                                     tokens 2048. We extract only the theorem ...                            :=
We use each model’s recommended prompt format. Kimina-               sorry block from each output.
Autoformalizer-7B uses its chat template with the sys-
tem prompt “You are an expert in mathematics and Lean
                                                                     B.3. BEq+ Wrapper Patch
4” and a user prompt requesting Lean 4 autoformaliza-
tion. DeepSeek-Prover-V2 uses single-turn completion                 BEq+ prepends a preamble (import Mathlib plus a
on the statement. Herald also uses single-turn completion            fixed namespace) to each prediction before compilation.
and emits its own import Mathlib preamble (see Ap-                   Herald-generated outputs already include their own pream-
pendix B.3). All three are run at temperature 0 with max             ble, and when concatenated, duplicate imports cause the
                                                                     Lean compiler to reject the file. For this reason, we strip
                                                                     the wrapper preamble before compilation; without this step,
                                                                     every Herald pair returns method=failed.




                                                                 8
