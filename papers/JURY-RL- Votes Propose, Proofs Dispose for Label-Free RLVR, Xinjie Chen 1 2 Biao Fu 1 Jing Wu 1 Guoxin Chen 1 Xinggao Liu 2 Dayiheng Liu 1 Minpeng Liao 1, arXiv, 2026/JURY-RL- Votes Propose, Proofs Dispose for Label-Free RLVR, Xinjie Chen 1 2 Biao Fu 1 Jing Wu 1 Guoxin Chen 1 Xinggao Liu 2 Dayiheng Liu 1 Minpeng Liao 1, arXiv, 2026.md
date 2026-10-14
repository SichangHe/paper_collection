                                                       JURY-RL: Votes Propose, Proofs Dispose for Label-Free RLVR


                                                  Xinjie Chen 1 2 Biao Fu 1 Jing Wu 1 Guoxin Chen 1 Xinggao Liu 2 Dayiheng Liu 1 Minpeng Liao 1


                                                                   Abstract                                   bottleneck (Wang et al., 2023; Lightman et al., 2024; Patil
                                                                                                              & Jadon, 2025; Huang et al., 2025b). Recent progress in re-
                                                Reinforcement learning with verifiable rewards                inforcement learning with verifiable rewards (RLVR) (Shao
                                                (RLVR) enhances the reasoning of large lan-                   et al., 2024; Lambert et al., 2024; DeepSeek-AI et al., 2025)
                                                guage models (LLMs), but standard RLVR of-
arXiv:2604.25419v1 [cs.AI] 28 Apr 2026




                                                                                                              offers a principled post-training route: rather than rewarding
                                                ten depends on human-annotated answers or care-               what merely appears plausible, RLVR aligns learning with
                                                fully curated reward specifications. In machine-              externally checkable correctness through signals such as
                                                checkable domains, label-free alternatives such as            program execution, unit tests, or mathematical verification
                                                majority voting or LLM-as-a-judge remove anno-                (Cobbe et al., 2021; Yu et al., 2025; AI & Agentica, 2025).
                                                tation cost but can introduce false positives that            However, in many practical settings, RLVR still depends
                                                destabilize training. We introduce JURY-RL, a                 on human-annotated answers or carefully curated reward
                                                label-free RLVR framework that decouples an-                  specifications, both of which are costly to obtain and limited
                                                swer proposal from reward disposal: votes from                in coverage (Ouyang et al., 2022; Bai et al., 2022; Shao
                                                model rollouts propose a candidate answer, and a              et al., 2024).
                                                formal verifier determines whether that candidate
                                                can receive positive reward. Concretely, only roll-           To reduce annotation cost, recent work has explored label-
                                                outs matching the plurality-voted answer are re-              free rewards, where no human ground-truth answers are pro-
                                                warded when that answer is successfully verified              vided during training. A prominent subset is self-supervised
                                                in Lean. When verification is inconclusive, we in-            self-reward, which derives signals from the model or un-
                                                voke ResZero (Residual-Zero), a fallback reward               labeled data itself, including entropy minimization (Prab-
                                                that discards the unverified plurality proposal and           hudesai et al., 2025), self-certainty (Zhao et al., 2025b),
                                                redistributes a zero-mean, variance-preserving sig-           and majority voting (Shafayat et al., 2025; Zhang et al.,
                                                nal over the residual answers. This design main-              2025). These approaches are attractive because they avoid
                                                tains a stable optimization gradient without re-              per-example labels, but they often optimize agreement or
                                                inforcing unverifiable consensus. Across three                confidence rather than verified correctness. As a result, they
                                                backbone models trained on mathematical data,                 are vulnerable to false positives, reward hacking, and train-
                                                JURY-RL consistently outperforms other label-                 ing collapse (Gao et al., 2022; Shafayat et al., 2025). LLM-
                                                free baselines on mathematical reasoning bench-               as-a-Judge (Lee et al., 2024; Su et al., 2025; Zhao et al.,
                                                marks and transfers competitively to code gener-              2025c) provides another label-free path, yet in practice it
                                                ation and general benchmarks. It attains pass@1               remains sensitive to prompting and format manipulation,
                                                performance comparable to supervised ground-                  incurs nontrivial compute overhead, and can inherit shared-
                                                truth training, with superior generalization demon-           model biases (Pang et al., 2023; Chen et al., 2024; Thakur
                                                strated by higher pass@k and response diversity.              et al., 2025; Shi et al., 2025).
                                                                                                              The flaws of existing label-free methods, from reinforcing
                                                                                                              false consensus to reward hacking, are not isolated issues but
                                                                                                              rather symptoms of a deeper challenge. We argue that a truly
                                         1. Introduction                                                      robust reward signal must satisfy three essential properties:
                                         Large language models (LLMs) (OpenAI, 2023; DeepSeek-                (i) scalable without costly human supervision, (ii) truth-
                                         AI et al., 2024; Yang et al., 2025b) continue to advance             aligned, rewarding verifiable correctness instead of error-
                                         in broad capabilities, yet reliable reasoning remains a core         prone consensus, and (iii) optimization-stable, allowing
                                                                                                              learning to proceed even when verification is inconclusive.
                                            1
                                             Tongyi Lab, Alibaba Group, Hangzhou, China 2 Zhejiang Uni-       Previous approaches have, in one degree or another, failed to
                                         versity, Hangzhou, China. Correspondence to: Minpeng Liao            meet all three criteria. Self-supervised signals such as major-
                                         <minpeng.lmp@alibaba-inc.com>.                                       ity voting achieve scalability but sacrifice truth-alignment,
                                                                                                              while LLM-as-a-Judge struggles with both truth-alignment

                                                                                                          1
                                  JURY-RL: Votes Propose, Proofs Dispose for Label-Free RLVR

                                                          Solution     Answer
   Unlabeled Data
                                       Rollout                                      Majority Voting
                            LLM


                   Update
                                   Binary Reward

                                            1
                                                                         Verified
                                            0
                                                                           𝛿=1

                                                                       Inconclusive
                                                                           𝛿=0
               Jury
                                     ResZero
              Judge                  Reward


Figure 1. The JURY-RL workflow: Votes Propose, Proofs Dispose. For each problem, a majority vote from multiple rollouts (Jury)
proposes a candidate answer. A Lean verifier (Judge) then disposes the reward. If the answer is Verified (δ = 1), supporting rollouts
receive a positive reward, directly linking the update to successful formal verification. Conversely, when verification is Inconclusive
(δ = 0), all rollouts receive the proposed ResZero (Residual-Zero) fallback reward.


due to high false positives and optimization instabilities.           proposal and assigns a carefully constructed, zero-mean,
                                                                      variance-preserving reward to the remaining (residual) an-
This motivates our core proposal, a new paradigm designed
                                                                      swers. This design maintains a stable optimization gradient
to resolve this conflict: Votes Propose, Proofs Dispose.
                                                                      for learning to proceed, without amplifying a potentially spu-
Our strategy is to decouple the proposal of a candidate an-
                                                                      rious consensus, ensuring both training stability and truth
swer from the final disposal of its reward. To maintain
                                                                      alignment. By combining proof-gated positive reward with
scalability, votes from model rollouts first propose a sin-
                                                                      a conservative residual fallback, JURY-RL remains trainable
gle consensus candidate through a computationally cheap
                                                                      even when formal verification does not produce a decisive
majority vote 1 . A formal theorem prover (de Moura &
                                                                      signal.
Ullrich, 2021; Ren et al., 2025; Lin et al., 2025) then acts
as a reliable judge to dispose the ultimate reward for this           Contributions. (1) We introduce JURY-RL, a label-free
single candidate, thus satisfying all three principles above.         RLVR framework for machine-checkable settings that de-
This design choice avoids the prohibitive cost of formally            couples candidate proposal from proof-gated reward dis-
verifying every unique answer, thereby making the entire              posal, requiring only a single formal verification call per
framework viable at scale.                                            rollout group. (2) We propose ResZero (Residual-Zero), a
                                                                      zero-mean, variance-preserving fallback reward for incon-
Our framework, JURY-RL, is shown in Figure 1. When
                                                                      clusive verification. It preserves optimization stability while
the plurality-voted answer is successfully verified, only the
                                                                      refusing to positively reinforce an unverified plurality. (3)
rollouts that produced that answer receive positive reward.
                                                                      Across mathematical reasoning, code generation, and multi-
This suppresses the false-positive reinforcement common
                                                                      task benchmarks, JURY-RL trains more stably and achieves
in consensus- or judge-based surrogates. A remaining chal-
                                                                      state-of-the-art results among label-free methods, matching
lenge is how to learn when verification is inconclusive. Re-
                                                                      a strong supervised ground-truth baseline in pass@1 while
warding the plurality would reintroduce the very failure
                                                                      consistently surpassing it in pass@k and solution diversity.
mode we seek to avoid, whereas assigning zero reward to
the entire group would collapse the grouped learning signal
under GRPO.                                                           2. Related Work
To address this, we introduce ResZero (Residual-Zero),                LLM Reasoning. The general capabilities of LLMs have
a fallback reward that discards the unverified plurality              rapidly expanded (OpenAI, 2023; Dubey et al., 2024; Yang
   1
                                                                      et al., 2025b), yet reliable mathematical and program-
   Throughout, “majority vote” follows the usual usage in the
community and means a plurality.
                                                                      matic reasoning remains a bottleneck: models often op-


                                                                  2
                                 JURY-RL: Votes Propose, Proofs Dispose for Label-Free RLVR

timize for plausibility rather than verifiable correctness             the label-free setting, ground-truth answers are unavailable
(Ouyang et al., 2022; Rafailov et al., 2023; Touvron et al.,           during training. Instead, each x can be associated with a
2023). Post-training techniques that elicit step-by-step rea-          machine-checkable specification spec(x), and an external
soning (e.g., chain-of-thought and self-consistency) can               verifier (e.g., a Lean-based checker) exposes a binary oracle
raise average accuracy but also amplify confident but wrong
results when no external check is available (Wei et al.,                                     verify(x, a) ∈ {0, 1},
2022; Wang et al., 2023). These problems motivate re-
cent verifiability-aligned training signals that reward what           which returns 1 when the candidate is accepted by the de-
is provably correct rather than what appears correct (Shao             ployed verification pipeline. In our setting, this means suc-
et al., 2024; Lambert et al., 2024; Hu et al., 2025; DeepSeek-         cessful Lean verification of a semantically faithful formaliza-
AI et al., 2025; Kimi-Team et al., 2025; Yang et al., 2025a).          tion; verify(x, a) = 0 may arise either because the answer
                                                                       is wrong or because upstream formalization or proof-search
Label-Free RLVR. To scale beyond labeled specifications,               steps fail to certify it.
label-free surrogates derive rewards from the model or unla-
beled data itself such as via majority voting (Shafayat et al.,        We optimize a KL-regularized RLVR objective with refer-
2025; Zhang et al., 2025), confidence (Zhao et al., 2025b),            ence policy πref and coefficient β:
entropy (Prabhudesai et al., 2025; Agarwal et al., 2025), or                               h                          i
LLM-as-a-Judge (Pang et al., 2023; Lee et al., 2024; Su                 max Ex∼D, y∼πθ r(x, y; Gx ) − β DKL πθ ∥ πref , (1)
                                                                          πθ
et al., 2025; Zhao et al., 2025a). While attractive for their
broad coverage and low cost, these signals are prone to false          where all distributions are conditioned on x, and r(·) is a
positives, prompt/format gaming (Zhao et al., 2025c), and              grouped reward computed from G rollouts Gx = {yi }G  i=1 .
training collapse (Zhang et al., 2025). As a result, consensus         We adopt Group Relative Policy Optimization (GRPO)
or judge approval models risk diverging from ground truth,             (Shao et al., 2024) to estimate group-normalized advan-
leading to reward hacking and instability (Shafayat et al.,            tages. Concretely, sample yi ∼ πold (· | x) for i = 1, . . . , G
2025; Zhang et al., 2025). Our work targets this conflict:             and compute ri := r(x, yi ; Gx ). The scalar group advantage
retain the scalability of label-free training while removing           is
optimism toward unverified agreement.
                                                                                                                                  G
Lean and Other Verifiers. Verification-based training em-                                   ri − r                       1
                                                                                                                                  X
                                                                               Âi =                      ,            r=G              rj .         (2)
ploys externally checkable signals such as program execu-                              std({rj }G
                                                                                                j=1 ) + ε                         j=1
tion and unit tests, SMT solvers, or formal proof assistants
such as Lean/Coq to couple reward with correctness (P.Huet                                                     θ     π (y
                                                                                                                   i,t      |x,y
                                                                                                                           i,<t         )
et al., 1997; C.Blanchette et al., 2011; de Moura & Ullrich,           Let the per-token ratio be ρi,t (θ) = πold (yi,t |x,yi,<t ) . GRPO
2021; Cobbe et al., 2021; AI & Agentica, 2025). Previous               maximizes
generate-then-verify pipelines typically provide no learning                             "      G        |yi |
signal when verification fails, limiting stability and sample                                1 X 1 X              
                                                                         JGRPO (θ) = E                         min ρi,t Âi,t ,
efficiency. JURY-RL decouples proposal from disposal to                                      G i=1 |yi | t=1
                                                                                                                                                     (3)
preserve label-free scalability while maintaining optimiza-
                                                                                                                                             #
                                                                                                                                           
tion alignment with provable correctness in the positive-                           clip(ρi,t , 1 ± ϵ) Âi,t       − β DKL πθ ∥ πref             ,
reward branch. Unlike process-reward approaches or hybrid
verifiers (Huang et al., 2025c) that rely on learned judges,           where Âi,t is a broadcast of Âi (or any per-token variant
JURY-RL uses successful Lean verification as the final ac-             compatible with GRPO), and the clipping avoids excessive
ceptance mechanism for positive reward, conditional on                 policy drift.
semantically faithful formalization. The autoformalization
pipeline is therefore part of the deployed verification sys-           Label-free Self-Reward in Reinforcement Learning. We
tem rather than an independent learned supervisor, and its             categorize existing methods for label-free self-reward based
practical imperfections primarily affect whether a candidate           on the origin of the reward signal: model-internal signals
can be certified at all.                                               versus those from an external judge.
                                                                       (A) Model-Internal Self-Reward Signals. These methods
3. Preliminaries                                                       derive rewards from the model’s own outputs without ex-
                                                                       ternal evaluators. (i) Output-side proxies, such as en-
Problem Setup. Let πθ denote a policy LLM with param-                  tropy minimization or confidence-based scores (Agarwal
eters θ. Given a problem x, the model generates a token                et al., 2025; Prabhudesai et al., 2025), reward hypothe-
sequence y = (y1 , . . . , yn ) ∼ πθ (· | x) and a deterministic       ses that exhibit high certainty. However, this approach is
extractor ans(·) parses a candidate answer a = ans(y). In              fragile, as it can amplify errors when the model becomes

                                                                   3
                                 JURY-RL: Votes Propose, Proofs Dispose for Label-Free RLVR

confidently wrong. (ii) Single-view agreement rewards                  4.1. The Proof-Gated Reward Framework
consistency among multiple outputs generated from the
                                                                       The JURY-RL workflow strictly follows the decoupled
same input x (Shafayat et al., 2025). Specifically, for G
                                                                       paradigm introduced above. First, in the proposal stage,
responses yi Gi=1 ,Pit identifies the majority-voted answer
                      G                                                given a problem x, we generate G trajectories {yi }G i=1 ∼
av = arg maxa i=1 I[ans(yi ) = a] and assigns a posi-
                                                                       πθ (·|x) and parse their corresponding answers ai = ans(yi ).
tive reward rsv (x, y) = I[ans(y) = av ] to responses that
                                                                       The policy proposes a single candidate â via majority vot-
match av . The primary risk is reinforcing an erroneous
                                                                       ing:
consensus, where the model converges on a popular but                                                  G
                                                                                                       X
incorrect answer, often by exploiting superficial heuristics                            â = arg max      I[ai = a].           (4)
such as formatting conventions. (iii) Multi-view agreement                                        a
                                                                                                             i=1
attempts to improve robustness by enforcing consistency                Next, in the disposal stage, a single call to the external Lean
across multiple, semantically equivalent prompts. For in-              verifier evaluates â against the formal specification of x.
stance, the majority answer from prompt variant x′ is used             This yields a binary proof-gate, δ = verify(x, â) ∈ {0, 1},
as a pseudo-label to supervise responses from the original             which governs the reward assignment.
prompt x (Zhang et al., 2025). This often improves train-
ing stability. However, it usually only delays rather than             The final reward ri for each trajectory yi is determined by a
eliminates hacking, since spurious shortcuts can eventually            conditional function gated by δ:
propagate across multiple views.
                                                                               ri = δ · I[ai = â] + (1 − δ) · riResZero ,                 (5)
(B) External-Judge Signals. This paradigm uses a powerful,                          |     {z    }    |      {z         }
                                                                                      Verified Correctness         Inconclusive Fallback
external LLM as an automated judge to score the model’s
outputs. LLM-as-a-Judge (Lee et al., 2024; Su et al., 2025;            where riResZero is the residual reward defined in Section 4.2.
Huang et al., 2025a; Zhao et al., 2025a) remains label-free
(no human annotation) but comes with distinct trade-offs.              The stability of this proof-gated design stems from its prin-
On the one hand, it mitigates the self-confirmation bias of            cipled handling of both successful and inconclusive verifi-
internal methods. On the other hand, it introduces sensitivity         cation. First, when verification succeeds (δ = 1), a positive
to the judge’s prompt design and decoding strategy, incurs             reward is granted exclusively to the trajectories that pro-
significant computational cost, and risks transferring the             duced the proven-correct answer. This approach binds the
judge’s biases into the training signal. Another approach              learning signal to hard evidence, which, under standard
is LLM-based Knowledge Distillation (LLM-KD) (Gu                       soundness assumptions, suppresses the false positives that
et al., 2024b), where a teacher model generates a reference            plague self-reward or judge-based surrogates (Zhang et al.,
answer to guide the student model. While potentially of-               2025; Cobbe et al., 2021). Second, when verification is
fering a more granular signal, it is similarly constrained by          inconclusive (δ = 0), the system defaults to our ResZero
the teacher’s capabilities and biases. Thus, while external            fallback rather than rewarding the majority consensus. This
judges reduce some weaknesses of the internal proxies, they            centered substitute maintains a stable optimization gradient
bring a different set of reliability and scalability challenges.       by preserving group-wise variance, which prevents learn-
                                                                       ing from stalling or oscillating, a common situation when
                                                                       verification fails for reasons like search limits or incom-
