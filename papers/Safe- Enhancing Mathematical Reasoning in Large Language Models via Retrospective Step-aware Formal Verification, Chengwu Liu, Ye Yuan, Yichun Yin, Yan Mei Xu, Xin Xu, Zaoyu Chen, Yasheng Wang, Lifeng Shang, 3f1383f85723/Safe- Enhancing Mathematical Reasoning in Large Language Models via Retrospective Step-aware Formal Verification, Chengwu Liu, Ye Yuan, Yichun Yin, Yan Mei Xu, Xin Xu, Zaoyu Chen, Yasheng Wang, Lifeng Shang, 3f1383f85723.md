                                             Safe: Enhancing Mathematical Reasoning in Large Language Models
                                                      via Retrospective Step-aware Formal Verification
                                                             Chengwu Liu1∗ , Ye Yuan1 , Yichun Yin2 , Yan Xu2 , Xin Xu3∗ ,
                                                        Zaoyu Chen4∗ , Yasheng Wang2 , Lifeng Shang2 , Qun Liu2 , Ming Zhang1 ,
                                        1
                                           School of Computer Science, National Key Laboratory for Multimedia Information Processing,
                                                       PKU-Anker LLM Lab, Peking University, 2 Huawei Noah’s Ark Lab,
                                        3
                                          The Hong Kong University of Science and Technology, 4 The Hong Kong Polytechnic University,
                                                                             Correspondence: Ming Zhang (mzhang_cs@pku.edu.cn)


                                                                   Abstract                                                          Preceding Step
                                                                                                                                                      Retrospective Verification
                                                                                                                                                      Find evidence to support correctness
                                                                                                                                                      by Formal Step Verifier
                                                                                                                                     Preceding Step
                                                 Chain-of-Thought (CoT) prompting has be-                   Can I

                                                                                                                             🤗                        🤔
                                                                                                           get this
arXiv:2506.04592v1 [cs.CL] 5 Jun 2025




                                                                                                                                     Current Step                 Did I
                                                 come the de facto method to elicit reasoning ca-           right?
                                                                                                                                                                 get it
                                                 pabilities from large language models (LLMs).                                                                   wrong?
                                                                                                        Prospective Verification      Future Step
                                                                                                                Q-value Estimation
                                                 However, to mitigate hallucinations in CoT that         by Process Reward Models
                                                                                                                                      Future Step
                                                 are notoriously difficult to detect, current meth-
                                                 ods such as process reward models (PRMs)
                                                 or self-consistency operate as opaque boxes           Figure 1: The distinction between prospective verifica-
                                                 and do not provide checkable evidence for their       tion and retrospective verification.
                                                 judgments, possibly limiting their effectiveness.
                                                 To address this issue, we draw inspiration from
                                                 the idea that “the gold standard for support-         While it is feasible to generate them on a large
                                                 ing a mathematical claim is to provide a proof”       scale with manageable costs, verifying the absence
                                                 (Avigad et al., 2021). We propose a retrospec-        of hallucinations in these steps remains challenging.
                                                 tive, step-aware formal verification framework
                                                                                                       The verification process is especially crucial in do-
                                                 Safe. Rather than assigning arbitrary scores,
                                                 we strive to articulate mathematical claims in        mains such as mathematical reasoning (Ahn et al.,
                                                 formal mathematical language Lean 4 at each           2024; Xu et al., 2025), code generation (Zhuo et al.,
                                                 reasoning step and provide formal proofs to           2024; Li et al., 2024), and many others (Wang et al.,
                                                 identify hallucinations. We evaluate our frame-       2023b; Rein et al., 2023), where even minor errors
                                                 work Safe across multiple language models and         can significantly disrupt subsequent generations
                                                 various mathematical datasets, demonstrating a        and the final outcome(Shen et al., 2021; Zelikman
                                                 significant performance improvement while of-
                                                                                                       et al., 2022). Consequently, verifying the accu-
                                                 fering interpretable and verifiable evidence. We
                                                 also propose FormalStep as a benchmark for
                                                                                                       racy of each individual step becomes crucial to the
                                                 step correctness theorem proving with 30, 809         overall performance.
                                                 formal statements. To the best of our knowl-             To mitigate hallucinations, a prevalent strategy
                                                 edge, our work represents the first endeavor to       involves employing a verification mechanism that
                                                 utilize formal mathematical language Lean 4           evaluates and assigns scores to the reasoning trajec-
                                                 for verifying natural language content gener-
                                                                                                       tories generated by LLMs (Lightman et al., 2024;
                                                 ated by LLMs, aligning with the reason why
                                                 formal mathematical languages were created in         Wang et al., 2024b; Xu et al., 2024a). This ap-
                                                 the first place: to provide a robust foundation       proach facilitates the selection of the most promis-
                                                 for hallucination-prone human-written proofs.         ing responses from a pool of candidates, commonly
                                                                                                       referred to as Best-of-N (BoN) sampling (Shen
                                         1       Introduction                                          et al., 2021; Cobbe et al., 2021). Although effective,
                                         The practice of guiding LLMs to generate ad-                  these approaches perceive the LLM-based verifier
                                         ditional chain of thought during inference has                as an opaque box, thereby forfeiting the benefits
                                         emerged as a paradigm for enhancing the reasoning             of symbolic computation and formal verification.
                                         capabilities of these models (Wei et al., 2022; Ko-           Consequently, they inherently lack interpretability
                                         jima et al., 2022; Yu et al., 2023; Xu et al., 2024b).        and do not provide guarantees of correctness.
                                             *
                                                                                                          In this study, we propose a formal verification
                                             Work done during the internship at Huawei Noah’s Ark
                                         Lab. The code and dataset are available at https://github.    framework designed to enhance the strengths of
                                         com/liuchengwucn/Safe.                                        natural language reasoning, which is characterized
by its abundant data and diverse reasoning forms         numerical scores for each step. To the best of our
(Huang and Chang, 2023), with formal language            knowledge, this is the first study utilizing formal
reasoning, known for its ability to verify correct-      mathematics language Lean 4 to verify the correct-
ness and provide better interpretability (Pan et al.,    ness of mathematical reasoning trajectories gener-
2023). During the inference phase of LLMs, we de-        ated by LLMs. (3) We propose a formal verifica-
compose complex mathematical reasoning trajecto-         tion framework Safe that aggregates a sequence of
ries, which are challenging to verify entirely, into a   states generated by the formal step verifier. Further-
series of simpler steps. For each step, we utilize an    more, we demonstrate that the retrospective scores
LLM to automatically generate formal statements          generated by our formal verifier can be effectively
that substantiate the correctness of that particu-       integrated with the prospective scores, resulting in
lar step, akin to the process of auto-formalization.     state-of-the-art performance.
These formal statements necessitate only the evalu-
ation of single-step correctness, allowing them to       2     Related Work
be effectively addressed by readily available auto-
mated theorem provers. By aggregating the formal         The rapid advancement of LLMs has catalyzed
statements and proofs from each step as evidence,        transformative applications across diverse domains,
we can evaluate the overall reasoning trajectory by      ranging from medical diagnostics to fundamen-
scoring its state sequences.                             tal scientific discovery (Jumper et al., 2021, 2020;
   Note that our formal verifier focuses on the cor-     Madani et al., 2023; Yang et al., 2024a; Feng et al.,
rectness of each step, which constitutes retrospec-      2024; Shao et al., 2024; Ying et al., 2024b). Par-
tive verification. In contrast, PRMs are typically       ticularly in the realm of mathematical reasoning,
trained using a loss function that evaluates the like-   which serves as a critical benchmark for evaluat-
lihood of achieving a correct outcome in the future      ing artificial intelligence systems, researchers have
(Hao et al., 2023; Wang et al., 2024b), a process        embarked on two distinct yet complementary re-
that can be perceived as prospective verification.       search trajectories. The first strand focuses on for-
The distinction between these two approaches is il-      mal mathematics, where scholars investigate how
lustrated in Figure 1. Our proposed approach Safe,       LLMs can assist in constructing machine-verifiable
integrates retrospective formal scores with those of     mathematical proofs through interactive theorem
a prospective PRM, resulting in significant perfor-      provers like Lean and Coq (Polu and Sutskever,
mance improvement. This outcome highlights the           2020; Wang et al., 2023a; Xin et al., 2024a,b). Con-
potential of combining formal reasoning and nat-         currently, a parallel research effort examines the
ural language reasoning, an approach commonly            models’ capacity for solving mathematical word
referred to as the neuro-symbolic system (Besold         problems expressed in natural language, aiming to
et al., 2021; Sarker et al., 2022).                      develop general-purpose systems capable of pars-
   In conclusion, we present the following three         ing complex problem statements, generating step-
main contributions: (1) We propose a novel auto-         wise solutions, and providing rigorous mathemati-
formalization task, which aims to generate formal        cal justifications (Kojima et al., 2022; Shao et al.,
statements that validate the correctness of one spe-     2024; Ying et al., 2024b). This bifurcation in re-
cific step instead of simply translating the prob-       search directions reflects both the multifaceted na-
lem. Our dataset comprising 30, 809 formal state-        ture of mathematical intelligence and the evolving
ments, referred to as FormalStep, will be released       capabilities of modern language models.
to facilitate auto-formalization and automated the-
                                                         2.1    Automated Theorem Proving
