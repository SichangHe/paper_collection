                                                              FANS: Formal Answer Selection for LLM
                                                            Natural Language Math Reasoning Using Lean4

                                                                       Jiarui Yao1 , Ruida Wang1 , Tong Zhang1
                                                                        1
                                                                        University of Illinois Urbana-Champaign
                                                                    {jiarui14, ruidaw, tozhang}@illinois.edu



                                                              Abstract
                                            Large Language Models (LLMs) have dis-
arXiv:2503.03238v2 [cs.CL] 1 Oct 2025




                                            played astonishing abilities in various tasks, es-
                                            pecially in text generation, classification, ques-
                                            tion answering, etc. However, the reasoning
                                            ability of LLMs still faces many debates, espe-
                                            cially in math reasoning. The inherent ambi-
                                            guity of Natural Language (NL) limits LLMs’
                                            ability to perform verifiable reasoning, mak-
                                            ing the answers lack coherence and trustworthy
                                            support. To tackle the above challenges, we pro-
                                            pose a novel framework named FANS: Formal
                                            ANswer Selection for LLM Natural Language
                                            Math Reasoning Using Lean4. It is a pioneer-
                                            ing framework that utilizes Lean4 to enhance
                                            LLMs’ NL math reasoning ability. In particular,
                                            given an NL math question and LLM-generated
                                            answers, FANS first translates it into Lean4
                                            theorem statements. Then it invokes another
                                            Lean4 prover LLM to produce proofs, and fi-
                                            nally verifies the proofs by Lean4 compiler.
                                            Answers are selected based on the verifications.      Figure 1: Comparision between FANS and majority
                                            It enhances LLMs’ NL math ability in provid-          vote, together with ORM and ORM + FANS method.
                                            ing a computer-verifiable solution for its cor-       From the results, we could see FANS based on ORM
                                            rect answer and proposes an alternative method        achieve the highest accuracies consistently across dif-
                                            for answer selection beyond the reward model          ferent base models and different test sets. In particular,
                                            based ones. Our experiments demonstrate the           FANS performs well on the sub-fields of number theory
                                            effectiveness of FANS with an improvement of          and algebra, which are better supported by Lean4 with
                                            nearly 2% across several math benchmarks, and         its existing libraries.
                                            even higher further based on reward models or
                                            in subfields such as algebra and number theory
                                            that Lean4 is better at. The code is available in
                                            https://github.com/MaxwellJryao/FANS.                 able to perform real reasoning or simply do pattern
                                                                                                  matching (Saparov et al., 2023). Consequently, re-
                                        1   Introduction
                                                                                                  searchers have begun to consider using symbolic
                                        Math reasoning and problem-solving capability             languages to perform computer-verifiable formal
                                        have been a hot topic in LLM’s research field. Re-        reasoning in mathematics. Consequently, many for-
                                        searchers are trying to develop new LLMs (Shao            mal mathematical languages have been proposed
                                        et al., 2024; Yang et al., 2024b; Yu et al., 2023), in-   such as Lean (De Moura et al., 2015; Moura and
                                        creasingly harder benchmarks (Cobbe et al., 2021;         Ullrich, 2021), Isabelle (Paulson, 1994), and HOL
                                        Hendrycks et al., 2021), and advanced reward              Light (Harrison, 2009). These Formal Languages
                                        model methods for evaluation of answers (Dong             (FLs) map existing mathematics into their formal
                                        et al., 2023; Yang et al., 2024b). However, there         kernels, which allows computers to automatically
                                        have always been debates on whether LLMs are              verify mathematical proofs. FL provides a clear
standard for evaluating answers to theorem proof         stages that work synergistically to enhance answer
and significantly impacts both mathematical and          selection and provide a verifiable formal foundation
computer science communities.                            for NL math reasoning:
   In the context of formal reasoning, most existing     (a) NL to FL translation: Based on the outstand-
works focus on how to use NL to enhance the FL           ing reasoning of Long Chain-of-Thought (CoT),
capability of the model (Xin et al., 2024b; Wang         we propose the training method for the Long CoT
et al., 2024b; Lin et al., 2024; Wang et al., 2025b).    translator named LeanTranslator. It can translate
Research has also shown that formal language so-         general math question-answering problems into
lutions to a math problem can be translated back         Lean4 provable formal statements. Applying the
to a valid natural language proof with very few er-      translator to question-answer pairs generated by
rors (Jiang et al., 2022). Despite extensive research    LLMs in NL math reasoning, we can obtain Lean4
on formal languages (FLs), few have successfully         statements for further processing.
leveraged Lean4 or other formal languages to en-         (b) Lean4 proof writing and verification: We
hance LLMs’ natural language based mathematical          pass the generated statement to an advanced prover
reasoning. On the other hand, for complex natural        to generate the proofs for the FL statement, then
language math reasoning problems, most LLMs              use the Lean4 verifier to judge the correctness of
struggle to find a correct solution in limited at-       the proofs. Final answer selection will be based on
tempts, but could eventually provide the correct         the verification results. (c) Answer selection and
solution through multiple attempts. This leads to        output: After we obtain the verification results, we
a natural idea of scaling the test-time computa-         can combine them with existing answer selection
tion resources in NL reasoning to get the correct        methods jointly. Since our answers are formally
answer. Dong et al. (2024); Shao et al. (2024);          provable, it conveys a more solid foundation and
Yang et al. (2024b) shown that a model with scale        trustworthiness than direct NL reasoning.
around 7B without advanced fine-tuning methods              We summarize our contributions as follows:
could achieve a pass@n accuracy around 90% on
MATH500 (Lightman et al., 2023) after a suffi-               1. We propose FANS, a pioneering framework
cient number of trials. Much recent literature has              that applies formal mathematical language,
revealed the effectiveness of test-time scaling for             Lean4, in enhancing the capability of LLMs
improving the model’s performance (Muennighoff                  to solve NL math problems.
et al., 2025; Chen et al., 2024; Snell et al., 2024;
Wu et al., 2024a; Guan et al., 2025).                        2. In our framework, we propose a new method
   However, this raises an important question of                to train the Long CoT translator that translates
how to select the correct answer from outputs from              NL question-answer pairs into Lean4 state-
the model, which is highly non-trivial especially in            ments. To be best of our knowledge, this is
the case that we do not have the ground truth an-               the first work that proposes such methods.
swer. Fundamentally speaking, this partially orig-
                                                             3. Extensive experiments indicate that enhanced
inates from mathematical reasoning being a task
                                                                by our framework, LLMs are able to perform
with a solid logical foundation, but natural lan-
                                                                better answer selection. It can improve the
guage’s inherent ambiguity makes the generated
                                                                accuracy on MATH500 by at most 1.91% and
results not trustworthy enough. To solve this prob-
                                                                AMC23 by at most 8.33%. In some particular
lem, many answer-selection methods have been
                                                                subfields that Lean is better at, we can even
proposed, ranging from majority vote to best-of-N
                                                                select all correct solutions. The qualitative
ranking built upon various reward models (Dong
                                                                studies also indicate that our framework can
et al., 2024; Yang et al., 2024b). But these methods
                                                                make the NL solutions generated by the model
are either too simple to fulfill the pass@n potential,
                                                                have a solid basis using formal language, en-
or still pure LLM-based, failing to make use of
                                                                hancing the trustworthiness of the answer.
the solid formal foundation of math reasoning. In
addition, it is hard for reward models to generalize     2     Methodology
to out-of-distribution (OOD) domains or models
due to the distribution shift.                           High-level speaking, FANS framework can be de-
   To solve the above challenges, we propose our         composed into three stages. Firstly, we introduce
novel FANS framework. It contains the following          methods for translation for Natural Language (NL)
       Natural Language Statement                                                                                          Follow these instructions
                                                                           Formal Language Statement                       carefully:
                                                                           theorem math_problem_0 (x : ℝ)                  1. Provide a logically correct
                               Answer 1
      Half the value of $3x-                                        (h₀ : (1 / 2) * (3 * x - 9) = x + 37) : x = 83 := by   and rigorous Lean4 proof.
      9$ is $x+37$. What is           The value                                                                            2. In the <Thought> section,
                                                       Translator
      the value of $x$?              of $x$ is 83.                                                                         include your detailed step-by-
                                                                                                                           step reasoning. …
      Question                 Answer 2
                                                                                  Proof 1                                   Long-CoT Prompt
                                      The value
                                     of $x$ is 70.

                               Answer 3                                                                                                                      Output
                                      The value
                                     of $x$ is 56.                                                  Prover       Backbone        Verifier

                                                                                   Proof n




                                                                                                                                             The value
                                                                          Output                                                             of $x$ is 83.

                                   Majority Vote     Best-of-N Based                                                                         Joint Output
                                                     on Reward Model                                                                        (FANS + ORM)



Figure 2: FANS Framework: The framework shown in the upper part first passes the Natural Language math
questions and the LLM-generated answers to our Long CoT NL-to-FL translator. Subsequently, it invokes a prover
to prove the translated Lean4 statements and uses the verifier to check whether the proofs are correct. The correct
outputs are used for further answer selection as a verifiable foundation. Existing Methods: majority vote and
best-of-N ranking based on reward models are shown in the lower part of the figure.