4. JURY-RL                                                             plete proofs. By paying only for verifiable correctness, this
                                                                       framework narrows the attack surface for prompt and format
To operationalize the principles of scalability, truth align-
                                                                       hacking, a critical vulnerability in other label-free systems.
ment, and optimization stability, JURY-RL decouples the
answer proposal process from reward disposal. In this frame-
work, votes from model rollouts serve as a scalable proposal           4.2. ResZero Reward
mechanism, while a formal theorem prover acts as the defini-           When formal verification is inconclusive, a learning signal
tive judge for reward disposal. By restricting formal verifica-        is still needed to maintain optimization stability. However, a
tion to only the single majority-voted candidate rather than           naive choice like rewarding the majority vote (MV) is brittle
evaluating every unique response, we maintain computa-                 and risks training collapse. Using MV as a reward conflates
tional tractability while ensuring the reward signal remains           agreement with correctness and can induce entropy collapse
anchored in provable correctness.                                      under GRPO, as spurious consensus strengthens. A simple
This section details the two key components of our frame-              zero-reward fallback is also suboptimal, as it would lead to
work: the overarching proof-gated reward mechanism that                zero group-wise advantage and stall the learning process.
enforces truth alignment when verification succeeds, and the           To address this, we introduce the ResZero (Residual-Zero)
Residual-Zero (ResZero) fallback designed to maintain                  Reward. Its principle is to penalize the unverifiable ma-
optimization stability when verification is inconclusive.              jority proposal and construct a meaningful, zero-mean

                                                                   4
                                     JURY-RL: Votes Propose, Proofs Dispose for Label-Free RLVR

reward from the remaining (residual) answers. This                               model is most confidently wrong, with this entire behavior
design preserves a useful learning signal by maintaining                         governed by only a single hyperparameter c. These prop-
variance among minority opinions without amplifying a                            erties prevent collapse into spurious consensus and foster
potentially false consensus. Furthermore, we propose an                          robust, exploratory learning.
adaptive variant that strengthens this signal precisely when
                                                                                 This dual-reward strategy hinges on the verifier’s outcome.
the model is most confidently wrong. The intuition is that a
                                                                                 If verification succeeds (δ=1), the policy update is guided
strong but unverified consensus (indicated by a high major-
                                                                                 by verifiable correctness. Conversely, if inconclusive (δ=0),
ity share, α) requires a stronger corrective signal. ResZero
                                                                                 our ResZero fallback penalizes the unverified majority,
operationalizes this by using α to simultaneously amplify
                                                                                 which is critical for mitigating entropy collapse caused by
the reward signal for residual answers and suppress the
                                                                                 spurious consensus. This design maintains the scalability of
majority answer.
                                                                                 label-free training by requiring only a single verification per
Let M = {i : ai = â} be the set of rollouts supporting the                      step. The full procedure is detailed in Appendix B.
majority answer and R = {i : ai ̸= â} be the set of residual
rollouts. The majority share is α = |M |/G. We first define                      5. Experiments
the leave-one-out residual share for an answer b within the
residual group:                                                                  5.1. Setting
                              1    X                                             Backbone Models. We evaluate JURY-RL on three open-
            u(−i) (b) =              I[aj = b].
                           |R| − 1                                               source backbones spanning base and instruction-tuned mod-
                                          j∈R
                                          j̸=i                                   els: Qwen3-1.7B-Base (Yang et al., 2025a), Llama-3.2-3B-
                                                                                 Instruct (Dubey et al., 2024) and Qwen2.5-7B (Yang et al.,
Let zi = u(−i) (ai ) if i ∈ R (the relative support for a                        2025b), to cover different sizes and instruction-following
residual answer ai within its peer group) and zi = 0 if                          behaviors.
i ∈ M . The ResZero reward is then assigned as:
                                                                                 Baselines. We compare JURY-RL with several estab-
                                                                                 lished label-free and supervised reward baselines. The self-
riResZero = α · I[i ∈ R] · (zi − ū) − cα · I[i ∈ M ] + γ ,                      supervised baselines include Majority-Voting (Shafayat
            |         {z           } |       {z    }    |{z}                     et al., 2025), Self-Certainty (Zhao et al., 2025b), Entropy
                Amplify residual             Penalize majority   Re-center
                                                                                 minimization (Prabhudesai et al., 2025) and CoReward
                           X                                                     (Zhang et al., 2025). To further contextualize the compari-
       where          1
                ū = |R|           zj ,    γ = cα2 .
                                                                                 son, we include ground-truth supervised oracle and LLM-
                           j∈R
                                                                      (6)        KD as baselines. Additionally, we benchmark against the
                                                                                 judge-based method, LLM-as-a-Judge (Pang et al., 2023;
Here, c is a positive hyperparameter controlling the penalty                     Zhao et al., 2025a), to provide a comprehensive evaluation.
strength. γ is a global re-centering term to ensure the total                    Additional details are provided in Appendix D.
reward sums to zero. The term (zi − ū) creates a zero-
mean signal within the residual group, rewarding answers                         Implementation Details. All methods are implemented
that are more popular among the minorities and penalizing                        using the VeRL framework (Sheng et al., 2025) and trained
those that are less so. This entire residual signal is then                      on 8× NVIDIA A100 GPUs. We train on 7,500 problems
scaledPby α. By construction, the total reward sums to                           from the MATH dataset’s training split (Hendrycks et al.,
zero ( i riResZero = 0), preserving the zero-mean property                       2021), and evaluate on the 5,000-problem validation split
crucial for GRPO stability. 2                                                    (referred to as MATH5000). For each GRPO (Shao et al.,
                                                                                 2024) update step, we sample a batch of 128 problems and
The design of our ResZero reward ensures robust optimiza-                        generate G = 8 rollouts per problem. We use a learning
tion through three properties. (i) Variance preservation:                        rate of 3 × 10−6 and a KL penalty coefficient of β = 0.005.
It maintains non-zero variance among differing answers,                          To ensure fair and reproducible comparisons, we utilize
which is critical for variance-normalized optimizers like                        the officially released chat-based prompting formats for all
GRPO to prevent vanishing gradients. (ii) Zero-mean con-                         models. More details in Appendix E.
struction: Its strictly zero-mean property makes it a princi-
pled, optimizer-agnostic signal, ensuring portability beyond                     Evaluation Datasets and Metrics. To comprehensively
GRPO to any general RL paradigm. (iii) Adaptive econ-                            assess model capabilities, we evaluate on a suite of bench-
omy: The corrective signal dynamically scales with the                           marks covering mathematical reasoning, code generation,
majority share α, applying maximum pressure when the                             and general abilities. Mathematical Reasoning: We
                                                                                 evaluate on the AIME24/25 (Hugging Face H4, 2024;
   2
     See App. A.2 for a formal proof and App. B.2 for a worked                   OpenCompass, 2025), MATH500 (Lightman et al., 2024),
example. c = 0.01 in our experiments.

                                                                             5
                                         JURY-RL: Votes Propose, Proofs Dispose for Label-Free RLVR

Table 1. RL performance (%) on math reasoning benchmarks. Cell background colors indicate relative performance: darker colors denote
better results within each model group.

                                                      Mathematics                                     Code              Instruction   Multi-Task
          Methods                                                                                                                                  Average
                            AIME24        AIME25      MATH-500      GSM8K            AMC      LiveCode       CRUX         IFEval      MMLU-Pro
                                                                         Qwen3-1.7B-Base
          Before RL          3.12 ±1.8    1.25 ±1.1    46.85 ±2.9   64.20 ±1.8   20.78 ±2.5    4.59 ±0.7    7.52 ±1.1   33.66 ±1.6    33.60 ±0.7    23.95
          GT-Reward          6.88 ±2.1    5.21 ±2.0    68.35 ±2.3   82.01 ±1.1   30.87 ±3.3   14.84 ±0.5   33.73 ±0.6   38.70 ±1.6    39.43 ±0.7    35.56
          LLM-KD             6.67 ±1.1    3.54 ±1.2    67.8 ±1.2    81.97 ±1.3   35.69 ±2.2   14.05 ±0.9   33.80 ±1.5   34.65 ±1.6    37.97 ±0.7    35.13
          Self-Certainty     3.54 ±1.6    3.12 ±1.8    57.05 ±2.7   73.71 ±1.4   27.41 ±2.3   10.37 ±0.9   18.73 ±1.3   38.58 ±1.6    35.28 ±0.7    29.75
          Entropy            6.67 ±1.6    4.17 ±1.5    65.0 ±1.7    79.45 ±1.6   31.17 ±3.0   12.64 ±1.0   30.38 ±0.5   35.00 ±1.6    37.01 ±0.7    33.50
          Majority-Voting    2.08 ±1.3    2.08 ±1.3    59.6 ±0.9    81.08 ±0.8   29.82 ±1.7   14.29 ±0.5   32.00 ±2.3   37.16 ±1.6    35.68 ±0.7    32.64
          CoReward           6.88 ±1.5    3.12 ±1.5    65.4 ±1.2    81.07 ±0.8   33.13 ±3.0   14.27 ±0.5   34.10 ±1.1   37.28 ±1.6    37.39 ±0.7    34.74
          LLM-as-a-Judge     5.83 ±1.5    1.88 ±0.9    63.0 ±2.4    81.84 ±1.4   33.89 ±1.1   14.33 ±0.8   34.98 ±1.5   36.28 ±1.6    33.83 ±0.7    33.98
          JURY-RL (Ours)     7.71 ±1.8    4.58 ±2.0    66.4 ±2.0    82.58 ±0.3   34.19 ±3.1   14.54 ±0.4   33.98 ±2.5   36.55 ±1.6    38.11 ±0.7    35.40
                                                                      Llama-3.2-3B-Instruct
          Before RL          6.88 ±2.1    0.42 ±0.6    44.4 ±2.1    68.78 ±1.2   17.47 ±3.3    3.00 ±0.4   24.70 ±1.2   54.41 ±1.8    32.01 ±0.7    28.01
          GT-Reward         10.62 ±2.1    0.21 ±0.4    47.5 ±1.4    78.60 ±0.8   22.89 ±1.9    7.05 ±0.6   32.48 ±0.8   50.16 ±1.7    34.26 ±0.7    31.53
          LLM-KD            10.21 ±1.9    0.42 ±0.6    51.25 ±4.5   79.72 ±1.2   24.55 ±3.4    7.55 ±0.6   31.20 ±1.6   49.06 ±1.7    34.04 ±0.7    32.00
          Self-Certainty     2.71 ±1.3    0.62 ±0.7    42.4 ±0.9    73.52 ±1.2   17.62 ±1.8    5.57 ±0.9   24.55 ±1.2   54.11 ±1.8    34.42 ±0.7    28.39
          Entropy            3.54 ±1.5    0.21 ±0.4    40.5 ±2.9    68.57 ±1.7   17.17 ±2.6    5.38 ±0.8   26.30 ±1.7   54.24 ±1.8    33.54 ±0.7    27.72
          Majority-Voting    8.33 ±1.3    0.00 ±0.0    48.4 ±3.0    78.64 ±1.4   21.69 ±2.8    8.11 ±0.5   30.83 ±1.4   48.36 ±1.7    33.94 ±0.7    30.92
          CoReward           7.71 ±1.4    0.00 ±0.0    47.2 ±1.9    80.00 ±1.7   19.58 ±3.6    5.57 ±0.4   30.87 ±1.2   50.46 ±1.7    32.95 ±0.7    30.48
          LLM-as-a-Judge     9.38 ±1.9    0.62 ±0.7    47.35 ±2.5   78.51 ±2.2   20.93 ±3.4    3.96 ±0.5   31.45 ±1.4   51.46 ±1.7    34.22 ±0.7    30.88
          JURY-RL (Ours)     9.17 ±2.0    1.25 ±0.9    48.8 ±2.6    78.96 ±0.5   26.05 ±1.6    6.16 ±0.6   31.60 ±1.2   50.09 ±1.8    34.54 ±0.7    31.85
                                                                            Qwen2.5-7B
          Before RL          4.38 ±1.4    1.67 ±1.4    49.2 ±2.6    71.00 ±1.9   22.44 ±3.7    4.57 ±0.5   27.38 ±2.3   40.61 ±1.7    44.03 ±0.8    29.48
          GT-Reward         18.33 ±2.3   11.25 ±1.7    75.1 ±1.4    90.83 ±0.5   46.54 ±2.5   12.78 ±1.6   53.67 ±1.0   41.50 ±1.7    45.09 ±0.7    43.90
          LLM-KD            12.08 ±2.0    7.92 ±1.7    72.7 ±1.2    90.96 ±0.9   44.28 ±2.1    8.09 ±0.5   53.57 ±0.5   43.09 ±1.7    43.73 ±0.7    41.82
          Self-Certainty     9.79 ±2.4    8.96 ±1.8    72.45 ±2.8   88.21 ±0.5   40.51 ±2.1   11.87 ±0.9   53.18 ±1.4   39.66 ±1.7    43.89 ±0.7    40.95
          Entropy           11.04 ±2.3    8.33 ±2.2    73.15 ±1.7   87.85 ±0.6   40.51 ±3.1   15.68 ±0.9   51.08 ±1.3   40.25 ±1.7    42.61 ±0.7    41.17
          Majority-Voting   11.25 ±2.1    4.17 ±1.2    71.0 ±0.7    90.52 ±0.7   38.70 ±1.3   18.37 ±0.9   52.20 ±1.1   42.72 ±1.7    43.83 ±0.8    41.42
          CoReward          11.25 ±1.8    3.96 ±1.9    73.85 ±1.1   90.16 ±0.9   40.81 ±1.8   10.37 ±0.5   55.08 ±2.4   43.75 ±1.7    42.08 ±0.7    41.26
          LLM-as-a-Judge    10.42 ±2.1    5.62 ±1.2    72.3 ±1.2    89.73 ±0.7   41.11 ±3.1   10.58 ±0.3   51.90 ±1.6   44.17 ±1.7    48.67 ±0.7    41.61
          JURY-RL (Ours)    13.75 ±1.8    7.50 ±1.6    75.65 ±0.7   90.35 ±0.9   47.29 ±3.2   14.69 ±1.1   54.37 ±0.4   41.51 ±1.7    50.00 ±0.8    43.90




GSM8K (Cobbe et al., 2021), and the competition-level                                 tion. Across three backbones, JURY-RL attains overall
AMC datasets (math-ai Team, 2024). Code Generation:                                   performance comparable to the supervised GT baseline,
We assess coding proficiency using LiveCodeBench (Jain                                with the clearest gains on harder competition-style evalua-
et al., 2024) and CRUX (Gu et al., 2024a). Instruction-                               tions and under multi-sample decoding. The gains on the
Following and Multi-Task: General abilities are measured                              in-distribution MATH500 set are more modest, which is
using IFEval (Zhou et al., 2023) for instruction follow-                              unsurprising given that training is performed on MATH. In
ing and MMLU-Pro (Wang et al., 2024) for multi-task un-                               contrast, the improvements on out-of-distribution math
derstanding. We report avg@k accuracy with k varying                                  benchmarks—most consistently on AMC, and on GSM8K
by benchmark difficulty: k=16 for AIME24/25, k=4 for                                  for smaller backbones—indicate that the proof-gated objec-
MATH500 and GSM8K, k=8 for AMC, and k=5 for code                                      tive is not merely memorizing dataset-specific answer pat-
generation benchmarks. More details in Appendix F.                                    terns. Table 2 further shows that JURY-RL improves average
                                                                                      pass@1 over both GT-Reward and LLM-as-a-Judge, while
5.2. Main Results                                                                     achieving even larger gains in average pass@k, suggesting
                                                                                      that the method improves both single-sample competence
We evaluate JURY-RL on both in- and out-domain tasks, as                              and the breadth of useful candidate solutions.
shown in Table 1 under avg@k settings3 . A key finding is
that JURY-RL not only outperforms all label-free RL base-                             Out-of-Domain Generalization. The model exhibits robust
lines but also consistently matches the supervised GRPO                               out-of-domain performance across code generation, instruc-
with ground-truth rewards (GT), suggesting that proof-gated                           tion following, and multi-task knowledge benchmarks. On
rewards can serve as a promising alternative to direct super-                         Qwen2.5-7B, JURY-RL again surpasses the GT baseline
vision.                                                                               on these out-of-domain benchmarks, achieving an average
                                                                                      of 40.14% (+1.88 pts, +4.92% rel.). On the other two
Mathematical Reasoning and In-Domain Generaliza-                                      backbone models, its performance remains close to GT
   3
       Values are reported as mean ± 95% confidence intervals.                        while consistently ranking as the best-performing label-free


                                                                                 6
                                       JURY-RL: Votes Propose, Proofs Dispose for Label-Free RLVR

