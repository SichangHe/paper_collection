                                                         Theorem Prover as a Judge for Synthetic Data Generation

                                                          Joshua Ong Jun Leang Giwon Hong Wenda Li Shay B. Cohen
                                                                  School of Informatics, The University of Edinburgh
                                                                    {jong2, giwon.hong, wenda.li, scohen}@ed.ac.uk




                                                                   Abstract                                              Find the area of a circle with radius 2

                                                                                                          1. The formula for area is                1. The formula for area is
                                                 The demand for synthetic data in mathemati-
arXiv:2502.13137v2 [cs.AI] 16 Jan 2026




                                                 cal reasoning has increased due to its poten-            2. By performing substitution:            2. By performing substitution:

                                                 tial to enhance the mathematical capabilities            3. The answer is                          3. The answer is
                                                 of large language models (LLMs). However,                                         Final Answer:
                                                 ensuring the validity of intermediate reason-
                                                 ing steps remains a significant challenge, af-
                                                                                                     Figure 1: An example of potential flawed reasoning
                                                 fecting data quality. While formal verification
                                                                                                     occurs when the correct answer is achieved despite con-
                                                 via theorem provers effectively validates LLM
                                                                                                     taining incorrect logical steps.
                                                 reasoning, the autoformalisation of mathemati-
                                                 cal proofs remains error-prone. We introduce
                                                 iterative autoformalisation, an approach that
                                                                                                     et al., 2022; Kojima et al., 2022). Although these
                                                 iteratively refines theorem prover formalisation
                                                 to mitigate errors, thereby increasing the ex-
                                                                                                     methods have achieved success on benchmarks like
                                                 ecution rate on the Lean prover from 60% to         GSM8K (Cobbe et al., 2021), they are prone to sig-
                                                 87%. Building upon that, we introduce The-          nificant flaws. Specifically, LLM-generated CoT
                                                 orem Prover as a Judge (TP-as-a-Judge), a           reasoning steps may often include errors, leading
                                                 method that makes use of theorem prover for-        to incorrect solutions even when the final answer
                                                 malisation to rigorously assess LLM interme-        appears plausible (Leang et al., 2024).
                                                 diate reasoning, effectively integrating autofor-      To address these flaws, coding-based tools such
                                                 malisation with synthetic data generation. Fi-
                                                                                                     as Python (Chen et al., 2022; Lyu et al., 2023)
                                                 nally, we present Reinforcement Learning from
                                                 Theorem Prover Feedback (RLTPF), a frame-           and SMT Solvers like the Z3 solver (De Moura
                                                 work that replaces human annotation with theo-      and Bjørner, 2008) have been widely used to im-
                                                 rem prover feedback in Reinforcement Learn-         prove reasoning capabilities, as well as theorem
                                                 ing from Human Feedback (RLHF). Across              provers such as Lean (De Moura et al., 2015) and
                                                 multiple LLMs, applying TP-as-a-Judge and           Isabelle (Paulson, 1994). These systems provide
                                                 RLTPF improves benchmarks with only 3,508           formal verification on the logical validity of LLM
                                                 samples, achieving 5.56% accuracy gain on
                                                                                                     reasoning steps. Nevertheless, they are not without
                                                 Mistral-7B for MultiArith, 6.00% on Llama-2-
                                                 7B for SVAMP, and 3.55% on Llama-3.1-8B             challenges; autoformalisation errors often lead to
                                                 for AQUA.1                                          execution failures during theorem prover verifica-
                                                                                                     tion in complex tasks (Xu et al., 2024; Quan et al.,
                                         1       Introduction                                        2024; Gou et al., 2024a; Olausson et al., 2023),
                                                                                                     including Python’s struggles with Olympiad-level
                                         Recent studies have shown that large language               problems (Leang et al., 2024).
                                         models (LLMs) are increasingly capable of tack-                Parallel to these strategies, synthetic data gener-
                                         ling mathematical problems (Dubey et al., 2024;             ation emerged as a promising approach to enhance
                                         Jaech et al., 2024; Yang et al., 2024a; Guo et al.,         mathematical reasoning (Xin et al., 2024; Lu et al.,
                                         2025). Techniques such as Chain of Thought (CoT)            2024b). A commonly used verification method
                                         aim to enhance the reasoning process by break-              is LLM-as-a-Judge (Zheng et al., 2023; Stephan
                                         ing complex problems into intermediate steps (Wei           et al., 2024; Saha et al., 2025), wherein LLMs eval-
                                             1
                                             Code is available            at   https://github.com/   uate and generate reasoning data. However, this
                                         joshuaongg21/RLTPF.                                         method often introduces bias (Guan et al., 2025).
       Theorem Prover as a Judge            LLM Data Generation
                                                                                  LLM(A) Generated Answer
        LLM Data Generation                 LLM Generated Question
                                                                                 LLM (B) Generated Answer



     Theorem Prover Verification                  Theorem Prover Verification
                                                                                                  Iterative Autoformalisation
                                            Question                  Answer                                                              Verified
                                                                                                    Incorrect Formalisation
                                            Formalisation             Formalisation
                                                                                                                                          False
                                                                                                         Error Output
        Reinforcement Learning
     from Theorem Prover Feedback
                                                        CoMAT          Autoformalisation         Auto-Informalisation           Alignment Check




                                            Reinforcement Learning from Theorem Prover Feedback

      SFT         DPO         Dispose        LLM                      SFT                  DPO                  Tuned-LLM




Figure 2: Overview of TP-as-a-Judge, comprising LLM data generation, theorem prover verification, and RLTPF.


Generating labeled training data for step-by-step               We then propose Reinforcement Learning from The-
reasoning remains resource-intensive as well, re-               orem Prover Feedback (RLTPF), a novel approach
quiring substantial human effort for annotation, and            in which the theorem prover replaces human an-
automatic annotation methods have shown limited                 notators by providing formalised feedback. By
success, as noisy reward scores often impede their              applying TP-as-a-Judge and RLTPF, we achieve
efficacy (Luo et al., 2024; Wang et al., 2024c; Chen            competitive performance in GSM8K and AIME
et al., 2024). Recently, iterative techniques like              2024 datasets compared to models fine-tuned on
Monte Carlo Tree Search (MCTS) have been ap-                    larger datasets. This demonstrates the significance
plied to refine reasoning steps and achieve accurate            of intermediate reasoning in data quality and en-
solutions (Guan et al., 2025; Park et al., 2024).               hances the data efficiency of model training.
While MCTS enhances reasoning quality, it is com-
putationally expensive due to extensive rollouts,               2      Theorem Prover as a Judge
limiting its scalability for large-scale applications.
                                                                As shown in Figure 2, TP-as-a-Judge consists of
   To overcome these challenges, we first address               two key stages: LLM Data Generation, where
execution failures in autoformalisation by propos-              LLMs generate questions and answers; Theorem
ing iterative autoformalisation, a method that inte-            Prover Verification, where a theorem prover as-
grates autoformalisation errors as feedback, thereby            sesses the validity of the model’s reasoning on the
ensuring that each intermediate reasoning step is               generated data and proceeds to RLTPF, leveraging
verified. Specifically, we use the Lean prover as our           verification results to refine the model through Su-
autoformalisation verifier. Unlike Python-based ap-             pervised Fine-Tuning (SFT) and Direct Preference
proaches (Bi et al., 2024), which refine execution              Optimization (DPO; Rafailov et al. 2023).
traces, iterative autoformalisation validates indi-
vidual proof tactics, theorems, and logical steps               2.1         LLM Data Generation
within the formal system. As problem complexity                 Building on the work of Balepur et al. (2024), we
increases, additional iterations are required for ac-           apply the Reverse Question-Answering method to
curate autoformalisation. Simply discarding ques-               the mathematical domain for constructing our ini-
tions after a single failed attempt risks introducing           tial synthetic datasets. This technique involves pro-
biases toward simpler problems (Lu et al., 2024a).              viding the model with a few example solutions
   Building on this foundation, we introduce The-               and instructing it to generate corresponding ques-
orem Prover as a Judge (TP-as-a-Judge), a novel                 tions that align with those solutions. The datasets
framework for generating synthetic data in math-                we use are sourced from two primary sources:
ematical reasoning tasks. TP-as-a-Judge is inte-                the GSM8K dataset (Cobbe et al., 2021) and the
grated with a theorem prover, leveraging its step-              MATH dataset (Hendrycks et al., 2021). This ap-
by-step verification to ensure logical correctness.             proach enables us to cover a broad array of math-
      Question: A rational function is given by                       . Determine the number of veritical asymptotes of the graph of this function

                                                                                                      Lean Theorem Prover Verifier
      Step 1: Recall the condition of vertical asymptotes
                                                                                        -- Generate a <tactic> for verification              Step 2
      Step 2: Factorise the denominator :
      The denominator is              . To factorize ... (skip) ...                     theorem factorize_denominator : ∀ x : ℝ,
      So the denominator is zero when         or           .                               denominator x = x^2 - 4 * x - 12 := by rfl
                                                                                           _ = (x - 6) * (x + 2) := by ring
      Step 3: Factorize the numerator
                                                                                        -- Verify the result                            Final Output
      Step 4: Check for cancellations
                                                                                        def verification_result : String :=
      Step 5: Count the vertical asymptotes: ... (skip) ...
                                                                                          if number_of_vertical_asymptotes = 2 then "verified"
      Final Output: there are 2 vertical asymptotes
                                                                                          #eval verification_result -- Outputs "verified"


Figure 3: An example of answer formalisation, where Lean prover verifies intermediate reasoning steps. For
simplicity, this is an abbreviation of the complete formalisation.


ematical topics, spanning domains such as simple                              This is followed by the final phase (s4 ), Alignment
problem solving, algebra, number theory, geometry,                            Check, which uses a second gpt-4o verification
counting and probability, and calculus. In our setup,                         step to ensure alignment between s0 and s3 . This
we primarily focus on three core areas: problem                               serves as a consistency check, confirming the cor-
solving, algebra, and counting and probability.                               rectness of the autoformalisation process.
                                                                                 Let Q denote the set of all generated questions.
2.2      Theorem Prover Verification                                          The autoformalisation function s maps each ques-
After generating the samples, we use gpt-4o and                               tion q ∈ Q to its formal representation s(q):
chatgpt-4o-latest (Hurst et al., 2024) as two
primary models to generate solutions for the syn-                                             s : Q → S,           s(q) = s4 (q),
thetic questions. Subsequently, gpt-4o is used
                                                                              where S is the set of successfully validated ques-
for autoformalisation, after which the outputs are
                                                                              tions and answers, and s4 (q) is the final represen-
passed to the theorem prover for validation. The
                                                                              tation after the four-phase process. Questions that
Theorem Prover Verification process is divided into
                                                                              do not fulfil the requirements, where s(q) ̸= s4 (q),
two stages: Question and Answer formalisation. A
                                                                              are flagged as logically inconsistent or poorly for-
detailed example of the process is shown in Ap-
                                                                              malised, and excluded from answer formalisation.
pendix K.
                                                                              2.2.2 Answer Formalisation
2.2.1      Question Formalisation
                                                                              During the answer formalisation stage, the model
In the question formalisation stage, each question is                         transforms the model reasoning a(q) for each valid
formalised and verified by a theorem prover, serv-                            question q ∈ Qvalid into a formal representation:
ing as a filter for questions lacking clarity.
   This process follows a four-phase approach,                                                  a′ (q) = Formalise(a(q)).
starting with the original question (s0 ). In the first
phase (s1 ), we apply the CoMAT method (Leang                                 It then verifies each step of the reasoning a′ (q) us-
et al., 2024) to convert s0 into a symbolic repre-                            ing a theorem prover, confirming the validity of
sentation. The second phase (s2 ) involves autofor-                           each step. For instance, the model may perform
malisation, where the symbolic representation is                              calculations or generate specific tactics to justify
formalised and verified using a theorem prover.                               its progression; these tactics are formally validated
   To address the formalisation errors raised                                 by the theorem prover to ensure adherence to math-
by Yang et al. (2024b), which highlight the inher-                            ematical principles, as shown in Figure 3.
ent difficulty of question autoformalisation due to                              Let {a′i (q)} denote the sequence of proof steps
the absence of definitive metrics for assessing cor-                          in a′ (q). The verification process yields one of
rectness, we introduce the third phase (s3 ), Auto-                           three outcomes for each answer, a(q): (i) Verified:
Informalisation, where the formalised statement is                            if all steps are validated by the theorem prover. (ii)
translated back into natural language via gpt-4o.                             False: if any step is refuted by the theorem prover.
      LLM (A)            LLM (B)             Action           Algorithm 1 Iterative Autoformalisation
                                                               1: Input: Answer a, Verifier P
      Verified (1)      Verified (1)          SFT
                                                               2: Derive formal proof A(a) from a
      Verified (1)        False (0)           DPO              3: Initialize retry counter r ← 0, maximum re-
      False (0)           False (0)         Dispose               tries R ← 5
                                                               4: Initialize result ← unknown, error ← None
Table 1: If both model responses are verified as correct,      5: while r < R do
they are incorporated into the training process via SFT.       6:     for each step Ti ∈ A(a) do
Conversely, if one response is verified as correct while       7:          Set s ← P (Ti )
the other is rejected, the dataset is processed using DPO.     8:          if s = verified then
Detailed analyses for this selection are discussed in §4.4.    9:               result ← verified
                                                              10:               break
(iii) error: if the autoformalisation failed to execute       11:          else if s = false then
through the theorem prover. Formally:                         12:               result ← false
                                                              13:               break
                                                             14:          else
        1
                      if ∀i, TP(a′i (q)) = verified,         15:               error ← s
  A(q) = 0             if ∃i, TP(a′i (q)) = false,            16:               Transmit error and formal proof
        
        
         error         if ∃i, TP(a′i (q)) = error.                A(a) to the model for refinement
                                                              17:               break
   Any answer resulting in false is either removed            18:          end if
from the synthetic dataset or kept for RLTPF, as              19:     end for
detailed in Table 1, whereas the error will undergo           20:     if result ∈ {verified, false} then
iterative autoformalisation for further refinement.           21:          break
By formalising both questions and answers and rig-            22:     end if
orously verifying them, we ensure that the overall            23:     r ←r+1              ▷ Increment retry count
reasoning chain complies with mathematical logic              24:     Refine A(a) using feedback from error
and standards, thus enhancing the dataset quality.            25: end while
                                                              26: Output: result ∈ {verified, false, error}
2.2.3 Iterative Autoformalisation
We propose iterative autoformalisation, an ap-
proach in which the model learns from its errors              RLTPF replaces human evaluators with a theorem
during the autoformalisation process (Algorithm 1).           prover, which verifies each formalised reasoning
Our approach concentrates on mathematical aut-                step. In our framework, the theorem prover cat-
oformalisation, correcting each individual step,              egorises training data based on verification out-
prompting the model to revise and reverify the                comes, ensuring the model learns from both val-
autoformalisation using theorem prover. This it-              idated reasoning patterns and cases requiring re-
erative process reflects the nature of formalisation,         finement. Specifically, when both the LLMs gen-
as even human experts require multiple attempts to            erate answers verified by the theorem prover, the
correctly formalise complex problems. The model               corresponding dataset is used for Supervised Fine-
may need to experiment with different definitions,            Tuning (SFT). When one LLM produces a correct
refine assumptions, or attempt partial proofs to              response while the other generates an incorrect one,
identify missing conditions. Iterative refinement             the paired dataset is used for Direct Preference Op-
improves the execution rate of the Lean prover                timisation (DPO). The model is then trained with
formalisation from 60% to 87% after up to five                SFT on verified data before undergoing further op-
iterations.                                                   timisation with DPO using the paired dataset. De-
                                                              tails for the dataset allocation are shown in Table 1.
2.3    Reinforcement Learning from Theorem
       Prover Feedback (RLTPF)
                                                              3   Experimental Setup
In conventional RLHF, human evaluators provide
structured feedback to help the model distinguish             SIMQA Our initial training dataset, Synthetic
between valid and invalid reasoning. By contrast,             Induced Mathematical Question Answering
(SIMQA) comprises 3,508 samples, of which              fine-tuned on over 860k mathematical problem-
1,876 are synthetically generated from GSM8K           solution pairs using the DeepSeek-Math-7B-Base
and 1,632 from MATH. Details on the dataset            model; OpenMath2 (Toshniwal et al., 2024),
breakdown and configurations are in Appendix A,        fine-tuned Llama-3.1-8B-Base with a significantly
and few-shot examples in Appendix H.                   larger corpus of 14M problem-solution pairs; and
                                                       Mathstral-7B (The Mistral AI Team, 2024).
Evaluation Datasets. We evaluate on a di-
verse set of mathematical benchmarks, includ-          Evaluation Metrics We report Pass@1 accu-
ing SVAMP (Patel et al., 2021), GSM8K (Cobbe           racy as the primary evaluation metric for all base-
et al., 2021), MultiArith (Roy and Roth, 2015)         lines. The answers were parsed based on an exact
GSMSymbolic-p1 (Mirzadeh et al., 2024), MATH-          match. For answers where exact matching failed,
500 (Hendrycks et al., 2021), AQUA (Ling et al.,       we parsed the numerical values from the model’s fi-
2017), AIME (2024), OlympiadBench (He et al.,          nal response and compared them against the ground
2024) datasets. Due to computational constraints,      truth. For the MATH-500, AIME, and Olympiad-
we evaluate only the first 500 samples from            Bench datasets, we adopt a similar evaluation strat-
GSMSymbolic-p1.                                        egy to Leang et al. (2024). We use gpt-4o-mini to
                                                       assess answer alignment by comparing the last two
Base Models and Setup. To demonstrate the ef-          output sentences to the ground truth, generating a
fectiveness and generalisability of our approach,      numerical score (1 or 0) without revealing the ques-
we apply it across a variety of LLMs, including        tion. Further details can be found in Appendix D.
Llama-2-7b-chat-hf (Touvron et al., 2023), Llama-
3.2-3B-Instruct, Llama-3.1-8B-Instruct (Dubey          4     Experimental Results
et al., 2024), OLMo-2-1124-7B-Instruct (OLMo           4.1    Main Results
et al., 2025), and Mistral-7B-Instruct-v0.3 (Jiang
                                                       Table 2 compares the performance of TP-as-a-
et al., 2023a). These models were selected as rep-
                                                       Judge, CoT prompting, and the standard baseline
resentative general-purpose single-task language
                                                       across various mathematical benchmarks. TP-as-a-
models (SLMs) without specific specialisation in
                                                       Judge consistently outperforms traditional CoT on
mathematical reasoning tasks. As part of our train-
                                                       most datasets, demonstrating the effectiveness of
ing pipeline, we use Low-Rank Adaptation (LoRA;
                                                       the synthetic data generation method.
Hu et al. 2022) as our fine-tuning baseline to im-
                                                          Among Llama models (Llama-2-7B, Llama-3.2-
prove computational efficiency. Details on hyper-
                                                       3B, and Llama-3.1-8B), we observe that while
parameters are provided in Appendix B.
                                                       CoT improves accuracy over the standard base-
Baselines Since the model focuses on mathemati-        line, TP-as-a-Judge further enhances performance.
cal reasoning, we compare it against three baselines   In particular, Llama-3.1-8B shows a notable in-
using the same decoding strategy: greedy decod-        crease in GSM-Symbolic (55.60% → 58.20%) and
ing, where the most probable next token is selected.   AQUA (53.54% → 57.09%). Llama-2-7B exhibits
The baselines include: (1) Standard Prompting,         substantial improvements in MultiArith (39.44%
which follows a similar prompt to that in the Holis-   → 59.44%), SVAMP (38.00% → 44.00%), and
tic Evaluation of Language Models (HELM; Liang         GSM8K (10.33% → 16.70%), while Llama-3.2-3B
et al., 2022), where the model is instructed to pro-   demonstrates an improvement in GSM-Symbolic
vide the answer without any reasoning; (2) CoT         (55.80% → 59.60%). Our empirical findings sug-
Prompting (Wei et al., 2022), and (3) Model Train-     gest that the incremental gains from additional
ing, which involves performing RLTPF training          model training diminish as models progress from
on 3,508 samples from the synthetic dataset. The       Llama-2 to Llama-3.1 to Llama-3.2. Neverthe-
prompts for (3) follow the same template as those      less, these results indicate that synthetic data de-
in (2) to ensure a fair comparison.                    rived solely from GSM8K and MATH generalises
                                                       well across a range of benchmarks. Even on
Benchmarks We compare GSM8K and                        AQUA, multiple-choice task performance is en-
AIME dataset across existing models, including         hanced through the inclusion of synthetic data.
DeepSeekMath (Shao et al., 2024), fine-tuned              For Mistral-7B and OLMo-2-7B, we observe
on an extensive dataset comprising 120B mathe-         consistent improvements across most benchmarks.
matical tokens; NuminaMath (Li et al., 2024a),         In particular, OLMo-2-7B demonstrates progress
 Model ↓ Tasks →   MultiArith   SVAMP     GSM8K     GSM-Symbolic    AQUA     MATH-500   AIME 2024   OlympiadBench
 Llama-3.1-8b         39.44%     65.67%   11.54%            1.80%   22.83%     13.00%      10.00%          3.12%
 + CoT                97.78%     88.33%   82.38%           55.60%   53.54%     44.00%      10.00%         20.03%
 + RLTPF              97.78%     88.67%   83.75%           58.20%   57.09%     46.00%      10.00%         19.88%
 Llama-3.2-3b         30.00%     54.67%    8.58%            1.60%    8.80%     11.04%       3.33%         11.04%
 + CoT                97.78%     80.67%   75.93%           55.80%   42.60%     42.60%      10.00%         12.46%
 + RLTPF              98.33%     81.67%   77.22%           59.60%   45.00%     45.00%      13.33%         14.24%
 Llama-2-7b           30.00%     54.67%    8.58%            1.60%    8.27%      8.80%       0.00%          4.15%
 + CoT                39.44%     38.00%   10.33%           10.60%   18.11%      2.60%       0.00%          1.93%
 + RLTPF              59.44%     44.00%   16.70%           13.20%   18.50%      3.20%       0.00%          1.93%
 Mistral-7b           15.00%     48.67%    8.20%            3.40%   20.08%      6.40%      10.00%          2.97%
 + CoT                62.22%     51.67%   37.36%           28.40%   27.95%     16.20%      10.00%          2.08%
 + RLTPF              67.78%     52.00%   36.52%           31.60%   27.95%     15.00%      10.00%          2.23%
 OLMo-2-7b            27.78%     52.00%   11.92%            5.00%   20.08%     10.80%       0.00%          3.71%
 + CoT                98.33%     81.33%   79.73%           58.40%   40.94%     33.20%       3.33%         11.28%
 + RLTPF              98.33%     81.67%   80.18%           59.20%   42.13%     33.20%       6.67%         11.57%

Table 2: Performance comparison of models across various mathematical reasoning benchmarks. We evaluate
TP-as-a-Judge augmented with RLTPF against direct answering and CoT-based methods.


 Model                          GSM8K AIME 2024              substantial mathematical datasets. Llama-3.1-8B,
                                                             when augmented with RLTPF, has outperformed
 Llama-3.2-3b                    8.58%         3.33%
 + CoT                          75.93%        10.00%         most of the models, although it remains slightly be-
 + RLTPF                        77.22%        13.33%         hind OpenMath-2 on GSM8K. Meanwhile, Llama-
                                                             3.2-3B with RLTPF has achieved the highest per-
 Llama-3.1-8b                   11.54%         10.00%
                                                             formance on the AIME 2024 benchmark. These
 + CoT                          82.38%         10.00%
 + RLTPF                        83.75%         10.00%        results suggest that leveraging RLTPF and TP-as-a-
                                                             Judge can provide performance gains comparable
 Mathstral-7B                   77.10%             6.67%     to large-scale fine-tuning while maintaining com-
 NuminaMath                     79.30%             0.00%
                                                             putational efficiency, showcasing the importance of
 DeepSeekMath-Instruct          82.90%               N/A
 OpenMath-2                     84.20%             6.67%     high-quality intermediate reasoning steps on syn-
                                                             thetic data. The results are summarised in Table 3.
Table 3: Comparison of TP-as-a-Judge against existing           Overall, our results demonstrate the potential
benchmarks. ‘N/A’ signifies that the model results are       of TP-as-a-Judge in ensuring data quality and the
not publicly available.                                      importance of intermediate reasoning in mathemat-
                                                             ical problem solving. Although SIMQA comprises
                                                             only 3,508 samples, it outperforms models fine-
across all evaluated tasks, whereas Mistral-7B ex-           tuned with larger samples of standard synthetic
hibits a 0.84% decrease on GSM8K and 1.2% de-                data, highlighting the significance of verifying in-
crease on MATH; however, it achieves an improve-             termediate reasoning. Increasing the dataset size
ment of 3.2% on GSM-Symbolic.                                could potentially improve model performance.
   Generally, our observations reveal a substantial
gap between the standard baseline and CoT reason-            4.2    Analysis
ing, thereby demonstrating the importance of inter-          We conduct an analysis on the effectiveness of TP-
mediate reasoning in mathematical tasks. Statistics          as-a-Judge in verifying model solution. We anal-
and consistency check can referred to Appendix C.            yse the effectiveness of TP-as-a-Judge in verifying
Older models, such as Mistral-7B and Llama-2-7B,             model solutions by extracting 2,000 samples from
struggle on the MATH-500 dataset, while more                 the SIMQA dataset, using GSM8K as the few-shot
advanced models exhibit stronger reasoning capa-             example. Our analysis revealed that 30% of these
bilities and achieve higher accuracy.                        samples failed during the question formalisation
   With RLTPF applied to a dataset of only 3,508             stage, potentially classified as poor question clar-
samples, TP-as-a-Judge achieves a competitive                ity. Among the remaining 70%, approximately 5%
benchmark against the other synthetic data gen-              exhibited execution errors from the Lean prover
eration models, all of which were fine-tuned with            during the answer formalisation stage (Figure 4).
                  40.8%
                                                                        Pred. →        TP-as-a-Judge        o1-mini
                                                                         Act. ↓        1         0          1      0
                                    Question Formalisation Error
                                    Answer Formalisation Error
      23.1%                         OK (verified)                           1          32         3         25      7
                                    OK (false)
          5.4%
                                                                            0           5        14         12     10
                  30.8%

                                                                   Table 4: Comparison of confusion matrices for
                                                                   TP-as-a-Judge with gpt-4o formalisation, and
Figure 4: Analysis of synthetic data generation, includ-
                                                                   o1-mini as LLM-as-the-judge, where Act represents
ing Question and Formalisation Error. OK represents a
                                                                   Actual Results, Pred represents Predicted Results, 1 rep-
successful verification, classifying into verified or false.
                                                                   resents verified, and 0 represents false.


   We then randomly sampled 54 successfully exe-                             Model              Accuracy (%)
cuted cases for manual annotation and evaluate the                                          GSM8K
performance of gpt-4o, o1, and o3-mini on these
                                                                             gpt-4o                        94.46
annotated questions. As shown in Table 5, while
                                                                             o1-mini                       94.80
the models achieve high accuracy on the GSM8K
dataset, their performance declines significantly                                    GSM8K-Synthetic
when answering synthetic questions. This high-                               gpt-4o                        51.85
lights a significant gap in the models’ ability to                           o3-mini                       64.00
handle self-generated questions, demonstrating the                           o1                            67.00
importance of theorem prover for verification, and
the potential gap of existing LLMs in mathemati-                   Table 5: Accuracy of gpt models on GSM8K and
cal reasoning. Details of autoformalisation break-                 GSM8K-SIMQA dataset.
down can be referred to Appendix G, and detailed
examples of manual annotations can be found in                     cessful autoformalisations that require iterative aut-
Appendix I.                                                        oformalisation are achieved by the third iteration,
   To further investigate, we examine a fundamen-                  indicating that multiple rounds of error correction
tal question: How effective is theorem prover for-                 significantly benefit the model. In a minority of
malisation in verifying reasoning chains? As                       cases, more than three iterations are necessary to
shown in Table 4, TP-as-a-Judge achieves an F1                     reach a correct autoformalisation. Instances re-
score of 0.87 and a Recall of 0.91 in correctly ver-               quiring more iterations often fail, even after seven
ifying reasoning steps. In contrast, using o1-mini                 attempts. By leveraging verification-based self-
as an LLM-based judge without a theorem prover,                    correction, the model improves its autoformalisa-
while achieving 94.80% accuracy on GSM8K, re-                      tion through an iterative cycle. This demonstrates
sults in a significantly lower F1 score of 0.72 and                the importance of structured feedback in enhanc-
a Recall of 0.78. This leads to a 2x increase in                   ing the robustness of formal proofs, ensuring that
False Positives, potentially degrading dataset qual-               logical errors are systematically identified and re-
ity. These results demonstrate the robustness of                   solved.
iterative autoformalisation within the Lean prover                    To further analyse the robustness of iterative
and highlight TP-as-a-Judge’s effectiveness in vali-               autoformalisation, we manually inspected ten ran-
dating intermediate reasoning steps.                               domly sampled examples. We observed that errors
                                                                   were typically caused by an incorrect theorem or
4.3    Robustness to Iterative Autoformalisation
                                                                   tactic generated by Lean, or by the model produc-
Given the strong performance of iterative autofor-                 ing invalid Lean syntax, and generally required
malisation, we explore another key aspect: How                     one or two further iterations to rectify. Feedback
many iterations are required for the model to im-                  from Lean via iterative autoformalisation allows
prove its autoformalisation? To do this, we analyse                the model to refine both the syntax and the choice
356 samples from the dataset. We find that approxi-                of theorem, thereby correctly verifying each rea-
mately 40% require iterative refinement to enhance                 soning step. This potentially enables the model to
formalisation (Appendix E). In addition, most suc-                 analyse reasoning in terms of intermediate steps
      Iteration       Average Sequence Length             Model                              GSM8K (Acc.)
      1                                      731.2        Llama-3.1-8b                                11.54%
      2                                      869.1          + CoT                                     82.38%
      3                                      937.6
                                                                    Supervised Fine-Tuning (SFT)
      4                                     1134.6
      5                                     1343.0        All Instances                               82.23%
                                                          Only Rejected Instances                     80.87%
      Table 6: Average sequence length per iteration.     Only Verified Instances                     81.55%
                                                                                RLTPF
rather than as a whole, and to verify the intermedi-      SFT (All) + RLTPF                           79.60%
ate steps of complex proofs accurately.                   SFT (Only Verified) + RLTPF                 83.75%
   Based on Table 6, we can conclude that the num-
ber of iterations exhibits a strong positive corre-      Table 7: Performance comparison of different training
                                                         strategies on SIMQA with Llama-3.1-8B model. In SFT,
lation with sequence length (measured in tokens),
                                                         the dataset used for training is classified based on the
since more complex reasoning naturally produces          theorem prover’s verification results §2.2.
longer token sequences (Muennighoff et al., 2025).
As the iteration count increases, the method ac-
commodates increasingly intricate reasoning cases,       Gou et al., 2024b; Luo et al., 2024; Yu et al.,
which may mitigate bias towards simpler instances.       2024; Tang et al., 2024), such as NuminaMath (Li
                                                         et al., 2024a) and OpenMathInstruct (Toshniwal
4.4       Effectiveness of RLTPF in TP-as-a-Judge        et al., 2024). Nevertheless, even solvable prob-
We conduct a more detailed analysis to determine         lems may contain error-prone intermediate reason-
which components of the proposed framework con-          ing steps, which are inherently challenging to de-
tribute to performance improvement and to evaluate       tect. Although rejection sampling methods (Yuan
the effectiveness of theorem prover in this process.     et al., 2023; Brown et al., 2024) can improve
   As shown in Table 7, performing SFT using             data quality by filtering out less reliable outputs,
