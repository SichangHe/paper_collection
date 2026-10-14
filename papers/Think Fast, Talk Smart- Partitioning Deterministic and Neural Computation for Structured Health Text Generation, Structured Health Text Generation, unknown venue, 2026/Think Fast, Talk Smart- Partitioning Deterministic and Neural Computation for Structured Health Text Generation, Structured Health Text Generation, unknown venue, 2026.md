                                         Think Fast, Talk Smart: Partitioning Deterministic and Neural Computation for
                                                              Structured Health Text Generation


                                                                              Kai-Chen Cheng 1 Haejun Han 1 David Q. Sun 1


                                                                   Abstract                                 applications are promising precisely because language mod-
                                                                                                            els can make technical records understandable. They are
                                                Large language models (LLMs) are increasingly
                                                                                                            also risky because fluent health text must remain faithful
arXiv:2605.29652v1 [cs.AI] 28 May 2026




                                                being used to generate health text from structured
                                                                                                            to the source record, consistent with task instructions, and
                                                records such as wearable time series, biomark-
                                                                                                            explicit about what evidence supports each claim (Ji et al.,
                                                ers, vitals, and care-management logs. For recur-
                                                                                                            2023; Van Veen et al., 2024). Recent wearable and personal-
                                                ring health outputs, fluency is not enough: sys-
                                                                                                            health systems show the promise of LLMs in this space
                                                tems must remain faithful to source data, ground
                                                                                                            (Kim et al., 2024; Khasentino et al., 2025; Merrill et al.,
                                                explanatory claims in available evidence, follow
                                                                                                            2026); they also sharpen a practical question: which parts
                                                stated policies, emit machine-readable outputs,
                                                                                                            of a recurring health-generation task should be learned gen-
                                                and run cheaply enough for repeated use. We
                                                                                                            eration, and which should be verified computation?
                                                ask which responsibilities in structured health
                                                generation should be deterministic computation              Prompting research offers several ways to improve model
                                                rather than runtime LLM prompting. We intro-                reasoning. Chain-of-thought elicits intermediate reasoning
                                                duce Think Fast, Talk Smart (TFTS), a sleep-                steps (Wei et al., 2022); iterative refinement trades more
                                                health insight pipeline in which deterministic code         calls for improved outputs (Madaan et al., 2023); program-
                                                performs recurring analysis before one bounded              aided methods externalize computation (Chen et al., 2023;
                                                LLM writer call. Across 280 user-nights and                 Gao et al., 2023); retrieval and tool-use systems augment
                                                six models, TFTS achieves lower numeric er-                 LLMs at runtime (Lewis et al., 2020; Yao et al., 2023);
                                                ror, lower instruction-compliance error, and lower          and prompt-programming frameworks such as DSPy opti-
                                                end-to-end cost than structured zero-shot and few-          mize LLM pipelines (Khattab et al., 2024). These methods
                                                shot one-call baselines. Layer replacement re-              improve what happens inside or around an LLM call. Our
                                                veals contract-specific failures: LLM comparison            work asks a different systems question: when should a recur-
                                                raises numeric error, LLM ranking degrades pol-             ring health task be implemented outside the LLM call? For
                                                icy selection, LLM attribution increases unsup-             structured health workloads, some decisions recur with little
                                                ported causal language, and an LLM-generated                change across inputs, such as comparing a measurement to
                                                writer interface reintroduces errors even after up-         a baseline, choosing what to surface, and deciding which
                                                stream facts are deterministic. The results support         explanatory claims are supported by logged evidence. When
                                                a broader design rule: let code own recurring anal-         such steps are stable and verifiable, runtime prompting may
                                                ysis, and let LLMs express verified facts within            be the wrong abstraction for the analytical work.
                                                bounded interfaces.
                                                                                                            We study this partitioning problem through Think Fast, Talk
                                                                                                            Smart (TFTS), a sleep-health insight pipeline. Sleep-health
                                                                                                            is a useful case study because wearable records are longitudi-
                                         1. Introduction
                                                                                                            nal and heterogeneous, while the final output must be brief,
                                         Many health and medical applications ask LLMs to turn              grounded, and usable by non-expert readers. TFTS im-
                                         structured records into user-facing text: wearable coach-          plements stable analytical steps as deterministic layers and
                                         ing summaries, lab results interpretations, medication guid-       uses an LLM only as a bounded final writer over a compact
                                         ance, vitals monitoring, and care-management reports               evidence interface. We compare this design against one-call
                                         (Thirunavukarasu et al., 2023; Singhal et al., 2023). These        baselines, then replace one analytical layer at a time with
                                            1
                                                                                                            an LLM-generated typed artifact. This layer-replacement
                                            AI/ML@Eight Sleep. Correspondence to: Kai-Chen Cheng            protocol tests whether a model preserves the intended mean-
                                         <kevin.cheng@eightsleep.com>.
                                                                                                            ing of an intermediate analytical artifact beyond producing
                                         Accepted at the ICML 2026 Workshop on Structured Data for          syntactically valid JSON.
                                         Health (SD4H).

                                                                                                        1
                                      Partitioning Deterministic and Neural Health Generation