Table 2. Performance of JURY-RL vs. GT-Reward and LLM-as-a-judge on math reasoning tasks. k=16 for AIME, k=4 for MATH500 and
GSM8K, and k=8 for AMC. ∆GT and ∆LJ denote JURY-RL’s improvements (in percentage points) over GT-Reward and LLM-as-a-judge,
respectively.

                                                  Average (pass@k)                                                               Average (pass@1)
 Model
                         GT-Reward    LLM-as-a-judge        JURY-RL        ∆GT (pp)         ∆LJ (pp)   GT-Reward      LLM-as-a-judge                             JURY-RL    ∆GT (pp)    ∆LJ (pp)
 Qwen3-1.7B-Base           55.36            50.35                59.41          +4.05       +9.06         39.25              37.60                                 41.57      +2.32      +3.97
 Llama-3.2-3B-Instruct     45.46            45.93                48.48          +3.02       +2.55         32.19              30.65                                 34.10      +1.91      +3.45
 Qwen2.5-7B                62.48            53.99                64.04          +1.56       +10.05        46.60              44.13                                 48.13      +1.53      +4.00


                         Table 3. Ablation results for the proposed ResZero reward (δ = 0) on reasoning benchmark.

                                                                 Mathematics                                          Code                              Instruction        Multi-Task
 Methods                                                                                                                                                                                Average
                                     AIME24         AIME25        MATH-500         GSM8K           AMC        LiveCode       CRUX                                IFEval    MMLU-Pro
                                                                                Qwen3-1.7B-Base
 GT-Reward                            6.88 ±2.1      5.21 ±2.0     68.35 ±2.3      82.01 ±1.1    30.87 ±3.3   14.84 ±0.5   33.73 ±0.6                        38.70 ±1.6    39.43 ±0.7    35.56
 Majority-Voting                      2.08 ±1.3      2.08 ±1.3     59.6 ±0.9       81.08 ±0.8    29.82 ±1.7   14.29 ±0.5   32.00 ±2.3                        37.16 ±1.6    35.68 ±0.7    32.64
 Proof-Gate + Zero Reward             3.54 ±1.6      2.92 ±1.4     59.85 ±1.2      83.21 ±0.5    30.87 ±2.4   15.00 ±0.8   34.10 ±1.4                        37.40 ±1.6    34.43 ±0.7    33.48
 Proof-Gate + Random Reward           4.58 ±1.4      2.50 ±1.2     59.75 ±2.0      77.58 ±0.8    26.96 ±1.3    9.14 ±1.3   18.48 ±1.6                        37.19 ±1.6    35.12 ±0.7    30.14
 Proof-Gate + MV Reward               0.00 ±0.0      0.00 ±0.0     41.2 ±1.0       82.47 ±0.4    9.64 ±0.8    14.48 ±1.1   34.40 ±2.1                        36.78 ±1.6    35.33 ±0.7    28.26
 JURY-RL (Proof-Gate + ResZero)       7.71 ±1.8      4.58 ±2.0     66.4 ±2.0       82.58 ±0.3    34.19 ±3.1   14.54 ±0.4   33.98 ±2.5                        36.55 ±1.6    38.11 ±0.7    35.40
                                                                           Llama-3.2-3B-Instruct
 GT-Reward                           10.62 ±2.1      0.21 ±0.4     47.5 ±1.4       78.60 ±0.8    22.89 ±1.9    7.05 ±0.6   32.48 ±0.8                        50.16 ±1.8    34.26 ±0.7    31.53
 Majority-Voting                      8.33 ±1.3      0.00 ±0.0     48.4 ±3.0       78.64 ±1.4    21.69 ±2.8    8.11 ±0.5   30.83 ±1.4                        48.36 ±1.8    33.94 ±0.7    30.92
 Proof-Gate + Zero Reward             8.33 ±1.6      0.42 ±0.6     47.8 ±2.2       78.54 ±0.8    20.48 ±3.2    4.36 ±0.5   30.70 ±1.1                        49.98 ±1.7    35.06 ±0.7    30.63
 Proof-Gate + Random Reward           2.92 ±1.4      1.25 ±1.1     41.85 ±2.2      72.71 ±2.9    17.32 ±2.1    3.03 ±0.8   26.88 ±1.1                        52.30 ±1.8    31.90 ±0.7    27.80
 Proof-Gate + MV Reward               7.29 ±1.6      0.00 ±0.0     47.25 ±3.3      78.28 ±0.6    21.99 ±2.6    7.07 ±1.0   30.87 ±0.7                        48.49 ±1.7    33.68 ±0.7    30.55
 JURY-RL (Proof-Gate + ResZero)       9.17 ±2.0      1.25 ±0.9     48.8 ±2.6       78.96 ±0.5    26.05 ±1.6    6.16 ±0.6   31.60 ±1.2                        50.09 ±1.7    34.54 ±0.7    31.85
                                                                                  Qwen2.5-7B
 GT-Reward                           18.33 ±2.3     11.25 ±1.7     75.1 ±1.4       90.83 ±0.5    46.54 ±2.5   12.78 ±1.6   53.67 ±1.0                        41.50 ±1.7    45.09 ±0.7    43.90
 Majority-Voting                     11.25 ±2.1      4.17 ±1.2     71.0 ±0.7       90.52 ±0.7    38.70 ±1.3   18.37 ±0.9   52.20 ±1.1                        42.72 ±1.7    43.83 ±0.7    41.42
 Proof-Gate + Zero Reward            11.67 ±1.7     10.21 ±2.9     75.15 ±1.8      90.13 ±0.5    41.11 ±3.0   18.10 ±1.2   52.02 ±1.8                        43.67 ±1.7    46.97 ±0.8    43.23
 Proof-Gate + Random Reward           8.75 ±1.9      2.50 ±1.2     60.7 ±2.0       82.66 ±1.7    30.72 ±4.5   21.97 ±1.2   43.50 ±1.1                        38.56 ±1.7    43.90 ±0.7    37.03
 Proof-Gate + MV Reward               0.00 ±0.0      0.00 ±0.0     51.4 ±1.1       90.54 ±1.0    14.76 ±1.0   17.29 ±1.0   54.83 ±1.5                        43.64 ±1.7    35.01 ±0.7    34.16
 JURY-RL (Proof-Gate + ResZero)      13.75 ±1.8      7.50 ±1.6     75.65 ±0.7      90.35 ±0.9    47.29 ±3.2   14.69 ±1.1   54.37 ±0.4                        41.51 ±1.7    50.00 ±0.7    43.90




method. These results demonstrate that optimizing for verifi-                               coding are substantially larger than those in pass@1, es-
able correctness encourages the model to learn fundamental,                                 pecially compared to LLM-as-a-judge (e.g., +9.06 and
transferable skills that generalize beyond the mathematical                                 +10.05 percentage points in pass@k on Qwen3-1.7B-Base
domain used for training.                                                                   and Qwen2.5-7B). This pattern indicates that JURY-RL in-
                                                                                            creases the number of distinct high-quality solutions rather
Overall Gains. Across all three backbones and different
                                                                                            than only refining the single best prediction. Our ResZero
benchmarks, JURY-RL consistently delivers the strongest
                                                                                            reward contributes to this behavior by down-weighting
overall performance among label-free RL methods. In terms
                                                                                            unverifiable majority answers and redistributing reward
of the aggregated averages in Table 1, it uniformly outper-
                                                                                            to residual trajectories, which promotes exploration of
forms other label-free methods, with especially clear gains
                                                                                            alternative reasoning paths and mitigates mode collapse.
on challenging out-of-distribution math and code bench-
                                                                                            Consistently, Figure 2
marks. At the same time, its overall performance remains
                                                                                                                                        Average Unique Answers




                                                                                            shows that the aver-            4
competitive with supervised variants like GT and LLM-KD,
                                                                                            age number of unique
while avoiding the training instabilities and collapse behav-
                                                                                            answers per problem
iors observed in other label-free approaches. Taken together,                                                               2      JURY-RL
                                                                                            remains high throughout                GT-Reward
these results show that JURY-RL is a strong label-free al-                                                                         Proof-Gate + MV Reward
                                                                                            training for JURY-RL,                  Majority-Voting
ternative in machine-checkable settings, while still leaving
                                                                                            whereas baselines such          00         100         200    300
room for further gains from stronger proposal models and
                                                                                            as       Majority-Voting                         Step
more reliable upstream formalization.
                                                                                            quickly collapse to a         Figure 2. Average unique an-
Does JURY-RL Enhance Diversity? Yes. Table 2 shows                                          single dominant answer.       swers per sample over training
that JURY-RL improves both pass@k and pass@1 over                                           Per-benchmark pass@k          steps on Qwen3-1.7B-Base.
GT-Reward and LLM-as-a-judge on all three backbones.                                        breakdowns are provided in Table 10, Appendix G.2.
On average, the gains in pass@k under multi-sample de-


                                                                                        7
                                                 JURY-RL: Votes Propose, Proofs Dispose for Label-Free RLVR

                             Qwen3-1.7B-Base                                                   Llama-3.2-3B-Instruct                                                    Qwen2.5-7B
                                                                                 50
               60
                                                                                 40                                                                     60
Accuracy (%)




                                                                  Accuracy (%)




                                                                                                                                         Accuracy (%)
                                                GT-Reward                                                              GT-Reward                                                         GT-Reward
               40                               JURY-RL                          30                                    JURY-RL                                                           JURY-RL
                                                                                                                                                        40
                                                LLM-KD                                                                 LLM-KD                                                            LLM-KD
                                                LLM-as-a-Judge                   20                                    LLM-as-a-Judge                                                    LLM-as-a-Judge
               20                               CoReward                                                               CoReward                         20                               CoReward
                                                Majority-Voting                  10                                    Majority-Voting                                                   Majority-Voting
                                                Self-Certainty                                                         Self-Certainty                                                    Self-Certainty
                                                Entropy                                                                Entropy                                                           Entropy
               0                                                                  0                                                                      0
                    0   50   100   150    200     250       300                       0   50     100       150   200     250       300                       0   50   100   150    200     250       300
                                   Step                                                                Step                                                                 Step

                                                Figure 3. Accuracy on MATH5000 Validation set over training steps.


  5.3. Analysis                                                                                             Analysis of Verifier Sig-       Table 4. Verifier signal quality on
                                                                                                            nal Quality.        While       training set. All metrics reported
 Ablation Studies of ResZero. We compare four fallback                                                                                      in percent (%).
                                                                                                            a formal verifier like
 designs under the same proof-gated framework when δ=0:
                                                                                                            Lean theoretically offers        Verifier             Prec. Rec. F1
 Zero Reward (no signal), Random Reward (rewarding a ran-
                                                                                                            near-zero false positives,       LLM-as-a-Judge       75.9 96.1 84.8
 domly selected candidate), MV Reward, and our proposed                                                                                      Lean Verifier (Ours) 84.5 88.0 86.2
                                                                                                            our practical pipeline in-
 ResZero, with GT and Majority-Voting as references. As
                                                                                                            volves upstream processes like auto-formalization and con-
 shown in Table 3, among all proof-gated variants ResZero
                                                                                                            sistency checks, which can introduce errors. It is therefore
 consistently achieves the highest Average. On average, it
                                                                                                            crucial to compare the signal quality of our verifier against
 outperforms Zero Reward by +1.3 pts, MV Reward by +6.1
                                                                                                            an LLM-as-a-Judge. As shown in Table 4, our Lean verifier
 pts, and essentially matches GT within +0.1 pts, while sur-
                                                                                                            provides a superior reward signal compared to the LLM-as-
 passing the Random Reward baseline by +5.4 pts. Notably,
                                                                                                            a-Judge. It achieves substantially higher precision (84.5%
 Proof-Gate + MV Reward performs worse than the plain
                                                                                                            vs. 75.9%) at the cost of moderately lower recall (88.0% vs.
 Majority-Voting baseline. This highlights that rewarding an
                                                                                                            96.1%). This trade-off is paramount: high precision drasti-
 unverified majority can reinforce spurious consensus even
                                                                                                            cally reduces false positives, preventing reward hacking and
 after verification fails, accelerating mode collapse. A simple
                                                                                                            tightly aligning the training objective with verifiable correct-
 Zero Reward achieves suboptimal performance by taking
                                                                                                            ness. Conversely, the LLM-judge’s noisy signal, stemming
 a safe but inefficient path: it avoids reinforcing errors, but
                                                                                                            from low precision, risks reinforcing errors despite its higher
 at the cost of stalling the learning process for inconclusive
                                                                                                            recall. The Lean verifier’s higher F1-score (86.2%) confirms
 samples. Meanwhile, the naive Random Reward baseline,
                                                                                                            its better overall balance, validating our “Proofs Dispose”
 which injects unstructured reward noise when verification
                                                                                                            principle of prioritizing signal fidelity for stable learning.
 fails, underperforms Zero Reward by 4.1 pts on average,
                                                                                                            While our verifier is not perfect, its imperfections stem from
 indicating that random reinforcement alone cannot provide
                                                                                                            upstream components rather than the prover’s core logic.
 a useful learning signal. ResZero provides a robust solution
                                                                                                            We provide a deeper analysis of these nuances and their
 by navigating this trade-off between dangerous reinforce-
                                                                                                            effect on training dynamics in Appendix G.5.
 ment and inefficient stagnation. Per-benchmark pass@k
 breakdowns can be found in Table 11, Appendix G.2, where
 ResZero significantly outperforms other variants and even                                                  6. Conclusion
 surpasses the GT-Reward baseline across all models.
                                                                                                            We introduced JURY-RL, a label-free RLVR framework
 JURY-RL Achieves Stable Training and Avoids Collapse.                                                      that decouples proposal from disposal: majority voting
 To evaluate training stability, we tracked the validation                                                  across rollouts proposes a candidate answer, while a formal
 accuracy of JURY-RL against label-free baselines on the                                                    Lean verifier disposes the final reward. If the proposal is
 MATH5000 validation set throughout the training process.                                                   verified, only the supporting trajectories are rewarded; when
 As illustrated in Figure 3, Entropy and Self-Certainty show                                                verification is inconclusive, ResZero discards the unverifi-
 collapse after an initial performance gain, as the model                                                   able majority and assigns a zero-mean, variance-preserving
 begins to reinforce spurious consensus. The LLM-as-a-                                                      residual reward that keeps optimization well-conditioned.
 Judge/LLM-KD/Majority-Voting exhibit noisy and subopti-                                                    This design jointly achieves three goals: scalability without
 mal convergence. In contrast, JURY-RL demonstrates stable,                                                 human labels, truth alignment via verifiable correctness, and
 monotonic improvement, confirming that its proof-gated re-                                                 optimization stability in the absence of proof. Across math-
 ward mechanism effectively prevents the mode collapse                                                      ematical reasoning, code generation, and multi-task evalua-
 common in self-supervised methods.                                                                         tions, JURY-RL trains more stably than label-free baselines

                                                                                                       8
                                JURY-RL: Votes Propose, Proofs Dispose for Label-Free RLVR

and achieves performance comparable to supervised train-                2022. doi: 10.48550/ARXIV.2204.05862. URL https:
ing with ground-truth rewards, while demonstrating greater              //doi.org/10.48550/arXiv.2204.05862.
response diversity and stronger pass@k performance. Our
work demonstrates that grounding RL in sparse but formally            C.Blanchette, J., Böhme, S., and C.Paulson, L. Extending
verified signals is a promising strategy for building robust            Sledgehammer with SMT Solvers. In Proceedings of the
and generalizable reasoning models without human labels.                23rd International Conference on Automated Deduction
                                                                        (CADE23), volume 6803 of Lecture Notes in Artificial
                                                                        Intelligence, pp. 116–130. Springer, 2011. doi: 10.1007/
Impact Statement                                                        978-3-642-22438-6 11.
This work studies label-free reinforcement learning with ver-
                                                                      Chen, G., Wu, J., Chen, X., Zhao, W. X., Song, R.,
ifiable rewards (RLVR) for mathematical and programmatic
                                                                        Li, C., Fan, K., Liu, D., and Liao, M. Reform: Re-
reasoning. It does not involve human subjects, crowd work-
                                                                        flective autoformalization with prospective bounded se-
ers, user studies, or the collection of personally identifiable
                                                                        quence optimization. CoRR, abs/2510.24592, 2025. doi:
information. All datasets used (e.g., MATH, GSM8K, AM-
                                                                       10.48550/ARXIV.2510.24592. URL https://doi.
C/AIME, LiveCodeBench, CRUX, MMLU-Pro, IFEval) are
                                                                        org/10.48550/arXiv.2510.24592.
publicly available and used under their respective licenses;
we redistribute nothing and provide only references and               Chen, G. H., Chen, S., Liu, Z., Jiang, F., and Wang, B.
scripts to download from the original sources.                          Humans or LLMs as the judge? a study on judgement
Potential risks include (i) misuse: stronger automated rea-             bias. In Proceedings of the 2024 Conference on Em-
soning could be used to complete graded assignments or to               pirical Methods in Natural Language Processing, pp.
generate convincing but incorrect solutions; (ii) bias/cov-             8301–8327, Miami, Florida, USA, 2024. Association
erage: public benchmarks may contain stylistic biases or                for Computational Linguistics. doi: 10.18653/v1/2024.
limited topical coverage; (iii) safety: LLM judges can trans-           emnlp-main.474. URL https://aclanthology.
fer prompt or format biases into training signals. Our design           org/2024.emnlp-main.474/.
explicitly mitigates these issues by proof-gating rewards             Cobbe, K., Kosaraju, V., Bavarian, M., Chen, M., Jun, H.,
with a formal verifier (Lean) to reduce false positives and             Kaiser, L., Plappert, M., Tworek, J., Hilton, J., Nakano,
by using the Residual-Zero (ResZero) fallback to avoid re-              R., Hesse, C., and Schulman, J. Training verifiers to
inforcing unverifiable consensus. We report precisely which             solve math word problems. CoRR, abs/2110.14168, 2021.
datasets, prompts, and evaluation harnesses are used, and we            doi: 10.48550/ARXIV.2110.14168. URL https://
provide ablations and diagnostics to surface failure modes              doi.org/10.48550/arXiv.2110.14168.
(e.g., collapse under majority-voting).
                                                                      de Moura, L. and Ullrich, S. The Lean4 Theorem Prover
