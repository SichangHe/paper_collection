                                                      V ER IF: Verification Engineering for Reinforcement Learning
                                                                          in Instruction Following

                                                            Hao Peng, Yunjia Qi, Xiaozhi Wang, Bin Xu, Lei Hou, Juanzi Li
                                                           Department of Computer Science and Technology, Tsinghua University
                                                                         {peng-h24}@mails.tsinghua.edu.cn



                                                                   Abstract
                                                                                                            Could you give a simple, friendly, and imaginative
                                                 Reinforcement learning with verifiable rewards             explanation of how solar panels work, as if you’re
arXiv:2506.09942v1 [cs.CL] 11 Jun 2025




                                                                                                            talking to a curious five-year-old? Submit your
                                                 (RLVR) has become a key technique for en-                  response that contains at least 160 words.
                                                 hancing large language models (LLMs), with
                                                 verification engineering playing a central role.
                                                 However, best practices for RL in instruction                   Soft Constraint                Hard Constraint
                                                 following remain underexplored. In this work,
                                                                                                                      Long chain-of-               def check (res):
                                                 we explore the verification challenge in RL for                         thought                   ... return False
                                                 instruction following and propose V ER IF, a                                                      return True
                                                                                                                        reasoning
                                                 verification method that combines rule-based
                                                 code verification with LLM-based verification
                                                                                                                   Verification Score for Instruction Following
                                                 from a large reasoning model (e.g., QwQ-32B).
                                                 To support this approach, we construct a high-
                                                 quality instruction-following dataset, V ER I N -       Figure 1: A simplified illustration of V ER IF. The in-
                                                 STRUCT , containing approximately 22,000 in-            struction constraints are categorized as soft or hard and
                                                 stances with associated verification signals. We        verified using different methods in V ER IF.
                                                 apply RL training with V ER IF to two models,
                                                 achieving significant improvements across sev-
                                                 eral representative instruction-following bench-           In this work, we explore verification engineering
                                                 marks. The trained models reach state-of-the-
                                                                                                         for reinforcement learning in instruction following.
                                                 art performance among models of comparable
                                                 size and generalize well to unseen constraints.
                                                                                                         Specifically, this work focuses on the following of
                                                 We further observe that their general capabil-          constraints in the instruction (Zhou et al., 2023),
                                                 ities remain unaffected, suggesting that RL             such as response length, as shown in Figure 1. The
                                                 with V ER IF can be integrated into existing RL         constraints are usually divided into two types: hard
                                                 recipes to enhance overall model performance.           constraints, which can be verified using simple
                                                 We have released our datasets, codes, and mod-          rules, e.g., length, and soft constraints, which re-
                                                 els to facilitate future research1 .                    quire semantic judgment, e.g., style. Assessing
                                         1       Introduction                                            whether a response satisfies these constraints pro-
                                                                                                         vides a natural basis for verification in RLVR. How-
                                         Reinforcement learning with verifiable rewards                  ever, reinforcement learning for instruction follow-
                                         (RLVR) has emerged as a key technique for enhanc-               ing remains underexplored. The only notable work,
                                         ing large language models (LLMs), leading to vari-              TULU 3 (Lambert et al., 2024), applies RLVR to
                                         ous advanced LLMs, such as DeepSeek R1 (Guo                     enhance instruction following. However, the im-
                                         et al., 2025). The core component of RLVR is ver-               provement is limited, and it focuses solely on hard
                                         ification engineering. Recently, numerous works                 constraints, neglecting soft constraints. Therefore,
                                         have explored reliable verification across diverse              the best practice of verification engineering for RL
                                         domains, such as math (Lambert et al., 2024; Guo                in instruction following remains under-explored.
                                         et al., 2025; Luo et al., 2025b), code (Wang et al.,               Given the above issues, we explore the best prac-
                                         2024b; Luo et al., 2025a), logic (Xie et al., 2025),            tice of RLVR in instruction following and propose
                                         medicine (Chen et al., 2024; Wang et al., 2025),                V ER IF, a verification method for instruction fol-
                                         and finance (Qian et al., 2025b; Liu et al., 2025a).            lowing that combines rule-based code verification
                                             1
                                                 https://github.com/THU-KEG/VerIF                        with verification from a large reasoning model. As

                                                                                                     1
shown in Figure 1, hard constraints are verified            gun et al., 2023). We observe that RL with V ER IF
through code, and soft constraints are handled by           preserves general and mathematical capabilities,
a large reasoning model, which enables effective            indicating its potential as an additional RL stage
verification through long chain-of-thought reason-          to enhance instruction following without affecting
ing (Liu et al., 2025b). V ER IF requires no man-           other skills. We analyze the performance gains of
ual annotations or reference answers, offering an           trained models across different constraint types and
efficient solution for automatic verification. To           find that RL with V ER IF exhibits good generaliza-
support this approach, we construct a high-quality          tion to unseen constraints. We also conduct abla-
dataset, V ER I NSTRUCT, containing approximately           tion studies on the verification method, using only
22, 000 instances with verification. The data con-          code validation or only LLM verification, both of
struction involves two main steps: (1) instruction          which lead to notable performance drops. Finally,
construction with multiple constraints, where we            we develop a smaller and efficient 7B LLM as the
apply constraint back-translation (Qi et al., 2024)         soft constraint verifier. Specifically, we extract ap-
to augment existing instructions with additional            proximately 130k complex instructions from Wild-
constraints; (2) verification generation. For hard          Chat (Zhao et al., 2024) and Infinity Instruct (BAAI,
constraints such as length, we use Qwen2.5-72B-             2024), collect responses from 6 different LLMs,
Instruct (Yang et al., 2024) to generate verification       and use QwQ to generate constraint verification.
code. For soft constraints, they are verified online        We then train DeepSeek-R1-Distill-Qwen-7B on
during RL training using large reasoning models.            this dataset as a generative verifier for soft con-
   We apply reinforcement learning with V ER IF             straints, achieving RL performance comparable to
on two SFT-trained models using V ER I NSTRUCT,             the model trained using QwQ-32B as the verifier.
including TULU 3 SFT (Lambert et al., 2024) and
DeepSeek-R1-Distill-Qwen-7B (Guo et al., 2025).             2     Pilot Experiments
Specifically, V ER IF computes the final reward as
the average of hard constraint scores (0 or 1) from         This section explores the potential of RL for in-
code validation and soft constraint scores (0 or 1)         struction following (§ 2.1) and preliminarily ex-
determined by the QwQ-32B (Qwen, 2025). We                  plores different verification methods (§ 2.2) using
train the models using the GRPO algorithm (Shao             the reward benchmark IFBench (Peng et al., 2025).
et al., 2024). We evaluate the trained models on sev-
eral widely-used instruction-following benchmarks,
                                                            2.1    Potential for RL Training
including IFEval (Zhou et al., 2023), Multi-IF (He
et al., 2024b), SysBench (Qin et al., 2024), Follow-        We first explore the potential of RL in instruction
Bench (Jiang et al., 2024), and CFBench (Zhang              following, as most previous works have adopted
et al., 2024a). Experimental results show that the          supervised fine-tuning (SFT; Ouyang et al., 2022)
RLVR-trained models using V ER IF achieve signif-           or direct preference optimization (DPO; Rafailov
icant improvements. Notably, the model trained              et al., 2023), with limited use of RL. This raises
based on TULU 3 SFT achieves state-of-the-art               a key question: Does RL hold untapped potential
performance among models of similar parameter               for instruction following? To explore this question,
scale and outperforms TULU 3 (Lambert et al.,               we evaluate the pass@k performance of several
2024), which is trained with extensive DPO data             LLMs on the instruction following benchmark IFE-
and rule-based RLVR. The results demonstrate the            val (Zhou et al., 2023). The motivation is that RL
effectiveness of our verification method V ER IF.           enhances performance by increasing the likelihood
   We conduct further analytical experiments. We            of sampling correct responses, and a high pass@k
