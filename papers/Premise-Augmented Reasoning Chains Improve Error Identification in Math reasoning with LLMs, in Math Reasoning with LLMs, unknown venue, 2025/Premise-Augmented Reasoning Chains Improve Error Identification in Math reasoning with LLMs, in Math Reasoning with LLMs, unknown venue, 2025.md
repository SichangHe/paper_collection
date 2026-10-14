                                                 Premise-Augmented Reasoning Chains Improve Error Identification
                                                                 in Math Reasoning with LLMs


                                                 Sagnik Mukherjee * 1 Abhinav Chinta * 1 Takyoung Kim 1 Tarun Sharma 1 Dilek Hakkani-Tür 1


                                                                Abstract                                   1. Introduction
                                             Chain-of-Thought (CoT) prompting enhances                     Chain-of-thought reasoning enhances problem solving by
arXiv:2502.02362v6 [cs.CL] 23 Sep 2025




                                             mathematical reasoning in large language models               breaking down complex tasks into a series of logical steps,
                                             (LLMs) by enabling detailed step-by-step solu-                improving the accuracy and clarity of decision-making pro-
                                             tions. However, due to the verbosity of LLMs, the             cesses. There has been a well-documented success of the
                                             resulting reasoning chains can be long, making                reasoning capabilities of LLMs with chain of thought rea-
                                             it harder to verify the reasoning steps and trace             soning (CoT; (Wei et al., 2023)) across applications such as
                                             issues resulting from dependencies between the                embodied reasoning (Gao et al., 2023; Philipov et al., 2024),
                                             steps that may be farther away in the sequence                code generation (Jiang et al., 2024), and mathematical and
                                             of steps. Importantly, mathematical reasoning                 scientific reasoning (Imani et al., 2023; Ahn et al., 2024).
                                             allows each step to be derived from a small set               However, the corresponding evaluation methods and metrics
                                             of premises, which are a subset of the preceding              have a significant limitation: they focus solely on the correct-
                                             steps in the reasoning chain. In this paper, we               ness of the final answer, neglecting intermediate reasoning
                                             present a framework that identifies the premises              processes and rationales that contribute to it. Although the
                                             for each step, to improve the evaluation of reason-           final answer serves as a proxy for the reasoning capability,
                                             ing. We restructure conventional linear reason-               it is not sufficient to judge the reasoning performance of
                                             ing chains into Premise Augmented Reasoning                   the model. Hence, evaluating the final answer provides a
                                             Chains (PARC) by introducing premise links,                   narrower view of the reasoning capabilities. Since the inter-
                                             resulting in a directed acyclic graph where the               mediate reasoning process is equally important as getting
                                             nodes are the steps and the edges are the premise             the correct final answer (Huang & Chang, 2023; Golovneva
                                             links. Through experiments with a PARC-based                  et al., 2023; Prasad et al., 2023), a comprehensive evaluation
                                             dataset that we built, namely PERL (Premises                  of the reasoning chains is crucial to holistically understand-
                                             and ERrors identification in LLMs), we demon-                 ing the reasoning capabilities of LLMs.
                                             strate that LLMs can reliably identify premises
                                                                                                           Evaluation of reasoning chains has been studied in litera-
                                             within complex reasoning chains. In particular,
                                                                                                           ture in the context of self-verification (Weng et al., 2023).
                                             even open-source LLMs achieve 90% recall in
                                                                                                           Previous work has shown that LLMs struggle to find rea-
                                             premise identification. We also show that PARC
                                                                                                           soning errors in chain-of-thought traces without the help
                                             helps to identify errors in reasoning chains more
                                                                                                           of external verifiers (Stechly et al., 2024; Wu et al., 2024;
                                             reliably. The accuracy of error identification im-
                                                                                                           Tyen et al., 2024), casting doubt on the overoptimism of
                                             proves by 6% to 16% absolute when step-by-
                                                                                                           LLMs’ self-critique abilities. Existing research focusing on
                                             step verification is carried out in PARC under
                                                                                                           the evaluation of reasoning chains in LLMs can be broadly
                                             the premises. Our findings highlight the utility
                                                                                                           categorized into reference-based and reference-free meth-
                                             of premise-centric representations in addressing
                                                                                                           ods. Reference-based methods, which rely on the avail-
                                             complex problem-solving tasks and open new av-
                                                                                                           ability of a ground truth reasoning chain (Welleck et al.,
                                             enues for improving the reliability of LLM-based
                                                                                                           2021; Han et al., 2024; Tian et al., 2021), are reliable but
                                             reasoning evaluations.
                                                                                                           are constrained by the significant cost of human annota-
                                            * Equal contribution 1 University of Illinois at Urbana
                                                                                                           tions, restricting their application. In contrast, reference-
                                                                                                           free methods (Prasad et al., 2023; Golovneva et al., 2023;
                                         Champaign. Correspondence to: Sagnik Mukherjee <sag-
                                         nikm3@illinois.edu>.                                              Zhu et al., 2024) bypass the need for annotations, but suffer
                                                                                                           from two major drawbacks: (1) most such works assign
                                         Proceedings of the 42𝑛𝑑 International Conference on Machine       only a chain-level score rather than localizing specific er-
                                         Learning, Vancouver, Canada. PMLR 267, 2025. Copyright 2025       rors, and (2) they often need fine-tuning of task-specific
                                         by the author(s).

                                                                                                       1
               Premise-Augmented Reasoning Chains Improve Error Identification in Math Reasoning with LLMs

                                                                                 Question:
                                                  given a=10 and b=20, what are the mean of the following a+b, ab, a^b, ab^2


                Linear Reasoning Chain                                                 Premise Augmented Reasoning Chain (PARC)

            Step 1: given a=10 and b=20, a+b=30                                  Step 1: given a=10 and
                                                                                                                                      ❌
                                                                                                                    Step 3: given ab=200

                                                                                                                                                                  ❌
                                                                                     b=20, a+b=30                  and a=100, a^b=10000

            Step 2: ab=200                                                                                                                      Step 5: mean = (30 +
                                                                   Question                                                                     200 + 10000 + 12000)

                                                                                                                                      ❌
                                                                                                                                                /4 = 5557.5
            Step 3: given ab=200 and a=100, a^b=10000
                                                                                                                    Step 4: given ab=600
                                                                                     Step 2: ab=200
                                                                                                                   and b=20, ab^2=12000
            Step 4: given ab=600 and b=20, ab^2=12000



         ❌  Step 5: mean = (30 + 200 + 10000 + 12000)
            /4 = 5557.5
                                                                              Premise Links    Correct step   Wrong Step   Accumulation Error




Figure 1. Comparison between a Linear Reasoning Chain (LRC) and our proposed PARC (Premise-Augmented Reasoning Chain). The
LRC (left), is linear and there no explicit premise link between steps. In PARC (right), premise links are explicitly established, enabling
better identification of correct and incorrect steps. Accumulation errors can be traced back to faulty premises. Establishing these premises
helps improve error detection with LLMs.

models, restricting their generalizability. One workaround                                    once the first mistake appears. Distinguishing accumulation
could be using formal proof assistants like Lean (Moura &                                     errors from inherently flawed steps (mathematical errors
Ullrich, 2021), which natively support the verifiability of                                   or logical inconsistencies) is crucial for a holistic evalua-
generated proofs (Yang et al., 2024; 2023; Murphy et al.,                                     tion of CoT traces. Moreover, establishing explicit premise
2024), but this requires a challenging auto-formalization of                                  links between steps allows each step to be verified only un-
natural language text (Wu et al., 2022) and often assumes                                     der its premises which reduces irrelevant information for
the solution is already known for proof construction.                                         each verification step, thus improving the error detection for
                                                                                              mathematical problem solving.
In our work, we focus on reference-free verification of LLM
reasoning chains in the context of mathematical reasoning.                                    Our main contributions are as follows:
Mathematical problem solving requires a series of deductive
reasoning steps, where each step is performed under a small                                      • We demonstrate that off-the-shelf LLMs can detect
set of premises. We hypothesize that a step in a reasoning                                         premises for a given step with high accuracy for mathe-
chain should be verified only under its premises. Previous                                         matical reasoning, enabling the conversion of a Linear
work has shown that having unnecessary context hurts the                                           Reasoning Chain (LRC) to a Premise-Augmented Rea-
performance of LLMs for solving math word problems (Shi                                            soning Chain (PARC).
et al., 2023). Thus, by excluding irrelevant context from
the verifier, we make the verification of a reasoning step                                       • We establish that verifying each step under its corre-
only conditioned on its premises, addressing the known                                             sponding premises increases the accuracy of identify-
susceptibility of LLMs to errors under distractors.                                                ing errors and their types.
We restructure conventional linear reasoning chains (LRCs)                                       • We propose a refined error taxonomy for mathemati-
into PARC (Premise-Augmented Reasoning Chains), by                                                 cal reasoning, introducing the notion of accumulation
identifying the premises of each step. Identifying those                                           errors for steps that are locally correct but inherit up-
premises improves the traceability of a reasoning chain. We                                        stream errors.
create a corresponding dataset, called PERL (Premises and
ERrors identification in Language models) to test LLMs’                                          • We introduce and will release PERL, a dataset of rea-
capability in identifying premises as well as the effective-                                       soning chains annotated with premises and error types,
ness of premise augmentation in annotating both premises                                           to facilitate broader research on premise-centered rea-
and errors. Additionally, we refine the error taxonomy (as                                         soning verification.
proposed in Golovneva et al. (2023)) for mathematical rea-
soning by introducing a new category: “accumulation error.”                                   The rest of the paper is structured as follows: in Section 2,
This error arises when a reasoning step is correct in isola-                                  we discuss relevant prior work in context of mathematical
tion but is derived from flawed premises (refer to step 5 in                                  reasoning and verification of reasoning chains with LLMs.
Fig.1), resulting in error propagation throughout the chain;                                  Section 3 introduces the research questions, alongside the
while such errors are common, existing work (Lightman                                         necessary background as well as mathematical definition of
et al., 2023; Zheng et al., 2024; Daheim et al., 2024) has                                    premises, conversion of LRC to PARC, as well as how we
not addressed them beyond discarding all subsequent steps                                     identify errors with premises. Section 4 details PERL, our
                                                                                              dataset to show effectiveness of the framework, and lastly,

                                                                                        2
              Premise-Augmented Reasoning Chains Improve Error Identification in Math Reasoning with LLMs

in section 5 we discuss the results and insights from our              premise extraction as a standalone step and refrains from
experiments. 1                                                         making strong assumptions about how the reasoning chain
                                                                       is structured.
2. Related work
                                                                       3. Method
Math Reasoning with LLMs. Mathematical and scien-
tific reasoning tasks have become a primary testbed to                 In this work, we explore how the establishment of premise
assess the capabilities of large language models (LLMs)                links improves the identification of errors in reasoning
(Hendrycks et al., 2021a; Arora et al., 2023; Wang et al.,             chains with LLMs. Our approach works in two steps. First,
2024). Solving these tasks requires complex planning, recall           we identify premises for each step and augment a linear rea-
of relevant formulae, and grounding the solution to the given          soning chain (LRC) to convert it into a Premise Augmented
problem (Arora et al., 2023). A widely adopted approach to             Reasoning Chain (PARC). And then verify each step in the
improve the reasoning of LLMs is to generate intermediate              PARC under its premises only. Lastly, we do a graph traver-
rationales, commonly known as chain-of-thought (CoT),                  sal to identify steps that are logically correct but have faulty
before predicting a final answer (Wei et al., 2023). Recent            premises to identify accumulation errors. In particular, we
work explores alternative structures for organizing these              are interested in the following research questions.
solutions, including Tree-of-Thoughts (Yao et al., 2023) and
                                                                       RQ 1 Given a sequential step-by-step answer to a math
Graph-of-Thoughts (Besta et al., 2024).
                                                                       word problem, can LLMs identify premises for each step?
                                                                       RQ 2 Given premise annotations, can LLMs identify errors
Evaluation of Chain-of-Thoughts. Although generating
                                                                       in reasoning more faithfully?
