                                           Beyond Correctness: Exposing LLM-generated Logical Flaws in
                                              Reasoning via Multi-step Automated Theorem Proving
                                                     Xinyi Zheng∗                                   Ningke Li∗                 Xiaokun Luan                       Kailong Wang†
                                               Huazhong University of                           National University of         Peking University               Huazhong University of
                                                Science and Technology                               Singapore                  Beijing, China                 Science and Technology
                                                    Wuhan, China                                     Singapore             luanxiaokun@pku.edu.cn                  Wuhan, China
                                              xinyi_zheng@hust.edu.cn                           ningke_li@u.nus.edu                                             wangkl@hust.edu.cn

                                                                                Ling Shi                            Meng Sun                     Haoyu Wang
                                                                      Nanyang Technological                      Peking University           Huazhong University of
arXiv:2512.23511v1 [cs.SE] 29 Dec 2025




                                                                            University                            Beijing, China             Science and Technology
                                                                             Singapore                          sunm@pku.edu.cn                  Wuhan, China
                                                                       ling.shi@ntu.edu.sg                                                  haoyuwang@hust.edu.cn

                                         Abstract                                                                          to address these limitations include Large Reasoning Models (LRMs)
                                         Large Language Models (LLMs) have demonstrated impressive rea-                    that augment LLMs with neuro-symbolic AI, reinforcement learn-
                                         soning capabilities, leading to their adoption in high-stakes do-                 ing, and causal inference. Yet Apple’s recent analysis [41] reveals
                                         mains such as healthcare, law, and scientific research. However,                  that even LRMs struggle with complex tasks, often relying on shal-
                                         their reasoning often contains subtle logical errors masked by fluent             low heuristics rather than robust reasoning. Moreover, LLM reason-
                                         language, posing significant risks for critical applications. While ex-           ing remains vulnerable to adversarial attacks, where minor input
                                         isting approaches like fact-checking, self-consistency methods, and               perturbations can systematically corrupt reasoning chains [11, 51].
                                         rule-based validation provide partial solutions, they fail to detect                 Existing research has largely focused on detecting flawed rea-
                                         complex logical flaws in multi-step reasoning.                                    soning in LLM outputs, but existing methods face key limitations.
                                             To overcome these challenges, we present MATP, an evalua-                     Fact-checking approaches [3, 4, 44] verify factual accuracy using
                                         tion framework for systematically verifying LLM reasoning via                     external knowledge bases but often miss logical errors, especially
                                         Multi-step Automatic Theorem Proving. MATP translates natural                     when reasoning involves novel or implicit fact combinations. Self-
                                         language reasoning into First-Order Logic (FOL) and applies au-                   consistency methods [50] reduce random mistakes via majority
                                         tomated theorem provers to assess step-by-step logical validity.                  voting across outputs, yet fail to catch systematic errors repeated
                                         This approach identifies hidden logical errors and provides fine-                 across generations. Rule-based and post-hoc validation [20, 40, 53]
                                         grained classifications of reasoning correctness. Evaluations on a                can flag simple contradictions but struggle with complex, multi-step
                                         benchmark comprising 10,830 reasoning instances generated by                      logic, offering only limited coverage of reasoning flaws.
                                         10 LLMs across tasks from PrOntoQA-OOD, ProofWriter, and                             Prior works [32, 34, 56], using formal methods to enhance LLM
                                         FOLIO show that MATP surpasses prompting-based baselines by                       reasoning, provide valuable insights. We consider applying formal
                                         over 42 percentage points in reasoning step verification. It further              methods to evaluate, rather than enhance, LLM reasoning quality
                                         reveals model-level disparities, with reasoning models generating                 as a promising direction for rigorous analysis. Despite their theoret-
                                         more logically coherent outputs than general models. These results                ical appeal, several intertwined challenges remain. Challenge#1:
                                         demonstrate MATP’s potential to enhance the trustworthiness of                    absence of explicit logical structure in LLM-generated rea-
                                         LLM-generated reasoning.                                                          soning. Unlike formal reasoning systems, LLMs generate reasoning
                                                                                                                           via probabilistic pattern matching rather than structured inference,
                                         1    Introduction                                                                 resulting in verbose and implicit reasoning chains. Formalizing
                                                                                                                           such unstructured reasoning into precise logical representations is
                                         Large Language Models (LLMs) have achieved remarkable progress
                                                                                                                           highly challenging, especially compared with Logic-LM [34], which
                                         in natural language understanding and generation, demonstrat-
                                                                                                                           only formalizes predefined reasoning tasks. Challenge#2: subtle
                                         ing strong capabilities in reasoning [2, 17, 36], inference [48], and
                                                                                                                           and silent reasoning errors within LLMs. A single incorrect or
                                         decision-making [10, 54]. Their success has driven their adoption in
                                                                                                                           unsupported inference step can silently contaminate subsequent
                                         high-stakes domains including healthcare [6], law [21], finance [26],
                                                                                                                           reasoning, producing conclusions that appear plausible yet are
                                         and scientific research [57, 59], where reliable reasoning is essential.
                                                                                                                           fundamentally unsound. Identifying and isolating such errors is dif-
                                         However, safe deployment remains challenging: despite producing
                                                                                                                           ficult because it requires precise tracking and validation of logical
                                         fluent and seemingly coherent outputs, LLMs often exhibit subtle
                                                                                                                           dependencies throughout an entire reasoning chain.
                                         logical errors, contradictions, or unsupported inferences [25, 31, 35]
                                                                                                                              To address the challenges outlined above, we propose Multi-
                                         that could lead to serious consequences like misdiagnoses, flawed
                                                                                                                           step Automatic Theorem Proving (MATP), a post-hoc evaluation
                                         legal judgments, or erroneous research conclusions. Recent efforts
                                                                                                                           framework that enables fine-grained analysis of LLM-generated
                                         ∗ Both authors contributed equally to this research.                              reasoning. MATP leverages the natural language understanding
                                         † Kailong Wang (wangkl@hust.edu.cn) is the corresponding author.
ICSE ’26, April 12-18, 2026, Rio de Janeiro, Brazil                                                                                      X Zheng, N Li, X Luan, K Wang, L Shi, M Sun, and H Wang


              Premises                                                                                               achieves 99% classification accuracy, substantially outperforming all
     1) The bear is green.            😊 Based  on the known premises, answer whether the conclusion is
                                        True or False, and give the corresponding reasoning process.
     2) The bear likes the cat.                                                                                      baselines and demonstrating its ability to distinguish fine-grained
     3) The bear likes the dog.
     4) The bear visits the dog.                       🤔Challenge      #1
                                                            Unstructured LLM Responses                               reasoning types, though occasional misclassifications remain.
     5) The cat is young.
     6) The cat sees the bear.
                                                                                                                        Based on MATP’s evaluation and classification of all LLM-genera-
                                      🤖 GPT-3.5-Turbo                🤖 GPT-4o
                                                      Answer: False.                  GPT-4o Answer: False.
     7) The cat sees the dog.                                                 Reasoning
     8) The cat visits the bear.        GPT-3.5-Turbo Reasoning
     9) The cat visits the mouse.           Process:                   Process:
                                                                                      1) The bear is green.
                                                                                                                     ted responses in the benchmark dataset, we observe that reasoning
     10) The dog is round.                  1) The cat is young. (Premise 5)
     11) The dog likes the bear.            2) The cat sees the bear.                    (Premise 1)
                                                                                      2) The cat visits the bear.
                                                                                                                     models—especially DeepSeek-R1—produce more logically coherent
     12) The dog likes the mouse.              (Premise 6)
     13) The dog visits the                 3) If something sees the bear                (Premise 8)
                                                                                      3) The cat visits the mouse.
                                                                                                                     reasoning chains than general models, despite similar answer ac-
        mouse.                                 then it is green. (Unknown)
                                                                                         (Premise 9)
     14) The mouse is big.                  4) The bear is green. (Premise 1)
                                            5) If something likes the cat then        4) The mouse visits the dog.
                                                                                                                     curacy. Moreover, most evaluation failures originate from errors
     15) The mouse is cold.                                                              (Premise 15 & Premise
     16) The mouse is round.                   it visits the dog. (Premise 18)
                                            6) The bear visits the dog.                  19 & Premise 18)            in the NL2FOL translation stage. We further identify and summa-
     17) If something visits the                                                      5) If something visits the
                                               (Premise 4)
        mouse and the mouse
                                            7) If something visits the dog and           mouse and the mouse         rize common failure patterns, providing insights to guide future
        visits the dog then it is                                                        visits the dog then it is
                                               the dog likes the bear then it is
        cold.
     18) If something likes the                cold. (Unknown)                           cold. (Premise 17)          improvements in LLM-generated reasoning evaluation.
                                            8) If something is cold then it           6) The cat visits the mouse
        cat then it visits the dog.
     19) If something is cold                  likes the cat. (Premise 19)               and the mouse visits the    Contributions. The main contributions of this paper are:
                                            9) The bear likes the cat.                   dog. (Reasoning Step 3
        then it likes the cat.                                                           & Reasoning Step 4)
     20) If something is green                 (Premise 2)
                                            10) The dog likes the bear.               7) The cat is cold.             • A post-hoc evaluation framework for LLM-generated rea-
        then it sees the dog.                                                            (Reasoning Step 5 &
                                               (Premise 11)
                                                                                                                        soning. We propose MATP, a framework that integrates for-
                                                                                                             ✔️
     21) If something likes the                                                          Reasoning Step 6)
        mouse then it sees the cat.         11) The dog visits the mouse.
                                               (Premise 13)
     22) If something is green
        and cold then it likes the          12) If something visits the mouse                                           mal methods to evaluate LLM-generated reasoning by verify-
                                               and the mouse visits the dog
        cat.
     23) If something is big and it            then it is cold. (Premise 17)               Correct Answer               ing both step-level correctness and overall logical consistency.
                                            13) The cat is not cold. (False)             & Correct Reasoning
        visits the bear then the
                                                                                                                        MATP is open-sourced at the repository [61].
        bear is green.                                                     ❌
          Conclusion &                                                                 Challenge #2                   • A novel fine-grained reasoning chain classification. We in-
                                                                                   🤔Reasoning Errors
        Ground Truth Label                                                             Subtle and Silent
                                          Correct Answer & Unvalid Reasoning
    The cat is not cold. ➡ False                                                                                        troduce a new classification scheme that distinguishes between
                                                                                                                        sound, partially flawed, and invalid reasoning chains, enabling