orem proving in low compute settings. Our em-
pirical findings indicate that, despite these state-     The objective of automated theorem proving (ATP)
ments being out of distribution, they can still be       is to produce a formal proof process composed of
effectively addressed by off-the-shelf automated         a sequence of tactics for statements articulated in a
theorem provers, provided there is an adequate           formal language. This proof process is designed to
computational budget. (2) We propose a step-level        be automatically verifiable by a machine, thereby
formal verifier that outputs one of four distinct        ensuring its correctness. Pioneering work in this
states, depending on whether a given step can be         field GPT-f is trained using the Metamath set.mm
auto-formalized by an LLM and resolved by an             dataset and employs a best-first search method to
automated theorem prover, rather than providing          iteratively generate formal theorem proofs (Polu
                                             Math Question
           Verification with                                                                    Verification with
           Natural Language                                 Let’s think                         Formal Language
                                                  LLM
                                                            step by step.
                           n Reasoning
                           Trajectories
       Score                                 Reasoning Steps                                 State            Formal Evidence
      Sequence                                                                              Sequence
                                                                                                            Formal        Formal
       Score 1                                   Step 1                                      State 1      Statement 1     Proof 1

                      Process                                                  Formal                       Formal
       Score 2                                   Step 2                                      State 2      Statement 2
                    Reward Model                                            Step Verifier



                                                                                                             Formal      Formal
       Score m                                   Step m                                      State m      Statement m    Proof m



        MEAN          𝑆𝑐𝑜𝑟𝑒𝑝𝑟𝑜                  𝑆𝑐𝑜𝑟𝑒𝑆𝑎𝑓𝑒                     𝑆𝑐𝑜𝑟𝑒𝑟𝑒𝑡𝑟𝑜      LSTM
      Aggregation                    Merge                        Merge                     Aggregation



Figure 2: The primary pipeline flowchart. Solutions for each mathematical problem, generated using the zero-shot
CoT Prompt, are decomposed into reasoning steps. Each step is evaluated by both a Formal Verifier and a process
reward model (PRM), which assesses the state or score of each step. Following this evaluation, the states or scores
are aggregated to yield retrospective and prospective scores. These two scores can subsequently be combined to
generate a final evaluation score.

and Sutskever, 2020). Subsequent research pri-                              costs associated with employing domain experts for
marily focuses on implementing improved search                              annotation are prohibitively high. To address this
strategies (Lample et al., 2022; Wang et al., 2023a),                       issue, auto-formalization leverages the in-context
leveraging the capabilities of formal theorem prov-                         learning capabilities of LLMs to transform abun-
ing environments into the proving process (Yang                             dant preexisting mathematical data into formal data
et al., 2023; Thakur et al., 2024; Polu et al., 2022),                      (Wu et al., 2022; Lu et al., 2024; Jiang et al., 2024).
and synthesizing new data to enhance the quality                               Currently, existing efforts in auto-formalization
of the training dataset (Han et al., 2022; Xin et al.,                      are focusing on natural language mathematical
2024a; Huang et al., 2024). The benchmarks for au-                          datasets created by humans (Jiang et al., 2022;
tomated theorem proving include miniF2F(Zheng                               Ying et al., 2024a), as these datasets are already
et al., 2021), FIMO (Liu et al., 2023), TRIGO (Xiong                        abundant and of high-quality (mathlib Community,
et al., 2023), among others.                                                2019). These efforts primarily focus on the formal-
   Despite significant advancements in ATP                                  ization of mathematical statements rather than their
through the synthesis of new data via expert it-                            proofs.
eration and the enhancement of model exploration
within the solution space using complex tree search                         2.3    Process Reward Models
techniques, solving complex mathematical prob-                              In the fields of mathematical reasoning and code
lems remains a challenging and computationally in-                          generation, existing research suggests that process
tensive task. For example, despite a sample budget                          reward models (PRMs) are more effective than
of 16 × 6400, DeepSeek-Prover achieves a 60.2%                              outcome reward models (ORMs) (Lightman et al.,
accuracy rate on the miniF2F benchmark (Zheng                               2024; Wang et al., 2024b). An ORM assesses the
et al., 2021), which includes formalized problems                           overall performance of the whole output of LLMs,
from high school, competition, and undergradu-                              while a PRM evaluates each individual step, pro-
ate mathematics. Additionally, it attains merely                            viding more fine-grained feedback.
a 3.4% accuracy on the FIMO dataset, which con-                                PRMs have two primary applications (Wang
sists of more challenging problems typical of the                           et al., 2024b). First, they can be employed dur-
International Mathematical Olympiad (Xin et al.,                            ing the post-training reinforcement learning phase,
2024b).                                                                     where an LLM samples its outputs and learns from
                                                                            trajectories that receive higher scores from a PRM,
2.2   Auto-Formalization                                                    thereby facilitating self-improvement (Shao et al.,
ATP represents a particularly challenging task, pri-                        2024; Lai et al., 2024; Yan et al., 2024). Second,
marily due to the limited availability of formal                            PRMs can be used during the inference phase of
mathematical data (Wu et al., 2022). Moreover, the                          LLMs, allowing the model to sample multiple re-
sponses and select the Best-of-N as the final output.      and automated theorem proving. Verification of
Numerous studies have shown that this approach             these steps can be conducted concurrently to min-
can enhance the performance of LLMs in reasoning           imize end-to-end latency. We aggregate the ver-
tasks (Havrilla et al., 2024; Setlur et al., 2024).        ification states of each step using an aggrega-
                                                           tor to produce a retrospective scoreretro . Subse-
2.4    Neuro-symbolic AI                                   quently, we utilize an off-the-shelf PRM to obtain
In the domains of formal language mathematical             a prospective scorepro , which is then integrated
reasoning and natural language mathematical rea-           into scoreretro to derive the final score. A diagram
soning, while these two approaches differ method-          for the overall reasoning model is presented in Fig-
ologically, they possess complementary and mu-             ure 2. The following sections will elaborate on
tually reinforcing capabilities that can collectively      the processes of sampling and decomposition, the
advance the frontier of mathematical reasoning in          auto-formalization and theorem proving conducted
artificial intelligence. This line of research is of-      by the step verifier, and the details regarding the
ten referred to as Neuro-symbolic AI, which inte-          score aggregator.
grates the strengths of neural networks and sym-
bolic logic-based reasoning to develop more robust         3.1   Sampling and Decomposition
and intelligent systems (Yang et al., 2024b).              We use the zero-shot CoT prompting technique to
   Draft, Sketch and Prove represents a representa-        sample n outputs, denoted as:
tive approach that employs natural language to aug-
ment formal language reasoning (Jiang et al., 2022).       Ai ∼ LLM(P, cot_prompt) for i = 1, 2, . . . , n
This methodology primarily focuses on automated
theorem proving, where natural language serves             where the prompt is expressed in its simplest form
as supplementary guidance to enhance the success           as “Let’s think step by step” (Kojima et al., 2022).
rate of formal theorem provers. On the other hand,            To decompose the output Ai into discrete steps,
LINC (Olausson et al., 2023) and Logic-LM (Pan             we have explored two approaches: heuristic rules
et al., 2023) represent prominent approaches that          and LLM in-context learning (ICL) (Brown et al.,
leverage formal languages to enhance natural lan-          2020). The details of the decomposition can be
guage reasoning. These methods primarily em-               found in Appendix C.
ploy automatic formalization to transform natural
language tasks into formal representations before          3.2   Step Verifier
solving them through symbolic reasoning. Besides,          The step verifier validates reasoning steps by for-
DTV employs Isabelle to formally verify the quan-          malizing natural language expressions into formal
titative reasoning capabilities of LLMs (Zhou et al.,      statements that establish the mathematical sound-
2024).                                                     ness of these steps. We employ readily available au-
                                                           tomated theorem provers to attempt to prove these
3     Methodology                                          statements. Following the proof attempt, a verifica-
For any given mathematical problem P , we em-              tion state is generated.
ploy zero-shot chain-of-thought (CoT) prompting               There are certain scenarios in which the auto-
to sample n output results from an LLM, denoted            formalization process is unnecessary or impractical,
as A1 , A2 , . . . , An . Each output Ai is decomposed     which typically involve straightforward steps such
into a sequence of steps represented by:                   as chanting, repeating, and summarizing. Addition-
                                                           ally, some steps are sufficiently complex and fall
      Ai = concat(stepi1 , stepi2 , . . . , stepimi )
                                                           outside the typical scope of our formal mathemat-
, where concat denotes the concatenation function,         ical language, Lean 4 (Moura and Ullrich, 2021).
and mi indicates the number of steps contained             While Lean 4 can effectively express relationships
within Ai . Each step undergoes formal validation          relevant to number theory and algebra, it may face
through a step verifier, resulting in a verification       limitations in articulating concepts related to geom-
state defined as:                                          etry and combinatorial mathematics.
                                                              Our step verifier can produce one of four pos-
          stateij = step_verifier(stepij )
                                                           sible states: 1) no verification required; 2) failed
for i = 1, 2, . . . , n, j = 1, 2, . . . , mi . The step   formalization, which may result from either the lim-
verifier integrates two modules: auto-formalization        itations of the Lean 4 language or the constraints
of our auto-formalization pipeline; 3) successful        derived from individual natural language steps may
formalization accompanied by a proof of the state-       be out of distribution, they may nonetheless fall
ment; and 4) successful formalization, but with a        within the capabilities of contemporary automated
failure in theorem proving. The following subsec-        theorem provers. Subsequent experiments demon-
tions will offer a detailed description of the two       strate that for the ATP task, sampling a limited
essential components of our step verifier: auto-         number of proofs can yield a success rate exceed-
formalization and automated theorem proving.             ing 80%. The right half of Figure 3 provides an
                                                         example.
3.2.1   Auto-Formalization Module
Previous efforts in auto-formalization have primar-      3.3   State Aggregator
ily focused on translating mathematical statements       Auto-formalization pipelines and automated theo-
articulated in natural language into their equivalent    rem provers are fallible, leading to proof failures
formal mathematical statements (Wu et al., 2022).        that can arise from two extra sources: (1) the auto-
In this study, we utilize auto-formalization in a        formalization pipeline may produce a plausible but
novel manner to verify the mathematical sound-           erroneous and consequently unprovable statement
ness of each step. For instance, when the reasoning      despite the step being correct; or (2) while the state-
LLM attempts to transform inequalities, we use the       ment may be accurate and provable, the automated
inequality prior to the transformation as a premise      theorem prover may not be able to complete the
and the resulting inequality as the proof objective      proof within a constrained sample budget. As a
for the Lean 4 statement. An illustrative exam-          result, the four states provided by the step verifier
ple of auto-formalization is presented in the left       are inherently susceptible to noise. To mitigate the
half of Figure 3. Additional examples of our auto-       effects of noise, we aggregate all the states at each
formalization can be found in Appendix F.                step to compute one final score.
   In accordance with the existing literature (Wu           To perform the score prediction task, we utilize
et al., 2022; Liu et al., 2023), we leverage the capa-   a tiny LSTM model (Hochreiter, 1997), with a to-
bilities of LLMs in in-context learning to automate      ken vocabulary size of 4. Our choice of LSTM is
the formalization process for our verifier. The gen-     motivated by its simplicity and effectiveness for
erated formal statements are subsequently submit-        this specific task. Since the step verifier outputs a
ted to the Lean read-eval-print-loop (REPL) envi-        sequence of four discrete states (treated as tokens),
ronment for validation, ensuring adherence to the        an LSTM provides an intuitive yet efficient way to
Lean 4 syntax. We manually curate a selection of         model this sequential evidence. The latent variable
few-shot examples to guide the LLM in the process        from the final step undergoes a linear transforma-
of auto-formalization. Furthermore, we include in-       tion, followed by the application of the sigmoid
structions within the prompts to prompt the model        function to yield a score within the range of 0 to 1.
to recognize that certain steps do not require valida-
tion or may exceed the capabilities of Lean 4. The
complete prompt utilized in the auto-formalization          scoreiretro = σ(W · LSTM(statei1 , statei2 ,
process is available in Appendix A.                                       . . . , stateij ) + b)