first evaluate the generalization of the trained mod-       at large k suggests untapped potential that RL can
els on general instruction following tasks, includ-         exploit (Yue et al., 2025a). The experimental re-
ing AlpacaEval 2.0 (Dubois et al., 2024) and MT-            sults of TULU 3 SFT and DeepSeek-R1-Distill-
Bench (Zheng et al., 2023), and mathematical rea-           Qwen-7B are shown in Figure 2. We can observe
soning tasks, including GSM8K (Cobbe et al.,                that the results are much higher with larger k, with
2021) and Omni-MATH (Gao et al., 2025), nat-                pass@64 showing over a 20% increase compared
ural language understanding datasets: MMLU-                 to pass@1. This suggests that LLMs can sample
Pro (Wang et al.) and DROP (Dua et al., 2019), and          correct answers on IFEval at higher k, with the
a natural language inference benchmark BBH (Suz-            potential that can be exploited during RL training.

                                                        2
            1.0                                                                         1.0
                                                                                                                  Code-only             LLM-only
            0.9                                                                         0.8 0.76                                            0.73
 Accuracy (%)




                                                                         Accuracy (%)
            0.8                                                                         0.6             0.53
            0.7                                                                         0.4      0.36             0.39
                                                                                                           0.29       0.29       0.31
            0.6                       TULU3-SFT                                         0.2                                              0.18
                                      DeepSeek-R1-Distill-Qwen-7B                                                             0.08
            0.5 1          2      4       8   16       32      64                       0.0
                                       Pass@k                                                 Keyword Length Format Content               Style

Figure 2: Pass@k results (%) of two SFT-trained LLMs                    Figure 3: Accuracy (%) of code-only or LLM-only
on IFEval. We report the prompt-level strict score.                     verification in verifying compliance with different types
                                                                        of constraints. LLM-only adopts QwQ-32B.
                  Method              Hard   Soft    Overall
                  Code-only           60.6   13.2     48.6              constraints and LLM verification performs better
                  LLM-onlyQ W Q       31.5   48.1     37.4              on soft constraints, supporting the rationale for the
                  LLM-onlyQ WEN       19.7   45.3     28.6
                  Code+LLMQ W Q       61.3   48.1     58.1              code+LLM verification approach. The detailed re-
                                                                        sults across different constraint types are shown
Table 1: Accuracy (%) of three verification methods on                  in Figure 3, and we can observe that LLMs per-
IFBench. “Hard” or “Soft” indicates that the rejected                   form particularly poorly on keyword and length
response only violates certain hard or soft constraints.                constraints, which may be due to inherent limita-
                                                                        tions in numerical counting (Fu et al., 2024; Ball
                                                                        et al., 2024). Since keyword and length constraints
2.2             Verification Engineering                                can be efficiently verified with code, we conclude
We preliminarily conduct verification engineer-                         that in instruction-following verification, hard con-
ing using reward model benchmarks. Specifically,                        straints should be checked with code, and soft con-
we evaluate different verification methods on IF-                       straints can be reliably verified by advanced LLMs.
Bench (Peng et al., 2025), a benchmark designed
for instruction-following rewards that consists of                      3               Method
an instruction and two responses, where the task is                     This section introduces the formalization of V ER IF
to select the response that better follows the instruc-                 (§ 3.1), the construction process of V ER I NSTRUCT
tion. IFBench includes 3 common hard constraints:                       (§ 3.2), and the RL training method (§ 3.3).
length, format, and keyword, and 2 common soft
constraints: style and content. We explore three                        3.1              Verification Method
verification methods: (1) code-only verification,                       Suppose we are given an instruction x, which in-
similar to RewardAgent proposed by Peng et al.                          cludes the task decription and a set of constraints
(2025), which uses automatically generated code                         C = {c1 , c2 , ..., cn }. We follow the task defini-
for each constraint verification; (2) LLM-only veri-                    tion of instruction-following by Zhou et al. (2023):
fication, which directly uses the LLM as the judge;                     given x, generating a response y that satisfies all
(3) code+LLM verification, which applies code ver-                      constraints in C. In this work, our primary goal is
ification for hard constraints and LLM for soft con-                    to accurately verify whether y meets all constraints
straints. We explore using QwQ-32B (Qwen, 2025)                         and to apply this reliable verification in reinforce-
and Qwen2.5-72B-Instruct (Yang et al., 2024) as                         ment learning training. Specifically, the constraint
the LLMs. The results are shown in Table 1. We                          set C consists of two types: hard constraints Ch ,
can observe that code+LLM verification performs                         which can be verified by simple rules or code (e.g.,
much better and reasoning LLMs (QwQ) also per-                          length), and soft constraints Cs , which require se-
form better than non-reasoning LLMs (Qwen).                             mantic understanding (e.g., style). As explored in
   We further investigate the accuracies of code and                    § 2.2, we propose a hybrid verification approach,
LLM verification on different types of constraints,                     V ER IF, that uses code verification for Ch and LLM
and report their respective accuracy for soft and                       verification for Cs . Formally, this is defined as:
hard constraints in Table 1, which further confirms
that code verification is more effective for hard                           V ER IF(x, y) = F (Code(y, Ch ), LLM(y, Cs ))

                                                                    3
      Instruction                                                      Complex Instruction
      Can you explain how solar panels work?                            Could you give a simple, friendly, and imaginative
      Response                                                          explanation … contains at least 160 words.
      Sure! Solar panels are devices that convert sunlight into
                                                                                   Sure! Let’s imagine the Sun is a giant
      electricity through the photovoltaic effect. …
                                                                                   flashlight in the sky, shining down …
                                                                       Policy Model
      Soft Constraint Generation Hard Constraint Generation
      1. A simple, friendly, and  1. Contain at least 160               [LLM] Cs      Response             Response
      imaginative tone.           words                                  1. Writing Style                [Length]
       2. …                       2. …                                   2. Semantic Elements           [Keyword]
                     Verification Construction                                  3. …
                                                                                                           …
               Tagging                         Coding                          LLM Verification     Code Verification

                 [LLM]               [Length] [Keyword]      …          Aggregation Final Verification Score∈ [0, 1]

Figure 4: Left: The construction process for V ER I NSTRUCT, including complex instruction generation and
verification construction. Right: Our verification method, V ER IF, providing verification for instruction following.


Code(y, Ch ) ∈ {0, 1} denotes whether y satis-                        Chat (Es, 2023), Evol Instruct (Xu et al., 2023),
fies all hard constraints in Ch , and LLM(y, Cs ) ∈                   and OpenAssitant (Köpf et al., 2024). We use
{0, 1} indicates whether y satisfies all soft con-                    Llama3.1-70B-Instruct (Grattafiori et al., 2024) to
straints in Cs . F denotes the aggregation method                     generate constraints implicitly satisfied by each re-
used to combine the code verification score and                       sponse, such as language style. Since LLMs often
the LLM verification score, including averaging or                    struggle with understanding length constraints (Sun
multiplication. In this work, we consider only three                  et al., 2024), we instead automatically synthesize
types of hard constraints, including length, format,                  them based on response length using Python scripts.
and keyword. All other constraints are taken as soft                  We combine the generated constraints with the orig-
and verified using LLMs. As explored in § 2.2, we                     inal instruction to form the final complex instruc-
use large reasoning models for LLM-based verifica-                    tion. (2) Verification construction. We then auto-
tion, which is a form of scaling up verification and                  matically generate a verification method for each
has been demonstrated effective in practice (Liu                      constraint. For hard constraints, including length,
et al., 2025b; ByteDance-Seed, 2025).                                 format, and keyword presence, we use Qwen2.5-
                                                                      72B-Instruct to generate verification Python code.
3.2    Data Construction Method                                       Given the simplicity of these generated Python
We construct a high-quality instruction-following                     code scripts, we manually check them and find
dataset for reinforcement learning, where each in-                    nearly no errors. For soft constraints, we do not
stance is paired with a corresponding verification.                   generate code but instead tag them with “LLM”,
Prior works on enhancing instruction-following of                     which indicates that verification during RL train-
LLMs (Sun et al., 2024; Dong et al., 2024; Qi et al.,                 ing should be online produced by an LLM. We
2024) have primarily focused on generating com-                       finally filter out instructions with fewer than 2 con-
plex instructions and corresponding high-quality                      straints, resulting in V ER I NSTRUCT, which con-
responses for supervised fine-tuning (SFT). In this                   tains 22, 000 instructions, each including an aver-
work, we focus on generating complex instruc-                         age of 6.2 constraints and corresponding verifica-
tions with associated verification, eliminating the                   tion methods. The details of V ER I NSTRUCT are
efforts to generate and filter high-quality responses.                placed in Appendix A.
As shown in Figure 4, the construction process
consists of two main parts: (1) Complex instruc-                      3.3   RL Training
tion generation. We adopt the constraint back-                        We conduct reinforcement learning using V ER IF
translation approach (Qi et al., 2024) to generate                    on V ER I NSTRUCT. Specifically, we adopt the
complex instructions, which produces few unrealis-                    GRPO algorithm (Shao et al., 2024) and perform 16
tic cases. Specifically, we randomly sample 25, 000                   rollouts per prompt for value estimation. For each
data instances from four high-quality datasets, in-                   response, the reward is provided online by V ER IF.
cluding Alpaca GPT4 (Peng et al., 2023), Orca                         To reduce the overhead of LLM-based verification,

                                                                  4
                                             IFEval                             Multi-IF            SysBench   FollowBench   CFBench
    Model
                           Pr. (S)   Pr. (L)    Ins. (S)   Ins. (L)   Turn 1    Turn 2     Turn 3     ISR         SSR          ISR
    GPT-4o                  79.9      84.8       85.6       89.6      82.3       71.7      59.3       80.2        75.3        80.0
    QwQ-32B                 82.8      86.1       88.0       90.4      64.2       56.6      48.4       67.8        73.5        80.0
    Qwen2.5-7B-Instruct     71.5      74.1       79.4       81.3      75.3       57.9      47.0        −          65.9        74.0
    LLaMA3.1-8B-Instruct    72.6      77.3       80.8       84.2      71.3       62.8      54.6        −          65.9        71.0
    TULU 3                  79.7      82.8       85.1       87.5      82.1       63.2      51.2       48.9        70.3        72.0
    Crab-7B-DPO             47.3      57.1       59.7       67.9      47.2       36.5      28.9        −          56.3        62.0
    Conifer-7B-DPO          48.1      52.3       59.1       63.3      50.7       37.6      26.6        −          56.9        62.0
    UltraIF-8B-DPO†         71.3      75.4       79.4       83.1      69.6       58.3      46.9        −          62.6         −
    R1-Distill-Qwen-7B      59.9      65.1       70.4       74.2      55.8       43.6      32.7       16.9        53.9        66.0
      +V ER IF              75.6      79.5       82.7       85.5      66.0       53.8      41.9       26.5        61.0        68.0
    TULU 3 SFT              68.4      71.7       76.3       79.5      67.3       50.9      40.3       33.2        62.0        63.0
      +V ER IF              84.5      87.1       89.3       91.4      79.4       65.2      54.0       54.7        68.6        72.0

Table 2: Experimental results (%) on several representative instruction-following benchmarks. “Pr.” and “Ins.”
denote prompt-level and instruction-level metrics respectively. “S” and “L” mean strict and loose respectively. †
denotes the results are sourced from the original paper (An et al., 2025). All the other results are reproduced by us
in this paper. For reasoning LLMs, we remove the thinking tokens and evaluate using only the final response.


we input all soft constraints Cs to the LLM at once                       et al., 2024b), which includes multi-turn and multi-
to assess whether the response satisfies all of them                      lingual instruction following; SysBench (Qin et al.,
in a single pass. We conduct RL training using the                        2024), which evaluates instruction following to sys-
VeRL framework2 and integrate a parallel reward                           tem prompts; FollowBench (Jiang et al., 2024) and
computation mechanism to accelerate RL training.                          CFBench (Zhang et al., 2024a), which cover a com-
                                                                          prehensive range of constraint types.
