                                                  MA-LoT: Model-Collaboration Lean-based Long Chain-of-Thought
                                                          Reasoning enhances Formal Theorem Proving


                                                                  Ruida Wang * 1 Rui Pan * 1 Yuxin Li * 2 Jipeng Zhang 2 Yizhen Jia 1
                                                                         Shizhe Diao 3 Renjie Pi 2 Junjie Hu 4 Tong Zhang 1
arXiv:2503.03205v3 [cs.CL] 27 May 2025




                                                                  Abstract                                    1. Introduction
                                                                                                              Formal reasoning is a cornerstone of human intelligence
                                                                                                              and a key objective in machine learning (Newell & Simon,
                                               Solving mathematical problems using computer-                  1956), often evaluated through rigorous mathematical deriva-
                                               verifiable languages like Lean has significantly               tions (Yang et al., 2024a). With the rise of Large Language
                                               impacted the mathematical and computer sci-                    Models (LLMs), Chain-of-Thought (CoT) prompting has
                                               ence communities. State-of-the-art methods uti-                emerged to formalize reasoning by generating intermediate
                                               lize a single Large Language Model (LLM) to                    steps. This approach improves interpretability and enhances
                                               generate complete proof or perform tree search,                reasoning performance (Wei et al., 2022).
                                               but they fail to balance these tasks. We pro-
                                                                                                                                       Initial state
                                               pose MA-LoT: Model-CollAboration Lean-based                           Return                                       Theorem
                                                                                                                    last state                                    Statement
                                               Long Chain-of-Thought, a comprehensive frame-
                                               work for Lean4 theorem proving to solve this is-
                                                                                                                         Wrong state                                Prover
                                                                                                                                                                                Another
                                               sue. It separates the cognition tasks of general NL                                                                  LLM        generation
                                               for whole-proof generation and error analysis for                                                                               ❌
                                                                                                                                                                  Analysis +
                                               proof correction using the model-collaboration                                                                     Complete
                                                                                                                                                                    proof
                                               method. We achieve this by structured interac-                                                          ✅

                                               tion of the LLM and Lean4 verifier in Long CoT.                                                 Proof Done    ✅
                                               To implement the framework, we propose the                                Tree-Search Method:                Whole-proof generation
                                               novel LoT-Transfer Learning training-inference                            ✅ Use ITP to check                 ✅ LLM NL planning and reasoning
                                               pipeline, which enables the Long CoT thinking ca-                         ✅ Find non-trivial proof           ✅ Controllable cost
                                                                                                                         ❌ Expensive                        ❌ No intermediate feedback
                                               pability to LLMs without special data annotation.                         ❌ No Long-term NL planning         ❌ Usually trivial solution
                                               Extensive experiment shows that our framework
                                               achieves a 61.07% accuracy rate on the Lean4 ver-              Figure 1. Two main directions of FL theorem proving using LLMs:
                                               sion of the MiniF2F-Test dataset, largely outper-              Single model tree-search and whole-proof generation with their
                                               forming DeepSeek-V3 (33.61%), single-model                     advantages/disadvantages.
                                               tree search (InternLM-Step-Prover, 50.70%), and                However, the ambiguity of Natural Language (NL) compli-
                                               whole-proof generation (Godel-Prover, 55.33%)                  cates verifying intermediate steps, particularly in advanced
                                               baselines. Furthermore, our findings highlight the             mathematics, where there is no answer to check but theo-
                                               potential of combining Long CoT with formal                    rems to prove. This challenge is exacerbated by the growing
                                               verification for a more insightful generation in a             complexity of modern mathematics, which makes proof ver-
                                               broader perspective.                                           ification highly demanding and can lead to errors, as seen in
                                                                                                              the prolonged validation of Fermat’s Last Theorem (Wang
                                                                                                              et al., 2024). Researchers propose grounding reasoning in
                                                                                                              rigorous first-order logic to address this, enabling automated
                                           *
                                             First Authors 1 Department of Computer Science, University       verification via Formal Language (FL) verifiers. This frame-
                                         of Illinois Urbana-Champaign 2 Hong Kong University of Science       work ensures rigor and has led to the development of tools
                                         and Technology 3 NVIDIA 4 Department of Computer Science,
                                         University of Wisconsin-Madison. Correspondence to: Ruida            like Lean (De Moura et al., 2015; Moura & Ullrich, 2021),
                                         Wang <ruidaw@illinois.edu>.                                          Isabelle (Paulson, 1994), and HOL Light (Harrison, 2009)
                                                                                                              for verifiable theorem proving.
                                         Proceedings of the 42 nd International Conference on Machine
                                         Learning, Vancouver, Canada. PMLR 267, 2025. Copyright 2025          However, writing mathematical proofs in FL requires signif-
                                         by the author(s).                                                    icant expertise and effort, as most proofs involve extensive

                                                                                                          1
      MA-LoT: Model-Collaboration Lean-based Long Chain-of-Thought Reasoning enhances Formal Theorem Proving


                                                              Prompt                                                  Prompt
                     LoT-Solver                                                     LoT-Solver                                                  LoT-Solver
                      as Prover                       1st Proof +                  as Corrector                  2nd Proof +                   as Corrector
                                                    Rethink prompt                                             Rethink prompt

                                                                ❌                                                       ❌

                     NL-Planning                                                   Error analysis                                             Error analysis                      ……
     Prompt             CoT                                                            CoT-1                                                      CoT-2

                                                               ✅                                                        ✅
                       1st Proof                                                       2nd Proof                                                   3rd Proof

                                                       Proof Done                                                 Proof Done

                                                              (a) Model-Collaboration Lean-based Long CoT inference

                                                                                    Training data sample                                   Inference data sample
                                                                          System Prompt: Complete the following Lean4             System Prompt: Complete the following Lean4
                         NL Statement:                                    theorem WITHOUT Long CoT                                theorem WITH Long CoT
                         Show that it is false that ¬a ∧ a.
                         Proof by contradiction                           ### NL statement:                                       ### NL statement:
                                                                          Show that it is false that ¬a ∧ a.                      Show that it is false that ¬a ∧ a.
                                                                          Proof by contradiction                                  Proof by contradiction
                                                                                                                                                                             Inferenced part
    Lean SFT                                                              ### FL statement:                                       ### FL statement:
                                                                          theorem not_and_self : ¬(¬a ∧ a)                        theorem not_and_self : ¬(¬a ∧ a)
      data
                                                                          <Thought> Not use CoT to solve </Thought>               <Thought> Alright, let me solve this step-by-
                                                                                                                                  step … </Thought>
                         Commented Theorem:                               ### Completed proof:                                    ### Completed proof:
                         theorem not_and_self : ¬(¬a ∧ a)                 theorem not_and_self : ¬(¬a ∧ a)                        theorem not_and_self : ¬(¬a ∧ a)
                            -- Proof by contradiction                        -- Proof by contradiction                               -- Proof by contradiction
                            | ⟨hn, ha⟩ => hn ha                              | ⟨hn, ha⟩ => hn ha                                     | ⟨hn, ha⟩ => hn ha
                                                                                                               Trained part

                                                                       (b) LoT-TL Training-Inference pipeline



                  Pretrained                      General NL Long                          Lean SFT data                    Lean Correction                            LoT-Solver
                    LLM                            CoT data (SFT)                            (LoT-TL)                        data (LoT-TL)

                                                                        (c) Training procedure of LoT-Solver

Figure 2. MA-LoT Framework: (a) Model-collaboration Lean4 theorem proving framework: The LoT-Solver model functions as the
prover to generate initial Lean4 proofs with emergent NL planning for Lean proof in Long CoT (orange block); then it acts as corrector to
analyze error from Lean executor in Long CoT to output a refined proof. (b) LoT-Transfer Learning (TL): The novel training-inference
pipeline enables formal reasoning ability to emerge in Long CoT (L-CoT) without the need for specifically annotated data. This is
achieved by adjusting the system prompt to control the on/off of L-CoT in training and inference. (c) Training procedure of LoT-Solver:
We use normal SFT to train general NL L-CoT, use LoT-TL to train on the Lean SFT, and correction data to make Lean L-CoT an emergent
capability in LLM.
repetition and application of low-resource functions (Jiang                                           writing (Polu & Sutskever, 2020; Polu et al., 2022; Xin
et al., 2022). With the rapid progress of LLMs, research                                              et al., 2024b; Wu et al., 2024a; Lin et al., 2024) or retrieval-
has explored LLMs’ application in FL reasoning to auto-                                               based techniques (Yang et al., 2024b; Kumarappan et al.,
mate theorem proving (Polu & Sutskever, 2020; Polu et al.,                                            2024). Tree-search methods apply an FL executor to verify
2022; Jiang et al., 2021; 2022; Yang et al., 2024b; Xin et al.,                                       after each generation step and can discover some non-trivial
2024b; Wang et al., 2024; Wu et al., 2024a; Kumarappan                                                proofs. However, as proof complexity increases, tree-search
et al., 2024; Lin et al., 2024). Prior research follows two                                           methods become computationally expensive and lack high-
main approaches, namely, tree-search (Jiang et al., 2021;                                             level NL planning to control the overall structure of the
2022; Lin et al., 2024; Xin et al., 2024b; Wang et al., 2024)                                         proof. The lack of overall planning causes the tree-search
and whole-proof generation (Polu & Sutskever, 2020; Polu                                              method to be unable to find some structured proof that
et al., 2022; Yang et al., 2024b; Wu et al., 2024a; Kumarap-                                          requires high-level NL planning to answer the question.
pan et al., 2024). The summary of dis/advantages of these
                                                                                                      In contrast, whole-proof generation treats theorem proving
two methods can be found in Figure 1.
                                                                                                      like the code generation problem, where LLMs generate
Tree-search methods train an LLM to iteratively generate                                              the entire proof in a single attempt using either supervised
proof steps by predicting the next tactic based on the current                                        training (Wang et al., 2024; Xin et al., 2024b) or prompt en-
proof state. This is achieved through either direct code                                              gineering (Jiang et al., 2021; 2022). This approach leverages


                                                                                                2
      MA-LoT: Model-Collaboration Lean-based Long Chain-of-Thought Reasoning enhances Formal Theorem Proving

LLMs’ NL reasoning and high-level planning capabilities               ing state-of-the-art whole-proof generation models (Godel-
with predictable computation costs, but it lacks intermediate         Prover (Lin et al., 2025), 55.33%) and tree-search baseline
feedback from FL executors. As a result, the generated                (InternLM-Step-Prover(Wu et al., 2024a), 50.70%).
proofs often lack post-hoc analysis of errors and tend to
                                                                      We summarize our contributions as follows: (1) We in-
perform badly on tedious questions that require non-trivial
                                                                      troduce MA-LoT, a comprehensive model-collaboration
or tedious tricks. In summary, existing single-model ap-
                                                                      framework to balance NL reasoning and FL verification
proaches struggle to balance the NL reasoning with the FL
                                                                      under the Long CoT paradigm for Lean4 theorem proving.
verifiability, motivating the need for a more comprehensive
                                                                      (2) We propose using Long CoT to synergically combine
framework.
                                                                      the nature of NL and FL, allowing the model to generate in-
To address the above challenges in Lean4 theorem proving,             depth and insightful formal reasoning through NL planning
we introduce MA-LoT: Model-CollAboration Lean-based                   and analysis. (3) We develop LoT-TL, a training-inference
Long Chain-of-Thought, a comprehensive framework de-                  pipeline that makes field-specific Long CoT capabilities
signed to coordinate multiple models for effective formal             emerge to LLMs without requiring explicitly annotated
reasoning. As illustrated in Figure 2 (a), MA-LoT sepa-               datasets.
rates the cognitive process into two distinct tasks: high-level
                                                                      Our framework has broad potential beyond Lean4 theorem
proof planning and writing, as well as fine-grained correc-
                                                                      proving, demonstrating how formal verification can be
tion based on verifier feedback. This separation is enabled
                                                                      effectively integrated with Long CoT reasoning. This
by a collaborative model architecture and the emergent rea-
                                                                      approach reveals the potential for structured, reflective, and
soning capability of Long CoT, which was developed during
                                                                      adaptable general text generation through iterative planning
training. The framework consists of two core components:
                                                                      and error analysis on formal executors. To accelerate
a prover model, responsible for generating well-structured
                                                                      advancements in this field, we open-source our code
proofs, and a corrector model, which interprets feedback
                                                                      at https://github.com/RickySkywalker/LeanOfThought-
from the Lean4 verifier to refine the output. Both models
                                                                      Official
are enhanced with Lean4 field-specific Long CoT capability,
allowing them to reason more thoroughly before producing
outputs. Moreover, we integrate Lean verification results             2. Methodology
into Long CoT to improve the system’s self-reflection and
                                                                      In this section, we detail the development of the MA-LoT
correction abilities.
                                                                      framework and training procedure of LoT-Solver model for