3.2.2   Automated Theorem Proving Module                 Note that the information derived from formal veri-
In this study, we utilize existing automated theo-       fication is highly condensed and retrospective, as
rem provers to generate proofs for formalized state-     each state conveys only two bits of information.
ments, thereby providing evidence for the correct-       This contrasts with the prospective scores of LLM-
ness of the natural language steps involved. Specif-     based PRM, which uses complete reasoning steps
ically, we examine the performance of two state-         in natural language as input to predict a Q-value,
of-the-art LLM-based automated theorem provers,          indicating whether these steps can potentially lead
COPRA (Thakur et al., 2023) and DeepSeek-                to the correct answer (Wang et al., 2024b).
Prover-V1.5 (Xin et al., 2024b).                            scoreipro = PRM(stepi1 , stepi2 , . . . , stepij )
   As previously noted, the difficulty of formally
proving the validity statement of a single step is       Recognizing the complementarity between the two
intuitively lower than that of solving an entire prob-   scores, we further combine the retrospective score
lem. Consequently, while the formal statements           from the state aggregator with the prospective score
                                                                                   Four Possible Output States
          The Pipeline of                      No Verification                Failed                      Success                   Failure
          Our Step Verifier                       Required                 Formalization                  of Proof                 of Proof

                                                                                     Max Attempts                                         Max Attempts
                                                                                     Reached                                              Reached

          Reasoning Trajectory
           in Natural Language                                                  Lean 4 REPL                                         Lean 4 REPL
             Math Question
           (test/number_theory/627)
                                                                   or Retry               Check                         or Retry               Check
          If $n \equiv 2 \pmod{7}$,
          then find the remainder
          when $(n + 2)(n + 4)(n + 6)$
          is divided by 7.                                            Formal Statement                                        Formal Proof
                                                                      in Lean 4 Language                                   in Lean 4 Language
            Reasoning Steps                                                                                             theorem test
              (Generated by LLMs)                                  theorem test
                                                                    (n : ℤ)                                              (n : ℤ)
                                                                    (h₀: n ≡ 2 [ZMOD 7]):                                (h₀: n ≡ 2 [ZMOD 7]):
            Preceding Steps 1
                                                                    ((n + 2) * (n + 4) * (n + 6)) ≡                      ((n + 2) * (n + 4) * (n + 6)) ≡
                                                                   (4 * 6 * 1) [ZMOD 7] := by                           (4 * 6 * 1) [ZMOD 7] := by
            Preceding Steps 2                                      sorry                                                 rw [Int.ModEq] at h₀ ⊢
                                                                                                                         have h₁ : n % 7 = 2 := h₀
                                                    LLM                                                    LLM           have h₂ : (n + 2) % 7 = 4 := by
                                                                                                                           rw [Int.add_emod]
            Preceding Steps n                                                                                              simp [h₁]
                                                                     What does it mean?
                                             Auto-Formalization                                         Automated        have h₃ : (n + 4) % 7 = 6 := by
                                                                                                                           rw [Int.add_emod]
               Step to Verify                                      If n is an integer that is         Theorem Proving      simp [h₁]
             (Sampled from GPT-4o)                                 congruent to 2 modulo 7, then                         have h₄ : (n + 6) % 7 = 1 := by
                                                                   the product of n plus 2, n plus                         rw [Int.add_emod]
            The expression                                         4, and n plus 6 is congruent to                         simp [h₁]
            \((n + 2)(n + 4)(n + 6)\)                              (4 * 6 * 1) modulo 7.
            becomes \((4)(6)(1)\).                                                                                       simp [Int.mul_emod, h₂, h₃,
                                                                                                                        h₄]




Figure 3: The pipeline of the step verifier. We construct a prompt that incorporates the relevant question and
context, then utilize the in-context learning capability of large language models to perform auto-formalization. The
formalized Lean 4 theorem is then validated using the Lean REPL. Once the auto-formalization is successful, we
attempt to prove the theorem using an LLM-based prover, followed by verification through the Lean REPL. Upon
completion of the entire procedure, each step corresponds to one of four distinct states.

from an existing PRM to generate an ensemble                                           Baselines and Metrics We evaluate the perfor-
score. We experimented with several methods for                                        mance in comparison to the zero-shot CoT method
calculating ensemble scores, the detailed discus-                                      and the self-consistency majority voting strategy,
sion of which can be found in Appendix D.                                              as well as other reward models. We choose reward
                                                                                       models as baselines which possess a parameter
                                         α                 (1−α)                       size comparable to that of our automated theorem
      scorei = scoreiretro · scoreipro
                                                                                       prover, the DeepSeek-Prover-V1.5 with 7B param-
         A∗ = Ai∗ , where i∗ ∈ arg max scorei                                          eters. The baseline models include both ORMs
                                                       i
                                                                                       and PRMs. We incorporate the current SOTA rea-
where α is a hyper-parameter.                                                          soning ORMs in RewardBench (Lambert et al.,
                                                                                       2024), featuring Skywork-Reward-Llama-3.1-8B-
4     Experiment
                                                                                       v0.2 (Liu et al., 2024) and ArmoRM-Llama3-8B-
4.1    Experimental Setup                                                              v0.1 (Wang et al., 2024a) as representative exam-
Datasets and LLMs We evaluate BoN@5 accu-                                              ples. Regarding PRMs, existing works are primar-
racy on the GSM8K (Cobbe et al., 2021), MATH-500                                       ily domain-specific. Thus we include two recent
(Hendrycks et al., 2021; Lightman et al., 2024), and                                   PRMs that concentrate on mathematical reason-
CollegeMath (Tang et al., 2024) datasets, which                                        ing, namely math-shepherd-mistral-7b-prm (Wang
encompass grade school, high school, and college-                                      et al., 2024b) and RLHFlow/Llama3.1-8B-PRM-
level mathematics. Our experiments includes four                                       Deepseek-Data (Xiong et al., 2024), as the repre-
language models: Llama-3-8B-Instruct (Dubey                                            sentative models.
et al., 2024), Llama-3.1-8B-Instruct (Dubey et al.,                                    State Aggregator Data Collection We randomly
2024), gpt-4o-2024-08-06 (Hurst et al., 2024), and                                     select a subset of the training dataset that has ap-
deepseek-math-7b-instruct (Shao et al., 2024). This                                    proximately the same size as the test dataset to train
selection represents a range of models from dif-                                       the LSTM model. Specifically, the selection com-
ferent model families and varying capacities. We                                       prise 500 problems from the MATH dataset, 1, 000
utilized GPT-4o as the LLM to perform the auto-                                        problems from the GSM8K dataset, and the entire
formalization process.                                                                 training set from the CollegeMath dataset. We
                            Llama 3.1                 Llama 3.0                    GPT-4o           Deepseek-Math
                     MATH      G8K      CM     MATH      G8K      CM       MATH      G8K    CM     MATH   G8K    CM
      ZS-CoT@1       49.1      85.4     52.6   26.1      79.9     31.3      76.9     95.0   73.4   40.8   80.1   48.4
      Majority@5     50.5      87.8     54.3   24.8      80.7     29.6      78.9     95.7   73.9   39.3   81.7   48.7
    Skywork (ORM)    48.9      90.2     53.2   30.5      76.0     36.6      76.7     88.6   73.1   43.6   76.8   50.7
    ArmoRM (ORM)     55.1      90.0     57.1   32.3      86.1     37.3      79.3     95.5   74.7   48.6   86.6   53.5
    Shepherd (PRM)   58.1      90.2     58.3   34.7      86.4     40.4      79.8     95.8   73.5   49.7   87.1   55.0
    RLHFlow (PRM)    51.7      89.9     53.6   29.6      86.2     36.5      78.7     95.3   74.2   44.4   86.3   50.9
     LSTM (Ours)     55.1      88.7     55.9   33.0      84.3     36.6      78.9     95.5   73.8   48.2   83.3   51.1
      Safe (Ours)    60.0      90.8     59.0   36.3      87.4     43.4      80.4     96.0   74.2   52.4   87.6   55.4
       Pass@5        70.8      95.5     72.3   48.9      92.5     52.9      87.8     97.0   81.5   62.6   92.1   67.1

Table 1: The experimental results of various models on the MATH-500, GSM8K and CollegeMath datasets are
presented, denoted as MATH, G8K and CM, respectively. LSTM and Safe denote our proposed methodologies.
Pass@5 indicates the probability of correct for at least one of the five samples, representing the performance
upperbound across all Best-of-N strategies.


query the reasoning LLM to answer these prob-                   the success rate of theorem proving and the com-
lems and the outputs are compared with the ground               putational overhead involved. Current endeavors
truth to assess the accuracy of the generated reason-           in automated theorem proving typically address
ing trajectories. The sampled reasoning trajectories            comprehensive mathematical problems, often em-
are subsequently utilized to train the LSTM model.              ploying tree search strategies and substantial search
State Aggregator Training Setup The LSTM                        budgets.
model utilized in this study features a tiny num-                  Although employing a large search budget with
ber of parameters, comprising two layers and a                  thousands of searches can significantly increase
hidden size of 64. The model was trained with a                 the success rate of proving theorems for com-
batch size of 32 and a learning rate of 0.0001 over             plete mathematical problems, the high computa-
the course of 200 epochs.                                       tional cost of searching renders such approaches
                                                                impractical for stepwise validation. Therefore,
4.2     Results
                                                                we employed a computationally efficient setting
The experimental results are presented in Table 1.              by opting not to use the complex Monte Carlo
We find that: (1) Despite the high parameter effi-              tree search (MCTS) strategy employed by the
ciency of our LSTM model and its minimal training               DeepSeek-Prover-V1.5 (Xin et al., 2024b). We
data requirements, its performance is comparable                found that DeepSeek-Prover-V1.5 with a sample
to that of other SOTA ORMs and PRMs. (2) Our                    budget of 16 is sufficient to prove over 80% of the
Safe framework, which integrates LSTM with a                    statements in FormalStepdescribed below. There-
PRM, consistently outperforms almost every other                fore, we adopted DeepSeek-Prover-V1.5 with a
baseline model across all datasets and reasoning                sample budget of 16 but without MCTS as the
models. (3) Our approach demonstrates significant               default theorem-proving strategy for other exper-
improvements on two more challenging datasets,                  iments. For additional evaluation on FormalStep,
namely MATH-500 and CollegeMath. We attribute                   please refer to Appendix H.
the mediocre improvement on the GSM8K dataset to
the low difficulty level of the dataset, which has
resulted in data imbalance; a detailed discussion of            5.2      The FormalStep Dataset
this issue is provided in the following section.
                                                                Construction of FormalStep We randomly sam-
