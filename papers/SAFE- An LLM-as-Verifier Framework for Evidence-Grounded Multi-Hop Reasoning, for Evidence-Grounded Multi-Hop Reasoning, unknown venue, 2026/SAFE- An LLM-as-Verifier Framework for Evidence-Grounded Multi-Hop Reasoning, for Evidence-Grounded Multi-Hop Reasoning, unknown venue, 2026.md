                                                                      SAFE: An LLM-as-Verifier Framework
                                                                   for Evidence-Grounded Multi-Hop Reasoning

                                                 Daeyong Kwon                                Soyoung Yoon                        Seung-won Hwang*
                                             daeyongkwon@snu.ac.kr                      soyoung.yoon@snu.ac.kr                  seungwonh@snu.ac.kr

                                                                                Seoul National University, South Korea



                                                                    Abstract                               entities, unsupported relations, or implicit shortcuts.
                                                                                                           As a result, final-answer accuracy alone can reward
arXiv:2604.01993v3 [cs.CL] 23 Aug 2026




                                                 Multi-hop QA benchmarks often reward Large                spurious reasoning rather than evidence-grounded
                                                 Language Models (LLMs) for spurious cor-
                                                                                                           inference.
                                                 rectness, where models reach correct answers
                                                 through invalid intermediate reasoning. We                   Recent LLM-as-judge approaches make it pos-
                                                 propose SAFE, an LLM-as-verifier framework                sible to evaluate generated answers, but judging
                                                 for evidence-grounded multi-hop QA. Rather                completed outputs is not sufficient for multi-hop
                                                 than judging only the final answer after gener-           reasoning. In evidence-grounded QA, errors of-
                                                 ation, SAFE verifies reasoning during genera-             ten arise before the final answer. A single unsup-
                                                 tion by checking intermediate steps against the           ported entity or wrong relation can mislead the
                                                 provided passages and previous reasoning tra-
                                                                                                           subsequent reasoning trajectory. This suggests that
                                                 jectory. To make this process checkable, SAFE
                                                 decomposes reasoning into atomic, evidence-
                                                                                                           verification should move from output-level judg-
                                                 grounded units represented with Knowledge                 ment to process-level verification. Rather than ask-
                                                 Graph (KG) triples. At train-time, SAFE verifies          ing only whether the final answer is correct, an
                                                 benchmark supervision under KG-grounded                   LLM-as-verifier framework should check whether
                                                 constraints and constructs reliable verifier train-       each intermediate reasoning step is supported by
                                                 ing data. At inference-time, an external verifier         the provided evidence and provide feedback before
                                                 checks each generated step, identifies invalid            errors propagate.
                                                 reasoning, and provides correction feedback
                                                                                                              We propose SAFE, an LLM-as-verifier frame-
                                                 before errors propagate. Across three multi-
                                                 hop QA benchmarks, SAFE improves accuracy                 work for evidence-grounded multi-hop QA. Instead
                                                 by 8.8 pp on average. These results show that             of verifying only the final output after generation,
                                                 evidence-grounded multi-hop QA benefits from              SAFE verifies reasoning during generation. Each
                                                 shifting LLM-based evaluation from post-hoc               intermediate step is treated as an atomic unit that
                                                 answer judgment to stepwise reasoning verifi-             should be grounded in the provided evidence, al-
                                                 cation.1                                                  lowing the verifier to check whether the reasoning
                                                                                                           process remains valid before moving to the next
                                         1       Introduction
                                                                                                           step. When an invalid step is detected, SAFE pro-
                                         The frontier of Large Language Models (LLMs)                      vides structured feedback that helps the generator
                                         has increasingly shifted toward complex reason-                   revise the reasoning trajectory before the error prop-
                                         ing tasks, such as multi-hop question answering                   agates. To support this stepwise verification, we
                                         (QA), where a model must synthesize evidence                      represent reasoning steps using Knowledge Graph
                                         across multiple documents to derive a final answer.               (KG) triples, which provide a compact and check-
                                         Chain-of-Thought (CoT) prompting has substan-                     able form for linking entities and relations to the
                                         tially improved performance on such tasks (Wei                    given context.
                                         et al., 2022), but its free-form reasoning traces re-                SAFE operates at both train-time and inference-
                                         main difficult to ground or verify (Turpin et al.,                time. At train-time, SAFE verifies benchmark super-
                                         2023). A model may arrive at the correct answer                   vision by enforcing atomicity and evidence ground-
                                         through intermediate steps that introduce unverified              ing over standard multi-hop QA datasets (Ho et al.,
                                             * Corresponding author
                                                                                                           2020; Yang et al., 2018; Trivedi et al., 2022). This
                                             1
                                             Code and data are available at https://github.com/            process removes up to 14% of instances whose rea-
                                         DaeyongKwon98/SAFE                                                soning supervision is not fully verifiable. More

                                                                                                       1
importantly, train-time verification constructs reli-          ing completed generations, but they typically oper-
able supervision for the verifier itself. Instead of           ate after the full output has already been produced.
treating noisy benchmark reasoning paths as gold,              In evidence-grounded multi-hop QA, however, im-
SAFE converts unverifiable reasoning steps into tar-           portant failures can occur before the final answer is
geted diagnostic and corrective signals. This allows           generated (Ishii et al., 2024). An intermediate step
the verifier to learn not only whether a step is valid,        may introduce an unsupported entity, an incorrect
but also how to respond when the reasoning process             relation, or a shortcut that affects the subsequent
deviates from the evidence.                                    reasoning process. In contrast, LLM-as-verifier
    At inference-time, SAFE uses an external verifier          methods aim to check whether each intermediate
as a stepwise process controller. Given a partial              step is supported by the provided evidence and
reasoning trajectory, the verifier checks whether              provide feedback before errors propagate.
the next generated step is grounded in the evidence               Process verification methods also emphasize in-
and corresponds to a single evidence-supported KG              termediate reasoning steps (Lightman et al., 2024).
triple. If the step is invalid, SAFE localizes the error       However, many of these methods are developed
and provides correction feedback for revising the              for domains such as mathematical reasoning (Wu
next step. This differs from LLM self-correction,              et al., 2025), where step correctness is not neces-
which relies on the same model to critique its own             sarily tied to retrieved textual evidence. In con-
reasoning and is often unreliable (Huang et al.,               trast, evidence-grounded multi-hop QA requires
2023; Tyen et al., 2024). By separating genera-                each reasoning step to be independently grounded
tion from verification, SAFE maintains evidence-               in the given context. SAFE targets this setting by
grounded reasoning trajectories rather than merely             treating multi-hop QA as stepwise verification over
scoring completed outputs.                                     evidence-grounded reasoning steps.
    Empirically, SAFE significantly improves multi-
hop QA performance, achieving an average +8.8                  2.2   Multi-hop QA Benchmarks and Spurious
pp accuracy gain over baseline reasoning meth-                       Reasoning
ods. Further analyses show that these gains come               Multi-hop QA benchmarks such as 2WikiMulti-
from structured step-level verification and feed-              hopQA (Ho et al., 2020), HotpotQA (Yang et al.,
back, rather than generic feedback alone. We also              2018), and MuSiQue (Trivedi et al., 2022) have
find that SAFE remains effective across different              been widely adopted for evaluating complex rea-
verifier-training and generator settings, and can be           soning and retrieval-augmented generation (RAG)
extended to incomplete-evidence scenarios.                     systems (Jimenez Gutierrez et al., 2024; Trivedi
    Our main contributions are as follows:                     et al., 2023). However, final-answer accuracy can
• We formulate evidence-grounded multi-hop QA                  overestimate true reasoning ability. Ishii et al.
   as an LLM-as-verifier problem, shifting from                (2024) show that a non-trivial portion of correct
   post-hoc LLM-as-judge evaluation to stepwise                answers in standard multi-hop QA datasets arise
   verification of intermediate reasoning.                     from spurious reasoning, where models reach the
• We propose SAFE, an LLM-as-verifier framework                right answer without following a fully supported
   that uses stepwise atomic verification to construct         reasoning path.
   reliable verifier supervision at train-time and cor-           To reduce or analyze such failures, prior work
   rect invalid reasoning steps at inference-time.             has incorporated KGs before or after generation.
• We show that SAFE achieves a +8.8 pp accuracy                For example, Fang et al. (2024) extract KG chains
   gain, with analyses confirming the importance               before generation, while Nguyen et al. (2024) eval-
   and robustness of structured step-level verifica-           uate generated CoT reasoning by mapping the rea-
   tion and feedback.                                          soning steps to a KG. More closely related to our
                                                               setting is REVEAL (Jacovi et al., 2024), which
2     Related Works                                            assigns correctness labels to individual reasoning
                                                               steps using a specialized error taxonomy. Hop,
2.1    From LLM-as-Judge to LLM-as-Verifier                    Skip, and Overthink (Yadav et al., 2025) similarly
Recent LLM-as-judge methods use LLMs as scal-                  studies post-hoc failure modes to localize reasoning
able evaluators for generated answers, rationales,             breakdowns.
and open-ended outputs (Zheng et al., 2023; Liu                   These approaches are important for exposing un-
et al., 2023). These methods are useful for assess-            supported or shortcut reasoning, but they mainly

                                                           2
analyze completed reasoning trajectories or rely on              Concretely, we represent each reasoning step as
static KG chains. SAFE instead uses KG-grounded               a KG triple, so that the step corresponds to a single
atomic steps as the basis for stepwise verification.          checkable operation. A step is considered valid
At train-time, this supports the construction of ver-         only when its entities and relation are explicitly
ifiable supervision. At inference-time, it enables            supported by the provided passages. This represen-
the verifier to check intermediate steps before the           tation allows the verifier to determine whether the
next step generation.                                         current reasoning state remains grounded before
                                                              the generator proceeds to the next step.
2.3    Self-Correction and Inference-Time                        When a proposed step is not supported, the veri-
       Feedback                                               fier returns structured feedback for correction. The
LLMs can be prompted to critique and revise their             feedback identifies the source of the failure and
own outputs (Madaan et al., 2023) or accumulate               provides guidance that helps the generator revise
reflective feedback across trials (Shinn et al., 2023).       the invalid step. In this way, SAFE uses verification
Methods such as Self-Refine (Madaan et al., 2023)             not only to judge whether a step is valid, but also
show that self-critique can improve output quality            to support correction during generation.
without additional training or external models.                  This stepwise verification process is used at
   However, self-correction alone is unreliable for           both train-time and inference-time. At train-time,
complex multi-hop reasoning. The same model                   the atomic and evidence-grounded representation
that produced an invalid step may fail to identify            guides benchmark verification and verifier-data
the error, especially when the error depends on               construction. At inference-time, the verifier applies
evidence grounding. Prior work shows that LLMs                the same evidence-grounding criterion to each pro-
often struggle to correct their own reasoning flaws           posed step and provides feedback when correction
without external ground-truth signals (Huang et al.,          is needed.
2023). Tyen et al. (2024) further identify mistake
                                                              3.2   Atomic Reasoning Units and Verification
finding as a key bottleneck, showing that unguided
                                                                    Feedback
models frequently fail to locate their own logical
missteps.                                                     We define a valid reasoning trajectory as a sequence
   SAFE differs from pure self-correction by separat-         of evidence-grounded atomic steps. Let P denote
ing generation from verification. Instead of asking           the passages provided as context. Each reason-
the generator to critique its own output, SAFE uses           ing step si must correspond to a single KG triple
an external verifier to check each reasoning step             (ehead , r, etail ), where both entities and the rela-
against the provided evidence. When a step is in-             tion are supported by P. This representation de-
valid, the verifier provides feedback that helps the          composes multi-hop reasoning into independently
generator return to evidence-supported reasoning.             checkable units, making it possible to verify each
                                                              step before proceeding to the next one. When a step
3     SAFE: An LLM-as-Verifier Framework                      is invalid, the verifier produces structured feedback
                                                              that indicates why the step fails and how the gen-
SAFE is an LLM-as-verifier framework for                      erator should revise it. We organize this feedback
evidence-grounded multi-hop QA. This section first            using four error categories: Procedural, Attribution,
defines the stepwise verification protocol used by            Logical, and Final Answer (Appendix Table 9).
SAFE, then describes how the framework constructs                SAFE applies these categories in a fixed verifica-
verifier supervision at train-time and applies exter-         tion order. Procedural errors capture invalid step
nal verification during inference.                            structure, such as loops and disconnected reasoning
                                                              paths. After procedural validity is checked, Attribu-
3.1    Evidence-Grounded Stepwise Verification                tion errors identify entities or relations that are not
A verifier for evidence-grounded multi-hop QA not             grounded in the provided passages. Logical errors
only assigns a correctness score, but also checks             capture relation-level inconsistencies, where the
whether each intermediate step is supported before            step uses an incorrect relation even if the entities
the reasoning process continues. SAFE addresses               are mentioned in the context. Finally, Final Answer
this by treating intermediate reasoning steps as              errors arise when the reasoning trajectory is locally
atomic units that can be independently checked                valid but does not reach the correct answer. The
against the provided evidence.                                predicted category is then used to produce feedback

                                                          3
  Dataset      Split    Total    Unverifiable    Ratio           datasets, 3%–14% of instances are unverifiable un-
               Train   167,454       7,452       4.45%           der our atomic grounding constraints. After filter-
  2Wiki
               Val      12,576        901        7.16%           ing these instances, SAFE uses the remaining exam-
  HotpotQA
               Train   90,447        2,376       2.63%           ples to train and evaluate the verifier on evidence-
               Val      7,345         227        3.09%           supported reasoning paths.
               Train   19,902        2,149      10.80%
  MuSiQue
               Val      2,412         342       14.18%           Constructing Verifier Training Data. Training
                                                                 the verifier requires both valid reasoning trajecto-
Table 1: Statistics of instances flagged as unverifiable
                                                                 ries and diverse invalid steps. Using the verified
by our KG-grounded benchmark verification pipeline.
                                                                 benchmark set, we construct 3.9k ideal trajecto-
                                                                 ries whose steps are grounded in the provided pas-
for revising the invalid step.
                                                                 sages. We then synthesize 7.6k negative examples
3.3   Train-Time Verification for Reliable                       through controlled error injection. Starting from
      Verifier Supervision                                       valid trajectories, a teacher model introduces step-
                                                                 level violations aligned with the error categories.
A verifier cannot be trained or evaluated reliably
                                                                 This produces corrupted trajectories with an error
if the underlying benchmark supervision is not it-
                                                                 step, category, diagnosis, and correction guidance.
self verifiable. Standard multi-hop QA datasets
                                                                    Synthetic perturbations provide controlled cov-
may contain missing relations, ambiguous entity
                                                                 erage of error types, but they may not fully capture
