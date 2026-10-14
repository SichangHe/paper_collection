                                                Learning to Generate Formally Verifiable Step-by-Step Logic Reasoning
                                                                via Structured Formal Intermediaries


                                                                               Luoxin Chen 1 Yichi Zhou 2 Huishuai Zhang 1


                                                                    Abstract                                   ploys a rule-based reward mechanism (outcome correctness
                                                Large language models (LLMs) have recently                     plus output format score) to guide learning via the Group
                                                demonstrated impressive performance on com-                    Relative Policy Optimization (GRPO) algorithm, success-
arXiv:2603.29500v1 [cs.AI] 31 Mar 2026




                                                plex, multi-step reasoning tasks, especially when              fully achieves strong multi-step reasoning capabilities and
                                                post-trained with outcome-rewarded reinforce-                  exhibits emergent reflection behaviors. The simplicity and
                                                ment learning (Guo et al., 2025). However, it                  efficiency of this approach have inspired a series of follow-
                                                has been observed that outcome rewards often                   up works, such as R1-Zero replications TinyZero (Pan et al.,
                                                overlook flawed intermediate steps, leading to un-             2025) and Logical RL (Xie et al., 2025), and various GRPO
                                                reliable reasoning steps even when final answers               variants (Yu et al., 2025; Liu et al., 2025).
                                                are correct. To address this unreliable reason-                However, although these approaches greatly improve the
                                                ing, we propose PRoSFI (Process Reward over                    final accuracy, they do not guarantee the correctness of
                                                Structured Formal Intermediates), a novel reward               the reasoning steps. In mathematical tasks, it has been
                                                method that enhances reasoning reliability with-               observed that models may arrive at correct answers through
                                                out compromising accuracy. Instead of generating               invalid arguments (Uesato et al., 2022; Lightman et al.,
                                                formal proofs directly, which is rarely accomplish-            2024). Empirical studies, including our own observations,
                                                able for a modest-sized (7B) model, the model                  show that RL guided by outcome-only rewards can degrade
                                                outputs structured intermediate steps aligned with             the faithfulness of reasoning chains (Chen et al., 2025b).
                                                its natural language reasoning. Each step is then              Furthermore, in domains like proof generation, where final
                                                verified by a formal prover. Only fully validated              results cannot be automatically validated, outcome-based
                                                reasoning chains receive high rewards. The inte-               rewards are inapplicable. To ensure trustworthy reasoning,
                                                gration of formal verification guides the model to-            process-level supervision, not just outcome supervision, is
                                                wards generating step-by-step machine-checkable                necessary.
                                                proofs, thereby yielding more credible final an-
                                                swers. PRoSFI offers a simple and effective ap-                Process-level supervision provides feedback at each chain-
                                                proach to training trustworthy reasoning models.               of-thought step, yielding more precise training signals and
                                                                                                               producing models with more interpretable, reliable reason-
                                                                                                               ing steps (Uesato et al., 2022). Nonetheless, collecting
                                         1. Introduction                                                       large-scale process-level feedback is challenging as human
                                                                                                               annotation at the granularity of individual proof steps is
                                         Recent advances in techniques such as Chain-of-Thought                prohibitively expensive (Lightman et al., 2024). A natural
                                         (CoT) prompting and Reinforcement Learning (RL) have                  solution is to leverage formal provers to verify intermediate
                                         significantly enhanced the reasoning capabilities of large lan-       reasoning steps. This approach requires access to formal
                                         guage models (LLMs). These methods have improved both                 codes, either directly generated by language models or trans-
                                         the length and quality of model-generated reasoning chains,           lated from their natural language reasoning steps, which
                                         giving rise to the paradigm of test-time scaling (Snell et al.,       poses two key challenges.
                                         2024). Representative systems include OpenAI o1 (Jaech
                                         et al., 2024) and DeepSeek-R1 (Guo et al., 2025), which set           First, models that excel in natural language reasoning often
                                         new records across multiple reasoning benchmarks.                     struggle to generate correct formal code. Training models
                                                                                                               to write formal proofs typically requires much larger model
                                         Notably, DeepSeek-R1-Zero (Guo et al., 2025), which em-               sizes and significant data distillation (Wang et al., 2025;
                                            1
                                              Wangxuan Institue of Computer Technology, Peking Uni-            Ren et al., 2025). Moreover, models optimized for formal
                                         versity. 2 ByteDance. Correspondence to: Huishuai Zhang               proof generation often struggle with structure and format
                                         <zhanghuishuai@pku.edu.cn>.                                           following (Xin et al., 2024). Consequently, it is difficult to
                                                                                                               have a model capable of generating both natural language
                                         Preprint. April 1, 2026.

                                                                                                           1
        Learning to Generate Formally Verifiable Step-by-Step Logic Reasoning via Structured Formal Intermediaries




Figure 1. Pipeline for Process Reward over Structured Formal Intermediates and comparison with Outcome Reward. The process
begins with a problem statement (left block) containing multiple propositions (h1–h4) related to individuals (Hattie and Candy). Then, a
large language model (LLM) first generates natural language reasoning steps to solve the problem (middle block). The Outcome Reward
approach then directly compares the generated answer with the ground truth, assigning a reward of 1 if they match. In contrast, PRoSFI
introduces an additional step by generating structured formal intermediates that capture logical dependencies, inferred conclusions, and
the application of formal inference rules such as Hypothetical Syllogism and Modus Ponens. These formal representations are then
submitted to a Formal Prover, which verifies the logical soundness of the reasoning. In the illustrated example, although the generated
answer (“Hattie does not gain community respect” is false) is correct, the formal proof fails verification. As a result, PRoSFI assigns a
low reward despite the correct outcome.


explanations and aligned formal proofs simultaneously.                 Specifically, PRoSFI offers the following advantages. First,
                                                                       generating intermediate representations is easy. Existing
Second, existing models that excel at formal proof gener-
                                                                       models, even modest-sized (7B) language models, are typi-
ation typically are not designed to take natural language
                                                                       cally well-equipped for generating structured intermediate
inputs, and there is a lack of reliable methods for translating
                                                                       representations, and in this case, they only need to produce
natural language into formal code, as well as for evaluating
                                                                       formalized propositions for each intermediate step—without
the faithfulness of such translations. Furthermore, gener-
                                                                       having to construct full formal proofs. This avoids the core
ating formal code is inherently more challenging for large
                                                                       challenges of formal proof construction. Second, structured
language models than producing natural language reasoning.
                                                                       formal intermediates facilitate formal verification. Specif-
Accurate formal code generation often relies on test-time
                                                                       ically, formal provers are tasked with verifying individual
scaling techniques like Best-of-N (BoN), which can signifi-
                                                                       propositions derived from the intermediate representation,
cantly increase computational costs particularly during RL
                                                                       rather than constructing complete proofs for the original
post-training.
                                                                       problems. This ensures step-level alignment with the inter-
To address these challenges, we propose a novel and effec-             mediate reasoning. Overall, the structured formal intermedi-
tive reward method: Process Reward over Structured Formal              ates serve as an effective bridge between language models
Intermediates (PRoSFI, see Figure 1). Instead of generating            and formal provers. They reduce the burden on both sides:
full formal proofs directly, PRoSFI asks the model to output           language models are freed from producing formal syntax,
a series of reasoning blocks where each block contains a               avoiding distribution drift, while provers benefit from sim-
natural language explanation and a corresponding structured            plified sub-problems defined in a detailed and verifiable
intermediate representation. This intermediate representa-             format.
tion takes the form of a formatted array, usually in JSON
                                                                       To evaluate the effectiveness of our method, we conduct
or YAML, including an identifier, a logical rule, a derived
                                                                       controlled experiments in a logical reasoning setting. We
conclusion (in formal language), and a list of dependencies
                                                                       use the ProverQA dataset (Qi et al., 2025b), which is hard
(prior steps or premises). Then, formal propositions are
                                                                       for current models and, as a synthetic dataset, provides high-
extracted from each intermediate representation and passed
                                                                       quality formal representations of the problems. Through
to a formal prover for verification. The reasoning chain is
                                                                       extensive experiments, we demonstrate that PRoSFI can
considered trustworthy and receives the highest reward only
                                                                       significantly improve the reasoning soundness for complex
if all steps are successfully verified.
                                                                       logical problems. We summarize our contributions as fol-

                                                                   2
        Learning to Generate Formally Verifiable Step-by-Step Logic Reasoning via Structured Formal Intermediaries