5     Discussion                                                pled 500 problems from the training part of MATH
                                                                dataset and employed Llama3.1 as the reason-
5.1     Theorem Proving Strategy                                ing model to generate reasoning trajectories, sub-
For each reasoning trajectory, we need to formalize             sequently passing these trajectories to the auto-
and validate each step. As a result, the quantity of            formalization pipeline. The 30, 809 theorems gen-
theorems that require proving is quite significant.             erated from this auto-formalization process were
As such, it is imperative to strike a balance between           designated as a benchmark for “step correctness
              Geo     Num     Alg     Comb    Oth     Total   For additional quality evaluations regarding auto-
 Frequency     873    11515   5525    9414    3482    30809   formalization, please refer to Appendix G.
  S Length    147.5    79.5   107.8   125.0   112.8   104.2
  P Length     51.1    36.4    39.8    49.8    25.5    41.0
 Proof Rate    72.3    82.1    81.7    81.4    79.1    81.2   5.4   Train & Inference Cost
                                                              In our analysis, we find that our method demon-
Table 2: Statistical information of the FormalStep
dataset, including category distributions, statement          strates high data efficiency. About 2, 000 reasoning
lengths, proof lengths and proof rates. The abbrevi-          trajectories sampled from 500 questions, are gen-
ations Geo, Num, Alg, Comb, Oth refer to Geometry,            erally sufficient to train an effective LSTM aggre-
Number Theory, Algebra, Combinatorics, Others, re-            gator, which is significantly less than the PRM800K
spectively.                                                   dataset, which contains approximately 800k step-
                                                              level labels across 75k solutions (Lightman et al.,
                                                              2024), as well as the Math-Shepherd datasets,
theorem proving”, denoted as FormalStep1 .
                                                              which comprise over 445k reasoning strategies
   Following common mathematical competition
                                                              (Wang et al., 2024b), which highlights the data
classification methods (Zheng et al., 2021), we cat-
                                                              efficiency of our proposed methodology. We hy-
egorized the Lean 4 statements into four types: ge-
                                                              pothesize that this discrepancy arises because the
ometry, number theory, algebra, and combinatorics.
                                                              LSTM aggregator focuses on pattern recognition
We employed the LLM-as-a-judge approach using
                                                              tasks centered on state sequences rather than di-
the GPT-4o-mini model to classify the FormalStep
                                                              rectly processing natural language. We also find
dataset. The statistics in Table 2 reveal that while
                                                              that training an effective LSTM becomes challeng-
previous automated theorem proving works in Lean
                                                              ing when there is a disproportionate ratio of correct
(e.g., miniF2F (Zheng et al., 2021), FIMO (Liu
                                                              to incorrect samples within the reasoning trajec-
et al., 2023)) primarily focused on Number The-
                                                              tories. For instance, the four tested models are
ory and Algebra problems, our dataset contains a
                                                              approaching saturation in the GSM8K dataset, result-
substantial proportion of Combinatorics statements
                                                              ing in a minimal presence of incorrect samples in
and a smaller but notable portion of Geometry prob-
                                                              the training set. Consequently, the LSTM model
lems. Notably, Geometry and Combinatorics state-
                                                              struggled to learn the patterns of incorrect examples
ments exhibit significantly longer statement lengths
                                                              effectively, which may account for the relatively
and proof lengths, highlighting the inherent chal-
                                                              modest performance improvements observed with
lenges in these categories.
                                                              our approach on the GSM8K dataset.
5.3    Auto-Formalization of Single Steps                        Regarding inference costs, we recognize that
                                                              our methodology requires more computational re-
Our experiment indicates that the statement gen-              sources. Specifically, each inference step entails a
erated by the auto-formalization process can en-              maximum of 3 auto-formalization attempts and up
compass not only numerical computations and                   to 16 theorem proving attempts, with each attempt
solving systems of equations — tasks that can be              necessitating a query to an LLM. During the cura-
easily tackled by general-purpose programming                 tion of FormalStep, our analysis revealed that, on
languages such as Python — but also verify spe-               average, approximately 1.02 automated formaliza-
cific mathematical properties that are frequently             tion attempts and 6.97 automated theorem proving
overlooked by general-purpose programming lan-                attempts are conducted. If we reduce the maximum
guages.                                                       number of ATP attempts from 16 to 8 — while still
   These mathematical properties include whether a            achieving a proof success rate exceeding 80% —
specific condition is sufficient or necessary, or prop-       the average number of theorem proving attempts
erties like “an integer is divisible by three if and          can be further decreased to 2.67. This suggests that
only if the sum of its digits is divisible by three”.         the LLM queries of our single-step validation is
This highlights the advantages of employing formal            approximately 4–8x greater than that of PRMs.
verification, as utilizing a domain-specific language            We increase the sample count for other RMs
like Lean facilitates a more efficient expression             to compare two scaling strategies: increasing the
of mathematical concepts. Additional examples                 sample count with a weaker RM or increasing com-
of auto-formalization are provided in Appendix F.             putational resources to verify each sample. The
   1
    Since these theorems were obtained through auto-          results presented in Figure 4 indicate that the scal-
formalization, they may not necessarily be provable.          ing patterns during the testing phase vary among
                                                      0.450                                                                                      0.54
       0.60                                                                                          0.81
                                                      0.425                                                                                      0.52
       0.58                                                                                          0.80
Accuracy




                                               Accuracy




                                                                                              Accuracy




                                                                                                                                          Accuracy
                                                      0.400                                                                                      0.50
       0.56                                                                                          0.79
                                                      0.375                                                                                      0.48
                                                                                                     0.78
       0.54                                           0.350                                                                                      0.46
                                                                                                     0.77                                        0.44
       0.52                                           0.325                                          0.76
                         Math-Shepherd (PRM)          0.300             Math-Shepherd (PRM)                         Math-Shepherd (PRM)          0.42             Math-Shepherd (PRM)
       0.50              ArmoRM (ORM)                                   ArmoRM (ORM)                 0.75           ArmoRM (ORM)                 0.40             ArmoRM (ORM)
                                                      0.275                                          0.74 0
              0    10 20 30 40 50 60                          0    10 20 30 40 50 60                          10 20 30 40 50 60                         0   10 20 30 40 50 60
                    Sample Count                                    Sample Count                               Sample Count                                  Sample Count
                  (a) Llama 3.1                                   (b) Llama 3.0                               (c) GPT-4o                             (d) DeekSeek-Math

 Figure 4: Scaling Best-of-N with Math-Shephed PRM and ArmoRM ORM. The red dashed line indicates the
 accuracy of Safe using Best-of-N@5, while the plot demonstrates the variations in the accruacy of the selection of
 Best-of-N as N increases when utilizing the ORM or the PRM.


       MATH-500 Acc                  L 3.1       L 3.0             GPT-4o        DSM              of the reasoning trajectory. We employ the same
     Skywork (ORM1 )                  48.9         30.5             76.7         43.6             metric, Best-of-N@5, to assess performance.
     ArmoRM (ORM2 )                   55.1         32.3             79.3         48.6                The results of the ablation experiments are pre-
     Shepherd (PRM1 )                 58.1         34.7             79.8         49.7
     RLHFlow (PRM2 )                  51.7         29.6             78.7         44.4             sented in the Table 3. The results indicate that
                                                                                                  PRMs and ORMs do benefit from model ensem-
       ORM1 ⊕ PRM1                    58.6         35.2             79.6         49.7
       ORM1 ⊕ PRM2                    55.9         34.1             79.3         47.6             bling; however, the improvement is not as sub-
       ORM2 ⊕ PRM1                    59.6         35.6             79.8         50.1             stantial as that achieved by Safe. Although the
       ORM2 ⊕ PRM2                    57.1         33.8             79.8         48.2
                                                                                                  performance of our LSTM is comparable to that
           LSTM (Ours)                55.1         33.0             78.9         48.2             of an ORM, Safe consistently outperforms ensem-
            Safe (Ours)               60.0         36.3             80.4         52.4
                                                                                                  ble models of all evaluated combinations, notably
 Table 3: An ablation analysis that combines various                                              achieving a 2.3% (50.1% → 52.4%) increase in the
 ORMs and PRMs. The accuracy is assessed using the                                                performance of DeepSeek-Math model. We posit
 BoN@5 metric. The abbreviations L 3.1, L 3.0, GPT-4o,                                            that the synergistic effect between the PRM and
 and DSM refer to Llama 3.1, Llama 3.0, GPT-4o, and                                               our formal step verifier is grounded in the comple-
 Deepseek-Math model, respectively.                                                               mentarity of prospective and retrospective, as well
                                                                                                  as formal and informal, verification methods.
 different LLMs. For stronger models such as GPT-
                                                                                                  6       Conclusion
 4o and Llama 3.1, it is advantageous to allocate
 additional computational resources during the veri-                                              In this paper, we introduce a retrospective step-
 fication process to achieve enhanced performance.                                                aware formal mathematical verification framework,
 Conversely, for less powerful models like Llama                                                  termed Safe, which utilizes auto-formalization and
 3.0, the quality of the sampled reasoning trajecto-                                              automated theorem proving to assign one of four
 ries is subpar. Therefore, increasing the sample                                                 distinct states to each step within the reasoning tra-
 count with a weaker yet more cost-effective RM                                                   jectory of LLMs when addressing mathematical
 may remain an effective strategy for these models.                                               problems. To the best of our knowledge, this is the
                                                                                                  first approach to employ formal mathematical lan-
 5.5          Synergistic Effect between PRM and
                                                                                                  guage Lean 4 for validating the correctness of LLM
              Formal Step Verifier
                                                                                                  generated mathematical reasoning expressed in nat-
 Our main experiment indicates a synergistic ef-                                                  ural language. The formal mathematical proofs
 fect between the PRM and our formal step veri-                                                   offer interpretable evidence for the correctness of
 fier. This observation prompts us to explore the                                                 natural-language reasoning steps. A benchmark
 potential existence of a similar synergistic effect                                              consisting of 30, 809 formal statements, referred to
 between PRMs and ORMs. We employed a similar                                                     as FormalStep, will be released to facilitate auto-
 strategy to integrate the PRM and the ORM. The                                                   formalization and automated theorem proving in
 integration method employed aligns with our Safe                                                 low-compute environments. Extensive experiments
 approach, wherein both models independently eval-                                                conducted across various LLMs and mathematical
 uate the same reasoning trajectory. Following this                                               datasets illustrate the effectiveness of our methods
 evaluation, a coefficient is applied to combine the                                              and highlight the potential role of formal mathe-
 scores, resulting in a comprehensive assessment                                                  matical language in enhancing LLM reasoning.