Figure 1. The TFTS partitioning framework. Recurring structured health-generation tasks are split into structured inputs, deterministic
analytical modules, a bounded LLM writer, and deterministic evaluation of the structured output. The sleep-health callouts instantiate this
partition in the evaluated pipeline.


Our contributions are threefold: we show that determinis-               pression: deterministic code handles recurring, verifiable
tic analytical layers plus a bounded writer achieve lower               reasoning, while the LLM focuses on phrasing verified facts
error and lower cost than strong prompting baselines on                 for the user. The experiment asks which recurring respon-
recurring health-insight generation tasks; introduce a layer-           sibilities can safely be moved from deterministic code into
replacement protocol that isolates individual analytical re-            LLM-generated intermediates.
sponsibilities with typed LLM-generated intermediates; and
identify the writer interface as a non-obvious failure point.           3. Baselines and Layer Replacement
Although our experiments use sleep-health data, the parti-
tioning principle targets broader structured health settings            One-call prompting baselines. We compare TFTS to
where inputs are machine-readable, analytical rules recur,              two single-call alternatives. S TRUCTURED Z ERO -S HOT
and intermediates can be checked.                                       receives raw data, the output schema, and the same sleep
                                                                        insight generation rules in prompt form; it must analyze,
2. Task and Pipeline                                                    select, attribute, and write in one call without demonstra-
                                                                        tions. S TRUCTURED F EW-S HOT strengthens this baseline
Figure 1 shows the four-stage partitioning pattern and the              with structured metric tables, few-shot examples, explicit
sleep-health instance we evaluate. For each user-night, the             selection rules, and numeric-grounding instructions.
system ingests wearable-derived sleep, recovery, physiol-
ogy, and behavior signals and returns a schema-constrained              Layer-replacement protocol. For mechanistic analysis,
insight with a title, core insight, improvement suggestion, se-         we replace exactly one analytical layer with an LLM-
lected metric metadata, attribution tags, and chart data. The           generated typed artifact. All upstream reference layers
deterministic reference pipeline follows a classic data-to-             remain deterministic; the generated artifact replaces the
text decomposition (Reiter, 2007; Wiseman et al., 2017): it             target layer’s reference output. This protocol is stricter and
formats data, computes numerical comparisons, ranks which               fairer than removing a layer from the final writer prompt:
metric should be surfaced, gates attribution by evidence, and           the model is asked to perform one bounded intermediate
compacts the selected facts into a deterministic prompt in-             task, not to recover missing context while writing the fi-
terface. The final LLM call then produces user-facing prose             nal JSON. The main conditions replaced C OMPARISON,
under a bounded schema, after which deterministic assem-                R ANKER, ATTRIBUTION, and H ANDOFF layers.
bly normalizes and wraps the response.
TFTS decouples analytical reasoning from linguistic ex-                 Data and models. The experiment uses 280 user-nights
                                                                        from 20 active users. We evaluate six models: GPT-5 nano,

                                                                    2
                                                         Partitioning Deterministic and Neural Health Generation

                                              (a) Cost vs. NumErr                                                                              (b) Cost vs. ICE




                                                                                           Instruction-Compliance Error (%)
                                                                                                                              100
                              50
     Numeric Error Rate (%)



                              40                                                                                               80

                              30                                                                                               60

                              20                                                                                               40

                              10                                                                                               20

                               0                                                                                                0
                              0.0003   0.001    0.003      0.01     0.03 0.06                                                  0.0003   0.001    0.003      0.01     0.03 0.06
                                         Cost/night (USD, log scale)                                                                      Cost/night (USD, log scale)

                                        TFTS                     Structured Few-Shot                        GPT-5 nano                    GPT-OSS-20B      Sonnet 4.6
                                        Structured Zero-Shot     GPT-4o mini                                GPT-OSS-120B                  Haiku 4.5