question-answer pairs into their corresponding For-                                     Wang et al. (2023), we generate NL statements for
mal Language (FL) statements in Section 2.1. Sub-                                       the DeepSeek-Prover-v1 dataset’s Lean4 theorem
sequently, we detail how we write FL proofs and                                         statement using Qwen-2.5-72B. Altogether, we ob-
verify it using the Lean4 verifier in Section 2.2. Fi-                                  tain a dataset containing 162,181 NL-FL aligned
nally, we introduce further usage for the verified                                      theorem statements without Long CoT. Among
proofs in Section 2.3. The general idea for FANS                                        them, 21,967 are generated from DeepSeek-v1 and
is to bridge the gap between FL and NL using the                                        140,214 are from Lean-Workbook.
verified FL proofs as a solid foundation for LLM’s                                         Based on the aligned dataset, we train a Long
NL reasoning.                                                                           CoT translator using the LoT-Solver (Wang et al.,
                                                                                        2025b) as the base model. Since there is no
2.1   From Natural Language to Formal                                                   Long CoT annotated theorem statement transla-
      Language                                                                          tion dataset, we apply the transfer learning tech-
To obtain accurately aligned FL statements from                                         nique. During training, we explicitly instruct the
the original NL question-answer pairs, we first train                                   model in the system prompt to answer without us-
a Long Chain-of-Thought (Long-CoT) (OpenAI,                                             ing Long CoT and provide the empty Long CoT
2024) translator using pair-wise NL-FL statements.                                      content. During inference, we instruct the model
We try to teach a prover to analyze the NL state-                                       to use Long CoT to answer the question. In the
ment in its Long CoT and then translate it into the                                     inference, the model learns from the basic Long
FL statement. However, since there is no Long                                           CoT ability in LoT-Solver to accurately translate
CoT data available for NL-to-FL statement transla-                                      the NL statement into the FL statement. Details of
tion, inspired by transfer learning methods for Lean                                    training and inference data examples can be found
prove Long CoT in MA-LoT (Wang et al., 2025b),                                          in Appendix A.
we introduce the following training method for FL                                          Besides our own Long CoT translator, recently,
statement translator training.                                                          Wang et al. (2025a) also released an NL-FL transla-
   Firstly, we collect the NL-FL aligned statement                                      tor, and we also utilize it as the translator in the fol-
translation data from Lean-Workbook (Ying et al.,                                       lowing experiments. Since it is not guaranteed that
2024). Based on such data, as versatile examples                                        the translated FL statements are perfectly consis-
and use analysis-then-generate method inspired by                                       tent with the original NL statements, we introduce
another procedure to check whether the translations      vote on those answers successfully verified by the
are faithful by prompting the LLMs themselves or         Lean4 verifier, and if there the number of votes for
a stronger one, QwQ-32B (Qwen Team, 2025) in             the winner is below one pre-specified threshold, we
our case, to generate a decision.                        discard the answer and return to the majority vote
                                                         directly to mitigate the impact of false positives
2.2   Formal Language Proofs and Verification            due to mis-translation.
After receiving the translated formal language state-       If the reward models are accessible, they could
ments, we utilize the open-sourced Lean4 provers         serve as a metric to determine which problems are
(Lin et al., 2025; Ren et al., 2025) to produce po-      more difficult by comparing the scores on specific
tential proofs written in Lean4 as well. To adapt        questions and model outputs. Intuitively, harder
the prover on the formal language statements from        problems might lead to more erroneous attempts,
natural language math problems, we use a few-            rendering the best-of-N based on reward models
shot prompt for better alignment with the formats        ineffective. Under this scenario, we resort to verifi-
of classic formal language proof problems. Since         able formal language proofs to accurately identify
the natural language statements have been trans-         the correct answer among multiple wrong options.
lated into the standard formal language statements
format, provers fine-tuned on formal language            3     Experiments
statements-proofs could be immediately applied
                                                         We conduct extensive experiments on the
without any modification. For this very reason,
                                                         MATH500 (Hendrycks et al., 2021) and
FANS could generalize among different backbone
                                                         AMC23 (Yang et al., 2024b) to evaluate the
provers easily, with a highly disentangled formula-
                                                         effectiveness of FANS on enhancing the NL
tion of its three-stage procedure.
                                                         mathematical reasoning using FL methods.
   The core backbone for FANS to be rigorously
                                                         We quantitatively measure its usage in answer
verified stems from the formal proof process in
                                                         selection in Section 3.3 and qualitatively show its
the functional programming level, which could be
                                                         capability in enhancing the trustworthiness of NL
implemented by retrieving the compilation results
                                                         math reasoning by providing a formal backbone in
from the verifier. At its core, Lean4 operates within
                                                         Section 3.5. Additionally, we conduct a thorough
the calculus of inductive constructions, ensuring
                                                         ablation study to validate the importance of each
that every proof is mechanically verified through
                                                         module of our proposed framework.
a type-checking system that enforces strict logical
consistency. This could eliminate human errors           3.1     Experiment Setup
commonly found in formal reasoning, getting rid
of unstable reasoning based on intuition and vague       3.1.1    Dataset and Task
derivation. Therefore, once a theorem is proven in       In this work, we evaluate FANS’s capability in en-
Lean4, it is mathematically indisputable, provid-        hancing LLMs’ NL reasoning on several challeng-
ing a robust foundation for tasks such as answer         ing datasets. The first is MATH500 (Hendrycks
selection in math problem solving.                       et al., 2021), a dataset containing 500 high-school-
                                                         level math problems ranging in 7 major fields, in-
2.3   Beyond Formal Language Itself                      cluding precalculus, algebra, number theory, etc.
Though the provers could achieve a 60% to 80%            Another dataset we use is AMC23 from the repo of
success rate on standard formal language proofs          Qwen-2.5-Math (Yang et al., 2024b). This dataset
datasets like miniF2F (Zheng et al., 2021), there are    contains 40 high-school-level math competition
still chances that all the tries of formal proofs fail   questions, ranging from similar fields as MATH500
because of the gap between the formal language           but harder and more versatile in the form of ques-
problems used to train the prover and the formats        tion types. Other datasets include Minverva Math
of translated formal language statements from the        (Lewkowycz et al., 2022) and Olympiad Bench (He
natural math QA questions. In this case, FANS            et al., 2024).
will fall back to other alternate methods to select         The goal of FANS is to use the FL method to
the best output. For example, we could turn to           enhance the existing answer selection methods like
the vanilla majority vote, or take advantage of re-      Majority Vote (MV) and Optimized Reward Model
ward models and output the answer with the highest       (ORM), and use formal reasoning to provide verifi-
score. For the former, we first conduct a majority       able support for NL reasoning.
        Models                         MATH(total)     MATH-Algebra     MATH-Number Theory       AMC23
        Mistral-MV                        33.80            42.74                 33.87           12.50
        Mistral-FANS                      36.40            45.97                 35.48           15.00
        Improvement(%)                    +7.69            +7.56                 +4.75           +20.00
        DeepSeek-Math-ORM                 62.60            82.26                 61.29            30.00
        DeepSeek-Math-ORM+FANS            63.80            82.26                 66.13            32.50
        Improvement(%)                    +1.91              -                   +7.90            +8.33
        Qwen-2.5-Math-ORM                 80.80            96.77                 91.94            70.00
        Qwen-2.5-MATH-ORM+FANS            81.80            98.39                 93.55            70.00
        Improvement(%)                    +1.25            +1.67                 +1.75              -

Table 1: Accuracies on math benchmarks (%). For all baselines, we apply ORM@8 for comparison to using FANS
based on ORM or using FANS compared with majority voting. The result for FANS is denoted as FANS-model.


    Models                          MATH500       Minerva Math     Olympiad Bench        AMC23     Average
    Llama-3.2-3B-Instruct             56.60            24.26             21.93           35.00      34.45
    FANS w/ self check                57.60            22.06             21.89           32.50      33.51
    FANS w/ external check            61.00            24.26             24.15           35.00      36.10
    FANS remove                       61.80            27.21             25.48           40.00      38.62
    Deepseek-Math-7B-Instruct         54.00            27.57             20.74           32.50      33.70
    FANS w/ self check                55.40            26.47             22.37           27.50      32.94
    FANS w/ external check            57.00            27.21             22.67           30.00      34.22
    FANS remove                       58.60            30.88             23.85           32.50      36.46
    Qwen2.5-Math-1.5B-Instruct        79.00            33.46             44.30           55.00      52.94
    FANS w/ self check                79.20            33.82             44.44           55.00      53.12
    FANS w/ external check            80.00            33.82             44.74           57.50      54.02
    FANS remove                       80.20            36.40             45.63           60.00      55.56
    Qwen2.5-Math-7B-Instruct          87.40            41.18             50.22           72.50      62.83
    FANS w/ self check                87.40            40.07             50.52           72.50      62.62
    FANS w/ external check            88.00            41.18             50.67           72.50      63.09
    FANS remove                       88.80            42.65             51.85           72.50      63.95

   Table 2: Results (%) with new translator (Wang et al., 2025a) and current SOTA prover (Ren et al., 2025).


3.1.2    Baselines                                       3.2   Implementation Details

                                                         In FANS, we use LoT-Solver as the base model for
