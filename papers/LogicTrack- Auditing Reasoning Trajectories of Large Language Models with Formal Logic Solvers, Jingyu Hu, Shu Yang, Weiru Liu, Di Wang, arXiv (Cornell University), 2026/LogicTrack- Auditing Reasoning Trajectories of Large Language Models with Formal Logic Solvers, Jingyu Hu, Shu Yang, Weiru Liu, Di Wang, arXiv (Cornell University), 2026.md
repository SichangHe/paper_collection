                                                                    LogicTrack: Auditing Reasoning Trajectories of
                                                                   Large Language Models with Formal Logic Solvers
                                                                               Jingyu Hu1 , Shu Yang2 , Weiru Liu1 , Di Wang2
                                                                                                   1
                                                                                                     University of Bristol
                                                                                 2
                                                                                     King Abdullah University of Science and Technology



                                                                     Abstract                                   first is training-free test-time self-refinement, where the LLM
arXiv:2609.21492v1 [cs.AI] 18 Sep 2026




                                                                                                                generates a response, receives feedback through a critic model
                                           Chain-of-Thought (CoT) reasoning has been shown to improve
                                                                                                                or retrieval mechanism, and applies a search algorithm to
                                           the performance of large language models (LLMs), yet ex-
                                           isting optimization methods largely rely on outcome-based            regenerate the response based on that feedback (Yao et al.
                                           feedback, leaving the logical validity of intermediate reasoning     2023a; Xie et al. 2023). The second is training-based process
                                           steps largely unverified. To address the gap whereby LLMs            supervision, where process reward models (PRMs) are trained
                                           arrive at correct final answers through logically flawed inter-      to evaluate the quality of individual reasoning steps, typi-
                                           mediate reasoning chains, we propose LogicTrack, a neuro-            cally using human-annotated or model-generated step-level
                                           symbolic framework that audits reasoning trajectories by auto-       labels (Lightman et al. 2023; Khalifa et al. 2023). However,
                                           formalizing each reasoning step into symbolic representations        methods in both categories ultimately rely on human feedback
                                           and verifying it with automated theorem provers. LogicTrack          or LLM-based judges to produce feedback and reward signals.
                                           introduces Solver-Based Backtracking Reward (SBR), a step-           Such signals are non-deterministic for logical correctness,
                                           wise scoring mechanism that quantifies logical soundness and
                                                                                                                prone to inconsistency, and difficult to scale reliably across
                                           guides backtracking tree search at inference time. We further
                                           extend LogicTrack to construct supervised fine-tuning (SFT)          diverse domains.
                                           data with backtracking traces from its trajectories, enabling           More recent efforts have turned to neuro-symbolic ap-
                                           fine-tuned models to internalize step-wise auditing as an in-        proaches to make verification more reliable. These include us-
                                           trinsic capability. Extensive experiments across 8 reasoning         ing formal tools for symbolic checking of LLM outputs (Olaus-
                                           benchmarks and 7 LLMs demonstrate that LogicTrack effec-             son et al. 2023; Pan et al. 2023), auto-formalization of natu-
                                           tively improves both the verifiability of reasoning chains and       ral language reasoning into solver-verifiable logic, and self-
                                           final answer pass rate, thereby enhancing overall CoT quality        refinement guided by solver feedback (Quan et al. 2024; Singh
                                           and trustworthiness in high-stakes domains.                          et al. 2026). Step-wise formal verification for natural language
                                                                                                                reasoning remains underexplored. Recent LogicReward (Xu
                                                              1     Introduction                                et al. 2025b) and VeriCoT (Feng et al. 2025) represent impor-
                                                                                                                tant initial steps in this direction. Concretely, both methods
                                         Reasoning chains have greatly advanced the capacity of large
                                                                                                                first generate a complete response and then apply solver-based
                                         language models (LLMs) to tackle complex tasks in cod-
                                                                                                                step verification retroactively, constructing SFT and DPO
                                         ing (Gao et al. 2023), question answering (Lu et al. 2022),
                                                                                                                training data from the verified traces.
                                         and logical reasoning (Xu et al. 2024). Recent models such as
                                         OpenAI-o1 (Jaech et al. 2024) and DeepSeek-R1 (Guo et al.                 However, both methods perform step verification in a
                                         2025) further improve performance by encouraging the model             post-hoc way. They require a complete reasoning chain and
                                         to verbalize and extend its thinking trajectory before generat-        final answer to be generated first, and then audit each step
                                         ing a final answer. However, producing a correct final answer          retroactively. This paradigm has two limitations. First, once
                                         is not sufficient on its own. If the intermediate reasoning            the full response has been produced, delayed verification
                                         steps contain logically invalid operations, users in high-stakes       raises safety concerns as flawed reasoning may have already
                                         domains such as legal and scientific reasoning cannot trust            been presented to or acted upon by users. Second, a logical
                                         its conclusions, even when the final answer happens to be              error in an intermediate step can propagate through and
                                         correct (Turpin et al. 2023; Huang and Chang 2023). This               corrupt subsequent reasoning steps, making after-the-fact
                                         concern is especially important as most current methods use            correction both more difficult and less reliable.
                                         outcome-driven training, which does not guarantee that the                These limitations naturally raise the question of whether
                                         reasoning path itself is sound.                                        we can audit LLMs’ reasoning trajectories during generation
                                            This concern has motivated a growing body of research               and intervene with timely backtracking to regenerate from
                                         focused on the quality of intermediate reasoning steps. Ex-            the point of failure. To address this question, we introduce
                                         isting work can be broadly divided into two categories. The            LogicTrack, a neuro-symbolic framework for generation-
                                                                                                                time auditing and improvement of CoT reasoning through a
                                         Preprint                                                               formally defined verification reward. Specifically, LogicTrack
       Autoformalization             𝑠!

      Automated Theorem                     Consistency
        Provers (ATP)                        Checker
                                                                    Reward-guided Search
     Error      Verification              Fidelity    Error          with Backtracking
     Logs        Reward                   Reward      Logs
                                                                      LogicTrack Generated Trajectories
                                                                                                          User P: ∀x Bird(x)→Fly(x); Cat⊂Bird;
                    Auditing Reflections                                       BT                 …       Cat(Kitty) Q: Fly(Kitty)?

                                                                      BT            BT            …       LLM Cat(x)→¬Fly(x) [BT] Cat⊂Bird
                               SBR                                                                …
                                                                                                          Bird(x)→Fly(x) ⊢ Cat(x)→Fly(x) [FW]
                                                                                                          Cat(Kitty) ⊢ Fly(Kitty)
 Decomposition &
 Formal Veri&ication [FW]            [BT]                                  LLM Self-Backtracking Supervised Fine-tuning

Figure 1: Overview of the LogicTrack workflow. Each NL reasoning step is decomposed, formalized into a solver-executable
specification, verified, assigned an SBR score, and either forwarded [FW] to the next step or backtracked [BT] for regeneration.
These generated trajectories can be used for backtracking fine-tuning.


decomposes each NL reasoning step into premises, expla-                             2    Methodology of LogicTrack
nations, and conclusions, auto-formalizes them into logic            Figure 1 illustrates the overall workflow of LogicTrack, which
specifications, and uses the solver for verification. We define      proceeds in three parts: decomposition and formal verification,
Solver-based Backtracking Reward (SBR), a fine-grained               reward-guided search with backtracking, and the extended
step-level signal that combines premise fidelity with solver         application of LogicTrack as higher-quality training data for
verification. LogicTrack enables a reward-guided backtrack-          self-backtracking supervised fine-tuning.
ing search at inference time. When SBR of a step falls below
a predefined threshold, the model triggers a backtrack and           Preliminaries. When models use natural language to infer
regenerates the reasoning from that step onward.                     logical reasoning tasks, their goal is to determine the logical re-
   Beyond inference-time auditing, we further extend the             lationship between a set of given premises P = {p1 , . . . , pn }
application of LogicTrack to self-backtracking supervised            and a query Q. Each data sample is a triple x = (P, Q, y),
fine-tuning (SFT). Unlike prior self-correction methods that         where y ∈ Y is the ground-truth label from a dataset-specific
rely on synthetically injected errors to construct backtracking      label set Y. Although label names (e.g., entailment/contra-
datasets (Yang et al. 2025a), LogicTrack pairs real model-           diction, yes/no/uncertain) differ across datasets, each Y cor-
generated flawed trajectories with solver-verified corrections.      responds to one of three underlying logical relations: P |= Q,
Fine-tuning on these trajectories with a dedicated backtrack         P |= ¬Q, or neither. Given a sample x, the model response
token <backtrack> allows the model to internalize step-              is an ordered sequence of T reasoning steps (s1 , s2 , . . . , sT )
wise verification behavior, and we show that this benefit            followed by a final prediction ŷ. To ensure the quality of both
generalizes across multiple benchmarks and models.                   the final prediction and the intermediate reasoning trajectories,
                                                                     we propose LogicTrack to audit the logical validity of each
  Overall, our main contributions are as follows:                    intermediate step and trigger backtracking when necessary.
 • We propose LogicTrack, a neuro-symbolic framework that
   audits NL reasoning trajectories via autoformalization and        2.1      Decomposition and Formal Verification
   solver verification at inference time. LogicTrack includes        Step Decomposition We specify in the LLM response
   a reward-guided backtracking mechanism that uses Solver-          format that each reasoning step needs to present new con-
   based Backtracking Reward to audit and guide model                clusion(s) derived from context Ci and explanation Ei , and
   step-wise reasoning.                                              the details are explained below. Let Ki = {q1 , . . . , qi } de-
 • We evaluate LogicTrack on eight reasoning benchmarks              note the set of derived conclusions from the first i verified
   across seven models, showing consistent improvements              reasoning steps (K0 = ∅). Specifically, the step si can be
   in both final-answer correctness and intermediate-step            decomposed into three components si = (Ci , Ei , qi ), defined
   validity. Further ablation studies and diverse variants of the    as below. With both Ci and Ei stated explicitly, the conclusion
   search strategy confirm the generalizability of LogicTrack.       qi should follow by logical entailment alone. The verified qi
 • We show that LogicTrack can be extended to construct              is then incorporated into Ki , making it available as context
   high-quality backtracking SFT data. By introducing a              for subsequent steps.
   dedicated backtrack token, the fine-tuned model inter-             • Context Ci : the premises from P and prior verified con-
   nalizes step-wise verification behavior and achieves self-            clusions relevant to this step, i.e., Ci ⊆ P ∪ Ki−1 .
   backtracking in reasoning.                                         • Explanation Ei : implicit assumptions and background
   knowledge that the step relies on but does not state, e.g.,
   “a father is a parent”.
 • Conclusion qi : the new claim derived from Ci and Ei .