Limitations                                                Neural-symbolic learning and reasoning: A survey
                                                           and interpretation 1. In Neuro-Symbolic Artificial
The correlation between the output of the Lean 4           Intelligence: The State of the Art, pages 1–51. IOS
REPL and the final evaluation scores appears to be         press.
relatively indirect. Furthermore, the scoring mech-
                                                         Tom Brown, Benjamin Mann, Nick Ryder, Melanie
anism based on LSTM neural network parameters              Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind
still lacks perfect interpretability. While verifica-      Neelakantan, Pranav Shyam, Girish Sastry, Amanda
tion is conducted at a stepwise level, our method          Askell, et al. 2020. Language models are few-shot
does not provide a precise reward score for each           learners. Advances in neural information processing
                                                           systems, 33:1877–1901.
step due to the noise introduced by the current lim-
itations of both auto-formalization and automated        Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian,
theorem proving. To address this challenge, we pro-        Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias
pose identifying critical proof steps by examining         Plappert, Jerry Tworek, Jacob Hilton, Reiichiro
the correlation between intermediate verification          Nakano, et al. 2021. Training verifiers to solve math
                                                           word problems. arXiv preprint arXiv:2110.14168.
states and the final outcome through systematic
analysis of the compact LSTM architecture’s pa-          Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey,
rameters and decision mechanisms.                          Abhishek Kadian, Ahmad Al-Dahle, Aiesha Letman,
   Theoretically, our proposed Safe is capable of          Akhil Mathur, Alan Schelten, Amy Yang, Angela
                                                           Fan, et al. 2024. The llama 3 herd of models. arXiv
fulfilling dual roles: it can function as a verifier
                                                           preprint arXiv:2407.21783.
during the testing phase and as a reward model dur-
ing the reinforcement training process. However,         Bin Feng, Zequn Liu, Nanlan Huang, Zhiping Xiao,
the increased computational overhead may present           Haomiao Zhang, Srbuhi Mirzoyan, Hanwen Xu,
frictions for the direct application of the current        Jiaran Hao, Yinghui Xu, Ming Zhang, et al. 2024.
                                                           A bioactivity foundation model using pairwise meta-
method in reinforcement learning scenarios. More-          learning. Nature Machine Intelligence, 6(8):962–
over, as shown in Figure 4, in some instances, when        974.
verification costs are similar, the performance gains
may not be significant. Therefore, we identify the       Jesse Michael Han, Jason Rute, Yuhuai Wu, Edward
following two points as areas for future work: to           Ayers, and Stanislas Polu. 2022. Proof artifact co-
                                                            training for theorem proving with language models.
alleviate the computational resource demands of             In International Conference on Learning Representa-
the existing method, and to integrate formal lan-           tions.
guage verification into the reinforcement learning
pipeline.                                                Shibo Hao, Yi Gu, Haodi Ma, Joshua Hong, Zhen
                                                           Wang, Daisy Wang, and Zhiting Hu. 2023. Rea-
                                                           soning with language model is planning with world
Acknowledgments                                            model. In Proceedings of the 2023 Conference on
                                                           Empirical Methods in Natural Language Processing,
This paper is partially supported by grants from the
                                                           pages 8154–8173.
National Key Research and Development Program
of China with Grant No. 2023YFC3341203 and               Alexander Havrilla, Sharath Chandra Raparthy, Christo-
the National Natural Science Foundation of China           foros Nalmpantis, Jane Dwivedi-Yu, Maksym Zhu-
(NSFC Grant Number 62276002).                              ravinskyi, Eric Hambro, and Roberta Raileanu. 2024.
                                                           Glore: When, where, and how to improve llm reason-
                                                           ing via global and local refinements. In Forty-first
                                                           International Conference on Machine Learning.
References
Janice Ahn, Rishu Verma, Renze Lou, Di Liu, Rui          Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul
  Zhang, and Wenpeng Yin. 2024. Large language             Arora, Steven Basart, Eric Tang, Dawn Song, and
  models for mathematical reasoning: Progresses and        Jacob Steinhardt. 2021. Measuring mathematical
  challenges. ArXiv preprint, abs/2402.00157.              problem solving with the math dataset. NeurIPS.

Jeremy Avigad, Leonardo De Moura, and Soonho Kong.       S Hochreiter. 1997. Long short-term memory. Neural
   2021. Theorem proving in lean.                          Computation MIT-Press.

Tarek R Besold, Artur d’Avila Garcez, Sebastian Bader,   Jie Huang and Kevin Chen-Chuan Chang. 2023. To-
  Howard Bowman, Pedro Domingos, Pascal Hit-                wards reasoning in large language models: A survey.
  zler, Kai-Uwe Kühnberger, Luis C Lamb, Priscila           In Findings of the Association for Computational
  Machado Vieira Lima, Leo de Penning, et al. 2021.         Linguistics: ACL 2023, pages 1049–1065.
Yinya Huang, Xiaohan Lin, Zhengying Liu, Qingxing         Jia Li, Ge Li, Xuanming Zhang, Yihong Dong, and
  Cao, Huajian Xin, Haiming Wang, Zhenguo Li, Linqi          Zhi Jin. 2024. Evocodebench: An evolving code
  Song, and Xiaodan Liang. 2024. Mustard: Mastering          generation benchmark aligned with real-world code
  uniform synthesis of theorem and proof data. In            repositories. arXiv preprint arXiv:2404.00599.
  The Twelfth International Conference on Learning
  Representations.                                        Hunter Lightman, Vineet Kosaraju, Yuri Burda, Harri-
                                                            son Edwards, Bowen Baker, Teddy Lee, Jan Leike,
Aaron Hurst, Adam Lerer, Adam P Goucher, Adam               John Schulman, Ilya Sutskever, and Karl Cobbe.
  Perelman, Aditya Ramesh, Aidan Clark, AJ Os-              2024. Let’s verify step by step. In The Twelfth Inter-
  trow, Akila Welihinda, Alan Hayes, Alec Radford,          national Conference on Learning Representations.
  et al. 2024. Gpt-4o system card. arXiv preprint
  arXiv:2410.21276.                                       Chengwu Liu, Jianhao Shen, Huajian Xin, Zhengying
                                                            Liu, Ye Yuan, Haiming Wang, Wei Ju, Chuanyang
Albert Qiaochu Jiang, Sean Welleck, Jin Peng Zhou,          Zheng, Yichun Yin, Lin Li, et al. 2023. Fimo: A chal-
  Timothee Lacroix, Jiacheng Liu, Wenda Li, Mateja          lenge formal dataset for automated theorem proving.
  Jamnik, Guillaume Lample, and Yuhuai Wu. 2022.            arXiv preprint arXiv:2309.04295.
  Draft, sketch, and prove: Guiding formal theorem
  provers with informal proofs. In The Eleventh Inter-    Chris Yuhao Liu, Liang Zeng, Jiacai Liu, Rui Yan, Ju-
  national Conference on Learning Representations.          jie He, Chaojie Wang, Shuicheng Yan, Yang Liu,
                                                            and Yahui Zhou. 2024. Skywork-reward: Bag of
Dongwei Jiang, Marcio Fonseca, and Shay B Cohen.            tricks for reward modeling in llms. arXiv preprint
  2024. Leanreasoner: Boosting complex logical rea-         arXiv:2410.18451.
  soning with lean. In Proceedings of the 2024 Con-
  ference of the North American Chapter of the Asso-      Jianqiao Lu, Yingjia Wan, Zhengying Liu, Yinya Huang,
  ciation for Computational Linguistics: Human Lan-          Jing Xiong, Chengwu Liu, Jianhao Shen, Hui Jin,
  guage Technologies (Volume 1: Long Papers), pages          Jipeng Zhang, Haiming Wang, et al. 2024. Process-
  7490–7503.                                                 driven autoformalization in lean 4. arXiv preprint
                                                             arXiv:2406.01940.
John Jumper, Richard Evans, Alexander Pritzel, Tim
  Green, Michael Figurnov, Olaf Ronneberger, Kathryn      Ali Madani, Ben Krause, Eric R Greene, Subu Subrama-
  Tunyasuvunakool, Russ Bates, Augustin Žídek, Anna         nian, Benjamin P Mohr, James M Holton, Jose Luis
  Potapenko, et al. 2021. Highly accurate pro-              Olmos, Caiming Xiong, Zachary Z Sun, Richard
  tein structure prediction with alphafold. nature,         Socher, et al. 2023. Large language models generate
  596(7873):583–589.                                        functional protein sequences across diverse families.
                                                            Nature Biotechnology, 41(8):1099–1106.
John Jumper, Richard Evans, Alexander Pritzel, Tim
  Green, Michael Figurnov, Kathryn Tunyasuvunakool,       The mathlib Community. 2019. The lean mathematical
  Olaf Ronneberger, Russ Bates, Augustin Žídek, Alex        library. CoRR, abs/1910.09336.
  Bridgland, et al. 2020. Alphafold 2. Fourteenth Crit-
  ical Assessment of Techniques for Protein Structure     Leonardo de Moura and Sebastian Ullrich. 2021. The
  Prediction.                                               lean 4 theorem prover and programming language. In
                                                            Automated Deduction–CADE 28: 28th International
Takeshi Kojima, Shixiang (Shane) Gu, Machel Reid, Yu-       Conference on Automated Deduction, Virtual Event,
  taka Matsuo, and Yusuke Iwasawa. 2022. Large lan-         July 12–15, 2021, Proceedings 28, pages 625–635.
  guage models are zero-shot reasoners. In Advances in      Springer.
  Neural Information Processing Systems, volume 35,
  pages 22199–22213. Curran Associates, Inc.              Theo Olausson, Alex Gu, Ben Lipkin, Cedegao Zhang,
                                                            Armando Solar-Lezama, Joshua Tenenbaum, and
Xin Lai, Zhuotao Tian, Yukang Chen, Senqiao Yang, Xi-       Roger Levy. 2023. Linc: A neurosymbolic approach
  angru Peng, and Jiaya Jia. 2024. Step-dpo: Step-wise      for logical reasoning by combining language models
  preference optimization for long-chain reasoning of       with first-order logic provers. In Proceedings of the
  llms. CoRR.                                               2023 Conference on Empirical Methods in Natural
                                                            Language Processing, pages 5153–5176.