Figure 1: Motivating Example. Premises used by GPT-3.5-                                                                 more nuanced evaluation of LLM-generated reasoning quality.
Turbo are marked in Bright Blue; GPT-4o includes these and                                                            • Analysis of LLM-generated reasoning behaviors. By large-
adds Deep Magenta premises. GPT-3.5-Turbo’s reasoning is                                                                scale evaluation and classification, we uncover model-specific
invalid, while GPT-4o, leveraging Premises 8, 9, and 15, yields                                                         reasoning patterns and failure modes, and identify common
the correct answer with a valid reasoning process.                                                                      NL2FOL translation errors that inform future improvements.
capabilities of LLMs to convert both reasoning tasks and model-
generated reasoning chains into unified First-Order Logic (FOL)
representations in a single pass (Challenge #1), enabling structured                                                 2 Background and Motivation
verification via Automated Theorem Prover (ATP). It subsequently                                                     2.1 Logic Reasoning in LLMs
verifies the correctness of each reasoning step and searches for                                                     Logical reasoning tasks performed by LLMs are generally catego-
a valid proof path within the reasoning chain that logically en-                                                     rized into inductive, abductive, and deductive reasoning. Among
tails the final conclusion, thereby distinguishing genuine deductive                                                 these, deductive reasoning is particularly crucial and forms the core
reasoning from mere information regurgitation (Challenge #2).                                                        focus of our work. It emphasizes rigorous, consistent, and system-
Based on the verification outcomes, MATP performs fine-grained                                                       atic inference from explicitly stated premises, making it essential in
classification of reasoning chains—identifying whether a chain is                                                    high-assurance domains such as formal verification, legal reason-
fully valid, partially flawed, or logically inconsistent. This classifi-                                             ing, and security-critical decision-making. Recent neuro-symbolic
cation jointly considers answer correctness, step-level validity, and                                                efforts have shown the feasibility of transforming natural language
proof-path soundness, moving beyond binary accuracy metrics to                                                       into formal representations and LLM–Prover integration for for-
provide deeper insights into reasoning quality. Through this design,                                                 mal reasoning [32, 34, 56]. Inspired by these efforts, we propose a
MATP provides a more interpretable and reliable assessment of                                                        lightweight divide-and-conquer framework for assessing logical
LLM reasoning performance in complex deductive tasks.                                                                validity in LLM-generated deductive reasoning chains.
Results and Findings. We evaluate MATP through extensive ex-                                                         A motivating example. Figure 1 illustrates why systematic verifi-
periments on two datasets: (1) a benchmark comprising reason-                                                        cation of LLM reasoning is necessary. When given a deductive rea-
ing tasks from PrOntoQA-OOD [39], ProofWriter [43], and                                                              soning task from ProofWriter, both GPT-3.5-Turbo and GPT-4o
FOLIO [15], along with LLM-generated responses from 10 main-                                                         reach the correct conclusion but through vastly different reasoning
stream LLMs, including five general and five reasoning models,                                                       processes. Notably, both models express their reasoning in natural
totaling 10,830 instances; and (2) a classification dataset based on                                                 language without an explicit logical structure, making it difficult
PrOntoQA-OOD, constructed by applying controlled perturba-                                                           to verify the correctness of individual steps and their interconnec-
tions to standard reasoning chains. Across the benchmark dataset,                                                    tions. This highlights Challenge #1. GPT-3.5-Turbo’s reasoning
MATP converts natural language sentences to FOL representa-                                                          contains critical flaws: steps 3 and 7 introduce unsupported infor-
tions with over 99% accuracy on syntactically simpler tasks from                                                     mation while step 13 contradicts the premises—yet these errors are
PrOntoQA-OOD and ProofWriter, while maintaining relatively                                                           masked by fluent natural language. This illustrates Challenge #2
strong performance on the more linguistically complex tasks from                                                     for identifying subtle yet consequential reasoning errors. Moreover,
FOLIO. In verifying individual reasoning steps, MATP consistently                                                    even when individual steps seem correct, the entire reasoning chain
outperforms prompting-based baselines by more than 42 percent-                                                       generated by GPT-3.5-Turbo still fails to support the conclusion,
age points in macro F1-score. On the classification dataset, MATP                                                    indicating that the answer might be coincidental.
Beyond Correctness: Exposing LLM-generated Logical Flaws in Reasoning via Multi-step Automated Theorem Proving       ICSE ’26, April 12-18, 2026, Rio de Janeiro, Brazil


2.2     Formal Foundations                                                           sufficiency of the reasoning chain. Formally, the input to MATP is
We outline the technical foundations for formalizing and verify-                     defined as 𝐷 = {𝑃, 𝐶, 𝐿, 𝑆, 𝐴}, consisting of five components:
ing logical reasoning using first-order logic (FOL) and automated                     (1) Premises (𝑃): A set of factual statements 𝑃 = {𝑃 1, 𝑃2, . . . , 𝑃𝑛 },
theorem provers (ATPs).                                                                   where each 𝑃𝑖 is assumed to be true for subsequent reasoning.
FOL serves as a formal language for representing and reasoning                        (2) Candidate Conclusion (𝐶): A statement that is subject to
about logical statements. It extends propositional logic with predi-                      validation based on the given premises 𝑃. By design, it is guar-
cates and quantified variables, enabling the expression of general                        anteed to either logically follow from 𝑃 or contradict it.
statements about objects in a domain. The core components of FOL                      (3) Ground Truth Label (𝐿): A manually annotated label 𝐿 ∈
include: constants representing specific objects, predicates represent-                   {𝑇𝑟𝑢𝑒, 𝐹𝑎𝑙𝑠𝑒} representing the correctness of the candidate
ing properties or relations, logical connectives such as negation (¬),                    conclusion 𝐶 under the given premises 𝑃. Specifically, 𝑇 𝑟𝑢𝑒
conjunction (∧), disjunction (∨), and implication (→), and quanti-                        indicates that 𝑃 ⊢ 𝐶, i.e., 𝐶 logically follows from 𝑃, and 𝐹𝑎𝑙𝑠𝑒
fiers (∀ for “for all”, ∃ for “there exists”).                                            indicates that 𝑃 ⊢ ¬𝐶, i.e., 𝐶 contradicts 𝑃.
   The central criterion for evaluating such reasoning is logical                     (4) Reasoning Steps (𝑆): A sequence of intermediate statements
validity. A conclusion 𝐶 is a logical consequence of a set of premises                    𝑆 = (𝑆 1, 𝑆 2, . . . , 𝑆𝑚 ) generated by the target LLM during its rea-
𝑃 = {𝑃 1, 𝑃2, . . . , 𝑃𝑛 }, denoted as 𝑃 |= 𝐶, if and only if 𝐶 is true in                soning process, where each 𝑆𝑖 represents a statement produced
every model (i.e., every possible interpretation of the symbols)                          as part of the model’s reasoning trajectory toward validating
that satisfies all premises in 𝑃. This property of validity ensures                       or refuting the conclusion.
that there can be no counterexample where the premises hold true                      (5) Predicted Answer (𝐴): The final judgment 𝐴 ∈ {𝑇 𝑟𝑢𝑒, 𝐹𝑎𝑙𝑠𝑒}
but the conclusion does not, providing a rigorous standard for                            produced by the target LLM regarding the correctness of the
correctness. In sound and complete logical systems like FOL, this                         candidate conclusion 𝐶, representing the model’s decision
semantic entailment (|=) is equivalent to syntactic provability (⊢),                      based on the reasoning steps 𝑆.
meaning a valid conclusion can also be derived from the premises
through a finite sequence of formal inference steps. Our work aims                      Based on the input 𝐷, MATP translates the premises 𝑃, candidate
to automatically check if the content generated by LLMs satisfy                      conclusion 𝐶, and reasoning steps 𝑆 into FOL formulas and performs
this standard of validity with respect to the given premises.                        logical verification using an automated theorem prover. It produces
ATPs are specialized tools designed to automatically determine the                   three key outputs to facilitate comprehensive evaluation:
validity of logical entailments in formal systems like FOL. State-of-                 (1) Reasoning Step Correctness Annotation: For each reason-
the-art ATPs, including Vampire [19] used in our work, primarily                          ing step, MATP assigns a correctness label 𝑆𝑡𝑒𝑝𝐶𝑜𝑟𝑟𝑒𝑐𝑡𝑛𝑒𝑠𝑠 (𝑆𝑖 )
operate on the principle of proof by refutation. To verify the logical                    ∈ {𝑇𝑟𝑢𝑒, 𝐹𝑎𝑙𝑠𝑒, 𝑈 𝑛𝑘𝑛𝑜𝑤𝑛}, indicating whether 𝑆𝑖 is provable,
validity 𝑃 |= 𝐶, the prover mechanistically attempts to find a syn-                       refutable, or indeterminate based on the premises 𝑃.
tactic proof for the unsatisfiability of 𝑃 ∪ {¬𝐶}, i.e., it searches for a            (2) Valid Proof Path Existence: MATP searches for a subset of
derivation 𝑃 ∪ {¬𝐶} ⊢ ⊥, where ⊥ represents a contradiction. Due                          correct reasoning steps 𝑆𝑖𝑛𝑃𝑟𝑜𝑜 𝑓 𝑃𝑎𝑡ℎ ⊆ 𝑆 that together entail
to the completeness of FOL, finding such a proof provides a defini-                       the conclusion 𝐶 or its negation ¬𝐶. If such a valid proof path
tive confirmation of the original semantic entailment 𝑃 |= 𝐶. For                         exists, it indicates that the reasoning chain is logically sound.
interoperability, our framework translates FOL formulas into the                      (3) Fine-Grained Classification of the Reasoning Chain: By
standardized TPTP (Thousands of Problems for Theorem Provers)                             analyzing the correctness of the final predicted answer, the
format [42]. Using a high-performance ATP like Vampire enables                            correctness of individual reasoning steps, and the existence of
the rigorous and automated validation of reasoning steps at scale.                        a valid proof path, MATP categorizes the reasoning output into
                                                                                          distinct fine-grained classes.
3     Methodology                                                                      Through this principled workflow, MATP enables a rigorous
We develop a fine-grained evaluation framework for LLM-generated                     and interpretable assessment of LLM reasoning capabilities, going
reasoning in deductive tasks, focusing on more than just the final                   beyond surface-level correctness to reveal potential logical errors
answer’s correctness (§ 3.1). Specifically, MATP uses an LLM to                      and providing insights into the underlying reasoning structure.
convert both reasoning tasks and model-generated responses into                      3.2     NL2FOL
formal representations (§ 3.2), employs an ATP tool and designed
                                                                                     This module converts the given premises 𝑃, candidate conclusion
algorithms to verify step-level correctness and overall validity of
                                                                                     𝐶, and reasoning steps 𝑆 into FOL representations to enable verifi-
the reasoning chain (§ 3.3), and classifies the reasoning chain into
                                                                                     cation with automated theorem proving.
fine-grained categories (§ 3.4). An overview is shown in Figure 2.
                                                                                     3.2.1 Preprocessing. To ensure the accuracy and reliability of trans-
3.1     Task Formalization                                                           lating NL to FOL, we first apply a series of preprocessing measures.
Given a set of premises and a candidate conclusion, the target LLM                   Interacting with LLMs. To generate reasoning chains for sub-
is prompted to determine whether the conclusion logically follows                    sequent formalization and verification, we employ a structured
from the premises and to generate reasoning to support its judg-                     interaction with LLMs. Given premises 𝑃 and a candidate conclu-
ment. MATP takes the problem statement and the generated rea-                        sion 𝐶, the model is prompted to assess whether 𝐶 logically follows
soning content as input, and performs formal verification to assess                  from 𝑃 through an explicitly generated reasoning process. We use
both the correctness of individual reasoning steps and the overall                   a few-shot prompting strategy, providing annotated examples to
ICSE ’26, April 12-18, 2026, Rio de Janeiro, Brazil                                                                                                          X Zheng, N Li, X Luan, K Wang, L Shi, M Sun, and H Wang




                                                                                                                                                                                       MATP
                      Reasoning Task                                            §3.2 NL2FOL                             §3.3 Automated Logic Verification
         Premises (P)
         P1: The cat sees the bear. P2: The cat visits the                                                                 Single Statement Verification with ATP
         mouse. P3: The mouse is cold. P4: If something visits
                                                                          Reasoning Steps Filtering
         the mouse and the mouse visits the dog then it is                                                                                 (P, S)               res1   True/False/
         cold. P5: If something likes the cat then it visits the                                                        State_Ver(P, S)                                Unknonwn/
         dog. P6: If something is cold then it likes the cat.                 Parse the premises and the conclu-                           (P, ¬S)              res2
                                                                                                                                                                       Error
                                                                                                                                                                                     §3.4 Response Analysis
                                                                              sions into first-order logic formulars.   Execution fail               ATP TOOL                           and Classification
         Conclusion (C)          Ground Truth Label (L)
         The cat is not cold.    False                                        Premises-FOL
                                                                              P1: See(cat, bear).                          FOL to               FOL Verification                                With Correct
                                                                    NL2FOL P2: Visit(cat, mouse).                           TPTP               State_Ver(P, C) = L ?                         Predicted Answer?
                                                                           P3: Cold(mouse).
                                                                     LLM   P4: ∀x ((Visit(x, mouse) ∧                                     No                Yes                             Yes                    No
                                                                              Visit(mouse, dog)) → Cold(x)).
                Interact with Target LLMs                                     P5: ∀x (Like(x, cat) → Visit(x, dog)).    Predicted Answer Correctness                                   With Valid       Without False
                                                                                                                                                                          True
                                                                              P6: ∀x (Cold(x) → Like(x, cat)).                            A=L?                                        Proof Path?           Step?
                  Based on the known premises, answer
                  whether the conclusion is True or False, and
                                                                              Conclusions-FOL
                                                                                                                                                                        S1: True                        Yes              No
                                                                              S1: See(cat, bear).
                  give the corresponding reasoning process.                                                              Reasoning Steps Correctness                    S2: True      Yes         No      F1            F2
                                                                              S2: ∀x (Cold(x) → Like(x, cat)).
                                                                              S3: ∀x ((Visit(x, mouse) ∧                       State_Ver(P, Sk), Sk∈S                   S3: True
                  Reasoning Steps (S)
                  S1: The cat sees the bear. S2: If something                 Visit(mouse, dog)) → Cold(x)).                                                            S4: False
                                                                                                                                                                                      Without False     Without False
                                                                              S4: ¬Cold(cat).
       Target     is cold then it likes the cat. S3: If something                                                          Valid Proof Path Existence                                     Step?             Step?
                  visits the mouse and the mouse visits the                   C: ¬Cold(cat).
        LLM                                                                                                                   State_Ver(SinProofPath, C),
                  dog then it is cold. S4: The cat is not cold.                                                                                                           False       Yes          No   Yes                  No
                  Predicted Answer (A)                                                                                             SinProofPath⊆S,
                  False                                                  Generation                                            Sk∈SinProofPath, Sk:True                                 T1        T2          T3        T4
                                                                                             Error (Analysis fail)
                                                                       limit exceeded



      Figure 2: The workflow of MATP. Yellow nodes indicate the input, while pink nodes represent intermediate outputs.

  Prompt Template for Translating NL to FOL                                                                             3.2.2 Translating Natural Language into First-Order Logic. Inspired
  Parse the given premises and conclusions into first-order logic formulas.                                             by Logic-LM [34], which successfully leverages prompt engineering
  ### Rules
  1. Each sentence must be converted into a single FOL formula.
                                                                                                                        with GPT-4 for formalizing long-text reasoning tasks, we follow its
  2. Use the following FOL syntax: logical conjunction of expr1 and expr2: 𝑒𝑥𝑝𝑟 1 ∧ 𝑒𝑥𝑝𝑟 2 ...                          prompt design framework to implement NL2FOL. While retaining
  3. Every formula must explicitly include quantifiers ( ∀ x or ∃ x) where applicable ...
  4. When an existential entity reappears with new properties, all properties (both old and new)
                                                                                                                        its core structure, we introduce several modifications tailored to
  should be conjoined within the scope of a single existential quantifier into the later formula ...                    the specific requirements of our task.
  ... (other more specific rules)
  ### Output Format                                                                                                     Prompt Structure. As illustrated in Figure 3, the prompt struc-
  Premises / Conclusions: fol-formula ::: (index) reference. ...                                                        ture comprises five components: task definition, translation rules,
  ### Examples
  Premises: (1) The cow is cold. (2) The cow is not round. ...                                                          output format, example demonstrations, and input instance, detailed
  Conclusions: (1) The mouse needs the cow. ... (9) The mouse eats the mouse.                                           as follows. Specifically, the “conclusions” in the prompt always
  ###
  Premises: Cold(cow) ::: (1) The cow is cold. ¬Round(cow) ::: (2) The cow is not round. ...                            include both the reasoning steps 𝑆 and the candidate conclusion 𝐶
  Conclusions: Needs(mouse, cow) ::: (1) The mouse needs the cow. ... Eats(mouse, mouse) ::: (9)
  The mouse eats the mouse.
                                                                                                                        from the actual input.
  ### Your Task                                                                                                            Task definition establishes the primary goal of converting
  Return first-order logic formulas with NO other texts.
  Premises: {premises}                                                                                                  premises and conclusions into corresponding FOL representations.
  Conclusions: {conclusions}                                                                                            Translation rules define the fundamental constraints that govern
                                                                                                                        the NL2FOL process. They ensure that each statement is trans-
    Figure 3: Prompt Template for Translating NL to FOL.                                                                lated in strict accordance with FOL syntax, while following a set of
                                                                                                                        quality assurance strategies. These rules can be flexibly adjusted
guide the model’s behavior. The LLM is instructed to first pro-                                                         based on specific scenarios when necessary. Output format requires
duce a step-by-step reasoning process based solely on 𝑃, followed                                                       that each generated output include a formal FOL expression, an
by a True/False decision on whether 𝐶 is entailed. This answer-                                                         index, and the corresponding reference sentence from the input.
after-reasoning format decouples the reasoning trace from the final                                                     To ensure completeness and avoid omissions, both premises and
verdict, enabling fine-grained evaluation of both components. To en-                                                    conclusions are numerically indexed, accommodating potentially
sure faithful reasoning, the prompt explicitly constrains the output                                                    lengthy inputs. Example demonstrations show the expected input-
to avoid unnecessary complexity, ambiguous language, or reliance                                                        output relationships, enhancing clarity and reinforcing the correct
on external knowledge. The full prompt design is included in [61].                                                      application of conversion principles. Input instance provides the
Further filtering. After generating the reasoning process, the out-                                                     reasoning input, where “Premises” corresponds to premises 𝑃, and
put is split into individual sentences. Subsequently, uncertain or                                                      “Conclusions” includes both reasoning steps 𝑆 and the candidate
speculative statements (e.g., “Wren is not necessarily a gorpus”)                                                       conclusion 𝐶. The model is instructed to output only the required
are filtered out. Inspired by prior work [8], which segments reason-                                                    FOL formulas, without any extraneous content.
ing content using reflection-related keywords to identify reflective                                                    Quality Assurance Strategies. In the Rules component, we imple-
phases, we extend this approach. We remove uncertain or spec-                                                           ment strategies to minimize common errors and improve translation
ulative statements by detecting ambiguity-indicative expressions                                                        quality. For quantifier usage, variables must have explicit exis-
(e.g., “possible”, “contradict”, or “not necessarily”), without introduc-                                               tential or universal quantifiers. Parentheses are applied to complex
ing additional filtering models. The remaining reasoning steps are                                                      statements to define quantifier scopes and avoid ambiguity. For ex-
concise and explicit, aiding downstream processing. In particular,                                                      istentially quantified entities, multiple statements can describe dif-
repetitive statements are deduplicated after converting sentences                                                       ferent attributes of the same entity, such as introducing property A
into FOL form, as direct comparison in natural language is difficult.                                                   for an entity Tom and later adding property B. The later translation
Beyond Correctness: Exposing LLM-generated Logical Flaws in Reasoning via Multi-step Automated Theorem Proving                     ICSE ’26, April 12-18, 2026, Rio de Janeiro, Brazil


should integrate both properties to preserve semantic completeness.                  𝑃 is true; refutable, which means 𝑆 contradicts 𝑃 and is always false
To ensure cross-step coherence in existential instantiation,                         when 𝑃 is true; indeterminate, which means 𝑆 is neither provable
we enforce rule constraints to consistently reference entities and                   nor refutable based on 𝑃. To determine this, we invoke the prover
their predicate attributes introduced in earlier steps, avoiding logi-               to simultaneously check whether 𝑃 ⊢ 𝑆 or 𝑃 ⊢ ¬𝑆. If either holds,
cal inconsistencies. As we translate premises, reasoning steps, and                  𝑆 is classified as True or False accordingly. If neither holds (i.e.,
candidate conclusions in a single pass, LLMs’ comprehension aids                     both 𝑃 ∪ 𝑆 and 𝑃 ∪ ¬𝑆 are consistent), 𝑆 is labeled Unknown. Algo-
predicate consistency. To further ensure consistent predicate us-                    rithm 1 summarizes this procedure, with the outputs True, False,
age, we add the rule that encourages reusing existing predicates                     and Unknown corresponding to the three provability outcomes. In
before introducing new ones. This reduces redundancy and pre-                        particular, if both 𝑆 and ¬𝑆 are provable, it indicates a contradiction
vents predicate proliferation. To address LLM’s confusion between                    within 𝑃, and we return an Error.
“exclusive or” and “inclusive or”, we include targeted conversion
                                                                                     Algorithm 1 Single Statement Verification using ATP
examples to clarify their distinction. Detailed implementations of
                                                                                     Require: Premises 𝑃 = {𝑃 1 , 𝑃 2 , . . . , 𝑃𝑛 } , candidate statement 𝑆
these strategies are provided in the full prompt [61].                               Ensure: Check Result (True, False, Unknown, or Error)
                                                                                      1: function VerifySingleStatement(𝑃, 𝑆 )
3.2.3 Regeneration. The translation from natural language to FOL                      2:    𝑟𝑒𝑠 1 ←ATPRun(𝑃, 𝑆 ) and 𝑟𝑒𝑠 2 ←ATPRun(𝑃, ¬𝑆 )
                                                                                      3:    if Refutation in 𝑟𝑒𝑠 1 and Refutation in 𝑟𝑒𝑠 2 then
by LLMs is not always correct initially. If the generated FOL re-                     4:        return Error                                                        ⊲ Contradiction exists in 𝑃
sults in execution errors during verification, or if the verification                 5:    if Refutation in 𝑟𝑒𝑠 1 then
                                                                                      6:        return True                                                                       ⊲ 𝑆 is verified
outcome of the candidate conclusion contradicts the ground-truth                      7:    if Refutation in 𝑟𝑒𝑠 2 then
label, the NL2FOL process is retried up to a fixed maximum number                     8:        return False                                                                    ⊲ ¬𝑆 is verified
                                                                                      9:    return Unknown
of attempts. If all retries fail, an error is returned, indicating failure
to analyze the input. No feedback is provided during regeneration.                   Verification of the Reasoning Steps. We begin by applying Ver-
Since pinpointing semantic errors in translation is challenging, we                  ifySingleStatement to the premises 𝑃 and the candidate con-
cannot provide useful and specific feedback. While using the entire                  clusion 𝐶 to check alignment with the ground-truth label 𝐿. A
output from the previous generation as feedback is another option,                   mismatch may arise from: (1) a semantically incorrect but syntac-
experiments in § 4.5 show its minimal impact.                                        tically valid NL2FOL translation that causes the ATP to produce
                                                                                     a judgment on 𝐶 inconsistent with 𝐿, or (2) an erroneous ground-
3.3     Logical Verification                                                         truth label annotation. Since these cases cannot be automatically
This module aims to perform logical verification on FOL represen-                    differentiated or corrected, the process reverts to the NL2FOL stage
tations of input statements (𝑃, 𝐶, 𝑆) using the automated theorem                    for regeneration. After verifying the conclusion, we assess the cor-
prover. This process assigns correctness labels to each reasoning                    rectness of each intermediate reasoning step 𝑆𝑖 under the same
step and determines whether a valid proof path exists.                               premises 𝑃. If a step is refuted or indeterminate, it is recorded as
FOL to TPTP. We convert FOL formulas into TPTP format for                            a potential logical error. Algorithm 2 outlines this process. The
compatibility with standard ATP tools. This is done via a Python                     algorithm returns both the correctness of the predicted answer and
script that enforces a deterministic one-to-one mapping between                      the correctness annotation for each reasoning step. Notably, some
FOL and TPTP representations. Preprocessing steps are applied                        incorrect steps may not affect the final judgment, while others may
to align the FOL formulas with TPTP syntax, including replacing                      compromise the entire reasoning chain. To distinguish these cases,
Unicode symbols with ASCII characters, normalizing predicate and                     further analysis is conducted to determine whether a valid proof
constant names, and handling unsupported logical connectives                         path exists within the reasoning steps.
(e.g., exclusive disjunction 𝐴 ⊕ 𝐵 is rewritten as (¬𝐴 ∧ 𝐵) ∨ (𝐴 ∧
                                                                                     Algorithm 2 Reasoning Steps Verification
¬𝐵)). The script also performs lightweight syntax repair—such as
                                                                                     Require: Premises 𝑃 = {𝑃 1 , 𝑃 2 , . . . , 𝑃𝑛 } , candidate conclusion 𝐶 , ground truth label 𝐿 , reasoning
correcting missing parentheses or misused connectives—to improve                         steps 𝑆 = {𝑆 1 , 𝑆 2 , . . . , 𝑆𝑚 } , predicted answer 𝐴
robustness and reduce parsing errors in downstream verification.                     Ensure: Returns 𝐴𝑛𝑠𝑤𝑒𝑟𝐶𝑜𝑟𝑟𝑒𝑐𝑡𝑛𝑒𝑠𝑠 , step correctness annotation 𝑆𝑐𝑜𝑟𝑟𝑒𝑐𝑡𝑛𝑒𝑠𝑠
                                                                                      1: function VerifyReasoningSteps(𝑃, 𝐶, 𝐿, 𝑆, 𝐴)
   Each formula is translated into TPTP’s FOF format: “fof(name,                      2:     if VerifySingleStatement(𝑃, 𝐶 ) ≠ 𝐿 then
role, formula)”, where name is a unique identifier for the logical                    3:         return Error                                     ⊲ NL2FOL translation error or labeling error
                                                                                      4:     𝑆𝑐𝑜𝑟𝑟𝑒𝑐𝑡𝑛𝑒𝑠𝑠 ← [ ]                                                 ⊲ Initialize step correctness list
statement, role specifies whether it is an axiom or a conjecture,                     5:     for 𝑖 ← 1 to 𝑚 do
and formula is the FOL expression rewritten in TPTP syntax. All                       6:         Append(𝑆𝑐𝑜𝑟𝑟𝑒𝑐𝑡𝑛𝑒𝑠𝑠 , VerifySingleStatement(𝑃, 𝑆𝑖 ))
                                                                                      7:     𝐴𝑛𝑠𝑤𝑒𝑟𝐶𝑜𝑟𝑟𝑒𝑐𝑡𝑛𝑒𝑠𝑠 ← (𝐿 = 𝐴)                                        ⊲ Check if the answer matches
premises are assigned as axioms, and the candidate conclusion as a                    8:     return 𝐴𝑛𝑠𝑤𝑒𝑟𝐶𝑜𝑟𝑟𝑒𝑐𝑡𝑛𝑒𝑠𝑠 , 𝑆𝑐𝑜𝑟𝑟𝑒𝑐𝑡𝑛𝑒𝑠𝑠
conjecture. Unique identifiers follow the pattern “premise_index”
and “conclusion”. We first translate natural language into FOL before                Verification of the Reasoning Proof Path. Beyond evaluating
TPTP because TPTP syntax is more complex and verbose, making                         individual reasoning steps, we also assess whether the reasoning
direct NL2TPTP translation more error-prone. Converting FOL to                       process contains all the necessary steps to logically support the
TPTP helps correct syntax errors and ensures compatibility with                      conclusion label. In other words, we determine whether the rea-
theorem provers, improving verification reliability.                                 soning chain includes a valid proof path leading to the correct
Provability Verification. A core component of the verification                       classification of the conclusion. To do this, we iteratively construct
process is to determine whether a statement 𝑆 is provable from a                     a candidate proof path by including only those True-labeled steps
set of premises 𝑃. There are three possible outcomes for 𝑆: provable,                that introduce new facts not derivable from previously included
which means 𝑆 is logically entailed by 𝑃 and it holds true whenever                  steps. Formally, the proof path is a subset 𝑆𝑖𝑛𝑃𝑟𝑜𝑜 𝑓 𝑃𝑎𝑡ℎ ⊆ 𝑆, where a
ICSE ’26, April 12-18, 2026, Rio de Janeiro, Brazil                                                                               X Zheng, N Li, X Luan, K Wang, L Shi, M Sun, and H Wang


step 𝑆𝑖 is added if and only if it is labeled True and not entailed by                                     4     Evaluation
𝑆𝑖𝑛𝑃𝑟𝑜𝑜 𝑓 𝑃𝑎𝑡ℎ . After processing all steps, we check if the truth value of                                Our evaluation targets the following research questions:
the candidate conclusion 𝐶 matches the ground truth label 𝐿, when
                                                                                                               • RQ1 (Effectiveness): Can MATP accurately verify the correct-
evaluated under the proof path 𝑆𝑖𝑛𝑃𝑟𝑜𝑜 𝑓 𝑃𝑎𝑡ℎ . If True, it indicates
                                                                                                                 ness of reasoning steps generated by LLMs?
that reasoning process contains a valid proof path that supports the
conclusion label. Otherwise, the proof path is considered invalid.                                             • RQ2 (Reasoning Chain Classification): Can MATP effec-
This verification process is detailed in Algorithm 3.                                                            tively classify different types of reasoning chains?
                                                                                                               • RQ3 (Model Reasoning Analysis): How do different LLMs
Algorithm 3 Reasoning Proof Path Verification                                                                    perform in terms of reasoning quality, and what are their char-
Require: Candidate conclusion 𝐶 , ground truth label 𝐿 , reasoning steps 𝑆 = {𝑆 1 , 𝑆 2 , . . . , 𝑆𝑚 } ,         acteristic behaviors when generating reasoning chains?
    step correctness annotation 𝑆𝑐𝑜𝑟𝑟𝑒𝑐𝑡𝑛𝑒𝑠𝑠
Ensure: Returns 𝐻𝑎𝑠𝑉 𝑎𝑙𝑖𝑑𝑃𝑟𝑜𝑜 𝑓 𝑃𝑎𝑡ℎ
 1: function VerifyReasoningProofPath(𝐶, 𝐿, 𝑆, 𝑆𝑐𝑜𝑟𝑟𝑒𝑐𝑡𝑛𝑒𝑠𝑠 )
                                                                                                           4.1      Experimental Setup
2:      𝑆𝑖𝑛𝑃𝑟𝑜𝑜 𝑓 𝑃𝑎𝑡ℎ ← [ ]                                                                               Benchmark Dataset. We construct our benchmark from three
3:      for 𝑖 ← 1 to 𝑚 do
4:          if 𝑆𝑐𝑜𝑟𝑟𝑒𝑐𝑡𝑛𝑒𝑠𝑠_𝑖 = True then                                                                  reasoning-focused datasets, each designed for natural language
5:              if VerifySingleStatement(𝑆𝑖𝑛𝑃𝑟𝑜𝑜 𝑓 𝑃𝑎𝑡ℎ , 𝑆𝑖 ) = Unknown then                              inference tasks. PrOntoQA-OOD [39] and ProofWriter [43] fo-
6:                  Append(𝑆𝑖𝑛𝑃𝑟𝑜𝑜 𝑓 𝑃𝑎𝑡ℎ , 𝑆𝑖 )                    ⊲ Construct the proof path
7:      𝐻𝑎𝑠𝑉 𝑎𝑙𝑖𝑑𝑃𝑟𝑜𝑜 𝑓 𝑃𝑎𝑡ℎ ← ( VerifySingleStatement(𝑆𝑖𝑛𝑃𝑟𝑜𝑜 𝑓 𝑃𝑎𝑡ℎ , 𝐶 ) = 𝐿)
                                                                                                           cus on logical reasoning within structured ontologies, emphasizing
8:      return 𝐻𝑎𝑠𝑉 𝑎𝑙𝑖𝑑𝑃𝑟𝑜𝑜 𝑓 𝑃𝑎𝑡ℎ                                                                        categories, attributes, and rule-based inference, while FOLIO [15]
                                                                                                           centers on realistic semantic reasoning with knowledge about peo-
   If the automated theorem prover encounters an execution error                                           ple, locations, quantities, and events. Each test case in these datasets
indicating syntactic flaws in the generated FOL content, we return                                         consists of premises, a candidate conclusion, and a ground-truth
to the NL2FOL stage for regeneration.                                                                      label (𝑇𝑟𝑢𝑒, 𝐹𝑎𝑙𝑠𝑒, or 𝑈 𝑛𝑘𝑛𝑜𝑤𝑛). Test cases in PrOntoQA-OOD
                                                                                                           and ProofWriter use structured natural language, while those in
3.4       Response Analysis and Classification                                                             FOLIO use expressions closer to everyday human language.
After the first two stages, inputs exceeding the maximum NL2FOL                                                • PrOntoQA-OOD [39] (384 test cases selected) is a synthetic
retries are categorized as Error, indicating that our framework                                                  dataset where all conclusions are labeled 𝑇𝑟𝑢𝑒. Tasks are cat-
cannot handle them. For successfully processed inputs, this module                                               egorized by the minimal number of reasoning steps required;
performs a fine-grained classification of reasoning chains based                                                 we sample from the 4-hop subset to ensure higher complexity.
on logical verification to evaluate the reasoning process compre-                                              • ProofWriter [43] (344 test cases selected) uses more natural
hensively. Instead of only assessing the final predicted answer, we                                              language and complex logic. We sample from its 5-hop test set,
analyze both individual reasoning steps and the overall reasoning                                                excluding tasks with 𝑈 𝑛𝑘𝑛𝑜𝑤𝑛 label due to unclear entailment.
chain to identify potential logical flaws. This allows us to distin-                                           • FOLIO [15] (355 test cases selected) is a human-authored
guish between responses that are correct by chance and those based                                               dataset grounded in real-world facts. We sample from the
on valid reasoning. After logical verification, we obtain three key                                              training set, retaining only 𝑇𝑟𝑢𝑒/𝐹𝑎𝑙𝑠𝑒 cases and discarding
evaluation dimensions: (1) correctness of the predicted answer, (2)                                              instances where the conclusion trivially repeats a premise.
correctness of each reasoning step, and (3) existence of a valid proof                                        To balance dataset scale and focus on higher-hop instances that
path within the reasoning chain. Based on these dimensions, we                                             elicit richer model responses, we randomly sample test cases from
define six reasoning categories, as illustrated in Figure 2.                                               the maximum-hop subset of PrOntoQA-OOD and ProofWriter,
   For responses with incorrect predicted answer, we classify them                                         rather than using all available data. For FOLIO, which lacks hop-
into two categories based on whether intermediate reasoning steps                                          based partitioning, we randomly sample from its training set. For
contain errors. Any reasoning step labeled as 𝐹𝑎𝑙𝑠𝑒 or 𝑈 𝑛𝑘𝑛𝑜𝑤𝑛 is                                         each selected test case, we generate reasoning chains and predicted
considered erroneous. F1 represents cases where all reasoning steps                                        answers using 10 representative LLMs (detailed in the next section).
are correct but the final answer is incorrect, suggesting that the                                         The prompting template used for generation is provided in [61].
target model likely fails to construct a valid proof path. F2 covers                                       This results in a total of 10830 benchmark instances. Each instance
cases where both the final answer and at least one reasoning step                                          includes the premises, candidate conclusion and ground-truth la-
are incorrect, suggesting that intermediate errors may mislead the                                         bel provided by the test case, as well as the reasoning chain and
reasoning process or that the model fails to form a coherent proof.                                        predicted answer generated by the target LLM. This benchmark is
   For responses with correct predicted answers, we assess both                                            used to evaluate the effectiveness of MATP (RQ1) and to analyze
the correctness of individual steps and the validity of the reasoning                                      reasoning chain categories across models (RQ3).
chain. T1 denotes the ideal cases where all steps are correct and a                                        Models Under Test. To ensure a comprehensive evaluation,
valid proof path exists. T2 includes cases with some erroneous steps,                                      we test 10 LLMs with MATP, including five general models
yet the proof path remains valid—indicating partial robustness.                                            and five reasoning models. The general models include GPT-3.5-
T3 represents cases where all reasoning steps are correct, but the                                         turbo, GPT-4o [1, 18], LLaMA3.1-8B-chat-hf, LLaMA3.1-70B-chat-
reasoning chain does not constitute a valid proof, suggesting that                                         hf [13] and Qwen2.5-7B-Instruct [46]. The reasoning models in-
the model correctly infers the answer but fails to provide a logically                                     clude QwQ-32B [37], DeepSeek-R1-Distill-Qwen-7B, DeepSeek-R1-
complete reasoning path. T4 includes responses with step-level                                             Distill-Qwen-32B1 , DeepSeek-R1 [14] and GPT-o4-mini [33].
errors and no valid proof path, raising concerns that the correct
answer may be reached by chance or flawed reasoning.                                                       1We use DS-R1-Qwen7B/32B to represent DeepSeek-R1-Distill-Qwen-7B/32B for short.
Beyond Correctness: Exposing LLM-generated Logical Flaws in Reasoning via Multi-step Automated Theorem Proving                      ICSE ’26, April 12-18, 2026, Rio de Janeiro, Brazil


Table 1: Evaluation of MATP on the Benchmark: NL2FOL Translation Accuracy and Reasoning Step Correctness Classification
Performance. NL2FOL accuracy (§ 4.2.1) is evaluated using four metrics—ER (Execution Rate), EA (Execution Accuracy), FB
(FOL BLEU), and LE (Logical Equivalence)—while reasoning step correctness (§ 4.2.2) is measured by Macro F1 score. All values
are reported as percentages (%), with higher scores indicating better performance. In the metric rows, GPT-4o and DS-R1 refer
to prompt-based baseline methods implemented using GPT-4o and DeepSeek-R1, respectively.
          Dataset                    PrOntoQA-OOD (384)                                      ProofWriter (344)                                           FOLIO (355)
                                                    Macro F1 Score                                         Macro F1 Score                                            Macro F1 Score
                    ER      EA      FB     LE                             ER      EA      FB     LE                              ER      EA       FB      LE
  Target LLM                                    MATP GPT-4o DS-R1                                     MATP GPT-4o DS-R1                                          MATP GPT-4o DS-R1
      GPT-3.5       99.22   100.0   100.0 100.0 87.13   54.33     39.94   99.71   99.71   83.88 99.91 100.0    43.03     38.39   96.34   69.59   36.98   88.37   91.93   57.11     43.21
       GPT-4o       98.96   100.0   100.0 100.0 100.0   49.75     47.92   99.71   99.42   84.14 100.0 100.0    33.08     33.33   96.06   70.09   37.11   87.78   100.0   42.23     31.06
    LLaMA3.1-8B     99.22   100.0   100.0 100.0 100.0   38.53     49.74   99.71   100.0   83.88 99.91 100.0    46.77     40.00   95.49   70.50   36.84   88.52   89.87   68.01     47.08
   LLaMA3.1-70B     99.22   99.74   100.0 100.0 55.42   49.59     69.69   99.71   97.38   83.69 99.91 98.61    46.10     43.05   94.37   71.64   36.46   88.20   93.51   38.53     42.12
     Qwen2.5-7B     98.96   100.0   100.0 100.0 100.0   44.43     32.80   99.42   99.42   84.14 100.0 96.34    52.80     47.29   97.18   72.46   36.35   88.15   79.69   49.34     38.40
      QwQ-32B       99.22   100.0   100.0 100.0 100.0   49.37     49.79   99.13   99.41   84.28 100.0 100.0    72.70     49.27   95.49   71.09   36.63   88.16   88.75   37.29     36.55
   DS-R1-Qwen7B     99.22   99.74   100.0 100.0 100.0   44.27     39.96   99.42   98.25   84.14 100.0 98.84    62.44     36.66   96.34   70.76   37.81   88.65   72.08   41.72     39.66
  DS-R1-Qwen32B     99.22   99.74   100.0 100.0 100.0   49.58     83.13   99.42   99.42   84.28 100.0 66.47    32.52     32.42   96.62   71.43   37.29   88.92   72.82   38.53     33.70
    DeepSeek-R1     99.22   99.74   100.0 100.0 100.0   49.82     100.0   99.42   99.42   84.21 100.0 52.16    49.19     49.35   97.18   70.72   37.06   87.82   61.33   32.82     31.33
    GPT-o4-mini     98.18   100.0   100.0 100.0 100.0   48.19     100.0   99.71   100.0   84.07 100.0 100.0    54.96     54.49   95.49   70.50   36.58   88.45   94.24   46.13     32.40
      Average       99.06   99.90   100.0 100.0 94.26   47.79     61.30   99.53   99.24   84.07 99.97 91.24    49.36     42.43   96.06   70.88   36.91   88.30   84.42   45.17     37.55


Model Configuration. We set temperature to 0 for stable and                                    conversion. FB applies FOL-specific tokenization to compute simi-
consistent reasoning outputs, with top-p = 1 and top-k = 0 to favor                            larity scores, while LE determines whether the generated and refer-
high-probability tokens. An exception is GPT-o4-mini, which uses                               ence FOL formulas are logically equivalent. For datasets with refer-
a fixed temperature of 1 due to model limitations.                                             ence FOLs (FOLIO), we compute FB and LE across all premises. For
Baseline. We compare our method against a prompting-based base-                                others (PrOntoQA-OOD, ProofWriter), we manually annotate
line using GPT-4o and DeepSeek-R1 (RQ1 and RQ2), following [58].                               reference FOLs for 300 premises per dataset for metric evaluation,
The prompt elicits two outputs: (1) step-by-step judgments on rea-                             with cross-verification by three authors to ensure consistency.
soning steps (𝑇 𝑟𝑢𝑒, 𝐹𝑎𝑙𝑠𝑒, or 𝑈 𝑛𝑘𝑛𝑜𝑤𝑛); and (2) a final decision on                          Results. As shown in Table 1, both ER and EA on PrOntoQA-
whether the reasoning supports the predicted answer (𝑌𝑒𝑠 or 𝑁𝑜),                               OOD and ProofWriter are close to 100%, indicating strong syn-
both with explanations. The full prompt is provided in [61].                                   tactic and semantic alignment. In contrast, FOLIO shows high ER
Implementation. Based on MetaGPT [16], a development frame-                                    (96.06%) but lower EA (70.88%), suggesting challenges in preserving
work for multi-agent systems that coordinates tool calls and man-                              semantics for complex statements. At the sentence level, FB and
ages pipeline stages, we integrate existing components to imple-                               LE scores on PrOntoQA-OOD and LE on ProofWriter are near
ment the evaluation framework as an automated toolchain. Specif-                               100%. However, ProofWriter’s FB drops to 84.07%, mainly due
ically, we use GPT-4o for the NL2FOL translation, leveraging its                               to mismatches in forms (e.g., “Like” vs. “Likes”) between model
strong performance on long and complex natural language tasks,                                 outputs and base-form annotations, highlighting FB’s sensitivity to
and limit generation attempts to three per input. For automated                                surface variations. On FOLIO, the FB score drops to 36.91%, while
verification, we adopt the widely used automated theorem prover                                LE remains relatively high (88.30%), reflecting logical equivalence
Vampire [19]. All implementation details are available at [61].                                despite low textual similarity. This discrepancy is understandable,
Running Environment. All experiments run on a server with                                      as for complex sentences, the choice of predicate or constant names
Ubuntu 22.04, equipped with two 64-core AMD EPYC 7713 CPUs,                                    is unlikely to consistently match the expected form.
512 GB RAM, and two NVIDIA A100 PCIe 80GB GPUs.                                                   To better understand the low EA on FOLIO, we conducted a
                                                                                               manual review of cases where the MATP’s labels for candidate
                                                                                               conclusion differ from the ground truth labels. The key factors
4.2     RQ1: Effectiveness                                                                     contributing to this issue will be analyzed in detail in § 4.4.3.
We conduct evaluations on the benchmark dataset to assess the
effectiveness of MATP. The evaluation focuses on two aspects:                                  4.2.2 Ability to identify the correctness of individual reasoning steps.
the accuracy of NL2FOL translation and the ability to identify the                             This evaluation focuses on whether each reasoning step is correctly
correctness of individual reasoning steps.                                                     labeled by MATP, and how it performs versus the baseline.
                                                                                               Metric. We formulate the task as a three-class classification prob-
4.2.1 Accuracy of NL2FOL translation. We evaluate NL2FOL trans-                                lem (𝑇𝑟𝑢𝑒, 𝐹𝑎𝑙𝑠𝑒, 𝑈 𝑛𝑘𝑛𝑜𝑤𝑛), evaluated using macro F1-score. Given
lation at both the overall and sentence levels.                                                the high annotation cost, we sample 20 ER-contributing tasks per
Overall Level Metrics. Following Logic-LM [34], we use Execu-                                  dataset for each of the ten models, totaling 600 samples. Each rea-
tion Rate (ER) and Execution Accuracy (EA) to evaluate NL2FOL                                  soning step correctness within these samples is manually labeled by
translation across the entire benchmark. ER measures the propor-                               three authors, and the aggregated annotations are used to compute
tion of FOL outputs that can be successfully executed by Vampire,                              the final macro F1 score.
reflecting syntactic correctness. EA measures how often Vampire’s                              Results. The detailed results are shown in Table 1. MATP con-
verdict matches the ground truth label when execution succeeds,                                sistently outperforms both GPT-4o and DeepSeek-R1 baselines in
indicating semantic preservation.                                                              classifying reasoning step correctness. On PrOntoQA-OOD and
Sentence Level Metrics. We adopt FOL BLEU (FB) and Logical                                     ProofWriter, MATP achieves 94.26% and 91.24% F1, significantly
Equivalence (LE) from LogicLLaMA [55] to assess sentence-level                                 higher than GPT-4o (47.79%, 49.36%) and DeepSeek-R1 (61.30%,
ICSE ’26, April 12-18, 2026, Rio de Janeiro, Brazil                                                                     X Zheng, N Li, X Luan, K Wang, L Shi, M Sun, and H Wang


                                                                                                       MATP Predicted Label        GPT-4o Predicted Label    DeepSeek-R1 Predicted Label
42.43%). Even on the more informal FOLIO dataset, MATP main-
                                                                                                       50    0     0     0         39     4     0     7          48   1     0     1




                                                                                                T1




                                                                                                                              T1




                                                                                                                                                            T1
                                                                                 Ground Truth Label
tains 84.42% F1, while the baselines drop below 46%. We further
analyze the reasons behind the poor performance of the baselines.                                       0    50    0     0          1    36     0    13          0    45    0     5




                                                                                                T2




                                                                                                                              T2




                                                                                                                                                            T2
Specifically, the baselines often mislabel correct steps as 𝐹𝑎𝑙𝑠𝑒 or                                    0    0    50     0          5     1    42     2          4    0    46     0




                                                                                                T3




                                                                                                                              T3




                                                                                                                                                            T3
𝑈 𝑛𝑘𝑛𝑜𝑤𝑛 when the inference is implicit or requires multi-hop                                           0    0     2     48         0     5     0    45          0    9     0    41




                                                                                                T4




                                                                                                                              T4




                                                                                                                                                            T4
reasoning. They also struggle to distinguish between 𝐹𝑎𝑙𝑠𝑒 and                                          T1   T2    T3    T4         T1    T2    T3    T4         T1   T2    T3    T4
𝑈 𝑛𝑘𝑛𝑜𝑤𝑛, resulting in frequent confusion between the two.
                                                                           Figure 4: Heatmap of Reasoning Chain Classification Perfor-
 ANSWER to RQ1                                                             mance for MATP and Baselines.
 MATP verifies reasoning steps by accurately translating NL to FOL and
 identifying correctness, outperforming prompting-based baselines across
 all datasets. It performs well on PrOntoQA-OOD and ProofWriter,           4.4                        RQ3: Model Reasoning Analysis
 but struggles on FOLIO due to more complex language patterns.             Using the reasoning chain classifications produced by MATP, we
                                                                           evaluate how different LLMs perform across tasks, focusing on rea-
4.3      RQ2: Reasoning Chain Classification                               soning quality and model-specific patterns. We first compare model
To evaluate whether MATP can accurately classify reasoning chains,         performance across datasets, identifying strengths, limitations, and
we conduct evaluations on a classification dataset and compare its         reasoning tendencies. Next, we analyze structural patterns within
performance with baselines.                                                each category to uncover common behaviors and failure modes.
Classification Dataset. We construct a classification dataset from         Lastly, we examine cases where MATP fails to evaluate and summa-
200 PrOntoQA-OOD tasks. Starting from the standard reasoning               rize typical causes. This analysis reveals key reasoning bottlenecks
chains provided by PrOntoQA-OOD (T1-type), we apply targeted               and guides future improvements in LLM reasoning.
mutations to obtain different types of reasoning chains: to generate       4.4.1 Analysis of Model Performance. The overall category distri-
T2-type chains, we insert a negated premise to introduce false             bution is shown in Figure 5. The Error part indicates cases where
reasoning step; for T3-type chains, we remove key steps and inject         MATP fails to evaluate. The failure rate of MATP analysis cases
irrelevant content to break the logical flow; for T4-type chains, we       averages 1.04% on PrOntoQA-OOD, 1.22% on ProofWriter, and
apply both T2-type and T3-type mutations. Each variant is created          31.92% on FOLIO. The notably higher rate on FOLIO suggests that
for 50 tasks to ensure balanced coverage across the four types.            MATP is more sensitive to complex, natural language structures,
Results. Figure 4 presents the classification accuracy of MATP             mainly due to challenges in NL2FOL translation. The specific failure
versus the baselines. As shown, MATP achieves 100% accuracy on             reasons are discussed in § 4.4.3. These failed cases are excluded
T1–T3 and 96% on T4. A review of the two T4 misclassifications             from subsequent classification analysis.
attributes the errors to minor NL2FOL translation deviations, sug-            While reasoning and general models achieve similar answer
gesting that with correct translation, MATP can consistently classify      accuracy on simple datasets like PrOntoQA-OOD, they differ
reasoning chains accurately. In contrast, the GPT-4o-based base-           significantly in actual reasoning quality. Reasoning models (e.g.,
line achieves lower accuracy—78%, 72%, 84%, and 90% for T1–T4,             DeepSeek-R1, QwQ-32B) consistently generate valid reasoning
respectively. Error analysis reveals two main issues: (1) 54 correct       chains (T1–T2), with DeepSeek-R1 reaching over 96% T1 on PrOnt-
steps were misjudged as incorrect, causing 14 T1/T3 cases to be            oQA-OOD. In contrast, general models (e.g., LLaMA3.1–8B) often
classified as T2/T4; and (2) it struggles to assess whether steps          rely on shallow or inconsistent logic, lacking valid proof paths de-
sufficiently support the conclusion, leading to 20 T1/T2 cases mis-        spite high accuracy. General models also show issues like redundant
classified as T3/T4 and 11 T3/T4 cases misclassified as T1/T2. The         logic (LLaMA) or overuse of irrelevant premises (GPT-3.5), leading
DeepSeek-R1-based baseline performs better, achieving 96%, 90%,            to correct but weakly justified answers. Even reasoning models
92%, and 82% accuracy. Most misclassifications arise from failure          struggle on challenging datasets like ProofWriter, where incom-
to assess whether steps sufficiently support conclusions—6 T1/T2           plete or invalid chains (T3/T4) still exist. On FOLIO, the proportion
cases were mistaken for T3/T4, and 13 T3/T4 as T1/T2—mainly                of T2 and T4 increases across all models. This stems partly from the
due to its weaker instruction-following ability, often defaulting to       evaluation tool’s difficulty in handling truly natural language, and
global premise-to-conclusion matching.                                     partly from the dataset’s reliance on background knowledge not
   While 100% classification accuracy can be guaranteed with per-          always captured in the explicit premises. Model scale also affects
fect translation, we cannot ensure flawless NL2FOL translation in          performance. Larger models such as LLaMA3.1–70B generally yield
practice. Consequently, MATP cannot ensure absolute correctness            higher T1 ratios and fewer errors than smaller variants, yet still lag
in real-world applications. Nevertheless, it achieves significantly        behind reasoning-specialized models in logical coherence.
higher accuracy than baselines. We also record the average pro-               In summary, answer accuracy alone fails to capture reasoning
cessing time per task for all tools. GPT-4o takes around 6s per task,      strength. Our classification strategy reveals critical differences in
DeepSeek-R1 is significantly slower at 96s, while MATP maintains           logical validity and robustness, highlighting the need to evaluate
a comparable speed of approximately 9s.                                    reasoning processes, not just final answers.
 ANSWER to RQ2
                                                                           4.4.2 Analysis of Reasoning Chain Categories. We further analyze
 MATP achieves perfect classification given accurate NL2FOL translation,
                                                                           each category to identify common patterns and provide representa-
 clearly outperforming the prompting-based baselines.
                                                                           tive examples in Table 2.
Beyond Correctness: Exposing LLM-generated Logical Flaws in Reasoning via Multi-step Automated Theorem Proving                                                                                          ICSE ’26, April 12-18, 2026, Rio de Janeiro, Brazil


                    400
                                                                                             T1            T2         T3                    T4           F1          F2             Error
                          PrOntoQA-OOD                 340                                        322
                                                                                                                                                 370
                                                                                                                                                                                            320
                                                                                                                                                                                                                  370                 360
                    300
                                                                            224
            Count



                    200                                                                                               199
                                           135                                                                                                                       138
                               99                                                                                      109
                    100                      64                               81                                                                                         66 82
                                  253622                                        2441 10             27                                                                 33 31 30                   44
                                                  3       3 12 2 14 9 4             1 3                  5 0 17 9 4         1526 5 26 4            10 1 0 0 0 3                    4          8        3324          901004             13 1 2 0 1 7
                     0

                    300   ProofWriter                                                                                                            265
                                                                                                                                                                                                                  306                 309

                                                       224                                                                                                                                  216
                    200
            Count




                                                                                                  155
                                     105                                                                                                                             106
                    100        69
                                                                            8770     76                               7462 72 89                                           88 85
                                       526439                   54                54                65
                                                                                                          3745                                              36                                    46 51
                                                                  29            23 33                                     22 21                                        11 20 26 8                      22                    22
                      0
                                  13              2       4 2010     3                       1        1517    10                        4          7 11 1 19 5                                3     2     4          1434         4     3 17 3 2 9 1

                    200   FOLIO                                                                                                                  180                                        173                   179                 175
                                                       158
                    150                                                                           147
                                                                                                                      133
                                                 117                  116                   116                 115                                                                                                                              116
            Count




                               104                                                                                                  105                       114    113           113                   110                  111
                    100                                                     90
                                                                              74                                                                                           80
                                                                                                                        66
                    50            31
                                        44               35                             44          43                                                                                          37                   38
                                    1913 27                19 16                                                                                   2318                                                                                 29
                                                                                                        11 8 1615           15 9 1512                                  15 9 16 9              17 7                                        1511 5
                                                             5 6                   6 1213                                                               8   48                                          65                8748                   4
                     0
                                    GPT-3.5                  GPT-4o         LLaMA3.1-8B LLaMA3.1-70B Qwen2.5-7B                                   QwQ-32B           DS-R1-Qwen7B DS-R1-Qwen32B DeepSeek-R1                            GPT-o4-mini
                              Figure 5: Category Distribution of LLM-Generated Reasoning Chains on Benchmark Datasets.
Table 2: Special Cases of Reasoning Chain Categorization                                                                                         Models often default to answering 𝐹𝑎𝑙𝑠𝑒 when uncertain, which
with Representative Examples. In the Reasoning Response,                                                                                         may also produce coincidentally correct answers.
sentences highlighted in orange are considered 𝑈 𝑛𝑘𝑛𝑜𝑤𝑛 rel-                                                                                     T4 exhibits the same issues as T3 but also includes incorrect reason-
ative to the task premises, while black sentences are 𝑇𝑟𝑢𝑒.                                                                                      ing steps. These outputs are typically disorganized and incoherent.
           Description                                   Reasoning Response                                   Task Name                          Some cases even introduce non-existent facts to fabricate plausible
 T2: If the 𝑈 𝑛𝑘𝑛𝑜𝑤𝑛 step is ex- GPT-4o: 1) The tiger eats the dog. 2) If someone                        Task ①:                                 chains (i.e., task ③).
 cluded, this answer is a standard eats the dog then the dog needs the bear. 3) The dog                  ProofWriter-
 response.                         eats the dog. 4) The dog needs the bear. 5) There is                  RelNeg-OWA-D5-                          F1 and F2 responses both yield incorrect final predicted answers.
                                   evidence to conclude that the dog needs the bear.                     226-Q3                                  Reasoning chains in F1 contain only correct steps, whereas in F2
 T3: The conclusion that needs GPT-3.5: ... 5) If Anne is white then Anne is big. 6)                     Task ②:
 to be proven is “Fiona is not big.”. There is evidence to conclude that Anne is big.                    ProofWriter-                            include at least one incorrect step. Common issues include incom-
 However, the model is proving                                                                           AttNeg-OWA-D5-                          plete reasoning due to missing or poorly integrated premises (i.e.,
 “Anne is big.”.                                                                                         1003-Q5
 T4: The model introduce an DS-R1-Qwen7B: 1) Sally is a dumpus. 2) Sally is a                            Task ③:
                                                                                                                                                 task ④). We also observe special failure modes: models may derive
 𝑈 𝑛𝑘𝑛𝑜𝑤𝑛 information to fabri- gorpus. 3) Every gorpus is a zumpus. 4) Therefore,                       PrOntoQA-OOD-                           the correct conclusion but answer it incorrectly (i.e., task ⑤), or
 cate a valid proof path.       Sally is a zumpus. 5) Every zumpus is a romrus. 6)                       4hop-Composed-
                                Therefore, Sally is a romrus.                                            random-noadj-69-4
                                                                                                                                                 enter repetitive loops that stall the reasoning process (i.e., task ⑥).
 F1: The model’s reasoning pro- QwQ-32B: 1) Fiona is quiet. 2) Quiet things are Task ④:
 cess contains sufficient informa- green. 3) Fiona must be green. 4) Fiona is rough. ... ProofWriter-                                            Table 3: MATP Misclassifications on DeepSeek-R1’s Response
 tion to derive the conclusion, 9) Therefore, Fiona is not green.                        AttNeg-OWA-D5-
 yet it incorrectly responds that                                                        630-Q4                                                  for folio-train-57-168. Red indicates MATP’s erroneous out-
 it cannot.                                                                                                                                      puts, while green marks the expected correct ones.
 F1: The model’s reasoning steps           GPT-4o: 1) Bob is quiet. 2) Bob is smart. 3) All smart        Task ⑤:
 are entirely correct, but the final       things are green. 4) Bob is green. 5) Green things            ProofWriter-                                  Task Info and Reasoning Response                        Step-FOL Generated by GPT-4o            MATP Output
 answer is incorrect.                      are white. 6) Bob is white. 7) There is evidence to           AttNeg-OWA-D5-                           Conclusion: Leo is an animal. (True)                       1) ∀𝑥 (𝑝𝑒𝑡 (𝑥) → 𝑎𝑛𝑖𝑚𝑎𝑙 (𝑥))              S1: True
                                           conclude that Bob is white.                                   327-Q5                                   Filtered Resoning Steps:                                   2) 𝑝𝑒𝑡 (𝑙𝑒𝑜) ∧𝑑𝑜𝑔(𝑙𝑒𝑜) ∧𝑛𝑎𝑢𝑔ℎ𝑡𝑦(𝑙𝑒𝑜) ∧    S2: True
 F1: The model enters a loop dur- LLaMA3.1-8B: 1) Every lorpus is a numpus. 2) Ev- Task ⑥:                                                        1) All pets are animals.                                   ℎ𝑎𝑠𝑝𝑒𝑡 (𝑐ℎ𝑎𝑟𝑙𝑖𝑒, 𝑙𝑒𝑜)                     S3: Unknown
 ing reasoning, causing the infer- ery lorpus is a numpus. ... 20) Every lorpus is a PrOntoQA-OOD-                                                2) Charlie has a naughty pet dog named Leo.                3) ∀𝑥 (𝑑𝑜𝑔(𝑥) → 𝑝𝑒𝑡 (𝑥))                  S3: True
 ence process to stall.            numpus. ...                                       4hop-Composed-                                               3) A pet dog is a type of pet.                             3) ∀𝑥 (𝑝𝑒𝑡 (𝑥) ∧ 𝑑𝑜𝑔(𝑥) → 𝑝𝑒𝑡 (𝑥))        S4: True
                                                                                     random-noadj-22-7                                            4) Since all pets are animals, Leo being a pet             4) ∀𝑥 ((𝑝𝑒𝑡 (𝑥) ∧ 𝑎𝑛𝑖𝑚𝑎𝑙 (𝑥))      →      Cate: T2
                                                                                                                                                  implies Leo is an animal.                                  (𝑝𝑒𝑡 (𝑙𝑒𝑜) → 𝑎𝑛𝑖𝑚𝑎𝑙 (𝑙𝑒𝑜)))               Cate: T1


                                                                                                                                                    In summary, T1 and T2 exhibit the most reliable reasoning, while