Autoformalization and Verification Unlike post-hoc veri-
fication methods that check the entire reasoning chain after the
response is fully generated, LogicTrack performs verification
during reasoning in a step-wise autoregressive way. Starting
from the i−1 verified steps (s1 , . . . , si−1 ) and knowledge
base Ki−1 , the reasoning LLM generates the next candidate
step si , conditioned on (P, Q, s1 , . . . , si−1 ). The candidate is
then decomposed, formalized and verified by the logic solver.
   For each candidate step si , the formalization model re-
ceives components (Ci , Ei , qi ) and formalizes them into an           Figure 2: An example of LogicTrack-SFT training data con-
executable logic specification Fi in SMT-LIB format. The con-           struction with backtracking trajectories.
text and explanations are jointly formalized as a conjunction
of solver assertions Φi , i.e., Φi encodes Ci ∪ Ei . The conclu-
sion qi is encoded as the proof goal, yielding Fi = (Φi , qi ),         maintains a verified prefix (s1 , . . . , st−1 ) and evaluates a
so that verification reduces to checking if Φi |= qi . Given            new candidate st against two quality criteria: the step-level
Fi = (Φi , qi ), LogicTrack verifies whether the candidate              reward SBR(st ) and running mean over all verified steps
                                                                                        Pt
step is well-formed and logically justified. The solver first           SBR(t) = 1t i=1 SBR(si ). The search starts from an empty
checks syntactic validity of the generated formalization; if            prefix and proceeds one step at a time. A candidate st is
the specification is malformed, the autoformalization module            forwarded if SBR(st ) ≥ θstep and SBR(t) ≥ θavg . In
is re-invoked up to M times. Once a valid specification is              that case, st is appended to the verified prefix and Kt−1 is
obtained, the solver tests whether Φi |= qi via proof by refu-          updated to Kt .
tation, that is, it checks whether Φi ∪ {¬qi } is unsatisfiable,           When triggering backtracking, LogicTrack collects the
and also records diagnostic signals such as contradiction or            audit logs for st and re-prompts the model with the verified
undecidability. These verification outcomes, together with              prefix (s1 , . . . , st−1 ) along with concise failure feedback
the judge’s assessment of explanation grounding, are stored             derived from error logs. The model then regenerates from
as a step-level audit log and converted into the scalar reward          position t onward. This backtracking process repeats until a
used by the search controller.                                          viable solution is found. We provide implementation details
                                                                        and discussion of other backtracking strategies like Beam
2.2    Reward-Guided Backtracking Search                                search and MCTS in Appendix A.1 A.1.
We consider two aspects of effective reasoning. The model
must ground its reasoning in the given premises, and each in-           2.3   LogicTrack with Backtracking-SFT
ference must be logically sound. We design a reward function            We introduce LogicTrack-SFT, an extension of LogicTrack
called the Solver-based Backtracking Reward (SBR) to quan-              that converts its backtracking trajectories into supervised
tify both aspects. LogicTrack assigns each step si a composite          fine-tuning data, allowing the model to internalize step-level
reward SBR(si ) = λ·Rfidelity (Φi ; P )+(1−λ)·Rverify (Fi ).            auditing as an intrinsic capability.
  • Fidelity reward Rfidelity (Φi ; P ): Checks the consistency            Recent work has shown that training on explicit error-
    of Φi , including if each assertion is grounded in the              correction trajectories can teach models to revise flawed rea-
    original premises P (not sourced from the query Q), if              soning. An et al. (An et al. 2023) construct mistake-correction
    introduced commonsense is acceptable, and if Φi is jointly          pairs; Ye et al. (Ye et al. 2024) show that retry data with erro-
    satisfiable. We define Rfidelity (Φi ; P ) = 1 if all checks        neous steps immediately followed by corrections improves
    pass, and 0 otherwise.                                              reasoning; and Self-Backtracking (Yang et al. 2025b) further
  • Verification reward RVerify (Fi ): The verification score           introduces a dedicated backtracking token to learn when and
    is set to 1 if the specification Fi is syntactically correct        where to revise a partial trajectory. However, the supervision
    and the step is logically valid (Φi |= qi ). If Fi is syn-          signals in these methods are largely synthesized from arti-
    tactically invalid, autoformalization will be regenerated           ficially injected or sampled errors in mathematical settings,
    up to M times before the step is marked as unverifiable             where correctness is straightforward to verify. We build on
    and RVerify (Fi ) = 0. We also set RVerify (Fi ) = 0 if the         the same backtracking intuition but focus on a harder setting:
    solver actively refutes the step (Φi |= ¬qi ). For undecided        using LogicTrack to construct verifier-grounded backtracking
    steps, the verifier assigns partial credit RVerify (Fi ) = α,       steps for NL logic reasoning.
    where α ∈ (0, 1) is a discounting constant, since these                Specifically, SFT training data is constructed from Log-
    steps may simply exceed the solver’s decision procedure             icTrack’s backtracking trajectories. We treat the verified
    without being logically wrong.                                      correct path from the search tree as s+ and the backtracked
LogicTrack builds the verified reasoning chain via reward-              steps that triggered backtracking events as s− . A training
guided backtracking search to decide whether to forward or              trajectory with backtrack at position k is assembled by con-
backtrack on each candidate step. At each step t, the search            catenating the correct prefixes, the backtracked step s−       k,
                                                                                                            BASE     LogicTrack (Our)      Closed-source     Open-source     GPT-4o-




                                                                                 Verified utility (VU)
 a special backtrack token, and the verified correct contin-                                                                                                                  mini

 uation: {s+          +
             1 · · · sk−1   s−
                             k    <backtrack> s+                    +
                                                           k · · · sn }.
                                                                                                                                                   GPT-5-
                                                                                                                                                   nano           Qwen-14B
 For example, one possible training trajectory with
                                                                                                                                                           Qwen-7B              Gemini-2.5
 backtracking in the workflow demo in Figure 1                                                                                  Llama-8B        GPT-5-
                                                                                                                   Mistral-7B                   nano
 is {s1 , s2 , s3 , s4 , <backtrack>, s′′4 , s′′5 , s′6 }. Figure 2                                                                                                Qwen-14B
 presents a more intuitive example, where we aim to determine                                                                                               GPT-4o-         Gemini-2.5
                                                                                                              Mistral-7B                       Qwen-7B       mini
 whether Alex is cold based on the given premises, such as
                                                                                                                           Llama-8B
‘Alex is Tumpus’ and ‘dompus is zumpus’. We consider both                                                                                                                    Outcome Accuracy (OA)
 single-round and multi-round backtracking during the syn-
 thetic stage, resulting in a set of ∼6,000 samples for training.
 Given the constructed trajectory s, LogicTrack-SFT mini-                  Figure 3: Overall OA and VU for all models averaged across
 mizes the standard                                                        eight benchmarks under BASE and LogicTrack settings. Here
                    Pn autoregressive negative log-likelihood              • indicates closed source models, and ▲ indicates locally
 LSFT (θ) = − t=1 log pθ (st | P, Q, s<t ). The backtrack
 token <backtrack> is added to the model vocabulary and                    deployed models. Dashed arrows connect each model’s BASE
 trained end-to-end, teaching the model to recognize flawed                and LogicTrack results.
 steps and self-correct without external critics. The detailed
 implementations can be found in Appendix A.2A.2.
                                                                           3.2                           Main Results: Higher Outcome Correctness
              3    Experiments and Results                                                               and Step Verifiability
This section presents the experimental setup and the discus-
sions of overall performance, ablation studies, and Logic-                 Figure 3 compares the average OA and VU of the base
Track’s extended application to SFT self-backtracking.                     models and LogicTrack across all seven models. Overall,
                                                                           LogicTrack consistently improves both metrics on almost
3.1    Experimental Setup                                                  all settings. The VU gains are especially pronounced: GPT-
                                                                           4o-mini rises from 21.51% to 46.61%, Llama3.1-8B from