Figure 2. Baseline cost/error frontier across six models (n = 280 per cell). Both panels use end-to-end C OST / NIGHT on a log scale.
I NSTRUCTION -C OMPLIANCE E RROR is the union of S EL E RR and ATTR E RR. TFTS remains lower on both error axes than the structured
zero-shot and few-shot one-call baselines across the evaluated cost range.


GPT-4o mini, GPT-OSS-20B, GPT-OSS-120B, Haiku 4.5,                                                            not be read as a negative result for prompting: prompting
and Sonnet 4.6. Replacement conditions use two LLM calls                                                      helps formatting and some safety language, but it does not
per night, one artifact call and one final writer call; TFTS                                                  reliably reproduce the recurring analytical decisions that
and prompting baselines use one call. We therefore report                                                     drive the insight.
end-to-end cost and latency per insight.
                                                                                                              Layer replacements isolate failure modes. Table 1 com-
4. Evaluation                                                                                                 plements the frontier by locating which analytical respon-
                                                                                                              sibility fails when delegated to an LLM. R EPLACE C OM -
All metrics are computed deterministically from saved                                                         PARISON delegates numerical observations and baseline
per-night JSON traces. S CHEMA E RR is the final JSON                                                         comparisons to an LLM artifact; the aggregate N UM E RR
parse/schema error rate. N UM E RR is the fraction of ex-                                                     rises to 16.9%. R EPLACE R ANKER keeps numeric facts
tracted numeric claims that are unsupported by, or inconsis-                                                  grounded but degrades adherence to selection rules, with
tent with, the source fact bank. Outputs with zero extracted                                                  an aggregate S EL E RR of 65.8%. R EPLACE ATTRIBUTION
numeric claims are excluded from N UM E RR, so denomi-                                                        preserves selection and numeric grounding but increases
nators vary across conditions. S EL E RR is the fraction of                                                   attribution errors, with aggregate ATTR E RR of 24.5%. The
outputs whose selected metric contradicts the selection rule                                                  pattern is more informative than a single end-to-end score:
given to both the deterministic ranker and the LLM prompt.                                                    arithmetic, ranking policy, and evidence-gated attribution
ATTR E RR is the fraction of outputs that make an attribution                                                 fail in different ways, and each is easier to verify as deter-
not supported by the evidence-gated input.                                                                    ministic code than as prompted generation.

5. Results                                                                                                    The writer interface matters. R EPLACE H ANDOFF tests
                                                                                                              a more subtle boundary. Upstream computation, ranking,
Error–cost frontier. Figure 2 shows the main comparison.                                                      and attribution remain deterministic, yet replacing the com-
Across all six models, TFTS occupies the low-cost, low-                                                       pact evidence-to-writer handoff raises aggregate N UM E RR
error region: average N UM E RR is 0.7%, the worst model                                                      to 4.8% and ATTR E RR to 10.7%. This suggests that the
remains at 2.0%, and instruction-compliance error stays be-                                                   interface between verified facts and prose is part of the relia-
low 3%. The one-call baselines do not recover this frontier.                                                  bility mechanism, not just prompt formatting. A final writer
S TRUCTURED Z ERO -S HOT often selects the wrong met-                                                         can be useful, but the evidence packet that constrains what
ric and makes unsupported numeric claims; S TRUCTURED                                                         it may say should remain deterministic.
F EW-S HOT improves schema and attribution behavior, but
aggregate S EL E RR remains 68.6% (see Table 1) and nu-                                                       Representative examples clarify the metrics. Figure 3
meric errors remain high for several models. This should                                                      shows representative examples for the four main error fami-

                                                                                       3
                                     Partitioning Deterministic and Neural Health Generation




