                                             Reliable Use of Lemmas via Eligibility Reasoning and Section-Aware
                                                                 Reinforcement Learning

                                                         Zhikun Xu1 * , Xiaodong Yu2 , Ben Zhou1 , Jiang Liu2 , Jialian Wu2 ,
                                                               Ze Wang2 , Ximeng Sun2 , Hao Chen2 , Zicheng Liu2
                                                               1
                                                                   Arizona State University, 2 Advanced Micro Devices, Inc.
                                                                                    zhikunxu@asu.edu


                                                               Abstract                                 Inspired by the human mathematician’s needs
                                                                                                     (Frieder et al., 2024), we cast lemma-judging as a
                                             Recent large language models (LLMs) per-
                                                                                                     structured prediction problem: given a statement-
arXiv:2602.00998v1 [cs.CL] 1 Feb 2026




                                             form strongly on mathematical benchmarks
                                             yet often misapply lemmas, importing con-               lemma pair, the model must output: 1 a precondi-
                                             clusions without validating assumptions. We             tion check (validating if the lemma’s assumptions
                                             formalize lemma-judging as a structured pre-            hold in the current context) and 2 a conclusion-
                                             diction task: given a statement and a candi-            utility check (assessing if the lemma is actually
                                             date lemma, the model must output a precon-             helpful for the proof goal), from which a useful
                                             dition check and a conclusion-utility check,            decision is derived. Our hypothesis is that requir-
                                             from which a usefulness decision is derived.
                                                                                                     ing models to externalize eligibility reasoning and
                                             We present RULES, which encodes this spec-
                                             ification via a two-section output and trains           aligning credit assignment per section will reduce
                                             with reinforcement learning plus section-aware          reliance on spurious surface cues, improve robust-
                                             loss masking to assign penalty to the sec-              ness and safety to applicability-breaking perturba-
                                             tion responsible for errors. Training and               tions, and transfer to end-to-end tasks. The intu-
                                             evaluation draw on diverse natural-language             ition mirrors standard proof practice, i.e., check
                                             and formal proof corpora; robustness is as-             the hypothesis, then use the lemma, and explains
                                             sessed with a held-out perturbation suite; and          why single-label supervision obscure the locus of
                                             end-to-end evaluation spans competition-style,
                                                                                                     failure.
                                             perturbation-aligned, and theorem-based prob-
                                             lems across various LLMs. Results show con-                We propose a training framework, RULES (Re-
                                             sistent in-domain gains over both a vanilla             liable Use of Lemmas via Eligibility Reasoning
                                             model and a single-label RL baseline, larger im-        and Section-Aware Reinforcement Learning). The
                                             provements on applicability-breaking perturba-          training is based on Group Relative Policy Opti-
                                             tions, and parity or modest gains on end-to-end         mization (GRPO) (Shao et al., 2024) with a section-
                                             tasks; ablations indicate that the two-section          aware loss masking mechanism, which assigns
                                             outputs and section-aware reinforcement are
                                                                                                     penalty to the precise section responsible for failure,
                                             both necessary for robustness.
                                                                                                     rather than the entire rollout. This design aligns
                                        1    Introduction                                            the supervision with the cognitive decomposition
                                                                                                     the task demands, encouraging models to learn the
                                        Recent large language models (LLMs) achieve                  check-before-use discipline rather than overfitting
                                        strong scores on mathematical benchmarks and                 to label-level shortcuts.
                                        can often generate proof-like text (Welleck et al.,             Empirical results over various models and di-
                                        2022; OpenAI et al., 2024; Yang et al., 2024; Shao           verse evaluation datasets have shown that RULES
                                        et al., 2024; Li et al., 2025b; Guo et al., 2025). Yet       improves in-domain lemma-judging over a vanilla
                                        their behavior frequently reflects pattern imitation         model and a single-label RL baseline. The margin
                                        rather than principled reasoning: models tend to             is larger on the held-out applicability-breaking per-
                                        reproduce familiar solution paths, and they can im-          turbation suite with at most 23 points, indicating
                                        port a lemma’s conclusion without validating its             better gating of lemma use. On end-to-end bench-
                                        hypotheses. Such behavior exploits surface corre-            marks, average performance is broadly better or on
                                        lations in the training distribution and undermines          par with the single-label RL baseline. Ablations
                                        trustworthiness in mathematical reasoning.                   show that both the two-section outputs and section-
                                            * Work done during research internship at AMD.           aware RL are necessary: entangling fine-grained

                                                                                                 1
supervision on checks or excluding training-time              {0, 1}. This task specification makes the precondi-
perturbations supervision substantially reduces the           tion and conclusion checks explicit and auditable,
robustness of eligibility reasoning.                          and a minimal schema with section sentinels en-
                                                              sures unambiguous parsing, which is illustrated in
2     Related Works                                           Appendix A by prompts.
Many works have explored pre-training on math                 3.2    Section-Aware Reinforcement Learning
corpora coupled with chain-of-thought prompting,
                                                              The training is adapted from GRPO. Specif-
which equips LLMs with domain-specific under-
                                                              ically, for each input x, given a rollout as
standing and step-by-step reasoning (Wang et al.,
                                                              y i = ypre
                                                                       i    ⊕ ycon i          i , li ) ⊕ (r i , li ), if
                                                                                        = (rpre     pre    con con
2025a). Reinforcement learning advances, such
                                                              the precondition check is correct but the aggregated
as GRPO, have offered significant gains on bench-
                                                              final label is incorrect, which implicitly means that
marks like GSM8K and MATH (Shao et al., 2024).
                                                              the conclusion check must be wrong, we will only
However, brittleness to premise order and prob-
                                                              keep the conclusion check section, i.e., setting the