References                                                              and Programming Language. In Automated Deduction–
                                                                        CADE28, volume 12699 of Lecture Notes in Computer
Agarwal, S., Zhang, Z., Yuan, L., Han, J., and Peng, H.                 Science, pp. 625–635. Springer, 2021. doi: 10.1007/
 The unreasonable effectiveness of entropy minimization                 978-3-030-79876-5 37. URL https://lean-lang.
  in llm reasoning. CoRR, abs/2505.15134, 2025. doi:                    org/papers/lean4.pdf.
 10.48550/ARXIV.2505.15134. URL https://doi.
  org/10.48550/arXiv.2505.15134.                                      DeepSeek-AI, Liu, A., Feng, B., Xue, B., Wang, B., Wu,
                                                                        B., Lu, C., Zhao, C., Deng, C., Zhang, C., Ruan, C., Dai,
AI, T. and Agentica. Deepcoder: A fully open-source 14b                 D., Guo, D., Yang, D., Chen, D., Ji, D., Li, E., Lin, F.,
  coder at o3-mini level. Blog post, 2025. URL https://                 Dai, F., Luo, F., Hao, G., Chen, G., Li, G., Zhang, H.,
  www.together.ai/blog/deepcoder. Accessed:                             Bao, H., Xu, H., Wang, H., Zhang, H., Ding, H., Xin,
  2025-09-10.                                                           H., Gao, H., Li, H., Qu, H., Cai, J. L., Liang, J., Guo,
                                                                        J., Ni, J., Li, J., Wang, J., Chen, J., Chen, J., Yuan, J.,
Bai, Y., Jones, A., Ndousse, K., Askell, A., Chen, A., Das-             Qiu, J., Li, J., Song, J., Dong, K., Hu, K., Gao, K., Guan,
  Sarma, N., Drain, D., Fort, S., Ganguli, D., Henighan,                K., Huang, K., Yu, K., Wang, L., Zhang, L., Xu, L.,
  T., Joseph, N., Kadavath, S., Kernion, J., Conerly, T.,               Xia, L., Zhao, L., Wang, L., Zhang, L., Li, M., Wang,
  El-Showk, S., Elhage, N., Hatfield-Dodds, Z., Hernan-                 M., Zhang, M., Zhang, M., Tang, M., Li, M., Tian, N.,
  dez, D., Hume, T., Johnston, S., Kravec, S., Lovitt, L.,              Huang, P., Wang, P., Zhang, P., Wang, Q., Zhu, Q., Chen,
  Nanda, N., Olsson, C., Amodei, D., Brown, T., Clark, J.,              Q., Du, Q., Chen, R. J., Jin, R. L., Ge, R., Zhang, R.,
  McCandlish, S., Olah, C., Mann, B., and Kaplan, J. Train-             Pan, R., Wang, R., Xu, R., Zhang, R., Chen, R., Li,
  ing a helpful and harmless assistant with reinforcement               S. S., Lu, S., Zhou, S., Chen, S., Wu, S., Ye, S., Ma,
  learning from human feedback. CoRR, abs/2204.05862,                   S., Wang, S., Zhou, S., Yu, S., Zhou, S., Pan, S., Wang,

                                                                  9
                                JURY-RL: Votes Propose, Proofs Dispose for Label-Free RLVR

  T., Yun, T., Pei, T., Sun, T., Xiao, W. L., and Zeng, W.               ematical problem solving with the MATH dataset. In Van-
  Deepseek-v3 technical report. CoRR, abs/2412.19437,                    schoren, J. and Yeung, S. (eds.), Proceedings of the Neu-
  2024. doi: 10.48550/ARXIV.2412.19437. URL https:                       ral Information Processing Systems Track on Datasets
  //doi.org/10.48550/arXiv.2412.19437.                                   and Benchmarks 1, NeurIPS Datasets and Benchmarks
                                                                         2021, December 2021, virtual, 2021.
DeepSeek-AI, Guo, D., Yang, D., Zhang, H., Song, J.,
  Zhang, R., Xu, R., Zhu, Q., Ma, S., Wang, P., Bi, X.,                Hu, J., Zhang, Y., Han, Q., Jiang, D., Zhang, X., and Shum,
  Zhang, X., Yu, X., Wu, Y., Wu, Z. F., Gou, Z., Shao,                   H. Open-reasoner-zero: An open source approach to
  Z., Li, Z., Gao, Z., Liu, A., Xue, B., Wang, B., Wu, B.,               scaling up reinforcement learning on the base model.
  Feng, B., Lu, C., Zhao, C., Deng, C., Zhang, C., Ruan,                 CoRR, abs/2503.24290, 2025. doi: 10.48550/ARXIV.
  C., Dai, D., Chen, D., Ji, D., Li, E., Lin, F., Dai, F., Luo,          2503.24290. URL https://doi.org/10.48550/
  F., Hao, G., Chen, G., Li, G., Zhang, H., Bao, H., Xu,                 arXiv.2503.24290.
  H., Wang, H., Ding, H., Xin, H., Gao, H., Qu, H., Li,
  H., Guo, J., Li, J., Wang, J., Chen, J., Yuan, J., Qiu, J.,          Huang, H., Bu, X., Zhou, H., Qu, Y., Liu, J., Yang, M.,
  Li, J., Cai, J. L., Ni, J., Liang, J., Chen, J., Dong, K.,            Xu, B., and Zhao, T. An empirical study of llm-as-
  Hu, K., Gao, K., Guan, K., Huang, K., Yu, K., Wang,                    a-judge for LLM evaluation: Fine-tuned judge model
  L., Zhang, L., Zhao, L., Wang, L., Zhang, L., Xu, L.,                  is not a general substitute for GPT-4. In Che, W.,
  Xia, L., Zhang, M., Zhang, M., Tang, M., Li, M., Wang,                 Nabende, J., Shutova, E., and Pilehvar, M. T. (eds.), Find-
  M., Li, M., Tian, N., Huang, P., Zhang, P., Wang, Q.,                  ings of the Association for Computational Linguistics,
  Chen, Q., Du, Q., Ge, R., Zhang, R., Pan, R., Wang, R.,               ACL 2025, Vienna, Austria, July 27 - August 1, 2025,
  Chen, R. J., Jin, R. L., Chen, R., Lu, S., Zhou, S., Chen,             pp. 5880–5895. Association for Computational Linguis-
  S., Ye, S., Wang, S., Yu, S., Zhou, S., Pan, S., and Li,               tics, 2025a. URL https://aclanthology.org/
  S. S. Deepseek-r1: Incentivizing reasoning capability in               2025.findings-acl.306/.
  llms via reinforcement learning. CoRR, abs/2501.12948,               Huang, L., Yu, W., Ma, W., Zhong, W., Feng, Z., Wang,
  2025. doi: 10.48550/ARXIV.2501.12948. URL https:                       H., Chen, Q., Peng, W., Feng, X., Qin, B., and Liu,
 //doi.org/10.48550/arXiv.2501.12948.                                   T. A survey on hallucination in large language mod-
Dubey, A., Jauhri, A., Pandey, A., Kadian, A., Al-Dahle,                 els: Principles, taxonomy, challenges, and open ques-
 A., Letman, A., Mathur, A., Schelten, A., Yang, A.,                     tions. ACM Transactions on Information Systems, 43
  Fan, A., Goyal, A., Hartshorn, A., Yang, A., Mitra,                   (2):42:1–42:55, 2025b. doi: 10.1145/3703155. URL
 A., Sravankumar, A., Korenev, A., Hinsvark, A., Rao,                    https://arxiv.org/abs/2311.05232.
 A., Zhang, A., and et al. The llama 3 herd of models.                 Huang, Y., Zeng, W., Zeng, X., Zhu, Q., and He, J. Pit-
 CoRR, abs/2407.21783, 2024. doi: 10.48550/ARXIV.                        falls of rule- and model-based verifiers - A case study
  2407.21783. URL https://doi.org/10.48550/                              on mathematical reasoning. CoRR, abs/2505.22203,
  arXiv.2407.21783.                                                      2025c. doi: 10.48550/ARXIV.2505.22203. URL https:
Gao, L., Schulman, J., and Hilton, J. Scaling laws for                  //doi.org/10.48550/arXiv.2505.22203.
  reward model overoptimization. CoRR, abs/2210.10760,
                                                                       Hugging Face H4.    AIME 2024 Benchmark.
  2022. doi: 10.48550/ARXIV.2210.10760. URL https:
                                                                         https://huggingface.co/datasets/
 //doi.org/10.48550/arXiv.2210.10760.
                                                                         HuggingFaceH4/aime_2024, 2024.
Gu, A., Rozière, B., Leather, H., Solar-Lezama, A., Syn-
                                                                       Jain, N., Han, K., Gu, A., Li, W.-D., Yan, F., Zhang, T.,
  naeve, G., and Wang, S. I. Cruxeval: A bench-
                                                                         Wang, S., Solar-Lezama, A., Sen, K., and Stoica, I. Live-
  mark for code reasoning, understanding and execution.
                                                                          codebench: Holistic and contamination free evaluation of
 CoRR, abs/2401.03065, 2024a. doi: 10.48550/ARXIV.
                                                                          large language models for code. CoRR, abs/2403.07974,
  2401.03065. URL https://doi.org/10.48550/
                                                                          2024. doi: 10.48550/ARXIV.2403.07974. URL https:
  arXiv.2401.03065.
                                                                         //doi.org/10.48550/arXiv.2403.07974.
Gu, Y., Dong, L., Wei, F., and Huang, M. Minillm: Knowl-
                                                                       Kimi-Team, Du, A., Gao, B., Xing, B., Jiang, C., Chen,
  edge distillation of large language models. In The Twelfth
                                                                         C., Li, C., Xiao, C., Du, C., Liao, C., Tang, C., Wang,
  International Conference on Learning Representations,
                                                                         C., Zhang, D., Yuan, E., Lu, E., Tang, F., Sung, F., Wei,
  ICLR 2024, Vienna, Austria, May 7-11, 2024. OpenRe-
                                                                         G., Lai, G., Guo, H., Zhu, H., Ding, H., Hu, H., Yang,
  view.net, 2024b. URL https://openreview.net/
                                                                         H., Zhang, H., Yao, H., Zhao, H., Lu, H., Li, H., Yu, H.,
  forum?id=5h0qf7IBZZ.
                                                                         Gao, H., Zheng, H., Yuan, H., Chen, J., Guo, J., Su, J.,
Hendrycks, D., Burns, C., Kadavath, S., Arora, A., Basart,               Wang, J., Zhao, J., Zhang, J., Liu, J., Yan, J., Wu, J., Shi,
  S., Tang, E., Song, D., and Steinhardt, J. Measuring math-             L., Ye, L., Yu, L., Dong, M., Zhang, N., Ma, N., Pan,

                                                                  10
                               JURY-RL: Votes Propose, Proofs Dispose for Label-Free RLVR

  Q., Gong, Q., Liu, S., Ma, S., Wei, S., Cao, S., Huang,             Ouyang, L., Wu, J., Jiang, X., Almeida, D., Wainwright,
  S., Jiang, T., Gao, W., Xiong, W., He, W., Huang, W.,                 C. L., Mishkin, P., Zhang, C., Agarwal, S., Slama, K.,
  Wu, W., He, W., Wei, X., Jia, X., Wu, X., Xu, X., Zu,                 Ray, A., Schulman, J., Hilton, J., Kelton, F., Miller, L.,
  X., Zhou, X., Pan, X., Charles, Y., Li, Y., Hu, Y., Liu, Y.,          Simens, M., Askell, A., Welinder, P., Christiano, P., Leike,
  Chen, Y., Wang, Y., Liu, Y., Qin, Y., Liu, Y., Yang, Y.,             J., and Lowe, R. Training language models to follow in-
  Bao, Y., Du, Y., Wu, Y., Wang, Y., Zhou, Z., Wang, Z.,                structions with human feedback. CoRR, abs/2203.02155,
  Li, Z., Zhu, Z., Zhang, Z., Wang, Z., Yang, Z., Huang,                2022. doi: 10.48550/ARXIV.2203.02155. URL https:
  Z., Huang, Z., Xu, Z., and Yang, Z. Kimi k1.5: Scaling               //doi.org/10.48550/arXiv.2203.02155.
  reinforcement learning with llms. CoRR, abs/2501.12599,
  2025. doi: 10.48550/ARXIV.2501.12599. URL https:                    Pang, J., Wang, P., Li, K., Chen, X., Xu, J., Zhang, Z., and
  //doi.org/10.48550/arXiv.2501.12599.                                  Yu, Y. Language model self-improvement by reinforce-
                                                                        ment learning contemplation. CoRR, abs/2305.14483,
Lambert, N., Morrison, J., Pyatkin, V., Huang, S., Ivison,              2023. doi: 10.48550/ARXIV.2305.14483. URL https:
  H., Brahman, F., Miranda, L. J. V., Liu, A., Dziri, N., Lyu,          //doi.org/10.48550/arXiv.2305.14483.
  S., Gu, Y., Malik, S., Graf, V., Hwang, J. D., Yang, J.,
  Bras, R. L., Tafjord, O., Wilhelm, C., Soldaini, L., Smith,         Patil, A. and Jadon, A. Advancing reasoning in large
  N. A., Wang, Y., Dasigi, P., and Hajishirzi, H. Tülu 3:              language models: Promising methods and approaches.
  Pushing frontiers in open language model post-training.               arXiv preprint arXiv:2502.03671, 2025. URL https:
  CoRR, abs/2411.15124, 2024. doi: 10.48550/ARXIV.                      //arxiv.org/abs/2502.03671.
  2411.15124. URL https://doi.org/10.48550/                           Peng, Z., Yao, Y., Ma, K., Guo, S., Li, Y., Zhang, Y., Zhang,
  arXiv.2411.15124.                                                     C., Zhang, Y., Yu, Z., Li, L., Liu, M., Xia, Y., Shen, J.,
Lee, H., Phatale, S., Mansoor, H., Mesnard, T., Ferret, J.,             Wu, Y., Cao, Y., Zhang, Z., Huang, W., Liu, J., and Zhang,
  Lu, K., Bishop, C., Hall, E., Carbune, V., Rastogi, A.,               G. Criticlean: Critic-guided reinforcement learning for
  and Prakash, S. Rlaif vs. rlhf: Scaling reinforcement                 mathematical formalization. CoRR, abs/2507.06181,
  learning from human feedback with ai feedback. In Pro-                2025. doi: 10.48550/ARXIV.2507.06181. URL https:
  ceedings of the 41st International Conference on Ma-                  //doi.org/10.48550/arXiv.2507.06181.
  chine Learning, pp. 26874–26901. PMLR, 2024. URL
                                                                      P.Huet, G., Kahn, G., and Paulin-Mohring, C. The Coq
  https://arxiv.org/abs/2309.00267.
                                                                        Proof Assistant: A Tutorial. Technical report, INRIA,
Lightman, H., Kosaraju, V., Burda, Y., Edwards, H.,                     1997. URL https://coq.inria.fr.
  Baker, B., Lee, T., Leike, J., Schulman, J., Sutskever,
                                                                      Prabhudesai, M., Chen, L., Ippoliti, A., Fragkiadaki, K.,
  I., and Cobbe, K. Letś verify step by step. CoRR,
                                                                        Liu, H., and Pathak, D. Maximizing confidence alone
  abs/2305.20050, 2024. doi: 10.48550/ARXIV.2305.
                                                                        improves reasoning. CoRR, abs/2505.22660, 2025. doi:
  20050.     URL https://doi.org/10.48550/
                                                                        10.48550/ARXIV.2505.22660. URL https://doi.
  arXiv.2305.20050.
                                                                        org/10.48550/arXiv.2505.22660.
Lin, Y., Tang, S., Lyu, B., Yang, Z., Chung, J.-H., Zhao,
                                                                      QwenTeam. Qwq-32b: Embracing the power of reinforce-
  H., Jiang, L., Geng, Y., Ge, J., Sun, J., Wu, J., Gesi, J.,
                                                                       ment learning, March 2025. URL https://qwenlm.
  Lu, X., Acuna, D., Yang, K., Lin, H., Choi, Y., Chen, D.,
                                                                       github.io/blog/qwq-32b/.
  Arora, S., and Jin, C. Goedel-prover-v2: Scaling formal
  theorem proving with scaffolded data synthesis and self-            Rafailov, R., Sharma, A., Mitchell, E., Manning, C. D.,
  correction, 2025. URL https://arxiv.org/abs/                          Ermon, S., and Finn, C. Direct preference optimization:
  2508.03613.                                                           Your language model is secretly a reward model. In Oh,
                                                                        A., Naumann, T., Globerson, A., Saenko, K., Hardt, M.,
math-ai Team. Amc23: American mathematics compe-
                                                                        and Levine, S. (eds.), Advances in Neural Information
 titions 2023 test set. https://huggingface.co/
                                                                        Processing Systems 36: Annual Conference on Neural
 datasets/math-ai/amc23, 2024. Hugging Face
                                                                        Information Processing Systems 2023, NeurIPS 2023,
 dataset; 40 AMC 2023 problems; accessed 2025-09-16.
                                                                        New Orleans, LA, USA, December 10 - 16, 2023, 2023.
OpenAI. GPT-4 technical report. CoRR, abs/2303.08774,
  2023. doi: 10.48550/ARXIV.2303.08774. URL https:                    Ren, Z. Z., Shao, Z., Song, J., Xin, H., Wang, H., Zhao,
 //doi.org/10.48550/arXiv.2303.08774.                                   W., Zhang, L., Fu, Z., Zhu, Q., Yang, D., Wu, Z. F.,
                                                                        Gou, Z., Ma, S., Tang, H., Liu, Y., Gao, W., Guo, D.,