To demonstrate how FANS works across diverse             our Long CoT translator training using the transfer
base models with different levels of answer-             learning method we proposed. We train the transla-
ing mathematical questions, we select Mistral-           tor on 162,181 records of NL-FL aligned statement
7B (Jiang et al., 2023), DeepSeek-Math-7B (Shao          data. To stabilize training, we also use block train-
et al., 2024) and Qwen-2.5-Math-1.5B / 7B (Yang          ing and curriculum data sorting techniques in Wang
et al., 2024b). The former two are relatively weaker     et al. (2024b). Besides, Kimina-Autoformalizer
models, leaving more space for them to be im-            (Wang et al., 2025a) is also tested as the translator.
proved by FANS itself. In contrast, for the latter       We use DeepSeek-Prover-v1.5 (Xin et al., 2024b),
stronger models, which could answer more prob-           Goedel Prover (Lin et al., 2025) and DeepSeek-
lems correctly, FANS majorly focus on providing          Prover-v2 (Ren et al., 2025) as our provers and
trustworthiness and a verifiable foundation to the       Santos et al. (2025) as the verifier, which signifi-
generated solutions. For ORM methods, we uni-            cantly reduces the verification overhead. We use
formly select Qwen-RM-72B because it is a larger         NVIDIA H200 for model training and inference.
model and has the best performance.                      Lean4 verification is conducted on CPUs.
3.3     Results                                                             FANS                   FANS
                                                        Dataset                                                FANS
                                                                         (GPT-4o-mini)        (w/o Long CoT)
Table 1 demonstrates that FANS consistently im-
                                                        Number Theory         30.65               37.10         37.10
proves the answer selection accuracy across all base    Prealgebra            57.32               59.76         60.98
models when compared to the baselines. On the           Inter Algebra         16.49               14.43         17.53
two sub-fields, algebra and number theory, where        Algebra               46.77               48.39         50.81
lean4 performs better compared to other fields due      Precalculus           14.29               21.43         19.64
                                                        MATH500-Full          33.80               35.40         37.40
to well-developed support from the language li-
braries, FANS could achieve an accuracy gain up        Table 3: Comparison among different translators with
to 7.90%. On stronger base models like Qwen-           Mistral-7B as the base model.
2.5-Math (Yang et al., 2024b), FANS increases the
accuracy for answer selection by 1.75% as well.                                                               ORM
                                                                                                   ORM
On the harder dataset AMC23, FANS helps weaker                           ORM          ORM                   (Qwen2.5
                                                        Dataset                                  (Qwen2.5
                                                                        (Mistral)   (Deepseek)               -Math)
models to select the correct answer successfully,                                                 -Math)
                                                                                                             + FANS
confirming that FANS working upon the verifiable        Precalculus      30.36        23.21        26.79       26.79
proof process would be more helpful to identify the     Prealgebra       64.63        65.84        73.17       73.17
                                                        Interalgebra     25.77        16.49        24.74       25.77
right answer from multiple wrong ones.
                                                        Algebra          56.45        52.42        60.48       60.48
   Table 2 displays the results with the translator     Number Theory    32.26        30.65        40.32       43.55
from Wang et al. (2025a) and the current SOTA           MATH500          42.40        38.80        45.80       46.40

prover from Ren et al. (2025) at 7B scale. Here
                                                       Table 4: Comparison among different reward models
“FANS remove” means we remove all false posi-          with Mistral-7B as the base model.
tive translations by eliminating those items with
incorrectly selected answers but successfully veri-
fied FL proofs. Therefore, it could be regarded as     presented in Table 3. The results show that the accu-
a kind of upper bound for FANS, while an exact         racy for MATH500 without the Long CoT transla-
one since, if the translations are correct, provers    tor drops significantly, confirming the effectiveness
could prove more FL statements. To ensure better       of Long CoT in providing a more faithful transla-
consistency and fidelity of translated FL statements   tion. Comparison to the results on GPT-4o-mini
with the original NL statements, we introduce an       shows that existing closed-source LLMs have sub-
extra stage to check whether the translations are      optimal performance on FL translation, aligned
correct or not, by invoking the base models them-      with previous studies (Wang et al., 2024b).
selves, or an external stronger model, for example,
                                                       3.4.2 Using different reward models
QwQ-32B (Qwen Team, 2025) here.
                                                       To test the effectiveness of reward models in FANS,
   After the verification of the translations from
                                                       we conduct the ablation study on switching be-
the external model, FANS could achieve uniformly
                                                       tween different kinds of Reward models. In the
better final performance compared to all baselines,
                                                       experiment, we use different reward models to se-
while the verification from the same base models
                                                       lect data generated by Mistral-7B. The results are
could also achieve slight improvements on some
                                                       presented in Table 4. It indicates that the Mistral
datasets. This implies the potential of integrat-
                                                       reward model has the best performance on Mistral
ing FL to assist the answer selection in LLMs’
                                                       generated data while other reward models all suffer
math reasoning, especially by providing a verifi-
                                                       from suboptimal performances. This experiment
able backbone when the translation from natural
                                                       shows that reward models may be unable to gener-
language to formal language is faithful enough.
                                                       alize to OOD model or data. Indicating the need
3.4     Ablation Studies                               for our generalizable answer selection methods.

3.4.1    Dropping Long CoT in Translator               3.5    Qualitative Studies
To validate the effectiveness of the Long CoT trans-   A concrete example through FANS pipeline is dis-
lator in FANS, we conduct the study on dropping        played in 1. From the example, we could see that
the Long CoT translator and replacing it with other    the translator translates the NL statement into its
models. Choices include the fine-tuned transla-        corresponding FL statement correctly, maintaining
tor without Long CoT and GPT-4o-mini. We use           the original semantic meaning and mathematical
few-shot prompts for all models. The results are       formulation without inappropriate modification. In
the proof stage, the prover successfully proves the     Dojo (Yang et al., 2024c) use retrial methods to
FL statement with detailed step-by-step explana-        select tactics; Wang et al. (2024b) tries to use LLM
tions preceding each line, which are omitted here       to translate NL proof to FL proof; MA-LoT (Wang
for brevity. In the example, the question asks for      et al., 2025b) proposed Long CoT and multi-
the solution to a system of equations. Since the        agent framework to solve FL questions; DeepSeek-
original natural language statement is already in       Prover (Xin et al., 2024b,a), Godel-Prover (Lin
a quite standard math format, our translator sim-       et al., 2025), and InternLM-Step-Prover (Wu et al.,
ply transforms the natural language description to      2024b) applies massive data annotation to provide
a formal language expression. The prover gener-         better foundation models. However, all of the
ates a rigorous proof for the statement, which is       above works focus on solving FL problems and
successfully verified by the verifier.                  ignore the potential of using FL to enhance the
                                                        performance of NL math reasoning.
4     Related Work
                                                        4.2   Natural Language Math Reasoning
   Reasoning models, both proprietary like              Recent efforts to enhance the mathematical reason-
OpenAI-O1, Google Gemini Flash Thinking, Kimi-          ing capabilities of large language models (LLMs)
k1.5 (Kimi Team, 2025) and open-sourced ones            have spurred the development of diverse math
such as Qwen Math (Yang et al., 2024b) and              problem-solving techniques. Many works in this
Deepseek-R1 (Xin et al., 2024a), begin to substi-       field focus on developing advanced foundation
tute general language models in the core of LLM         models for solving math word problems such as
research. This stems from not only the representa-      DeepSeek-Math (Shao et al., 2024), Qwen-2.5-
tive of (math) reasoning ability for evaluating the     Math (Yang et al., 2024b), Mistral-Math (Yu et al.,
intelligence of LLMs but also the various down-         2023), and Llemma (Azerbayev et al., 2023). Other
stream tasks it could be applied to and the potential   focus on the inference methods to query the exist-
it reveals about the underlying immense abilities       ing models to write better answers, typical methods
of LLMs to solve complicated problems that can          like traditional Chain-of-Thought (CoT) (Wei et al.,
only be resolved by humans in the past. Zhou et al.     2022; Yao et al., 2025; Xiong et al., 2025; Zhang
(2024) proposed a similar framework to FANS, but        et al., 2025a), tree-search methods (Yao et al., 2023;
their method is heavily prompt-based, built upon        Jiang et al., 2024) and recent proposed Long-CoT
weaker base models, while we train another Long         approaches (OpenAI, 2024; Wang et al., 2025b;
CoT translator and utilize more advanced models         Open-Source-O1, 2024). However, none of them
to generate proofs and translation verification.        jump beyond the context of natural language in
                                                        math reasoning, leading to LLMs’ math reasoning
4.1    Formal Language Reasoning
                                                        without formal foundations.