all possible training instances achieves the high-       they do not guarantee the correctness of interme-
est accuracy among SFT, as it uses a large num-          diate steps. Consequently, the benefits of scaling
ber of samples. Meanwhile, using only rejected           CoT datasets exhibit diminishing returns, with per-
instances results in lower accuracy compared to          formance gains nearing saturation. For instance,
using only verified instances. This implies that         OpenMathInstruct reported only a 3.9% improve-
the Theorem Prover provides an effective inductive       ment on the MATH dataset despite an 8× increase
bias for learning, but SFT fails to fully leverage it.   in dataset size. Recently, STaR (Zelikman et al.,
   To address this issue, the proposed RLTPF (§2.3)      2022), Lean-STaR (Lin et al., 2024) and rStar-
enables more efficient training by assigning differ-     Math (Guan et al., 2025), have been proposed.
ent preferences to verified instances and rejected in-   These approaches rely on generating multiple roll-
stances, achieving the highest accuracy among the        outs and trajectories for verification and synthesis.
tested approaches. Interestingly, SFT with all in-
                                                         Theorem Proving and Autoformalisation Mod-
stances showed degraded performance when com-
                                                         ern formal mathematics environments typically
bined with RLTPF. This is likely due to a conflict
                                                         centre on theorem provers, such as Lean (Jiang
between SFT, which was trained with a focus on
                                                         et al., 2024; Lin et al., 2024), Isabelle (Zhou et al.,
all instances including rejected ones, and RLTPF,
                                                         2024; Wang et al., 2024a) and Coq (Huet et al.,
which learns preferences between rejected and ver-
                                                         1997). These systems have been widely used to