OpenCompass.      AIME     2025 Benchmark.                              and Ruan, C. Deepseek-prover-v2: Advancing formal
  https://huggingface.co/datasets/                                      mathematical reasoning via reinforcement learning for
  opencompass/AIME2025, 2025.                                           subgoal decomposition. CoRR, abs/2504.21801, 2025.

                                                                 11
                                JURY-RL: Votes Propose, Proofs Dispose for Label-Free RLVR

  doi: 10.48550/ARXIV.2504.21801. URL https://                          R., Edunov, S., and Scialom, T. Llama 2: Open founda-
  doi.org/10.48550/arXiv.2504.21801.                                    tion and fine-tuned chat models. CoRR, abs/2307.09288,
                                                                        2023. doi: 10.48550/ARXIV.2307.09288. URL https:
Shafayat, S., Tajwar, F., Salakhutdinov, R., Schneider, J.,             //doi.org/10.48550/arXiv.2307.09288.
  and Zanette, A. Can large reasoning models self-train?
  CoRR, abs/2505.21444, 2025. doi: 10.48550/ARXIV.                    Wang, X., Wei, J., Schuurmans, D., Le, Q. V., Chi,
  2505.21444. URL https://doi.org/10.48550/                            E. H., Narang, S., Chowdhery, A., and Zhou, D. Self-
  arXiv.2505.21444.                                                    consistency improves chain of thought reasoning in lan-
Shao, Z., Wang, P., Zhu, Q., Xu, R., Song, J., Bi, X.,                 guage models. In International Conference on Learning
  Zhang, H., Zhang, M., Li, Y. K., Wu, Y., and Guo, D.                 Representations, 2023. URL https://openreview.
  Deepseekmath: Pushing the limits of mathematical rea-                net/forum?id=pZ3i2yt5DoY.
  soning in open language models. CoRR, abs/2402.03300,
                                                                      Wang, Y., Ma, X., Zhang, G., Ni, Y., Chandra, A., Guo, S.,
  2024. doi: 10.48550/ARXIV.2402.03300. URL https:
                                                                       Ren, W., Arulraj, A., He, X., Jiang, Z., Li, T., Ku, M.,
  //doi.org/10.48550/arXiv.2402.03300.
                                                                       Wang, K., Zhuang, A., Fan, R., Yue, X., and Chen, W.
Sheng, G., Zhang, C., Ye, Z., Wu, X., Zhang, W., Zhang,                Mmlu-pro: A more robust and challenging multi-task lan-
  R., Peng, Y., Lin, H., and Wu, C. Hybridflow: A flexible             guage understanding benchmark. CoRR, abs/2406.01574,
  and efficient RLHF framework. In Proceedings of the                  2024. doi: 10.48550/ARXIV.2406.01574. URL https:
  Twentieth European Conference on Computer Systems,                   //doi.org/10.48550/arXiv.2406.01574.
  EuroSys 2025, Rotterdam, The Netherlands, 30 March
  2025 - 3 April 2025, pp. 1279–1297. ACM, 2025. doi: 10.             Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B.,
  1145/3689031.3696075. URL https://doi.org/                           Xia, F., Chi, E., Le, Q., and Zhou, D. Chain-of-thought
  10.1145/3689031.3696075.                                             prompting elicits reasoning in large language models.
                                                                       CoRR, abs/2201.11903, 2022. doi: 10.48550/ARXIV.
Shi, J., Yuan, Z., Liu, Y., Huang, Y., Zhou, P., Sun, L., and          2201.11903. URL https://doi.org/10.48550/
  Gong, N. Z. Optimization-based prompt injection attack               arXiv.2201.11903.
  to llm-as-a-judge, 2025. URL https://arxiv.org/
  abs/2403.17710.                                                     Yang, A., Li, A., Yang, B., Zhang, B., Hui, B., Zheng, B.,
                                                                        Yu, B., Gao, C., Huang, C., Lv, C., Zheng, C., Liu, D.,
Su, Y., Yu, D., Song, L., Li, J., Mi, H., Tu, Z., Zhang,
                                                                        Zhou, F., Huang, F., Hu, F., Ge, H., Wei, H., Lin, H., and
  M., and Yu, D. Crossing the reward bridge: Expand-
                                                                        et al. Qwen3 technical report. CoRR, abs/2505.09388,
  ing RL with verifiable rewards across diverse domains.
                                                                        2025a. doi: 10.48550/ARXIV.2505.09388. URL https:
  CoRR, abs/2503.23829, 2025. doi: 10.48550/ARXIV.
                                                                        //doi.org/10.48550/arXiv.2505.09388.
  2503.23829. URL https://doi.org/10.48550/
  arXiv.2503.23829.                                                   Yang, A., Yang, B., Zhang, B., Hui, B., Zheng, B., Yu, B.,
Thakur, A. S., Choudhary, K., Ramayapally, V. S.,                       Li, C., Liu, D., Huang, F., Wei, H., Lin, H., Yang, J.,
  Vaidyanathan, S., and Hupkes, D. Judging the judges:                  Tu, J., Zhang, J., Yang, J., Yang, J., Zhou, J., Lin, J.,
  Evaluating alignment and vulnerabilities in llms-as-                  Dang, K., Lu, K., Bao, K., Yang, K., Yu, L., Li, M., Xue,
  judges, 2025. URL https://arxiv.org/abs/                              M., Zhang, P., Zhu, Q., Men, R., Lin, R., Li, T., Tang,
  2406.12624.                                                           T., Xia, T., Ren, X., Ren, X., Fan, Y., Su, Y., Zhang,
                                                                        Y., Wan, Y., Liu, Y., Cui, Z., Zhang, Z., Qiu, Z., and
Touvron, H., Martin, L., Stone, K., Albert, P., Almahairi,              et al. Qwen2.5 technical report. CoRR, abs/2412.15115,
  A., Babaei, Y., Bashlykov, N., Batra, S., Bhargava, P.,               2025b. doi: 10.48550/ARXIV.2412.15115. URL https:
  Bhosale, S., Bikel, D., Blecher, L., Canton-Ferrer, C.,               //doi.org/10.48550/arXiv.2412.15115.
  Chen, M., Cucurull, G., Esiobu, D., Fernandes, J., Fu,
  J., Fu, W., Fuller, B., Gao, C., Goswami, V., Goyal, N.,            Yu, Q., Zhang, Z., Zhu, R., Yuan, Y., Gao, H., Kulkarni, A.,
  Hartshorn, A., Hosseini, S., Hou, R., Inan, H., Kardas,               Hui, B., Li, L., Xu, Z., Jiang, M., Liu, Q., Zhu, X., Chen,
  M., Kerkez, V., Khabsa, M., Kloumann, I., Korenev, A.,                D., Li, L., Cheng, W., Zhang, Y., Zhang, T., Zhang, H.,
  Koura, P. S., Lachaux, M., Lavril, T., Lee, J., Liskovich,            Shang, C., Cheng, Y., Pu, Q., Yang, F., Jiang, Y., Hao,
  D., Lu, Y., Mao, Y., Martinet, X., Mihaylov, T., Mishra, P.,          X., Wang, S., Tian, W., Xi, Y., Wang, B., Li, C., Guo, J.,
  Molybog, I., Nie, Y., Poulton, A., Reizenstein, J., Rungta,           Ouyang, H., Wang, K., Timmons, B., and et al. Dapo: An
  R., Saladi, K., Schelten, A., Silva, R., Smith, E. M., Sub-           open-source llm reinforcement learning system at scale.
  ramanian, R., Tan, X. E., Tang, B., Taylor, R., Williams,             CoRR, abs/2503.14476, 2025. doi: 10.48550/ARXIV.
  A., Kuan, J. X., Xu, P., Yan, Z., Zarov, I., Zhang, Y., Fan,          2503.14476. URL https://doi.org/10.48550/
  A., Kambadur, M., Narang, S., Rodriguez, A., Stojnic,                 arXiv.2503.14476.

                                                                 12
                               JURY-RL: Votes Propose, Proofs Dispose for Label-Free RLVR

Zhang, Z., Zhu, J., Ge, X., Zhao, Z., Zhou, Z., Li, X., Feng,
  X., Yao, J., and Han, B. Co-reward: Self-supervised
  reinforcement learning for large language model reason-
  ing via contrastive agreement. CoRR, abs/2508.00410,
  2025. doi: 10.48550/ARXIV.2508.00410. URL https:
  //doi.org/10.48550/arXiv.2508.00410.
Zhao, A., Wu, Y., Yue, Y., Wu, T., Xu, Q., Lin, M.,
  Wang, S., Wu, Q., Zheng, Z., and Huang, G. Abso-
  lute zero: Reinforced self-play reasoning with zero data.
  CoRR, abs/2505.03335, 2025a. doi: 10.48550/ARXIV.
  2505.03335. URL https://doi.org/10.48550/
  arXiv.2505.03335.

Zhao, X., Kang, Z., Feng, A., Levine, S., and Song,
  D.    Learning to reason without external rewards.
  CoRR, abs/2505.19590, 2025b. doi: 10.48550/ARXIV.
  2505.19590. URL https://doi.org/10.48550/
  arXiv.2505.19590.

Zhao, Y., Liu, H., Yu, D., Kung, S. Y., Mi, H., and Yu, D.
  One token to fool llm-as-a-judge, 2025c. URL https:
  //arxiv.org/abs/2507.08794.
Zhou, J., Lu, T., Mishra, S., Brahma, S., Basu, S., Luan, Y.,
  Zhou, D., and Hou, L. Instruction-following evaluation
  for large language models. CoRR, abs/2311.07911, 2023.
  doi: 10.48550/ARXIV.2311.07911. URL https://
  doi.org/10.48550/arXiv.2311.07911.
Zuo, Y., Zhang, K., Qu, S., Sheng, L., Zhu, X.,
  Qi, B., Sun, Y., Cui, G., Ding, N., and Zhou,
  B. TTRL: Test-time reinforcement learning. CoRR,
  abs/2504.16084, 2025. URL https://doi.org/10.
  48550/arXiv.2504.16084.




                                                                13
                               JURY-RL: Votes Propose, Proofs Dispose for Label-Free RLVR

Organization of the Appendix. For navigation, Appendix A presents the theoretical analysis (stability of JURY-RL and
the zero-mean property of ResZero). Appendix B gives the full algorithm and a worked example of reward computation.
Appendix C details the Lean Verifier (components, cost trade-offs, and full prompt templates). Appendices D–F cover
baselines, hyperparameters, and evaluation metrics. Appendix G provides extended empirical analyses (sensitivity, pass@k,
and test-time training results). Appendix H presents a qualitative case study comparing an LLM-as-a-judge with the formal
verifier.

A. Theoretical Analysis
This section gives a minimal, checkable account of why Jury-RL stabilizes policy optimization.

   • §A.1 — Why naive majority voting is brittle. We show that, under GRPO, majority-vote rewards conflate agreement
     with correctness: as the majority share increases, supporters’ advantages go to zero while dissenters’ penalties blow up,
     driving entropy collapse.
   • §A.2 — ResZero is zero-mean with non-degenerate variance. We prove the group reward strictly sums to zero
     with the choice γ = cα2 , and that the group variance is non-zero whenever residual answers are not all identical, so
     gradients remain informative when verification fails (Eq. 6).
   • §A.3 — Fallback comparison (MV / Zero / ResZero). We derive group-normalized advantages for each fallback and
     show that only ResZero yields a corrective (negative for unverifiable majorities) yet exploratory (variance preserved on
     residuals) update, aligning with the stability observed in §5.3.

A.1. Why naive majority voting is brittle.
We retain the previously derived analysis showing that majority voting (MV) conflates agreement with correctness and
induces entropy collapse under GRPO as consensus strengthens. Using MV as a label-free reward conflates single-view
agreement with correctness and induces entropy collapse. For a question x, sample G rollouts yi ∼ πθ (· | x) and parse
                                           PG                                     1
                                                                                    PG
answers ai = ans(yi ). Let â = arg maxa j=1 I[aj = a] with vote share v̂ = G        j=1 I[a  = â]. MV assigns binary
         MV
                                                                                           pj
rewards ri = I[ai = â]. Under GRPO, group-normalized advantages satisfy r = v̂, std = v̂(1 − v̂), hence
                                                         q
                                                              1−v̂
                                                                v̂ ,    ai = â,
                                               MV
                                              r −r 
                                      Âi = i          =      q
                                                std      −        v̂
                                                                      , a ̸= â .
                                                                      1−v̂   i


As a spurious consensus strengthens (v̂ → 1), supporters receive vanishing signal (Â+i → 0) while dissenters incur diverging
penalties (Â−
             i → −∞),   suppressing    exploration and shrinking the token-level entropy toward a single mode; ratio clipping
preserves the sign of Âi , so the collapse persists. Because riMV ignores ground truth, MV is also vulnerable to formatting
hacks: repeated insertion of a frequent symbol in the “answer box” can maximize agreement without correctness.

A.2. Proof of Zero-Mean Property for ResZero Reward
Proposition (Zero-mean property of ResZero). Consider any group of G ≥ 1 trajectories, with majority set M , residual
set R, and majority share α = |M |/G. Let the ResZero reward riResZero be defined as in Equation (6) with γ = cα2 . Then,
for all possible vote patterns (including ties and degenerate cases),
                                                      G
                                                      X
                                                            riResZero = 0.
                                                      i=1

This property is critical for ensuring stable optimization for different RL methods.

Edge cases. (i) Tie-breaking When multiple answers tie for the most frequent, we select a single â by a fixed rule, so
M = {i : ai = â} and R = {i : ai ̸= â} are uniquely defined. (ii) No residuals
                                                                           P If all G trajectories coincide, then
|R| = 0, |M | = G, and the residual sum is zero. The total reward becomes i∈M riResZero = |M |(−cα + γ). With
α = |M |/G = 1 and γ = cα2 = c, this equals G(−c + c) = 0. (iii) Single dissenter (|R| = 1) With a single residual

                                                               14
                               JURY-RL: Votes Propose, Proofs Dispose for Label-Free RLVR

trajectory, α = (G − 1)/G and ū coincides with the unique zi , so the dissenter receives r = α(zi − ū) + γ = γ =
cα2 > 0, while each of the |M | = G − 1 majority members    receives −cα   + γ = cα(α − 1) < 0. The total sum is
cα2 + (G − 1) cα(α − 1) = cα α + (G − 1)(α − 1) = cα Gα − (G − 1) = 0, using Gα = G − 1. Thus the zero-mean
property also holds in the minimal-residual case, in which a lone dissenter is positively credited while the over-represented
majority is uniformly down-weighted.
We now present the proof for the general case where |R| > 0. The total sum of rewards is decomposed as:
                                         G
                                         X                    X                   X
                                                riResZero =         riResZero +         riResZero
                                         i=1                  i∈M                 i∈R


Step 1: Calculate the sum of rewards for the residual group (R). For any trajectory i ∈ R, the reward is riResZero =
α · (zi − ū) + γ. Summing over all members of the residual group:
                                        X               X
                                            riResZero =     [α(zi − ū) + γ]
                                           i∈R                 i∈R
                                                                X                       X
                                                          =α             (zi − ū) +          γ
                                                                i∈R                     i∈R
                                                                                P
By the definition of a mean, the sum of deviations from the mean is zero, i.e., i∈R (zi − ū) = 0. This simplifies the total
reward for the residual group to:         X
                                               riResZero = α · 0 + |R| · γ = |R|γ
                                           i∈R


Step 2: Calculate the sum of rewards for the majority group (M). For any trajectory i ∈ M , the reward is riResZero =
−cα + γ. Since the reward is identical for all members of the majority group, the sum is:
                                              X
                                                 riResZero = |M | · (−cα + γ)
                                                i∈M


Step 3: Combine the sums from both groups.             We add the sums from Step 1 and Step 2 to find the total sum:
                                         G
                                         X
                                                riResZero = |M |(−cα + γ) + |R|γ
                                          i=1
                                                         = −cα|M | + (|M | + |R|)γ
Since |M | + |R| = G, the equation becomes:
                                                 G
                                                 X
                                                       riResZero = −cα|M | + Gγ
                                                 i=1


Step 4: Derivation of the Global Re-centering Term γ. To enforce the zero-mean property, we design the global
re-centering term γ such that the total sum from Step 3 is identically zero.
                                                   −cα|M | + Gγ = 0
                                                                             cα|M |
                                                                      γ=
                                                                               G
By substituting the definition of the majority share, α = |M |/G, we arrive at the required form for γ:
                                                                 
                                                             |M |
                                                   γ = cα           = cα2
                                                              G
This derivation shows that setting γ = cα2 is the precise design choice required to make the ResZero reward strictly
zero-centered. This term acts as a global offset that exactly balances the penalties applied to the majority group and the
rewards distributed among the residual group.

                                                                    15
                                 JURY-RL: Votes Propose, Proofs Dispose for Label-Free RLVR

A.3. Fallback Rewards for Inconclusive Verification
This section provides a theoretical analysis of different fallback reward mechanisms within the GRPO framework for the
scenario where formal verification of the majority-voted answer is inconclusive (δ = 0). The analysis focuses on the
dynamics of the group-normalized advantage, Âi , which serves as the learning signal for the policy update. The advantage
is defined as:
                                                                                  G
                                                 ri − r̄                       1 X
                                    Âi =                     ,  where    r̄ =       rj .
                                          std({rj }Gj=1 ) + ε                  G j=1

We analyze three cases: rewarding the majority vote (MV), assigning a zero reward, and using our proposed ResZero reward.

C ASE 1: M AJORITY VOTING (MV) R EWARD
As established in Appendix A.1, if we naively reward the majority consensus when verification fails, thepreward is
riMV = I[ai = â]. Let v̂ be the vote share of the majority answer â. The key statistics are r̄ = v̂ and std({rj }) = v̂(1 − v̂).
This yields the following advantage:
                                                  q
                                                   1−v̂ ,      if ai = â (Supporter)
                                           Âi =      qv̂
                                                  −       v̂
                                                         1−v̂ , if ai ̸= â (Dissenter)