T1 chains that are fully correct in both step-level logic and overall
                                                                                                                                                 T3 and T4 are less stable. F1 shows potential for improvement, while
consistency, representing ideal outputs. Nonetheless, even when
                                                                                                                                                 F2 is the most flawed. Overall reasoning quality follows: T1 > T2 >
satisfying our classification criteria, there remain minor issues that
                                                                                                                                                 T3 > T4 > F1 > F2. Manual inspection also reveals a few misclassi-
warrant further discussion, such as redundant steps that are correct
                                                                                                                                                 fications. As shown in Table 3, an NL2FOL translation error in one
but irrelevant, and skipped steps where a step relies on multiple
                                                                                                                                                 step leads to T1 being mislabeled as T2. While the classification is
unstated premises. Such cases are illustrated in GPT-4o’s output in
                                                                                                                                                 not perfectly accurate, it reliably captures overall reasoning patterns
Figure 1 (step 1 and step 4).
                                                                                                                                                 and pinpoints potential error steps, offering clearer consistency and
T2 responses resemble T1 but contain one or more incorrect steps
                                                                                                                                                 interpretability than prompt-based baselines.
that do not affect the final conclusion. Once removed, the remaining
steps form an entirely correct and valid proof (i.e., task ①).                                                                                   4.4.3 Analysis of Error Cases. Most evaluation failures originate
T3 chains consist of correct steps but fail to form a valid proof path.                                                                          from NL2FOL translation errors. Table 4 presents representative
This often results from implicit reasoning, where key premises are                                                                               cases. While translation from PrOntoQA-OOD and ProofWriter
omitted, or accidental correctness, where an unrelated conclusion                                                                                is largely accurate, occasional issues remain, such as incorrect quan-
is proven that happens to share the same truth value (i.e., task ②).                                                                             tifier scope (i.e., case ❶) or misinterpreting “or” as a conjunction
ICSE ’26, April 12-18, 2026, Rio de Janeiro, Brazil                                                                                    X Zheng, N Li, X Luan, K Wang, L Shi, M Sun, and H Wang