Datasets and Baselines. We evaluate on a diverse col-                      9.24% to 32.75%, and Qwen2.5-7B from 16.33% to 35.54%.
lection of natural-language reasoning benchmarks includ-                   Among the closed-source models, GPT-4o-mini also achieves
ing e-SNLI (Camburu et al. 2018), FOLIO (Han et al.                        the strongest joint gain in OA, increasing from 70.68% to
2024), LogiQA (Liu et al. 2020), ProntoQA (Saparov and                     78.49%. The simultaneous improvement of OA and VWA
He 2023), ProofWriter (Tafjord, Dalvi, and Clark 2021),                    suggests that verification does more than trigger backtracking;
QASC (Khot et al. 2020), SARA (Holzenberger, Blair-Stanek,                 it can steer regeneration toward reasoning paths that are both
and Van Durme 2020), and SemEval (SemEval-2026 Team                        more valid and more answer-preserving.
2026).                                                                        Table 1 further confirms that this pattern holds at the
   Each dataset is split into train and test set following (Xu             benchmark level. LogicTrack improves over the baseline in
et al. 2025b). The evaluation covers seven large language                  133 out of 168 benchmark metric comparisons. Specifically,
models with varying architectures and scales, including three              LogicTrack preserves or improves OA on most model and
proprietary models (Gemini-2.5 (Comanici et al. 2025), GPT-                dataset pairs, with especially large gains on tasks that require
4o (Hurst et al. 2024), and GPT-5 (Singh et al. 2025)) and four            multi-step deduction. Qwen2.5-7B shows 0% VWA on QASC
open-weight models (Llama (AI 2024), Mistral (Jiang et al.                 as it directly outputs answers with no reasoning steps, causing
2023), Qwen2.5-7B, and Qwen2.5-14B (Yang et al. 2024)).                    step-level evaluation to fail. This issue can be mitigated by our
We use the vanilla CoT as our primary baseline (BASE).                     SFT model (Table 5). GPT-4o-mini on ProofWriter rises from
Additional baseline comparisons (i.e. LogicReward) can be                  54.27% to 79.9%, Qwen2.5-7B on ProntoQA from 92% to
found in Appendix C, and more detailed descriptions of the                 97%, and Mistral-7B on ProofWriter from 27.14% to 39.2%.
datasets and models are reported in Appendix B.                            Even when the base model is already strong, LogicTrack
                                                                           maintains OA while improving verifiability. GPT-5-nano on
Metrics. We evaluate models using four metrics that assess                 ProntoQA, for example, stays at high OA while UR drops
outcome-level performance, process-level performance, and                  from 11.17% to 10.24%. LogicTrack also reduces UR for
their combination. Outcome Accuracy (OA) is the fraction                   most model and dataset pairs, confirming that backtracking
of LLM responses where the final answer is correct. Verified               replaces unverifiable steps with solver-validated alternatives.
Ratio (VR) measures the average proportion of reasoning                    The largest reductions include Gemini-2.5 on FOLIO from
steps that pass solver checks. Unverified Ratio (UR) is the                75.63% to 27.79%, Llama-3.1-8B on SARA from 39.1% to
complementary fraction of unverified steps. Verified Utility               9.89%, and Llama-3.1-8B on QASC from 44.65% to 16.3%.
(VU) refers to answer accuracy restricted to all fully verified            These reductions are accompanied by large VWA gains.
steps. Verification-Weighted Accuracy (VWA) combines                       GPT-4o-mini on ESNLI rises from 46.38% to 87.21%, and
both aspects by weighting each correct prediction by its per-              Gemini-2.5 on FOLIO from 21.17% to 56.37%. Overall, these
problem verification ratio. More detailed metric descriptions              results show that LogicTrack improves both final answers and
are provided in Appendix B.                                                the verifiability of the reasoning process.
Dataset   Metric     Gemini-2.5     GPT-4o-mini      GPT-5-nano    Llama-3.1-8B     Mistral-7B    Qwen2.5-7B       Qwen2.5-14B

                    BASE    Ours BASE       Ours BASE        Ours BASE     Ours    BASE    Ours BASE       Ours    BASE    Ours
        VWA ⇑       21.17   56.37 46.35    59.91 46.35      51.36 27.76    39.40   32.87   43.82 31.90     48.97   45.14   57.53
FOLIO OA ⇑          79.31   77.59 68.97    74.14 71.70      73.28 48.28    45.69   48.28   54.31 59.48     65.52   75.00   75.00
        UR ⇓        75.63   27.79 34.74    19.76 38.75      31.90 41.85    17.45   33.75   26.72 47.65     28.41   42.09   28.00
        VWA ⇑       31.09   39.08 46.38    87.21 30.10      44.32 11.89    19.07   16.12   22.74 35.25     50.52   39.50   53.89
ESNLI   OA ⇑        66.67   66.67 86.05    100.00 65.12     63.57 22.48    21.71   31.01   31.01 60.47     64.34   68.22   65.89
        UR ⇓        52.84   42.96 45.87    12.79 53.36      29.46 38.45    11.18   35.84   21.64 40.71     23.58   40.61   15.67
        VWA ⇑       24.91   20.36 34.33    44.98 24.30      40.23 25.97    44.72   28.11   36.27 24.81     40.38   29.17   46.70
LogiQA OA ⇑         62.50   65.91 61.93    54.55 50.86      55.11 46.02    50.00   44.32   46.02 51.70     51.70   55.11   62.50
        UR ⇓        63.07   68.56 46.26    16.05 54.82      31.70 42.25    12.47   39.62   23.48 50.17     25.20   50.43   27.22
        VWA ⇑       35.71   52.43 78.70    81.29 88.83      89.76 56.64    71.52   57.01   62.60 60.02     82.27   71.67   72.81
Pron.QA OA ⇑        99.00   99.00 90.00    94.00 100.00     100.00 85.00   87.00   68.00   73.00 92.00     97.00   96.00   97.00
        UR ⇓        64.29   46.69 15.05    14.28 11.17      10.24 34.17    20.46   18.89   16.29 35.14     15.73   25.44   24.82
        VWA ⇑       32.45   53.61 40.21    63.82 75.41      78.02 36.65    42.91   19.33   29.02 41.95     53.58   48.35   49.61
PW      OA ⇑        88.44   86.43 54.27    79.90 100.00     99.50 59.80    57.29   27.14   39.20 63.32     66.83   80.40   78.39
        UR ⇓        65.13   36.97 37.45    23.82 24.59      21.47 40.77    29.10   38.31   26.83 38.19     22.35   43.59   38.15
        VWA ⇑       20.78   55.88 54.43    71.35 30.82      43.04 47.89    64.02   25.67   40.64 0.00      0.00    59.09   80.59
QASC    OA ⇑        86.30   91.78 93.15    90.41 61.64      63.01 84.93    75.34   53.42   60.27 87.67     87.67   91.78   94.52
        UR ⇓        76.14   44.12 42.60    23.29 42.58      26.71 44.65    16.30   56.06   33.56 100.00   100.00   37.95   16.67
        VWA ⇑       32.20   25.04 48.38    56.27 33.30      34.14 30.53    42.93   37.68   40.39 38.20     48.82   42.61   50.28
SemEval OA ⇑        93.68   93.68 82.63    82.11 50.79      46.84 60.53    60.53   65.79   64.74 74.74     80.53   81.58   80.00
        UR ⇓        63.77   73.98 40.89    32.89 40.44      33.84 50.91    32.15   43.29   36.18 52.10     41.01   48.35   36.44
        VWA ⇑       36.87   23.67 40.51    65.90 39.89      54.46 32.13    57.98   38.81   49.39 36.00     53.52   42.67   57.00
SARA    OA ⇑        77.94   77.21 60.29    73.16 59.93      68.75 52.94    63.60   59.93   58.82 62.50     69.49   65.81   68.38
        UR ⇓        55.04   68.36 32.55    10.81 37.67      20.20 39.10    9.89    37.73   17.51 42.40     24.34   39.33   20.02

Table 1: Benchmark-level Performance Comparison of VWA%, OA%, and UR% between BASE and LogicTrack (Ours) across
Eight Reasoning Data Benchmarks and Seven Models.


3.3   Ablation Study of LogicTrack                                 the solver reward alone achieves 23.4% VWA and 12.9%
                                                                   OA gains over the baseline, while reducing the unverified
We perform an ablation study on SARA with both open-source         ratio from 32.55% to 15.78%. On Llama-8B, it delivers an
and proprietary LLMs to examine the effects of different           identical ∆VWA of 25.4% and brings the unverified step
reward designs and model backtracking strategies on the            ratio down from 39.10% to 7.89%. These results align with
performance of LogicTrack.                                         our expectation that the solver reward directly incentivizes
   Effectiveness of SBR reward. Table 2a ablates the contri-       the model to produce structurally valid, executable reasoning
bution of each SBR component: fidelity reward only Rfidelity ,     steps, which are precisely what VWA and UR measure.
solver reward only Rverify , and the full SBR reward. The             Combining both rewards (SBR) yields the best VWA for
fidelity reward Rfidelity yields stronger outcome-based metric     both models with ∆VWA of 25.4% and 25.9% over the base-
gains, with a ∆OA of 10.7% on GPT-4o-mini and 11% on               line, as well as the lowest UR on GPT-4o-mini at 10.81%.
Llama-8B. Yet its effect on metrics that require step-level        On Llama-8B, adding both rewards further lifts OA from
verification is far more modest. For instance, on the VWA          62.50% to 63.60%, confirming that these two signals are com-
metric, fidelity reward improves over the baseline by 5.4% on      plementary. Rverify incentivizes structural correctness while
GPT-4o-mini and a mere 0.4% on Llama-8B. In contrast, the          Rfidelity enforces factual grounding, and together they cover
solver reward alone achieves VWA improvements exceeding            both dimensions of high-quality structural logical reasoning.
20% on both models. This suggests that grounding each step            Backtracking Search Strategy Variants. Table 2b com-
in the given premises helps the model avoid certain flawed         pares three search strategies, including default greedy back-
steps and therefore contributes positively to final answer         tracking, beam search, and Monte Carlo Tree Search. The
correctness. However, improving step-level verifiability still     default strategy achieves the highest VWA and lowest UR
requires other reward signals. This gap supports the design        across both models. On GPT-4o-mini, it yields a ∆VWA of
choice of using solver feedback as a separate reward term.         25.4% and ∆OA of 12.9% over the baseline, with UR reduced
   This is validated by the results showing that reward Rverify    to 10.81%. Beam search and MCTS improve VWA by only