The Formal Languages (FL) for math reasoning
express mathematical statements in verifiable first-    4.3   Reward Modeling
order logic. By solving math problems using FL,         Reward models play a crucial role in assessing
we can not only verify the correctness of the prob-     the quality of LLMs’ outputs, serving as an essen-
lem by the final answer like MATH (Hendrycks            tial component in downstream applications such
et al., 2021) or GSM8k (Cobbe et al., 2021) but         as reinforcement learning from human feedback
also explicitly verify the correctness of each inter-   (RLHF). These models function as evaluative mech-
mediate steps, making math reasoning has a solid        anisms that guide optimization processes, ensuring
foundation. Typical FL are like Isabelle (Paulson,      that generated responses align with human prefer-
1994), Coq (Coq, 1996), Metamath (Megill and            ences and ethical considerations. Several studies
Wheeler, 2019), HOL Light (Harrison, 2009), and         have incorporated reward models into their RLHF
Lean (De Moura et al., 2015; Moura and Ullrich,         frameworks, highlighting their significance in fine-
2021). Following Yang et al. (2024c), we choose         tuning LLMs (Dong et al., 2024; Bai et al., 2022;
Lean4, the latest and most actively studied FL, as      Ouyang et al., 2022; Dong et al., 2023; Wang et al.,
the language we use.                                    2024a). Depending on the design of how to model
   Traditional studies on FL all focused on how         the rewards, reward models can be categorized into
to annotate more data to boost the performance          both explicit and implicit frameworks. The for-
of LLMs on FL. Representative works like Lean-          mer includes outcome-based or process-based ones
        Demonstration of FANS
        Natural Language Math Problem
                                                               C     D
        Find the product CD of the integers C and D for which x−3 + x+8 = x24x−23
                                                                            +5x−24
                                                                                   for all real values
        of x except −8 and 3.
        Answer −5.
        Translated Formal Language Statement
         theorem math_problem_0 (C D : Z) (h : ∀ x : R, x ̸= 3 ∧ x ̸= -8 → C / (x - 3) + D / (x +
            8) = (4 * x - 23) / (x ^ 2 + 5 * x - 24)) : C * D = -5 := by
        Formal Language Proof
        theorem math_problem_0 (C D : Z) (h : ∀ x : R, x ̸= 3 ∧ x ̸= -8 → C / (x - 3) + D / (x + 8)
            = (4 * x - 23) / (x ^ 2 + 5 * x - 24)) : C * D = -5 := by
            have h1 := h 0 (by norm_num)
            have h2 := h 1 (by norm_num)
            have h3 := h (-1) (by norm_num)
            field_simp at h1 h2 h3
            ring_nf at h1 h2 h3
            norm_cast at h1 h2 h3
            nlinarith




(Ma et al., 2023; Zhang et al., 2025b, 2024b,a; Li       Refining the NL-FL translation process is cru-
and Li, 2024) with each assessing only the final         cial to reducing false positives in theorem formu-
output or intermediate steps respectively. In con-       lation. Errors in translation, such as misrepresent-
trast, implicit reward modeling bypasses the need        ing an equation-solving problem as a tautology or
for explicit reward function engineering by lever-       mishandling extremum problems by misinterpret-
aging preference optimization techniques. Notable        ing constraints, often lead to vacuous proofs and
examples include direct preference optimization          incorrect answer selection. Enhancing the trans-
(DPO) (Rafailov et al., 2024) and other variants         lator to preserve problem constraints accurately
like KTO (Ethayarajh et al., 2024), SimPO (Meng          and explicitly consider optimization conditions can
et al., 2024), IPO (Azar et al., 2024), etc., all of     significantly improve formalization quality.
which aim to refine LLM behavior without explicit
reward function definition.                              Enhancing the proving capabilities of the prover
                                                         is necessary. Lean4’s current package ecosystem
5   Conclusion and Discussion                            is biased toward certain fields like algebra and num-
                                                         ber theory, limiting its applicability in others like
Faced with the gap between existing answer selec-        geometry and combinatorics. Expanding its library
tion methods and the upper bound from models’            support would enable broader coverage of mathe-
intrinsic abilities in the math problem-solving task,    matical domains. Additionally, while the Goedel-
we propose FANS, a framework that introduces a           Prover (Lin et al., 2025) achieves state-of-the-art
formal language-based approach to perform bet-           results on formal language benchmarks (Zheng
ter answer selection, offering a more rigorous and       et al., 2021; Ying et al., 2024), it still struggles
trustworthy alternative to heuristic methods like        with nearly 40% of proof problems. Strengthening
majority voting or best-of-N based on reward mod-        its reasoning abilities through iterative fine-tuning
els. From the experiment results 1, we could see         and improved proof-search strategies could address
FANS indeed improve the accuracy for answer se-          this limitation.
lection, achieving at most a relative improvement           Despite these challenges, the formal verification
of 7.9% on MATH500 Number Theory and 20%                 approach provides a trustworthy and interpretable
on AMC23. This highlights the potential of utiliz-       alternative compared to conventional answer selec-
ing formal language in enhancing answer selection        tion methods. By incorporating rigorously verifi-
for math problem-solving tasks. While it demon-          able Lean4 deductions, FANS reduces dependence
strates notable improvements over baselines, there       on extensive adaptation for different base mod-
is still a gap between its current performance and       els, ensuring consistent and scalable improvements
the theoretical upper bound, i.e., pass @ N. Two         in LLM-driven mathematical reasoning, shedding
primary directions for improvement stand out given       light on a more trustworthy way to better leverage
the two-stage workflow of FANS.                          the capability of existing models.
Limitations                                              References
One major limitation of using formal language for        Mohammad Gheshlaghi Azar, Zhaohan Daniel Guo, Bi-
                                                          lal Piot, Remi Munos, Mark Rowland, Michal Valko,
answer selection is its high false positive rate and
                                                          and Daniele Calandriello. 2024. A general theoret-
the inherent incompleteness of provers, which pro-        ical paradigm to understand learning from human
hibits successfully verifying all factually correct       preferences. In International Conference on Arti-
statements. Errors in formalization, such as in-          ficial Intelligence and Statistics, pages 4447–4455.
correct theorem representations or inadequate con-        PMLR.
straint handling, further lead to misclassification.     Zhangir Azerbayev, Hailey Schoelkopf, Keiran Paster,
Additionally, the limited domain coverage of Lean          Marco Dos Santos, Stephen McAleer, Albert Q Jiang,
4 constrains its applicability to only a subset of         Jia Deng, Stella Biderman, and Sean Welleck. 2023.
mathematical fields.                                       Llemma: An open language model for mathematics.
                                                           arXiv preprint arXiv:2310.10631.
   Future work could focus on improving the ro-
bustness of NL-FL translation, ensuring accurate         Yuntao Bai, Andy Jones, Kamal Ndousse, Amanda
problem formulation, and enhancing the theorem-            Askell, Anna Chen, Nova DasSarma, Dawn Drain,
proving capabilities of provers to handle more com-        Stanislav Fort, Deep Ganguli, Tom Henighan, and 1
                                                           others. 2022. Training a helpful and harmless assis-
plex and diverse mathematical problems. Expand-            tant with reinforcement learning from human feed-
ing the formal proof ecosystem beyond algebra              back. arXiv preprint arXiv:2204.05862.
and number theory will be essential for broader
                                                         Zhe Chen, Weiyun Wang, Yue Cao, Yangzhou Liu,
applicability as well. We believe addressing these
                                                           Zhangwei Gao, Erfei Cui, Jinguo Zhu, Shenglong
challenges will bring formal verification closer to a      Ye, Hao Tian, Zhaoyang Liu, and 1 others. 2024.
more reliable, scalable solution for mathematical          Expanding performance boundaries of open-source
reasoning in LLMs.                                         multimodal models with model, data, and test-time
   For potential risks, since this work focuses on the     scaling. arXiv preprint arXiv:2412.05271.
math reasoning task of LLMs, with no intersection        Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian,
with ethics or other societal questions, we believe        Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias
it currently contains no such risk. Besides, AI            Plappert, Jerry Tworek, Jacob Hilton, Reiichiro
assistants were only used for spelling and grammar         Nakano, and 1 others. 2021. Training verifiers
                                                           to solve math word problems. arXiv preprint
checking during writing.                                   arXiv:2110.14168.

Acknowledgments                                          Projet Coq. 1996. The coq proof assistant-reference
                                                           manual. INRIA Rocquencourt and ENS Lyon, ver-
This research used both the DeltaAI advanced               sion, 5.
computing and data resource, which is supported
by the National Science Foundation (award OAC            Leonardo De Moura, Soonho Kong, Jeremy Avigad,
                                                           Floris Van Doorn, and Jakob von Raumer. 2015. The
2320345) and the State of Illinois, and the Delta ad-      lean theorem prover (system description). In Auto-
vanced computing and data resource which is sup-           mated Deduction-CADE-25: 25th International Con-
ported by the National Science Foundation (award           ference on Automated Deduction, Berlin, Germany,
OAC 2005572) and the State of Illinois.. Delta             August 1-7, 2015, Proceedings 25, pages 378–388.
                                                           Springer.
and DeltaAI are joint efforts of the University of
Illinois Urbana-Champaign and its National Center        Hanze Dong, Wei Xiong, Deepanshu Goyal, Rui Pan,
for Supercomputing Applications. This work is              Shizhe Diao, Jipeng Zhang, Kashun Shum, and
partially supported by NSF grant No. 2416897 and           Tong Zhang. 2023. Raft: Reward ranked finetuning
                                                           for generative foundation model alignment. arXiv