rationales can significantly improve model reasoning, sys-
tematically evaluating these explanations remains a chal-              RQ 3 Can LLMs perform the entire process end-to-end, i.e.,
lenge. Traditional metrics focused on word overlap or em-              given a reasoning chain, can they identify premises for each
bedding similarity (Celikyilmaz et al., 2021; Reiter, 2019)            step and detect errors?
fail to capture logical soundness, especially for step-by-step
deductions. To address this gap, methods such as ROSCOE                3.1. Premise Augmented Reasoning Chains (PARC)
(Golovneva et al., 2023), ReCEval (Prasad et al., 2023), and
Socreval (He et al., 2024) offer reference-free evaluation             Let q represent the question, 𝑎ˆ the predicted answer, 𝑎 the
frameworks that assess correctness and identify various cat-           ground truth answer, and r ≤t = [𝑠1 , 𝑠2 , . . . , 𝑠𝑡 ] the gener-
egories of errors. However, these methods generally provide            ated reasoning chain composed of 𝑡 intermediate steps 𝑠𝑖 ,
a single chain-level score and offer limited explainability,           leading to 𝑎.ˆ Using CoT reasoning, the predicted answer
making it difficult to pinpoint specific error types in individ-       𝑎ˆ is derived by first generating a reasoning chain r ≤t . The
ual reasoning steps. In contrast, our proposed framework               probability distribution for 𝑎ˆ can be expressed as:
provides a natural language characterization of the correct-
ness of each step, providing fine-grained insights into the                    PLM ( 𝑎ˆ | q) = PLM ( 𝑎ˆ | r ≤t ) × PLM (r ≤t | q),
precise nature of errors.
                                                                       where the reasoning chain r ≤t can be decomposed into in-
                                                                       termediate steps as:
Verifiers for Math Reasoning. Verifiers have proven ef-
fective in enhancing LLM-based reasoning. Uesato et al.                                                       𝑡 −1
                                                                                                              Ö
(2022) and Lightman et al. (2023) demonstrate that pro-                   PLM (r ≤t | q) = PLM (𝑠1 | q) ×            PLM (𝑠𝑖+1 | q, 𝑠𝑖 ).
viding reward signals for intermediate steps can stabilize                                                    𝑖=1

training and improve final performance. Deductive Beam                 Our objective is to identify errors in the intermediate steps
Search (Zhu et al., 2024) similarly incorporates a trained             𝑠𝑖 of the reasoning chain r ≤t .
verifier to refine model outputs during inference, leading to
higher accuracy for the final task. While these studies high-          The premises for a step s𝑖 are defined as the necessary and
light the benefits of verifiers, a clear strategy for training a       sufficient subset of prior steps, denoted as
robust verifier, one that generalizes across diverse problem
formats, remains elusive. The closest existing effort, Ling                                   P𝑖 ⊆ {𝑠 𝑗 ∀ 𝑗 < 𝑖},
et al. (2023), requires models to encode premises in a partic-
ular “natural program” style, which constrains applicability           satisfying the following properties:
to general chains-of-thought. In contrast, our method treats           1. Verifiability: The correctness of 𝑠𝑖 is verifiable based on
   1 Our code and data is available on https://github.com              P𝑖 alone:
/SagnikMukherjee/PARC                                                                         F (𝑠𝑖 | P𝑖 ) = 1.

                                                                   3
               Premise-Augmented Reasoning Chains Improve Error Identification in Math Reasoning with LLMs

2. Minimality: The set P𝑖 is minimal such that removing                      Algorithm 1 Constructing and Evaluating PARC
any element s 𝑗 ∈ P𝑖 results in 𝑠𝑖 becoming unverifiable:                      Input: 𝑅 = [𝑠1 , 𝑠2 , . . . , 𝑠𝑡 ]
                                                                               // Step 1: Premise Extraction
              F (𝑠𝑖 | P𝑖 \ {𝑠 𝑗 }) = 0,        ∀𝑠 𝑗 ∈ P𝑖 .         (1)         for 𝑘 = 1 to 𝑡 do
                                                                                  P𝑘 ← E XTRACT P REMISE (𝑠 𝑘 , {𝑠1 , . . . , 𝑠 𝑘−1 })
Given premises P𝑖 for a step s𝑖 , we convert a linear reason-                  end for
ing chain into a PARC, where each step s𝑖 is augmented                         𝑅 ′ ← [(𝑠1 , P1 ), . . . , (𝑠𝑡 , P𝑡 )]
with its premises P𝑖 . F is a function that estimates whether                  // Step 2: Error Detection
                                                                               for 𝑘 = 1 to 𝑡 do
a step is verifiable or not.                                                      E 𝑘(1) ← I S M ATHEMATICAL E RROR (𝑠 𝑘 )
          r ≤t ′ = [(𝑠1 , P1 ), (𝑠2 , P2 ), . . . , (𝑠𝑡 , P𝑡 )],                  E 𝑘(2) ← I S L OGICALLY I NCONSISTENT (𝑠 𝑘 , P𝑘 )
                                                                                  E 𝑘 ← E 𝑘(1) ∨ E 𝑘(2)
where r ≤t ′ represents the transformed reasoning chain.                       end for
                                                                               // Step 3: Accumulation Error Detection
                                                                               for 𝑘 = 1 to 𝑡 do
3.2. Progressive Premise Mapping                                                  if 𝑠 𝑘 is correct then
To transform a reasoning chain r ≤t = [𝑠1 , 𝑠2 , . . . , 𝑠𝑡 ] into a                  for 𝑠 𝑗 ∈ P𝑘 do
                                                                                         if 𝑠 𝑗 is incorrect then
premise-augmented reasoning chain (PARC), each step 𝑠𝑖                                      E 𝑘 ← ACCUMULATION E RROR
must be explicitly linked to its premises P𝑖 . We explore two                               break
approaches to identify these premises: Aggregative Premise                               end if
Mapping and Dyadic Premise Mapping.                                                   end for
                                                                                  end if
                                                                               end for
3.2.1. AGGREGATIVE P REMISE M APPING                                           𝑅 ′ ← [(𝑠1 , P1 , E1 ), . . . , (𝑠𝑡 , P𝑡 , E𝑡 )]
In the Aggregative approach, the premises for each step s 𝑘
are collectively identified by querying an LLM with the
complete reasoning context up to the step. For a given                       from issues such as incorrect mathematical calculations (de-
question q, the reasoning chain so far r<k , and the next step               fined as Mathematical Error), logical irregularities (defined
𝑠 𝑘 , the LLM is prompted to output P𝑘 .                                     as logical inconsistencies) and are evaluated independently
                                                                             of the broader reasoning context. Although significant, this
