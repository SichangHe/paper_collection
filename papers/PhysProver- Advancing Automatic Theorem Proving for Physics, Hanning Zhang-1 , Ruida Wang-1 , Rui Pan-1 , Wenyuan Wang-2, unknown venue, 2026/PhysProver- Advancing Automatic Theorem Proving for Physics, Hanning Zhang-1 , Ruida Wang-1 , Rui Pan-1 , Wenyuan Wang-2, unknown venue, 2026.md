                                                PhysProver: Advancing Automatic Theorem Proving for Physics

                                                         Hanning Zhang*1 , Ruida Wang*1 , Rui Pan*1 , Wenyuan Wang*2 ,
                                                                         Bingxu Meng1 , Tong Zhang1
                                                                   1
                                                                     University of Illinois Urbana-Champaign
                                                                               2
                                                                                 Rutgers University
                                                       {hanning5, ruidaw, ruip4, bingxum2, tozhang}@illinois.edu
                                                                      ww462@scarletmail.rutgers.edu


                                                               Abstract                               domain in machine learning research (Newell and
                                                                                                      Simon, 1956). With the recent advancements in
                                             The combination of verifiable languages and
                                                                                                      Large Language Models (LLMs), much research
arXiv:2601.15737v1 [cs.AI] 22 Jan 2026




                                             LLMs has significantly influenced both the
                                             mathematical and computer science commu-                 has investigated their applications in formal theo-
                                             nities because it provides a rigorous founda-            rem proving. They explored domains from training
                                             tion for theorem proving. Recent advance-                foundation models (Lin et al., 2025b; Ren et al.,
                                             ments in the field provide foundation mod-               2025; Wang et al., 2025c) and specialized agent
                                             els and sophisticated agentic systems pushing            framework (Wang et al., 2025d; Chen et al., 2025b;
                                             the boundaries of formal mathematical rea-               Varambally et al., 2025). Among these, math theo-
                                             soning to approach the natural language ca-
                                                                                                      rem proving in Lean4 (Moura and Ullrich, 2021a)
                                             pability of LLMs (Chen et al., 2025b). How-
                                             ever, little attention has been given to the for-        has emerged as one of the most extensively studied
                                             mal physics reasoning, which also heavily re-            areas (Wang et al., 2024; Lin et al., 2025a; Xin
                                             lies on similar problem-solving and theorem-             et al., 2024). Researchers typically start from a
                                             proving frameworks. To solve this problem,               general-purpose LLM, employing Supervised Fine-
                                             this paper presents, to the best of our knowl-           Tuning (SFT) and Reinforcement Learning (RL) to
                                             edge, the first approach to enhance formal the-          enhance the formal reasoning capability. This ap-
                                             orem proving in the physics domain. We com-
                                                                                                      proach has achieved strong results on formal math
                                             pose a dedicated dataset PhysLeanData for the
                                             task. It is composed of theorems sampled from            benchmarks, such as MiniF2F (Zheng et al., 2022)
                                             PhysLean (Tooby-Smith, 2025) and data gener-             and PutnamBench (Tsoukalas et al., 2024)1 .
                                             ated by a conjecture-based formal data genera-              Previous works have demonstrated that develop-
                                             tion pipeline. In the training pipeline, we lever-       ing expert models for Lean4 theorem proving de-
                                             age DeepSeek-Prover-V2-7B, a strong open-                mands substantial training data and a large amount
                                             source mathematical theorem prover, and ap-              of GPU hours. For instance, DeepSeek-Prover (Xin
                                             ply Reinforcement Learning with Verifiable Re-
                                                                                                      et al., 2024) applies a 120B math-related tokens
                                             wards (RLVR) to train our model PhysProver.
                                             Comprehensive experiments demonstrate that,              continue pretraining and 8M formal statements
                                             using only ∼5K training samples, PhysProver              with proofs to train an expert prover. Similarly,
                                             achieves an overall 2.4% improvement in mul-             Goedel-Prover (Lin et al., 2025a) applies expert
                                             tiple sub-domains. Furthermore, after formal             iteration on more than 1 million formal statements.
                                             physics training, we observe 1.3% gains on the           Despite these advancements, formal theorem prov-
                                             MiniF2F-Test benchmark, which indicates non-             ing faces significant challenges due to a scarcity
                                             trivial generalization beyond physics domains
                                                                                                      of high-quality data that is able to give the model
                                             and enhancement for formal math capability
                                             as well. The results highlight the effectiveness         a general formal reasoning capability, rather than
                                             and efficiency of our approach, which provides           focusing on a narrow field (Li et al., 2025).
                                             a paradigm for extending formal provers out-                While significant progress has been made in
                                             side mathematical domains. To foster further             mathematical theorem proving, the formal physics
                                             research, we will release both our dataset and           domain remains largely overlooked. Physics, with
                                             model to the community.                                  its reliance on rigorous mathematical foundations
                                         1   Introduction                                             and formal derivations, offers a natural yet under-
                                                                                                      explored extension to formal reasoning. Li et al.
                                         Formal reasoning has long been recognized as a
                                                                                                         1
                                         cornerstone of human intelligence and a critical                    https://github.com/hanningzhang/PhysProver


                                                                                                  1
Figure 1: Physics Prover Framework: (a) Data Generation Stage: the training set comprises 5,541 physics
statements from both PhysLean (Tooby-Smith, 2025) and synthetic lemmas from Claude-4.5-Sonnet, where the
latter are further filtered by Lean syntax and proof existence checks. (b) Self-Evolving Stage: after obtaining the
training set, GRPO (Shao et al., 2024) is adopted to train the base prover models, with reward signals of proof
correctness provided by Lean.

(2025) highlights that SOTA theorem-proving mod-             provers on the testing dataset. Furthermore, when
els perform poorly in physics-related tasks but fail         tested on the Out-of-Distribution (OOD) MiniF2F
to propose methods for improvement.                          benchmark (Zheng et al., 2022), PhysProver
   To settle this gap, we, as far as we are concerned,       achieved over 1% of improvement compared to
take the first step toward enhancing theorem prov-           the base model under pass@16. It demonstrates
ing in the physics domain by constructing a spe-             the effectiveness of our approach and shows that
cialized data pipeline and employing Reinforce-              physics dataset training can enhance the formal
ment Learning with Verifiable Rewards (RLVR).                math capability of the model.
The overview of our framework can be found in                   We summarize our contribution as follows:
Figure 1. Specifically, we collect foundational the-             1. Introducing the first methods specifically de-
orems and lemmas from the open-source repository                    signed to train the formal theorem provers for
of PhysLean (Tooby-Smith, 2025), which contains                     physics.
Lean4-based results across advanced physics do-
mains such as Quantum Field Theory and String                    2. Developing and releasing a compact and com-
Theory. The extracted data, along with their head-                  prehensive small dataset, along with a conjec-
ers, are divided into the training and testing sets.                ture synthesis pipeline for physical theorems
To augment the training dataset, we apply Claude-                   to benefit the research community.
4.5 to generate additional conjectures based on the
dataset. Subsequently, we apply formal LLMs to                   3. Training a formal physics prover that outper-
annotate these conjectures, thereby formulating the                 forms the SOTA model and achieves superior
Basic Physics Lean training dataset, which contains                 performance in both physics and mathemati-
approximately 5K training samples and 250 testing                   cal theorem proving.
samples.                                                     2     Related Works
   With the dataset, we leverage RLVR (Lambert
et al., 2025) to enhance physical theorem-proving            2.1    Formal Math Reasoning
capability using the GRPO algorithm. Our evalua-             Formal math reasoning involves representing math-
tion demonstrates consistent improvement across              ematical components in a computer-verifiable for-
multiple physics domains and achieves a 2.4% of              mat. It reduces the ambiguity and establishes a
overall improvements compared to SOTA math                   rigorous foundation for logical reasoning. Over

                                                         2
the past decades, researchers have developed nu-           reasoning is one key field that receives significant
merous Formal Languages (FLs) based on two pri-            attention. In the context of benchmarks, early com-
mary theoretical frameworks. The first relies on           prehensive benchmarks, such as SciBench (Wang
dependent type languages, such as Lean (De Moura           et al., 2023) and GPQA (Rein et al., 2024), evalu-
et al., 2015; Moura and Ullrich, 2021b) and                ate college-level scientific problem-solving across
Coq (Coq, 1996), where formal verification is              multiple scientific fields, including physics. More
achieved through a small kernel to perform type            recently, physics benchmarks have emerged at mul-
checking. The second line utilizes higher-order            tiple difficulty levels: UGPhysics (Xu et al., 2025)
logic to quantify functions and predicates. This           presents 5,520 undergraduate-level bilingual prob-
line of work is represented by languages such              lems that advanced thinking models are hard to
as Isabelle (Paulson, 1994), HOL, and HOL                  solve; OlympiadBench (He et al., 2024) introduces
Light (Harrison, 2009). Among the above lan-               8,476 Olympiad-level problems with multi-module
guages, Lean4 (Moura and Ullrich, 2021b) has               inputs; and recent HiPhO (Yu et al., 2025) compiles
gained significant attention due to its expressive-        the latest 13 Physics Olympiad exams in 2024-2025
ness and extensive Mathlib4 repository, which en-          with human-aligned evaluation.
compasses almost all major mathematical domains.              On the model training side, researchers began
   The rise of LLMs has accelerated the advance-           exploring the potential for LLMs as physics rea-