lows:                                                                large-scale reasoning problems with controllable complex-
                                                                     ity.
  • Conceptually, we introduce a new reinforcement learn-            Other synthetic logic-reasoning datasets also include Log-
    ing paradigm with step-by-step rewards guided by for-            icPro (Jiang et al., 2024), which converts LeetCode program
    mal provers, which, to our knowledge, has not been               problems into narrative reasoning problems and leverages
    addressed in the literature. This shifts the focus from          Python execution to extract and verify detailed intermediate
    rewarding only final answers to ensuring the correct-            solution traces; LogicBench (Parmar et al., 2024b), a natu-
    ness of the entire reasoning process. We create a setup          ral language inference benchmark that covers propositional,
    for training and evaluating verifiable reasoning models          first-order, and non-monotonic logics; and FLD (Morishita
    of a modest size (7B), greatly lowering the entry barrier        et al., 2023; 2024b), which employs a set of first-order logic
    for the community.                                               rules to generate synthetic multistep proofs.
  • Technically, we propose PRoSFI, a framework that ef-             Formal-Language-Augmented Reasoning Techniques
    fectively bridges language models and formal provers.            have recently attracted great attention to improve language
    It enables RL post-training by incorporating formal              models’ rigor and reliability. In logical reasoning tasks,
    verification feedback into policy optimization.                  systems such as LINC (Olausson et al., 2023) and Logic-
  • Empirically, we demonstrate that Qwen2.5-7B-                     LM (Pan et al., 2023) treat the LLM as a semantic parser,
    Instruct, after PRoSFI RL post-training, can generate            translating natural language premises and conclusions into
    verifiable proofs on hard first-order logic tasks, achiev-       first-order logic expressions. These expressions are then
    ing this without relying on massive LLMs or extensive            checked by external solvers like Prover9 (McCune, 2005)
    data distillation, marking the first such result at this         or Z3 (De Moura & Bjørner, 2008). Logic-LM further
    scale.                                                           incorporates a self-correction loop, using solver error feed-
                                                                     back to iteratively refine the symbolic translations until they
                                                                     pass validation. Similarly, Logic Agent (Liu et al., 2024)
2. Related Work                                                      systematically applies propositional logic rules to structure
Reinforcement Learning Post-Training has recently                    and verify the model’s reasoning, enhancing both effective-
played a crucial role in training large language models,             ness and interpretability. Other related work on logical and
particularly for human preference alignment (RLHF) and               program-aided reasoning includes (Gao et al., 2023; Light-
enhancing complex reasoning abilities. Early work such as            man et al., 2024; Morishita et al., 2024a; Olausson et al.,
InstructGPT (Ouyang et al., 2022) leveraged Proximal Pol-            2023; Pan et al., 2023; Parmar et al., 2024a; Qi et al., 2025a;
icy Optimization (PPO) (Schulman et al., 2017) to extract            Ryu et al., 2025; Xu et al., 2024; Yang et al., 2023; Zhou
reward signals from human preference data, steering the              et al., 2024a).
model toward outputs more aligned with user expectations.            For automated theorem proving, OpenAI’s GPT-f system
However, the high computational cost of PPO on large-scale           (Polu & Sutskever, 2020) first demonstrated that LLMs
models motivated the development of more efficient alterna-          can generate formal mathematical proofs, achieving a 31%
tives.                                                               success rate on the miniF2F benchmark (Zheng et al.,
One such alternative is Group Relative Policy Optimization           2022). More recent advances along this direction include
(GRPO) (Shao et al., 2024), which has been adopted in                DeepSeek-Prover-V1.5 (Xin et al., 2024), Kimina-Prover
training DeepSeek-R1-Zero (Guo et al., 2025). DeepSeek-              (Wang et al., 2025), DeepSeek-Prover-V2 (Ren et al., 2025),
R1-Zero trains a pretrained model by using GRPO with only            and Seed-Prover (Chen et al., 2025a). Delta-Prover (Zhou
rule-based rewards to achieve significant gains on complex           et al., 2025) further leverages the sketching and reflection
mathematical reasoning tasks. Since then, many replication           capabilities of general-purpose LLMs, solving 95.9% of
projects have become public (Pan et al., 2025).                      the MiniF2F problems through decomposition and iterative
                                                                     reflection.
Logical Reasoning Datasets serve as important bench-
marks for evaluating the deductive and symbolic reason-              In mathematical reasoning, recent work has begun to in-
ing capabilities of LLMs. These datasets are typically               tegrate provers into LLM reasoning: Don’t Trust: Verify
constructed either by manual annotation or via automatic             (DTV) framework (Zhou et al., 2024b) focuses on quantita-
generation. Manually curated collections, such as Reclor             tive solutions by instructing LLMs to formalize their natural
(Yu et al., 2020) and FOLIO (Han et al., 2022), offer rich           language steps into Isabelle (Paulson, 1994) proof scripts,
linguistic diversity and complex logical rules. Automatic            which are then automatically verified. On benchmarks such
dataset generation methods have been proposed. ProntoQA              as GSM8K (Cobbe et al., 2021) and MATH (Hendrycks
(Saparov & He, 2022) and ProofWriter (Tafjord et al., 2020)          et al., 2021), DTV outperforms naive majority voting by fil-
use predefined templates or rule-based systems to generate           tering out unsound solution paths, demonstrating that formal

                                                                 3
        Learning to Generate Formally Verifiable Step-by-Step Logic Reasoning via Structured Formal Intermediaries

provers can supply valuable feedback for reasoning paths.            less of the validity of the reasoning steps. Reward Hit Rate
                                                                     reflects how often the model receives the maximum reward
Process Reward Models and Verification. Early work
                                                                     (R = 1) under our reinforcement learning framework, that
(Uesato et al., 2022; Lightman et al., 2024; Wang et al.,
                                                                     is, when the final answer is correct and all intermediate
2023) train process reward models (PRMs) to provide fine-
                                                                     reasoning steps are formally verified. Soundness assesses
grained feedback for reasoning steps, achieving higher accu-
                                                                     both answer correctness and reasoning path validity, which
racy on GSM8K and MATH benchmarks. Recent research
                                                                     is defined as the proportion of examples where the final
has shifted towards using LLMs as verifiers to detect er-
                                                                     answer is correct and the reasoning path is logically valid.
rors in the reasoning process. For example, (Huang & Yang,
2025) employed a general-purpose model with a verification-          We note that Reward Hit, i.e., all structured formal inter-
refinement pipeline to achieve a gold medal in IMO 2025.             mediates are verified, does not necessarily guarantee the
                                                                     Soundness of the entire reasoning path. This is because the
3. Preliminaries on Dataset, Base Model,                             extracted formal propositions may not fully cover the entire
                                                                     reasoning path. In practice, rigorously assessing the sound-
   Algorithms and Evaluation Metrics                                 ness of a reasoning path would require extensive human
Dataset Description ProverQA (Qi et al., 2025b) is a                 evaluation, which is often infeasible at scale. As an alterna-
synthetic first-order logic reasoning benchmark generated            tive, we adopt state-of-the-art LLM-based evaluators, such
by the ProverGen framework, which combines the linguis-              as GPT-OSS-120B, to approximate Soundness. In the exper-
tic diversity of LLMs with the rigor of a symbolic prover            imental section, we will analyze potential biases introduced
(Prover9 (McCune, 2005)). More details are provided in               by these LLM-as-a-Judge metrics.
Appendix B.                                                          With the dataset, model, algorithm, and evaluation metrics
                                                                     defined, we now explore how to train LLMs to generate
Model Description The Qwen2.5-7B-Instruct model, an                  step-by-step reasoning that is formally verifiable.
instruction-tuned variant of the Qwen2.5 family developed
by Alibaba’s Qwen team, comprises 7 billion parameters
and is released under the Apache License 2.0 (Team, 2024).           4. Method: Process Reward over Structured
It builds on the Qwen2.5 base LLM with further fine-tuning              Formal Intermediates
to follow instructions and engage in chat/dialogue. Specifi-
                                                                     To incorporate step-level verification into the reinforcement
cally, it can produce reliable structured outputs (e.g. JSON),
                                                                     learning process, a natural approach is to (1) ask for the
parses tables, spreadsheets, and other semi-structured for-
                                                                     model to emit natural language reasoning step and formal
mats robustly.
                                                                     proof script at the same time (e.g., in Lean 4 (Moura &
                                                                     Ullrich, 2021)), and (2) use a theorem prover to verify the
Group Relative Policy Optimization (GRPO) GRPO is                    correctness of each step. The verification outcomes can
a variant of Proximal Policy Optimization (PPO) tailored for         then be used as reward signals to distinguish valid reasoning
training large language models (LLMs) without an explicit            chains from unsound ones.
value (critic) model (Shao et al., 2024). The algorithm
details can be found in Appendix C.
                                                                     However, direct generation of stepwise formal proofs
Metrics We introduce several metrics to evaluate the vari-           fails in practice. We prompted the model to emit Lean
ous facets of the model performance: Answer Correct Rate,            4 proof code immediately after natural-language reason-
Reward Hit Rate and Soundness.                                       ing steps, exploring multiple prompt templates and both
                                                                     Qwen2.5-7B-Instruct and Qwen2.5-Coder-7B-Instruct vari-
       Table 1. Evaluation metrics and their definitions.
                                                                     ants. However, these attempts yielded unsatisfactory results:
    Metric                             Definition                    only a small fraction of the generated Lean scripts com-
                                                                     piled successfully, and those that did were overly reliant
                                #Final Answer Correct                on generic tactics such as simp. The proofs were typically
    Answer Correct Rate
                                  #Total Examples                    brittle, poorly structured, and misaligned with the model’s
                             #Outputs with Max Reward                natural-language reasoning, and consequently ineffective
    Reward Hit Rate
                                #Total Examples                      for verifying the reasoning process.
                            #Answer Correct & Path Valid             We attribute this failure to two key challenges. First, modest-
    Soundness
                                #Total Examples                      sized models (e.g., 7B) struggle to generate accurate and
                                                                     meaningful formal proofs. This makes it difficult for GRPO