Figure 3. Annotated examples of error types. Red highlights mark the LLM output span that violates the target rule; green callouts show
the deterministic reference used by the evaluator. S CHEMA E RR captures parse/schema failures, N UM E RR captures numeric hallucinations,
S EL E RR captures selection-policy mismatch, and ATTR E RR captures unsupported attribution.


lies. The examples are not used as evidence by themselves;              domains with structured inputs, stable analytical rules, re-
they make the deterministic metrics in Table 1 interpretable.           peated deployment, and verifiable intermediates. Lab re-
They also show why schema-valid output is not enough: a                 sult explanations, vitals monitoring summaries, medication-
response can parse correctly while still using an unsupported           adherence coaching, and chronic-disease reports often share
number, selecting the wrong metric, or adding attribution               this shape. We have not validated those domains here, and
with no evidence above threshold.                                       tasks requiring open-ended clinical reasoning, diagnosis, or
                                                                        treatment planning may need a different partition.
6. Discussion and Limitations                                           This study evaluates preservation of a deterministic refer-
                                                                        ence system, not clinical optimality. S EL E RR is disagree-
For recurring structured health outputs, deterministic code
                                                                        ment with an application selection rule rather than ground-
should own stable, verifiable responsibilities: arithmetic
                                                                        truth health importance, and ATTR E RR is attribution-policy
over records, selection policy, evidence-gated attribution,
                                                                        compliance rather than biological causality. Human evalua-
and the writer interface that controls which facts may enter
                                                                        tion of helpfulness and perceived personalization is comple-
prose. LLMs remain useful where their strengths match
                                                                        mentary future work.
the task: converting verified facts into natural, empathetic,
schema-constrained language. This framing complements
RAG, tool use, and LLM-pipeline optimization (Lewis et al.,             7. Conclusion
2020; Schick et al., 2023; Yao et al., 2023; Mialon et al.,
                                                                        Structured health generation requires both reliable analyti-
2023): those methods can improve learned calls or retrieve
                                                                        cal computation and natural user-facing expression. In our
better context, while our question is which repeated health-
                                                                        sleep-health case study, one-call prompting cannot match a
generation responsibilities should be removed from run-
                                                                        deterministic analytical pipeline plus bounded writer, even
time prompting entirely. Another promising direction is
                                                                        with few-shot examples. Layer replacement shows why:
build-time agentic AI, where LLM agents help humans con-
                                                                        numerical comparison, ranking policy, attribution gates, and
struct and audit deterministic health-insight pipelines be-
                                                                        writer handoff each encode responsibilities that schema-
fore deployment, closer to pipeline-compilation systems
                                                                        valid LLM artifacts often fail to preserve. TFTS supports a
and wearable-health agent case studies than to the runtime
                                                                        practical design rule for structured health systems with re-
prompting baselines evaluated here (Khattab et al., 2024;
                                                                        curring analytical work: let code think fast over stable facts
Merrill et al., 2026).
                                                                        and policies, then let the LLM talk smart within verified
The partitioning principle should transfer most directly to             bounds.

                                                                    4
                                    Partitioning Deterministic and Neural Health Generation

References                                                             Reiter, E. An architecture for data-to-text systems. In Pro-
                                                                         ceedings of the Eleventh European Workshop on Natural
Chen, W., Ma, X., Wang, X., and Cohen, W. W. Program
                                                                         Language Generation, pp. 97–104. Association for Com-
  of thoughts prompting: Disentangling computation from
                                                                         putational Linguistics, 2007.
  reasoning for numerical reasoning tasks. Transactions on
  Machine Learning Research, 2023.                                     Schick, T., Dwivedi-Yu, J., Dessı̀, R., Raileanu, R., Lomeli,