ments in formal proving tasks. Researchers have            soning tools from an early stage. Early works
compiled extensive datasets of mathematical the-           have demonstrated that LLMs can solve complex
orems and proofs(Wang et al., 2025c; Lin et al.,           word problems that require calculation and infer-
2025a; Dong and Ma, 2025), which provide a ro-             ence (Ding et al., 2023). Such capability can be
bust foundation for model training. Building on            further enhanced by Reinforcement Learning from
these resources, increasingly sophisticated mod-           Human Feedback (RLHF) (Anand et al., 2024) or
els have emerged. Early efforts, such as Ex-               simple multi-agent collaboration (Pang et al., 2025).
pert Iteration (Polu et al., 2022), employed it-           Recent works apply RLVR on natural language
erative annotation using LLMs to enhance the               physics problems, with P1 (Chen et al., 2025a)
training data. Open-source frameworks like                 achieving gold-level IPhO performance. However,
DeepSeek-Prover (Xin et al., 2024) and Theorem-            with a lack of datasets and training methods, de-
Llama (Wang et al., 2024) further advanced the             veloping LLMs for formal physics reasoning is
formal provers. More recently, RLVR has enabled            relatively understudied currently (Li et al., 2025).
Long CoT training for formal theorem proving,
which works like MA-LoT (Wang et al., 2025c),              3     Methodology
Kimina-Prover (Wang et al., 2025a), DeepSeek-
Prover-V2 (Ren et al., 2025), and Goedel-Prover-           3.1    Seed Dataset Collection
V2 (Lin et al., 2025b), achieving notable progress.        We construct a lemma–proof dataset from the
The emergence of agentic frameworks, such as               PhysLean GitHub repository (Tooby-Smith, 2025)
Hilbert (Varambally et al., 2025) and Seed-Prover-         by extracting all provable lemmas from .lean files
V1 (Chen et al., 2025c), achieves notable progress         along with their preceding formal headers. The
by enabling multi-agent theorem decomposition              lemma statements with context serve as inputs,
and sub-goal proofs. The latest works apply agen-          while the corresponding proof scripts serve as out-
tic RL to push LLMs’ formal reasoning capabil-             puts. We filter the samples to retain only those with
ity closer to natural language proficiency (Chen           a total length under 4,096 tokens. The resulting
et al., 2025b). Despite these advancements, for-           corpus contains over 3,000 examples, which are
mal reasoning in physics remains an underexplored          randomly split into training and test sets at approx-
domain, representing a significant opportunity for         imately a 9:1 ratio, yielding 2,933 training and 250
future research.                                           test instances. The dataset spans a broad range of
                                                           domains in physics and mathematics, encompass-
2.2   LLM for Physics Reasoning                            ing classical and modern physics (e.g., classical
With the rapid development of general reasoning ca-        mechanics, electromagnetism, quantum mechan-
pabilities in LLMs, researchers are actively explor-       ics, and relativity) as well as advanced theoretical
ing the application of these models in more diverse        areas such as quantum field theory, string theory,
fields (Wang et al., 2025b). Among them, physics           and mathematical foundations. An example of the

                                                       3
collected data is shown in Figure 3.                              converting them to Lean4 statements using an auto-
                                                                  formalizer. However, auto-formalizers fail at this
3.2   Synthetic Data Generation                                   task due to the difficulty of identifying a uniform
To augment our dataset, we construct a conjec-                    header, which is caused by the complex depen-
ture generation and verification pipeline inspired                dencies in physical statements. Consequently, this
by STP (Dong and Ma, 2025). Specifically, we                      approach also yielded low success rates.
treat our initial data as seed data, denoted as
Dseed = {(hi , li , pi )}N                                        3.3   Self-Evolving Pipeline
                          i=1 , where hi , li , and pi are
the header, lemma, and corresponding proof of the                 We conduct Reinforcement Learning (RL) to lift
ith sample, and N is the total number of seed exam-               the performance on physics domain. Specifically,
ples. For each sample, we use Claude-4.5-Sonnet                   our experiments are mainly based on Group Rel-
(Anthropic, 2025) to generate 10 conjectures by                   ative Policy Optimization (GRPO) (Shao et al.,
providing the header–lemma pairs (hi , li ), yield-               2024). For each prompt x in the training set, they
ing 29,330 candidate statements. The prompting                    sample G (Group size) responses during the rollout
template is provided in Figure 7 in the Appendix.                 stage, and optimize the following objective:
   After collecting the conjectures, we apply a two-
stage pipeline to select well-formed and correct
statements. We first examine the syntactic cor-                   JGRPO (θ) = Ex∼D,{yi }G ∼πθ (·|x)
                                                                                          i=1       old
rectness of each conjecture. Specifically, for each                          
                                                                                    G         |yi |
                                                                             1
                                                                                   X 1 X                
conjecture cij , we append it to the correspond-                                                    min wi,t (θ)Âi,t ,
ing header hi to form Dc = {(hi , cij ) | i =                                  G       |yi |
                                                                                   i=1        t=1
1, . . . , N, j = 1, . . . , 10} and use the Lean ver-                                                            i
ifier to check whether the statement is well-formed.                          clip (wi,t (θ), 1 − ε, 1 + ε) Âi,t
This includes verifying that all variables are prop-                            − β DKL (πθ ∥πθref ) ,
erly defined and that all referenced definitions and
theorems exist. After this step, 6,971 conjectures                   where yi is the ith generated sequence of tokens,
remain, corresponding to a retention rate of 23.8%.               ε is the clip ratio. The importance ratio wi,t (θ) and
   The second stage examines the provability of                   the advantage Âi,t are calculated as follows:
conjectures. Given a conjecture with its corre-
sponding header, we leverage DeepSeek-Prover-                                              πθ (yi,t |x, yi,<t )
                                                                             wi,t (θ) =                           ,
V2-7B (Ren et al., 2025), Kimina-Prover-Distill-                                          πθold (yi,t |x, yi,<t )
8B (Wang et al., 2025a), and Goedel-Prover-V2-
8B (Lin et al., 2025b), to generate 16 proofs, pro-
                                                                                 r(x, yi ) − mean {r(x, yi )}G
                                                                                                                 
ducing response samples {(hi , cij , rp )}16   p=1 . A con-                                                  i=1
                                                                   Âi,t = Âi =                                   ,
                                                                                        std {r(x, yi )}G
                                                                                                           
jecture is deemed provable if                                                                          i=1

  ∃ p, 1 ≤ p ≤ 16 : Verify(hi , cij , rp ) = True                 respectively. And all the tokens in yi share the
                                                                  same advantage as Âi,t .
where Verify denotes the Lean verification result.                   The reward signal r(x, yi ) is provided by the
This process yields 2,608 verified conjectures, rep-              Lean verifier to guide the reinforcement learning
resenting an overall pipeline yield rate of 8.9%,                 process. Specifically, a score of 1 or 0 is presented
which is comparable to STP (Dong and Ma, 2025).                   to indicate whether the proof is correct or not. Be-
Combining these with the 2,933 seed training ex-                  cause of the symbolic nature of Lean, all verified
amples in Section 3.1 produces a total of 5,541                   proofs with reward 1 are correct, with no halluci-
training instances for our experiments.                           nation at all, which allows the model to learn the
   Notably, we also compared different propri-                    foundation of physics in a concrete and rigorous