4        Experiments
                                                                          4.2    Main Results
This section introduces experimental setup (§ 4.1),
main results (§ 4.2), analytical experiments (§§ 4.3                      All experimental results are presented in Table 2.
to 4.5), and developing a smaller verifier (§ 4.6).                       We have the following observations: (1) Reinforce-
                                                                          ment learning with V ER IF demonstrates strong per-
4.1       Experimental Setup                                              formance. Compared to their corresponding back-
Reported Models We conduct RL training based                              bones (R1-Distill-Qwen-7B and TULU 3 SFT),
on two SFT-trained models: TULU 3 SFT (Lam-                               the trained models using RL perform much bet-
bert et al., 2024) and DeepSeek-R1-Distill-Qwen-                          ter. Notably, the model trained based on TULU 3
7B (Guo et al., 2025). For the specific implemen-                         SFT even outperforms the original TULU 3 (Lam-
tation of V ER IF, we use QwQ-32B as the LLM                              bert et al., 2024), which is trained based on TULU
verifier and set F in Equation 3.1 as average. For                        3 SFT using approximately 271k DPO pairs and
comparison, we evaluate TULU 3 (Lambert et al.,                           specialized RLVR data. Among models with sim-
2024), which is trained directly based on TULU                            ilar parameter scales, the model trained based on
3 SFT with extensive DPO and RLVR training.                               TULU 3 SFT achieves state-of-the-art performance
We also evaluate various industrial models, includ-                       and surpasses several open-source models devel-
ing GPT-4o (Hurst et al., 2024), QwQ-32B (Qwen,                           oped by industry using larger datasets and more
2025), Qwen2.5-7B-Instruct (Yang et al., 2024),                           resources. This demonstrates the potential of RL
LLaMA3.1-8B-Instruct (Grattafiori et al., 2024),                          training for instruction following and the effective-
and open-source models specifically optimized for                         ness of V ER IF in providing reliable rewards. (2)
instruction following, including Conifer (Sun et al.,                     RL with V ER IF generalizes effectively to unseen
2024), Crab (Qi et al., 2024), and UltraIF (An et al.,                    instruction-following tasks. Although the training
2025). More details are placed in appendix B.                             dataset V ER I NSTRUCT contains only English and
                                                                          single-turn instruction-following data, the trained
Evaluation benchmarks We evaluate the mod-
                                                                          model shows substantial improvements on multi-
els on several representative instruction-following
                                                                          lingual, multi-turn (Multi-IF) instruction following,
benchmarks, including IFEval (Zhou et al., 2023),
                                                                          and following system prompts (SysBench). This