Answer Correct Rate measures the percentage of examples              to bootstrap useful supervision from the generated formal
where the model produces the correct final answer, regard-           codes, a finding consistent with recent progress in formal

                                                                 4
        Learning to Generate Formally Verifiable Step-by-Step Logic Reasoning via Structured Formal Intermediaries

proof generation, which has primarily relied on much larger          tics in Lean (e.g., aesop, simp), or through external
base models (Wang et al., 2025; Ren et al., 2025).                   automated solvers such as Z3 (De Moura & Bjørner, 2008)
                                                                     or Prover9 (McCune, 2005). For more complex settings, we
Second, the process of integrating formal verification into
                                                                     optionally delegate verification to powerful formal models
the GRPO rollout pipeline introduces significant compu-
                                                                     such as DeepSeek-Prover-V1.5 (Xin et al., 2024). These
tational overhead. The frequent calls to external formal
                                                                     configurations can be adapted with different formal formats
provers disrupt GPU parallelism during sequence genera-
                                                                     or verification tools for different tasks and domains.
tion, drastically slowing down training and reducing scala-
bility.
                                                                     Reward Design If all steps pass formal verification, the
These limitations motivate our alternative solution: rather          entire reasoning path will be assigned a high reward R = 1.
than having models directly generate full formal proofs,             Otherwise, a failure of any individual step flags a potential
we introduce a structured intermediate representation that           flaw in the reasoning process. Based on this framework, we
enables effective extraction of formal propositions and step-        definethe reward function as follows:
level verification with formal tools, which at the same time                1.0, Answer correct and all steps verified,
                                                                           
remaining within the capability of modest-sized language                   
                                                                           0.3, Answer correct, but some steps not verified,
models.                                                              R=
                                                                           
                                                                           
                                                                            0.1, Output format correct, but answer incorrect,
                                                                             0.0, Output format incorrect or other failure cases.
                                                                           
4.1. The Design of Process Reward over Structured
     Formal Intermediates
                                                                     This reward design of PRoSFI exploits the rigor of formal
To overcome the challenges encountered in directly generat-          provers while avoiding the difficulties of generating full
ing formal proofs, we propose a novel approach: Process              formal proofs, resulting in more stable, fine-grained, and
Reward over Structured Formal Intermediates (PRoSFI),                structure-aligned supervision signals, which are crucial for
which introduces a structured JSON/YAML based interme-               effective reinforcement learning. Moreover, PRoSFI avoids
diate representation as a bridge between natural language            the efficiency bottlenecks typically associated with integrat-
reasoning paths and formal verification. This format serves          ing formal provers into the rollout phase of RL training.
as a lightweight, verifiable scaffold that enables formal re-        The model generates the full natural language reasoning
ward during reinforcement learning. Crucially, Qwen2.5-              and the structured formal intermediates in a single, unin-
7B-Instruct, the base model, is well-suited for this task due        terrupted forward pass. Formal verification is performed
to its strong formatting capabilities, particularly for struc-       after generation, allowing it to be fully decoupled from the
tured JSON or YAML outputs (Team, 2024).                             autoregressive process. This decoupling not only improves
                                                                     training throughput by enabling batch-level parallelism but
                                                                     also allows verification tools to run asynchronously, maxi-
Structured Formal Intermediates In PRoSFI, the model
                                                                     mizing efficiency.
is prompted to produce a sequence of reasoning steps in
structured format, where each step explicitly encodes the            We next present empirical results to demonstrate that
structure of logical reasoning, which includes the follow-           PRoSFI can effectively improve the soundness of LLM
ing fields: id: a unique identifier for the step, used for           reasoning paths.
reference; dependencies: a list of premises this step de-
pends on, which may include given conditions or previous             5. Experimental Results
steps; conclusion: The new conclusion drawn in this
step, expressed in a formal language; rule: The logical              5.1. Training and Testing Setup
rule applied to derive the conclusion.
                                                                     Training Setup As described in Section 3, our experi-
To ensure each step remains atomic, we impose a constraint           ments are conducted on the ProverQA dataset, a synthetic
that the number of dependencies per step must be fewer               logical reasoning benchmark designed with controlled dif-
than 5 (tunable). Each step can then be converted into a             ficulty levels and well-defined ground-truth labels (True/-
sub-problem for verification. Moreover, we also require that         False/Uncertain). This makes it particularly well-suited for
the final step’s conclusion match the target proposition, and        evaluating models in a controlled reinforcement learning
that its identifier be among the provided answer candidates.         (RL) setting. To address the difficulty imbalance within the
                                                                     ProverQA dataset, we excluded instances labeled as Uncer-
This structured format allows natural language reasoning
                                                                     tain. The remaining data were then partitioned into training
to be decomposed into discrete, formalizable sub-problems.
                                                                     and test sets for each difficulty level (easy, medium, and
For the first-order logic (FOL) tasks considered in this pa-
                                                                     hard), yielding a total of 769 instances for the training set.
per, which are relatively simple and well-structured, each
proposition can typically be verified using lightweight tac-         We adopt Qwen2.5-7B-Instruct as our base model. This

                                                                 5
        Learning to Generate Formally Verifiable Step-by-Step Logic Reasoning via Structured Formal Intermediaries

model offers a good choice for strong performance given             indexed premises (see Figure 1). We refer to this setup as
the model size under our hardware constraints. Moreover,            Outcome Reward with CoT or Outcome-CoT for short. The
it has demonstrated superior responsiveness to RL-based             full user prompt is presented in Appendix D.
post-training compared to other open-source alternatives
such as the LLaMA series (Shao et al., 2025; Zeng et al.,
                                                                    Results: GRPO with Outcome-CoT significantly boosts
2025).
                                                                    the Answer Correct Rate but achieves rather low Sound-
We use the GRPO algorithm with a learning rate of 3×10−7            ness. Specifically, in our evaluation on the ProverQA-
and batch size of 64. For each training iteration, GRPO sam-        Hard subset, GRPO with Outcome-CoT substantially im-
ples 8 responses, with the maximum sequence length set to           proves the Answer Correct Rate, rising from 46.0% with
5120 tokens. The KL coefficient in the GRPO loss function           Qwen2.5-7B-Instruct to 91.31%. This confirms the suc-
is set to 0.001. To enhance training stability, we implement        cessful replication of the R1-Zero training procedure. How-
the clip-higher strategy from the Decoupled Advantage Pol-          ever, the GPT Soundness score remains low, improving only
icy Optimization (DAPO) algorithm (Yu et al., 2025), whose          from 9.0% to 21.97%. This indicates that although the final
details are in Appendix C.                                          answers are often correct, the generated reasoning paths
                                                                    frequently contain flawed or invalid inference steps.
All experiments are conducted on a compute node equipped
with 8× Hopper GPUs, running on Debian GNU/Linux 12
with CUDA 12.4, PyTorch 2.6.0, vLLM 0.8.3, and Verl                 5.3. Direct Lean Generation Fails to Provide Reliable
0.4.0. Each training run consists of 960 iterations, which               Stepwise Verification
takes approximately 14 hours to complete.                           As a direct baseline for integrating formal verification
                                                                    into reinforcement learning, we evaluated an approach
Testing Setup Besides the test splits of difficulty levels in       in which the model is required to emit complete Lean 4
the ProverQA dataset, we introduce a more challenging out-          proof scripts (rather than the structured intermediates in-
of-distribution (OOD) test set, named ProverQA-Extra. This          troduced in PRoSFI). This baseline was designed to iso-
set consists of 128 synthesized examples generated from             late the effect of output modality: reward schedule and
the ProverQA repository using Qwen2.5-32B-Instruct as the           training protocol were kept the same as in the structured-
background story generation model. To reduce randomness,            intermediate condition, and the only difference was that the
we sampled 16 responses for each test data instance and             model produced full formal proofs immediately following
took the average of their results.                                  each natural-language reasoning trace.

5.2. Outcome Reward Leads to High Answer Correct                    Empirically, this direct-generation strategy failed to provide
     Rate But Low Soundness                                         a useful stepwise verification signal for GRPO. Compile-
                                                                    and-verify rates were low: the Reward Hit Rate on
We employ GRPO with a reward scheme similar to that                 ProverQA-Hard was 13.77% and on ProverQA-Extra was
of DeepSeek-R1-Zero to replicate its training methodology           4.35%. Instances that did compile were vanishingly rare,
on ProverQA. This serves a baseline for the evaluation of           and when compilation succeeded the resulting proofs typ-
reasoning path soundness.                                           ically reduced to a single opaque tactic (e.g. a one-line
                                                                    simp invocation) that bore little structural correspondence
Reward Design Following the DeepSeek-R1-Zero                        to the model’s natural-language chain of thought. Conse-
pipeline, the model must emit its chain of thought wrapped          quently, the direct-Lean baseline produced almost no reli-
in <think> . . . </think> tags before the final answer,             able, fine-grained supervision: both final-answer accuracy
referred to as format correct. We define the outcome-based          and measured reasoning soundness decreased relative to the
reward R as:                                                        Outcome-CoT baseline, as shown in Table 2.
           
           1.0, format correct and answer correct,
           
     R = 0.1, format correct but answer incorrect,                  5.4. PRoSFI Learning with ProverQA
           
           
             0.0, format incorrect.                                 Results: Structured formal rewards improve final ac-
                                                                    curacy with significantly more credible reasoning path.