Nathan Lambert, Valentina Pyatkin, Jacob Morrison,
  LJ Miranda, Bill Yuchen Lin, Khyathi Chandu,            Liangming Pan, Alon Albalak, Xinyi Wang, and
  Nouha Dziri, Sachin Kumar, Tom Zick, Yejin Choi,          William Wang. 2023. Logic-lm: Empowering large
  Noah A. Smith, and Hannaneh Hajishirzi. 2024. Re-         language models with symbolic solvers for faithful
  wardbench: Evaluating reward models for language          logical reasoning. In Findings of the Association
  modeling. Preprint, arXiv:2403.13787.                     for Computational Linguistics: EMNLP 2023, pages
                                                            3806–3824.
Guillaume Lample, Timothee Lacroix, Marie-Anne
  Lachaux, Aurelien Rodriguez, Amaury Hayat,              Stanislas Polu, Jesse Michael Han, Kunhao Zheng, Man-
  Thibaut Lavril, Gabriel Ebner, and Xavier Martinet.        tas Baksys, Igor Babuschkin, and Ilya Sutskever.
  2022. Hypertree proof search for neural theorem            2022. Formal mathematics statement curriculum
  proving. Advances in neural information processing         learning. In The Eleventh International Conference
  systems, 35:26337–26349.                                   on Learning Representations.
Stanislas Polu and Ilya Sutskever. 2020. Generative        Peiyi Wang, Lei Li, Zhihong Shao, Runxin Xu, Damai
   language modeling for automated theorem proving.          Dai, Yifei Li, Deli Chen, Yu Wu, and Zhifang Sui.
   arXiv preprint arXiv:2009.03393.                          2024b. Math-Shepherd: Verify and Reinforce LLMs
                                                             Step-by-step without Human Annotations. In Pro-
David Rein, Betty Li Hou, Asa Cooper Stickland, Jack-        ceedings of the 62nd Annual Meeting of the Associa-
  son Petty, Richard Yuanzhe Pang, Julien Dirani, Ju-        tion for Computational Linguistics (Volume 1: Long
  lian Michael, and Samuel R Bowman. 2023. Gpqa: A           Papers), pages 9426–9439, Bangkok, Thailand. As-
  graduate-level google-proof q&a benchmark. arXiv           sociation for Computational Linguistics.
  preprint arXiv:2311.12022.
                                                           Xiaoxuan Wang, Ziniu Hu, Pan Lu, Yanqiao Zhu,
Md Kamruzzaman Sarker, Lu Zhou, Aaron Eberhart,              Jieyu Zhang, Satyen Subramaniam, Arjun R Loomba,
 and Pascal Hitzler. 2022. Neuro-symbolic artificial         Shichang Zhang, Yizhou Sun, and Wei Wang.
 intelligence: Current trends. Ai Communications,            2023b. Scibench: Evaluating college-level scientific
 34(3):197–209.                                              problem-solving abilities of large language models.
                                                             arXiv preprint arXiv:2307.10635.
Amrith Setlur, Chirag Nagpal, Adam Fisch, Xinyang
 Geng, Jacob Eisenstein, Rishabh Agarwal, Alekh            Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten
 Agarwal, Jonathan Berant, and Aviral Kumar. 2024.            Bosma, brian ichter, Fei Xia, Ed H. Chi, Quoc V Le,
 Rewarding progress: Scaling automated process ver-           and Denny Zhou. 2022. Chain of thought prompt-
 ifiers for llm reasoning. In The Thirteenth Interna-         ing elicits reasoning in large language models. In
 tional Conference on Learning Representations.              Advances in Neural Information Processing Systems.
                                                           Yuhuai Wu, Albert Qiaochu Jiang, Wenda Li, Markus
Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu,
                                                             Rabe, Charles Staats, Mateja Jamnik, and Christian
  Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan
                                                             Szegedy. 2022. Autoformalization with large lan-
  Zhang, YK Li, Y Wu, et al. 2024. Deepseekmath:
                                                             guage models. Advances in Neural Information Pro-
  Pushing the limits of mathematical reasoning in open
                                                             cessing Systems, 35:32353–32368.
  language models. arXiv preprint arXiv:2402.03300.
                                                           Huajian Xin, Daya Guo, Zhihong Shao, Zhizhou Ren,
Jianhao Shen, Yichun Yin, Lin Li, Lifeng Shang, Xin          Qihao Zhu, Bo Liu, Chong Ruan, Wenda Li, and
   Jiang, Ming Zhang, and Qun Liu. 2021. Generate            Xiaodan Liang. 2024a. Deepseek-prover: Advancing
   & Rank: A Multi-task Framework for Math Word              theorem proving in llms through large-scale synthetic
   Problems. In Findings of the Association for Com-         data. arXiv preprint arXiv:2405.14333.
   putational Linguistics: EMNLP 2021, pages 2269–
   2279, Punta Cana, Dominican Republic. Association       Huajian Xin, ZZ Ren, Junxiao Song, Zhihong Shao,
   for Computational Linguistics.                            Wanjia Zhao, Haocheng Wang, Bo Liu, Liyue Zhang,
                                                             Xuan Lu, Qiushi Du, et al. 2024b. Deepseek-prover-
Zhengyang Tang, Xingxing Zhang, Benyou Wang, and             v1. 5: Harnessing proof assistant feedback for re-
  Furu Wei. 2024. Mathscale: Scaling instruction tun-        inforcement learning and monte-carlo tree search.
  ing for mathematical reasoning. In Forty-first Inter-      CoRR.
  national Conference on Machine Learning.
                                                           Jing Xiong, Jianhao Shen, Ye Yuan, Haiming Wang,
Amitayush Thakur, George Tsoukalas, Yeming Wen,               Yichun Yin, Zhengying Liu, Lin Li, Zhijiang Guo,
 Jimmy Xin, and Swarat Chaudhuri. 2024. An in-                Qingxing Cao, Yinya Huang, et al. 2023. Trigo:
 context learning agent for formal theorem-proving.           Benchmarking formal mathematical proof reduction
 In First Conference on Language Modeling.                    for generative language models. In Proceedings of
                                                              the 2023 Conference on Empirical Methods in Natu-
Amitayush Thakur, Yeming Wen, and Swarat Chaud-               ral Language Processing, pages 11594–11632.
 huri. 2023. A language-agent approach to formal
 theorem-proving. In The 3rd Workshop on Mathe-            Wei Xiong, Hanning Zhang, Nan Jiang, and Tong Zhang.
 matical Reasoning and AI at NeurIPS’23.                     2024. An implementation of generative prm. https:
                                                            //github.com/RLHFlow/RLHF-Reward-Modeling.
Haiming Wang, Ye Yuan, Zhengying Liu, Jianhao Shen,
                                                           Xin Xu, Shizhe Diao, Can Yang, and Yang Wang. 2024a.
  Yichun Yin, Jing Xiong, Enze Xie, Han Shi, Yujun
                                                             Can we verify step by step for incorrect answer de-
  Li, Lin Li, Jian Yin, Zhenguo Li, and Xiaodan Liang.
                                                             tection? arXiv preprint arXiv:2402.10528.
  2023a. DT-solver: Automated theorem proving with
  dynamic-tree sampling guided by proof-level value        Xin Xu, Tong Xiao, Zitong Chao, Zhenya Huang, Can
  function. In Proceedings of the 61st Annual Meeting        Yang, and Yang Wang. 2024b. Can llms solve
  of the Association for Computational Linguistics (Vol-     longer math word problems better? arXiv preprint
  ume 1: Long Papers), pages 12632–12646, Toronto,           arXiv:2405.14804.
  Canada. Association for Computational Linguistics.
                                                           Xin Xu, Jiaxin Zhang, Tianhao Chen, Zitong Chao,
Haoxiang Wang, Wei Xiong, Tengyang Xie, Han Zhao,            Jishan Hu, and Can Yang. 2025. Ugmathbench: A
  and Tong Zhang. 2024a. Interpretable preferences           diverse and dynamic benchmark for undergraduate-
  via multi-objective reward modeling and mixture-of-        level mathematical reasoning with large language
  experts. In EMNLP.                                         models. arXiv preprint arXiv:2501.13766.
Yuchen Yan, Jin Jiang, Yang Liu, Yixin Cao, Xin           A      Prompt for Auto-Formalization
  Xu, Xunliang Cai, Jian Shao, et al. 2024. S 3 c-
  math: Spontaneous step-level self-correction makes      The following prompt is utilized to instruct an
  large language models better mathematical reasoners.    LLM in the task of auto-formalization. It con-
  arXiv preprint arXiv:2409.01524.                        sists of four components: a task description, de-
Junwei Yang, Hanwen Xu, Srbuhi Mirzoyan, Tong             tailed instructions, a comparison of key differences
  Chen, Zixuan Liu, Zequn Liu, Wei Ju, Luchen Liu,        between Lean 3 and Lean 4, and a selection of
  Zhiping Xiao, Ming Zhang, et al. 2024a. Poison-         manually curated few-shot examples. The steps
  ing medical knowledge using large language models.      included in the few-shot examples are derived from
  Nature Machine Intelligence, 6(10):1156–1168.
                                                          PRM800K dataset. We observed that during auto-
Kaiyu Yang, Gabriel Poesia, Jingxuan He, Wenda Li,        formalization, LLMs may conflate the syntactical
  Kristin Lauter, Swarat Chaudhuri, and Dawn Song.        elements of Lean 3 with those of Lean 4. To ad-
  2024b. Formal mathematical reasoning: A new fron-
  tier in ai. arXiv preprint arXiv:2412.16075.            dress this issue, we revised the prompts by incorpo-
                                                          rating key syntactical distinctions between Lean 3
Kaiyu Yang, Aidan Swope, Alex Gu, Rahul Chala-            and Lean 4, thereby guiding the model to generate
  mala, Peiyang Song, Shixing Yu, Saad Godil, Ryan J      outputs that are consistent with Lean 4.
  Prenger, and Animashree Anandkumar. 2023. Le-
                                                          Given a question and the steps to answer it, you need to determine
  andojo: Theorem proving with retrieval-augmented               whether the final step of the answer may involve a hallucination
  language models. Advances in Neural Information         ∗
                                                                 that requires theorem proving in Lean 4.
                                                            If the step is simple and intuitive, and you are confident that it
  Processing Systems, 36:21573–21612.                     ∗
                                                                 does not need verification, please answer False.
                                                            However, you need to verify ∗ ∗ ALL NUMERICAL ∗ ∗ operations, no
                                                                 matter how simple or intuitive they may seem.
                                                          ∗
                                                            If the step has a certain leap that is not very intuitive and may