the most commonly used dataset; Multi-IF (He
                                                                          suggests that the patterns of instruction following
     2
         https://github.com/volcengine/verl                               may be inherently generalizable and that RL further

                                                                      5
      Model                  AlpacaEval 2.0   MT-Bench   GSM8K       Omni-MATH         MMLU-Pro        BBH       DROP
      Qwen2.5-7B-Instruct        37.5           7.8          91.4        13.6             56.5          71.8      77.2
      Llama3.1-8B-Instruct       29.4           6.0          83.6        10.8             48.1          63.0      74.4
      TULU 3                     39.9           7.5          88.4        14.2             35.9          68.5      69.4
      R1-Distill-Qwen-7B         16.6           5.7          87.0        35.0             54.3          21.5      74.0
        +V ER IF                 15.5           5.9          90.0        33.6             54.8          32.2      75.6
      TULU 3 SFT                  7.9           6.3          78.8        11.4             36.4          67.4      58.3
        +V ER IF                 22.0           7.0          83.4        12.4             36.0          67.9      59.5

                 Table 3: Experimental results (%) on various general natural language benchmarks.


enhances this generalization (Chu et al., 2025). (3)                                   TULU3 + VerIF           TULU3
RL with V ER IF benefits both reasoning and non-                  Startend
reasoning models. As reinforcement learning has                Punctuation
demonstrated its effectiveness in enhancing reason-                 Length
ing abilities on challenging tasks (Guo et al., 2025;            Language
                                                                 Keywords
Luo et al., 2025a), such as math and code, we sug-               D. Format
gest integrating instruction-following training into            D. Content
RL pipelines. Our further analysis (§ 4.3) shows              Combination
that general capabilities, such as mathematical rea-          Change Case
soning and language understanding, do not degrade                            50   60        70         80       90       100
                                                                                           Accuracy (%)
after RL with V ER IF and may even slightly im-
prove, indicating that RL with V ER IF can be inte-          Figure 5: Prompt-level strict scores (%) across different
grated into broader model development for enhanc-            types of constraints on IFEval. “D.” denotes Detectable.
ing the model’s instruction following capabilities.
(4) Models developed by the academic community,
                                                             natural language understanding datasets: MMLU-
such as Conifer, Crab, and UltraIF, show relatively
                                                             Pro (Wang et al.) and DROP (Dua et al., 2019), and
lower performance, which is reasonable given their
                                                             a natural language inference benchmark BBH (Suz-
focus on exploring effective SFT data synthesis
                                                             gun et al., 2023). The results are shown in Table 3.
and limited training resources. Given that there is
                                                             We can observe that RL training does not degrade
abundant open-source SFT data, such as Infinity In-
                                                             general performance and even improves the perfor-
struct (BAAI, 2024) with approximately 7 million
                                                             mance in some cases, such as MT-Bench, GSM8K,
instances, we encourage the research community
                                                             and BBH. We attribute this to a key difference
to devote more attention to constructing RL data
                                                             between RL and SFT: while SFT learns and memo-
instead, as RL data remains scarce and RL has been
                                                             rizes patterns from data and is prone to catastrophic
demonstrated to be effective for instruction follow-
                                                             forgetting (Chu et al., 2025), RL typically maxi-
ing. In conclusion, RL with V ER IF effectively en-
                                                             mizes optimal patterns it has learned (Yue et al.,
hances instruction-following capabilities, and we
                                                             2025b), thereby reducing the risk of knowledge for-
encourage more efforts on developing effective RL
                                                             getting. These results suggest a promising finding
methods or data for instruction-following.
                                                             that instruction-following reinforcement learning
                                                             can be integrated into existing RL pipelines to en-
4.3    Analysis on General Capabilities
                                                             hance adherence to instructions without compro-
We further investigate the general capabilities of the       mising the model’s general capabilities.
trained models to assess the broader impact of RL
with V ER IF. Specifically, we conduct an evaluation         4.4    Analysis on Constraint Types
on various representative general benchmarks, in-            V ER I NSTRUCT includes only five constraint types:
cluding general instruction-following datasets that          length, keyword, format, content, and style. We fur-
focus on task completion and are evaluated using             ther investigate the improvements across different
LLM-as-a-judge: AlpacaEval 2.0 (Dubois et al.,               constraint types in IFEval to analyze the general-
2024) and MT-Bench (Zheng et al., 2023), math-               ization of constraint adherence. Results are shown
ematical reasoning benchmarks: GSM8K (Cobbe                  in Figure 5. We observe clear improvements across
et al., 2021) and Omni-Math (Gao et al., 2025),              most types except for “Startend” and “Language”

                                                         6
     0.8                                                                         0.8
     0.7                                                                         0.7
     0.6                                                                         0.6
Reward




                                                                            Reward
     0.5                                                                         0.5
     0.4                                                                         0.4
     0.3         VerIF             w/o code          VerIF (Qwen-2.5)            0.3        VerIF (QwQ-32B)        VerIF (Qwen-7B)
                 w/o code*         w/o llm                                                  VerIF (IF-Verifier-7B)
     0.2 0        25    50    75    100 125 150 175 200                          0.2 0      25 50 75 100 125 150 175 200
                                   Step                                                                   Step
 Figure 6: Reward curves during RL training with dif-                        Figure 7: Reward curves during RL training using dif-
 ferent verification methods. We visualize the first 200                     ferent LLM verifiers in V ER IF. Qwen-7B is short for
 steps and smooth the data for better visualization.                         DeepSeek-R1-Distilled-Qwen-7B.

         Model                IFEval      Multi-IF      CFBench
                                                                             contrast, using only LLM verification results in
         V ER IF               84.5           54.0        72.0
           w/o code*           81.7           51.2        70.0               higher and more pronounced reward growth, pos-
           w/o code            76.2           52.0        73.0               sibly because the LLM verifier is easier to fit or
           w/o LLM             74.7           46.0        59.0               hack (Li et al., 2024). The results are shown in
         V ER IF (Qwen-2.5)    76.9           48.5        71.0               Table 4. We can observe that removing any veri-
                                                                             fication component degrades model performance
 Table 4: Ablation results (%) for different verification                    compared to V ER IF. Notably, “w/o LLM”, which
 methods. “Qwen-2.5” uses Qwen2.5-72B-Instruct as
                                                                             uses only Python scripts for hard constraint veri-
 the LLM instead of QwQ-32B. We report the prompt-
 level strict score for IFEval, the Turn 3 score for Multi-                  fication, performs significantly poorly. This may
 IF, and the ISR score for CFBench.                                          be due to that approximately 77.7% constraints in
                                                                             training data are soft. This suggests that using code
                                                                             verification for hard constraints only, as adopted
 (which already achieves 100% accuracy). This in-                            in training TULU 3 (Lambert et al., 2024), is sub-
 dicates that RL training can generalize instruction-                        optimal for RL in instruction following. We also
 following ability to unseen constraint types. For                           adopt Qwen2.5-72B-Instruct as the LLM verifier
 constraint types covered in V ER I NSTRUCT, such                            in V ER IF and find it significantly underperforms
 as length, keyword, and content, the improvements                           QwQ-32B. The potential reason may be that in our
 are more pronounced, which demonstrates the pre-                            implementation of V ER IF, the LLM is required
 cision of the verification provided by V ER IF. This                        to verify whether a response satisfies all soft con-
 also suggests that incorporating datasets with richer                       straints in a single pass, which requires step-by-step
 constraint types can further improve performance.                           reasoning and poses significant challenges. The
 We encourage the community to explore more di-                              results demonstrate the potential of scaling up ver-
 verse data for RL for instruction following.                                ification (Liu et al., 2025b). In conclusion, we
                                                                             suggest that the best practice for verification in RL
 4.5        Ablation Studies                                                 for instruction following is V ER IF with reasoning
 We conduct ablation studies on the verification                             models as the LLM verifier. We further explore a
 method. Specifically, we perform three ablations:                           smaller reasoning LLM as the verifier in § 4.6.
 (1) “w/o code*”, which uses only the LLM to verify
 all constraints; (2) “w/o code”, which uses only the                        4.6       Training a Smaller Verifier
 LLM for soft constraints; (3) “w/o LLM”, which                              Although we have demonstrated V ER IF with a
 verifies only hard constraints using Python code                            large reasoning model, such as QwQ-32B, is ef-
 scripts. We conduct RL training using different                             fective for RL in instruction following, the long
 verification methods based on TULU 3 SFT. The                               outputs of QwQ-32B lead to high latency during
 reward curves during training are shown in Fig-                             online reward computation. For example, when
 ure 6. We observe that using only code verification                         training TULU 3 SFT, we adopt 8 H800 GPUs for
 yields lower rewards and limited growth, likely due                         deploying QwQ-32B and set batch size to 32, roll-
 to the difficulty of following hard constraints. In                         outs to 16, and the average time to obtain the reward

                                                                        7
                                                 IFEval                            Multi-IF            SysBench   FollowBench   CFBench
    Model
                               Pr. (S)   Pr. (L)    Ins. (S)   Ins. (L)   Turn 1   Turn 2     Turn 3     ISR         SSR          ISR
    V ER IF (QwQ-32B)           84.5      87.1       89.3       91.4      79.4      65.2      54.0       54.7        68.6        72.0
    V ER IF (Qwen-7B)           77.1      80.4       84.3       86.6      78.5      60.8      49.0       42.7        62.0        72.0
    V ER IF (IF-Verifier-7B)    80.0      84.5       86.0       89.4      80.1      63.7      52.7       49.5        68.8        70.0

Table 5: Experimental results (%) of models trained using different LLM verifiers. Qwen-7B is short for DeepSeek-
R1-Distilled-Qwen-7B. The base model used for RL training is TULU 3 SFT.


for a batch reaches about 180 seconds, accounting                             et al., 2024; He et al., 2024a; Dong et al., 2024;
for roughly 80% of the time per training step. To                             Ren et al., 2025), back-translation (Qi et al., 2024;
address this, we explore using smaller reasoning                              Pham et al., 2024), and training dedicated instruc-
models as LLM verifiers while maintaining compa-                              tion composers (An et al., 2025), and (2) collecting
rable performance. A straightforward approach is                              preference pairs (Cheng et al., 2024; Pham et al.,
to distill a verifier from QwQ-32B. Therefore, we                             2024; Dong et al., 2024; Zhang et al., 2024b). No-
distill 130k SFT data instances from QwQ, where                               tably, two works are similar to ours: AutoIF (Dong
each instance consists of an instruction, a response,                         et al., 2024), which constructs both instructions
and a critic indicating whether a response satisfies                          and corresponding verification code, but but does
the given constraints in the instruction. The data                            not explore RL training or soft constraints verifi-
collection process is detailed in Appendix C.                                 cation; and TULU 3 (Lambert et al., 2024), which
   We fine-tune DeepSeek-R1-Distill-Qwen-7B on                                adopts RLVR for instruction following but the im-