3.2.2. DYADIC P REMISE M APPING                                              focus on native errors tends to overlook another critical
In the Dyadic approach, the task of identifying premises is                  category of errors, called accumulation errors.
reformulated as a pairwise evaluation. Instead of querying                   An accumulation error occurs when a reasoning step is valid
the LLM to identify all premises P𝑘 for 𝑠 𝑘 at once, we                      in isolation but is built upon one or more erroneous premises
evaluate whether each individual step 𝑠𝑖 (where 𝑖 < 𝑘)                       from earlier steps. Unlike native errors, accumulation errors
serves as a valid premise for 𝑠 𝑘 . For each pair (𝑠𝑖 , 𝑠 𝑘 ), the           emerge from the compounding effects of prior inaccura-
LLM is queried to compute:                                                   cies, propagating through sequential steps. Formally, in the
                     (                                                       context of the reasoning chain, a step 𝑠𝑖 is classified as:
                       1, if 𝑠𝑖 is a valid premise for 𝑠 𝑘 ,
     I (𝑠 𝑘 | 𝑠𝑖 ) =                                                         1. Correct, if it contains no logical or mathematical errors,
                       0, otherwise.
                                                                             and is performed under premises that are also correct
The premises for 𝑠 𝑘 are then given by:
                                                                             2. A native error if it contains an inherent discrepancy (e.g.,
             P𝑘 = {𝑠𝑖 | F (𝑠 𝑘 | 𝑠𝑖 ) = 1, ∀𝑖 < 𝑘 }.                         a miscalculation or logical inconsistency)
                                                                             3. An accumulation error if 𝑠𝑖 is logically valid, but at least
3.3. Error Identification                                                    one of its premises is incorrect.
Next, we present our setup for error identification and how                  By addressing both native and accumulation errors, we can
premises play a significant role in this task. We introduce a                achieve a more comprehensive understanding of error dy-
taxonomy of error types that occur in math reasoning with                    namics in sequential reasoning processes.
LLMs and then describe our approach to identify them.
                                                                             3.3.2. E RROR I DENTIFICATION
3.3.1. T YPES OF E RROR
                                                                             Baseline. In the baseline approach, a large language
Traditionally, prior research has predominantly focused on                   model (LLM) is used in a zero-shot setting to classify the
identifying native errors, which refer to inaccuracies inher-                reasoning steps. For a given question q, the reasoning chain
ent to individual reasoning steps. These errors often arise                  so far 𝑟 <𝑘 , and the next step proposed 𝑠 𝑘 , the model is

                                                                         4
               Premise-Augmented Reasoning Chains Improve Error Identification in Math Reasoning with LLMs


      At constant temperature, the pressure of a sample of gas is inversely proportional to its volume. I have some hydrogen in a 3.67 liter container
      with a pressure of 4 kPa. If I move all of it to a 1.835 liter container at the same temperature, what will the new pressure be in kPa?

                                        Solution                                                 Baseline Verifier           Our Verifier
      Step 1: We can use the formula for inverse proportionality between pressure (P)
      and volume (V) of a gas at constant temperature, which is given by: P ∝ 1/V


      Step 2: We can rewrite this as an equation by introducing a constant of
      proportionality (k): P = k / V


      Step 3: Given that the initial pressure (P1) is 4 kPa and the initial volume (V1) is
      3.67 liters, we can write: P1 = k / V1, 4 = k / 3.67


      Step 4: To find the value of k, we can multiply both sides by 3.67: k = 4 * 3.67, k =
      14.68


      Step 5: Now that we have the value of k, we can use it to find the new pressure
      (P2) when the volume (V2) is 1.835 liters: P2 = k / V2, P2 = 14.68 / 1.835


                                                                                                                                          Mathematical
      Step 6: To find the new pressure, we can divide 14.68 by 1.835: P2 = 7.98 kPa
                                                                                                                                          Error


      Step 7: Therefore, the new pressure of the hydrogen in the 1.835 liter container                                                   Accumulation
      will be approximately 7.98 kPa.                                                                                                    Error


Figure 2. An example where the baseline method fails to detect errors, while our verification method with established premise links
successfully identifies the mathematical error in step 6, and the accumulation error in step 7.


queried to assign an error type E 𝑘 for 𝑠 𝑘 according to the                        3. Accumulation Error: After identifying native errors,
predefined error taxonomy (Correct / Mathematical Error /                           accumulation errors are identified by analyzing the depen-
Logical Error / Accumulation Error): The model processes                            dency graph of the reasoning chain. The premises P𝑘 form
the entire context (q, 𝑟 <𝑘 , 𝑠 𝑘 ) and generates a classification                  directed edges in the graph, where each step depends on
directly. The zero-shot prompt explicitly defines all error                         its premises. A Depth-First Search (DFS) traversal is per-
types to guide the classification.                                                  formed, and a step 𝑠 𝑘 is classified as an Accumulation Error
                                                                                    if it satisfies the following criteria: 1. 𝑠 𝑘 itself is classified
                                                                                    as correct, and 2. At least one premise 𝑠 𝑗 ∈ P𝑘 (where
Proposed Approach. Our proposed approach refines the                                𝑗 < 𝑘) is classified as incorrect.
classification process by situating each reasoning step s 𝑘
explicitly within the context of its premises P𝑘 . Algorithm
1 illustrates the overall pipeline of conversion of LRC to                          4. PERL: Premises and ERrors identification
PARC and step-by-step error classification. The prompts for                            in Language models
the following are reported in Appendix 16 and 17.                                   In order to test the ability of LLMs to identify premises and
                                                                                    error categories, we designed a testbed. We used existing
1. Mathematical Error: To detect mathematical errors,                               datasets of math word problems to create PERL, our testbed
we prompt an LLM to assess whether 𝑠 𝑘 contains a mathe-                            for step-level premise and error annotations.
matical error by analyzing the step in isolation, excluding
the broader reasoning chain.                                                        Generating Reasoning Chains: In order to generate the
                                                                                    reasoning chains, we used two popular benchmarks (i)
                                                                                    GSM8K (Cobbe et al., 2021), a collection of 8,500 grade
2. Logical Inconsistency: For the detection of logical                              school math word problems, and (ii) MATH (Hendrycks
inconsistencies, we restrict the evaluation to the premises P𝑘                      et al., 2021b), a dataset of 12,500 challenging competi-
of the reasoning step 𝑠 𝑘 . The LLM is prompted to determine                        tion level math word problems. In addition, we use the
whether 𝑠 𝑘 is logically consistent with its premises. This                         (iii) Orca-Math dataset by Mitra et al. (2024), a synthetic
ensures that the step’s validity is evaluated in the context                        dataset of 200K math problems alongside solutions written
of the dependencies defined by P𝑘 , without considering                             by GPT4Turbo, and the (iv) MetaMathQA dataset by (Yu
unrelated parts of the reasoning chain.                                             et al., 2023). We first randomly sampled 1000 examples

                                                                                5
              Premise-Augmented Reasoning Chains Improve Error Identification in Math Reasoning with LLMs

                                     GSM8K                             MATH                           Orca Math                       MetaMathQA
          Model Name
                           Precision    Recall     F1      Precision     Recall        F1      Precision     Recall     F1      Precision     Recall    F1
          Llama 3.1 8b       65.64      89.33    75.66      51.00        82.40        62.94     54.65        79.77    64.85      53.92        81.42    64.75
          Llama 3.1 70b      81.26      97.55    88.65      69.80        96.82        81.11     71.05        96.73    81.91      73.10        96.46    83.05
          Qwen 2.5 7b        67.42      63.53    65.36      55.87        59.73        57.70     63.08        72.64    67.05      55.54        61.66    58.14
          Qwen 2.5 32b       84.07      95.35    89.34      72.56        88.55        79.74     74.27        90.63    81.62      75.57        90.89    82.49
          GPT4o-mini         72.54      86.18    78.75      57.72        69.29        62.96     60.12        73.96    66.31      60.77        76.70    67.71
          GPT-4o             85.93      94.42    89.96      69.40        89.78        78.28     71.12        92.17    80.79      75.49        90.37    81.85

Table 1. Precision, Recall and F1 scores for premise identification under the Aggregative approach. Note that ideally this needs to be a
high recall system, because missing even a single premise step could hurt the verifiability of the reasoning chain.

                                                   Positives                          Negatives                  Synthetic Negatives
                          Model Name
                                         Precision      Recall    F1      Precision         Recall    F1      Precision      Recall    F1
                          GPT4o-mini
                          Aggregative      74.93        84.81    79.56      70.85           87.01    78.10      71.84        86.73    78.59
                            Dyadic         75.04        82.82    78.74      64.57           71.12    67.68      55.18        53.98    54.57
                           GPT4o
                          Aggregative      89.38        93.66    91.47      84.97           94.95    89.69      83.43        94.65    88.72
                            Dyadic         75.32        99.01    85.55      67.70           92.68    78.25      67.27        79.42    72.84

Table 2. Precision, Recall and F1 scores for the premise mapping task for the GSM8K dataset under the aggregative and dyadic approaches.
We saw a consistent drop in F1 score for the dyadic approach, in spite of it being computationally more expensive.


from the GSM8k and MATH test split and the Orca-Math                                   only 4 out of 71 had a discrepancy and 5 out of 71 had
and MetaMathQA training split (since these are training                                issues in error annotations. For premise identification, the
datasets). We began by using the open weight Large Lan-                                discrepancy typically indicates additional steps as premises.
guage Model Llama-3.1-8B-Instruct (Grattafiori et al., 2024)                           However, for error annotation, the annotation errors do not
to generate step-by-step reasoning chains. Next, we catego-                            have a clear pattern and manifest themselves in forms of
rized the reasoning chains as positive or negative, depending                          misclassification of the correctness of the step. The prompts
on whether the final answer matches the ground-truth an-                               used to generate the annotations of the premises and errors
swer. Next, we randomly sampled 50 positive (correct)                                  are in Appendix A.3. A detailed summary of the dataset
and 50 negative (incorrect) reasoning chains. To expand                                statistics can be found in Appendix A.2
our dataset, we employed GPT-4o to systematically intro-
duce mathematical or logical errors into the correct reason-                           5. Results and Discussion
ing chains, creating additional synthetic negative examples
(since prior work also focused on such synthetic negatives).                           For detailed information on our experimental setup, includ-
When introducing errors, we ensured that the subsequent                                ing model configurations and implementation details, refer
steps were appropriately modified to reflect the impact of                             to Appendix A.1.
the initial error. In contrast with existing works such as
Golovneva et al. (2023), where the perturbation in a step is                           5.1. Premise Mapping
not followed up in subsequent steps, our synthetic negatives
are more realistic.                                                                    In this section we try to answer RQ1 - “Can LLMs identify
                                                                                       premises to convert a Linear Reasoning Chain to a PARC?”
Premise and Error Annotation: Next, for each step in
the reasoning chain, we identified the ground truth premises                           Metrics: For identification of premises, we use precision,
for each step using the OpenAI o1-Preview model (OpenAI                                recall, and F1 score as metrics. However, we would want to
et al., 2024). Then, we use the same o1-Preview model                                  highlight to the reader that the most important metric here
to map each step to the predefined taxonomy of errors or                               is Recall. Since marking an extra step as a premise will not
mark it as correct, to create ground-truth error annotations.                          hurt the verifiability of the step, missing one will hurt its
Upon obtaining the annotated data sets, 2 authors manually                             verifiability and all subsequent steps that rely on this step as
went through 10% of the generated data points to identify                              a premise. Further, we note that some reasoning chains have
the discrepancy between the human annotations and the                                  a higher number of reasoning steps compared to others. In
annotations done by the o1 model. Manual inspection of                                 order to ensure robustness of the metrics, we first compute
71 samples showed that, in the case of premise annotations,                            them at the level of each data point and later average the

                                                                                  6
             Premise-Augmented Reasoning Chains Improve Error Identification in Math Reasoning with LLMs

metrics across the dataset. We tried two approaches for the           quite thin, and models often classify one as the other, so
task of premise mapping.                                              we merge these two error categories into a single error type
                                                                      Error, while keeping Accumulation Error separate. Further-
Aggregative Approach: Table 1 contains the results of                 more, since an early erroneous step for a solution containing
the Aggregative approach for a suite of models and datasets.          multiple steps could cause the number of errors to skew
From the table, it is evident that LLMs are efficient in iden-        toward accumulation errors, we first normalize the accuracy
tifying premises for a given step. In particular, Llama 3.1           by the number of steps in a datapoint, and later normalize
70b (Grattafiori et al., 2024), Qwen 2.5 32b (Qwen et al.,            across the dataset.
2025) and GPT4o are very efficient in this task, all having a
recall greater than 90%. It also shows that these models can
convert an LRC to a PARC with high accuracy.                          Results: Table 3 presents the experimental results for the
We note that the scale of the model is an important factor.           error identification task. We evaluate performance under
The increase in recall varies from 8.2% to 32.2% when                 two setups: under complete context as input (Full Context),
we scale up for the same model class, and the pattern is              on the other hand, the Model Premises setup denotes the
consistent. Tables 9, 10, 12 and 11 in the appendix contain           end-to-end approach, wherein the model is tasked with first
the detailed metrics across the splits Positive, Negative and         identifying the relevant premises and subsequently utilizing
Synthetic negatives for GSM8K, MATH, OrcaMath and                     them. All models are provided with the question and the
MetaMathQA respectively.                                              solutions generated up to the current step and are tasked
                                                                      with predicting the error type observed in the current step.
Dyadic Approach: Table 2 provides a comparative analy-                Premises Help Error Identification : It is evident from
sis of precision, recall, and F1 scores for the GSM8K dataset         Table 3, that providing only the premise steps as context (in-
using two models for the aggregative and dyadic approaches.           stead of providing the full context) improves the accuracy of
This approach causes the LLM to be more biased to mark                error detection with LLMs. Figure 2 shows one such exam-
a step as a premise, causing precision to drop significantly.         ple, where the baseline approach (using an LRC, and error
In addition, this approach has a time complexity of 𝑂 (𝑛2 ),          detection performed in the full context) could not identify
where 𝑛 is the number of reasoning steps. Note that for               errors, but our approach was able to successfully identify
almost all cases the precision drops, and the change in recall        the mathematical and accumulation errors. Our results show
gives a mixed view on how this approach might be helpful.             that the models are not as biased towards marking a step as
                                                                      correct, when given a more precise context (no distractor).
Our analysis revealed that this methodology often led the
                                                                      Hence, upon providing only the premises, identification of
model to incorrectly classify second- or higher-order de-
                                                                      errors becomes much more robust. However, it is important
pendencies as premises, even when the current step did not
                                                                      to note that this also comes at the cost of a drop of accuracy
directly rely on them. This misclassification contributed to
                                                                      for correct steps, this can be observed from comparing the
the observed degradation in precision.
                                                                      Pos column for Full context and Model Premises. However,
5.2. Error Identification                                             this accuracy drop is much smaller for larger models. In
In this section, we address RQ2 and RQ3, i.e. is error                addition, our approach impacts larger and more capable
identification more robust when we only use the premises              models more than smaller models.
for a given step as context. We explain the experimental              Models Struggle With Error Detection, Especially Accu-
setup for error identification for the baseline, as well as our       mulation Errors: We find that, while capable of identifying
approach, in the previous sections. For the identification of         correct steps, all models struggle with identifying errors.
errors under premises, we consider two settings. For the first        This can be attributed to the fact that models are inherently
one, we use the oracle premise annotation (from the ground            biased toward marking a step as correct. This issue was also
truth). For the second, we first identify the premises with           pointed out by Ling et al. (2023). Identifying errors with
the LLMs and then use those premises for the identification           directly connected premises as context yields significantly
of errors. Note that in the previous section we established           better performance than simply providing the full context.
that LLMs can identify premises with a high recall, and in            Moreover, models struggle to identify accumulation errors.
this experiment, we exploit that. The prompts we used for             Table 5 contains the accuracies across error types in the neg-
our experiments are shared in Appendix A.5.                           ative split of GSM8K. Note that, in full context, accuracy is
                                                                      quite high for correct steps, but lower for erroneous steps
Metrics: For this task, we report the average accuracy                (mathematical and logical errors), and significantly lower
for the identification of error types for each step. In our           for accumulation errors. However, in our approach, the
analysis, we observe that the boundaries between the error            identification of errors becomes significantly robust, with a
types Mathematical Error and Logical Inconsistency are                minor drop in performance in identifying correct steps.

                                                                  7
               Premise-Augmented Reasoning Chains Improve Error Identification in Math Reasoning with LLMs

                               GSM8K                               MATH                            Orca Math                          MetaMathQA
  Model
                     Neg      Syn      Pos      Avg     Neg      Syn     Pos       Avg     Neg     Syn       Pos     Avg      Neg      Syn     Pos      Avg
  Llama 3.1 8b
  Full Context   48.87 57.68          91.9     58.6 46.91 60.29          90.61      60.2   43.26    51.2      96.7   55.06   50.47     55.15   95.17   59.45
  Model Premises 54.61 76.74          65.44    64.53 52.16 59.83         50.96     54.88   55.57   59.82     67.36   59.22   54.52     69.13   62.63   61.78
  Llama 3.1 70b
  Full Context   58.35 77.03 98.61 71.37 55.55 72.83                     96.24     69.77   50.33   64.25     96.74   63.52   55.59     73.13   97.93   69.49
  Model Premises 74.51 86.22 94.69 81.92 70.94 79.29                     77.91     75.45   64.95   72.28     93.37   72.52   65.69     82.74   89.71   76.52
  Qwen 2.5 7b
  Full Context   40.88 54.13           100 54.94        40.47    53.60   98.07     56.26   41.20   53.69      100    55.85   43.36     53.18   99.39 56.26
  Model Premises 53.03 78.40          90.37 69.73       58.47    66.87   82.72     65.96   52.07   71.12     84.28   65.38   54.98     73.87   91.02 68.43
  Qwen 2.5 32b
  Full Context   46.76 69.26          99.8 63.56        49.58     66.5    98   65.11       49.44   63.01      99.5   63.06    49.7      67.8    99.6   65.02
  Model Premises 65.58 86.34          96.95 79.37       68.61    76.96   88.71 75.57       61.89   69.24     95.25   70.26   62.18     85.60   97.32   77.40
  Qwen 2.5 72b
  Full Context   47.48 67.17           100 63.11        53.19    67.87   99.79 67.52       50.41   60.33      100    62.50   47.31     63.59   99.05 62.20
  Model Premises 69.87 85.12          96.38 80.56       69.51    79.92   90.84 77.28       69.45   71.34     94.19   74.41   64.73     85.52   98.12 78.53
  GPT4o-mini
  Full Context   52.68 73.14 95.02 66.68 50.41 62.39                      93.4     63.03   55.22   61.18      98.6   64.59   51.52     65.42   97.35   64.47
  Model Premises 58.25 80.81 86.72 72.33 65.84 72.4                      71.88     69.45   61.18   72.48     85.94   69.93   57.04     81.63   91.15   72.51
  GPT-4o
  Full Context   53.81        75.3 98.33 68.52          50.9 68.41       98.57 66.52       59.55   65.75      100    68.55   56.26     71.72    99.3   69.41
  Model Premises 65.23        86.67 99.76 79.82         70.12 76.67      91.84 76.45       66.33   71.74     93.14   72.96   67.28     88.19   89.85   79.41

Table 3. Accuracy for Error identification of various models under Full Context (baseline) and Premises settings across different datasets.
Note that Neg, Syn and Pos means Negative, Synthetic Negatives and Positive splits of PERL, as explained earlier. For each dataset, we
highlighted the models that benefit the most from the PARC.

   Model             GSM8K       MATH         Orca-Math    MetaMath                        Model               Correct     Error     Acc. Error   Avg
   Llama 3.1 70b                                                                           Llama 3.1 70b
   Oracle Premises    81.46         74.68       73.45           76.05                      Full Context         96.79      60.87        12        58.35
   Model Premises     81.92         75.45       72.52           76.52                      Oracle Premises      90.18      75.25       55.63      74.41
                                                                                           Model Premises       88.78      75.25       57.54      74.51
   Qwen 2.5 72b
   Oracle Premises    80.58         79.50       74.87           79.49                      GPT-4o
   Model Premises     80.56         77.28       74.41           78.53                      Full Context         95.75       48.2        13.2      53.81
                                                                                           Oracle Premises      96.83      60.02       41.79      67.03
   GPT-4o                                                                                  Model Premises       94.15      55.13       44.91      65.23
   Oracle Premises    78.74         76.79       75.56           82.88
   Model Premises     79.82         76.45       72.96           79.41
                                                                                   Table 5. Error identification accuracy for each type of steps in
Table 4. Comparison of Error identification under oracle premises                  ground truth. Acc. Error means Accumulation Errors
vs model generated premises. Since these models have high recall
in premise identification, we observe that the error identification                the accuracy of error identification improves when oracle
accuracy is comparable.                                                            premises are provided. However, it is noteworthy that for
                                                                                   most models, the performance remains comparable to that
                                                                                   achieved with oracle premises. This can be attributed to the
Synthetic Negatives are Easier: The average performance
                                                                                   fact that all these models can identify premises with a recall
of all models on synthetically generated negatives is consis-
                                                                                   of higher than 90.
tently higher compared to the performance on true negatives
(evident from comparing the Neg and Syn columns in Table
3). This observation highlights an important insight: per-                         5.3. Experiments on ProcessBench
turbing reasoning chains does not serve as a reliable proxy                        Beyond the PERL dataset, we also evaluate our framework
for evaluating a model’s ability to identify genuine errors in                     on ProcessBench (Zheng et al., 2024), a benchmark that
reasoning. While prior work has focused on such synthetic                          contains human-annotated stepwise labels for mathemati-
negatives, it might provide an overoptimistic view of LLMs’                        cal solutions. Unlike PERL, ProcessBench only includes
ability to detect errors.                                                          annotations up to the first incorrect step in each solution.
Oracle Premises vs Model Generated Premises: In Table
4, we present results of an ablation, where instead of provid-                     Experimental Setup. We focus on the step-level error
ing the model generated premises, we provide the ground                            identification task, following the protocol used by Zheng
truth premises (oracle premises from PERL). As anticipated,                        et al. (2024). Specifically, for correct solutions (i.e., ones

                                                                               8
              Premise-Augmented Reasoning Chains Improve Error Identification in Math Reasoning with LLMs

    Model           Method     Correct   Wrong   F1     Delta         iments with our annotated dataset, PERL, we empirically
    Qwen 2.5 7B     Baseline    66.3      36.7   47.2                 show that error identification under premises in PARC is
                     Ours       60.1      38.6   47.0   -0.2          more reliable and has higher accuracy than error identifica-
    Qwen 2.5 32B    Baseline    97.9      43.0   59.8                 tion under full context in LRC. We also show that LLMs
                     Ours       95.9      55.1   70.0 +10.2           can convert an LRC to PARC with no additional guidance,
    Qwen 2.5 72B    Baseline    98.4      61.4   75.6                 and then can do error identification under the premises in
                     Ours       97.8      59.7   74.1   -1.5          PARC. Further, we show that accumulation errors are partic-
    Llama 3.1 8B    Baseline    17.1      36.7   23.3                 ularly challenging to detect, and our method improves their
                     Ours       33.7      37.8   35.6 +12.3
                                                                      identification by verifying each step under its premises.
    Llama 3.1 70B   Baseline    77.7      57.5   66.1
                     Ours       89.6      70.0   78.6 +12.5
                                                                      Acknowledgments
Table 6. Performance comparison on the GSM8K split of Process-
Bench with Baseline vs. PARC (Ours implies premise augmented          This research project has benefited from the Microsoft Ac-
verification) for various model.                                      celerate Foundation Models Research (AFMR) grant pro-
                                                                      gram through which leading foundation models hosted by
    Model           Method     Correct   Wrong   F1     Delta
                                                                      Microsoft Azure along with access to Azure credits were
    Qwen 2.5 7B     Baseline    46.0      25.4   32.7                 provided to conduct the research.
                     Ours       45.6      41.2   43.3 +10.6
    Qwen 2.5 32B    Baseline    90.0      22.4   35.9
                     Ours       86.9      53.9   66.5 +30.7           Impact Statement
    Qwen 2.5 72B    Baseline    88.5      33.7   48.8
                     Ours       86.7      53.9   66.5 +17.7           The broader impact of this research extends to multiple do-
                                                                      mains where step-by-step reasoning is critical, including
    Llama 3.1 8B    Baseline     5.6      19.1    8.7
                     Ours       11.0      27.5   15.7   +7.1          automated theorem proving, educational AI tutors, and sci-
    Llama 3.1 70B   Baseline    32.4      32.8   32.6
                                                                      entific discovery. By enabling more reliable self-verification
                     Ours       61.6      55.4   58.3 +25.7           mechanisms in LLMs, our approach contributes to the long-
                                                                      term goal of enhancing the transparency and trustworthiness
Table 7. Performance comparison on the MATH split of Process-         of AI systems in high-stakes applications.
Bench with Baseline vs. PARC (Ours implies premise augmented
verification) for various model.                                      Potential ethical considerations include the risk of overre-
                                                                      liance on LLM-generated verification without human over-
where the final answer is correct), every step is marked              sight, particularly in domains where reasoning errors can
as correct. For incorrect solutions, the task is to identify          have significant real-world consequences.
the first incorrect step in the chain; all subsequent steps are       This paper primarily aims to advance the field of Machine
automatically deemed irrelevant by design of the benchmark.           Learning by proposing a structured approach to reasoning
We adopt the same prompting strategy as in our previous               evaluation. Although we acknowledge that any advances
experiments, with LLMs classifying each step as correct               in LLM-based reasoning may have broader societal impli-
or incorrect. The baseline is a standard critic model as              cations, we do not foresee any immediate ethical concerns
proposed by (Zheng et al., 2024) that identifies the first            beyond those generally associated with the development of
erroneous step from the solution as a whole.                          AI reasoning systems.

Results and Observations. Tables 6 and 7 show that                    References
our findings on ProcessBench (on the GSM8K and MATH
splits) align with the trends we observe on PERL. Premise-            Ahn, J., Verma, R., Lou, R., Liu, D., Zhang, R., and Yin,
augmented verification continues to outperform verification            W. Large language models for mathematical reasoning:
conducted in the full reasoning chain. We see consistent                Progresses and challenges, 2024. URL https://ar
gains from evaluating each step under its extracted premises           xiv.org/abs/2402.00157.
and classifying its correctness accordingly. This further
strenghtens our previous findings.                                    Arora, D., Singh, H., and Mausam. Have LLMs advanced
6. Conclusion                                                           enough? a challenging problem solving benchmark for
                                                                        large language models. In Bouamor, H., Pino, J., and
In this paper, we introduced a framework to enhance the                 Bali, K. (eds.), Proceedings of the 2023 Conference on
evaluation of mathematical reasoning chains in large lan-               Empirical Methods in Natural Language Processing, pp.
guage models by transforming Linear Reasoning Chains                    7527–7543, Singapore, December 2023. Association for
into Premise Augmented Reasoning Chains. Through exper-                 Computational Linguistics. doi: 10.18653/v1/2023.emn

                                                                  9
             Premise-Augmented Reasoning Chains Improve Error Identification in Math Reasoning with LLMs

  lp-main.468. URL https://aclanthology.org                        C., McConnell, C., Keller, C., Touret, C., Wu, C., Wong,
  /2023.emnlp-main.468.                                            C., Ferrer, C. C., Nikolaidis, C., Allonsius, D., Song, D.,
                                                                   Pintz, D., Livshits, D., Wyatt, D., Esiobu, D., Choudhary,
Besta, M., Blach, N., Kubicek, A., Gerstenberger, R., Pod-         D., Mahajan, D., Garcia-Olano, D., Perino, D., Hupkes,
  stawski, M., Gianinazzi, L., Gajda, J., Lehmann, T.,             D., Lakomkin, E., AlBadawy, E., Lobanova, E., Dinan,
  Niewiadomski, H., Nyczyk, P., and Hoefler, T. Graph              E., Smith, E. M., Radenovic, F., Guzmán, F., Zhang, F.,
  of thoughts: Solving elaborate problems with large lan-          Synnaeve, G., Lee, G., Anderson, G. L., Thattai, G., Nail,
  guage models. Proceedings of the AAAI Conference on              G., Mialon, G., Pang, G., Cucurell, G., Nguyen, H., Ko-
  Artificial Intelligence, 38(16):17682–17690, March 2024.         revaar, H., Xu, H., Touvron, H., Zarov, I., Ibarra, I. A.,
  ISSN 2159-5399. doi: 10.1609/aaai.v38i16.29720. URL              Kloumann, I., Misra, I., Evtimov, I., Zhang, J., Copet, J.,
  http://dx.doi.org/10.1609/aaai.v38i16                            Lee, J., Geffert, J., Vranes, J., Park, J., Mahadeokar, J.,
  .29720.                                                          Shah, J., van der Linde, J., Billock, J., Hong, J., Lee, J.,
Celikyilmaz, A., Clark, E., and Gao, J. Evaluation of text         Fu, J., Chi, J., Huang, J., Liu, J., Wang, J., Yu, J., Bitton,
  generation: A survey, 2021. URL https://arxiv.                   J., Spisak, J., Park, J., Rocca, J., Johnstun, J., Saxe, J., Jia,
  org/abs/2006.14799.                                              J., Alwala, K. V., Prasad, K., Upasani, K., Plawiak, K., Li,
                                                                   K., Heafield, K., Stone, K., El-Arini, K., Iyer, K., Malik,
Cobbe, K., Kosaraju, V., Bavarian, M., Chen, M., Jun, H.,          K., Chiu, K., Bhalla, K., Lakhotia, K., Rantala-Yeary,
  Kaiser, L., Plappert, M., Tworek, J., Hilton, J., Nakano,        L., van der Maaten, L., Chen, L., Tan, L., Jenkins, L.,
  R., Hesse, C., and Schulman, J. Training verifiers to solve      Martin, L., Madaan, L., Malo, L., Blecher, L., Landzaat,
  math word problems, 2021. URL https://arxiv.                     L., de Oliveira, L., Muzzi, M., Pasupuleti, M., Singh,
  org/abs/2110.14168.                                              M., Paluri, M., Kardas, M., Tsimpoukelli, M., Oldham,
                                                                   M., Rita, M., Pavlova, M., Kambadur, M., Lewis, M.,
Daheim, N., Macina, J., Kapur, M., Gurevych, I., and
                                                                   Si, M., Singh, M. K., Hassan, M., Goyal, N., Torabi, N.,
  Sachan, M. Stepwise verification and remediation of
                                                                   Bashlykov, N., Bogoychev, N., Chatterji, N., Zhang, N.,
  student reasoning errors with large language model tu-
                                                                   Duchenne, O., Çelebi, O., Alrassy, P., Zhang, P., Li, P.,
  tors, 2024. URL https://arxiv.org/abs/2407
                                                                   Vasic, P., Weng, P., Bhargava, P., Dubal, P., Krishnan,
  .09136.
                                                                   P., Koura, P. S., Xu, P., He, Q., Dong, Q., Srinivasan,
Gao, Q., Thattai, G., Shakiah, S., Gao, X., Pansare, S.,           R., Ganapathy, R., Calderer, R., Cabral, R. S., Stojnic,
  Sharma, V., Sukhatme, G., Shi, H., Yang, B., Zhang,              R., Raileanu, R., Maheswari, R., Girdhar, R., Patel, R.,
  D., Hu, L., Arumugam, K., Hu, S., Wen, M., Guthy, D.,            Sauvestre, R., Polidoro, R., Sumbaly, R., Taylor, R., Silva,
  Chung, S., Khanna, R., Ipek, O., Ball, L., Bland, K.,            R., Hou, R., Wang, R., Hosseini, S., Chennabasappa, S.,
  Rocker, H., Johnston, M., Ghanadan, R., Hakkani-Tur,             Singh, S., Bell, S., Kim, S. S., Edunov, S., Nie, S., Narang,
  D., and Natarajan, P. Alexa arena: A user-centric inter-         S., Raparthy, S., Shen, S., Wan, S., Bhosale, S., Zhang,
  active platform for embodied ai. In Oh, A., Naumann,             S., Vandenhende, S., Batra, S., Whitman, S., Sootla, S.,
  T., Globerson, A., Saenko, K., Hardt, M., and Levine, S.         Collot, S., Gururangan, S., Borodinsky, S., Herman, T.,
  (eds.), Advances in Neural Information Processing Sys-           Fowler, T., Sheasha, T., Georgiou, T., Scialom, T., Speck-
  tems, volume 36, pp. 19170–19194. Curran Associates,             bacher, T., Mihaylov, T., Xiao, T., Karn, U., Goswami, V.,
  Inc., 2023. URL https://proceedings.neurip                       Gupta, V., Ramanathan, V., Kerkez, V., Gonguet, V., Do,
  s.cc/paper_files/paper/2023/file/3d0                             V., Vogeti, V., Albiero, V., Petrovic, V., Chu, W., Xiong,
  758f0b95e19abc68c1c8070d36510-Paper-                             W., Fu, W., Meers, W., Martinet, X., Wang, X., Wang,
  Datasets_and_Benchmarks.pdf.                                     X., Tan, X. E., Xia, X., Xie, X., Jia, X., Wang, X., Gold-
                                                                   schlag, Y., Gaur, Y., Babaei, Y., Wen, Y., Song, Y., Zhang,
Golovneva, O., Chen, M., Poff, S., Corredor, M., Zettle-           Y., Li, Y., Mao, Y., Coudert, Z. D., Yan, Z., Chen, Z.,
  moyer, L., Fazel-Zarandi, M., and Celikyilmaz, A.                Papakipos, Z., Singh, A., Srivastava, A., Jain, A., Kelsey,
  Roscoe: A suite of metrics for scoring step-by-step rea-         A., Shajnfeld, A., Gangidi, A., Victoria, A., Goldstand,
  soning, 2023. URL https://arxiv.org/abs/22                       A., Menon, A., Sharma, A., Boesenberg, A., Baevski, A.,
 12.07919.                                                         Feinstein, A., Kallet, A., Sangani, A., Teo, A., Yunus, A.,
Grattafiori, A., Dubey, A., Jauhri, A., Pandey, A., Kadian,        Lupu, A., Alvarado, A., Caples, A., Gu, A., Ho, A., Poul-
  A., Al-Dahle, A., Letman, A., Mathur, A., Schelten, A.,          ton, A., Ryan, A., Ramchandani, A., Dong, A., Franco,
  Vaughan, A., Yang, A., Fan, A., Goyal, A., Hartshorn,            A., Goyal, A., Saraf, A., Chowdhury, A., Gabriel, A.,
  A., Yang, A., Mitra, A., Sravankumar, A., Korenev,               Bharambe, A., Eisenman, A., Yazdan, A., James, B.,
  A., Hinsvark, A., Rao, A., Zhang, A., Rodriguez, A.,             Maurer, B., Leonhardi, B., Huang, B., Loyd, B., Paola,
  Gregerson, A., Spataru, A., Roziere, B., Biron, B., Tang,        B. D., Paranjape, B., Liu, B., Wu, B., Ni, B., Hancock,
  B., Chern, B., Caucheteux, C., Nayak, C., Bi, C., Marra,         B., Wasti, B., Spence, B., Stojkovic, B., Gamido, B.,

                                                              10
           Premise-Augmented Reasoning Chains Improve Error Identification in Math Reasoning with LLMs

Montalvo, B., Parker, C., Burton, C., Mejia, C., Liu, C.,            Qi, Y., Li, Y., Zhang, Y., Zhang, Y., Adi, Y., Nam, Y., Yu,
Wang, C., Kim, C., Zhou, C., Hu, C., Chu, C.-H., Cai, C.,            Wang, Zhao, Y., Hao, Y., Qian, Y., Li, Y., He, Y., Rait,
Tindal, C., Feichtenhofer, C., Gao, C., Civin, D., Beaty,            Z., DeVito, Z., Rosnbrick, Z., Wen, Z., Yang, Z., Zhao,
D., Kreymer, D., Li, D., Adkins, D., Xu, D., Testuggine,             Z., and Ma, Z. The llama 3 herd of models, 2024. URL
D., David, D., Parikh, D., Liskovich, D., Foss, D., Wang,            https://arxiv.org/abs/2407.21783.
D., Le, D., Holland, D., Dowling, E., Jamil, E., Mont-
gomery, E., Presani, E., Hahn, E., Wood, E., Le, E.-T.,            Han, S., Schoelkopf, H., Zhao, Y., Qi, Z., Riddell, M., Zhou,
Brinkman, E., Arcaute, E., Dunbar, E., Smothers, E., Sun,            W., Coady, J., Peng, D., Qiao, Y., Benson, L., Sun, L.,
F., Kreuk, F., Tian, F., Kokkinos, F., Ozgenel, F., Cag-             Wardle-Solano, A., Szabo, H., Zubova, E., Burtell, M.,
gioni, F., Kanayet, F., Seide, F., Florez, G. M., Schwarz,           Fan, J., Liu, Y., Wong, B., Sailor, M., Ni, A., Nan, L.,
G., Badeer, G., Swee, G., Halpern, G., Herman, G., Sizov,            Kasai, J., Yu, T., Zhang, R., Fabbri, A. R., Kryscinski, W.,
G., Guangyi, Zhang, Lakshminarayanan, G., Inan, H.,                  Yavuz, S., Liu, Y., Lin, X. V., Joty, S., Zhou, Y., Xiong,
Shojanazeri, H., Zou, H., Wang, H., Zha, H., Habeeb, H.,             C., Ying, R., Cohan, A., and Radev, D. Folio: Natural
Rudolph, H., Suk, H., Aspegren, H., Goldman, H., Zhan,               language reasoning with first-order logic, 2024. URL
H., Damlaj, I., Molybog, I., Tufanov, I., Leontiadis, I.,            https://arxiv.org/abs/2209.00840.
Veliche, I.-E., Gat, I., Weissman, J., Geboski, J., Kohli,         He, H., Zhang, H., and Roth, D. Socreval: Large language
J., Lam, J., Asher, J., Gaya, J.-B., Marcus, J., Tang, J.,           models with the socratic method for reference-free rea-
Chan, J., Zhen, J., Reizenstein, J., Teboul, J., Zhong, J.,          soning evaluation, 2024. URL https://arxiv.or
Jin, J., Yang, J., Cummings, J., Carvill, J., Shepard, J.,           g/abs/2310.00074.
McPhie, J., Torres, J., Ginsburg, J., Wang, J., Wu, K., U,
K. H., Saxena, K., Khandelwal, K., Zand, K., Matosich,             Hendrycks, D., Burns, C., Basart, S., Zou, A., Mazeika,
K., Veeraraghavan, K., Michelena, K., Li, K., Jagadeesh,             M., Song, D., and Steinhardt, J. Measuring massive
K., Huang, K., Chawla, K., Huang, K., Chen, L., Garg,                multitask language understanding, 2021a. URL https:
L., A, L., Silva, L., Bell, L., Zhang, L., Guo, L., Yu, L.,         //arxiv.org/abs/2009.03300.
Moshkovich, L., Wehrstedt, L., Khabsa, M., Avalani, M.,
Bhatt, M., Mankus, M., Hasson, M., Lennie, M., Reso,               Hendrycks, D., Burns, C., Kadavath, S., Arora, A., Basart,
M., Groshev, M., Naumov, M., Lathi, M., Keneally, M.,                S., Tang, E., Song, D., and Steinhardt, J. Measuring math-
Liu, M., Seltzer, M. L., Valko, M., Restrepo, M., Patel,             ematical problem solving with the math dataset. NeurIPS,
M., Vyatskov, M., Samvelyan, M., Clark, M., Macey,                   2021b.
M., Wang, M., Hermoso, M. J., Metanat, M., Rastegari,
                                                                   Huang, J. and Chang, K. C.-C. Towards reasoning in large
M., Bansal, M., Santhanam, N., Parks, N., White, N.,
                                                                     language models: A survey, 2023. URL https://ar
Bawa, N., Singhal, N., Egebo, N., Usunier, N., Mehta,
                                                                    xiv.org/abs/2212.10403.
N., Laptev, N. P., Dong, N., Cheng, N., Chernoguz, O.,
Hart, O., Salpekar, O., Kalinli, O., Kent, P., Parekh, P.,         Imani, S., Du, L., and Shrivastava, H. MathPrompter:
Saab, P., Balaji, P., Rittner, P., Bontrager, P., Roux, P.,          Mathematical reasoning using large language models.
Dollar, P., Zvyagina, P., Ratanchandani, P., Yuvraj, P.,             In Sitaram, S., Beigman Klebanov, B., and Williams,
Liang, Q., Alao, R., Rodriguez, R., Ayub, R., Murthy, R.,            J. D. (eds.), Proceedings of the 61st Annual Meeting of
Nayani, R., Mitra, R., Parthasarathy, R., Li, R., Hogan,             the Association for Computational Linguistics (Volume
R., Battey, R., Wang, R., Howes, R., Rinott, R., Mehta,              5: Industry Track), pp. 37–42, Toronto, Canada, July
S., Siby, S., Bondu, S. J., Datta, S., Chugh, S., Hunt, S.,          2023. Association for Computational Linguistics. doi:
Dhillon, S., Sidorov, S., Pan, S., Mahajan, S., Verma,               10.18653/v1/2023.acl-industry.4. URL https://ac
S., Yamamoto, S., Ramaswamy, S., Lindsay, S., Lindsay,               lanthology.org/2023.acl-industry.4/.
S., Feng, S., Lin, S., Zha, S. C., Patil, S., Shankar, S.,
Zhang, S., Zhang, S., Wang, S., Agarwal, S., Sajuyigbe,            Jiang, J., Wang, F., Shen, J., Kim, S., and Kim, S. A survey
S., Chintala, S., Max, S., Chen, S., Kehoe, S., Satter-               on large language models for code generation, 2024. URL
field, S., Govindaprasad, S., Gupta, S., Deng, S., Cho,               https://arxiv.org/abs/2406.00515.
S., Virk, S., Subramanian, S., Choudhury, S., Goldman,
S., Remez, T., Glaser, T., Best, T., Koehler, T., Robinson,        Kwon, W., Li, Z., Zhuang, S., Sheng, Y., Zheng, L., Yu,
T., Li, T., Zhang, T., Matthews, T., Chou, T., Shaked,              C. H., Gonzalez, J. E., Zhang, H., and Stoica, I. Efficient
T., Vontimitta, V., Ajayi, V., Montanez, V., Mohan, V.,             memory management for large language model serving
Kumar, V. S., Mangla, V., Ionescu, V., Poenaru, V., Mi-             with pagedattention, 2023. URL https://arxiv.or
hailescu, V. T., Ivanov, V., Li, W., Wang, W., Jiang, W.,           g/abs/2309.06180.
Bouaziz, W., Constable, W., Tang, X., Wu, X., Wang, X.,            Lightman, H., Kosaraju, V., Burda, Y., Edwards, H., Baker,
Wu, X., Gao, X., Kleinman, Y., Chen, Y., Hu, Y., Jia, Y.,            B., Lee, T., Leike, J., Schulman, J., Sutskever, I., and

                                                              11
             Premise-Augmented Reasoning Chains Improve Error Identification in Math Reasoning with LLMs

  Cobbe, K. Let’s verify step by step, 2023. URL https:                  Ahmad, L., Yang, L., Liu, L., Maksin, L., Ho, L., Fedus,
  //arxiv.org/abs/2305.20050.                                            L., Weng, L., Li, L., McCallum, L., Held, L., Kuhn, L.,
                                                                         Kondraciuk, L., Kaiser, L., Metz, L., Boyd, M., Trebacz,
Ling, Z., Fang, Y., Li, X., Huang, Z., Lee, M., Memisevic,               M., Joglekar, M., Chen, M., Tintor, M., Meyer, M., Jones,
  R., and Su, H. Deductive verification of chain-of-thought              M., Kaufer, M., Schwarzer, M., Shah, M., Yatbaz, M.,
  reasoning, 2023. URL https://arxiv.org/abs/                            Guan, M. Y., Xu, M., Yan, M., Glaese, M., Chen, M.,
  2306.03872.                                                            Lampe, M., Malek, M., Wang, M., Fradin, M., McClay,
                                                                         M., Pavlov, M., Wang, M., Wang, M., Murati, M., Bavar-
Mitra, A., Khanpour, H., Rosset, C., and Awadallah, A.
                                                                         ian, M., Rohaninejad, M., McAleese, N., Chowdhury,
 Orca-math: Unlocking the potential of slms in grade
                                                                         N., Chowdhury, N., Ryder, N., Tezak, N., Brown, N.,
 school math, 2024. URL https://arxiv.org/ab
                                                                         Nachum, O., Boiko, O., Murk, O., Watkins, O., Chao, P.,
 s/2402.14830.
                                                                         Ashbourne, P., Izmailov, P., Zhokhov, P., Dias, R., Arora,
Moura, L. d. and Ullrich, S. The lean 4 theorem prover and               R., Lin, R., Lopes, R. G., Gaon, R., Miyara, R., Leike, R.,
 programming language. In Platzer, A. and Sutcliffe, G.                  Hwang, R., Garg, R., Brown, R., James, R., Shu, R., Cheu,
 (eds.), Automated Deduction – CADE 28, pp. 625–635,                     R., Greene, R., Jain, S., Altman, S., Toizer, S., Toyer, S.,
 Cham, 2021. Springer International Publishing. ISBN                     Miserendino, S., Agarwal, S., Hernandez, S., Baker, S.,
 978-3-030-79876-5.                                                      McKinney, S., Yan, S., Zhao, S., Hu, S., Santurkar, S.,
                                                                         Chaudhuri, S. R., Zhang, S., Fu, S., Papay, S., Lin, S., Bal-
Murphy, L., Yang, K., Sun, J., Li, Z., Anandkumar, A., and               aji, S., Sanjeev, S., Sidor, S., Broda, T., Clark, A., Wang,
 Si, X. Autoformalizing euclidean geometry, 2024. URL                    T., Gordon, T., Sanders, T., Patwardhan, T., Sottiaux, T.,
 https://arxiv.org/abs/2405.17216.                                       Degry, T., Dimson, T., Zheng, T., Garipov, T., Stasi, T.,
                                                                         Bansal, T., Creech, T., Peterson, T., Eloundou, T., Qi, V.,
OpenAI. Openai o1 system card. Technical report, Decem-                  Kosaraju, V., Monaco, V., Pong, V., Fomenko, V., Zheng,
  ber 2024. URL https://cdn.openai.com/o1-                               W., Zhou, W., McCabe, W., Zaremba, W., Dubois, Y., Lu,
  system-card-20241205.pdf.                                              Y., Chen, Y., Cha, Y., Bai, Y., He, Y., Zhang, Y., Wang, Y.,
OpenAI, :, Jaech, A., Kalai, A., Lerer, A., Richardson, A.,              Shao, Z., and Li, Z. Openai o1 system card, 2024. URL
  El-Kishky, A., Low, A., Helyar, A., Madry, A., Beu-                    https://arxiv.org/abs/2412.16720.
  tel, A., Carney, A., Iftimie, A., Karpenko, A., Passos,              Philipov, D., Dongre, V., Tur, G., and Hakkani-Tür, D. Sim-
 A. T., Neitz, A., Prokofiev, A., Wei, A., Tam, A., Bennett,             ulating user agents for embodied conversational-ai, 2024.
 A., Kumar, A., Saraiva, A., Vallone, A., Duberstein, A.,                URL https://arxiv.org/abs/2410.23535.
  Kondrich, A., Mishchenko, A., Applebaum, A., Jiang, A.,
  Nair, A., Zoph, B., Ghorbani, B., Rossen, B., Sokolowsky,            Prasad, A., Saha, S., Zhou, X., and Bansal, M. Receval:
  B., Barak, B., McGrew, B., Minaiev, B., Hao, B., Baker,                Evaluating reasoning chains via correctness and informa-
  B., Houghton, B., McKinzie, B., Eastman, B., Lugaresi,                 tiveness, 2023. URL https://arxiv.org/abs/
  C., Bassin, C., Hudson, C., Li, C. M., de Bourcy, C., Voss,            2304.10703.
  C., Shen, C., Zhang, C., Koch, C., Orsinger, C., Hesse,
  C., Fischer, C., Chan, C., Roberts, D., Kappler, D., Levy,           Qwen, :, Yang, A., Yang, B., Zhang, B., Hui, B., Zheng,
  D., Selsam, D., Dohan, D., Farhi, D., Mely, D., Robinson,             B., Yu, B., Li, C., Liu, D., Huang, F., Wei, H., Lin, H.,
  D., Tsipras, D., Li, D., Oprica, D., Freeman, E., Zhang,              Yang, J., Tu, J., Zhang, J., Yang, J., Yang, J., Zhou, J.,
  E., Wong, E., Proehl, E., Cheung, E., Mitchell, E., Wal-              Lin, J., Dang, K., Lu, K., Bao, K., Yang, K., Yu, L.,
  lace, E., Ritter, E., Mays, E., Wang, F., Such, F. P., Raso,          Li, M., Xue, M., Zhang, P., Zhu, Q., Men, R., Lin, R.,
  F., Leoni, F., Tsimpourlas, F., Song, F., von Lohmann,                Li, T., Tang, T., Xia, T., Ren, X., Ren, X., Fan, Y., Su,
  F., Sulit, F., Salmon, G., Parascandolo, G., Chabot, G.,              Y., Zhang, Y., Wan, Y., Liu, Y., Cui, Z., Zhang, Z., and
  Zhao, G., Brockman, G., Leclerc, G., Salman, H., Bao,                 Qiu, Z. Qwen2.5 technical report, 2025. URL https:
  H., Sheng, H., Andrin, H., Bagherinezhad, H., Ren, H.,                //arxiv.org/abs/2412.15115.
  Lightman, H., Chung, H. W., Kivlichan, I., O’Connell,                Reiter, E. Natural language generation challenges for ex-
  I., Osband, I., Gilaberte, I. C., Akkaya, I., Kostrikov, I.,           plainable AI. In Alonso, J. M. and Catala, A. (eds.),
  Sutskever, I., Kofman, I., Pachocki, J., Lennon, J., Wei,              Proceedings of the 1st Workshop on Interactive Natural
 J., Harb, J., Twore, J., Feng, J., Yu, J., Weng, J., Tang, J.,          Language Technology for Explainable Artificial Intelli-
 Yu, J., Candela, J. Q., Palermo, J., Parish, J., Heidecke,              gence (NL4XAI 2019), pp. 3–7. Association for Compu-
 J., Hallman, J., Rizzo, J., Gordon, J., Uesato, J., Ward,               tational Linguistics, 2019. doi: 10.18653/v1/W19-8402.
 J., Huizinga, J., Wang, J., Chen, K., Xiao, K., Singhal,                URL https://aclanthology.org/W19-8402.
  K., Nguyen, K., Cobbe, K., Shi, K., Wood, K., Rimbach,
  K., Gu-Lemberg, K., Liu, K., Lu, K., Stone, K., Yu, K.,              Shi, F., Chen, X., Misra, K., Scales, N., Dohan, D., Chi, E.,

                                                                  12
             Premise-Augmented Reasoning Chains Improve Error Identification in Math Reasoning with LLMs

  Schärli, N., and Zhou, D. Large language models can be            Weng, Y., Zhu, M., Xia, F., Li, B., He, S., Liu, S., Sun, B.,
  easily distracted by irrelevant context. In Proceedings of          Liu, K., and Zhao, J. Large language models are better
  the 40th International Conference on Machine Learning,              reasoners with self-verification. In Bouamor, H., Pino, J.,
  ICML’23. JMLR.org, 2023.                                            and Bali, K. (eds.), Findings of the Association for Com-
                                                                      putational Linguistics: EMNLP 2023, pp. 2550–2575,
Stechly, K., Valmeekam, K., and Kambhampati, S. On                    Singapore, December 2023. Association for Computa-
  the self-verification limitations of large language models          tional Linguistics. doi: 10.18653/v1/2023.findings-
  on reasoning and planning tasks, 2024. URL https:                   emnlp.167. URL https://aclanthology.org
  //arxiv.org/abs/2402.08115.                                         /2023.findings-emnlp.167/.
Tian, J., Li, Y., Chen, W., Xiao, L., He, H., and Jin, Y. Di-        Wu, Y., Jiang, A. Q., Li, W., Rabe, M. N., Staats, C., Jam-
  agnosing the first-order logical reasoning ability through          nik, M., and Szegedy, C. Autoformalization with large
  LogicNLI. In Moens, M.-F., Huang, X., Specia, L., and               language models, 2022. URL https://arxiv.org/
  Yih, S. W.-t. (eds.), Proceedings of the 2021 Conference            abs/2205.12615.
  on Empirical Methods in Natural Language Processing,
  pp. 3738–3747, Online and Punta Cana, Dominican Re-                Wu, Z., Zeng, Q., Zhang, Z., Tan, Z., Shen, C., and Jiang,
  public, November 2021. Association for Computational                M. Large language models can self-correct with key
  Linguistics. doi: 10.18653/v1/2021.emnlp-main.303.                  condition verification. In Al-Onaizan, Y., Bansal, M., and
  URL https://aclanthology.org/2021.em                                Chen, Y.-N. (eds.), Proceedings of the 2024 Conference
  nlp-main.303.                                                       on Empirical Methods in Natural Language Processing,
                                                                      pp. 12846–12867, Miami, Florida, USA, November 2024.
Tyen, G., Mansoor, H., Carbune, V., Chen, P., and Mak,                Association for Computational Linguistics. doi: 10.186
  T. LLMs cannot find reasoning errors, but can correct               53/v1/2024.emnlp-main.714. URL https://aclant
  them given the error location. In Ku, L.-W., Martins,               hology.org/2024.emnlp-main.714/.
  A., and Srikumar, V. (eds.), Findings of the Association
  for Computational Linguistics: ACL 2024, pp. 13894–                Yang, K., Swope, A. M., Gu, A., Chalamala, R., Song,
  13908, Bangkok, Thailand, August 2024. Association for               P., Yu, S., Godil, S., Prenger, R., and Anandkumar, A.
  Computational Linguistics. doi: 10.18653/v1/2024.findi               Leandojo: Theorem proving with retrieval-augmented
  ngs-acl.826. URL https://aclanthology.org                            language models, 2023. URL https://arxiv.org/
  /2024.findings-acl.826/.                                             abs/2306.15626.
Uesato, J., Kushman, N., Kumar, R., Song, F., Siegel, N.,            Yang, K., Poesia, G., He, J., Li, W., Lauter, K., Chaudhuri,
 Wang, L., Creswell, A., Irving, G., and Higgins, I. Solv-             S., and Song, D. Formal mathematical reasoning: A new
  ing math word problems with process- and outcome-                    frontier in ai, 2024. URL https://arxiv.org/ab
  based feedback, 2022. URL https://arxiv.or                           s/2412.16075.
  g/abs/2211.14275.
                                                                     Yao, S., Yu, D., Zhao, J., Shafran, I., Griffiths, T. L., Cao,
Wang, X., Hu, Z., Lu, P., Zhu, Y., Zhang, J., Subramaniam,             Y., and Narasimhan, K. Tree of thoughts: Deliberate
 S., Loomba, A. R., Zhang, S., Sun, Y., and Wang, W.                   problem solving with large language models, 2023. URL
 Scibench: Evaluating college-level scientific problem-                https://arxiv.org/abs/2305.10601.
 solving abilities of large language models, 2024. URL
 https://openreview.net/forum?id=u6jb                                Yu, L., Jiang, W., Shi, H., Yu, J., Liu, Z., Zhang, Y., Kwok,
 caCHqO.                                                               J. T., Li, Z., Weller, A., and Liu, W. Metamath: Boot-
                                                                       strap your own mathematical questions for large language
Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B.,              models. arXiv preprint arXiv:2309.12284, 2023.
 Xia, F., Chi, E., Le, Q., and Zhou, D. Chain-of-thought
 prompting elicits reasoning in large language models,               Zheng, C., Zhang, Z., Zhang, B., Lin, R., Lu, K., Yu, B.,
 2023. URL https://arxiv.org/abs/2201.1                                Liu, D., Zhou, J., and Lin, J. Processbench: Identifying
 1903.                                                                 process errors in mathematical reasoning, 2024. URL
                                                                       https://arxiv.org/abs/2412.06559.
Welleck, S., Liu, J., Bras, R. L., Hajishirzi, H., Choi, Y.,
 and Cho, K. Naturalproofs: Mathematical theorem prov-               Zhu, T., Zhang, K., Xie, J., and Su, Y. Deductive
 ing in natural language. In Thirty-fifth Conference on                beam search: Decoding deducible rationale for chain-
 Neural Information Processing Systems Datasets and                    of-thought reasoning, 2024. URL https://arxiv.
 Benchmarks Track (Round 1), 2021. URL https:                          org/abs/2401.17686.
 //openreview.net/forum?id=Jvxa8adr3iY.

                                                                13
             Premise-Augmented Reasoning Chains Improve Error Identification in Math Reasoning with LLMs

A. Appendix                                                                       {
                                                                                      "step_number": ,
A.1. Experimental Details                                                             "has_error": boolean,
Model For the Llama model (Grattafiori et al., 2024), we                              "errors": [
used vLLM (Kwon et al., 2023) for model serving and                                     {
AzureOpenAI for the GPT4o and GPT4-o1 (OpenAI, 2024)                                      "error_type": ,
models. To ensure reproducibility, all generations were                                   "error_description":
performed with a temperature=0. For all models, we used                                 }
their instruct variant.                                                               ]
                                                                                  }
A.2. Data statistics                                                          ]
                                                                          }
