                                        TheoremLlama: Transforming General-Purpose LLMs into Lean4 Experts

                                                                   Ruida Wang1 * , Jipeng Zhang1 * , Yizhen Jia1 * , Rui Pan2 ,
                                                                           Shizhe Diao3 , Renjie Pi1 , Tong Zhang2 ,
                                                                      1
                                                                        Hong Kong University of Science and Technology,
                                                                     2
                                                                       University of Illinois Urbana-Champaign, 3 NVIDIA
                                                              Correspondence: rwangbr@connect.ust.hk, jzhanggr@ust.hk, yizhen.jia96@gmail.com,
                                                                 ruip4@illinois.edu, sdiao@nvidia.com, rpi@ust.hk, tongzhang@tongzhang-ml.org



                                                                   Abstract                              systems (Newell and Simon, 1956). Among these
                                                                                                         tasks, mathematical reasoning is considered crucial
                                             Proving mathematical theorems using
                                                                                                         for evaluating the capabilities of Large Language
                                             computer-verifiable Formal Languages (FL)
                                             like Lean significantly impacts mathematical
                                                                                                         Models (LLMs). However, in modern mathemat-
arXiv:2407.03203v2 [cs.FL] 4 Oct 2024




                                             reasoning. One approach to formal theorem                   ics, verifying the correctness of theorem proofs
                                             proving involves generating complete proofs                 written in natural language is challenging, com-
                                             using Large Language Models (LLMs)                          plicating the assessment of LLMs’ mathematical
                                             based on Natural Language (NL) proofs.                      reasoning in advanced topics. Additionally, the
                                             However, due to the scarcity of aligned NL                  rapid development of modern mathematics and the
                                             and FL theorem-proving data, most modern                    increasing complexity of proofs pose significant
                                             LLMs exhibit suboptimal performance. This
                                                                                                         barriers to reviewing their correctness. This has
                                             scarcity results in a paucity of methodologies
                                             for training LLMs and techniques to fully                   led to erroneous proofs that require considerable
                                             utilize their capabilities in composing formal              effort to be identified by the mathematical com-
                                             proofs. To address these challenges, this paper             munity, as exemplified by the process of proving
                                             proposes TheoremLlama, an end-to-end                        Fermat’s Last Theorem (Taylor and Wiles, 1995).
                                             framework that trains a general-purpose LLM                 To address these issues, formal mathematical lan-
                                             to be a Lean4 expert. TheoremLlama includes                 guages such as Lean (De Moura et al., 2015; Moura
                                             NL-FL dataset generation and bootstrapping
                                                                                                         and Ullrich, 2021), Isabelle (Paulson, 1994), and
                                             method to obtain aligned dataset, curriculum
                                             learning and block training techniques to
                                                                                                         HOL Light (Harrison, 2009) have been developed.
                                             train the model, and iterative proof writing                These languages allow computers to automatically
                                             method to write Lean4 proofs that work                      verify proofs, providing a clear standard for evaluat-
                                             together synergistically. Using the dataset                 ing mathematical theorem proofs and significantly
                                             generation method in TheoremLlama, we                       impacting both the mathematical and computer sci-
                                             provide Open Bootstrapped Theorems (OBT),                   ence communities.
                                             an NL-FL aligned and bootstrapped dataset.                     However, writing mathematical proofs in Formal
                                             Our novel NL-FL bootstrapping method,
                                                                                                         Language (FL) requires significant expertise and
                                             where NL proofs are integrated into Lean4
                                             code for training datasets, leverages the                   effort. Additionally, formal proofs involve much
                                             NL reasoning ability of LLMs for formal                     repetitive and tedious work (Jiang et al., 2022a),
                                             reasoning. The TheoremLlama framework                       which is not customary for mathematicians who
                                             achieves cumulative accuracies of 36.48% and                are more familiar with high-level proofs. Conse-
                                             33.61% on MiniF2F-Valid and Test datasets                   quently, there has been significant demand for au-
                                             respectively, surpassing the GPT-4 baseline                 tomated theorem-proving using FL, leading to a
                                             of 22.95% and 25.41%. Our code, model
                                                                                                         considerable number of works on this task (Polu
                                             checkpoints, and the generated dataset is
                                             published in GitHub
                                                                                                         and Sutskever, 2020; Polu et al., 2022; Jiang et al.,
                                                                                                         2021, 2022b,a; Yang et al., 2024). However, most
                                        1    Introduction                                                of these works rely on searching methods in an infi-
                                                                                                         nite space of possible tactics to complete the proof,
                                        The ability to perform logical reasoning has always              resulting in unaffordable computational costs (e.g.,
                                        been regarded as a cornerstone of human intelli-                 Polu et al. (2022) uses 2,000 A100 GPU hours
                                        gence and a fundamental goal of machine learning                 for training) in finishing complex proofs and not
                                            * First authors                                              fully leveraging NL reasoning ability of LLMs. Re-
 (a) NL-FL Aligned Data Generation
                                                                                             Generated NL:
                                                                                             Show that it is false
                                                                                             that ¬a ∧ a.                           NL Annoted Lean4:
                           Data                                                              Proof by contradiction                 theorem not_and_self : ¬(¬a ∧ a)
                         Extraction                                                                                                    -- Proof by contradiction
                                                                                                                                       | ⟨hn, ha⟩ => hn ha
                                                                                             Lean4 code:
                                     100k Lean4                Informalization               theorem not_and_self :
                                                                                             ¬(¬a ∧ a) | ⟨hn, ha⟩ =>
                                                                                                                          NL-FL Bootstrapping                             Open Bootstrapped
                                    Theorem Proofs         with Example Retrieval            hn ha                                                                          Dataset (OBT)

 (b) Lean4 Prover Training          Context length                                                                     (c) Iterative Proof Writing
                                                                   Record 1      Easy data
                                …     i-2   i- 1      i            Record 2
                                                                   Record 3
                                                                                                                                                         Auto Eval
                                …     i-1     i      i+1              ⋮                                                                               Proof Correctness
                                                                  Record N-2
                                …      i    i+1      i+2          Record N-1                                                                                Extract correct       ✅
                                                                  Record N       Hard data
          OBT                  Block Training                                                      Instruction                                            proofs as example
                                                                  Curriculum                                                 Write Proofs for
                                                                                                Finetune Llama3              Lean4 theorems
                                                                  Data Sorting


Figure 1: TheoremLlama Framework: (a) NL-FL Aligned Data Generation: We first extract Lean4 data from
Mathlib4. Subsequently, we fine-tune a T5 encoder to search for the best examples to guide the informalization of
the extracted data. Then, we apply Gemini-1.5 to informalize extracted theorems with retrieved examples. Finally,
we perform NL-FL Bootstraping to integrate natural language reasoning into Lean4 codes. Using this generation
method, we have the OBT dataset. (b) Lean4 Prover Training: We use block training to enhance the in-context
ability and the curriculum data sorting to let LLM learn from easy to hard data. These techniques can make LLM
better learn unfamiliar Lean4 theorem proving tasks. (c) Iterative Proof Writing: We iteratively use the correct
proofs from the same dataset of the previous iterations as in-context examples to enhance the proof-writing ability
of the LLM.

cent advancements in LLMs, especially in reason-                                                     framework comprises three major components that
ing (Wei et al., 2022) and coding (Roziere et al.,                                                   work synergistically:
2023), have prompted researchers to explore us-                                                         (a) NL-FL Aligned Data Generation: This com-
ing them to write formal proofs guided by natural                                                    ponent tackles the data scarcity problem. During
language (Wu et al., 2022; Jiang et al., 2022a).                                                     generation, we identified Mathlib4, a pure Lean4
   In this paper, we focus on enabling general-                                                      repository containing 100k proofs of important
purpose LLMs to write formal Lean4 proofs guided                                                     mathematical theorems. We informalize Mathlib4
by natural language (NL) proofs. We have cho-                                                        (i.e., write natural language theorem statements
sen Lean4 because it has recently garnered con-                                                      and proofs based on Lean4 code) using a Gemini-
siderable attention from the mathematical commu-                                                     1.5 with retrieved examples from a fine-tuned T5
nity (Tao et al., 2023; Tao, 2023; Avigad et al.,                                                    encoder. Subsequently, we bootstrap the NL-FL
2020), whereas Lean3 and Isabelle are older for-                                                     aligned data by integrating the natural language
mal languages. Despite the potential demonstrated                                                    proofs into Lean4 code via comments. This process
by previous works (Wu et al., 2022; Jiang et al.,                                                    of embedding natural language reasoning within
2022a) in similar tasks using Isabelle, the few-shot                                                 the formal language code helps the LLM better
performance of LLMs in Lean4 remains relatively                                                      understand the theorems and leverages its natural
unsatisfactory in Lean 4 (details in Appendix A).                                                    language reasoning ability to perform formal rea-
This is because Lean4 is a more concise FL that dif-                                                 soning. Following this generation and bootstrap-
fers significantly from NL, making the direct trans-                                                 ping method, we create the Open Bootstrapped
fer of reasoning abilities from NL to Lean4 infeasi-                                                 Theorems (OBT) dataset.
ble. The situation is exacerbated by the inclusion                                                      (b) Lean4 Prover Training: This component in-
of confusing Lean3 code in the LLMs’ pre-training                                                    troduces training methods that are currently under-
data (details in Appendix A). More importantly,                                                      studied in the field. It includes block training tech-
there is a significant lack of NL-FL aligned data,                                                   niques to improve the LLM’s in-context learning
making the training of LLMs to write Lean4 proofs                                                    ability and curriculum data sorting tactics to ensure
an overlooked and challenging task. Additionally,                                                    a smoother training process. Using this method, we
Jiang et al. (2022a) indicates that there remains a                                                  fine-tune Llama3-8B-Instruct to be a Lean4 expert
large potential for researchers to fully utilize LLMs                                                with the OBT dataset.
in writing formal proofs.                                                                               (c) Iterative Proof Writing: This component en-
   To address these challenges, we propose The-                                                      hances the LLM’s ability to write formal proofs