lem phrasing remains a challenge (Chen et al.,                                       i , li ) to be 1 and others as 0.
                                                              loss mask of (rcon          con
2024; Huang et al., 2025). Self-correction meth-
                                                              For the RL update, the gradient function in each
ods have also improved LLM mathematical rea-
                                                              group G is illustrated as: ∇θ Lsection−aware =
soning by enabling self-refinement (Xiong et al.,                 1 P|G| 1 P|y |
                                                                                        i
                                                                                               i ˜i           i     i
2025; Yan et al., 2025). Benchmarks such as                   − |G|      i=1 |y i |    j=1 mj Aj ∇θ log πθ (yj |x, y<j ),
the Open Proof Corpus (Dekoninck et al., 2025)                where mij is the j-th token mask for the i-th rollout
and MathArena (Balunović et al., 2025) reveal a              and other notations in this equation follow the
gap between the accuracy of final answers and                 default GRPO setting such as estimated advantages
the validity of proofs. Knowledge-graph agents                A˜ij . By this, we are penalizing the incorrect
have been explored to improve success rates (Li               sections only and supervising models in more
et al., 2025a), while LeanDojo (Yang et al., 2023)            fine-grained signals on certain wrong tokens,
and other works (Mikuła et al., 2023; Tao et al.,             enforcing "check-before-use" as a safety filter for
2025) enhance premise selection. Recent inno-                 theorem application. Crucially, this objective-level
vations (Mukherjee et al., 2025; Pan et al., 2025;            modification operates independently of the underly-
Wang et al., 2025b) further align supervision with            ing model architecture or scale. The computational
intermediate reasoning, improving error detection             overhead is restricted to negligible token-masking
and reflective reasoning. Our work builds on exist-           operations during the loss calculation, making
ing insights and focuses on structured intermediate           RULES compatible with any LLM backbones.
reasoning that aims to improve generalizable LLM
reasoning on math.                                            4     Experimental Settings
                                                              4.1    Models
3     Methodology: RULES
                                                              We have mainly experimented with four LLMs:
RULES has two components: 1 a two-section                     DeepMath-1.5B (He et al., 2025), OLMo-2-1124-
lemma-judging task that requires explicit eligi-              7B-Instruct (OLMo et al., 2025), Qwen2.5-Math-
bility checks before use, and 2 section-aware re-             7B-Instruct (Yang et al., 2024), and Llama-3.1-
inforcement learning that aligns credit assignment            8B-Instruct (Grattafiori et al., 2024). For each
with these checks.                                            model, we report three variants: 1 Vanilla: di-
                                                              rect inference with our two-section schema. 2
3.1    Lemma-judging Task                                     GRPO: default GRPO optimization with only the
Given an input x = (L, S) with lemma L and state-             final usefulness label (single-label objective) using
ment S, the model produces a structured output                the vanilla prompt. 3 RULES: GRPO with section-
with two sections y = (rpre , lpre ) ⊕ (rcon , lcon )         aware masking by two-section schema.
where rpre and rcon are free-form rationales for the
precondition and conclusion-utility checks, and the           4.2    Training Settings
section (predicted) labels, i.e., lpre , lcon ∈ {0, 1},       The training data are from natural language and
are extracted judgments. The final usefulness de-             formal proof corpora, i.e., NaturalProofs (Welleck
cision is a deterministic aggregation of the precon-          et al., 2021), NLPS (Natural Language Premise Se-
dition and conclusion checks luse = lpre ∧ lcon ∈             lection) (Ferreira and Freitas, 2020), Premise Se-

                                                          2
                                         In-Domain Test              Perturbation Test                             E2E Benchmark
         Models \Tests
                                NP       NLPS      IS       IL             DT              PA       CM       IM     MP-hard     MP-simple      TQ-Math
                  vanilla       60.8      51.5     51.6     31.9            24             39.1     45.7     76        53           72           55.4
    DeepMath      GRPO          77.5      77.2     67.6     65.8           35.6            37.9     63.1     73       54.5         72.8          56.1
                  RULES         88.5      86.2     75.8     89.5            47             39.5      46      71       56.3         72.8          57.7
                  vanilla       77.6      69.1     53.9     64.9           47.6            8.4      52.3     29        8.6         18.6          27.1
    OLMO2         GRPO          85.2      84.2     72.2     83.6           46.8            7.8      48.1     23        9.3         21.9          30.3
                  RULES         84.9      83.4     76.6     82.5           60.5            6.7      48.2     24       10.4         23.3          26.9
                  vanilla       63.9      71.9     55.5     55.8           71.9            32.4     59.5     55       33.7         59.5          49.8
    Qwen2.5       GRPO          76.5      83.7     74.2     80.4           81.2            35.6     60.5     54       33.7         59.5           50
                  RULES         88.2      85.8     81.3     92.7           87.8             32      61.3     53       35.1         62.4          50.5
                  vanilla       61.3      75.1     54.7     52.3           89.2            11.5     56.5     22       13.3         38.7          33.5
    Llama-3.1     GRPO          88.6      86.5     85.9     89.8           80.9            13.2     50.7     18       13.3         36.2          32.6
                  RULES         93.2      86.4     86.3     93.6           90.9            12.8     49.3     16       12.9         36.9           33