ified instances. This finding validates the dataset
                                                         verify complex mathematical results, including the
allocation criteria established in Table 1 and §2.3.
                                                         Liquid Tensor Experiment (Castelvecchi, 2021),
                                                         the formalisation of the PER conjecture (Gowers
5     Related Work
                                                         et al., 2023), and efforts to formalise graduate-level
Math Data Synthesis Advancements in mathe-               number theory (Eberl et al., 2024). The Draft-
matical reasoning for LLMs increasingly rely on          Sketch-Prove (Jiang et al., 2023b) approach en-
high-quality CoT datasets, often distilled from fron-    hances language models’ formal proving abilities
tier models (Guo et al., 2025; Wang et al., 2024b;       by generating informal proofs, translating them
into formal sketches, and completing them with           ity of synthetic data and preventing the creation
symbolic tools.                                          of more advanced mathematical questions. Next,
                                                         computational constraints limit scalability, partic-
6   Conclusion                                           ularly for models exceeding 8 billion parameters,
                                                         requiring substantial resources for large-scale veri-
We propose Theorem Prover as a Judge (TP-as-a-
                                                         fication and training. Finally, the iterative nature of
Judge), a framework for synthetic data generation
                                                         formalisation incurs a high computational cost, as
that ensures the correctness of intermediate rea-
                                                         multiple refinement cycles are needed to ensure cor-
soning steps. TP-as-a-Judge comprises three main
                                                         rect execution. Addressing these challenges would
stages: synthetic data generation, theorem prover
                                                         enable more efficient and scalable synthetic data
verification, and Reinforcement Learning from the-
                                                         generation.
orem Prover Feedback (RLTPF). Synthetic data
generation includes question and answer formalisa-       Acknowledgements
tion, a process that is inherently challenging and of-
ten leads to execution errors in the theorem prover.     We thank the reviewers for their useful feedback
To address this, we introduce iterative autoformali-     and comments. We also thank Pasquale Min-
sation, which incrementally refines the model’s aut-     ervini, Yifu Qiu, Aryo Pradipta Gema, Xuanli He,
oformalisation until a correct execution is achieved.    Christina Du, Rohit Saxena, Zhaowei Wang, Isaac
We mitigate question formalisation errors by in-         Ong and Dongwei Jiang for their constructive feed-
corporating Auto-Informalisation and Alignment           back and insights. We appreciate the computational
Check, reducing autoformalisation errors within the      resources provided by the Edinburgh International
synthetic dataset generation and improving verifi-       Data Facility (EIDF) and the Data-Driven Inno-
cation consistency. RLTPF involves TP-as-a-Judge         vation Programme at the University of Edinburgh.
separating the dataset into two subsets: one for SFT     We thank netmind.AI for an additional contribution
and another for DPO. The model is then trained           of computational resources.
sequentially through SFT followed by DPO. TP-
as-a-Judge with RLTPF enhances model accuracy
using only 3,508 samples, achieving results compa-       References
rable to those obtained with large samples. Despite      Nishant Balepur, Feng Gu, Abhilasha Ravichander, Shi
its simplicity, TP-as-a-Judge presents a promising         Feng, Jordan Boyd-Graber, and Rachel Rudinger.
direction using autoformalisation for improving            2024. Reverse question answering: Can an LLM
                                                           write a question so hard (or bad) that it can’t answer?
mathematical reasoning in LLMs.                            ArXiv preprint, abs/2410.15512.

Limitations                                              Zhangqian Bi, Yao Wan, Zheng Wang, Hongyu Zhang,
                                                           Batu Guan, Fangxin Lu, Zili Zhang, Yulei Sui, Xu-
While TP-as-a-Judge demonstrates strong capabil-           anhua Shi, and Hai Jin. 2024. Iterative refinement
ities in verifying intermediate reasoning for syn-         of project-level code context for precise code gen-
thetic data generation, it has several limitations.        eration with compiler feedback. ArXiv preprint,
                                                           abs/2403.16792.
Firstly, theorem prover verification is highly effec-
tive in mathematical reasoning but remains chal-         Bradley Brown, Jordan Juravsky, Ryan Ehrlich, Ronald
lenging in other domains, making its extension             Clark, Quoc V Le, Christopher Ré, and Azalia Mirho-
beyond mathematics an open research question.              seini. 2024. Large language monkeys: Scaling in-
                                                           ference compute with repeated sampling. ArXiv
While formalisation enhances verification com-             preprint, abs/2407.21787.
pared to standard methods, it is not flawless, re-
quiring further refinement for broader applicabil-       Davide Castelvecchi. 2021. Mathematicians welcome
ity. Secondly, our current implementation primar-          computer-assisted proof in ‘grand unification’theory.
                                                           Nature, 595(7865):18–19.
ily focuses on algebra, counting, probability, and
problem-solving datasets. Expanding to additional        Guoxin Chen, Minpeng Liao, Chengxi Li, and Kai Fan.
mathematical areas could improve generalisation            2024. Alphamath almost zero: Process supervision
and model performance. Thirdly, dataset complex-           without process. In Advances in Neural Information
                                                           Processing Systems 38: Annual Conference on Neu-
ity is limited by the LLM’s ability to reliably solve      ral Information Processing Systems 2024, NeurIPS
problems. When generating more challenging prob-           2024, Vancouver, BC, Canada, December 10 - 15,
lems, the model often fails, restricting the complex-      2024.
Wenhu Chen, Xueguang Ma, Xinyi Wang, and                    Peiyi Wang, Xiao Bi, et al. 2025. Deepseek-R1:
 William W Cohen. 2022. Program of thoughts                 Incentivizing reasoning capability in LLMs via rein-
 prompting: Disentangling computation from reason-          forcement learning. ArXiv preprint, abs/2501.12948.
 ing for numerical reasoning tasks. ArXiv preprint,
 abs/2211.12588.                                          Chaoqun He, Renjie Luo, Yuzhuo Bai, Shengding Hu,
                                                            Zhen Leng Thai, Junhao Shen, Jinyi Hu, Xu Han,
Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian,             Yujie Huang, Yuxiang Zhang, et al. 2024. Olympiad-
  Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias            bench: A challenging benchmark for promoting AGI
  Plappert, Jerry Tworek, Jacob Hilton, Reiichiro           with olympiad-level bilingual multimodal scientific
  Nakano, et al. 2021. Training verifiers to solve math     problems. ArXiv preprint, abs/2402.14008.
  word problems. ArXiv preprint, abs/2110.14168.
Leonardo De Moura and Nikolaj Bjørner. 2008. Z3:          Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul
  An efficient SMT solver. In International conference      Arora, Steven Basart, Eric Tang, Dawn Song, and Ja-
  on Tools and Algorithms for the Construction and          cob Steinhardt. 2021. Measuring mathematical prob-
  Analysis of Systems, pages 337–340. Springer.             lem solving with the math dataset. ArXiv preprint,
                                                            abs/2103.03874.
Leonardo De Moura, Soonho Kong, Jeremy Avigad,
  Floris Van Doorn, and Jakob von Raumer. 2015. The       Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan
  lean theorem prover (system description). In Auto-        Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and
  mated Deduction-CADE-25: 25th International Con-          Weizhu Chen. 2022. Lora: Low-rank adaptation of
  ference on Automated Deduction, Berlin, Germany,          large language models. In The Tenth International
  August 1-7, 2015, Proceedings 25, pages 378–388.          Conference on Learning Representations, ICLR 2022,
  Springer.                                                 Virtual Event, April 25-29, 2022. OpenReview.net.

Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey,          Gérard Huet, Gilles Kahn, and Christine Paulin-
  Abhishek Kadian, Ahmad Al-Dahle, Aiesha Letman,           Mohring. 1997. The Coq proof assistant a tutorial.
  Akhil Mathur, Alan Schelten, Amy Yang, Angela             Rapport Technique, 178.
  Fan, et al. 2024. The Llama 3 herd of models. ArXiv
  preprint, abs/2407.21783.                               Aaron Hurst, Adam Lerer, Adam P Goucher, Adam
Manuel Eberl, Anthony Bordg, Lawrence C Paulson,            Perelman, Aditya Ramesh, Aidan Clark, AJ Os-
 and Wenda Li. 2024. Formalising half of a graduate         trow, Akila Welihinda, Alan Hayes, Alec Radford,
 textbook on number theory (short paper). In 15th In-       et al. 2024. GPT-4o system card. ArXiv preprint,
 ternational Conference on Interactive Theorem Prov-        abs/2410.21276.
 ing (ITP 2024). Schloss Dagstuhl–Leibniz-Zentrum
 für Informatik.                                          Aaron Jaech, Adam Kalai, Adam Lerer, Adam Richard-
                                                            son, Ahmed El-Kishky, Aiden Low, Alec Helyar,
Zhibin Gou, Zhihong Shao, Yeyun Gong, Yelong Shen,          Aleksander Madry, Alex Beutel, Alex Carney, et al.
  Yujiu Yang, Nan Duan, and Weizhu Chen. 2024a.             2024. OpenAI o1 system card. ArXiv preprint,
  CRITIC: large language models can self-correct with       abs/2412.16720.
  tool-interactive critiquing. In The Twelfth Inter-
  national Conference on Learning Representations,        Albert Q Jiang, Alexandre Sablayrolles, Arthur Men-
  ICLR 2024, Vienna, Austria, May 7-11, 2024. Open-         sch, Chris Bamford, Devendra Singh Chaplot, Diego
  Review.net.                                               de las Casas, Florian Bressand, Gianna Lengyel, Guil-
                                                            laume Lample, Lucile Saulnier, et al. 2023a. Mistral
Zhibin Gou, Zhihong Shao, Yeyun Gong, Yelong Shen,          7b. ArXiv preprint, abs/2310.06825.
  Yujiu Yang, Minlie Huang, Nan Duan, and Weizhu
  Chen. 2024b. Tora: A tool-integrated reasoning          Albert Qiaochu Jiang, Sean Welleck, Jin Peng Zhou,
  agent for mathematical problem solving. In The            Timothée Lacroix, Jiacheng Liu, Wenda Li, Mateja
  Twelfth International Conference on Learning Rep-         Jamnik, Guillaume Lample, and Yuhuai Wu. 2023b.
  resentations, ICLR 2024, Vienna, Austria, May 7-11,       Draft, sketch, and prove: Guiding formal theorem
  2024. OpenReview.net.                                     provers with informal proofs. In The Eleventh In-
                                                            ternational Conference on Learning Representations,
WT Gowers, Ben Green, Freddie Manners, and Ter-
                                                            ICLR 2023, Kigali, Rwanda, May 1-5, 2023. Open-
 ence Tao. 2023. On a conjecture of marton. ArXiv
                                                            Review.net.
 preprint, abs/2311.05762.
Xinyu Guan, Li Lyna Zhang, Yifei Liu, Ning Shang,         Dongwei Jiang, Marcio Fonseca, and Shay Cohen. 2024.
  Youran Sun, Yi Zhu, Fan Yang, and Mao Yang. 2025.         LeanReasoner: Boosting complex logical reasoning
  rstar-math: Small LLMs can master math reason-            with lean. In Proceedings of the 2024 Conference of
  ing with self-evolved deep thinking. ArXiv preprint,      the North American Chapter of the Association for
  abs/2501.04519.                                           Computational Linguistics: Human Language Tech-
                                                            nologies (Volume 1: Long Papers), pages 7497–7510,
Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song,          Mexico City, Mexico. Association for Computational
  Ruoyu Zhang, Runxin Xu, Qihao Zhu, Shirong Ma,            Linguistics.
Takeshi Kojima, Shixiang Shane Gu, Machel Reid, Yu-       Qing Lyu, Shreya Havaldar, Adam Stein, Li Zhang,
  taka Matsuo, and Yusuke Iwasawa. 2022. Large lan-         Delip Rao, Eric Wong, Marianna Apidianaki, and
  guage models are zero-shot reasoners. In Advances         Chris Callison-Burch. 2023. Faithful chain-of-
  in Neural Information Processing Systems 35: An-          thought reasoning. In Proceedings of the 13th In-
  nual Conference on Neural Information Processing          ternational Joint Conference on Natural Language
  Systems 2022, NeurIPS 2022, New Orleans, LA, USA,         Processing and the 3rd Conference of the Asia-Pacific
  November 28 - December 9, 2022.                           Chapter of the Association for Computational Lin-
                                                            guistics (Volume 1: Long Papers), pages 305–329,
Joshua Ong Jun Leang, Aryo Pradipta Gema, and               Nusa Dua, Bali. Association for Computational Lin-
  Shay B Cohen. 2024. Comat: Chain of mathemati-            guistics.
  cally annotated thought improves mathematical rea-
  soning. ArXiv preprint, abs/2410.10336.                 Iman Mirzadeh, Keivan Alizadeh, Hooman Shahrokhi,
                                                            Oncel Tuzel, Samy Bengio, and Mehrdad Farajtabar.
Jia Li, Edward Beeching, Lewis Tunstall, Ben Lip-           2024. Gsm-symbolic: Understanding the limitations
   kin, Roman Soletskyi, Shengyi Huang, Kashif Rasul,       of mathematical reasoning in large language models.
   Longhui Yu, Albert Q Jiang, Ziju Shen, et al. 2024a.     ArXiv preprint, abs/2410.05229.
   Numinamath: The largest public dataset in ai4maths
   with 860k pairs of competition math problems and       Niklas Muennighoff, Zitong Yang, Weijia Shi, Xi-
   solutions. Hugging Face repository, 13:9.                ang Lisa Li, Li Fei-Fei, Hannaneh Hajishirzi, Luke
                                                            Zettlemoyer, Percy Liang, Emmanuel Candès, and
Zenan Li, Yifan Wu, Zhaoyu Li, Xinming Wei, Xian            Tatsunori Hashimoto. 2025. s1: Simple test-time
  Zhang, Fan Yang, and Xiaoxing Ma. 2024b. Autofor-         scaling. ArXiv preprint, abs/2501.19393.
  malize mathematical statements by symbolic equiv-
  alence and semantic consistency. In Advances in         Theo Olausson, Alex Gu, Ben Lipkin, Cedegao Zhang,
  Neural Information Processing Systems 38: Annual          Armando Solar-Lezama, Joshua Tenenbaum, and
  Conference on Neural Information Processing Sys-          Roger Levy. 2023. LINC: A neurosymbolic approach
  tems 2024, NeurIPS 2024, Vancouver, BC, Canada,           for logical reasoning by combining language models
  December 10 - 15, 2024.                                   with first-order logic provers. In Proceedings of the
                                                            2023 Conference on Empirical Methods in Natural
Percy Liang, Rishi Bommasani, Tony Lee, Dimitris            Language Processing, pages 5153–5176, Singapore.
  Tsipras, Dilara Soylu, Michihiro Yasunaga, Yian           Association for Computational Linguistics.
  Zhang, Deepak Narayanan, Yuhuai Wu, Ananya Ku-
  mar, et al. 2022. Holistic evaluation of language       Team OLMo, Pete Walsh, Luca Soldaini, Dirk Groen-
  models. ArXiv preprint, abs/2211.09110.                   eveld, Kyle Lo, Shane Arora, Akshita Bhagia, Yuling
                                                            Gu, Shengyi Huang, Matt Jordan, et al. 2025. 2 olmo
Haohan Lin, Zhiqing Sun, Yiming Yang, and Sean              2 furious. ArXiv preprint, abs/2501.00656.
  Welleck. 2024.   Lean-star: Learning to inter-
  leave thinking and proving.   ArXiv preprint,           Sungjin Park, Xiao Liu, Yeyun Gong, and Edward Choi.
  abs/2407.10040.                                           2024. Ensembling large language models with pro-
                                                            cess reward-guided tree search for better complex
Wang Ling, Dani Yogatama, Chris Dyer, and Phil Blun-        reasoning. ArXiv preprint, abs/2412.15797.
  som. 2017. Program induction by rationale genera-
  tion: Learning to solve and explain algebraic word      Arkil Patel, Satwik Bhattamishra, and Navin Goyal.
  problems. In Proceedings of the 55th Annual Meet-         2021. Are NLP models really able to solve simple
  ing of the Association for Computational Linguistics      math word problems? In Proceedings of the 2021
 (Volume 1: Long Papers), pages 158–167, Vancouver,         Conference of the North American Chapter of the
  Canada. Association for Computational Linguistics.        Association for Computational Linguistics: Human
                                                            Language Technologies, pages 2080–2094, Online.
Jianqiao Lu, Yingjia Wan, Zhengying Liu, Yinya Huang,       Association for Computational Linguistics.
   Jing Xiong, Chengwu Liu, Jianhao Shen, Hui Jin,
   Jipeng Zhang, Haiming Wang, et al. 2024a. Process-     Lawrence C Paulson. 1994. Isabelle: A generic theorem
   driven autoformalization in lean 4. ArXiv preprint,      prover. Springer.
   abs/2406.01940.
                                                          Auguste Poiroux, Gail Weiss, Viktor Kunčak, and
Zimu Lu, Aojun Zhou, Houxing Ren, Ke Wang,                  Antoine Bosselut. 2024. Improving autoformal-
  Weikang Shi, Junting Pan, Mingjie Zhan, and Hong-         ization using type checking.    ArXiv preprint,
  sheng Li. 2024b. Mathgenie: Generating synthetic          abs/2406.07222.
  data with question back-translation for enhancing
  mathematical reasoning of llms. ArXiv preprint,         Xin Quan, Marco Valentino, Louise A Dennis, and An-
  abs/2402.16352.                                           dré Freitas. 2024. Verification and refinement of
                                                            natural language explanations through llm-symbolic
Liangchen Luo, Yinxiao Liu, Rosanne Liu, Samrat             theorem proving. ArXiv preprint, abs/2405.01379.
  Phatale, Harsh Lara, Yunxuan Li, Lei Shu, Yun Zhu,
  Lei Meng, Jiao Sun, et al. 2024. Improve mathemati-     Rafael Rafailov, Archit Sharma, Eric Mitchell, Christo-
  cal reasoning in language models by automated pro-        pher D. Manning, Stefano Ermon, and Chelsea Finn.
  cess supervision. ArXiv preprint, abs/2406.06592.         2023. Direct preference optimization: Your language
  model is secretly a reward model. In Advances in          Conference on Learning Representations, ICLR 2024,
  Neural Information Processing Systems 36: Annual          Vienna, Austria, May 7-11, 2024. OpenReview.net.
  Conference on Neural Information Processing Sys-
  tems 2023, NeurIPS 2023, New Orleans, LA, USA,          Peiyi Wang, Lei Li, Zhihong Shao, Runxin Xu, Damai
  December 10 - 16, 2023.                                   Dai, Yifei Li, Deli Chen, Yu Wu, and Zhifang Sui.
                                                            2024c. Math-shepherd: Verify and reinforce llms
Subhro Roy and Dan Roth. 2015. Solving general arith-       step-by-step without human annotations. In Proceed-
  metic word problems. In Proceedings of the 2015           ings of the 62nd Annual Meeting of the Association
  Conference on Empirical Methods in Natural Lan-           for Computational Linguistics (Volume 1: Long Pa-
  guage Processing, pages 1743–1752, Lisbon, Portu-         pers), pages 9426–9439.
  gal. Association for Computational Linguistics.
                                                          Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten
Swarnadeep Saha, Xian Li, Marjan Ghazvininejad, Ja-          Bosma, Brian Ichter, Fei Xia, Ed H. Chi, Quoc V. Le,
  son Weston, and Tianlu Wang. 2025. Learning to             and Denny Zhou. 2022. Chain-of-thought prompting
  plan & reason for evaluation with thinking-llm-as-a-       elicits reasoning in large language models. In Ad-
  judge. ArXiv preprint, abs/2501.18099.                     vances in Neural Information Processing Systems 35:
                                                            Annual Conference on Neural Information Process-
Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu,              ing Systems 2022, NeurIPS 2022, New Orleans, LA,
  Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan             USA, November 28 - December 9, 2022.
  Zhang, YK Li, Y Wu, et al. 2024. Deepseekmath:
  Pushing the limits of mathematical reasoning in open    Huajian Xin, Daya Guo, Zhihong Shao, Zhizhou Ren,
  language models. ArXiv preprint, abs/2402.03300.          Qihao Zhu, Bo Liu, Chong Ruan, Wenda Li, and
                                                            Xiaodan Liang. 2024. Deepseek-prover: Advancing
Andreas Stephan, Dawei Zhu, Matthias Aßenmacher,
                                                            theorem proving in llms through large-scale synthetic
  Xiaoyu Shen, and Benjamin Roth. 2024. From
                                                            data. ArXiv preprint, abs/2405.14333.
  calculation to adjudication: Examining llm judges
  on mathematical reasoning tasks. ArXiv preprint,        Jundong Xu, Hao Fei, Liangming Pan, Qian Liu, Mong-
  abs/2409.04168.                                           Li Lee, and Wynne Hsu. 2024. Faithful logical
Zhengyang Tang, Xingxing Zhang, Benyou Wang, and            reasoning via symbolic chain-of-thought. ArXiv
  Furu Wei. 2024. Mathscale: Scaling instruction tun-       preprint, abs/2405.18357.
  ing for mathematical reasoning. In Forty-first Inter-   An Yang, Beichen Zhang, Binyuan Hui, Bofei Gao,
  national Conference on Machine Learning, ICML             Bowen Yu, Chengpeng Li, Dayiheng Liu, Jianhong
  2024, Vienna, Austria, July 21-27, 2024. OpenRe-          Tu, Jingren Zhou, Junyang Lin, et al. 2024a. Qwen2.
  view.net.                                                 5-math technical report: Toward mathematical ex-
The Mistral AI Team. 2024.         Mathstral-7b-v0.1.       pert model via self-improvement. ArXiv preprint,
  https://huggingface.co/mistralai/Mathstral-7B-v0.1.       abs/2409.12122.

Shubham Toshniwal, Wei Du, Ivan Moshkov, Branislav        Kaiyu Yang, Gabriel Poesia, Jingxuan He, Wenda Li,
  Kisacanin, Alexan Ayrapetyan, and Igor Gitman.            Kristin Lauter, Swarat Chaudhuri, and Dawn Song.
  2024. Openmathinstruct-2: Accelerating ai for math        2024b. Formal mathematical reasoning: A new fron-
  with massive open-source instruction data. ArXiv          tier in ai. ArXiv preprint, abs/2412.16075.
  preprint, abs/2410.01560.
                                                          Longhui Yu, Weisen Jiang, Han Shi, Jincheng Yu,
Hugo Touvron, Louis Martin, Kevin Stone, Peter Al-          Zhengying Liu, Yu Zhang, James T. Kwok, Zhenguo
  bert, Amjad Almahairi, Yasmine Babaei, Nikolay            Li, Adrian Weller, and Weiyang Liu. 2024. Meta-
  Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti        math: Bootstrap your own mathematical questions
  Bhosale, et al. 2023. Llama 2: Open founda-               for large language models. In The Twelfth Inter-
  tion and fine-tuned chat models. ArXiv preprint,          national Conference on Learning Representations,
  abs/2307.09288.                                           ICLR 2024, Vienna, Austria, May 7-11, 2024. Open-
                                                            Review.net.
Haiming Wang, Huajian Xin, Chuanyang Zheng,
  Zhengying Liu, Qingxing Cao, Yinya Huang, Jing          Zheng Yuan, Hongyi Yuan, Chengpeng Li, Guanting
  Xiong, Han Shi, Enze Xie, Jian Yin, Zhenguo Li, and       Dong, Keming Lu, Chuanqi Tan, Chang Zhou, and
  Xiaodan Liang. 2024a. Lego-prover: Neural theo-           Jingren Zhou. 2023. Scaling relationship on learning
  rem proving with growing libraries. In The Twelfth        mathematical reasoning with large language models.
  International Conference on Learning Representa-          ArXiv preprint, abs/2308.01825.
  tions, ICLR 2024, Vienna, Austria, May 7-11, 2024.
  OpenReview.net.                                         Eric Zelikman, Yuhuai Wu, Jesse Mu, and Noah D.
                                                            Goodman. 2022. Star: Bootstrapping reasoning with
Ke Wang, Houxing Ren, Aojun Zhou, Zimu Lu, Sichun           reasoning. In Advances in Neural Information Pro-
  Luo, Weikang Shi, Renrui Zhang, Linqi Song,               cessing Systems 35: Annual Conference on Neural
  Mingjie Zhan, and Hongsheng Li. 2024b. Mathcoder:         Information Processing Systems 2022, NeurIPS 2022,
  Seamless code integration in llms for enhanced math-      New Orleans, LA, USA, November 28 - December 9,
  ematical reasoning. In The Twelfth International          2022.
Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan
  Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin,
  Zhuohan Li, Dacheng Li, Eric P. Xing, Hao Zhang,
  Joseph E. Gonzalez, and Ion Stoica. 2023. Judging
  llm-as-a-judge with mt-bench and chatbot arena. In
  Advances in Neural Information Processing Systems
  36: Annual Conference on Neural Information Pro-
  cessing Systems 2023, NeurIPS 2023, New Orleans,
  LA, USA, December 10 - 16, 2023.
Jin Peng Zhou, Charles Staats, Wenda Li, Christian
   Szegedy, Kilian Q. Weinberger, and Yuhuai Wu. 2024.
   Don’t trust: Verify - grounding LLM quantitative
   reasoning with autoformalization. In The Twelfth
   International Conference on Learning Representa-
   tions, ICLR 2024, Vienna, Austria, May 7-11, 2024.
   OpenReview.net.
A     Detailed Breakdown of Dataset                   A.4    Cost for Dataset Creation

The dataset breakdown is presented in Table 8. It     The dataset creation process incurs a cost of ap-
comprises 2,562 samples for SFT and 473 pairs (a      proximately $50 for generating 300 samples, av-
total of 946 samples) for DPO training, resulting     eraging $0.60 per sample. However, the total ex-
in an overall count of 3,508 samples. Based on the    pense varies depending on the number of iterations,
datasets generated, Theorem Prover as a Judge is      with fewer iterations potentially reducing costs. All
generalisable to various domains within mathemat-     Lean Prover verifications were conducted on a local
ics, and iterative autoformalisation has increased    machine.
its generalszability across domains, covering areas
such as arithmetic, number theory, algebra, and       B     Details on hyperparameters Tuning
others. However, in domains beyond mathematics,       For RLTPF, we use a two-stage training strategy
iterative autoformalisation may be ineffective. Ad-   consisting of one epoch of Supervised Fine-Tuning
ditional analysis of each component’s of Theorem      (SFT) followed by three epochs of Direct Prefer-
Prover as a Judge contribution to dataset creation    ence Optimisation (DPO) for reinforcement learn-
can be referred to Appendix G.                        ing. Our hyperparameter selection was configured
                                                      in a similar way with DPO (Rafailov et al., 2023),
A.1    SIMQA dataset Creation Details
                                                      using the default seed (seed=42), and a slight con-
In creating our datasets, we use OpenAI gpt-4o        figuration in the learning rate, as shown below:
models, which include gpt-4o-2024-08-06 and gpt-
4o-2024-11-20 and ChatGPT-4o-latest alternatively     Supervised Fine-Tuning (SFT) The initial fine-
for the SIMQA synthetic dataset creation pro-         tuning phase uses a batch size of 4 per device, with
cess. For API details regarding gpt-4o, please        gradient accumulation over 16 steps, effectively
refer to https://platform.openai.com/docs/            increasing the batch size to 64. We adopt a linear
models/gpt-4o.                                        learning rate scheduler with an initial learning rate
                                                      of 3 × 10−5 and a warmup phase of 150 steps.
A.2    Generation Parameters                          To improve training stability, we apply gradient
                                                      clipping with a maximum norm of 0.3 and enable
The SIMQA synthetic dataset is generated under
                                                      gradient checkpointing to reduce memory overhead.
the following parameter settings:
                                                      The optimisation strategy uses RMSprop, and we
                                                      save model checkpoints at the end of each epoch.
    • Temperature: 0.0 (greedy decoding)
                                                      Reinforcement Learning from Theorem Prover
    • Maximum Tokens: 3500                            Feedback (RLTPF) For the reinforcement learn-
                                                      ing phase, we adopt a DPO-based RL approach.
A.3    Experimental Settings                          Training is conducted over three epochs with a
To ensure consistency across dataset generation,      batch size of 2 per device, accumulating gradients
we adopt different prompting strategies for various   over 32 steps to achieve an effective batch size of
tasks:                                                64. The learning rate remains at 3 × 10−5 , but
                                                      we switch to a cosine learning rate scheduler to
    • LLM-Generated Questions: All questions          facilitate smoother convergence. We continue us-
      are generated using a few-shot setting. The     ing RMSprop as the optimiser and apply the same
      specific few-shot examples are provided in      gradient checkpointing strategy. To regulate policy
      Section H.                                      updates, we set the DPO regularisation parameter
                                                      (β) to 0.1, ensuring stable policy updates while
    • LLM-Generated Answers: All answers are          maintaining alignment with human preferences.
      generated using a zero-shot setting.
                                                      Evaluation and Checkpointing Model perfor-
    • Theorem Prover Formalisation: A 10-shot         mance is evaluated at fixed intervals, with logging
      setting is applied for GSM8K, while an 8-shot   conducted every 10 to 30 steps, depending on the
      setting is used for MATH (Algebra), and a       training phase. The evaluation strategy is based on
      6-shot setting for MATH (Counting and Prob-     step-wise validation, and models are stored at the
      ability).                                       end of each epoch.
  Category                    Number of Samples for SFT Number of Samples for DPO (pairs)
  GSM8K                                                    1500                                         188
  Algebra                                                     542                                       185
  Counting & Probability                                      512                                        86
  Others                                                       8                                         14
  Total                                                    2562                                         473

                          Table 8: Distribution of labeled datasets for model training.


Computational Resources for Model Training                E    Iterative Autoformalisation
and Evaluation All experiments were conducted
using 2 80-GB A100 GPUs.                                  Based on Figure 6, we observe that 50% of auto-
                                                          formalisation attempts require multiple iterations
                                                          to produce a correct autoformalisation that can be
C    Consistency Check                                    successfully evaluated by the Lean prover. This
                                                          demonstrates the significance of iterative autofor-
We conducted a consistency check by evaluat-              malisation in refining reasoning steps. Notably,
ing three runs of llama-3.2-3b-instruct and               the majority of cases are resolved by the third it-
llama-3.1-8b-instruct using different random              eration, while a subset of more complex instances
seeds (seed 42, seed 2103 and seed 1234). The re-         requires up to five iterations. These findings high-
sults, summarised in Tables 9 and 10, indicate that       light the potential of iterative autoformalisation as
the average accuracy remains stable across runs,          a robust mechanism for bridging the gap between
with relatively low standard deviation. However,          autoformalisation and LLM Reasoning, with fur-
GSM8K-Symbolic and AIME exhibit higher stan-              ther refinements offering promising avenues for
dard deviation, suggesting that the true accuracy         improvement.
may be higher than the reported values.
   A consistent trend is observed across both             F    Dataset Details
models, though CoT in llama-3.1-8b-instruct
slightly outperforms the average attempt, while           URL and Licenses
llama-3.2-3b-instruct shows a marginal ad-                    • SVAMP (Patel et al., 2021): https://
vantage on SVAMP. Due to computational con-                     github.com/arkilpatel/SVAMP, License:
straints, our evaluation is limited to these two mod-           SVAMP License
els. Nevertheless, the results reinforce their robust-
ness and stability across different runs.                     • MultiArith (Roy and Roth, 2015): https:
                                                                //huggingface.co/datasets/ChilleD/
                                                                MultiArith/viewer/default/test,      li-
D    Evaluation Metrics
                                                                cense: CC BY 4.0.
Similar to (Leang et al., 2024), the majority of our
                                                              • GSM8K     (Cobbe      et  al.,   2021):
datasets use exact match as our evaluation met-
                                                                https://huggingface.co/datasets/
rics. For the OlympiadBench datasets, where exact
                                                                openai/gsm8k, License: GSM8K License
match is not a suitable evaluation metric, we used
the gpt-4o-mini model as a benchmark to assess                • GSM-Symbolic (Mirzadeh et al., 2024):
how closely the answers of the model aligned with               https://huggingface.co/datasets/
the ground truth. To prevent the model from gener-              apple/GSM-Symbolic, License:   GSM-
ating reasoning that could influence its decision, we           Symbolic License
input only the final three sentences, which typically
contain both the answer and the correct solution.             • AQUA (Ling et al., 2017):      https:
The task was to determine whether these two ele-                //github.com/google-deepmind/AQuA,
ments matched, without providing any intermediate               also   available   on    HuggingFace:
reasoning. The prompt is shown below:                           https://huggingface.co/datasets/
Llama-3.1-8b          MultiArith       SVAMP          GSM8K GSM-Symbolic-500            MATH-500            AIME
Original Attempt        97.78%          88.67%            83.75%            58.20%         46.00%          10.00%
Second Attempt          98.33%          85.33%            83.68%            66.80%         46.00%          20.00%
Third Attempt           97.22%          88.00%            83.45%            63.80%         46.00%          10.00%
Average Attempt 97.78% ± 0.56 87.33% ± 1.77 83.63% ± 0.16            62.93% ± 4.37 46.00% ± 0.00 13.33% ± 5.77
Original CoT            97.78%         88.33%             82.38%            55.60%         44.00%          10.00%

                   Table 9: Performance comparison of Llama-3.1-8b on various benchmarks.

Llama-3.2-3b         MultiArith        SVAMP          GSM8K GSM-Symbolic-500            MATH-500            AIME
Original Attempt        98.33%          81.67%            77.22%            59.60%         46.00%          13.33%
Second Attempt          98.89%          80.33%            75.09%            55.80%         44.00%          13.33%
Third Attempt           98.89%          81.00%            76.84%            56.20%         44.80%          10.00%
Average Attempt 98.70% ± 0.32 81.00% ± 0.67 76.38% ± 1.14            57.20% ± 2.09 44.93% ± 1.01 12.22% ± 1.92
Original CoT            98.89%          80.67%            75.97%            56.00%         44.00%          10.00%

                   Table 10: Performance comparison of Llama-3.2-3b on various benchmarks.


     deepmind/aqua_rat/viewer/raw/test,                     improves answer verification. Each aspect of our
     License: AQUA License                                  theorem prover-as-judge approach has been care-
                                                            fully curated to enhance autoformalisation and data
    • MATH (Hendrycks et al., 2021):                        quality.
      https://huggingface.co/datasets/
                                                               Autoformalisation is an inherently challenging
      HuggingFaceH4/MATH-500, License: MATH
                                                            problems due to the difficulty of ensuring that auto-
      License
                                                            formalised questions align with their original coun-
    • AIME-2024:        https://huggingface.                terparts. Our generated pipeline is crucial at each
      co/datasets/Maxwell-Jia/AIME_2024,                    step because components either facilitate correct
      License: AIME-2024 License                            formalisation (e.g., CoMAT (Leang et al., 2024)
                                                            during question formalisation) or ensure verifica-
    • OlympiadBench (He et al., 2024):                      tion accuracy (e.g., alignment check). The decom-
      https://huggingface.co/datasets/                      position into question and answer formalisation
      Hothan/OlympiadBench/tree/main,  Li-                  is based on existing theorem provers (Jiang et al.,
      cense: OlympiadBench License                          2023b), as research shows question formalisation
                                                            improves answer verification. Each aspect of theo-
G    Breakdown of Theorem Prover as a                       rem prover as judge has been carefully curated to
     Judge                                                  enhance autoformalisation and data quality.
Autoformalisation presents inherent challenges due             Within the question-formalisation phase
to the difficulty of ensuring that autoformalised           (S1,2,3,4 ), the CoMAT step, S1 improves per-
questions align with their original counterparts.           formance by approximately 20%, while our
Most recent works involve multiple calls to LLMs            autoformalisation component, S2 enhances answer
and expensive automated theorem proving tech-               formalisation. Auto-Informalisation, S3 and
niques (Li et al., 2024b; Poiroux et al., 2024). Sim-       alignment checks S4 serve as metrics to verify
ilarly, our generated pipeline is crucial at each step,     that CoMAT and autoformalisation are performed
as components either facilitate correct formalisa-          correctly. This additional layer is essential as there
tion (e.g., CoMAT during question formalisation)            are no definitive metrics to validate question for-
or ensure verification accuracy (e.g., alignment            malisation correctness. Misalignments potentially
checks).                                                    caused by errors may result in disposal before
   The decomposition into question and answer for-          proceeding to answer formalisation. Removing
malisation is based on existing theorem provers, as         any component could compromise data quality (eg.
research demonstrates that question formalisation           omitting CoMAT may reduce autoformalisation by
    System Message:
    You are a decider that decides whether the answer is the same as the correct answer. If the output doesn’t align with the
    correct answer, respond with ’0’, whereas if it’s correct, then respond with ’1’. DO NOT PROVIDE YOUR OWN
    ANSWER OR REASONING, JUST SELECT ‘0’ OR ‘1’.

    User Message:
    gpt-4o Result: {gpt_result}
    Correct Answer: {correct_answer}.
    Answer with 0 (Wrong) or 1 (Correct).



                                               Figure 5: gpt-4o evaluation prompt.

                      Category                            Subcategory                        Error (%)
                                                          Autoformalisation Error                  13.10
                      Question Formalisation
                                                          Alignment Check Error                    10.00
                      Answer Formalisation                —                                          5.40

                     Table 11: Error rates for each component of the autoformalisation pipeline.


         160                                                      to reconstruct problem statements solely from the
         140
         120                                                      provided solutions.
         100                                                         Each question below (all from GSM8K and par-
          80                                                      tially from MATH) and its corresponding answer
          60
          40                                                      are then formalised as a few-shot example for the
          20                                                      Lean prover formalisation.
           0
               1       2         3         4       5
                        Number of Iterations                      I    Manual Annotation Details
Figure 6: Number of iterations for the GSM8K-                     We conduct a manual annotation process to verify
Synthetic dataset.                                                the correctness of the theorem prover’s validations.
                                                                  Manual annotation is performed by a mathematics
                                                                  and statistics bachelor’s graduate, who is specifi-
20%, while eliminating alignment checks might                     cally instructed to solve the mathematical problems.
allow incorrect but seemingly verified autofor-                   To ensure consistency in manual verification, we
malisation to progress to answer formalisation,                   randomly sampled 54 instances from the GSM8K-
affecting the verification of model reasoning.                    synthetic dataset (see examples in Appendix J).
   As shown in Figure 4, 23.10% of total sam-
ples resulted in question formalisation error, 5.4%
in answer formalisation error, while the remain-
ing 71.50% were categorised as verified or false.
The detailed breakdown of filtering components is
shown in Table 11. While we have not analysed
CoMAT, it could potentially be evaluated using
alignment check as well. These statistics provide
clear analysis of each component.

H     Few-shot Examples for Synthetic Data
      Creation

In our experiments, we used the Reverse Question-
Answering method, which uses only the solution as
the few-shot example during synthetic data genera-
tion. This approach ensures that the model learns
Few Shot Examples for GSM8K

  Question

  Sara babysits the neighbor’s kids 4 times, earning $5 each time she babysits them. Her parents pay
  her $4 each time she mows the lawn. If Sara already had $10 saved before she started babysitting,
  how many times must she mow the lawn before she can afford the jacket and shoes?


  Solution
  Both pairs of shoes will cost a total of 2 ∗ $20 = $ << 2 ∗ 20 = 40 >> 40. Sara will need to
  save a total of $30 + $40 = $ << 30 + 40 = 70 >> 70 to buy everything that she wants. Sara
  has earned 4 ∗ $5 = $ << 4 ∗ 5 = 20 >> 20 from babysitting. Between her savings and the
  babysitting, Sara has already saved $10 + $20 = $ << 10 + 20 = 30 >> 30. Sara needs to
  earn an additional $70 − $30 = $ << 70 − 30 = 40 >> 40 from mowing the lawn to afford
  her clothes. Sara must mow the lawn $40/$4 =<< 40/4 = 10 >> 10 times to afford to buy the
  jacket and shoes. #### 10


  Question

  Adrien’s total salary was 30 percent higher than Lylah’s. Four years later, his salary had increased,
  and he was earning 40% more than what he was making four years ago. If Adrien’s and Lylah’s
  salary increased simultaneously, and Adrien earned $40000 four years ago, calculate the total
  salary the two were receiving four years later?


  Solution
  Since Adrien was earning $40000 four years ago and received a raise that makes him earn
  40% more, he received a 40/100 ∗ $40000 = $ << 40/100 ∗ 40000 = 16000 >> 16000
  raise. In total, four years later, Adrien’s salary is $40000 + $16000 = $56000 If four years
  ago Adrien was earning $40000, and Lylah’s salary was 30% less, then Lylah’s salary was
  30/100 ∗ $40000 = $12000 less than Adrien’s salary four years ago. Four years ago, Lylah
  was earning $40000 − $12000 = $28000 After receiving a 40% raise, Lylah earns 40/100 ∗
  $28000 = $ << 40/100 ∗ 28000 = 11200 >> 11200 In total, four years later, Lylah earns
  $28000 + $11200 = $ << 28000 + 11200 = 39200 >> 39200. The total amount of salary the
  two earn four years later is $39200 + $56000 = $ << 39200 + 56000 = 95200 >> 95200 ####
  95200


  Question

  Carlos is planting a lemon tree. The tree will cost $90 to plant. Each year it will grow 7 lemons,
  which he can sell for $1.5 each. It costs $3 a year to water and feed the tree. How many years will
  it take before he starts earning money on the lemon tree?


  Solution
  He makes $10.5 selling lemons each year because 7 x 1.5 = «7*1.5=10.5»10.5 He earns $7.5 each
  year from the lemon tree because 10.5 - 3 = «10.5-3=7.5»7.5 It will take 12 years to earn enough
  to pay off the tree because 90 / 7.5 = «90/7.5=12»12 He will make money in year 13 because 12 +
  1 = «12+1=13»13 #### 13
Question

A company pays each of its employees $600 in a month. The company has a policy of increasing
the salaries of each of its employees by 10% of the initial salary every year for those who’ve stayed
in the company for five years. If Sylvie just clocked 5 years in the company last December, what’s
her annual salary after three more years of service?

Solution
In a month, Sylvie earns $600. which totals $600/month * 12 months/year = $7200 in a year. Sylvie
earnings will increase by 10/100 * $7200/year = $«10/100*7200=720»720/year after 5 years. In
three years, the total increase in her salary will be 3 years * $720/year = $«3*720=2160»2160
After three years, Sylvie will be paid $7200 + $2160 = $«7200+2160=9360»9360 #### 9360

Question

Howard spends $8 dollars at the arcade on Monday. On Tuesday, he spends twice as much at the
arcade as he did on Monday. On Wednesday, he spends 4 times as much at the arcade as he spent
on Tuesday. If he originally had $100, how much money does he have left?

Solution
On Tuesday, he spends $8 ∗ 2 = $ << 8 ∗ 2 = 16 >> 16. On Wednesday, he spends $16 ∗ 4 =
$ << 16 ∗ 4 = 64 >> 64. In total he spent $8 + $16 + $64 = $ << 8 + 16 + 64 = 88 >> 88
at the arcade. He has $100 − $88 = $ << 100 − 88 = 12 >> 12 left. #### 12

Question

While Joanne is gathering apples from her family’s orchard, her sister comes outside to help her.
Joanne gathers 30 apples from the tallest trees, half this amount from the shortest trees, and more
apples from the average trees. Compared with Joanne, her sister gathers twice as many apples
from the tallest trees and 3 times as many apples from the shortest trees. She doesn’t take any from
the average trees. If the sisters have gathered a combined total of 500 apples, how many apples did
Joanne gather from the average trees?

Solution
Joanna gathered 30 apples /2 =<< 30/2 = 15 >> 15 apples from the shortest trees. Her sister
gathered 30 apples ∗2 =<< 30 ∗ 2 = 60 >> 60 apples from the tallest trees. Her sister also
gathered 15 apples ∗3 =<< 15 ∗ 3 = 45 >> 45 apples from the shortest trees. In total, her
sister gathered 60 + 45 =<< 60 + 45 = 105 >> 105 apples. From the tallest and shortest trees,
Joanna gathered 30 + 15 =<< 30 + 15 = 45 >> 45 apples. So far, the sisters have a combined
total of 105 + 45 =<< 105 + 45 = 150 >> 150 apples. Therefore, Joanna must have gathered
500total apples − 150apples so far =<< 500 − 150 = 350 >> 350 apples from the average trees.
#### 350

Question

Pauline visits her favorite local museum three times a year. The cost of one visit is $2. After 5
years, the cost of one visit has increased by 150%, but Pauline decided not to give up any visit and
continued to go to the museum for 3 more years. How much did Pauline spend on all visits to the
museum?
Solution
Pauline visited the local museum 3 times a year, so she paid 3 ∗ 2 = $ << 3 ∗ 2 = 6 >> 6 every
year on visits. That means during the first 5 years Pauline spend 5∗6 = $ << 5∗6 = 30 >> 30 on
tickets. After 5 years the cost of one visit increased by 150/100∗2 = $ << 150/100∗2 = 3 >> 3.
That means the new price of the ticket was 2 + 3 = $ << 2 + 3 = 5 >> 5. So for per year
Pauline paid 3 * 5 = $ << 3 ∗ 5 = 15 >> 15. During the last 3 years, she paid in total
3 ∗ 15 = $ << 3 ∗ 15 = 45 >> 45. In total Pauline spend 30 + 45 = $ << 30 + 45 = 75 >> 75
on visits at the museum. #### 75



Question

Tim makes a special honey and jam mix. To make 1 jar of the mixture it takes 2 pounds of passion
fruit and 1.5 pounds of jackfruit. It also takes 2 pounds of special honey. The passion fruit costs $6
per pound, the jackfruit is $8 per pound, and the honey is $10 per pound. He sells each jar for $50.
How much profit does he make selling 10 jars?



Solution
The cost of the passion fruit is 2 ∗ 6 = $ << 2 ∗ 6 = 12 >> 12 The jackfruit cost 1.5 ∗ 8 = $ <<
1.5 ∗ 8 = 12 >> 12 The honey is 2 ∗ 10 = $ << 2 ∗ 10 = 20 >> 20 So the total cost for a jar
is 12 + 12 + 20 = $ << 12 + 12 + 20 = 44 >> 44 So the profit per jar is 50 − 44 = $ <<
50 − 44 = 6 >> 6 So the total profit for 10 jars is 10 ∗ 6 = $ << 10 ∗ 6 = 60 >> 60 #### 60



Question

Stacy is a high school Calculus teacher. She assigns 45 problems for homework. There are twice
as many multiple choice problems as free response, and 7 more free response than true/false. How
many true/false questions are there?



Solution
Define a variable ** Let x represent the number of true/false questions How many free response
problems are there? ** Free response:x + 7 How many multiple choice problems are there? **
Multiple choice: 2(x + 7) = 2x + 14 Write an equation ** Total:x + x + 7 + 2x + 14 = 45
Combine like terms ** 4x + 21 = 45 Subtract 21 from each side ** 4x = 24 Divide by 4 **
x =<< 6 = 6 >> 6 true/false questions #### 6



Question

Jamal works at a library shelving books. He has a cart full of books to put away in different
sections. In the history section, he shelves 12 books. In the fiction section, he shelves 19 books. In
the children’s section, he shelves 8 books but finds 4 that were left in the wrong place that he adds
to his cart to shelve elsewhere. He still has 16 books to shelve. How many books did he start with
in the cart?
  Solution
  How many books did Jamal start with? ** Jamal started with B books in the cart. How many
  books did Jamal have after the history section? ** He had B − 12 books after the history section.
  How many books did Jamal have after the fiction section? ** He had B − 12 − 19 = B - 31 books
  after the fiction section. How many books did Jamal have after the children’s section? ** He had
  B − 31 − 8 + 4 = B − 35 books after the children’s section. How many books did Jamal have
  left to shelve? ** He still had B - 35 = 16 books to shelve. How many books did Jamal start with?
  ** Thus, he started with B = 16 + 35 =<< 16 + 35 = 51 >> 51 books in the cart. #### 51




Few Shot Examples for MATH


Algebra


  Question
                                                         2
  How many vertical asymptotes does the graph of y = x2 +x−6 have?



  Solution

  The denominator of the rational function factors into x2 + x − 6 = (x − 2)(x + 3). Since the
  numerator is always nonzero, there is a vertical asymptote whenever the denominator is 0, which
  occurs for x = 2 and x = −3. Therefore, the graph has 2 vertical asymptotes.



  Question

  What is the simplified numerical value of a+11b   4a+3b
                                             a−b if a−2b = 5?




  Solution
  Let’s play with the given condition a little. Clearing out the denominator gives 4a + 3b =
  5(a − 2b) = 5a − 10b. Selectively combine like terms by adding 9b − 4a to both sides to get
                           12b
  12b = a − b. This gives        = 1.
                          a−b
                       a + 11b                   a − b + 12b   a−b     12b
  Now, we want to find         . Rewrite this as             =      +       = 1 + 1 = 2 , and
                        a−b                         a−b        a−b a−b
  we are done.



  Question

  What is the shortest distance between the circles defined by x2 − 24x + y 2 − 32y + 384 = 0 and
  x2 + 24x + y 2 + 32y + 384 = 0?
Solution

We complete the square for the first equation by adding (−24/2)2 and (−32/2)2 to both sides,
which gives:
(x2 − 24x + 144) + (y 2 − 32y + 256) − 16 = 0,
which is also equivalent to:
(x − 12)2 + (y − 16)2 = 42 .
Similarly, the equation for the second circle is:
(x + 12)2 + (y + 16)2 = 42 .
Hence, the centers of the circles are (12,16) and (-12,-16) respectively. Furthermore, the radii
of the circles are equal to 4. Now the distance between the points (12,16) and (-12,-16) by the
distance formula or similarity of 3-4-5 triangles is 40. Therefore, to find the shortest distance
between the two circles, we must subtract from 40 the distances from the centers to the circles.
Thus, the shortest distance between the circles is 40 − 4 − 4 = 32.

Question

Let f(x) be an even function, and let g(x) be an odd function. Is f(x) g(x) even, odd, or neither?
Enter "odd", "even", or "neither."

Solution
Since f(x) is even and g(x) is odd,
f (−x)g(−x) = f (x)(−g(x)) = −f (x)g(x),
so f(x) g(x) is an "odd" function.

Question

The function f(x) satisfies
f (f (x)) = 6x − 2005
for all real numbers x. There exists an integer n such that f (n) = 6n − 2005. Find n.

Solution
Setting x = n, we get
f (f (n)) = 6n − 2005,
so f (6n − 2005) = 6n − 2005. Then
f (f (6n − 2005)) = f (6n − 2005) = 6n − 2005.
But f (f (6n − 2005)) = 6(6n − 2005) − 2005. Solving
6(6n − 2005) − 2005 = 6n − 2005,
we find n = 401.

Question

Cheldelin Middle School has 12 doors to enter or leave the building. In how many ways is it
possible to enter the building by one door and leave the building by a different door?

Solution
You can enter the building through one of 12 different doors. Since only that door is eliminated
from the doors for you to exit, there are 11 choices for the exit door. So the total number of ordered
pairs of enter, exit doors is 12 ∗ 11 = 132.
   Question

   A world-record swimmer and a dolphin compete in a 400-meter race. The swimmer swims at a
   rate of 2 meters per second, and the dolphin swims at a rate of 8 meters per second. When the
   dolphin crosses the finish line, how many meters is the swimmer from the finish line?

   Solution
   The dolphin swims four times faster than the swimmer, so it covers four times the distance in a
   given time. So when the dolphin has swum 400 meters to get to the finish line, the swimmer has
   swum 400/4=100 meters, and is thus 400 − 100 = 300 meters from the finish line.

   Question

   The function f(x) satisfies f (f (x)) = 6x − 2005 for all real numbers x. There exists an integer n
   such that f (n) = 6n − 2005. Find n.

   Solution
   Setting x = n, we get f(f(n)) = 6n - 2005, so f(6n - 2005) = 6n - 2005. Then f(f(6n - 2005)) = f(6n -
   2005) = 6n - 2005. But f(f(6n - 2005)) = 6(6n - 2005) - 2005. Solving 6(6n - 2005) - 2005 = 6n -
   2005, we find n = 401.

Counting and Probability
   Question

   For a particular peculiar pair of dice, the probabilities of rolling 1, 2, 3, 4, 5, and 6 on each die are
   in the ratio 1 : 2 : 3 : 4 : 5 : 6. What is the probability of rolling a total of 7 on the two dice?

   Solution
  On each die the probability of rolling k, for 1 ≤ k ≤ 6, is
  ( k / (1+2+3+4+5+6) ) = ( k / 21 ).
  There are six ways of rolling a total of 7 on the two dice, represented by the ordered pairs (1,6),
  (2,5), (3,4), (4,3), (5,2), and (6,1).
  Thus, the probability of rolling a total of 7 is
  (1 ∗ 6 + 2 ∗ 5 + 3 ∗ 4 + 4 ∗ 3 + 5 ∗ 2 + 6 ∗ 1)/(212 ) = (56/212 ) = (8/63).

   Question

   Two candidates, Dan and Donald, run for class president. Two other candidates, Freddie and
   Bernie, run for vice president. Each candidate has a 50

   Solution
   The probability that Dan wins is (1/2). The probability that Freddie wins is also (1/2).
   Therefore, the probability that both win is (1/2 ∗ 1/2) = (1/4).

   Question

   Given that (15 choose 8) = 6435, (16 choose 9) = 11440, and (16 choose 10) = 8008, find (15
   choose 10).
Solution
We can use Pascal’s identity:
(n − 1 choose k − 1) + (n − 1 choose k) = (n choose k)
to find (15 choose 9).
(15 choose 8 ) + (15 choose 9 ) = (16 choose 9)6435 + (15 choose 9) = 11440(15 choose 9 ) =
5005
We use the identity again to find (15 choose 10).
(15 choose 9) + (15 choose 10) = (16 choose 10)5005 + (15 choose 10) = 8008 (15 choose 10)
= 3003
Therefore, (15 choose 10) = 3003.



Question

An ant is walking on a hexagon. At each step, he moves from the vertex on which he is standing to
an adjacent vertex. After 15 steps, what is the probability that he is standing on the same vertex on
which he began?



Solution
There are two ways in which the ant can return to his original vertex: either he can go part of the
way around the hexagon and then retrace his steps, or he can go all the way around the hexagon.
In the first case, the ant necessarily moves an even number of steps, because his total number of
steps is twice the number of steps needed to get to the point at which he begins to retrace.
In the second case, because a hexagon has an even number of vertices, the ant is again moving an
even number of steps.
Thus, he has no way to return to the vertex on which he began in an odd number of steps, so the
probability is 0.



Question

Link is coloring a triforce, which consists of four equilateral triangles and is depicted below. He
has three colors to use: gold, black, and green. So that it remains recognizable, he doesn’t want to
color any two triangles the same color if they share a side. How many different ways can he color
the triforce? (Two colorings that differ by rotation are considered distinct.)



Solution
There are 3 ways to choose a color for the center. Once the center color is chosen, for each of the
remaining triangles there are 2 ways to choose a color (any color except the center color).
Therefore, there are (3 ∗ 2 ∗ 2 ∗ 2) = 24 ways to color the triforce.



Question

Coin A is flipped three times and coin B is flipped four times. What is the probability that the
number of heads obtained from flipping the two fair coins is the same?
Solution
The result will occur when both A and B have either 0, 1, 2, or 3 heads, and these probabilities are
shown in the table:
Heads | 0 | 1 | 2 | 3
——|—|—|—|—
A | (1/8) | (3/8) | (3/8) | (1/8)
B | (1/16) | (4/16) | (6/16) | (4/16)
The probability of both coins having the same number of heads is
(1/8 ∗ 1/16) + (3/8 ∗ 4/16) + (3/8 ∗ 6/16) + (1/8 ∗ 4/16) = (35/128).
J   Examples for Manual Annotation

    Manual Annotation Question 1

    Question               Emily is planning a fundraising event to help a local charity. She plans to sell tickets and
                           also host different activities at the event which cost different amounts to host. She originally
                           purchased 150 tickets, and each ticket will be sold for $25. Before the event, Emily decides
                           to buy an additional 50% more tickets at a discounted rate of $15 per ticket to ensure she
                           can accommodate everyone. During the event, she spends $200 on materials for a painting
                           activity and $300 on materials for a crafting activity. If Emily sells all the tickets and collects an
                           additional $500 from people attending the activities, how much does she need to raise in total
                           to offset all her costs (excluding the first 150 ticket costs) and make sure the charity receives a
                           donation of at least $2000?
    Model Result           Step 1: Calculate the total number of tickets

                               • Original tickets: 150

                               • Additional tickets: 150 × 0.5 = 75

                               • Total tickets: 150 + 75 = 225

                           Step 2: Calculate the total cost of the tickets

                               • Cost of additional tickets: 75 × 15 = 1125

                           Step 3: Calculate the costs of the activities

                               • Painting activity: $200

                               • Crafting activity: $300

                               • Total activity cost: 200 + 300 = 500

                           Step 4: Calculate Emily’s total costs

                               • Total costs: 1125 + 500 = 1625

                           Step 5: Calculate total revenue

                               • Revenue from ticket sales: 225 × 25 = 5625

                               • Additional revenue from activities: $500

                               • Total revenue: 5625 + 500 = 6125

                           Step 6: Determine the amount Emily needs to raise

                               • Required amount: 1625 + 2000 = 3625

                           Step 7: Verify if Emily raises enough money

                               • Since total revenue ($6125) is greater than required amount ($3625), Emily raises enough
                                 money.

                           Final Answer: Emily needs to raise $3625 in total to cover all costs and donate at least $2000
                           to charity.
    Verification Results   Verified
Manual Annotation Question 2

Question               Jason is a handyman who has multiple projects lined up for the month. For Project A, he spends
                       3 days working 5 hours each day, earning $15 per hour. For Project B, he works twice as many
                       hours as Project A but at a rate 25% lower than for Project A. Project C requires him to work
                       50% more hours than he worked on Project B, and the pay rate is $5 more per hour than his rate
                       for Project A. Additionally, he spends $150 on supplies for Project C. At the end of the month,
                       Jason has completed another two projects, D and E, each composed of the same number of
                       hours as Project A but both at a 10% higher pay rate than Project C. Calculate the total amount
                       Jason earns in the month after accounting for all his expenses including the cost of supplies.
Model Result           Step 1: Calculate earnings from Project A

                          • Total hours: 3 × 5 = 15

                          • Earnings: 15 × 15 = 225

                       Step 2: Calculate earnings from Project B

                          • Total hours: 2 × 15 = 30

                          • Pay rate: 15 − (0.25 × 15) = 11.25

                          • Earnings: 30 × 11.25 = 337.50

                       Step 3: Calculate earnings from Project C

                          • Total hours: 30 + (0.5 × 30) = 45

                          • Pay rate: 15 + 5 = 20

                          • Earnings before expenses: 45 × 20 = 900

                          • Net earnings: 900 − 150 = 750

                       Step 4: Calculate earnings from Projects D and E

                          • Total hours: 15 + 15 = 30

                          • Pay rate: 20 + (0.1 × 20) = 22

                          • Earnings: 30 × 22 = 660

                       Step 5: Calculate total earnings and expenses

                          • Total earnings:
                                                     225 + 337.50 + 750 + 660 = 1972.50

                          • Total expenses: $150

                       Step 6: Calculate net earnings

                          • Net earnings:
                                                           1972.50 − 150 = 1822.50

                       Final Answer: Jason’s total earnings after expenses are $1822.50.
Verification Results   False



                       Figure 7: Verification of Jason’s monthly earnings calculation.
Manual Annotation Question 3

Question               A factory produces a special type of widget and incurs a production cost that includes a fixed
                       cost of $5000 per month and a variable cost of $20 per widget produced. The widgets are sold at
                       a price of $60 each. Due to new regulations, the variable cost per widget will increase by 25%,
                       and the factory plans to increase the selling price by 10% to maintain profitability. Currently,
                       the factory produces 300 widgets per month. If the factory wants to achieve the same profit
                       margin in the new scenario as it does currently, how many widgets must it produce and sell to
                       maintain this profit margin, if the fixed costs remain the same and all other conditions apply?
Model Result           Step 1: Define the Current Profit Margin

                          • Fixed Cost = $5000

                          • Variable Cost per Widget = $20

                          • Selling Price per Widget = $60

                          • Number of Widgets Produced and Sold = 300

                       Revenue:
                                                       Revenue = 60 × 300 = 18, 000
                       Total Cost:
                                                Total Cost = 5000 + (20 × 300) = 11, 000
                       Profit:
                                                     Profit = 18, 000 − 11, 000 = 7, 000
                       Profit Margin:
                                                                 7, 000
                                              Profit Margin =           = 0.3889 (or 38.89%)
                                                                18, 000
                       Step 2: Define the New Scenario

                          • New Variable Cost per Widget:

                                                              20 + (0.25 × 20) = 25

                          • New Selling Price per Widget:

                                                              60 + (0.10 × 60) = 66

                       Step 3: Formulate the Equation for the New Scenario
                                                           41x − 5000
                                                                      = 0.3889
                                                              66x
                       Multiply both sides by 66x:

                                                          41x − 5000 = 25.3674x

                                                          41x − 25.3674x = 5000

                                                             15.6326x = 5000
                       Solve for x:
                                                                 5000
                                                           x=           ≈ 319.8
                                                                15.6326
                       Since x must be an integer, we round up to:

                                                                  x = 320
                       Final Answer: The factory must produce and sell 320 widgets to maintain the same profit
                       margin.
Verification Results   False
Mannutal Annotation 4 - Example of False Verification Result

Question               Sara is saving money to buy a new bicycle and some accessories. The bicycle costs $350, and
                       she wants to buy a helmet, a lock, and a pump, which cost $45, $30, and $25 respectively. Sara
                       earns $12 per hour working at a cafe and $8 per hour tutoring. She can work up to 15 hours a
                       week in the cafe and 10 hours tutoring. She already has $150 in savings. Sara plans to divide her
                       work hours equally between the two jobs each week, but she also wants to save $50 each month
                       for emergencies before spending on the bicycle and accessories. If her expenses (excluding the
                       bicycle and accessories) amount to $200 each month, how many weeks will Sara need to work
                       to afford the bicycle and all the accessories, while maintaining her savings goal and expenses?
Model Result           Step 1: Calculate the total cost of the bicycle and accessories

                       Bicycle: $350
                       Helmet: $45
                       Lock: $30
                       Pump: $25
                       Total cost: 350 + 45 + 30 + 25 = 450

                       Step 2: Calculate the amount Sara still needs to save

                           • Sara’s current savings: $150

                           • Additional amount needed: 450 − 150 = 300

                       Step 3: Calculate Sara’s weekly earnings

                           • Cafe hours per week: 15
                                                  2
                                                     = 7.5

                           • Tutoring hours per week: 10
                                                       2
                                                         =5

                           • Cafe earnings per week: 7.5 × 12 = 90

                           • Tutoring earnings per week: 5 × 8 = 40

                           • Total weekly earnings: 90 + 40 = 130

                       Step 4: Calculate Sara’s monthly earnings

                           • Monthly earnings: 130 × 4 = 520

                       Step 5: Calculate Sara’s monthly savings after expenses

                           • Monthly expenses: $200

                           • Emergency savings: $50

                           • Total money set aside per month: 200 + 50 = 250

                           • Amount left for bicycle savings: 520 − 250 = 270

                       Step 6: Calculate the number of months required to save $300

                           • Required months: 300
                                              270
                                                  ≈ 1.11

                           • Rounding up, Sara needs to work for **2 months**.

                       Step 7: Convert months to weeks

                           • Total weeks needed: 2 × 4 = 8

                       Final Answer: Sara needs to work for 8 weeks to afford the bicycle and all accessories while
                       maintaining her savings goal and covering expenses.
Verification Results   Verified
Actual Results         FALSE - 2.75 weeks
Manual Annotation 5 - Verification of Solutions on Bad Question Clarity

Question               An art collector has a variety of art pieces, including paintings, sculptures, and photographs, all
                       of which she bought at different times. She initially bought a collection of paintings, which she
                       later expanded by purchasing additional paintings, doubling her original number. The total cost
                       she paid for all these paintings was $56,000. Later, she sold 5 paintings at a profit of 20% of
                       their buying price, which contributed to a profit of $9,000. She then bought sculptures, spending
                       75% of the remaining money she gained from selling paintings. Afterward, she purchased
                       photographs using the remaining funds from the money left after buying sculptures and an
                       additional $8,000 she acquired from selling an old rare drawing. She bought 12 photographs,
                       each costing $500 more than twice the amount she spent on a single sculpture. After all these
                       purchases, the collector realized she has $10,000 left. Determine the initial number of paintings
                       the art collector bought and the cost of each sculpture.
Model Result           Step 1: Define Variables

                       Let x be the initial number of paintings.
                       Let p be the price of each painting.
                       Let s be the cost of each sculpture.

                       Step 2: Total Cost of Paintings

                           • The collector initially bought x paintings.

                           • Later, she doubled her collection by purchasing another x paintings.

                           • Total paintings: 2x.

                           • Given total cost:
                                                                    2x · p = 56000

                           • Simplifying:
                                                           x · p = 28000      (divide by 2)                           (1)

                       Step 3: Selling 5 Paintings at 20% Profit

                           • Cost price of 5 paintings:
                                                                           5·p

                           • Selling price (with 20% profit):
                                                                       5 · p · 1.2

                           • Profit equation:
                                                            9000 = (5 · p · 1.2) − (5 · p)

                           • Simplify:
                                                                9000 = 5 · p · (1.2 − 1)
                                                                   9000 = 5 · p · 0.2
                                                                       9000 = p
                                                           p = 1800      (cost per painting)                          (2)

                       Step 4: Solve for x (Initial Number of Paintings)

                           • Substitute p = 1800 into equation (1):

                                                                   x · 1800 = 28000
                                                                          28000
                                                                      x=
                                                                           1800
                                                                      x = 15.56

                       Final Answer: The initial number of paintings the art collector bought is 15.56
Verification Results   False
Manual Annotation 6.1

Question               Five years ago, Thomas invested $150,000 in a commercial property. Over the years, the
                       property’s value increased by 25% every two years. After five years, Thomas decided to sell the
                       property, but before selling, he spent $35,000 on renovations. Additionally, he had to pay a 6%
                       commission fee on the final selling price to the real estate agency. If Thomas made a profit of
                       $120,000 after all expenses and fees, what was the selling price of the property?
Model Result           To find the selling price of the property, we will follow these steps:
                       —
                       Step 1: Calculate the value of the property after 5 years - The property value increases by
                       25% every two years. - In 5 years, there are two full 2-year periods (4 years) and one additional
                       year. - After the first 2 years, the value increases by 25%:

                                           Value after 2 years = 150,000 × (1 + 0.25) = 187,500

                       - After the next 2 years (4 years total), it increases again by 25%:

                                           Value after 4 years = 187,500 × (1 + 0.25) = 234,375

                       - Since the extra one year does not complete another 2-year period, the value remains

                                                         Value after 5 years = 234,375

                       —
                       Step 2: Add the renovation costs - Thomas spent $35,000 on renovations. - Hence, the total
                       cost basis is
                                           Total cost basis = 234,375 + 35,000 = 269,375.
                       —
                       Step 3: Calculate the profit - He made a profit of $120,000 after all expenses and fees. Let the
                       selling price be S. - Profit equation:

                                                          S − 269,375 = 120,000.

                       - So
                                                     S = 120,000 + 269,375 = 389,375.
                       —
                       Step 4: Account for the commission fee - The real-estate agent takes 6% of S. So Thomas
                       receives
                                              Amount received = S − 0.06 S = 0.94 S.
                       - We set that equal to his cost basis + profit:

                                                                                389,375
                                            0.94 S = 389,375       =⇒     S=            ≈ 414,000.
                                                                                  0.94
                       —
                       Step 5: Final verification - Check amount received after commission:

                                                          0.94 × 414,000 ≈ 389,160.

                       - Check profit:
                                                 389,160 − 269,375 ≈ 119,785 ≈ $120,000.
                       - This is sufficiently close to $120,000, so the calculations are consistent.
                       Thus, the selling price is approximately $414,000.
                       The final answer is: 414,000. The answer is 414000.
Verification Results   False (Correct Lean Verification)
Manual Annotation 6.2

Question               Five years ago, Thomas invested $150,000 in a commercial property. Over the years, the
                       property’s value increased by 25% every two years. After five years, Thomas decided to sell the
                       property, but before selling, he spent $35,000 on renovations. Additionally, he had to pay a 6%
                       commission fee on the final selling price to the real estate agency. If Thomas made a profit of
                       $120,000 after all expenses and fees, what was the selling price of the property?
Model Result           We are tasked with finding the selling price of the property based on the given information.
                       Let’s solve this step by step.
                       —
                       ### Step 1: Understand the problem - Initial investment: $150,000 - Value increase: 25%
                       every 2 years - Renovation cost: $35,000 - Commission fee: 6% of the selling price - Profit
                       after all expenses and fees: $120,000
                       We need to calculate the selling price of the property.
                       —
                       ### Step 2: Calculate the property’s value after 5 years The property’s value increases by 25%
                       every 2 years. Since 5 years is not a multiple of 2, we will break it into two periods: 1. The
                       first 2 years 2. The next 2 years 3. The remaining 1 year
                       #### Step 2.1: After the first 2 years The property’s value increases by 25% after 2 years. The
                       new value is:

                        Value after 2 years = 150, 000 + (25% × 150, 000) = 150, 000 × (1 + 0.25) = 187, 500

                       #### Step 2.2: After the next 2 years (4 years total) The property’s value increases by another
                       25% after 2 more years. The new value is:

                        Value after 4 years = 187, 500 + (25% × 187, 500) = 187, 500 × (1 + 0.25) = 234, 375

                       #### Step 2.3: After the remaining 1 year The property’s value increases proportionally for the
                       remaining 1 year. Since 1 year is half of 2 years, the increase will be half of 25%, which is
                       12.5%. The new value is:

                       Value after 5 years = 234, 375+(12.5%×234, 375) = 234, 375×(1+0.125) = 263, 671.875

                       Thus, the property’s value after 5 years is $263,671.88 (rounded to 2 decimal places).
                       —
                       ### Step 3: Account for renovation costs and commission fees Let the selling price of the
                       property be S.
                       #### Step 3.1: Total expenses Thomas spent $35,000 on renovations. Additionally, he paid a
                       6% commission fee on the selling price. The total expenses related to the sale are:

                                        Total expenses = 35, 000 + (6% × S) = 35, 000 + 0.06S

                       #### Step 3.2: Profit equation Thomas made a profit of $120,000 after all expenses and fees.
                       The profit equation is:

                                        Profit = Selling price − Initial investment − Total expenses

                       Substitute the known values:

                                              120, 000 = S − 150, 000 − (35, 000 + 0.06S)

                       —
                       ### Step 4: Solve for S Simplify the equation:

                                               120, 000 = S − 150, 000 − 35, 000 − 0.06S

                                                      120, 000 = S − 185, 000 − 0.06S
                                                             305, 000 = 0.94S
                                                              S = 324, 468.09
                       Thus, the selling price of the property is $324,468.09.
Verification Results   Verified (Correct Lean Verification)
K    Example of Iterative Autoformalisation
In the process of Theorem Prover as a Judge, there are two main components: question formalisation
and answer formalisation. During question formalisation, we follow four steps (denoted S4 ): applying
the CoMAT method, autoformalisation, Auto-Informalisation, and Alignment Check. We used the
example from the previous appendix (Manual Example 6.2) as an illustration. In this example, we present
how autoformalisation works during question formalisation and then proceed to answer formalisation,
providing a detailed analysis of how iterative autoformalisation refines the Lean code into a correct version
over three iterations. When one is formalised as False (6.1) and the other as Verified (6.2), the model
will be trained using Direct Preference Optimisation. The examples and prompts have been modified to
remove unicode,

    Question Formalisation

    import Mathlib

    def initial_investment : Int := 150000
    def renovation_cost    : Int := 35000
    def commission_rate    : Rat := 6 / 100
    def profit             : Int := 120000
    def increase_rate      : Rat := 25 / 100

    def value_after_5_years : Rat :=
    initial_investment * (1 + increase_rate) ^ 2 * (1 + increase_rate / 2)

    def selling_price : Rat :=
    (profit + initial_investment + renovation_cost) / (1 - commission_rate)

    def commission_fee : Rat := commission_rate * selling_price
    def total_expenses : Rat := renovation_cost + commission_fee
Answer Formalisation
[Iterative Autoformalisation 1]
import Mathlib

-- Define constants
def initial_investment : Int := 150000
def renovation_cost    : Int := 35000
def commission_rate    : Rat := 6 / 100
def profit             : Int := 120000

-- Define the property value increase rate and time periods
def increase_rate : Rat := 25 / 100
def years         : Int := 5

-- Step 1: Property value after 5 years
def value_after_2_years : Rat := initial_investment * (1 + increase_rate)
def value_after_4_years : Rat := value_after_2_years * (1 + increase_rate)
def value_after_5_years : Rat := value_after_4_years * (1 + (increase_rate / 2))

theorem compute_value_after_5_years :
  value_after_5_years = 263671.875 := by
  calc
   value_after_5_years = value_after_4_years * (1 + increase_rate / 2) := by rfl
    _ = (initial_investment * (1 + increase_rate) ^ 2)
    * (1 + increase_rate / 2) := by norm_num

-- Step 2: Selling price & expenses
def selling_price   : Rat := 324468.09
def commission_fee : Rat := commission_rate * selling_price
def total_expenses : Rat := renovation_cost + commission_fee

theorem compute_total_expenses :
  total_expenses = 54468.09 := by
  calc
    total_expenses = 35000 + (6 / 100 * 324468.09) := by norm_num

-- Step 3: Profit verification
def computed_profit : Rat := selling_price - initial_investment - total_expenses

theorem verify_profit :
  computed_profit = profit := by
  norm_num

-- Step 4: Check selling price
def result : String :=
  if selling_price = 324468.09 then "verified" else "false"

#eval result        -- "verified"
#eval selling_price -- 324468.09
Answer Formalisation
[Iterative Autoformalisation 2]
[Same as previous autoformalisation]
.....

-- Step 1: Compute property value after 5 years
-- After two 2-year periods: multiply by (1 + 0.25)^2
-- For the remaining 1 year (half of a 2-year period): multiply by (1 + 0.25/2)
def value_after_5_years : Rat :=
  initial_investment * (1 + increase_rate) ^ 2 * (1 + increase_rate / 2)

theorem compute_value_after_5_years :
  value_after_5_years = (2109375 : Rat) / 8 := by
  -- Unfold definitions so norm_num can simplify
  unfold value_after_5_years increase_rate initial_investment
  norm_num

-- Step 2: Solve for selling_price S in the profit equation:
-- profit = S - initial_investment - (renovation_cost + commission_rate * S)
-- Numerator = 120000 + 150000 + 35000 = 305000
-- Denominator = 1 - 6/100 = 94/100
def selling_price : Rat :=
  (305000 : Rat) / (94 / 100)

-- Commission fee and total expenses
def commission_fee : Rat := commission_rate * selling_price
def total_expenses : Rat := renovation_cost + commission_fee

theorem compute_total_expenses :
  total_expenses = (2560000 : Rat) / 47 := by
  -- Unfold so that norm_num can compute the rational sum exactly
  unfold total_expenses commission_fee selling_price commission_rate
  renovation_cost norm_num

-- Step 3: Verify the profit equation
def computed_profit : Rat :=
  selling_price - initial_investment - total_expenses

theorem verify_profit :
  computed_profit = profit := by
  unfold computed_profit selling_price total_expenses
  commission_fee initial_investment renovation_cost commission_rate
  norm_num

-- Step 4: Check that selling_price matches the explicit rational
def result : String :=
  if selling_price = (305000 : Rat) / (94 / 100) then "verified" else "false"

#eval result        -- "verified"
#eval selling_price -- 305000 / (94/100) = 15250000/47 ~= 324468.085106383
Answer Formalisation
[Iterative Autoformalisation 3]
[Same as previous autoformalisation]
.....

-- Step 2: Solve for selling_price S in the profit equation:
-- profit = S - initial_investment - (renovation_cost + commission_rate * S)
-- => profit + initial_investment + renovation_cost = S * (1 - commission_rate)
-- => S = (profit + initial_investment + renovation_cost) / (1 - commission_rate)
--
-- CORRECTION: Define `selling_price` using the formula for a more robust proof.
def selling_price : Rat :=
  (profit + initial_investment + renovation_cost) / (1 - commission_rate)

-- Commission fee and total expenses
def commission_fee : Rat := commission_rate * selling_price
def total_expenses : Rat := renovation_cost + commission_fee

-- The theorem to compute the explicit value of total_expenses still works.
theorem compute_total_expenses :
  total_expenses = (2560000 : Rat) / 47 := by
  -- Unfold all definitions to compute the rational sum exactly
  unfold total_expenses commission_fee selling_price profit initial_investment
  renovation_cost commission_rate
  norm_num

-- Step 3: Verify the profit equation
def computed_profit : Rat :=
  selling_price - initial_investment - total_expenses

theorem verify_profit :
  computed_profit = profit := by
  unfold computed_profit total_expenses commission_fee selling_price
 field_simp [show (1:Q) - commission_rate != 0 by unfold commission_rate; norm_num]
  ring

-- Step 4: We can verify the value of selling_price with a theorem.
theorem selling_price_evaluates_correctly :
  selling_price = (15250000 : Rat) / 47 := by
 unfold selling_price profit initial_investment renovation_cost commission_rate
  norm_num

def result : String :=
  if selling_price = (305000 : Rat) / (94 / 100) then "verified" else "false"
#eval result        -- "verified"
#eval selling_price -- Evaluates to (15250000 : Rat)/47
Error for Answer Formalisation 1

   Answer Formalisation Error
   [Error for Autoformalisation 1]
   No info found.
   mathlib-demo.lean:22:84
   unsolved goals
   |- value_after_4_years = ↑initial_investment * (1 +
   increase_rate) ^ 2 or 1 + increase_rate / 2 = 0
   mathlib-demo.lean:19:38
   unsolved goals
   |- ↑initial_investment * (1 + increase_rate) ^ 2 * (1 + increase_rate / 2)
   = 263671.875
   mathlib-demo.lean:32:54
   unsolved goals
   |- total_expenses = 272340427 / 5000
   mathlib-demo.lean:30:31
   unsolved goals
   |- 35000 + 6 / 100 * 324468.09 = 54468.09
   mathlib-demo.lean:38:30
   unsolved goals
   |- computed_profit = ↑profit
   mathlib-demo.lean:45:0
   "verified"
   mathlib-demo.lean:46:0
   (32446809 : Rat)/100



Error for Answer Formalisation 2

   Answer Formalisation Error
   [Error for Autoformalisation 2]
   No info found.
   All Messages (3)
   mathlib-demo.lean:49:30
   unsolved goals
   |- 8200000 / 47 - (35000 + 3 / 50 * selling_price) = profit
   mathlib-demo.lean:58:0
   mathlib-demo.lean:59:0
   (15250000 : Rat)/47
   Restart File