oremLlama, an end-to-end framework that trans-                                                       by using previously generated correct proofs as
forms a general-purpose LLM into a Lean4 expert.                                                     in-context examples to further improve its formal
The framework overview is presented in Fig. 1. Our                                                   reasoning capabilities.
   We summarize our contributions in this paper             2.1     NL-FL Aligned Data Generation
as follows: (1) We propose TheoremLlama, an                 This section describes the Natural Language (NL)
end-to-end framework that transforms a general-             - Formal Language (FL) Aligned Dataset Genera-
purpose LLM into a formal proving expert. The-              tion method. As previously discussed, we chose
oremLlama spans from NL-FL aligned dataset                  Lean4 as the formal language for our study. The
generation to Lean4 prover training techniques and          dataset generation aims to enhance the LLM’s abil-
iterative proof writing for Lean4 prover. It amends         ity in Theorem proving from the dataset point-of-
the significant data scarcity problem by contribut-         view. To the best of our knowledge, no open-source
ing to the OBT dataset. Additionally, it contains           Lean4 NL-FL aligned dataset exceeds 1k records,
LLM training and proof writing methods that have            our dataset generation provides Open Bootstrapped
largely been overlooked in Lean4 theorem proving.           Theorems (OBT) dataset containing 106,852 NL-
(2) Our major innovative point is the NL-FL boot-           FL aligned and bootstrapped theorems.
strapping method, which integrates informal proofs
into Lean4 code. this method enhances the LLMs’             2.1.1    Lean4 Proof Extration
abilities by using training data to transfer their infor-   Although there is no NL-FL aligned dataset, for
mal reasoning capabilities to Lean4 proof writing.          Lean4, there is Mathlib4, a repository containing
(3) We conduct extensive experiments using The-             100k high-quality, human-crafted proofs. It is a
oremLlama, which achieves 36.48% and 33.61%                 general repository that contains the most important
accuracy rate on MiniF2F-Valid and Test, largely            definitions and theorems from basic mathematics,
suppressing GPT-4 baseline (25.41% and 22.95%               including logic, set theory, number theory, and alge-
separately). Additionally, we perform a thorough            bra; to advanced topics like topology, differential
ablation study to prove the effectiveness of major          geometry, and real/complex analysis. Mathlib4
components in dataset generation and training.              offers the LLM a high-quality, and comprehen-
   Furthermore, we open-source the OBT dataset,             sive foundation for dataset generation tasks. Previ-
model checkpoints, and codes to support further             ous works have used such a dataset for tree-search
research in the community. Under a reasonable               prover training (Yang et al., 2024; Polu et al., 2022).
GPU footprint for TheoremLlama (the fine-tuning             We directly extract Mathlib4’s theorems from the
only takes about 32 hours for an 8 GPU A6000 ma-            LeanDojo (Yang et al., 2024) repository for further
chine) our work will significantly lower barriers to        dataset generation.
academic researchers in corresponding fields of ob-         2.1.2    Informalization with Example Retrival
taining considerably well-behaved Lean4 prover.
                                                            To the best of our knowledge, the potential for
                                                            using Mathlib4 as a dataset for training LLMs to
                                                            generate formal proofs based on natural language
2   Methodology                                             guidance is an understudied field. This is due
                                                            to Mathlib4 does not contain corresponding nat-
                                                            ural language statements for most of the theorems.
In this section, we present the details of Theo-            However, with the development of modern LLMs,
remLlama, including generation methods for the              we propose a way to generate the NL-FL aligned
OBT dataset. The key idea for our framework is              dataset for Mathlib4. This method, which writes
to enable LLMs to perform well in the unfamil-              informal proofs from formal proofs, is called for-
iar Lean4 theorem proving task under the circum-            malization
stances of limited or even confusing data during its           Due to the mix of Lean4 and Lean3 data on
pre-training. We introduce the Dataset Generation           the internet, LLMs pre-trained on web-scale data
method in Section 2.1, illustrate the training tech-        only have limited ability to recognize Lean4 proofs
niques for Lean4 prover training using the OBT              and may be interfered by perplexing Lean3 data
dataset in Section 2.2, and propose an Iterative            (Appendix A.) Therefore, it is important to have
Proof Writing method LLM prover in Section 2.3.             high-quality in-context examples for informaliza-
The task that this methodology works on can be de-          tion. Inspired by the idea of contrastive loss (Izac-
fined as: "Training the general purpose LLM to be           ard et al., 2021). We develop the example retrieval
an expert in Lean4 whole-proof generation under             method to extract such high-quality examples. The
the guidance of Natural Language Proofs."                   first step for our example retrieval is using the Nat-
ural Language annotated MiniF2F dataset (Jiang         largely improve the performance of LLM coders.
et al., 2022a) to fine-tune the ByT5-Tacgen model      We propose the novel NL-FL Bootstrapping. This
provided by Yang et al. (2024), which trained on       is a simple but effective method to enhance the
pure Lean4 data, has a relative good understanding     LLMs’ Lean4 proof writing ability by integrating
of both NL and FL data.                                natural language reasoning into Lean4 proofs in
   Specifically, we fine-tune the ByT5 encoder to      Mathlib4.
align the cosine similarity of the theorem statement      We achieve such an integration by providing
of natural language and Lean4 code. The sentence-      Gemini with NL and FL of the theorem and ask-
level encoding is obtained by mean pooling of ev-      ing it to document the natural language proof to
ery token’s encoding. To prevent the model from        the Lean4 code through comment. We ensure the
producing trivial results, we add in-batch negative    correctness of the bootstrapped data by running a
sampling in the loss function. Thus, the loss for      check algorithm that removes all comments in the
fine-tuning ByT5 is:                                   generated code and makes sure it is the same as the
                                                       original code.
    L =1 − cos(xN L , xF L )+                             This bootstrapping approach aims to lower the
         1       (−)                        (−)        barrier between complex and unfamiliar-to-LLM
           (cos(xN L , xF L ) + cos(xN L , xF L ))
         2                                             Lean4 formal language reasoning and natural lan-
where xN L/F L represents sentence encoding; x(−)      guage reasoning. We find that most modern LLMs
means not aligned NL/FL statement in the same          possess relatively strong natural language reason-
batch as the negative sample.                          ing abilities but lack familiarity with formal rea-
   Subsequently, we use this encoder to encode the     soning. This method helps LLMs transfer their
Lean4 theorem statement in Mathlib4 and the in-        natural language reasoning skills to Lean4 theo-
formal theorem statement in a tiny NL-FL aligned       rem proving by bootstrapping the dataset, prompt-
dataset (less than 100 theorem proofs, provide by      ing the LLM to perform both formal and informal
Yang et al. (2024)). We select a few examples with     reasoning simultaneously. LLMs trained with the
the highest similarity and use these as in-context     bootstrapped dataset will learn to better utilize the
examples to query Gemini-1.5 (Reid et al., 2024) to    NL steps to guide Lean4 proof writing. Follow-
obtain informalized theorem statements and proofs      ing above generation and bootstrapping method,
for the theorems in Mathlib4.                          we have the Open Bootstrapped Theorems (OBT)
   After informalization, we conduct a primary-        dataset for training LLMs.
level data quality check. Wu et al. (2022) found
that most of the informalization made by LLMs          2.2     LLM Prover Training
generally makes sense so our quality check ma-         Training LLMs to generate whole proof based on
jorly focuses on removing abnormal behavior of         natural language guidance is an under-explored
LLMs, including repeated generation, overlength        field of study due to the lack of datasets. There are
generation, and other erroneous data. We iteratively   only a few studies that discuss the training method
query the Gemnin-1.5 with failed examples, and         of the LLM for such a task. This section proposes
ultimately, we obtain an NL-FL aligned dataset con-    two instruction fine-tuning techniques to train the
sisting of 106,852 theorems, a much larger dataset     LLMs for formal reasoning tasks, namely Block
than any currently open-sourced NL-FL aligned          Training and Curriculum Data Sorting.
dataset for Lean4.
                                                       2.2.1    Block Training
2.1.3   NL-FL Bootstrapping                            The Block Training method aims to incorporate
We find that due to the significant differences        the in-context learning ability during training. For
between performing natural language reasoning          standard instruction fine-tuning in formal theorem
and Lean4 theorem proving, externally NL-guided        proving, we use natural language as the input and
training data is not sufficient to enable LLMs to      the corresponding Lean4 with bootstrapped NL rea-
develop strong Lean4 theorem-proving abilities. It     soning as the target output to fine-tune the LLM. In
is common for the LLMs to lose track of the proof      the Block Training, we view the tokenized training
and repeatedly generate the final Lean4 tactic. In-    dataset as a ring of text. We take full advantage
spired by findings in LLM coder (Song et al., 2024),   of the context length of LLM by filling it with ex-
where NL comments of code task description can         amples of previous records. Formally, the original
training data for i-th record is:                            2.3     Iterative Proof Writing
        {"Instruction": N Li , "Target": F Li }              Jiang et al. (2022a) have demonstrated that the
                                                             potential of LLMs in formal reasoning is largely
where N Li is the natural language of i-th record            undervalued. Typically, LLMs possess relevant
and F Li is its corresponding bootstrapped Lean4             knowledge but lack appropriate methods to extract
code. After Block Training, the i-th data record is:         this knowledge in Lean4 form. To further harness
{"Instruction": “N Li−k , F Li−k ; · · · F Li−1 ; N L′′i ,   the LLM’s ability to prove Lean4 theorems, in-
                                                             spired by Wang et al. (2023), we propose the Itera-
 "Target": “F L′′i }
                                                             tive Proof Writing strategy. This method involves
  where k is the number of examples that just fill           initially having the prover finish as many theorems
the context length.                                          in a dataset as possible. Then, use the Lean-verified
  Using the block training method, we enhance                correct proofs written by the current prover as ad-
the LLM’s in-context learning ability for Lean4,             ditional examples for proof writing in the next it-
providing a better understanding of examples when            eration. The iteration stops when the maximum
writing proofs.                                              number of steps is reached or no additional theo-
                                                             rems can be proved with the given examples. This
2.2.2    Curriculum Data Sorting                             step is effective because there are potential distribu-
Because modern LLMs have limited exposure to                 tion shifts between the generated and the real-world
writing Lean4 proofs with NL guidance during                 natural language statement and proof, using exam-
pre-training, they are unfamiliar with this task.            ples from the same dataset, such differences can be
This issue is evident as LLMs with a significant             largely mitigated.
difference in parameters show only slight perfor-
                                                             3     Experiments
mance differences in these tasks (details in Sec-
tion 3.3). Inspired by previous work in Curriculum           We conduct extensive experiments on the MiniF2F-
Learning (Polu and Sutskever, 2020; Soviany et al.,          Lean4 dataset (Zheng et al., 2021) to test the effec-
2022), we propose a training data sorting technique          tiveness of TheoremLlama framework on formal
named Curriculum Data Sorting to enable LLMs                 reasoning with NL guidance. We also conduct
to learn this unfamiliar task from easy to difficult.        ablation studies (Section 3.4) and case studies (Sec-
   Specifically, we reorganize the generated train-          tion 3.7) to further validate the TheoremLlama.
ing dataset by difficulty level. We measure the
difficulty of a Lean4 proof by the steps it takes to         3.1     Experiment Setup
solve all goals and sort the training data records           3.1.1    Dataset and Task
with easier data at the beginning and harder data            In this work, we evaluate the TheoremLlama
at the end. This sorting method allows the LLM               Lean4 formal reasoning ability on MiniF2F-Test
to first learn to solve trivial and easy problems be-        and Validation dataset (Zheng et al., 2021) and
fore tackling complex proofs. It largely stabilizes          NL theorem statement and proofs provided by
the loss curve of training and improves the perfor-          Jiang et al. (2022a). We contribute the Lean4 ver-
mance of the LLM prover.                                     sion of MiniF2F-Test based on (Yang et al., 2024).
                                                             MiniF2F is a standard testing dataset for evaluat-
2.2.3    Instruction Fine-tuning                             ing the performance of formal provers. Both the
Using Blocked Training and Curriculum Data Sort-             test and validation datasets contain Lean4 state-
ing on the OBT dataset, we perform the Instruc-              ments of 244 problems. The range of problems
tion Fine-tuning on Llama3-8B-Instruct using SFT             varies from high-school competition questions to
trainer in an autoregressive manner. The given in-           undergraduate-level theorem proofs. Specifically,
struction is a natural language statement and proof          MiniF2F comprises a total of 488 problems from
of a theorem, along with a Lean4 theorem state-              three sources: (1) 260 problems sampled from the
ment, and use examples in the dataset filling con-           MATH dataset (Hendrycks et al., 2021); (2) 160
text windows. The target output is the Lean4 proof           problems from high-school mathematical compe-
bootstrapped with natural language explanations.             titions (including AMC, AIME, and IMO); (3) 68
This process trains the LLM to leverage its natural          manually crafted problems at the same difficulty
language reasoning ability to write Lean4 proofs.            level as (2). We are unable to use the Mathlib
                          Method            Model size    MiniF2F-Valid     MiniF2F-Test      Average
                    Tree-search Methods
                      Expert Iteration         774M            28.5%             25.9%         27.2%
                         ReProver              229M               -             25.00%           -
                      Unfinetuned LLM
                       GPT-4-Turbo             > 1T            25.41%           22.95%        24.18%
                      Gemini-1.5-pro             -             29.92%           27.87%        28.90%
                      Llama3-Instruct           8B             25.41%           20.08%        22.75%
                      Math Expert LLM
                         Llemma                 31B            21.03%           22.13%        21.58%
                      DeepSeek-Math              7B            25.80%           24.60%        25.20%
                      TheoremLlama              8B             36.48%           33.61%        35.04%

Table 1: Main experimental results. Each LLMs result takes 128 rounds of generation, TheoremLlama are
cumulative results for multiple iterations of proofs

dataset for comparison because some baselines                   et al., 2023)2 , Gemini-1.5 (Reid et al., 2024), and
does not open-source their train-test split of such             Llama3-8B-Instruct (AI@Meta, 2024). This base-
dataset.                                                        line is set to compare the TheoremLlama’s ability
   Our task is to query LLM to generate the com-                to perform formal reasoning effectively. (4) Mathe-