Table 1: Main Results. For in-domain test, NP, NLPS, IS, and IL stands for NaturalProofs, NLPS, Premise Selection
in Isabelle, IMO-Lemma derived test sets. DT stands for DeepTheorem-sampled perturbation test set. PA, CM,
IM, MP, and TQ stand for Putnam-Axiom, CounterMATH, IneqMath, MATH-Perturb, and TheoremQA. MP-hard
and MP-simple stand for hard and simple perturbations based on the paper. TQ-Math is the math subset of the TQ
benchmark. The CounterMATH is using F1 due to imbalanced data distribution mentioned in Li et al. (2025b) and
the rest of data is using exact-match based accuracy.

                                          In-Domain Test               Perturbation Test                            E2E Benchmark
           Ablations
                                  NP       NLPS       IS      IL              DT             PA       CM      IM      MP-hard      MP-simple    TQ-Math
  vanilla                         63.9      71.9     55.5     55.8           71.9            32.4     59.5    55        33.7         59.5          49.8
  GRPO                            76.5      83.7     74.2     80.4           81.2            35.6     60.5    54        33.7         59.5           50
  two-section-onetime              87       85.4     84.4     92.7           73.1            32.4     60.5    49        35.5         60.9          49.5
  w/o perturbation data           93.2      87.4     82.4     94.4           19.1            32.2     56.4    49        34.4         59.1          50.5
  de-noised perturbation data      86       83.9     83.6      95            74.3            34.1     59.6    54        35.8         58.8          50.9
  RULES                           88.2      85.8     81.3     92.7           87.8             32      61.3    53        35.1         62.4          50.5


Table 2: Ablation Results. two-section-onetime refers to output two checks predictions at last. w/o perturbation
data and de-noised perturbation data refers to removing perturbation data in training and filter the unqualified
perturbation training data by the o3 model and human validation, respectively. The experiments are done with
Qwen2.5-Math-7B-Instruct.


lection in Isabelle (Mikuła et al., 2023), and IMO-                                 fail to parse under the two-section schema receive
lemmas (Liang et al., 2025), pairing statement with                                 a format penalty of -2.
candidate lemmas and binary labels showing the
usefulness of lemmas. More training settings and                                    4.3     Evaluation Settings
designs are in Appendix B.                                                          We evaluate three axes that mirror our intended
                                                                                    use: in-domain lemma-judging, robustness to
Perturbation Design. As our goal is to separate                                     applicability-breaking perturbations, and transfer
surface similarity from true eligibility, we also add                               to end-to-end mathematical problem solving. All
some perturbation data in training by making a                                      results are calculated by sampling 7 outputs and
lemma inapplicable while keeping the statement                                      majority-voting the extracted answers by self-
minimally changed and mathematically coherent.                                      consistency, which is noted as SC@7. More evalu-
The reason of only providing labels for the pre-                                    ation details are shown in Appendix C.
condition check when constructing perturbations
is two fold: 1 Precondition satisfaction is directly                                In-domain Evaluation We use held-out splits
falsifiable from the statement-lemma pair and inde-                                 drawn from the training data sources, which are
pendent of proof strategy, yielding reliable supervi-                               named as naturalproofs-test, nlps-test, isabelle-
sion with low ambiguity. 2 Conclusion utility is                                    test, and IMO-lemma-test.
inherently strategy-dependent (e.g., proof by coun-
terexample), making it costly and noisy to annotate                                 Perturbation Test Similar to the goal and pro-
at scale.                                                                           cess of training perturbation data curation, we also
                                                                                    evaluate on a out-of-domain perturbation suite con-
Reward Design. For a fair comparison with base-                                     structed by minimally editing statements to violate
lines, the reward is rule-based and binary, i.e., 1 for                             lemma preconditions. But the raw data is sampled
correct and -1 for incorrect. Moreover, outputs that                                from DeepTheorem (Zhang et al., 2025), which is

                                                                                3
noted as deeptheorem-perturbation. More details            on perturbation-aligned suites where robustness
about perturbation data quality are in Appendix D.         against invalid inputs is paramount. Conversely,
                                                           constructive tasks like CounterMATH require ex-
End-to-end Benchmarks Besides the task-
                                                           ample synthesis, a capability distinct from eligibil-
related evaluations, we also assess transfer on
                                                           ity gating. Thus, RULES functions as a necessary
diverse mathematical tasks, including competition-
                                                           robustness layer, ensuring models do not attempt
style problems (Putnam-Axiom (Gulati et al.,
                                                           proofs with fundamentally inapplicable premises.
2024)), inequality reasoning (IneqMath (Sheng
et al., 2025b)), counterexample-driven ques-               5.2    Ablations
tions (CounterMATH (Li et al., 2025b)),                    Two-time v.s. one-time prediction. Replacing
perturbation-aligned suites (MATH-Perturb                  the sequential two-section protocol with a “two-
(Huang et al., 2025)), and theorem-centric math            section-onetime” variant (emitting both judgements
QA (TheoremQA (Chen et al., 2023)).                        only at the end) yields strong in-domain accuracy
5     Analysis                                             but notably weaker robustness on the perturbation
                                                           suite. This indicates that the staged structure and