Table 4: Representative Error Cases in NL2FOL Translation.                                                        4.5    Ablation Study
Key erroneous parts are highlighted in red.
                                                                                                                  We conduct an ablation study comparing MATP’s performance
         Description                     NL Sentences                  FOL Representation            Dataset
                                                                                                                  with and without feedback during NL2FOL regeneration.
 The domain of the universal        If someone is smart and      ∀𝑥 (𝑠𝑚𝑎𝑟𝑡 (𝑥) ∧ ¬𝑘𝑖𝑛𝑑 (𝑥)) →     Case ❶ from
 quantifier in FOL is wrong.        not kind then they are       𝑦𝑜𝑢𝑛𝑔(𝑥)                         ProofWriter     Setup. As shown in Figure 5, most analysis failures occur on FOLIO.
                                    young.
 The wrong use of ∧ instead         Alex is a gorpus, a ster- 𝐺𝑜𝑟𝑝𝑢𝑠 (𝑎𝑙𝑒𝑥)∧𝑆𝑡𝑒𝑟𝑝𝑢𝑠 (𝑎𝑙𝑒𝑥)        Case ❷ from
                                                                                                                  Therefore, we evaluate the responses of two models, GPT-4o and
 of ∨ for “or”.                     pus, a numpus, or a gor- ∧𝑁𝑢𝑚𝑝𝑢𝑠 (𝑎𝑙𝑒𝑥)∧𝐺𝑜𝑟𝑝𝑢𝑠 (𝑎𝑙𝑒𝑥)         PrOntoQA-       DeepSeek-R1, on 355 tasks from FOLIO. Since pinpointing specific
                                    pus.                                                          OOD
 𝐵𝑜𝑦𝐵𝑎𝑛𝑑 (𝑏𝑡𝑜𝑏4𝑢) which is Show Your Love is a song 𝑆𝑜𝑛𝑔(𝑠ℎ𝑜𝑤𝑦𝑜𝑢𝑟𝑙𝑜𝑣𝑒)                       ∧    Case ❸ from
                                                                                                                  errors is difficult, we use the entire previous generation as feedback.
 effective for reasoning candi- recorded by the South Ko- 𝑅𝑒𝑐𝑜𝑟𝑑𝑒𝑑𝐵𝑦(𝑠ℎ𝑜𝑤𝑦𝑜𝑢𝑟𝑙𝑜𝑣𝑒,                FOLIO           We extend the original prompt in Figure 3 by adding a Feedback
 date conclusion is omitted.    rean boy band BtoB 4u.    𝑏𝑡𝑜𝑏4𝑢)
 The predicate is used improp-      Brian Winter was ap- 𝐴𝑝𝑝𝑜𝑖𝑛𝑡𝑒𝑑𝑂𝑏𝑠𝑒𝑟𝑣𝑒𝑟 (𝑏𝑟𝑖𝑎𝑛).               Case ❹ from     field under Input instance, containing the prior NL2FOL translation
 erly, where the same word
 “referee observer” in the con-
                                    pointed as a referee ob- ∃𝑥 (𝐹𝑜𝑜𝑡𝑏𝑎𝑙𝑙𝑅𝑒 𝑓 𝑒𝑟𝑒𝑒 (𝑥)
                                    server after his retire- 𝑅𝑒 𝑓 𝑒𝑟𝑒𝑒𝑂𝑏𝑠𝑒𝑟𝑣𝑒𝑟 (𝑥))
                                                                                       ∧          FOLIO           with conversion errors. This field helps the model avoid similar
 text is represented by differ-     ment. Some football ref-                                                      mistakes during regeneration. Similarly, the maximum number of
 ent predicates.                    erees become referee ob-
                                    servers.                                                                      regeneration attempts is set to three. We focus on the number of
 “Either...or...” represents XOR,   Everything displayed in      ∀𝑥 (𝐷𝑖𝑠𝑝𝑙𝑎𝑦𝑒𝑑 (𝑥)          →     Case ❺ from     failures in both feedback and non-feedback settings.
 which differs from OR and          the collection is either a   (𝑃𝑙𝑎𝑛𝑡 (𝑥)∨𝐴𝑛𝑖𝑚𝑎𝑙 (𝑥)))          FOLIO
 should be denoted using the        plant or an animal.                                                           Results. As shown in Table 5, using Feedback has minimal effect,
 ⊕.
                                                                                                                  with non-feedback settings sometimes yielding better results. Ad-
 The direct use of > is Airbus made more rev- 𝑅𝑒𝑣𝑒𝑛𝑢𝑒 (𝑎𝑖𝑟𝑏𝑢𝑠, 𝑙𝑎𝑠𝑡𝑦𝑒𝑎𝑟 )>                        Case ❻ from
 not   grammatical       and enue than Boeing last 𝑅𝑒𝑣𝑒𝑛𝑢𝑒 (𝑏𝑜𝑒𝑖𝑛𝑔, 𝑙𝑎𝑠𝑡𝑦𝑒𝑎𝑟 )                    FOLIO           ditionally, feedback increases resource consumption. Therefore,
 should be expressed as year.
 𝑀𝑜𝑟𝑒𝑅𝑒𝑣𝑒𝑛𝑢𝑒 (𝑎𝑖𝑟𝑏𝑢𝑠, 𝑏𝑜𝑒𝑖𝑛𝑔).                                                                                    feedback is excluded during MATP’s actual implementation.

                                                                                                                         Table 5: Impact of Feedback on MATP Failures.
