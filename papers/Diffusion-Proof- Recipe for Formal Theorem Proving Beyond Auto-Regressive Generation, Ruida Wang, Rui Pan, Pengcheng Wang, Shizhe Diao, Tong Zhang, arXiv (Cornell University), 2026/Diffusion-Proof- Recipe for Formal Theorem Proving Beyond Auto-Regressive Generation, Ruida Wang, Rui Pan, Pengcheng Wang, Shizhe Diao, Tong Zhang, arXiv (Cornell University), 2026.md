                                              Diffusion-Proof: Recipe for Formal Theorem Proving Beyond
                                                              Auto-Regressive Generation

                                                Ruida Wang1 , Rui Pan1 , Pengcheng Wang1 , Shizhe Diao2 , Tong Zhang1
                                                                      1
                                                                          University of Illinois Urbana-Champaign, 2 NVIDIA
                                                        {ruidaw, ruip4, pw29}@illinois.edu, shizhe.diao@gmail.com, tozhang@illinois.edu




                                                           Abstract                                 1   Introduction

                                                                                                    Building machine-learning systems capable of per-
arXiv:2606.19315v1 [cs.LG] 17 Jun 2026




                                         Enhancing the formal math reasoning capa-                  forming human-level reasoning based on rigorous
                                         bilities of Large Language Models (LLMs)                   logical rules has always been considered a funda-
                                         has become a key focus in both mathemati-                  mental goal for artificial intelligence (Wang et al.,
                                         cal and computer science communities in re-                2024). This capability is often evaluated through
                                         cent years. While significant progress has been            the derivation of complex formal mathematical
                                         made in using state-of-the-art Auto-Regressive
                                                                                                    proofs, where maintaining long-range coherence
                                         (AR) LLMs for formal theorem proving, these
                                         models suffer from inherent limitations. Their             is essential (Yang et al., 2024a). However, the
                                         next-token prediction generation methods may               inherent ambiguity in natural language makes it
                                         yield suboptimal performance due to the chal-              challenging to formally verify the intermediate rea-
                                         lenges of long-range coherence and the com-                soning steps.
                                         pounding of errors over long sequences. Recent                To provide a trustworthy foundation for mathe-
                                         advancements in diffusion LLMs (dLLMs),
                                                                                                    matical reasoning, multiple works have developed
                                         which generate text through iterative denoising
                                         of a multi-token block, offer a promising alter-
                                                                                                    verifiable languages based on different theoreti-
                                         native. However, the application of dLLMs to               cal foundations. Some apply the dependent type
                                         formal mathematics, where maintaining long-                language, such as Lean (De Moura et al., 2015;
                                         range coherence is critical, remains largely un-           Moura and Ullrich, 2021) and Coq (Coq, 1996),
                                         derstudied. To address the challenges above,               which enforce type safety to ensure logical con-
                                         we propose Diffusion-Proof, to the best of                 sistency. Others employ higher-order logic, such
                                         our knowledge, the first framework to train                as Isabelle (Paulson, 1994) and HOL (Harrison,
                                         and apply dLLMs for formal theorem proving.
                                                                                                    2009). Proving both types of systems allows ex-
                                         Our frameworks contain training and inference
                                         methods for two models. The first one is dLLM-             plicit verification of every internal step, regardless
                                         Prover-7B, which performs whole-proof writ-                of its complexity. The formal verification mini-
                                         ing with long-range coherent tactic usage. The             mizes errors and prevents the hallucinations and
                                         second one is dLLM-Corrector-7B, which is                  logical inconsistencies often observed in natural
                                         a novel large block diffusion-based correction             language-based reasoning.
                                         model. It leverages the in-filling capabilities               With the rapid development of Large Language
                                         of dLLMs to perform local proof correction
                                                                                                    Models (LLMs), their significant potential in for-
                                         using bi-directional information. Extensive ex-
                                         periments demonstrate that Diffusion-Proof                 mal reasoning using Lean4 (Moura and Ullrich,
                                         relatively significantly outperforms the AR                2021) has become a key area of research. Recent ef-
                                         LLM baseline trained under the same dataset.               forts focus on generating large-scale datasets (Ying
                                         Diffusion-Proof achieves an absolute improve-              et al., 2024; Wu et al., 2024; Xin et al., 2024a;
                                         ment of 1.61% on ProofNet-Test and 6.14% on                Wang et al., 2024) and training models using meth-
                                         MiniF2F-Test benchmarks compare to the base-               ods ranging from standard Supervised Fine-Tuning
                                         line. Notably, Diffusion-Proof successfully re-
                                                                                                    (SFT) (Wang et al., 2024; Lin et al., 2025a) to ad-
                                         solves one IMO problem that more advanced
                                         thinking model DeepSeek-Prover-V2-7B (Ren                  vanced Reinforcement Learning (RL) (Ren et al.,
                                         et al., 2025) could not solve, showcasing the              2025; Wang et al., 2025a; Lin et al., 2025b). Lat-
                                         unique advantage of dLLMs in formal theorem                est research proposes multi-agent methods, from
                                         proving.                                                   recursive decomposition of subgoals (Varambally
                                                                                                                                              Block Diffusion Training Sample

                                                                                                                                    theorem lean_workbook_plus_79832 (x : ℝ)
                                                                                                                                    (h₀ : 5 + 3.5 * x = 2.5 * x - 25) :
                                 Cleaning                                                            Base                           x = -30 := by
                                                                                                    dLLM                            /-<NL-analysis>-/
                                 Selection
                                                                                                                                    -- Rewrite the equation to have the terms involving x
          5.5M Lean                             300k NL-FL          Block Diffusion                                                 on one side and constants on the other side.
                                                                       Training                                                     rw [eq_comm] at h₀…
            dataset                             mixture data                                                                                                                Block diffusion training

                                  Selection                                                         dLLM-
                                                                                                                                              Diffusion Correction Training Sample
                                                                                                    Prover
                                                                                                                                    theorem lean_workbook_21545 (a b c : ℝ) (ha : 0 ≤ a)
           Sub-goal              Correction      Correction            Diffusion                                                    (hb : 0 ≤ b) (hc : 0 ≤ c) (hab : a + b + c = 3) : a ^ 2 / ( a +
                                block filling                      Correction Training                                              1) + b ^ 2 / ( b + 1) + c ^ 2 / ( c + 1) ≥ a * b * c / ( a + b
         decomp data                            training data                                                                       + c) * Real.sqrt ( a * b + b * c + c * a):= by
                                                                                                                                       …
                                                                                                                                       have h₂ : b ^ 2 / (b + 1) ≥ b ^ 2 / 4 := by
                                                                                                    dLLM-                                 gcongr; linarith <|fim_middle|><|fim_middle|>…
                                                                                                   Corrector                           have h₃ : c ^ 2 / (c + 1) ≥ c ^ 2 / 4 := by …
                                                                                                                                       have h₄ : …                        Large diffusion block
                                                                                                                                                                      covering correction window


                                                                       (a) Data Collection & Model Training

                                                      Initial Lean Proof                                 Proof Done                                                  Fixed Lean Proof
  Lean statement                                     theorem mathd_algebra_215                                                                                       theorem mathd_algebra_215
                                                     (S : Finset ℝ)                                            ✅                                                     (S : Finset ℝ)
 theorem mathd_algebra_215
                                                     (h₀ : ∀ (x : ℝ), x ∈ S ↔(x + 3)^2 = 121) :                                                                      (h₀ : ∀ (x : ℝ), x ∈ S ↔(x + 3)^2 = 121) :
 (S : Finset ℝ)
 (h₀ : ∀ (x : ℝ), x ∈ S ↔(x +
                                      dLLM-          ∑ k in S, k = -6 := by                                            ❌ with have        dLLM-                      ∑ k in S, k = -6 := by
 3)^2 = 121) :                        Prover            have h₁ : <stat_1> := <proof_1>                               statement error    Corrector                      have h₁ : <stat_1> := <proof_1>
                                                        have h₂ : <stat_2> := <proof_2>                                                                                 have h₂ : <stat_2> := <fixed_proof>
 ∑ k in S, k = -6 := by
                                                        have h₃ : <stat_3> := <proof_3>                                                                                 have h₃ : <stat_3> := <proof_3>
                                                        exact h₃                                                                                                        exact h₃               Large diffusion
                                                                            Block diffusion gen.
                                                                                                                                                                                                 block correction

                                                                           (b) Proof Writing & Correction

Figure 1: Diffusion-Proof framework: (a) Data Collection and Model Training: We first collect a 5.5M Lean SFT
dataset from previous works, then perform cleaning and selection to obtain 300k natural language (NL)-formal
language (FL) mixture data to fine-tune Fast-dLLM-V2-7B into dLLM-Prover-7B. Subsequently, we select data with
subgoal decomposition and perform block filling to formulate data for corrector training. The dLLM-Corrector-7B is
fine-tuned by the dataset using Large-block correction training. (b) Proof Writing & Correction: The prover model
firstly generates the complete proof for the Lean4 theorems using block-diffusion generation. If the verification fails
but the skeleton is correct, the corrector model applies large diffusion block correction to adjust the subgoal proofs
based on bi-directional information.
et al., 2025), to agentic RL methods (Wang et al.,                                                       we propose Diffusion-Proof, to the best of our
2025c; Chen et al., 2025) for formal theorem prov-                                                       knowledge, the first framework for training and
ing. However, most, if not all, previous works on                                                        applying dLLMs for formal theorem proving. The
exploring LLMs’ usage in formal theorem prov-                                                            overview of our framework can be found in Fig-
ing are based on traditional Auto-Regressive (AR)                                                        ure 1. Diffusion-Proof contains the training and in-
LLMs. The AR models perform next-token predic-                                                           ference methods of two 7B-parameter models that
tion in a strict left-to-right manner. It has inherent                                                   work synergically together, namely dLLM-Prover-
problems, including potential exponential error ac-                                                      7B and dLLM-Corrector-7B. In the training stage of
cumulation (Dziri et al., 2023) and a lack of long-                                                      Diffusion-Proof, we collect 5.5 million records of
range coherence (Ye et al., 2025). Furthermore,                                                          theorem proving data from previous works, clean
the AR models are naturally unable to perform in-                                                        and select 300k records of SFT data. It is applied
filling proof correction. These make AR models                                                           to fine-tune Fast-dLLM-V2-7B into dLLM-Prover-
have natural flaws for formal reasoning.                                                                 7B to enhance its whole-proof writing capability.
   On the other hand, diffusion LLMs (dLLMs)                                                             Subsequently, we introduce a novel Large Block
present a promising alternative in language gen-                                                         Correction training method, enabling the model to
eration by reformulating the task as an iterative                                                        perform local in-filling correction of formal proof
denoising process of the multi-token block. Re-                                                          with bidirectional information awareness. During
cent studies (Nie et al., 2025; Ye et al., 2025; Wu                                                      inference, the dLLM-Prover-7B firstly generates
et al., 2025b; Bie et al., 2025) have demonstrated                                                       proofs based on the theorem statement. If the ini-
their potential in coding tasks, supported by effi-                                                      tial proof is wrong but the proof skeleton is correct,
cient training and inference frameworks (Wu et al.,                                                      we apply dLLM-Corrector-7B using large diffusion
2025a). While dLLMs naturally benefit from long-                                                         block generation to refine the proof locally.
range coherence and bi-directional awareness in                                                            We summarize our contribution as follows: (1)
generation, their application to formal reasoning                                                        To the best of our knowledge, we present Diffusion-
remains largely understudied.                                                                            Proof, the first framework for fine-tuning and ap-
    To address the limitations of existing methods,                                                      plying the dLLMs for formal theorem proving. (2)
We introduce the novel large-block correction train-     of size B, with bi-directional attention restricted
ing and inference method that leverages the bi-          to individual blocks while preserving causal rela-
directional information to perform in-filling cor-       tionships between blocks. During inference, the
rection. (3) Through extensive experiments, we           block dLLMs iteratively decode one block at a time
demonstrate that Diffusion-Proof relatively sig-         until a stopping condition is reached. This process
nificantly outperforms AR LLMs trained on the            balances the diffusion generation and the flexible
same dataset, achieving a 1.61% improvement              nature of AR models.
on ProofNet-Test and a 6.14% improvement on
MiniF2F-Test under pass@32. Notably, Diffusion-          2.2   Data Collection & Pre-process
Proof successfully solves one IMO problem that
the more advanced DeepSeek-Prover-V2-7B (Ren                This section outlines the data collection and
et al., 2025) could not solve.                           preprocessing steps for fine-tuning dLLM-Prover-
   Our study highlights the unique advantages of         7B and dLLM-Corrector-7B models in Diffusion-