etary models, including GPT-5 (OpenAI, 2025)                      way. To further reduce the difficulty of the learning
and Gemini-2.5-Pro (Google, 2025). However, the                   process, curriculum learning is employed, where
syntactically correct rates of their generated conjec-            the input statements (conjectures) are sorted based
tures were substantially lower than those produced                on their ground-truth proof lengths. This enables
by Claude. We additionally explored the approach                  easy-to-hard learning, encouraging prover models
of generating conjectures in natural language and                 to proceed in a bottom-up manner.

                                                              4
 Method                                            Classical     Particle & String      Relativity    Quantum Field Theory      Overall
 Proprietary Models
 GPT-5 (OpenAI, 2025)                               37.3%             13.4%              21.3%               35.2%              26.4%
 Claude-4.5-Sonnet (Anthropic, 2025)                52.9%             19.4%              29.5%               39.4%              34.4%
 Formal Math Provers
 Kimina-Prover-Distill-8B (Wang et al., 2025a)      35.3%             14.9%              29.5%               22.5%              24.8%
 Goedel-Prover-V2-8B (Lin et al., 2025b)            49.0%             19.4%              34.4%               28.2%              31.6%
 Deepseek-Prover-V2-7B (Ren et al., 2025)           54.9%             23.9%              37.7%               25.4%              34.0%
 Formal Physics Provers
 PhysProver                                      58.8% (+3.9%)   26.9% (+3.0%)        39.3% (+1.6%)      26.8% (+1.4%)       36.4% (+2.4%)


Table 1: Main experimental results. We evaluate all the models on PhysLeanData test set, which includes
Classical, Particle & String, Relativity, and Quantum Field Theory domains. The pass@16 accuracy is reported.


4     Experiments                                                         DeepSeek-Prover-V2-7B, Kimina-Prover-Distill-
                                                                          8B, and Goedel-Prover-V2-8B without any ad-
To evaluate our methodology, we use PhysLean-                             ditional training. We also include comparisons
Data to train popular Lean-based formal mathe-                            with strong proprietary systems, namely GPT-5
matics provers. Our experiments reveal that strong                        (OpenAI, 2025) and Claude-4.5-Sonnet (Anthropic,
mathematical reasoning models exhibit notable lim-                        2025). For all baselines, we use a fixed sampling
itations when handling formal physics problems,                           budget and report pass@16 accuracy, ensuring fair
underscoring the importance of domain-specific                            comparison under a consistent inference budget.
formal datasets and self-evolving strategies.                             For open-source provers, we use the prompt tem-
4.1     Experimental Setup                                                plate provided in Appendix D.1. For proprietary
                                                                          models, we employ a tailored Chain-of-Thought
4.1.1     Dataset and Tasks                                               (CoT) (Wei et al., 2023) prompt to encourage step-
Model performance is evaluated on the test set of                         by-step reasoning before generating the final proof.
PhysLeanData, which shares the same source as
the training set with a 9:1 train-test split. To ensure                   4.2        Implementation Details
fair comparison across models with different con-                         We directly apply Reinforcement Learning start-
text lengths, we retain only samples with prompt                          ing from the DeepSeek-Prover-V2-7B using verl
lengths under 4,096 tokens, resulting in 250 lem-                         (Sheng et al., 2025). Specifically, we apply
mas in the final evaluation set.                                          GRPO with rule-based rewards (Lambert et al.,
   For finer-grained analysis, we organize the test                       2025; DeepSeek-AI et al., 2025) to guide the self-