when linking multiple entities (i.e., case ❷). In contrast, FOLIO
introduces more diverse and complex errors due to its rich natural                                                         Model         With Feedback          Without Feedback
language. We summarize common error patterns as follows.                                                                  GPT-4o              118                     116
Information Omission. Key details are omitted when sentences                                                            DeepSeek-R1           119                     111
contain multiple facts (case ❸).
Improper Predicate Usage. The same concept may be mapped to
different predicates, causing semantic inconsistency (i.e., case ❹).                                              5 Discussion
XOR vs. OR Confusion. Expressions involving exclusive choice,                                                     5.1 Future Enhancement
such as “either...or...”, are often mistakenly represented as disjunc-
                                                                                                                  This paper proposes (1) a framework for translating informal LLM
tion (∨) rather than exclusive or (⊕), even when explicitly prompted
                                                                                                                  reasoning into formal logic and verifying with ATP tools, and (2) a
(i.e., case ❺).
                                                                                                                  multi-level classification strategy beyond binary answer correctness.
Inadequacy in Handling Domain-Specific Expressions.
                                                                                                                  Thanks to the modular design of MATP, we can independently
Domain-specific expressions involving comparatives, superlatives,
                                                                                                                  upgrade each component, making it adaptable for deployment in
mathematics, or time are often poorly handled, resulting in ungram-
                                                                                                                  high-stakes scenarios that require rigorous reasoning validation.