dLLMs in theorem proving, and (as far as we              Proof. While previous works (Wu et al., 2024;
know), as the first work in such field, we plan to       Lin et al., 2025a; Dong and Ma, 2025; Wang
release all training code, models, and datasets pre-     et al., 2025c,a) have contributed millions of the-
sented in this work.                                     orem proof records. The data lacks proper structur-
                                                         ing. Specifically, these datasets are often in their
2     Methodology                                        raw input-output form and lack a clear separation
                                                         between FL statements, NL statements, and FL
In this section, we introduce the details of the         proofs.
Diffusion-Proof framework. It is designed to lever-         Thus, to uniform the dataset, we extract and
age the long-range coherence and in-filling cor-         standardize the data using rule-based methods to
rection capabilities of diffusion LLMs (dLLMs)           separate NL statements, FL statements, and FL
for formal theorem proving. We first present the         proofs. Additionally, proof data from STP (Dong
preliminaries of dLLMs in Section 2.1. Subse-            and Ma, 2025) lacks NL components and is used
quently, Section 2.2 details the data preparation        as syntax understanding data for Lean. In total,
and Section 2.3 presents model training. Finally,        we obtained 5,595,798 records of code-completion
we present the proof writing and correction method       proofs and sampled 300k records to create the SFT
that applies the trained model in Section 2.4.           dataset for prover. We maintain an approximate
2.1    Preliminaries                                     ratio of 1:2 between pure Lean proofs and those
                                                         with NL annotations and comments. Following the
Consider a token sequence x = {x1 , x2 , · · · , xL }    DeepSeek-Prover (Xin et al., 2024a) standard, we
with length L, traditional Auto-regressive (AR)          format the data in a code-completion style without
LLMs generate text sequentially following a stright      adopting a chat template. Examples of the training
left-to-right manner by modeling the conditional         data are provided in Section E.1.
distribution Pθ (xi |x[0 : i − 1]), where θ is the AR
                                                            We then prepare the data for the training correc-
model’s parameters. These models are trained to
                                                         tor by sampling from the 300k data that has subgoal
minimize cross-entropy loss of predicted tokens
                                                         decomposition in its proof. For a Lean proof, sub-
based only on previous tokens.
                                                         goals are defined as internal statements and their
   Diffusion LLMs, on the other hand, approach
                                                         proofs in the theorem proof are marked by the have
text generation differently by introducing a time
                                                         keyword, as illustrated in Figure 2. We organize
step t ∈ [0, 1] and adding noise to create x(t) ,
                                                         the top-level subgoal proof into token blocks of
where tokens are masked independently with prob-
                                                         size 256 by filling the proof with a placeholder
ability t. The model Pω (x(0) |x(t) ) iteratively pre-
                                                         <|fim_middle|> token. The data trains the model
dicts the original tokens from the noisy input.
                                                         to fill placeholder token when a block of proof is
The training objective for dLLMs is defined as:
                                   (t)                   finished. Additionally, we only consider one to fill