Theoretical Implication. As a spurious consensus strengthens (v̂ → 1), the advantage for supporters vanishes (Â+
                                                                                                                i → 0)
while the penalty for dissenters diverges (Â−
                                             i  →  −∞).  This dynamic  punishes any exploration and provides no positive
signal for adhering to the consensus, leading to entropy collapse and policy degradation.

C ASE 2: Z ERO R EWARD
A seemingly safe alternative is to assign a zero reward to all rollouts when verification is inconclusive. In this case, riZero = 0
for all i ∈ {1, . . . , G}.
The resulting statistics are trivial:

                       1
                                PG
   • Mean Reward: r̄ = G           i=1 0 = 0.
                                            q       PG
                                                1                  2 = 0.
   • Standard Deviation: std({rj }) =           G    i=1 (0 − 0)


Substituting these into the advantage formula gives:
                                                                 0−0
                                                         Âi =       =0
                                                                 0+ε

Theoretical Implication. The advantage signal is nullified for all rollouts in the group. This leads to a vanishing gradient
for the policy update, effectively stalling the learning process for that entire batch. While it avoids the destructive collapse of
MV, it does so at the cost of learning efficiency, rendering the update step ineffective.

C ASE 3: R ES Z ERO R EWARD
The ResZero reward is designed specifically to address the shortcomings of the above methods. It has two crucial properties
by construction:
                                                                                         PG      ResZero
   • Zero-Mean Property: The total reward across the group sums to zero, i.e.,              i=1 ri       = 0. This immediately
     implies the mean reward is r̄ = 0.

   • Non-Zero Variance: By assigning a negative reward to the majority group and a structured, zero-mean reward
     to the residual group, riResZero is non-zero for most rollouts (unless all residual answers are identical). Therefore,
     std({rj }) > 0 as long as there is diversity among residual answers.

                                                                   16
                               JURY-RL: Votes Propose, Proofs Dispose for Label-Free RLVR

The advantage function thus becomes:

                                                    riResZero − 0      riResZero
                                           Âi =                  =
                                                   std({rj }) + ε   std({rj }) + ε

Theoretical Implication. This formulation establishes a stable, self-regulating update dynamic that avoids the extremes
of vanishing gradients (Case 2) or diverging penalties (Case 1). Intuitively, ResZero operates as a damped correction
mechanism:

  • Adaptive Penalization: If the model is uncertain (small majority share α), the corrective signal is mild. However, if
    the model is confidently wrong (large α but unverified), both the majority penalty and residual amplification scale up.
    This specifically targets spurious consensus without destabilizing early training.

  • Stability against Oscillations: Unlike a binary flip, ResZero redistributes probability mass toward residuals propor-
    tional to their internal support zi (as defined in §A.2). This creates a zero-mean, variance-preserving gradient that
    gently pushes the policy toward a more balanced mixture rather than inducing unbounded oscillations.

This mechanism explains the stability observed in our experiments (§5.3): ResZero provides a directional signal to undo
unverified confidence while GRPO ensures the updates remain bounded.
In summary, our theoretical analysis reveals that each fallback strategy results in a fundamentally different learning dynamic:

  • Majority Voting (MV) leads to a destructive update. As a spurious consensus strengthens, it creates a diverging
    penalty for dissent while the positive signal for supporters vanishes. This dynamic ultimately causes entropy collapse,
    suppressing exploration and degrading the policy.

  • Zero Reward results in an ineffective update. By nullifying the reward for all rollouts, the advantage signal becomes
    zero for the entire group. This causes a vanishing gradient that stalls the learning process for that step, wasting
    computational resources.

  • ResZero Reward provides a constructive update. It maintains a stable, non-zero learning signal that is both corrective,
    by penalizing the unverified majority consensus, and exploratory, by rewarding promising alternatives among the
    residual answers.


B. Implementation Details
B.1. The JURY-RL Algorithm
The full algorithm is summarized in Algorithm 1.

Algorithm 1 JURY-RL (one grouped update for a prompt x)
 1: Sample G rollouts yi ∼ πold (· | x); parse ai = ans(yi ).
 2: Compute vote shares v(a) and majority â ∈ arg maxa v(a).
 3: Query verifier once: δ = verify(x, â).
 4: if δ=1 then
 5:    Set ri = I[ai = â].
 6: else
 7:    Form M, R; compute u(−i) and ū; set ri via Eq. (6).
 8: end if
 9: Compute group-normalized advantages Âi from {ri }G    i=1 ; broadcast token-wise.
10: Update πθ with GRPO (clipped ratios, KL to reference).




                                                              17
                               JURY-RL: Votes Propose, Proofs Dispose for Label-Free RLVR

B.2. An Intuitive Example of the ResZero Reward
Consider a scenario with G = 8 rollouts for a given problem. A majority vote reveals that |M | = 4 rollouts support a
proposal â, so the majority share is α = |M |/G = 4/8 = 0.5. The remaining |R| = 4 residual rollouts are split: three
support answer b, and one supports answer c. If the verifier is inconclusive (δ = 0), the ResZero reward is activated.
First, we analyze the residual group R. For a trajectory yi with answer ai = b, its leave-one-out support within the residual
                              2
group is zi = u(−i) (b) = |R|−1   = 2/3. For the singleton answer ai = c, the support is zi = u(−i) (c) = 0/3 = 0. The
                                                             1
average support across the residual group is therefore ū = |R| (3 · 32 + 1 · 0) = 0.5.

Let the penalty hyperparameter be c = 0.1. The global re-centering term is γ = cα2 = 0.1 · (0.5)2 = 0.025. The final
reward for each trajectory is assigned according to Eq. (6):
                     
                     
                     
                      −cα + γ = −0.1(0.5) + 0.025 = −0.025,                         if i ∈ M (proposal â)
                     
         riResZero = α(zi − ū) + γ = 0.5( 32 − 0.5) + 0.025 = 12
                                                                1
                                                                  + 0.025 ≈ 0.1083, if i ∈ R, ai = b
                     
                     
                     
                     α(z − ū) + γ = 0.5(0 − 0.5) + 0.025 = −0.225,
                           i                                                         if i ∈ R, ai = c
                                                                1
By design, the total reward sums exactly to zero: 4(−0.025)+3( 12 +0.025)+1(−0.225) = −0.1+0.25+0.075−0.225 = 0.
This demonstrates how ResZero penalizes the unverifiable majority while redistributing a zero-mean signal among diverse
residual answers. This maintains a useful, variance-driven learning gradient for GRPO without reinforcing a potentially
spurious consensus.

C. Lean Verifier Details
C.1. Lean Verifier
Lean (de Moura & Ullrich, 2021) has emerged as a transformative framework in the formal verification of mathematical
proofs, grounded in a rigorous type-theoretic foundation that guarantees unprecedented levels of logical soundness and
mechanized reliability. Its intrinsic dependency on computer-assisted compilation environments not only ensures formal
correctness but also serves as a high-fidelity feedback mechanism for refining and validating mathematical reasoning within
LLMs.
In response to this potential, we have designed and implemented a comprehensive mathematical verification system centered
on Lean. This system bridges the gap between informal natural language mathematics and machine-verifiable formalism by
automatically translating problem statements and proposed solutions into syntactically and semantically well-formed Lean
expressions, followed by formal proof verification via Lean’s trusted kernel.
The architecture of this verification system (illustrated in Figure 4 ) is a cascaded, modular pipeline comprising three
specialized components:

  • Autoformalizer Translates natural language mathematical content (question—answer pairs in our setting) into precise,
    executable Lean formal specifications, preserving both syntactic structure and semantic intent.
  • Consistency-Checker Performs bidirectional semantic alignment between the original input of natural language and
    its formalized Lean counterpart, ensuring fidelity of meaning and detecting potential misinterpretations or translation
    artifacts.
  • Prover Synthesizes formal proof scripts in Lean and submits them to the theorem prover for mechanized validation,
    thus certifying the logical correctness of the solution under the foundational logic of the system.

This framework not only advances the automation of mathematical reasoning verification, but also establishes a scalable,
feedback-driven paradigm for integrating formal methods into natural language-based mathematical systems.

C.2. Setting
To ensure reliable and precise reward signals, our Lean Verifier employs a three-stage inference pipeline composed of the
following core components:

                                                             18
                                  JURY-RL: Votes Propose, Proofs Dispose for Label-Free RLVR




Figure 4. The pipeline of our Lean Verifier: a collaborative system that combines autoformalization, formal verification, and consistency
checking to validate mathematical reasoning with high reliability.


   • Autoformalizer: Utilizes the Goedel-Formalizer-V2-32B model (Lin et al., 2025) to translate informal mathematical
     statements into formal Lean specifications.
   • Consistency-Checker: Implemented using QwQ-32B (QwenTeam, 2025), this component validates the outputs of the
     Autoformalizer.
   • Prover: Employs the Goedel-Prover-V2-32B model (Lin et al., 2025) to synthesize formal proofs for the specifications
     that have been validated in the previous stage.

The pipeline operates as follows: first, the Autoformalizer generates up to 8 candidate formalizations. The Consistency-
Checker then evaluates effective candidates and selects one checked candidate. Finally, the Prover conducts up to 16
independent sampling trials to find a valid proof.
All formal verification outputs were generated under the same hyperparameter configuration below:

   • Temperature: 0.7
   • Maximum Tokens: 32,768

We make this configuration choice to balance exploration, fidelity, and resource efficiency.

C.3. Component-wise Accuracy Analysis
To better understand the reliability of our reward signal, we evaluated the independent performance of the Autoformalizer
and Consistency Checker on the MATH500 dataset.
Autoformalizer Reliability. We evaluated the autoformalization success rate. The Autoformalizer successfully generated
syntactically valid and type-checkable Lean 4 statements for 477 out of 500 problems, yielding a success rate of 95.4%.
This high coverage ensures that the vast majority of mathematical problems can be converted into a verifiable format.
Consistency Checker Accuracy. The Consistency Checker is responsible for filtering out formalizations that are syntacti-
cally valid but semantically inconsistent with the original problem. As shown in Table 5, the model achieves an F1-score
of 91.1% and a Recall of 94.9%, demonstrating its effectiveness in maintaining semantic fidelity without aggressively
discarding valid candidates.

                                      Table 5. Performance metrics of our Consistency Checker.

                             Metric                      Accuracy       Precision     Recall    F1-score
                             Consistency Checker           85.3%         87.7%        94.9%       91.1%


                                                                   19
                                JURY-RL: Votes Propose, Proofs Dispose for Label-Free RLVR

Held-out Verifier Signal Quality. To address the concern that the MATH500 evaluation above overlaps with the training
distribution, we additionally evaluate both components on external held-out benchmarks that were not used to train or tune
any part of the pipeline. Table 6 reports the Consistency Checker on two out-of-distribution benchmarks and Table 7 reports
the Autoformalizer success rate on four external datasets spanning textbook, olympiad, and competition mathematics.

                       Table 6. Held-out evaluation of the Consistency Checker on two external benchmarks.

                   Benchmark                                   Accuracy      Precision     Recall     F1-score
                   ReformBench-859(Chen et al., 2025)            80.4%         80.1%       94.2%       86.6%
                   CriticleanBench(Peng et al., 2025)            84.4%         82.1%       88.0%       84.9%


                         Table 7. Held-out success rate of the Autoformalizer on four external benchmarks.

                         Benchmark        miniF2F      ProofNet      Putnam      AIME 2025          AVG
                         Success rate      97.1%         71.5%        74.2%          66.7%          77.4%

Two observations follow. First, the Consistency Checker maintains strong performance on out-of-distribution data, with
F1 above 84% on both external benchmarks and recall remaining high (94.2% / 88.0%); the checker does not aggressively
discard valid formalizations on unseen problems. Second, the Autoformalizer shows domain-dependent variation: near-
perfect on miniF2F (97.1%) but lower on harder competition problems (Putnam 74.2%, AIME 2025 66.7%). Crucially,
autoformalization failures are conservative errors: they produce δ = 0 (inconclusive verification) and fall back to ResZero,
rather than emitting false-positive rewards. Lower autoformalization coverage therefore reduces supervision density on the
hardest domains without compromising reward precision, which is consistent with our precision-first design.
Combined with the formal soundness of the Lean Prover (which has a false positive rate of 0%), these components ensure
that JURY-RL receives a reward signal that is both high-coverage and high-precision.

C.4. Performance and Cost Analysis
A crucial factor for the practical implementation of JURY-RL is the computational overhead introduced by the formal Lean
Verifier, especially when compared to baselines like an LLM-as-a-Judge. To provide a clear and quantitative assessment of
this cost, we conducted a wall-clock time analysis using the Qwen-2.5-7B model. The evaluation was performed under the
synchronous RL training configuration specified in our main paper.

Initial (Cold-Start) Overhead. To accurately assess the computational cost, we first establish the baseline training time.
The oracle setting with Ground-Truth (GT) rewards, which involves no external verification, requires approximately 100
seconds per step. This duration represents the core training workload.
We then measured the additional verification overhead for the other methods under a worst-case scenario, defined as
processing a batch composed entirely of unseen question-answer (QA) pairs. The specific overheads are as follows:

   • JURY-RL (Lean Verifier): Under the shared setting where each training step processes 128 questions and the verifier
     is called once per question on the majority-vote answer, the Lean-based verification adds an overhead of approximately
     200 seconds per step.

   • LLM-as-a-Judge (Qwen-2.5-72B): Using the judge to score only the majority-vote answer for each of the 128
     questions adds an overhead of approximately 80 seconds per step.

This means that in the initial training stages, the total step time for JURY-RL is approximately 300 seconds (100s for training
+ 200s for verification), compared to 180 seconds for the LLM-as-a-Judge. It is important to note that the efficiency of
JURY-RL is significantly bolstered by an early-stopping mechanism. Although our framework attempts to autoformalize
and prove the statement up to k times (in the pass@k setting), the process terminates immediately upon the first success.
Since we verify the consensus answer derived from majority voting—which has a high probability of correctness—the
prover often succeeds in the very first few attempts, avoiding the computational cost of executing all k trials.

                                                                20
                                JURY-RL: Votes Propose, Proofs Dispose for Label-Free RLVR

Cost Amortization and Convergence. The initial cold-start overhead is not representative of the average cost over
the entire training process. Our framework uses a caching mechanism for all verification results (shown in Fig.4). As
training proceeds and the policy begins to converge, the diversity of generated answers for any given problem stabilizes.
Consequently, an increasing fraction of QA pairs in subsequent batches will have been previously encountered and verified.
These cached results can be retrieved almost instantly, bypassing the expensive formal verification process. In the steady-state
phase of training, this caching effect becomes dominant. The per-step time cost for JURY-RL progressively converges
toward that of the GT baseline, as most verification lookups are resolved via the cache. Therefore, while the initial cost of
the Lean Verifier is higher, this cost is effectively amortized throughout the training run. We contend that this represents an
acceptable and practical trade-off for the substantial gains in reward fidelity, training stability, and final model performance
documented in our main results.

Comparison with LLM-as-a-Judge. Beyond the runtime overhead, another critical aspect of the verifier is the trade-off
between its performance and consumption, which directly impacts both the quality of the reward signal and the operational
cost. To analyze this, we evaluated different prover configurations on the MATH500 dataset and compared them with an
LLM-as-a-judge baseline.
Table 8 summarizes the performance, model size, and runtime characteristics of these configurations. Among the Lean-
based verifiers, the Prover@64 configuration achieves the highest accuracy with the largest end-to-end evaluation time on
MATH500 (655.80 s). In contrast, the Prover@16 configuration, while exhibiting only a slight and acceptable decrease
in performance to 87.6% ACC, reduces the total runtime to 324.31 s. Given this highly favorable trade-off between a
marginal performance drop and substantial cost savings, we adopt Prover@16 as the default Lean-based configuration for
our main experiments. For comparison, Table 8 also reports an LLM-as-a-judge variant based on Qwen2.5-72B-instruct
with four-way majority voting (mv@4). This judge uses a substantially larger model (72B versus 32B) and runs at a much
lower normalized throughput (6.39 versus 102.82 tokens/s in A100-equivalent units). Despite requiring far fewer output
tokens per response, its end-to-end verification time on MATH500 (290.30 s) is therefore comparable to that of Prover@16
(324.31 s), rather than dramatically faster.
Moreover, unlike the Lean-based verifier, the LLM-as-a-judge approach provides no formal guarantees and yields a purely
heuristic natural-language scoring signal, which is more susceptible to inconsistency and reward hacking. Our empirical
results show that the formally verified Prover@16 offers substantially higher reward fidelity and more stable training
dynamics for JURY-RL. Taking both wall-clock runtime and supervision quality into account, we view its additional token
cost as a practical and acceptable investment in verifier quality.

             Table 8. Performance, token cost, and runtime analysis of Lean Verifier and LLM-as-a-judge on MATH500.

                                               MATH500                 Token Costs                          Runtime
 Setting                   Model Size
                                        ACC    TPR    F1-Score    Avg Tokens per Response   Eqv. Speed (tokens/s)     Time Cost (s)
 Prover@16                    32B       87.6   87.6      93.4              5,858                   102.82                324.31
 Prover@32                    32B       89.1   89.1      94.2              6,607                   102.82                506.36
 Prover@64                    32B       91.1   91.1      95.3              6,435                   102.82                655.80
 LLM-as-a-judge (MV@4)        72B       87.2   87.2      93.2              464                      6.39                 290.30



C.5. Prompt
We list the prompts for all three models below for reference.

  Autoformalizer Prompt
  Please autoformalize the following natural language problem statement in Lean 4.
  Use the following theorem name: test problem
  The natural language statement is:
  {informal statement content}.
  Think before you provide the lean statement.



                                                                 21
                             JURY-RL: Votes Propose, Proofs Dispose for Label-Free RLVR