matical FOL (i.e., case ❻).
                                                                                                                  Several directions remain for future exploration:
Annotation Errors. In addition to the extraction issues above, we
                                                                                                                  Enhanced Formalization. MATP’s accuracy depends on reliable
also observe annotation errors in the FOLIO dataset during manual
                                                                                                                  NL2FOL translation. Current prompt-based methods still show
inspection. Figure 6 provides an example of such a mislabeling.
                                                                                                                  limitations with complex natural language inputs. Future work
We find that the FOL ground truth representation of the fourth
                                                                                                                  may incorporate more robust or domain-adapted translation tools.
premise in the task is incorrectly given as “∀𝑥 ((𝑃𝑟𝑜 𝑓 𝑒𝑠𝑠𝑖𝑜𝑛𝑎𝑙 (𝑥) ∧
                                                                                                                  Open-Domain Knowledge Requirement. Some mappings (e.g.,
𝐻𝑖𝑔ℎ𝑊 𝑖𝑛𝑅𝑎𝑡𝑖𝑜 (𝑥)) → 𝐵𝑖𝑔3(𝑥))”, which may be the cause of the
                                                                                                                  “Low” to “¬ High”) require external knowledge not present in the
labeling error. Similar issues are also found in tasks such as folio-
                                                                                                                  premises. To ensure a strict one-to-one mapping between natural
train-63-186, 167-480, 167-479, 302-746, 470-1359, and 470-1360.
                                                                                                                  and formal language while handling implicit common knowledge,
                      Premises                                              MATP Check Result                     the model needs to autonomously introduce necessary knowledge
 1) Rafa Nadal was born in Mallorca.
 2) Rafa Nadal is a professional tennis player.
                                                          Premises-FOL:                                           (e.g., “low” equals “not high”) either before or during translation.
                                                          1) BornInMallorca(rafa)
 3) Nadal's win ratio is high.
                                                          2) Professional(rafa) ∧ TennisPlayer(rafa)              Improved Evaluation Metrics. Evaluation of extracted FOL typ-
 4) All players in the Big 3 are professionals who        3) HighWinRatio(rafa)
 have a high win ratio.                                   4) ∀x (Big3(x) → (Professional(x) ∧ HighWinRatio(x)))   ically relies on gold-standard annotations and similarity-based
                                                          Conclusion-FOL:                                         metrics, which often fail to reflect semantic fidelity and logical
        Conclusion & Ground Truth Label

        Nadal is in the Big 3.      ➡ True      ❌
                                                          Big3(rafa)
                                                          Vampire Result: Unknown      ✔️                         validity [47]. This underscores the need for more principled and
                                                                                                                  automated evaluation methods.
Figure 6: Example of Annotation Error in FOLIO. The task
                                                                                                                  Reconstructing Reasoning Graphs. Future work may model
ID is folio-train-34-99.
                                                                                                                  reasoning steps as nodes and ATP-detected inferences as directed
                                                                                                                  edges, constructing a reasoning graph from LLM-generated rea-
 ANSWER to RQ3
                                                                                                                  soning outputs. This structure enables fine-grained verification
 MATP reveals clear differences in reasoning behavior across LLMs. De-                                            and helps identify redundant, missing, or conflicting logic beyond
 spite similar answer accuracy, reasoning models yield more coherent                                              simple path existence checks.
 logic than general models, highlighting the need to assess reasoning
                                                                                                                  Expanded Reasoning Support. Beyond forward entailment, sup-
 quality beyond final answers.
                                                                                                                  porting reverse reasoning could broaden applicability.
Beyond Correctness: Exposing LLM-generated Logical Flaws in Reasoning via Multi-step Automated Theorem Proving           ICSE ’26, April 12-18, 2026, Rio de Janeiro, Brazil


5.2                   Optimization on Response Analysis                                     Enhancing Reasoning Capabilities of LLMs. Enhancing LLM
To improve efficiency and reduce manual effort—particularly in                              reasoning is critical for high-stakes tasks. Internally, DeepSeek-
NL2FOL evaluation, we leverage LLM internal features using en-                              R1 [14] combines supervised fine-tuning and reinforcement learn-
tropy and Jensen-Shannon (JS) divergence [30] to identify uncertain                         ing to enable reasoning abilities such as chain-of-thought and
or potentially flawed reasoning steps. As demonstrated in Figure 7,                         self-verification. Externally, prompting strategies like Logic-of-
when Llama3.1-8B series are evaluated on ProofWriter, flawed                                Thought [28] and Chain-of-Knowledge [49] improve logical com-
reasoning often correlates with higher entropy or JS divergence.                            pleteness and factual coherence by injecting structured logic or
Note that the full figure across datasets and LLMs is available in [61].                    knowledge into prompts. Tool-augmented methods improve rea-
    Based on this, we implement a threshold-based filtering strat-                          soning accuracy by using LLMs as semantic parsers to translating