This reward encourages adherence to the output format and
                                                                    After GRPO training with stepwise formal rewards, we
correctness of the final answer.
                                                                    achieve comparable final-answer accuracy to the GRPO
                                                                    training with only final-answer reward on ProverQA, as
Prompt Design The system prompt, adapted from
                                                                    shown in Table 2. This confirms that our stepwise rewards
DeepSeek-R1-Zero, is provided in Appendix D.
                                                                    can effectively be combined into R1-Zero reward with high
The user prompt starts with the original dataset description,       reasoning accuracy. We can also see that stepwise formal
then presents the problem in formal language with clearly           rewards can significantly improve the credibility of reason-

                                                                6
        Learning to Generate Formally Verifiable Step-by-Step Logic Reasoning via Structured Formal Intermediaries

Table 2. Results on ProverQA Hard and Extra. GPT Soundness values include the difference of each method versus the Outcome-CoT
baseline.

                       Method                      Metric (%)                                             Hard                   Extra

                                                   Answer Correct Rate                                    91.31                  86.96
                       Outcome-CoT
                                                   GPT Soundness                                          21.97                  11.87

                                                   Answer Correct Rate                                    92.29                  83.15
                       Direct Lean Generation
                                                   GPT Soundness                                   33.11 ↑ 11.1           10.45 ↓ −1.4

                                                   Answer Correct Rate                                    92.97                  91.94
                       ProSFI
                                                   GPT Soundness                                   76.07 ↑ 54.1           56.10 ↑ 44.2


ing paths in comparison with final-answer only reward in                       PRoSFI + Majority Voting               PRoSFI + ProSFI Selection         Outcome-CoT + Majority Voting
                                                                                 1.0
Section 5.2. Moreover, the results on ProverQA-Extra also
demonstrates PRoSFI achieves strong out-of-distribution                                  0.8



                                                                         GPT Soundness
(OOD) performance on logical reasoning questions of pre-                                 0.6
viously unseen difficulty.                                                               0.4

                                                                                         0.2
5.5. Test-Time Scaling Behaviors of PRoSFI
                                                                                         0.0
                                                                                               1          2       4       8       16      1       2        4        8        16
A critical advantage of PRoSFI is its strong test-time scaling                                                Sample @N                                Sample @N
behavior, made possible through integration with the Don’t
                                                                     Figure 2. Left: GPT Soundness on ProverQA-hard subset.
Trust; Verify (DTV) method (Zhou et al., 2024b). DTV is              Right: GPT Soundness on ProverQA-extra subset. As the
designed to enhance both accuracy and reasoning reliabil-            number of sampled paths increases, PRoSFI with PRoSFI selection
ity by sampling multiple reasoning paths and employing               consistently improves, while Outcome-CoT cannot benefit due
a lightweight verifier to assess the logical validity of each        to translation limits.
output. If any candidates are successfully verified, one of
them is selected; otherwise, the method defaults to majority
                                                                                                                                                                                  1.00
voting. PRoSFI is particularly well-suited for integration
                                                                         Answer                    1.00        0.56       0.47            1.00        0.33       0.33             0.75
with DTV due to its structured intermediate representations,         Correctness
                                                                                                                                                                                  0.50
which enable reliable formal verification. In contrast, ap-                                                                                                                       0.25
proaches that rely solely on natural language reasoning lack             ProSFI                    0.56        1.00       0.71            0.33        1.00       0.63             0.00
                                                                      Reward Hit
the structured outputs required for effective collaboration                                                                                                                        0.25

with DTV, limiting their ability to benefit from test-time                                                                                                                         0.50
                                                                           GPT-                    0.47        0.71       1.00            0.33        0.63       1.00
                                                                      Soundness                                                                                                    0.75
verification.
                                                                                                                                                                                   1.00
                                                                                                 Answer      ProSFI     GPT-             Answer      ProSFI     GPT-
In our experiments, we apply the DTV method to the out-                                        Correctness Reward Hit Soundness        Correctness Reward Hit Soundness

puts generated by PRoSFI. As shown in Figure 2, increas-             Figure 3. Left: Metric correlation heatmap on ProverQA-Hard.
ing the number of sampled reasoning paths consistently               Right: Metric correlation heatmap on ProverQA-Extra. Com-
improves performance on the Soundness metric, demon-                 pared to Answer Correctness, PRoSFI Reward Hit better reflects
strating PRoSFI’s robust and scalable behavior at test time.         reasoning-path soundness.
This trend holds across both the ProverQA-Hard and
ProverQA-Extra subsets. In contrast, methods such as
Outcome-CoT fail to benefit from additional sampling, as
                                                                     5.6. PRoSFI Reward Aligns Well with Soundness
majority voting alone is insufficient to discern the sound-
ness of the reasoning paths and cannot effectively filter out        To evaluate the effectiveness of the reward design used in
logically invalid reasoning.                                         PRoSFI, we conduct a correlation analysis among three
                                                                     metrics: Answer Correctness, PRoSFI Reward Hit, and
                                                                     GPT-Soundness of generated reasoning paths. This analysis
                                                                     is performed on the outputs of PRoSFI, and the results are
                                                                     in Figure 3.

                                                                 7
        Learning to Generate Formally Verifiable Step-by-Step Logic Reasoning via Structured Formal Intermediaries

                                        Table 3. Results on Knights and Knaves dataset.

               Method          Metric (%)              2ppl         3ppl    4ppl    5ppl     6ppl     7ppl     8ppl

                               Answer Correct Rate    99.63     99.81      99.81    98.13    98.69    95.13    94.25
               Outcome-CoT
                               GPT Soundness          64.81     68.56      69.13    61.75    56.06    53.88    47.94

                               Answer Correct Rate    99.75     99.31      99.75    99.63    99.25    98.56    97.38
               PRoSFI
                                                      86.56     90.31      90.50    90.44    91.00    86.31    80.94
                               GPT Soundness
                                                      ↑ 21.8    ↑ 21.8     ↑ 21.4   ↑ 28.7   ↑ 35.0   ↑ 32.4   ↑ 33.0




The results reveal that the PRoSFI Reward Hit signal ex-             beyond ProverQA.
hibits a high correlation with GPT-Soundness, much higher
than the Answer Correctness. This suggests that our reward           7. Conclusion
function is more aligned with step-by-step reasoning qual-
ity, thereby achieving our design goal. In contrast, answer          It is known that LLMs may make mistakes in the reason-
correctness alone may fail to capture subtle flaws or incon-         ing steps even when the final answer is correct, which can
sistencies in intermediate reasoning steps. These findings           undermine their credibility in high-risk domains. In this
highlight that PRoSFI’s reward design provides meaning-              work, we study the problem of how to enable large language
ful supervision that better promotes logically coherent and          models generating step-by-step verifiable reasoning paths
sound outputs.                                                       via formal prover’s feedback. We propose a novel method
                                                                     Process Reward over Structured Formal Intermediates that
6. PRoSFI Generalizes to Knights and Knaves                          connects natural language reasoning with formal provers’
                                                                     verification. By training LLM to output structured formal
   Data                                                              intermediates and validating them with formal provers, we
To demonstrate the generalization ability of our proposed            obtain precise, step-level soundness signals. These signals
method, we extend experiments to the Knights and Knaves              serve as stepwise formal rewards during reinforcement learn-
dataset (Xie et al., 2024), whose details can be found in            ing, enabling the model to learn verifiably correct reasoning
Appendix B.3.                                                        behaviors.
For the Outcome-CoT baseline, we adopt the same prompt               While our current framework focuses on first-order logic
template as Logic-RL, while the prompt for PRoSFI is                 tasks, future work can extend it to broader domains such
adapted slightly to suit this task. Following the out-of-            as general natural language reasoning and automatic the-
distribution (OOD) evaluation protocol established in Logic-         orem proving. These extensions will require more di-
RL, our model is trained exclusively on instances with diffi-        verse datasets, meticulously designed cold-start strategies,
culty levels from 3ppl to 7ppl. Evaluation is then conducted         stronger base models, and deeper integration with domain-
across the full test range, from 2ppl to 8ppl, with the 8ppl         specific formal reasoning tools.
split serving as the primary benchmark for OOD perfor-               Another viable direction involves further exploration of
mance.                                                               training algorithm development. Instead of relying solely
The training configuration closely follows that of ProverQA,         on binary pass/fail signals, future systems could incorpo-
including a batch size of 64, 8 sampled responses per                rate more granular reward functions or more precise credit
prompt, a maximum sequence length of 5120, and the same              assignment mechanisms to enhance training efficacy and
KL coefficient and clip-higher strategy from DAPO, except            stability.
that we set the learning rate to 4 × 10−7 , consistent with
Logic-RL, and extend the training schedule to 1440 steps to          References
align with our experimental design.
                                                                     Chen, L., Gu, J., Huang, L., Huang, W., Jiang, Z., Jie, A., Jin,