the collected dataset, resulting in IF-Verifier-7B.                           provement is limited and also does not consider
We then conduct RL training on TULU 3 SFT using                               soft constraints. In summary, the best practice for
the new LLM verifiers in V ER IF. Figure 7 shows                              RL in instruction following remains underexplored.
the reward curves during training. We can observe                                As RL has proven to be an effective post-training
that DeepSeek-R1-Distill-Qwen-7B yields higher                                technique, many prior studies have explored its ap-
initial rewards, but its reward growth is limited.                            plications across various domains, primarily focus-
IF-Verifier-7B exhibits a similar reward trajectory                           ing on verification engineering, such as math (Lam-
as QwQ-32B. The results of the trained models                                 bert et al., 2024; Guo et al., 2025; Luo et al., 2025b;
are shown in Table 5. We observe that using IF-                               ByteDance-Seed, 2025), code (Wang et al., 2024b;
Verifier-7B as the LLM verifier in V ER IF signifi-                           Luo et al., 2025a), logic (Xie et al., 2025), tool
cantly outperforms DeepSeek-R1-Distill-Qwen-7B                                using (Feng et al., 2025; Jin et al., 2025; Qian et al.,
and achieves competitive performance to QwQ-                                  2025a; Li et al., 2025; Zheng et al., 2025), machine
32B. Moreover, IF-Verifier-7B reduces computa-                                translation (Wang et al., 2024a; He et al., 2025),
tional cost a lot. Deploying IF-Verifier-7B requires                          medicine (Chen et al., 2024; Wang et al., 2025),
only one single H800 GPU, with an average re-                                 and finance (Qian et al., 2025b; Liu et al., 2025a).
ward computation time of 120 seconds per batch,                               In this work, we explore the best practice of RL
which can be further reduced with multi-GPUs.                                 for instruction following and propose V ER IF, an
This makes V ER IF a practical method for effective                           effective verification method for RL training.
RL training under limited resources. This work
preliminarily explores more efficient LLM verifiers                           6    Conclusion
and encourages further efforts (Liu et al., 2025b).                           In this work, we propose V ER IF, an effective verifi-
                                                                              cation method for RL in instruction following. We
5      Related Work
                                                                              also construct V ER I NSTRUCT, a dataset for instruc-