5.1    Main Results                                        section-aware alignment matters for learning to
In-domain lemma-judging. Across all four base              withhold lemmas when preconditions are not satis-
models, RULES improves in-domain lemma-judging             fied.
over both vanilla and the single-label GRPO base-          Role of training-time perturbation data. Re-
line. Gains are consistent on most splits and              moving perturbation data during training preserves
especially pronounced on the IMO-derived test,             in-domain scores but collapses robustness on the
with OLMO2 showing comparable performance                  out-of-domain suite, confirming that curated neg-
to GRPO on three splits and clear improvements             atives are essential to teach the precondition gate.
on the Isabelle split. These results indicate that         However, we emphasize that this robustness is not
enforcing explicit precondition and conclusion             merely a function of data scaling. The architecture
checks could help models improve understanding             contributes significantly: RULES improves over the
of lemma applicability.                                    data-equivalent “two-section-onetime” baseline by
Robustness to applicability-breaking perturba-             14.7 points on the perturbation test (Table 2). This
tions. On the out-of-domain perturbation suite,            substantial margin confirms that while the data pro-
RULES consistently outperforms vanilla and GRPO            vides the necessary signals, the Section-Aware RL
across all four models, with sizable margins for           mechanism is indispensable for effectively lever-
23+ points at most. This pattern supports the in-          aging them to prevent superficial pattern matching.
tended effect of training-time perturbation data and       Effect of "de-noised" perturbation data. Fil-
section-aware masking: the model more reliably             tering low-quality perturbations leads to mixed out-
gates off familiar but inapplicable lemmas under           come: modest improvements on some end-to-end
minimal statement edits that invalidate the precon-        metrics and in-domain tests, but still below RULES
ditions.                                                   on the perturbation suite. This evidence thus far
Mixed E2E transfer. On downstream tasks,                   does not support that "clean fine-grained labels" al-
RULES performs broadly on par with single-label            ways improve overall math reasoning; rather, there
GRPO, yielding gains on perturbation-aligned               appears to be a trade-off between strict cleaning
subsets while showing occasional regressions on            and robustness coverage.
competition-style and inequality-based problems.
                                                           6     Conclusion
We interpret these regressions as a performance-
rigorousness tradeoff: whereas standard models             We propose RULES, aligning lemma use with an
may sometimes “get lucky” by hallucinating appli-          explicit check-before-use protocol and section-
cability to force a solution, RULES enforces strict        aware RL. RULES yields consistent in-domain gains,
precondition checks. This discipline prioritizes           large robustness improvements under precondition-
precision and safety against invalid reasoning, nat-       breaking perturbations, and parity or small gains
urally lowering recall on tasks where looser con-          on end-to-end tasks. Ablations show the staged
straints might inadvertently permit a correct an-          two-section output and section-aligned credit as-
swer. Consequently, gains are most pronounced              signment are both required.

                                                       4
Limitations                                                   Deborah Ferreira and André Freitas. 2020. Natural
                                                                language premise selection: Finding supporting state-
Task scope and supervision. Our study focuses                   ments for mathematical text. In Proceedings of the
on lemma-judging rather than full proof generation.             Twelfth Language Resources and Evaluation Confer-
                                                                ence, pages 2175–2182, Marseille, France. European
The supervision signals are tailored to the specific            Language Resources Association.
task, which may bias models toward unexpected
behaviors.                                                    Simon Frieder, Julius Berner, Philipp Petersen, and
                                                                Thomas Lukasiewicz. 2024. Large language models
Label coverage and noise. In the perturbation                   for mathematicians. Preprint, arXiv:2312.04556.
data, only the precondition label is available while          Aaron Grattafiori, Abhimanyu Dubey, Abhinav Jauhri,
the conclusion-utility label is omitted to avoid strat-         Abhinav Pandey, Abhishek Kadian, Ahmad Al-
egy dependence. This asymmetric supervision can                 Dahle, Aiesha Letman, Akhil Mathur, Alan Schel-
                                                                ten, Alex Vaughan, Amy Yang, Angela Fan, Anirudh
introduce bias and limit learning of usefulness be-             Goyal, Anthony Hartshorn, Aobo Yang, Archi Mi-
yond eligibility. In addition, rewards are binary               tra, Archie Sravankumar, Artem Korenev, Arthur
with a format penalty, which simplifies optimiza-               Hinsvark, and 542 others. 2024. The llama 3 herd of
tion but may underutilize graded signals.                       models. Preprint, arXiv:2407.21783.
                                                              Aryan Gulati, Brando Miranda, Eric Chen, Emily Xia,
Model and data coverage. Experiments cover                      Kai Fronsdal, Bruno de Moraes Dumont, and Sanmi
four mid-sized models and a specific suite of math              Koyejo. 2024. Putnam-AXIOM: A functional and
corpora (NaturalProofs, NLPS, Isabelle premise se-              static benchmark for measuring higher level mathe-
lection, and IMO-lemma). This leaves gaps across                matical reasoning. In The 4th Workshop on Mathe-
                                                                matical Reasoning and AI at NeurIPS’24.
subfields of mathematics and automated theorem
proving techniques, and languages other than En-              Dadi Guo, Jiayu Liu, Zhiyuan Fan, Zhitao He, Haoran
glish. While the eligibility reasoning mechanism                Li, Yumeng Wang, and Yi R. Fung. 2025. Math-
                                                                ematical proof as a litmus test: Revealing failure
is theoretically language-agnostic, the extension               modes of advanced large reasoning models. Preprint,
to multilingual settings or other formal proof as-              arXiv:2506.17114.
sistants (e.g., Lean, Coq) remains a direction for
                                                              Zhiwei He, Tian Liang, Jiahao Xu, Qiuzhi Liu, Xingyu
future work.
                                                                Chen, Yue Wang, Linfeng Song, Dian Yu, Zhen-
                                                                wen Liang, Wenxuan Wang, Zhuosheng Zhang, Rui
                                                                Wang, Zhaopeng Tu, Haitao Mi, and Dong Yu. 2025.
References                                                      Deepmath-103k: A large-scale, challenging, decon-
                                                                taminated, and verifiable mathematical dataset for
Mislav Balunović, Jasper Dekoninck, Ivo Petrov, Nikola         advancing reasoning. Preprint, arXiv:2504.11456.
  Jovanović, and Martin Vechev. 2025. Matharena:
  Evaluating llms on uncontaminated math competi-             Kaixuan Huang, Jiacheng Guo, Zihao Li, Xiang Ji, Ji-
  tions. arXiv preprint arXiv:2505.23281.                       awei Ge, Wenzhe Li, Yingqing Guo, Tianle Cai, Hui
                                                                Yuan, Runzhe Wang, Yue Wu, Ming Yin, Shange