plete Lean4 proofs for the mathematical problems                matical LLMs: This baseline uses LLMs that are
in MiniF2F based on their Lean4 statement and NL                specifically trained in massive math-related corpus
statement and proof together using no more than 16              to perform whole proof generation. In particular,
in-context examples. All the imports are manually               we choose: Llemma (Azerbayev et al., 2023b), and
set to lighten the workload of LLM.                             DeepSeek-Math-7B (Shao et al., 2024) as the base-
                                                                lines. This aims to demonstrate under fine-tuned
3.1.2 Baseline                                                  general-purpose LLMs can outperform math expert
Due to the lack of previous studies that use LLMs               model under some cricumstances.
to generate complete proofs for Lean4; and most                    Following the results from (Yang et al., 2024;
of the existing works working on Reinforcement                  Polu et al., 2022), we adopt pass@1 for all tree-
Learning (RL) or searching methods, there are                   search methods to ensure a consistent comparison
no universally approved baselines for compari-                  under a similar GPU footprint during evaluation.
son. Many existing works are focusing on Is-                    The variation in the number of parameters for tree-
abelle (Jiang et al., 2022a,b; Wu et al., 2022), a              search models also stems from our aim to maintain
language that is largely different from Lean4, mak-             comparable computational costs. Specifically, our
ing direct comparison infeasible (Yang et al., 2024).           primary consideration for selecting baselines was
Many Lean-based methods concentrate on online                   to ensure the inference cost remains on the same
iteration with Lean (Lample et al., 2022; Polu et al.,          scale, with an inference cost of 1.5 A6000 GPU
2022).                                                          days.
   Therefore, our baseline selection focuses on tree-