ONR grant No. N000142512318.                               preprint arXiv:2304.06767.

                                                         Hanze Dong, Wei Xiong, Bo Pang, Haoxiang Wang,
                                                           Han Zhao, Yingbo Zhou, Nan Jiang, Doyen Sahoo,
                                                           Caiming Xiong, and Tong Zhang. 2024. Rlhf work-
                                                           flow: From reward modeling to online rlhf. arXiv
                                                           preprint arXiv:2405.07863.

                                                         Kawin Ethayarajh, Winnie Xu, Niklas Muennighoff,
                                                           Dan Jurafsky, and Douwe Kiela. 2024. Kto: Model
                                                           alignment as prospect theoretic optimization. arXiv
                                                           preprint arXiv:2402.01306.
Xinyu Guan, Li Lyna Zhang, Yifei Liu, Ning Shang,         Hunter Lightman, Vineet Kosaraju, Yura Burda, Harri
  Youran Sun, Yi Zhu, Fan Yang, and Mao Yang.               Edwards, Bowen Baker, Teddy Lee, Jan Leike,
  2025. rstar-math: Small llms can master math reason-      John Schulman, Ilya Sutskever, and Karl Cobbe.
  ing with self-evolved deep thinking. arXiv preprint       2023. Let’s verify step by step. arXiv preprint
  arXiv:2501.04519.                                         arXiv:2305.20050.
John Harrison. 2009. Hol light: An overview. In Inter-    Haohan Lin, Zhiqing Sun, Yiming Yang, and Sean
  national Conference on Theorem Proving in Higher          Welleck. 2024.      Lean-star: Learning to in-
  Order Logics, pages 60–66. Springer.                      terleave thinking and proving. arXiv preprint
                                                            arXiv:2407.10040.
Chaoqun He, Renjie Luo, Yuzhuo Bai, Shengding Hu,
  Zhen Leng Thai, Junhao Shen, Jinyi Hu, Xu Han, Yu-      Yong Lin, Shange Tang, Bohan Lyu, Jiayun Wu,
  jie Huang, Yuxiang Zhang, Jie Liu, Lei Qi, Zhiyuan        Hongzhou Lin, Kaiyu Yang, Jia Li, Mengzhou
  Liu, and Maosong Sun. 2024. Olympiadbench:                Xia, Danqi Chen, Sanjeev Arora, and Chi Jin.
  A challenging benchmark for promoting agi with            2025. Goedel-prover: A frontier model for open-
  olympiad-level bilingual multimodal scientific prob-      source automated theorem proving.     Preprint,
  lems. Preprint, arXiv:2402.14008.                         arXiv:2502.07640.
Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul        Qianli Ma, Haotian Zhou, Tingkai Liu, Jianbo Yuan,
  Arora, Steven Basart, Eric Tang, Dawn Song, and Ja-       Pengfei Liu, Yang You, and Hongxia Yang. 2023.
  cob Steinhardt. 2021. Measuring mathematical prob-        Let’s reward step by step: Step-level reward model
  lem solving with the math dataset. arXiv preprint         as the navigators for reasoning. arXiv preprint
  arXiv:2103.03874.                                         arXiv:2310.10080.
Albert Q Jiang, Alexandre Sablayrolles, Arthur Men-       Norman Megill and David A Wheeler. 2019. Metamath:
  sch, Chris Bamford, Devendra Singh Chaplot, Diego         a computer language for mathematical proofs. Lulu.
  de las Casas, Florian Bressand, Gianna Lengyel, Guil-     com.
  laume Lample, Lucile Saulnier, and 1 others. 2023.
  Mistral 7b. arXiv preprint arXiv:2310.06825.            Yu Meng, Mengzhou Xia, and Danqi Chen.
                                                            2024. Simpo: Simple preference optimization
Albert Q Jiang, Sean Welleck, Jin Peng Zhou,                with a reference-free reward. arXiv preprint
  Wenda Li, Jiacheng Liu, Mateja Jamnik, Timo-              arXiv:2405.14734.
  thée Lacroix, Yuhuai Wu, and Guillaume Lample.
  2022. Draft, sketch, and prove: Guiding formal the-     Leonardo de Moura and Sebastian Ullrich. 2021. The
  orem provers with informal proofs. arXiv preprint         lean 4 theorem prover and programming language. In
  arXiv:2210.12283.                                         Automated Deduction–CADE 28: 28th International
                                                            Conference on Automated Deduction, Virtual Event,
Jinhao Jiang, Zhipeng Chen, Yingqian Min, Jie Chen,         July 12–15, 2021, Proceedings 28, pages 625–635.
   Xiaoxue Cheng, Jiapeng Wang, Yiru Tang, Haox-            Springer.
   iang Sun, Jia Deng, Wayne Xin Zhao, and 1 oth-
   ers. 2024. Technical report: Enhancing llm reason-     Niklas Muennighoff, Zitong Yang, Weijia Shi, Xi-
   ing with reward-guided tree search. arXiv preprint       ang Lisa Li, Li Fei-Fei, Hannaneh Hajishirzi, Luke
   arXiv:2411.11694.                                        Zettlemoyer, Percy Liang, Emmanuel Candès, and
                                                            Tatsunori Hashimoto. 2025. s1: Simple test-time
Kimi Team. 2025. Kimi k1.5: Scaling reinforcement           scaling. arXiv preprint arXiv:2501.19393.
  learning with llms.
                                                          Open-Source-O1. 2024. Open-o1. Accessed: 2024-12-
Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying                28.
 Sheng, Lianmin Zheng, Cody Hao Yu, Joseph E.
 Gonzalez, Hao Zhang, and Ion Stoica. 2023. Effi-         OpenAI. 2024.       Learning to reason with
 cient memory management for large language model           llms.            https://openai.com/index/
 serving with pagedattention. In Proceedings of the         learning-to-reason-with-llms/.    Accessed:
 ACM SIGOPS 29th Symposium on Operating Systems             2024-11-24.
 Principles.
                                                          Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida,
Aitor Lewkowycz, Anders Andreassen, David Dohan,            Carroll Wainwright, Pamela Mishkin, Chong Zhang,
  Ethan Dyer, Henryk Michalewski, Vinay Ramasesh,           Sandhini Agarwal, Katarina Slama, Alex Ray, and 1
  Ambrose Slone, Cem Anil, Imanol Schlag, Theo              others. 2022. Training language models to follow in-
  Gutman-Solo, and 1 others. 2022. Solving quan-            structions with human feedback. Advances in neural
  titative reasoning problems with language models.         information processing systems, 35:27730–27744.
  Advances in Neural Information Processing Systems,
  35:3843–3857.                                           Lawrence C Paulson. 1994. Isabelle: A generic theorem
                                                            prover. Springer.
Wendi Li and Yixuan Li. 2024.         Process reward
 model with q-value rankings.         arXiv preprint      Qwen Team. 2025. Qwq-32b: Embracing the power of
 arXiv:2410.11287.                                          reinforcement learning.
Rafael Rafailov, Archit Sharma, Eric Mitchell, Christo-   Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten
  pher D Manning, Stefano Ermon, and Chelsea Finn.           Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou,
  2024. Direct preference optimization: Your language        and 1 others. 2022. Chain-of-thought prompting elic-
  model is secretly a reward model. Advances in Neu-         its reasoning in large language models. Advances
  ral Information Processing Systems, 36.                    in neural information processing systems, 35:24824–
                                                             24837.
ZZ Ren, Zhihong Shao, Junxiao Song, Huajian Xin,
  Haocheng Wang, Wanjia Zhao, Liyue Zhang, Zhe            Thomas Wolf, Lysandre Debut, Victor Sanh, Julien
  Fu, Qihao Zhu, Dejian Yang, and 1 others. 2025.           Chaumond, Clement Delangue, Anthony Moi, Pier-
  Deepseek-prover-v2: Advancing formal mathemati-           ric Cistac, Tim Rault, Rémi Louf, Morgan Funtowicz,
  cal reasoning via reinforcement learning for subgoal      Joe Davison, Sam Shleifer, Patrick von Platen, Clara
  decomposition. arXiv preprint arXiv:2504.21801.           Ma, Yacine Jernite, Julien Plu, Canwen Xu, Teven Le
                                                            Scao, Sylvain Gugger, and 3 others. 2020. Trans-
Marco Dos Santos, Haiming Wang, Hugues de Saxcé,            formers: State-of-the-art natural language processing.
 Ran Wang, Mantas Baksys, Mert Unsal, Junqi Liu,            In Proceedings of the 2020 Conference on Empirical
 Zhengying Liu, and Jia Li. 2025. Kimina lean server:       Methods in Natural Language Processing: System
 Technical report. Preprint, arXiv:2504.21230.              Demonstrations, pages 38–45, Online. Association
                                                            for Computational Linguistics.