mappings, or incomplete supporting facts that al-
                                                                 the failures made by the target generator during
low the correct answer without a fully grounded
                                                                 inference. To reduce this gap, we use an iterative
reasoning path. Such cases make it difficult to de-
                                                                 refinement strategy. We first train an initial ver-
termine whether an intermediate step is valid under
                                                                 ifier on the synthetic data and analyze recurring
an evidence-grounded verification.
                                                                 failures, such as confusing lexically similar entities
   To address this issue, SAFE first verifies bench-
                                                                 or mishandling numerical comparisons. For each
mark supervision under the KG-grounded step con-
                                                                 recurring failure pattern, we use the teacher model
straints defined in Section 3.2. This train-time veri-
                                                                 to generate additional feedback labels. Through
fication produces a filtered benchmark set in which
                                                                 this train → analyze → augment cycle, we add 848
verifier supervision can be constructed and evalu-
                                                                 hard cases to the training pool. The final verifier
ated from evidence-supported reasoning paths. We
                                                                 training set contains 11.5k instances.
use gpt-oss-120b (Agarwal et al., 2025) as the base
                                                                    The overall training set statistics are shown in
LLM for this pipeline, with prompts detailed in
                                                                 Appendix Figure 4. Additional details, including
Appendix A.9. The pipeline proceeds as follows.
                                                                 the positional distribution of error steps and dataset
1. Triple Extraction: We prompt the LLM to ex-
                                                                 statistics, are provided in Appendix A.5.
    tract atomic triples (ehead , r, etail ) from the gold
    passages, treating the context as a localized KG.            3.4   Inference-Time Stepwise Verification
2. Iterative Gleaning: We perform up to two addi-                At inference-time, SAFE uses an external verifier to
   tional extraction rounds to recover valid triples             check generated reasoning steps during generation.
   that may have been missed in the initial stage.               Given a question q, passages P, and a partial rea-
3. Entity Resolution: We merge synonymous                        soning trajectory, the generator proposes the next
   or coreferential entities, such as “USA” and                  atomic step. The verifier then checks whether the
   “United States”, to build a normalized local KG.              proposed step is grounded in the evidence and con-
                                                                 sistent with a single evidence-supported KG triple.
4. Reasoning Path Discovery: We search for a
                                                                    Formally, let a reasoning trajectory be repre-
   continuous evidence-grounded reasoning path
                                                                 sented as a sequence of atomic steps:
   that connects entities to the gold answer.
                                                                                 τ = (s1 , s2 , . . . , st ).
5. Validation: If no valid reasoning path can be
   found under this protocol, the data is marked as              Given the current reasoning prefix s1:t , the verifier
   unverifiable and removed from the verified set.               F predicts:
   Appendix Figure 1 provides an overview of the                             (yt , dt , gt ) = F (q, P, s1:t ),
verification pipeline, and Table 1 summarizes the                 where:
benchmark-level results. Across the examined                     • yt denotes whether the current step is valid or

                                                             4
   belongs to one of the error categories defined in               GPT 5.4 mini (OpenAI, 2026), reported separately
   Section 3.2.                                                    in Section 5. The stepwise verifier is trained on
• dt provides a natural language diagnosis of why                  the non-thinking version of Qwen3-8B to prioritize
   the step is invalid or inconsistent with the evi-               training efficiency and architectural simplicity. For
   dence.                                                          constructing verified training data, we use gpt-oss-
• gt provides correction guidance for revising the                 120b (Agarwal et al., 2025) as the teacher model.
   invalid step or generating a valid next step.
    If the verifier marks the step as valid, the step              Compared Methods. We compare SAFE against
is accepted and generation continues. If the ver-                  both specialized multi-hop QA systems and step-
ifier detects an error, the generator receives the                 wise reasoning baselines. First, we include
feedback, revises the step, and continues from the                 TRACE (Fang et al., 2024) as a specialized KG-
corrected reasoning prefix. In this way, SAFE veri-                based baseline. TRACE uses KG chains for multi-
fies and corrects intermediate reasoning steps dur-                hop QA, but it relies on static pre-generation ex-
ing generation. Our inference-time diagram is de-                  traction rather than inference-time verification. We
scribed in Appendix Figure 3.                                      evaluate TRACE under the same context setting
                                                                   as SAFE. For additional context, we also report IR-
4       Experiments                                                CoT (Trivedi et al., 2023), a retrieval-based multi-
                                                                   hop QA framework. Because IRCoT operates with
4.1       Experimental Setup                                       iterative retrieval, its results are included as a con-
Datasets. We evaluate SAFE on three multi-                         textual reference rather than a strictly controlled
hop QA benchmarks: 2WikiMultihopQA (Ho                             comparison.
et al., 2020), HotpotQA (Yang et al., 2018), and                       Second, to isolate the effect of stepwise verifica-
MuSiQue (Trivedi et al., 2022). We apply the KG-                   tion, we compare three reasoning methods for the
grounded verification pipeline in Section 3.3 to the               same generator models:
validation splits and construct a verified evaluation              • No Verification: The generator produces one
pool. From this pool, we sample 1,000 instances                       atomic reasoning step at a time until it reaches a
per benchmark, yielding 3,000 evaluation exam-                        final answer. No verifier is used.
ples in total. Each question is evaluated with 10
                                                                   • Self-Verification: The generator evaluates its own
passages, including the gold evidence passages and
                                                                     intermediate step after each generation and re-
distractors. Additional data processing details are
                                                                     vises the step if it detects an error.
provided in Appendix A.4.
                                                                   • SAFE: The generator is paired with our external
Evaluation Metrics. We report Exact Match                            verifier. The verifier checks each step against the
(EM), token-level F1, and answer accuracy. EM                        provided evidence and returns a diagnosis and
and F1 measure surface-level overlap with the                        actionable guidance when the step is invalid.
ground-truth answer, but they may underestimate
performance when a generated answer is semanti-                    Implementation Details. We fine-tune the ver-
cally correct with different wording. We therefore                 ifier with QLoRA (Dettmers et al., 2023) on the
use an LLM-as-judge evaluator (Li et al., 2025),                   Qwen3-8B non-thinking architecture for 2 epochs.
implemented with gpt-oss-120b, to assess answer-                   We use a learning rate of 1 × 10−4 and an effective
level semantic equivalence.                                        batch size of 64. All experiments are conducted
                                                                   on 4× A6000 GPUs. During inference, we use
Models. We evaluate SAFE across multiple gen-                      greedy decoding with temperature 0 for determinis-
erator families and sizes: Qwen3-4B, Qwen3-                        tic generation. We set the maximum retry attempts
8B (Yang et al., 2025), Qwen2.5-14B (Qwen et al.,                  N to 3 and the maximum reasoning steps K to 10,
2025), Llama-3.1-8B (Grattafiori et al., 2024), and                which provides the best cost-performance trade-off
Gemma-3-12B (Team et al., 2025).2 These models                     in Appendix A.8. Additional training details are
are used for the main evaluation on the full veri-                 provided in Appendix A.2.
fied benchmark set. To further test whether SAFE
remains useful with stronger reasoning models, we                  4.2   Main Results
additionally conduct a subset evaluation with Gem-                 Table 2 reports results on the three verified multi-
ini 3.1 Flash Lite (Google DeepMind, 2026) and                     hop QA benchmarks. Across datasets and gen-
    2
        We use the instruction-tuned version when available.       erator models, SAFE consistently improves an-

                                                               5
                                            2Wiki               HotpotQA                 MuSiQue                 Average
 Model           Method                                                                                                            ∆
                                     EM      F1     Acc    EM         F1   Acc    EM       F1      Acc    EM       F1      Acc
 Without Feedback
                 IRCoT†              36.1   52.3     -     50.8   65.7      -     27.4     36.9     -     38.1    51.6      -       -
 Llama 3 8B
                 TRACE†              45.5   56.4     -     55.1   70.0      -     33.4     40.1     -     44.7    55.5      -       -
 Gemma 3 12B                         50.7   65.1    79.4   51.1   68.1     86.6   41.7     56.4    67.3   47.8    63.2     77.8     -
 Qwen 2.5 14B                        55.4   71.0    87.2   49.5   68.4     87.9   40.4     54.1    67.1   48.4    64.5     80.7     -
 Llama 3.1 8B    No Verification     51.0   59.6    67.5   51.1   66.7     78.9   36.3     46.9    53.4   46.1    57.7     66.6     -
 Qwen 3 8B                           53.7   66.6    85.6   47.5   65.8     87.4   40.2     53.0    68.7   47.1    61.8     80.6     -
 Qwen 3 4B                           65.8   75.8    84.2   56.2   72.4     86.5   42.2     53.6    63.2   54.7    67.3     78.0     -

 With Feedback
                 Self-Verification   54.3   65.0    73.3   54.6   70.5     83.4   45.6     58.1    68.0   51.5    64.5     74.9
 Gemma 3 12B
                 SAFE (Ours)         72.9   82.7    91.8   59.6   77.5     90.0   53.7     66.6    76.7   62.1    75.6     86.2   +8.4
                 Self-Verification   63.2   72.2    80.6   53.9   69.7     84.3   37.2     49.3    60.5   51.4    63.7     75.1
 Qwen 2.5 14B
                 SAFE (Ours)         72.8   81.7    91.0   60.8   76.8     91.2   50.7     63.6    74.7   61.4    74.0     85.6   +4.9
                 Self-Verification   54.2   65.0    73.2   54.9   70.8     83.8   44.1     56.7    66.0   51.1    64.2     74.3
 Llama 3.1 8B
                 SAFE (Ours)         71.7   80.9    90.7   60.4   77.1     90.3   51.8     64.7    75.3   61.3    74.3     85.4   +11.1
                 Self-Verification   64.0   73.4    82.9   55.0   71.2     84.4   44.5     55.7    65.2   54.5    66.8     77.5
 Qwen 3 8B
                 SAFE (Ours)         71.5   81.3    91.3   61.2   78.3     90.9   53.8     66.7    76.6   62.2    75.4     86.3   +5.7
                 Self-Verification   65.9   74.9    82.8   56.5   70.6     82.6   38.4     48.2    56.9   53.6    64.6     74.1
 Qwen 3 4B
                 SAFE (Ours)         70.8   79.8    89.4   60.5   75.7     89.0   49.8     61.5    74.5   60.4    72.3     84.3   +6.3

                 No Verification     55.3   67.6    80.8   51.1   68.3     85.5   40.2     52.8    63.9   48.9    62.9     76.7
 Total Average   Self-Verification   60.3   70.1    78.6   55.0   70.6     83.7   42.0     53.6    63.3   52.4    64.8     75.2
                 SAFE (Ours)         71.9   81.3    90.8   60.5   77.1     90.3   52.0     64.6    75.6   61.5    74.3     85.6   +8.8

Table 2: Results on three multi-hop QA benchmarks. Evaluation metrics are Exact Match, F1 score, and LLM-as-
judge accuracy. ∆ denotes the improvement of SAFE over the best baseline (No Verification or Self-Verification) in
terms of average accuracy. † indicates results directly reported from the original paper (Fang et al., 2024).


swer accuracy over both no-verification and self-                     paths. On MuSiQue, SAFE improves average ac-
verification baselines. On average, SAFE achieves                     curacy by 11.7 pp, from 63.9% to 75.6%, and im-
an 8.8 pp accuracy gain over the strongest baseline                   proves EM by 10.0 pp. These gains suggest that
and improves EM by 9.1 pp, from 52.4% to 61.5%.                       stepwise verification is most beneficial when errors
   The comparison with no-verification shows that                     can accumulate across multiple reasoning steps.
atomic step-wise generation is a strong starting                         Finally, the results show that SAFE is not tied
point, but it is not sufficient. Even when the gen-                   to a single generator architecture. Despite differ-
erator is prompted to produce one atomic step at                      ences in model family and scale, generators paired
a time, unsupported entities, invalid relations, and                  with SAFE reach a similar high-performance range
skipped intermediate steps can still appear. SAFE                     of roughly 84%–86% average accuracy. This sug-
addresses these failures by checking each interme-                    gests that the gains come from external stepwise
diate step against the evidence before the reasoning                  verification rather than from the characteristics of
process continues.                                                    a particular generator. Overall, the main results
   The comparison with self-verification highlights                   show that evidence-grounded multi-hop QA bene-
the limitation of relying on the generator to critique                fits from an LLM-as-verifier framework that checks
itself. Self-verification decreases average accuracy                  and corrects intermediate reasoning steps during
from 76.7% to 75.2%, and the drop is especially                       generation.
large for Qwen2.5-14B, where accuracy falls from
                                                                      5    Analysis: What Makes SAFE Effective?
80.7% to 75.1%. This supports the need for an ex-
ternal verifier, since the same model that generates                  The main results show that SAFE improves answer
a reasoning step may fail to locate its own ground-                   accuracy across datasets and generator models. We
ing errors or may reinforce an invalid trajectory                     analyze the sources and robustness of these gains
when asked to verify it.                                              through five findings, covering structured step-level
   SAFE is especially effective on MuSiQue, the                       feedback, train-time supervision, teacher strength,
most challenging benchmark in our evaluation due                      generator strength, and incomplete-evidence sce-
to its longer and more compositional reasoning                        narios. Additional efficiency and failure-pattern

                                                                  6
 Model         Setting             2Wiki      Hotpot     MSQ     Avg          Model          Training Data     2Wiki         Hotpot         MSQ            Avg
                                                                                             Verified           91.8          90.0          76.7          86.2
               Diagnosis only      86.5         88.0     71.2    81.9         Gemma-3-12B
                                                                                             + Unverifiable   88.5 (-3.3)   89.7 (-0.3)   74.9 (-1.8)   84.4 (-1.8)
 Gemma 12B     Guidance only       90.9         88.8     76.9    85.5
               Full                91.8         90.0     76.7    86.2                        Verified           90.2          90.1          76.6          85.6
                                                                              Qwen2.5-14B
                                                                                             + Unverifiable   88.0 (-2.2)   87.9 (-2.2)   70.9 (-5.7)   82.3 (-3.3)
               Diagnosis only      83.7         83.6     66.5    77.9                        Verified           90.7          90.3          75.3          85.4
 Llama 8B      Guidance only       89.5         89.5     77.2    85.4         Llama-3.1-8B
                                                                                             + Unverifiable   88.2 (-2.5)   87.5 (-2.8)   72.3 (-3.0)   82.7 (-2.7)
               Full                90.7         90.3     75.3    85.4                        Verified           91.3          90.9          76.6          86.3
                                                                              Qwen3-8B
               Diagnosis only      90.1         88.6     74.1    84.3                        + Unverifiable   88.0 (-3.3)   89.5 (-1.4)   75.0 (-1.6)   84.2 (-2.1)
 Qwen 8B       Guidance only       91.2         90.0     76.6    85.9         Qwen3-4B
                                                                                             Verified           89.4          89.0          74.5          84.3
               Full                91.3         90.9     76.6    86.3                        + Unverifiable   86.6 (-2.8)   86.8 (-2.2)   70.6 (-3.9)   81.3 (-3.0)

                                                                                             Verified           90.7          90.1          75.9          85.6
                                                                              Total
                                                                                             + Unverifiable   87.9 (-2.8)   88.3 (-1.8)   72.7 (-3.2)   83.0 (-2.6)