greatly improved the VWA performance. On GPT-4o-mini,              14.4% and 12.6% respectively and retain higher unverified
                (a) SBR Reward Component Ablation                             (b) Backtracking Search Strategy Variants
 Model       Method        VWA ⇑   ∆VWA ⇑   OA ⇑    ∆OA ⇑   UR ⇓     Model    Method   VWA ⇑   ∆VWA ⇑     OA ⇑    ∆OA ⇑   UR ⇓
  gpt-     Fidelity Only   45.80    5.3     70.96    10.7   37.19     gpt-    Beam     54.87      14.4    69.12     8.8   23.79
   4o       Solver Only    63.96    23.4    73.16    12.9   15.78     4o-     MCTS     53.06      12.6    72.06    11.8   26.84
  mini      SBR (Both)     65.90    25.4    73.16    12.9   10.81     mini    Main     65.90      25.4    73.16    12.9   10.81
 Llama-    Fidelity Only   32.49    0.4     63.97    11.0   48.83    Llama-   Beam     56.71      24.6    65.44    12.5   12.88
   3.1      Solver Only    57.55    25.4    62.50     9.6   7.89      3.1-    MCTS     56.19      24.1    64.34    11.4   13.54
   8B       SBR (Both)     57.98    25.9    63.60    10.7   9.89       8B     Main     57.98      25.9    63.60    10.7   9.89

Table 2: Ablation Study of LogicTrack. (a) SBR reward component ablation. (b) Backtracking search strategy variants. The ∆
values report the absolute improvement (%) over the BASE model.




Figure 4: OA ⇑ and VWA ⇑ under BASE, LogicTrack, and LogicTrack-SFT averaged over all datasets. LogicTrack-SFT refers to
the model fine-tuned on LogicTrack-generated train data.


ratios of 23.79% and 26.84%. On Llama-8B, all three strate-         generalize beyond what inference-time search alone achieves.
gies converge in VWA improvement at 25.9%, 24.6%, and                  SFT partially transfers step-level verification capability,
24.1%, yet the greedy strategy still achieves the lowest UR at      though inference-time LogicTrack retains the advantage.
9.89%, compared to 12.88% and 13.54%.                               Figure 4b shows that SFT also improves step-level quality:
   This advantage can be attributed to the greedy strategy’s        VWA increases over the base model from 32.12% to 39.24%
mechanism of immediate verification feedback: a failed step         on Llama-8B, from 31.86% to 34.62% on Mistral-7B, and
triggers the instant delivery of the solver’s audit log and         from 35.07% to 38.46% on Qwen-7B, showing that Logic-
regeneration from the exact failure position, whereas beam          Track trajectories can transfer partial verification capability
search and MCTS distribute their search budget across parallel      into the model’s intrinsic reasoning. However, inference-time
candidates. Notably, MCTS achieves a higher ∆OA than                LogicTrack still achieves the highest VWA, reaching 47.17%,
beam search on GPT-4o-mini, at 11.8% compared with 8.8%.            40.25%, and 49.42% on the three models respectively. This
This suggests that broader exploration improves final-answer        gap shows that keeping the solver in the loop at inference
correctness, albeit at the expense of step-level verifiability.     time provides stronger step-level guarantees.
                                                                       Better performance than other state-of-the-art tuning
3.4      Extended Application of LogicTrack on SFT                  methods. Monitoring reasoning trajectories remains an under-
LogicTrack operates at inference time to improve step-level         explored area, and the work most closely related to ours is
verification of model reasoning. We further extend it to the        LogicReward (Xu et al. 2025b). LogicReward designs a solver-
construction of fine-tuning datasets, exploring its potential for   based reward to score multiple responses for each problem and
producing self-backtracking SFT data. We first report overall       then uses the top responses to construct training data for SFT
performance after SFT, then present case studies that compare       and DPO. Table 3 compares LogicReward with two variants of
reasoning steps before and after backtracking to show the           LogicTrack in terms of average performance across datasets.
effectiveness of the fine-tuning.                                   The results show that our methods achieve stronger overall
   LogicTrack-SFT surpasses inference-time LogicTrack               performance: inference-time LogicTrack improves OA from
on answer correctness. As shown in Figure 4a, models                0.4338 to 0.5765 and VWA from 0.2656 to 0.4782, while
fine-tuned on LogicTrack backtracking trajectories achieve          LogicTrack-SFT further achieves the best OA of 0.6808. The
the highest OA across all models. Compared with inference-          full dataset-level results in Table 3 also show that LogicTrack
time LogicTrack, SFT improves OA from 56.81% to 68.08%              reduces UR from 0.4089 to 0.1863. Since both LogicReward
on Llama-8B, from 52.75% to 63.11% on Mistral-7B, and               and LogicTrack-SFT rely on SFT, this improvement suggests
from 70.60% to 71.16% on Qwen-7B. This suggests that                that LogicTrack constructs higher-quality SFT training data.
training on solver-verified trajectories with explicit backtrack       To isolate the contribution of adding explicit backtracking
tokens enables the model to internalize reasoning patterns that     supervision to training samples, we trained LogicTrack-SFT-
Metric     LogicReward (Xu et al. 2025b)   LogicTrack   LogicTrack-SFT   et al. 2026; Calanzone, Teso, and Vergari 2024; Lightman
OA ↑                 0.4338                  0.5765         0.6808       et al. 2023; Wang et al. 2024). However, the criteria used
VWA ↑                0.2656                  0.4782         0.3924
                                                                         to assess reasoning quality generally lack formal grounding.
                                                                         Outcome-based critics evaluate only final-answer correct-
Table 3: Performance comparison among LogicReward and
                                                                         ness, while process-level critics rely on human annotations or
LogicTrack. Full comparisons are in Table 6 of Appendix C.
                                                                         LLM-generated judgments, limiting verifiability and allowing
                                                                         subtle logical errors to go undetected. To address this, we
                                                                         define intermediate-step reasoning quality based on whether
                                                                         each step is logically supported by deterministic step-level
                                                                         feedback from solver verification.

                                                                         4.2   LLM Reasoning Chain Verification
                                                                         Recent work increasingly combines LLMs with verifica-
                                                                         tion mechanisms to improve soundness of model-generated
                                                                         reasoning (Cheng et al. 2025; Liu et al. 2025). Existing ap-
                                                                         proaches generally fall into two broad paradigms: formalizing
                                                                         LLM-generated responses and verifying them with external
                                                                         solvers (Olausson et al. 2023; Pan et al. 2023), or treating
                                                                         LLMs themselves as symbolic provers (Xu et al. 2025a, 2024).
                                                                         This work focuses on external solver-based approaches, as
                                                                         they provide a more explicit and controllable verification
                                                                         signal than self-verification. Within this paradigm, (Zhang,
                                                                         Valentino, and Freitas 2025; Ranaldi, Valentino, and Freitas
                                                                         2025) discuss efficient auto-formalization; (Xu et al. 2026)
                                                                         study adaptive solver selection; (Quan et al. 2024, 2025)
                                                                         use solver feedback for iterative refinement. These works
Figure 5: Effectiveness of backtracking supervision in                   mainly target reasoning tasks close to formal representa-
LogicTrack-SFT on Qwen2.5-7B. The VWA ↑ and UR ↓                         tions, or highly structured domains such as mathematics and
comparison across inference-time LogicTrack, LogicTrack-                 programming (Ren et al. 2025), where complete responses
SFT-BT, and LogicTrack-SFT-NoBT.                                         can be directly passed to a solver for verification. Step-level
                                                                         verification for general natural language reasoning remains
                                                                         under-explored, as it requires independently formalizing and
NoBT, a control model trained on data without backtracking               checking each intermediate chain rather than one-off final
traces. As shown in Figure 5, models fine-tuned with Logic-              answer verification. In contrast, LogicTrack verifies the sym-
Track backtracking trajectory data consistently achieve higher           bolic formalization induced from each NL reasoning step and
VWA and lower UR than LogicTrack-SFT-NoBT across all                     backtracks at the first failed step, preventing local errors from
benchmarks. These results confirm that the observed gains                propagating through the full reasoning chain.
are not only a generic effect of SFT on correct trajecto-
ries. The better performance of LogicTrack-SFT-BT over                                         5    Conclusion
LogicTrack-SFT-NoBT demonstrates that incorporating back-                We presented LogicTrack, a neuro-symbolic framework for
tracking trajectories provides additional supervision and can            generation-time auditing of LLM reasoning trajectories. Log-
effectively enhance fine-tuned model performance.                        icTrack decomposes each step into explicit context, expla-
                                                                         nations, and conclusions. Following standard practice in
                       4     Related Work                                solver-based verification, LogicTrack uses autoformalization
                                                                         as a modular interface that maps NL reasoning steps to solver-