L(θ) = −Et,x(0) ,x(t) [ L
                        P
                            i=1 I[xi   = [MASK]] ·       in the block at a time for a proof containing multi-
          (0)
log Pω (xi |x(t) )                                       ple subgoals. Following the above preprocessing,
   In the Diffusion-Proof, we apply the block            we construct a dataset containing 300k records of
dLLM framework as the base model. Unlike the tra-        SFT data for prover training and 128k records for
ditional dLLMs, the sequence is divided into blocks      corrector training.
      theorem lean_workbook_21545_1 (a b c: R) (ha: 0 ≤ a) (hb: 0 ≤ b) (hc: 0 ≤ c) (hab: a + b +
          c = 3) : a^2 / (a + 1) + b^2 / (b + 1) + c^2/(c + 1) ≥ a*b*c / (a + b + c) * Real.sqrt
          (a*b + b*c + c*a):= by
        rw [hab]
        have : 0 ≤ a*b*c := by positivity
        have h1 : a^2 / (a + 1) ≥ a^2 / 4 := by gcongr; linarith
        have h2 : b^2 / (b + 1) ≥ b^2 / 4 := by gcongr; linarith
        have h3 : c^2 / (c + 1) ≥ c^2 / 4 := by gcongr; linarith
        have h4 : a^2 / 4 + b^2 / 4 + c^2 / 4 ≥ a*b*c / 3 * Real.sqrt (a*b + b*c + c*a) := by
          have : a*b*c ≤ 1 := by
            nlinarith [sq_nonneg (a - b), sq_nonneg (b - c), sq_nonneg (c - a)]
          have : Real.sqrt (a*b + b*c + c*a) ≤ 2 := by
            apply Real.sqrt_le_iff.mpr
            constructor
            · positivity
            · nlinarith [sq_nonneg (a - b), sq_nonneg (b - c), sq_nonneg (c - a)]
          nlinarith [sq_nonneg (a - b), sq_nonneg (b - c), sq_nonneg (c - a)]
        nlinarith



  Figure 2: Example of data with subgoal-decomposition, the have hi at top-level is the decomposed subgoal

2.3    Prover & Corrector Training                       information from the extended diffusion block to
                                                         perform in-filling corrections on subgoals by lever-
After obtaining the dataset, we fine-tune the dLLM-      aging bi-directional information.
Prover-7B and dLLM-Corrector-7B models. For
the prover model, we start with the base model           2.4   Proof Writing & Correction
Fast-dLLM-V2-7B (Wu et al., 2025a) and employ            Using the dLLM-Prover-7B and dLLM-Corrector-
a standard text-to-text training framework under         7B trained from above steps, Diffusion-Proof is
the Lean4 code-completion task. To ensure the sta-       able to perform both whole-proof generation and
bility of training, we maintain the diffusion block      error correction with long-range coherence. During
size to be 32, which is consistent with the origi-       the whole-proof writing stage, the dLLM-Prover-
nal model. Additionally, we implement curriculum         7B generates proofs based on the NL and Lean4
data sorting (Wang et al., 2024), which organizes        statement of the theorem. This process is based
the training by increasing order of proof complexity     on the proof generation method from DeepSeek-
based on proof length. This approach enables the         Prover-V1 (Xin et al., 2024a).
model to first learn simpler proofs before progress-        If the initial proof by the prover fails the Lean
ing to more complex ones, thereby stabilizing the        verification but all the top-level subgoal statements
loss curve. Following the above training process         and their usages are correct, we perform a large-
on the 300k SFT dataset, the dLLM-Prover-7B be-          block correction using the corrector. The correction
comes proficient in formal theorem proving. Such         process begins with deleting the proofs in the sub-
training enables the model to write formal proofs        goal that causes the error and replacing them with
with better long-range coherence in the sense of         a 256-token sequence of diffusion generation mask
planning and tactic usage through block diffusion        <|MASK|>. The dLLM-Corrector-7B then refines
generation.                                              these masked sections using 512-length diffusion
   Subsequently, we further leverage the bi-             blocks, such that a large block can leverage both
directional information understanding of dLLMs           prefix and suffix context to perform in-filling cor-
by proposing a large-block training method for the       rections. To encourage more creative and accurate
corrector. Under such a training method, we ex-          proof writing, we set the generation temperature to
tend the diffusion block size from 32 to 512 and         1.2. Additionally, the confidence of one token to be
apply loss to both the subgoal proof block and the       denoised is increased to 0.95 to ensure the robust-
placeholder token. It aims to train the model to         ness of the generation. The input-output example
write local corrections and fill the rest of the block   for dLLM-Corrector can be found in Appendix F.
with placeholder tokens. We apply such a training           Through the above inference process, we are
method to dLLM-Prover-7B and obtain the dLLM-            able to perform long-range coherent proof genera-
Corrector-7B. This enables the corrector to utilize      tion that surpasses the limitations of AR generation
and effectively fixes local errors through in-filling   as dLLM-Prover-7B and employs the same text-to-
corrections.                                            text training method. The SFT version is named
                                                        Qwen-2.5-Lean-SFT-7B in our experiment. We se-
3     Experiments                                       lect this baseline because Qwen-2.5-Instruct-7B is
We evaluate Diffusion-Proof on Lean4 theo-              the base model for Fast-dLLM-V2-7B (Wu et al.,
rem proving through extensive experiments on            2025a), and neither model undergoes additional
MiniF2F-Test (Zheng et al., 2021) and ProofNet-         post-training focused on mathematics or Lean4 cod-
Test (Azerbayev et al., 2023) benchmarks. Sec-          ing. Therefore, both models share a comparable
tion 3.1 and 3.2 describe the experiment setup and      foundation in formal reasoning. It makes the perfor-
implementation details. Subsequently, Section 3.3       mance improvement of Diffusion-Proof a strong
reports the main results of our experiment. Fur-        indicator of the effectiveness of the diffusion-based
thermore, Section 3.4 provides further analyses in      framework.
the training-loss study; Section 3.5 analyzes the          We emphasize that the primary goal of this study
performance after dropping out the key component,       is to investigate whether dLLMs offer architec-
and Section 3.6 offers detailed case studies.           tural advantages over AR models for formal rea-
                                                        soning, rather than achieving state-of-the-art per-
3.1    Experiment Setup                                 formance. Therefore, we deliberately control for
3.1.1 Dataset and Task                                  confounding factors and compare only the genera-
We evaluate the formal reasoning capabilities           tion paradigm. For reference, contemporary SFT-
of the Diffusion-Proof framework by MiniF2F-            only provers like DeepSeek-Prover-V1.5 achieve
Test (Zheng et al., 2021) and ProofNet-Test (Azer-      approximately 48.2% on MiniF2F with larger-scale
bayev et al., 2023) benchmarks. These datasets          training, suggesting the meaningfulness of our
are frequently employed in major studies on the         framework.
LLM formal reasoning field (Xin et al., 2024a;             To measure the performance, we adopt the stan-
Ren et al., 2025; Wang et al., 2024; Dong and Ma,       dard pass@32 metric applied in almost all previous
2025; Lin et al., 2025b; Wang et al., 2025c). The       studies. The details of the evaluation metric can be
MiniF2F-Test datasets comprise 244 math prob-           found in Appendix G.
lems formalized in Lean4. Its difficulty ranges from    3.2   Implementation Details
high-school competition problems to elementary
undergraduate-level problems. The problems in-          This section outlines the implementation details for
clude formalized competition problems from IMO,         the prover, corrector, and baseline models. The
AIME, and AMC, a subset of the Math-500 bench-          prover and baseline models are fine-tuned on the
mark (Lightman et al., 2023), and hand-crafted          SFT dataset described in Section 2.2 using a learn-
problems with a similar level of difficulty. On the     ing rate of 1E-5 and a context length of 2,048 to-
other hand, the ProofNet-test contains 186 theo-        kens. On the other hand, the corrector is trained
rems derived from college textbooks, covering ad-       with a reduced learning rate of 5E-6. All models
vanced topics such as real and complex analysis,        share the same other training configuration, em-
linear algebra and topology.                            ploying a learning rate scheduler with 3% warm-
   The task for the LLMs is to generate formal          up steps. Training is conducted on 4-card H100
proofs for theorems based on their NL and Lean4         GPUs with a global batch size of 64. Each model
statements using direct code-completion. We do          requires approximately one day of training. For
not allow Long CoT thinking process because both        detailed training and inference setup, please refer
Diffusion-Proof and baselines does not support          Appendix B.
such long context.                                      3.3   Results
3.1.2 Baselines & Evaluation Metric                     The main evaluation results is presented in Table 1.
The primary goal of this study is to evaluate the       It shows that Diffusion-Proof achieves an accuracy
potential of dLLMs in formal theorem proving,           rate of 50.00% on MiniF2F and 7.53% on ProofNet.
particularly their capability to achieve long-range     The result surpasses the Qwen-2.5-Lean-SFT-7B
coherent tactics usage. Thus, for a fair comparison,    baseline by 6.14% and 1.61%, respectively. The
we use Qwen-2.5-Instruct-7B (Qwen et al., 2025),        baseline records 43.85% on MiniF2F and 5.91%
which is fine-tuned on the same training dataset        on ProofNet.
             Dataset              Data Number    Qwen-2.5-Lean-SFT-7B      Diffusion-Proof    Improvement

          ProofNet-Test               186                5.91%                 7.53%              1.61%

          MiniF2F-Test                244               43.85%                 50.00%             6.14%

   MiniF2F-Test by problem type
             IMO                      20                5.00%                  15.00%            10.00%
             AIME                     15                33.33%                 33.33%             0.00%
             AMC                      45                22.22%                 26.67%             4.44%
            Algebra                   88                55.68%                 67.05%            11.36%
        Number Theory                 68                58.82%                 63.24%             4.41%
           Induction                   8                25.00%                 25.00%             0.00%

Table 1: Main experiment result of Diffusion-Proof under MiniF2F-Test (Zheng et al., 2021) and ProofNet-
Test (Azerbayev et al., 2023) with pass@32 metric and 32 corrections for each valid theorem

   A detailed analysis of MiniF2F results indi-
cates that Diffusion-Proof outperforms the base-
line across most problem types. Notably, it demon-
strates relatively significant gains in challenging
IMO and AMC problems, solving two additional
problems in each category. Furthermore, compa-
rably significant improvements are also observed
in Algebra and Number Theory. It highlights
the framework’s enhanced formal reasoning ca-
pabilities in both fields. On the more challeng-
ing ProofNet benchmark, despite the lower abso-
lute improvements, Diffusion-Proof also shows           Figure 3: Validation loss for trained dLLM, trained AR
clear progress over the baseline. We also compare       LLM, base dLLM, and base AR LLM
Diffusion-Proof with broader baselines and the          The p-value for both correlations is under 10−100 .
performance of Diffusion-Proof on harder prob-          This demonstrates that, in terms of causal attention
lems that require longer proofs. Detailed results       loss, the models within each category are almost
are provided in Appendix C.1 and C.2.                   equivalent. However, the fine-tuned dLLM rela-
                                                        tively significantly outperforms the SFT AR model
3.4   Validation Loss Study                             across all benchmarks. We attribute this advantage
In this section, we investigate why dLLMs outper-       to the natural diffusion generation. It features iter-
form AR models in formal proof writing based            ative refinement in the diffusion block, enhanced
on the validation loss. Using the 190 correct           long-range coherence, and bi-directional informa-
Lean theorem proofs from MiniF2F-Test com-              tion awareness. The loss comparison highlights the
pleted by DeepSeek-Prover-V2 (Ren et al., 2025).        superior capability of dLLMs in formal reasoning.
We compare the cross-entropy loss of different
models under the pure causal mask. For dLLMs,           3.5   Ablation Study in Correction Process
this comparison is achieved by setting the diffu-       This section presents an ablation study to evaluate
sion block size to 1. We evaluate four models:          the impact of the correction process in the
the fine-tuned dLLM (dLLM-Prover-7B), the fine-         Diffusion-Proof framework.           The corrector
tuned AR model (Qwen-2.5-Lean-SFT-7B), the              contributes to solving 4 out of 122 problems
base dLLM (Fast-dLLM-V2-7B), and the base AR            in the MiniF2F-Test, namely imo_1962_p2,
model (Qwen-2.5-Instruct-7B). The validation loss       amc12b_2002_p7, mathd_algebra_215, and
distribution is presented in Figure 3, whith detailed   mathd_numbertheory_521. It results in a 1.64%
plots available in Appendix H.                          improvement in the benchmark. These problems
   The results reveal that the two base models ex-      typically involve complex subgoal decomposition
hibit nearly identical loss distributions, as well as   and require the corrector to further split objectives
two fine-tuned models. The statistical analysis         into multiple cases to complete the proof. The
shows that the Pearson correlation for SFT mod-         detailed case study is presented in Section 3.6.1.
els is 0.9846 and for base models, it is 0.9838.        On the other side, even without the corrector, the
dLLM-Prover-7B still outperforms the baseline by           proof. Leveraging the corrector’s long-range gener-
4.51% on MiniF2F, validating the effectiveness of          ation capability and large attention block, it identi-
dLLMs for formal reasoning.                                fies the appropriate tactic and applies it correctly.
   However, on the ProofNet-test dataset, the cor-         Notably, the proof of h6 is generated before h4 ,
rector’s local proof fix proves no additional theo-        and the bi-directional awareness of the diffusion
rems. This is because such a dataset focuses more          corrector allows the model to learn from the suffix
on advanced knowledge over complex subgoal di-             generation of the same block directly. This further
vision or long-range reasoning. With its inherent          proves the advantages of the corrector’s large dif-
difficulty, such a dataset is naturally not suitable for   fusion block in capturing and utilizing contextual
a corrector’s local proof fix. We further perform the      information effectively.
analysis using the AR model and dLLM-Prover-7B
to replace the corrector and to compare in-place           3.6.2   Compare to AR baseline model
correction with top-level correction; the results are      We analyze two representative cases where dLLM-
shown in Appendix C.3.                                     Prover-7B succeeds while the AR baseline fails,
                                                           namely imo_1983_p6 and mathd_algebra_188.
3.6     Case Study                                         The complete examples are provided in Ap-
This section presents a detailed case study to evalu-      pendix I.2. In the case of imo_1983_p6, both mod-
ate the qualitative performance of Diffusion-Proof.        els attempt to prove the inequality by supplying
We only present analysis here with additional ex-          complex conditions to the tactic linearity. The
amples provided in Appendix I.                             dLLM’s block diffusion generation enables it to
                                                           take a more comprehensive strategy, providing suit-
3.6.1    Theorems proved by corrector                      able input for the theorem mul_nonneg. In con-
This section analyzes the performance of dLLM-             trast, the AR model fails to provide adequate in-
Corrector-7B in successfully performing local              puts, rendering the wrong theorem proof. In the
theorem proofs based on a skeleton generated               mathd_algebra_188, the AR model applies incor-
by dLLM-Prover-7B. We select two represen-                 rect tactics in both subgoal proofs, leaving the the-
tative cases, namely mathd_algebra_215 and                 orem incomplete. On the other hand, the dLLM
mathd_numbertheory_521, for the case study.                employs a more effective approach. It successfully
   In the case of mathd_algebra_215, both the ini-         solves the subgoals. This comparison highlights
tial failed proof (Figure 10) and the corrected proof      the dLLM’s ability to perform coherent planning, a
(Figure 9) share the same global structure. The            capability that the AR models lack.
proof begins by establishing the elements of the
set S and then demonstrating that these elements           3.6.3   Compare to DeepSeek-Prover-V2
satisfy the given conditions. However, the origi-          One surprising result from our experiments is that
nal proof struggles to apply tactics for handling          Diffusion-Proof successfully completes the proof
complex algebraic computations. On the contrary,           for imo_1962_p2. The problem fails the DeepSeek-
the corrector generates the entire proof in a single       Prover-V2-7B (Ren et al., 2025) under pass@32
diffusion block, enabling a more strategic plan-           with Long CoT reasoning. The detail of this ex-
ning. The process begins with generating the in-           ample is presented in Appendix I.3. As shown in
ternal have decomposition, followed by proving             Figure 16, despite DS-Prover providing sufficient
each subgoal. It demonstrates the corrector’s ca-          natural language analysis during the Long CoT
pability to perform long-range coherent reasoning          process, it lacks a detailed proof plan and coher-
and tactic usage. Additionally, the final intro h          ent tactic usage. This deficiency leads to repeated
steps mirror the type refinement seen in the latter        self-corrections in the natural language plan with-
parts of the proof. It further highlights the model’s      out providing additional insight into Lean beyond
bi-directional context awareness, which enables it         direct code writing. Although the model easily
to complete the proof based on suffix information.         proves the condition −1 ≤ x. It fails on the second
   In the case of mathd_numbertheory_521, the              case, by providing the wrong direction of inequal-
original proof fails due to incorrect usage of             ity in h19 , which collapses the entire proof. In
linarith and rw tactics. These tactics are less            contrast, the corrector in Diffusion-Proof demon-
effective in the domain of natural numbers com-            strates a more robust and coherent tactic usage. It
pared to omega, which is used in the corrected             successfully addresses the long-range dependen-
cies required for this proof. By leveraging its large       Early foundational efforts, such as LLaDA (Nie
diffusion block, the corrector can have better plan-     et al., 2025) and Dream (Ye et al., 2025), demon-
ning and execution of complex reasoning steps.           strated the potential of this paradigm. Subsequent
This highlights the potential of dLLMs in formal         advancements, including efficient inference frame-
theorem proving, particularly for tasks requiring        works like dInfer (Ma et al., 2025) and Fast-dLLM
intricate tactic planning.                               family (Wu et al., 2025b) have substantially im-
                                                         proved the practical deployment of dLLMs through
4     Related Work                                       innovations in KV-cache management and system-
                                                         level optimizations. Additionally, block diffusion
4.1    LLMs For Formal Theorem Proving
                                                         techniques (Wu et al., 2025a) extend diffusion
In recent years, LLMs have gained prominence in          models beyond fixed-length generation, enabling
formal theorem proving with Lean4 (Moura and             greater flexibility. LLaDA 2.0 (Bie et al., 2025)
Ullrich, 2021) emerging as a widely used environ-        scales dLLMs to 100B parameters and has show-
ment for formal verification tasks. Multiple works       cased the viability of these architectures at the fron-
have contributed millions of records of theorem          tier of language modeling. Despite their grow-
statements and proofs (Wang et al., 2024; Wu et al.,     ing application in downstream tasks (You et al.,
2024; Lin et al., 2025a; Dong and Ma, 2025), es-         2025; Dong et al., 2025; Shi et al., 2025), apply-
tablishing a robust foundation for the domain.           ing dLLMs for formal reasoning is still an under-
   In the sense of model training, early advance-        explored field. This gap highlights an opportunity
ments in training LLMs for theorem proving               for further research into applying dLLMs to tasks
introduced SFT frameworks, including Expert              requiring rigorous logical coherence.
Iteration (Polu et al., 2022), Re-Prover (Yang
et al., 2024b), TheoremLlama (Wang et al., 2024),        5   Conclusion
DeepSeek-Prover-V1 (Xin et al., 2024a), BFS-
Prover (Xin et al., 2025), and Goedel-Prover-            This paper presents Diffusion-Proof, a compre-
V1 (Lin et al., 2025a). Subsequent developments          hensive training and inference framework for ap-
leveraged RL with verifier rewards, leading to           plying diffusion LLM (dLLM) for formal theorem
the reasoning systems such as MA-LoT (Wang               proving. Diffusion-Proof aims to address limi-
et al., 2025b), Kimina-Prover (Wang et al.,              tations of Auto-Regressive (AR) models, such as
2025a), Goedel-Prover-V2 (Lin et al., 2025b), and        their inherent lack of long-range coherence in proof
DeepSeek-Prover-V2 (Ren et al., 2025). More              generation and inability to perform bi-directional
recently, agentic-RL has been actively explored          aware, in-filling proof corrections. Diffusion-
for multi-agent proving systems, leading to frame-       Proof tries to overcome these challenges by in-
works like GAR (Wang et al., 2025c) and Seed-            tegrating two key components: dLLM-Prover and
Prover-V1.5 (Chen et al., 2025), which further im-       dLLM-Corrector. The prover employs block diffu-
proved the performance in theorem proving. De-           sion training and generation to enable long-range
spite these significant strides, most, if not all, ex-   coherent tactic usage and improve long-range proof
isting approaches rely on AR LLMs, leaving the           planning. The corrector, a large-block diffusion
dLLM largely under-explored in the context of for-       model, performs in-filling proof corrections using
mal reasoning.                                           bi-directional context, allowing the system to tackle
                                                         more complex problems. Extensive experiments
4.2    Diffusion LLMs                                    demonstrate that Diffusion-Proof framework out-
Diffusion Large Language Models (dLLMs) have             performs the AR baseline trained under the same
emerged as a promising alternative to Auto-              dataset by 6.14% in MiniF2F-Test and 1.61%
Regressive (AR) models for text generation. Unlike       in ProofNet-Test under pass@32. Notably, with
AR models, which generate tokens sequentially            the integration of the corrector, Diffusion-Proof
from left to right, dLLMs generate text using a de-      successfully solves an IMO problem that much
noising process. It progressively refines the masked     stronger DeepSeek-Prover-V2-7B cannot handle.
tokens through multiple diffusion steps (Nie et al.,     Beyond theorem proving, Diffusion-Proof pro-
2025; Ye et al., 2025). This iterative approach in-      vides a promising approach by highlighting the
herently supports long-range coherence, a feature        unique advantages of dLLMs in tasks that require
often lacking in AR architectures.                       long-range coherence and precise reasoning.
Limitations                                               Leonardo De Moura, Soonho Kong, Jeremy Avigad,
                                                            Floris Van Doorn, and Jakob von Raumer. 2015. The
Despite Diffusion-Proof presenting promising re-            lean theorem prover (system description). In Auto-
sults, there are areas that warrant further explo-          mated Deduction-CADE-25: 25th International Con-
                                                            ference on Automated Deduction, Berlin, Germany,
ration as the application of dLLMs in formal rea-           August 1-7, 2015, Proceedings 25, pages 378–388.
soning and other downstream tasks is still in its           Springer.
nascent stages. First, this work is conducted with
limited computational resources, which restricts          Kefan Dong and Tengyu Ma. 2025. Stp: Self-play
                                                            llm theorem provers with iterative conjecturing and
the training scale below the state-of-the-art open-         proving. arXiv preprint arXiv:2502.00212.
source AR provers such as Goedel-Prover-V2 (Lin
et al., 2025b) and DeepSeek-Prover-V2 (Ren et al.,        Xuanzhao Dong, Wenhui Zhu, Xiwen Chen, Zhipeng
                                                            Wang, Peijie Qiu, Shao Tang, Xin Li, and Yalin Wang.
2025). Second, the current base model’s limited             2025. Llada-medv: Exploring large language dif-
Long CoT capability prevents a comprehensive                fusion models for biomedical image understanding.
exploration of dLLM’s potential for long think-             arXiv preprint arXiv:2508.01617.
ing in theorem proving. Third, this work focuses
                                                          Nouha Dziri, Ximing Lu, Melanie Sclar, Xiang Lorraine
only on Lean4. Although benchmarks such as                  Li, Liwei Jiang, Bill Yuchen Lin, Sean Welleck, Peter
MiniF2F include partial formalizations in other             West, Chandra Bhagavatula, Ronan Le Bras, and 1
theorem provers, training a dLLM prover requires            others. 2023. Faith and fate: Limits of transformers
large-scale proof corpora, verification infrastruc-         on compositionality. Advances in Neural Information
                                                            Processing Systems, 36:70293–70332.
ture, and model-specific preprocessing. Compara-
ble resources are currently much stronger for Lean4       John Harrison. 2009. Hol light: An overview. In Inter-
than for theorem provers such as Isabelle in our            national Conference on Theorem Proving in Higher
                                                            Order Logics, pages 60–66. Springer.
setting. Finally, this study focuses primarily on
the empirical improvements and does not delve             Hunter Lightman, Vineet Kosaraju, Yuri Burda, Harri-
into the theoretical foundations of dLLMs. These            son Edwards, Bowen Baker, Teddy Lee, Jan Leike,
                                                            John Schulman, Ilya Sutskever, and Karl Cobbe.
aspects provide valuable opportunities for future
                                                            2023. Let’s verify step by step. In The Twelfth Inter-
research to scale training further, develop models          national Conference on Learning Representations.
with enhanced reasoning capabilities, and establish
a theoretical framework to further understand and         Yong Lin, Shange Tang, Bohan Lyu, Jiayun Wu,
                                                            Hongzhou Lin, Kaiyu Yang, Jia Li, Mengzhou
advance the usage of dLLMs in formal reasoning              Xia, Danqi Chen, Sanjeev Arora, and Chi Jin.
tasks.                                                      2025a.   Goedel-prover: A frontier model for
                                                            open-source automated theorem proving. Preprint,
                                                            arXiv:2502.07640.
References                                                Yong Lin, Shange Tang, Bohan Lyu, Ziran Yang, Jui-
Zhangir Azerbayev, Bartosz Piotrowski, Hailey               Hui Chung, Haoyu Zhao, Lai Jiang, Yihan Geng,
  Schoelkopf, Edward W Ayers, Dragomir Radev, and           Jiawei Ge, Jingruo Sun, and 1 others. 2025b. Goedel-
  Jeremy Avigad. 2023. Proofnet: Autoformalizing            prover-v2: Scaling formal theorem proving with
  and formally proving undergraduate-level mathemat-        scaffolded data synthesis and self-correction. arXiv
  ics. arXiv preprint arXiv:2302.12433.                     preprint arXiv:2508.03613.
                                                          Yuxin Ma, Lun Du, Lanning Wei, Kun Chen, Qian Xu,
Tiwei Bie, Maosong Cao, Kun Chen, Lun Du, Min-
                                                            Kangyu Wang, Guofeng Feng, Guoshan Lu, Lin Liu,
  gliang Gong, Zhuochen Gong, Yanmei Gu, Jiaqi Hu,
                                                            Xiaojing Qi, and 1 others. 2025. dinfer: An efficient
  Zenan Huang, Zhenzhong Lan, and 1 others. 2025.
                                                            inference framework for diffusion language models.
  Llada2. 0: Scaling up diffusion language models to
                                                            arXiv preprint arXiv:2510.08666.
  100b. arXiv preprint arXiv:2512.15745.
                                                          Leonardo de Moura and Sebastian Ullrich. 2021. The
Jiangjie Chen, Wenxiang Chen, Jiacheng Du, Jinyi Hu,        lean 4 theorem prover and programming language. In
   Zhicheng Jiang, Allan Jie, Xiaoran Jin, Xing Jin,        Automated Deduction–CADE 28: 28th International
   Chenggang Li, Wenlei Shi, and 1 others. 2025. Seed-      Conference on Automated Deduction, Virtual Event,
   prover 1.5: Mastering undergraduate-level theorem        July 12–15, 2021, Proceedings 28, pages 625–635.
   proving via learning from experience. arXiv preprint     Springer.
   arXiv:2512.17260.
                                                          Shen Nie, Fengqi Zhu, Zebin You, Xiaolu Zhang,
Projet Coq. 1996. The coq proof assistant-reference         Jingyang Ou, Jun Hu, Jun Zhou, Yankai Lin, Ji-Rong
  manual. INRIA Rocquencourt and ENS Lyon, ver-             Wen, and Chongxuan Li. 2025. Large language dif-
  sion, 5.                                                  fusion models. arXiv preprint arXiv:2502.09992.
Lawrence C Paulson. 1994. Isabelle: A generic theorem     Chengyue Wu, Hao Zhang, Shuchen Xue, Zhijian Liu,
  prover. Springer.                                         Shizhe Diao, Ligeng Zhu, Ping Luo, Song Han, and
                                                            Enze Xie. 2025b. Fast-dllm: Training-free accel-
Stanislas Polu, Jesse Michael Han, Kunhao Zheng, Man-       eration of diffusion llm by enabling kv cache and
   tas Baksys, Igor Babuschkin, and Ilya Sutskever.         parallel decoding. arXiv preprint arXiv:2505.22618.
   2022. Formal mathematics statement curriculum
   learning. arXiv preprint arXiv:2202.01344.             Zijian Wu, Jiayu Wang, Dahua Lin, and Kai Chen.
                                                             2024. Lean-github: Compiling github lean repos-
Qwen, :, An Yang, Baosong Yang, Beichen Zhang,               itories for a versatile lean prover. arXiv preprint
 Binyuan Hui, Bo Zheng, Bowen Yu, Chengyuan                  arXiv:2407.17227.
 Li, Dayiheng Liu, Fei Huang, Haoran Wei, Huan            Huajian Xin, Daya Guo, Zhihong Shao, Zhizhou Ren,
 Lin, Jian Yang, Jianhong Tu, Jianwei Zhang, Jianxin        Qihao Zhu, Bo Liu, Chong Ruan, Wenda Li, and
 Yang, Jiaxi Yang, Jingren Zhou, and 25 oth-                Xiaodan Liang. 2024a. Deepseek-prover: Advancing
 ers. 2025. Qwen2.5 technical report. Preprint,             theorem proving in llms through large-scale synthetic
 arXiv:2412.15115.                                          data. arXiv preprint arXiv:2405.14333.
ZZ Ren, Zhihong Shao, Junxiao Song, Huajian Xin,          Huajian Xin, ZZ Ren, Junxiao Song, Zhihong Shao,
  Haocheng Wang, Wanjia Zhao, Liyue Zhang, Zhe              Wanjia Zhao, Haocheng Wang, Bo Liu, Liyue Zhang,
  Fu, Qihao Zhu, Dejian Yang, and 1 others. 2025.           Xuan Lu, Qiushi Du, and 1 others. 2024b. Deepseek-
  Deepseek-prover-v2: Advancing formal mathemati-           prover-v1. 5: Harnessing proof assistant feedback for
  cal reasoning via reinforcement learning for subgoal      reinforcement learning and monte-carlo tree search.
  decomposition. arXiv preprint arXiv:2504.21801.           arXiv preprint arXiv:2408.08152.

Teng Shi, Chenglei Shen, Weijie Yu, Shen Nie, Chongx-     Ran Xin, Chenguang Xi, Jie Yang, Feng Chen, Hang
  uan Li, Xiao Zhang, Ming He, Yan Han, and Jun Xu.         Wu, Xia Xiao, Yifan Sun, Shen Zheng, and Kai Shen.
  2025. Llada-rec: Discrete diffusion for parallel se-      2025. Bfs-prover: Scalable best-first tree search for
  mantic id generation in generative recommendation.        llm-based automatic theorem proving. arXiv preprint
  arXiv preprint arXiv:2511.06254.                          arXiv:2502.03438.

Sumanth Varambally, Thomas Voice, Yanchao Sun,            Kaiyu Yang, Gabriel Poesia, Jingxuan He, Wenda Li,
  Zhifeng Chen, Rose Yu, and Ke Ye. 2025. Hilbert:          Kristin Lauter, Swarat Chaudhuri, and Dawn Song.
  Recursively building formal proofs with informal rea-     2024a. Formal mathematical reasoning: A new fron-
  soning. arXiv preprint arXiv:2509.22819.                  tier in ai. arXiv preprint arXiv:2412.16075.

                                                          Kaiyu Yang, Aidan Swope, Alex Gu, Rahul Chala-
Haiming Wang, Mert Unsal, Xiaohan Lin, Mantas               mala, Peiyang Song, Shixing Yu, Saad Godil, Ryan J
  Baksys, Junqi Liu, Marco Dos Santos, Flood Sung,          Prenger, and Animashree Anandkumar. 2024b. Le-
  Marina Vinyes, Zhenzhe Ying, Zekai Zhu, and 1 oth-        andojo: Theorem proving with retrieval-augmented
  ers. 2025a. Kimina-prover preview: Towards large          language models. Advances in Neural Information
  formal reasoning models with reinforcement learning.      Processing Systems, 36.
  arXiv preprint arXiv:2504.11354.
                                                          Jiacheng Ye, Zhihui Xie, Lin Zheng, Jiahui Gao, Zirui
Ruida Wang, Rui Pan, Yuxin Li, Jipeng Zhang,                 Wu, Xin Jiang, Zhenguo Li, and Lingpeng Kong.
  Yizhen Jia, Shizhe Diao, Renjie Pi, Junjie Hu, and         2025. Dream 7b: Diffusion large language models.
  Tong Zhang. 2025b. Ma-lot: Model-collaboration             arXiv preprint arXiv:2508.15487.
  lean-based long chain-of-thought reasoning en-
  hances formal theorem proving. arXiv preprint           Huaiyuan Ying, Zijian Wu, Yihan Geng, Jiayu Wang,
  arXiv:2503.03205.                                         Dahua Lin, and Kai Chen. 2024. Lean workbook:
                                                            A large-scale lean problem set formalized from
Ruida Wang, Jiarui Yao, Rui Pan, Shizhe Diao, and           natural language math problems. arXiv preprint
  Tong Zhang. 2025c. Gar: Generative adversarial            arXiv:2406.03847.
  reinforcement learning for formal theorem proving.
                                                          Zebin You, Shen Nie, Xiaolu Zhang, Jun Hu, Jun Zhou,
  arXiv preprint arXiv:2510.11769.
                                                            Zhiwu Lu, Ji-Rong Wen, and Chongxuan Li. 2025.
                                                            Llada-v: Large language diffusion models with visual
Ruida Wang, Jipeng Zhang, Yizhen Jia, Rui Pan, Shizhe       instruction tuning. arXiv preprint arXiv:2505.16933.
  Diao, Renjie Pi, and Tong Zhang. 2024. Theoreml-
  lama: Transforming general-purpose llms into lean4      Kunhao Zheng, Jesse Michael Han, and Stanislas Polu.
  experts. arXiv preprint arXiv:2407.03203.                 2021. Minif2f: a cross-system benchmark for for-
                                                            mal olympiad-level mathematics. arXiv preprint
Chengyue Wu, Hao Zhang, Shuchen Xue, Shizhe Diao,           arXiv:2109.00110.
  Yonggan Fu, Zhijian Liu, Pavlo Molchanov, Ping
  Luo, Song Han, and Enze Xie. 2025a. Fast-dllm
  v2: Efficient block-diffusion llm. arXiv preprint
  arXiv:2509.26328.
A     Discussion                                           in the entire prover ecosystem. The results are
                                                           demonstrated in Table 2.
A.1    AI usage                                               From these results, we observe that Diffusion-
This work utilized Copilot to assist with code writ-       Proof, trained only on 300k data with standard
ing and OpenAI’s models to correct grammatical             SFT, outperforms AR-based SFT models on larger
issues in the paper. All the ideas of the paper are        datasets and achieves results comparable to early-
original.                                                  stage RL methods. This demonstrates the potential
                                                           of diffusion models for formal theorem proving.
A.2    Potential Risk                                      However, the lack of the RLVR (Reinforcement
This work focuses on applying a new form of                Learning with Verifiable Feedback) technique and
model beyond AR LLMs to physics theorem prov-              Long CoT reasoning currently limits our model’s
ing tasks; there is no foreseeable potential risk for      ability to surpass SOTA AR provers. This re-
this paper.                                                sult demonstrates that diffusion provers provide
                                                           a stronger foundation for models and point the fu-
A.3    Discussion on Data                                  ture direction of developing better RL methods for
The data used in this paper are based on open-             the field.
source data from previous peer-reviewed works,             C.2   Long Proof Subset Comparison
which adhere to the ethics standards of major con-
ferences, introducing no foreseeable risk of leak-         To evaluate whether the gain is concentrated in
ing personally identifiable information or offensive       problems requiring longer formal derivations, we
content.                                                   sort MiniF2F-Test problems by the length of re-
                                                           leased DeepSeek-Prover-V2 proofs and evaluate
A.4    Discussion on License and Scientific                performance on the longest subsets. As shown
       Artifact Use                                        in Table 3, Diffusion-Proof solves 5/54 problems
                                                           on the longest 25% subset and 26/108 problems
The datasets we use are published under the MIT
                                                           on the longest 50% subset, compared with 4/54
License, and the base model Qwen-2.5 is published
                                                           and 20/108 for the AR baseline. The larger gap
under the Apache 2.0 License. When we open-
                                                           on the longest half of the benchmark supports our
source the model, it follows the Apache 2.0 Li-
                                                           hypothesis that block diffusion generation is par-
cense, and the dataset follows the MIT License.
                                                           ticularly useful when proof construction requires
Additionally, with internal checks, authors agree
                                                           longer-range tactic consistency.
that the scientific artifact follows the original inten-
                                                              More surprisingly, Diffusion-Proof successfully
tion.
                                                           solves one problem (imo_1962_p2) in MiniF2F-
                                                           Test that the more advanced DeepSeek-Prover-V2-
B     Additional Implementation Detail
                                                           7B (Ren et al., 2025), equipped with Long CoT,
The global batch size is implemented with per-GPU          fails to prove under pass@32. This further high-
batch size 2 and gradient accumulation 8. Training         lights the unique advantage of dLLMs in generating
dLLM-Prover-7B and Qwen-2.5-Lean-SFT-7B each               long-range coherent proofs that even more sophis-
takes approximately 96 H100 GPU-hours, while               ticated reasoning models struggle to complete.
training dLLM-Corrector-7B takes an additional 48
H100 GPU-hours. During evaluation, the complete            C.3   Additional Ablation Study on Correction
Diffusion-Proof pipeline, including whole-proof                  Process
generation, Lean verification, and correction, takes       We further test whether a unified model can replace
about 16 hours on our machine. The AR baseline             the proposed dual-model design by using dLLM-
takes about 24 hours without vLLM optimization.            Corrector-7B for both whole-proof writing and cor-
                                                           rection. This pure-corrector setup reaches only
C     Additional Experiment Results                        40.98% on MiniF2F-Test, compared with 50.00%
                                                           for the proposed pipeline. The result indicates
C.1    Compare with Broader Baselines                      that large-block correction training improves local
In this section, we provide a detailed comparison of       infilling behavior but harms first-attempt whole-
provers with different sizes and training methods to       proof generation, supporting the separation be-
better demonstrate the position of Diffusion-Proof         tween global proof writing and local correction.
     Method                                               Size   Training / Inference Setting     MiniF2F-Test
     TheoremLlama (Wang et al., 2024)                   8B                AR SFT                     35.7%
     Lean-STaR                                          7B        AR SFT / expert iteration     46.3% (pass@64)
     DeepSeek-Prover-V1 (Xin et al., 2024a)             7B                AR SFT                     46.3%
     DeepSeek-Prover-V1.5 (Xin et al., 2024b)           7B             AR SFT + RL                   50.0%
     Kimina-Prover-Preview (Wang et al., 2025a)        1.5B      AR SFT + RLVR + Long CoT            56.2%
     DeepSeek-Prover-V2 (Ren et al., 2025)              7B       AR SFT + RLVR + Long CoT           70.49%
     Diffusion-Proof                                    7B              dLLM SFT                     50.0%

Table 2: Contextual comparison with specialized theorem provers. This table is not a controlled comparison because
the systems differ in data scale, RL usage, search, and Long CoT reasoning.

 MiniF2F Subset      Diffusion-Proof   Qwen-Lean-SFT-7B          3tfm1m5zeqn68_feqn10_zeq7. In these cases,
 Longest 25%           5/54 (9.26%)      4/54 (7.41%)            the generated proof often follows a plausible
 Longest 50%         26/108 (24.07%)    20/108 (18.52%)
                                                                 high-level algebraic plan, but then asks Lean
Table 3: Performance on MiniF2F-Test subsets with the
                                                                 arithmetic tactics to discharge obligations that
longest released DeepSeek-Prover-V2 proof lengths.               require missing nonlinear, complex-number, or
                                                                 domain-specific transformations. For example, in
  Model / Correction Setting               MiniF2F-Test
                                                                 amc12a_2020_p15, the model attempts to derive
  dLLM-Corrector-7B as unified model          40.98%             complex-valued polynomial consequences using
  dLLM-Prover-7B only                         48.36%
  dLLM-Prover-7B + dLLM-Corrector-7B          50.00%             arithmetic tactics that are not sufficient for the
  AR line-level rewrite correction          +1 problem           goal.
  dLLM in-place correction                  +2 problems             One example, amc12a_2021_p19, is caused by
  dLLM top-level correction                 +4 problems
                                                                 invalid tactic usage. The model invokes simplifica-
Table 4: Ablations for dual-model design and correc-
                                                                 tion tactics with theorem combinations that do not
tion strategy on MiniF2F-Test. The lower block reports           make progress in Lean, indicating that the tactic
additional problems solved by each correction method.            pattern is locally plausible but not applicable to the
                                                                 current goal state.
   We also compare the top-level correction design                  The remaining two examples, imo_1981_p6 and
with an in-place correction baseline that removes                amc12b_2020_p13, exceed the current model ca-
the erroneous line and regenerates the remaining                 pacity and show repetitive or incomplete proof end-
proof inside the same subgoal. In-place correc-                  ings. These failures occur on problems requiring
tion solves 2 additional MiniF2F-Test problems,                  substantially longer decomposition or specialized
while top-level correction solves 4. This suggests               identities, suggesting that stronger Long CoT rea-
that regenerating the entire top-level subgoal proof             soning, verifier-guided self-reflection, or additional
gives the corrector more freedom to revise the lo-               difficult-proof data may be needed.
cal proof trajectory, whereas in-place correction
remains constrained by earlier potentially mislead-              E     Training data examples
ing tactic choices. Finally, we equip the AR base-               E.1    dLLM-Prover SFT Data Example
line with a correction mechanism by asking Qwen-
                                                                 The training input-output example for dLLM-
2.5-Lean-SFT-7B to rewrite from the line before
                                                                 Prover is presented in Figure 5.
the first error. This corrects only one problem,
mathd_algebra_275, which is already solved by                    E.2    dLLM-Corrector Data Example
dLLM-Prover-7B in whole-proof generation.                        The input and output example for dLLM-Corrector
                                                                 is presented in Figure 6. Additionally, we demon-
D    Error Analysis
                                                                 strate the extent to which a single 512-token dif-
We analyze seven representative failed proofs to                 fusion block can cover in the example. From the
identify common limitations of Diffusion-Proof.                  data example, we can observe that the target block
Four examples are caused by overconfident use of                 for correction is h3 , the training diffusion block
arithmetic tactics such as linarith or nlinarith:                covers both prefix and suffix. Through training
induction_pord1p1on2powklt5on2,                                  on the presented data, the corrector model learns
amc12_2000_p20,                 amc12a_2020_p15,                 to write proofs for subgoals with awareness of bi-
and          algebra_2varlineareq_fp3zeq11_                      directional information.
F     Input-output Examples for corrector               in Figure 16, and the example of a wrong proof for
                                                        DS-Prover is in Figure 17.
The input example for the corrector is presented
in Figure 7, and the output example is in Figure 8.
From the example, we can see that the input se-
quence replaces the original wrong proof in the h1
with a 256 mask token and leaves the corrector to
perform in-filling correction. For the output ex-
ample, we can see the model successfully writes
the proof for the decomposed subgoal and learns
to fill the extra space for the diffusion block with
placeholder tokens. This indicates the success of
our training in the corrector, enabling it to perform
in-filling correction and complete the proof with
placeholder tokens.

G     Evaluation Metrics
The pass@32 evaluation we apply means that,
given a theorem statement, the model generates
32 proofs. If one of the proofs is correct, the theo-
rem is considered correctly proved. For each the-
orem that is valid for correction, we perform an
additional five rounds of correction. In the dataset,
18.31% of records are valid for correction. With
the 2.54x inference speedup of dLLM compared
to the AR models, the GPU hours for baseline and
Diffusion-Proof are comparable.

H     Full Validation Loss results
The complete set of plots for validation analysis
can be found in Figure 4.

I     Case Study Examples
I.1    Examples for corrector
The      corrected     theorem       proof       of
mathd_algebra_215 is presented in Figure 9, and
the wrong proof is in Figure 10. The corrector’s
output of mathd_numbertheory_521 is in Fig-
ure 11 and the base proof with tactic failure is in
Figure 12.

I.2    Example for comparison with AR baseline
The     example      of imo_1983_p2      and
mathd_algebra_188 are presented in Figure 13
and 14 respectively.

I.3    Example for comparison with
       DeepSeek-Prover-V2
The success proof for imo_1962_p2 of Diffusion-
Proof is presented in Figure 15. The DeepSeek-
Prover-V2’s failed proof analysis is demonstrated
                                           Trained Autoreg                                                                                                                   Base Autoreg                                                                                                                 Base Diffusion                                                                                              Trained Diffusion
                                           Loss Distribution                                                                                                                Loss Distribution                                                                                                            Loss Distribution                                                                                            Loss Distribution
                                                                                          Mean: 0.4197                               14                                                                                   Mean: 0.7456                                                                                                     Mean: 0.7421                          14                                                                             Mean: 0.4088
            14                                                                                                                                                                                                                                                         12
                                                                                                                                     12                                                                                                                                                                                                                                          12
            12
                                                                                                                                                                                                                                                                       10
                                                                                                                                     10                                                                                                                                                                                                                                          10
            10
                                                                                                                                                                                                                                                                        8
Frequency




                                                                                                               Frequency




                                                                                                                                                                                                                                                 Frequency




                                                                                                                                                                                                                                                                                                                                                            Frequency
                                                                                                                                      8                                                                                                                                                                                                                                           8
             8
                                                                                                                                                                                                                                                                        6
             6                                                                                                                        6                                                                                                                                                                                                                                           6

                                                                                                                                      4                                                                                                                                 4                                                                                                         4
             4

             2                                                                                                                        2                                                                                                                                 2                                                                                                         2

             0                                                                                                                        0                                                                                                                                 0                                                                                                         0
                         0.2               0.4                 0.6               0.8                  1.0                                      0.25          0.50    0.75      1.00      1.25         1.50         1.75       2.00                                                 0.25   0.50    0.75      1.00      1.25   1.50   1.75       2.00                                                0.2               0.4           0.6               0.8              1.0
                                                    Loss                                                                                                                          Loss                                                                                                                         Loss                                                                                                         Loss


                               All Models - Overlapped Distribution                                                                                                    Box Plot Comparison                                                                                                Cumulative Distribution Function (CDF)                                                                                 Violin Plot Comparison
                                                                                       Trained Autoreg                                                                                                                                                                 1.0
            14                                                                         Base Autoreg                                  2.0                                                                                                                                                                                                                                         2.0
                                                                                       Base Diffusion
                                                                                       Trained Diffusion                                                                                                                                                               0.8
            12




                                                                                                                                                                                                                                              Cumulative Probability
                                                                                                                                     1.5                                                                                                                                                                                                                                         1.5
            10
                                                                                                                                                                                                                                                                       0.6
Frequency




                                                                                                            Loss




                                                                                                                                                                                                                                                                                                                                                          Loss
             8
                                                                                                                                     1.0                                                                                                                                                                                                                                         1.0
             6                                                                                                                                                                                                                                                         0.4

             4                                                                                                                       0.5                                                                                                                                                                                                                                         0.5
                                                                                                                                                                                                                                                                       0.2                                                           Trained Autoreg
                                                                                                                                                                                                                                                                                                                                     Base Autoreg
             2                                                                                                                                                                                                                                                                                                                       Base Diffusion
                                                                                                                                                                                                                                                                       0.0                                                           Trained Diffusion
             0                                                                                                                       0.0                                                                                                                                                                                                                                         0.0
                  0.0           0.5                1.0                     1.5                  2.0                                                                                                                                                                          0.0            0.5               1.0             1.5              2.0
                                                                                                                                                      reg




                                                                                                                                                                            reg




                                                                                                                                                                                                                               on




                                                                                                                                                                                                                                                                                                                                                                                             reg




                                                                                                                                                                                                                                                                                                                                                                                                                reg




                                                                                                                                                                                                                                                                                                                                                                                                                                                                on
                                                                                                                                                                                                  on




                                                                                                                                                                                                                                                                                                                                                                                                                                         on
                                                    Loss                                                                                                                                                                                                                                                       Loss


                                                                                                                                                                                                                             usi




                                                                                                                                                                                                                                                                                                                                                                                                                                                             usi
                                                                                                                                                                                                 usi




                                                                                                                                                                                                                                                                                                                                                                                                                                    usi
                                                                                                                                                   uto




                                                                                                                                                                         uto




                                                                                                                                                                                                                                                                                                                                                                                         uto




                                                                                                                                                                                                                                                                                                                                                                                                               uto
                                                                                                                                                                                                                           iff




                                                                                                                                                                                                                                                                                                                                                                                                                                                            iff
                                                                                                                                                                                                iff




                                                                                                                                                                                                                                                                                                                                                                                                                                   iff
                                                                                                                                              dA




                                                                                                                                                                        A




                                                                                                                                                                                                                                                                                                                                                                                       dA




                                                                                                                                                                                                                                                                                                                                                                                                             A
                                                                                                                                                                                                                          dD




                                                                                                                                                                                                                                                                                                                                                                                                                                                           dD
                                                                                                                                                                                             D




                                                                                                                                                                                                                                                                                                                                                                                                                                    D
                                                                                                                                                                     se




                                                                                                                                                                                                                                                                                                                                                                                                          se
                                                                                                                                             ne




                                                                                                                                                                                                                                                                                                                                                                                   ne
                                                                                                                                                                                          se




                                                                                                                                                                                                                                                                                                                                                                                                                                 se
                                                                                                                                                                    Ba




                                                                                                                                                                                                                                                                                                                                                                                                         Ba
                                                                                                                                                                                                                      ne




                                                                                                                                                                                                                                                                                                                                                                                                                                                      ne
                                                                                                                                                                                         Ba




                                                                                                                                                                                                                                                                                                                                                                                                                            Ba
                                                                                                                                               i




                                                                                                                                                                                                                                                                                                                                                                                     i
                                                                                                                                           Tra




                                                                                                                                                                                                                                                                                                                                                                                 Tra
                                                                                                                                                                                                                       i




                                                                                                                                                                                                                                                                                                                                                                                                                                                        i
                                                                                                                                                                                                                   Tra




                                                                                                                                                                                                                                                                                                                                                                                                                                                    Tra
                                      Loss per Sample - All Models                                                                                                  Trained Models Comparison                                                                                                     Base Models Comparison                                                                                 Autoregressive Models Comparison
                                                                                       Trained Autoreg
            2.0                                                                        Base Autoreg
                                                                                                                                     1.0                                                                                                                          2.00                                                                                                           2.0
                                                                                       Base Diffusion
                                                                                       Trained Diffusion                                                                                                                                                          1.75
                                                                                                                                     0.8
                                                                                                            Trained Diffusion Loss




                                                                                                                                                                                                                                                                                                                                                          Trained Autoreg Loss
            1.5                                                                                                                                                                                                                                                                                                                                                                  1.5
                                                                                                                                                                                                                                         Base Diffusion Loss

                                                                                                                                                                                                                                                                  1.50

                                                                                                                                     0.6                                                                                                                          1.25
Loss




            1.0                                                                                                                                                                                                                                                   1.00                                                                                                           1.0
                                                                                                                                     0.4                                                                                                                          0.75
            0.5                                                                                                                                                                                                                                                   0.50                                                                                                           0.5
                                                                                                                                     0.2
                                                                                                                                                                                                                                                                  0.25
            0.0                                                                                                                                                                                                                                                                                                                                                                  0.0
                    0   25            50     75          100         125         150         175                                                       0.2               0.4             0.6                 0.8                1.0                                                0.25   0.50    0.75      1.00      1.25   1.50   1.75       2.00                                    0.0               0.5               1.0                1.5                    2.0
                                                 Sample Index                                                                                                            Trained Autoreg Loss                                                                                                            Base Autoreg Loss                                                                                            Base Autoreg Loss



Figure 4: Full set of plots for validation loss analysis, including detailed distribution for each model, detailed
distribution analysis, and correlation study for models.




                    ================MODEL INPUT================
                    <|im_start|>Complete the following Lean 4 code with explanatory comments preceding each line of code:

                    ```lean4
                    import Mathlib
                    import Aesop

                    set_option maxHeartbeats 0

                    open BigOperators Real Nat Topology Rat


                    theorem lean_workbook_plus_79832 (x : R)
                       (h0 : 5 + 3.5 * x = 2.5 * x - 25) :
                       x = -30   :=
                    ================TRAINED OUTPUT================
                    by
                       /-
                       To solve the equation \(5 + 3.5x = 2.5x - 25\) for \(x\), we proceed as follows:
                       1. Rewrite the equation to isolate terms involving \(x\) on one side and constant terms on the other side.
                       2. Simplify the equation by eliminating the decimals and combining like terms.
                       3. Solve for \(x\) by isolating it on one side of the equation.
                       -/
                       -- Rewrite the equation to have the terms involving x on one side and constants on the other side.
                       rw [eq_comm] at h0
                       -- Normalize the equation by simplifying and combining like terms.
                       ring_nf at h0 ⊢
                       -- Use linear arithmetic to solve for x.
                       linarith
                    ``` <|im_end|>



                                                                                             Figure 5: Input & output example for SFT data of dLLM-Prover
================MODEL INPUT================
<|im_start|>Complete the following Lean 4 code with explanatory comments preceding each line of code:

```lean4
import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Topology Rat


theorem amc12a_2007_p18
    (n : N) (hn : n ̸= 0)
    (h' : n ̸= 1)
    (x : N → R)
    (h0 : ∀ m, x m = Real.sqrt (n ^ (m + 2)) ) :
    Real.sqrt (1 + 4 * Real.sqrt n) ≤ n * (2 + x n) ^ (n + 1):= by
================TRAINED OUTPUT================
=== Diffusion Block Begins
  have h1 : (n : R) ≥ 2 := by
    norm_cast
    omega
  have h2 : Real.sqrt n ≥ 1 := by
    apply Real.le_sqrt_of_sq_le
    nlinarith
  have h3 : (2 + x n : R) ≥ 3 := by
    have h4 : (x n : R) = Real.sqrt (n ^ (n + 2)) := by
      simpa [h0 ] using rfl
    have h5 : Real.sqrt (n ^ (n + 2)) ≥ 1 := by
      apply Real.le_sqrt_of_sq_le
      have h6 : (n : R) ^ (n + 2) ≥ 1 := by
        apply one_le_pow_of_one_le
        nlinarith
      nlinarith
    nlinarith<|fim_middle|><|fim_middle|><|fim_middle|>(in total 138 placeholder tokens)...
  have h4 : Real.sqrt (1 + 4 * Real.sqrt n) ≤ (n : R) * (2 + x n) ^ (n + 1) := by
    apply Real.sqrt_le_iff.mpr
    constructor
    · positivity
    · have h5 : (n : R) * (2 + x n) ^ (n + 1) ≥ (n : R) * 3 ^ (n + 1) := by
        gcongr
        <;> nlinarith
      have h6 : (n : R) * 3 ^ (n + 1) ≥ n * 3 ^ 2 := by
        apply mul_le_mul_of_nonneg_left
        · exact pow_le_pow_right (by linarith) (by omega)
        · nlinarith
      have h7 :
=== Diffusion Block Ends
        (n : R) * 3 ^ 2 ≥ 9 := by
        nlinarith
      nlinarith [sq_sqrt (show 0 ≤ (n : R) from by positivity),
        sq_sqrt (show 0 ≤ (n : R) from by positivity),
        Real.sqrt_nonneg (n : R),
        Real.sqrt_nonneg (n : R)]
  exact h4
  <;> norm_num
  <;> omega
``` <|im_end|>



 Figure 6: Input & output example for training data of dLLM-Corrector with diffusion block annotation
Complete the following Lean 4 code with explanatory comments preceding each line of code:

```lean4
import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Topology Rat

theorem mathd_algebra_215
   (S : Finset R)
   (h
   P0 : ∀ (x : R), x ∈ S ↔ (x + 3)^2 = 121) :
       k in S, k = -6 := by
   /-
   Given the set \( S \) defined by the equation \((x+3)^2 = 121\), we need to show that the sum of all elements in \( S \)
  ,→ equals \(-6\).
   1. **Identify the elements of \( S \)**:
       - The equation \((x+3)^2 = 121\) implies \( x^2 + 6x + 9 = 121 \).
       - Simplifying this equation, we get \( x^2 + 6x + 9 = 121 \), which simplifies to \( x^2 + 6x - 112 = 0 \).
       - Solving the quadratic equation \( x^2 + 6x - 112 = 0 \), we find the roots using the quadratic formula \( x =
      ,→ \frac{-b \pm \sqrt{b^2 - 4ac}}{2a} \):
         \[
         x = \frac{-6 \pm \sqrt{36 + 448}}{2} = \frac{-6 \pm \sqrt{484}}{2} = \frac{-6 \pm 22}{2}
         \]
       - This gives us two solutions:
         \[
         x = \frac{16}{2} = 8 \quad \text{and} \quad x = \frac{-28}{2} = -14
         \]
       - Therefore, the elements of \( S \) are \( 8 \) and \( -14 \).
   2. **Sum the elements of \( S \)**:
       - The sum of the elements \( 8 \) and \( -14 \) is \( 8 + (-14) = -6 \).
   Thus, the sum of all elements in \( S \) is indeed \(-6\).
   -/
   -- We need Pto show that the sum of all elements in S equals -6.
   have h1 :      k in S, k = -6 := by <|MASK|><|MASK|><|MASK|><|MASK|><|MASK|><|MASK|>(in total 256 generation mask)...
   exact h1
```<|im_end|>



                                  Figure 7: Input example for dLLM-Corrector
Complete the following Lean 4 code with explanatory comments preceding each line of code:

```lean4
import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Topology Rat

theorem mathd_algebra_215
   (S : Finset R)
   (h
   P0 : ∀ (x : R), x ∈ S ↔ (x + 3)^2 = 121) :
       k in S, k = -6 := by
   /-
   Given the set \( S \) defined by the equation \((x+3)^2 = 121\), we need to show that the sum of all elements in \( S \)
  ,→ equals \(-6\).
   1. **Identify the elements of \( S \)**:
       - The equation \((x+3)^2 = 121\) implies \( x^2 + 6x + 9 = 121 \).
       - Simplifying this equation, we get \( x^2 + 6x + 9 = 121 \), which simplifies to \( x^2 + 6x - 112 = 0 \).
       - Solving the quadratic equation \( x^2 + 6x - 112 = 0 \), we find the roots using the quadratic formula \( x =
      ,→ \frac{-b \pm \sqrt{b^2 - 4ac}}{2a} \):
         \[
         x = \frac{-6 \pm \sqrt{36 + 448}}{2} = \frac{-6 \pm \sqrt{484}}{2} = \frac{-6 \pm 22}{2}
         \]
       - This gives us two solutions:
         \[
         x = \frac{16}{2} = 8 \quad \text{and} \quad x = \frac{-28}{2} = -14
         \]
       - Therefore, the elements of \( S \) are \( 8 \) and \( -14 \).
   2. **Sum the elements of \( S \)**:
       - The sum of the elements \( 8 \) and \( -14 \) is \( 8 + (-14) = -6 \).
   Thus, the sum of all elements in \( S \) is indeed \(-6\).
   -/
   -- We need Pto show that the sum of all elements in S equals -6.
   have h1 :      k in S, k = -6 := by   -- Identify the elements of S using the given equation.
     have h2 : S = {8, -14} := by
        ext x
        simp [h0 , Set.mem_insert_iff, Set.mem_singleton_iff]
        constructor
        · intro h
          have h2 := h0 x
          have h3 : x + 3 = 11 ∨ x + 3 = -11 := by
            apply eq_or_eq_neg_of_sq_eq_sq
            linarith
          cases' h3 with h3 h3
          · exact Or.inl (by linarith)
          · exact Or.inr (by linarith)
        · intro h
          cases' h with h h
          · rw [h]
            norm_num
          · rw [h]
            norm_num
     -- Sum the elements of S.
     rw [h2 ]
     norm_num
   -- The final result is -6<|fim_middle|><|fim_middle|><|fim_middle|>(53 place holder tokens generated in total)...
   exact h1
```<|im_end|>



                                 Figure 8: Output example for dLLM-Corrector
theorem mathd_algebra_215
  (S : Finset R)
  (h0 : ∀ (x : R), x ∈ S ↔ (x + 3)^2 = 121) :
  Σ k in S, k = -6 := by
  /-
  Given the set \( S \) of all real numbers \( x \) such that \( (x + 3)^2 = 121 \), we need
      to show that the sum of all elements in \( S \) equals \(-6\).
  1. **Identify the elements of \( S \)**:
       - The equation \( (x + 3)^2 = 121 \) implies \( x + 3 = \pm 11 \).
       - Therefore, \( x + 3 = 11 \) or \( x + 3 = -11 \).
       - Solving these equations, we get \( x = 8 \) or \( x = -14 \).
  2. **Sum the elements of \( S \)**:
       - The elements of \( S \) are \( 8 \) and \( -14 \).
       - The sum of these elements is \( 8 + (-14) = -6 \).
  -/
  -- We need to show that the sum of all elements in set S is -6.
  have h1 : S = {8, -14} := by -- Identifyify the elements of S.
    ext x
    simp [h0 , Set.mem_insert_iff, Set.mem_singleton_iff]
    constructor
    · intro h
        have h2 := h0 x
        have h3 : x + 3 = 11 ∨ x + 3 = -11 := by
          apply eq_or_eq_neg_of_sq_eq_sq
          linarith
        cases' h3 with h3 h3
        · exact Or.inl (by linarith)
        · exact Or.inr (by linarith)
     · intro h
        cases' h with h h
        · rw [h]
          norm_num
        · rw [h]
          norm_num
  -- Substitute the known elements of S into the sum.
  rw [h1 ]
  -- Calculate the sum of 8 and -14.
  norm_num



        Figure 9: Example of corrector successfully corrected proof for mathd_algebra_215
theorem mathd_algebra_215_failed
  (S : Finset R)
  (h0 : ∀ (x : R), x ∈ S ↔ (x + 3)^2 = 121) :
  Σ k in S, k = -6 := by
  /-
  Same as above, omitted . . .
  -/
  -- We know that the elements of S are 8 and -14.
  have h1 : S = {8, -14} := by
    ext x
    simp only [h0 , Set.mem_insert_iff, Set.mem_singleton_iff, sq]
    constructor
    · intro h
      have h1 : x + 3 = 11 ∨ x + 3 = -11 := by
         apply or_iff_not_imp_left.mpr
         intro h1
         apply mul_left_cancel0 (sub_ne_zero_of_ne h1 )
         nlinarith
      cases' h1 with h1 h1 -- Error Tactic
      · left
         linarith
      · right
         linarith
    · intro h
      cases' h with h h h
      · rw [h]
         norm_num
      · rw [h]
         norm_num
  -- Substitute the set S with {8, -14} and calculate the sum.
  rw [h1 ]
  -- The sum of {8, -14} is 8 + (-14) = -6.
  norm_num



                   Figure 10: The problem of mathd_algebra_215 for corrector
theorem mathd_numbertheory_521
  (m n : N)
  (h0 : Even m)
  (h1 : Even n)
  (h2 : m - n = 2)
  (h3 : m * n = 288) :
  m = 18 := by
  /-
  Given two integers \( m \) and \( n \) such that \( m - n = 2 \) and \( m \times n = 288
     \), we need to show that \( m = 18 \).
  1. From \( m - n = 2 \), we can express \( m \) as \( m = n + 2 \).
  2. Substitute \( m = n + 2 \) into \( m \times n = 288 \):
      \[
      (n + 2) \times n = 288
      \]
  3. Simplify the equation:
      \[
      n^2 + 2n = 288
      \]
  4. Rearrange the equation to form a standard quadratic equation:
      \[
      n^2 + 2n - 288 = 0
      \]
  5. Solve the quadratic equation using the quadratic formula \( n = \frac{-b \pm \sqrt{b^2 -
     4ac}}{2a} \), where \( a = 1 \), \( b = 2 \), and \( c = -288 \):
      \[
      n = \frac{-2 \pm \sqrt{2^2 - 4 \cdot 1 \cdot (-288)}}{2 \cdot 1} = \frac{-2 \pm \sqrt{4 +
      1152}}{2} = \frac{-2 \pm \sqrt{1156}}{2} = \frac{-2 \pm 34}{2}
      \]
  6. This gives two solutions:
      \[
      n = \frac{32}{2} = 16 \quad \text{and} \quad n = \frac{-36}{2} = -18
      \]
  7. Since \( n \) must be positive integer, we select \( n = 16 \).
  8. Substitute \( n = 16 \) back into \( m = n + 2 \):
      \[
      m = 16 + 2 = 18
      \]
  Thus, we have shown that \( m = 18 \).
  -/
  -- From m - n = 2, express m in terms of n
  have h4 : m = n + 2 := by omega
  rw [h4 ] at h3
  -- Simplify the equation to form a quadratic equation in n
  have h5 : n = 16 := by
    -- Solve the quadratic equation n^2 + 2n - 288 = 0
    nlinarith
  -- Substitute n = 16 back into m = n + 2
  have h6 : m = 18 := by omega
  exact h6



     Figure 11: Example of corrector successfully corrected proof for mathd_numbertheory_521
theorem mathd_numbertheory_521_failed
  (m n : N)
  (h0 : Even m)
  (h1 : Even n)
  (h2 : m - n = 2)
  (h3 : m * n = 288) :
  m = 18 := by
  /-
  Same as above, omitted . . .
  -/
  -- From m - n = 2, express m in terms of n
  have h4 : m = n + 2 := by linarith -- Error Tactic
  -- Substitute m = n + 2 into m * n = 288
  rw [h4 ] at h3
  -- Simplify the equation to form a quadratic equation in n
  have h5 : n = 16 := by
    -- Solve the quadratic equation n^2 + 2n - 288 = 0
    nlinarith
  -- Substitute n = 16 back into m = n + 2
  have h6 : m = 18 := by
    rw [h5 ] -- Error Tactic
    linarith
  -- Conclude the proof by stating the final result
  exact h6



                Figure 12: The problem of mathd_numbertheory_521 for corrector
theorem imo_1983_p6
  (a b c : R)
  (h0 : 0 < a ∧ 0 < b ∧ 0 < c)
  (h1 : c < a + b)
  (h2 : b < a + c)
  (h3 : a < b + c) :
  0 ≤ a^2 * b * (a - b) + b^2 * c * (b - c) + c^2 * a * (c - a) := by
  /-
  To prove that the expression \( a^2 b(a - b) + b^2 c(b - c) + c^2 a(c - a) \) is
     non-negative, we start by analyzing the given conditions and the expression itself. The
     conditions are:
  1. \( 0 < a \), \( 0 < b \), \( 0 < c \)
  2. \( c < a + b \)
  3. \( b < a + c \)
  4. \( a < b + c \)
  We need to show that the expression \( a^2 b(a - b) + b^2 c(b - c) + c^2 a(c - a) \) is
     non-negative. This can be achieved by considering the non-negativity of the terms and
     the constraints on the variables.
  -/
  -- We need to prove that the expression is non-negative.
  -- Given the constraints on the variables, we can use the non-negativity of the terms to
     bound the expression.
  nlinarith [sq_nonneg (a - b), sq_nonneg (b - c), sq_nonneg (c - a),
    mul_nonneg (sub_nonneg.mpr h1 .le) (sub_nonneg.mpr h2 .le),
    mul_nonneg (sub_nonneg.mpr h2 .le) (sub_nonneg.mpr h3 .le),
    mul_nonneg (sub_nonneg.mpr h3 .le) (sub_nonneg.mpr h1 .le)]

theorem imo_1983_p6_failed
  (a b c : R)
  (h0 : 0 < a ∧ 0 < b ∧ 0 < c)
  (h1 : c < a + b)
  (h2 : b < a + c)
  (h3 : a < b + c) :
  0 ≤ a^2 * b * (a - b) + b^2 * c * (b - c) + c^2 * a * (c - a) := by
  /-
  Given a triangle \(ABC\) with \(AB = a\), \(BC = b\), and \(CA = c\) where \(a, b, c > 0\),
     and the conditions \(c < a + b\), \(b < a + c\), \(a < b + c\), we need to prove that:
  \[a^2 b (a - b) + b^2 c (b - c) + c^2 a (c - a) \geq 0\]
  To prove this, we use the fact that each term in the expression is a product of squares and
     differences. Since the squares of real numbers are non-negative, and the differences are
     also non-negative due to the given inequalities, the entire expression is non-negative.
  -/
  -- Use the non-negativity of squares to prove the inequality.
  nlinarith [sq_nonneg (a - b), sq_nonneg (b - c), sq_nonneg (c - a),
    mul_nonneg h0 .1.le h0 .2.1.le, mul_nonneg h0 .2.1.le h0 .2.2.le, mul_nonneg h0 .2.2.le
     h0 .1.le,
    mul_nonneg (sq_nonneg (a - b)) h0 .2.1.le, mul_nonneg (sq_nonneg (b - c)) h0 .2.2.le,
     mul_nonneg (sq_nonneg (c - a)) h0 .1.le,
    mul_nonneg (sq_nonneg (a - b)) h0 .1.le, mul_nonneg (sq_nonneg (b - c)) h0 .2.1.le,
     mul_nonneg (sq_nonneg (c - a)) h0 .2.2.le]



            Figure 13: imo_1983_p6 proved by Diffusion-Proof while the baseline fails
theorem mathd_algebra_188
  (σ : Equiv R R)
  (h : σ.1 2 = σ.2 2) :
  σ.1 (σ.1 2) = 2 := by
  /-
  Given an equivalence \( \sigma \) on the real numbers such that \( \sigma(2) = \sigma(2)
     \), we need to show that \( \sigma(\sigma(2)) = 2 \).
  1. Start with the given condition \( \sigma(2) = \sigma(2) \).
  2. Apply \( \sigma \) to both sides of the equation \( \sigma(2) = \sigma(2) \) to get \(
     \sigma(\sigma(2)) = \sigma(\sigma(2)) \).
  3. Since \( \sigma(2) = \sigma(2) \), it follows that \( \sigma(\sigma(2)) = 2 \).
  -/
  -- Start with the given condition σ(2) = σ(2)
  have h1 : σ.1 2 = σ.2 2 := h
  -- Apply σ to both sides of the equation σ(2) = σ(2) to get σ(σ(2)) = σ(σ(2))
  have h2 : σ.1 (σ.1 2) = σ.1 (σ.2 2) := by simp_all
  -- Since σ(2) = σ(2), it follows that σ(σ(2)) = 2
  have h3 : σ.1 (σ.1 2) = 2 := by simp_all
  -- The final result is σ(σ(2)) = 2
  exact h3

theorem mathd_algebra_188_failed
  (σ : Equiv R R)
  (h : σ.1 2 = σ.2 2) :
  σ.1 (σ.1 2) = 2 := by
  /-
  Given an equivalence \(\sigma\) between the real numbers, we need to show that if
     \(\sigma(1) = 2\), then \(\sigma(\sigma(1)) = 2\). By the definition of an equivalence,
     there exists a function \(\sigma\) such that \(\sigma(1) = 2\) and \(\sigma(\sigma(1)) =
     2\). We can use these properties to derive the desired equality.
  -/
  -- Using the symmetry property of the equivalence, we know that σ(2) = σ(1).
  have h1 := σ.symm_apply_left 2
  have h2 := σ.symm_apply_right 2
  -- Simplifying the expressions using the given values and the properties of the equivalence.
  simp_all [Equiv.eq_symm_apply_left]



         Figure 14: mathd_algebra_188 proved by Diffusion-Proof while the baseline fails
theorem imo_1962_p2
  (x : R)
  (h0 : 0 ≤ 3 - x)
  (h1 : 0 ≤ x + 1)
  (h2 : 1 / 2 < Real.sqrt (3 - x) - Real.sqrt (x + 1)) :
  -1 ≤ x ∧ x < 1 - Real.sqrt 31 / 8 := by
  /-
  We need to prove that for a real number \( x \) such that \( 0 \leq 3 - x \) and \( 0 \leq
      x + 1 \), the inequality \( \frac{1}{2} < \sqrt{3 - x} - \sqrt{x + 1} \) holds if and
      only if \( -1 \leq x < 1 - \frac{\sqrt{31}}{8} \).
  1. **Establish the range of \( x \)**:
       - We need to show that \( -1 \leq x < 1 - \frac{\sqrt{31}}{8} \).
  2. **Use the properties of the square root function:
       - We use the properties of the square root function to derive the inequalities.
  3. **Verify the inequalities**:
       - We verify that the inequalities hold under the given conditions.
  -/
  have h_main : -1 ≤ x ∧ x < 1 - Real.sqrt 31 / 8 := by
    constructor
    · -- Show that -1 ≤ x
    have h3 : 0 ≤ Real.sqrt (3 - x) := Real.sqrt_nonneg (3 - x)
    have h4 : 0 ≤ Real.sqrt (x + 1) := Real.sqrt_nonneg (x + 1)
    have h5 : 0 ≤ Real.sqrt 31 := Real.sqrt_nonneg 31
    have h6 : 0 ≤ Real.sqrt (3 - x) * Real.sqrt (x + 1) := by positivity
    have h7 : 0 ≤ Real.sqrt 31 * Real.sqrt (3 - x) := by positivity
     have h8 : 0 ≤ Real.sqrt 31 * Real.sqrt (x + 1) := by positivity
     have h9 : 0 ≤ Real.sqrt 31 * Real.sqrt (3 - x) * Real.sqrt (x + 1) := by positivity
     nlinarith [sq_sqrt (show 0 ≤ 3 - x by linarith), sq_sqrt (show 0 ≤ x + 1 by linarith),
        sq_sqrt (show 0 ≤ 31 by linarith), h2 ]
     · -- Show that x < 1 - Real.sqrt 31 / 8
     have h3 : 0 ≤ Real.sqrt (3 - x) := Real.sqrt_nonneg (3 - x)
     have h4 : 0 ≤ Real.sqrt (x + 1) := Real.sqrt_nonneg (x + 1)
     have h5 : 0 ≤ Real.sqrt 31 := Real.sqrt_nonneg 31
     have h6 : 0 ≤ Real.sqrt (3 - x) * Real.sqrt (x + 1) := by positivity
     have h7 : 0 ≤ Real.sqrt 31 * Real.sqrt (3 - x) := by positivity
     have h8 : 0 ≤ Real.sqrt 31 * Real.sqrt (x + 1) := by positivity
     have h9 : 0 ≤ Real.sqrt 31 * Real.sqrt (3 - x) * Real.sqrt (x + 1) := by positivity
     nlinarith [sq_sqrt (show 0 ≤ 3 - x by linarith), sq_sqrt (show 0 ≤ x + 1 by linarith),
        sq_sqrt (show 0 ≤ 31 by linarith), h2 ]
  exact h_main



                   Figure 15: Correct proof of imo_1962_p2 by Diffusion-Proof
### Detailed Proof and Analysis

#### Problem Analysis
We are given a real number \( x \) with the following constraints:
1. \( 0 \leq 3 - x \) (i.e., \( x \leq 3 \)),
2. \( 0 \leq x + 1 \) (i.e., \( x \geq -1 \)),
3. \( \frac{1}{2} < \sqrt{3 - x} - \sqrt{x + 1} \).

We need to prove that:
1. \( -1 \leq x \),
2. \( x < 1 - \frac{\sqrt{31}}{8} \).

 First, observe that the inequality \( \frac{1}{2} < \sqrt{3 - x} - \sqrt{x + 1} \) is only possible when \( x + 1 \leq 3 -
,→   x \), i.e., \( x \leq 1 \). This is because:
 - If \( x > 1 \), then \( \sqrt{3 - x} \) is real only when \( x \leq 3 \), and \( \sqrt{x + 1} \) is real only when \( x
,→ \geq -1 \). However, \( \sqrt{3 - x} - \sqrt{x + 1} \) would be negative for \( x > 1 \), because \( \sqrt{3 - x} <
,→ \sqrt{x + 1} \) (since \( 3 - x < x + 1 \), i.e., \( x > 1 \)).

But we must ensure \( x \leq 3 \) (which is already given) and \( x \geq -1 \) (which is also given). So \( x \) is in \(
,→  [-1, 3] \).

 #### Step 1: Establish \( x \leq 1 \)
 Assume for contradiction that \( x > 1 \). Then:
 1. \( \sqrt{3 - x} < \sqrt{x + 1} \) (since \( 3 - x < x + 1 \) because \( x > 1 \)),
 2. Therefore, \( \sqrt{3 - x} - \sqrt{x + 1} < 0 \),
 3. But \( \frac{1}{2} > 0 \), so \( \frac{1}{2} < \sqrt{3 - x} - \sqrt{x + 1} \) would imply \( \sqrt{3 - x} - \sqrt{x + 1}
,→ > \frac{1}{2} \), which is false because \( \sqrt{3 - x} - \sqrt{x + 1} < 0 \). Hence, \( x \leq 1 \).

But in Lean, we do not have \( x > 1 \) as a direct assumption. Instead, we use the contrapositive: if \( x > 1 \), then
,→  \( \sqrt{3 - x} - \sqrt{x + 1} \leq 0 \), which is \( \sqrt{3 - x} - \sqrt{x + 1} \leq \frac{1}{2} \), contradicting
,→  the hypothesis.

#### Step 2: Prove \( -1 \leq x \)
This is already given as \( h1 \).

#### Step 3: Prove \( x < 1 - \frac{\sqrt{31}}{8} \)
Omitted for simplicity...

#### Correct Approach
Omitted for simplicity...

#### Better Approach
Omitted for simplicity...

#### Final Simplification
Omitted for simplicity...

#### Revised Plan
Omitted for simplicity...

#### Correct Solution
Omitted for simplicity...

 #### Conclusion
 The problem reduces to verifying that \( x < 1 - \frac{\sqrt{31}}{8} \) is the correct upper bound, which is tedious but
,→ straightforward.

### Step-by-Step Abstract Plan
1. **Establish \( x \leq 1 \)**:
    - Assume for contradiction \( x > 1 \). Then \( \sqrt{3 - x} < \sqrt{x + 1} \), so \( \sqrt{3 - x} - \sqrt{x + 1} < 0
   ,→ \), violating the hypothesis. Hence, \( x \leq 1 \).
2. **Prove \( x \geq -1 \)**:
    - This is given by \( h1 \).
3. **Prove \( x < 1 - \frac{\sqrt{31}}{8} \)**:
    - Square both sides of \( \sqrt{3 - x} - \sqrt{x + 1} > \frac{1}{2} \) to find bounds on \( x \), using the fact that
   ,→ \( x \leq 1 \) and \( x \geq -1 \).

### Lean 4 Proof Sketch with `have`

```lean4
theorem imo_1962_p2
  (x : R)
  (h0 : 0 ≤ 3 - x)
  (h1 : 0 ≤ x + 1)
  (h2 : 1 / 2 < Real.sqrt (3 - x) - Real.sqrt (x + 1)) :
  -1 ≤ x ∧ x < 1 - Real.sqrt 31 / 8 := by
  have h_main_goal : -1 ≤ x ∧ x < 1 - Real.sqrt 31 / 8 := by
    sorry
  sorry
```

 ### Explanation
 The `have` statement directly encodes the main goal of the proof, which is to prove `-1 ≤ x ∧ x < 1 - Real.sqrt 31 / 8`.
,→ The actual proof of this statement is marked as `sorry` and would require detailed calculations based on the
,→ inequalities and bounds derived in the proof sketch.




                   Figure 16: Analysis process for DS-Prover-V2 in proving imo_1962_p2
theorem imo_1962_p2_failed
  (x : R)
  (h0 : 0 ≤ 3 - x)
  (h1 : 0 ≤ x + 1)
  (h2 : 1 / 2 < Real.sqrt (3 - x) - Real.sqrt (x + 1)) :
  -1 ≤ x ∧ x < 1 - Real.sqrt 31 / 8 := by
  have h_main : -1 ≤ x ∧ x < 1 - Real.sqrt 31 / 8 := by
    constructor
    · -- Prove -1 ≤ x
       linarith [h1 ]
    · -- Prove x < 1 - Real.sqrt 31 / 8
       have h3 : x < 1 - Real.sqrt 31 / 8 := by
         by_contra! h
         have h4 : x ≥ 1 - Real.sqrt 31 / 8 := by linarith
         have h5 : Real.sqrt (3 - x) - Real.sqrt (x + 1) ≤ 1 / 4 := by
           have h6 : x ≥ 1 - Real.sqrt 31 / 8 := by linarith
           have h7 : Real.sqrt (3 - x) - Real.sqrt (x + 1) ≤ 1 / 4 := by
             have h8 : 0 ≤ Real.sqrt (3 - x) := by
                apply Real.sqrt_nonneg
             have h9 : 0 ≤ Real.sqrt (x + 1) := by
                apply Real.sqrt_nonneg
             have h10 : Real.sqrt (3 - x) ≥ 0 := Real.sqrt_nonneg (3 - x)
             have h11 : Real.sqrt (x + 1) ≥ 0 := Real.sqrt_nonneg (x + 1)
             have h12 : Real.sqrt (3 - x) * Real.sqrt (x + 1) ≥ 0 := by positivity
             have h13 : Real.sqrt (3 - x) * Real.sqrt (x + 1) ≥ 0 := by positivity
             have h14 : (Real.sqrt (3 - x) - Real.sqrt (x + 1)) ^ 2 ≤ (1 / 4) ^ 2 := by
                have h15 : x ≥ 1 - Real.sqrt 31 / 8 := by linarith
                have h16 : Real.sqrt 31 ≥ 0 := Real.sqrt_nonneg _
                have h17 : Real.sqrt 31 ^ 2 = 31 := Real.sq_sqrt (by positivity)
                have h18 : x + 1 ≥ 2 - Real.sqrt 31 / 8 := by linarith
                have h19 : 3 - x ≥ 3 - (1 - Real.sqrt 31 / 8) := by linarith     -- Error
     occurs here
                have h20 : 3 - x ≥ 2 + Real.sqrt 31 / 8 := by linarith
                nlinarith [Real.sq_sqrt (show 0 ≤ 3 - x by linarith),
                  Real.sq_sqrt (show 0 ≤ x + 1 by linarith),
                  Real.sqrt_nonneg 31,
                  sq_nonneg (Real.sqrt (3 - x) - Real.sqrt (x + 1)),
                  sq_nonneg (Real.sqrt (3 - x) + Real.sqrt (x + 1) - 5 / 2),
                  sq_nonneg (Real.sqrt (3 - x) - Real.sqrt (x + 1) - 1 / 4)]
             nlinarith [Real.sqrt_nonneg (3 - x), Real.sqrt_nonneg (x + 1),
                Real.sq_sqrt (show 0 ≤ 3 - x by linarith),
                Real.sq_sqrt (show 0 ≤ x + 1 by linarith)]
           exact h7
         linarith
       exact h3
  exact h_main



                  Figure 17: Failed proof of imo_1962_p2 by DeepSeek-Prover-V2