From the results shown in Table 3, we can see that on the              X., Jin, X., Li, C., Ma, K., et al. Seed-prover: Deep and
Knights and Knaves dataset, ProSFI consistently improves               broad reasoning for automated theorem proving. arXiv
GPT soundness over Outcome-CoT across all difficulty lev-              preprint arXiv:2507.23726, 2025a.
els, while maintaining comparable answer accuracy, demon-
strating strong logical consistency and reliable generaliza-
                                                                     Chen, Y., Benton, J., Radhakrishnan, A., Uesato, J., Deni-
tion, particularly on the hardest 8ppl split. Therefore, our
                                                                       son, C., Schulman, J., Somani, A., Hase, P., Wagner, M.,
approach is generalizable to other logical reasoning tasks
                                                                       Roger, F., et al. Reasoning models don’t always say what

                                                                8
        Learning to Generate Formally Verifiable Step-by-Step Logic Reasoning via Structured Formal Intermediaries

  they think. arXiv preprint arXiv:2505.05410, 2025b.                 Liu, Z., Chen, C., Li, W., Qi, P., Pang, T., Du, C., Lee,
                                                                        W. S., and Lin, M. Understanding r1-zero-like training:
Cobbe, K., Kosaraju, V., Bavarian, M., Chen, M., Jun, H.,               A critical perspective. arXiv preprint arXiv:2503.20783,
  Kaiser, L., Plappert, M., Tworek, J., Hilton, J., Nakano,             2025.
  R., et al. Training verifiers to solve math word problems.
  arXiv preprint arXiv:2110.14168, 2021.                              McCune, W. Release of prover9. In Mile high conference on
                                                                       quasigroups, loops and nonassociative systems, Denver,
De Moura, L. and Bjørner, N. Z3: An efficient smt solver.              Colorado, 2005.
  In International conference on Tools and Algorithms for
  the Construction and Analysis of Systems, pp. 337–340.              Morishita, T., Morio, G., Yamaguchi, A., and Sogawa,
  Springer, 2008.                                                      Y. Learning deductive reasoning from synthetic corpus
                                                                       based on formal logic. In International Conference on
Gao, L., Madaan, A., Zhou, S., Alon, U., Liu, P., Yang, Y.,            Machine Learning, pp. 25254–25274. PMLR, 2023.
  Callan, J., and Neubig, G. PAL: Program-aided language
  models. In Krause, A., Brunskill, E., Cho, K., Engelhardt,          Morishita, T., Morio, G., Yamaguchi, A., and Sogawa, Y.
  B., Sabato, S., and Scarlett, J. (eds.), Proceedings of the          Enhancing reasoning capabilities of llms via principled
  40th International Conference on Machine Learning, vol-              synthetic logic corpus. In Advances in Neural Information
  ume 202 of Proceedings of Machine Learning Research,                 Processing Systems 37 (NeurIPS 2024), 2024a.
  pp. 10764–10799. PMLR, 23–29 Jul 2023.
                                                                      Morishita, T., Morio, G., Yamaguchi, A., and Sogawa, Y.
Guo, D., Yang, D., Zhang, H., Song, J., Zhang, R., Xu, R.,             Enhancing reasoning capabilities of llms via principled
  Zhu, Q., Ma, S., Wang, P., Bi, X., et al. Deepseek-r1: In-           synthetic logic corpus. Advances in Neural Information
  centivizing reasoning capability in llms via reinforcement           Processing Systems, 37:73572–73604, 2024b.
  learning. arXiv preprint arXiv:2501.12948, 2025.
                                                                      Moura, L. d. and Ullrich, S. The lean 4 theorem prover
Han, S., Schoelkopf, H., Zhao, Y., Qi, Z., Riddell, M., Zhou,          and programming language. In Automated Deduction–
  W., Coady, J., Peng, D., Qiao, Y., Benson, L., et al. Folio:         CADE 28: 28th International Conference on Automated
  Natural language reasoning with first-order logic. arXiv             Deduction, Virtual Event, July 12–15, 2021, Proceedings
  preprint arXiv:2209.00840, 2022.                                     28, pp. 625–635. Springer, 2021.

Hendrycks, D., Burns, C., Kadavath, S., Arora, A., Basart,            Olausson, T., Gu, A., Lipkin, B., Zhang, C., Solar-Lezama,
  S., Tang, E., Song, D., and Steinhardt, J. Measuring math-            A., Tenenbaum, J., and Levy, R. LINC: A neurosymbolic
  ematical problem solving with the math dataset. arXiv                 approach for logical reasoning by combining language
  preprint arXiv:2103.03874, 2021.                                      models with first-order logic provers. In Proceedings of
                                                                        the 2023 Conference on Empirical Methods in Natural
Huang, Y. and Yang, L. F. Winning gold at imo 2025 with                 Language Processing, pp. 5153–5176, Singapore, De-
  a model-agnostic verification-and-refinement pipeline.                cember 2023. Association for Computational Linguistics.
  arXiv preprint arXiv:2507.15855, 2025.
                                                                      Ouyang, L., Wu, J., Jiang, X., Almeida, D., Wainwright, C.,
Jaech, A., Kalai, A., Lerer, A., Richardson, A., El-Kishky,             Mishkin, P., Zhang, C., Agarwal, S., Slama, K., Ray, A.,
  A., Low, A., Helyar, A., Madry, A., Beutel, A., Car-                  et al. Training language models to follow instructions
  ney, A., et al. Openai o1 system card. arXiv preprint                 with human feedback. Advances in neural information
  arXiv:2412.16720, 2024.                                               processing systems, 35:27730–27744, 2022.
Jiang, J., Yan, Y., Liu, Y., Jin, Y., Peng, S., Zhang, M., Cai,       Pan, J., Zhang, J., Wang, X., Yuan, L., Peng, H., and Suhr, A.
   X., Cao, Y., Gao, L., and Tang, Z. Logicpro: Improving               Tinyzero. https://github.com/Jiayi-Pan/TinyZero, 2025.
   complex logical reasoning via program-guided learning.               Accessed: 2025-01-24.
   arXiv preprint arXiv:2409.12929, 2024.
                                                                      Pan, L., Albalak, A., Wang, X., and Wang, W. Logic-
Lightman, H., Kosaraju, V., Burda, Y., Edwards, H., Baker,              LM: Empowering large language models with symbolic
  B., Lee, T., Leike, J., Schulman, J., Sutskever, I., and              solvers for faithful logical reasoning. In Findings of
  Cobbe, K. Let’s verify step by step. In Proceedings of the            the Association for Computational Linguistics: EMNLP
  International Conference on Learning Representations                  2023, pp. 3806–3824, Singapore, December 2023. Asso-
  (ICLR 2024), 2024.                                                    ciation for Computational Linguistics.
Liu, H., Teng, Z., Zhang, C., and Zhang, Y. Logic agent:              Parmar, M., Patel, N., Varshney, N., Nakamura, M., Luo,
  Enhancing validity with logic rule invocation. arXiv                  M., Mashetty, S., Mitra, A., and Baral, C. Logicbench:
  preprint arXiv:2404.18130, 2024.                                      Towards systematic evaluation of logical reasoning ability

                                                                  9
        Learning to Generate Formally Verifiable Step-by-Step Logic Reasoning via Structured Formal Intermediaries

  of large language models. In Proceedings of the 62nd                 Shao, Z., Wang, P., Zhu, Q., Xu, R., Song, J., Bi, X., Zhang,
  Annual Meeting of the Association for Computational                    H., Zhang, M., Li, Y., Wu, Y., et al. Deepseekmath: Push-
  Linguistics (Volume 1: Long Papers), pp. 13679–13707,                  ing the limits of mathematical reasoning in open language
  Bangkok, Thailand, August 2024a. Association for Com-                  models. arXiv preprint arXiv:2402.03300, 2024.
  putational Linguistics.
                                                                       Snell, C., Lee, J., Xu, K., and Kumar, A. Scaling llm test-
Parmar, M., Patel, N., Varshney, N., Nakamura, M., Luo,                  time compute optimally can be more effective than scal-
  M., Mashetty, S., Mitra, A., and Baral, C. Logicbench:                 ing model parameters. arXiv preprint arXiv:2408.03314,
  Towards systematic evaluation of logical reasoning ability             2024.
  of large language models. In Proceedings of the 62nd
  Annual Meeting of the Association for Computational                  Tafjord, O., Mishra, B. D., and Clark, P. Proofwriter: Gen-
  Linguistics (Volume 1: Long Papers), pp. 13679–13707,                  erating implications, proofs, and abductive statements
  2024b.                                                                 over natural language. arXiv preprint arXiv:2012.13048,
                                                                         2020.
Paulson, L. C. Isabelle: A generic theorem prover. Springer,
  1994.                                                                Team, Q. Qwen2.5: A party of foundation models, Septem-
                                                                         ber 2024.
Polu, S. and Sutskever, I. Generative language model-
  ing for automated theorem proving. arXiv preprint                    Uesato, J., Kushman, N., Kumar, R., Song, F., Siegel, N.,
  arXiv:2009.03393, 2020.                                               Wang, L., Creswell, A., Irving, G., and Higgins, I. Solv-
                                                                         ing math word problems with process-and outcome-based