Table 3: Ablation of verifier feedback formats.
Guidance-only feedback provides the strongest signal,
                                                                             Table 5: Effect of adding unverifiable instances to veri-
while the full format combines diagnosis and guidance
                                                                             fier training data. Training with unverifiable supervision
for more stable correction.
                                                                             consistently degrades accuracy, showing the importance
                                                                             of train-time benchmark verification.
 Drop Category    Gemma 3 12B         Llama 3.1 8B        Qwen 3 8B
 No Drop               86.2                  85.4            86.3
 Procedural          85.2 (-1.0)           82.9 (-2.5)     84.4 (-1.9)       validity from evidence-grounding failures. These
 Attribution         84.4 (-1.8)           82.8 (-2.6)     84.5 (-1.8)
 Logical             85.5 (-0.7)           84.3 (-1.1)     85.0 (-1.3)       results show that the feedback categories provide
                                                                             useful supervision for detecting and correcting in-
Table 4: Performance degradation (average score) under                       valid reasoning steps.
different error category removals. Values in parentheses
indicate absolute change (∆) from the No Drop setting.                       Finding 2: Train-time verification improves ver-
                                                                             ifier supervision. We next examine how train-
analyses are provided in Appendix A.8.                                       time verification affects verifier training. As shown
                                                                             in Table 5, we compare our standard verifier,
Finding 1: Structured step-level feedback mat-
                                                                             trained on the verified training set, with a vari-
ters. We first analyze whether SAFE improves per-
                                                                             ant trained on the same data plus 5.3k instances
formance through generic feedback or structured
                                                                             flagged as unverifiable by our KG-grounded verifi-
step-level feedback. To isolate this effect, we ab-
                                                                             cation pipeline. These additional instances follow
late the verifier’s response format with three set-
                                                                             the same data generation format but do not satisfy
tings: Diagnosis only, Guidance only, and Full.
                                                                             the evidence-grounding constraints.
Diagnosis-only explains the error without provid-
                                                                                Adding unverifiable instances consistently hurts
ing correction guidance, guidance-only provides
                                                                             performance, causing an average accuracy drop of
correction guidance without explicit diagnosis, and
                                                                             2.6 pp. This indicates that unverifiable supervision
full uses both.
                                                                             introduces contradictory training signals, causing
   Table 3 shows that guidance provides the                                  the verifier to approve steps that cannot be sup-
strongest signal. Across Gemma-3-12B, Qwen3-                                 ported by the provided evidence. This shows that
8B, and Llama-3.1-8B, guidance-only substantially                            train-time verification helps construct reliable su-
outperforms diagnosis-only, indicating that simply                           pervision for the verifier.
explaining what went wrong is insufficient. The
                                                                                We also evaluate whether the iterative refinement
verifier must also provide information that helps
                                                                             strategy in Section 3.3 improves the verifier beyond
the generator revise the invalid step. At the same
                                                                             synthetic error injection. As shown in Appendix
time, the full verifier is the most stable overall, sug-
                                                                             Table 17, targeted refinement improves average ac-
gesting that diagnosis contributes to a reliable feed-
                                                                             curacy by 2.9 pp, with the largest gain on MuSiQue
back interface. Thus, SAFE goes beyond generic
                                                                             (+4.2 pp). This suggests that synthetic perturba-
feedback by using step-level verification to support
                                                                             tions provide broad coverage of error categories,
correction during generation.
                                                                             while targeted refinement helps the verifier learn
   We further test whether the error categories are                          model-specific failures that occur during actual in-
useful for verifier training by removing each ma-                            ference.
jor category. As shown in Table 4, dropping any
category degrades performance across generator                               Finding 3: SAFE is not merely strong teacher
models. Removing Procedural and Attribution cat-                             distillation. Because gpt-oss-120b is used to con-
egories is especially harmful, indicating that the                           struct verifier training data, a natural question
verifier benefits from distinguishing reasoning-path                         is whether SAFE’s gains mainly come from the

                                                                         7
 Model           No Verification   Self-Verification   SAFE (20B)   SAFE (120B)           Model          Dataset    W/O Retrieval   W/ Retrieval
 Gemma3 12B           78.0               73.0             84.7         89.7
 Qwen3 8B             83.7               76.3             86.7         89.0                              2Wiki           44             92
 Llama 3.1 8B         66.3               56.7             78.7         83.0               Gemma 3 12B    HotpotQA        55             90
                                                                                                         MuSiQue         43             81
Table 6: Performance with weaker teacher model’s veri-                                                   2Wiki           31             95
fication signal (gpt-oss-20b). Results are averaged over                                  Qwen 3 8B      HotpotQA        57             88
100 examples per benchmark.                                                                              MuSiQue         42             77
                                                                                                         2Wiki           35             93
 Model             Method              2Wiki     Hotpot    MSQ      Avg       ∆           Llama 3.1 8B   HotpotQA        53             87
                   No Verification      94.0      90.0     71.0     85.0    –                            MuSiQue         44             69
 Gemini 3.1 FL     Self-Verification    91.0      86.0     71.0     82.7    –
                   SAFE                 94.0      94.0     76.0     88.0   +3.0           Total Avg.                    44.9        85.8 (+40.9)
                   No Verification      85.0      93.0     82.0     86.7    –
 GPT-5.4 Mini      Self-Verification    92.0      87.0     74.0     84.3    –
                   SAFE                 97.0      93.0     80.0     90.0   +3.3       Table 8: Performance of with/without retrieval under
                                                                                      incomplete evidence setting. Results are averaged over
Table 7: Subset evaluation on stronger reasoning models.                              100 examples per benchmark.
Results are averaged over 100 examples per benchmark.

                                                                                      removed from the initial context. We add Missing
strength of this teacher model. To test this, we                                      Evidence as an additional error category and train
replace gpt-oss-120b with the weaker gpt-oss-20b                                      the verifier to produce a search query when the
for generating verifier supervision while keeping                                     current context is insufficient.
the rest of the pipeline unchanged.                                                      At inference-time, we compare answering with
   Table 6 shows that SAFE remains effective even                                     the incomplete context against retrieving the top-
with the weaker teacher. For Gemma-3-12B,                                             3 passages from the full corpus using verifier-
Qwen3-8B, and Llama-3.1-8B, the verifier trained                                      generated search queries and BM25 (Robertson
with gpt-oss-20b supervision still outperforms both                                   and Zaragoza, 2009). Table 8 shows that using
no-verification and self-verification baselines. The                                  the retrieved passages improves average accuracy
stronger gpt-oss-120b teacher provides additional                                     from 44.9% to 85.8%, yielding a gain of 40.9 pp.
gains, but the consistent improvement with gpt-oss-                                   While this experiment does not aim to solve full
20b indicates that the benefit is not simply inherited                                open-domain retrieval, it demonstrates that SAFE
from a strong teacher. Moreover, the teacher is used                                  can identify missing-evidence failures and use them
only offline for data construction. At inference-                                     to guide retrieval.
time, SAFE uses a separately trained verifier.
                                                                                      6      Conclusion
Finding 4: SAFE remains effective for stronger
generators. To test whether SAFE’s external veri-                                     We introduced SAFE, an LLM-as-verifier frame-
fication remains useful for stronger generators be-                                   work for evidence-grounded multi-hop QA. Rather
yond the small to mid-sized models in our main                                        than treating verification as post-hoc judgment,
experiments, we additionally evaluate Gemini 3.1                                      SAFE verifies intermediate reasoning steps during
Flash-Lite and GPT-5.4 mini. Table 7 shows that                                       generation. By representing reasoning steps as
SAFE still improves over the strongest baseline.                                      evidence-grounded atomic units, SAFE constructs
For Gemini 3.1 Flash-Lite, SAFE improves aver-                                        reliable verifier supervision at train-time and pro-
age accuracy from 85.0% to 88.0%, a gain of 3.0                                       vides feedback for correcting invalid reasoning at
pp. For GPT-5.4 mini, SAFE improves average ac-                                       inference-time. Across three multi-hop QA bench-
curacy from 86.7% to 90.0%, a gain of 3.3 pp.                                         marks, SAFE achieves an average +8.8 pp accu-
These results suggest that stronger reasoning ability                                 racy gain over baselines. Our analyses show that
does not remove the benefit of explicit evidence-                                     these gains arise from structured step-level verifi-
grounded verification.                                                                cation and feedback, highlighting the importance
                                                                                      of checking and correcting intermediate reasoning
Finding 5: SAFE extends to incomplete-evidence                                        steps in evidence-grounded multi-hop QA.
settings. Our main evaluation assumes that the
required evidence is fully included in the provided
context. To examine whether SAFE can extend
beyond this setting, we conduct an incomplete-
evidence experiment where one gold passage is

                                                                                  8
Limitations                                                 Computational Efficiency and Environmental
                                                            Impact Iterative reasoning and correction frame-
While we utilized a KG to ensure the quality of our         works can incur additional computational overhead
verification pipeline, we acknowledge the potential         due to repeated generation and verification steps.
for mislabeling due to inherent noise or incomplete         SAFE mitigates this issue by using efficient KV
coverage in the KG. To address this, rather than            caching mechanisms to reduce redundant compu-
aggressively excluding instances that might con-            tation during iterative generation. While SAFE still
tain valuable reasoning trajectories, we provide the        introduces additional inference-time verification
original dataset with our feedback labels as an aug-        cost compared to single-pass generation, our cost
mented resource. This non-destructive approach              analysis shows that it can improve multi-hop rea-
allows future researchers to audit, refine, or lever-       soning reliability with a moderate computational
age the full context of the data while accounting           overhead. This aligns with the broader need for
for potential label noise in automated diagnostics.         more efficient and sustainable AI systems.
   Furthermore, the efficacy of the SAFE frame-
                                                            Bias and Fairness The performance and behav-
work inherently relies on the reasoning genera-
                                                            ior of SAFE depend on the underlying pre-trained
tor’s instruction-following capabilities. We ob-
                                                            LLMs and the external knowledge sources used for
served instances where, despite the feedback model
                                                            reasoning, such as retrieved Wikipedia passages.
successfully producing accurate diagnoses and ex-
                                                            These models and corpora may contain historical,
plicit corrective guidance, the reasoning genera-
                                                            cultural, or demographic biases. While SAFE tar-
tor failed to effectively incorporate these instruc-
                                                            gets procedural, attribution, logical, and answer-
tions into its subsequent generation step. Such
                                                            level reasoning errors, it is not explicitly designed
instruction-following failures can lead to uncor-
                                                            to detect or mitigate social biases. Users should
rected errors or repeated mistakes within the iter-
                                                            therefore remain cautious, as the system may re-
ative loop. This highlights a dependency on the
                                                            produce or amplify biases present in the source
base language model’s capacity to adhere to com-
                                                            material.
plex, stepwise constraints, suggesting that future
work must address the alignment between correc-             Licenses and Terms of Use. We use publicly
tive feedback and the generator’s execution.                available multi-hop QA benchmarks and open-
                                                            source language models in accordance with their
Ethics Statement                                            respective licenses and terms of use. We cite the
                                                            original creators of all datasets, models, and soft-
This work introduces SAFE, a framework designed             ware artifacts used in our experiments. Our use of
to enhance the reliability of LLMs in evidence-             these artifacts is limited to research and evaluation
grounded multi-hop reasoning through LLM-as-                purposes.
verifier framework. We acknowledge several eth-
ical considerations and potential broader impacts           AI Usage AI-based tools were used for grammar
associated with its development and deployment.             correction and language refinement. The authors
                                                            take full responsibility for all scientific content,
Transparency and Interpretability A persis-                 including the methodology, experiments, and con-
tent ethical challenge with LLMs is their “black-           clusions.
box” nature, which obscures the rationale behind
generated answers. SAFE addresses this opacity
by decomposing multi-hop reasoning into atomic,
evidence-grounded steps that can be independently
verified. This design makes the reasoning process
more transparent by allowing researchers and prac-
titioners to inspect which intermediate steps are
supported, unsupported, or corrected. By expos-
ing step-level diagnoses and actionable guidance,
SAFE can support more precise error analysis, au-
diting, and accountability in AI-assisted reasoning
systems.

                                                        9
References                                                    Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying
                                                               Sheng, Lianmin Zheng, Cody Hao Yu, Joseph Gon-
Sandhini Agarwal, Lama Ahmad, Jason Ai, Sam Alt-               zalez, Hao Zhang, and Ion Stoica. 2023. Efficient
  man, Andy Applebaum, Edwin Arbus, Rahul K                    memory management for large language model serv-
  Arora, Yu Bai, Bowen Baker, Haiming Bao, and 1               ing with pagedattention. In Proceedings of the 29th
  others. 2025. gpt-oss-120b & gpt-oss-20b model               symposium on operating systems principles, pages
  card. arXiv preprint arXiv:2508.10925.                       611–626.
Tim Dettmers, Artidoro Pagnoni, Ari Holtzman, and             Dawei Li, Bohan Jiang, Liangjie Huang, Alimohammad
  Luke Zettlemoyer. 2023. Qlora: Efficient finetuning           Beigi, Chengshuai Zhao, Zhen Tan, Amrita Bhat-
  of quantized llms. Advances in neural information             tacharjee, Yuxuan Jiang, Canyu Chen, Tianhao Wu,
  processing systems, 36:10088–10115.                           and 1 others. 2025. From generation to judgment:
                                                                Opportunities and challenges of llm-as-a-judge. In
Jinyuan Fang, Zaiqiao Meng, and Craig Macdonald.                Proceedings of the 2025 Conference on Empirical
   2024. Trace the evidence: Constructing knowledge-            Methods in Natural Language Processing, pages
   grounded reasoning chains for retrieval-augmented            2757–2791.
   generation. In Findings of the Association for Com-
   putational Linguistics: EMNLP 2024, pages 8472–            Hunter Lightman, Vineet Kosaraju, Yuri Burda, Harri-
   8494.                                                        son Edwards, Bowen Baker, Teddy Lee, Jan Leike,
                                                                John Schulman, Ilya Sutskever, and Karl Cobbe.