Huaiyuan Ying, Zijian Wu, Yihan Geng, Jiayu Wang,                involve a hallucination, please provide a Lean theorem that can
  Dahua Lin, and Kai Chen. 2024a. Lean work-              ∗
                                                                 verify the step.
                                                            This Lean 4 theorem should support the step; if the Lean 4 theorem
  book: A large-scale lean problem set formalized                can be proven, then the step is correct and does not involve a
                                                                 hallucination.
  from natural language math problems. arXiv preprint     ∗
                                                            Ensure that the Lean theorems you provide ∗ ∗ CONFORM ∗ ∗ to the
                                                                 syntax of Lean 4, and ∗ ∗ AVOID USING NATURAL LANGUAGE ∗ ∗ to
  arXiv:2406.03847.                                       ∗
                                                                 describe properties.
                                                            Do ∗ ∗ NOT ∗ ∗ provide a proof method for the theorem; you can use
                                                                 "sorry" as a placeholder.
                                                          ∗
Huaiyuan Ying, Shuo Zhang, Linyang Li, Zhejian Zhou,        Output the formalized theorem of the final step or False, and do ∗ ∗
                                                                 NOT ∗ ∗ output any other content or predict next step.
  Yunfan Shao, Zhaoye Fei, Yichuan Ma, Jiawei Hong,       ∗
                                                            Note that each step is derived from the previous ones, so the theorem
                                                                 may require referencing information from the question or earlier
  Kuikun Liu, Ziyi Wang, et al. 2024b. Internlm-math:            steps.
  Open math large language models toward verifiable       Note that Lean 4 is not backward compatible with Lean 3.
                                                          ∗
  reasoning. arXiv preprint arXiv:2402.06332.               Type constants are now in UpperCamelCase, for example, ‵ Nat‵ and ‵
                                                                 List‵ . Many variables in Mathlib have also changed to
                                                                 UpperCamelCase, such as ‵ fintype‵ becoming ‵ Fintype‵ .
                                                          ∗