Abulhair Saparov, Richard Yuanzhe Pang, Vishakh Pad-
  makumar, Nitish Joshi, Mehran Kazemi, Najoung           Yangzhen Wu, Zhiqing Sun, Shanda Li, Sean Welleck,
  Kim, and He He. 2023. Testing the general deductive       and Yiming Yang. 2024a. Inference scaling laws:
  reasoning capacity of large language models using         An empirical analysis of compute-optimal inference
  ood examples. Advances in Neural Information Pro-         for problem-solving with language models. arXiv
  cessing Systems, 36:3083–3105.                            preprint arXiv:2408.00724.
Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu,           Zijian Wu, Suozhi Huang, Zhejian Zhou, Huaiyuan
  Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan            Ying, Jiayu Wang, Dahua Lin, and Kai Chen. 2024b.
  Zhang, YK Li, Y Wu, and 1 others. 2024. Deepseek-          Internlm2. 5-stepprover: Advancing automated theo-
  math: Pushing the limits of mathematical reason-           rem proving via expert iteration on large-scale lean
  ing in open language models. arXiv preprint                problems. arXiv preprint arXiv:2410.15700.
  arXiv:2402.03300.
                                                          Huajian Xin, Daya Guo, Zhihong Shao, Zhizhou Ren,
Charlie Snell, Jaehoon Lee, Kelvin Xu, and Aviral Ku-       Qihao Zhu, Bo Liu, Chong Ruan, Wenda Li, and
  mar. 2024. Scaling llm test-time compute optimally        Xiaodan Liang. 2024a. Deepseek-prover: Advancing
  can be more effective than scaling model parameters.      theorem proving in llms through large-scale synthetic
  arXiv preprint arXiv:2408.03314.                          data. arXiv preprint arXiv:2405.14333.
Binghai Wang, Rui Zheng, Lu Chen, Yan Liu, Shihan         Huajian Xin, ZZ Ren, Junxiao Song, Zhihong Shao,
  Dou, Caishuang Huang, Wei Shen, Senjie Jin, Enyu          Wanjia Zhao, Haocheng Wang, Bo Liu, Liyue Zhang,
  Zhou, Chenyu Shi, and 1 others. 2024a. Secrets of         Xuan Lu, Qiushi Du, and 1 others. 2024b. Deepseek-
  rlhf in large language models part ii: Reward model-      prover-v1. 5: Harnessing proof assistant feedback for
  ing. arXiv preprint arXiv:2401.06080.                     reinforcement learning and monte-carlo tree search.
                                                            arXiv preprint arXiv:2408.08152.
Haiming Wang, Mert Unsal, Xiaohan Lin, Mantas
  Baksys, Junqi Liu, Marco Dos Santos, Flood Sung,        Wei Xiong, Jiarui Yao, Yuhui Xu, Bo Pang, Lei Wang,
  Marina Vinyes, Zhenzhe Ying, Zekai Zhu, and 1 oth-       Doyen Sahoo, Junnan Li, Nan Jiang, Tong Zhang,
  ers. 2025a. Kimina-prover preview: Towards large         Caiming Xiong, and 1 others. 2025. A minimalist
  formal reasoning models with reinforcement learning.     approach to llm reasoning: from rejection sampling
  arXiv preprint arXiv:2504.11354.                         to reinforce. arXiv preprint arXiv:2504.11343.
Ruida Wang, Rui Pan, Yuxin Li, Jipeng Zhang, Yizhen       An Yang, Baosong Yang, Binyuan Hui, Bo Zheng,
  Jia, Shizhe Diao, Renjie Pi, Junjie Hu, and Tong          Bowen Yu, Chang Zhou, Chengpeng Li, Chengyuan
  Zhang. 2025b. Ma-lot: Multi-agent lean-based long         Li, Dayiheng Liu, Fei Huang, and 1 others.
  chain-of-thought reasoning enhances formal theorem        2024a. Qwen2 technical report. arXiv preprint
  proving. arXiv preprint arXiv:2503.03205.                 arXiv:2407.10671.
Ruida Wang, Jipeng Zhang, Yizhen Jia, Rui Pan, Shizhe     An Yang, Beichen Zhang, Binyuan Hui, Bofei Gao,
  Diao, Renjie Pi, and Tong Zhang. 2024b. Theoreml-         Bowen Yu, Chengpeng Li, Dayiheng Liu, Jian-
  lama: Transforming general-purpose llms into lean4        hong Tu, Jingren Zhou, Junyang Lin, Keming Lu,
  experts. arXiv preprint arXiv:2407.03203.                 Mingfeng Xue, Runji Lin, Tianyu Liu, Xingzhang
                                                            Ren, and Zhenru Zhang. 2024b. Qwen2.5-math tech-
Ruida Wang, Wangchunshu Zhou, and Mrinmaya                  nical report: Toward mathematical expert model via
  Sachan. 2023. Let’s synthesize step by step: Iter-        self-improvement. arXiv preprint arXiv:2409.12122.
  ative dataset synthesis with large language models
  by extrapolating errors from small models. arXiv        Kaiyu Yang, Aidan Swope, Alex Gu, Rahul Chala-
  preprint arXiv:2310.13671.                                mala, Peiyang Song, Shixing Yu, Saad Godil, Ryan J
  Prenger, and Animashree Anandkumar. 2024c. Le-           A       Translator Training Example
  andojo: Theorem proving with retrieval-augmented
  language models. Advances in Neural Information          This section gives examples of the training and
  Processing Systems, 36.                                  inference method for using the transfer learning
                                                           method to train the Long CoT capability of transla-
Jiarui Yao, Yifan Hao, Hanning Zhang, Hanze Dong,          tor based on data without special Long CoT anno-
   Wei Xiong, Nan Jiang, and Tong Zhang. 2025. Opti-
   mizing chain-of-thought reasoners via gradient vari-    tation.
   ance minimization in rejection sampling and rl. arXiv      The prompt for training is as follows:
   preprint arXiv:2505.02391.
                                                           [
Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran,              {
  Thomas L Griffiths, Yuan Cao, and Karthik                      "role": "system",
  Narasimhan. 2023. Tree of thoughts: Deliberate                 "content":"You are a helpful
  problem solving with large language models, 2023.
  URL https://arxiv. org/pdf/2305.10601. pdf.                     ,→ mathematical assistant
                                                                  ,→ specialized in formal language
Huaiyuan Ying, Zijian Wu, Yihan Geng, Jiayu Wang,                 ,→ Lean4. Please translate the
  Dahua Lin, and Kai Chen. 2024. Lean workbook:                   ,→ following natural language
  A large-scale lean problem set formalized from                  ,→ statement into Lean4 theorem
  natural language math problems. arXiv preprint
  arXiv:2406.03847.                                               ,→ statement. You are directly
                                                                  ,→ asked to provide the answer to
Longhui Yu, Weisen Jiang, Han Shi, Jincheng Yu,                   ,→ the problem **WITHOUT** using
  Zhengying Liu, Yu Zhang, James T Kwok, Zhen-                    ,→ the Long Chain of Thought."
  guo Li, Adrian Weller, and Weiyang Liu. 2023.                },
  Metamath: Bootstrap your own mathematical ques-              {
  tions for large language models. arXiv preprint
  arXiv:2309.12284.                                              "role": "user",
                                                                 "content": """@ Natural language
Dan Zhang, Sining Zhoubian, Ziniu Hu, Yisong Yue,                 ,→ theorem statement: Let $a,b,c$
  Yuxiao Dong, and Jie Tang. 2024a. Rest-mcts*: Llm               ,→ be positive real numbers .Prove
  self-training via process reward guided tree search.            ,→ that $ \\frac{b+c}{\\sqrt{a^2 +
  arXiv preprint arXiv:2406.03816.
                                                                  ,→ 8bc}} + \\frac{c+a}{\\sqrt{b^2 +
                                                                  ,→ 8ca}} + \\frac{a+b}{\\sqrt{c^2 +
Hanning Zhang, Jiarui Yao, Chenlu Ye, Wei Xiong,
  and Tong Zhang. 2025a. Online-dpo-r1: Unlocking                 ,→ 8ab}} \\geq 2. $
  effective reasoning without the ppo overhead.
                                                                 @ Lean4 theorem statement:"""
Lunjun Zhang, Arian Hosseini, Hritik Bansal, Mehran            },
  Kazemi, Aviral Kumar, and Rishabh Agarwal. 2024b.            {
  Generative verifiers: Reward modeling as next-token
  prediction. arXiv preprint arXiv:2408.15240.
                                                                 "role": "assistant",
                                                                 "content": """<Thought> The user ask
Zhenru Zhang, Chujie Zheng, Yangzhen Wu, Beichen                  ,→ not to solve with long CoT, so I
  Zhang, Runji Lin, Bowen Yu, Dayiheng Liu, Jin-                  ,→ will directly write the
  gren Zhou, and Junyang Lin. 2025b. The lessons of               ,→ answer.</Thought>
  developing process reward models in mathematical
  reasoning. arXiv preprint arXiv:2501.07301.
                                                                   ```lean4
Kunhao Zheng, Jesse Michael Han, and Stanislas Polu.
                                                                   theorem lean_workbook_0 (a b c : R)
  2021. Minif2f: a cross-system benchmark for for-                 ,→  (ha : 0 < a) (hb : 0 < b) (hc :
  mal olympiad-level mathematics. arXiv preprint                   ,→  0 < c) : (b + c) / Real.sqrt (a
  arXiv:2109.00110.                                                ,→  ^ 2 + 8 * b * c) + (c + a) /
                                                                   ,→  Real.sqrt (b ^ 2 + 8 * c * a) +
Jin Peng Zhou, Charles Staats, Wenda Li, Christian                 ,→  (a + b) / Real.sqrt (c ^ 2 + 8 *
   Szegedy, Kilian Q Weinberger, and Yuhuai Wu.
   2024. Don’t trust: Verify–grounding llm quantita-               ,→  a * b) >= 2 := by
   tive reasoning with autoformalization. arXiv preprint           ```"""
   arXiv:2403.18120.                                           }
                                                           ]
   We use system prompt and user input as the           ===Model Output===