Google DeepMind. 2026.        Gemini 3.1 flash-                 2024. Let’s verify step by step. In International
  lite. https://deepmind.google/models/gemini/                  Conference on Learning Representations, volume
  flash-lite/. Accessed: 2026-05-12.                            2024, pages 39578–39601.

Aaron Grattafiori, Abhimanyu Dubey, Abhinav Jauhri,           Yang Liu, Dan Iter, Yichong Xu, Shuohang Wang,
  Abhinav Pandey, Abhishek Kadian, Ahmad Al-                    Ruochen Xu, and Chenguang Zhu. 2023. G-eval:
  Dahle, Aiesha Letman, Akhil Mathur, Alan Schelten,            Nlg evaluation using gpt-4 with better human align-
  Alex Vaughan, and 1 others. 2024. The llama 3 herd            ment. In Proceedings of the 2023 conference on
  of models. arXiv preprint arXiv:2407.21783.                   empirical methods in natural language processing,
                                                                pages 2511–2522.
Xanh Ho, Anh-Khoa Duong Nguyen, Saku Sugawara,
  and Akiko Aizawa. 2020. Constructing a multi-hop            Ilya Loshchilov and Frank Hutter. 2017. Decou-
  qa dataset for comprehensive evaluation of reasoning           pled weight decay regularization. arXiv preprint
  steps. In Proceedings of the 28th International Con-           arXiv:1711.05101.
  ference on Computational Linguistics, pages 6609–
  6625.                                                       Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler
                                                               Hallinan, Luyu Gao, Sarah Wiegreffe, Uri Alon,
                                                               Nouha Dziri, Shrimai Prabhumoye, Yiming Yang,
Jie Huang, Xinyun Chen, Swaroop Mishra,
                                                               and 1 others. 2023. Self-refine: Iterative refinement
   Huaixiu Steven Zheng, Adams Wei Yu, Xiny-
                                                               with self-feedback. Advances in neural information
   ing Song, and Denny Zhou. 2023. Large language
                                                               processing systems, 36:46534–46594.
   models cannot self-correct reasoning yet. arXiv
   preprint arXiv:2310.01798.                                 Minh-Vuong Nguyen, Linhao Luo, Fatemeh Shiri, Dinh
                                                                Phung, Yuan-Fang Li, Thuy Vu, and Gholamreza
Ai Ishii, Naoya Inoue, Hisami Suzuki, and Satoshi               Haffari. 2024. Direct evaluation of chain-of-thought
  Sekine. 2024. Analysis of llm’s “spurious” correct            in multi-hop reasoning with knowledge graphs. In
  answers using evidence information of multi-hop               Findings of the Association for Computational Lin-
  qa datasets. In Proceedings of the 1st Workshop               guistics: ACL 2024, pages 2862–2883.
  on Knowledge Graphs and Large Language Models
  (KaLLM 2024), pages 24–34.                                  OpenAI. 2026.          Introducing gpt-5.4 mini
                                                                and nano.           https://openai.com/index/
Alon Jacovi, Yonatan Bitton, Bernd Bohnet, Jonathan             introducing-gpt-5-4-mini-and-nano/.       Ac-
  Herzig, Or Honovich, Michael Tseng, Michael                   cessed: 2026-05-12.
  Collins, Roee Aharoni, and Mor Geva. 2024. A
  chain-of-thought is as strong as its weakest link: A        Qwen, :, An Yang, Baosong Yang, Beichen Zhang,
  benchmark for verifiers of reasoning chains. In Pro-         Binyuan Hui, Bo Zheng, Bowen Yu, Chengyuan
  ceedings of the 62nd Annual Meeting of the Associa-          Li, Dayiheng Liu, Fei Huang, Haoran Wei, Huan
  tion for Computational Linguistics (Volume 1: Long           Lin, Jian Yang, Jianhong Tu, Jianwei Zhang, Jianxin
  Papers), pages 4615–4634.                                    Yang, Jiaxi Yang, Jingren Zhou, and 25 oth-
                                                               ers. 2025. Qwen2.5 technical report. Preprint,
Bernal Jimenez Gutierrez, Yiheng Shu, Yu Gu, Michi-            arXiv:2412.15115.
  hiro Yasunaga, and Yu Su. 2024. Hipporag: Neu-
  robiologically inspired long-term memory for large          Stephen Robertson and Hugo Zaragoza. 2009. The prob-
  language models. Advances in Neural Information                abilistic relevance framework: BM25 and beyond,
  Processing Systems, 37:59532–59569.                            volume 4. Now Publishers Inc.


                                                         10
Noah Shinn, Federico Cassano, Ashwin Gopinath,                   Gao, Chengen Huang, Chenxu Lv, and 1 others.
  Karthik Narasimhan, and Shunyu Yao. 2023. Re-                  2025. Qwen3 technical report. arXiv preprint
  flexion: Language agents with verbal reinforcement             arXiv:2505.09388.
  learning. Advances in neural information processing
  systems, 36:8634–8652.                                       Zhilin Yang, Peng Qi, Saizheng Zhang, Yoshua Bengio,
                                                                 William Cohen, Ruslan Salakhutdinov, and Christo-
Gemma Team, Aishwarya Kamath, Johan Ferret, Shreya               pher D Manning. 2018. Hotpotqa: A dataset for
  Pathak, Nino Vieillard, Ramona Merhej, Sarah Perrin,           diverse, explainable multi-hop question answering.
  Tatiana Matejovicova, Alexandre Ramé, Morgane                  In Proceedings of the 2018 conference on empiri-
  Rivière, Louis Rouillard, Thomas Mesnard, Geoffrey             cal methods in natural language processing, pages
  Cideron, Jean bastien Grill, Sabela Ramos, Edouard             2369–2380.
  Yvinec, Michelle Casbon, Etienne Pot, Ivo Penchev,
  and 197 others. 2025. Gemma 3 technical report.              Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan
  Preprint, arXiv:2503.19786.                                    Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin,
                                                                 Zhuohan Li, Dacheng Li, Eric Xing, and 1 others.
Harsh Trivedi, Niranjan Balasubramanian, Tushar Khot,            2023. Judging llm-as-a-judge with mt-bench and
  and Ashish Sabharwal. 2022. Musique: Multi-                    chatbot arena. Advances in neural information pro-
  hop questions via single-hop question composition.             cessing systems, 36:46595–46623.
  Transactions of the Association for Computational
  Linguistics, 10:539–554.
Harsh Trivedi, Niranjan Balasubramanian, Tushar Khot,
  and Ashish Sabharwal. 2023. Interleaving retrieval
  with chain-of-thought reasoning for knowledge-
  intensive multi-step questions. In Proceedings of
  the 61st annual meeting of the association for com-
  putational linguistics (volume 1: long papers), pages
  10014–10037.
Miles Turpin, Julian Michael, Ethan Perez, and Samuel
  Bowman. 2023. Language models don’t always say
  what they think: Unfaithful explanations in chain-of-
  thought prompting. Advances in Neural Information
  Processing Systems, 36:74952–74965.
Gladys Tyen, Hassan Mansoor, Victor Cărbune,
  Yuanzhu Peter Chen, and Tony Mak. 2024. Llms
  cannot find reasoning errors, but can correct them
  given the error location. In Findings of the Associa-
  tion for Computational Linguistics: ACL 2024, pages
  13894–13908.
Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten
   Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou,
   and 1 others. 2022. Chain-of-thought prompting elic-
   its reasoning in large language models. Advances
   in neural information processing systems, 35:24824–
   24837.
Zhenyu Wu, Qingkai Zeng, Zhihan Zhang, Zhaoxuan
  Tan, Chao Shen, and Meng Jiang. 2025. Enhancing
  mathematical reasoning in llms by stepwise correc-
  tion. In Proceedings of the 63rd Annual Meeting of
  the Association for Computational Linguistics (Vol-
  ume 1: Long Papers), pages 21602–21623.
Anushka Yadav, Isha Nalawade, Srujana Pillarichety,
  Yashwanth Babu, Reshmi Ghosh, Samyadeep Basu,
  Wenlong Zhao, Ali Nasaeh, Sriram Balasubrama-
  nian, and Soundararajan Srinivasan. 2025. Hop, skip,
  and overthink: Diagnosing why reasoning models
  fumble during multi-hop analysis. arXiv preprint
  arXiv:2508.04699.
An Yang, Anfeng Li, Baosong Yang, Beichen Zhang,
  Binyuan Hui, Bo Zheng, Bowen Yu, Chang


                                                          11
A     Appendix                                                 A.2   Verifier Training Details
A.1    Overview                                                As described in Section 4.1, we fine-tune the veri-
                                                               fier using Parameter-Efficient Fine-Tuning (PEFT)
This appendix provides implementation details,
                                                               with QLoRA (Dettmers et al., 2023). We set
supplementary analyses, and qualitative examples
                                                               the LoRA rank to r = 64, the scaling factor to
that support the findings in the main text. The con-
                                                               α = 128, and the dropout rate to 0.05. LoRA is ap-
tents are organized as follows:
                                                               plied to all linear modules, including the attention
• Section A.2 provides implementation details for              projections (q, k, v, and o_proj) and the MLP lay-
  training the verifier, including hyperparameters,            ers (gate, up, and down_proj). For optimization,
  LoRA settings, decoding configurations, and                  we use the AdamW optimizer (Loshchilov and Hut-
  hardware specifications.                                     ter, 2017) with a cosine learning-rate scheduler and
                                                               a warmup ratio of 0.03.
• Section A.3 presents qualitative examples from
  our KG-grounded benchmark verification, includ-              A.3   KG-Grounded Benchmark Verification:
  ing false positives and unverifiable benchmark                     Examples
  instances flagged by the pipeline (see Table 10,
  Table 11, and Figure 2).                                     False Positive Examples. Table 10 presents qual-
                                                               itative examples of false positives from our KG-
• Section A.4 describes the preprocessing and sam-             grounded benchmark verification pipeline. Here, a
  pling procedure for constructing the verified eval-          false positive refers to a valid multi-hop query that
  uation pool used in our multi-hop QA experi-                 the pipeline incorrectly flags as unverifiable.
  ments.                                                          As illustrated by the three representative cases,
                                                               the provided gold passages contain the necessary
• Section A.5 provides details of the verifier train-
                                                               evidence to complete the intended reasoning paths.
  ing data, including examples, error-step positions,
                                                               For example, the queries require comparing direc-
  and dataset statistics (see Figure 5, Figure 6, and
                                                               tors’ ages, matching a specific birth date to a TV
  Table 12).
                                                               show judge, or tracing a newspaper’s sponsorship
• Section A.6 presents qualitative case studies com-           to its base city. In these cases, the textual evidence
  paring SAFE with the self-verification baseline.             is clear, self-contained, and sufficient to support an
  These examples illustrate how the external ver-              unambiguous answer.
  ifier handles common multi-hop failure modes,                   These examples show that misclassifications can
  including lexical distractors, premature attribu-            occur even for standard, well-structured reasoning
  tion, and self-verification collapse (see Table 14,          paths. They are not limited to unusually complex
  Table 15, and Table 16).                                     or poorly phrased queries. This observation is im-
                                                               portant because it suggests that our verification
• Section A.7 reports an ablation study on targeted
                                                               pipeline does not simply remove difficult examples
  refinement, comparing a verifier trained only on
                                                               or penalize complex reasoning structures. The veri-
  synthetic errors with the final verifier trained with
                                                               fied set therefore preserves challenging multi-hop
  additional hard cases (see Table 17).
                                                               reasoning instances while removing cases that are
• Section A.8 provides detailed efficiency and                 not verifiable under our evidence-grounding proto-
  failure-pattern analyses, including the cost-                col.
  accuracy comparison between SAFE and self-
                                                               Unverifiable Benchmark Examples. In contrast
  verification, the sensitivity of performance and
                                                               to the false positives above, Table 11 and Fig-
  cost to the maximum reasoning steps K and retry
                                                               ure 2 illustrate benchmark instances that are gen-
  limit N , the use of Prefix KV caching, and the
                                                               uinely unverifiable under our KG-grounded pro-
  distributions of detected error types and error
                                                               tocol. These examples highlight why train-time
  positions.
                                                               benchmark verification is necessary for construct-
• Section A.9 lists the prompts used throughout our            ing reliable verifier supervision and evaluation data.
  pipeline, including reasoning generation, step-                 First, some instances contain insufficient context,
  wise verification, diagnostic error injection, and           as shown in Table 11 and at the bottom of Figure 2.
  KG-grounded benchmark verification (see Fig-                 In these cases, the provided gold passages lack the
  ure 15–23).                                                  evidence needed to complete the reasoning path.

                                                          12
Category                Error Type               Definition

                                                Engaging in excessive extraction or derivation steps even after
                        Overthinking†
Procedural                                      the target node (eans ) has been reached.
(Attribution &                                  Generating textual steps that do not correspond to any valid
                        Inefficiency†
Logical Steps)                                  KG operation (i.e., no node or edge traversal).
                                                Extracting entities or traversing paths that form a disconnected
                        Off-topic†
                                                subgraph, not contributing to the target path.
                                                Repeating the extraction of a node e or traversal of an edge
                        Redundancy†
                                                (ea , r, eb ) already documented in previous steps.

                                                 Incorporating an entity e or relationship r that is completely
                        Unsupported
                                                 absent from the evidence subgraph G.
Attribution
                                                 Attempting to connect a valid entity en to em while bypassing
(Attribution Steps)     Premature Attribution
                                                 the necessary intermediate edge (em , r, en ).
                                                 Overlooking a necessary node e that is explicitly present and
                        Information Miss
                                                 available within G.
                                                 Generating a node or edge relation that directly conflicts with
                        Contradictory
                                                 explicit facts within G.

Logical                                          Inferring a new relation rinf erred that cannot be logically
                        Logical Fallacy
(Logical Steps)                                  proven via established KG traversal rules over extracted paths.

Final Answer                                     Producing a target eans that is missing from the reasoning
                        Wrong Conclusion
(Final Answer Steps)                             path or fails to logically terminate the grounded sequence.

Table 9: Feedback categories used by SAFE for stepwise verification. Each invalid reasoning step is assigned one
mutually exclusive error type, which determines the feedback provided for correction. Procedural errors marked
with † are checked first because they concern the structure and progress of the reasoning path before evidence
attribution and logical consistency are assessed.

For example, a passage may specify a composer’s              A.4   Evaluation Dataset Preprocessing Details
year of death but omit the location required by the
                                                             For evaluation, we use a constrained distractor set-
question.
                                                             ting with exactly 10 passages per question across
                                                             all benchmarks. For 2WikiMultihopQA and Hot-
   Other instances suffer from entity confusion. Ta-         potQA, we use the 10 passages provided in their