based methods without RL and few-shot LLM                       3.2     Implementation Details
proof writing. The baselines we use include: (1)                The OBT dataset is generated using Gemini-
Expert Iteration (Polu et al., 2022): A tree search             1.5 (Reid et al., 2024) for writing the natural lan-
method based on GPT-f (Polu and Sutskever, 2020)                guage of the theorems and performing NL-FL boot-
that applies expert iteration to enhance the perfor-            strapping. We use Gemnin-1.5 because it can
mance1 ; (2) ReProver (Yang et al., 2024): The                  give more human-like proofs and a better abil-
Lean4 tree-search baseline that builds on ByT5                  ity in NL-FL combination, details can be found
to search for tactics based on current formal state             in Appendix D. The OBT dataset contains NL-
and goal. (3) Few-shot LLMs: This baseline fo-                  FL aligned and bootstrapped 106,852 theorems,
cuses on directly querying LLMs to get the full                 the data record format is in Appendix E. We per-
proof of a formal theorem in a few-shot manner.                 form Instruction Fine-tuning on Llama3-Instruct-
In particular, we choose GPT-4-Turbo (Achiam                    8B (AI@Meta, 2024) with 1,000 warm-up steps
   1
    Since full training of such methods uses closed source      and a learning rate of 1E-5. Training takes approx-
model and full training of such models takes more than 2,000
                                                                   2
A100 GPU hours, for a fair comparison, we use θ1 result as           From (Bambhaniya et al., 2024), we infer the parameter
baseline                                                        size of GPT-4 Trubo to be larger than 1T
          Method               MiniF2F-Valid   MiniF2F-Test   3.4   Ablation Studies
       TheoremLlama               34.84%         31.15%
      w/o NL Guidance             24.18%         17.21%       Due to the low GPU footprint of TheoremLlama,
      w/o Bootstrapping           26.23%         26.23%       we are able to perform a comprehensive ablation
     w/o Block Training           27.87%         23.36%       study to test the effectiveness of each component
 w/o Curriculum Data Sorting      29.51%         25.83%
                                                              in the framework, namely, NL guidance, NL-FL
             Table 2: Ablation study result                   bootstrapping, block training, and curriculum data
                                                              sorting. In the ablation studies, we use the result
imately 32 hours on an 8 GPU A6000 machine.                   of the first iteration with the default example list
During the evaluation, we perform a uniform 128               from Yang et al. (2024). The results are demon-
generation for LLM’s whole-proof generation. The              strated in Tab. 2. From the table, we can find that
initial examples for in-context learning are obtained         the removal of any component of our framework
from the proved theorem list of Yang et al. (2024).           will lead to a significant performance drop com-
Depending on the context length, we use 10-16 ex-             pared to the full framework result, which proves
amples for all LLM queries. We stop at the second             that modules we propose are not trivial combina-
round of iterative proof writing.                             tions, but work synergically to enhance the perfor-
   For few-shot LLM baselines, we use GPT-4-                  mance.
Turbo-0409 and Gemini-1.5-preview-0409 to per-                   In the removal of NL Guidance, we perform the
form formal reasoning. Since both models are re-              experiment under the setting without NL in train-
leased after Mathlib4, so they can have such data in          ing data but use the NL examples and NL guidance
their training set, which makes a fair comparison.            in the testing data. The accuracy rate dropped sig-
                                                              nificantly, and the fine-tuned model does not out-
3.3   Results                                                 perform the untrained model. This indicates that
                                                              merely more exposure to Lean4 proof code does
We present the main experimental results in                   not improve the ability of LLM in formal reasoning.
Tab.1. From the table, we can observe that Theo-              When we remove the NL-FL bootstrapping, the per-
remLlama achieves a cumulative accuracy rate                  formance drops because the LLM often loses track
of 36.48% on MiniF2F-Valid and 33.61% on                      of the proof and keeps on generating the same tac-
MiniF2F-Test, suppressing all the baselines.                  tic. With bootstrapping, the performance is much
   It is also notable that the result of un-finetuned         better due to the NL guidance.
Llama3-8B-Instruct and GPT-4 have a similar accu-                The ablation study also shows that removing
racy rate on both the Test and Valid set despite the          block training results in a performance drop, which
great difference in model size, this demonstrates             we attribute to the distribution shift between train-
most modern LLMs are under-trained on Lean4                   ing and testing data. Without block training, the
reasoning. Surprisingly, Gemini has the best perfor-          training data lacks information about in-context
mance among all the baselines rather than GPT-4;              examples, while the testing phase includes this in-
this demonstrates its superior ability to understand          context knowledge for the LLM to learn. Addition-
formal language and gives indirect evidence that              ally, removing curriculum data sorting also leads
Gemini is a better choice of LLM to perform Infor-            to a performance decline. Curriculum data sorting
malization and Bootstrapping.                                 provides a smoother training process by ensuring
   For the tree-search method, the large search               that lengthy and difficult examples do not appear
space limits the choice of model in relatively small          early on and disrupt learning.
size and they only achieve an average 27.2% ac-                  Despite performance drop when removing the
curacy rate, which is relatively low, demonstrating           individual component, with other components, our
the limitation of such a method.                              method still outperforms un-finetuned Llama3 ex-
   For the math-expert models, we can spot that               cept for without the NL guidance. It supports the
TheoremLlama also significantly outperforms                   effectiveness of other components from another
them. This shows that large math-related code and             perspective.
text pertaining itself does not naturally provide the
                                                              3.5   Iterative Proof Writing study
formal reasoning ability. This also demonstrates
the effectiveness of our fine-tuning to transform a           This section gives a closer look into the behavior
general-purpose model into a Lean4 expert.                    of different rounds of iterative proof writing as
      Method     MiniF2F-Valid     MiniF2F-Test           kindly refer to Appendix B.
      Round 1        34.84%           31.15%              NL Statement: Let a and b be two real numbers
      Round 2        36.48%           33.61%              such that a2 + b2 = 1. Show that ab + (a − b) ≤ 1
                                                          NL Proof: We have that (a − b − 1)2 ≥ 0. By
  Table 3: Different rounds of iterative proof writing
                                                          expanding, we have: 0 ≤ a2 − ab − a − ab +
                                                          b2 + b − a + b + 1. Since a2 + b2 = 1, we get
                                                          0 ≤ 2−2ab−2a+2b. As a result, ab+(a−b) ≤ 1.
                                                          Generated Proof:
                                                          theorem algebra_sqineq_unitcircatbpamblt1
                                                            (a b: R)
                                                            (h0 : a^2 + b^2 = 1) :
                                                            a * b + (a - b) ≤ 1 := by
                                                            -- We have that (a - b - 1)^2 ≥ 0.
                                                            have h1 : 0 ≤ (a - b - 1) ^ 2 := sq_nonneg _
                                                            -- By expanding, we have:
                                                            -- 0 ≤ a^2 -ab-a-ab+b^2 +b-a+b+1.
                                                            linarith [h0 , sub_add_cancel a b]
Figure 2: Histogram for all combinations of NL state-        From the generated proof, we can see that the
ment in example list and FL statement in Mathlib4
                                                          LLMs learn from the data to obtain the condition of
demonstrated in the Tab.3. From the table, we can         ≥ 0 in Lean and use the correct condition expres-
see that when using the example from the same             sion. Also, it learns to use the lean tactic linarith
dataset for proof writing, there is a 2% accuracy         to expand the inequality to obtain correct proof,
increment in pass rate. This shows that our iterative     which shows the Lean4 ability that LLM obtained
proof writing method can reduce the distribution          in fine-tuning. This example also demonstrates
gap between testing data and examples to some             the effectiveness of using external and in-code NL
extent.                                                   proof to guide LLM in writing Lean4 proofs, which
                                                          qualitatively validate the NL guidance and NL-FL
3.6   Effectiveness of Example Retrieval                  bootstrapping method.
This section studies the effectiveness of our fine-       4     Related work
tuned T5 for example retrieval using graphical
methods. We encode all the formal theorem state-          4.1    Formal Reasoning
ments in Mathlib4 and the natural language theo-          Formal mathematical languages express mathemati-
rem statement in the example list following Sec-          cal statements in first-order logic. Such verification
tion 2.1.2. We then compare the cosine similarity of      systems for mathematics are also known as Inter-
all possible combinations of the formal and natural       active Theorem Provers (ITPs). There are many
language theorem statement set.                           ITP languages such as Isabelle (Paulson, 1994),
   From the two peaks in the histogram at cos sim-        Lean (De Moura et al., 2015; Moura and Ullrich,
ilarities of 1.0 and 0.0 in Fig. 2, we can see that       2021), Coq (Coq, 1996), Metamath (Megill and
our example selection model is certain about its          Wheeler, 2019), and HOL Light (Harrison, 2009).
prediction. Plus a low testing loss that we observed      The formal languages embed mathematical defini-
when training the model, means its performance            tions and theorems onto a concrete logical founda-
is relatively good. We can say our retriever can          tion in their kernels. Following Polu et al. (2022),
largely distinguish similar and different informal        we work on Lean because Lean proves are typically
statements in the example list and formal state-          more concise and relatively understudied.
ments in Mathlib4.                                           Many works focus on automatically complet-
                                                          ing formal reasoning using machine learning-based
3.7   Case study                                          methods. Some use more traditional methods like
We analyze the behavior of TheoremLlama by ex-            K Nearest Neighbor (KNN) (Gauthier et al., 2021)
amining the proofs generated by the theorem prover        or Graph Neural Network (GNN) (Yang and Deng,
from MiniF2F-Test in Lean4. Since MiniF2F-Test            2019). Others take advantage of the recent devel-
is a dataset that does not have publicly available        opment of deep transformer-based methods that
proof, it is highly unlikely it will be included in the   treat theorems as plain texts. Among them, Expert
training dataset of any LLM. For more case studies,       Iteration (Polu et al., 2022) and ReProver (Yang
et al., 2024) focus on training existing LLMs to          erated data. We also conduct comprehensive exper-
generate tactics and perform a tree search to com-        iments to evaluate the effectiveness of Theorem-
plete the proofs. Other methods focus on exploring        Llama, where our framework successfully proves
the few-shot capability, allowing LLMs to directly        36.48% and 33.61% of the theorems in MiniF2F-
generate the whole proof based on the guidance            Valid and Test, respectively, surpassing the GPT-4
of natural language (Wu et al., 2022; Jiang et al.,       and Gemini-1.5 baselines. We will open-source all
2022a). Although there are some attempts to con-          the datasets to facilitate further development in the
struct aligned datasets for theorem proofing (Azer-       field.
bayev et al., 2023a; Ying et al., 2024), there is still
no large-scale NL-FL aligned dataset. This leads          6   Discussion
to the fact that there are currently no universally       Although large-scale pre-train provides LLMs with
recognized methods for training LLMs to generate          strong abilities in most general tasks, there are
whole proof directly.                                     many corner cases that lack data for any machine
                                                          learning methods to be effective. Formal reason-
4.2    Dataset Generation
                                                          ing is one of the most significant examples. From
Modern machine learning methods typically re-             a border perspective, TheoremLlama sheds light
quire massive datasets to learn an application. How-      on a general framework to further apply modern
ever, it is impractical to have high-quality data for     LLMs to such corner cases. It contains methods
every corner case, prompting researchers to explore       to leverage existing incomplete data, techniques to
dataset generation. By combining existing incom-          better train LLMs for unfamiliar tasks, and strate-
plete data with the rich knowledge in LLMs, dataset       gies to enhance LLM’s performance in application.
generation can leverage this knowledge to produce         Thus, the contribution of this paper is not limited
a complete dataset suitable for model training. Ini-      to the field of formal reasoning but gives a general
tial attempts have achieved this through fine-tuned       framework for the further usage of LLMs in corner
generative models (Anaby-Tavor et al., 2020; Chen         cases.
et al., 2020). Other researchers explore zero-shot
or few-shot performance for modern LLMs by di-            Acknowledgement
rectly querying the LLMs to obtain the intended           We thank the anonymous reviewers for their feed-
dataset (Meng et al., 2022; Gao et al., 2022; Wang        back on our paper. We also want to express our
et al., 2023). In this work, we take advantage of         greatest gratitude to Professor Frederick Tsz-Ho
these ideas for dataset generation to obtain the OBT      Fong at HKUST for his generous support in the
dataset.                                                  mathematical aspect of this paper.

5     Conclusion                                          Limitations
This paper proposes TheoremLlama, an end-to-              Despite the promising results of TheoremLlama,
end framework for transforming a general-purpose          there are still some limitations in our work that can
LLM into a Lean4 expert, along with the Open              be addressed in future research. First, even with nat-
Bootstrapped Theorems (OBT) dataset, a NL-FL              ural language proofs to guide Lean4 proof writing,
aligned, bootstrapped dataset for training an LLM         all existing formal provers, including Theorem-
Lean4 prover. This work largely addresses the sig-        Llama, struggle with solving difficult IMO-level
nificant data scarcity problem by introducing the         problems. We conclude that LLMs currently lack
NL-FL Aligned Dataset Generation method, which            the ability to understand the intricate technical as-
is used to create the OBT dataset. Subsequently,          pects of human proofs. Integrating the "kindles" in
we demonstrate block training and curriculum data         human-written proofs into LLMs is an overlooked
sorting techniques to enhance LLM training. Fur-          area in current research. Secondly, due to the com-
thermore, we present the Iterative Proof Writing          plexity of the Lean4 kernel, this paper does not
tactic to better utilize the LLM’s capability in the-     explore the potential of RL methods for enabling
orem proving. The major innovation of this work           LLMs to write formal proofs through online inter-
is the NL-FL bootstrapping method, which enables          action with Lean, nor does it incorporate feedback
the LLM to better transfer its natural language rea-      from Lean to refine incorrect proofs. This requires
soning ability to Lean4 proof writing through gen-        deeper integration of Lean and Python. Thirdly,
although formal language provides a concrete foun-           lean theorem prover (system description). In Auto-
dation for verifying the correctness of mathemat-            mated Deduction-CADE-25: 25th International Con-
                                                             ference on Automated Deduction, Berlin, Germany,
ical proofs, there are potential risks that a natural
                                                             August 1-7, 2015, Proceedings 25, pages 378–388.
language-guided Lean4 prover may automatically               Springer.
correct some errors in natural language. This could
                                                           Jiahui Gao, Renjie Pi, Yong Lin, Hang Xu, Jiacheng
lead to errors in natural language being considered           Ye, Zhiyong Wu, Weizhong Zhang, Xiaodan Liang,
correct and cause wrong natural language proofs to            Zhenguo Li, and Lingpeng Kong. 2022. Self-guided
be subsequently propagated within the mathemati-              noise-free data generation for efficient zero-shot
cal community.                                                learning. arXiv preprint arXiv:2205.12679.
                                                           Thibault Gauthier, Cezary Kaliszyk, Josef Urban, Ra-
                                                             mana Kumar, and Michael Norrish. 2021. Tactictoe:
References                                                   learning to prove with tactics. Journal of Automated
                                                             Reasoning, 65(2):257–286.
Josh Achiam, Steven Adler, Sandhini Agarwal, Lama
  Ahmad, Ilge Akkaya, Florencia Leoni Aleman,              John Harrison. 2009. Hol light: An overview. In Inter-
  Diogo Almeida, Janko Altenschmidt, Sam Altman,             national Conference on Theorem Proving in Higher
  Shyamal Anadkat, et al. 2023. Gpt-4 technical report.      Order Logics, pages 60–66. Springer.
  arXiv preprint arXiv:2303.08774.
                                                           Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul
                                                             Arora, Steven Basart, Eric Tang, Dawn Song, and Ja-
AI@Meta. 2024. Llama 3 model card.
                                                             cob Steinhardt. 2021. Measuring mathematical prob-
                                                             lem solving with the math dataset. arXiv preprint
Ateret Anaby-Tavor, Boaz Carmeli, Esther Goldbraich,
                                                             arXiv:2103.03874.
  Amir Kantor, George Kour, Segev Shlomov, Naama
  Tepper, and Naama Zwerdling. 2020. Do not have           Gautier Izacard, Mathilde Caron, Lucas Hosseini, Se-
  enough data? deep learning to the rescue! In Pro-          bastian Riedel, Piotr Bojanowski, Armand Joulin,
  ceedings of the AAAI conference on artificial intelli-     and Edouard Grave. 2021. Unsupervised dense in-
  gence, volume 34, pages 7383–7390.                         formation retrieval with contrastive learning. arXiv
                                                             preprint arXiv:2112.09118.
Jeremy Avigad, Kevin Buzzard, Robert Y Lewis, and
   Patrick Massot. 2020. Mathematics in lean.              Albert Q Jiang, Sean Welleck, Jin Peng Zhou,
                                                             Wenda Li, Jiacheng Liu, Mateja Jamnik, Timo-
Zhangir Azerbayev, Bartosz Piotrowski, Hailey                thée Lacroix, Yuhuai Wu, and Guillaume Lample.
  Schoelkopf, Edward W Ayers, Dragomir Radev, and            2022a. Draft, sketch, and prove: Guiding formal
  Jeremy Avigad. 2023a. Proofnet: Autoformalizing            theorem provers with informal proofs. arXiv preprint
  and formally proving undergraduate-level mathemat-         arXiv:2210.12283.
  ics. arXiv preprint arXiv:2302.12433.                    Albert Qiaochu Jiang, Wenda Li, Jesse Michael Han,
                                                             and Yuhuai Wu. 2021. Lisa: Language models of
Zhangir Azerbayev, Hailey Schoelkopf, Keiran Paster,         isabelle proofs. In 6th Conference on Artificial Intel-
  Marco Dos Santos, Stephen McAleer, Albert Q Jiang,         ligence and Theorem Proving, pages 378–392.
  Jia Deng, Stella Biderman, and Sean Welleck. 2023b.
  Llemma: An open language model for mathematics.          Albert Qiaochu Jiang, Wenda Li, Szymon Tworkowski,
  arXiv preprint arXiv:2310.10631.                           Konrad Czechowski, Tomasz Odrzygóźdź, Piotr
                                                             Miłoś, Yuhuai Wu, and Mateja Jamnik. 2022b. Thor:
Abhimanyu Bambhaniya, Ritik Raj, Geonhwa Jeong,              Wielding hammers to integrate language models and
  Souvik Kundu, Sudarshan Srinivasan, Midhilesh              automated theorem provers. Advances in Neural In-
  Elavazhagan, Madhu Kumar, and Tushar Krishna.              formation Processing Systems, 35:8360–8373.
  2024. Demystifying platform requirements for
  diverse llm inference use cases. arXiv preprint          Guillaume Lample, Timothee Lacroix, Marie-Anne
  arXiv:2406.01698.                                          Lachaux, Aurelien Rodriguez, Amaury Hayat,
                                                             Thibaut Lavril, Gabriel Ebner, and Xavier Martinet.
Ting Chen, Simon Kornblith, Kevin Swersky, Moham-            2022. Hypertree proof search for neural theorem
  mad Norouzi, and Geoffrey E Hinton. 2020. Big              proving. Advances in neural information processing
  self-supervised models are strong semi-supervised          systems, 35:26337–26349.
  learners. Advances in neural information processing      Norman Megill and David A Wheeler. 2019. Metamath:
  systems, 33:22243–22255.                                   a computer language for mathematical proofs. Lulu.
                                                             com.
Projet Coq. 1996. The coq proof assistant-reference
  manual. INRIA Rocquencourt and ENS Lyon, ver-            Yu Meng, Jiaxin Huang, Yu Zhang, and Jiawei Han.
  sion, 5.                                                   2022. Generating training data with language mod-
                                                             els: Towards zero-shot language understanding. Ad-
Leonardo De Moura, Soonho Kong, Jeremy Avigad,               vances in Neural Information Processing Systems,
  Floris Van Doorn, and Jakob von Raumer. 2015. The          35:462–477.
Leonardo de Moura and Sebastian Ullrich. 2021. The         Ruida Wang, Wangchunshu Zhou, and Mrinmaya
  lean 4 theorem prover and programming language. In         Sachan. 2023. Let’s synthesize step by step: Iter-
  Automated Deduction–CADE 28: 28th International            ative dataset synthesis with large language models
  Conference on Automated Deduction, Virtual Event,          by extrapolating errors from small models. arXiv
  July 12–15, 2021, Proceedings 28, pages 625–635.           preprint arXiv:2310.13671.
  Springer.
                                                           Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten
Allen Newell and Herbert Simon. 1956. The logic               Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou,
  theory machine–a complex information processing             et al. 2022. Chain-of-thought prompting elicits rea-
  system. IRE Transactions on information theory,             soning in large language models. Advances in neural
  2(3):61–79.                                                 information processing systems, 35:24824–24837.

Lawrence C Paulson. 1994. Isabelle: A generic theorem      Yuhuai Wu, Albert Qiaochu Jiang, Wenda Li, Markus
  prover. Springer.                                          Rabe, Charles Staats, Mateja Jamnik, and Christian
                                                             Szegedy. 2022. Autoformalization with large lan-
Stanislas Polu, Jesse Michael Han, Kunhao Zheng, Man-        guage models. Advances in Neural Information Pro-
   tas Baksys, Igor Babuschkin, and Ilya Sutskever.          cessing Systems, 35:32353–32368.
   2022. Formal mathematics statement curriculum
   learning. arXiv preprint arXiv:2202.01344.              Kaiyu Yang and Jia Deng. 2019. Learning to prove
                                                             theorems via interacting with proof assistants. In In-
Stanislas Polu and Ilya Sutskever. 2020. Generative          ternational Conference on Machine Learning, pages
   language modeling for automated theorem proving.          6984–6994. PMLR.
   arXiv preprint arXiv:2009.03393.
                                                           Kaiyu Yang, Aidan Swope, Alex Gu, Rahul Chala-
Machel Reid, Nikolay Savinov, Denis Teplyashin,              mala, Peiyang Song, Shixing Yu, Saad Godil, Ryan J
 Dmitry Lepikhin, Timothy Lillicrap, Jean-baptiste           Prenger, and Animashree Anandkumar. 2024. Le-
 Alayrac, Radu Soricut, Angeliki Lazaridou, Orhan Fi-        andojo: Theorem proving with retrieval-augmented
 rat, Julian Schrittwieser, et al. 2024. Gemini 1.5: Un-     language models. Advances in Neural Information
 locking multimodal understanding across millions of         Processing Systems, 36.
 tokens of context. arXiv preprint arXiv:2403.05530.
                                                           Huaiyuan Ying, Zijian Wu, Yihan Geng, Jiayu Wang,
Baptiste Roziere, Jonas Gehring, Fabian Gloeckle, Sten       Dahua Lin, and Kai Chen. 2024. Lean workbook:
  Sootla, Itai Gat, Xiaoqing Ellen Tan, Yossi Adi,           A large-scale lean problem set formalized from
  Jingyu Liu, Romain Sauvestre, Tal Remez, et al. 2023.      natural language math problems. arXiv preprint
  Code llama: Open foundation models for code. arXiv         arXiv:2406.03847.
  preprint arXiv:2308.12950.
                                                           Kunhao Zheng, Jesse Michael Han, and Stanislas Polu.
Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu,              2021. Minif2f: a cross-system benchmark for for-
  Junxiao Song, Mingchuan Zhang, YK Li, Yu Wu,               mal olympiad-level mathematics. arXiv preprint
  and Daya Guo. 2024. Deepseekmath: Pushing the              arXiv:2109.00110.
  limits of mathematical reasoning in open language
  models. arXiv preprint arXiv:2402.03300.

Demin Song, Honglin Guo, Yunhua Zhou, Shuhao Xing,
  Yudong Wang, Zifan Song, Wenwei Zhang, Qipeng
  Guo, Hang Yan, Xipeng Qiu, et al. 2024. Code needs
  comments: Enhancing code llms with comment aug-
  mentation. arXiv preprint arXiv:2402.13013.

Petru Soviany, Radu Tudor Ionescu, Paolo Rota, and
  Nicu Sebe. 2022. Curriculum learning: A survey. In-
  ternational Journal of Computer Vision, 130(6):1526–
  1565.

Terence Tao. 2023. A slightly longer lean 4 proof tour.
  https://terrytao.wordpress.com/2023/12/
  05/a-slightly-longer-lean-4-proof-tour/.
  Accessed: 2024-06-15.

Terence Tao, Yael Dillies, and Bhavik Mehta. 2023.
  Formalizing the proof of pfr in lean4 using blueprint:
  a short tour. Accessed: 2024-06-15.

Richard Taylor and Andrew Wiles. 1995. Ring-theoretic
  properties of certain hecke algebras. Annals of Math-
  ematics, 141(3):553–572.
A    Confusing Lean3 Data in LLM                                             1k       10k     full OBT ( 100k)
     Pre-train                                               MiniF2F-Test   29.01%   30.74%       31.15%

While studying how to directly generate Lean4                         Table 4: Various dataset size
formal proofs using LLMs, we found that most
LLMs have a serious problem with hallucination.
The most significant issue is that, even with clear     step reasoning in both natural language and formal
prompt instructions, the LLMs tend to write Lean3       language in relatively complex proofs, demonstrat-
proofs that are incompatible with Lean4.                ing the effectiveness of NL-FL bootstrapping.
   The results for GPT-4 are shown in Tab. 6 and 7.
                                                        C     Various dataset size training
From these tables, we can observe that even with
clear instructions to use Lean4 for writing proofs,     This section presents the results of training the
the LLM still uses Lean3 syntax for all imports         model on different scales of the OBT dataset.
and proofs. The imports are from Lean3 repos-           Specifically, we randomly sampled 1k and 10k
itories or sometimes do not exist, and the proof        subsets from the OBT dataset, and the results are
segments, indicated by "begin" and "end," are also      shown in Tab. 4.
from Lean3. This issue also occurs with Llama-3-          From the table, we observe that the performance
8B-Instruct and Gemini-1.5-Pro, but less frequently.    improvement does not align with typical human
We attribute this behavior to the massive amount of     behavior in text writing, resulting in the perfor-
Lean3 data used in the pre-training of these LLMs.      mance increase not following the expected scaling
This causes LLMs to fail in fully utilizing their       law. This phenomenon is also observed in dataset
knowledge in formal reasoning, as many generated        generation works such as Wang et al. (2023).
formal proofs are incorrect in format.
   Alternatively, TheoremLlama uses extensive           D     Different LLM’s behavior in
Lean4 data during instruction fine-tuning to sig-             Informalization
nificantly reduce this problem, as detailed in Sec-     This section details why we use Gemini-1.5 as the
tion 3.7 and Appendix B.                                LLM for informalization and NL-FL cootstrapping
                                                        rather than the commonly used OpenAI GPT fam-
B   Case Study
                                                        ily models through examples. We demonstrate an
This section provides additional case studies to        example of informalization in Table 13. From the
further evaluate the performance of TheoremL-           table, we can see that the GPT-4-generated proof
lama in proving Lean4 theorems with NL guidance.        is more like an explanation of the Lean4 code,
Here, we select most examples from MiniF2F-             while the Gemini-1.5-generated proof resembles
Valid to avoid revealing too much proof informa-        the wording commonly used in mathematics. This
tion about MiniF2F-Test and contaminating the           demonstrates that Gemini-1.5 has a better ability to
dataset. We present the examples in Tab. 8, 9, 10,      understand Lean4 code for informalization. This is
11, and 12.                                             also indirectly supported by Gemini’s superior per-
   From case 1 in Tab. 8, we can see that the LLMs      formance in writing Lean4 proofs for the MiniF2F
learn how to perform complex reductions stated in       dataset, as shown in Table 1.
Lean4 code based on the natural language. The
"calc" section demonstrates the LLM’s ability to        E     OBT dataset record
correctly reduce algebraic formulas based on con-       The data record in OBT contains the following
ditions that are not explicitly stated in the natural   components:
language proof.
   Case 2 in Tab. 9 demonstrates that under the             1. Name: the name of the theorem, following
TheoremLlama framework, the LLM learns how                     the name of dataset extracted in Yang et al.
to add sub-goals for proving in the correct Lean4              (2024)
form from natural language proof. This is not ob-           2. Statement: Lean4 statement of the theorem
served in any of the correct proofs in the untrained
model.                                                      3. Proof: Lean4 theorem statement together
   From cases 3, 4, and 5 in Tab. 10, 11, and 12, we           with the proof, directly extracted from Math-
can see the ability of our LLM to perform step-by-             lib4
    4. File_path: The git repository for the given                 Method               MiniF2F-Valid   MiniF2F-Test

       data record (for OBT dataset, it should be              DeepSeek-Math-7B            25.80%         24.60%
                                                         TheoremLlama + DeepSeek-Math      38.52%         35.66%
       Mathlib4)
                                                        Table 5: Applying TheoremLlama method to DeepSeek-
    5. Commit: The exact commit number of the
                                                        Math
       theorem
                                                        H     Analyze the impact of NL-FL
    6. Generated_informal_statement_and_proof:
                                                              Bootstrapping
       The generated theorem informal theorem
       statement and proof                              This section provides a example towards the NL-FL
                                                        Bootstrapping.
    7. Commented_proof:        The NL-FL boot-
                                                          Generated theorem proof without Bootstrapping:
       strapped Lean4 code.
                                                        theorem amc12b_2002_p2
the example of an OBT dtaset record is presented          (x : Z)
at Tab. 14                                                (h0 : x = 4) :
                                                          (3 * x - 2) * (4 * x + 1) - (3 * x - 2) * (4 *
                                                              x) + 1 = 11 := by
F     More bootstrapping method analysis                  subst x
                                                          ring
This section studies the differences between vari-
ous data bootstrapping methods. Our NL-FL Boot-             Generated theorem proof with Bootstrapping:
strapping method is inspired by in-code comments,       theorem algebra_sqineq_unitcircatbpamblt1
which can help the LLM transfer its ability from          (a b: R)
natural language to formal language. To demon-            (h0 : a^2 + b^2 = 1) :
                                                          a * b + (a - b) ≤ 1 := by
strate the effectiveness of this approach, we experi-     -- We have that (a - b - 1)^2 ≥ 0.
mented with another bootstrapping method, namely          have h1 : 0 ≤ (a - b - 1) ^ 2 := sq_nonneg _
                                                          -- By expanding, we have:
Head Bootstrapping. This method involves adding           -- 0 ≤ a^2 -ab-a-ab+b^2 +b-a+b+1.
natural language reasoning as comments before the         linarith [h0 , sub_add_cancel a b]
formal language in the training data, allowing the
model to learn this behavior and potentially encour-       We can clearly find out that the generated re-
aging deeper reasoning. We tested this approach         sult without bootstrapping tends not to use nat-
using blocked training and a curriculum-learning        ural language to guide the generation of proof,
strategy. The Head Bootstrapping method achieved        which makes it fail to solve the problem alge-
a result of 25.46%, while our NL-FL Bootstrap-          bra_sqineq_unitcircatbpamblt1. Thus, both abla-
ping method reached 31.15%. This comparison             tion studies in Section 2 and case studies can pro-
demonstrates the effectiveness of our bootstrap-        vide the effectiveness of the bootstrapping method.
ping method over other dataset bootstrapping tech-
niques.                                                 I    OBT dataset quality analysis
                                                        This section analyzes the quality of the OBT
G     Applying TheoremLlama framework
                                                        dataset. Due to the large volume of data, it is
      to other models
                                                        infeasible to analyze every record to verify if it
To evaluate the generality of the TheoremLlama          has been informalized correctly. Therefore, we
framework, we apply the dataset generated, to-          randomly sampled 40 records and evaluated them
gether with curriculum learning technique and           manually. Among these, 29 are correct, 4 are par-
block training method to fine-tune other models.        tially correct, and 7 contain critical mistakes that
In particular, we choose DeepSeek-Math-7B (Shao         render the proof mathematically incorrect. The
et al., 2024) as the base model for training, the       major mistake the LLM makes is confusing some
result demonstrated in Tab.5.                           complex mathematical concepts, such as mixing
   From the table, we can see that after applying       the general Lebesgue measure with the probability
our method to the math expert, the Lean4 perfor-        measure. There are also misunderstandings in vital
mance of the model has been greatly increased.          parts of formal reasoning, for instance, mistakenly
This proves TheoremLlama can be effective in            using normal sequence convergence in natural lan-
a wide range of models rather than could be only        guage reasoning while the formal language uses the
applied to Llama.                                       Cauchy sequence to prove sequence convergence.
J   Term List
Since formal theorem proving is a relatively new
field, there is many fundamental terms that are hard
to remember. Thus, we provide a table explaining
some important terms in this paper that are not
fully elaborated in Tab.15 for researchers who are
not that familiar with that field to read our paper
smoother.

K    License
Our dataset will be distributed under the CC BY 2.0
license, code will be distributed under the MIT li-
cense. The dataset extracted from LeanDojo (Yang
et al., 2024) is under CC BY 2.0. The original
Mathlib4 and Lean is under Apache 2.0 license.
Prompt      You are a Lean4 expert who can write good Lean4 code based on natural
            language mathematical theorem and proof
            <Examples>
            ### Natural language version of theorem and proof:          <NL of
            amc12a_2019_p21>
            ### Lean4 version of theorem statement:        <Lean4 statement of
            amc12a_2019_p21>

            theorem amc12a_2019_p21 (z : C) (h0 : z = (1 + Complex.I) / Real.sqrt 2) :
              ((Σ k : Z in Finset.Icc 1 12, z ^ k ^ 2) * (Σ k : Z in Finset.Icc 1 12,
                1 / z ^ k ^ 2)) = 36 :=


            ### Lean4 version of theorem and proof:
Generated To translate the given natural language explanation of the theorem into a Lean4
Result    proof, we must first define the necessary elements accurately in Lean4 syntax.
          This includes the expression for z, the computation of powers and their modulo
          reductions, and ultimately the statement of the sums and their product. Lean4
          provides a robust framework for handling complex numbers and integer arith-
          metic, which we will use here.

            import data.complex.basic
            import data.finset.basic
            import data.nat.basic

            open complex

            -- Define the main theorem
            theorem amc12a_2019_p21 :
              let z := (1 + I) / sqrt 2 in
              let s := Σ k in finset.range 12, (z ^ (k+1) ^ 2) in
              let t := Σ k in finset.range 12, (1 / (z ^ (k+1) ^ 2)) in
              s * t = 36 :=
            begin
              . . . -- Details omitted
            end



                      Table 6: GPT-4 writing Lean4 proof Example 1
Prompt     You are a Lean4 expert who can write good Lean4 code based on natural
           language mathematical theorem and proof
           <Examples>
           Natural language version of theorem and proof:
           mathd_numbertheory_543: Find the number of distinct positive divisors of
           (30)4 excluding 1 and (30)4 . Show that it is 123.

                                (304 ) = (21 · 31 · 51 )4 = 24 · 34 · 54
            Since t(304 ) = (4 + 1)3 = 125, taking out 1 and (304 ) leaves 125 − 2 = 123
            positive divisors.
            ### Lean4 version of theorem statement:

                theorem mathd_numbertheory_543 : (Σ k in Nat.divisors (30 ^ 4), 1) - 2
                = 123 :=


            ### Lean4 version of theorem and proof:
Generated To formalize and prove the given theorem in Lean4, we need to use Lean’s
Result    mathematical libraries, particularly those related to natural numbers and their
          properties, such as divisor functions. The theorem involves computing the total
          number of divisors of 304 , excluding 1 and 304 itself.

            import data.nat.prime
            import algebra.big_operators

            open_locale big_operators

            -- Define the theorem stating that the number of divisors of 30^4,
                 excluding 1 and 30^4, is 123.
            theorem mathd_numbertheory_543 :
              (Σ k in nat.divisors (30^4), 1) - 2 = 123 :=
            begin
                . . . -- Details omitted
            end



                       Table 7: GPT-4 writing Lean4 proof Example 2
                              1                                       3
NL Statement      If f (x) =      , what is f (f (1))? Show that it is .
                            x+2                                       7
                                                                             
                                         1        1                          1      1
NL Proof          We see that f (1) =          = . Therefore, f (f (1)) = f     = 1    =
                                      1+2         3                          3    3 +2
                  1    3
                  7 = 7.
                  3
Generated Proof
                  theorem mathd_algebra_270
                    (f : R → R)
                    (h0 : ∀ x, x ̸= -2 -> f x = 1 / (x + 2)) :
                    f (f 1) = 3/7 := by
                    -- We see that f 1 = 1 / (1 + 2) = 1 / 3
                    have h1 : f 1 = 1 / 3 := by norm_num [h0 ]
                    -- Thus f (f 1) = f (1 / 3) = 1 / (1 / 3 + 2) = 1 / (7 / 3) = 3 / 7
                    calc
                      f (f 1) = f (1 / 3) := by rw [h1 ]
                      _ = 1 / (1 / 3 + 2) := by norm_num [h0 ]
                      _ = 1 / (7 / 3) := by norm_num
                      _ = 3 / 7 := by norm_num



                               Table 8: Additional Case Study 1




NL Statement      If |x − 2| = p, where x < 2, then x − p =
                  (A) − 2      (B)2     (C)2 − 2p      (D)2p − 2     (E)|2p − 2|
                  Show that it is (C)2 − 2p.
NL Proof          When x < 2, x − 2 is negative so |x − 2| = 2 − x = p and x = 2 − p. Thus
                  x − p = (2 − p) − p = 2 − 2p. Leading to answer (C)2 − 2p
Generated Proof
                  theorem amc12_2000_p5 (x p : R) (h0 : x < 2) (h1 : abs (x - 2) = p) : x -
                      p = 2 - 2 * p := by
                    -- If x < 2, then x - 2 is negative, so |x - 2| = 2 - x = p.
                    -- Thus, x = 2 - p.
                    suffices abs (x - 2) = -(x - 2) by
                      rw [h1 ] at this
                      linarith
                    -- Therefore, x - p = (2 - p) - p = 2 - 2p.
                    apply abs_of_neg
                    linarith



                               Table 9: Additional Case Study 2
NL Statement      Suppose that g(x) = f −1 (x). If g(−15) = 0, g(0) = 3, g(3) = 9 and
                  g(9) = 20, what is f (f (9))? Show that it is 0.
NL Proof          Since f and g are inverses and g(3) = 9, we have f (9) = 3, so f (f (9)) = f (3).
                  Similarly, g(0) = 3, so f (3) = 0.
Generated Proof
                  theorem mathd_algebra_451
                      (σ : Equiv R R)
                      (h0 : σ.2 (-15) = 0)
                      (h1 : σ.2 0 = 3)
                      (h2 : σ.2 3 = 9)
                      (h3 : σ.2 9 = 20) : σ.1 (σ.1 9) = 0 := by
                    -- Since f and g are inverses and g(3) = 9, we have f(9) = 3, so f(f(9))
                      = f(3).
                    simp only [Equiv.invFun_as_coe, eq_comm] at h0 h1 h2 h3
                    -- Similarly, g(0) = 3, so f(3) = 0.
                    simp only [Equiv.toFun_as_coe]
                    rw [← Equiv.apply_eq_iff_eq_symm_apply σ] at h2
                    rw [← Equiv.apply_eq_iff_eq_symm_apply σ] at h1
                    have h4 := (Equiv.apply_eq_iff_eq σ).mpr h2
                    rw [h1 ] at h4
                    exact h4



                              Table 10: Additional Case Study 3
                                                √
NL Statement      For what real value of k is 13−4 131 a root of 2x2 − 13x + k? Show that it is 19
                                                                                                4 .
                                               √
NL Proof          We could substitute (13 − 131)/4 for x in the equation, but the quadratic
                  formula suggests a quicker approach. Substituting 2, −13, and k into the
                  quadratic formula gives
                                          p                              √
                              −(−13) ± (−13)2 − 4(2)(k)              13 ± 169 − 8k
                                                                  =                 .
                                             2(2)                           4
                                √                          √                           √
                  Setting (13+ 169 − 8k)/4 and (13− 169 − 8k)/4 equal to (13− 131)/4,
                  we find no solution in the first case and 169 − 8k = 131 in the second case.
                  Solving yields k = (169 − 131)/8 = 38/8 = 19     4 .
Generated Proof
                  theorem mathd_algebra_116 (k x : R) (h0 : x = (13 - Real.sqrt 131) / 4)
                      (h1 : 2 * x ^ 2 - 13 * x + k = 0) : k = 19 / 4 := by
                    -- Proof: We are given that (13 - $\sqrt{131}$) / 4 is a root of the
                      quadratic 2²x - 13x + k = 0
                    -- and want to show that k = 19/4.
                    rw [h0 ] at h1 -- Substitute (13 - $\sqrt{131}$) / 4 for x in the
                      quadratic equation.
                    -- We now have a equation that is reducible to k = 19/4.
                    rw [eq_comm.mp (add_eq_zero_iff_neg_eq.mp h1 )] -- Rearrange the equation
                      obtained from the previous step.
                    norm_num -- Normalize the numeric expressions.
                    rw [pow_two] -- Expand the square term.
                    rw [mul_sub] -- Expand by distributivity.
                    rw [sub_mul, sub_mul] -- Expand by distributivity.
                    rw [Real.mul_self_sqrt _] -- Simplify $\sqrt{a}$ * $\sqrt{a}$ to a.
                    ring -- Apply the ring axioms to simplify the expression.
                    linarith -- Verify that the left and right sides of the equation are
                      equal, thus proving k = 19/4



                              Table 11: Additional Case Study 4
NL Statement      If 3a + b + c = −3, a + 3b + c = 9, a + b + 3c = 19, then find abc. Show that
                  it is -56.
NL Proof          Summing all three equations yields that 5a + 5b + 5c = −3 + 9 + 19 = 25.
                  Thus, a + b + c = 5. Subtracting this from each of the given equations, we
                  obtain that 2a = −8, 2b = 4, 2c = 14. Thus, a = −4, b = 2, c = 7, and their
                  product is abc = −4 × 2 × 7 = −56.
Generated Proof
                  theorem mathd_algebra_338
                    (a b c : R)
                    (h0 : 3 * a + b + c = -3)
                    (h1 : a + 3 * b + c = 9)
                    (h2 : a + b + 3 * c = 19) :
                    a * b * c = -56 := by
                    -- This theorem shows that if 3a + b + c = -3, a+3b+c = 9, a+b+3c = 19,
                    -- then a * b * c = -56.
                    have h3 : a + b + c = 5 := by linarith
                    -- From the first equation, 3a + b + c = -3, we have a + b + c = 5.
                    have h4 : 2 * a = -8 := by linarith
                    -- From the first equation, 3a + b + c = -3, we also have 2 * a = -8.
                    have h5 : 2 * b = 4 := by linarith
                    -- From the second equation, a+3b+c = 9, we have 2 * b = 4.
                    have h6 : 2 * c = 14 := by linarith
                    -- From the third equation, a+b+3c = 19, we have 2 * c = 14.
                    have h7 : a = -4 := by linarith
                    -- From h4 and h3 , we have a = -4.
                    have h8 : b = 2 := by linarith
                    -- From h5 and h3 , we have b = 2.
                    have h9 : c = 7 := by linarith
                    -- From h6 and h3 , we have c = 7.
                    simp_all only [mul_neg, neg_mul, mul_assoc, neg_add, add_assoc,
                       add_left_comm, sub_eq_add_neg,
                      sub_neg_eq_add, eq_self_iff_true, true_and]
                    ring_nf
                    -- Finally, we can conclude that a * b * c = -4 * 2 * 7 = -56.
                    -- QED.



                             Table 12: Additional Case Study 5
Prompt      You are a mathematician who can write natural language proof based on Lean4
            proof
            <Examples>
            Lean4 version of theorem statement and proof:

            theorem integral_eq_sub_of_hasDerivAt (hderiv : ∀ x ∈ uIcc a b, HasDerivAt
                f (f' x) x)
                (hint : IntervalIntegrable f' volume a b) :   y in a..b, f' y = f b -
                                                            R
                f a :=
              integral_eq_sub_of_hasDeriv_right (HasDerivAt.continuousOn hderiv)
                (fun _x hx => (hderiv _ (mem_Icc_of_Ioo hx)).hasDerivWithinAt) hint


            Natural language version of theorem statement and proof:
Gemini      Statement: Let f : R → R be    R b a ′function that is differentiable on the interval
Result      [a, b]. We want to show that a f (x) dx = f (b) − f (a).
            Proof: Since f is differentiable on [a, b], it is continuous on [a, b]. By the
            Fundamental Theorem
                 ′
                                R x of′ Calculus, Part 1, we know that if F is an antiderivative
            of f on [a, b], then a f (t) dt = F (x) − F (a) for any x ∈ [a, b]. In particular,
                                     Rb
            if we take x = b, we get a f ′ (t) dt = F (b)−F (a). Since F is an antiderivative
            of f ′ , we can choose F to be f itself. Therefore, we have F (x) = f (x) and
                                    Rb
            the equation becomes a f ′ (t) dt = f (b) − f (a). Thus, we have shown that
            Rb ′
              a f (x) dx = f (b) − f (a), which completes the proof.
GPT Re- Statement: Given a function f defined on an interval [a, b], and f ′ , its derivative,
sult    prove that the integral of f ′ from a to b equals f (b) − f (a).
        Proof: Assume that for every point x in the closed interval [a, b], the
        function f has a derivative f ′ (x) at x, denoted by HasDerivAt f (f ′ (x))x.
        Also, assume that f ′ is integrable over the interval from a to b, denoted by
        IntervalIntegrable f ′ volume a b.
        To prove the theorem, we utilize the Fundamental Theorem of Calculus, which
        states that if a function g is continuous on [a, b] and has an antiderivative F
                                    Rb
        over that interval, then a g(x) dx = F (b) − F (a). In this case, f ′ acts as
        g, and its antiderivative is f by the definition of a derivative. The condition
        HasDerivAt f (f ′ (x))x implies that f ′ is continuous on [a, b] due to the contin-
        uous nature of derivatives under normal circumstances.
        1. Continuity of f ′ : The hypothesis ∀x ∈ [a, b], HasDerivAt f (f ′ (x))x as-
        sures that f ′ is continuous on [a, b]. This is because the derivative at a point
        implies local continuity at that point.
        2. Integral of f ′ : Since f ′ is continuous over [a, b] and integrable (as given
                                  ′
                            R b f′ volume a b), we apply the Fundamental Theorem of
        by IntervalIntegrable
        Calculus. Hence, a f (y) dy = f (b) − f (a).
        This concludes the proof. The integral of the derivative f ′ from a to b results in
        the net change in the function f over the interval, which is f (b) − f (a).

                Table 13: Comparison of Gemini-1.5 and GPT-4 generated NL proofs
Name         intervalIntegral.integral_eq_sub_of_hasDerivAt
Statement
             theorem integral_eq_sub_of_hasDerivAt (hderiv : ∀ x ∈ uIcc a b, HasDerivAt
                 f (f' x) x)
                 (hint : IntervalIntegrable f' volume a b) :   y in a..b, f' y = f b -
                                                             R
                 f a :=



Proof
             theorem integral_eq_sub_of_hasDerivAt (hderiv : ∀ x ∈ uIcc a b, HasDerivAt
                 f (f' x) x)
                 (hint : IntervalIntegrable f' volume a b) :   y in a..b, f' y = f b -
                                                             R
                 f a :=
                 integral_eq_sub_of_hasDeriv_right (HasDerivAt.continuousOn hderiv)
                 (fun _x hx => (hderiv _ (mem_Icc_of_Ioo hx)).hasDerivWithinAt) hint



File_path    https://github.com/leanprover-community/mathlib4
Commit       3ce43c18f614b76e161f911b75a3e1ef641620ff
Generated_ Let f : R → R be a function that is differentiable on the interval [a, b]. Use the
infor-     Fundamental Theorem of Calculus to show that
mal_                                  Z b
state-                                    f ′ (x)dx = f (b) − f (a).
ment_                                  a
and_
proof
           Proof: Since f is differentiable on [a, b], it is continuous
                                                                  R x ′ on [a, b]. ′By the Sec-
                                                                d
           ond Fundamental Theorem of Calculus, we have dx a f (t)dt = f (x) ∀x ∈
           [a, b]. Integrating both sides of this equation with respect to x from a to b,
                    Rb d Rx ′               Rb ′
           we get a dx     aR f (t)dtdx = a f (x)dx.     But the left-hand side of this equa-
                              b ′                    Rb ′            Rb
           tion is equal to a f (x)dx, so we have a f (x)dx = a f ′ (x)dx. Subtracting
           Rb ′
             a f (x)dx from both sides of this equation, we get 0 = f (b)−f (a). Therefore,
           f (b) − f (a) = 0, which proves the desired result.
Commented_proof:
             theorem integral_eq_sub_of_hasDerivAt (hderiv : ∀ x ∈ uIcc a b, HasDerivAt
                 f (f' x) x)
                 (hint : IntervalIntegrable f' volume a b) :   y in a..b, f' y = f b -
                                                             R
                 f a :=
                 -- This theorem states that the integral of the derivative of a
                 function over an interval
                 -- is equal to the difference of the function values at the endpoints
                 of the interval.
                 -- This is a fundamental theorem of calculus.
                 integral_eq_sub_of_hasDeriv_right (HasDerivAt.continuousOn hderiv)
                 -- This part of the proof uses the second fundamental theorem of
                 calculus, which states that
                 -- the derivative of the integral of a function is equal to the
                 function itself.
                 (fun _x hx => (hderiv _ (mem_Icc_of_Ioo hx)).hasDerivWithinAt) hint
                 -- This part of the proof uses the fact that the derivative of a
                 function is continuous on
                 -- the interval where it is differentiable.



                           Table 14: Example of one record of OBT dataset
Term                 Explaination
Lean4 & Lean    Lean is a modern, functional programming language that is
                designed for formalizing mathematics proof and performing
                auto verification. It allows users to write proofs as code, and its
                auto-verification ensures current written proofs are correct by
                verifying each logical step. Lean4 is the latest version of Lean
Mathlib & Math- Mathlib is a large open-source library built on Lean. It con-
lib4            tains comprehensive collection of theorems, definitions and
                proofs across most major areas of mathematics, including al-
                gebra, calculus and topology. Mathlib is originally build on
                Lean3 (De Moura et al., 2015), and Mathlib4 is the Lean4
                version of Mathlib.
MiniF2F         It is a benchmark designed for evaluating automated theorem
                proving systems in formal mathematics. It contains a collection
                of mathematical problems sourced from various high-school
                to university-level mathematical problems. It was proposed in
                Zheng et al. (2021). The NL statement and proof of MiniF2F
                is provided by Jiang et al. (2022a). The MiniF2F-Valid is
                provided in Yang et al. (2024) and we provide the MiniF2F-
                Test.
ByT5-Tacgen     This is a tree-search Lean model provided by Yang et al. (2024),
                which is used to retrieve the most relevant tactic based on the
                current Lean status and unfinished goals. It is based on fine-
                tuning By-T5 using Mahtlib data

                                Table 15: Term list