Gao, L., Madaan, A., Zhou, S., Alon, U., Liu, P., Yang, Y.,              M., Hambro, E., Zettlemoyer, L., Cancedda, N., and
  Callan, J., and Neubig, G. PAL: Program-aided language                 Scialom, T. Toolformer: Language models can teach
  models. International Conference on Machine Learning,                  themselves to use tools. Advances in Neural Information
  pp. 10764–10799, 2023.                                                 Processing Systems, 36, 2023.

Ji, Z., Lee, N., Frieske, R., Yu, T., Su, D., Xu, Y., Ishii, E.,       Singhal, K., Tu, T., Gottweis, J., Sayres, R., Wulczyn, E.,
   Bang, Y., Madotto, A., and Fung, P. Survey of halluci-                Hou, L., Clark, K., Pfohl, S., Cole-Lewis, H., Neal, D.,
   nation in natural language generation. ACM Computing                  et al. Towards expert-level medical question answering
   Surveys, 55(12):1–38, 2023. doi: 10.1145/3571730.                     with large language models. Nature Medicine, 29:2899–
                                                                         2910, 2023. doi: 10.1038/s41591-023-02528-7.
Khasentino, J., Belyaeva, A., Liu, X., Yang, Z., Furlotte,
  N. A., et al. A personal health large language model                 Thirunavukarasu, A. J., Ting, D. S. J., Elangovan, K., Gutier-
  for sleep and fitness coaching. Nature Medicine, 31(10):               rez, L., Tan, T. F., and Ting, D. S. W. Large language
  3394–3403, 2025. doi: 10.1038/s41591-025-03888-0.                      models in medicine. Nature medicine, 29(8):1930–1940,
                                                                         2023.
Khattab, O., Singhvi, A., Maheshwari, P., Zhang, Z., San-
  thanam, K., et al. DSPy: Compiling declarative language              Van Veen, D., Van Uden, C., Blankemeier, L., Delbrouck,
  model calls into self-improving pipelines. In Interna-                 J.-B., Aali, A., et al. Adapted large language models can
  tional Conference on Learning Representations, 2024.                   outperform medical experts in clinical text summarization.
                                                                         Nature Medicine, 30:1134–1142, 2024. doi: 10.1038/
Kim, Y., Xu, X., McDuff, D., Breazeal, C., and Park,
                                                                         s41591-024-02855-5.
  H. W.     Health-LLM: Large language models for
  health prediction via wearable sensor data. In Pro-                  Wei, J., Wang, X., Schuurmans, D., Bosma, M., Xia, F.,
  ceedings of the Fifth Conference on Health, Infer-                    Chi, E. H., Le, Q. V., and Zhou, D. Chain-of-thought
  ence, and Learning, volume 248 of Proceedings of                      prompting elicits reasoning in large language models.
  Machine Learning Research, pp. 522–539. PMLR,                         Advances in Neural Information Processing Systems, 35:
  2024. URL https://proceedings.mlr.press/                              24824–24837, 2022.
  v248/kim24b.html.
                                                                       Wiseman, S., Shieber, S. M., and Rush, A. M. Challenges in
Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V.,           data-to-document generation. In Proceedings of the 2017
  Goyal, N., Küttler, H., Lewis, M., Yih, W.-t., Rocktäschel,         Conference on Empirical Methods in Natural Language
  T., et al. Retrieval-augmented generation for knowledge-              Processing, pp. 2253–2263. Association for Computa-
  intensive NLP tasks. In Advances in Neural Information                tional Linguistics, 2017.
  Processing Systems, volume 33, pp. 9459–9474, 2020.
                                                                       Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan,
Madaan, A., Tandon, N., Gupta, P., Hallinan, S., Gao,                    K., and Cao, Y. ReAct: Synergizing reasoning and act-
 L., Wiegreffe, S., Alon, U., Dziri, N., Prabhumoye, S.,                 ing in language models. In International Conference on
 Yang, Y., et al. Self-refine: Iterative refinement with self-           Learning Representations, 2023.
 feedback. Advances in Neural Information Processing
 Systems, 36, 2023.
Merrill, M. A., Paruchuri, A., Rezaei, N., Kovacs, G.,
 Perez, J., et al. Transforming wearable data into per-
 sonal health insights using large language model agents.
 Nature Communications, 17:1143, 2026. doi: 10.1038/
 s41467-025-67922-y.