ble 11 shows a case where two distinct historical            standard distractor settings. For MuSiQue, which
figures, Lorenzo Costa the Elder and Lorenzo Costa           originally provides 20 passages per instance, we
the Younger, are conflated to form an invalid rea-           retain all gold supporting passages and randomly
soning path. Some examples also contain incor-               sample the remaining passages from the distractor
rect ground-truth labels that contradict the provided        set to satisfy the 10-passage constraint. Finally, we
text, such as identifying a director’s nationality as        randomly shuffle the passage order for every in-
Lebanese when the gold passage states that she is            stance in all three datasets to prevent models from
Palestinian, as shown at the top of Figure 2. In             exploiting positional shortcuts.
addition, the middle example in Figure 2 shows
an ambiguous query that does not support a single            A.5   Verifier Training Dataset
definitive answer.                                           This section describes the structure, composition,
                                                             and statistical distribution of the dataset used to
  By removing insufficient, contradictory, and am-           train our stepwise verifier.
biguous instances from the verified set, our pipeline           Figure 5 illustrates a representative training in-
ensures that models are evaluated on evidence-               stance. Unlike post-hoc evaluation datasets, our
grounded multi-hop reasoning rather than on guess-           training data is structured to support step-level ver-
ing, hallucination, or parametric memorization.              ification during generation. Each instance provides

                                                        13
Figure 1: Overview of our KG-grounded benchmark verification pipeline. The example shows an unverifiable
reasoning path, where the fact is supported by a passage about North Carolina’s Piedmont rather than Virginia’s
Piedmont. Our pipeline detects such evidence-grounding gaps and removes the instance from the verified set.


the verifier with the question, the provided pas-            near the final answer. As shown in the figure, the
sages, the previous reasoning steps, and the current         training data covers errors across different reason-
step to be evaluated. The target output follows the          ing positions. This distribution helps the verifier
verifier response format used in SAFE: an Error              learn to diagnose and correct failures throughout
Type, a natural language Diagnosis, and actionable           the generation process.
Guidance. Together, these fields teach the verifier
not only to detect unsupported reasoning steps, but          A.6   Qualitative Case Studies
also to explain the violation and guide the generator        In this section, we provide qualitative case studies
toward a valid correction.                                   comparing SAFE with the self-verification baseline.
   Table 12 reports the statistics of the constructed        These examples illustrate how an external stepwise
training dataset across 2WikiMultihopQA, Hot-                verifier can detect unsupported reasoning steps, pro-
potQA, and MuSiQue. The dataset contains 11.5k               vide diagnostic and actionable guidance, and help
step-level verification instances derived from 5k            the generator remain grounded in the provided pas-
unique questions. Because SAFE verifies reason-              sages during generation.
ing iteratively, a single question can yield multi-             Table 14 shows a case involving lexical distrac-
ple training instances corresponding to different            tors. The self-verification baseline is misled by
reasoning prefixes and current steps. This one-to-           lexical overlap with the term “Eden” in Passage
many structure exposes the verifier to diverse valid         1. However, the relevant entity in the question is
and invalid steps within multi-hop reasoning trajec-         “Lake Eden,” which is supported by different evi-
tories.                                                      dence in Passage 10. SAFE identifies this mismatch
   Finally, Figure 6 shows the positional distribu-          and guides the generator away from the incorrect
tion of error steps across reasoning trajectories. A         entity. By distinguishing the hamlet “Eden” from
stepwise verifier should be able to detect unsup-            the target entity “Lake Eden,” SAFE keeps the rea-
ported reasoning regardless of where it occurs in            soning process grounded in the correct evidence.
the trajectory, rather than only at the beginning or            Table 15 illustrates a structural reasoning fail-

                                                        14
Question                            Gold Passages (Truncated)                      Answer              Reasoning Analysis
Which film has the director who     [1] Koeputkiaikuinen... directed, written      Koeputkiaikuinen The passages provide all nec-
is older, Koeputkiaikuinen Ja Si-   and starring Spede Pasanen...                  Ja Simon Enke- essary components for the
mon Enkelit or Indiana Jones        [2] Indiana Jones and the Temple of            lit              multi-hop chain: (1) identifies
And The Temple Of Doom?             Doom... directed by Steven Spielberg...                         Pasanen and Spielberg as re-
                                    [3] Spede Pasanen (10 April 1930 – 7                            spective directors, and (2) pro-
                                    Sept 2001) was a Finnish film director...                       vides their birth years (1930
                                    [4] Steven Spielberg (born December 18,                         vs. 1946), enabling a correct
                                    1946) is an American filmmaker...                               age comparison.
What judge who was on the           [1] Paul Joseph Mercurio (born 31              Paul Joseph Mer-    The passages provides a clear
show “Dancing with the Stars”       March 1963) is an Australian actor,            curio               multi-hop chain: (1) identifies
was born on the 31st of March,      dancer, and TV presenter...                                        the specific birth date for Paul
1963?                               [2] ...with the exception of Paul Mercu-                           Joseph Mercurio, and (2) con-
                                    rio who wanted to focus more on the                                firms his role as a judge on the
                                    Australian version of “Dancing with the                            mentioned TV show, allowing
                                    Stars”.                                                            for an unambiguous match.
Beena Sarwar is the editor of a     [1] Beena Sarwar is the Pakistan Editor        Karachi,    Pak-    The passages provide a com-
peace initiative sponsored by a     of the Aman ki Asha initiative... jointly      istan               plete, self-contained chain:
newspaper based in what city?       sponsored by the Jang group...                                     (1) connects Beena Sarwar to
                                    [2] The Daily Jang is an Urdu newspa-                              the Aman ki Asha initiative,
                                    per based in Karachi, Pakistan.                                    (2) identifies Jang group as
                                                                                                       the sponsor, and (3) explicitly
                                                                                                       states the newspaper’s base
                                                                                                       city as Karachi.

Table 10: False positive examples from our KG-grounded benchmark verification pipeline. These valid instances are
incorrectly flagged as unverifiable, showing that misclassifications can occur on standard, well-structured reasoning
paths rather than only on unusually complex queries. This suggests that the pipeline does not simply remove
examples based on reasoning difficulty.




Question                            Gold Passages (Truncated)                        Answer           Error Description
Where was the place of death of     [1] ...The score was composed by Erich           Hollywood        Missing Evidence: The pas-
the composer of film The Private    Wolfgang Korngold...                                              sages state that the composer
Lives Of Elizabeth And Essex?       [2] ...Although his late classical Romantic                       (Korngold) died in 1957, but
                                    compositions were no longer as popular                            explicitly lack information re-
                                    when he died in 1957...                                           garding his place of death.
Where did the creator of the Al-    [1] The Allegory... is a painting by the         Mantua           Entity Disambiguation Fail-
legory of Isabella d’Este’s Coro-   Italian Renaissance painter Lorenzo Costa                         ure: The dataset incorrectly
nation die?                         the Elder...                                                      matches “Lorenzo Costa the
                                    [2] Lorenzo Costa the Younger                                     Elder” (the creator) with his
                                    (1537–1583) was an Italian painter...                             grandson “Lorenzo Costa the
                                    active in his native city of Mantua.                              Younger,” conflating two dis-
                                                                                                      tinct entities.
What movie did Lauren Bacall’s      [1] Humphrey Bogart... received three            The African      External Knowledge Re-
spouse win his only Oscar?          Academy Award nominations for Best Ac-           Queen            quirement: The passages
                                    tor, winning one (for The African Queen).                         establish that Bogart and Ba-
                                    [2] Bold Venture was a syndicated radio                           call co-starred in a radio series,
                                    series starring Humphrey Bogart and Lau-                          but omit their marital status.
                                    ren Bacall...                                                     Answering requires parametric
                                                                                                      external knowledge.
What nationality is the director    [1] 3000 Nights is a 2015 drama film di-         Lebanon          Wrong Answer: The pas-
of film 3000 Nights?                rected by Mai Masri...                                            sages explicitly identify the
                                    [2] Mai Masri... is a Palestinian filmmaker,                      director as “Palestinian,” yet
                                    director and producer.                                            the ground-truth answer is
                                                                                                      “Lebanon,” which contradicts
                                                                                                      the provided context.

Table 11: Representative examples of benchmark instances flagged as unverifiable by our KG-grounded benchmark
verification pipeline. These cases include evidence-grounding failures, such as missing necessary information in the
gold passages or ground-truth answers that contradict the provided evidence.


                                                               15
                                                                  Figure 4: Distribution of diagnostic error categories in
Figure 2: Representative benchmark instances flagged              the verifier training set. The inner ring shows broad
as unverifiable by our KG-grounded benchmark verifica-            categories, while the outer ring shows specific error
tion pipeline. The examples show an incorrect ground-             types, illustrating coverage of diverse failure modes
truth answer that contradicts the provided evidence (top),        used for stepwise verification.
an ambiguous question without a unique answer (mid-
dle), and insufficient context where the gold passages
                                                                   Dataset       Step-Level Instances    Unique Questions
do not support a complete evidence-grounded reasoning
path (bottom).                                                     2Wiki                 5,476                  2,292
                                                                   HotpotQA              3,063                  1,330
                                                                   MuSiQue               2,976                  1,438
                                                                   Total                11,515                  5,060

                                                                  Table 12: Statistics of the verifier training dataset. Step-
                                                                  level instances correspond to individual verifier inputs
                                                                  constructed from reasoning prefixes and current steps.
                                                                  Because SAFE verifies reasoning iteratively, a single
                                                                  question can produce multiple step-level training in-
                                                                  stances.


                                                                  of implicit assumptions and causes the model to
                                                                  lose track of the question’s main constraint, which
                                                                  is to identify a film title. As a result, the model
                                                                  outputs the director’s name instead, even though
                                                                  the relevant passages are available.
                                                                     In contrast, SAFE detects the missing link at the
Figure 3: Diagram of SAFE at inference-time. The Gen-
                                                                  first step and provides guidance for revising the rea-
erator produces or refines an atomic reasoning step,
while the Verifier detects errors and provides feedback.          soning path. By correcting this early unsupported
This step-level feedback loop continues until the reason-         step, SAFE helps ensure that later steps are built on
ing terminates.                                                   evidence-grounded reasoning. In the final stage,
                                                                  the verifier also provides guidance that the answer
                                                                  should be a film title, keeping the reasoning process
ure caused by premature attribution. In this exam-                aligned with the question requirement.
ple, the self-verification baseline jumps directly to                Finally, Table 16 shows a case where self-
extracting a death date without first establishing                verification leads to a broader reasoning breakdown.
the required link between the film and the direc-                 The baseline exhibits target drift: instead of main-
tor. This early unsupported step leads to a chain                 taining focus on the entity requested by the ques-

                                                             16
  Example Training Data                                           ter failing to find the population of Phoenix in the
  Question: Are director of film The Raft of the Dead and         provided passages, the self-verifier further instructs
  director of film The World Gone Mad both from the same          the generator to rely on external sources. This
  country?
                                                                  example shows that self-verification can amplify
  Passages:                                                       errors when the evaluator itself is not grounded in
  Passage 1: The World Gone Mad ... is a 1933 American            the provided evidence. By separating generation
  ... directed by Christy Cabanne ...
  Passage 5: Carl Boese ... was a German film director ...        from verification, SAFE reduces this failure mode
  Passage 8: Christy Cabanne ... was an American film             and keeps correction guidance tied to the available
  director ...                                                    context.
  Passage 9: The Raft of the Dead ... directed by Carl
  Boese ...
                                                                  A.7   Ablation: Synthetic-Only vs. Refined
  Previous Reasoning Steps:                                             Verifier Training
  Step 1: Passage 9 states the director of The Raft of the
  Dead is Carl Boese.                                             To evaluate the effect of targeted refinement in
  Step 2: Passage 5 reveals the country of origin of Carl         verifier training, we compare two variants: a ver-
  Boese is Germany.
  Step 3: Passage 1 reveals the director of The World
                                                                  ifier trained only on synthetic error-injected ex-
  Gone Mad is Christy Cabanne.                                    amples (“Synthetic Only”) and the final verifier
  Step 4: The country of origin of Christy Cabanne (from          trained with additional hard cases collected through
  Step 3) is America, based on Passage 8.
                                                                  our analysis-driven refinement strategy (“Refined”).
  Current Step:                                                   Table 17 reports the results across generator models
  Step 5: As previously established in Step 2, Carl Boese         with different architectures and sizes.
  is indeed from Germany.
                                                                     Overall, adding refined training examples consis-
  Verifier Output:                                                tently improves performance, yielding an average
  Error Type: Redundancy                                          gain of +2.9 pp across all evaluated models. The
  Diagnosis: The step repeats the previously established
  fact from Step 2 without adding any new inference or            largest gains appear on MuSiQue, the most chal-
  moving closer to the final answer.                              lenging benchmark in our evaluation, where the
  Guidance: Compare the countries of origin established
  in Step 2 (Germany) and Step 4 (America) to determine
                                                                  average improvement reaches +4.2 pp. This sug-
  if they are the same.                                           gests that synthetic error injection provides broad
                                                                  coverage of diagnostic categories, while targeted re-
Figure 5: Example verifier training instance. The veri-           finement captures more complex reasoning failures
fier receives the question, provided passages, previous
                                                                  that arise during actual inference.
reasoning steps, and the current step, then outputs an er-
ror type, diagnosis, and corrective guidance. For brevity,           At the model level, the improvement is most
distractor passages are omitted from the original 10-             pronounced for Llama-3.1-8B, which gains +6.1 pp
passage context, and step-type tags are removed.                  on average and +8.6 pp on MuSiQue. The refined
                                                                  data also improves Gemma-3-12B by +3.0 pp on
                                                                  average. The gains are smaller for Qwen2.5-14B,
                                                                  with a +0.4 pp average improvement, and Qwen3-
                                                                  4B shows a slight regression on HotpotQA of -
                                                                  0.2 pp. Despite these small variations, the overall
                                                                  trend shows that targeted refinement improves the
                                                                  verifier’s ability to handle diverse inference-time
                                                                  failure modes.
                                                                     This ablation shows that synthetic error injection
                                                                  alone is not sufficient for training the final veri-
                                                                  fier. Adding refinement examples helps the verifier
                                                                  generalize beyond controlled synthetic errors and
Figure 6: Positional distribution of error steps in the
verifier training data. Errors appear across different            better support step-level correction during genera-
reasoning stages, providing supervision for detecting             tion.
unsupported steps at multiple points during generation.
                                                                  A.8   Efficiency and Failure Patterns
                                                                  SAFE vs. Self-Verification. Figure 7 compares