Qi, C., Ma, R., Li, B., Du, H., Hui, B., Wu, J., Laili, Y., and          feedback. arXiv preprint arXiv:2211.14275, 2022.
  He, C. Large language models meet symbolic provers
  for logical reasoning evaluation. In Proceedings of the              Wang, H., Unsal, M., Lin, X., Baksys, M., Liu, J., Santos,
  International Conference on Learning Representations                  M. D., Sung, F., Vinyes, M., Ying, Z., Zhu, Z., et al.
  (ICLR 2025), 2025a.                                                   Kimina-prover preview: Towards large formal reason-
                                                                        ing models with reinforcement learning. arXiv preprint
Qi, C., Ma, R., Li, B., Du, H., Hui, B., Wu, J., Laili, Y., and
                                                                        arXiv:2504.11354, 2025.
  He, C. Large language models meet symbolic provers
  for logical reasoning evaluation. In The Thirteenth Inter-           Wang, P., Li, L., Shao, Z., Xu, R., Dai, D., Li, Y., Chen,
  national Conference on Learning Representations (ICLR                 D., Wu, Y., and Sui, Z. Math-shepherd: A label-free
  2025), 2025b.                                                         step-by-step verifier for llms in mathematical reasoning.
Ren, Z., Shao, Z., Song, J., Xin, H., Wang, H., Zhao, W.,               arXiv preprint arXiv:2312.08935, 3, 2023.
  Zhang, L., Fu, Z., Zhu, Q., Yang, D., et al. Deepseek-
                                                                       Xie, C., Huang, Y., Zhang, C., Yu, D., Chen, X., Lin, B. Y.,
  prover-v2: Advancing formal mathematical reasoning via
                                                                         Li, B., Ghazi, B., and Kumar, R. On memorization
  reinforcement learning for subgoal decomposition. arXiv
                                                                         of large language models in logical reasoning. arXiv
  preprint arXiv:2504.21801, 2025.
                                                                         preprint arXiv:2410.23123, 2024.
Ryu, H., Kim, G., Lee, H. S., and Yang, E. Divide and
                                                                       Xie, T., Gao, Z., Ren, Q., Luo, H., Hong, Y., Dai, B., Zhou,
  translate: Compositional first-order logic translation and
                                                                         J., Qiu, K., Wu, Z., and Luo, C. Logic-rl: Unleashing llm
  verification for complex logical reasoning. In Proceed-
                                                                         reasoning with rule-based reinforcement learning. arXiv
  ings of the International Conference on Learning Repre-
                                                                         preprint arXiv:2502.14768, 2025.
  sentations (ICLR 2025), 2025.

Saparov, A. and He, H. Language models are greedy rea-                 Xin, H., Ren, Z., Song, J., Shao, Z., Zhao, W., Wang, H., Liu,
  soners: A systematic formal analysis of chain-of-thought.              B., Zhang, L., Lu, X., Du, Q., et al. Deepseek-prover-v1.
  arXiv preprint arXiv:2210.01240, 2022.                                 5: Harnessing proof assistant feedback for reinforcement
                                                                         learning and monte-carlo tree search. arXiv preprint
Schulman, J., Wolski, F., Dhariwal, P., Radford, A., and                 arXiv:2408.08152, 2024.
  Klimov, O. Proximal policy optimization algorithms.
  arXiv preprint arXiv:1707.06347, 2017.                               Xu, J., Fei, H., Pan, L., Liu, Q., Lee, M.-L., and Hsu, W.
                                                                         Faithful logical reasoning via symbolic chain-of-thought.
Shao, R., Li, S. S., Xin, R., Geng, S., Wang, Y., Oh, S., Du,            In Proceedings of the 62nd Annual Meeting of the Asso-
  S. S., Lambert, N., Min, S., Krishna, R., Tsvetkov, Y.,                ciation for Computational Linguistics (Volume 1: Long
  Hajishirzi, H., Koh, P. W., and Zettlemoyer, L. Spurious              Papers), pp. 13326–13365, Bangkok, Thailand, August
  rewards: Rethinking training signals in rlvr, 2025.                    2024. Association for Computational Linguistics.

                                                                  10
       Learning to Generate Formally Verifiable Step-by-Step Logic Reasoning via Structured Formal Intermediaries

Yang, K., Swope, A., Gu, A., Chalamala, R., Song, P.,
  Yu, S., Godil, S., Prenger, R. J., and Anandkumar, A.
  Leandojo: Theorem proving with retrieval-augmented
  language models. In Advances in Neural Information
  Processing Systems 36 (NeurIPS 2023), Datasets and
  Benchmarks Track, 2023.
Yu, Q., Zhang, Z., Zhu, R., Yuan, Y., Zuo, X., Yue, Y., Fan,
  T., Liu, G., Liu, L., Liu, X., et al. Dapo: An open-source
  llm reinforcement learning system at scale. arXiv preprint
  arXiv:2503.14476, 2025.
Yu, W., Jiang, Z., Dong, Y., and Feng, J. Reclor: A reading
  comprehension dataset requiring logical reasoning. arXiv
  preprint arXiv:2002.04326, 2020.
Zeng, W., Huang, Y., Liu, Q., Liu, W., He, K., Ma, Z.,
  and He, J. Simplerl-zoo: Investigating and taming
  zero reinforcement learning for open base models in
  the wild, 2025. URL https://arxiv.org/abs/
  2503.18892.
Zheng, K., Han, J. M., and Polu, S. minif2f: a cross-system
  benchmark for formal olympiad-level mathematics. In
  ICLR, 2022.
Zhou, J. P., Staats, C. E., Li, W., Szegedy, C., Weinberger,
  K. Q., and Wu, Y. Don’t trust: Verify—grounding llm
  quantitative reasoning with autoformalization. In Pro-
  ceedings of the International Conference on Learning
  Representations (ICLR 2024), 2024a.
Zhou, J. P., Staats, C. E., Li, W., Szegedy, C., Weinberger,
  K. Q., and Wu, Y. Don’t trust: Verify – grounding LLM
  quantitative reasoning with autoformalization. In The
  Twelfth International Conference on Learning Represen-
  tations, 2024b.
Zhou, Y., Zhao, J., Zhang, Y., Wang, B., Wang, S., Chen,
  L., Wang, J., Chen, H., Jie, A., Zhang, X., et al. Solving
  formal math problems by decomposition and iterative
  reflection. arXiv preprint arXiv:2507.15225, 2025.




                                                               11
         Learning to Generate Formally Verifiable Step-by-Step Logic Reasoning via Structured Formal Intermediaries

Appendices
A. Use of Large Language Models (LLMS)
While preparing this manuscript, we made use of Large Language Models (LLMs) as writing aids, specifically for tasks such
as grammar correction, wording refinement, and rephrasing to enhance clarity and readability. In line with ethical guidelines,
we, the authors, confirm that we take full responsibility for the content of this work. Any text produced with the assistance of
LLMs has been carefully reviewed, revised, and approved by us. All scientific claims, findings, and conclusions are entirely
our own. We are responsible for any possible mistakes, inaccuracies, or ethical issues that may arise in this submission.

B. Details of Datasets
B.1. ProverQA dataset
The ProverQA dataset contains 1,500 problems evenly split into easy, medium, and hard subsets, each defined by controlled
complexity. For each difficulty level, we first filtered out the instances labeled as ”Uncertain” and reserved 64 instances
examples for testing. To assess generalization to even harder problems, we further synthesized 128 additional extra hard
examples using the same framework, referred to as the Extra Split.
Every instance of ProverQA comprises:

   • A background story created for each problem to introduce linguistic context and variation,

   • A logic skeleton of FOL premises (facts + rules with 7 operators: ∧, ∨, ¬, →, ⊕, ∀, ∃) and distractors (non-essential
     facts or semantically related but irrelevant rules),

   • A goal to classify as True, False, or Uncertain,

   • Intermediate reasoning chains provided in both symbolic form and natural language.

This design meets key criteria: scalability, natural & diverse language, explicit symbolic representations, and faithful
reasoning chains. At the same time, it is challenging enough, for example, GPT4o achieves accuracy 46.2 with standard
prompts, and 50 with CoT prompts for hard samples (Qi et al., 2025b). Hence it is good to work with ProverQA for logical
reasoning studies.

B.2. An Example from ProverQA
  An Example from ProverQA

  {
      "id": 0,
      "options": [
         "A) True",
         "B) False",
         "C) Uncertain"
      ],
      "answer": "B",
      "question": "Based on the above information, is the following statement true, false, or uncertain? Brecken
          ,→ has never experienced heartbreak.",
      "reasoning": "fact1: Brecken has experienced heartbreak.\nrule: Either Brecken has experienced heartbreak or
          ,→ he has never experienced heartbreak, but not both.\nconclusion: Brecken has experienced heartbreak.\n\
          ,→ nTherefore, it is false that Brecken has never experienced heartbreak. The correct option is: B.",
      "context": "Brecken has experienced heartbreak. Either Brecken has experienced heartbreak or he has never
          ,→ experienced heartbreak, but not both.",
      "nl2fol": {
         "Brecken has experienced heartbreak.": "has_experienced_heartbreak(Brecken)",
         "Either Brecken has experienced heartbreak or he has never experienced heartbreak, but not both.": "
          ,→ has_experienced_heartbreak(Brecken) ⊕ has_never_experienced_heartbreak(Brecken)"
      },
      "conclusion_fol": "has_never_experienced_heartbreak(Brecken)"
  }




                                                              12
        Learning to Generate Formally Verifiable Step-by-Step Logic Reasoning via Structured Formal Intermediaries