Mialon, G., Dessı̀, R., Lomeli, M., Nalmpantis, C., Pa-
 sunuru, R., Raileanu, R., Rozière, B., Schick, T., Dwivedi-
 Yu, J., Celikyilmaz, A., et al. Augmented language mod-
 els: a survey. Transactions on Machine Learning Re-
 search, 2023.

                                                                   5
                                           Partitioning Deterministic and Neural Health Generation

Appendix
A. Full Results
Table 1. Full condition-by-model results. Values are percentages except n, C OST / NIGHT, and latency. S CHEMA E RR is the final
parse/schema failure rate; S EL E RR is disagreement with the selection rule; ATTR E RR is unsupported attribution. Replacement conditions
include both the artifact call and final writer call in C OST / NIGHT.

                               Condition              Model             n SchemaErr NumErr SelErr AttrErr Cost/night    Lat.

                                                      GPT-5 nano       280        0.0    0.4    0.0    2.5   $0.0005 4.4s
                                                      GPT-4o mini      280        0.0    0.4    0.0    0.0   $0.0007 8.1s
                                                      GPT-OSS-20B      280        0.0    0.4    0.0    0.0   $0.0009 2.6s
                               TFTS
                                                      GPT-OSS-120B     280        0.0    2.0    0.0    0.4   $0.0023 4.5s
                                                      Haiku 4.5        280        0.0    0.3    0.0    0.0   $0.0063 8.6s
                                                      Sonnet 4.6       280        0.0    0.4    0.0    0.0   $0.0218 15.1s

                                                      GPT-5 nano       280        0.0   54.2   95.0   18.6   $0.0010 4.4s
                                                      GPT-4o mini      280        0.0   20.7   93.2   42.2   $0.0014 8.6s
                                                      GPT-OSS-20B      280        0.4   15.5   71.8    2.5   $0.0020 4.8s
                               Structured Zero-Shot
                                                      GPT-OSS-120B     280        0.0   21.5   61.1    2.5   $0.0053 7.5s
                                                      Haiku 4.5        280       20.7   11.0   77.5    0.4   $0.0157 12.0s
                                                      Sonnet 4.6       280       32.5   24.2   82.5    1.1   $0.0538 16.8s

                                                      GPT-5 nano       280        0.0    3.4   71.1    3.6   $0.0004    3.8s
                                                      GPT-4o mini      280        0.0   21.9   70.4    4.6   $0.0005    8.7s
                                                      GPT-OSS-20B      280        0.0   38.9   68.9    2.1   $0.0008    2.4s
                               Structured Few-Shot
                                                      GPT-OSS-120B     280        0.0   37.0   71.1    0.4   $0.0020    3.9s
                                                      Haiku 4.5        280        0.0   26.5   67.1    0.7   $0.0055    6.3s
                                                      Sonnet 4.6       280        0.0   14.9   63.2    0.7   $0.0189    9.9s

                                                        GPT-5 nano     280        0.0    0.6    8.9   11.8   $0.0009    8.2s
                                                        GPT-4o mini    280        0.0    0.4    4.6   11.4   $0.0012   14.5s
                                                        GPT-OSS-20B    280        0.4    1.8    1.4   10.0   $0.0024    7.5s
                               Replace Reference Report
                                                        GPT-OSS-120B   280        0.0    3.4    0.7   10.7   $0.0060   12.9s
                                                        Haiku 4.5      280        0.7    3.0    2.1    8.9   $0.0115   15.4s
                                                        Sonnet 4.6     280        0.0    1.6    3.2   10.0   $0.0381   24.0s

                                                      GPT-5 nano       280        0.0   21.1   76.8    1.8   $0.0014   14.8s
                                                      GPT-4o mini      280        0.0   20.9   68.2    5.7   $0.0021   31.0s
                                                      GPT-OSS-20B      280        1.4    6.6   25.4    8.6   $0.0031    9.3s
                               Replace Comparison
                                                      GPT-OSS-120B     280        0.0    8.8   15.0   10.0   $0.0077   16.3s
                                                      Haiku 4.5        280        0.0   26.7   34.6    8.6   $0.0225   23.7s
                                                      Sonnet 4.6       280        0.0   17.6   27.5    9.3   $0.0632   34.6s

                                                      GPT-5 nano       280        0.7    0.3   63.9    8.9   $0.0014    6.9s
                                                      GPT-4o mini      280        0.0    0.0   71.8    9.6   $0.0022   13.5s
                                                      GPT-OSS-20B      280        0.4    0.5   62.5    6.8   $0.0025    6.0s
                               Replace Ranker
                                                      GPT-OSS-120B     280        0.0    3.1   67.1   10.7   $0.0070   10.2s
                                                      Haiku 4.5        280        5.3    2.2   62.9    7.5   $0.0160   11.9s
                                                      Sonnet 4.6       280       17.8    1.0   66.4    8.6   $0.0499   17.6s

                                                      GPT-5 nano       280        0.0    0.3    9.6   10.3   $0.0015 9.0s
                                                      GPT-4o mini      280        0.0    0.4    2.9   21.1   $0.0020 12.7s
                                                      GPT-OSS-20B      280        0.0    0.8    0.0   17.1   $0.0023 5.5s
                               Replace Attribution
                                                      GPT-OSS-120B     280        0.7    5.0    0.7   22.1   $0.0058 8.0s
                                                      Haiku 4.5        280        0.4    1.1    1.1   32.8   $0.0198 22.9s
                                                      Sonnet 4.6       280        0.4    1.3    0.4   43.6   $0.0610 28.7s

                                                      GPT-5 nano       280        0.0    7.9    2.9   16.8   $0.0010 8.9s
                                                      GPT-4o mini      280        0.0    1.5    2.9   11.4   $0.0014 14.2s
                                                      GPT-OSS-20B      280        0.0    1.9    0.4   10.0   $0.0020 5.6s
                               Replace Handoff
                                                      GPT-OSS-120B     280        0.0    3.8    0.4    9.3   $0.0046 8.1s
                                                      Haiku 4.5        280        0.4    8.1    0.4    8.6   $0.0133 17.9s
                                                      Sonnet 4.6       280        0.0    5.8    0.4    7.8   $0.0423 27.0s




                                                                             6
                                     Partitioning Deterministic and Neural Health Generation