Consistency-Checker System Prompt
Your role is a Lean4 expert, please help me check consistency between natural language expression and its Lean4 proof
statement.
Guidelines for Consistency Checking:
Goal:
Determine if the Lean theorem statement is an exact and faithful formalization of the mathematical problem.
Do not evaluate or consider the answer or the proof. Your sole task is to verify the correctness of the formalization.
Evaluation Stages (All required):
1. Math Assertion Analysis
Identify all structurally and semantically relevant components of the mathematical problem, including variables, types,
quantifiers, constraints, logic structure, conclusion, and so on. The analysis should be based on the actual content of the
text.
2. Lean Statement Analysis (ignore proof part)
Extract all structurally and semantically relevant components from the Lean statement, including variables, types,
conditions, quantifiers, constraints, the final claim, and so on. The analysis should reflect the actual content present in
the Lean code.
3. Comparative Verification
Check for exact correspondence between the math and Lean statements; you may refer to aspects like:
- Semantic alignment, logic structure, and quantifier correctness.
- Preservation of constraints and boundary assumptions.
- Accurate typing and use of variables.
- Syntactic validity and proper Lean usage (free from errors).
- Use of symbols and constructs without semantic drift.
- No missing elements, no unjustified additions, and no automatic corrections or completions.
4. Final Judgement
Based solely on the above analysis, judge whether the Lean statement is a correct and exact formalization of the
mathematical problem.
5. Accuracy Confirmation
If correct: clearly confirm why all elements match.
If incorrect: list all mismatches and explain how each one affects correctness.
Note: While the analysis may be broad and open to interpreting all relevant features, the final judgment must be based
only on what is explicitly and formally expressed in the Lean statement. **Do not consider or assess any part of the
proof. Your judgment should be entirely about the accuracy of the statement formalization.**
You should present the results following the format:
Input:
The Natural Language Statement:
A math problem and its answer (no proof).
The Formal Statement in Lean4:
‘‘‘lean
A Lean 4 theorem statement formalizing the problem. Proof is intentionally omitted (e.g., sorry).
‘‘‘
Output Format:
Return exactly one xml object
<comments>
Your brief analysis:
Math Assertion Analysis: [. . . ]
Lean Statement Analysis (Proof Ignored): [. . . ]
Comparative Verification: [. . . ]
Conclusion: [. . . ]
Accuracy Confirmation: [. . . match confirmation or list of discrepancies. . . ]
</comments>
<consistency>[Correct/Incorrect]</consistency>



                                                            22
                              JURY-RL: Votes Propose, Proofs Dispose for Label-Free RLVR

 Consistency-Checker User Prompt
 Input Data:
 The Natural Language Statement:
 {informal prefix}
 The Formal Statement in Lean4:
 ‘‘‘lean
 {formal statement}
 ‘‘‘

 Prover Prompt
 Complete the following Lean 4 code:
 ‘‘‘ lean4
 {formal statement}
 ‘‘‘
 Before producing the Lean 4 code to formally prove the given theorem, provide a detailed proof plan outlining the main
 proof steps and strategies.
 The plan should highlight key ideas, intermediate lemmas, and proof structures that will guide the construction of the
 final formal proof.


D. Baseline Details
  • Majority Voting (MV). A self-supervised consensus reward (Shafayat et al., 2025). For each problem, we generate
    G rollouts. A rollout yi receives reward 1 if its extracted answer ans(yi ) matches the majority answer among the G
    rollouts, and 0 otherwise. This directly reinforces popular answers regardless of correctness.
  • Self-Certainty. A confidence-derived signal (Zhao et al., 2025b). The reward is computed from the log-probabilities of
    the tokens composing the final answer (as extracted by ans(·)); higher cumulative log-probability indicates greater
    model certainty and yields a higher reward.
  • Entropy Minimization. A low-entropy proxy (Prabhudesai et al., 2025). The reward is inversely related to the policy’s
    output entropy for the final-answer tokens, encouraging more deterministic, high-confidence predictions.
  • CoReward. Contrastive agreement over input-level variants (Zhang et al., 2025). For each training question, CoReward
    generates semantically equivalent paraphrased versions, samples multiple rollouts for both the original and paraphrased
    questions, and aggregates their answers via majority voting to obtain pseudo-consensus labels. These majority-voted
    answers are then used in a cross-over manner as rewards for policy optimization on both sides.
  • Ground Truth (GT). The ground-truth supervised oracle baseline. Using human-annotated labels, a rollout receives 1
    if its extracted answer matches the ground truth and 0 otherwise. We train this baseline with the same GRPO objective
    (Shao et al., 2024) as our method for a fair comparison.
  • LLM-as-a-Judge. An external-judge paradigm (Pang et al., 2023; Zhao et al., 2025a). We employ
    qwen-2.5-72b-instruct as the judge. It assesses the reasoning process and the final answer of each roll-
    out; its evaluation (numeric score or a binary correct/incorrect label) is used as the reward for the RL update. The
    prompt for it is shown below.
  • LLM-KD (Knowledge Distillation). Teacher–student distillation has been used in Label-Free RLVR (Zhao et al.,
    2025a). We use qwen-2.5-72b-instruct to produce an answer for each problem and treat it as a pseudo label.
    The policy model is trained to align its outputs with these machine-generated references.

 LLM-as-a-Judge prompt
 You are a professional math QA pair evaluator. Your sole task is to determine whether a given mathematical question
 and answer are correctly matched. First explain your reasoning, then end your response with your final judgment: True
 or False.


                                                           23
                                 JURY-RL: Votes Propose, Proofs Dispose for Label-Free RLVR

E. Additional Experimental Details
Detailed training and testing settings are provided in Table 9.
Table 9. Reinforcement learning training hyperparameters. This configuration is consistently applied across all experiments to ensure a
fair comparison.


 Hyperparameter                                                                                                             Value
 Training Configuration
 Train Batch size (Number of Sampled Questions)                                                                              128
 Rollouts per problem (G)                                                                                                      8
 Max prompt length                                                                                                            512
 Max new tokens                                                                                                              3072
 Training epoch                                                                                                                6
 Optimizer Parameters (AdamW)
 Learning rate                                                                                                            3 × 10−6
 β1                                                                                                                          0.9
 β2                                                                                                                         0.999
 ϵ                                                                                                                          10−8
 Warmup style                                                                                                              Cosine
 Warmup steps ratio                                                                                                          0.1
 GRPO Algorithm Parameters
 KL loss coefficient (β)                                                                                                    0.005
 clip ratio (ϵ)                                                                                                              0.2
 Generation Parameters
 Training temperature                                                                                                         1.0
 Evaluation temperature                                                                                                       0.8
 top-p                                                                                                                       0.95


F. Benchmark and Metric Details
This section details the specific metrics and software frameworks used for each benchmark mentioned in the main text.

   • AIME24/25, MATH500, GSM8K: We report avg@16 accuracy for AIME24/25, computed by averaging correctness
     over 16 independently sampled solutions per problem, and avg@4 accuracy for MATH500 and GSM8K. All bench-
     marks are evaluated using the lighteval framework: https://github.com/huggingface/lighteval
   • AMC: We report avg@8 accuracy. This is evaluated using the ttrl implementation: https://github.com/
     ruixin31/Spurious_Rewards/tree/main/code/ttrl
   • LiveCodeBench: We report avg@5 accuracy. This is evaluated using the official library: https://github.com/
     LiveCodeBench/LiveCodeBench
   • CRUX: We report avg@5 accuracy. This is evaluated using the ZeroEval framework: https://github.com/
     WildEval/ZeroEval
   • MMLU-Pro, IFEval: We report pass@1 accuracy. This is evaluated using the lm-evaluation-harness:
     https://github.com/EleutherAI/lm-evaluation-harness

G. Further Analysis
G.1. Impact of c
We analyze the impact of the hyperparameter c in Eq. 6, which controls the penalty strength on the unverified majority
proposal in our ResZero reward. As illustrated in Figure 5, c is critical in navigating the trade-off between preventing

                                                                  24
                                                  JURY-RL: Votes Propose, Proofs Dispose for Label-Free RLVR

  mode collapse and maximizing task performance. The right panel clearly demonstrates that a non-zero c is essential for
  maintaining solution diversity. When c = 0, the framework effectively degenerates to a zero-reward fallback, leading to a
  sharp decline in the average number of unique answers as training progresses—a classic symptom of the model converging
  to a spurious consensus. In contrast, any positive c value successfully sustains a high level of diversity. However, the left
  and center panels reveal a subtle trade-off: an overly aggressive penalty (e.g., c = 0.1) can slightly suppress the final reward
  and accuracy. This suggests that while the penalty is crucial for exploration, an excessive value may overly restrict the
  policy from exploiting a potentially correct, high-consensus answer. This ablation validates that a moderately tuned c (e.g.,
  c = 0.01 in our experiments) strikes an optimal balance, ensuring robust training stability and solution diversity without
  compromising convergence on the primary task objectives.


               65.0                                                     0.6




                                                                                                                       Average Unique Answers
                                                                        0.5                                                                     3.2
               62.5
Accuracy (%)




                                                               Reward
               60.0                                  c=0.0              0.4                                  c=0.0                              3.0       c=0.0
                                                     c=0.005                                                 c=0.005                                      c=0.005
               57.5                                  c=0.01                                                  c=0.01                                       c=0.01
                                                                        0.3
                                                     c=0.02                                                  c=0.02                             2.8       c=0.02
               55.0                                  c=0.05                                                  c=0.05                                       c=0.05
                                                     c=0.1              0.2                                  c=0.1                                        c=0.1
               52.5                                                                                                                             2.6
                      0   50   100   150    200    250   300                  0   50   100    150    200   250   300                                  0   50        100   150    200   250   300
                                     Step                                                     Step                                                                        Step

                                            Figure 5. Training dynamics under different values of the hyperparameter c.



  G.2. Pass@k Results
  Main Results across Benchmarks. This appendix complements The Diversity Analysis of JURY-RL in Section 5.2.
  The complete numerical results are listed in Table 10 for easy cross-reference. The pass@k results presented in Table 10
  unequivocally demonstrate the effectiveness of our JURY-RL framework. Across all three backbone models, JURY-RL not
  only surpasses every label-free baseline but also consistently outperforms the strong supervised GT-Reward baseline, which
  is trained directly on ground-truth answers.

  Ablation Study on Fallback Rewards. This appendix complements Ablation Studies of ResZero in Section 5.2. The
  complete numerical results are listed in Table 11 for easy cross-reference with Table 3. Table 11 demonstrates that our
  proposed ResZero fallback reward consistently achieves the highest average performance.

  G.3. Test-Time Training Results
 While our main experiments focus on offline RLVR, recent work has emphasized test-time reinforcement learning (TTRL)
 (Zuo et al., 2025), where the model is adapted on the evaluation distribution itself. To examine whether the conclusions in
 §5.3 also hold in this regime, we instantiate a TTRL variant of JURY-RL and compare it with the majority-vote (MV) reward
 used in the public ttrl implementation. For each benchmark (AIME24, AIME25, AMC23, MATH500 and GSM8K), we
 treat the validation split as the TTRL environment, start from the same base policy, and run GRPO for 30 epochs with the
 hyperparameters in Table 9. We run this setup on two backbones: Qwen2.5-7B (Figure 6) and Qwen2.5-14B (Table 12 and
 Figure 7); in both cases, the only difference between the two runs is the reward: MV vs. our ResZero fallback. To keep the
 14B comparison aligned with the 7B figure, we contrast JURY-RL with the majority-vote baseline (MV-TTRL) only.

 Results on Qwen2.5-7B. On Qwen2.5-7B, the dynamics on AIME24 and AMC highlight the brittleness of MV in
 the test-time setting: the validation reward first increases slightly and then degrades, eventually falling below the initial
 performance, whereas JURY-RL continues to make steady progress with a smoother learning curve, consistent with our
 analysis in Appendix A.1 that spurious consensus under MV drives entropy collapse and hurts generalization. For AIME25
 in particular, the first points in Figure 6 correspond to 0/30 (JURY-RL) and 1/30 (MV) solved problems; since both runs start
 from the same base model, this small gap is due to stochasticity in GRPO rather than an inherent disadvantage of JURY-RL.
 As training proceeds, JURY-RL attains a more stable plateau on AIME25 and still ends slightly ahead of MV, while on
 MATH500 and GSM8K the two curves remain close but JURY-RL consistently finishes higher.

                                                                                             25
                               JURY-RL: Votes Propose, Proofs Dispose for Label-Free RLVR

                   Table 10. Pass@k results (%) of RL performance comparison on math reasoning benchmarks.

                                       AIME24      AIME25     MATH500       GSM8K       AMC
                   Methods                                                                        Average
                                       pass@16     pass@16     pass@4       pass@4     pass@8
                                                     Qwen3-1.7B-Base
                   Before RL             16.67      13.33         72.0       89.31      56.63      49.59
                   GT-Reward             26.67      16.67         82.0       92.42      59.04      55.36
                   LLM-KD                20.00      16.67         82.2       93.25      55.42      53.51
                   Entropy               20.00      23.33         81.2       90.75      59.04      54.86
                   Self-Certainty        23.33      26.67         77.2       90.83      57.83      55.17
                   Majority-Voting       23.33      16.67         77.2       92.34      53.01      52.51
                   CoReward              26.67      16.67         77.4       92.04      54.22      53.40
                   LLM-as-a-Judge        16.67      13.33         74.6       91.74      55.42      50.35
                   JURY-RL (Ours)        30.00      30.00         82.0       92.42      62.65      59.41
                                                   Llama-3.2-3B-Instruct
                   Before RL             23.33       6.67         65.0       86.88      49.40      46.26
                   GT-Reward             23.33       6.67         63.8       90.14      43.37      45.46
                   LLM-KD                23.33       3.33         65.0       89.99      49.40      46.21
                   Entropy               16.67       3.33         58.8       84.46      50.60      42.77
                   Self-Certainty        13.33      10.00         58.0       84.69      44.58      42.12
                   Majority-Voting       16.67       0.00         63.6       90.98      39.76      42.20
                   CoReward              23.33       0.00         60.4       90.45      43.37      43.51
                   LLM-as-a-Judge        26.67      10.00         62.2       89.84      40.96      45.93
                   JURY-RL (Ours)        30.00       3.33         64.8       90.07      54.22      48.48
                                                        Qwen2.5-7B
                   Before RL             30.00      20.00         76.2       93.78      63.86      56.77
                   GT-Reward             33.33      30.00         85.2       95.22      68.67      62.48
                   LLM-KD                33.33      33.33         87.8       95.75      67.47      63.54
                   Entropy               30.00      36.67         85.2       93.78      67.47      62.62
                   Self-Certainty        23.33      30.00         84.6       93.86      69.88      60.33
                   Majority-Voting       33.33      30.00         85.4       95.00      63.86      61.52
                   CoReward              30.00      26.67         83.8       95.60      63.86      59.99
                   LLM-as-a-Judge        20.00      13.33         82.2       95.38      59.04      53.99
                   JURY-RL (Ours)        36.67      30.00         86.6       95.83      71.08      64.04



Results on Qwen2.5-14B. The same pattern holds at 14B scale. As summarized in Table 12, JURY-RL improves AVG
pass@1 by +3.53 points and AVG pass@k by +5.16 points over MV-TTRL on Qwen2.5-14B, with the largest gains on the
hardest competition-style benchmarks (AIME24 pass@1 +6.67, AIME25 pass@1 +6.67, AMC pass@k +10.84). The
training curves in Figure 7 follow the same overall pattern observed at 7B: JURY-RL exhibits smoother and more sustained
improvement than MV-TTRL on AIME24, AIME25, and AMC, whereas MV-TTRL again shows the characteristic initial
gain followed by degradation. Taken together, these results indicate that the benefit of JURY-RL in the test-time setting is
not a 7B-specific phenomenon and transfers to 14B under a matched setup.

G.4. Verifier Branch Dynamics over Training
To characterize how the proof-gated and fallback branches of JURY-RL evolve over training, we tracked two diagnostics on
a Qwen2.5-7B run with group size G = 8 under the main experimental configuration in Table 9. All measurements use
benchmark ground truth as the reference rather than pipeline verifiability, to avoid circular evaluation.