tion, the second largest city Tucson, it shifts the               the cost-accuracy trade-off between SAFE and the
generator toward an irrelevant target, Phoenix. Af-               self-verification baseline under different retry bud-

                                                             17
 Component      Total    Cached    Computed     Savings           Cost-Accuracy Trade-off of SAFE. To further an-
 Generator      43.8M     32.9M      10.9M       75.2%            alyze the cost-performance trade-off of inference-
 Evaluator     100.4M     95.4M       5.0M       95.0%            time verification, we vary the maximum number
 Overall       144.2M    128.3M      15.9M      89.0%             of reasoning steps K and the maximum number
                                                                  of retry attempts N . As shown in Figure 8, ac-
Table 13: Inference cost measured in total and cached             curacy generally improves when the generator is
tokens. In SAFE, prefix KV caching eliminates 89.0%               given more steps and retry opportunities, since the
of redundant computations, and the marginal increase
                                                                  verifier has more chances to detect unsupported
remains practically negligible.
                                                                  steps and guide corrections. However, performance
                                                                  begins to plateau as the retry budget increases. In-
                                                                  creasing N beyond 3 yields only marginal gains
                                                                  and can sometimes slightly degrade performance.
                                                                     The highest accuracy, 84.71%, is achieved with
                                                                  K = 13 and N = 3, but this setting requires ad-
                                                                  ditional computation. We therefore use K = 10
                                                                  and N = 3 as the default configuration, which
                                                                  achieves a similar accuracy of 84.40% with a lower
                                                                  reasoning budget. This setting provides a practi-
                                                                  cal balance between verification cost and answer
                                                                  accuracy.
Figure 7: Cost-accuracy comparison between SAFE
and the Self-Verification baseline. We evaluate the in-           Prefix KV Caching. A key concern with iterative
ference efficiency across different max_steps (K ∈                inference-time verification is the additional compu-
{7, 10, 13}) and max_retries (N ∈ {1..5}). While the              tational cost introduced by repeated generation and
Self-Verification exhibits a severe cost explosion without
                                                                  verification. In multi-hop QA, much of this cost
meaningful accuracy improvements, SAFE achieves su-
perior accuracy with minimal computational overhead.              comes from the prefill stage, where the model pro-
                                                                  cesses the system instruction, provided passages,
                                                                  question, and previous reasoning context.
                                                                     As shown in Table 13, SAFE mitigates this over-
                                                                  head through Prefix KV caching (Kwon et al.,
                                                                  2023). Both the reasoning generator and the step-
                                                                  wise verifier independently cache the representa-
                                                                  tions of static prefixes, such as the instruction, pas-
                                                                  sages, and question. As generation proceeds, ver-
                                                                  ified reasoning steps are appended to the cached
                                                                  context. Thus, later reasoning and verification calls
                                                                  mainly require computation for newly generated
                                                                  tokens rather than reprocessing the entire prefix.
Figure 8: Cost-accuracy trade-off of SAFE. Annota-                   Across 3,000 evaluation examples from the three
tions indicate the (K, N ) configuration, where K is
                                                                  benchmarks, Prefix KV caching reduces redun-
max_steps and N is max_retries.
                                                                  dant prefill token processing by 89.0%. This result
                                                                  shows that SAFE can support iterative stepwise ver-
gets. As the retry limit increases, self-verification             ification with substantially reduced computational
requires substantially more LLM calls but does not                overhead.
achieve comparable accuracy gains. This occurs                    Failure Type Distribution. We also analyze the
because the generator often fails to identify its own             failures detected by the verifier. Figure 9 shows
unsupported step and may repeatedly revise along                  that Procedural errors, such as redundancy and off-
an invalid trajectory. In contrast, SAFE reaches over             topic reasoning, account for 64.1% of detected fail-
84% average accuracy with fewer than 15 calls                     ures. This indicates that many multi-hop reasoning
on average. This suggests that external stepwise                  failures are not simply caused by missing factual
verification is more efficient than unguided self-                knowledge, but by invalid reasoning structure. This
correction for evidence-grounded multi-hop QA.                    finding further supports the need for a verifier that

                                                             18
 Question            Are both Missisa Lake and Lake Eden located in the same country?
 Passages            [1] Eden is a CDP in Erie County, New York, United States. (Distractor)
                     [6] Missisa Lake is a lake in Ontario, Canada.
                     [10] Lake Eden is a small, recreational lake in Alberta, Canada.
 Reasoning Step      Step 1: According to Passage 1, Lake Eden is located in New York.

 Self-Verification   error_type: Correct (No Error)
                     diagnosis: The step correctly extracts the location of Lake Eden from Passage 1.
                     guidance: Find the location of Missisa Lake from the provided passages.
 Ours                error_type: Contradictory
                     diagnosis: The step misreads Passage 10 by claiming Lake Eden is in New York, whereas Passage 10
                     explicitly states that Lake Eden is in Alberta, Canada. This directly contradicts the retrieved passage.
                     guidance: Correct the attribution by stating that Lake Eden is located in Alberta, Canada, based on
                     Passage 10.

Table 14: Qualitative comparison between self-verification and SAFE. The self-verification baseline is misled by
lexical overlap with the distractor term “Eden” in Passage 1 and fails to distinguish it from the target entity “Lake
Eden.” In contrast, SAFE detects the entity mismatch and provides evidence-grounded corrective guidance.




                                                                  Figure 10: Distribution of detected errors across reason-
                                                                  ing steps. A large fraction of failures occurs within the
Figure 9: Distribution of error types detected by SAFE.           first three steps (59.0%), supporting the use of inference-
Procedural errors, such as Redundancy and Off-topic,              time verification to detect and correct unsupported steps
account for the majority of failures (64.1%), suggesting          before they propagate.
that many errors arise from invalid reasoning structure
rather than missing factual knowledge.
                                                                  uses evidence-grounded diagnosis with actionable
                                                                  guidance, allowing the generator to revise unsup-
checks not only factual attribution, but also the                 ported steps before continuing.
structure and progress of the reasoning path.
                                                                  A.9    Prompts
Error Position Distribution. Figure 10 shows
that 59.0% of detected errors occur within the first              This section provides the prompt templates used
three reasoning steps. This early concentration                   throughout SAFE to support transparency and re-
helps explain why inference-time verification is                  producibility. For clarity, we group the prompts
useful. Unsupported early steps can shape the rest                according to their roles in the framework:
of the reasoning trajectory, so correcting them be-
fore generation continues helps reduce downstream                 • Inference-Time Verification and Answer Eval-
error propagation.                                                  uation: This group includes prompts for step-by-
                                                                    step reasoning generation (Figure 11), inference-
Qualitative Failure Modes. Qualitative exam-                        time step verification and corrective guidance
ples in Appendix A.6 further illustrate the limita-                 (Figure 12), and final answer extraction (Fig-
tions of self-verification. Self-verification often                 ure 13). It also includes the LLM-as-judge
fails due to lexical overlap bias, unsupported logi-                prompt used to evaluate semantic equivalence
cal jumps, and evaluator hallucination. In contrast,                between the predicted answer and the ground-
SAFE separates generation from verification and                     truth answer (Figure 14).

                                                             19
 Question: Which film has the director who died earlier, Un’Estate Ai Caraibi or Her Honor, The Governor?
 Passages (Truncated):
 [2] Chester “Chet” Withey... died 6 October 1939.
 [4] Her Honor, the Governor is a 1926... film starring Pauline Frederick, directed by Chester Withey...
 [5] Carlo Vanzina (13 March 1951 – 8 July 2018) was an Italian film director, producer and screenwriter...
 [7] Un’estate ai Caraibi is a 2009 Italian comedy film directed by Carlo Vanzina...

                      Self-Verification                                                       Ours
 Step 1: According to Passage 2, Chester “Chet” Withey died        Step 1: According to Passage 2, Chester “Chet” Withey died
 on Oct 6, 1939.                                                   on Oct 6, 1939.
 error_type: Correct (No Error)                                    error_type: Premature Attribution
 diagnosis: The step correctly extracts the death date of          diagnosis: Missing the preceding step to identify that Withey
 Chester Withey.                                                   is the director of “Her Honor, The Governor”.
 guidance: Find the death date of Carlo Vanzina.                   guidance: First, explicitly identify the director of “Her
                                                                   Honor, The Governor” based on Passage 4.

 Step 2: According to Passage 5, Carlo Vanzina died on July        Step 1 (Retry):
 8, 2018. (Accepted)                                               According to Passage 4, Chester Withey directed “Her Honor,
 Step 3: Comparing the death date of Chester Withey (Oc-           The Governor”. (Accepted)
 tober 6, 1939) with the death date of Carlo Vanzina (July 8,      Step 2-4: Identifies Vanzina as director, then collects death
 2018), Chester Withey died earlier. (Accepted)                    dates for both directors. (Accepted)
 Step 4: ####ANSWER: Chester Withey                                Step 5: Compares death dates of two directors.
 Analysis: Because the feedback model did not enforce the Step 6: ####ANSWER: Her Honor, The Governor
 director-to-film connection in Step 1, the generator lost track Analysis: The verifier’s guidance explicitly instructed:
 of the final goal (finding the film title) and mistakenly output
                                                                  “State which film has the director who died earlier... using
 the director’s name instead.                                      format ####ANSWER: <film_title>.”. This ensured task com-
                                                                   pliance and correct entity type.

Table 15: Detailed trace comparison between self-verification and SAFE. Self-verification loses entity consistency
through premature attribution, whereas SAFE detects the missing link and provides stepwise corrective guidance to
keep the reasoning path evidence-grounded and aligned with the required answer type.


• Verifier Training Data Construction: This
  group contains prompts for dataset-specific query
  decomposition and reasoning planning for 2Wiki-
  MultihopQA (Figure 15), HotpotQA (Figure 16),
  and MuSiQue (Figure 17). It also includes
  prompts for generating evidence-grounded rea-
  soning trajectories (Figure 18) and creating nega-
  tive examples through diagnostic error injection
  (Figure 19).

• KG-Grounded Benchmark Verification: This
  group details the prompts used in our KG-
  grounded verification pipeline to identify un-
  verifiable benchmark supervision. The prompts
  cover triple extraction (Figures 20 and 21), en-
  tity resolution for synonymous or coreferential
  mentions (Figure 22), and reasoning path discov-
  ery for checking whether the question entities
  can be connected to the answer through evidence-
  supported triples (Figure 23).




                                                              20
 Question: In 1900, what was the population of the second largest city in the state where the Oh Yeah performer is from?
 Passages (Truncated):
 [2] Tucson is the largest city in southern Arizona, the second largest in the state after Phoenix.
 [6] By 1900, 7,531 people lived in the city Tucson.
 [9] Oh Yeah is a 1962 album by jazz musician Charles Mingus.
 [10] Charles Mingus was born in Nogales, Arizona.
 Ground Truth Answer: 7531

 Self-Verification Reasoning Trace (Summarized)
 Step 4: According to Passage 2, Phoenix is the second largest city in Arizona after Tucson.
 error_type: Off-topic
 diagnosis: The question asks for the population of the *second largest* city... While this step correctly identifies Phoenix as
 the second largest city in Arizona, it doesn’t address the core requirement of finding the population in 1900.
 guidance: Find the population of Phoenix in 1900 from the passages.
 Step 9: According to Passage 2, Phoenix is the largest city in Arizona, but it does not state the population of Phoenix in 1900.
 error_type: Redundancy
 diagnosis: This step simply reiterates information already established in Step 8.
 guidance: Find the population of Phoenix in 1900 from external sources.
 Step 10: According to the United States Census Bureau, the population of Phoenix, Arizona in 1900 was 10611.
 Predicted Answer: 10611

Table 16: Detailed trace of reasoning collapse in the self-verification baseline. The self-verifier shifts the target
from the requested entity, Tucson, to an irrelevant entity, Phoenix, and then instructs the generator to use external
knowledge when the required evidence is not found in the provided passages. This example illustrates how self-
verification can amplify unsupported reasoning when the evaluator is not grounded in the evidence.




    Model                   Verifier Training             2Wiki          HotpotQA            MuSiQue            Average
                            Synthetic Only                88.6              89.4               71.6               83.2
    Gemma-3-12B
                            + Refined                  91.8 (+3.2)       90.0 (+0.6)        76.7 (+5.1)        86.2 (+3.0)
                            Synthetic Only                90.2              89.7               75.7               85.2
    Qwen2.5-14B
                            + Refined                  90.2 (+0.0)       90.1 (+0.4)        76.6 (+0.9)        85.6 (+0.4)
                            Synthetic Only                86.5              84.8               66.7               79.3
    Llama-3.1-8B
                            + Refined                  90.7 (+4.2)       90.3 (+5.5)        75.3 (+8.6)        85.4 (+6.1)
                            Synthetic Only                88.6              88.6               70.9               82.7
    Qwen3-8B
                            + Refined                  91.3 (+2.7)       90.9 (+2.3)        76.6 (+5.7)        86.3 (+3.6)
                            Synthetic Only                87.3               89.2              73.5               83.3
    Qwen3-4B
                            + Refined                  89.4 (+2.1)         89.0 (-0.2)      74.5 (+1.0)        84.3 (+1.0)

                            Synthetic Only                88.2              88.3               71.7               82.7
    Average
                            + Refined                  90.7 (+2.5)       90.1 (+1.8)        75.9 (+4.2)        85.6 (+2.9)

Table 17: Ablation of targeted refinement for verifier training. “Synthetic Only” uses only diagnostic error-injected
examples, while “+ Refined” adds hard cases collected through analysis-driven targeted refinement. Values in
parentheses indicate absolute changes relative to Synthetic Only.




                                                               21
Reasoning Step Generation Prompt
You are a meticulous, step-by-step logical reasoner. Your task is to solve a complex question by generating **ONLY
THE NEXT SINGLE, ATOMIC STEP** in a chain of thought.

## Core Task Definition
You must analyze the ‘Question‘, ‘Retrieved Passages‘, and ‘Previous Reasoning Steps‘. Most importantly, you must
analyze the ‘Feedback‘ received on the last step, which consists of three parts:
1. **Error Type**: The category of the error.
2. **Diagnosis**: An explanation about the latest previous step.
3. **Guidance**: Specific instruction on what to do in this current step. (e.g. Fixing previous step’s error, Proceeding to
extract new information, or Making the final logical conclusion).
You must prioritize the **Guidance**. It tells you exactly what action to take now.
—
## Step Classifications
Every step must be strictly classified into one of three types. Attribution and Logical actions cannot be mixed in a single
step.