Wenhu Chen, Ming Yin, Max Ku, Pan Lu, Yixin Wan,                Tang, Yangsibo Huang, Chi Jin, Xinyun Chen,
 Xueguang Ma, Jianyu Xu, Xinyi Wang, and Tony                   Chiyuan Zhang, and Mengdi Wang. 2025. MATH-
 Xia. 2023. TheoremQA: A theorem-driven question                perturb: Benchmarking LLMs’ math reasoning abil-
 answering dataset. In Proceedings of the 2023 Con-             ities against hard perturbations. In Forty-second In-
 ference on Empirical Methods in Natural Language               ternational Conference on Machine Learning.
 Processing, pages 7889–7901, Singapore. Associa-
 tion for Computational Linguistics.                          Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying
                                                               Sheng, Lianmin Zheng, Cody Hao Yu, Joseph E.
                                                               Gonzalez, Hao Zhang, and Ion Stoica. 2023. Effi-
Xinyun Chen, Ryan A Chi, Xuezhi Wang, and Denny
                                                               cient memory management for large language model
  Zhou. 2024. Premise order matters in reasoning with
                                                               serving with pagedattention. In Proceedings of the
  large language models. In Proceedings of the 41st In-
                                                               ACM SIGOPS 29th Symposium on Operating Systems
  ternational Conference on Machine Learning, pages
                                                               Principles.
  6596–6620.
                                                              Vincent Li, Tim Knappe, Yule Fu, Kevin Han, and Kevin
Jasper Dekoninck, Ivo Petrov, Kristian Minchev, Mis-            Zhu. 2025a. Automating mathematical proof gener-
   lav Balunovic, Martin Vechev, Miroslav Marinov,              ation using large language model agents and knowl-
   Maria Drencheva, Lyuba Konova, Milen Shumanov,               edge graphs. arXiv preprint arXiv:2503.11657.
   Kaloyan Tsvetkov, and 1 others. 2025.        The
   open proof corpus: A large-scale study of llm-             Yinghui Li, Jiayi Kuang, Haojing Huang, Zhikun Xu,
   generated mathematical proofs. arXiv preprint                Xinnian Liang, Yi Yu, Wenlian Lu, Yangning Li,
   arXiv:2506.21621.                                            Xiaoyu Tan, Chao Qu, Ying Shen, Hai-Tao Zheng,


                                                          5
  and Philip S. Yu. 2025b. One example shown, many            Jiayi Sheng, Luna Lyu, Jikai Jin, Tony Xia, Alex Gu,
  concepts known! counterexample-driven conceptual               James Zou, and Pan Lu. 2025b. Solving inequal-
  reasoning in mathematical LLMs. In Forty-second                ity proofs with large language models. Preprint,
  International Conference on Machine Learning.                  arXiv:2506.07927.

Zhenwen Liang, Linfeng Song, Yang Li, Tao Yang,               Yicheng Tao, Haotian Liu, Shanwen Wang, and
  Feng Zhang, Haitao Mi, and Dong Yu. 2025. To-                 Hongteng Xu. 2025. Learning an effective premise
  wards solving more challenging imo problems via               retrieval model for efficient mathematical formaliza-
  decoupled reasoning and proving. arXiv preprint.              tion. In 2nd AI for Math Workshop @ ICML 2025.

Maciej Mikuła, Szymon Antoniak, Szymon                        Peng-Yuan Wang, Tian-Shuo Liu, Chenyang Wang, Yi-
 Tworkowski, Bartosz Piotrowski, Albert Jiang,                  Di Wang, Shu Yan, Cheng-Xing Jia, Xu-Hui Liu,
 Jin Peng Zhou, Christian Szegedy, Łukasz Kuciński,            Xin-Wei Chen, Jia-Cheng Xu, Ziniu Li, and 1 others.
 Piotr Miłoś, and Yuhuai Wu. 2023. Magnushammer:               2025a. A survey on large language models for mathe-
 A transformer-based approach to premise selection.             matical reasoning. arXiv preprint arXiv:2506.08446.
 In The 3rd Workshop on Mathematical Reasoning                Pinzheng Wang, Juntao Li, Zecheng Tang, Haijia Gui,
 and AI at NeurIPS’23.                                          and 1 others. 2025b. Improving rationality in the
                                                                reasoning process of language models through self-
Sagnik Mukherjee, Abhinav Chinta, Takyoung Kim,                 playing game. In Forty-second International Confer-
  Tarun Anoop Sharma, and Dilek Hakkani Tur. 2025.              ence on Machine Learning.
  Premise-augmented reasoning chains improve error
  identification in math reasoning with llms. In Forty-       Sean Welleck, Jiacheng Liu, Ronan Le Bras, Hannaneh
  second International Conference on Machine Learn-             Hajishirzi, Yejin Choi, and Kyunghyun Cho. 2021.
  ing.                                                          Naturalproofs: Mathematical theorem proving in nat-
                                                                ural language. In Thirty-fifth Conference on Neural
Team OLMo, Pete Walsh, Luca Soldaini, Dirk Groen-               Information Processing Systems Datasets and Bench-
  eveld, Kyle Lo, Shane Arora, Akshita Bhagia, Yuling           marks Track (Round 1).
  Gu, Shengyi Huang, Matt Jordan, Nathan Lambert,
  Dustin Schwenk, Oyvind Tafjord, Taira Anderson,             Sean Welleck, Jiacheng Liu, Ximing Lu, Hannaneh
  David Atkinson, Faeze Brahman, Christopher Clark,             Hajishirzi, and Yejin Choi. 2022. Naturalprover:
  Pradeep Dasigi, Nouha Dziri, and 21 others. 2025. 2           Grounded mathematical proof generation with lan-
  olmo 2 furious. Preprint, arXiv:2501.00656.                   guage models. In Advances in Neural Information
                                                                Processing Systems, volume 35, pages 4913–4927.