Longhui Yu, Weisen Jiang, Han Shi, Jincheng Yu,             Lambda expressions now use ‵ =>‵ as the separator. For example, ‵ fun x
                                                                 => x‵ is the identity function, instead of ‵ λ x, x‵ .
  Zhengying Liu, Yu Zhang, James T Kwok, Zhen-
                                                          ### Question:
  guo Li, Adrian Weller, and Weiyang Liu. 2023.           Let \[f(x) = \left\{
                                                          \begin{array}{cl} ax+3, &\text{ if }x>2, \\
  Metamath: Bootstrap your own mathematical ques-         x-5 &\text{ if } -2 \le x \le 2, \\
                                                          2x-b &\text{ if } x <-2.
  tions for large language models. ArXiv preprint,        \end{array}
                                                          \right.\]
  abs/2309.12284.                                         Find $a+b$ if the piecewise function is continuous (which means that its
                                                                 graph can be drawn without lifting your pencil from the paper).

Eric Zelikman, Yuhuai Wu, Jesse Mu, and Noah Good-        ### Step to be verified:
                                                          For the piecewise function to be continuous, the cases must "meet" at $
   man. 2022. Star: Bootstrapping reasoning with rea-            2$ and $-2$.
                                                          ### Lean:
   soning. Advances in Neural Information Processing      False

  Systems, 35:15476–15488.                                ### Step to be verified:
                                                          For example, $ax+3$ and $x-5$ must be equal when $x=2$.
                                                          This implies $a(2)+3=2-5$, which we solve to get $2a=-6 \Rightarrow
                                                                  a=-3$.
Kunhao Zheng, Jesse Michael Han, and Stanislas Polu.      ### Lean:
                                                          ‵‵‵
                                                              lean
  2021. minif2f: a cross-system benchmark for for-        theorem test
  mal olympiad-level mathematics. In International          (a x: R)
                                                            (h0 : a ∗ x + 3 = x - 5)
  Conference on Learning Representations.                   (h1 : x = 3):
                                                            (a = (-3)) := by sorry
                                                          ‵‵‵

Jin Peng Zhou, Charles Staats, Wenda Li, Christian        . . . (More steps have been omitted.)
   Szegedy, Kilian Q Weinberger, and Yuhuai Wu. 2024.     ### Question
                                                          <question>
   Don’t trust: Verify-grounding llm quantitative rea-
                                                          ### Steps that do not require verification:
   soning with autoformalization. In ICLR.                <answer>
                                                          ### Step to be verified:
                                                          <step>
Terry Yue Zhuo, Minh Chien Vu, Jenny Chim, Han Hu,        ### Lean:

  Wenhao Yu, Ratnadira Widyasari, Imam Nur Bani
  Yusuf, Haolan Zhan, Junda He, Indraneil Paul, et al.
  2024. Bigcodebench: Benchmarking code genera-
                                                          B      Prompt for LLM-as-a-Judge
  tion with diverse function calls and complex instruc-          Evaluation
  tions. arXiv preprint arXiv:2406.15877.
                                                          The following prompt is utilized to instruct an LLM
                                                          to evaluate the semantic alignment between the rea-
soning step and the auto-formalized Lean 4 state-                          I want to find the smallest positive integer $X$ that
                                                                                   satisfies the given conditions . I know that any
ment.                                                                              multiple of 3 has the form $3k$ for some integer $k$ ,
                                                                                   so $X$ has the form $3k + 2$. I also know that any
Given a mathematical problem, its step-by-step reasoning chain, and a              multiple of 5 has the form $5n$ for some integer $n$ ,
       Lean 4 statement, you need to verify whether the Lean 4 statement           so the number with the same units digit as $X$ has the
       corresponds to the final reasoning step.                                    form $5n + 4$. Since the units digits of $X$ and $5n +
If they are properly aligned, then proving the Lean 4 statement
       mathematically validates the correctness of the final step.                 4$ are the same , I can equate them and get $3k + 2 \
If they ’dont match, the Lean 4 statement is irrelevant to the final               equiv 5n + 4 \ pmod {10} $. This means that the difference
       ’steps correctness.                                                          between $3k + 2$ and $5n + 4$ is a multiple of 10. I
The three categories are ["good", "fair", "poor"].                                 can simplify this difference by subtracting 4 from both
Do ∗ ∗ NOT ∗ ∗ respond with any other characters.                                   sides and get $3k - 2 \ equiv 5n \ pmod {10} $. Now I need
### Problem:                                                                        to find the smallest values of $k$ and $n$ that make
<problem>                                                                          this equation true . I can try some values of $k$ and
                                                                                   see what they imply for $n$ . If $k = 0$ , then $3k - 2 =
### Chain-of-thoughts:                                                              -2$ and $5n = -2 + 10 m$ for some integer $m$ . This
<cot>
                                                                                   implies that $n = -0.4 + 2m$ , which is not an integer .
### Step to Verify:                                                                So $k = 0$ does not work . If $k = 1$ , then $3k - 2 = 1$
<step>                                                                              and $5n = 1 + 10 m$ for some integer $m$ . This implies
                                                                                   that $n = 0.2 + 2m$ , which is also not an integer . So
### Lean 4 Statement:
<statement>                                                                        $k = 1$ does not work either . If $k = 2$ , then $3k - 2
                                                                                   = 4$ and $5n = 4 + 10 m$ for some integer $m$ . This
Which category does this statement fall into? Please respond with one of           implies that $n = 0.8 + 2m$ , which is again not an
       ["good", "fair", "poor"].                                                   integer . So $k = 2$ does not work as well . If $k = 3$ ,
                                                                                   then $3k - 2 = 7$ and $5n = 7 + 10 m$ for some integer
                                                                                   $m$ . This implies that $n = 1.4 + 2m$ , which is not an
  The following prompt is employed to instruct an                                  integer . So $k = 3$ does not work . If $k = 4$ , then $3k
                                                                                    - 2 = 10 $ and $5n = 10 + 10 m$ for some integer $m$ .
LLM to classify Lean statements into one of four                                   This implies that $n = 2 + 2m$ , which is an integer . So
                                                                                    $k = 4$ works . This means that the smallest value of
predefined categories.                                                             $X$ is $3k + 2 = 3 \ cdot 4 + 2 = 14 $.
                                                                           ### Steps :
Given a Lean 4 theorem, you need to identify its category.                 ``` json
The five categories are ["geometry", "number theory", "algebra",           [
       "combinatorics", "others"].                                              "I want to find the smallest positive integer $X$ that
∗
  Do ∗ ∗ NOT ∗ ∗ respond with any other characters.
                                                                                        satisfies the given conditions ." ,
Theorem:                                                                        "I know that any multiple of 3 has the form $3k$ for
<statement>                                                                             some integer $k$ , so $X$ has the form $3k + 2$ ." ,
                                                                                "I also know that any multiple of 5 has the form $5n$
To which category does this theorem belong?
Your answer should be one of ["geometry", "number theory", "algebra",                   for some integer $n$ , so the number with the same
       "combinatorics", "others"].                                                      units digit as $X$ has the form $5n + 4$ ." ,
                                                                                " Since the units digits of $X$ and $5n + 4$ are the same
                                                                                        , I can equate them and get $3k + 2 \\ equiv 5n + 4
                                                                                        \\ pmod {10} $ ." ,
                                                                                " This means that the difference between $3k + 2$ and $5n
C     Decomposition Specifications                                                       + 4$ is a multiple of 10." ,
                                                                                "I can simplify this difference by subtracting 4 from
                                                                                        both sides and get $3k - 2 \\ equiv 5n \\ pmod {10} $
Heuristic Rules In this approach, we utilize pe-                                        ." ,
                                                                                " Now I need to find the smallest values of $k$ and $n$
riods or line breaks as delimiters to partition the                                     that make this equation true ." ,
                                                                                "I can try some values of $k$ and see what they imply
reasoning process into independent steps. However,                                      for $n$ ." ,
                                                                                " If $k = 0$ , then $3k - 2 = -2$ and $5n = -2 + 10 m$ for
we have observed that this simplistic rule may re-                                      some integer $m$ ." ,
                                                                                " This implies that $n = -0.4 + 2m$ , which is not an
sult in excessively fragmented steps and may also                                       integer ." ,
                                                                                " So $k = 0$ does not work ." ,
lead to erroneous decomposition. For instance, a                                " If $k = 1$ , then $3k - 2 = 1$ and $5n = 1 + 10 m$ for
                                                                                        some integer $m$ ." ,
period could serve as a decimal point rather than a                             " This implies that $n = 0.2 + 2m$ , which is also not an
separator between sentences.                                                            integer ." ,
                                                                                " So $k = 1$ does not work either ." ,
LLM In-Context Learning This approach in-                                       " If $k = 2$ , then $3k - 2 = 4$ and $5n = 4 + 10 m$ for
                                                                                        some integer $m$ ." ,
volves utilizing an LLM to decompose the reason-                                " This implies that $n = 0.8 + 2m$ , which is again not an
                                                                                         integer ." ,
ing process into distinct, independent steps. We ran-                           " So $k = 2$ does not work as well ." ,
                                                                                " If $k = 3$ , then $3k - 2 = 7$ and $5n = 7 + 10 m$ for
domly select accurate reasoning processes from the                                      some integer $m$ ." ,
                                                                                " This implies that $n = 1.4 + 2m$ , which is not an
PRM800K training set, which consists of manually                                        integer ." ,
                                                                                " So $k = 3$ does not work ." ,
annotated stepwise data, and utilize the stepwise                               " If $k = 4$ , then $3k - 2 = 10 $ and $5n = 10 + 10 m$ for
                                                                                        some integer $m$ ." ,
partitioning method derived from these responses                                " This implies that $n = 2 + 2m$ , which is an integer ." ,
                                                                                " So $k = 4$ works ." ,
as few-shot examples. The model is directed to pro-                             " This means that the smallest value of $X$ is $3k + 2 =
                                                                                        3 \\ cdot 4 + 2 = 14 $ ."
duce a JSON-formatted array with each element                              ]
                                                                           ```
representing a string that corresponds to an inde-
                                                                           ... ( More examples have been omitted .)
pendent step. Below are the step decomposition
                                                                           ### Solution :
few-shot prompts.                                                          < solution >
                                                                           ### Steps :
Given a solution to a problem , you need to break down the
      solution into individual logical steps .
You have to answer the question in JSON format .
The answer must be an Array , where each element is a string
      representing a logically independent step .
You can only split the answer simply , and you cannot make
      any modifications to the answer , even if the answer is
      incorrect .
You must include the complete solution without any missing                    We prioritize the LLM in-context learning set-
      steps .
Here are some examples .                                                   ting; if the JSON output is not parsable, we revert
### Solution :                                                             to the heuristic rules-based approach as a fallback.
                                                                     Distribution of Steps by State and Correctness
                                                                                                   14179
                                                                 14000
                              MATH BoN@5
                                                                 12000
                                                                                                           10838
        LSTM only                  55.1                          10000
        PRM only                   55.2




                                                         Count
                                                                 8000
        Weighted Sum               59.6
        Weighted Mul (Safe)        60.0                          6000                       5655
        Min                        57.0                                              4394
                                                                 4000                                                               3450
        Max                        58.2                                                                              2342
                                                                 2000    1366 1428
Table 4: The ablation study results comparing score                 0




                                                                          Formalization

                                                                          Formalization




                                                                             Successful

                                                                             Successful
                                                                         No Verification

                                                                         No Verification




                                                                                                                   Proof Failed

                                                                                                                                  Proof Failed
ensembling strategies on Llama3.1 (MATH-500).




                                                                                Proof

                                                                                Proof
                                                                                False
                                                                            Required

                                                                            Required


                                                                                 True




                                                                                                                                     False
                                                                                                                      True
                                                                              Failed

                                                                              Failed
                                                                               False
                                                                               True




                                                                              False
                                                                              True
D    Score Ensembling Strategies                                                     State and Correctness
The design of weighted multiplication was inten-         Figure 5: The distribution of steps by state and their
tionally kept simple and intuitive while proving ef-     correctness. Out of a total of 43, 652 steps, 30, 809
fective in practice. The key motivation is that when     steps (72.2%) were auto-formalized into valid Lean 4
either the PRM score or LSTM verification score          statements. Among these, 25, 017 statements (81.2%)
approaches 0 (indicating likely errors), the com-        were successfully proven by DeepSeek-Prover-V1.5.
bined score should similarly reflect low confidence.        We can observe that the likelihood of ultimately
During development, we empirically evaluated four        arriving at the correct answer for steps classified
ensemble variants:                                       as “Proof Successful” is relatively high, at 56.7%.
                                                         In contrast, the correctness for steps categorized
    • Weighted summation
                                                         under the “Proof Failed” state is significantly lower,
    • Weighted multiplication (our final choice)
                                                         at 40.4%. However, the noise introduced during
    • Max selection
                                                         the processes of auto-formalization and automated
    • Min selection
                                                         theorem proving complicates the direct assessment
   The ablation results in Table 4 show that             of the overall correctness of reasoning trajectories.
weighted multiplication achieved the best perfor-
                                                         F        Extra Examples of Auto-Formalization
mance. This aligns with our design principle
that strong negative signals from either component       The following example validates a theorem: an
should significantly impact the final score.             integer whose sum of digits is divisible by three
                                                         can be inferred to be divisible by three itself.
E    Analysis of State Distributions                     ### Problem:
                                                         Let $N$ be the units digit of the number $
Each step has one of four potential states that in-          21420N$. Which nonzero value of $N$ makes
dicate whether the particular step of the reasoning          this number divisible by $6$?
trajectory contain flaws. Ideally, each step within      ### Reasoning Step by an LLM:
                                                         Divisibility by 3: A number is divisible by 3
a correct reasoning trajectory should correspond             if the sum of its digits is divisible by 3.
to either the state of “Proof Successful” or “No
                                                         ### Formal Statement & Proof:
Verification Required”, and a step classified under      theorem divisible_by_3
the state of “Proof Failed” signifies that this step       (n N : N)
                                                           (h0 : n = 2 + 1 + 4 + 2 + 0 + N)
has inherent flaws. However, due to the noise intro-       (h1 : n % 3 = 0):
                                                           (21420 + N) % 3 = 0 := by
duced during the processes of auto-formalization           rw [h0 ] at h1
and automated theorem proving, this is not true for        simp_all [Nat.add_mod, Nat.mul_mod,
                                                              Nat.mod_mod]
all reasoning trajectories.                                <;> aesop
   During the curation of FormalStep, we analyzed
the distribution of states produced by our pipeline         The following example is intended to demon-
across these trajectories. The statistical results are   strate the sufficient and necessary conditions be-
presented in Figure 5. Notably, the most com-            tween equations. This mathematical property may
mon state identified is “Proof Successful”, sug-         be challenging to articulate within the framework
gesting that the majority of the steps can be auto-      of general-purpose programming languages.
formalized into valid Lean statements and be tack-
led by automated theorem provers.
                                                                             1.0




                                                     Statements Proof Rate
### Problem:                                                                                                    24724          25173     25417
                                                                                                       24054
                                                                             0.8           22559
What real values of $x$ are not in the domain of                                   19361                                                  376
                                                                                                                                354
                                                                             0.6                        318      329
$f(x)=\frac{1}{|x^2+3x-4|+|x^2+9x+20|}$?                                                    286
                                                                                    259
                                                                             0.4
### Reasoning Step by an LLM:                                                0.2                                         DeepSeek-Prover-V1.5
This means that the denominator will be equal                                                                            COPRA with GPT-4o
    to zero if and only if $x+4=0$, regardless                               0.0
                                                                                     20                  22       23
                                                                                             21                                  24        25
    of the values of $x-1$ and $x+5$.                                                                  Max Attempts
### Formal Statement & Proof:
theorem test                                          Figure 6: The proof rates of two SOTA theorem provers
  (x: R):
  (|x + 4| ∗ |x - 1| + |x + 4| ∗ |x + 5| = 0) ↔       on FormalStep. The numbers indicate the total quantity
     (x + 4 = 0) := by                                of statements that have been successfully proved. Note
  constructor                                         that COPRA is significantly more resource-intensive
  intro h
  cases′ le_total 0 (x + 4) with h0 h0 <;>            due to its reliance on GPT-4o; therefore, it is tested on
    cases′ le_total 0 (x - 1) with h1 h1 <;>          a randomly selected subset of 500 statements, while
      cases′ le_total 0 (x + 5) with h2 h2 <;>        DeepSeek-Prover-V1.5 is evaluated on full FormalStep,
        simp_all only [abs_of_nonneg,
    abs_of_nonpos, add_left_neg, add_right_neg,       comprising a total of 30, 809 statements.
          add_zero, zero_add, mul_zero,
    zero_mul, mul_one, mul_neg, neg_mul,
    neg_neg,
          mul_right_comm, mul_left_comm] <;>          prompt utilized in the LLM-as-a-Judge evalution
        nlinarith                                     process is available in Appendix B.
  intro h
  rw [h]
  simp                                                                             Good              Fair               Poor           Total
                                                                24,938 (80.9%)                     138 (0.4%)   5733 (18.6%)           30,809
   The following example illustrates that the Lean
4 language is capable of performing some tasks        Table 5: The evaluation results of semantic alignment
typically associated with general-purpose program-    on the FormalStep using the LLM-as-a-Judge method.
ming languages, such as numerical computation.
### Problem:                                             The results in Table 5 show 80.9% of formalized
A shirt′ s sale price is marked $\$14.40$, which      theorems maintain good semantic alignment, which
    is $60\%$ off the original price. How many
    dollars was the original price of the shirt?      aligns with both recent work 2 (72% for FormL4
### Reasoning Step by an LLM:
                                                      (Lu et al., 2024) and 93.5% for Lean Workbook
So, the original price of the shirt was $36.          (Ying et al., 2024a)) and our manual observations
### Formal Statement & Proof:                         during the design phase. We use an LSTM ag-
theorem test                                          gregator rather than rejecting all unprovable steps
  (sale_price original_price: R)
  (h0 : sale_price = 14.40)                           outright, therefore our method should be robust to
  (h1 : sale_price = 0.4 ∗ original_price):           imperfect consistency.
  (original_price = 36) := by
  rw [h0 ] at h1
  ring_nf at h1                                       H                            Additional Evaluation of FormalStep
  linarith
                                                     We conducted experiments with DeepSeek-Prover-
                                                     V1.5 and COPRA combined with GPT-4o under
G   Additional Quality Evaluation                    varying sample budgets, and the results are il-
    Regarding Auto-formalization                     lustrated in Figure 6. Our results indicate that
                                                     both provers are capable of effectively address-
Regarding accuracy (here defined as whether the      ing the ATP task of proving single-step statements
auto-formalized statements comply with the Lean 4    when provided with a substantial computational
syntax (Ying et al., 2024a)), 72.2% (30, 809 out     budget. DeepSeek-Prover-V1.5 exhibits a signif-
of 43, 652) of steps were successfully formalized    icantly greater performance advantage over the
into Lean 4-compliant statements when construct-     agent-based COPRA in low-compute scenarios.
ing the FormalStep. Concerning consistency (here
defined as semantic alignment between success-
fully formalized statements and original natural          2
                                                            Note that these recent studies report results for conven-
language statements (Ying et al., 2024a)), we em-     tional auto-formalization tasks (i.e., translating problem state-
                                                      ments), thus precluding direct comparison with our novel auto-
ployed GPT-4o-mini to evaluate our FormalStep         formalization approach (i.e., translating individual solution
using an LLM-as-a-Judge approach. The complete        steps).