training input and the assistant part as the expected   he `mathd_numbertheory_3` has the
output for our model training. We can see that in       ,→  following conditions:
the system prompt, we indicate the model not to
use Long CoT and in training, we just put a dummy       - The problem asks for the units digit
placeholder for the Long CoT.                           ,→  of the sum of the squares of the
   The inference output is as follows:                  ,→  first nine positive integers.
                                                        - The expected answer is 5.
===Model Input===
<|begin_of_sentence|>Follow these
                                                        So, the theorem should state that the
,→  instructions carefully:
                                                        ,→  units digit of the sum of the
1. Provide a logically correct and
                                                        ,→  squares of the first nine positive
,→  rigorous translate of natural
                                                        ,→  integers is 5.
,→  language theorem statement to Lean4
                                                        </Thought>
,→  statement.
2. In the <Thought> section, include
                                                        <Output>
,→  your detailed step-by-step
                                                        ```lean4
,→  reasoning.
                                                        theorem mathd_numbertheory_3 : (Sum i in
3. In the <Output> section, provide only
                                                        ,→  Finset.range 10, i ^ 2) % 10 = 5 :=
    the final Lean4 proof or final
                                                        ```&
,→

,→  result.### Instruction:You will
                                                        </Output>
,→  receive several Lean4 problems. For
,→  each:                                                  We can see that by using the system prompt to
- **Use** a step-by-step solution                       clearly instruct the model to use Long CoT in in-
,→  internally in <Thought>.                            ference, the model apply its internal bearing Long
- **Do not** reveal your chain of                       CoT capability, together with the Lean4 knowledge
,→  thought outside the <Thought> block.                and statement translation ability learned in transfer
- **Ensure** the final Lean4 code or                    learning. The model can perform accurate transla-
,→  final result is placed **only** in                  tion from NL to FL using Long CoT inference.
,→  <Output>.
@ Natural language theorem statement:                   B     Experiments Details
mathd_numbertheory_3
                                                        B.1    Implementation Settings
What is the units digit of the sum of the
,→  squares of the first nine positive                  For the answer generation, we use vLLM (Kwon
,→  integers? Show that it is 5.                        et al., 2023) as the inference framework, with the
                                                        temperature set to 0.6 to avoid too much repetition,
@ Lean4 theorem statement:                              and set the max tokens allowed to be generated as
### Response:                                           4096. During the first stage of translation, we set
<Thought>                                               the temperature of generation to 0, together with
                                                        the number of max new tokens set to 2048, and use
Alright, I should do the following:                     Transformers (Wolf et al., 2020) as the inference
                                                        framework directly. For the prover, we use vLLM
  1. Analysis the problem and understand                for inference as well and set the temperature to 1.0,
  ,→  the requirements.                                 with the max number of new tokens set to 2048.
                                                           For all experiment results, we evaluate our
  2. Use natural language to analysis                   method FANS on four different base models,
  ,→  the potentional Lean4 condition                   Mistral-7B (Jiang et al., 2023), DeepSeek-Math-
  ,→  and requirements in the natural                   7B-Instruct (Shao et al., 2024), Qwen-2.5-Math-
  ,→  language theorem statement.                       1.5B-Instruct (Yang et al., 2024b), Qwen2-Math-
                                                        7B-Instruct (Yang et al., 2024a), and the results
  3. Write the translated Lean4                         could be found in table 5. We did not include Qwen-
  ,→  statement code.                                   2.5-Math-7B-Instruct as one of our base models
                                                        because during inference we found that it could
      Formal Language Translation Prompt with-           the alignment model to transform the original nat-
      out Natural Language Alignment                     ural language statements into the corresponding
                                                         aligned format. During translation, we keep the
      "{question} Show that it is: {answer}."            temperature as zero, and set the max length of new
                                                         tokens to 1024. To accelerate the inference, we
                                                         utilize the package vLLM (Kwon et al., 2023) as
Figure 3: Formal language translation prompt without
natural language alignment.                              our translation framework. The alignment prompt
                                                         is shown as in Figure 4.
                                                             For a given math question answering problem in
easily generate nonsense outputs not related to the      its original format, the alignment format will be in
math problems until the inference budget is reached.     “Given ... (premises), show that ... (goal)”, or “If
This phenomenon persists no matter what inference        ... (premises), prove that ... (goal)” like standard
framework we use. So as an alternative, we chose         formats. Table 5 demonstrates a concrete example
the 7B model from a version before. Overall, the         of aligning the original natural language statement
performance of the latter two models is better than      into the standard format. From the results in table 6,
the former two. And FANS could achieve uniform           we may notice that whether to use natural language
performance gain among all different base models,        alignment does not affect the overall performance
with a larger margin on weaker base models.              of FANS, so we omit this alignment step in the
   The performance gain on stronger base mod-            other experiments.
els is smaller due to the fact that harder problems          The prompt used for formal language translation
are more challenging to be translated into appro-        without Long-CoT is shown in Figure 6, which
priate natural language statements with consistent       takes advantage of the ability of LLMs’ in-context
meaning and math formulation, and they are hard          learning provided few-shot examples.
to be proved automatically by the prover in stage            Concatenating the formal language statement
two. In an ideal situation, if the success rates for     and the proof header, together with the natural lan-
NL-FL translation and prover are p and q respec-         guage statement as the auxiliary comment, we trig-
tively, and the accuracies for majority vote and pass    ger the prover model and generate potential proofs
@ n are r1 and r2 respectively, then the theoreti-       for the given formal language statements.
cal performance gain of FANS should be roughly               Below we present more concrete examples from
(r2 − r1 ) · pq. This leaves a huge space for future     FANS, verifying that with the assistance of formal
work to improve the current pipeline from both the       language, we could select the correct answer out of
point of views of translator and prover. With better     all possible candidates successfully.
translator achieving lower false positive rates, and /
or better prover which could systematically prove
harder formal language statements, FANS will be
more effective and efficient benefiting from both
aspects.

B.2     Effects of Natural Language Alignment
Without natural language statements alignment, we
directly append the generated answers to the end of
the questions and utilize the concatenated ones as
instructions for the formal language translator. In
this scenario, the prompt used for formal language
translation is table 3.
   However, since the translator model is mainly
trained on the dataset in the aligned format, we
conduct an ablation study on whether natural lan-
guage statement alignment is helpful or not. We
use meta-llama/Llama-3.3-70B-Instruct1 as
   1
     https://huggingface.co/meta-llama/Llama-3.3-70B-
Instruct
Base Model                      Method                Precalculus   Prealgebra    InterAlgebra   Algebra    Number Theory        MATH500    AMC23
                                Pass @ 1                0.1071       0.4954          0.1289      0.3579        0.2681             0.2785     0.0781
                                Pass @ 8                0.3214       0.8049          0.3402      0.6532        0.4677             0.5180     0.3250
Mistral-7B
                                Majority Vote @ 8       0.1786       0.5732          0.1546      0.4274        0.3387             0.3880     0.1250
                                FANS @ 8                0.1786       0.6341          0.1753      0.4597        0.3548             0.3640     0.1500
                                Pass @ 1                0.1696       0.6387          0.2023      0.5998        0.3609             0.4098     0.1687
                                Pass @ 8                0.4107       0.8780          0.4742      0.8548        0.7258             0.6860     0.4500
                                Majority Vote @ 8       0.1786       0.7195          0.3402      0.7177        0.5484             0.5200     0.2250
Deepseek-Math-7B-Instruct
                                FANS @ 8                0.1786       0.7195          0.3608      0.7339        0.5484             0.5240     0.2250
                                ORM @ 8                 0.3750       0.8049          0.4021      0.8226        0.6129             0.6260     0.3000
                                ORM + FANS @ 8          0.3750       0.8171          0.4227      0.8226        0.6613             0.6380     0.3250
                                Pass @ 1                0.5558       0.7774          0.5296      0.8871        0.8165             0.7055     0.4938
                                Pass @ 8                0.7500       0.8902          0.7526      0.9839        0.9839             0.8720     0.8000
                                Majority Vote @ 8       0.6250       0.8415          0.5979      0.9435        0.8871             0.7740     0.6000
Qwen-2.5-Math-1.5B-Instruct
                                FANS @ 8                0.6250       0.8659          0.5979      0.9435        0.8871             0.7760     0.6250
                                ORM @ 8                 0.6607       0.8780          0.6392      0.9677        0.9194             0.8080     0.7000
                                ORM + FANS @ 8          0.6607       0.8780          0.6495      0.9839        0.9355             0.8180     0.7000
                                Pass @ 1                0.5446       0.8110          0.5206      0.8891        0.8145             0.7182     0.4781
                                Pass @ 8                0.7321       0.9302          0.7320      0.9758        0.9677             0.8700     0.8500
                                Majority Vote @ 8       0.6071       0.8780          0.5773      0.9355        0.9194             0.7840     0.5500