OpenAI, Josh Achiam, Steven Adler, Sandhini Agarwal,            Curran Associates, Inc.
  Lama Ahmad, Ilge Akkaya, Florencia Leoni Ale-
  man, Diogo Almeida, Janko Altenschmidt, Sam Alt-            Wei Xiong, Hanning Zhang, Chenlu Ye, Lichang
  man, Shyamal Anadkat, Red Avila, Igor Babuschkin,            Chen, Nan Jiang, and Tong Zhang. 2025. Self-
  Suchir Balaji, Valerie Balcom, Paul Baltescu, Haim-          rewarding correction for mathematical reasoning.
  ing Bao, Mohammad Bavarian, Jeff Belgum, and                 arXiv preprint arXiv:2502.19613.
  262 others. 2024. Gpt-4 technical report. Preprint,
  arXiv:2303.08774.                                           Yuchen Yan, Jin Jiang, Yang Liu, Yixin Cao, Xin Xu,
                                                                Mengdi Zhang, Xunliang Cai, and Jian Shao. 2025.
Zhuoshi Pan, Yu Li, Honglin Lin, Qizhi Pei, Zinan Tang,         Sˆ 3cmath: Spontaneous step-level self-correction
  Wei Wu, Chenlin Ming, H. Vicky Zhao, Conghui He,              makes large language models better mathematical
  and Lijun Wu. 2025. LEMMA: Learning from er-                  reasoners. In Proceedings of the AAAI Conference
  rors for MatheMatical advancement in LLMs. In                 on Artificial Intelligence, volume 39, pages 25588–
  Findings of the Association for Computational Lin-            25596.
  guistics: ACL 2025, pages 11615–11639, Vienna,              An Yang, Beichen Zhang, Binyuan Hui, Bofei Gao,
  Austria. Association for Computational Linguistics.           Bowen Yu, Chengpeng Li, Dayiheng Liu, Jian-
                                                                hong Tu, Jingren Zhou, Junyang Lin, Keming Lu,
Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu,                 Mingfeng Xue, Runji Lin, Tianyu Liu, Xingzhang
  Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan                Ren, and Zhenru Zhang. 2024. Qwen2.5-math tech-
  Zhang, Y. K. Li, Y. Wu, and Daya Guo. 2024.                   nical report: Toward mathematical expert model via
  Deepseekmath: Pushing the limits of mathemati-                self-improvement. Preprint, arXiv:2409.12122.
  cal reasoning in open language models. Preprint,
  arXiv:2402.03300.                                           Kaiyu Yang, Aidan Swope, Alex Gu, Rahul Chala-
                                                                mala, Peiyang Song, Shixing Yu, Saad Godil, Ryan J
Guangming Sheng, Chi Zhang, Zilingfeng Ye, Xibin                Prenger, and Animashree Anandkumar. 2023. Le-
  Wu, Wang Zhang, Ru Zhang, Yanghua Peng, Haibin                andojo: Theorem proving with retrieval-augmented
  Lin, and Chuan Wu. 2025a. Hybridflow: A flexible              language models. Advances in Neural Information
  and efficient rlhf framework. In Proceedings of the           Processing Systems, 36:21573–21612.
  Twentieth European Conference on Computer Sys-
  tems, EuroSys ’25, page 1279–1297, New York, NY,            Ziyin Zhang, Jiahao Xu, Zhiwei He, Tian Liang, Qi-
  USA. Association for Computing Machinery.                     uzhi Liu, Yansi Li, Linfeng Song, Zhenwen Liang,


                                                          6
    Zhuosheng Zhang, Rui Wang, Zhaopeng Tu, Haitao                              Precondition Perturbation Prompt for o3 (DeepTheo-
    Mi, and Dong Yu. 2025. Deeptheorem: Advanc-                                 rem)
    ing llm reasoning for theorem proving through nat-                          Based on the given statement and its proof, could you help me
    ural language and reinforcement learning. Preprint,                         perturb the statement with the minimal edits so that one certain
                                                                                precondition of some lemma used in the proof is no longer satisfied?
    arXiv:2505.23754.                                                           If the perturbation is not possible, please output suitability: False.
                                                                                Otherwise, return suitability: True, and then extract the affected
                                                                                lemma in the proof, generate the perturbed statement, and the
                                                                                rationale of the perturbation.

                                                                                Critical Requirements:
                                                                                1. MATHEMATICAL COHERENCE: The perturbed statement
                                                                                must be mathematically well-defined and meaningful. Do not create
                                                                                statements that are conceptually impossible or nonsensical (e.g.,
                                                                                "subgroups of semigroups").