This results in a total of 607 reasoning chains with 203 posi-        }
tives, 214 negatives, and 190 synthetic negatives. In total,
we have 2,134 steps annotated as Correct, 321 steps as Math-          Chain-Level Error Types
ematical Error, 443 steps as Logical Inconsistency, and 741
                                                                      1. “Missing Steps”
steps as Accumulation Error, indicating that native and ac-
                                                                      Definition: Solution lacks crucial concluding steps or final
cumulation errors appear at almost equal rates. Additionally,
                                                                      answer derivation
we model each chain-of-thought as a directed acyclic graph
                                                                      Examples:
(PARC) based on the step-level premise annotations. Across
                                                                      - Not showing the final calculated value
607 PARCs, each chain contains on average 7.30 steps, rep-
                                                                      - Missing the ultimate conclusion
resenting the length of the chain-of-thought; 11.27 premises,
                                                                      - Failing to complete the proof
corresponding to the total premise references across steps;
                                                                      Impact: Makes the solution incomplete or inconclusive
and 10.42 edges linking premises to conclusions. The av-
erage depth of the PARC is 6.02, measuring the longest                 2. “Planning Error”
path of dependencies, while the maximum width is 1.90,                 Definition: The reasoning takes an invalid or fundamentally
quantifying how many steps can appear at the same layer in             incorrect approach
the PARC. Finally, the branching factor is 1.37, which is the          Examples:
ratio of edges to nodes, indicating that each step typically          - Using inapplicable theorems or methods
spawns fewer than two subsequent steps on average.                    - Solving for incorrect variables
                                                                      - Taking an approach that cannot possibly lead to a solution