B. Example Pipeline Trace

Input record and deterministic facts                                    Bounded writer output
  {                                                                     {
  "date": "2026-02-23",                                                 "headline": {
  "history window": "2026-02-09..2026-02-23",                           "title": "Your recovery looks different",
  "sleep": {                                                            "core insight": "Your HRV dropped to
  "score": 84,                                                          34 ms, down 17% from your baseline.",
  "duration": "7h 50m",                                                 "how to improve": "Do a 10-minute
  "deep": "1h 26m", "rem": "1h 40m",                                    progressive muscle relaxation tonight..."
  "light": "4h 44m"                                                     },
  },                                                                    "analysis card": {
  "vitals": {                                                           "metric id": "hrv",
  "hrv": "34.2 ms",                                                     "finding statement": "HRV down 17%",
  "heart rate": "59.2 bpm",                                             "tags": [
  "resp rate": "15.8 brpm"                                              {"name": "Alcohol", ...},
  },                                                                    {"name": "Stress", ...},
  "snore percent": "6.0%",                                              {"name": "Sick", ...},
  "tag candidates": [                                                   {"name": "Fever", ...}
  "Alcohol", "Stress", "Sick", "Fever"                                  ]
  ],                                                                    }
  "selected metric": "hrv",                                             }
  "comparison": "34.2 vs 41.3 ms (-17%)"
  }


    Deterministic handoff. The pipeline selects hrv as the surfaced metric and gives the writer the fixed comparison “34.2 vs 41.3
    ms (−17%).” The writer may copy the pre-generated attribution tags shown in blue, but it may not add new tags or recalculate
    numbers.

Figure 4. Representative TFTS trace for one user-night (Sonnet 4.6, 2026-02-23). The figure shows the compacted structured input,
deterministic selected facts, and final schema-constrained output. Blue spans mark tag fields copied through the bounded writer interface.




                                                                    7