A     Prompts
                                                                                 2.      GENUINE INAPPLICABILITY: The chosen lemma
                                                                                 must be fundamentally unusable in ANY reasonable proof approach
                                                                                 for the perturbed statement. Avoid superficial changes where:
                                                                                - The lemma applies to a subset/restriction of the new domain
                                                                                - The lemma can be used indirectly through standard correspondences
    Two-Section Prompt                                                          - The statement can be reduced back to the lemma’s domain

    Lemma: {lemma}                                                              3. VERIFICATION TEST: Before finalizing, ask: "Could
    Statement: {statement}                                                      the chosen lemma still contribute meaningfully to proving or
                                                                                disproving the perturbed statement through any mathematical
    Please analyze step by step whether the lemma is useful                     pathway?" If yes, the perturbation is ineffective.
    for proving or disproving the given statement. You should perform
    two sequential checks:                                                       Rules:
                                                                                - Copy the OriginalStatement verbatim except for that one span.
    **Step 1: Precondition Check**                                              - Do NOT strengthen assumptions, introduce unrelated concepts/sym-
    First, analyze whether the lemma’s preconditions are satisfied in            bols, or make changes that render the statement trivial.
    the given statement. After your reasoning, provide your answer              - Prefer the simplest change that creates a fundamental barrier to
    within boxed{} as either boxed{True} (preconditions are satisfied) or        lemma applicability.
    boxed{False} (preconditions are not satisfied).                             - The perturbation should target the lemma’s core assumptions or
                                                                                 domain in a way that cannot be circumvented.
    **Step 2: Conclusion Check**
    Next, analyze whether the lemma’s conclusion is helpful for proving          Ineffective Perturbation Patterns to Avoid:
    or disproving the given statement. After your reasoning, provide            - Domain changes where standard correspondences exist (e.g.,
    your answer within boxed{} as either boxed{True} (conclusion is              R exponential → C exponential when differentiating w.r.t. real
    helpful) or boxed{False} (conclusion is not helpful).                       variables)
                                                                                - Structure downgrades that still allow the target concept (e.g., group
                                                                                 → semigroup but keeping "subgroup" terminology)
    Please use the same section titles as above (i.e., **Step 1:                - Changes that only affect surface terminology but not mathematical
    Precondition Check** and **Step 2: Conclusion Check**) to start              substance
    the two checks respectively and STRICTLY follow the following
    format:                                                                     Return ONLY this schema:
    - First, provide your reasoning for the precondition check                  Suitability: {bool}
    - Then output boxed{True} or boxed{False} for the precondition              AffectedLemma: {lemma-content}
    check                                                                       OriginalStatement: {original statement}
    - Then provide your reasoning for the conclusion check                      PerturbedStatement: {perturbed statement}
    - Finally output boxed{True} or boxed{False} for the conclusion             Rationale: {rationale explaining why the lemma becomes
    check                                                                       fundamentally inapplicable, not just surface-level different}

                                                                                Now Process:

                                                                                Statement: {statement}
                                                                                Proof: {proof}
    Vanilla Prompt
    Lemma: {lemma}
    Statement: {statement}

    Please reason step by step about whether the above lemma
    is useful for proving or disproving its following statement, and then
    put your final answer (i.e., True or False) within
    boxed.




    Two-Section Onetime Prompt
    Lemma: {lemma}
    Statement: {statement}

    Please think step by step whether the lemma is useful for
    proving or disproving the given statement. Specifically, please 1)
    check whether the lemma’s preconditions are satisfied in the given
    statement, and 2) check whether the lemma’s conclusion is helpful
    for proving the given statement. Then put your final answers for
    precondition check and conclusion check, i.e., True or False for each
    check, within boxed{} (For example, boxed{True, False} means the
    lemma’s preconditions are satisfied but its conclusion is not helpful
    for proving the given statement).




                                                                            7
    Precondition Perturbation Validation Prompt for o3                            2048 for reasoning and non-reasoning models re-
    You are evaluating the quality of a mathematical statement                    spectively. Training checkpoints are used when the
    perturbation. Your task is to determine if the perturbation effectively
    breaks the chosen lemma’s applicability.                                      percentage of activated section aware loss masking
    Given Perturbation Data:
                                                                                  instances of a single batch is close to zero. Our
    Lemma: {lemma}                                                                training framework is based on verl (Sheng et al.,
    Original Statement: {statement}
    Perturbed Statement: {perturbed statement}                                    2025a). The training data distribution is Natural-
    Rationale: {rationale}                                                        Proofs: 4744, NLPS: 2858, Premise Selection in
    Evaluation Criteria (ALL must pass):                                          Isabelle: 4484, and IMO-lemma: 986.
    1. MATHEMATICAL COHERENCE CHECK:
    - Is the perturbed statement mathematically well-defined?
    - Are all mathematical concepts used consistently and meaningfully?           Details of Perturbation Design. Concretely, we
    - Do the mathematical objects and relations make sense together?
                                                                                  target a specific hypothesis of the lemma used in a
    Common failures:                                                              proof and apply a minimal edit to the statement so
    - Mixing incompatible concepts (e.g., "subgroups of semigroups")                                          gold
    - Ill-defined operations or structures                                        that the hypothesis fails (lpre  = 0), without intro-
    - Conceptual contradictions
                                                                                  ducing unrelated concepts or trivializing the claim.
    2. LEMMA INAPPLICABILITY VERIFICATION:                                        This is derived from NaturalProofs and processed
    Systematically check if the lemma could still be used via:
                                                                                  by o3 model1 . The perturbation data is the only part
    a) DIRECT APPLICATION:
    - Can the lemma’s hypotheses still be satisfied in the new context?           with the gold precondition label for section-aware
    b) RESTRICTION/SUBSET APPLICATION:
                                                                                  masking.
    - Does the lemma apply to relevant subsets of the new domain?
    - Can we restrict to cases where the lemma’s conditions hold?

    c) CORRESPONDENCE/ISOMORPHISM:
                                                                                  C       More Evaluation Details
    - Are there standard mathematical correspondences between the old
    and new domains?
    - Can we map the problem back to where the lemma applies?                     Our evaluation framework is based on vllm (Kwon
    d) INDIRECT/FOUNDATIONAL USE:
                                                                                  et al., 2023). The max token length is set to
    - Could the lemma be used in proving prerequisite results?                    10k to avoid early truncation and temperature is
    - Is the lemma foundational to the theory needed for the perturbed
    statement?                                                                    set to 0.7 for SC@7 across all models. The in-
    - Could it be applied to finite quotients, local analysis, etc.?
                                                                                  domain and perturbation evaluation data distri-
    e) ANALOGOUS RESULTS:                                                         butions are naturalproofs-test (1002), nlps-test
    - Are there direct analogs of the lemma in the new domain?
    - Would the original lemma be a key step in proving such analogs?             (676), isabelle-test (256), IMO-lemma-test (342),
    3. FAILURE PATTERN DETECTION:                                                 and deeptheorem-perturbation (839)
    Check for these known ineffective patterns:

    - SUPERFICIAL DOMAIN CHANGES: Changes that look
    different but preserve mathematical substance                                 D       Perturbation Data Quality
    - TERMINOLOGY SWAPS: Changing labels without affecting
    underlying mathematics
    - TRIVIAL GENERALIZATIONS: Moving to broader categories                       To verify the quality of our perturbation suite
    where restrictions still apply
    - INCOMPLETE DOMAIN SHIFTS: Changing some but not all                         (where only the precondition label is flipped), we
    relevant aspects of the domain
                                                                                  conducted a multi-stage validation. For the training
    4. PROOF PATHWAY ANALYSIS:                                                    data, we have used O3 model and GPT-OSS-120B
    Consider: "In any reasonable attempt to prove or disprove the
    perturbed statement, could the given lemma contribute meaningfully            to cross-validate them, where both models reached
    to the argument?"
                                                                                  consensus on 84.8% of training data. We only use
    If YES to any pathway → INEFFECTIVE perturbation                              these 84.8% data as our final perturbation training.
    If NO to all pathways → EFFECTIVE perturbation
                                                                                  Moreover, we authors have also sampled 100 data-
    Return your evaluation in this format:
                                                                                  points from it for human verification, and the pass
    EFFECTIVENESS: [BOOLEAN]                                                      rate is 90%. For perturbation evaluation data, we
    RATIONALE: [Explanation of why the perturbation is effective or
    ineffective]                                                                  authors have sampled 100 datapoints after o3-based
    Now evaluate the given perturbation:                                          and human filtering to verify the quality of the final
                                                                                  data. Our evaluation guideline follows exactly the