A.3. Prompt for Error Annotation with O1                               Impact: Makes the entire solution path invalid
                                                                      - Note: Valid but longer approaches (e.g., integration by
You are an expert mathematical reasoning analyzer. Your                parts instead of a substitution trick) should NOT be marked
task is to analyze mathematical solutions and generate de-             as errors
tailed error annotations in a specific JSON format. For each
solution provided, you must carefully examine the reasoning           Step-Level Error Types
chain and individual steps to identify any errors or issues.          1. “Logical Inconsistency”
Response Format                                                       Definition: Steps that violate logical principles or make
                                                                      unjustified conclusions
Your response must be a valid JSON object following ex-               Examples:
actly this structure:                                                 - False equivalences
                                                                      - Invalid deductions
{
                                                                      - Unsupported assumptions
    "error_annotations": {
                                                                      - Note that incorrect use of previous information (exam-
      "chain_level": {
                                                                      ple the step uses a wrong value of a variable) is a Logi-
        "has_errors": boolean,
                                                                      cal Inconsistency
        "errors": [
                                                                      Impact: Breaks the logical flow of the solution
          {
            "error_type": string,                                     2. “Mathematical Error”
            "error_description": string                               Definition: Incorrect calculations, misuse of formulas, or
          }                                                           mathematical operations
        ]                                                             Examples:
      },                                                              - Arithmetic mistakes
      "step_level": [                                                 - Incorrect algebraic manipulations

                                                                 14
              Premise-Augmented Reasoning Chains Improve Error Identification in Math Reasoning with LLMs

                               GSM8K                                 MATH                            Orca Math                           MetaMathQA
  Method
                    Neg       Syn      Pos       Avg       Neg     Syn     Pos       Avg    Neg      Syn      Pos      Avg      Neg       Syn    Pos     Avg
  Full Context
  Llama 3.1 8b      48.87 57.68 91.9             58.6     46.91    60.29   90.61    60.2   43.26     51.2     96.7     55.06    50.47    55.15   95.17   59.45
  Llama 3.1 70b     58.35 77.03 98.61           71.37     55.55    72.83   96.24   69.77   50.33    64.25    96.74     63.52    55.59    73.13   97.93   69.49
  Qwen 2.5 7b       40.88 54.13 100             54.94     40.47    53.60   98.07   56.26   41.20    53.69     100      55.85    43.36    53.18   99.39   56.26
  Qwen 2.5 32b      46.76 69.26 99.8            63.56     49.58     66.5     98    65.11   49.44    63.01     99.5     63.06     49.7     67.8    99.6   65.02
  Qwen 2.5 72b      47.48 67.17 100             63.11     53.19    67.87   99.79   67.52   50.41    60.33     100      62.50    47.31    63.59   99.05   62.20
  GPT4o-mini        52.68 73.14 95.02           66.68     50.41    62.39    93.4   63.03   55.22    61.18     98.6     64.59    51.52    65.42   97.35   64.47
  GPT-4o            53.81 75.3 98.33            68.52      50.9    68.41   98.57   66.52   59.55    65.75     100      68.55    56.26    71.72    99.3   69.41
  Oracle Premises
  Llama 3.1 8b      57.02 82.64        74.61    69.26     54.58    60.94   51.65   56.47   57.43    60.61    59.48     59.09    52.65    68.48   60.51   60.37
  Llama 3.1 70b     74.41 85.12        94.69    81.46     68.55    79.88   78.11   74.68   66.78    72.65    93.37     73.45    63.31    83.15   92.16   76.05
  Qwen 2.5 7b       52.40 79.37        89.56    69.74     56.86    70.23   79.85   65.96   55.01    66.66    76.65     63.39    56.32    77.06   91.94   70.45
  Qwen 32b          66.57 88.64        96.95    80.76     69.24    82.26   89.32   77.98   63.58    69.88    96.31      71.4    59.84    85.74   96.87   76.38
  Qwen 2.5 72b      69.48 86.34        98.98    80.58     72.98    81.10   91.03   79.50   69.76    72.77    93.24     74.87    66.23    86.21   98.06   79.50
  GPT4o-mini        63.83 85.77        91.29    76.16     65.86    74.99   78.41   71.71   64.03    72.66    83.56     70.74    58.77    85.11   91.44   74.73
  GPT-4o            67.03 87.2         94.76    78.74     70.32     77.3   90.65   76.79   71.19    73.69    92.15     75.56    72.76    88.95   94.82   82.88
  Model Premises
  Llama 3.1 8b      54.61    76.74     65.44    64.53     52.16    59.83   50.96   54.88   55.57    59.82    67.36     59.22    54.52    69.13   62.63   61.78
  Llama 3.1 70b     74.51    86.22     94.69    81.92     70.94    79.29   77.91   75.45   64.95    72.28    93.37     72.52    65.69    82.74   89.71   76.52
  Qwen 2.5 7b       53.03    78.40     90.37    69.73     58.47    66.87   82.72   65.96   52.07    71.12    84.28     65.38    54.98    73.87   91.02   68.43
  Qwen 32b          65.58    86.34     96.95    79.37     68.61    76.96   88.71   75.57   61.89    69.24    95.25     70.26    62.18    85.60   97.32   77.40
  Qwen 2.5 72b      69.87    85.12     96.38    80.56     69.51    79.92   90.84   77.28   69.45    71.34    94.19     74.41    64.73    85.52   98.12   78.53
  GPT4o-mini        58.25    80.81     86.72    72.33     65.84     72.4   71.88   69.45   61.18    72.48    85.94     69.93    57.04    81.63   91.15   72.51
  GPT-4o            65.23    86.67     99.76    79.82     70.12    76.67   91.84   76.45   66.33    71.74    93.14     72.96    67.28    88.19   89.85   79.41

                                 Table 8. Detailed results for error identification for all dataset and models

                                                       Positives                     Negatives               Synthetic Negatives
                       Model Name
                                          Precision       Recall    F1     Precision    Recall     F1      Precision   Recall     F1
                       Llama 3.1 8b            67.80      89.91    77.31     65.03      91.31     75.96     64.08      86.76     73.71
                       Llama 3.1 70b           83.49      97.09    89.78     80.36      98.87     88.66     79.92      96.68     87.51
                            Qwen 7b            69.94      62.85    66.21     66.14      67.60     66.86     66.18      60.15     63.02
                            Qwen 32b           85.98      93.49    89.58     83.78      96.95     89.88     82.45      95.61     88.54
                        GPT4o-mini             74.93      84.81    79.56     70.85      87.01     78.10     71.84      86.73     78.59
                         GPT-4o                89.38      93.66    91.47     84.97      94.95     89.69     83.43      94.65     88.72

                               Table 9. Precision, Recall and F1 score for premise identification with GSM8K

                                                       Positives                     Negatives               Synthetic Negatives
                       Model Name
                                          Precision       Recall    F1     Precision    Recall     F1      Precision   Recall     F1
                       Llama 3.1 8b            53.98      82.36    65.22     46.39      82.43     59.37     52.63      82.42     64.24
                       Llama 3.1 70b           71.13      95.82    81.65     67.82      97.16     79.88     70.46      97.47     81.80
                            Qwen 7b            59.40      60/30    59.85     48.82      56.02     52.17     59.40      62.87     61.09
                            Qwen 32b           74.57      87.30    80.43     69.98      87.31     77.69     73.13      91.04     81.11
                        GPT4o-mini             57.58      66.57    61.75     54.42      69.01     60.85     61.18      72.29     66.27
                         GPT-4o                69.76      90.19    78.67     66.95      87.16     75.73     71.48      91.99     80.45

                                Table 10. Precision, Recall and F1 score for premise identification in MATH


- Wrong formula application                                                        Examples:
- Note that Mathematical Error can only appear when there                          - Using wrong intermediate results
 is an error in calculation                                                        - Building upon previously miscalculated values
 Impact: Produces incorrect numerical or algebraic results                         Impact: Compounds previous mistakes into larger errors
3. “Accumulation Error”
Definition: Errors that propagate from previous incorrect                          4. “Other”
steps                                                                              Definition: Any error that doesn’t fit into the above cate-


                                                                              15
             Premise-Augmented Reasoning Chains Improve Error Identification in Math Reasoning with LLMs

                                              Positives                    Negatives             Synthetic Negatives
                     Model Name
                                     Precision   Recall    F1     Precision   Recall    F1     Precision   Recall    F1
                     Llama 3.1 8b     58.94      84.52    69.45    44.14      76.76    56.05    58.67      82.99    68.74
                     Llama 3.1 70b    77.82      97.37    86.50    65.18      96.13    77.69    76.29      95.88    84.97
                       Qwen 7b        58.05      59.09    58.57    48.72      66.48    56.23    59.86      59.41    59.63
                       Qwen 32b       78.73      91.60    84.68    69.89      88.99    78.29    78.09      92.07    84.50
                      GPT4o-mini      65.06      76.92    70.50    51.74      73.81    60.84    65.52      79.37    71.78
                       GPT-4o         79.91      92.51    84.68    67.13      88.11    76.26    79.42      90.49    84.62

                      Table 11. Precision, Recall and F1 score for premise identification with MetaMathQA.

                                              Positives                    Negatives             Synthetic Negatives
                     Model Name
                                     Precision   Recall    F1     Precision   Recall    F1     Precision   Recall    F1
                     Llama 3.1 8b     56.02      80.12    65.94    52.60      78.92    63.13    55.31      80.26    65.49
                     Llama 3.1 70b    72.82      96.83    83.13    68.15      96.42    79.86    72.17      96.93    82.74
                       Qwen 7b        62.33      61.81    62.07    68.15      96.42    79.86    58.75      59.69    59.22
                       Qwen 32b       77.73      91.18    83.92    71.55      89.55    79.54    73.55      91.16    81.41
                      GPT4o-mini      63.24      75.36    68.77    57.36      73.38    64.39    59.75      73.13    65.77
                       GPT-4o         73.90      92.63    83.92    66.97      92.87    77.92    72.50      91.02    80.53

                          Table 12. Precision, Recall and F1 score for premise identification in OrcaMath


gories Examples:                                                         - Focus on correctness rather than elegance or brevity
- Notation mistakes
- Unclear explanations
                                                                         Workflow
- Formatting issues
                                                                         1. Read and understand the problem statement
Impact: Varies depending on the specific error
                                                                         2. Analyze the reasoning chain step-by-step
Analysis Requirements                                                    3. Check for chain-level errors
1. Examine each step against mathematical principles and                 4. Analyze each step for specific errors
theorems                                                                 5. Verify all premises and justifications
2. Verify all calculations and mathematical operations                   6. Ensure completeness of the solution
3. Check for proper use of definitions and formulas
4. Ensure logical flow between steps
5. Compare against the provided ground truth answer                        A.4. Prompt for Premise Annotation with O1
6. Consider the completeness of the solution
                                                                         The system prompt and the instruction for the O1 model for
 Important Notes                                                         identifying premises for a given step is shared in Table 13
- Provide ONLY the JSON output, no additional text or
 explanations                                                              A.5. Prompt for Error identification
- Every step in the solution must have a corresponding entry
 in step level array                                                     The prompts used for the baseline approach are shared in
- Keep error descriptions clear, specific, and mathematically            Appendix 14 and 15 . The evaluation for our error identifi-
 precise                                                                 cation with premises are done with the prompts outlined in
- Use empty arrays for errors when no errors exist                       Tables 16 and 17,
- Ensure your response is always valid JSON that matches
 the exact format specified
- Each error must have both an error type and a correspond-
 ing detailed error description
- Error descriptions should be specific to the mathematical
 context of the problem
- Do NOT penalize valid but verbose approaches (e.g.,
 breaking down algebra into multiple steps)
- Do NOT mark alternative solution methods as errors
 unless they are genuinely invalid

                                                                    16
   Premise-Augmented Reasoning Chains Improve Error Identification in Math Reasoning with LLMs




Instruction:
Given this math word problem and its solution steps, identify the key premises and their relationships.
Problem: {problem[’question’]}
Solution Steps:
{chr(10).join(problem[’steps’])}
Return your analysis in this exact JSON format:
{json template}
Critical Rules for Premises:
1. A step can NEVER use itself as a premise. For example, Step 3 cannot use any premise labeled as [3,
”...”].
2. Premises can only come from:
- Step 0 (problem statement and fundamental mathematical principles)
- Previous steps (steps with lower index)
3. Any intermediate calculations or logical steps within a single step should be part of that step’s
reasoning, not treated as separate premises.
4. Mathematical principles (like properties of operations) should be treated as part of Step 0.

Additional Requirements:
1. Start with Step 0 containing the problem statement.
2. For each step after 0, copy the EXACT text from the student’s solution into ‘original step‘.
3. Show clear reasoning for how premises lead to conclusions.
4. Return ONLY valid JSON with no additional text.
5. Do not use any special characters like &, ¡, ¿, etc.
6. Do not add any additional text for formatting it (e.g., ”json”), just output the raw JSON.
7. Maintain the exact same number of steps as in the original solution.

 Remember:
- Each step’s premises must strictly come from either the problem statement (Step 0) or previous steps.
 Never from the current step.
- Keep each step atomic—do not split steps into multiple substeps even if they contain multiple
 calculations.
- The number of steps in your output (excluding Step 0) must match exactly with the number of steps in
 the student’s solution.

System Prompt:
You are an expert in mathematical reasoning. Your task is to analyze solution steps and output a JSON
object containing:
1. The premises used in each step.
2. The conclusion reached.
3. The reasoning that connects premises to conclusions.

Output MUST be valid JSON with no additional text or explanation.


        Table 13. System prompt and instruction for the O1 model to identify premises for a given step




                                                     17
   Premise-Augmented Reasoning Chains Improve Error Identification in Math Reasoning with LLMs




Instruction:
Question: {question}
Solution so far: {solution}


1. “Logical Inconsistency”
- Definition: Steps that violate logical principles or make unjustified conclusions
- Examples:
- False equivalences
- Invalid deductions
- Unsupported assumptions
- Note that incorrect use of previous information (example the step uses a wrong value of a variable) is a
 Logical Inconsistency
- Impact: Breaks the logical flow of the solution

2. “Mathematical Error”
- Definition: Incorrect calculations, misuse of formulas, or mathematical operations
- Examples:
- Arithmetic mistakes
- Incorrect algebraic manipulations
- Wrong formula application
- Note that Mathematical Error can only appear when there is an error in calculation
- Impact: Produces incorrect numerical or algebraic results

3. “Accumulation Error”
- Definition: Errors that propagate from previous incorrect steps
- Examples:
- Using wrong intermediate results
- Building upon previously miscalculated values
- Impact: Compounds previous mistakes into larger errors

4. “Other”
- Definition: Any error that doesn’t fit into the above categories
- Examples:
- Notation mistakes
- Unclear explanations
- Formatting issues
- Impact: Varies depending on the specific error

Statement to analyze: step
Format your response as: Reasoning: [detailed analysis of the statement’s validity] Verdict: [CORRECT,
Mathematical Error, Logical Inconsistency, or Accumulation Error]


                              Table 14. Baseline error identification Instruction




                                                      18
   Premise-Augmented Reasoning Chains Improve Error Identification in Math Reasoning with LLMs



System Prompt:
You are a helpful AI assistant that analyzes mathematical solution steps. Your task is to determine if
each statement is COMPLETELY correct by carefully analyzing its validity. Focus ONLY on whether
the current step is valid - do not consider whether it helps reach the final answer or whether better steps
could have been taken. Mark a statement as CORRECT unless you find a specific error.


                           Table 15. Baseline error identification System prompt



System Prompt:
Your task is to determine whether a given sentence contains any mathematical errors. For mathematical
error, check if the sentence contains mathematical calculations (arithmetic or algebraic), and whether
they are incorrect. If there are such errors, mark the sentence as ”mathematical error” - Mathematical
errors can only come from incorrect results of mathematical operations If no such errors exist, mark it
as ”correct”.
Note: mathematical error can only come from incorrect numerical or algebraic calculations (i.e. wrong
multiplication, wrong addition etc.) if there are no numerical or algebraic calculations done, you can
mark it as correct
Instruction :
Statement to analyze:
step
Format your response as:
Reasoning: [detailed analysis of the statement’s validity]
Verdict: [correct or mathematical error]


                               Table 16. Math error identification instruction



System Prompt:
You are provided with a math question, a statement which is a step in the solution to the question and
the premises to this steps (the question is also a premise). Your task is to identify whether the step
follow naturally from the premises or not. If the current step contradicts the premises, mark is as a
logical inconsistency If the step can be directly inferred from the premises, mark it as correct. You
should not check whether the premises are correct, assume they are correct. Only check the sentence
given.
Instruction :
Given Premises:
Question: {question}
Previous steps as premise: {premises}
Statement to analyze: {step}
Guidelines:
1. for logical inconsistency check if the step was performed under misinterpretation of the premises,
made invalid deductions or had unsupported assumptions
2. Don’t check for correctness of the premises, your only task is to check correctness of the given
sentence
Format your response as: Reasoning: [detailed analysis of the statement’s validity] Verdict: [correct,
logical inconsistency]


                              Table 17. Logical error identification instruction


                                                     19
   Premise-Augmented Reasoning Chains Improve Error Identification in Math Reasoning with LLMs




Instruction:
You are provided with a question, a partial solution, and the next step in the solution.
Your task is to identify the steps that serve as premises for the given next step.
A step qualifies as a premise if the next step directly relies on information from that step. Based on the
identified premises, the correctness of the next step should be fully verifiable.
Question (Step 0):
{question}
Solution so far:
{solution}
Next step to analyze:
{step}
For the step above, identify which previous steps (including Step 0 - the question) are premises and
explain why each one is necessary. Remember:
1. A step cannot be a premise to itself
2. The question (Step 0) can be a premise if used directly
Generate ONLY the premises and nothing else.
Format your response with one premise per line as:
Step X: [explanation of why this step is necessary for the current step]



             Table 18. Prompt for evaluating models in the premise identification task (zero shot)




                                                      20