samples into four physics categories: Classical &                         evolving training. In particular, the Lean verifier
Foundational Physics, Particle & String Physics,                          with version 4.20.0 is integrated into the verl
Relativity & Spacetime, and Quantum Field The-                            framework for verifying the proofs. The reward
ory. This classification reflects distinct theoreti-                      score for each trajectory is calculated as follows:
cal frameworks and varying levels of required do-                                          (
main expertise. Further details are provided in                                              1 if Verify(x, yi ) = True
                                                                               r(x, yi ) =
Appendix B.                                                                                  0 otherwise
4.1.2     Models and Baselines                                            Additionally, if the proof contains sorry, admit,
We compare several popular open-source prover                             or apply? keywords, we directly assign a 0 for the
models, including DeepSeek-Prover-V2-7B (Ren                              reward score to avoid reward hacking. Furthermore,
et al., 2025), Kimina-Prover-Distill-8B (Wang                             to allow a smooth transition of difficulties during
et al., 2025a), and Goedel-Prover-V2-8B (Lin et al.,                      the learning process, curriculum learning (Parashar
2025b), all of which are strong formal theorem                            et al., 2025) is employed by sorting the lemma
provers tailored for mathematical domains. Since                          based on their ground-truth proof lengths.
DeepSeek-Prover-V2-7B performs the best among                                We train all models on 8×H200 GPUs with a
them, our experiments will focus on training the                          constant learning rate of 1e−6 and a batch size
DeepSeek prover to push the boundaries of open-                           of 256 for 2 epochs, where the training takes ap-
source models.                                                            proximately 8 hours. Notably, we do not have a
   For baselines, we first report the performance of                      warm-up stage with Supervised Fine-Tuning (SFT)

                                                                      5
because it degrades performance. This behavior                  Header and Context Lemmas
is investigated and further analyzed in Section 6.
We also investigate the Rejection-Sampling Fine-                import PhysLean.QFT.PerturbationTheory.WickAlgebra.
                                                                      NormalOrder.Lemmas
tuning method (Yuan et al., 2023; Dong et al., 2023)            import PhysLean.QFT.PerturbationTheory.WickAlgebra.
                                                                      TimeOrder
in Section 6.
                                                                namespace FieldSpecification
                                                                variable {F : FieldSpecification}
4.3   Experiment Results
                                                                def timeContract (φ ψ: F .FieldOp) : F .WickAlgebra
                                                                      :=
Our experimental results are presented in Table 1.                  T (ofFieldOp φ* ofFieldOp ψ) - T (ofFieldOp φ*
                                                                          ofFieldOp ψ)
We first observe that all existing models achieve rel-
atively low scores despite their proficiency in math-           lemma timeContract_eq_superCommute (φ ψ: F .FieldOp)
                                                                       :
ematical theorem proving, with none exceeding                       timeContract φψ= if timeOrderRel φψthen [anPart
                                                                            φ, ofFieldOp ψ]s
40% accuracy. Notably, even small open-source                       else S(F |>s φ, F |>s ψ) ·[anPart ψ, ofFieldOp
                                                                          φ]s := by
theorem prover models exhibit competitive accu-                   split_ifs
racy compared to the latest proprietary systems,                  ·rename_i h
                                                                    rw [timeContract_of_timeOrderRel _ _ h]
such as Claude-4.5-Sonnet and GPT-5. However,                     ·rename_i h
                                                                    rw [timeContract_of_not_timeOrderRel_expand _ _ h
proprietary models demonstrate different strengths                        ]
across physical domains compared to their open-
                                                                lemma timeContract_zero_of_diff_grade (φ ψ: F .
source counterparts. For instance, all open-source                     FieldOp) (h : (F |>s φ) ̸=(F |>s ψ)) :
                                                                    timeContract φψ= 0 := by
provers achieve below 30% accuracy on Quantum                     by_cases h1 : timeOrderRel φψ
Field Theory, whereas proprietary models exceed                   ·rw [timeContract_of_timeOrderRel _ _ h1]
                                                                    rw [
35%. This suggests that proprietary and open-                                superCommute_anPart_ofFieldOpF_diff_grade_zero
                                                                             ]
source models may be trained on different mixtures                  exact h
                                                                  ·rw [timeContract_of_not_timeOrderRel _ _ h1]
of physics data. We also investigated context length                rw [timeContract_of_timeOrderRel _ _ _]
in the Quantum Field Theory category and found                      rw [
                                                                             superCommute_anPart_ofFieldOpF_diff_grade_zero
that the average length is one-third longer than in                          ]
                                                                    simp only [instCommGroup.eq_1, smul_zero]
other domains. These findings align with those of                   exact h.symm
Li et al. (2025), suggesting that larger models such                have ht := IsTotal.total (r := F .timeOrderRel) φ
                                                                             ψ
as Claude demonstrate superior in-context learning                  simp_all
                                                                    ········
ability, thereby achieving better performance than
open-source models.
   Our trained model, PhysProver, substantially                 DeepseekProver + PhysProver
surpasses its formal mathematics prover counter-
                                                                /-- This lemma claims that the normal ordering of the
parts, consistently achieving gains across all cate-                   time-contracted product of any two field
gories. Specifically, on the most challenging do-                     operators φand ψis identically zero.-/
                                                                lemma normalOrder_timeContract (φ ψ: F .FieldOp) :
mains—Particle & String Physics—where all base-                     N (timeContract φψ) = 0 := by
                                                                  rw [timeContract_eq_superCommute]
lines exhibit low accuracy, our model still yields                split_ifs <;> simp_all [timeContract,
a notable improvement of 3.0%. These results                            superCommute_anPart_ofFieldOpF_diff_grade_zero
                                                                        ,
demonstrate the effectiveness of extending a math-                  smul_eq_zero, map_zero]
ematics prover to physics domains with only small
high-quality datasets. Moreover, the continued per-             DeepseekProver
formance gains suggest that current provers are far
from saturated, indicating that constructing high-              lemma normalOrder_timeContract (φ ψ: F .FieldOp) :
quality physics-specific datasets remains a promis-                 N (timeContract φψ) = 0 := by
                                                                  rw [timeContract_eq_superCommute]
ing direction                                                     split_ifs
                                                                  ·rw [normalOrder_ofFieldOp_pair_eq_zero]
   On top of that, the small 7B-sized PhysProver                    <;> simp_all [timeOrderRel_of_isContraction]
                                                                  ·rw [normalOrder_anPart_ofFieldOp_smul]
model outperforms both GPT-5 and Claude-4.5-                        <;> simp_all [timeOrderRel_of_isContraction]
Sonnet in terms of overall performance, which
shows the huge potential of small expert models in
specific domains of formal physics theorem prov-             Figure 2: Successful examples from the PhysProver
ing. This provides a promising path toward efficient         and failed proofs from the base model for the same
training of physics prover models.                           statements. PhysProver demonstrates better in-context
                                                             learning ability to make good usage of lemmas.

                                                         6
           Problem Category           Deepseek-Prover-V2          Deepseek-Prover-V2 + PhysLeanData
                                                Pass@16                                     Pass@16
                        IMO                    4/20 = 20.0%                                 4/20 = 20.0%
      Olympiad          AIME                   8/15 = 53.3%                                 7/15 = 46.7%
                        AMC                   25/45 = 55.6%                                25/45 = 55.6%
                     Algebra                  63/70 = 90.0%                                65/70 = 92.9%
       MATH
                   Number Theory              51/60 = 85.0%                                53/60 = 88.3%
                      Algebra                  8/18 = 44.4%                                 8/18 = 44.4%
       Custom      Number Theory                4/8 = 50.0%                                  4/8 = 50.0%
                     Induction                  4/8 = 50.0%                                  4/8 = 50.0%
           Overall Pass Rate               167/244 = 68.4%                              170/244 = 69.7%

    Table 2: Out-of-Distribution Generalization in Formal Math Proving on MiniF2F-Test (Zheng et al., 2022).


5     Analysis                                             curacy observed across all base models: their unfa-
                                                           miliarity with physics-specific lemmas and contex-
5.1    Improved In-Context Learning Through
                                                           tual structures impedes their ability to effectively
       Reinforcement Learning
                                                           utilize these resources for proof completion.
In this subsection, we provide a detailed analysis
of the performance gains achieved by PhysProver            5.2    Out-of-Distribution Generalization
through a comparative examination of proofs gen-
                                                           Surprisingly, we also observe that training on
erated by the baselines and our model. Figure 2
                                                           physics-centered problems yields notable gener-
presents an illustrative example from our test set
                                                           alization improvements in formal mathematical
along with the corresponding generations. The
                                                           theorem proving. In this subsection, we evaluate
header and lemmas constitute the context for phys-
                                                           our trained model on MiniF2F-Test (Zheng et al.,
ical theorem proving, where the lemmas serve as
                                                           2022), which comprises 244 Lean4 statements in
auxiliary tools during the proof process.
                                                           the mathematics domain, ranging from high school
   We observe that PhysProver consistently
                                                           competition problems to elementary undergraduate-
makes correct use of functions and lemmas,
                                                           level proofs. We partition the dataset into several
with successful applications highlighted in blue.
                                                           categories following Ren et al. (2025). For each
For instance, to prove the given conjecture, it
                                                           statement in MiniF2F-Test, we prompt both the
first applies timeContract_eq_superCommute,
                                                           baseline and our trained model to generate 16 tra-
followed by the function timeContract. Sub-
                                                           jectories and compute pass@16 accuracy. We use
sequently, the model correctly invokes super-
                                                           the same prompt template from the DeepSeek web-
Commute_anPart_ofFieldOpF_diff_grade_zero,
                                                           site 2 .
demonstrating effective utilization of contextual
                                                              As shown in Table 2, PhysProver overall
information. By synthesizing the knowledge
                                                           achieve comparable performance and even surpass
provided in the context, PhysProver successfully
                                                           their base versions. It is worth noticing that the
completes the proof.
                                                           improvement is not consistent across all categories.
   In contrast, while the base model initially ap-
                                                           For example, our model demonstrates meaning-
plies timeContract_eq_superCommute correctly,
                                                           ful gains on medium-level problems from MATH
it subsequently generates hallucinated content,
                                                           (Hendrycks et al., 2021). Conversely, more chal-
including non-existent lemmas such as nor-
                                                           lenging Olympiad-level problems may not benefit
malOrder_ofFieldOp_pair_eq_zero and timeOrder-
                                                           from GRPO training, as performance drops in the
Rel_of_isContraction (marked in red). These ob-
                                                           AIME category. These results reveal both the in-
servations suggest that the reinforcement learning
                                                           trinsic connections and distinctions between mathe-
process on PhysLeanData enhances performance
                                                           matical and physical theorem proving in Lean4. In
by enabling the model to better leverage contextual
information and comprehend domain-specific ter-               2
                                                               https://huggingface.co/deepseek-ai/
minology. This finding also accounts for the low ac-       DeepSeek-Prover-V2-7B


                                                       7
general, training on physics problems can enhance            and the GRPO model from our main experiments.
mathematical reasoning capabilities. However, dif-              To assess model uncertainty on both training and
ficult mathematics problems may demand substan-              test data, we measured the average perplexity of
tially different problem-solving skills that cannot          sampled responses conditioned on input prompts.
be directly acquired from physics-based training.            Given a prompt x from either the training or test set,
                                                             we sampled K = 16 responses yk from the model
6   Revisiting the Role of Supervised                        and computed the mean perplexity across these
    Fine-tuning                                              samples. We randomly selected 50 samples from
                                                             each of the training and test sets. The computation
We additionally investigated whether conducting              is defined as:
Supervised Fine-tuning (SFT) on PhysLeanData
                                                                              K
could enhance model performance on Physics, fol-                          1 X
                                                             P P L(x) =       P P L(y (k) ),          y (k) ∼ pθ (· | x)
lowing standard practice in training specialized                          K
                                                                             k=1
LLMs. However, we did not observe any improve-
ment on our test set after SFT. Instead, we observed         where
consistent performance degradation.                                           
                                                                                      |y|
                                                                                                                   
   Specifically, we first fine-tuned Deepseek-                                      1 X
                                                             P P L(y) = exp −                 log pθ (yt | y<t , x) .
Prover-V2-7B on PhysLeanData, where ground-                                        |y|
                                                                                         t=1
truth answers were either extracted from the
PhysLean library written by humans, or generated             This metric captures the model’s self-uncertainty:
by open-source provers with subsequent verifica-             lower values indicate that the model generates re-
tions. The training sample template follows the              sponses it considers likely and more relevant to the
RL prompt template in D.1, with loss computation             input, while higher values suggest greater variabil-
restricted to the completion portion. We then con-           ity or unfamiliarity with the prompt.
sider Rejection Sampling Fine-tuning, or Reward-                As shown in Table 4, the findings demonstrate
Ranked Fine-tuning (RAFT) (Dong et al., 2023;                that the average perplexity for DS-Prover-GRPO
Yuan et al., 2023), where we sample Deepseek-                and DS-Prover-RAFT is substantially lower than
Prover-V2-7B on the training set and retain only             that of DS-Prover-SFT on both the training and
the correct proofs as our new training set. We               test sets, which explains why GRPO and RAFT im-
fine-tuned Deepseek-Prover-V2-7B on both train-              prove the performance while SFT does not. These
ing sets for one epoch, using a learning rate of 5e−7        results suggest that although supervised fine-tuning
and a batch size of 32. They are denoted as DS-              directly maximizes the probability of target tokens,
Prover-SFT and DS-Prover-RAFT, respectively.                 it does not necessarily reduce model uncertainty,
   As shown in Table 3, for the DS-Prover-SFT, we            particularly for models such as DeepSeek-Prover
observe consistent performance degradation across            that have already undergone extensive domain-
all categories, with an average accuracy decline of          specific (MATH) training. This observation offers
6.4%. On the contrary, DS-Prover-RAFT demon-                 an important insight for further improving expert
strates an overall 1.6% improvement, with all other          models: supervised fine-tuning may not always be
3 categories increasing except Classical Physics.            necessary or optimal. On the contrary, using the Re-
We attribute this performance difference to the dis-         jection Sampling Fine-tuning method to collect and
tributional properties of the training data. The orig-       fine-tune on In-Distribution (ID) data could be a
inal PhysLeanData consists of human-written ex-              pratical solution. Additionally, direct application of
amples, which are Out-of-Distribution (OOD) with             reinforcement learning can serve as a viable alterna-
respect to the model’s generation capabilities. In           tive, particularly in low-resource settings. We also
contrast, Rejection Sampling yields In-Distribution          explore Reinforcement Learning after Rejection-
(ID) data that more closely aligns with the model’s          Sampling Fine-tuning in Appendix C, but do not
output distribution. Consequently, ID data may               observe improvements.
be easier for the model to learn from, leading to
                                                             7   Conclusion
improved performance.
   To gain a closer look into this phenomenon, prob-         In this paper, we present the first systematic effort
ing experiments are conducted to compare the un-             to advance formal theorem proving in the physi-
certainty of the SFT model, RAFT model (Table 3),            cal domain. We first introduce PhysLeanData, a

                                                         8
 Method                                Budget     Classical     Particle & String     Relativity     Quantum Field Theory      Overall
 Deepseek-Prover-V2-7B                pass@16       54.9%            23.9%              37.7%               25.4%                34.0%
 Deepseek-Prover-V2-7B + Phys SFT     pass@16   45.1% (-9.8%)    19.4% (-4.5%)      26.2% (-11.5%)       23.9 (-1.5%)        27.6% (-6.4%)
 Deepseek-Prover-V2-7B + Phys RAFT    pass@16   52.9% (-2.0%)   25.4% (+1.5%)       41.0% (+3.3%)        28.2 (+2.8%)       35.6% (+1.6%)


Table 3: Supervised Fine-tuning (SFT) and Rejection-Sampling Fine-tuning (RAFT) on PhysLeanData of
Deepseek-Prover-V2-7B. The pass@16 accuracy drops significantly after SFT, but increases after RAFT.


                              Training Set        Test Set              potentially limiting the model’s applicability to the
                                                                        full breadth of physical theorem proving.
    DS-Prover-SFT                    1.817          1.711
    DS-Prover-RAFT                   1.321          1.186
    DS-Prover-GRPO                   1.141          1.209               References
                                                                        Avinash Anand, Kritarth Prasad, Chhavi Kirtani, Ash-
Table 4: Perplexity on the training set and the test set                  win R Nair, Mohit Gupta, Saloni Garg, Anurag Gau-
for DS-Prover-SFT, DS-Prover-RAFT, and DS-Prover-                         tam, Snehal Buldeo, and Rajiv Ratn Shah. 2024. En-
GRPO.                                                                     hancing llms for physics problem-solving using rein-
                                                                          forcement learning with human-ai feedback. arXiv
                                                                          preprint arXiv:2412.06827.
dataset of physical theorems formalized in Lean4,
along with a conjecture formulation pipeline for                        Anthropic. 2025. Claude sonnet 4.5 system card. Tech-
                                                                          nical report, Anthropic.
generating valid and correct conjectures. By ap-
plying Reinforcement Learning with Verifiable Re-                       Jiacheng Chen, Qianjia Cheng, Fangchen Yu, Haiyuan
wards (RLVR) to an open-source state-of-the-art                            Wan, Yuchen Zhang, Shenghe Zheng, Junchi
                                                                           Yao, Qingyang Zhang, Haonan He, Yun Luo,
theorem prover, our PhysProver achieves con-                               and 1 others. 2025a. P1: Mastering physics
sistent 2.4% improvements across physical sub-                             olympiads with reinforcement learning. arXiv
domains such as Quantum Field Theory using only                            preprint arXiv:2511.13612.
5K samples. The model also demonstrates over 1%                         Jiangjie Chen, Wenxiang Chen, Jiacheng Du, Jinyi
improvement on the out-of-distribution MiniF2F-                            Hu, Zhicheng Jiang, Allan Jie, Xiaoran Jin, Xing
test benchmark, highlighting strong generalization                         Jin, Chenggang Li, Wenlei Shi, and 1 others. 2025b.
capability. Our work bridges a critical gap between                        Seed-prover 1.5: Mastering undergraduate-level the-
                                                                           orem proving via learning from experience. arXiv
formal theorem proving in mathematics and its ap-
                                                                           preprint arXiv:2512.17260.
plication to the physical sciences. We will publicly
release our dataset and models to facilitate future                     Luoxin Chen, Jinming Gu, Liankai Huang, Wenhao
research in this direction.                                               Huang, Zhicheng Jiang, Allan Jie, Xiaoran Jin,
                                                                          Xing Jin, Chenggang Li, Kaijing Ma, and 1 oth-
                                                                          ers. 2025c. Seed-prover: Deep and broad reason-
8   Limitations                                                           ing for automated theorem proving. arXiv preprint
                                                                          arXiv:2507.23726.
Our work has several limitations that we acknowl-
edge and hope to address in future research. First,                     Projet Coq. 1996. The coq proof assistant-reference
due to computational resource constraints, we were                        manual. INRIA Rocquencourt and ENS Lyon, ver-
                                                                          sion, 5.
unable to collect more data or scale the conjecture
generation process to a larger extent. As noted                         Leonardo De Moura, Soonho Kong, Jeremy Avigad,
in Section 3.2, our synthetic data pipeline has a                         Floris Van Doorn, and Jakob von Raumer. 2015. The
yield rate of only 8.9%, meaning that a substantial                       lean theorem prover (system description). In Auto-
                                                                          mated Deduction-CADE-25: 25th International Con-
portion of generated conjectures are filtered out                         ference on Automated Deduction, Berlin, Germany,
during validity and correctness verification. Scal-                       August 1-7, 2015, Proceedings 25, pages 378–388.
ing up the generation process would require sig-                          Springer.
nificantly more compute for both the LLM-based                          DeepSeek-AI, Daya Guo, Dejian Yang, Haowei Zhang,
conjecture generation and the multi-prover verifi-                        Junxiao Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu,
cation stage, which was beyond our current budget.                        Shirong Ma, Peiyi Wang, Xiao Bi, Xiaokang Zhang,
Additionally, our dataset is derived solely from the                      Xingkai Yu, Yu Wu, Z. F. Wu, Zhibin Gou, Zhi-
                                                                          hong Shao, Zhuoshu Li, Ziyi Gao, and 181 others.
PhysLean repository, which, while comprehensive,                          2025. Deepseek-r1: Incentivizing reasoning capa-
may not cover all areas of physics uniformly. Cer-                        bility in llms via reinforcement learning. Preprint,
tain specialized domains may be underrepresented,                         arXiv:2501.12948.


                                                                    9
Jingzhe Ding, Yan Cen, and Xinyuan Wei. 2023. Using              Jiawei Ge, Jingruo Sun, and 1 others. 2025b. Goedel-
   large language model to solve and explain physics             prover-v2: Scaling formal theorem proving with
   word problems approaching human level. arXiv                  scaffolded data synthesis and self-correction. arXiv
   preprint arXiv:2309.08182.                                    preprint arXiv:2508.03613.
Hanze Dong, Wei Xiong, Deepanshu Goyal, Yihan                  Leonardo de Moura and Sebastian Ullrich. 2021a. The
  Zhang, Winnie Chow, Rui Pan, Shizhe Diao, Jipeng               lean 4 theorem prover and programming language.
  Zhang, Kashun Shum, and Tong Zhang. 2023. Raft:                In Automated Deduction – CADE 28, pages 625–635,
  Reward ranked finetuning for generative foundation             Cham. Springer International Publishing.
  model alignment. Preprint, arXiv:2304.06767.
                                                               Leonardo de Moura and Sebastian Ullrich. 2021b. The
Kefan Dong and Tengyu Ma. 2025. Stp: Self-play                   lean 4 theorem prover and programming language. In
  llm theorem provers with iterative conjecturing and            Automated Deduction–CADE 28: 28th International
  proving. Preprint, arXiv:2502.00212.                           Conference on Automated Deduction, Virtual Event,
                                                                 July 12–15, 2021, Proceedings 28, pages 625–635.
Google. 2025.     Gemini 2.5:    Our newest                      Springer.
  gemini model with thinking.         https:
  //blog.google/technology/google-deepmind/                    Allen Newell and Herbert Alexander Simon. 1956. The
  gemini-model-thinking-updates-march-2025/.                     Logic Theory Machine: A Complex Information Pro-
  Accessed: 2025.                                                cessing System. RAND Corporation, Santa Monica,
                                                                 CA.
John Harrison. 2009. Hol light: An overview. In Inter-
  national Conference on Theorem Proving in Higher             OpenAI. 2025. GPT-5 system card. Technical report,
  Order Logics, pages 60–66. Springer.                           OpenAI.

Chaoqun He, Renjie Luo, Yuzhuo Bai, Shengding                  Xinyu Pang, Ruixin Hong, Zhanke Zhou, Fangrui Lv,
  Hu, Zhen Thai, Junhao Shen, Jinyi Hu, Xu Han,                  Xinwei Yang, Zhilong Liang, Bo Han, and Chang-
  Yujie Huang, Yuxiang Zhang, and 1 others. 2024.                shui Zhang. 2025. Physics reasoner: Knowledge-
  Olympiadbench: A challenging benchmark for pro-                augmented reasoning for solving physics problems
  moting agi with olympiad-level bilingual multimodal            with large language models. In Proceedings of the
  scientific problems. In Proceedings of the 62nd An-            31st International Conference on Computational Lin-
  nual Meeting of the Association for Computational              guistics, pages 11274–11289.
  Linguistics (Volume 1: Long Papers), pages 3828–             Shubham Parashar, Shurui Gui, Xiner Li, Hongyi Ling,
  3850.                                                          Sushil Vemuri, Blake Olson, Eric Li, Yu Zhang,
Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul               James Caverlee, Dileep Kalathil, and Shuiwang Ji.
  Arora, Steven Basart, Eric Tang, Dawn Song, and                2025. Curriculum reinforcement learning from easy
  Jacob Steinhardt. 2021. Measuring mathematical                 to hard tasks improves llm reasoning. Preprint,
  problem solving with the math dataset. Preprint,               arXiv:2506.06632.
  arXiv:2103.03874.                                            Lawrence C Paulson. 1994. Isabelle: A generic theorem
                                                                 prover. Springer.
Nathan Lambert, Jacob Morrison, Valentina Pyatkin,
  Shengyi Huang, Hamish Ivison, Faeze Brahman,                 Stanislas Polu, Jesse Michael Han, Kunhao Zheng, Man-
  Lester James V. Miranda, Alisa Liu, Nouha Dziri,                tas Baksys, Igor Babuschkin, and Ilya Sutskever.
  Shane Lyu, Yuling Gu, Saumya Malik, Victoria                    2022. Formal mathematics statement curriculum
  Graf, Jena D. Hwang, Jiangjiang Yang, Ronan Le                  learning. arXiv preprint arXiv:2202.01344.
  Bras, Oyvind Tafjord, Chris Wilhelm, Luca Sol-
  daini, and 4 others. 2025. Tulu 3: Pushing fron-             David Rein, Betty Li Hou, Asa Cooper Stickland, Jack-
  tiers in open language model post-training. Preprint,          son Petty, Richard Yuanzhe Pang, Julien Dirani, Ju-
  arXiv:2411.15124.                                              lian Michael, and Samuel R Bowman. 2024. Gpqa:
                                                                 A graduate-level google-proof q&a benchmark. In
Yuxin Li, Minghao Liu, Ruida Wang, Wenzhao Ji, Zhi-              First Conference on Language Modeling.
  tao He, Rui Pan, Junming Huang, Tong Zhang, and
  Yi R Fung. 2025. Lean4physics: Comprehensive rea-            ZZ Ren, Zhihong Shao, Junxiao Song, Huajian Xin,
  soning framework for college-level physics in lean4.           Haocheng Wang, Wanjia Zhao, Liyue Zhang, Zhe
  arXiv preprint arXiv:2510.26094.                               Fu, Qihao Zhu, Dejian Yang, and 1 others. 2025.
                                                                 Deepseek-prover-v2: Advancing formal mathemati-
Yong Lin, Shange Tang, Bohan Lyu, Jiayun Wu,                     cal reasoning via reinforcement learning for subgoal
  Hongzhou Lin, Kaiyu Yang, Jia Li, Mengzhou                     decomposition. arXiv preprint arXiv:2504.21801.
  Xia, Danqi Chen, Sanjeev Arora, and Chi Jin.
  2025a.   Goedel-prover: A frontier model for                 Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu,
  open-source automated theorem proving. Preprint,               Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan
  arXiv:2502.07640.                                              Zhang, YK Li, Yang Wu, and 1 others. 2024.
                                                                 Deepseekmath: Pushing the limits of mathematical
Yong Lin, Shange Tang, Bohan Lyu, Ziran Yang, Jui-               reasoning in open language models. arXiv preprint
  Hui Chung, Haoyu Zhao, Lai Jiang, Yihan Geng,                  arXiv:2402.03300.


                                                          10
Guangming Sheng, Chi Zhang, Zilingfeng Ye, Xibin               Huajian Xin, Daya Guo, Zhihong Shao, Zhizhou Ren,
  Wu, Wang Zhang, Ru Zhang, Yanghua Peng, Haibin                 Qihao Zhu, Bo Liu, Chong Ruan, Wenda Li, and
  Lin, and Chuan Wu. 2025. Hybridflow: A flexible                Xiaodan Liang. 2024. Deepseek-prover: Advancing
  and efficient rlhf framework. In Proceedings of the            theorem proving in llms through large-scale synthetic
  Twentieth European Conference on Computer Sys-                 data. Preprint, arXiv:2405.14333.
  tems, EuroSys ’25, page 1279–1297. ACM.
                                                               Xin Xu, Qiyun Xu, Tong Xiao, Tianhao Chen, Yuchen
Joseph Tooby-Smith. 2025. Heplean: Digitalising high             Yan, Jiaxin Zhang, Shizhe Diao, Can Yang, and Yang
   energy physics. Computer Physics Communications,              Wang. 2025. Ugphysics: A comprehensive bench-
   308:109457.                                                   mark for undergraduate physics reasoning with large
                                                                 language models. arXiv preprint arXiv:2502.00334.
George Tsoukalas, Jasper Lee, John Jennings, Jimmy
  Xin, Michelle Ding, Michael Jennings, Amitayush              Fangchen Yu, Haiyuan Wan, Qianjia Cheng, Yuchen
  Thakur, and Swarat Chaudhuri. 2024. Putnam-                    Zhang, Jiacheng Chen, Fujun Han, Yulun Wu, Junchi
  bench: Evaluating neural theorem-provers on                    Yao, Ruilizhen Hu, Ning Ding, and 1 others. 2025.
  the putnam mathematical competition. Preprint,                 Hipho: How far are (m) llms from humans in the lat-
  arXiv:2407.11214.                                              est high school physics olympiad benchmark? arXiv
                                                                 preprint arXiv:2509.07894.
Sumanth Varambally, Thomas Voice, Yanchao Sun,
  Zhifeng Chen, Rose Yu, and Ke Ye. 2025. Hilbert:             Zheng Yuan, Hongyi Yuan, Chengpeng Li, Guanting
  Recursively building formal proofs with informal rea-          Dong, Keming Lu, Chuanqi Tan, Chang Zhou, and
  soning. Preprint, arXiv:2509.22819.                            Jingren Zhou. 2023. Scaling relationship on learning
                                                                 mathematical reasoning with large language models.
Haiming Wang, Mert Unsal, Xiaohan Lin, Mantas                    Preprint, arXiv:2308.01825.
  Baksys, Junqi Liu, Marco Dos Santos, Flood Sung,
  Marina Vinyes, Zhenzhe Ying, Zekai Zhu, and 1 oth-           Kunhao Zheng, Jesse Michael Han, and Stanislas
  ers. 2025a. Kimina-prover preview: Towards large               Polu. 2022. Minif2f: a cross-system benchmark
  formal reasoning models with reinforcement learning.           for formal olympiad-level mathematics. Preprint,
  arXiv preprint arXiv:2504.11354.                               arXiv:2109.00110.

Ruida Wang, Yuxin Li, Tong Zhang, and 1 others. 2025b.         A    Author Contributions
  Let’s reason formally: Natural-formal hybrid reason-
  ing enhances llm’s math capability. arXiv preprint           This work stems from all authors’ valuable contri-
  arXiv:2505.23703.                                            butions and close collaborations.
Ruida Wang, Rui Pan, Yuxin Li, Jipeng Zhang,
                                                               HZ, together with RW, develops the Lean verifi-
  Yizhen Jia, Shizhe Diao, Renjie Pi, Junjie Hu, and           cation pipeline. HZ constructs the conjecture gen-
  Tong Zhang. 2025c. Ma-lot: Model-collaboration               eration pipeline to generate conjectures, develops
  lean-based long chain-of-thought reasoning en-               the RL training pipeline integrated with Lean eval-
  hances formal theorem proving. arXiv preprint
                                                               uation, conducts all experiments presented in this
  arXiv:2503.03205.
                                                               paper, and, based on the skeleton provided by RP,
Ruida Wang, Jiarui Yao, Rui Pan, Shizhe Diao, and              writes most of the paper except for the related work
  Tong Zhang. 2025d. Gar: Generative adversarial               section and performs polishing.
  reinforcement learning for formal theorem proving.           RW, provides the initial main idea for the paper.
  arXiv preprint arXiv:2510.11769.
                                                               RW builds most of the Lean verification pipeline
Ruida Wang, Jipeng Zhang, Yizhen Jia, Rui Pan, Shizhe          and collaborates closely with HZ on both data gen-
  Diao, Renjie Pi, and Tong Zhang. 2024. Theoreml-             eration and model training. Additionally, RW also
  lama: Transforming general-purpose llms into lean4           contributed to analysis of case study. In terms of
  experts. Preprint, arXiv:2407.03203.
                                                               paper writing, RW contributed to the Introduction
Xiaoxuan Wang, Ziniu Hu, Pan Lu, Yanqiao Zhu,                  and Related Work sections and modified the other
  Jieyu Zhang, Satyen Subramaniam, Arjun R Loomba,             sections in terms of logical and conceptual coher-
  Shichang Zhang, Yizhou Sun, and Wei Wang.                    ence.
  2023. Scibench: Evaluating college-level scientific
  problem-solving abilities of large language models.          RP, together with RW, initiates the project, draft-
  arXiv preprint arXiv:2307.10635.                             ing proposals to ensure computational resources,
                                                               debugging the Lean evaluation pipeline, and driv-
Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten               ing collaboration efforts between different mem-
   Bosma, Brian Ichter, Fei Xia, Ed Chi, Quoc Le, and
   Denny Zhou. 2023. Chain-of-thought prompting elic-
                                                               bers. RP also provides the skeleton of the paper,
   its reasoning in large language models. Preprint,           the first draft of the experimental section, draws
   arXiv:2201.11903.                                           Figure 1, and polishes the paper by supplementing

                                                          11
Section 3.3 and improving coherence/grammatical              checkpoints every 5 steps and report RL perfor-
correctness.                                                 mance in Table 5.
WW, together with RW, provides the initial Lean                 We observe that overall performance does not im-
dataset, consisting of provable theorems and their           prove beyond 30 steps of GRPO training, with over-
proof scripts extracted from the P HYS L EAN li-             all accuracy remaining unchanged (both 35.6%).
brary. WW also conducts preliminary explorations             While the Particle & String category shows im-
on SFT experimental design and the verification              provement relative to both the base model and the
pipeline. In terms of paper writing, the collected           RAFT model, we observe a corresponding perfor-
dataset is described in Section 3.1 Seed Dataset             mance drop in the Relativity category, indicating
Collection.                                                  inconsistent gains across categories. Throughout
BM, together with HZ and RW, reviewed case stud-             the RL process, both overall and category-level
ies for both open-source and proprietary model re-           accuracies fluctuate without demonstrating a clear
sponses. BM contributed physics expertise, ensur-            trend. Although we observe the best overall results
ing the mathematics accuracy and physics sound-              at Step 20, we attribute this to random noise given
ness of all model outputs.                                   the training process. These results suggest that RL
TZ supports the work and provides computational              after RAFT may not be consistently effective when
resources, guidance, and suggestions for experi-             both stages use the same prompt set. This observa-
ment design and paper writing.                               tion aligns with common practice in LLM training,
                                                             where different prompt sets are typically employed
B   PhysProver Categories                                    for fine-tuning and reinforcement learning.
The Classical & Foundational Physics category                D     Experimental Details
groups core undergraduate-level subjects, includ-
ing mathematical methods, classical mechanics,               D.1    Prompt Template for Main Experiments
quantum mechanics, statistical mechanics, and                We list the prompt template for DeepSeek-Prover-
electromagnetism. These areas represent foun-                V2-7B in Figure 4 with a concrete example from
dational discoveries in physics and are primarily            PhysLeanData. Specifically, in the user round, we
textbook-driven, with standardized problem formu-            append the statement with sorry to act as a task for
lations and solution methods.                                the model. And in the assistant round, we give the
   Particle and String Physics is grouped separately         model the entire context of the header and the state-
to capture topics centered on high-energy physics            ment. We chose this template because we found it
and fundamental interactions, often motivated by             stable for the models to generate proof completions,
experimental programs such as those at the Large             as it allows the model to directly generate the proof
Hadron Collider. String theory topics are included           part.
in this category due to their close conceptual align-           The prompt template for Kimina-Prover and
ment with high-energy theoretical frameworks.                Goedel-Prover is exactly the same except for the
   Quantum Field Theory and Relativity are treated           special tokens which are shown in Figure 5.
as distinct categories due to their advanced mathe-             The prompt template for the proprietary models
matical structure and conceptual complexity. Both            is different due to the inaccessibility of the actual
subjects are typically introduced at the graduate            models. Instead, we apply the Chain-of-Thought
level, with quantum field theory extending quantum           prompting (Wei et al., 2023), and the template is
mechanics and relativity providing a foundational            shown in Figure 6
framework for spacetime and gravitation.                        We also list the prompt template for Claude-4.5-
                                                             Sonnet to generate conjectures in Figure 7.
C    Reinforcement Learning after
     Rejection-Sampling Fine-tuning                          D.2    Conjecture Generation
In this section, we investigate the effectiveness of         We also list an example of the conjecture, given
Reinforcement Learning (RL) following Rejection-             a header and a lemma, which is shown in Fig-
Sampling Fine-tuning (RAFT). Starting from the               ure 8. In this example, the conjecture is a variant
RAFT checkpoint described in Section 6, we apply             of the original lemma - Both lemmas are basic al-
RL using the same hyperparameters and settings               gebraic properties of matrix-vector multiplication.
as in our main experiments (Section 4.2). We save            In other examples we examined, the conjectures

                                                        12
 Method                  Budget      Classical     Particle & String     Relativity    Quantum Field Theory      Overall
 DeepSeek-Prover-V2-7B   pass@16       54.9%           23.9%               37.7%              25.4%               34.0%
 +RAFT                   pass@16   52.9% (-2.0%)   25.4% (+1.5%)       41.0% (+3.3%)       28.2 (+2.8%)       35.6% (+1.6%)
 RAFT+GRPO Step 5        pass@16   52.9% (-2.0%)   23.9% (+0.0%)       41.0% (+3.3%)       28.2 (+2.8%)       35.2% (+1.2%)
 RAFT+GRPO Step 10       pass@16   52.9% (-2.0%)   25.4% (+1.5%)       39.3% (+1.6%)      26.8% (+1.4%)       34.8% (+0.8%)
 RAFT+GRPO Step 15       pass@16   56.9% (+2.0%)   25.4% (+1.5%)       39.3% (+1.6%)      26.8% (+1.4%)       35.6% (+1.6%)
 RAFT+GRPO Step 20       pass@16   54.9% (+0.0%)   25.4% (+1.5%)       41.0% (+3.3%)       28.2 (+2.8%)       36.0% (+2.0%)
 RAFT+GRPO Step 25       pass@16   54.9% (+0.0%)   25.4% (+1.5%)       39.3% (+1.6%)       28.2 (+2.8%)       35.6% (+1.6%)
 RAFT+GRPO Step 30       pass@16   54.9% (+0.0%)   26.9% (+3.0%)       37.7% (+0.0%)       28.2 (+2.8%)       35.6% (+1.6%)


Table 5: Reinforcement Learning after Rejection-Sampling Fine-tuning (RAFT) on PhysLeanData of
Deepseek-Prover-V2-7B. The pass@16 accuracy does not improve after RAFT.


consistently fall into predictable categories relative
to their preceding lemmas. These variations typ-
ically manifest as: (1) special cases obtained by
substituting specific values such as zero, (2) defi-
nitional unwrapping where a concept is restated in
more explicit form, or (3) algebraic variants that
apply the same underlying principle to a differ-
ent argument. Since PhysLean formalizes abstract
concepts in mathematical physics, many lemmas
establish foundational API properties—such as lin-
earity, group action behavior, or interaction with
zero elements—and the conjectures naturally com-
plete this API by covering symmetric or boundary
cases. Consequently, these conjectures primarily
serve to help models become more familiar with the
dataset’s conventions, naming patterns, and proof
structures to improve the accuracy, rather than to
evaluate deep mathematical reasoning capabilities.




                                                            13
Figure 3: An example of the PhysLeanData. The black lines denote the header, the blue lines denote the lemma
statement, and the red lines denote the proof.

   Example of Header, Statement, and the Proof from PhysLean


   import PhysLean.Mathematics.Fin.Involutions
   import PhysLean.QFT.PerturbationTheory.WickContraction.ExtractEquiv
   import PhysLean.QFT.PerturbationTheory.WickContraction.Involutions

   open FieldSpecification

   variable {F : FieldSpecification}

   namespace WickContraction

   variable {n : N } (c : WickContraction n)

   open PhysLean.List
   open FieldStatistic
   open Nat

   def IsFull : Prop := c.uncontracted = ∅

   instance : Decidable (IsFull c) := decEq c.uncontracted ∅

   /-- This theorem states that the configuration c is full if and only if, for every index i
       in the finite set of size n, the involution function associated with c does not map i
       to itself.-/

   lemma isFull_iff_equivInvolution_no_fixed_point :
   IsFull c ↔∀(i : Fin n), (equivInvolution c).1 i ̸=i := by
   simp only [IsFull, ne_eq]
   rw [Finset.eq_empty_iff_forall_notMem]
   simp [equivInvolution, toInvolution, uncontracted]




                                                    14
              Figure 4: Prompt template for DeepSeek Prover with a concrete example

DeepSeek Prover Prompt Template

<|begin_of_sentence|> You are an expert in mathematics, physics and Lean 4.
<|User|>Think about and solve the following problem step by step in Lean 4. →Directly give
    the formal statement in Lean 4.

# Problem: This theorem states that the matrix product of the Minkowski metric with itself
    yields the identity matrix.
# Formal statement:
```lean4
import Mathlib.Algebra.Lie.Classical
import Mathlib.Analysis.Normed.Ring.Lemmas

open Matrix

def minkowskiMatrix {d : N} : Matrix (Fin 1 ⊕Fin d) (Fin 1 ⊕Fin d) R:=
  LieAlgebra.Orthogonal.indefiniteDiagonal (Fin 1) (Fin d) R

namespace minkowskiMatrix

variable {d : N}

scoped[minkowskiMatrix] notation "η" => minkowskiMatrix

/-- This theorem states that the matrix product of the Minkowski metric with itself yields
     the identity matrix.-/
@[simp]
lemma sq : @minkowskiMatrix d * minkowskiMatrix = 1 :=
  sorry
```

<|Assistant|>
```lean4
import Mathlib.Algebra.Lie.Classical
import Mathlib.Analysis.Normed.Ring.Lemmas

open Matrix

def minkowskiMatrix {d : N} : Matrix (Fin 1 ⊕Fin d) (Fin 1 ⊕Fin d) R:=
  LieAlgebra.Orthogonal.indefiniteDiagonal (Fin 1) (Fin d) R

namespace minkowskiMatrix

variable {d : N}

scoped[minkowskiMatrix] notation "η" => minkowskiMatrix

/-- This theorem states that the matrix product of the Minkowski metric with itself yields
    the identity matrix.-/
@[simp]
lemma sq : @minkowskiMatrix d * minkowskiMatrix = 1 :=




                                               15
Figure 5: Prompt template for Kimina Prover and Goedel Prover with a concrete example. They are the same as the
Deepseek Prover except for the special tokens, such as the BOS token.

   Kimina and Goedel Provers Prompt Template


   <|im_start|>system
   You are an expert in mathematics, physics and Lean 4.<|im_end|>
   <|im_start|>user
   Think about and solve the following problem step by step in Lean 4. →Directly give the
       formal statement in Lean 4.

   # Problem: This theorem states that the matrix product of the Minkowski metric with itself
       yields the identity matrix.
   # Formal statement:
   ```lean4
   import Mathlib.Algebra.Lie.Classical
   import Mathlib.Analysis.Normed.Ring.Lemmas

   open Matrix

   def minkowskiMatrix {d : N} : Matrix (Fin 1 ⊕Fin d) (Fin 1 ⊕Fin d) R:=
     LieAlgebra.Orthogonal.indefiniteDiagonal (Fin 1) (Fin d) R

   namespace minkowskiMatrix

   variable {d : N}

   scoped[minkowskiMatrix] notation "η" => minkowskiMatrix

   /-- This theorem states that the matrix product of the Minkowski metric with itself yields
        the identity matrix.-/
   @[simp]
   lemma sq : @minkowskiMatrix d * minkowskiMatrix = 1 :=
     sorry
   ```<|im_end|>
   <|im_start|>assistant
   ```lean4
   import Mathlib.Algebra.Lie.Classical
   import Mathlib.Analysis.Normed.Ring.Lemmas

   open Matrix

   def minkowskiMatrix {d : N} : Matrix (Fin 1 ⊕Fin d) (Fin 1 ⊕Fin d) R:=
     LieAlgebra.Orthogonal.indefiniteDiagonal (Fin 1) (Fin d) R

   namespace minkowskiMatrix

   variable {d : N}

   scoped[minkowskiMatrix] notation "η" => minkowskiMatrix

   /-- This theorem states that the matrix product of the Minkowski metric with itself yields
       the identity matrix.-/
   @[simp]
   lemma sq : @minkowskiMatrix d * minkowskiMatrix = 1 :=




                                                      16
              Figure 6: Prompt template for proprietary models for the main experiments.

Proprietary Models Prompt Template


Complete the following Lean 4 code:

```lean4
{THE LEAN4 HEADERS AND STATEMENT}
```

Before producing the Lean 4 code to formally prove the given theorem, provide a proof plan
    outlining the main proof steps and strategies.

The plan should highlight key ideas, intermediate lemmas, and proof structures that will
    guide the construction of the final formal proof.




            Figure 7: Prompt template for Claude-4.5-Sonnet to generate formal conjectures

Claude-4.5-Sonnet Prompt Template for Conjecture Generation


You are an expert in mathematics, physics and Lean 4.
You are provided a context, a lemma, and a proof. Your task is to generate a list of 10
    related physics conjecture in formal language based on the context and the seed
    language statements.

The conjectures should be:
1. A meaningful variant of the original theorem: modify hypotheses, generalize structures,
    or extend scope while keeping the core mathematical insight.
2. Must differ significantly in mathematical content (changed assumptions, stronger/weaker
    conclusions, or different algebraic structures) but remain recognizably related.
3. The new conjecture should be in formal language.
4. Do not include the proof.

When generating the conjectures, preserve all specific Lean identifiers exactly as they
    appear in the formal statement. You can also refer to the original formal statement.

Context:
{context}

Natural Language Statement:
{nq}

Original Formal Statement:
{theorem}

Return the final conjectures in JSON format as a dictionary where:
- The key is "conjectures"
- The value is a list of dictionaries
- Each dictionary in the list has a key "statement" whose value is a string containing one
    conjecture

Please read, understand, and then generate a list of conjectures.




                                                 17
             Figure 8: An example of the conjecture based on the header and the lemma

The Header of the Original Lemma

import PhysLean.Relativity.PauliMatrices.SelfAdjoint
import Mathlib.RepresentationTheory.Basic
import PhysLean.Relativity.Lorentz.Group.Basic
import Mathlib.Analysis.InnerProductSpace.PiL2

namespace Lorentz

noncomputable section
open Matrix
open MatrixGroups
open Complex

structure ContrMod (d : N) where
  val : Fin 1 ⊕Fin d →R

namespace ContrMod

variable {d : N}

def toFin1dRFun : ContrMod d ≃(Fin 1 ⊕Fin d →R) where
  toFun v := v.val
  invFun f := ⟨f⟩
  left_inv _ := rfl
  right_inv _ := rfl

instance : AddCommMonoid (ContrMod d) := Equiv.addCommMonoid toFin1dRFun

instance : AddCommGroup (ContrMod d) := Equiv.addCommGroup toFin1dRFun

instance : Module R(ContrMod d) := Equiv.module RtoFin1dRFun

def toFin1dREquiv : ContrMod d ≃l [R] (Fin 1 ⊕Fin d →R) :=
  Equiv.linearEquiv RtoFin1dRFun

abbrev toFin1dR (ψ : ContrMod d) := toFin1dREquiv ψ

@[simps!]
def stdBasis : Basis (Fin 1 ⊕Fin d) R(ContrMod d) := Basis.ofEquivFun toFin1dREquiv

abbrev mulVec (M : Matrix (Fin 1 ⊕Fin d) (Fin 1 ⊕Fin d) R) (v : ContrMod d) :
    ContrMod d := Matrix.toLinAlgEquiv stdBasis M v

scoped[Lorentz] infixr:73 " ∗v " => ContrMod.mulVec


The Original Lemma

/-- This theorem states that for any two real matrices M and N of dimension (1+d) ×(1+d)
     and any vector v in ContrMod d, the matrix-vector product of their difference with v
     equals the difference of their individual matrix-vector products with v.-/
lemma sub_mulVec (M N : Matrix (Fin 1 ⊕Fin d) (Fin 1 ⊕Fin d) R) (v : ContrMod d) :
    (M - N) ∗v v = M ∗v v - N ∗v v := sorry


The New Conjecture


lemma mulVec_zero (M : Matrix (Fin 1 ⊕Fin d) (Fin 1 ⊕Fin d) R) : M ∗v (0 : ContrMod d) = 0
    := sorry




                                               18