B     More Training Details                                                       principles in the prompt: (i) mathematical coher-
                                                                                  ence (ii) genuine inapplicability (iii) verification
Our training experiments are mainly implemented                                   for similar pathways by equivalent lemmas. The
on AMD MI250 and Nvidia H200 GPU servers.                                         pass rate for the sampled evaluation data is 95%.
The training batch size is 128 and the number of
                                                                                      1
rollout is set to 8. The response length is 8000 and                                      https://platform.openai.com/docs/models/o3


                                                                              8
                                                Stage 1: Precondition Check


                                                       Rationale (𝑟𝑝𝑟𝑒 )                Section-Aware Gradient Masking

                                                   Prediction (𝑙𝑝𝑟𝑒 ∈ {0,1})

        Input                                                                                                         𝑔𝑜𝑙𝑑
                                                                                                                     𝑙𝑓𝑖𝑛𝑎𝑙
                        LLM Policy                                                             Final Decision                     ∑
     Statement (S)         (𝜋𝜃 )                                                           (𝑙𝑓𝑖𝑛𝑎𝑙 = 𝑙𝑝𝑟𝑒 ∧ 𝑙𝑐𝑜𝑛 )
      Lemma (L)                                                                                                               Reward/Loss
                                                 Stage 2: Conclusion Check


                                                       Rationale (𝑟𝑐𝑜𝑛 )
                                                                                    𝑚𝑝𝑟𝑒/𝑐𝑜𝑛 = 1in the gradient for activation
                                                   Prediction (𝑙𝑐𝑜𝑛 ∈ {0,1})
                                                                                    if the section is judged as incorrect (only
                                                                                    when fine-grained labels are provided)




Figure 1: Overview of RULES Training Framework. As mentioned in Section 3.2, if the fine-grained label (precondi-
tion/conclusion check) is provided, we could know which section of tokens are to blame with negative rewarding.


E    Case Study: Preventing Lemma                               F          Use of LLM
     Misapplication
                                                                We have only used LLM for language polishing
To illustrate how RULES prevents the hallucinations             purposes in the paper writing. We do not use LLM
of lemma applicability, we present a case from the              for idea formalization, or to an extent that it could
Riemannian Geometry domain where a standard                     be regarded as a contributor.
vanilla model fails.
Scenario. Statement: Let G = SU (n) and let
g be a left-invariant metric. Show that any sym-
metric 2-tensor h satisfying the linearized Einstein
equation... must be trivial.
Candidate Lemma: "Since g is bi-invariant, it
is an Einstein metric... that Ricg = λg for some
λ > 0."
Analysis. The lemma requires the metric to be
bi-invariant. However, the problem statement only
guarantees that g is left-invariant. In differential
geometry, left-invariance is a weaker condition than
bi-invariance; thus, the lemma’s preconditions are
not met.
Model Behavior.
    • Baseline (Vanilla): The model ignores the
      subtle distinction between "left-invariant" and
      "bi-invariant," hallucinates that the condition
      is met, outputs True, and attempts to use the
      lemma.
    • RULES: The model correctly identifies the
      mismatch in the Precondition Check sec-
      tion: "Rationale: The lemma requires bi-
      invariance, but the statement only assumes
      left-invariance..." It outputs F alse for the
      precondition, effectively gating off the invalid
      path.

                                                           9