Evolution of the proof-gated fraction P (δ). At checkpoints {0, 50, 100, 200, 400}, the fraction of training steps in which
the plurality answer is formally verified by the Lean pipeline (δ = 1) rises monotonically, while the fallback fraction
P (δ = 0) falls correspondingly (Table 13). This is consistent with our design intent: ResZero acts as an early- and
mid-stage stabilizer when inconclusive verification is common, and is progressively phased out as proof-gated updates
become dominant.

                                                             26
                                                   JURY-RL: Votes Propose, Proofs Dispose for Label-Free RLVR

                          Table 11. Ablation results (Pass@k) for the proposed ResZero reward (δ = 0) on math reasoning benchmark.

                                                                      AIME24           AIME25       MATH500     GSM8K           AMC
                       Methods                                                                                                                 Average
                                                                      pass@16          pass@16       pass@4     pass@4         pass@8
                                                                                 Qwen3-1.7B-Base
                       GT-Reward                                           26.67         16.67           82.0    92.42              59.04       55.36
                       Majority-Voting                                     23.33         16.67           77.2    92.34              53.01       52.51
                       Proof-Gate + Zero Reward                            23.33          6.67           70.2    92.65              46.99       47.97
                       Proof-Gate + Random Reward                          20.00          6.67           78.0    92.34              54.22       50.25
                       Proof-Gate + MV Reward                               0.00          0.00           48.8    92.19              13.25       30.85
                       JURY-RL (Proof-Gate + ResZero)                      30.00         30.00           82.0    92.42              62.65       59.41
                                                                            Llama-3.2-3B-Instruct
                       GT-Reward                                           23.33          6.67           63.8    90.14              43.37       45.46
                       Majority-Voting                                     16.67          0.00           63.6    90.98              39.76       42.20
                       Proof-Gate + Zero Reward                            20.00          6.67           64.0    89.92              40.96       44.31
                       Proof-Gate + Random Reward                          23.33          6.67           62.6    88.32              46.99       45.58
                       Proof-Gate + MV Reward                              20.00          0.00           62.2    89.76              44.58       43.31
                       JURY-RL (Proof-Gate + ResZero)                      30.00          3.33           64.8    90.07              54.22       48.48
                                                                                     Qwen2.5-7B
                       GT-Reward                                           33.33         30.00           85.2    95.22              68.67       62.48
                       Majority-Voting                                     33.33         30.00           85.4    95.00              63.86       61.52
                       Proof-Gate + Zero Reward                            30.00         33.33           85.6    95.38              62.65       61.39
                       Proof-Gate + Random Reward                          33.33         16.67           79.6    93.63              63.86       57.42
                       Proof-Gate + MV Reward                               0.00          0.00           58.2    95.60              19.28       34.62
                       JURY-RL (Proof-Gate + ResZero)                      36.67         30.00           86.6    95.83              71.08       64.04



  Minority-correct missed rate Et . A concern for proof-gated RLVR is that a correct minority answer is overlooked when
  the plurality candidate is wrong and is selected for verification. To quantify this, we define
                                                                                                                    
                                   Et = Pr plurality answer is GT-incorrect ∧ ∃ a minority rollout that is GT-correct .

 At the same checkpoints {0, 50, 100, 200, 400}, Et is reported in Table 14. These missed opportunities are real but not
 dominant: Et peaks at 9.3% during the mid-training phase and then declines to 5.4% by checkpoint 400, as the correct
 answer increasingly coincides with the plurality candidate (the majority-correct rate rises from 50.9% to 67.9% over the
 same training window). Among the remaining groups in which the plurality is wrong, roughly 78–85% contain no correct
 rollout at all, which explains why verifying the top-2 or top-3 candidates instead of top-1 yields little additional benefit
 (Figure 8).


                         AIME24                        AIME25                             AMC                   Math500                         GSM8K
                       JURY-RL             4                                           JURY-RL           65
               9                                                            50
                       TTRL (MV)                                                       TTRL (MV)                                      80
Accuracy (%)




                                           3
                                                                            48                           60
               8                           2
                                                                            45                                                        70
                                           1                                                             55
                                                               JURY-RL      42                                          JURY-RL                          JURY-RL
               7                                               TTRL (MV)                                                TTRL (MV)                        TTRL (MV)
                                           0                                                                                          60
                   0      200        400       0        200         400          0        200      400   50 0    200         400           0     200          400
                          Step                          Step                              Step                   Step                             Step
 Figure 6. Test-Time Training Dynamics on Qwen2.5-7B. We plot exponentially moving-averaged (EMA) validation accuracy for
 Jury-RL (purple) and majority-voting TTRL (orange) over 400 test-time training steps. Jury-RL exhibits more stable and continued
 improvement on challenging benchmarks.


                                                                                         27
                                                   JURY-RL: Votes Propose, Proofs Dispose for Label-Free RLVR

                        AIME24                         AIME25                         AMC                         Math500                        GSM8K
                        JURY-RL                                          60
                                                                                                       70                              90
                        TTRL (MV)
Accuracy (%)


                                          10
               14                                                        50                                                            80
                                           5                                                           60
                                                           JURY-RL       40                JURY-RL                    JURY-RL          70           JURY-RL
               12                                          TTRL (MV)                       TTRL (MV)                  TTRL (MV)                     TTRL (MV)
                                           0                                                           50
                    0            100           0                100           0               100           0              100              0            100
                          Step                           Step                          Step                         Step                          Step
 Figure 7. Test-Time Training Dynamics on Qwen2.5-14B. We plot exponentially moving-averaged (EMA) validation accuracy for
 JURY-RL (purple) and majority-voting TTRL (orange) over 150 test-time training steps. JURY-RL exhibits more stable and continued
 improvement on challenging benchmarks.



 Table 12. Test-time training results on Qwen2.5-14B. Each benchmark cell reports pass@1 / pass@k. The two “AVG” columns are
 averages across the five benchmarks.

        Method              AVG pass@1             AVG pass@k          AIME24              AIME25               AMC                GSM8K         MATH500
        MV-TTRL                   46.23               57.38           10.00 / 20.00    3.33 / 23.33         44.58 / 62.65        94.62 / 95.53   78.60 / 85.40
        JURY-RL                   49.76               62.54           16.67 / 26.67    10.00 / 30.00        46.99 / 73.49        94.54 / 96.74   80.60 / 85.80




  G.5. Deeper Dive into Verifier Imperfections
 While a formal verifier is theoretically sound, its practical application is imperfect. We analyze how the number of
 verification attempts, k in a pass@k setting, affects the quality of the reward signal. As shown in Figure 8, the Lean verifier
 exhibits a highly desirable trade-off.
  The precision (top-left panel) remains consistently high, around 85%. It is crucial to note that this precision gap from
  a perfect 100% is not a flaw in the Lean prover’s core logic, which is formally sound. Instead, it primarily stems from
  imperfections in upstream components like auto-formalization and consistency checks, which translate the problem into a
  verifiable format. Despite this, the signal’s high fidelity is vital for preventing reward hacking and ensuring the model learns
  from genuinely correct examples.
 In contrast, the recall (top-right panel) shows a clear dependency on k. With a single attempt (pass@1), the recall is modest
 (around 30%), but it steadily increases with more attempts, reaching nearly 90% at pass@16. This indicates that while a
 single verification attempt might fail to prove a correct answer (e.g., due to search limits), multiple attempts significantly
 increase the chance of success, thereby improving the richness of the training signal.
  Crucially, despite the wide variance in recall, the final validation accuracy (bottom-left) and training entropy (bottom-
  right) converge to similar stable states across different values of k. This suggests that the high precision of the verifier’s
  signal is the dominant factor for successful and stable training. This behavior stands in stark contrast to an LLM-as-a-Judge.
  Mechanistically, an LLM-judge’s potential for error is inherent to its probabilistic and opaque reasoning process, making it
  fundamentally prone to biases, format gaming, and confident mistakes. Its reward signal is therefore inherently noisier and
  less reliable. The imperfections in our pipeline, however, are largely confined to the modular pre-processing steps, leaving
  the core judgment by the Lean prover itself principled and trustworthy.



  Effect of top-k verification on performance. To quantify how many candidates actually need to be verified, we compare
  JURY-RL training runs on Qwen2.5-7B that verify only the top-1, top-2, or top-3 majority-voting candidates selected by the
  policy, and report accuracy on the MATH5000 validation set in Figure 9. All three curves reach a similar plateau around
  72% accuracy, and they remain almost indistinguishable throughout training, with final differences well within random
  fluctuation. This indicates that almost all useful learning signal is already contained in the highest-probability candidate, and
  additional verified candidates mainly increase computational cost without improving final accuracy. Consequently, we adopt
  the more efficient top@1 verify setting as our default choice in all main experiments.

                                                                                      28
                                 JURY-RL: Votes Propose, Proofs Dispose for Label-Free RLVR

Table 13. Evolution of the proof-gated fraction P (δ = 1) and the fallback fraction P (δ = 0) over training checkpoints on Qwen2.5-7B
(G = 8).

                                      Checkpoint           0      50     100     200      400
                                      P (δ = 1) (%)      53.0    56.7    60.0    66.2     70.7
                                      P (δ = 0) (%)      47.0    43.3    40.0    33.8     29.3

            Table 14. Evolution of the minority-correct missed rate Et over training checkpoints on Qwen2.5-7B (G = 8).

                                          Checkpoint       0     50     100     200     400
                                          Et (%)          7.6    8.7    9.3     7.4     5.4


H. Case Study
To illustrate our “Proofs Dispose” principle, we present a case study comparing an LLM-as-a-Judge with a Lean formal
verifier. This case highlights a core problem with LLM judges: their reliability is limited by their own reasoning. The first
example shows that an LLM judge can reach a wrong conclusion due to flawed reasoning, which generates an incorrect
training signal. In contrast, once the autoformalization and consistency checks are passed, a Lean proof has the property of
zero false positives. As shown in the second example, it provides a definitive and highly reliable signal through formal logic.
This comparison explains why in JURY-RL, we use proofs, not an LLM, to dispose the final reward.
  Question

  Let $x$ and $y$ be positive real numbers such that $3x + 4y < 72.$                                  Find the maximum
      ,→ value of xy (72 - 3x - 4y).


  Answer

  1152


  LLM-as-a-Judge Output (Judge Wrong)

  To evaluate whether the given answer of 1152 is correct for the problem, we need to
      ,→ find the maximum value of the function \( f(x, y) = xy (72 - 3x - 4y) \)
      ,→ subject to the constraint \( 3x + 4y < 72 \).

  First, let’s rewrite the function:
  \[ f(x, y) = xy (72 - 3x - 4y). \]

  We can use the method of Lagrange multipliers or analyze the function directly.
      ,→ However, a simpler approach is to use symmetry and calculus.

  Consider the function \( g(t) = t(72 - 3t - 4t) = t(72 - 7t) = 72t - 7tˆ2 \). This is
      ,→ a quadratic function in terms of \( t \), where \( t = x + y \). The maximum
      ,→ value of this quadratic function occurs at the vertex, which is given by:
  \[ t = -\frac{b}{2a} = -\frac{72}{-14} = \frac{72}{14} = \frac{36}{7}. \]

  Now, we need to find \( x \) and \( y \) such that \( x + y = \frac{36}{7} \) and \(
      ,→ 3x + 4y \) is minimized while still satisfying \( 3x + 4y < 72 \).

  Given the symmetry and the nature of the problem, we can assume \( x = y \). Then:
  \[ 2x = \frac{36}{7} \implies x = \frac{18}{7}. \]
  \[ 3x + 4y = 3\left(\frac{18}{7}\right) + 4\left(\frac{18}{7}\right) =
      ,→ 7\left(\frac{18}{7}\right) = 18. \]

  Substituting \( x = y = \frac{18}{7} \) into the function:


                                                                 29
                                          JURY-RL: Votes Propose, Proofs Dispose for Label-Free RLVR

                100                                                                        100

                 80                                                                         80
Precision (%)




                 60                                                                         60




                                                                              Recall (%)
                 40                                                                         40
                        pass@1                                                                     pass@1
                        pass@2                                                                     pass@2
                 20     pass@4                                                              20     pass@4
                        pass@8                                                                     pass@8
                        pass@16                                                                    pass@16
                  0 0      50     100   150          200   250   300   350                   0 0      50     100   150          200   250   300       350
                                              Step                                                                       Step
                100                                                                        1.0
                                                                                                                                                  pass@1
                                                                                                                                                  pass@2
                 80                                                                        0.8                                                    pass@4
                                                                                                                                                  pass@8
                                                                                                                                                  pass@16
Accuracy (%)




                 60                                                                        0.6

                 40
                        pass@1
                                                                               Entropy     0.4
                        pass@2
                 20     pass@4                                                             0.2
                        pass@8
                        pass@16
                  0 0      50     100   150          200   250   300   350                 0.0 0      50     100   150          200   250   300       350
                                              Step                                                                       Step
 Figure 8. Training dynamics of precision, recall, validation accuracy, and training entropy under different Lean pass@k verification
 settings.



            \[ f\left(\frac{18}{7}, \frac{18}{7}\right) =
                ,→ \left(\frac{18}{7}\right)\left(\frac{18}{7}\right)(72 -
                ,→ 3\left(\frac{18}{7}\right) - 4\left(\frac{18}{7}\right)) \]
            \[ = \left(\frac{18}{7}\right)ˆ2 (72 - 7\left(\frac{18}{7}\right)) \]
            \[ = \left(\frac{18}{7}\right)ˆ2 (72 - 18) \]
            \[ = \left(\frac{18}{7}\right)ˆ2 \cdot 54 \]
            \[ = \frac{324}{49} \cdot 54 \]
            \[ = \frac{17496}{49} \]
            \[ = 357.0612244898. \]

            This value does not match 1152. Therefore, the given answer of 1152 is incorrect.

            Final judgment: False.


            Lean Prover Output (Prove Success)

            import Mathlib
            import Aesop

            set_option maxHeartbeats 0

            open BigOperators Real Nat Topology Rat

            theorem test_problem :
              sSup {z : R | ∃ x y : R, x > 0 ∧ y > 0 ∧ 3*x + 4*y < 72 ∧ z = x * y * (72 - 3*x -
                ,→ 4*y)} = 1152 := by


                                                                             30
                    JURY-RL: Votes Propose, Proofs Dispose for Label-Free RLVR

                                                 Qwen2.5-7B
                                 70




                  Accuracy (%)
                                 60

                                 50
                                                                JURY-RL (verify@3)
                                                                JURY-RL (verify@2)
                                 40                             JURY-RL (verify@1)
                                      0   50   100    150    200     250       300
                                                      Step
                  Figure 9. Accuracy on MATH5000 Validation set over training steps.



have h1 : (1152 : R) ∈ {z : R | ∃ x y : R, x > 0 ∧ y > 0 ∧ 3*x + 4*y < 72 ∧ z = x *
  ,→ y * (72 - 3*x - 4*y)} := by
   refine’ ⟨8, 6, by norm_num, by norm_num, by norm_num, _⟩
   <;> norm_num
   <;> ring_nf
   <;> norm_num

have h2 : ∀ (z : R), z ∈ {z : R | ∃ x y : R, x > 0 ∧ y > 0 ∧ 3*x + 4*y < 72 ∧ z = x
  ,→ * y * (72 - 3*x - 4*y)} → z ≤ (1152 : R) := by
   intro z hz
   rcases hz with ⟨x, y, hx, hy, hxy, rfl⟩
   have h3 : 0 < x := hx
   have h4 : 0 < y := hy
   have h5 : 3 * x + 4 * y < 72 := hxy
   have h6 : 0 < 72 - 3 * x - 4 * y := by linarith
   have h7 : 0 < 3 * x := by positivity
   have h8 : 0 < 4 * y := by positivity
   have h9 : 0 < (3 * x) * (4 * y) := by positivity
   have h10 : 0 < (3 * x) * (4 * y) * (72 - 3 * x - 4 * y) := by positivity
   -- Use AM-GM inequality to show that x * y * (72 - 3 * x - 4 * y) ≤ 1152
   have h11 : (3 * x + 4 * y + (72 - 3 * x - 4 * y)) ˆ 3 ≥ 27 * (3 * x) * (4 * y) *
  ,→ (72 - 3 * x - 4 * y) := by
     nlinarith [sq_nonneg (3 * x - 4 * y), sq_nonneg (3 * x - (72 - 3 * x - 4 * y)),
  ,→ sq_nonneg (4 * y - (72 - 3 * x - 4 * y)),
       mul_nonneg h7 .le h8 .le, mul_nonneg h7 .le h6 .le, mul_nonneg h8 .le h6 .le]
   -- Simplify the inequality to get the desired result
   have h12 : (72 : R) ˆ 3 ≥ 27 * (3 * x) * (4 * y) * (72 - 3 * x - 4 * y) := by
     have h13 : (3 * x + 4 * y + (72 - 3 * x - 4 * y)) = 72 := by ring
     rw [h13 ] at h11
     linarith
   have h13 : x * y * (72 - 3 * x - 4 * y) ≤ 1152 := by
     have h14 : (72 : R) ˆ 3 = 373248 := by norm_num
     have h15 : 27 * (3 * x) * (4 * y) * (72 - 3 * x - 4 * y) = 324 * (x * y * (72 -
  ,→ 3 * x - 4 * y)) := by
       ring
     rw [h14 ] at h12
     rw [h15 ] at h12
     nlinarith
   linarith

have h3 : sSup {z : R | ∃ x y : R, x > 0 ∧ y > 0 ∧ 3*x + 4*y < 72 ∧ z = x * y * (72
  ,→ - 3*x - 4*y)} = 1152 := by




                                                     31
                  JURY-RL: Votes Propose, Proofs Dispose for Label-Free RLVR

  have h4 : IsLUB {z : R | ∃ x y : R, x > 0 ∧ y > 0 ∧ 3*x + 4*y < 72 ∧ z = x * y *
 ,→ (72 - 3*x - 4*y)} 1152 := by
    refine’ ⟨fun z hz => h2 z hz, fun y hy => _⟩
    -- We need to show that 1152 is the least upper bound.
    -- Since 1152 is in the set, any upper bound y must be at least 1152.
    have h5 : (1152 : R) ∈ {z : R | ∃ x y : R, x > 0 ∧ y > 0 ∧ 3*x + 4*y < 72 ∧ z =
 ,→ x * y * (72 - 3*x - 4*y)} := h1
    have h6 : (1152 : R) ≤ y := by
       apply hy
       exact h5
    linarith
  -- The supremum of the set is 1152 because it is the least upper bound.
  have h5 : sSup {z : R | ∃ x y : R, x > 0 ∧ y > 0 ∧ 3*x + 4*y < 72 ∧ z = x * y *
 ,→ (72 - 3*x - 4*y)} = 1152 := by
    apply le_antisymm
    · -- Show that the supremum is less than or equal to 1152.
       apply csSup_le
       · -- The set is nonempty.
          exact ⟨1152, h1 ⟩
       · -- Every element in the set is less than or equal to 1152.
          intro z hz
          exact h2 z hz
    · -- Show that 1152 is less than or equal to the supremum.
       apply le_csSup
       · -- The set is bounded above.
          use 1152
          intro z hz
          exact h2 z hz
       · -- 1152 is in the set.
          exact h1
  exact h5

exact h3




                                             32