### 1. Attribution Step
- **Definition**: Extracts **ONE** explicit fact from a **SINGLE** retrieved passage.
- **Requirement**: You MUST explicitly cite the source (e.g., "According to Passage X...").
- **Constraint**: Do **NOT** combine information from multiple passages (e.g., "Passage 1 says X and Passage 2
says Y").
- **Format suffix**: End the sentence with ‘(Attribution)‘.

### 2. Logical Step - **Definition**: Performs **ONE** logical operation (comparison, calculation, or inference)
based **ONLY** on ‘Previous Reasoning Steps‘.
- **Requirement**: Do NOT look up new information from passages.
- **Constraint**: This step is for **Intermediate Reasoning** only.
- You must NOT output the final answer marker here.
- Even if you derived the answer mentally, just state the conclusion of the logic (e.g., "A is older than B").
- **Format suffix**: End the sentence with ‘(Logical)‘.

### 3. Final Answer Step
- **Definition**: Submits the final answer.
- **Strict Syntax Rule**: This step must ONLY generate the final answer following the format: ‘####ANSWER:
<answer_value>‘.
- **Constraint**: Do not write "Therefore...", or "The answer is...". Just the marker and value.
- **Format suffix**: End with ‘(Final Answer)‘.
—
## Strict Formatting Rules
1. **Numbering**: Start your response with ‘Step K:‘, where ‘K‘ is the next integer after the last step number.
2. **Atomic Nature**: Adhere strictly to the "One Step = One Action" rule defined above.
3. **Suffix Mandatory**: Every step must end with one of ‘(Attribution)‘, ‘(Logical)‘, ‘(Final Answer)‘.
4. **Final Answer Pattern**: The pattern for the final step is immutable: ‘Step K: ####ANSWER: <answer_value>
(Final Answer)‘
—
## Examples of Valid Atomic Steps
[EXAMPLES...]

**FOR THE FINAL ANSWER STEP, YOU MUST USE EXACT FOLLOWING FORMAT:**
Step X: ####ANSWER: your_answer_here (Final Answer)



                                   Figure 11: Reasoning step generation prompt.




                                                            22
Reasoning Step Evaluation Prompt 1
# Role
You are a Precision Reasoning Evaluator. Your goal is to critically assess a specific reasoning step (Step to evaluate)
within the context of a multi-hop QA task. You must verify if the step is logically sound, factually grounded in the
provided ‘Retrieved Passages‘, and efficiently moves towards the answer.

# Input Data Context
- **Question**: The main query to answer.
- **Retrieved Passages**: The only source of truth. External knowledge is strictly forbidden.
- **Previous Steps**: The chain of thought leading up to the Step to evaluate.
- **Step to evaluate**: The specific step you need to evaluate. It must end with one of these tags:
- ‘(Attribution)‘: Extracting facts directly from a passage.
- ‘(Logical)‘: Intermediate reasoning (comparing, calculating) without the final answer marker.
- ‘(Final Answer)‘: Strict submission of the final answer ONLY (Format: ‘####ANSWER: <answer_value>‘).

# Task
1. Compare the ‘Step to evaluate‘ against the ‘Retrieved Passages‘ and ‘Previous Steps‘.
2. Choose one ‘error_type‘ from the given categories based on the Evaluation Protocol.
3. Generate a structured evaluation with ‘diagnosis‘ and ‘guidance‘.

# Feedback Guidelines
You must follow this Evaluation Protocol sequentially to determine the ‘error_type‘.

 ## Phase 1: Assess (Final Answer) Steps
**Condition**: If the ‘Step to evaluate‘ is tagged as ‘(Final Answer)‘.
- **Check 1 (Consistency)**: Does the submitted answer value match the conclusion derived from the preceding steps?
- If NO -> error_type: Wrong Conclusion
- **Check 2 (Correctness)**: Are sufficiency and consistency met?
- If YES -> error_type: Correct (No Error)

 ## Phase 2: Assess Utility & Progress (For Attribution/Logical Steps)
**Condition**: If the ‘Step to evaluate‘ is ‘(Attribution)‘ or ‘(Logical)‘.
- **Check 1 (Necessity)**: Can the final answer be fully derived only from previous steps?
- If YES -> error_type: Overthinking
- **Check 2 (Relevance)**: Is this step deals with necessary information to answer the question?
- If NO (e.g., deriving true but useless facts, focusing on wrong entities) -> error_type: Off-topic
- **Check 3 (Novelty)**: Does this step provide new meaningful information or deduction not present in previous steps?
- If NO -> error_type: Redundancy
- **Check 4 (Efficiency)**: Does this step actually perform a meaningful action (extraction/deduction)?
- If NO (e.g., purely planning, stating "I will now...", or summarizing without progress) -> error_type: Inefficiency

 ## Phase 3: Assess Validity & Soundness (For Attribution/Logical Steps)
**Condition**: If the step passes Phase 2 (it is useful and relevant), now check its truthfulness.
**[If Attribution Step]**
- **Check 1 (Consistency)**: Does it contradict the Passage?
- If YES -> error_type: Contradictory
- **Check 2 (Grounding)**: Is the fact explicitly present in the referenced Passage?
- If NO (Hallucination) -> error_type: Unsupported
- **Check 3 (Completeness)**: Does it claim information is missing when the Passage actually has it?
- If YES -> error_type: Information Miss
- **Check 4 (Ordering)**: Does this step extract an attribute (e.g., nationality, birth date) of an entity before establishing
 the necessary relationship (e.g., "is the director of...") that connects this entity to the question’s subject?
- If YES -> error_type: Premature Attribution

**[If Logical Step]**
- **Check 1 (Soundness)**: Is the calculation, comparison, or inference logically valid?
- If NO -> error_type: Logical Fallacy

## Priority Rules
This protocol is hierarchical. You must stop at the first error type with highest priority.
1. **Phase 1 (Final Answer Checks)** take precedence over everything else for ‘(Final Answer)‘ steps.
2. **Phase 2 (Utility Checks)** take precedence over Phase 3.
- If a step is useless (e.g., Redundant, Off-topic, Overthinking, Inefficiency), it is an error regardless of whether it is
factually true or false.
- Do NOT check for Hallucinations (Phase 3) if the step has already failed a Utility Check (Phase 2).
- Report ONLY the first error encountered.




                                                             23
Reasoning Step Evaluation Prompt 2
# Output Generation Instructions

After determining the ‘error_type‘ using the Evaluation Protocol (Phase 1-3), you must generate the ‘diagnosis‘ and
‘guidance‘ fields following these rules.

## 1. How to Write "Diagnosis"
The diagnosis must be a self-contained explanation of *why* the specific ‘error_type‘ was chosen.
NO Protocol References: DO NOT explicitly mention "Phase 1", "Phase 2", "Check 1", etc. The protocol is for your
internal reasoning only. In the output, describe the content issue directly.
Be concise and avoid verbosity. Get straight to the point. Do not repeat the entire content of the step.

- **If Error**:
- **Cite the Violation**: Explicitly mention which Check in the Protocol failed.
- **Provide Evidence**: Quote conflicting text, state missing facts, or compare derived vs. submitted values.
- **If Correct**:
- Briefly explain the specific contribution of this step to the overall reasoning chain.

## 2. How to Write "Guidance"
Based on your ‘diagnosis‘, provide a concise, specific instruction for the **single next immediate step**:
- **If the Step to evaluate has an Error**: Explicitly instruct how to fix the error in the immediate next step.
- **If the Step to evaluate is Correct**: Instruct the specific reasoning action required for the next step.

Important: The guidance must focus ONLY on the single, atomic next action. Do not provide a long-term plan or list
multiple future steps (e.g., "Do A, then B, then C"). Just tell the model to do "A".

If your guidance instruct to generate the final answer step, your guidance must say to include the exact format required:
‘####ANSWER: <answer_value>‘.
—
# Output Format (JSON Only)
{
"error_type": "Selected error type category",
"diagnosis": "Evaluation about the Step to evaluate.",
"guidance": "Instruction for immediate single next step."
}

# Few-shot Demonstrations
[EXAMPLES...]


                                            Figure 12: Evaluation prompt.




Final Answer Generation Prompt
You are an expert answering agent.
The reasoning process is complete. Your task is to formulate the FINAL ANSWER based on the provided history.

INSTRUCTIONS:
1. Do not generate any new reasoning steps.
2. Directly output the final answer.
3. YOU MUST USE THE FOLLOWING FORMAT: ####ANSWER: your_final_answer_here (Final Answer)



                                   Figure 13: Final Answer Generation prompt.




                                                            24
LLM Judge Prompt
You are an expert evaluator for a Question Answering task.
Your goal is to determine if the ’Generated Answer’ is correct based on the ’Ground Truth List’.

**Evaluation Criteria:**
1. **Semantic Equivalence:** If the ’Generated Answer’ refers to the same real-world entity, concept, or event as
**ANY** item in the ’Ground Truth List’, it is "correct". This includes aliases, abbreviations, and common synonyms.
2. **Granularity & Hierarchy:** Accept answers that are factually accurate but differ in specificity or granularity,
provided they refer to the same location or entity.
- **Geographic Inclusion:** Accept constituent countries, states, or specific locations if they are part of the broader
Ground Truth entity (e.g., "England" is correct for "United Kingdom"; "New York" is correct for "USA" if the context
implies origin).
- **Specificity:** Accept broader correct terms if they encompass the specific Ground Truth (e.g., "UK" is correct for
"England" if the question asks for country).
3. **Logical Entailment & Event Description:** Accept answers that describe the same event or fact using different but
factually compatible attributes.
- **Cause vs. Nature:** If Ground Truth specifies the mechanism (e.g., "shot") and Generated Answer specifies the
nature of the event (e.g., "homicide" or "murder"), and both describe the same factual occurrence, it is "correct".
- **Implication:** If the Generated Answer logically implies the Ground Truth or vice versa in the given context (e.g.,
"shot by father" implies "killed by family member"), it is "correct".
4. **Robustness:** Ignore minor formatting, casing, punctuation, or conversational fillers (e.g., "The answer is...").
5. **Contextual Correctness:** If the answer is factually different, references a completely distinct entity, or introduces
contradictory information compared to the ground truth (e.g., "died of old age" vs "shot"), it is "wrong".

**Output Format:**
You must output ONLY a valid JSON object with exactly two keys: "is_correct" and "reasoning". Do not include any
markdown styling or extra text.
- "is_correct": Must be either "correct" or "wrong".
- "reasoning": A brief, high-density explanation of why the answer was judged this way, specifically mentioning any
logical entailment or hierarchy logic if applicable.

[EXAMPLES...]


                                           Figure 14: LLM judge prompt.




                                                           25
Plan Generatom Prompt (2Wiki)
You are an expert AI assistant specializing in query analysis and multi-hop reasoning. Your task is to analyze a given
question and generate the minimal, step-by-step reasoning plan required to answer it.

**Instructions:**
1. Read the user’s question and identify the two entities being compared (Entity A and Entity B) if it is a comparison
question.
2. Identify the specific attribute being compared (e.g., country, release date, lifespan).
3. Determine the correct reasoning plan based on the question type:
* **If the question is a Comparison:**
* **Plan 1 (Simple Attribute Comparison):** The attribute is a single value that can be directly looked up (e.g., country,
date, nationality). This plan involves 3 steps: Find A, Find B, Compare.
* **Plan 2 (Calculated Attribute Comparison):** The attribute must be calculated from other facts (e.g., lifespan). This
plan involves 5 steps: Find facts for A, Calculate attribute for A, Find facts for B, Calculate attribute for B, Compare.
* **Plan 3 (Set Attribute Comparison):** The attribute is a list whose size must be counted (e.g., number of professions,
number of directors). This plan involves 5 steps: Find list for A, Count list for A, Find list for B, Count list for B,
Compare.
* **Plan 4 (Bridge Comparison):** The comparison is about an attribute of a "bridge entity" (e.g., director) connected to
the main entities (e.g., films). This plan involves 5 steps: Find bridge entity A, Find attribute of bridge entity A, Find
bridge entity B, Find attribute of bridge entity B, Compare the attributes to determine which main entity satisfies the
condition.
* **If the question is a Multi-hop Fact Retrieval:**
* **Plan 5 (Sequential Fact Retrieval):** Generate the sequential chain of attribution and logical steps needed to find the
answer.
4. Generate the reasoning plan as a numbered list.
5. Label each step with its type: ‘(Attribution)‘ for finding information or ‘(Logical)‘ for reasoning, calculating, or
comparing.
6. **CRITICAL (Dependencies):** If a step (e.g., Step 2) uses the information found in a previous step (e.g., Step 1),
you **must** explicitly refer to it. (e.g., "Find the father of the person from Step 1.")
7. **CRITICAL (Atomicity):** Do NOT combine multiple actions into a single step. Specifically, do not find an entity
and its attribute simultaneously (e.g., "Find the director and their birth date"). This must be split into two steps: first
identify the entity, then find the attribute.
8. The plan should only contain the intermediate reasoning steps, not the final answer.
9. **CRITICAL (Final Step):** All reasoning plans must end with a ‘(Logical)‘ step, which compares, calculates, or
identifies the final piece of information required by the question. This step must explicitly determine the specific entity
or value requested by the question (e.g., if the question asks ’Which film...’, the final step must be ’determine which film
...’).
10. **CRITICAL (Format):** You MUST output **only** the list in the specified format: ‘[Step 1: ..., Step 2: ..., ...]‘.
Do not include *any* other text, JSON formatting, explanations, or conversational chat before or after the list.
—
**Examples:**
[EXAMPLES...]


                         Figure 15: Plan generation prompt for 2WikiMultiHop dataset.




                                                            26
Plan Generation Prompt (HotpotQA)
You are an expert AI assistant specializing in query analysis and multi-hop reasoning. Your task is to analyze a given
question and generate the minimal, step-by-step reasoning plan required to answer it.

**Instructions:**
1. Read the user’s question and determine its primary type:
* **Fact Retrieval (Sequential/Compositional/Inference):** The question asks for a single fact (Who/What/When/Where)
which requires finding intermediate facts first (e.g., "Who is the mother of the director of..."). This is **Plan 4**.
* **Comparison:** The question compares two or more entities (e.g., "Who was born first, A or B?", "Which has
more..."). This is **Plan 1, 2, or 3**.
2. **If the question is a Comparison:**
* **Plan 1 (Simple Attribute Comparison):** The attribute is a single value that can be directly looked up (e.g., country,
date, nationality). This plan involves 3 steps: Find A, Find B, Compare.
* **Plan 2 (Calculated Attribute Comparison):** The attribute must be calculated from other facts (e.g., lifespan,
duration). This plan involves 5 steps: Find facts for A, Calculate attribute for A, Find facts for B, Calculate attribute for
B, Compare.
* **Plan 3 (Set Attribute Comparison):** The attribute is a list whose size must be counted (e.g., number of professions,
number of members). This plan involves 5 steps: Find list for A, Count list for A, Find list for B, Count list for B,
Compare.
3. **If the question is a Fact Retrieval:** * **Plan 4 (Sequential Fact Retrieval):** Generate the sequential chain of
attribution and logical steps needed to find the answer.
4. **CRITICAL (Minimal Atomic Plan):** The plan must be **minimal** and **atomic**.
* A search for an entity with multiple constraints (e.g., "the 2011 film scored by Chris Bacon that is based on
Shakespeare") must be a **single (Attribution) step**, not multiple filtering steps.
* Descriptive clauses (e.g., "Ku Hye-sun, who appeared in...") are constraints for the *first* search step. **DO NOT**
create separate steps for "confirmation" or "verification" of this descriptive information.
5. Generate the reasoning plan as a numbered list.
6. Label each step with its type: ‘(Attribution)‘ for finding information or ‘(Logical)‘ for reasoning, calculating, or
comparing.
7. **CRITICAL (Dependencies):** If a step (e.g., Step 2) uses the information found in a previous step (e.g., Step 1),
you **must** explicitly refer to it. (e.g., "Find the director of the film found in Step 1.")
8. **CRITICAL (Final Step):** All reasoning plans must end with a ‘(Logical)‘ step, which compares, calculates, or
identifies the final piece of information required by the question. This step must explicitly determine the specific entity
or value requested by the question (e.g., if the question asks ’Which film...’, the final step must be ’determine which film
...’).
9. Output the steps in a **list format**: ‘[Step 1: ..., Step 2: ..., ...]‘
10. **CRITICAL (Format):** You MUST output **only** the list in the specified format. Do not include *any* other
text, JSON formatting, explanations, or conversational chat before or after the list.
—
**Examples:**
[EXAMPLES...]


                             Figure 16: Plan generation prompt for HotpotQA dataset.




                                                             27
Plan Generatom Prompt (MuSiQue)
You are an expert AI assistant specializing in query analysis and reasoning plan generation. Your task is to translate a
given Question Decomposition (a list of sub-questions/steps) into a formal, step-by-step reasoning plan.

The user will provide two inputs:
**Question:** The original multi-hop question.
**Question Decomposition:** A numbered list of sub-questions labeled as Q1, Q2, Q3, etc. Each sub-question describes
one reasoning step, where later steps (e.g., Q2, Q3) may depend on previous results using references like "#1" (meaning
the answer from Q1) or "#2" (meaning the answer from Q2).

Your task is to convert this Question Decomposition into a reasoning plan with (Attribution) and (Logical) steps.

**Instructions:**

1. Read the Question Decomposition list carefully. Each line will be labeled as Q1, Q2, Q3, etc. Treat each "Qn" as one
reasoning step in sequence.
2. For each item in the Question Decomposition list, create one corresponding (Attribution) step.
Example: A decomposition step like ’Q1: Keep the Faith » performer’ must be translated into Step 1: Find the performer
of "Keep the Faith". (Attribution).
3. **CRITICAL (Dependencies):** Translate the dependencies exactly. A decomposition step like ’Q2: #1 » record
label’ must be translated to Step 2: Find the record label for the entity found in Step 1. (Attribution). A decomposition
step like ’Q3: #2 » genre’ must be translated to Step 3: Find the genre of the entity found in Step 2. (Attribution).
4. **CRITICAL (Final Step):** After translating all steps from the Question Decomposition, add one final (Logical)
step. This final (Logical) step must identify the result of the last attribution step as the answer, based on what the original
Question was asking. Example: If the last attribution step was Step 3: Find the genre... and the original Question was
"What is the... genre...", the final step must be "Step 4: Identify the genre found in Step 3 as the answer. (Logical)".
5. **CRITICAL (Format):** Output the plan as a numbered list in a single list format: [Step 1: ..., Step 2: ..., ...]
6. **CRITICAL (Output Only):** You MUST output only the list in the specified format. Do not include any other text,
JSON formatting, explanations, or conversational chat before or after the list.
—
**Examples:**
[EXAMPLES...]


                              Figure 17: Plan generation prompt for MuSiQue dataset.



Ideal Reasoning Generation Prompt
You are an expert AI assistant specializing in multi-hop reasoning. Your task is to generate the ideal, step-by-step
reasoning that correctly follows a given reasoning plan, using only the provided ground truth context.

**Instructions:**
1. You will be given a ‘Question‘, a ‘Ground Truth Context‘, and a ‘Reasoning Plan‘ (list of instructions).
2. Your goal is to "execute" the ‘Reasoning Plan‘ to generate the final reasoning steps.
3. You must generate exactly one reasoning step for each instruction in the ‘Reasoning Plan‘.
4. **CRITICAL (Context):** Your reasoning *must* be based *only* on the facts provided in the ‘Ground Truth
Context‘. Do not use any external knowledge.
5. **CRITICAL (Citation):** For all ‘(Attribution)‘ steps, you **must** explicitly cite the passage number in the text
("According to Passage 1, ...").
6. **CRITICAL (Tags):** Each reasoning step you generate *must* end with the exact ‘(Attribution)‘ or ‘(Logical)‘ tag
that appears in the corresponding plan step.
7. **CRITICAL (Dependencies):** When a plan step has a dependency (e.g., "...from Step 1"), your reasoning step
must clearly show this (e.g., "The father of Bengt Snivil (from Step 1) is...").
8. **CRITICAL (Index Mapping):** - For **(Attribution)** steps: ‘supporting_index‘ must be the integer index of
the Passage used (e.g., 1 for Passage 1). - For **(Logical)** steps: ‘supporting_index‘ must be a list of indices of the
previous steps used as evidence (e.g., [2, 4]).
9. **CRITICAL (Format):** You MUST output **only** a valid JSON-style list of dictionaries. Do not include
markdown code blocks (“‘json), backticks, or any conversational text. Start directly with ’[’ and end with ’]’.
—
**Examples:**
[EXAMPLES...]


                                    Figure 18: Ideal reasoning generation prompt.



                                                             28
Error Injection Prompt
You are an expert in logical reasoning, tasked with intentionally introducing a specific logical error into a reasoning
steps.

Your Goal: Replace a single, correct reasoning step with an {error_type} error.

Error Definition:
[ERROR_DEFINITION]

Input Format:
You will receive:
1. Question: The user’s original question.
2. Retrieved Passages: Contextual information.
3. Ideal Reasoning Steps: The correct, multi-step reasoning.
4. Target Step to Corrupt: The specific step from the ideal steps that you must replace. (ex. Step 2)

Output Format:
- You MUST output only the single, new, erroneous reasoning step.
- The new step MUST be formatted exactly like the target step, including the "Step X:" prefix and the "(Label)" suffix.

—
EXAMPLES
—

[Examples...]



                                         Figure 19: Error Injection prompt.


Triple Extraction Prompt
You are an expert Knowledge Graph Engineer and Computational Linguist. Your task is to extract all factual triples from
the provided text passage to construct a comprehensive Knowledge Graph.

### CRITICAL INSTRUCTION: COREFERENCE RESOLUTION (DECONTEXTUALIZATION)
Before extracting any triples, you must strictly perform **Coreference Resolution** internally.
- **Never use pronouns** (e.g., "he", "she", "it", "they", "this", "that", "the film", "the company") as the Subject or
Object in the output triples.
- You must identify the specific entity the pronoun refers to from the context and replace the pronoun with the **full
canonical name** of that entity.
- Example: If the text says "Barack Obama: Barack Obama was born in Hawaii. He served as the 44th president.", the
extracted triple must be ‘["Barack Obama", "served_as", "44th president"]‘, NOT ‘["He", "served_as", "44th president"]‘.

### EXTRACTION GUIDELINES
1. **Atomic Triples:** Break down complex sentences into atomic facts (Subject, Predicate, Object).
2. **Predicate Standardization:** Use clear, concise, and meaningful predicates (e.g., "born_in", "directed_by",
"spouse", "occupation"). Avoid vague verbs like "is" or "has" if a more specific relation exists.
3. **Attribute Extraction:** Extract numerical values, dates, and specific roles as Objects.
- Dates should be in ‘YYYY-MM-DD‘ format if possible.
- Numbers should be kept as raw values suitable for comparison.

### OUTPUT FORMAT
Output **ONLY** a standard JSON list of lists. Do not include any explanation or markdown formatting outside the
JSON. Each inner list must strictly follow the order: ‘[Subject, Predicate, Object]‘. The Subject is the entity being
described.

JSON Format:
[["Entity Name", "Relation/Attribute", "Entity Name/Value"], ["Entity Name", "Relation/Attribute", "Entity
Name/Value"], ...]

### EXAMPLES
[EXAMPLES...]


                                        Figure 20: Triple extraction prompt.


                                                           29
Triple Gleaning Prompt
You are a meticulous Knowledge Graph Auditor and QA Specialist. Your goal is to review the extraction results from a
previous step and identify **MISSING** factual triples that were overlooked.

### INPUTS
You will be provided with:
1. **Original Text Passage**: The source text.
2. **Existing Triples**: A list of triples already extracted from the text.

### TASK
Compare the **Original Text** against the **Existing Triples**. Extract **NEW** factual triples that are present in
the text but **NOT** in the Existing Triples list.

### CRITICAL RULES
1. **NO DUPLICATES**: Do not output any triple that is semantically identical to one in the "Existing Triples" list.
2. **Focus on Detail**: Look specifically for: - Secondary entities mentioned in the text (not just the main subject).
- Specific dates, numbers, or measurements previously missed.
- Relationships between secondary entities.
- Adjectives or roles acting as attributes (e.g., "Polish-French" -> nationality).
3. **Coreference Resolution (Mandatory)**: Just like the first step, you MUST resolve pronouns (he, she, it, they) to
their full canonical entity names. **Never** use pronouns in your output.
4. **Atomic & Standardized**: Follow the same extraction standards (Atomic facts, standardized predicates).
5. **Aliases & Alternate Names:**
- If an entity has multiple names (e.g., "better known as", "born as", "pseudonym", "nickname"), you MUST extract a
triple linking them.
- Use predicates like ‘same_as‘, ‘alias‘, ‘birth_name‘, or ‘alternative_name‘.
- Example: "Donna Paige Helmintoller, better known as Paige O’Hara" -> Extract ‘["Donna Paige Helmintoller",
"same_as", "Paige O’Hara"]‘.

### OUTPUT FORMAT
Output **ONLY** a standard JSON list of lists containing the **NEWLY EXTRACTED** triples. If no new triples are
found, output an empty list ‘[]‘.

JSON Format:
[["Subject", "Predicate", "Object"], ["Subject", "Predicate", "Object"], ...]



                                         Figure 21: Triple gleaning prompt.




                                                            30
Entity Resolution Prompt
You are an expert Knowledge Graph Engineer specializing in Entity Resolution (Coreference Resolution). Your task is
to identify and group entities that refer to the **same real-world object** (Named Entities) from the provided list of
entities and context triples.

### INSTRUCTIONS
1. **Analyze Entities:** Review the provided list of entities.
2. **Check Context:** Use the "Context Triples" to verify if similar names refer to the exact same unique entity.
3. **Group Synonyms:** Group variations (abbreviations, acronyms, partial names, typos) of the same **Specific
Named Entity** into a single list.
4. **Filter Noise:** **STRICTLY EXCLUDE** generic terms, common nouns, numbers, dates, and abstract concepts.

### OUTPUT FORMAT
Output **ONLY** a JSON list of lists. Each inner list represents a group of synonymous entities.
Example: ‘[["USA", "United States", "U.S."], ["JFK", "John F. Kennedy"], ["The Green Album", "Green"]]‘

### RULES
1. **Target Proper Nouns Only:** Only group Specific People, Places, Organizations, Events, and Works.
2. **Exclude Generics:** Do NOT include or group common nouns or roles.
- **Bad:** "president", "mother", "clothes", "the album", "the band", "different stage names", "two sons".
- **Good:** "President Obama", "Mother Teresa", "The White Album", "System 7".
3. **Exclude Literals:** Do NOT include or group Values.
- **Dates:** "2020-01-01", "1990s", "May 5th".
- **Numbers:** "3", "100", "first", "one".
- **Measurements:** "3 years", "10kg", "50%".
4. **Avoid Super Nodes:** Never group a specific entity with a generic category (e.g., DO NOT group ‘["Barack
Obama", "President"]‘). "President" is a title/role, not the person’s unique identifier.
5. **Context is King:** If "Jordan" appears in a triple about basketball and another about the Middle East, DO NOT
group them.



                                      Figure 22: Entity resolution prompt.




                                                         31
Logical Path Discovery Prompt
You are an expert Knowledge Graph Reasoner. Your task is to identify the **Reasoning Evidence (Subgraph)** required
to answer a Multi-hop Question using the provided Normalized Triples.

### GOAL
Select the **minimal set of triples** that acts as the necessary premises to logically derive the **Ground Truth Answer**.

### UNDERSTANDING REASONING PATTERNS
The "Reasoning Path" is NOT always a single connected chain. It can be:
1. **Sequential (Bridge):** (e1, r1, e2) -> (e2, r2, e3)
* *Ex:* "When is the birthplace of the director of the movie Parasite?"
2. **Parallel (Comparison/Intersection):** (e1, r1, v1) and (e2, r1, v2)
* *Ex:* "Are Obama and Trump born in the same country?" (Requires birthplaces of BOTH persons, even if they are
disjoint nodes).
* *Ex:* "Who is older, A and B?" (Requires birthdates of BOTH persons).

### INSTRUCTIONS
1. **Analyze the Logic:** Determine if the question requires a chain of facts, a comparison of two facts, or an
intersection of attributes.
2. **Select Evidence:** Pick ONLY the triples necessary to support the reasoning.
* **Ignore Direction:** Treat relations as bidirectional if semantically appropriate (e.g., ‘["Movie", "directed_by",
"Director"]‘ supports finding the director).
* **Semantic Match:** Match predicates loosely (e.g., "born_in" is equal to "place of birth").
3. **Verify & Explain:**
* Do these selected triples logically lead to the Ground Truth Answer?
* If the required triples are missing (e.g., one side of a comparison is missing), mark as invalid.

### OUTPUT FORMAT
Output **ONLY** a JSON object:
{
"is_valid": true, // true if ALL necessary evidence is present to derive the Ground Truth Answer
"reasoning_path": [ // List of selected triples. Can be disjoint (e.g., two separate birth dates). ["Subject1", "Predicate1",
"Object1"], ["Subject2", "Predicate2", "Object2"], ... ],
"explanation": "Briefly explain the logic (e.g., ’Found birth dates for both persons to compare them’)."
}

### EXAMPLES

[Examples...]



                                     Figure 23: Logical path discovery prompt.




                                                            32