Qwen-2-Math-7B-Instruct
                                FANS @ 8                0.5893       0.8659          0.5773      0.9355        0.9194             0.7760     0.5750
                                ORM @ 8                 0.6964       0.8902          0.6289      0.9597        0.9032             0.8180     0.7500
                                ORM + FANS @ 8          0.6964       0.8902          0.6392      0.9597        0.9194             0.8220     0.7500


                                                    Table 5: Full experiments results.




Method                 Precalculus    Prealgebra     InterAlgebra   Algebra      Number Theory   Geometry     Counting & Probability       MATH500
FANS @ 8                    0.2143       0.5976        0.1443       0.4839          0.3710         0.2195               0.2632              0.354
FANS @ 8 aligned NL         0.1786       0.5244        0.1753       0.5081          0.3548         0.3171               0.2368              0.354


         Table 6: Comparision between FANS with aligned natural language statement and original ones.
Natural Language Statements Alignment Prompt

Example list:
====================
``` md
Let q
    a,b,c>0. Prove that:q                  q
  a        bc        b        ca        c        ab             2abc
b+c    (b+a)(c+a) + c+a   (c+b)(a+b) + a+b   (a+c)(b+c) + (a+b)(b+c)(c+a) ≤ 1
```
====================
```md
Let a, b, c ≥ 0 satisfy a + b + c = 3 . Prove that
                                                            81
                     (a2 + 2bc)(b2 + 2ca)(c2 + 2ab) ≤          (ab + bc + ca)
                                                            8

```
====================
```md
If x1 + x2 = −a and x2 + x3 = −b , then x1 − x3 = b − a
```
====================
```md
                                                                                                  3
If a, b, c ∈ [−k, k] where a, b, c, k are real numbers and a+b+c = 0 , show that a3 +b3 +c3 ≤ 3k4
```
====================
```md
If x, y, z > 0 then prove:
                                       3xyz
                                                 p
x2 + y 2 + z 2 − xy − yz − zx + x+y+z         ≥ 3 x2 y 2 z 2
```
====================
Help me transform the following math problem with the given answer to a proof problem, and the
language format of the question should be identical to the example list above, also in the “‘md“‘
structure. Do not modify the given answer even if it is not correct, just transform the format.
Question
```md


                Figure 4: The prompt used for natural language statements alignment.
   Example of Natural Language Statements Alignment

   Question Convert the point (0, 3) in rectangular coordinates to polar coordinates. Enter your
   answer in the form (r, θ), where r > 0 and 0 ≤ θ < 2π.

   Answer
       p Step 1: To convert from rectangular   coordinates to polar coordinates, we use
                                                                                      √the formulas
                                      y
   r = x + y andθ = arctan x . Step 2: In this case, x = 0 and y = 3, so r = 02 + 32 = 3
           2     2

   and θ = arctan 30 = π2 . Step 3: Since 0 ≤ θ < 2π, we have θ = π2 . Step 4: Therefore, the polar
                                        π
   coordinates of the point (0, 3) are 3,    . The answer is: (3, π2 )
                                          2

   Aligned Output Let (x, y) = (0, 3). Prove that the polar coordinates of the point are (3, π2 ).


Figure 5: Example of the aligned natural language statement generated by the alignment model, given the original
question and answer.
Formal Language Translation Prompt without Long-CoT

Convert the following natural language mathematical statement into a corresponding Lean4
statement.
### Natural language statement:
Let q
    a,b,c>0. Prove that:q                  q
  a        bc        b        ca        c        ab             2abc
b+c    (b+a)(c+a) + c+a   (c+b)(a+b) + a+b   (a+c)(b+c) + (a+b)(b+c)(c+a) ≤ 1
### Lean4 statement:
```lean4
theorem lean_workbook_plus_49559 (a b c : R) (ha : 0 < a) (hb : 0 < b) (hc : 0 < c) : (a / (b + c) *
Real.sqrt (b * c / (b + a) * (c + a)) + b / (c + a) * Real.sqrt (c * a / (c + b) * (a + b)) + c / (a + b) *
Real.sqrt (a * b / (a + c) * (b + c)) + 2 * a * b * c / (a + b) / (b + c) / (c + a)) ≤ 1 := by
```&
====================
Convert the following natural language mathematical statement into a corresponding Lean4
statement.
### Natural language statement:
Let a, b, c ≥ 0 satisfy a + b + c = 3 . Prove that
                                                               81
                       (a2 + 2bc)(b2 + 2ca)(c2 + 2ab) ≤           (ab + bc + ca)
                                                                8
### Lean4 statement:
```lean4
theorem lean_workbook_plus_82625 (a b c : R) (ha : a ≥ 0 ∧ b ≥ 0 ∧ c ≥ 0) (hab : a + b + c = 3)
: (aˆ2 + 2 * b * c) * (bˆ2 + 2 * c * a) * (cˆ2 + 2 * a * b) ≤ 81 / 8 * (a * b + b * c + c * a) := by
```&
====================
Convert the following natural language mathematical statement into a corresponding Lean4
statement.
### Natural language statement:
{natural language statement to be translated}
### Lean4 statement:
```lean4


              Figure 6: Formal language translation prompt without Long-CoT instruction.
Formal Language Translation Prompt with Long-CoT

Follow these instructions carefully:
1. Provide a logically correct and rigorous translate of natural language theorem statement to
Lean4 statement.
2. In the <Thought> section, include your detailed step-by-step reasoning.
3. In the <Output> section, provide only the final Lean4 proof or final result.
### Instruction:You will receive several Lean4 problems. For each:
- **Use** a step-by-step solution internally in <Thought>.
- **Do not** reveal your chain of thought outside the <Thought> block.
- **Ensure** the final Lean4 code or final result is placed **only** in <Output>.
@ Natural language theorem statement:
algebra_sqineq_2unitcircatblt1
Show that for any real numbers a and b such that a2 + b2 = 2, ab ≤ 1.
@ Lean4 theorem statement:
theorem algebra_sqineq_2unitcircatblt1 (a b : R) (h0 : a ^ 2 + b ^ 2 = 2) : a * b ≤ 1 :=

====================
@ Natural language theorem statement:
mathd_numbertheory_629
Suppose t is a positive integer such that lcm[12, t]3 = (12t)2 . What is the smallest possible value
for t? Show that it is 18.
@ Lean4 theorem statement:
theorem mathd_numbertheory_629 : IsLeast { t : N | 0 < t ∧ Nat.lcm 12 t ^ 3 = (12 * t) ^ 2 }
    18 :=

====================
@ Natural language theorem statement:
{title} {NL statement}
@ Lean4 theorem statement:
### Response:
<Thought>
Alright, I should do the following:
1. Analyze the problem and understand the requirements.
2. Use natural language to analyze the potential Lean4 condition and requirements in the natural
language theorem statement.
3. Write the translated Lean4 statement code.
The `{title}` has the following conditions


                    Figure 7: Formal Language Translation Prompt with Long-CoT

Header of Formal Proof Prompt

Complete the following Lean 4 code with explanatory comments preceding each line of code:
```lean4
import Mathlib
import Aesop

set_option maxHeartbeats 0
open BigOperators Real Nat Topology Rat


                              Figure 8: Header of Formal Proof Prompt
   More Concrete Examples for FANS Pipeline

   Natural Language Math Problem
   Find the value of log2 3 · log3 4 · log4 5 · log5 6 · log6 7 · log7 8.
   Answer 3
   Translated Formal Language Statement
   theorem math_problem_0 : Real.logb 2 3 * Real.logb 3 4 * Real.logb 4 5 * Real.logb 5 6 *
       Real.logb 6 7 * Real.logb 7 8 = 3 := by


   Formal Language Proof
   theorem math_problem_0 : Real.logb 2 3 * Real.logb 3 4 * Real.logb 4 5 * Real.logb 5 6 *
       Real.logb 6 7 * Real.logb 7 8 = 3 := by
     simp [Real.logb, mul_assoc, mul_comm, mul_left_comm, show (3 : R) = 3 by norm_num,
       show (4 : R) = 2 ^ 2 by norm_num, show (5 : R) = 5 by norm_num, show (6 : R) = 2 * 3 by
       norm_num,
       show (7 : R) = 7 by norm_num, show (8 : R) = 2 ^ 3 by norm_num]
     field_simp
     ring_nf


   Natural Language Math Problem
   A steel sphere with a 3-inch radius is made by removing metal from the corners of a cube that has
   the shortest possible side lengths. How many cubic inches are in the volume of the cube?
   Answer 216
   Translated Formal Language Statement
   theorem math_problem_0 (r : R) (h0 : r = 3) : let cube_side := 2 * r; cube_side ^ 3 = 216 :=
       by


   Formal Language Proof
   theorem math_problem_0 (r : R) (h0 : r = 3) : let cube_side := 2 * r; cube_side ^ 3 = 216 :=
       by
     subst h0
     simp only [pow_three]
     norm_num



Figure 9: More concrete examples that demonstrate formal language could indeed translate the natural language
statement correctly and then prove it successfully.