egy: reasoning outputs with entropy below 7.0 and JS divergence                             natural language into formal languages, which are subsequently
below 0.065 are considered likely correct, allowing us to focus anal-                       processed by external symbolic tools. LINC [32] converts NL into
ysis on more uncertain cases. This pre-filtering step effectively                           FOL for logic theorem proving. SatLM [56] translates NL into declar-
reduces the evaluation burden, with correct reasoning coverage                              ative task specifications for Z3 SMT solver [9], targeting mathemati-
rates ranging from 14.7% to 40.5% across datasets and models. While                         cal and logical reasoning tasks. Logic-LM [34] covers four categories
some incorrect responses are mistakenly filtered out (e.g., 8.5% for                        of formal languages and corresponding tools, selecting appropriate
ProofWriter and 6.7% for FOLIO under Llama3.1-8B), other config-                            ones for different types of reasoning tasks. Our work adopts a simi-
urations show near-zero false negatives, validating the approach’s                          lar strategy but focuses on evaluating the correctness and logical
reliability. Overall, this method improves evaluation efficiency by                         consistency of LLM responses to reasoning tasks.
prioritizing uncertain reasoning steps. Future work will explore                            Evaluating Reasoning Capabilities of LLMs. Evaluating LLM
tighter integration of LLM internal signals to enable automated                             reasoning has become a key research focus. Prior studies assess
filtering and semi-supervised reasoning quality assessment.                                 model performance across diverse tasks, such as code understand-
                                                                                            ing correctness at both the function [27] and software engineer-
                                             ProofWriter - Llama3.1-8B                      ing [45] levels, as well as factual hallucination detection in real-
                    0.12                                                    Correct (T)
                               Lowest Entropy (Inorrect)                    Incorrect (F)   world reasoning scenarios [24]. As reasoning abilities advance, eval-
    JS Divergence




                    0.10
                                                                                            uation objectives have expanded beyond overall task correctness to
                    0.08                                                                    step-by-step reasoning analysis. The survey [23] summarizes four
                    0.06                                                                    key dimensions for evaluating reasoning steps: factuality, validity,
                    0.04                                                                    coherence, and utility. Despite progress, most methods either rely
                                                                                            on labor-intensive gold-standard reasoning chains [12, 38] or prob-
                           0            10                 20        30         40
                                                      Entropy                               abilistic LLM-based evaluations [52, 58], which undermine logical
                                             ProofWriter - Llama3.1-70B                     rigor. ROSCOE [12] proposes several metrics using embedding-
                    0.14                                                    Correct (T)     based calculations among reasoning steps, reference steps, and
                                                                            Incorrect (F)
    JS Divergence




                    0.12                                                                    problems for evaluation. MR-GSM8K [58] prompts LLMs to check
                    0.10                                                                    reasoning correctness, outputting structured fields like Solution
                    0.08                                                                    Correctness, First Error Step, and Error Analysis. ReasonEval [52]
                    0.06                                                                    fine-tunes LLMs on high-quality labeled data to score validity and
                    0.04         Lowest Entropy (Inorrect)                                  redundancy for each reasoning step. Our work extends this research
                           0      10          20     30         40    50   60        70     line by incorporating automated theorem provers to evaluate LLM-
                                                       Entropy                              generated reasoning steps.
Figure 7: Comparison of entropy and Jensen–Shannon diver-
gence distributions for correct (T) and incorrect (F) reasoning                             7   Conclusion
responses for Llama3.1 series on ProofWriter.                                               In this paper, we presented MATP, an evaluation framework that
                                                                                            bridges the gap between informal LLM reasoning and formal ver-
6            Related Work                                                                   ification through automated theorem proving. By systematically
Automatically Generating Formal Specifications. LLMs have                                   converting natural language reasoning into First-Order Logic and
been increasingly applied to automate formal specification genera-                          applying rigorous verification at each step, MATP provides unprece-
tion and logical translation from natural language. SpecGen [29]                            dented insight into the logical validity of LLM-generated reasoning
adopts a conversational and mutation-based approach to generate                             chains. Our extensive evaluation demonstrates that MATP not only
program specifications without relying on templates. NL2CTL [60]                            achieves high accuracy in FOL translation and reasoning verifica-
translates requirements into Computation Tree Logic (CTL) by                                tion, but also enables fine-grained classification that distinguishes
constructing an NL-CTL dataset through prompt engineering and                               genuine deductive reasoning from superficial pattern matching
fine-tuning a T5 model. SAFE [5] targets Rust, integrating data                             or accidental correctness. The stark differences revealed between
synthesis, fine-tuning, and symbolic verification to automate proof                         models underscore the critical need for formal verification in high-
generation with over 70% accuracy. NL2FOL [22] converts natural                             stakes applications. While challenges remain in handling complex
language into FOL, using SMT solvers for fallacy detection and                              linguistic constructs, MATP establishes a foundational framework
explanation. NL2SPEC [7] supports interactive translation into tem-                         for ensuring reliable, verifiable AI reasoning in safety-critical do-
poral logic, allowing iterative refinement to resolve ambiguity.                            mains where trust through logical soundness is paramount.
ICSE ’26, April 12-18, 2026, Rio de Janeiro, Brazil                                                                 X Zheng, N Li, X Luan, K Wang, L Shi, M Sun, and H Wang


References                                                                                 [17] Jie Huang and Kevin Chen-Chuan Chang. 2023. Towards Reasoning in Large
 [1] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Floren-              Language Models: A Survey. In Findings of the Association for Computational
     cia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal                   Linguistics: ACL 2023, Anna Rogers, Jordan Boyd-Graber, and Naoaki Okazaki
     Anadkat, et al. 2023. Gpt-4 technical report. arXiv preprint arXiv:2303.08774              (Eds.). Association for Computational Linguistics, Toronto, Canada, 1049–1065.
     (2023).                                                                                    https://doi.org/10.18653/v1/2023.findings-acl.67
 [2] Janice Ahn, Rishu Verma, Renze Lou, Di Liu, Rui Zhang, and Wenpeng Yin. 2024.         [18] Aaron Hurst, Adam Lerer, Adam P Goucher, Adam Perelman, Aditya Ramesh,
     Large Language Models for Mathematical Reasoning: Progresses and Challenges.               Aidan Clark, AJ Ostrow, Akila Welihinda, Alan Hayes, Alec Radford, et al. 2024.
     In Proceedings of the 18th Conference of the European Chapter of the Association           Gpt-4o system card. arXiv preprint arXiv:2410.21276 (2024).
     for Computational Linguistics: Student Research Workshop, Neele Falk, Sara Papi,      [19] Laura Kovács and Andrei Voronkov. 2013. First-Order Theorem Proving and
     and Mike Zhang (Eds.). Association for Computational Linguistics, St. Julian’s,            Vampire. In Computer Aided Verification, Natasha Sharygina and Helmut Veith
     Malta, 225–237. https://aclanthology.org/2024.eacl-srw.17/                                 (Eds.). Springer Berlin Heidelberg, Berlin, Heidelberg, 1–35.
 [3] Isabelle Augenstein, Timothy Baldwin, Meeyoung Cha, Tanmoy Chakraborty,               [20] Satyapriya Krishna, Jiaqi Ma, Dylan Z Slack, Asma Ghandeharioun, Sameer Singh,
     Giovanni Luca Ciampaglia, David Corney, Renee DiResta, Emilio Ferrara, Scott               and Himabindu Lakkaraju. 2023. Post Hoc Explanations of Language Models Can
     Hale, Alon Halevy, Eduard Hovy, Heng Ji, Filippo Menczer, Ruben Miguez, Preslav            Improve Language Models. In Thirty-seventh Conference on Neural Information
     Nakov, Dietram Scheufele, Shivam Sharma, and Giovanni Zagni. 2024. Factuality              Processing Systems. https://openreview.net/forum?id=3H37XciUEv
     challenges in the era of large language models and opportunities for fact-checking.   [21] Jinqi Lai, Wensheng Gan, Jiayang Wu, Zhenlian Qi, and Philip S. Yu. 2024. Large
     Nature Machine Intelligence 6, 8 (2024), 852–863. https://doi.org/10.1038/s42256-          language models in law: A survey. AI Open 5 (2024), 181–196. https://doi.org/10.
     024-00881-z                                                                                1016/j.aiopen.2024.09.002
 [4] Shiqi Chen, Yiran Zhao, Jinghan Zhang, I-Chun Chern, Siyang Gao, Pengfei              [22] Abhinav Lalwani, Lovish Chopra, Christopher Hahn, Caroline Trippel, Zhijing Jin,
     Liu, and Junxian He. 2023. FELM: Benchmarking Factuality Evaluation of Large               and Mrinmaya Sachan. 2024. NL2FOL: translating natural language to first-order
     Language Models. In Thirty-seventh Conference on Neural Information Processing             logic for logical fallacy detection. arXiv preprint arXiv:2405.02318 (2024).
     Systems Datasets and Benchmarks Track. https://openreview.net/forum?id=               [23] Jinu Lee and Julia Hockenmaier. 2025. Evaluating step-by-step reasoning traces:
     jSO7Vgolc6                                                                                 A survey. arXiv preprint arXiv:2502.12289 (2025).
 [5] Tianyu Chen, Shuai Lu, Shan Lu, Yeyun Gong, Chenyuan Yang, Xuheng Li,                 [24] Ningke Li, Yuekang Li, Yi Liu, Ling Shi, Kailong Wang, and Haoyu Wang. 2024.
     Md Rakib Hossain Misu, Hao Yu, Nan Duan, Peng Cheng, et al. 2024. Automated                Drowzee: Metamorphic testing for fact-conflicting hallucination detection in
     proof generation for rust code via self-evolution. arXiv preprint arXiv:2410.15756         large language models. Proceedings of the ACM on Programming Languages 8,
     (2024).                                                                                    OOPSLA2 (2024), 1843–1872.
 [6] Jan Clusmann, Fiona R. Kolbinger, Hannah Sophie Muti, Zunamys I. Carrero,             [25] Yanda Li, Dixuan Wang, Jiaqing Liang, Guochao Jiang, Qianyu He, Yanghua
     Jan-Niklas Eckardt, Narmin Ghaffari Laleh, Chiara Maria Lavinia Löffler, Sophie-           Xiao, and Deqing Yang. 2024. Reason from Fallacy: Enhancing Large Language
     Caroline Schwarzkopf, Michaela Unger, Gregory P. Veldhuizen, Sophia J. Wagner,             Models’ Logical Reasoning through Logical Fallacy Understanding. In Findings
     and Jakob Nikolas Kather. 2023. The future landscape of large language models              of the Association for Computational Linguistics: NAACL 2024, Kevin Duh, Helena
     in medicine. Communications Medicine 3, 1 (2023), 141. https://doi.org/10.1038/            Gomez, and Steven Bethard (Eds.). Association for Computational Linguistics,
     s43856-023-00370-1                                                                         Mexico City, Mexico, 3053–3066. https://doi.org/10.18653/v1/2024.findings-
 [7] Matthias Cosler, Christopher Hahn, Daniel Mendoza, Frederik Schmitt, and Car-              naacl.192
     oline Trippel. 2023. nl2spec: Interactively translating unstructured natural lan-     [26] Yinheng Li, Shaofei Wang, Han Ding, and Hang Chen. 2023. Large Language
     guage to temporal logics with large language models. In International Conference           Models in Finance: A Survey. In Proceedings of the Fourth ACM International
     on Computer Aided Verification. Springer, 383–396.                                         Conference on AI in Finance (Brooklyn, NY, USA) (ICAIF ’23). Association for
 [8] Yu Cui and Cong Zuo. 2025. Practical Reasoning Interruption Attacks on Rea-                Computing Machinery, New York, NY, USA, 374–382. https://doi.org/10.1145/
     soning Large Language Models. arXiv preprint arXiv:2505.06643 (2025).                      3604237.3626869
 [9] Leonardo De Moura and Nikolaj Bjørner. 2008. Z3: An efficient SMT solver. In          [27] Ziyu Li and Donghwan Shin. 2024. Mutation-based consistency testing for eval-
     International conference on Tools and Algorithms for the Construction and Analysis         uating the code understanding capability of llms. In Proceedings of the IEEE/ACM
     of Systems. Springer, 337–340.                                                             3rd International Conference on AI Engineering-Software Engineering for AI. 150–
[10] Eva Eigner and Thorsten Händler. 2024. Determinants of LLM-assisted decision-              159.
     making. arXiv preprint arXiv:2402.17385 (2024).                                       [28] Tongxuan Liu, Wenjiang Xu, Weizhe Huang, Yuting Zeng, Jiaxing Wang, Xingyu
[11] Esther Gan, Yiran Zhao, Liying Cheng, Mao Yancan, Anirudh Goyal, Kenji                     Wang, Hailong Yang, and Jing Li. 2024. Logic-of-thought: Injecting logic into con-
     Kawaguchi, Min-Yen Kan, and Michael Shieh. 2024. Reasoning Robustness of                   texts for full reasoning in large language models. arXiv preprint arXiv:2409.17539
     LLMs to Adversarial Typographical Errors. In Proceedings of the 2024 Conference            (2024).
     on Empirical Methods in Natural Language Processing, Yaser Al-Onaizan, Mohit          [29] Lezhi Ma, Shangqing Liu, Yi Li, Xiaofei Xie, and Lei Bu. 2024. Specgen: Automated
     Bansal, and Yun-Nung Chen (Eds.). Association for Computational Linguistics,               generation of formal program specifications via large language models. arXiv
     Miami, Florida, USA, 10449–10459. https://doi.org/10.18653/v1/2024.emnlp-                  preprint arXiv:2401.08807 (2024).
     main.584                                                                              [30] M.L. Menéndez, J.A. Pardo, L. Pardo, and M.C. Pardo. 1997. The Jensen-Shannon