To illustrate the structure of the ProverQA dataset, we present a representative example as follows. Each entry is organized
as a JSON object containing the question, multiple-choice options, the correct answer, and the reasoning chain used to
derive the conclusion. In addition, the dataset provides a context field capturing the relevant facts and rules, as well as a
mapping from natural language (NL) to first-order logic (FOL) formulas (nl2fol). Finally, the conclusion fol field specifies
the logical statement under evaluation.
This example highlights how ProverQA combines natural language reasoning with its corresponding logical formalization,
enabling the evaluation of models not only on final predictions but also on their formal reasoning steps.

B.3. Knight and Knaves Dataset
The Knights and Knaves (K&K) puzzles(Xie et al., 2025) are an algorithmically generated reasoning dataset where characters
are either knights, who always tell the truth, or knaves, who always lie. The goal is to determine each character’s role from
their statements. The dataset is procedurally generated, providing unlimited variation and unseen test cases for evaluating
generalization. Difficulty is precisely controlled by varying the number of characters (2–8) and the complexity of logical
operations, supporting curriculum learning and out-of-distribution testing. Each puzzle has a single verifiable solution,
ensuring evaluations rely on strict deductive reasoning.
K&K dataset is particularly useful due to its formal, synthetic design. Every puzzle is governed by explicit rules and admits
a unique, deterministic solution, eliminating ambiguity and allowing researchers to clearly separate true reasoning ability
from memorization.
Here is an example adapted from the (Xie et al., 2025).

  An Example from K&K Puzzle Problem

  Problem: A very special island is inhabited only by knights and knaves. Knights always tell the truth, and
       ,→ knaves always lie. You meet 2 inhabitants: Zoey, and Oliver. Zoey remarked, "Oliver is not a knight".
       ,→ Oliver stated, "Oliver is a knight if and only if Zoey is a knave". So who is a knight and who is a
       ,→ knave?

  Solution: (1) Zoey is a knave (2) Oliver is a knight




C. Algorithm Details
For completeness, we revisit the GRPO algorithm in detail. The procedure consists of the following steps:

 1. Samples a group of output sequences {o1 , . . . , oG } for each prompt q from the policy πθold .

 2. Scores each sequence oi with a reward model rϕ (q, oi ), yielding rewards {ri }G
                                                                                   i=1 .


 3. Computes relative advantages by normalizing these rewards within the group:

                                                           1
                                                             PG
                                                      ri − G   j=1 rj
                                             Âi = q P                    2 .
                                                    1 G        1
                                                                 PG
                                                    G     r
                                                      j=1 j  − G       r
                                                                    k=1 k



 4. Optimizes the policy by maximizing a PPO-style clipped surrogate objective, with a KL penalty against a frozen
    reference model πref .

Moreover in the experiments, we implement the clip-higher strategy from the Decoupled Advantage Policy Optimization
(DAPO) algorithm (Yu et al., 2025) to stablize the training of GRPO. This strategy increases the upper clip range of the
importance sampling ratio in the policy gradient loss to encourage exploration. Consistent with the DAPO methodology, we
set the asymmetric clipping range with εlow = 0.2 and εhigh = 0.28.

                                                             13
          Learning to Generate Formally Verifiable Step-by-Step Logic Reasoning via Structured Formal Intermediaries

D. Prompts for The Outcome-CoT Approach
  System Prompt for Outcome-CoT

  System:

  Given a problem statement as contexts, the task is to answer a logical reasoning question.

  The assistant first thinks about the reasoning process in the mind and then provides the user with the answer.
  The reasoning process is enclosed within <think> </think> tags, followed by the answer, i.e., <think> reasoning
       ,→ process here </think> answer here.

  The last A), B), or C) in the answer section (i.e., the content outside <think> </think>)
  will be considered your answer. If the format is incorrect, you may not receive a score.



The User Prompt for the Outcome-CoT approach used in Section 5.2 is as follows.
The prompt begins with a context section containing background knowledge expressed in natural language, including facts
(e.g., Paola appreciates beauty) and rules (e.g., Anyone who can solve problems and communicate effectively has practical
skills). These statements establish the logical environment within which reasoning must take place.
Following the context, the prompt specifies a question that requires truth evaluation of a target statement—in this case,
whether Paola is artistically inclined. The prompt also provides a set of options (True, False, or Uncertain), mirroring the
multiple-choice format used throughout the dataset. Finally, the template ends with the phrase “The correct option is:”,
leaving space for the model to generate its answer.
  User Prompt for Outcome-CoT

  User:

  Context:
  Anyone who can solve problems and communicate effectively has practical skills.
  If Paola appreciates beauty, then she values precision and enjoys manual work.
  Paola appreciates beauty.
  Paola is either skilled in mathematics or has practical skills, but not both.
  If someone enjoys manual work and values attention to detail, then they can craft with their hands.
  Paola is either skilled in mathematics or artistically inclined, but surprisingly, she is actually both.
  Paola values attention to detail.
  Anyone who crafts with their hands has practical skills.

  Question:
  Based on the above information, is the following statement true, false, or uncertain?
  Paola is artistically inclined.

  Options:
  A) True
  B) False
  C) Uncertain

  The correct option is:




E. Prompts and Example Responses for PRoSFI
E.1. System Prompt for PRoSFI
To demonstrate how PRoSFI is guided in the reasoning process, we provide the system prompt used in Section 4 (see
Listing X). The prompt instructs the model to behave as a mathematical reasoner that operates on premises expressed in
Lean4 syntax (e.g., ∧, ∨, ¬, →, ⊕, ∀, ∃).
The structure of the prompt has several key elements:

   • Formatted reasoning: All intermediate thinking is enclosed within <think>...</think>.

   • Formatted summarized output: Inside <summary>...</summary>, the model must return a JSON array of atomic
     inference steps.

                                                             14
       Learning to Generate Formally Verifiable Step-by-Step Logic Reasoning via Structured Formal Intermediaries

Each JSON object specifies:

  • id: a unique identifier for the step,

  • dependencies: the premises or earlier steps it relies on,

  • conclusion: a single new FOL formula expressed in Lean4,

  • rule: the inference rule applied.

Constraints – Each inference step must be as fine-grained as possible (fewer than 5 dependencies), and the JSON must
be valid and parsable. The final object corresponds to the model’s chosen answer and must align with one of the provided
options.
This design enforces faithful, step-by-step reasoning, making the model’s decision process transparent and verifiable.

  System Prompt for PRoSFI

  System:

  You are a math reasoner. For each problem, you will receive a set of premises annotated in Lean4 (use →, ⊕, ∧,
       ,→ ∨, ¬, ∀, ∃). Answer the multiple-choice reasoning question as follows:

  1. Internal reasoning goes inside <think>· · ·</think>.
  2. Then, inside <summary>· · ·</summary>, emit a JSON array of atomic inferences, one per object:

    ‘‘‘json
    {
      "id": "s",
      "dependencies": ["h1 ","s"], // original premises or earlier steps
      "conclusion": ". . .",         // exactly one new FOL formula (Lean4 syntax)
      "rule": ". . ."                // the single inference rule applied
    }
    ‘‘‘

    - The JSON array must be valid and parsable without errors.
    - Each object must represent exactly one atomic inference step.
    - Each step should be as atomic as possible, using less than 5 dependencies.

  The last object in the array corresponds to your answer. Its id and conclusion must be identical to one of the
       ,→ options.




E.2. User Prompt for PRoSFI
To make the interaction format concrete, we show the user prompt used for PRoSFI in Section 4. The prompt is divided
into several components:

  • Context: A sequence of natural language premises paired with their corresponding formal statements in Lean4 syntax.
    For example, the first two premises assert conditional rules about Hattie and Candy, while the 3rd and 4th connect
    moral courage to principled action.

  • Question: A query formulated in natural language, asking whether a target statement (here, “Hattie does not gain
    community respect”) is true or false given the context.

  • Options: The possible answers, each expressed both in natural language and as a formal Lean4 statement.

  • Answer slot: The prompt ends with “The correct option is:”, leaving space for the model to provide its choice.

This structure illustrates how PRoSFI is guided to align natural language reasoning with formal logical inference, ensuring
that both the problem and the candidate answers are clearly specified in parallel in both natural language and formal
statement.

                                                            15
          Learning to Generate Formally Verifiable Step-by-Step Logic Reasoning via Structured Formal Intermediaries

  User Prompt for PRoSFI

  User:

  Context:
  1. If Hattie stands up for her principles, then she gains community respect. Formal statement: ‘h1 :
       ,→ stands_up_for_principles Hattie → gains_community_respect Hattie‘.
  2. If Candy stands up for her principles, then she gains community respect. Formal statement: ‘h2 :
       ,→ stands_up_for_principles Candy → gains_community_respect Candy‘.
  3. Hattie has moral courage. Formal statement: ‘h3 : has_moral_courage Hattie‘.
  4. Everyone who has moral courage will stand up for their principles. Formal statement: ‘h4 : ∀x, (
       ,→ has_moral_courage x → stands_up_for_principles x)‘.

  Question: Based on the above information, is the following statement true or false? Hattie does not gain
       ,→ community respect.

  Options:
  A) True. Formal statement: ‘h_goal_true: ¬gains_community_respect Hattie‘.
  B) False. Formal statement: ‘h_goal_false: ¬(¬gains_community_respect Hattie)‘.

  The correct option is:




E.3. Model Response after RL with PRoSFI
We next illustrate how the model responds after RL with PRoSFI. The response is divided into two main parts:

  • Reasoning path: Enclosed within ¡think¿ . . . ¡/think¿, the model provides a step-by-step explanation in natural
    language. In this case, it applies Universal Instantiation and Modus Ponens to derive that Hattie stands up for her
    principles, and subsequently that she gains community respect. This reasoning shows why the negated claim (Hattie
    does not gain community respect) is false.
  • Structured summary: Enclosed within ¡summary¿ . . . ¡/summary¿, the model outputs a JSON array of atomic
    inference steps. Each object specifies the inference id, the set of dependencies, the derived conclusion (in Lean4
    syntax), and the rule applied. The last object corresponds to the final answer and matches one of the candidate options.

We can see the model’s response is both interpretable in natural language and machine-verifiable through its structured
reasoning steps.
Assistant:

<think>
1. From h4 (∀x, has_moral_courage x → stands_up_for_principles x) and h3 (has_moral_courage Hattie), by Universal
      ,→ Instantiation on Hattie and Modus Ponens, derive stands_up_for_principles Hattie.
2. From h1 (stands_up_for_principles Hattie → gains_community_respect Hattie) and the above, by Modus Ponens,
      ,→ derive gains_community_respect Hattie.
3. Therefore ¬ gains_community_respect Hattie is false.
</think>
<summary>[
  {
     "id": "s1",
     "dependencies": ["h3 ", "h4 "],
     "conclusion": "stands_up_for_principles Hattie",
     "rule": "Universal Instantiation + Modus Ponens"
  },
  {
     "id": "h_goal_false",
     "dependencies": ["h1 ", "s1"],
     "conclusion": "¬(¬gains_community_respect Hattie)",
     "rule": "Modus Ponens"
  }
]
</summary>




F. Typical Errors for Outcome-CoT
In this section, we select two representative cases to analyze two typical types of errors that occur during the reasoning
process of the Outcome-CoT model, namely semantic confusion and commonsense shortcuts.

                                                             16
        Learning to Generate Formally Verifiable Step-by-Step Logic Reasoning via Structured Formal Intermediaries

F.1. Semantic Confusion
User:

Context:
···
3. Either Miracle is community-oriented or self-centered, but not both.
···
6. If Miracle is a leader, then she is either selfless or thinks of herself, but not both.
···
Assistant:
···
Since she is community-oriented, she cannot be self-centered (statement 3). Therefore, she must be selfless. Thus,
     ,→ the statement ’Miracle is not self-centered’ is true.
···


In this example, the model infers that “Miracle is not self-centered” from the premise that “Miracle is
community-oriented”, and then equates “not self-centered” with “selfless”. In doing so, it bypasses a
rigorous logical analysis of the premises and directly concludes that “Miracle is selfless”. However, determining
whether Miracle is truly selfless requires a more comprehensive evaluation based on Proposition 6, whether Miracle is
a leader, as well as the mutually exclusive conditions specified by the two choices. Thus, the model’s conclusion reflects a
logical error arising from semantic confusion.

F.2. Commonsense Shortcut
User:

Context:
···
6. If Alvaro faces adversity, then he either stays motivated or pursues his goals, but not both.
···
Assistant:
···
Since Alvaro is facing adversity and is either staying motivated or pursuing his goals, it is clear that Alvaro is
     ,→ overcoming challenges in some form. Therefore, the statement "Alvaro does not overcome challenges" is false.
···


In this example, after confirming that Alvaro is facing adversity and satisfies either “staying motivated” or
“pursuing goals”, the model proceeds to conclude that “Alvaro overcame the challenge”. Although this
inference may seem reasonable from a commonsense perspective, it lacks a rigorous logical basis. The context of the
question does not provide information on whether Alvaro actually overcame the challenge. Therefore, the model’s conclusion
is a flawed logical generalization based on a commonsense shortcut, which fails to adhere to the principles of deductive
reasoning.

G. Details and Credibility Analysis of the GPT Soundness Metric
  System prompt

  System:

  The following is a problem statement and a reasoning chain to solve it.

  Problem:
  ...

  Reasoning:
  ...

  Task:
  Please evaluate whether the reasoning process contains any irreparable logical errors.
  - If so, return a JSON where "is_error" is True, "error_instance" contains the original text of the first
       ,→ instance of the error, "error_type" specifies the type of the error, and "error_reason" explains the
       ,→ reason for the error.
  - Otherwise, return a JSON where "is_error" is False.
  Wrap your JSON within ‘‘‘json ‘‘‘.



We use a simple prompt to ask the GPT-OSS-120B model to evaluate the correctness of the reasoning path and ask it to

                                                            17
        Learning to Generate Formally Verifiable Step-by-Step Logic Reasoning via Structured Formal Intermediaries

return a JSON; when the reasoning is correct, it only needs to return a bool value, but when it is incorrect, it needs to provide
the location and reason for the error.
We manually checked 10 outputs each from Outcome-CoT and PRoSFI to evaluate the correctness of GPT’s assessment
of the reasoning process.
For the outputs of Outcome-CoT, GPT’s evaluations were all correct. Among them, 8 outputs had errors of invalid
deduction, one output was completely correct, and one output had an error of misinterpretation of premise.
For the outputs of PRoSFI, GPT’s evaluations were almost entirely correct but slightly too strict. Among them, 5 outputs
had errors of invalid deduction, while 3 outputs were completely correct. The remaining two outputs had reasoning that was
generally correct but contained some minor errors: the first output used unnecessary premises in one step, and the second
output wrote the wrong name for the reasoning rule used.

H. Reward Function for PRoSFI Step-by-Step Verification
We first extract a structured JSON representation from the natural language reasoning paths generated by the model. We
then determine whether the format is correct based on its validity and the structural specifications defined in the main text.
By analyzing the id and conclusion fields of the last object in the JSON, we can determine whether the final answer is
correct.
To verify the logical correctness of the entire reasoning process, we use a top-down syntax parser to parse the first-order
logic (FOL) expressions generated by the model. These are then converted into formats supported by target formal tools
such as Lean4, Prover9, or Z3. For each reasoning conclusion, we express it as a proposition in Lean4 and verify it using a
sequence of tactics or a large language model capable of formal theorem proving. Alternatively, the reasoning steps can be
converted into input formats accepted by Prover9 or Z3, and the validity of each step can be verified using an automated
solver.

Algorithm 1 Reward Function for PRoSFI Step-by-Step Verification
 1: Input: response, ground truth
 2: Output: score
 3: summary ← extract summary(response)
 4: statements ← extract fol problems(summary, ground truth)
 5: if statements is None then
 6:    return 0.0
 7: end if
 8: if summary.last id ̸= ground truth then
 9:    return format score
10: end if
11: if fol all solved(statements) then
12:    return full score
13: else
14:    return option score
15: end if


The algorithm is presented in Algorithm 1, which follows this routine:

  1. Extract a summary and FOL statements from the model’s response.

  2. If no valid statements are extracted, return a score of 0.

  3. If the ID of the final reasoning step doesn’t match the ground truth, return a score reflecting formatting issues.

  4. If all FOL problems are solved correctly, return the full score.

  5. Otherwise, return a partial (optional) score.

                                                               18
        Learning to Generate Formally Verifiable Step-by-Step Logic Reasoning via Structured Formal Intermediaries

I. Correlation Analysis of the Results on Outcome-CoT
For the output of the Outcome-CoT method, we analyze the relationship between two available metrics: the correctness of
the final answer and the reasoning soundness automatically evaluated by GPT (GPT Soundness). The confusion matrix is
shown in Figure 4.
It can be observed that a large number of reasoning paths, although yielding the correct answer, are evaluated as unsound in
their reasoning process. This result indicates that a correct answer alone is not sufficient to reflect the logical validity of the
reasoning process. It further supports the qualitative observation in Section 5.2 — namely, that traditional CoT methods
struggle to ensure the validity of reasoning paths.
                     Reasoning Unsound




                                               89                        710                 267                     1538
            GPT Soundness
                     Reasoning Sound




                                                0                        225                   0                        243


                                         Answer Incorrect         Answer Correct        Answer Incorrect         Answer Correct
                                                    Answer Correctness                             Answer Correctness
Figure 4. Left: Confusion matrix of answer correctness vs. reasoning soundness for Outcome-CoT on the ProverQA-hard subset.
Right: Corresponding results on the ProverQA-extra subset. The lack of alignment between correct answers and sound reasoning
indicates that answer accuracy alone is not a sufficient criterion for judging the quality of reasoning.

In comparison, Figure 3 presents the heatmaps of variable correlations on the two subsets. The results show that the designed
reward signal has a stronger correlation with GPT Soundness than with the final answer correctness. This suggests that our
formal verification mechanism effectively identifies and enhances logical rigor, making it a more reliable signal for training
and selection.




                                                                                   19