4.1      LLM Reasoning Capability Enhancement                            executable logical specifications. Finally, LogicTrack uses the
Many methods have been proposed to improve LLM rea-                      Solver-based Backtracking Reward (SBR) to combine premise
soning patterns, and they can be broadly categorized into                fidelity with solver feedback for online backtracking and regen-
training-based and training-free approaches. Training-free ap-           eration. Across eight reasoning benchmarks and seven LLMs,
proaches improve reasoning quality during inference without              LogicTrack substantially improves step-level verifiability and
updating parameters, including prompting strategies (Wang                generally preserves or improves final-answer accuracy, with
et al. 2022; Wei et al. 2022), search-based methods (Yang                ablations showing that solver verification drives most of the
et al. 2025b; Yao et al. 2023b), and external knowledge                  gains. LogicTrack backtracking traces also serve as useful
augmentation (Peng et al. 2023). Training-based methods                  supervision for fine-tuning open-source models, improving
design rewards to identify high-quality reasoning data for               both final answer accuracy and verification performance over
fine-tuning (Gulcehre et al. 2023; Zelikman et al. 2022), or to          the base models. Future work on autoformalization optimaza-
incorporate these rewards into the training objective (Luong             tion, verification reward variants, backtracking strategies,
et al. 2024). Reward designs include outcome-based and                   and fine-tuning approaches that enable LLMs to internalize
process-level critics that attend to intermediate steps (Yue             verification capabilities will be valuable.
                        References                                  Jaech, A.; Kalai, A.; Lerer, A.; Richardson, A.; El-Kishky,
AI, M. 2024. The Llama 3 Herd of Models. CoRR,                      A.; Low, A.; Helyar, A.; Madry, A.; Beutel, A.; Carney,
abs/2407.21783.                                                     A.; et al. 2024. Openai o1 system card. arXiv preprint
                                                                    arXiv:2412.16720.
An, S.; Ma, Z.; Lin, Z.; Zheng, N.; Lou, J.-G.; and Chen, W.
                                                                    Jiang, A. Q.; Sablayrolles, A.; Mensch, A.; Bamford, C.;
2023. Learning From Mistakes Makes LLM Better Reasoner.
                                                                    Chaplot, D. S.; de las Casas, D.; Bressand, F.; Lengyel, G.;
arXiv preprint arXiv:2310.20689.
                                                                    Lample, G.; Saulnier, L.; Lavaud, L. R.; Lachaux, M.-A.;
Calanzone, D.; Teso, S.; and Vergari, A. 2024. Logically            Stock, P.; Scao, T. L.; Lavril, T.; Wang, T.; Lacroix, T.; and
consistent language models via neuro-symbolic integration.          Sayed, W. E. 2023. Mistral 7B. arXiv:2310.06825.
arXiv preprint arXiv:2409.13724.                                    Khalifa, M.; Logeswaran, L.; Lee, M.; Lee, H.; and Wang,
Camburu, O.-M.; Rocktäschel, T.; Lukasiewicz, T.; and Blun-         L. 2023. Grace: Discriminator-guided chain-of-thought rea-
som, P. 2018. e-snli: Natural language inference with natural       soning. In Findings of the Association for Computational
language explanations. Advances in Neural Information Pro-          Linguistics: EMNLP 2023, 15299–15328.
cessing Systems, 31.                                                Khot, T.; Clark, P.; Guerquin, M.; Jansen, P.; and Sabharwal,
Cheng, F.; Li, H.; Liu, F.; van Rooij, R.; Zhang, K.; and Lin,      A. 2020. Qasc: A dataset for question answering via sentence
Z. 2025. Empowering LLMs with Logical Reasoning: A                  composition. In Proceedings of the AAAI Conference on
Comprehensive Survey. In Proceedings of the International           Artificial Intelligence, volume 34, 8082–8090.
Joint Conference on Artificial Intelligence, 10400–10408.           Lightman, H.; Kosaraju, V.; Burda, Y.; Edwards, H.; Baker,
Comanici, G.; Bieber, E.; Schaekermann, M.; Pasupat, I.;            B.; Lee, T.; Leike, J.; Schulman, J.; Sutskever, I.; and Cobbe,
Sachdeva, N.; Dhillon, I.; Blistein, M.; Ram, O.; Zhang,            K. 2023. Let’s verify step by step. In The twelfth international
D.; Rosen, E.; et al. 2025. Gemini 2.5: Pushing the fron-           conference on learning representations.
tier with advanced reasoning, multimodality, long context,          Liu, H.; Fu, Z.; Ding, M.; Ning, R.; Zhang, C.; Liu, X.;
and next generation agentic capabilities. arXiv preprint            and Zhang, Y. 2025. Logical Reasoning in Large Language
arXiv:2507.06261.                                                   Models: A Survey. CoRR, abs/2502.09100.
Feng, Y.; Weir, N.; Bostrom, K.; Bayless, S.; Cassel, D.;           Liu, J.; Cui, L.; Liu, H.; Huang, D.; Wang, Y.; and Zhang,
Chaudhary, S.; Kiesl-Reiter, B.; and Rangwala, H. 2025. Veri-       Y. 2020. Logiqa: A challenge dataset for machine read-
CoT: Neuro-symbolic Chain-of-Thought Validation via Logi-           ing comprehension with logical reasoning. arXiv preprint
cal Consistency Checks. arXiv preprint arXiv:2511.04662.            arXiv:2007.08124.
Gao, L.; Madaan, A.; Zhou, S.; Alon, U.; Liu, P.; Yang, Y.;         Lu, P.; Mishra, S.; Xia, T.; Qiu, L.; Chang, K.-W.; Zhu,
Callan, J.; and Neubig, G. 2023. Pal: Program-aided language        S.-C.; Tafjord, O.; Clark, P.; and Kalyan, A. 2022. Learn
models. In International conference on machine learning,            to explain: Multimodal reasoning via thought chains for
10764–10799. PMLR.                                                  science question answering. Advances in neural information
Gulcehre, C.; Paine, T. L.; Srinivasan, S.; Konyushkova, K.;        processing systems, 35: 2507–2521.
Weerts, L.; Sharma, A.; Siddhant, A.; Ahern, A.; Wang, M.;          Luong, T. Q.; Zhang, X.; Jie, Z.; Sun, P.; Jin, X.; and Li, H.
Gu, C.; et al. 2023. Reinforced self-training (rest) for language   2024. Reft: Reasoning with reinforced fine-tuning. arXiv
modeling. arXiv preprint arXiv:2308.08998.                          preprint arXiv:2401.08967.
Guo, D.; Yang, D.; Zhang, H.; Song, J.; Wang, P.; Zhu, Q.;          Olausson, T.; Gu, A.; Lipkin, B.; Zhang, C.; Solar-Lezama,
Xu, R.; Zhang, R.; Ma, S.; Bi, X.; et al. 2025. Deepseek-r1:        A.; Tenenbaum, J.; and Levy, R. 2023. LINC: A neurosym-
Incentivizing reasoning capability in llms via reinforcement        bolic approach for logical reasoning by combining language
learning. arXiv preprint arXiv:2501.12948.                          models with first-order logic provers. In Proceedings of the
                                                                    2023 Conference on Empirical Methods in Natural Language
Han, S.; Schoelkopf, H.; Zhao, Y.; Qi, Z.; Riddell, M.; Zhou,       Processing, 5153–5176.
W.; Coady, J.; Peng, D.; Qiao, Y.; Benson, L.; et al. 2024.
                                                                    Pan, L.; Albalak, A.; Wang, X.; and Wang, W. 2023. Logic-
Folio: Natural language reasoning with first-order logic. In
                                                                    LM: Empowering Large Language Models with Symbolic
Proceedings of the 2024 Conference on Empirical Methods
                                                                    Solvers for Faithful Logical Reasoning. In Findings of the
in Natural Language Processing, 22017–22031.
                                                                    Association for Computational Linguistics: EMNLP 2023,
Holzenberger, N.; Blair-Stanek, A.; and Van Durme, B. 2020.         3806–3824.
A dataset for statutory reasoning in tax law entailment and         Peng, B.; Galley, M.; He, P.; Cheng, H.; Xie, Y.; Hu, Y.;
question answering. arXiv preprint arXiv:2005.05257.                Huang, Q.; Liden, L.; Yu, Z.; Chen, W.; et al. 2023. Check
Huang, J.; and Chang, K. C.-C. 2023. Towards reasoning              your facts and try again: Improving large language models
in large language models: A survey. In Findings of the              with external knowledge and automated feedback. arXiv
association for computational linguistics: ACL 2023, 1049–          preprint arXiv:2302.12813.
1065.                                                               Quan, X.; Valentino, M.; Dennis, L. A.; and Freitas, A.
Hurst, A.; Lerer, A.; Goucher, A. P.; Perelman, A.; Ramesh,         2024. Verification and Refinement of Natural Language
A.; Clark, A.; Ostrow, A.; Welihinda, A.; Hayes, A.; Rad-           Explanations through LLM-Symbolic Theorem Proving. In
ford, A.; et al. 2024. Gpt-4o system card. arXiv preprint           Proceedings of the Conference on Empirical Methods in
arXiv:2410.21276.                                                   Natural Language Processing, 2933–2958.
Quan, X.; Valentino, M.; Dennis, L. A.; and Freitas, A. 2025.    Xu, J.; Fei, H.; Luo, M.; Liu, Q.; Pan, L.; Wang, W. Y.; Nakov,
Faithful and Robust LLM-Driven Theorem Proving for NLI           P.; Lee, M.-L.; and Hsu, W. 2025a. Aristotle: Mastering logical
Explanations. In Proceedings of the Annual Meeting of the        reasoning with a logic-complete decompose-search-resolve
Association for Computational Linguistics, 17734–17755.          framework. In Proceedings of the 63rd Annual Meeting of the
Ranaldi, L.; Valentino, M.; and Freitas, A. 2025. Improving      Association for Computational Linguistics (Volume 1: Long
chain-of-thought reasoning via quasi-symbolic abstractions.      Papers), 3052–3075.
In Proceedings of the 63rd Annual Meeting of the Association     Xu, J.; Fei, H.; Pan, L.; Liu, Q.; Lee, M.-L.; and Hsu, W. 2024.
for Computational Linguistics (Volume 1: Long Papers),           Faithful Logical Reasoning via Symbolic Chain-of-Thought.
17222–17240.                                                     In Proceedings of the Annual Meeting of the Association for
                                                                 Computational Linguistics, 13326–13365.
Ren, Z.; Shao, Z.; Song, J.; Xin, H.; Wang, H.; Zhao, W.;
Zhang, L.; Fu, Z.; Zhu, Q.; Yang, D.; et al. 2025. Deepseek-     Xu, J.; Fei, H.; Zhou, H.; Quan, X.; Huang, Q.; Wu, S.; Wang,
prover-v2: Advancing formal mathematical reasoning via           W. Y.; Lee, M.-L.; and Hsu, W. 2025b. LogicReward: Incen-
reinforcement learning for subgoal decomposition. arXiv          tivizing LLM Reasoning via Step-Wise Logical Supervision.
preprint arXiv:2504.21801.                                       arXiv preprint arXiv:2512.18196.
Saparov, A.; and He, H. 2023. Language Models Are                Xu, L.; Beckmann, P.; Valentino, M.; and Freitas, A. 2026.
Greedy Reasoners: A Systematic Formal Analysis of Chain-         Adaptive llm-symbolic reasoning via dynamic logical solver
of-Thought. In Proceedings of the International Conference       composition. In Proceedings of the 19th Conference of the
on Learning Representations.                                     European Chapter of the Association for Computational
                                                                 Linguistics (Volume 1: Long Papers), 1187–1208.
SemEval-2026 Team. 2026. SemEval-2026 Task 11: Disentan-
                                                                 Yang, A.; Zhang, B.; Hui, B.; Gao, B.; Yu, B.; Li, C.; Liu,
gling Content and Formal Reasoning in Large Language Mod-
                                                                 D.; Tu, J.; Zhou, J.; Lin, J.; et al. 2024. Qwen2. 5-math
els. https://sites.google.com/view/semeval-2026-task-11. Ac-
                                                                 technical report: Toward mathematical expert model via self-
cessed: 2026-03-28.
                                                                 improvement. arXiv preprint arXiv:2409.12122.
Singh, A.; Fry, A.; Perelman, A.; Tart, A.; Ganesh, A.; El-      Yang, X.-W.; Zhu, X.-Y.; Wei, W.-D.; Zhang, D.-C.; Shao,
Kishky, A.; McLaughlin, A.; Low, A.; Ostrow, A.; Ananthram,      J.-J.; Zhou, Z.; Guo, L.-Z.; and Li, Y.-F. 2025a. Step back
A.; et al. 2025. Openai gpt-5 system card. arXiv preprint        to leap forward: Self-backtracking for boosting reasoning of
arXiv:2601.03267.                                                language models. arXiv preprint arXiv:2502.04404.
Singh, V.; Cassel, D.; Weir, N.; Feng, N.; and Bayless, S.       Yang, X.-W.; Zhu, X.-Y.; Wei, W.-D.; Zhang, D.-C.; Shao,
2026. VERGE: Formal Refinement and Guidance Engine for           J.-J.; Zhou, Z.; Guo, L.-Z.; and Li, Y.-F. 2025b. Step Back to
Verifiable LLM Reasoning. arXiv preprint arXiv:2601.20055.       Leap Forward: Self-Backtracking for Boosting Reasoning of
Tafjord, O.; Dalvi, B.; and Clark, P. 2021. Proofwriter:         Language Models. arXiv preprint arXiv:2502.04404.
Generating implications, proofs, and abductive statements        Yao, S.; Yu, D.; Zhao, J.; Shafran, I.; Griffiths, T.; Cao, Y.;
over natural language. In Findings of the Association for        and Narasimhan, K. 2023a. Tree of thoughts: Deliberate
Computational Linguistics: ACL-IJCNLP 2021, 3621–3634.           problem solving with large language models. Advances in
Turpin, M.; Michael, J.; Perez, E.; and Bowman, S. 2023.         neural information processing systems, 36: 11809–11822.
Language models don’t always say what they think: Unfaithful     Yao, S.; Yu, D.; Zhao, J.; Shafran, I.; Griffiths, T.; Cao, Y.;
explanations in chain-of-thought prompting. Advances in          and Narasimhan, K. 2023b. Tree of thoughts: Deliberate
Neural Information Processing Systems, 36: 74952–74965.          problem solving with large language models. Advances in
Wang, P.; Li, L.; Shao, Z.; Xu, R.; Dai, D.; Li, Y.; Chen,       neural information processing systems, 36: 11809–11822.
D.; Wu, Y.; and Sui, Z. 2024. Math-shepherd: Verify and          Ye, T.; Xu, Z.; Li, Y.; and Allen-Zhu, Z. 2024. Physics
reinforce llms step-by-step without human annotations. In        of Language Models: Part 2.2, How to Learn From Mis-
Proceedings of the 62nd Annual Meeting of the Association        takes on Grade-School Math Problems. arXiv preprint
for Computational Linguistics (Volume 1: Long Papers),           arXiv:2408.16293.
9426–9439.                                                       Yue, C.; Dong, C.; Gao, Y.; He, H.; Chai, J.; Lin, W.; and
Wang, X.; Wei, J.; Schuurmans, D.; Le, Q.; Chi, E.; Narang,      Yin, G. 2026. Promoting efficient reasoning with verifiable
S.; Chowdhery, A.; and Zhou, D. 2022. Self-consistency           stepwise reward. In Proceedings of the AAAI Conference on
improves chain of thought reasoning in language models.          Artificial Intelligence, volume 40, 34530–34538.
arXiv preprint arXiv:2203.11171.                                 Zelikman, E.; Wu, Y.; Mu, J.; and Goodman, N. 2022. Star:
Wei, J.; Wang, X.; Schuurmans, D.; Bosma, M.; Xia, F.; Chi,      Bootstrapping reasoning with reasoning. Advances in Neural
E.; Le, Q. V.; Zhou, D.; et al. 2022. Chain-of-thought prompt-   Information Processing Systems, 35: 15476–15488.
ing elicits reasoning in large language models. Advances in      Zhang, L.; Valentino, M.; and Freitas, A. 2025. MASA:
neural information processing systems, 35: 24824–24837.          LLM-driven multi-agent systems for autoformalization. In
                                                                 Proceedings of the 2025 Conference on Empirical Methods
Xie, Y.; Kawaguchi, K.; Zhao, Y.; Zhao, J. X.; Kan, M.-Y.;
                                                                 in Natural Language Processing: System Demonstrations,
He, J.; and Xie, M. 2023. Self-evaluation guided beam search
                                                                 615–624.
for reasoning. Advances in Neural Information Processing
Systems, 36: 41618–41650.
  A     Appendix A: Methods Implementation                          backtracking points. A rejected step at position k is kept only
                                                                    when its prefix up to step k − 1 matches the verified path.
A.1    Backtracking Search Strategies
                                                                    This keeps the error local and avoids trajectories that have
This section provides additional implementation details for         already diverged earlier.
the search-strategy ablation in Table 2(b). We compare three           We then construct three kinds of training trajectories:
variants: the default greedy backtracking search used in the         • Single backtracking correction. One wrong step is fol-
main experiments, beam search, and Monte Carlo Tree Search              lowed by a dedicated backtracking token and then the
(MCTS).                                                                verified continuation:
Default Search The default search is the greedy backtrack-                                   −
                                                                              s+        +                   +        +
                                                                               1 · · · sk−1 sk <backtrack> sk · · · sn ŷ .
ing strategy used throughout the main experiments and the
implementation is described in Section 2.2. Its step-level ac-       • Multiple backtracking corrections. These trajectories
ceptance threshold is set to θstep = 0.8, the running-average           contain two or more corrections at different step positions.
threshold is set to θavg = 0.5. The maximum number of regen-            We prefer cases whose wrong continuation ends with an
eration attempts per step position is k = 2. If all k attempts          incorrect final answer.
fail, the candidate with the highest SBR is force-forwarded          • Clean correct trajectories. These trajectories contain all
to guarantee forward progress.                                          verified steps and provide positive examples.
Beam Search Beam search maintains a frontier of B partial              During fine-tuning, we add <backtrack> as the new vo-
reasoning paths and expands all of them in parallel at each         cabulary item. The model learns to emit this token when a step
layer. At each layer, every frontier path contributes up to         is wrong and then continue with a corrected path, without rely-
k = 2 continuation branches: if the path carries a pending          ing on an external verifier at inference time. The final training
tail from a prior generation, its leading provisional step is       set contains ∼6,000 samples across the three trajectory types.
consumed as one free branch; the remaining slots are filled by      We fine-tune three large language models on the constructed
fresh LLM completions conditioned on the current verified           SFT dataset: Qwen2.5-7B-Instruct, Mistral-7B-Instruct-v0.3,
prefix. All verification tasks are dispatched concurrently. After   and Llama-3.1-8B-Instruct. We use LoRA supervised fine-
verification, nodes with SBR(st ) < 0.75 are pruned; the top-       tuning for 2 epochs with rank 32 and scaling factor 64.
B survivors ranked by path-average SBR advance to the               Training uses bfloat16 and AdamW (adamw_torch) with
next layer. If all candidates are pruned, the best low-reward       a learning rate of 3 × 10−5 , a linear scheduler, warmup ratio
node is reactivated to guarantee forward progress. The search       0.05, and gradient clipping with maximum norm 0.3. The
terminates as soon as the top frontier node yields a complete       per-device batch size is 2 and the effective batch size is 16.
reasoning chain; otherwise the best node found is returned.         We also enable gradient checkpointing and save checkpoints
                                                                    every 50 steps.
Monte Carlo Tree Search We follow the standard MCTS
framework, repeating four stages each iteration. During selec-            B     Appendix B: Experimental Settings
tion, the algorithm traverses from the root by choosing at each
node the child with the highest UCB score, which balances           B.1    Datasets
the mean backpropagated SBR against an exploration bonus,           We evaluate on eight reasoning benchmarks. For e-SNLI, FO-
until it reaches a node with fewer than k children. During          LIO, LogiQA, ProntoQA, ProofWriter, and QASC, we adopt
expansion, up to k fresh LLM completions are generated              the processed releases used in LogicReward (Xu et al. 2025b).
from the selected node. The first step st of each completion        We then resplit their released ‘data.jsonl‘ into training and test
is verified and attached as a new child. A child is marked ter-     subsets with the ratio of 4 : 1. All fine-tuning experiments are
minal if SBR(st ) = 0, if the reasoning chain is complete, or       based on the training dataset. For SemEval (SemEval-2026
if a depth limit is reached. During rollout, each non-terminal      Team 2026), Task 2 is used for testing and the English portion
child whose SBR(st ) ≥ θ is extended by consuming the               of Task 4 is used for training. For SARA (Holzenberger, Blair-
remaining provisional steps from the same generation, verify-       Stanek, and Van Durme 2020), we follow the instructions
ing each in turn without additional LLM calls, until the chain      from (Feng et al. 2025) and use the instances from SARA
terminates or a step falls below θ. During backpropagation,         Entailment in the testing stage only. We briefly summarize
the path-average SBR of the reached leaf is propagated back         the benchmarks below.
to the root, updating each ancestor’s statistics. After a fixed      • e-SNLI (Camburu et al. 2018) extends SNLI with human-
number of iterations the best complete leaf is returned, or, if         annotated natural language explanations for premise–
none exists, the best leaf overall.                                     hypothesis pairs.
                                                                     • FOLIO (Han et al. 2024) is a human-annotated benchmark
A.2    Backtracking SFT                                                 for natural language reasoning with accompanying first-
We build the SFT data from backtracking traces produced                 order logic annotations that are automatically verified by
by LogicTrack. For each training example, we keep only                  an inference engine.
cases whose final answer is correct and whose reasoning              • LogiQA (Liu et al. 2020) is originally a multiple-choice
steps pass both syntactic and semantic verification. From               reading comprehension benchmark for logical reasoning
each trace, we extract the verified path s+ = (s+            +
                                                1 , . . . , sn )        over short passages. We use the preprocessed version from
                                            −
from final_path and the rejected steps {sk } collected at              (Xu et al. 2025b).
 • ProntoQA (Saparov and He 2023) is a synthetic question          GPUs (40 GB or 80 GB) or equivalent GPUs, using PyTorch
   answering benchmark in which each example is generated          2.8 and Python 3.12. The BASE method in this paper is the
   from a synthetic world model represented in first-order         zero-shot strategy that uses the Reasoning Prompt described in
   logic, providing a controlled setting for analyzing multi-      Appendix D. Our LogicTrack method uses the same reasoning
   step deduction.                                                 prompt as the baseline and applies our monitoring mechanism
 • ProofWriter (Tafjord, Dalvi, and Clark 2021) is a syn-          during answer generation. For formal verification, we use
   thetic benchmark over natural-language theories of facts        the ‘gpt-4o-min’ as the autoformalizer backend and Z3 SMT
   and rules, with associated questions and proofs at different    solver as the solver backend. The automatic formalizer and
   reasoning depths.                                               fidelity judge in LogicTrack are both implemented with gpt-
 • QASC (Khot et al. 2020) is an 8-way multiple-choice             4o-mini. Evaluating the intermediate reasoning processes
   science question answering benchmark for question an-           of LLMs remains an underexplored area. To the best of our
   swering via sentence composition.                               knowledge, LogicReward (Xu et al. 2025b) is the only relevant
                                                                   prior work with open-source code. We select it as baseline
 • SARA (Holzenberger, Blair-Stanek, and Van Durme 2020)           and the performance comparison between LogicTrack and
   is a benchmark for statutory reasoning in tax law, with         LogicReward is presented in Appendix C.
   entailment and question answering tasks.
 • SemEval (SemEval-2026 Team 2026) refers to SemEval-             B.3        Metric Definitions
   2026 Task 11 on disentangling content from formal rea-
                                                                   For each problem x, let Tx be the number of reasoning steps
   soning in multilingual syllogistic arguments. We use Task
                                                                   and Kx the number of verified steps, giving the per-problem
   2 for testing and the English portion of Task 4 for training,
                                                                   verification ratio ρx = Kx /Tx .
   and in both cases use the binary validity labels.
                                                                      Outcome Accuracy (OA) is the fraction of examples with
B.2      Models                                                    correct final answers. Verified
                                                                                                P Ratio (VR) is the dataset-
                                                                   average verification ratio N1 x ρx , Unverified Ratio (UR) is
Our experiments cover seven models with diverse architec-
                                                                   the mean fraction of unverified steps N1 x (1 − ρx ).
                                                                                                             P
tures and scales.
                                                                      Verified Utility (VU) is the fraction of all examples for
Proprietary models.                                                which the final answer is correct and the entire reasoning
                                                                                                   PN
 • GPT-4o-mini (Hurst et al. 2024) is a member of the GPT-         trajectory is verified: VU = N1 x=1 1[ŷx = yx ] · 1[ρx = 1].
   4o family that offers strong reasoning performance at low          Verification-Weighted Accuracy (VWA) is defined as
                                                                    1
                                                                      PN
                                                                         x=1 ρx · 1[ŷx = yx ], it weights each correct predic-
   inference cost.                                                 N
 • GPT-5-nano (Singh et al. 2025) is the smallest model in         tion by its per-problem verification ratio.
   the GPT-5 family and is designed for fast and lightweight
   inference.                                                                        C     Appendix C: Results
 • Gemini-2.5-Flash-Lite (Comanici et al. 2025) is a               C.1        More Results of LogicTrack Performance
   lightweight model from the Gemini 2.5 family that bal-
   ances efficiency with strong reasoning ability.                 Table 4 reports the average OA and VU of the base models and
                                                                   LogicTrack across all seven models. Table 5 reports the perfor-
Open weight models.                                                mance of the three LogicTrack-SFT models on each dataset.
 • Llama-3.1-8B-Instruct (AI 2024) is an instruction-tuned         We further compare LogicTrack with LogicReward (Xu et al.
   model with 8B parameters from Meta’s Llama 3.1 family.          2025b) on Llama-8B. LogicReward is based on their released
                                                                   model after SFT and DPO fine-tuning3 . Table 6 compares
 • Mistral-7B-Instruct-v0.3 (Jiang et al. 2023) is an
                                                                   LogicReward, LogicTrack, and LogicTrack-SFT at the dataset
   instruction-tuned model with 7B parameters from Mistral
                                                                   level.
   AI with strong performance relative to its size.
 • Qwen2.5-7B-Instruct (Yang et al. 2024) is an instruction-       C.2        Backtracking Case Study in LogicTrack-SFT
   tuned model with 7B parameters from the Qwen2.5 family.
                                                                   Figure 6 presents two representative examples of self-
 • Qwen2.5-14B-Instruct (Yang et al. 2024) is an instruction-
                                                                   backtracking from LogicTrack-SFT (Qwen2.5-7B). In Ex-
   tuned model with 14B parameters from the same Qwen2.5
                                                                   ample 1, the model makes a non-sequitur by deriving an
   family with stronger reasoning capacity at higher comput-
                                                                   unrelated property instead of continuing the type chain. After
   ing cost.
                                                                   backtracking, it completes the correct deduction. Example 2
Implementations. For all models, the temperature is set            shows an irrelevant derivation in which the model explores an
to 0.7 and the maximum generation length is set to 10240           off-topic property. The model triggers backtracking in these
tokens when answering questions. For proprietary models,           cases and, after backtracking, follows the targeted reasoning
experiments are performed via corresponding OpenAI APIs1           path. These cases highlight LogicTrack-SFT’s internalized
and Gemini APIs2 . For open-weight models, all testing and         backtracking ability and show how it recovers from non-
fine-tuning experiments are conducted on NVIDIA A100               sequitur inferences and unproductive reasoning paths in a
   1                                                                    3
       https://developers.openai.com/api/docs                               https://huggingface.co/Aiden0526/LogicReward-Llama3.1-
   2
       https://ai.google.dev/gemini-api/docs                       8B
               Gemini-2.5           GPT-4o-mini               GPT-5-nano          Llama-3.1-8B            Mistral-7B            Qwen2.5-7B           Qwen2.5-14B
Metric
           Base     LogicTrack   Base     LogicTrack     Base     LogicTrack   Base      LogicTrack   Base      LogicTrack    Base    LogicTrack   Base      LogicTrack

OA ⇑       0.8096     0.8112     0.7068     0.7849      0.6850      0.7044     0.5506      0.5681     0.4964      0.5275     0.6629     0.7060     0.7402      0.7506
VU ⇑       0.1936     0.2725     0.2151     0.4661      0.2607      0.3968     0.0924      0.3275     0.1841      0.2980     0.1633     0.3554     0.2382      0.4143
VWA ⇑      0.3071     0.3693     0.4578     0.6436      0.4527      0.5394     0.3212      0.4717     0.3186      0.4025     0.3507     0.4942     0.4484      0.5573
UR ⇓       0.6273     0.5477     0.3727     0.1898      0.3832      0.2570     0.4171      0.1871     0.3793      0.2476     0.4737     0.3068     0.4213      0.2687


Table 4: Overall performance for all models averaged across eight benchmarks under BASE and LogicTrack. Here OA and VU
correspond to the coordinates used in Figure 3




    Model               Metric       ESNLI            FOLIO          LogiQA           ProntoQA          ProofWriter            QASC         SARA            SemEval

         SFT              OA            0.6047         0.6121         0.5170             0.9900                0.6548          0.8767       0.6324          0.7842
                         VWA            0.3366         0.3412         0.2922             0.8069                0.3654          0.5194       0.4029          0.3004
Llama-3.1-8B
                          UR            0.4012         0.4735         0.4413             0.1856                0.5069          0.4463       0.3836          0.6207

         SFT              OA            0.7984         0.6552         0.6136             0.9700                0.6131          0.8767       0.6360          0.7895
                         VWA            0.4180         0.3329         0.3428             0.6183                0.3302          0.4840       0.4053          0.2982
 Qwen2.5-7B
                          UR            0.4554         0.4825         0.4313             0.3587                0.5335          0.4589       0.3580          0.6433

         SFT              OA            0.4651         0.5862         0.4943             0.9800                0.6432          0.8904       0.5184          0.7632
                         VWA            0.1970         0.3099         0.2846             0.7046                0.3566          0.5057       0.3232          0.2991
  Mistral-7B
                          UR            0.4864         0.5037         0.4380             0.2934                0.5216          0.4372       0.3958          0.6246

         Table 5: Performance of LogicTrack-SFT across different models and datasets. We report OA ↑, VWA ↑, and UR ↓.




                                    OA ↑                                                 VWA ↑                                             UR ↓
Dataset
               LogicReward LogicTrack LogicTrack-SFT LogicReward LogicTrack LogicTrack-SFT LogicReward LogicTrack LogicTrack-SFT

FOLIO               0.3103       0.4569              0.6121           0.1841            0.3940         0.3412              0.4490        0.1745             0.4735
ESNLI               0.0155       0.2171              0.6047           0.0052            0.1907         0.3366              0.2605        0.1118             0.4012
LogiQA              0.3920       0.5000              0.5170           0.2408            0.4472         0.2922              0.3655        0.1247             0.4413
ProntoQA            0.6100       0.8700              0.9900           0.4457            0.7152         0.8069              0.3085        0.2046             0.1856
ProofWriter         0.4121       0.5729              0.6548           0.2130            0.4291         0.3654              0.5150        0.2910             0.5069
QASC                0.6027       0.7534              0.8767           0.3144            0.6402         0.5194              0.4685        0.1630             0.4463
SemEval             0.5105       0.6053              0.7842           0.3222            0.4293         0.3004              0.5778        0.3215             0.6207
SARA                0.6176       0.6360              0.6324           0.3996            0.5798         0.4029              0.3263        0.0989             0.3836


Table 6: Dataset-level comparison among LogicReward, LogicTrack, and LogicTrack-SFT on Llama-3.1-8B. We report OA ↑,
VWA ↑, and UR ↓.
way that is consistent with the solver-guided corrections in          1    Step 1:
LogicTrack training trajectories.                                     2    ##Premises:## Sally is a yumpus; Every
                                                                               yumpus is not opaque; Yumpuses are
Example 1: Non-sequitur inference. Premises: Alex is a tumpus                  zumpuses; Zumpuses are nervous;
⇒ jompus ⇒ dumpus ⇒ zumpus ⇒ yumpus; each yumpus is not                        Every zumpus is a tumpus; Each
cold. Query: Alex is cold. Answer label: False                                 tumpus is not large; Tumpuses are
                                                                               impuses; Impuses are temperate;
                                                                               Impuses are numpuses; Every wumpus
 Before <backtrack>
                                                                               is bitter; Each numpus is not
 Step 4: {C4 , E4 , q4 }, where q4 : “Alex is not a wumpus (since              bitter; Numpuses are vumpuses; Every
 zumpuses are dull and cannot be cold).”                                       vumpus is not kind; Vumpuses are
 ————–                                                                         rompuses; Rompuses are brown;
 × Non-sequitur: “dull” is unrelated to “cold”; the chain must                 Rompuses are jompuses; Every jompus
 reach yumpus.                                                                 is wooden; Every jompus is a dumpus.
                                                                      3    ##Derived Fact:## Sally is a yumpus,
 After <backtrack>                                                             which means she is not opaque.
                                                                               However, we need to determine if she
 Step 4: “Alex is a yumpus (every zumpus is a yumpus).”                        is bitter or not.
 Step 5: “Each yumpus is not cold ⇒ Alex is not cold.”                4    <backtrack>
 ————–                                                                5    Step 1:
 ✓ Answer: False.                                                     6    ##Premises:## Sally is a yumpus; Every
                                                                               yumpus is not opaque; Yumpuses are
Example 2: Irrelevant derivation. Premises: Sally is a yumpus ⇒                zumpuses; Zumpuses are nervous;
zumpus ⇒ numpus; each numpus is not bitter. Query: Sally is not                Every zumpus is a tumpus; Each
bitter. Answer label True                                                      tumpus is not large; Tumpuses are
                                                                               impuses; Impuses are temperate;
                                                                               Impuses are numpuses; Every wumpus
 Before <backtrack>                                                            is bitter; Each numpus is not
                                                                               bitter; Numpuses are vumpuses; Every
 Step 1: {C1 , E1 , q1 }, where q1 :“Sally is a yumpus, which
                                                                               vumpus is not kind; Vumpuses are
 means she is not opaque. But we need to determine if she is bitter
                                                                               rompuses; Rompuses are brown;
 or not.”
                                                                               Rompuses are jompuses; Every jompus
 ————–                                                                         is wooden; Every jompus is a dumpus.
 × Derives irrelevant property (“not opaque”).                        7    ##Derived Fact:## Sally is a yumpus.
                                                                               Since yumpuses are zumpuses and
 After <backtrack>
                                                                               zumpuses are numpuses, we can
 Step 1: “Sally is a yumpus ⇒ zumpus ⇒ numpus.”                                conclude that Sally is also a numpus.
 Step 2: “Each numpus is not bitter ⇒ Sally is not bitter.”           8    Step 2:
 ————–                                                                9    ##Premises:## Sally is a numpus; Each
 ✓ Answer: True.                                                               numpus is not bitter.
                                                                      10   ##Derived Fact:## Sally is not bitter.
                                                                      11   Step 3:
Figure 6: Self-backtracking Examples of LogicTrack-SFT.               12   ##Premises:## The hypothesis states:
Each pair contrasts the flawed step with the corrected contin-                 Sally is not bitter; We have
uation.                                                                        established that Sally is not bitter.
                                                                      13   ##Derived Fact:## The hypothesis
  The examples above displayed the traces in the simplified                    matches the derived fact above.
way. Below displays full settings of Example 2 in Figure 6. It                 Therefore, the claim is true. The
shows the original flawed step that triggers <backtrack>                       final answer is \boxed{True}.
and the regenerated continuation.
Original Given premises. P=’ Every yumpus is not opaque;
Yumpuses are zumpuses; Zumpuses are nervous; Every zum-
                                                                            D    Appendix D: Prompt Templates
pus is a tumpus; Each tumpus is not large; Tumpuses are               This section includes the prompt templates used in our ex-
impuses; Impuses are temperate; Impuses are numpuses; Ev-             periments, including the reasoning prompt, the consistency
ery wumpus is bitter; Each numpus is not bitter; Numpuses             check prompt, and the answer extraction procedure.
are vumpuses; Every vumpus is not kind; Vumpuses are
rompuses; Rompuses are brown; Rompuses are jompuses;
Every jompus is wooden; Every jompus is a dumpus; Sally is
a yumpus.’ Query: Sally is not bitter. Answer label: True
   Model generated answer with backtracking is as follows.
Reasoning Prompt Given a sample x, the reasoning model                System Prompt for Consistency Check
receives a system message instructing it to reason step-by-step
in the structured format described in § 2.1, followed by a user        1   You are a logical consistency
message containing the premises P , query Q, and a dataset-                    checker. Determine whether the
specific answer instruction. The system prompt includes an                     assumption in the reasoning
in-context demonstration and enforces the three-part step                      step conflicts with the
format (Premises, Explanation, Derived Fact).                                  overall context.
                                                                       2
                                                                       3   *Examples*
    System Prompt for Step-by-Step Reasoning                           4   - Consistent: given context
                                                                               contains 'the infant is
     1   You are a meticulous logician.                                        crying, Tom is round', and the
             Read the user's given premise                                     assumption says 'infants are
             and hypothesis carefully, then                                    babies; given context includes
             reason step by step explicitly                                    Tom is round'.
             in a Natural Language                                     5   - Inconsistent: given context
             Inference (NLI) style, and                                        contains 'dog is round, cat is
             conclude with \boxed{LABEL}.                                      green', and the assumption
     2   Do not stop reasoning just because                                    says 'we don't know if cat is
             the current facts do not prove                                    round'. Because it introduces
             the claim. Stop only when the                                     information not grounded in
             claim is settled, or when no                                      the current context.
             unresolved inference path can                             6
             still settle it.                                          7   Respond with a JSON object in this
     3                                                                         exact format:
     4   Each step in the response stage                               8   {"check_result": "consistent",
             must follow the format below,                                     "reason": "..."}
             which contains three sections:                            9   or
             Premises, Assumptions, and                               10   {"check_result": "inconsistent",
             Derived Fact:                                                     "reason": "..."}
     5
     6   **Response Format**                                      Answer Extraction The predicted answer ŷ is extracted
     7   Step X:                                                  from the model’s response via a rule-based procedure. We first
     8   ##Premises:##
     9   - [Facts from the input premises
                                                                  look for the \boxed{...} notation specified in the prompt,
             or prior derived facts.]                             extracting the innermost content and stripping wrappers (e.g.,
   10    - [Don't include any user query or                       \text{}). If no boxed answer is found, we also consider al-
             hypothesis here.]                                    ternative patterns such as <answer>...</answer> tags
   11    ##Explanation:##                                         and common answer-declaration phrases (e.g., “the answer is
   12    - [Add linguistic bridges only                           {LABEL}”) in the final sentences of the response. If none of
             (e.g., synonyms, lexical                             these patterns match, the prediction is marked as unanswered.
             equivalences, definitional
             mappings)]
   13    - [Never use Assumptions to fill
             logical gaps. Write None if no
             assumption is needed]
   14    ##Derived Fact:##
   15    - [The derived fact must be fully
             supported by that step's
             premises and assumptions.]
   16    - [Do not speculate about other
             facts.]
   17
   18    After your final step, output
             exactly your answer with
             \boxed{LABEL}.



Consistency Check Prompt The consistency check de-
scribed in § 2.1 uses an LLM judge to determine whether
the explanations Ei and context Ci conflict with the original
given premises P . The judge is instructed to be lenient, only
flag direct and unambiguous conflicts.