[12] Olga Golovneva, Moya Chen, Spencer Poff, Martin Corredor, Luke Zettlemoyer,                divergence. Journal of the Franklin Institute 334, 2 (1997), 307–318. https:
     Maryam Fazel-Zarandi, and Asli Celikyilmaz. 2022. Roscoe: A suite of metrics               //doi.org/10.1016/S0016-0032(96)00063-4
     for scoring step-by-step reasoning. arXiv preprint arXiv:2212.07919 (2022).           [31] Niels Mündler, Jingxuan He, Slobodan Jenko, and Martin Vechev. 2024. Self-
[13] Aaron Grattafiori, Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek               contradictory Hallucinations of Large Language Models: Evaluation, Detection
     Kadian, Ahmad Al-Dahle, Aiesha Letman, Akhil Mathur, Alan Schelten, Alex                   and Mitigation. In The Twelfth International Conference on Learning Representa-
     Vaughan, et al. 2024. The llama 3 herd of models. arXiv preprint arXiv:2407.21783          tions. https://openreview.net/forum?id=EmQSOi1X2f
     (2024).                                                                               [32] Theo Olausson, Alex Gu, Ben Lipkin, Cedegao Zhang, Armando Solar-Lezama,
[14] Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin                     Joshua Tenenbaum, and Roger Levy. 2023. LINC: A Neurosymbolic Approach
     Xu, Qihao Zhu, Shirong Ma, Peiyi Wang, Xiao Bi, et al. 2025. Deepseek-r1:                  for Logical Reasoning by Combining Language Models with First-Order Logic
     Incentivizing reasoning capability in LLMs via reinforcement learning. arXiv               Provers. In Proceedings of the 2023 Conference on Empirical Methods in Natural
     preprint arXiv:2501.12948 (2025).                                                          Language Processing, Houda Bouamor, Juan Pino, and Kalika Bali (Eds.). Associ-
[15] Simeng Han, Hailey Schoelkopf, Yilun Zhao, Zhenting Qi, Martin Riddell, Wenfei             ation for Computational Linguistics, Singapore, 5153–5176. https://doi.org/10.
     Zhou, James Coady, David Peng, Yujie Qiao, Luke Benson, Lucy Sun, Alex Wardle-             18653/v1/2023.emnlp-main.313
     Solano, Hannah Szabo, Ekaterina Zubova, Matthew Burtell, Jonathan Fan, Yixin          [33] OpenAI. 2025. Introducing OpenAI o3 and o4-mini. https://openai.com/index/
     Liu, Brian Wong, Malcolm Sailor, Ansong Ni, Linyong Nan, Jungo Kasai, Tao                  introducing-o3-and-o4-mini/. Accessed: 2025-07-13.
     Yu, Rui Zhang, Alexander R. Fabbri, Wojciech Kryscinski, Semih Yavuz, Ye Liu,         [34] Liangming Pan, Alon Albalak, Xinyi Wang, and William Yang Wang. 2023. Logic-
     Xi Victoria Lin, Shafiq Joty, Yingbo Zhou, Caiming Xiong, Rex Ying, Arman                  lm: Empowering large language models with symbolic solvers for faithful logical
     Cohan, and Dragomir Radev. 2024. FOLIO: Natural Language Reasoning with                    reasoning. arXiv preprint arXiv:2305.12295 (2023).
     First-Order Logic. arXiv:2209.00840 [cs.CL] https://arxiv.org/abs/2209.00840          [35] Amirreza Payandeh, Dan Pluth, Jordan Hosier, Xuesu Xiao, and Vijay K. Gurbani.
[16] Sirui Hong, Mingchen Zhuge, Jonathan Chen, Xiawu Zheng, Yuheng Cheng,                      2024. How Susceptible Are LLMs to Logical Fallacies?. In Proceedings of the 2024
     Jinlin Wang, Ceyao Zhang, Zili Wang, Steven Ka Shing Yau, Zijuan Lin, Liyang               Joint International Conference on Computational Linguistics, Language Resources
     Zhou, Chenyu Ran, Lingfeng Xiao, Chenglin Wu, and Jürgen Schmidhuber.                      and Evaluation (LREC-COLING 2024), Nicoletta Calzolari, Min-Yen Kan, Veronique
     2024. MetaGPT: Meta Programming for A Multi-Agent Collaborative Frame-                     Hoste, Alessandro Lenci, Sakriani Sakti, and Nianwen Xue (Eds.). ELRA and ICCL,
     work. In The Twelfth International Conference on Learning Representations. https:          Torino, Italia, 8276–8286. https://aclanthology.org/2024.lrec-main.726/
     //openreview.net/forum?id=VtmBAGCN7o                                                  [36] Shuofei Qiao, Yixin Ou, Ningyu Zhang, Xiang Chen, Yunzhi Yao, Shumin Deng,
                                                                                                Chuanqi Tan, Fei Huang, and Huajun Chen. 2023. Reasoning with Language
                                                                                                Model Prompting: A Survey. In Proceedings of the 61st Annual Meeting of the
Beyond Correctness: Exposing LLM-generated Logical Flaws in Reasoning via Multi-step Automated Theorem Proving               ICSE ’26, April 12-18, 2026, Rio de Janeiro, Brazil


     Association for Computational Linguistics (Volume 1: Long Papers), Anna Rogers,     [55] Yuan Yang, Siheng Xiong, Ali Payani, Ehsan Shareghi, and Faramarz Fekri. 2023.
     Jordan Boyd-Graber, and Naoaki Okazaki (Eds.). Association for Computational             Harnessing the Power of Large Language Models for Natural Language to First-
     Linguistics, Toronto, Canada, 5368–5393. https://doi.org/10.18653/v1/2023.acl-           Order Logic Translation. arXiv preprint arXiv:2305.15541 (2023).
     long.294                                                                            [56] Xi Ye, Qiaochu Chen, Isil Dillig, and Greg Durrett. 2023. SatLM: Satisfiability-
[37] Qwen Team. 2025. QwQ-32B: Embracing the Power of Reinforcement Learning.                 Aided Language Models Using Declarative Prompting. In Advances in Neu-
     https://qwenlm.github.io/blog/qwq-32b/. Accessed: 2025-07-13.                            ral Information Processing Systems, A. Oh, T. Naumann, A. Globerson,
[38] Abulhair Saparov and He He. 2023. Language Models Are Greedy Reasoners:                  K. Saenko, M. Hardt, and S. Levine (Eds.), Vol. 36. Curran Associates,
     A Systematic Formal Analysis of Chain-of-Thought. In The Eleventh Interna-               Inc., 45548–45580. https://proceedings.neurips.cc/paper_files/paper/2023/file/
     tional Conference on Learning Representations. https://openreview.net/forum?id=          8e9c7d4a48bdac81a58f983a64aaf42b-Paper-Conference.pdf
     qFVVBzXxR2V                                                                         [57] Junqi Yin, Sajal Dash, Feiyi Wang, and Mallikarjun Shankar. 2023. FORGE: Pre-
[39] Abulhair Saparov, Richard Yuanzhe Pang, Vishakh Padmakumar, Nitish Joshi,                Training Open Foundation Models for Science. In Proceedings of the International
     Seyed Mehran Kazemi, Najoung Kim, and He He. 2023. Testing the General                   Conference for High Performance Computing, Networking, Storage and Analysis
     Deductive Reasoning Capacity of Large Language Models Using OOD Exam-                    (Denver, CO, USA) (SC ’23). Association for Computing Machinery, New York,
     ples. CoRR abs/2305.15269 (2023). https://doi.org/10.48550/arXiv.2305.15269              NY, USA, Article 81, 13 pages. https://doi.org/10.1145/3581784.3613215
     arXiv:2305.15269                                                                    [58] Zhongshen Zeng, Pengguang Chen, Shu Liu, Haiyun Jiang, and Jiaya Jia. 2024. MR-
[40] Sergio Servantez, Joe Barrow, Kristian Hammond, and Rajiv Jain. 2024. Chain              GSM8K: A Meta-Reasoning Benchmark for Large Language Model Evaluation.
     of Logic: Rule-Based Reasoning with Large Language Models. In Findings of the            arXiv:2312.17080 [cs.CL] https://arxiv.org/abs/2312.17080
     Association for Computational Linguistics: ACL 2024, Lun-Wei Ku, Andre Martins,     [59] Yu Zhang, Xiusi Chen, Bowen Jin, Sheng Wang, Shuiwang Ji, Wei Wang, and
     and Vivek Srikumar (Eds.). Association for Computational Linguistics, Bangkok,           Jiawei Han. 2024. A Comprehensive Survey of Scientific Large Language Models
     Thailand, 2721–2733. https://doi.org/10.18653/v1/2024.findings-acl.159                   and Their Applications in Scientific Discovery. In Proceedings of the 2024 Con-
[41] Parshin Shojaee, Iman Mirzadeh, Keivan Alizadeh, Maxwell Horton, Samy Ben-               ference on Empirical Methods in Natural Language Processing, Yaser Al-Onaizan,
     gio, and Mehrdad Farajtabar. 2025. The Illusion of Thinking: Understanding               Mohit Bansal, and Yun-Nung Chen (Eds.). Association for Computational Linguis-
     the Strengths and Limitations of Reasoning Models via the Lens of Problem                tics, Miami, Florida, USA, 8783–8817. https://doi.org/10.18653/v1/2024.emnlp-
     Complexity. https://ml-site.cdn-apple.com/papers/the-illusion-of-thinking.pdf            main.498
[42] Geoff Sutcliffe. 2017. The TPTP Problem Library and Associated Infrastructure.      [60] Mengyan Zhao, Ran Tao, Yanhong Huang, Jianqi Shi, Shengchao Qin, and Yang
     J. Autom. Reason. 59, 4 (Dec. 2017), 483–502. https://doi.org/10.1007/s10817-017-        Yang. 2024. NL2CTL: Automatic Generation of Formal Requirements Specifica-
     9407-7                                                                                   tions via Large Language Models. In Formal Methods and Software Engineering,
[43] Oyvind Tafjord, Bhavana Dalvi Mishra, and Peter Clark. 2021. ProofWriter: Gen-           Kazuhiro Ogata, Dominique Mery, Meng Sun, and Shaoying Liu (Eds.). Springer
     erating Implications, Proofs, and Abductive Statements over Natural Language.            Nature Singapore, Singapore, 1–17.
     arXiv:2012.13048 [cs.CL] https://arxiv.org/abs/2012.13048                           [61] zxyhp. 2025. MATP. https://github.com/zxyhp/MATP.
[44] Derek Tam, Anisha Mascarenhas, Shiyue Zhang, Sarah Kwan, Mohit Bansal, and
     Colin Raffel. 2023. Evaluating the Factual Consistency of Large Language Models
     Through News Summarization. In Findings of the Association for Computational
     Linguistics: ACL 2023, Anna Rogers, Jordan Boyd-Graber, and Naoaki Okazaki
     (Eds.). Association for Computational Linguistics, Toronto, Canada, 5220–5255.
     https://doi.org/10.18653/v1/2023.findings-acl.322
[45] Minaoar Hossain Tanzil, Junaed Younus Khan, and Gias Uddin. 2024. ChatGPT
     incorrectness detection in software reviews. In Proceedings of the IEEE/ACM 46th
     International Conference on Software Engineering. 1–12.
[46] Qwen Team. 2024. Qwen2.5: A Party of Foundation Models. https://qwenlm.
     github.io/blog/qwen2.5/. Accessed: 2025-07-13.
[47] Ramya Keerthy Thatikonda, Wray Buntine, and Ehsan Shareghi. 2025. Assessing
     the Alignment of FOL Closeness Metrics with Human Judgement. arXiv preprint
     arXiv:2501.08613 (2025).
[48] Zhongwei Wan, Xin Wang, Che Liu, Samiul Alam, Yu Zheng, Jiachen Liu, Zhong-
     nan Qu, Shen Yan, Yi Zhu, Quanlu Zhang, Mosharaf Chowdhury, and Mi Zhang.
     2024. Efficient Large Language Models: A Survey. Transactions on Machine Learn-
     ing Research (2024). https://openreview.net/forum?id=bsCCJHbO8A Survey
     Certification.
[49] Jianing Wang, Qiushi Sun, Xiang Li, and Ming Gao. 2024. Boosting Language
     Models Reasoning with Chain-of-Knowledge Prompting. In Proceedings of the
     62nd Annual Meeting of the Association for Computational Linguistics (Volume 1:
     Long Papers), Lun-Wei Ku, Andre Martins, and Vivek Srikumar (Eds.). Association
     for Computational Linguistics, Bangkok, Thailand, 4958–4981. https://doi.org/
     10.18653/v1/2024.acl-long.271
[50] Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc V Le, Ed H. Chi, Sharan
     Narang, Aakanksha Chowdhery, and Denny Zhou. 2023. Self-Consistency Im-
     proves Chain of Thought Reasoning in Language Models. In The Eleventh Inter-
     national Conference on Learning Representations. https://openreview.net/forum?
     id=1PL1NIMMrw
[51] Junda Wu, Tong Yu, Xiang Chen, Haoliang Wang, Ryan Rossi, Sungchul Kim,
     Anup Rao, and Julian McAuley. 2024. DeCoT: Debiasing Chain-of-Thought for
     Knowledge-Intensive Tasks in Large Language Models via Causal Intervention.
     In Proceedings of the 62nd Annual Meeting of the Association for Computational
     Linguistics (Volume 1: Long Papers), Lun-Wei Ku, Andre Martins, and Vivek
     Srikumar (Eds.). Association for Computational Linguistics, Bangkok, Thailand,
     14073–14087. https://doi.org/10.18653/v1/2024.acl-long.758
[52] Shijie Xia, Xuefeng Li, Yixin Liu, Tongshuang Wu, and Pengfei Liu. 2025. Eval-
     uating mathematical reasoning beyond accuracy. In Proceedings of the AAAI
     Conference on Artificial Intelligence, Vol. 39. 27723–27730.
[53] Tian Xie, Zitian Gao, Qingnan Ren, Haoming Luo, Yuqian Hong, Bryan Dai, Joey
     Zhou, Kai Qiu, Zhirong Wu, and Chong Luo. 2025. Logic-RL: Unleashing LLM
     reasoning with rule-based reinforcement learning. arXiv preprint arXiv:2502.14768
     (2025).
[54] Sherry Yang, Ofir Nachum, Yilun Du, Jason Wei, Pieter Abbeel, and Dale Schuur-
     mans. 2023. Foundation models for decision making: Problems, methods, and
     opportunities. arXiv preprint arXiv:2303.04129 (2023).