To implement the MA-LoT framework, we propose a novel                 Lean4 theorem proving. Our framework’s core idea is to
training-inference pipeline called LoT-Transfer Learning              enable the model to perform Long Chain-of-Thought (CoT)
(LoT-TL), which is used to train the LoT-Solver model, as             reasoning under the context of Lean4 theorem proving. The
shown in Figure 2 (b) and (c). This pipeline enables the              Long CoT is designed to perform deep integration between
emergence of using Long CoT to solve the FL problems                  Natural Language (NL) and Formal Language (FL) reason-
without requiring specifically annotated formal data. It is           ing. Training of such Long CoT thinking model is achieved
achieved by leveraging transfer learning across three data            under an extreme scarcity of NL-FL aligned data faced
sources: NL-based general Long CoT reasoning, SFT data                by the entire field (Wang et al., 2024). We introduce the
for theorem proving under the code completion task, and               methods by first outlining the preliminaries of LLM for-
in/correct proof pairs based on Lean4 feedback. Through               mal theorem proving in Section 2.1. Then, we describe
structured adaptation, LoT-TL equips the model with aware-            the LoT-Transfer Learning (LoT-TL) training pipeline in
ness of FL proof states and tactics while preserving its strong       Section 2.2. Finally, we present comprehensive details on
NL reasoning and planning capabilities. Then, the model               how our trained model facilitates MA-LoT framework for
trained under this pipeline can generate coherent and in-             Lean4 proof writing in Section 2.3.
sightful formal proofs grounded in both symbolic precision
and high-level planning.                                              2.1. Preliminaries
Extensive experiments demonstrate that MA-LoT frame-                  We introduce preliminary knowledge of applying Long
work effectively enhances the model’s formal reasoning                Chain-of-Thought (CoT) LLMs to Lean4 formal theorem
ability through model-collaboration design and emergent               proving in a model-collaboration manner.
formal reasoning in Long CoT. The framework can success-
fully prove some of the advanced IMO and AIME problems                Current state-of-the-art methods treat Lean4 code as plain
in the MiniF2F dataset (Zheng et al., 2021), with which               text and feed it directly to LLMs. There are two main
existing models struggle. Under similar sampling budgets,             branches of techniques to apply LLMs for Lean4 theorem
our framework achieves a 61.07% accuracy rate, surpass-               proving. The first branch is the tree-search method (Yang
                                                                      et al., 2024b; Wu et al., 2024a). This method converts the

                                                                  3
      MA-LoT: Model-Collaboration Lean-based Long Chain-of-Thought Reasoning enhances Formal Theorem Proving

Lean4 theorem statement and current proof state (includ-            OBT (Wang et al., 2024)), or lack Lean4 proofs (e.g., Lean-
ing conditions and goals based on the existing proofs) into         Workbook (Ying et al., 2024)).
plain text as input to LLMs and asks it to generate the next
                                                                    To address this, we compile a new Lean theorem proof
possible tactic to complete the proof. The other direction
                                                                    dataset named LoT-ProveData (LoT-PD), containing 54,465
is whole-proof generation methods. It provides the LLMs
                                                                    data records. Each record contains Lean4 theorem state-
with NL instruction, NL theorem statement, and Lean4 state-
                                                                    ments, verified proofs with NL explanations as comments,
ment to the LLMs. The intended outcome is to generate
                                                                    and NL statements. The Lean4 theorem proofs come
a complete Lean4 proof in a single pass. This is achieved
                                                                    from two sources: the DeepSeek-Prover-v1 dataset and
by first leveraging the LLM’s NL reasoning to produce a
                                                                    the annotated Lean-Workbook using TheoremLlama and
high-level plan, then guiding the generation of the actual
                                                                    DeepSeek-Prover-v1.5-RL. Next, inspired by the analysis-
Lean4 proof The input-output examples for both tree-search
                                                                    then-generate approach in Wang et al. (2023), we employ
and whole-proof generation are presented in Appendix B.
                                                                    Qwen-2.5-72B to provide an analysis of Lean4 proofs, fol-
The Long CoT LLMs, represented by O1 (OpenAI, 2024),                lowed by writing the NL proof based on the analysis. Fi-
make long internal NL thinking before outputting the final          nally, we integrate these NL proofs as comments in the
answer. It largely enhances the NL math reasoning ability           Lean4 code by Qwen. For data records lacking NL state-
of LLMs through self-reflection and correction in Long CoT.         ments, we generate NL statements using a similar method.
However, it still struggles to provide rigorous NL proofs           The core components of our LoT-ProveData are as follows:
and typically has relatively low FL capability.
                                                                    {FL Statement, Commented FL proof, NL
Our approach combines the strengths of tree search                   ,→ statement}
and whole-proof generation methods through a model-
collaboration system. By leveraging Long CoT, we coordi-            During proof generation for the ProverData, some incor-
nate the interaction between NL and FL in LLMs, which               rect proofs were also produced. We recorded these along-
allows the model to write more structured and insightful            side their error messages to form LoT-CorrectionData (LoT-
proofs.                                                             CD), consisting of 64,912 records of correct-incorrect Lean4
                                                                    proof pairs with error messages of the incorrect proof. Ad-
2.2. LoT-TL Training Pipeline                                       ditionally, it contains an NL statement and proof of the
                                                                    theorem. LoT-CD is used to train the model’s error analysis
This section introduces a simple but effective training             and correction capability. The core part of the LoT-CD is:
pipeline LoT-Transfer Learning (LoT-TL). The pipeline in-
tends to make LLMs have the ability to perform Lean4                {FL Statement, Correct FL proof, Error
field-specific Long CoT reasoning. Such ability can be ob-           ,→ messages, Incorrect FL proof, NL
tained through LoT-TL without the need for specifically              ,→ statement}
annotated Long CoT data. The main idea of LoT-TL is
                                                                    These datasets work together to improve both the prover and
to leverage system prompts to regulate training and infer-
                                                                    corrector models’ capability, acting as the source of strong
ence behaviors, which can be divided into the following
                                                                    NL-FL joint thinking ability for our model-collaboration
stages: (1) collecting field-specific Supervised Fine-Tuning
                                                                    framework.
(SFT) data (Section 2.2.1), (2) training the model on general
natural language Long CoT tasks (Section 2.2.2), and (3)
                                                                    2.2.2. NL L ONG C OT T RAINING
training the model using the transfer learning method on
SFT and correction data to make formal Long CoT abil-               In the second stage, we train a normal instruction-finetuned
ity emerge(Section 2.2.3). Although this paper focuses on           model to obtain the general Long CoT reasoning capa-
Lean4, our framework shows potential to be applied to more          bility in Natural Language. We use the OpenO1-SFT-
fields, making LLMs obtain field-specific Long CoT capa-            Pro dataset provided by Open-Source-O1 (2024), a 126k
bility without RL or special data annotation.                       records dataset for general NL question-answering on math
                                                                    and science topics with Long CoT for training. We apply
2.2.1. O BTAIN SFT DATA                                             standard next-token prediction SFT, guiding the model to
                                                                    produce Long CoT before it outputs final answers. Through-
The first step of LoT-TL pipeline is to gather a moderate
                                                                    out the NL Long CoT training, we set the system prompt as
amount of NL-FL aligned SFT data for the specific target
                                                                    follows to explicitly instruct the model to use the Long CoT
field (in our case, Lean4). However, existing open-source
                                                                    approach:
datasets do not meet the requirement. They are typically
small in size (e.g., MiniF2F (Zheng et al., 2021)), or omit         You are a helpful assistant who will
NL annotations (e.g., DeepSeek-Prover-v1 dataset (Xin                ,→ solve every problem **WITH** Long
et al., 2024a)), or exhibit relatively low NL quality (e.g.,         ,→ Chain-of-Thought

                                                                4
      MA-LoT: Model-Collaboration Lean-based Long Chain-of-Thought Reasoning enhances Formal Theorem Proving

This system prompt indicates that the model should use the           and tree-search methods under the Lean-based Long CoT
Long CoT to write the answer. The training input includes            paradigm. We use the LoT-Solver as the base model for both
the system prompt and NL question, with the expected out-            the prover and the corrector. Under this setup, we use the
put being the Long CoT and final answer. After training,             prover model to write a complete proof draft (Section 2.3.1)
we observe that the model gains robust NL Long CoT ca-               and apply the corrector model to analyze and correct the
pabilities, which serve as a base for models to analyze and          proof based on Lean verifier feedback (Section 2.3.2).
interact with Lean code. However, when applied to Lean4
reasoning, it tends to provide only NL solutions rather than         2.3.1. P ROVER M ODEL
outputting Lean4 code in its output section, indicating the
                                                                     The prover model writes the initial Lean4 proof using a
need for further alignment.
                                                                     whole-proof generation strategy. Then, it is submitted to
                                                                     the Lean4 verifier to check its correctness and passed to the
2.2.3. F IELD - SPECIFIC ALIGNMENT
                                                                     corrector model if it is wrong. We use the system prompt to
In the final stage of the training process of LoT-TL pipeline,       turn on the Long CoT reasoning and use a specific header in
we train the model to obtain emergent Lean4 Long CoT                 Long CoT to guide the model in making a high-level proof
ability. In this training stage, we set the system prompt to         plan. Here is the instruction template for the prover model:
instruct the model not to use Long CoT when answering.               {... **WITH** Long CoT ...}
In the meantime, to make the model aware of the Long                 ### Instruction:
CoT structure, we use a simple placeholder to occupy the             {NL statement}
original place of the Long CoT. The above method allows us           {FL statement}
to train the model aware of the Lean4 Long CoT structure             ### Response:
without requiring any Lean4 Long CoT data. Specifically,             Alright, I should do the following:
the system prompt is:                                                1. Provide the natural language
You are a helpful assistant who will                                  ,→ analysis for the theorem based on
 ,→ solve every problem **WITHOUT**                                   ,→ the Natural language theorem
 ,→ Long Chain-of-Thought                                             ,→ statement.
                                                                     2. Draft the Lean4 tactics I should use
and the placeholder Long CoT is:                                      ,→ to solve the problem
                                                                     3. Write the output Lean4 code.
The user asks not to solve with Long
 ,→ CoT, so I will directly write the                                The prover model’s input and output example can be found
 ,→ answer.                                                          in Appendix G. The emergent Lean reasoning ability in the
                                                                     Long CoT enables the model to write a better-structured
Under this setup, we first train on the LoT-ProveData for            proof based on its high-level plan than direct proof genera-
formal theorem proving ability, then train on the LoT-               tion. Upon generating the proof, the prover model submits
CorrectionData to make the model learn error-analysis and            it to the Lean evaluator for verification. The theorem is
correction skills. The example of training data can be found         then passed to the corrector model for further refinement if
in Appendix F. We also adopt the curriculum learning data            incorrect.
sorting method from Wang et al. (2024) to stabilize training.
After training, we find that the Long CoT Lean4 proving              2.3.2. C ORRECTOR M ODEL
and error analysis ability emerges in the LLMs when using
the system prompt to turn on Long CoT in inference. We               After receiving a wrong proof and Lean verifier feedback,
conclude the effectiveness of the TL framework because it            the corrector model will systematically analyze them in
preserves the structure of Long CoT and enables the model            Long CoT. The corrector re-evaluates and rethinks the proof
to activate such capability when instructed.                         strategy, then generates a revised proof that intends to cor-
                                                                     rect the errors and complete the proof. In conceptual anal-
Following the above steps, we train the LoT-Solver model             ogy, the corrector model functions similarly to the tree-
based on an expert Lean4 prover with instruction fine-tuning.        search method but with greater flexibility and deeper analy-
LoT-Solver is a model with Lean4 Long CoT reasoning                  sis.
capability, which also enables the separation of whole-proof
writer and corrector.                                                The instruction prompt remains identical to the prover
                                                                     model. We incorporate the incorrect proof and feedback
                                                                     from the Lean verifier in the Long CoT, followed by instruc-
2.3. Model-Collaboration Lean4 Proof Writing
                                                                     tions to direct the model to analyze the error and formulate
This section presents the model-collaboration framework              a revised proof. Detailed examples of such prompts are
that combines the advantages of whole-proof generation               available in Appendix G. Then, the corrector model will

                                                                 5
      MA-LoT: Model-Collaboration Lean-based Long Chain-of-Thought Reasoning enhances Formal Theorem Proving

pass the new proof to the Lean4 verifier. If the new proof                 3.1.2. BASELINES
is still wrong, iteratively analyze the errors until success or
                                                                           To highlight MA-LoT ’s capabilities, we select some
reach the max retry limit.
                                                                           of the most competitive baselines in recent years, cov-
The corrector model enhances theorem proving by enabling                   ering both tree-search and whole-proof generation ap-
deeper reflection and systematically exploring alternative                 proaches. For tree-search methods, we include: Expert
proof strategies based on error messages. This iterative cor-              Iteration (Polu et al., 2022), Llemma (Azerbayev et al.,
rection process increases the likelihood of discovering non-               2023), ReProver (Yang et al., 2024b), Lean-STaR(Lin et al.,
trivial proofs while maintaining computational efficiency.                 2024), and InternLM2.5-StepProver(Wu et al., 2024a) as our
                                                                           baselines. For whole-proof generation baselines, we include
3. Experiments                                                             closed-source LLMs, represented by GPT-4-Turbo(Achiam
                                                                           et al., 2023), Gemini-1.5(Reid et al., 2024), and DeepSeek-
We conduct comprehensive experiments on the MiniF2F-                       V3 (Liu et al., 2024). Moreover, we include representative
Lean4 (Zheng et al., 2021) dataset to assess the perfor-                   open-source expert models for whole-proof writing, such as
mance of the MA-LoT framework in formal proof writ-                        DeepSeek-Math(Shao et al., 2024), TheoremLlama(Wang
ing. Specifically, we intend to prove the advantage of the                 et al., 2024), DeepSeek-Prover-v1.5-RL (Xin et al., 2024b)2 ,
MA-LoT framework by showing its capability to generate                     STP-Lean (Dong & Ma, 2025), and Godel-Prover-SFT (Lin
better-structured and more insightful proofs. We do this                   et al., 2025).
by showing our model has a better general performance in
                                                                           For whole-proof generation baselines, we set the sample
Section 3.3. Moreover, we perform studies on our correc-
                                                                           budget to pass@128 with 4096 context length (except for
tor model in Section 3.4, the efficiency of the Long CoT
                                                                           Godel-Prover, where, following the original paper, we use
method in Section 3.5, training components of LoT-Solver
                                                                           pass@32), balancing robustness and manageable GPU con-
in Section 3.6, and a case study in Section 3.7 to further
                                                                           sumption. We align the search cost as closely as possible
analyze the impact of individual components.
                                                                           for tree-search methods to whole-proof generation.3
3.1. Experiment Setup
                                                                           3.2. Implementation Details
3.1.1. DATASET AND TASK
                                                                           In the model’s training process, we use Openo1-SFT-Pro,
In this paper, we assess MA-LoT’s Lean4 reasoning capabil-                 LoT-ProverData, and LoT-CorrectionData to train two base
ities on the MiniF2F-Test and Valid1 datasets (Zheng et al.,               models, namely DeepSeek-Prover-v1.5-SFT and Godel-
2021; Yang et al., 2024b; Wang et al., 2024). MiniF2F is a                 Prover-SFT. For different training stages, the learning rate is
widely used and challenging benchmark for formal theorem                   as follows: 1E-5 for NL Long CoT training, 1E-7 for LoT-
proving (Frieder et al., 2024), which is adopted in nearly                 TL on LoT-PD, and 1E-6 for LoT-CD. The total computa-
all major studies in the field (Jiang et al., 2021; Polu et al.,           tional cost for training is around 1 GPU day, and evaluation
2022; Jiang et al., 2022; Wu et al., 2024a; Lin et al., 2024;              is 11 GPU days on a 4× H100-96G cluster4 . To evaluate
Yang et al., 2024b; Xin et al., 2024b; Wang et al., 2024;                  our framework in detail, we present three sets of results,
Azerbayev et al., 2023).                                                   including: (1) LoT (whole-proof): pass@128 whole-proof
                                                                           generation result of LoT-Solver. (2) MA-LoT: Our primary
Both the test and validation datasets contain 244 Lean4 state-
                                                                           evaluation result, where the prover performs 64 whole-proof
ments. The range of problems varies from high-school com-
                                                                           generations and undergoes two rounds of corrector refine-
petition questions to undergraduate-level theorem proofs. It
                                                                           ment5 . (3) Cumulative Results: A combined evaluation
includes 488 problems from three sources: (1) 260 problems
                                                                           aggregating all LoT models’ outputs obtained throughout
sampled from the MATH dataset (Hendrycks et al., 2021);
(2) 160 problems from high-school math competitions, in-                      2
                                                                                 The reported results of DeepSeek-Prover-V1.5 and Goedel-
cluding AMC, AIME, and AMO; (3) 68 manually crafted                        Prover in our paper are different from the original paper because
problems at the same difficulty level as (2). Our task is to               we are unable to access vLLM in our machine, and it is known that
                                                                           the inference without vllm will lead to slight drop of the model’s
query the LLM to generate Lean4 proofs for MiniF2F prob-                   capability
lems based on their formal statements and NL descriptions.                     3
                                                                                 This explains why we exclude RMaxTS for DeepSeek-Prover-
To minimize computational overhead, imports are manually                   v1.5, as its smallest disclosed sample budget (1 × 3200) is not a
configured.                                                                comparable result to our baselines.
                                                                               4
    1
                                                                                 The high evaluation cost is due to accelerated inference meth-
      Although DeepSeek-Prover-v1.5 declared that they applied             ods like vLLM being unable to fit our machine
MiniF2F-Valid for training, yet its performance does significantly             5
                                                                                 Because we don’t need to pass a correct proof to the corrector,
differentiate from other methods. Thus, we still keep this baseline.       two rounds of correction are approximately the same as one round
                                                                           of whole-proof generation


                                                                       6
      MA-LoT: Model-Collaboration Lean-based Long Chain-of-Thought Reasoning enhances Formal Theorem Proving

                            Method                        Model size   Sample budget       MiniF2F-Valid   MiniF2F-Test   Average
        Tree-search Methods
               ReProver (Yang et al., 2024b)                229M                 -               -            26.5%           -
              Llemma (Azerbayev et al., 2023)                34B           1 × 32 × 100       27.9%           25.8%       26.85%
             Expert Iteration (Polu et al., 2022)           837M            8 × 8 × 512       41.2%           36.6%        38.9%
                Lean-STaR (Lin et al., 2024)                 7B             64 × 1 × 50         -             46.3%          -
         InternLM2.5-StepProver (Wu et al., 2024a)           7B            2 × 32 × 600       56.0%           50.7%       53.35%
        Whole-proof generation
            GPT-4-Turbo (Achiam et al., 2023)               > 1T                              25.41%         22.95%       24.18%
            DeepSeek-Math (Shao et al., 2024)                7B                               25.80%         24.60%       25.20%
            Gemini-1.5-pro (Reid et al., 2024)                -                               29.92%         27.87%       28.90%
                                                                            pass@128
            TheoremLlama (Wang et al., 2024)                 8B                               38.52%         35.66%       37.66%
        DeepSeek-Prover-v1.5-RL (Xin et al., 2024b)          7B                               54.10%         48.36%       51.23%
              STP-Lean (Dong & Ma, 2025)                     7B                                  -           56.15%          -
              Godel-Prover (Lin et al., 2025)                7B              pass@32             -           55.33%          -
              DeepSeek-V3 (Liu et al., 2024)                685B             pass@32             -           33.61%          -
        Ours
           DeepSeek-Prover + LoT (whole-proof)                              pass@128          62.70%         52.05%       57.42%
               DeepSeek-Prover + MA-LoT                                    64 + 32 × 2        64.34%         54.51%       59.22%
            Godel-Prover + LoT (whole-proof)                   7B            pass@32             -           57.79%          -
                Godel-Prover + MA-LoT                                       16 + 8 × 2           -           61.07%          -
                       MA-LoT                                               cumulative        65.98%         63.93%       64.96%

Table 1. Main experimental results of MA-LoT. Our results are presented as Base model + method. The LoT (whole-proof) indicates
using the whole-proof results of our LoT-Solver model, and MA-LoT indicates the result of our whole pipeline. The sampling budget
x + k × y in the MA-LoT framework indicates we first perform x whole-proof writing using the prover model and k rounds of correction
using the corrector model. In practice, one round of correction costs approximately half of the whole-proof generation budget, resulting in
y = 12 x.

                                                                            the experiment process.
          Method           Prover    round 1   round 2   round 3
      DS-Prover-v1.5       51.64%    53.28%    54.51%    55.33%
                                                                            3.3. Results
     Godel-Prover-SFT      54.92%    59.43%    61.07%    61.89%
    Prover as Corrector    54.92%    56.15%    57.38%       -
                                                                            Table 1 presents our main results, showing that MA-LoT
                                                                            achieves 61.07% accuracy rate on MiniF2F-Test benchmark
Table 2. Results from multiple rounds of correction using                   and 57.79% for LoT-Solver using whole-proof generation.
DeepSeek-Prover and Godel-Prover as base models, along with                 After the enhancement of MA-LoT, we achieve 10.37%
the outcomes of using the prover to perform correction.                     on Godel-Prover and 12.72% on DeepSeek-Prover on the
                                                                            MiniF2F-Test benchmark. This significant and uniform
                                                                            improvement of our framework indicates its effectiveness.
                                                                            Detailed analysis also shows that our models can solve IMO
                      Method                      MiniF2F-Test
                                                                            and AIME problems that previous models struggled with.
    DeepSeek-Prover-v1.5-SFT (base model)            46.31%                 Our model surpasses state-of-the-art tree-search (InternLM-
        LoT-Solver witch-off Long CoT                49.18%
                                                                            2.5) and whole-proof generation (Godel-Prover) baselines,
     w/o Long CoT training (on RL model)             48.36%
           base model + Long CoT                     46.72%                 demonstrating that our proposed model-collaboration frame-
        base model + Long CoT + SFT                  50.00%                 work based on Long CoT excels in formal theorem proving.
                   LoT-Solver                        51.64%                 MA-LoT outperforms all tree-search baselines by at least
                                                                            20.45% because its prover model constructs proofs with
Table 3. Ablation study result in pass@64 under DeepSeek-Prover             high-level NL planning using emergent Lean Long CoT
as base model.
                                                                            reasoning capability. This indicates our prover model can
                                                                            leverage LLMs’ strong NL reasoning ability in its Long CoT,
                                                                            which leads to more comprehensive proofs. Additionally,
        Method            Godel-Prover-SFT     MA-LoT-Godel                 MA-LoT surpasses whole-proof generation baselines by at
    Sample budget              pass@32            16 + 2 × 8                least 10.37%, as its corrector model analyzes, reflects, and
    Avg. tokens gen             492.10              657.54                  reformulates proofs based on Lean4 executor feedback in
     MiniF2F-Test               58.20%             61.07%                   Long CoT. The strong performance also demonstrates the ef-
                                                                            fectiveness of our ideas of integrating FL verification in NL
           Table 4. Long CoT efficiency study result.


                                                                       7
      MA-LoT: Model-Collaboration Lean-based Long Chain-of-Thought Reasoning enhances Formal Theorem Proving

Long CoT reasoning with its emergent capability. Notably,            3.5. Long CoT Efficiency Study
the DeepSeek-Prover + MA-LoT is based on DeepSeek-
                                                                     To further study the property of Long CoT, we perform
Prover-v1.5-SFT; it outperforms its RL-trained variant by
                                                                     this experiment to test whether MA-LoT is able to search
6.15%. This suggests that our model-collaboration frame-
                                                                     for the answer more efficiently. In this experiment, we
work and Lean-based Long CoT methodology align more
                                                                     measure the GPU hours as well as the tokens generated in
naturally with formal theorem proving than RL alone.
                                                                     both MA-LoT and the base model. We observed that the
The comparison between LoT (whole-proof) and MA-LoT                  MA-LoT generated 33% additional tokens and costs 70%
further highlights the importance of our model-collaboration         additional GPU hours compared to the base model. Thus, to
framework. We observe a 2.46% improvement by reallo-                 make a fair comparison in the sense of computation hours,
cating the computation resources from the prover model,              we enlarge the base model’s sample budget to 1.7 times
which performs more whole-proof generation, to the cor-              in this experiment; the results are presented in the Tab. 4.
rector model, which analyzes and refines proofs based on             The table shows that despite having a smaller sampling
Lean executor feedback. This validates the necessity of a            budget, MA-LoT still outperforms the base model by 4.93%,
model-collaboration system over relying solely on a prover           which indicates that MA-LoT is a better way to allocate
model. In summary, these results confirm that Long CoT               computation power.
reasoning, combined with formal verification and a model-
collaboration paradigm, enhances the discovery of non-               3.6. Ablation Study
trivial and in-depth proofs, thereby validating the effec-
tiveness of our proposed method.                                     To show the effectiveness of each component of our LoT-TL
                                                                     training pipeline, we conduct this thorough ablation study.
3.4. Corrector study                                                 We demonstrate that the elements in LoT-TL pipeline work
                                                                     synergistically to strengthen the model’s formal theorem-
To assess the impact of the correct model in MA-LoT, we              proving capability through integrating FL in Long CoT. We
present the cumulative accuracy on the MiniF2F-Test across           use DeepSeek-Prover-v1.5-SFT as our base model and apply
different rounds of correction in Table 2 for two of our base        the pass@64 accuracy rate on the whole-proof generation
models. The prover column presents the pass@64 (or 16)               method for this set of experiments. The results are presented
accuracy rate of the prover model in whole-proof genera-             in Table 3.
tion, while Round-i columns indicate successive correction
rounds. The results indicate that during the first three cor-        3.6.1. E FFECT OF T RAINING S TAGES
rection rounds, the corrector model successfully corrects
an average of 11.55% theorems that the prover cannot an-             We evaluate training progression by measuring performance
swer. Our analysis shows that most corrected proofs belong           across key intermediate models, namely base model, base
to IMO, AIME, and high-level MATH problems, which                    model + Long CoT, and base model + Long CoT + SFT, as
are particularly difficult for prior models. Such additional         shown in Table 3. Results indicate that training solely on NL
solved problems highlight the corrector’s ability to analyze         CoT data provides minimal improvement. It suggests that
feedback from the Lean4 executor feedback using emergent             the model lacks field-specific information to finish a com-
Lean capability in Long CoT to discover non-trivial proofs.          prehensive Lean4 proof under pure general NL Long CoT
The case study for the analysis and regeneration of new              training. However, incorporating SFT data with the LoT-
proofs can be found in Section 3.7 and Appendix E.                   TL training method yields a marked improvement, demon-
                                                                     strating the effectiveness of transfer learning in equipping
Additionally, to validate the effectiveness of the expert cor-       models with Lean4 Long CoT capabilities. Interestingly, al-
rector, we conducted an experiment that used prover to               though it is not designed for whole-proof writing, additional
perform corrections. In particular, we apply the LoT-Solver          training with correction data further enhances the perfor-
based on Goedel-Prover-SFT. We add the wrong Lean4                   mance. This improvement likely arises from the model’s
proof and error message as a comment in the Lean4 code               development of self-analysis capabilities in Lean4 code,
block and ask the prover to correct it. Results are shown in         allowing it to avoid potentially wrong solutions.
the last row of Table 2. It shows a clear drop in performance
in both correction rounds. This drop is because the prover           3.6.2. S WITCH - OFF L ONG C OT
model tends to directly repeat the wrong proof instead of
using the Long CoT to analyze the error and correct the              This experiment shows that the strong FL reasoning power
proof. This experiment shows the importance of an expert             of LoT-Solver comes from the emergent formal reasoning
corrector model, further validating the effectiveness of our         ability in Long CoT, rather than trivially stacking more
idea of using FL as a backbone for Long CoT in NL.                   data. It uses our LoT-Solver model to write Lean4 proofs
                                                                     directly using the code completion method without Long
                                                                     CoT. We find the performance drop from 51.64% to 49.18%

                                                                 8
      MA-LoT: Model-Collaboration Lean-based Long Chain-of-Thought Reasoning enhances Formal Theorem Proving

because the model does not take an explicit high-level plan          reasoning and multi-round thinking in Long CoT.
in Long CoT, making it unable to finish some questions in
the induction field.                                                 4.2. LLM Collaboration

3.6.3. A BLATION OF L ONG C OT                                       Traditional RL methods offer a training method solution for
                                                                     general reasoning and decision-making processes, but often
To validate the quality of integration between NL and FL             suffer from low sample efficiency and generalization prob-
in Long CoT, we fine-tune the DeepSeek-Prover-v1.5-RL                lems (Pourchot & Sigaud, 2018). With the fast-developing
model directly using our SFT dataset without Long CoT                reasoning and instruction-following ability of LLMs, many
reasoning. We can find that the performance of w/o Long              researchers began to separate the cognition task for a sin-
CoT model (48.36%) is lower than LoT-Solver (51.64%).                gle LLM (Wang et al., 2022; Ma et al., 2024). The pri-
The results confirm that Long CoT plays a crucial role in            mary method for the separation of tasks is to design special
Lean4 theorem proving, offering structured reasoning that            prompts and in-context examples to let LLMs interact with
outperforms a direct RL-based additional data fine-tuned             the outsourcing tools using actionable responses (Xie et al.,
model.                                                               2023; Yang et al., 2023). Further efforts were made to apply
                                                                     specialized training to enhance their field-specific capabil-
3.7. Case Study                                                      ities (Xu et al., 2023; Reed et al., 2022). In the context of
                                                                     formal reasoning, most tree-search methods (Yang et al.,
This section presents the general results of case studies of
                                                                     2024b; Lin et al., 2024; Wu et al., 2024a) apply an LLM
the MA-LoT framework. Due to the limited space, we
                                                                     to continuously query the executor and receive feedback
leave detailed examples in Appendix E. From the examples,
                                                                     to further refine the proof. Because of the huge difference
we can observe a clear collaboration between models. The
                                                                     between FL and NL, such methods are unable to provide a
prover can use a high-level plan to prove advanced MATH
                                                                     high-level analysis of the problem and provide a structured
theorems, and the corrector can analyze the feedback from
                                                                     response.
the Lean executor to formulate a correct proof of an IMO-
level problem. The content in Long CoT also demonstrates
the formal reasoning abilities that emerge from our LoT-             5. Conclusion
TL training pipeline in both prover and corrector. These
                                                                     This paper introduces MA-LoT, a comprehensive model-
observations qualitatively validate the model-collaboration
                                                                     collaboration framework for formal theorem proving that
system’s design and emergence of formal reasoning ability
                                                                     leverages Lean-based Long Chain-of-Thought (CoT) reason-
in Long CoT, demonstrating its ability to combine high-level
                                                                     ing. MA-LoT separate high-level proof planning from fine-
planning with iterative refinement in Lean-based Long CoT.
                                                                     grained correction, overcoming limitations of single-model
                                                                     approaches that either fail to harness LLMs’ NL reasoning
4. Related Work                                                      capability or lack integration with formal feedback. By coor-
                                                                     dinating a prover and a corrector model through Long CoT,
4.1. Lean4 Theorem Proving using LLMs
                                                                     MA-LoT produces more structured, coherent, and insight-
The application of LLMs for FL proving has been a hot                ful proofs. To support this framework, we introduce LoT-TL
topic for study in recent years. The tree-search including           training-inference pipeline. This pipeline enables LLMs
works represented by Expert Iteration (Polu et al., 2022), Re-       to develop domain-specific Long CoT reasoning capabil-
Prover (Yang et al., 2024b), Lean-Star (Lin et al., 2024), and       ity through transfer learning without requiring specifically
InternLM-Step-Prover (Wu et al., 2024b). This direction              annotated Lean Long CoT data. We conduct extensive ex-
does not take full consideration of the LLMs’ NL reason-             periments on the MiniF2F benchmark, where the MA-LoT
ing ability and costs exponentially increasing computation           achieves 61.07% accuracy, surpassing all baselines, includ-
power. Another direction treats formal languages as code             ing both tree-search and whole-proof generation methods.
and asks the LLMs to do the whole-proof generation without           These results highlight the value of combining formal veri-
interaction with the Lean executor to fully use the NL reason-       fication with structured and iterative Long CoT reasoning.
ing ability of LLMs. Significant works includes DeepSeek-            Beyond theorem proving, LoT-TL we proposed offers a
Prover (Xin et al., 2024b;a), TheoremLlama (Wang et al.,             general method for enabling Long CoT reasoning in other
2024), and Llemma (Azerbayev et al., 2023). Works in                 specialized domains without expensive RL or data annota-
this direction tend to overlook the verification signals from        tion. Additionally, the success of the model-collaboration
Lean executors or do not thoroughly think about the error            Long CoT in Lean4 suggests broader applications of for-
messages. Although there is some early work (First et al.,           mal verification for enhancing structured reasoning across
2023; Zheng et al., 2023) that tries to combine both models,         diverse fields.
it did not perform well because of the lack of thorough NL


                                                                 9
      MA-LoT: Model-Collaboration Lean-based Long Chain-of-Thought Reasoning enhances Formal Theorem Proving

Impact statement                                                      References
This paper presents work whose goal is to advance the for-            Achiam, J., Adler, S., Agarwal, S., Ahmad, L., Akkaya, I.,
mal theorem proving using LLMs. The potential social im-                Aleman, F. L., Almeida, D., Altenschmidt, J., Altman, S.,
pact is majorly in the field of education. With the increasing          Anadkat, S., et al. Gpt-4 technical report. arXiv preprint
number of formal languages used in graduate-level educa-                arXiv:2303.08774, 2023.
tion, a more advanced formal theorem proving model may
                                                                      Azerbayev, Z., Schoelkopf, H., Paster, K., Santos, M. D.,
result in educators being unable to distinguish the model-
                                                                        McAleer, S., Jiang, A. Q., Deng, J., Biderman, S., and
generated results and student writing results. Despite the
                                                                       Welleck, S. Llemma: An open language model for math-
societal consequences of improving formal reasoning sys-
                                                                        ematics. arXiv preprint arXiv:2310.10631, 2023.
tems, specific discussions of ethical concerns are still too
early at this stage.                                                  De Moura, L., Kong, S., Avigad, J., Van Doorn, F., and von
                                                                        Raumer, J. The lean theorem prover (system description).
                                                                        In Automated Deduction-CADE-25: 25th International
                                                                        Conference on Automated Deduction, Berlin, Germany,
                                                                        August 1-7, 2015, Proceedings 25, pp. 378–388. Springer,
                                                                        2015.

                                                                      Dong, K. and Ma, T. Beyond limited data: Self-play llm
                                                                        theorem provers with iterative conjecturing and proving.
                                                                        arXiv preprint arXiv:2502.00212, 2025.

                                                                      First, E., Rabe, M. N., Ringer, T., and Brun, Y. Baldur:
                                                                        Whole-proof generation and repair with large language
                                                                        models. In Proceedings of the 31st ACM Joint European
                                                                        Software Engineering Conference and Symposium on the
                                                                        Foundations of Software Engineering, pp. 1229–1241,
                                                                        2023.

                                                                      Frieder, S., Bayer, J., Collins, K. M., Berner, J., Loader, J.,
                                                                        Juhász, A., Ruehle, F., Welleck, S., Poesia, G., Griffiths,
                                                                        R.-R., et al. Data for mathematical copilots: Better ways
                                                                        of presenting proofs for machine learning. arXiv preprint
                                                                        arXiv:2412.15184, 2024.

                                                                      Harrison, J. Hol light: An overview. In International
                                                                        Conference on Theorem Proving in Higher Order Logics,
                                                                        pp. 60–66. Springer, 2009.

                                                                      Hendrycks, D., Burns, C., Kadavath, S., Arora, A., Basart,
                                                                        S., Tang, E., Song, D., and Steinhardt, J. Measuring math-
                                                                        ematical problem solving with the math dataset. arXiv
                                                                        preprint arXiv:2103.03874, 2021.

                                                                      Jiang, A. Q., Li, W., Han, J. M., and Wu, Y. Lisa: Language
                                                                         models of isabelle proofs. In 6th Conference on Artificial
                                                                         Intelligence and Theorem Proving, pp. 378–392, 2021.

                                                                      Jiang, A. Q., Welleck, S., Zhou, J. P., Li, W., Liu, J., Jamnik,
                                                                         M., Lacroix, T., Wu, Y., and Lample, G. Draft, sketch,
                                                                         and prove: Guiding formal theorem provers with informal
                                                                         proofs. arXiv preprint arXiv:2210.12283, 2022.

                                                                      Kumarappan, A., Tiwari, M., Song, P., George, R. J.,
                                                                       Xiao, C., and Anandkumar, A. Leanagent: Lifelong
                                                                        learning for formal theorem proving. arXiv preprint
                                                                        arXiv:2410.06209, 2024.

                                                                 10
      MA-LoT: Model-Collaboration Lean-based Long Chain-of-Thought Reasoning enhances Formal Theorem Proving

Lin, H., Sun, Z., Yang, Y., and Welleck, S. Lean-star: Learn-         Reid, M., Savinov, N., Teplyashin, D., Lepikhin, D., Lilli-
  ing to interleave thinking and proving. arXiv preprint                crap, T., Alayrac, J.-b., Soricut, R., Lazaridou, A., Firat,
  arXiv:2407.10040, 2024.                                               O., Schrittwieser, J., et al. Gemini 1.5: Unlocking multi-
                                                                        modal understanding across millions of tokens of context.
Lin, Y., Tang, S., Lyu, B., Wu, J., Lin, H., Yang, K., Li,              arXiv preprint arXiv:2403.05530, 2024.
  J., Xia, M., Chen, D., Arora, S., and Jin, C. Goedel-
  prover: A frontier model for open-source automated the-             Shao, Z., Wang, P., Zhu, Q., Xu, R., Song, J., Bi, X., Zhang,
  orem proving, 2025. URL https://arxiv.org/                            H., Zhang, M., Li, Y., Wu, Y., et al. Deepseekmath: Push-
  abs/2502.07640.                                                       ing the limits of mathematical reasoning in open language
                                                                        models. arXiv preprint arXiv:2402.03300, 2024.
Liu, A., Feng, B., Xue, B., Wang, B., Wu, B., Lu, C., Zhao,
  C., Deng, C., Zhang, C., Ruan, C., et al. Deepseek-v3               Wang, R., Jansen, P., Côté, M.-A., and Ammanabrolu, P.
  technical report. arXiv preprint arXiv:2412.19437, 2024.             Scienceworld: Is your agent smarter than a 5th grader?
                                                                       arXiv preprint arXiv:2203.07540, 2022.
Ma, C., Zhang, J., Zhu, Z., Yang, C., Yang, Y., Jin, Y.,
 Lan, Z., Kong, L., and He, J. Agentboard: An analytical              Wang, R., Zhou, W., and Sachan, M. Let’s synthesize step
 evaluation board of multi-turn llm agents. arXiv preprint             by step: Iterative dataset synthesis with large language
 arXiv:2401.13178, 2024.                                               models by extrapolating errors from small models. arXiv
                                                                       preprint arXiv:2310.13671, 2023.
Moura, L. d. and Ullrich, S. The lean 4 theorem prover
                                                                      Wang, R., Zhang, J., Jia, Y., Pan, R., Diao, S., Pi, R., and
 and programming language. In Automated Deduction–
                                                                       Zhang, T. Theoremllama: Transforming general-purpose
 CADE 28: 28th International Conference on Automated
                                                                       llms into lean4 experts. arXiv preprint arXiv:2407.03203,
 Deduction, Virtual Event, July 12–15, 2021, Proceedings
                                                                       2024.
 28, pp. 625–635. Springer, 2021.
                                                                      Wei, J., Wang, X., Schuurmans, D., Bosma, M., Xia, F., Chi,
Newell, A. and Simon, H. The logic theory machine–a com-
                                                                       E., Le, Q. V., Zhou, D., et al. Chain-of-thought prompting
  plex information processing system. IRE Transactions
                                                                       elicits reasoning in large language models. Advances in
  on information theory, 2(3):61–79, 1956.
                                                                       neural information processing systems, 35:24824–24837,
Open-Source-O1. Open-o1, 2024. URL https://                            2022.
  github.com/Open-Source-O1/Open-O1. Ac-                              Wu, Z., Huang, S., Zhou, Z., Ying, H., Wang, J., Lin, D., and
  cessed: 2024-12-28.                                                  Chen, K. Internlm2. 5-stepprover: Advancing automated
                                                                       theorem proving via expert iteration on large-scale lean
OpenAI.             Learning    to reason with
                                                                       problems. arXiv preprint arXiv:2410.15700, 2024a.
  llms.           https://openai.com/index/
  learning-to-reason-with-llms/, September                            Wu, Z., Wang, J., Lin, D., and Chen, K. Lean-github:
 13 2024. Accessed: 2024-11-24.                                        Compiling github lean repositories for a versatile lean
                                                                       prover. arXiv preprint arXiv:2407.17227, 2024b.
Paulson, L. C. Isabelle: A generic theorem prover. Springer,
  1994.                                                               Xie, T., Zhou, F., Cheng, Z., Shi, P., Weng, L., Liu, Y., Hua,
                                                                        T. J., Zhao, J., Liu, Q., Liu, C., et al. Openagents: An
Polu, S. and Sutskever, I. Generative language model-                   open platform for language agents in the wild. arXiv
  ing for automated theorem proving. arXiv preprint                     preprint arXiv:2310.10634, 2023.
  arXiv:2009.03393, 2020.
                                                                      Xin, H., Guo, D., Shao, Z., Ren, Z., Zhu, Q., Liu, B., Ruan,
Polu, S., Han, J. M., Zheng, K., Baksys, M., Babuschkin, I.,            C., Li, W., and Liang, X. Deepseek-prover: Advancing
  and Sutskever, I. Formal mathematics statement curricu-               theorem proving in llms through large-scale synthetic
  lum learning. arXiv preprint arXiv:2202.01344, 2022.                  data. arXiv preprint arXiv:2405.14333, 2024a.
Pourchot, A. and Sigaud, O. Cem-rl: Combining evolution-              Xin, H., Ren, Z., Song, J., Shao, Z., Zhao, W., Wang, H., Liu,
  ary and gradient-based methods for policy search. arXiv               B., Zhang, L., Lu, X., Du, Q., et al. Deepseek-prover-v1.
  preprint arXiv:1810.01222, 2018.                                      5: Harnessing proof assistant feedback for reinforcement
                                                                        learning and monte-carlo tree search. arXiv preprint
Reed, S., Zolna, K., Parisotto, E., Colmenarejo, S. G.,                 arXiv:2408.08152, 2024b.
  Novikov, A., Barth-Maron, G., Gimenez, M., Sulsky,
  Y., Kay, J., Springenberg, J. T., et al. A generalist agent.        Xu, Y., Su, H., Xing, C., Mi, B., Liu, Q., Shi, W., Hui, B.,
  arXiv preprint arXiv:2205.06175, 2022.                                Zhou, F., Liu, Y., Xie, T., et al. Lemur: Harmonizing

                                                                 11
     MA-LoT: Model-Collaboration Lean-based Long Chain-of-Thought Reasoning enhances Formal Theorem Proving

  natural language and code for language agents. arXiv
  preprint arXiv:2310.06830, 2023.
Yang, H., Yue, S., and He, Y. Auto-gpt for online decision
  making: Benchmarks and additional opinions. arXiv
  preprint arXiv:2306.02224, 2023.
Yang, K., Poesia, G., He, J., Li, W., Lauter, K., Chaudhuri,
  S., and Song, D. Formal mathematical reasoning: A new
  frontier in ai. arXiv preprint arXiv:2412.16075, 2024a.
Yang, K., Swope, A., Gu, A., Chalamala, R., Song, P.,
  Yu, S., Godil, S., Prenger, R. J., and Anandkumar, A.
  Leandojo: Theorem proving with retrieval-augmented
  language models. Advances in Neural Information Pro-
  cessing Systems, 36, 2024b.
Ying, H., Wu, Z., Geng, Y., Wang, J., Lin, D., and Chen,
  K. Lean workbook: A large-scale lean problem set for-
  malized from natural language math problems. arXiv
  preprint arXiv:2406.03847, 2024.

Zheng, C., Wang, H., Xie, E., Liu, Z., Sun, J., Xin, H.,
  Shen, J., Li, Z., and Li, Y. Lyra: Orchestrating dual
  correction in automated theorem proving. arXiv preprint
  arXiv:2309.15806, 2023.

Zheng, K., Han, J. M., and Polu, S. Minif2f: a cross-system
  benchmark for formal olympiad-level mathematics. arXiv
  preprint arXiv:2109.00110, 2021.




                                                               12
     MA-LoT: Model-Collaboration Lean-based Long Chain-of-Thought Reasoning enhances Formal Theorem Proving

A. Term chart                                                                     Training Steps             MiniF2F-Test
To make the reader better understand the terms, we pro-                            125 Steps                     32.79%
vide this chart that explains every term, abbreviation, and                        250 Steps                     35.25%
corresponding tool in detail.                                                     1,250 Steps                    45.08%
                                                                                  2,500 Steps                    47.54%
                                                                           13,616 Steps (full training)          51.64%
 1. NL (Natural Language): Refers to language that hu-
    mans use in our daily life, often unable to perform            Table 5. MiniF2F-Test result on different data-scale trained models
    auto-verification.

 2. FL (Formal Language): A structured and mathemati-              B. Examples for tree-search and whole-proof
    cally precise representation of logic and proofs, which           generation
    ensures rigorous verification and eliminates ambigui-
    ties present in NL reasoning.                                  Following Section 2.1, we present the input-output example
                                                                   for tree-search method and whole-proof generation method
 3. Lean4: A functional programming language and in-               here.
    teractive theorem prover developed for formalizing             Example for whole-proof generation:
    mathematics and verifying proofs.
                                                                   ### Input Example
                                                                   Complete the following Lean 4 code:
 4. Lean Executor: The built-in proof verification engine          theorem algebra_sqineq_unitcircatbpamblt1
    of Lean4. It evaluates proof steps, checks for correct-          (a b: R)
    ness, and ensures that every logical inference follows           (h0 : aˆ2 + bˆ2 = 1) :
    strict formal verification rules.                                a * b + (a - b) ≤ 1 := by
                                                                   ### Output Example
                                                                     -- We have that (a - b - 1)ˆ2 ≥ 0.
 5. Long CoT (Long Chain-of-Thought): The reasoning                  have h1 : 0 ≤ (a - b - 1) ˆ 2 :=
    structure provided by OpenAI-O1 (OpenAI, 2024) that                sq_nonneg _
    performs long and detailed thinking before making the            -- By expanding, we have:
    final output. Different from standard CoT, Long CoT              -- 0 ≤ aˆ2 -ab-a-ab+bˆ2 +b-a+b+1.
    allows for multi-step logical reasoning before proof             linarith [h0 , sub_add_cancel a b]
    generation, reflection, and iterative refinement from
    self-check of Lean4 feedback.                                  Example for tree-search method:
                                                                   ### Input Example
 6. MA-LoT (Model-CollAboration Lean-based Long                    DECL MyNat.mul_pow
    Chain-of-Thought framework): Our proposed model-               GOAL a b n : N
                                                                   ⊢ (a * b) ˆ n = a ˆ n * b ˆ n
    collaboration framework for formal theorem proving.            ### Output Example
                                                                   PROOFSTEP induction n with t Ht
 7. LoT-TL (LoT-Transfer Learning): The transfer learn-
    ing pipeline we propose to enable LLMs with Lean4
    Long CoT capability without the need for a specially           C. Scaling Law Study
    annotated dataset.
                                                                   We conduct an additional experiment to investigate whether
 8. LoT-Solver: The model we train through LoT-TL                  our model adheres to scaling laws by evaluating its perfor-
    pipeline that serves both as prover and corrector. It          mance across varying training dataset scales. Specifically,
    is a high-standard Lean4 theorem proving model with            we train the model with four distinct step sizes (125, 250,
    Long CoT capability to control the type of cognition           1250, and 2500 steps) under a fixed batch size of 4 and
    task and enhance formal thinking.                              evaluate its accuracy on the MiniF2F-Test benchmark using
                                                                   the Long Chain-of-Thought (CoT) format. The resulting
 9. LoT-PD & LoT-CD (LoT-ProveData) & (LoT-                        accuracy rates are presented in Table 5. To analyze these
    CorrectionData): The LoT-PD is a dataset containing            results, we plot the relationship between log-scaled training
    verified Lean4 theorem proofs and NL statement and             steps and model accuracy in Figure 3. A linear approxima-
    proof. Its main function is to provide basic capability        tion of the data yields a strong coefficient of determination
    for the prover. The LoT-CD is a dataset containing             (R2 = 0.9664), indicating a near-linear improvement in
    incorrect error messages and correct Lean4 proofs to-          performance as training steps increase logarithmically. This
    gether with NL annotations. It mainly provides the             aligns with the predictions of scaling laws, suggesting that
    capability for the prover model to refine proofs.              our approach benefits significantly from larger-scale train-

                                                              13
                    MA-LoT: Model-Collaboration Lean-based Long Chain-of-Thought Reasoning enhances Formal Theorem Proving

                                     Scaling Law Study
                  0.55

                                                    y = 0.0998x + 0.1235
                                                         R² = 0.9664
                   0.5
  Accuracy Rate




                  0.45



                   0.4



                  0.35



                   0.3
                         2.1   2.6            3.1              3.6         4.1
                                      Log-Scale Training Steps


Figure 3. Log-scale training steps and accuracy rate on MiniF2F
of trained model. The dashed line is a linear regression approxima-
tion.


ing. Our findings further highlight the potential for enhanced
performance with expanded resources to annotate additional
Lean4 data.

D. ProofNet result
We perform a small-scale baseline comparison on the
ProofNet benchmark using the Goedel-Prover-SFT and MA-
LoT(Goedel), where MA-LoT achieves 15.47% of accuracy
rate under 16+16 metric while the original Goedel-Prover is
12.15% under pass@32. The relatively low performance of
both models is that Goedel-Prover does not fit the ProofNet
well as reported in Lin et al. (2025). However, we can still
see the improvement of our method compared to the base-
line, indicating MA-LoT’s effectiveness is not constrained
to the baseline.

E. Case studies
We present two case studies in Appendix E.1 and E.2. We
can see that the model-collaboration framework can write a
more coherent and well-structured proof by making a high-
level NL plan and executing such a plan in the prover. The
corrector can analyze the unsolved goals, make plans for
correction, and write correct proof. This is achieved by our
proposed training procedure.




                                                                                 14
      MA-LoT: Model-Collaboration Lean-based Long Chain-of-Thought Reasoning enhances Formal Theorem Proving

E.1. Prover analysis
This is an example of a prover-generated result, in which we can see that the prover model learns to write a high-level proof
plan in the Long CoT and details execute the plan when writing the Lean4 code

### Provided Long CoT Header
<Thought>
Alright, I should do the following:
   1. Provide the natural language analysis for the theorem based on the Natural
     ,→     language theorem statement.
    2. Draft the Lean4 tactics I should use to solve the problem
    3. Write the output Lean4 code.
The user also asks that I should avoid using the keyword `sorry` to give up the
 ,→     proof, so I will not write it in my Lean4 code.
### Generated results:
The `mathd_numbertheory_458` can be proofed by leveraging the properties of
 ,→     modular arithmetic. Specifically, we know that if `n % 8 = 7`, then `n` can
 ,→     be expressed as `n = 8k + 7` for some integer `k`. We need to find `n % 4`.
First, observe that `n % 8 = 7` implies `n = 8k + 7`. Since `8k` is divisible by
 ,→     `4`, we only need to consider the remainder when `7` is divided by `4`, which
 ,→     is `3`. Therefore, `n % 4 = 3`.
Now, translating this reasoning into Lean4 code, we can use the properties of
 ,→     modular arithmetic to directly derive the result.
</Thought>
<Output>
```lean4
theorem mathd_numbertheory_458 (n : N) (h0 : n % 8 = 7) : n % 4 = 3 := by
    -- We know that n leaves a remainder of 7 when divided by 8.
    have h1 : n % 8 = 7 := h0
    -- We need to find the remainder when n is divided by 4.
    have h2 : n % 4 = 3 := by
        -- Using the fact that 4 divides 8, we can use the modulo operation
         ,→   properties.
        rw [← Nat.mod_mod_of_dvd n (by decide : 4 | 8)]
        -- Simplify the expression using the given remainder when divided by 8.
        simp [h1 ]
    -- Therefore, the remainder when n is divided by 4 is 3.
    exact h2
```&
</Output>

E.2. Corrector analysis
This is an example of error correction that successfully solves an IMO problem, We can see that the model first analyzes the
error message, then makes a proof plan, and then writes a correct proof for another IMO-level problem

### Provided Long CoT Header
<Thought>
Alright, I need to prove the theorem prover_data_68493 using the Lean4 code. Here
 ,→ is my draft of the proof:

```lean4
theorem imo_1983_p6
  (a b c : R)
  (h0 : 0 < a ∧ 0 < b ∧ 0 < c)

                                                             15
    MA-LoT: Model-Collaboration Lean-based Long Chain-of-Thought Reasoning enhances Formal Theorem Proving

  (h1 : c < a + b)
  (h2 : b < a + c)
  (h3 : a < b + c) :
  0 ≤ aˆ2 * b * (a - b) + bˆ2 * c * (b - c) + cˆ2 * a * (c - a) := by
  /-
  To prove that \( aˆ2 b(a - b) + bˆ2 c(b - c) + cˆ2 a(c - a) \geq 0 \) for
   ,→     positive real numbers \( a \), \( b \), and \( c \) satisfying certain
   ,→     conditions related to being part of a triangle, we can proceed as follows:
  1. **Nonlinear Arithmetic**: Utilize nonlinear arithmetic (`nlinarith`) to
   ,→    verify inequalities involving squares and products of differences between
   ,→    variables. These operations inherently handle cases where expressions might
   ,→     not hold due to cancellation or sign changes.
  Equality holds if all pairwise differences among \( a \), \( b \), and \( c \)
   ,→     become zero simultaneously. However, since they must satisfy strict
   ,→     positivity constraints imposed by `triangle`, such an eventuality cannot
   ,→     occur under normal circumstances unless specified otherwise. Nonetheless,
   ,→    within the confines of algebraic manipulation without additional
   ,→     constraints beyond those provided, no immediate contradictions arise
   ,→     regarding potential zeros leading to equality.
  -/
  -- Introduce intermediate hypotheses ensuring divisibility properties do not
   ,→     disrupt expected behavior.
  have ha' : True := trivial
  have hb' : True := trivial
  have hc' : True := trivial
  -- Employ nonlinear arithmetic to iteratively check for inequalities involving
   ,→     sums and products of our main variables and constants.
  repeat' nlinarith [mul_pos h0 .1 h0 .2.1, mul_pos h0 .2.1 h0 .2.2, mul_pos h0 .2.2
   ,→     h0 .1,
      sub_self a, sub_self b, sub_self c, add_sub_cancel'_right a b,
       ,→    add_sub_cancel'_right b c,
      add_sub_cancel'_right c a, mul_nonneg (ha'.le) (hb'.le), mul_nonneg (hb'.le)
       ,→    (hc'.le),
      mul_nonneg (hc'.le) (ha'.le)]
```&
Let me test it in Lean4
Emmm, it seems the above proof is wrong.
Let me check the error messages.
OK, Here is the error messages:
```bash
line 13

unsolved goals
a b c : R
h0 : 0 < a ∧ 0 < b ∧ 0 < c
h1 : c < a + b
h2 : b < a + c
h3 : a < b + c
ha' hb' hc' : True
⊢ 0 ≤ a ˆ 2 * b * (a - b) + b ˆ 2 * c * (b - c) + c ˆ 2 * a * (c - a)
```&
So, I will rethink a Lean4 proof following the steps




                                                     16
    MA-LoT: Model-Collaboration Lean-based Long Chain-of-Thought Reasoning enhances Formal Theorem Proving

   1. Provide the natural language analysis for the theorem based on the Natural
     ,→   language theorem statement, Lean4 theorem statement, my previous proof and
     ,→   the error message.
    2. Draft the Lean4 tactics I should use to solve the problem
    3. Write the output Lean4 code.
Let me analysis the wrong Lean4 solution through the error messages.
### Generated results"
The error message indicates that the proof is incomplete.
The error message says:
```
unsolved goals
a b c : R
h0 : 0 < a ∧ 0 < b ∧ 0 < c
h1 : c < a + b
h2 : b < a + c
h3 : a < b + c
ha' hb' hc' : True
⊢ 0 ≤ a ˆ 2 * b * (a - b) + b ˆ 2 * c * (b - c) + c ˆ 2 * a * (c - a)
```&
So, the main issue is that the proof is incomplete, and the final goal `0 ≤ aˆ2 *
 ,→     b * (a - b) + bˆ2 * c * (b - c) + cˆ2 * a * (c - a)` is not being addressed
 ,→     properly.
Therefore, I need to construct a proper proof strategy that addresses all the
 ,→     conditions and goals properly.
First, I need to understand the mathematical structure of the inequality `aˆ2 * b
 ,→    * (a - b) + bˆ2 * c * (b - c) + cˆ2 * a * (c - a)`.
This expression is symmetric in `a`, `b`, and `c`.
Given that `a`, `b`, and `c` are positive real numbers and they satisfy certain
 ,→     conditions related to being part of a triangle (triangle inequalities), I can
 ,→     think about the properties of such expressions.
One approach is to consider the symmetry and positivity of `a`, `b`, and `c`.
Since `a`, `b`, and `c` are sides of a triangle, they satisfy the triangle
 ,→     inequalities:
- `a + b > c`
- `b + c > a`
- `c + a > b`
Additionally, since `a`, `b`, and `c` are positive, we can use properties of real
 ,→     numbers and inequalities to prove the desired result.
Another approach is to use algebraic manipulation or inequalities like AM-GM
 ,→     inequality or Cauchy-Schwarz inequality.
Given the complexity of the expression, perhaps rearranging terms or applying
 ,→     known inequalities could help.
Also, considering the conditions of the triangle, perhaps expressing the
 ,→    variables in terms of each other or using substitution could simplify the
 ,→     problem.
I need to ensure that the final proof is logically sound and does not rely on
 ,→     assumptions that are not justified.
Therefore, I will proceed to construct a revised proof based on these
 ,→     considerations.
Let me proceed with the thought process and output the corrected Lean4 code.
</Thought>

<Output>
```lean4

                                                     17
     MA-LoT: Model-Collaboration Lean-based Long Chain-of-Thought Reasoning enhances Formal Theorem Proving

/-- Let $a$, $b$, and $c$ be the lengths of the sides of a triangle. Prove that
$aˆ2 b(a - b) + bˆ2 c(b - c) + cˆ2 a(c - a) \geq 0$.
-/
theorem imo_1983_p6
  (a b c : R)
  (h0 : 0 < a ∧ 0 < b ∧ 0 < c)
   (h1 : c < a + b)
   (h2 : b < a + c)
   (h3 : a < b + c) :
   0 ≤ aˆ2 * b * (a - b) + bˆ2 * c * (b - c) + cˆ2 * a * (c - a) := by
   -- We will use the fact that the square of any real number is non-negative.
   have h4 : 0 ≤ (a - b)ˆ2 := sq_nonneg (a - b)
   have h5 : 0 ≤ (b - c)ˆ2 := sq_nonneg (b - c)
   have h6 : 0 ≤ (c - a)ˆ2 := sq_nonneg (c - a)
   -- Using these inequalities, we can conclude the desired inequality using
    ,→     non-linear arithmetic.
   nlinarith [mul_pos h0 .1 h0 .2.1, mul_pos h0 .2.1 h0 .2.2, mul_pos h0 .2.2 h0 .1,
       mul_pos (sub_pos.mpr h1 ) (sub_pos.mpr h2 ), mul_pos (sub_pos.mpr h2 )
        ,→   (sub_pos.mpr h3 ),
       mul_pos (sub_pos.mpr h3 ) (sub_pos.mpr h1 )]
```&
</Output>


Another example is demonstrated as follows:


@ Natural language theorem statement:
mathd_algebra_419:
What is the value of $-a-bˆ2+3ab$ if $a=-1$ and $b=5$? Show that it is -39.

@ Lean4 theorem statement:
```lean4
theorem mathd_algebra_419
  (a b : R)
  (h0 : a = -1)
  (h1 : b = 5) :
  -a - bˆ2 + 3 * (a * b) = -39 := by
```&


@ Lean4 theorem statement and proof with explanatory comments preceding each line
 ,→ of code:
### Response:
<Thought>
Okay the user asks me to write Lean4 theorem proof using Long CoT, I should do
 ,→ the following:

  1. Provide the natural language analysis for the theorem based on the Natural
   ,→ language theorem statement.

  2. Draft the Lean4 tactics I should use to solve the problem

  3. Write the output Lean4 code.


                                                      18
   MA-LoT: Model-Collaboration Lean-based Long Chain-of-Thought Reasoning enhances Formal Theorem Proving

The user also asks that I should avoid using the keyword `sorry` to give up the
 ,→ proof, so I will not write it in my Lean4 code.

The natural language analysis for the theorem `mathd_algebra_419` is:

Given a = -1 and b = 5, we need to compute the value of the expression -a - b² +
 ,→ 3ab and show that it equals -39.

The steps to solve this problem are:

1. Substitute a = -1 and b = 5 into the expression.
2. Simplify the expression step by step.
3. Verify that the result is -39.

The Lean4 code for this theorem would involve substituting the given values for a
 ,→ and b into the expression and then simplifying it using algebraic operations.

Now, let's outline the Lean4 code:

The theorem statement is:

theorem mathd_algebra_419
  (a b : R)
  (h0 : a = -1)
  (h1 : b = 5) :
  -a - bˆ2 + 3 * (a * b) = -39 := by

The proof would involve substituting the values of a and b into the expression
 ,→ and simplifying:

First, substitute a = -1 and b = 5 into the expression:

-a - b² + 3ab becomes:

-(-1) - (5)² + 3*(-1)*(5)

Simplify each term:

-(-1) = 1

-(5)² = -25

3*(-1)*(5) = -15

So the expression becomes:

1 - 25 - 15

Now compute the result:

1 - 25 = -24

-24 -15 = -39



                                                    19
    MA-LoT: Model-Collaboration Lean-based Long Chain-of-Thought Reasoning enhances Formal Theorem Proving

Thus, the value of the expression is -39.

Now, let's write the Lean4 code.

The code would start with the theorem statement, then use the `rw` tactic to
 ,→ substitute the values of a and b.

Wait, but in Lean4, we can directly substitute the values into the expression.

So the code would be:

theorem mathd_algebra_419
  (a b : R)
  (h0 : a = -1)
  (h1 : b = 5) :
  -a - bˆ2 + 3 * (a * b) = -39 := by

  rw [h0 , h1 ]
  ring

But wait, let me check. The expression is -a - b² + 3ab. So substituting a = -1
 ,→ and b = 5:

-(-1) - 5² + 3*(-1)*5 = 1 -25 -15 = -39.

Yes, that's correct.

So the code can be written as:

rw [h0 , h1 ]

Then use the `ring` tactic to simplify the expression.

So the complete code would be:

theorem mathd_algebra_419
  (a b : R)
  (h0 : a = -1)
  (h1 : b = 5) :
  -a - bˆ2 + 3 * (a * b) = -39 := by

  rw [h0 , h1 ]
  ring

Alternatively, using the `simp` tactic with the appropriate lemmas.

But in this case, the `ring` tactic is sufficient.

So the code is straightforward.

I should test this code in Lean4 to ensure that it works.

But since the user asked to avoid using `sorry`, I will not write the code.
 ,→ Instead, I will provide the explanation.

                                                     20
      MA-LoT: Model-Collaboration Lean-based Long Chain-of-Thought Reasoning enhances Formal Theorem Proving

</Thought>

<Output>

To solve the problem, we need to evaluate the expression \(-a - bˆ2 + 3ab\) given
 ,→ \(a = -1\) and \(b = 5\), and show that the result is \(-39\).

### Key steps:
1. **Substitute the given values into the expression:**
   - Replace \(a\) with \(-1\) and \(b\) with \(5\).
   - The expression becomes \(-(-1) - (5)ˆ2 + 3(-1)(5)\).

2. **Simplify each term:**
   - \(-(-1) = 1\)
   - \((5)ˆ2 = 25\)
   - \(3(-1)(5) = -15\)

3. **Combine the simplified terms:**
   - \(1 - 25 - 15 = -39\)

### Proof:
```lean4
theorem mathd_algebra_419
  (a b : R)
  (h0 : a = -1)
  (h1 : b = 5) :
  -a - bˆ2 + 3 * (a * b) = -39 := by
  rw [h0 , h1 ]
  ring
```&

### Explanation:
- **Substitution:** The `rw [h0 , h1 ]` tactic replaces \(a\) with \(-1\) and \(b\)
 ,→ with \(5\) in the expression.
- **Simplification:** The `ring` tactic simplifies the expression using algebraic
 ,→ rules, resulting in \(-39\).

This approach ensures that we efficiently and correctly evaluate the expression
 ,→ by substituting the given values and simplifying step-by-step. The final
 ,→ result confirms that the value of the expression is indeed \(-39\).
</Output>

From the example above, we can clearly see the saying of wait, which indicates a rethinking process of the Long CoT. Such
rethinking can help the model to reach conclusion that needs more thorough thinking.

E.3. Theorem only solved by MA-LoT
We have observed that algebra 2varlineareq fp3zeq11 3tfm1m5zeqn68 feqn10 zeq7 is only solved in the MA-LoT setup.
From the original code draft and the error analysis, we can spot that our corrector framework is able to restructure the proof
from the previous left and right cases into direct solving. This indicates our method’s superiority in rethinking based on
formal guidance.

<Thought>
Alright, I need to prove the theorem lean_workbook_plus_68493 using the Lean4
 ,→ code. Here is my draft of the proof:

                                                             21
   MA-LoT: Model-Collaboration Lean-based Long Chain-of-Thought Reasoning enhances Formal Theorem Proving


```lean4
import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Topology Rat
theorem algebra_2varlineareq_fp3zeq11_3tfm1m5zeqn68_feqn10_zeq7
  (f z: C)
  (h0 : f + 3*z = 11)
  (h1 : 3*(f - 1) - 5*z = -68) :
  f = -10 ∧ z = 7 := by
  /-
  Given the equations \( f + 3z = 11 \) and \( 3(f - 1) - 5z = -68 \), we need to
   ,→   show that \( f = -10 \) and \( z = 7 \).
  1. Start by isolating \( f \) from the first equation: \( f = 11 - 3z \).
  2. Substitute \( f = 11 - 3z \) into the second equation: \( 3((11 - 3z) - 1) -
   ,→   5z = -68 \).
  3. Simplify the equation step by step:
       - Distribute the 3: \( 3(10 - 3z) - 5z = -68 \).
       - Distribute the 3 again: \( 30 - 9z - 5z = -68 \).
       - Combine like terms: \( 30 - 14z = -68 \).
  4. Solve for \( z \):
       - Subtract 30 from both sides: \( -14z = -98 \).
       - Divide both sides by -14: \( z = 7 \).
  5. Substitute \( z = 7 \) back into \( f = 11 - 3z \):
       - \( f = 11 - 3(7) \).
       - \( f = 11 - 21 \).
       - \( f = -10 \).
  Thus, we have shown that \( f = -10 \) and \( z = 7 \).
  -/
  constructor
  case left =>
      -- Isolate f from the first equation
      have h2 : f = 11 - 3*z := by linear_combination h0
      -- Substitute f into the second equation
      have h3 : 3*(11 - 3*z - 1) - 5*z = -68 := by rw [h2 ] at h1 ; exact h1
      -- Simplify the equation to solve for z
      have h4 : 30 - 14*z = -68 := by linear_combination h3
      have h5 : -14*z = -98 := by linear_combination h4
      have h6 : z = 7 := by linear_combination h5 / -14
      exact h6
  case right =>
      -- Isolate z from the first equation
      have h2 : z = 7 := by linear_combination h0
      exact h2
```&

Let me test it in Lean4

Emmm, it seems the above proof is wrong.

Let me check the error messages.

                                                    22
   MA-LoT: Model-Collaboration Lean-based Long Chain-of-Thought Reasoning enhances Formal Theorem Proving


OK, Here is the error messages:

```bash
line 39

type mismatch
  h6
has type
  z = 7 : Prop
but is expected to have type
  f = -10 : Prop
```&

```bash
line 42

ring failed, ring expressions not equal
f z : C
h0 : f + 3 * z = 11
h1 : 3 * (f - 1) - 5 * z = -68
⊢ 4 + (-(z * 2) - f) = 0
```&


So, I will rethink a Lean4 proof following the steps

  1. Provide the natural language analysis for the theorem based on the Natural
   ,→ language theorem statement, Lean4 theorem statement, my previous proof and
   ,→ the error message.

  2. Draft the Lean4 tactics I should use to solve the problem

  3. Write the output Lean4 code.

Let me analysis the wrong Lean4 solution through the error messages

The first error says:

line 39: type mismatch

h6 has type z = 7 : Prop but is expected to have type f = -10 : Prop

Wait, in the code, I have two cases: left and right. The left case is supposed to
 ,→ prove f = -10, and the right case z = 7. But in the left case, I derived z =
 ,→ 7 and then tried to use h6 to conclude f = -10, but h6 is z = 7. That's the
 ,→ type mismatch. So, I need to fix that.

The second error is:

line 42: ring failed, ring expressions not equal

f z : C



                                                    23
    MA-LoT: Model-Collaboration Lean-based Long Chain-of-Thought Reasoning enhances Formal Theorem Proving

h0 : f + 3 * z = 11

h1 : 3 * (f - 1) - 5 * z = -68

⊢ 4 + (-(z * 2) - f) = 0

Hmm, this seems like an unrelated expression that Lean is trying to check. Maybe
 ,→ there's a mistake in how I'm handling the substitutions or the algebraic
 ,→ manipulations.

Let me revisit the code. In the left case (proving f = -10), I first derived f =
 ,→ 11 - 3*z from h0 , then substituted that into h1 to get h3 . Then I simplified
 ,→ h3 to get h4 , h5 , and h6 , which led to z = 7. But then I tried to use h6 to
 ,→ conclude f = -10, but h6 is z = 7. I need to instead use z = 7 to find f.

So, in the left case, after getting z = 7, I should substitute that back into f =
 ,→ 11 - 3*z to get f = -10. Then I can use that to conclude f = -10.

Similarly, in the right case, I need to properly handle the substitution and
 ,→ simplification steps to avoid the ring error.

Let me try adjusting the code accordingly. Instead of having separate cases for
 ,→ left and right, maybe I should first solve for z, then use that to solve for
 ,→ f, and then combine the results. Let's see how the corrected code does it.
</Thought>

<Output>
```lean4
import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Topology Rat


/--Given that $f + 3z = 11$ and $3(f - 1) - 5z = -68$, show that $f = -10$ and $z
 ,→    = 7$.-/
theorem algebra_2varlineareq_fp3zeq11_3tfm1m5zeqn68_feqn10_zeq7
   (f z: C)
   (h0 : f + 3*z = 11)
   (h1 : 3*(f - 1) - 5*z = -68) :
   f = -10 ∧ z = 7 := by
   /-
   Given the equations \( f + 3z = 11 \) and \( 3(f - 1) - 5z = -68 \), we aim to
    ,→   show that \( f = -10 \) and \( z = 7 \).
   1. Start by isolating \( f \) in the first equation: \( f = 11 - 3z \).
   2. Substitute \( f = 11 - 3z \) into the second equation: \( 3(11 - 3z - 1) -
    ,→   5z = -68 \).
   3. Simplify the equation step by step:
        - Expand the terms inside the parentheses: \( 3(10 - 3z) - 5z = -68 \).
        - Distribute the 3: \( 30 - 9z - 5z = -68 \).
        - Combine like terms: \( 30 - 14z = -68 \).
   4. Solve for \( z \):

                                                     24
     MA-LoT: Model-Collaboration Lean-based Long Chain-of-Thought Reasoning enhances Formal Theorem Proving

     - Subtract 30 from both sides: \( -14z = -98 \).
     - Divide both sides by -14: \( z = 7 \).
  5. Substitute \( z = 7 \) back into \( f = 11 - 3z \):
     - Calculate \( f \): \( f = 11 - 3(7) = 11 - 21 = -10 \).
  6. Conclude that \( f = -10 \) and \( z = 7 \).
  -/
  -- Isolate f in the first equation
  have h2 : f = 11 - 3*z := by linear_combination h0
  -- Substitute f = 11 - 3z into the second equation
  have h3 : 3*(11 - 3*z - 1) - 5*z = -68 := by rw [h2 ] at h1 ; exact h1
  -- Simplify the equation step by step
  have h4 : 3*10 - 9*z - 5*z = -68 := by linear_combination h3
  have h5 : 30 - 14*z = -68 := by linear_combination h4
  -- Solve for z
  have h6 : -14*z = -98 := by linear_combination h5 - 30
  have h7 : z = 7 := by linear_combination h6 / -14
  -- Substitute z = 7 back into f = 11 - 3z
  have h8 : f = -10 := by rw [h7 ] at h2 ; linear_combination h2
  -- Conclude the proof
  exact 〈h8 , h7 〉
```&
</Output>

F. Training examples
This section, we present the training examples for SFT data and correction data. We can see that in the LoT-TL training
stage, we keep the system prompt to switch off the Long CoT thinking. In particular, in the SFT data, we switch off the
entire Long CoT., In the correction data training, we only switch off the analysis of error messages in the Long CoT while
providing the error message as well as the original proof draft as a component in the Long CoT.

F.1. LoT-TL Training example for SFT data
      === Input Example ===
      <|begin_of_sentence|>You are a helpful assistant who will solve every problem
       ,→   **WITHOUT** Long Chain-of-Thought
      ### Instruction:
      @ Natural language theorem statement:
      prover_data_298:
      This all simplifies to: $\frac{55*35}{12ˆ7}$
      @ Lean4 theorem statement:
      ```lean4
      theorem prover_data_298 :
          ((55 * 35) / (12ˆ7) : Q) = (55 * 35) / (12ˆ7) := by
      ```&
      @ Lean4 theorem statement and proof with explanatory comments preceding each
       ,→   line of code:
      ### Response:
      === Output Example ===
      <Thought>
      The user ask not to solve with long CoT, so I will directly write the answer.
      </Thought>
      <Output>
      ```lean4
      /--This all simplifies to: $\frac{55*35}{12ˆ7}$-/
      theorem prover_data_298 :

                                                           25
     MA-LoT: Model-Collaboration Lean-based Long Chain-of-Thought Reasoning enhances Formal Theorem Proving

       ((55 * 35) / (12ˆ7) : Q) = (55 * 35) / (12ˆ7)   := by
       /-
       To prove that \(\frac{55 \cdot 35}{12ˆ7}\) is equal to \(\frac{55 \cdot
        ,→ 35}{12ˆ7}\), we simply observe that the expressions on both sides of
        ,→ the equality are identical. This identity holds true because the
        ,→ numerator and denominator are the same on both sides.
       -/
       -- We use the fact that the left-hand side and the right-hand side of the
        ,→ equality are the same.
       congr 1
       -- Simplify the power expression.
       <;> simp [pow_succ]
       -- Normalize the numerical values to confirm the equality.
       <;> norm_num
     ```&
     </Output><|end_of_sentence|>


F.2. LoT-TL Training example for correction data
     === Input Example ===
     <|begin_of_sentence|>You are a helpful assistant who will solve every problem
      ,→   **WITH** Long Chain-of-Thought. You can make some Lean4 proof draft in
      ,→   your O1 style Long internal Chain of Thought (CoT) and you have the
      ,→   ability to test the thing during your thinking. You need to use the error
      ,→   messages in your Long CoT to guide your proof generation but you are
      ,→   required **NOT** to provide natural language analysis to the errors.
     ### Instruction:
     @ Natural language theorem statement:
     prover_data_2216:
     Given non-negative real numbers $a, b, c$ with $a + b + c = 1$. Prove that:
      ,→   $7(ab + bc + ca) \leq 2 + 9abc$.
     @ Lean4 theorem statement:
     ```lean4
     theorem prover_data_2216 (a b c : R) (ha : 0 ≤ a) (hb : 0 ≤ b) (hc : 0 ≤ c)
      ,→   (habc : a + b + c = 1) : 7 * (a * b + b * c + c * a) ≤ 2 + 9 * a * b * c
      ,→   := by
     ```&
     @ Lean4 theorem statement and proof with explanatory comments preceding each
      ,→   line of code:
     ### Response:
     <Thought>
     Alright, I need to prove the theorem prover_data_2216 using the Lean4 code.
      ,→   Here is my draft of the proof:
     ```lean4
     theorem prover_data_2216 (a b c : R) (ha : 0 ≤ a) (hb : 0 ≤ b) (hc : 0 ≤ c)
      ,→   (habc : a + b + c = 1) : 7 * (a * b + b * c + c * a) ≤ 2 + 9 * a * b * c
      ,→   := by
         with aes
     ```&
     Let me test it in Lean4
     Emmm, it seems the above proof is wrong.
     Let me check the error messages.
     OK, Here is the error messages:
     ```bash

                                                      26
MA-LoT: Model-Collaboration Lean-based Long Chain-of-Thought Reasoning enhances Formal Theorem Proving

line 7
unexpected token 'with'; expected '{' or tactic
```&
```bash
line 7
unsolved goals
a b c : R
ha : 0 ≤ a
hb : 0 ≤ b
hc : 0 ≤ c
habc : a + b + c = 1
⊢ 7 * (a * b + b * c + c * a) ≤ 2 + 9 * a * b * c
```&
=== Output Example ===
Since the user ask NOT to provide natural language analysis to the problem.
 ,→     Let me directly try to write the revised code.
<\Thought>
<Output>
```lean4
/--Given non-negative real numbers $a, b, c$ with $a + b + c = 1$. Prove
 ,→     that: $7(ab + bc + ca) \leq 2 + 9abc$.-/
theorem prover_data_2216 (a b c : R) (ha : 0 ≤ a) (hb : 0 ≤ b) (hc : 0 ≤ c)
 ,→    (habc : a + b + c = 1) : 7 * (a * b + b * c + c * a) ≤ 2 + 9 * a * b * c
 ,→     := by
    /-
    Given non-negative real numbers \(a\), \(b\), and \(c\) such that \(a + b +
     ,→   c = 1\), we need to prove that \(7(ab + bc + ca) \leq 2 + 9abc\). The
     ,→   proof involves using algebraic manipulations and inequalities to show
     ,→   that the left-hand side is bounded above by the right-hand side.
     ,→   Specifically, we use the fact that squares of real numbers are
     ,→   non-negative, which helps in establishing the required inequality.
    -/
    -- Normalize the expression involving `a`, `b`, and `c` to prepare for
     ,→   algebraic manipulation.
    ring_nf at habc ⊢
    -- Use `nlinarith` to handle nonlinear arithmetic inequalities. This
     ,→   includes checking non-negativity of expressions involving `a`, `b`, and
     ,→   `c`.
    nlinarith [sq_nonneg (a - 1), sq_nonneg (b - 1), sq_nonneg (c - 1),
        sq_nonneg (a - b), sq_nonneg (b - c), sq_nonneg (c - a),
        sq_nonneg (a + b + c)]
```&
</Output><|end_of_sentence|>




                                                 27
     MA-LoT: Model-Collaboration Lean-based Long Chain-of-Thought Reasoning enhances Formal Theorem Proving

G. Models input example
G.1. Prover model input-output example
     ### Input Example
     IMO problem our prover found
     @ Natural language theorem statement:
     imo_1961_p1:
     (''Hungary'')
     Solve the system of equations:

     <center>
     $
     \begin{matrix}
     \quad x + y + z \\\ &= a \; \, \\
     xˆ2 +yˆ2+zˆ2 \\\ &=bˆ2 \\
     \qquad \qquad xy \\\ &= zˆ2
     \end{matrix}
     $
     </center>

     where $a $ and $b $ are constants. Give the conditions that $a $ and $b $
      ,→ must satisfy so that $x, y, z $ (the solutions of the system) are
      ,→ distinct positive numbers.

     @ Lean4 theorem statement:
     ```lean4
     theorem imo_1961_p1 (x y z a b : R) (h0 : 0 < x ∧ 0 < y ∧ 0 < z) (h1 : x ̸= y)
      ,→    (h2 : y ̸= z)
         (h3 : z ̸= x) (h4 : x + y + z = a) (h5 : x ˆ 2 + y ˆ 2 + z ˆ 2 = b ˆ 2) (h6 :
          ,→  x * y = z ˆ 2) :
         0 < a ∧ b ˆ 2 < a ˆ 2 ∧ a ˆ 2 < 3 * b ˆ 2 := by
     ```&

     @ Lean4 theorem statement and proof with explanatory comments preceding each
      ,→     line of code:
       Response:
     <Thought>
     Alright, I should do the following:
         1. Provide the natural language analysis for the theorem based on the
          ,→   Natural language theorem statement.
         2. Draft the Lean4 tactics I should use to solve the problem
         3. Write the output Lean4 code.
     The user also asks that I should avoid using the keyword `sorry` to give up
      ,→     the proof, so I will not write it in my Lean4 code.
     ### Output Example
     The `imo_1961_p1` can be proofed by analyzing the given equations and
      ,→     deriving necessary inequalities to ensure that the solutions are distinct
      ,→     positive numbers.
     </Thought>
     <Output>
     ```lean4
     theorem imo_1961_p1 (x y z a b : R) (h0 : 0 < x ∧ 0 < y ∧ 0 < z) (h1 : x ̸= y)
      ,→    (h2 : y ̸= z)


                                                      28
     MA-LoT: Model-Collaboration Lean-based Long Chain-of-Thought Reasoning enhances Formal Theorem Proving

       (h3 : z ̸= x) (h4 : x + y + z = a) (h5 : x ˆ 2 + y ˆ 2 + z ˆ 2 = b ˆ 2) (h6 :
        ,→ x * y = z ˆ 2) :
       0 < a ∧ b ˆ 2 < a ˆ 2 ∧ a ˆ 2 < 3 * b ˆ 2 := by
       -- We need to prove three inequalities: 0 < a, bˆ2 < aˆ2, and aˆ2 < 3 *
        ,→ bˆ2.
       refine' 〈_, _, _〉
       -- First, prove 0 < a.
       -- Since x, y, z are positive, their sum a must also be positive.
       . nlinarith [h0 .1, h0 .2.1, h0 .2.2, sq_nonneg (x - y), sq_nonneg (y - z),
        ,→ sq_nonneg (z - x)]
       -- Next, prove bˆ2 < aˆ2.
       -- Using the given equations and inequalities, derive the necessary
        ,→ inequalities.
       . nlinarith [mul_self_pos.mpr (sub_ne_zero.mpr h1 ), mul_self_pos.mpr
        ,→ (sub_ne_zero.mpr h2 ),
           mul_self_pos.mpr (sub_ne_zero.mpr h3 ), sq_nonneg (x - y), sq_nonneg (y -
            ,→  z), sq_nonneg (z - x)]
       -- Finally, prove aˆ2 < 3 * bˆ2.
       -- Combine all the given information to derive this inequality.
       . nlinarith [mul_self_pos.mpr (sub_ne_zero.mpr h1 ), mul_self_pos.mpr
        ,→ (sub_ne_zero.mpr h2 ),
           mul_self_pos.mpr (sub_ne_zero.mpr h3 ), sq_nonneg (x - y), sq_nonneg (y -
            ,→  z), sq_nonneg (z - x)]
     ```&
     </Output>


G.2. Corrector model input-output example
     ### Input Example
     You are a helpful mathematical assistant specialized in formal theorem
      ,→ proving using Lean4.
     Your objectives:
     1. Read and interpret the Lean4 theorem statement and any error messages.
     2. **If a previous proof attempt was incorrect, analyze its exact mistakes
      ,→ and completely discard or rewrite the proof as needed.**
     3. **Avoid reusing incorrect proof structures or strategies unless explicitly
      ,→ validated as correct.**
     4. **Address all error messages** by modifying the proof structure as needed.
     5. Provide a detailed thought process in the <Thought> section, but **only
      ,→ place the corrected Lean4 code in the <Output> section**.
     6. **Ensure the new proof is logically valid and does not use `sorry`.**
      ,→ Instruction:Below are some **correct Lean4 theorem proof examples** for
      ,→ your reference. Use them as guidance when constructing the revised proof.
      ,→ Ensure that your final proof aligns with these examples in terms of
      ,→ clarity, structure, and correctness. Instruction: @ Natural language
      ,→ theorem statement:
     mathd_algebra_392
     The sum of the squares of three consecutive positive even numbers is $12296$.
      ,→ Find the product of the three numbers divided by $8$. Show that it is
      ,→ 32736.

     @ Lean4 theorem statement:
     ```lean4
     theorem mathd_algebra_392

                                                      29
MA-LoT: Model-Collaboration Lean-based Long Chain-of-Thought Reasoning enhances Formal Theorem Proving

  (n : N)
  (h0 : Even n)
  (h1 : ((n:Z) - 2)ˆ2 + (n:Z)ˆ2 + ((n:Z) + 2)ˆ2 = 12296) :
  ((n - 2) * n * (n + 2)) / 8 = 32736 :=
```&

@ Lean4 theorem statement and proof with explanatory comments preceding each
 ,→  line of code:
  Response:
<Thought>
Alright, I need to prove the theorem prover_data_68493 using the Lean4 code.
 ,→  Here is my draft of the proof:

```lean4
theorem mathd_algebra_392
  (n : N)
  (h0 : Even n)
  (h1 : ((n:Z) - 2)ˆ2 + (n:Z)ˆ2 + ((n:Z) + 2)ˆ2 = 12296) :
  ((n - 2) * n * (n + 2)) / 8 = 32736 := by
  -- Convert the equation to integers for easier manipulation
  norm_cast at h1
  -- Expand and simplify the given equation
  ring_nf at h1
  -- Solve for n using numerical reasoning
  have h2 : n = 24 := by
     nlinarith
  -- Substitute n = 24 into the expression and simplify
  norm_num [h2 ]
```&
Let me test it in Lean4
Emmm, it seems the above proof is wrong.
Let me check the error messages.
OK, Here is the error messages:
```bash
line 18

linarith failed to find a contradiction
case h1.h
n : N
h0 : Even n
h1 : Int.subNatNat n 2 ˆ 2 + ↑(n ˆ 2) + ↑(4 + n * 4 + n ˆ 2) = 12296
a† : n < 24
⊢ False
failed
```&
```bash
line 11

unsolved goals
n : N
h0 : Even n
h1 : Int.subNatNat n 2 ˆ 2 + ↑(n ˆ 2) + ↑(4 + n * 4 + n ˆ 2) = 12296
h2 : n = 24
⊢ False

                                                 30
MA-LoT: Model-Collaboration Lean-based Long Chain-of-Thought Reasoning enhances Formal Theorem Proving

```&

So, I will rethink a Lean4 proof following the steps
    1. Provide the natural language analysis for the theorem based on the
     ,→   Natural language theorem statement, Lean4 theorem statement, my
     ,→   previous proof and the error message.
    2. Draft the Lean4 tactics I should use to solve the problem
    3. Write the output Lean4 code.
Let me analysis the wrong Lean4 solution through the error messages.
### Output Example
From the error messages, it seems the following points:
- `linarith failed to find a contradiction` suggests that the linear
 ,→     arithmetic tactic was unable to derive a contradiction from the given
 ,→     hypotheses, indicating that the assumptions might not lead to a
 ,→     contradiction as expected.
- `case h1.h` indicates a specific case within a larger context where a
 ,→     contradiction was expected but was not found, suggesting that the
 ,→     assumption `n < 24` might not be valid under certain conditions.
- `unsolved goals` means that after applying the tactics, there are still
 ,→     unresolved goals left, indicating that the tactics applied were
 ,→     insufficient to complete the proof.
From these error messages, I realize that my previous approach might not have
 ,→     handled the specifics of the problem correctly. Therefore, I need to
 ,→     revise my proof strategy.
First, I will analyze the natural language theorem statement and the provided
 ,→     Lean4 theorem statement to understand the problem fully.
The problem involves three consecutive even numbers whose squares sum up to
 ,→    12296. The goal is to find the product of these three numbers divided by
 ,→     8 and show that it equals 32736.
Given that the numbers are consecutive even numbers, I can denote the middle
 ,→     number as `n`. Then, the three consecutive even numbers can be
 ,→     represented as `n-2`, `n`, and `n+2`.
The sum of their squares is given by:
```
((n - 2)ˆ2) + (nˆ2) + ((n + 2)ˆ2) = 12296
```
Expanding these squares, we get:
```
(nˆ2 - 4n + 4) + nˆ2 + (nˆ2 + 4n + 4) = 12296
```
Combining like terms:
```
3nˆ2 + 8 = 12296
```
Subtracting 8 from both sides:
```
3nˆ2 = 12288
```
Dividing both sides by 3:
```
nˆ2 = 4096
```
Taking the square root of both sides:
```

                                                 31
MA-LoT: Model-Collaboration Lean-based Long Chain-of-Thought Reasoning enhances Formal Theorem Proving

n = 64
```
Since we are dealing with squares, we take the positive root because we are
 ,→ dealing with natural numbers.
Now, the three consecutive even numbers are:
```
n - 2 = 62
n = 64
n + 2 = 66
```
The product of these numbers is:
```
62 * 64 * 66
```
To compute this product, I can break it down into smaller factors:
```
62 * 64 = 3968
3968 * 66 = 3968 * (60 + 6) = 3968 * 60 + 3968 * 6 = 238080 + 23808 = 261888
```
Now, divide this product by 8:
```
261888 / 8 = 32736
```
Thus, the final result matches the expected outcome.
Now, I need to translate this reasoning into Lean4 code.
I will follow these steps:
1. Define the theorem with the given parameters.
2. Convert the given integer expressions to natural numbers.
3. Expand and simplify the equation using algebraic manipulation.
4. Solve for `n` using numerical methods.
5. Compute the product of the three numbers and verify that dividing by 8
 ,→ gives the desired result.
I will also include necessary imports and use appropriate tactics to handle
 ,→ the calculations.
Now, I will proceed to write the Lean4 code following this plan.
</Thought>

<Output>
```lean4
theorem mathd_algebra_392
  (n : N)
  (h0 : Even n)
  (h1 : ((n:Z) - 2)ˆ2 + (n:Z)ˆ2 + ((n:Z) + 2)ˆ2 = 12296) :
  ((n - 2) * n * (n + 2)) / 8 = 32736 := by
  -- Convert the equation to integers for easier manipulation
  push_cast at h1
  -- Expand and simplify the given equation
  ring_nf at h1
  -- Solve for n using numerical reasoning
  have h2 : n = 64 := by
    nlinarith
  -- Substitute n = 64 into the expression and simplify
  subst h2
  norm_num

                                                 32
MA-LoT: Model-Collaboration Lean-based Long Chain-of-Thought Reasoning enhances Formal Theorem Proving

```&
</Output>




                                                 33