Instruction following requires models to generate                             tion following where each instruction is paired with
responses that satisfy complex user instructions.                             corresponding verification signals. We perform RL
Recent work has primarily focused on following                                training with V ER IF on V ER I NSTRUCT, leading
constraints in instructions, such as length and key-                          to significant improvements. The trained models
word (Zhou et al., 2023). Existing efforts to en-                             achieve SoTA performance on several representa-
hance instruction-following capabilities primarily                            tive instruction-following benchmarks at a similar
focus on methods for (1) collecting SFT data, in-                             model scale, without hurting general capabilities.
cluding directly distilling from larger LLMs (Sun                             This work demonstrates the promising potential

                                                                          8
of RL in instruction following, and we encourage               Advancing instruction following from the wild. arXiv
further exploration of novel RL methods and data.              preprint arXiv:2502.04153.
                                                             BAAI. 2024.    Infinity instruct.     arXiv preprint
Limitations                                                    arXiv:2406.XXXX.

We discuss the limitations of our work here, in-             Thomas Ball, Shuo Chen, and Cormac Herley. 2024.
cluding two main aspects: (1) The training dataset             Can we count on llms? the fixed-effect fallacy and
                                                               claims of gpt-4 capabilities. Transactions on Ma-
V ER I NSTRUCT includes only English data, which               chine Learning Research.
may limit the broader usage of the dataset. We
observe that RL on V ER I NSTRUCT still general-             ByteDance-Seed. 2025. Seed1.5-thinking: Advancing
                                                               superb reasoning models with reinforcement learning.
izes well to multiple languages, and we encourage              Preprint, arXiv:2504.13914.
the community to collect more diverse data cover-
ing more languages. (2) V ER IF relies on an LLM             Junying Chen, Zhenyang Cai, Ke Ji, Xidong Wang,
                                                               Wanlong Liu, Rongsheng Wang, Jianye Hou, and
as the verifier, which inherits common issues of
                                                               Benyou Wang. 2024. Huatuogpt-o1, towards med-
LLM-as-a-judge, such as potential biases (Ye et al.,           ical complex reasoning with llms. arXiv preprint
2024) and vulnerability to adversarial attacks (Shi            arXiv:2412.18925.
et al., 2024). We believe developing more robust
                                                             Jiale Cheng, Xiao Liu, Cunxiang Wang, Xiaotao Gu,
and efficient LLM judges (Liu et al., 2025b) is a               Yida Lu, Dan Zhang, Yuxiao Dong, Jie Tang, Hongn-
promising direction and leave it for future work.               ing Wang, and Minlie Huang. 2024. Spar: Self-play
                                                                with tree-search refinement to improve instruction-
Ethical Considerations                                          following in large language models. arXiv preprint
                                                                arXiv:2412.11605.
We discuss potential ethical concerns as follows:            Tianzhe Chu, Yuexiang Zhai, Jihan Yang, Sheng-
(1) Intellectual property. Alpaca-GPT4 and Infinity-           bang Tong, Saining Xie, Dale Schuurmans, Quoc V
Instruct are licensed under CC BY-NC 4.03 , Ope-               Le, Sergey Levine, and Yi Ma. 2025. Sft mem-
nAssistant is licensed under Apache License 2.04 .             orizes, rl generalizes: A comparative study of
                                                               foundation model post-training. arXiv preprint
WildChat is licensed under ODC-By license5 . Evol-
                                                               arXiv:2501.17161.
Instruct and Orca-Chat do not specify explicit li-
censes. We strictly adhered to all claimed licenses.         Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian,
Our dataset will be released under the Apache Li-              Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias
                                                               Plappert, Jerry Tworek, Jacob Hilton, Reiichiro
cense 2.0. We believe the original open-source                 Nakano, and 1 others. 2021. Training verifiers
datasets are properly anonymized, and we do not                to solve math word problems. arXiv preprint
introduce any additional sensitive information. (2)            arXiv:2110.14168.
Potential risk control. In this paper, we propose            Guanting Dong, Keming Lu, Chengpeng Li, Tingyu
V ER IF, a verification method for RL to improve               Xia, Bowen Yu, Chang Zhou, and Jingren Zhou.
instruction-following capabilities of LLMs. As                 2024. Self-play with execution feedback: Improving
V ER IF includes an LLM verifier, it inherits the              instruction-following capabilities of large language
                                                               models. arXiv preprint arXiv:2406.13542.
known risks of LLMs, such as potential bias (Gal-
legos et al., 2024; Ye et al., 2024). We do not intro-       Dheeru Dua, Yizhong Wang, Pradeep Dasigi, Gabriel
duce any additional risks. Users should not exploit            Stanovsky, Sameer Singh, and Matt Gardner. 2019.
                                                               Drop: A reading comprehension benchmark requir-
V ER IF for reward hacking (Skalse et al., 2022) and           ing discrete reasoning over paragraphs. In Proceed-
are responsible for verifying the compliance of the            ings of NAACL-HLT, pages 2368–2378.
models trained using it. (3) AI assistance. We use
                                                             Yann Dubois, Balázs Galambosi, Percy Liang, and Tat-
ChatGPT and Claude to refine some sentences.
                                                               sunori B Hashimoto. 2024. Length-controlled al-
                                                               pacaeval: A simple way to debias automatic evalua-
                                                               tors. arXiv preprint arXiv:2404.04475.
References
                                                             Shahul Es. 2023.        Orca-chat:   A high-quality
Kaikai An, Li Sheng, Ganqu Cui, Shuzheng Si, Ning              explanation-style chat dataset.
  Ding, Yu Cheng, and Baobao Chang. 2025. Ultraif:
                                                             Jiazhan Feng, Shijue Huang, Xingwei Qu, Ge Zhang,
     3
         https://creativecommons.org/licenses/by-nc/4.          Yujia Qin, Baoquan Zhong, Chengquan Jiang, Jinxin
0/                                                              Chi, and Wanjun Zhong. 2025. Retool: Reinforce-
     4
         https://www.apache.org/licenses/LICENSE-2.0            ment learning for strategic tool use in llms. arXiv
     5
         https://opendatacommons.org/licenses/by/1-0/           preprint arXiv:2504.11536.


                                                         9
Tairan Fu, Raquel Ferrando, Javier Conde, Carlos Ar-           Bowen Jin, Hansi Zeng, Zhenrui Yue, Jinsung Yoon,
  riaga, and Pedro Reviriego. 2024. Why do large lan-            Sercan Arik, Dong Wang, Hamed Zamani, and Jiawei
  guage models (llms) struggle to count letters? arXiv           Han. 2025. Search-r1: Training llms to reason and
  preprint arXiv:2412.18626.                                     leverage search engines with reinforcement learning.
                                                                 arXiv preprint arXiv:2503.09516.
Isabel O Gallegos, Ryan A Rossi, Joe Barrow,
   Md Mehrab Tanjim, Sungchul Kim, Franck Dernon-              Andreas Köpf, Yannic Kilcher, Dimitri von Rütte,
   court, Tong Yu, Ruiyi Zhang, and Nesreen K Ahmed.             Sotiris Anagnostidis, Zhi Rui Tam, Keith Stevens,
   2024. Bias and fairness in large language models:             Abdullah Barhoum, Duc Nguyen, Oliver Stanley,
   A survey. Computational Linguistics, 50(3):1097–              Richárd Nagyfi, and 1 others. 2024. Openassistant
   1179.                                                         conversations-democratizing large language model
                                                                 alignment. Advances in NeurlPS, 36.
Bofei Gao, Feifan Song, Zhe Yang, Zefan Cai, Yibo
  Miao, Chenghao Ma, Shanghaoran Quan, Liang                   Nathan Lambert, Jacob Morrison, Valentina Pyatkin,
  Chen, Qingxiu Dong, Runxin Xu, and 1 others. 2025.             Shengyi Huang, Hamish Ivison, Faeze Brahman,
  Omni-math: A universal olympiad level mathematic               Lester James V Miranda, Alisa Liu, Nouha Dziri,
  benchmark for large language models. In Proceed-               Shane Lyu, and 1 others. 2024. T\" ulu 3: Pushing
  ings of ICLR.                                                  frontiers in open language model post-training. arXiv
                                                                 preprint arXiv:2411.15124.
Aaron Grattafiori, Abhimanyu Dubey, Abhinav Jauhri,
  Abhinav Pandey, Abhishek Kadian, Ahmad Al-                   Dawei Li, Bohan Jiang, Liangjie Huang, Alimoham-
  Dahle, Aiesha Letman, Akhil Mathur, Alan Schelten,             mad Beigi, Chengshuai Zhao, Zhen Tan, Amrita
  Alex Vaughan, and 1 others. 2024. The llama 3 herd             Bhattacharjee, Yuxuan Jiang, Canyu Chen, Tian-
  of models. arXiv preprint arXiv:2407.21783.                    hao Wu, and 1 others. 2024. From generation to
                                                                 judgment: Opportunities and challenges of llm-as-a-
Daya Guo, Dejian Yang, Haowei Zhang, Junxiao                     judge. arXiv preprint arXiv:2411.16594.
  Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu, Shi-
  rong Ma, Peiyi Wang, Xiao Bi, and 1 others. 2025.            Xuefeng Li, Haoyang Zou, and Pengfei Liu. 2025.
  Deepseek-r1: Incentivizing reasoning capability in             Torl: Scaling tool-integrated rl. arXiv preprint
  llms via reinforcement learning. arXiv preprint                arXiv:2503.23383.
  arXiv:2501.12948.
                                                               Zhaowei Liu, Xin Guo, Fangqi Lou, Lingfeng Zeng,
Minggui He, Yilun Liu, Shimin Tao, Yuanchang Luo,                Jinyi Niu, Zixuan Wang, Jiajie Xu, Weige Cai, Zi-
  Hongyong Zeng, Chang Su, Li Zhang, Hongxia                     wei Yang, Xueqian Zhao, and 1 others. 2025a. Fin-
  Ma, Daimeng Wei, Weibin Meng, and 1 others.                    r1: A large language model for financial reason-
  2025. R1-t1: Fully incentivizing translation capa-             ing through reinforcement learning. arXiv preprint
  bility in llms via reasoning learning. arXiv preprint          arXiv:2503.16252.
  arXiv:2502.19735.
                                                               Zijun Liu, Peiyi Wang, Runxin Xu, Shirong Ma, Chong
Qianyu He, Jie Zeng, Qianxi He, Jiaqing Liang, and                Ruan, Peng Li, Yang Liu, and Yu Wu. 2025b.
  Yanghua Xiao. 2024a. From complex to simple: En-                Inference-time scaling for generalist reward model-
  hancing multi-constraint complex instruction follow-            ing. arXiv preprint arXiv:2504.02495.
  ing ability of large language models. In Findings of
  ACL, pages 10864–10882.                                      Michael Luo, Sijun Tan, Roy Huang, Ameen Patel, Al-
                                                                 pay Ariyak, Qingyang Wu, Xiaoxiang Shi, Rachel
Yun He, Di Jin, Chaoqi Wang, Chloe Bi, Karishma                  Xin, Colin Cai, Maurice Weber, Ce Zhang, Li Erran
  Mandyam, Hejia Zhang, Chen Zhu, Ning Li, Tengyu                Li, Raluca Ada Popa, and Ion Stoica. 2025a. Deep-
  Xu, Hongjiang Lv, Shruti Bhosale, Chen Zhu,                    coder: A fully open-source 14b coder at o3-mini
  Karthik Abinav Sankararaman, Eryk Helenowski,                  level. Notion Blog.
  Melissa Hall Melanie Kambadur, Aditya Tayade, Hao
  Ma, Han Fang, and Si-Ying Wang. 2024b. Multi-if:             Michael Luo, Sijun Tan, Justin Wong, Xiaoxiang Shi,
  Benchmarking llms on multi-turn and multilingual              William Y. Tang, Manan Roongta, Colin Cai, Jeffrey
  instructions following. ArXiv, abs/2410.15553.                 Luo, Li Erran Li, Raluca Ada Popa, and Ion Stoica.
                                                                 2025b. Deepscaler: Surpassing o1-preview with a
Aaron Hurst, Adam Lerer, Adam P Goucher, Adam                   1.5b model by scaling rl. Notion Blog.
  Perelman, Aditya Ramesh, Aidan Clark, AJ Ostrow,
  Akila Welihinda, Alan Hayes, Alec Radford, and 1             Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida,
  others. 2024. Gpt-4o system card. arXiv preprint               Carroll Wainwright, Pamela Mishkin, Chong Zhang,
  arXiv:2410.21276.                                              Sandhini Agarwal, Katarina Slama, Alex Ray, and
                                                                 1 others. 2022. Training language models to follow
Yuxin Jiang, Yufei Wang, Xingshan Zeng, Wanjun                   instructions with human feedback. In Proceedings of
  Zhong, Liangyou Li, Fei Mi, Lifeng Shang, Xin                  NeurIPs.
  Jiang, Qun Liu, and Wei Wang. 2024. Follow-
  bench: A multi-level fine-grained constraints fol-           Baolin Peng, Chunyuan Li, Pengcheng He, Michel Gal-
  lowing benchmark for large language models. In                 ley, and Jianfeng Gao. 2023. Instruction tuning with
  Proceedings of ACL, pages 4667–4688.                           gpt-4. arXiv preprint arXiv:2304.03277.


                                                          10
Hao Peng, Yunjia Qi, Xiaozhi Wang, Zijun Yao, Bin               Haoran Sun, Lixin Liu, Junjie Li, Fengyu Wang, Bao-
  Xu, Lei Hou, and Juanzi Li. 2025. Agentic reward                hua Dong, Ran Lin, and Ruohui Huang. 2024.
  modeling: Integrating human preferences with verifi-            Conifer: Improving complex constrained instruction-
  able correctness signals for reliable reward systems.           following ability of large language models. arXiv
  arXiv preprint arXiv:2502.19328.                                preprint arXiv:2404.02823.

Chau Pham, Simeng Sun, and Mohit Iyyer. 2024. Suri:             Mirac Suzgun, Nathan Scales, Nathanael Schärli, Se-
  Multi-constraint instruction following in long-form             bastian Gehrmann, Yi Tay, Hyung Won Chung,
  text generation. In Findings of ACL, pages 1722–                Aakanksha Chowdhery, Quoc V Le, Ed H Chi, Denny
  1753.                                                           Zhou, and 1 others. 2023. Challenging big-bench
                                                                  tasks and whether chain-of-thought can solve them.
Yunjia Qi, Hao Peng, Xiaozhi Wang, Bin Xu, Lei Hou,               In Findings of ACL.
  and Juanzi Li. 2024. Constraint back-translation im-
  proves complex instruction following of large lan-            Lewis Tunstall, Edward Beeching, Nathan Lambert,
  guage models. arXiv preprint arXiv:2410.24175.                  Nazneen Rajani, Shengyi Huang, Kashif Rasul, Al-
                                                                  varo Bartolome, Alexander M. Rush, and Thomas
Cheng Qian, Emre Can Acikgoz, Qi He, Hongru Wang,                 Wolf. The Alignment Handbook.
  Xiusi Chen, Dilek Hakkani-Tür, Gokhan Tur, and                Bingning Wang, Haizhou Zhao, Huozhi Zhou, Liang
  Heng Ji. 2025a. Toolrl: Reward is all tool learning             Song, Mingyu Xu, Wei Cheng, Xiangrong Zeng, Yu-
  needs. arXiv preprint arXiv:2504.13958.                         peng Zhang, Yuqi Huo, Zecheng Wang, and 1 oth-
                                                                  ers. 2025. Baichuan-m1: Pushing the medical ca-
Lingfei Qian, Weipeng Zhou, Yan Wang, Xueqing Peng,
                                                                  pability of large language models. arXiv preprint
  Han Yi, Jimin Huang, Qianqian Xie, and Jianyun
                                                                  arXiv:2502.12671.
  Nie. 2025b. Fino1: On the transferability of rea-
  soning enhanced llms to finance. arXiv preprint               Jiaan Wang, Fandong Meng, Yunlong Liang, and Jie
  arXiv:2502.08127.                                                Zhou. 2024a. Drt-o1: Optimized deep reasoning
                                                                   translation via long chain-of-thought. arXiv e-prints,
Yanzhao Qin, Tao Zhang, Yanjun Shen, Wenjing Luo,                  pages arXiv–2412.
  Haoze Sun, Yan Zhang, Yujing Qiao, Weipeng Chen,
  Zenan Zhou, Wentao Zhang, and 1 others. 2024. Sys-            Junqiao Wang, Zeng Zhang, Yangfan He, Yuyang Song,
  bench: Can large language models follow system                  Tianyu Shi, Yuchen Li, Hengyuan Xu, Kunyu Wu,
  messages? arXiv preprint arXiv:2408.10943.                      Guangwu Qian, Qiuwu Chen, and 1 others. 2024b.
                                                                  Enhancing code llms with reinforcement learning in
Team Qwen. 2025. Qwq-32b: Reward model for factu-                 code generation. arXiv preprint arXiv:2412.20367.
  ality and harmlessness. Accessed: 2025-05-13.
                                                                Yubo Wang, Xueguang Ma, Ge Zhang, Yuansheng Ni,
Rafael Rafailov, Archit Sharma, Eric Mitchell, Christo-           Abhranil Chandra, Shiguang Guo, Weiming Ren,
  pher D Manning, Stefano Ermon, and Chelsea Finn.                Aaran Arulraj, Xuan He, Ziyan Jiang, and 1 others.
  2023. Direct preference optimization: Your language             Mmlu-pro: A more robust and challenging multi-task
  model is secretly a reward model. In Proceedings of             language understanding benchmark. In The Thirty-
  NeurIPs.                                                        eight Conference on Neural Information Processing
                                                                  Systems Datasets and Benchmarks Track.
Qingyu Ren, Jie Zeng, Qianyu He, Jiaqing Liang,
  Yanghua Xiao, Weikang Zhou, Zeye Sun, and Fei                 Tian Xie, Zitian Gao, Qingnan Ren, Haoming Luo,
  Yu. 2025. Step-by-step mastery: Enhancing soft con-             Yuqian Hong, Bryan Dai, Joey Zhou, Kai Qiu, Zhi-
  straint following ability of large language models.             rong Wu, and Chong Luo. 2025. Logic-rl: Un-
  arXiv preprint arXiv:2501.04945.                                leashing llm reasoning with rule-based reinforcement
                                                                  learning. arXiv preprint arXiv:2502.14768.
Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Jun-            Can Xu, Qingfeng Sun, Kai Zheng, Xiubo Geng,
  Mei Song, Mingchuan Zhang, Y. K. Li, Yu Wu, and                 Pu Zhao, Jiazhan Feng, Chongyang Tao, and Daxin
  Daya Guo. 2024. Deepseekmath: Pushing the limits                Jiang. 2023. Wizardlm: Empowering large lan-
  of mathematical reasoning in open language models.              guage models to follow complex instructions. arXiv
  ArXiv, abs/2402.03300.                                          preprint arXiv:2304.12244.
Jiawen Shi, Zenghui Yuan, Yinuo Liu, Yue Huang, Pan             An Yang, Baosong Yang, Beichen Zhang, Binyuan Hui,
   Zhou, Lichao Sun, and Neil Zhenqiang Gong. 2024.               Bo Zheng, Bowen Yu, Chengyuan Li, Dayiheng Liu,
   Optimization-based prompt injection attack to llm-as-          Fei Huang, Haoran Wei, and 1 others. 2024. Qwen2.
   a-judge. In Proceedings of the 2024 on ACM SIGSAC              5 technical report. arXiv preprint arXiv:2412.15115.
   Conference on Computer and Communications Secu-
   rity, pages 660–674.                                         Jiayi Ye, Yanbo Wang, Yue Huang, Dongping Chen,
                                                                   Qihui Zhang, Nuno Moniz, Tian Gao, Werner Geyer,
Joar Skalse, Nikolaus Howe, Dmitrii Krasheninnikov,                Chao Huang, Pin-Yu Chen, and 1 others. 2024. Jus-
  and David Krueger. 2022. Defining and characteriz-               tice or prejudice? quantifying biases in llm-as-a-
  ing reward hacking. Advances in Neural Information               judge. In Neurips Safe Generative AI Workshop
  Processing Systems, 35:9460–9471.                                2024.


                                                           11
Yang Yue, Zhiqi Chen, Rui Lu, Andrew Zhao, Zhaokai
  Wang, Shiji Song, and Gao Huang. 2025a. Does
  reinforcement learning really incentivize reasoning
  capacity in llms beyond the base model? arXiv
  preprint arXiv:2504.13837.
Yang Yue, Zhiqi Chen, Rui Lu, Andrew Zhao, Zhaokai
  Wang, Yang Yue, Shiji Song, and Gao Huang. 2025b.
  Does reinforcement learning really incentivize rea-
  soning capacity in llms beyond the base model?
  Preprint, arXiv:2504.13837.
Tao Zhang, Yanjun Shen, Wenjing Luo, Yan Zhang, Hao
  Liang, Fan Yang, Mingan Lin, Yujing Qiao, Weipeng
  Chen, Bin Cui, and 1 others. 2024a. Cfbench: A
  comprehensive constraints-following benchmark for
  llms. arXiv preprint arXiv:2408.01122.
Xinghua Zhang, Haiyang Yu, Cheng Fu, Fei Huang,
  and Yongbin Li. 2024b. Iopo: Empowering llms with
  complex instruction following via input-output prefer-
  ence optimization. arXiv preprint arXiv:2411.06208.
Wenting Zhao, Xiang Ren, Jack Hessel, Claire Cardie,
 Yejin Choi, and Yuntian Deng. 2024. Wildchat: 1m
 chatgpt interaction logs in the wild. In Proceedings
 of ICLR.
Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan
  Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin,
  Zhuohan Li, Dacheng Li, Eric Xing, and 1 others.
  2023. Judging llm-as-a-judge with mt-bench and
  chatbot arena. Advances in Neural Information Pro-
  cessing Systems, 36:46595–46623.

Yuxiang Zheng, Dayuan Fu, Xiangkun Hu, Xiaojie Cai,
  Lyumanshan Ye, Pengrui Lu, and Pengfei Liu. 2025.
  Deepresearcher: Scaling deep research via reinforce-
  ment learning in real-world environments. arXiv
  preprint arXiv:2504.03160.

Jeffrey Zhou, Tianjian Lu, Swaroop Mishra, Sid-
   dhartha Brahma, Sujoy Basu, Yi Luan, Denny Zhou,
   and Le Hou. 2023. Instruction-following evalu-
   ation for large language models. arXiv preprint
   arXiv:2311.07911.




                                                           12
Appendices
A        V ER I NSTRUCT
A.1       Dataset Construction Details
Following Qi et al. (2024), we collect original
instructions and responses from several publicly            Figure 8: left: Proportional distribution of constraint
available instruction-tuning datasets, including Al-        types in the dataset. right: Distribution of the number
paca GPT-4 (Peng et al., 2023), Orca Chat (Es,              of constraints per instruction.
2023), Evol Instruct (Xu et al., 2023), and Ope-
nAssistant (Köpf et al., 2024). We then apply a
back-translation-based method to extract both soft          are typically found within the first 200 steps. For
and hard constraints from the instruction-response          evaluation, we set the sampling temperature to 0
pairs. Table 6 presents the prompt to generate soft         to ensure reproducibility. For all evaluations us-
constraints used in V ER I NSTRUCT construction.            ing LLM-as-a-judge, we adopt gpt-4o-2024-11-20
The hard constraints, including Length, Keyword,            as the judge. Since the Conifer model (Sun et al.,
and selected aspects of Format, are automatically           2024) is not publicly open-sourced, we instead train
generated through Python-based processing. These            a model using its SFT and DPO data, and the re-
constraints are subsequently combined to form the           ported results of Conifer are evaluated based on our
final constraint-enhanced prompt.                           reproduced model. For the evaluation of reasoning
                                                            LLMs, we remove thinking tokens and evaluate
A.2       Dataset Statistics                                only the final responses. For evaluation of general
Figure 8 shows the distribution of 22, 000 in-              capabilities, we report the length-controlled win
stances in the V ER I NSTRUCT dataset. Following            rate for AlpacaEval 2.0 (Dubois et al., 2024). Both
IFBench (Peng et al., 2025), we categorize con-             training and evaluation are conducted on Nvidia
straints into five types: length, keyword, format,          H800 GPUs, with the entire training process taking
content, and style. The left chart presents the pro-        approximately 1, 900 GPU hours in total.
portional distribution of constraint types. Since
certain format constraints, such as those requiring         C    Training a Small Verifier
hierarchical output structures, are not easily veri-
fiable via Python, we define format, content, and           We provide a detailed description of the training
style as soft constraints, which together account           data construction process and training details. Fol-
for 77.7% of the total. Length and keyword are de-          lowing the construction of V ER I NSTRUCT, we first
fined as hard constraints, making up the remaining          generate an additional 20, 000 data instances. To
22.3%. The right chart categorizes the data by the          ensure diversity, we additionally mined complex
number of constraints after merging.                        instructions from WildChat (Zhao et al., 2024) and
                                                            Infinity Instruct (BAAI, 2024). Specifically, we
B       Experimental Details                                use Qwen2.5-72B-Instruct to extract constraints
                                                            from each instruction and classify them as hard
We train our model using the open-source VeRL               or soft. For hard constraints, we adopt Qwen2.5-
framework6 with the GRPO algorithm (Shao et al.,            72B-Instruct to generate corresponding verifica-
2024), setting the KL loss coefficient to 1 × 10−3 .        tion Python code scripts. The full prompt is pre-
The batch size is set to 32, the number of rollouts         sented in Table 7. For each instruction, we ran-
to 16, the maximum generation length of rollout             domly sample a response from 6 different models,
to 4, 096, and the learning rate to 1 × 10−6 . We           including Llama3.1-8B-Instruct (Grattafiori et al.,
save checkpoints every 20 steps during training.            2024), Llama-3.3-70B-Instruct (Grattafiori et al.,
Following TULU 3 (Lambert et al., 2024), we use             2024), Qwen2.5-7B-Instruct (Yang et al., 2024),
IFEval (Zhou et al., 2023) as the validation set to         Qwen2.5-72B-Instruct (Yang et al., 2024), QwQ-
select the best checkpoint. We train the models             32B (Qwen, 2025), DeepSeek-R1-Distilled-Qwen-
for one epoch on V ER I NSTRUCT with early stop-            32B (Guo et al., 2025). We then adopt QwQ-32B
ping if performance on IFEval does not improve              to generate a step-by-step verification indicating
for more than 5 checkpoints. The best checkpoints           whether the output satisfies the instruction for each
    6
        https://github.com/volcengine/verl                  instruction-response pair. As a result, we collect

                                                       13
about 130k instruction–response pairs with corre-
sponding step-by-step verification. For SFT train-
ing, we use the open-source alignment-handbook
framework (Tunstall et al.). Based on DeepSeek-
R1-Distill-Qwen-7B, we train the model on the
collected dataset for 2 epochs, with 2 × 10−5 learn-
ing rate, 64 batch size, 8, 192 max sequence length,
resulting in the verifier IF-Verifier-7B.




                                                       14
Prompt: Generating Constraints from Instruction and Output
As a linguist with expertise in contextual language nuances, please add constraints to enrich the #Given Instruction# based on the
#Given Output#. The goal is to enhance the specificity and detail of the instruction to ensure that the response is more aligned
with the output text.
To supplement the instruction using the output, please consider adding specific and detailed constraints across the following
dimensions:

    • Desired_Writing_Style: Specify the intended tone or narrative voice, such as humorous, formal, poetic, or conversational.

    • Semantic_Elements: Clarify the core meaning, focus, or conceptual emphasis that the response should reflect.

    • Morphological_Constraints: Indicate any forbidden words, expressions, or formatting (e.g., avoid passive voice or
      markdown).

    • Multi-lingual_Constraints: Specify the language(s) or code-switching rules to be used in the response.

    • Hierarchical_Instructions: Define a priority order among multiple tasks, outlining how they should be structured or
      emphasized.

    • Special_Output_Format: Specify required formats, such as Python code, JSON structure, tables, LaTeX, or HTML.

    • Paragraphs_Constraints: Indicate how many paragraphs are needed, and whether any separators (e.g., horizontal lines,
      “***”) should be used.

    • Specific_Sentence: Require inclusion of a specific sentence at the beginning or end of the response.

    • Key_Formatting: Specify formatting of key phrases—such as using bold, italics, or ALL CAPS—based on content in the
      #Given Output#.

    • Item_Listing_Details: Define how items should be listed, including use of symbols like bullets (•), numbers (1., 2., 3.), or
      dashes (-).

#Given Instruction#
{Instruction}
#Given Output#
{Response}
Please format your response directly in JSON, using "Constraint_Type" as the key and the specific constraint as its value.
Ensure that each constraint is a concise and complete sentence of 10–20 words, and use varied phrasing across types.
If a specific type of constraint cannot be derived from the #Given Output#, assign the value "NULL". For example:
"Constraint_Type": "NULL",
Do not include any headings or prefixes in your response.

Table 6: Prompt for generating format, content, and style constraint types based on the back-translation method.




                                                               15
 Prompt: Extracting Constraints from Instruction
 You are an expert in natural language processing and constraint checking. Your task is to analyze a given instruction and identify
 which constraints need to be checked.
 The ‘instruction’ contains a specific task query along with several explicitly stated constraints. Based on the instructions, you
 need to return a list of checker names that should be applied to the constraints.
 [Task Example 1]
 Instruction: Write a 300+ word summary of the Wikipedia page "https://en.wikipedia.org/wiki/Raymond_III_Count_of_Tripoli".
 Do not use any commas and highlight at least 3 sections that have titles in markdown format, for example *highlighted section
 part 1*, *highlighted section part 2*, *highlighted section part 3*.
 Response: NumberOfWordsChecker: 300+ word <sep> HighlightSectionChecker: highlight at least 3 sections that have titles in
 markdown format <sep> ForbiddenWordsChecker: Do not use any commas.
 #Task Instruction#
 {Instruction}
 ### Your task:
 - Generate the appropriate checker names with corresponding descriptions from the original instruction description. - Return the
 checker names with their descriptions separated by <sep>.
 - Focus only on the constraints explicitly mentioned in the instruction.
 - Ensure that each constraint is complete, such as specifying whether the 300-word limit applies to the entire text or a specific
 section. A defined scope is required.
 - Do **not** generate checkers for the task query itself or its quality.
 - If the instruction is in Chinese/English, please output the constraint in the same language.
 - Each checker should be responsible for checking only one constraint.
 - Do not output any constraints that are not included in the instruction.
 Prompt: Classifying Constraints
 Please classify whether the given checker can be judged using simple lexical rules.
 #Checker#
 {checker_name}
 Classification rules:
 - If the checker can be determined using simple lexical rules—such as word count, text length, number of paragraphs, number of
 sentences, or presence of specific keywords—output [[A]].
 - If the checker requires semantic understanding—such as style, tone, sentiment, language, context, genre, or structure—and thus
 necessitates an additional semantic analysis model (e.g., a large language model), output [[B]].
 - If the constraint is meaningless, non-informative, or irrelevant (e.g., "NA"), output [[C]].
 Prompt: Generating code
 You are tasked with implementing a ‘Python’ function ‘check_following’ that determines whether a given ‘response’ satisfies the
 constraint defined by a checker. The function should return ‘True’ if the constraint is satisfied, and ‘False’ otherwise.
 [Example Input 1]
 no more than 800 words
 [Example Output 1]
 def check_following(response): return len(response.split()) <= 800
 [Example Input 2]
 Include keywords ’cloud storage’, ’open-source’
 [Example Output 2]
 import re def check_following(response): return bool(re.search(r’cloud storage’, response, re.IGNORECASE) and
 re.search(r’open-source’, response, re.IGNORECASE))
 [Example Input 3]
 The word ’huge’ should appear 3 times
 [Example Output 3]
 import re def check_following(response): return len(re.findall(r’huge’, response, re.IGNORECASE)) == 3
 #Task Input Checker#
 {checker_name}
 [Requirements]
 - The function should be self-contained with necessary imports.
 - DO NOT use nltk.
 - Only return exactly ‘Python‘ code script, without any other info.

Table 7: Prompt for extracting constraints from instruction, classifying constraint types, and generating code for
hard constraints.




                                                                16
