                                                Efficient PRM Training Data Synthesis via Formal Verification

                                                 Ryo Kamoi1 Yusen Zhang2 Nan Zhang1 Sarkar Snigdha Sarathi Das1
                                                        Ranran Haoran Zhang1 Wenpeng Yin1 Rui Zhang1
                                                            1
                                                              Penn State University 2 Columbia University
                                                                   {ryokamoi, rmz5227}@psu.edu



                                                              Abstract                            to classify the correctness of individual reason-
                                                                                                  ing steps, using training datasets annotated with
                                            Process Reward Models (PRMs) have emerged             step-level error labels on LLM-generated reason-
arXiv:2505.15960v3 [cs.CL] 8 Apr 2026




                                            as a promising approach for improving LLM             ing traces (Wang et al., 2024; Zhang et al., 2025).
                                            reasoning capabilities by providing process su-          Despite their growing adoption, creating PRM
                                            pervision over reasoning traces. However, ex-
                                                                                                  training data remains costly and noisy. Early stud-
                                            isting approaches for constructing PRM train-
                                            ing data remain costly and noisy, as they typ-        ies (Uesato et al., 2022; Lightman et al., 2024) cre-
                                            ically rely on human annotation or sampling-          ate PRM training data via human annotation, which
                                            based labeling methods that require repeated          is particularly expensive for obtaining step-level
                                            LLM calls. In this work, we propose F OV ER,          error labels and suffers from low inter-annotator
                                            a framework that synthesizes PRM training             agreement (Zheng et al., 2025). Although Monte
                                            data from formal reasoning tasks by annotating        Carlo roll-outs (Wang et al., 2024; Luo et al.,
                                            step-level error labels using formal verification     2024), also known as Math-Shepherd, provide an
                                            tools such as Z3 and Isabelle. By leveraging
                                                                                                  annotation-free alternative for training data cre-
                                            formal verification, F OV ER enables efficient
                                            and accurate PRM data construction without            ation, it requires multiple LLM calls to label each
                                            requiring human annotation or additional LLM          step and generates noisy training labels.
                                            calls. Using F OV ER, we create PRM training             To address this gap, we propose F OV ER, a novel
                                            data from formal logic and theorem proving            framework for efficiently creating accurate PRM
                                            tasks. Experiments on 12 reasoning bench-             training data. As shown in Figure 1, F OV ER lever-
                                            marks show that fine-tuning on our training           ages formal verification tools to assign accurate
                                            data improves PRMs not only on math and
                                                                                                  step-level error labels to reasoning traces for formal
                                            logic reasoning tasks, which are informal vari-
                                            ants of the training tasks, but also on NLI and       reasoning tasks such as logic and theorem proving,
                                            BBH benchmarks, which differ substantially            without relying on human annotation or repeated
                                            from the tasks used to construct the training         LLM calls. Using F OV ER, we create PRM train-
                                            data. These results demonstrate the practical         ing data named F OV ER-40K by annotating step-
                                            effectiveness of F OV ER, showing that PRM            level error labels on LLM responses to formal logic
                                            training data created using formal verification       and theorem proving tasks using Z3 (de Moura
                                            improves PRMs on informal reasoning tasks             and Bjørner, 2008) and Isabelle (Nipkow et al.,
                                            written in natural language. The datasets, mod-
                                                                                                  2002). We then fine-tune Llama 3.1 8B (Llama
                                            els, and code are provided at https://github.
                                            com/psunlpgroup/FoVer.                                Team, 2024) and Qwen 2.5 7B (Qwen Team, 2024)
                                                                                                  on F OV ER-40K to use them as PRMs, which we
                                                                                                  refer to as F OV ER-PRMs.
                                        1   Introduction                                             Although F OV ER creates PRM training data
                                                                                                  from formal reasoning tasks, PRMs are typically
                                        Process Reward Models (PRMs) have recently                used to detect mistakes in informal reasoning tasks
                                        emerged as a promising approach for improving             written in natural language. Therefore, in our exper-
                                        the reasoning capabilities of LLMs. They provide          iments, we evaluate PRMs trained with F OV ER on
                                        fine-grained process supervision over intermediate        widely used informal reasoning benchmarks. First,
                                        reasoning steps during training and inference (Ue-        we evaluate F OV ER-PRMs on informal logic and
                                        sato et al., 2022; Lightman et al., 2024). In practice,   mathematical reasoning benchmarks. These bench-
                                        PRMs are usually created by fine-tuning LLMs              marks can be regarded as informal variants of the
Figure 1: Comparison of F OV ER with existing methods for PRM training data creation. F OV ER efficiently produces
accurate PRM training data for formal reasoning tasks by leveraging formal verification tools. In contrast, existing
methods are costly and produce noisy labels, as they rely on human annotation or repeated LLM calls.


     Baseline                                                 80.0
                                                       74.0          existing PRMs (e.g., Xiong et al., 2024; Zhang
     Ours
                                           56.8 54.8
                                                                     et al., 2025), whose training data is constructed
   53.0 54.7                        55.6
                 48.9 50.6   47.8                                    via human annotation or Monte Carlo roll-outs that
                                                                     require substantially higher cost than F OV ER.
     Math         Logical       NLI        MMLU-Pro      BBH
   Reasoning     Reasoning                  NoMath                      Together, as shown in Figure 2, our experi-
                (a) PRMs based on Llama 3.1 8B                       ments demonstrate the practical effectiveness of
                                                                     F OV ER in improving PRMs on widely used infor-
                                                       69.7 70.7     mal reasoning benchmarks. These results showcase
   64.8 66.2
                 54.2 56.6   58.4 58.4     58.0 60.4                 formal-to-informal transfer and cross-task gener-
                                                                     alization in PRM training using formally verified
     Math         Logical       NLI        MMLU-Pro      BBH         labels annotated on formal reasoning tasks.
   Reasoning     Reasoning                  NoMath
                                                                        Our main contributions are as follows:
                (b) PRMs based on Qwen 2.5 7B

Figure 2: Best-of-7 results across 5 categories of 12 rea-           • We propose F OV ER, a method that efficiently
soning benchmarks. PRMs trained with F OV ER out-                      constructs accurate PRM training data from for-
perform baseline PRMs on average, showing that our                     mal reasoning tasks using formal verification,
training data created from formal reasoning improves                   addressing the annotation cost and labeling inac-
PRMs on widely used reasoning benchmarks. Details                      curacy of existing approaches.
are in Section 4.
                                                                     • Our experiments show the practical effectiveness
                                                                       of F OV ER, with PRM training data from formal
training tasks, as F OV ER-40K consists of formal                      reasoning tasks improving performance on infor-
logic and theorem proving tasks. We conduct eval-                      mal reasoning tasks written in natural language,
uations on 6 widely used benchmarks, including                         demonstrating formal-to-informal transfer and
LogicNLI (Tian et al., 2021), AQuA-RAT (Ling                           cross-task generalization in PRM training.
et al., 2017), and AIME (Art of Problem Solv-
ing, 2025). Using Best-of-K (Cobbe et al., 2021;                     2   Background and Related Work
Li et al., 2023), a standard evaluation approach
for PRMs (Lightman et al., 2024; Wang et al.,                        PRMs for reasoning tasks are typically created
2024), we show that F OV ER-PRMs outperform                          by fine-tuning LLMs on the classification task
baseline PRMs based on LLMs without additional                       to detect errors in reasoning traces at the step
fine-tuning. Second, we evaluate F OV ER-PRMs                        level (Lightman et al., 2024; Wang et al., 2024).
on informal reasoning benchmarks involving tasks                     Training data for PRMs are often constructed by an-
that substantially differ from those used to con-                    notating step-level error labels on reasoning traces
struct F OV ER-40K. We use six benchmarks, includ-                   generated by LLMs. Given a problem p ∈ P from a
ing HANS (McCoy et al., 2019), MMLU (Paech,                          reasoning task, an LLM generates a step-by-step so-
2024), and BBH (Suzgun et al., 2023). The re-                        lution consisting of k steps: s = [s1 , s2 , . . . , sk ] ∼
sults show that F OV ER-PRMs outperform baseline                     LLM(p). We then assign step-level error labels
PRMs and achieve performance competitive with                        [ys1 , ys2 , . . . , ysk ] ∈ {0, 1}k , which serves as the
supervision signal for PRM training. Here, we                        3     F OV ER
consider binary labels of correct and incorrect.
                                                                     We propose F OV ER, a method for creating PRM
   Despite extensive research on PRM training data
                                                                     training data by annotating step-level error labels
construction, obtaining reliable step-level labels re-
                                                                     on formal reasoning tasks using formal verifica-
mains challenging. Existing approaches are costly
                                                                     tion tools. Using F OV ER, we create PRM training
and noisy, as they often rely on human annotation
                                                                     data named F OV ER-40K from first-order logical
or computationally expensive automatic methods.
                                                                     reasoning tasks using Z3 and from formal theorem
Human annotation. Human annotation (Uesato                           proving tasks using Isabelle.
et al., 2022; Lightman et al., 2024) is the primary
approach used in early studies. However, for step-                   3.1    Step-level Formal Verification
level reasoning tasks, it is particularly costly, and
                                                                     Background: Formal verification. Formal rea-
achieving high inter-annotator agreement is diffi-
                                                                     soning tasks (or symbolic reasoning tasks), includ-
cult. For example, Zheng et al. (2025) discard 30%
                                                                     ing formal logic and formal theorem proving, are
of the annotated solutions due to low agreement.
                                                                     problems defined and solved using formal syn-
Monte Carlo roll-outs.                    Monte Carlo roll-          tax and rules (Nawaz et al., 2019; Clark et al.,
outs (Wang et al., 2024; Luo et al., 2024), also                     2021). Formal verification tools, such as automated
known as Math-Shepherd, is a widely used method                      solvers and theorem provers, are used to formally
for automating PRM training data creation. MC                        verify solutions to formal reasoning tasks (Zhou
roll-outs generate multiple continuations from a tar-                et al., 2024; Yang et al., 2025). The tools differ
get reasoning step and use the frequency of reach-                   in the methods they use and in the groups of tasks
ing the correct final answer as an estimate of the                   to which they apply. For example, Z3 (de Moura
correctness of that step.                                            and Bjørner, 2008) is an SMT solver, which ex-
   Specifically, to label a step sr in a solution s =                tends SAT solvers with background theories, appli-
[s1 , . . . , sr , . . . , sk ], the method samples multiple         cable to decidable subsets of first-order logic. Is-
continuations from an LLM conditioned on the                         abelle/HOL (Nipkow et al., 2002) is an interactive
problem p and the prefix s1:r :                                      theorem prover applicable to higher-order logic.
                                                                        To illustrate the process of formal verification,
                     (1)           (1)
    [s1 , . . . , sr , cr+1 , . . . , cK1 ] ∼ LLM( · | p, s1:r )     we present a simple example of a first-order logic
                     (2)           (2)
    [s1 , . . . , sr , cr+1 , . . . , cK2 ] ∼ LLM( · | p, s1:r )     reasoning (logical entailment) task that can be veri-
                                                                     fied using a SAT solver:
                     (n)          (n)
. . . [s1 , . . . , sr , cr+1 , . . . , cKn ] ∼ LLM( · | p, s1:r )
                                                                      Context: A → B, B → C, A           Hypothesis: C
Let ai denote the final answer produced by the
i-th continuation and let a∗ be the ground-truth                     Assume that the predicted answer is “entailment,”
final answer.  The quality of step sr is estimated as                meaning the hypothesis is logically entailed by the
        1 Pn
qsr = n i=1 I(ai = a∗ ), which can be used as a                      context. We want to verify whether this prediction
soft label or binarized to obtain a hard label.                      is correct, which is equivalent to showing that the
   Although widely adopted, MC roll-outs suffer                      following implication is valid:
from high computational cost due to the need to                                                          
generate multiple continuations per step, and the                            (A → B) ∧ (B → C) ∧ A → C.
estimated labels can be noisy and inaccurate.
                                                                     We can check this with a SAT solver using resolu-
Other approaches. Perturbations (Yang et al.,                        tion: combine the premises with the negation of the
2022; Ma et al., 2023; Paul et al., 2024) is another                 hypothesis and test its satisfiability in Conjunctive
automated approach that introduces mistakes into                     Normal Form (CNF):
generated solutions by applying heuristic methods
or using LLMs. However, it results in training data                          (¬A ∨ B) ∧ (¬B ∨ C) ∧ A ∧ ¬C.
with artificial and unnatural errors. Some work cre-
ates PRM training data by annotating error labels                    If the solver reports this formula unsatisfiable, then
using stronger LLMs (Zhang et al., 2025; Zeng                        the entailment is confirmed. SAT solvers such as
et al., 2025), but this approach results in merely                   Z3 automate this process and thus can formally
distilling the capabilities of stronger LLMs.                        verify the correctness of the prediction.
Step-level formal verification. In this paper, we                               Training Data Creation of FoVer
propose using formal verification tools to verify so-                        Formal Reasoning Task
lutions at the step level. As illustrated above, these                        $hypothesis$: ({D}{b} & ¬{C}{b})
                                                                              $context$:
tools have primarily been applied to solution-level                           fact1: {D}{b} -> {C}{b}
                                                                              fact2: ({D}{b} & ¬{C}{a}) [...]
verification. Our key idea is that, for certain tasks,                                                             (2) Automatic Error
                                                                                                                        Annotation
they can also be employed to verify the correct-                     (1) Formal Solution
                                                                                                                          Formal
                                                                          Generation            LLM
                                                                                                                     Verification Tool
ness of individual reasoning steps. For instance,
                                                                             Formal Solution
for the above problem, suppose an LLM produces                                         fact2 -> int1: {D}{b}               ✅
the following step-by-step solution:                                                int1 & fact1 -> int2: {C}{b}           ✅
                                                                                     int2 & int1 -> hypothesis             ❌
                                                                                  The final answer is PROVED              ❌
         Step 1:      (A → B) ∧ A          → B.
                                                                                                                       Fine-tuning
         Step 2:      B ∧ (A → B)) → C.                                                       Fine-tuning PRM
                                                                                                                    LLM-based PRM

  It can be verified at the step level: we adopt a
simple strategy that evaluates the logical correct-            Figure 3: Top: F OV ER creates PRM training data from
ness of each step independently. Once we check                 formal reasoning tasks using formal verification tools.
                                                               Bottom: Using the training data, we fine-tune PRMs on
that each step only uses the provided context and
                                                               the task of step-level verification.
preceding results, we can verify the logical correct-
ness by testing the satisfiability of:
                                                               {0, 1}K , without the need for human annotation:
           Step 1: (¬A ∨ B) ∧ A ∧ ¬B.
                                                                 [ys1 , ys2 , . . . , ysk ]
           Step 2: B ∧ (¬A ∨ B) ∧ ¬C.
                                                                     = FormalVerification(p, [s1 , s2 , . . . , sk ]),
The SAT solver will show that the first formula is
                                                               where FormalVerification(, ), a formal verifica-
unsatisfiable, indicating Step 1 is correct, and the
                                                               tion tool, accurately outputs label ysk = 1 if the
second is satisfiable, indicating Step 2 is incorrect.
                                                               solution step sk is correct, ysk = 0 otherwise.
This procedure provides step-level verification for
                                                                  Using training data created with F OV ER, we fine-
the solution to the logical entailment task.
                                                               tune an LLM on the step-level binary classification
   In this work, we implement step-level verifica-
                                                               task to serve as a PRM (P × S → [0, 1]K ), which
tion for formal logic (logical entailment) using Z3
                                                               is the standard approach for creating classification-
and theorem-proving tasks using Isabelle to create
                                                               based PRMs (Zhang et al., 2025). The cross-
PRM training data.
                                                               entropy training objective for PRMs is given by:
3.2   F OV ER Framework                                                K
                                                                       X
F OV ER synthesizes PRM training data in two                    L=           (ysi log rsi + (1 − ysi ) log(1 − rsi )) ,
                                                                       i=1
stages, as shown in Figure 3. In the first stage,
given a problem p ∈ P from a formal reasoning                  where rsi is the step-level score for step si pre-
task that is compatible with formal verification, an           dicted by the PRM. In our implementation, we
LLM generates a step-by-step formal solution con-              fine-tune LLM in a text generation task to output
sisting of k steps: s = [s1 , s2 , . . . , sk ] ∼ LLM(p).      the token “correct” or “incorrect” for each step.
The solution s may contain logical errors but is
required to follow the format compatible with a                3.3    F OV ER-40K Dataset
formal verification tool. In this work, we provide             Using F OV ER, we synthesize PRM training data
a few-shot demonstration to guide LLMs. Alter-                 that includes step-level binary error labels on the
natively, it is also possible to use models trained            formal logic and formal theorem proving tasks,
for specific formal verification tools (Yang et al.,           which we refer to as F OV ER-40K. As shown in Ta-
2023; Xin et al., 2024). LLMs may generate solu-               ble 1, F OV ER-40K includes 40K steps in reasoning
tions in an invalid format, so we generate multiple            traces generated by Llama 3.1 8B (Llama Team,
solutions until we obtain one with a valid format.             2024) and Qwen 2.5 7B (Qwen Team, 2024) with
   In the second stage, the formal verification tool           error labels annotated by formal verification tools,
assigns step-level error labels [ys1 , ys2 , . . . , ysk ] ∈   Z3 and Isabelle. Figure 4 shows example data.
                                Formal Logic                                                                 Formal Theorem Proving
Formal Statement                                                                    Formal Statement
                       $hypothesis$: ({D}{b} & ¬{C}{b})                                                 assumes "(total_pencils::nat) = 1500"
                       $context$:                                                                         and "(cost_per_pencil::real) = 0.10"
                       fact1: {D}{b} -> {C}{b}                                                            and "(sell_price_per_pencil::real) = 0.25"
                       fact2: ({D}{b} & ¬{C}{a}) [...]                                                    and "(profit::real) = 100.00 [...]
                                                                                                        shows "pencils_to_sell = 1000"
Formal Solution                                                                     Formal Solution
                                fact2 -> int1: {D}{b}                          ✅                   have "total_pencils * cost_per_pencil = 150" by simp                               ✅
                             int1 & fact1 -> int2: {C}{b}                      ✅          then have "profit + (total_pencils * cost_per_pencil) = 250" by simp                        ✅
                             int2 & int1 -> hypothesis                         ❌                then have "(profit + (total_pencils * cost_per_pencil)) / [...]                       ✅
                          The final answer is PROVED                           ❌    then have "(profit + (total_pencils * cost_per_pencil)) / sell_price_per_pencil = 1000" by simp   ✅
                                                                                     have "total_pencils * cost_per_pencil / sell_price_per_pencil = 600" by simp                     ❌
                                                                                                        then have "pencils_to_sell = 1000" by simp                                    ❌
                                                            Figure 4: Examples from F OV ER-40K.



  Tasks
                  Source           Formal
                                                  Step-by-step
                                                                   Error Labels     4      Experimental Results
                  Datasets       Verification
                                                   Solutions   # of Steps % Error
                                    Tools
 Formal                                          Llama 3.1 8B   10,000     50%
                                                                                    This section evaluates our F OV ER-PRMs fine-
                  FLDx2               Z3
  Logic                                          Qwen 2.5 7B    10,000     50%      tuned on F OV ER-40K. While F OV ER-40K in-
 Formal  GSM8K,                                                                     cludes step-level error labels on formal reasoning
Theorem MetaMathQA,                Isabelle      Qwen 2.5 7B    20,000     50%
Proving  Big-Math                                                                   tasks, PRMs are often used to detect mistakes in in-
                                                                                    formal reasoning tasks written in natural language.
Table 1: Statistics of the F OV ER-40K training dataset.                            Therefore, we evaluate F OV ER-PRMs on widely
                                                                                    used informal reasoning benchmarks to answer the
   The F OV ER-40K dataset is created from                                          following research questions.
FLDx2 (Morishita et al., 2023, 2024) and GSM8K-
                                                                                    • RQ1: Does training on F OV ER-40K improve
level mathematical reasoning tasks. We select these
                                                                                      PRMs on informal logic and math reasoning
tasks based on diversity, simplicity, and general-
                                                                                      tasks, which are informal variants of the train-
ization considerations. For the formal logic task,
                                                                                      ing tasks? (formal-to-informal transfer, §4.2)
we selected FLDx2 because it offers the greatest
diversity among those expressible via deduction                                     • RQ2: Does training on F OV ER-40K improve
rules (Morishita et al., 2024). For mathematical                                      PRMs on informal reasoning tasks that largely
reasoning, we selected GSM8K-level datasets to                                        differ from the training tasks, such as NLI and
simplify the verification pipeline.                                                   BBH? (cross-task generalization, §4.3)
Formal logic. We use the logical entailment task
in FLDx2 (Morishita et al., 2023, 2024), a dataset                                  4.1        Experimental Setting
for multi-step first-order logic deduction, in which                                Evaluation methodology. We evaluate PRMs us-
the goal is to determine whether a hypothesis is                                    ing the Best-of-K performance on reasoning bench-
entailed by a given set of premises. We generate                                    marks and step-level verification performance, both
step-by-step formal solutions with the LLMs and                                     of which are widely used approaches to assess
annotate step-level error labels using Z3.                                          PRMs (Li et al., 2023; Zhang et al., 2024b). First,
Formal theorem proving. We use the task of                                          Best-of-K (Cobbe et al., 2021; Li et al., 2023) uses
formal theorem proving for verifying solutions to                                   PRMs to select the best solution from multiple
math word problems (Wu et al., 2022; Zhou et al.,                                   candidates generated by LLMs for the same in-
2024). The conditions of a math word problem are                                    put. The performance of the selected solutions
presented as premises, a candidate final answer is                                  indirectly indicates the verification performance
formulated as a hypothesis, and the task is to gen-                                 of the PRMs. We use few-shot demonstrations
erate a proof for this statement. We generate for-                                  to generate K = 7 step-by-step solutions from
mal proofs with the LLMs in the task of verifying                                   Llama 3.1 8B and Qwen 2.5 7B with a tempera-
the solutions to GSM8K-level problems, including                                    ture of 0.5. Following prior work (Lightman et al.,
GSM8K (Cobbe et al., 2021), GSM8K-based cases                                       2024; Wang et al., 2024), we then use PRMs to
in MetaMathQA (Yu et al., 2024), and math word                                      score each step, and the solution score is the min-
problems in Big-Math (Albalak et al., 2025). We                                     imum score across all steps. The solution with
then annotate step-level error labels using Isabelle.                               the highest solution score is selected. For large
                                                     Logic                                       Math
                             PRMs                                  Average                                                     Average
                                             FOLIO      LogicNLI               GSM8K      MATH           AQuA       AIME
       PRMs based on   Llama 3.1 8B          58.6        39.2       48.9        87.6      54.4           66.1       4.0         53.0
        Llama 3.1 8B   F OV ER-Llama3.1-8B   60.1        41.2       50.6        88.4      53.6           71.7∗      5.2         54.7∗
       PRMs based on   Qwen 2.5 7B           64.0        44.4       54.2        90.0      76.4           80.3       12.4        64.8
        Qwen 2.5 7B    F OV ER-Qwen2.5-7B    63.5        49.6       56.6        92.4      79.2           81.1       12.0        66.2∗


Table 2: Best-of-K (K=7) performance on informal logic and math benchmarks. The first rows represent the
baseline PRMs based on LLMs without additional training. F OV ER-PRMs exhibit significantly better performance,
showing that F OV ER-40K improves verification on informal logic and math reasoning. ∗ : Statistically significant
improvement over the baseline PRMs in the first row (p < 0.05, paired bootstrap).


datasets, we use 250 randomly sampled examples                               PRMs              GSM8K MATH Olympiad Omni                  Ave.

from each dataset. Second, we evaluate step-level                    Llama 3.1 8B                70.0       67.4       68.3      63.9 67.4
                                                                     F OV ER-Llama3.1-8B-PRM     81.2∗      76.4∗      75.5∗     76.3∗ 77.3∗
verification performance on math reasoning tasks
                                                                     Qwen 2.5 7B                 75.5       78.2       76.2      73.6 75.9
in ProcessBench (Zheng et al., 2025), which in-                      F OV ER-Qwen2.5-7B-PRM      86.6∗      88.0∗      84.0∗     84.5∗ 85.8∗
cludes human annotated binary step-level error la-
bels. ProcessBench includes labels only for the                     Table 3: Step-level binary classification performance of
earliest error in each reasoning traces, so we use                  PRMs on math reasoning tasks in ProcessBench (AU-
                                                                    ROC). F OV ER-PRMs exhibit significantly better perfor-
the steps up to the first error in each solution.
                                                                    mance than the baselines, showing that F OV ER-40K im-
Evaluated PRMs. We evaluate classification-                         proves verification on informal math reasoning. ∗ : Statis-
based PRMs that use Llama 3.1 8B (Llama Team,                       tically significant improvement over the baseline PRMs
2024) and Qwen 2.5 7B (Qwen Team, 2024) as the                      in the first rows (p < 0.05, paired bootstrap).
backbone. We choose these LLMs because they
are widely used as backbones for PRMs, which
allows for direct comparison with PRMs intro-
duced in prior work. Our PRMs, referred to as                       theorem proving tasks included in F OV ER-40K.
F OV ER-PRMs, are obtained by fine-tuning these
LLMs on F OV ER-40K. Baseline PRMs: We com-                         Results of Best-of-K. We evaluate the Best-of-
pare with baselines that use the backbone LLMs                      K performance of PRMs on two logical rea-
as PRMs without additional fine-tuning. Existing                    soning benchmarks: FOLIO (Han et al., 2024),
PRMs: In Section 4.3, we also evaluate five PRMs                    LogicNLI (Tian et al., 2021), and four math
introduced in prior work (Table 4). Among PRMs                      benchmarks: GSM8K (Cobbe et al., 2021),
based on Llama 3.1 8B, we evaluate RLHFlow-                         MATH (Hendrycks et al., 2021), AQuA-RAT (Ling
Llama3.1-8B trained on the DeepSeek or Mis-                         et al., 2017), AIME (2016-2024) (Art of Problem
tral data (Xiong et al., 2024), which include er-                   Solving, 2025). Table 2 reports the Best-of-K per-
ror labels on solutions generated by stronger mod-                  formance, showing that F OV ER-PRMs outperform
els on GSM8K and MATH acquired via Monte                            the baseline PRMs on average both on the informal
Carlo roll-outs (Wang et al., 2024). Among PRMs                     logic and math tasks.
based on Qwen 2.5 7B, we evaluate Qwen2.5-
Math-7B-PRM800K (Zheng et al., 2025), which                         Results on ProcessBench. We also evaluate the
is trained on human-annotated labels on MATH,                       PRMs on the step-level binary classification (error
and Qwen2.5-Math-PRM-7B (Zhang et al., 2025),                       detection) task on mathematical reasoning tasks in
which is trained on labels synthesized using Monte                  ProcessBench (Zheng et al., 2025). ProcessBench
Carlo roll-outs and verification by a stronger model.               includes human-annotated step-level error labels
We also evaluate Qwen2.5-7B-Skywork-PRM (He                         (correct vs. incorrect) for reasoning traces on four
et al., 2024), which is trained on math and coding.                 math benchmarks: GSM8K, MATH, Olympiad-
                                                                    Bench, and Omni-Math. Table 3 shows the step-
                                                                    level verification performance of PRMs, measured
4.2   Results on Logic and Math
                                                                    in AUROC. The results show that fine-tuning on
First, we evaluate F OV ER-PRMs on widely-used                      F OV ER-40K significantly improves PRM perfor-
informal logic and math reasoning benchmarks,                       mance at detecting step-level mistakes from the
which are informal variants of formal logic and                     baseline PRMs in informal math reasoning tasks.
                                                                    Step-Level Error         # LLM Calls per       Does Not Require      No Human       Accurate
            PRM                    Tasks in Training Data
                                                                       Annotation          Solution for Labeling    Stronger LLMs        Annotation    Annotation
 RLHFlow-Llama3.1-8B (M, D)           Math Reasoning                  MC Roll-out              8 × # Steps                  ✓                ✓             ✗
 Qwen2.5-Math-7B-PRM800K             Math Reasoning                Human Annotation                  1                      ✓                ✗             ✗
  Qwen2.5-7B-Skywork-PRM          Math Reasoning, Coding             MC Roll-out              (not reported)                ✓                ✓             ✗
   Qwen2.5-Math-PRM-7B               Math Reasoning                MC Roll-out, LLMs           8 × # Steps                  ✗                ✓             ✗
                                      Formal Logic,
      F OV ER-PRM (Ours)                                           Formal Verification              1                       ✓                ✓             ✓
                                  Formal Theorem Proving


                       Table 4: Training data creation methods for PRMs evaluated in Section 4.3.

                                                                   NLI                             MMLU                         BBH
                                  PRMs                                           Average                                                                Average
                                                            ANLI      HANS                      Pro-NoMath         Temporal     Tracking     Sorting

                   Llama 3.1 8B                             26.4       69.2       47.8              56.8             90.4        90.0         41.6       74.0

  PRMs based on    RLHFlow-Llama3.1-8B-M                    26.8       77.6∗      52.2∗             56.8             92.0        90.8         39.2       74.0
   Llama 3.1 8B    RLHFlow-Llama3.1-8B-D                    27.2       74.4∗      50.8∗             57.6             98.8∗       92.8         40.0       77.2∗
                   F OV ER-Llama3.1-8B-PRM (ours)           30.0       81.2∗      55.6∗             54.8             97.2∗       96.0∗        46.8∗      80.0∗

                   Qwen 2.5 7B                              32.4       84.4       58.4              58.0             91.2        89.2         28.8       69.7
                   Qwen2.5-Math-7B-PRM800K                  29.6       83.2       56.4              62.0∗            82.0        90.8         28.4       67.1
  PRMs based on
                   Qwen2.5-7B-Skywork-PRM                   29.2       81.2       55.2              58.8             84.0        91.2         31.6       68.9
   Qwen 2.5 7B
                   Qwen2.5-Math-PRM-7B                      27.6       86.0       56.8              60.4             86.4        92.8∗        28.8       69.3
                   F OV ER-Qwen2.5-7B-PRM (ours)            30.8       86.0       58.4              60.4             92.4        90.0         29.6       70.7


Table 5: Best-of-K (K=7) performance on tasks that differ from tasks in training data of F OV ER-PRMs and existing
PRMs (i.e., unseen tasks). The first rows represent the baseline PRMs based on LLMs without additional training.
The next set of rows contains existing PRMs introduced in prior work. The last rows show our F OV ER-PRMs.
∗
  : Statistically significant improvement over the baseline PRMs in the first row (p < 0.05, paired bootstrap).


  Answer to RQ1: Formal-to-Informal Transfer                                           Table 5 shows the Best-of-K performance of
 PRMs trained on F OV ER-40K outperform base-                                       PRMs on the unseen tasks. First, compared to
 line PRMs on average on informal math and                                          the baseline PRMs, F OV ER-PRMs improve perfor-
 logic benchmarks. These results demonstrate                                        mance on average on almost all tasks. Furthermore,
 that PRM training on formally verified error la-                                   F OV ER-PRMs are competitive with existing PRMs,
 bels on formal reasoning tasks exhibits formal-                                    whose training datasets are created at substantially
 to-informal transfer and improves performance                                      higher cost. In particular, F OV ER-Llama3.1-8B-
 on informal variants of the formal training tasks.                                 PRM achieves the best performance on the majority
                                                                                    of the benchmarks, compared with existing PRMs
                                                                                    based on the same LLM.
4.3    Results on Unseen Tasks
                                                                                           Answer to RQ2: Cross-Task Generalization
Second, we evaluate F OV ER-PRMs on reasoning
tasks that are substantially different from the for-                                     PRMs trained on formal reasoning tasks in
mal logic and theorem proving tasks in F OV ER-                                          F OV ER-40K exhibit cross-task generalization,
40K, which we refer to as unseen tasks. We con-                                          improving performance on informal reasoning
duct evaluations on 6 reasoning benchmarks span-                                         tasks such as NLI and BBH that are substantially
ning three tasks: NLI, including ANLI (Nie et al.,                                       different from the formal logic and theorem prov-
2020) and HANS (McCoy et al., 2019); MMLU-                                               ing tasks in F OV ER-40K.
Pro-NoMath (Paech, 2024); and BIG-Bench Hard,
including temporal sequences, tracking shuffled                                     5      Analysis
objects (three objects), and word sorting (Suzgun
et al., 2023). Here, in addition to F OV ER-PRMs,                                   Ablation on training tasks. F OV ER-40K con-
we evaluate existing PRMs introduced in prior                                       sists of formal logic and theorem proving tasks.
work (Table 4). Since these PRMs are trained on                                     To assess the contribution of each task, we train
mathematical reasoning or coding tasks, the reason-                                 PRMs on each task separately and evaluate their
ing benchmarks evaluated in this section are also                                   performance. Table 6 reports the Best-of-K per-
unseen for the existing PRMs.                                                       formance of PRMs based on Llama 3.1 8B trained
Formal Formal
               GSM8K LogicNLI HANS Temporal Tracking Ave.                                               100




                                                                               Best-of-K Accuracy (%)
 Logic Theorem
  –          –     87.6    39.2       69.2    90.4       90.0       75.3
                                                                                                        80
                                  ∗
  ✓          –     86.8    46.0       75.2∗   96.8∗      92.4       79.4∗                                                     GSM8K              Temporal
                                          ∗       ∗
  –          ✓     90.4    44.0       76.8    96.0       94.8∗      80.4∗
                                                                                                        60                    LogicNLI           Tracking
  ✓          ✓     88.4    41.2          ∗
                                      81.2    97.2   ∗
                                                         96.0   ∗
                                                                    80.8   ∗
                                                                                                                              HANS

Table 6: Ablation on training tasks for Best-of-K (K=7)                                                 40
                                                                                                              10K             20K                               40K
performance of PRMs based on Llama 3.1 8B trained on                                                                            Training Data Size
different subsets of F OV ER-40K. The top row represents
the baseline PRM, and the last row represents the PRM                          Figure 5: Ablation on training data size for PRMs based
trained on the original F OV ER-40K.                                           on Llama 3.1 8B trained on randomly sampled subsets
                                                                               of F OV ER-40K with 10K and 20K instances.
      PRMs         GSM8K LogicNLI HANS Temporal Tracking Ave.
    Qwen 3 4B      93.2    66.4       89.6    87.6       95.6       86.5
F OV ER-Qwen3-4B   91.6    70.0       89.6    89.2       95.6       87.2                          Problem: Today, Sarah went to the art show. Between what
                                                                                                  times could they have gone? [...] Lisa saw Sarah working at
                                                                                                  the office from 11am to 2pm. [...] Options: (A) 11am to 2pm
Table 7: Best-of-K (K=7) performance of PRMs based                                                (B) 7pm to 9pm [...]
                                                                                                  Ground truth answer: (B) 7pm to 9pm
on Qwen 3 4B. Fine-tuning on F OV ER-40K (second
row) yields improved or comparable performance on all
but one benchmark.                                                                    Step                      Solution from Llama 3.1 8B           Baseline F OV ER
                                                                                                          Lisa saw Sarah working at the office
                                                                                                2         from 11am to 2pm, so Sarah could have       0.98     0.99
                                                                                                          gone to the art show from 2pm.
on different subsets of F OV ER-40K. The results                                                          From the options, we can see that 11am
show that each task is independently effective and                                              7         to 2pm is the only option that fits this    0.94     0.06
                                                                                                          time frame.
leads to significant improvements over the base-
line PRMs on average. Looking more closely, we                                 (a) Positive example of F OV ER-PRM on the temporal se-
                                                                               quence task. F OV ER-Llama3.1-8B-PRM detects an error in
observe that combining the two tasks during train-                             Step 7, whereas the baseline erroneously assigns a high score.
ing improves performance on unseen tasks (HANS,
Temporal, and Tracking), while PRMs trained on
                                                                                                  Problem: For what integer x is 53 < x7 < 79 ?
individual tasks achieve better performance on their
corresponding logic and math benchmarks. In
                                                                                      Step                      Solution from Llama 3.1 8B           Baseline F OV ER
light of this observation, when creating PRMs in-
                                                                                                          We can rewrite the inequality as
tended for use in a specific domain with available                                              0         3                                           1.00     1.00
                                                                                                          5
                                                                                                            < x7 < 97 .
in-distribution training data, it may be preferable                                                       Multiplying the inequality by 315 to
not to include additional domains in the training                                               1         eliminate the fractions, we obtain          1.00     0.98
                                                                                                          189 < 45x < 245.
data. We will add this discussion to the updated
                                                                                                          Dividing the inequality by 45, we get
version of the paper.                                                                           2         189                                         1.00     0.68
                                                                                                           45
                                                                                                              < x < 245 45
                                                                                                                           ⇒ 4.2 < x < 5.44.
Robustness to stronger backbone LLM. To                                        (b) Negative example for F OV ER-PRM on MATH. F OV ER-
evaluate the robustness of PRM training with                                   Llama3.1-8B-PRM is too strict in Step 2 and considers round-
F OV ER, we additionally evaluate PRMs based on                                ing 5.44444 . . . to 5.44 as a mistake.
Qwen 3 4B (Qwen Team, 2025), which is newer                                                             Table 8: Example outputs from F OV ER-PRMs.
and stronger than Llama 3.1 8B and Qwen 2.5 7B.
Table 7 reports the Best-of-K performance of PRMs
based on Qwen 3 4B with and without fine-tuning                                an ablation study on training data size for the Best-
on F OV ER-40K. The results show that fine-tuning                              of-K performance of PRMs based on Llama 3.1 8B
on F OV ER-40K yields improved or comparable                                   trained on randomly sampled subsets of F OV ER-
performance across nearly all benchmarks, aside                                40K with 10K and 20K instances. The results show
from GSM8K. These findings indicate that F OV ER-                              that PRMs trained on a subset with 10K instances
40K, which is constructed from responses gener-                                already achieve performance comparable to those
ated by weaker models, improves PRMs built on                                  trained on the full dataset, showing the data effi-
stronger LLM backbones, demonstrating the ro-                                  ciency in the F OV ER training.
bustness of training with F OV ER with respect to                              Case study. Table 8 shows example outputs from
backbone LLM choice.                                                           F OV ER-PRM and baseline PRMs. Table 8a shows
Ablation on training data size. Figure 5 presents                              a positive example on a solution to the temporal
sequence task in BBH. The task is to find a free         ification tools. In contrast to existing approaches
time slot that does not overlap with any events in       that are costly and noisy, F OV ER efficiently pro-
a given list of past time intervals, which is distinct   duces accurate PRM training data without relying
from formal reasoning tasks in F OV ER-40K. This         on human annotation or repeated LLM calls. Exper-
example shows that F OV ER-Llama3.1-8B-PRM               imental results show that PRMs trained on data gen-
properly understands the task and solutions de-          erated by F OV ER achieve improved performance
scribed in natural language and correctly detects        across reasoning benchmarks in math, logic, NLI,
a logical error in Step 7, showing the formal-to-        and BBH, demonstrating informal-to-formal trans-
informal transfer and cross-task generalization in       fer and cross-task generalization in PRM training.
PRM training with F OV ER. Table 8b shows a neg-         These findings show that formal verification pro-
ative example illustrating a potential side effect       vides a practical approach to PRM training data
of F OV ER. In this example, F OV ER-Llama3.1-           construction, improving PRMs on widely used in-
8B-PRM assigns a low score when a solution step          formal reasoning tasks written in natural language.
rounds 245
         45 = 5.44444 . . . to 5.44 for conciseness.
While this can be considered a mistake under strict      Limitations
evaluation, it is often acceptable when applied to       This work focuses on classification-based PRMs
intermediate values where the exact precision is         that generate a single score to each step. Although
not required for the correctness of the final result.    recent studies introduce PRMs that provide step-
Training on formally annotated labels in F OV ER         level reasoning for error classification (Khalifa
may cause PRMs to become overly strict, assigning        et al., 2025; Feng et al., 2025; Kim et al., 2025),
lower scores to intermediate steps that are accept-      we leave the study of this type of PRM to future
able but not strictly precise.                           work, as they are not directly comparable with
                                                         classification-based PRMs. PRMs with step-level
6   Discussion                                           reasoning incur substantially higher computational
Our experiments show that PRMs trained on sym-           costs for verification, often multiple times greater
bolic solutions for formal tasks improve perfor-         than those required to generate the target reasoning
mance on widely used informal reasoning tasks,           traces, which limits their practical usefulness.
demonstrating effective formal-to-informal trans-
                                                         Acknowledgments
fer in PRM training. Compared to prior work that
directly fine-tunes LLMs on symbolic reasoning           This work was supported by NSF IIS-2338418 and
traces, our results indicate that PRM training yields    DMS-2533995. We thank Jin Peng Zhou for pro-
stronger transferability. For instance, Morishita        viding guidance on the use of his code (Zhou et al.,
et al. (2024) train LLMs on reasoning traces from        2024). We also thank Terufumi Morishita for the
a formal logic dataset to improve general reason-        valuable discussions and for his assistance with
ing, but report limited transfer in a naive setup. To    the FLDx2 dataset (Morishita et al., 2024), and we
address this issue, they convert symbolic solutions      appreciate NLP Colloquium JP for providing the
into natural language and apply RecAdam (Chen            opportunity to connect with him. We thank Hieu
et al., 2020). In contrast, our results show that PRM    N. Nguyen for his suggestions on improving the
training exhibits formal-to-informal transfer with-      presentation of this work.
out these modifications. We attribute this advantage
to the consistency of the output space in PRM train-
ing. Regardless of the input format, PRMs generate       References
a binary label indicating whether each step is cor-      Alon Albalak, Duy Phung, Nathan Lile, Rafael Rafailov,
rect or incorrect, which reduces shifts in model           Kanishk Gandhi, Louis Castricato, Anikait Singh,
                                                           Chase Blagden, Violet Xiang, Dakota Mahan, and
behavior that can arise when LLMs are directly
                                                           Nick Haber. 2025. Big-math: A large-scale, high-
fine-tuned to generate symbolic reasoning traces.          quality math dataset for reinforcement learning in
                                                           language models. arXiv preprint arXiv:2502.17387.
7   Conclusion
                                                         Art of Problem Solving. 2025. Aime problems and
We introduce F OV ER, a method for constructing            solutions.
PRM training data from formal reasoning tasks by         Sanyuan Chen, Yutai Hou, Yiming Cui, Wanxiang Che,
annotating step-level error labels using formal ver-       Ting Liu, and Xiangzhan Yu. 2020. Recall and learn:
  Fine-tuning deep pretrained language models with          Lawrence, Julia Hockenmaier, Graham Neubig, and
  less forgetting. In Proceedings of the 2020 Confer-       Sean Welleck. 2025. Scaling evaluation-time com-
  ence on Empirical Methods in Natural Language             pute with reasoning models as process evaluators.
  Processing (EMNLP), pages 7870–7881, Online. As-          arXiv preprint arXiv:2503.19877.
  sociation for Computational Linguistics.
                                                          Takeshi Kojima, Shixiang (Shane) Gu, Machel Reid, Yu-
Peter Clark, Oyvind Tafjord, and Kyle Richardson. 2021.     taka Matsuo, and Yusuke Iwasawa. 2022. Large lan-
  Transformers as soft reasoners over language. In          guage models are zero-shot reasoners. In Advances in
  Proceedings of the Twenty-Ninth International Joint       Neural Information Processing Systems, volume 35,
  Conference on Artificial Intelligence, IJCAI’20.          pages 22199–22213. Curran Associates, Inc.
Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian,           Laura Kovács and Andrei Voronkov. 2013. First-order
  Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias            theorem proving and vampire. In Computer Aided
  Plappert, Jerry Tworek, Jacob Hilton, Reiichiro           Verification, pages 1–35, Berlin, Heidelberg. Springer
  Nakano, Christopher Hesse, and John Schulman.             Berlin Heidelberg.
  2021. Training verifiers to solve math word prob-
  lems. arXiv preprint arXiv:2110.14168.                  Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying
                                                           Sheng, Lianmin Zheng, Cody Hao Yu, Joseph E.
Leonardo de Moura and Nikolaj Bjørner. 2008. Z3: an        Gonzalez, Hao Zhang, and Ion Stoica. 2023. Effi-
  efficient smt solver. In 2008 Tools and Algorithms       cient memory management for large language model
  for Construction and Analysis of Systems, pages 337–     serving with pagedattention. In Proceedings of the
  340. Springer, Berlin, Heidelberg.                       ACM SIGOPS 29th Symposium on Operating Systems
                                                           Principles.
DeepSeek-AI. 2025. Deepseek-r1 incentivizes reason-
  ing capability in large language models. Nature.        Aitor Lewkowycz, Anders Johan Andreassen,
                                                            David Dohan, Ethan Dyer, Henryk Michalewski,
Zhangyin Feng, Qianglong Chen, Ning Lu, Yongqian            Vinay Venkatesh Ramasesh, Ambrose Slone, Cem
  Li, Siqi Cheng, Shuangmu Peng, Duyu Tang, Sheng-          Anil, Imanol Schlag, Theo Gutman-Solo, Yuhuai Wu,
  cai Liu, and Zhirui Zhang. 2025. Is PRM necessary?        Behnam Neyshabur, Guy Gur-Ari, and Vedant Misra.
  problem-solving RL implicitly induces PRM capabil-        2022. Solving quantitative reasoning problems with
  ity in LLMs. In The Thirty-ninth Annual Conference        language models. In Advances in Neural Information
  on Neural Information Processing Systems.                 Processing Systems.
Simeng Han, Hailey Schoelkopf, Yilun Zhao, Zhent-         Yifei Li, Zeqi Lin, Shizhuo Zhang, Qiang Fu, Bei Chen,
  ing Qi, Martin Riddell, Wenfei Zhou, James Coady,         Jian-Guang Lou, and Weizhu Chen. 2023. Making
  David Peng, Yujie Qiao, Luke Benson, Lucy Sun,             language models better reasoners with step-aware
  Alexander Wardle-Solano, Hannah Szabó, Ekaterina          verifier. In Proceedings of the 61st Annual Meet-
  Zubova, Matthew Burtell, Jonathan Fan, Yixin Liu,          ing of the Association for Computational Linguistics
  Brian Wong, Malcolm Sailor, and 16 others. 2024.          (Volume 1: Long Papers), pages 5315–5333, Toronto,
  FOLIO: Natural language reasoning with first-order         Canada. Association for Computational Linguistics.
  logic. In Proceedings of the 2024 Conference on
  Empirical Methods in Natural Language Processing,       Hunter Lightman, Vineet Kosaraju, Yuri Burda, Harri-
  pages 22017–22031, Miami, Florida, USA. Associa-          son Edwards, Bowen Baker, Teddy Lee, Jan Leike,
  tion for Computational Linguistics.                       John Schulman, Ilya Sutskever, and Karl Cobbe.
                                                            2024. Let’s verify step by step. In The Twelfth Inter-
Jujie He, Tianwen Wei, Rui Yan, Jiacai Liu, Chaojie         national Conference on Learning Representations.
  Wang, Yimeng Gan, Shiwen Tu, Chris Yuhao Liu,
   Liang Zeng, Xiaokun Wang, Boyang Wang, Yong-           Wang Ling, Dani Yogatama, Chris Dyer, and Phil Blun-
   cong Li, Fuxiang Zhang, Jiacheng Xu, Bo An, Yang         som. 2017. Program induction by rationale genera-
   Liu, and Yahui Zhou. 2024. Skywork-o1 open series.       tion: Learning to solve and explain algebraic word
   https://huggingface.co/Skywork.                          problems. In Proceedings of the 55th Annual Meet-
                                                            ing of the Association for Computational Linguistics
Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul         (Volume 1: Long Papers), pages 158–167, Vancouver,
  Arora, Steven Basart, Eric Tang, Dawn Song, and           Canada. Association for Computational Linguistics.
  Jacob Steinhardt. 2021. Measuring mathematical
  problem solving with the MATH dataset. In Thirty-       Llama Team. 2024. The llama 3 herd of models. arXiv
  fifth Conference on Neural Information Processing         preprint arXiv:2407.21783.
  Systems Datasets and Benchmarks Track (Round 2).
                                                          Ilya Loshchilov and Frank Hutter. 2019. Decoupled
Muhammad Khalifa, Rishabh Agarwal, Lajanugen Lo-             weight decay regularization. In International Confer-
 geswaran, Jaekyeom Kim, Hao Peng, Moontae Lee,              ence on Learning Representations.
 Honglak Lee, and Lu Wang. 2025. Process reward
 models that think. arXiv preprint arXiv:2504.16828.      Liangchen Luo, Yinxiao Liu, Rosanne Liu, Samrat
                                                            Phatale, Meiqi Guo, Harsh Lara, Yunxuan Li, Lei
Seungone Kim, Ian Wu, Jinu Lee, Xiang Yue, Seongyun         Shu, Yun Zhu, Lei Meng, Jiao Sun, and Abhinav
  Lee, Mingyeong Moon, Kiril Gashteovski, Carolin           Rastogi. 2024. Improve mathematical reasoning in
  language models by automated process supervision.         Tobias Nipkow, Markus Wenzel, and Lawrence C. Paul-
  arXiv preprint arXiv:2406.06592.                            son. 2002. Isabelle/HOL: A Proof Assistant for
                                                              Higher-Order Logic, volume 2283 of Lecture Notes
Qianli Ma, Haotian Zhou, Tingkai Liu, Jianbo Yuan,            in Computer Science. Springer.
  Pengfei Liu, Yang You, and Hongxia Yang. 2023.
  Let’s reward step by step: Step-level reward model        Theo Olausson, Alex Gu, Ben Lipkin, Cedegao Zhang,
  as the navigators for reasoning. arXiv preprint             Armando Solar-Lezama, Joshua Tenenbaum, and
  arXiv:2310.10080.                                           Roger Levy. 2023. LINC: A neurosymbolic approach
                                                              for logical reasoning by combining language models
Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler              with first-order logic provers. In Proceedings of the
 Hallinan, Luyu Gao, Sarah Wiegreffe, Uri Alon,               2023 Conference on Empirical Methods in Natural
 Nouha Dziri, Shrimai Prabhumoye, Yiming Yang,                Language Processing, pages 5153–5176, Singapore.
 Shashank Gupta, Bodhisattwa Prasad Majumder,                 Association for Computational Linguistics.
 Katherine Hermann, Sean Welleck, Amir Yazdan-
 bakhsh, and Peter Clark. 2023. Self-refine: Itera-         Sam Paech. 2024. Mmlu-pro-nomath.
 tive refinement with self-feedback. In Advances in
 Neural Information Processing Systems, volume 36,
                                                            Sarah Pan, Vladislav Lialin, Sherin Muckatira, and
 pages 46534–46594. Curran Associates, Inc.
                                                              Anna Rumshisky. 2023. Let’s reinforce step by step.
R. Thomas McCoy, Ellie Pavlick, and Tal Linzen. 2019.         In NeurIPS 2023 Workshop on Instruction Tuning
   Right for the wrong reasons: Diagnosing syntactic          and Instruction Following.
   heuristics in natural language inference. In Proceed-
   ings of the 57th Annual Meeting of the Association for   Debjit Paul, Mete Ismayilzada, Maxime Peyrard, Beat-
   Computational Linguistics, pages 3428–3448, Flo-           riz Borges, Antoine Bosselut, Robert West, and Boi
   rence, Italy. Association for Computational Linguis-       Faltings. 2024. REFINER: Reasoning feedback on
   tics.                                                      intermediate representations. In Proceedings of the
                                                              18th Conference of the European Chapter of the As-
Arindam Mitra, Hamed Khanpour, Corby Rosset, and              sociation for Computational Linguistics (Volume 1:
  Ahmed Awadallah. 2024. Orca-math: Unlocking                 Long Papers), pages 1100–1126, St. Julian’s, Malta.
  the potential of slms in grade school math. arXiv           Association for Computational Linguistics.
  preprint arXiv:2402.14830.
                                                            Stanislas Polu and Ilya Sutskever. 2020. Generative
Terufumi Morishita, Gaku Morio, Atsuki Yamaguchi,              language modeling for automated theorem proving.
  and Yasuhiro Sogawa. 2023. Learning deductive rea-           arXiv preprint arXiv:2009.03393.
  soning from synthetic corpus based on formal logic.
  In Proceedings of the 40th International Conference       Qwen Team. 2024. Qwen2.5 technical report. arXiv
  on Machine Learning, volume 202 of Proceedings             preprint arXiv:2412.15115.
  of Machine Learning Research, pages 25254–25274.
  PMLR.                                                     Qwen Team. 2025. Qwen3 technical report. arXiv
                                                             preprint arXiv:2505.09388.
Terufumi Morishita, Gaku Morio, Atsuki Yamaguchi,
  and Yasuhiro Sogawa. 2024. Enhancing reasoning            Rafael Rafailov, Archit Sharma, Eric Mitchell, Christo-
  capabilities of LLMs via principled synthetic logic         pher D Manning, Stefano Ermon, and Chelsea Finn.
  corpus. In The Thirty-eighth Annual Conference on           2023. Direct preference optimization: Your language
  Neural Information Processing Systems.                      model is secretly a reward model. In Thirty-seventh
                                                              Conference on Neural Information Processing Sys-
Leonardo de Moura and Sebastian Ullrich. 2021. The
                                                              tems.
  lean 4 theorem prover and programming language.
  In Automated Deduction – CADE 28: 28th Interna-
  tional Conference on Automated Deduction, Virtual         Z. Z. Ren, Zhihong Shao, Junxiao Song, Huajian Xin,
  Event, July 12–15, 2021, Proceedings, page 625–635,          Haocheng Wang, Wanjia Zhao, Liyue Zhang, Zhe Fu,
  Berlin, Heidelberg. Springer-Verlag.                         Qihao Zhu, Dejian Yang, Z. F. Wu, Zhibin Gou, Shi-
                                                               rong Ma, Hongxuan Tang, Yuxuan Liu, Wenjun Gao,
M. Saqib Nawaz, Moin Malik, Yi Li, Meng Sun, and               Daya Guo, and Chong Ruan. 2025. Deepseek-prover-
  M. Ikram Ullah Lali. 2019. A survey on theo-                 v2: Advancing formal mathematical reasoning via
  rem provers in formal methods. arXiv preprint                reinforcement learning for subgoal decomposition.
  arXiv:1912.03028.                                            arXiv preprint arXiv:2504.21801.

Yixin Nie, Adina Williams, Emily Dinan, Mohit Bansal,       William Saunders, Catherine Yeh, Jeff Wu, Steven Bills,
  Jason Weston, and Douwe Kiela. 2020. Adversarial            Long Ouyang, Jonathan Ward, and Jan Leike. 2022.
  NLI: A new benchmark for natural language under-            Self-critiquing models for assisting human evaluators.
  standing. In Proceedings of the 58th Annual Meet-           arXiv preprint arXiv:2206.05802.
  ing of the Association for Computational Linguistics,
  pages 4885–4901, Online. Association for Computa-         Stephan Schulz. 2002. E - a brainiac theorem prover.
  tional Linguistics.                                         AI Commun., 15(2,3):111–126.
Charlie Victor Snell, Jaehoon Lee, Kelvin Xu, and Avi-    Wei Xiong, Hanning Zhang, Nan Jiang, and Tong Zhang.
  ral Kumar. 2025. Scaling LLM test-time compute            2024. An implementation of generative prm. https:
  optimally can be more effective than scaling param-      //github.com/RLHFlow/RLHF-Reward-Modeling.
  eters for reasoning. In The Thirteenth International
  Conference on Learning Representations.                 Kaiyu Yang, Jia Deng, and Danqi Chen. 2022. Gen-
                                                            erating natural language proofs with verifier-guided
Mirac Suzgun, Nathan Scales, Nathanael Schärli, Se-         search. In Proceedings of the 2022 Conference on
  bastian Gehrmann, Yi Tay, Hyung Won Chung,                Empirical Methods in Natural Language Processing,
  Aakanksha Chowdhery, Quoc Le, Ed Chi, Denny               pages 89–105, Abu Dhabi, United Arab Emirates.
  Zhou, and Jason Wei. 2023. Challenging BIG-bench          Association for Computational Linguistics.
  tasks and whether chain-of-thought can solve them.
  In Findings of the Association for Computational Lin-   Kaiyu Yang, Gabriel Poesia, Jingxuan He, Wenda Li,
  guistics: ACL 2023, pages 13003–13051, Toronto,           Kristin E. Lauter, Swarat Chaudhuri, and Dawn Song.
  Canada. Association for Computational Linguistics.        2025. Position: Formal mathematical reasoning—a
                                                            new frontier in AI. In Forty-second International
Oyvind Tafjord, Bhavana Dalvi, and Peter Clark. 2021.       Conference on Machine Learning Position Paper
  ProofWriter: Generating implications, proofs, and         Track.
  abductive statements over natural language. In Find-    Kaiyu Yang, Aidan Swope, Alex Gu, Rahul Chala-
  ings of the Association for Computational Linguis-        mala, Peiyang Song, Shixing Yu, Saad Godil, Ryan J
  tics: ACL-IJCNLP 2021, pages 3621–3634, Online.           Prenger, and Animashree Anandkumar. 2023. Le-
  Association for Computational Linguistics.                andojo: Theorem proving with retrieval-augmented
                                                            language models. In Advances in Neural Information
The Coq Development Team. 2024. The Coq reference           Processing Systems, volume 36, pages 21573–21612.
  manual – release 8.19.0. https://coq.inria.fr/            Curran Associates, Inc.
  doc/V8.19.0/refman.
                                                          Longhui Yu, Weisen Jiang, Han Shi, Jincheng YU,
Jidong Tian, Yitian Li, Wenqing Chen, Liqiang Xiao,         Zhengying Liu, Yu Zhang, James Kwok, Zhenguo Li,
   Hao He, and Yaohui Jin. 2021. Diagnosing the first-      Adrian Weller, and Weiyang Liu. 2024. Metamath:
   order logical reasoning ability through LogicNLI.        Bootstrap your own mathematical questions for large
   In Proceedings of the 2021 Conference on Empiri-         language models. In The Twelfth International Con-
   cal Methods in Natural Language Processing, pages        ference on Learning Representations.
   3738–3747, Online and Punta Cana, Dominican Re-
   public. Association for Computational Linguistics.     Lifan Yuan, Wendi Li, Huayu Chen, Ganqu Cui, Ning
                                                             Ding, Kaiyan Zhang, Bowen Zhou, Zhiyuan Liu,
Jonathan Uesato, Nate Kushman, Ramana Kumar, Fran-           and Hao Peng. 2025. Free process rewards without
  cis Song, Noah Siegel, Lisa Wang, Antonia Creswell,        process labels. In Forty-second International Confer-
  Geoffrey Irving, and Irina Higgins. 2022. Solving          ence on Machine Learning.
  math word problems with process- and outcome-
  based feedback. arXiv preprint arXiv:2211.14275.        Thomas Zeng, Shuibai Zhang, Shutong Wu, Christian
                                                            Classen, Daewon Chae, Ethan Ewer, Minjae Lee,
Peiyi Wang, Lei Li, Zhihong Shao, Runxin Xu, Damai          Heeju Kim, Wonjun Kang, Jackson Kunde, Ying Fan,
  Dai, Yifei Li, Deli Chen, Yu Wu, and Zhifang Sui.         Jungtaek Kim, Hyung Il Koo, Kannan Ramchandran,
  2024. Math-shepherd: Verify and reinforce LLMs            Dimitris Papailiopoulos, and Kangwook Lee. 2025.
  step-by-step without human annotations. In Proceed-       VersaPRM: Multi-domain process reward model via
  ings of the 62nd Annual Meeting of the Association        synthetic reasoning data. In Forty-second Interna-
  for Computational Linguistics (Volume 1: Long Pa-         tional Conference on Machine Learning.
  pers), pages 9426–9439, Bangkok, Thailand. Associ-      Dan Zhang, Sining Zhoubian, Ziniu Hu, Yisong Yue,
  ation for Computational Linguistics.                      Yuxiao Dong, and Jie Tang. 2024a. ReST-MCTS*:
                                                            LLM self-training via process reward guided tree
Sean Welleck. 2023. Neural theorem proving tutorial.        search. In The Thirty-eighth Annual Conference on
  https://github.com/wellecks/ntptutorial.                  Neural Information Processing Systems.
Yuhuai Wu, Albert Qiaochu Jiang, Wenda Li, Markus         Lunjun Zhang, Arian Hosseini, Hritik Bansal, Mehran
  Rabe, Charles Staats, Mateja Jamnik, and Christian        Kazemi, Aviral Kumar, and Rishabh Agarwal. 2024b.
  Szegedy. 2022. Autoformalization with large lan-          Generative verifiers: Reward modeling as next-token
  guage models. In Advances in Neural Information           prediction. In The 4th Workshop on Mathematical
  Processing Systems, volume 35, pages 32353–32368.         Reasoning and AI at NeurIPS’24.
  Curran Associates, Inc.
                                                          Zhenru Zhang, Chujie Zheng, Yangzhen Wu, Beichen
Huajian Xin, Daya Guo, Zhihong Shao, Zhizhou Ren,           Zhang, Runji Lin, Bowen Yu, Dayiheng Liu, Jin-
  Qihao Zhu, Bo Liu, Chong Ruan, Wenda Li, and              gren Zhou, and Junyang Lin. 2025. The lessons of
  Xiaodan Liang. 2024. Deepseek-prover: Advancing           developing process reward models in mathematical
  theorem proving in llms through large-scale synthetic     reasoning. In Findings of the Association for Compu-
  data. arXiv preprint arXiv:2405.14333.                    tational Linguistics: ACL 2025, pages 10495–10516,
  Vienna, Austria. Association for Computational Lin-            Table of Contents of Appendix
  guistics.
Chujie Zheng, Zhenru Zhang, Beichen Zhang, Runji          A Additional Related Work                        13
  Lin, Keming Lu, Bowen Yu, Dayiheng Liu, Jingren
  Zhou, and Junyang Lin. 2025. ProcessBench: Iden-        B Examples from F OV ER-40K                      14
  tifying process errors in mathematical reasoning. In
  Proceedings of the 63rd Annual Meeting of the As-       C Creation Process of F OV ER-40K                14
  sociation for Computational Linguistics (Volume 1:
  Long Papers), pages 1009–1024, Vienna, Austria.           C.1 Formal Logic . . . . . . . . . . .         15
  Association for Computational Linguistics.                C.2 Formal Theorem Proving . . . . .           16
Yaowei Zheng, Richong Zhang, Junhao Zhang, Yanhan
  Ye, and Zheyan Luo. 2024. LlamaFactory: Unified         D F OV ER Beyond F OV ER-40K                     17
  efficient fine-tuning of 100+ language models. In
  Proceedings of the 62nd Annual Meeting of the As-       E Implementation Details                  17
  sociation for Computational Linguistics (Volume 3:        E.1 Input Format and Postprocessing . 17
  System Demonstrations), pages 400–410, Bangkok,
  Thailand. Association for Computational Linguistics.      E.2 Training Settings . . . . . . . . . 18
                                                            E.3 Evaluation Settings of Best-of-K . 18
Jin Peng Zhou, Charles E Staats, Wenda Li, Christian
                                                            E.4 Computational Resources . . . . . 19
   Szegedy, Kilian Q Weinberger, and Yuhuai Wu. 2024.
   Don’t trust: Verify – grounding LLM quantitative         E.5 Model Access and Software Libraries 19
   reasoning with autoformalization. In The Twelfth In-
   ternational Conference on Learning Representations.    F Ethical Considerations                         19

                                                          G Reproducibility Statement and License 19


                                                          A   Additional Related Work

                                                          Applications of PRMs. PRMs can be used to
                                                          supervise LLM reasoning during training and in-
                                                          ference. For training, PRMs can generate reward
                                                          signals, particularly in reinforcement learning set-
                                                          tings (Pan et al., 2023; Zhang et al., 2024a). They
                                                          can be applied either to re-rank candidate responses
                                                          from the policy or to provide direct reward (Ue-
                                                          sato et al., 2022). For inference, PRMs can guide
                                                          response selection and refinement through Best-
                                                          of-K (Li et al., 2023), self-correction (Saunders
                                                          et al., 2022; Madaan et al., 2023), and step-level
                                                          search (Ma et al., 2023; Snell et al., 2025).
                                                          Outcome-based training for PRMs. Provided the
                                                          difficulty of collecting step-level error labels, re-
                                                          cent work proposes methods to train PRMs without
                                                          using step-level labels. Yuan et al. (2025) proposes
                                                          implicit PRMs that can be trained only using fi-
                                                          nal answers. They theoretically show that ORMs
                                                          trained with the reward that is parameterized by the
                                                          log-likelihood ratio of two causal language mod-
                                                          els (e.g., DPO (Rafailov et al., 2023)) implicitly
                                                          learns a Q function and can be used as PRMs.
                                                          In addition, recent work (Feng et al., 2025; Kim
                                                          et al., 2025) reports that existing Large Reasoning
                                                          Models like DeepSeek-R1 (DeepSeek-AI, 2025)
                                                          have strong process-level rewarding capabilities on
mathematical reasoning tasks, while they are not                        Your task is to evaluate the accuracy of each step in the
                                                                        ,→  provided solution to the above question. For each
explicitly trained for process-level rewarding.                         ,→  step, respond with "correct" if the reasoning is
                                                                        ,→  logically valid and mathematically sound, or if the
Formal logic and theorem proving. Formal logic                          ,→  step is a general statement or transition that does
                                                                        ,→  not contain reasoning. Respond with "incorrect" if
tasks have been used to evaluate and improve the                        ,→  the step includes any errors or flawed logic.
reasoning of LLMs (Clark et al., 2021; Tafjord                             ** Sotluion **
et al., 2021; Morishita et al., 2024). These tasks are                     fact7 -> int1: {B} -> (¬{DC} & ¬{A})'},
                                                                           {'role': 'assistant', 'content': 'correct'},
often formulated in logical languages compatible                           {'role': 'user', 'content': 'fact6 -> int2: ¬{B}'},
                                                                           {'role': 'assistant', 'content': 'incorrect'}
with automated solvers such as Z3 (de Moura and                       ],
Bjørner, 2008), Vampire (Kovács and Voronkov,                     }

2013), or E (Schulz, 2002). Separately, formal the-
orem proving has been studied in the context of                   Formal theorem proving. Here is an example of
LLM-based proof generation (Polu and Sutskever,                   the data in the formal proof task based on the initial
2020; Yang et al., 2023; Xin et al., 2024), where                 responses from Qwen 2.5 7B.
proof assistants such as Isabelle/HOL (Nipkow
                                                                  {
et al., 2002), Coq (The Coq Development Team,                          'id':
2024), and Lean (Moura and Ullrich, 2021) are                         ,→    'metamathqa_GSM_Rephrased_076554_Qwen2.5-7B-Instruct',
                                                                       'error_labels': [True, True, True, True, True, True,
used to validate generated proofs. In contrast, our                   ,→ False],
                                                                       'messages': [
work presents the first attempt to use verification                       {'role': 'user', 'content': '** Problem **
outputs from these tools as training signals for re-                      Generate a proof for the following theorem in the
                                                                         ,→ Isabelle proof assistant format.
ward models. Moreover, while these tools are de-
                                                                           theorem example:
signed and have been used for solution-level verifi-                            assumes "(Jorge_age_2005::nat) = 16"
                                                                                and "(Jorge_age_difference::nat) = 24"
cation, we introduce a novel use of them to provide                             and "(Jorge_current_age::nat) = Jorge_age_2005 +
step-level supervision for PRMs.                                               ,→ (2022 - 2005)"
                                                                                and "(Simon_current_age::nat) = Jorge_current_age +
                                                                               ,→ Jorge_age_difference"
                                                                                and "(Simon_age_2010::nat) = Simon_current_age +
B     Examples from F OV ER-40K                                                ,→ (2010 - 2022 + 2005)"
                                                                                shows "Simon_age_2010 = 50"

We provide examples from F OV ER-40K.                                   ** Task **\nYour task is to evaluate the accuracy of each
                                                                        ,→  step in the provided solution to the above question.
Formal logic. Here is an example of the data in                         ,→  For each step, respond with "correct" if the
                                                                        ,→  reasoning is logically valid and mathematically
the formal logic task based on the initial responses                    ,→  sound, or if the step is a general statement or
from Llama 3.1 8B.                                                      ,→  transition that does not contain reasoning. Respond
                                                                        ,→  with "incorrect" if the step includes any errors or
                                                                        ,→  flawed logic.
{
    'id': 'fldx2-train-020948_Llama-3.1-8B-Instruct',                    ** Sotluion **
    'error_labels': [True, False],                                       We\'ll start from the beginning and proceed logically.'},
    'messages': [                                                        {'role': 'assistant', 'content': 'correct'},
    {'role': 'user', 'content': '** Problem **                           {'role': 'user', 'content': 'have "Jorge_current_age = 16
       Based on the provided facts ($context$), either prove or         ,→ + (2022 - 2005)" using assms by simp'},
      ,→ disprove the hypothesis or state that it is unknown.            {'role': 'assistant', 'content': 'correct'},
      ,→ The facts and the hypothesis are written in logical             {'role': 'user', 'content': 'then have "Jorge_current_age
      ,→ formulas as follows: capital letters such as "{A}",            ,→ = 16 + 17" using assms by simp\nthen have
      ,→ "{B}", "{AB}" are predicates, small letters such as            ,→ "Jorge_current_age = 33" using assms by simp'},
      ,→ "{a}", "{b}", "{ab}" are constants, "&" is logical              {'role': 'assistant', 'content': 'correct'},
      ,→ conjunction, "v" is logical disjunction, "¬" is                 {'role': 'user', 'content': 'then have "Simon_current_age
      ,→ negation, "->" is implication, "(x)" is "for all x",           ,→ = 33 + 24" using assms by simp'},
      ,→ and "(Ex)" is "for some x".                                     {'role': 'assistant', 'content': 'correct'},
                                                                         {'role': 'user', 'content': 'then have "Simon_current_age
      $hypothesis$: ¬{B}                                                ,→ = 57" using assms by simp'},
                                                                         {'role': 'assistant', 'content': 'correct'},
      $context$:\nfact1: ¬(¬{F} & ¬{G}) -> ¬{E}                          {'role': 'user', 'content': 'then have "Simon_age_2010 =
      fact2: ¬{CF}\nfact3: ¬{IG}                                        ,→ 57 + (2010 - 2022 + 2005)" using assms by simp'},
      fact4: ¬{DQ}                                                       {'role': 'assistant', 'content': 'correct'},
      fact5: ¬{CN}\nfact6: ¬{BA}                                         {'role': 'user', 'content': 'then have "Simon_age_2010 =
      fact7: {B} -> (¬{DC} & ¬{A})                                      ,→ 57 + 83" using assms by simp'},
      fact8: ¬{DM}\nfact9: {C} -> {B}                                    {'role': 'assistant', 'content': 'incorrect'}
      fact10: ¬{IF}                                                   ],
      fact11: ¬{JJ}                                               }
      fact12: (¬{GL} & ¬{AP})
      fact13: ¬{E} -> ({D} & {C})
      fact14: (¬{A} & ¬{B})
      fact15: (¬{DC} & ¬{L})
      fact16: ¬{IJ}
      fact17: ¬{EM}                                               C        Creation Process of F OV ER-40K
      fact18: {H} -> ¬(¬{F} & ¬{G})
      fact19: ¬{DO}                                               This section provides details of the creation process
      ** Task **                                                  of F OV ER-40K, which is outlined in Section 3.
                 Formal Step generated from LLM                                   the verification pipeline, we removed cases whose
               int2 & int1 -> int3: ({D}{b} & ¬{C}{b});
                                                                                  reasoning steps include “assump,” which is used in
                                                                                  cases such as proof by contradiction.
                      Postprocessed Step
              ¬{C}{b} & {D}{b} -> ({D}{b} & ¬{C}{b});                                We generate formal solutions from Llama 3.1 8B
                                                                                  and Qwen 2.5 7B. The following is an example of
                           Automatic Verifier (Z3)
                                                                                  a few-shot demonstration for the initial generation.
                                                                                  We provide six examples as a demonstration. After
                                                                                  generating the formal solutions, we filter out those
                                           ✅                                      with an invalid format using Z3.
                         (a) Formal logic task.
                                  Informal Question
                                                                                  {
                                                                                       'role': 'user',
           A store owner bought 1500 pencils at $0.10 each. If he sells them
           for $0.25 each, how many of them must he sell to make a profit of
                                                                                       'content':
                                  exactly $100.00?                                        'Based on the provided facts ($context$), either prove or
             Final Answer                          1000 pencils.
                                                                                         ,→ disprove the hypothesis or state that it is unknown.
                                                                                         ,→ The facts and the hypothesis are written in logical
                                   Conversion LLM
                                                                                         ,→ formulas as follows: capital letters such as "{A}",
                                                                                         ,→ "{B}", "{AB}" are predicates, small letters such as
                                                                                         ,→ "{a}", "{b}", "{ab}" are constants, "&" is logical
                                  Formal Statement
                                                                                         ,→ conjunction, "v" is logical disjunction, "¬" is
           assumes "(total_pencils::nat) = 1500"                                         ,→ negation, "->" is implication, "(x)" is "for all x",
            and "(cost_per_pencil::real) = 0.10"
                                                                                         ,→ and "(Ex)" is "for some x".
            and "(sell_price_per_pencil::real) = 0.25" [...]
           shows "pencils_to_sell = 1000"
                                                                                            Don't generate anything other than the proof and
                                           LLM                                             ,→   proof_label.
                                                                                            Don't generate the proof by contradiction. If the
                                     Formal Proof                                          ,→ hypothesis is disproved, provide a direct
                                                                                           ,→ counterexample. If the proof_label is PROVED, your
           have "total_pencils * cost_per_pencil = 150" by simp
           then have "profit + (total_pencils * cost_per_pencil) = 250" by simp            ,→ proof should end with the 'hypothesis'. If the
           then have "(profit + (total_pencils * cost_per_pencil)) / [...]                 ,→ proof_label is DISPROVED, your proof should end with
           have "total_pencils * cost_per_pencil / [...]                                   ,→ '¬hypothesis'.

                             Automatic Verifier (Isabelle)                                 $hypothesis$: ({AB}{c} & ¬{B}{c})

                                             ✅                                             $context$:
                                                                                           fact1: (x): ¬{D}x -> ({A}x & {C}x)
             (b) Formal theorem proving task.                                              fact2: ¬({B}{a} & ¬{A}{a})
                                                                                           fact3: ¬{AB}{b} -> ¬{C}{d}
Figure 6: Automatic step-level error annotation for                                        fact4: ¬{C}{a} -> ¬{A}{d}
                                                                                           fact5: ¬{A}{a}
F OV ER-40K by formal verification tools.                                                  fact6: ({AB}{c} & ¬{B}{c}) -> {C}{d}
                                                                                           fact7: ¬({F}{b} v {D}{b}) -> ¬{D}{a}
                                                                                           fact8: {A}{a} -> ({AB}{c} & ¬{B}{c})
                                                                                           fact9: ({AB}{c} & ¬{AA}{c}) -> {B}{b}
C.1     Formal Logic                                                                       fact10: ({AB}{c} & ¬{B}{c}) -> {C}{b}'
                                                                                  },
                                                                                  {
Formal solution generation (Appendix C.1.1).                                           'role': 'assistant',
                                                                                       'content':
We prompt Llama 3.1 8B and Qwen 2.5 7B to                                                '$proof$:
                                                                                         fact6 -> int1: ¬{C}{d} -> ¬({AB}{c} & ¬{B}{c});
generate step-by-step formal solutions to FLDx2                                          fact3 & int1 -> int2: ¬{AB}{b} -> ¬({AB}{c} & ¬{B}{c});
in a format compatible with Z3. We use a few-shot
                                                                                           $proof_label$: UNKNOWN'
instruction to guide LLMs to follow the format and                                }
filter out syntactically invalid solutions using Z3.
Automatic error annotation (Appendix C.1.2).                                      C.1.2         Automatic Step-level Annotation
Z3 is designed for verification at the solution level,                            Second, we automatically annotate step-level er-
but we use it at the step level by supplying Z3 with                              ror labels, which will be used to train PRMs. We
the premises and conclusion for the target step to                                use Z3 (de Moura and Bjørner, 2008) for annotat-
determine logical validity, as in Figure 6a.                                      ing step-level error labels. Specifically, we use the
                                                                                  checker provided by the FLDx2 paper (Morishita
C.1.1    Initial Response Generation
                                                                                  et al., 2024) based on Z3.1 Z3 is originally de-
First, we need to generate symbolic solutions from                                signed for solution-level verification, so we need to
LLMs, which may include logical mistakes, but                                     write code to use it for step-level verification. As
they should be in a valid format compatible with                                  explained in Figure 6a, we first postprocess each
Z3 (de Moura and Bjørner, 2008).
   We use FLDx2 (Morishita et al., 2023, 2024) as                                     https://github.com/hitachi-nlp/FLD-generator/
                                                                                       1

                                                                                  blob/00d12c4a9132a4fb43cd77f24db03ea7f5b27877/
a base dataset for our formal logic task. We use                                  FLD_generator/formula_checkers/z3_logic_
the symbolic version of the dataset. To simplify                                  checkers/checkers.py#L179
step in solutions to an independent logical step and           'content': 'proof -
                                                                  have "Cypress_count * Cypress_price = 2000"
check the validity using Z3.                                          using assms by simp
                                                                  then have "Maple_count * Maple_price = 7200"
                                                                      using assms by simp
C.2   Formal Theorem Proving                                      then have "Pine_count * Pine_price = 120000"
                                                                      using assms by simp
Formal statement generation (Appendix C.2.1).                     then have "Gloria_cash + Cypress_count * Cypress_price +
                                                                 ,→ Maple_count * Maple_price + Pine_count * Pine_price =
We first generate formal statements in the for-                  ,→ 129200"
                                                                      using assms by simp
mat compatible with Isabelle from GSM8K-level                     then have "Gloria_cash + Cypress_count * Cypress_price +
problems, including GSM8K (Cobbe et al., 2021),                  ,→ Maple_count * Maple_price + Pine_count * Pine_price -
                                                                 ,→ Cabin_cost = 200"
GSM8K-based cases in MetaMathQA (Yu et al.,                           using assms by simp
                                                                  then have "After_paying_Alfonso = 200"
2024), and math word problems in Big-Math (Al-                        using assms by simp
balak et al., 2025), using Qwen 2.5 7B.                           show ?thesis
                                                                      using assms by simp
                                                             qed'
Formal solution generation (Appendix C.2.2).                 }
We instruct Qwen 2.5 7B to generate step-by-step
formal proofs in the format compatible with Is-              C.2.3    Automatic Step-level Proof Verification
abelle to the formal statements.
                                                             Format verification. As we use LLMs for the con-
Automatic error annotation (Appendix C.2.3).
                                                             version, it is possible that the conversion generates
Isabelle is designed for solution-level verification.
                                                             proofs in an invalid format. To filter out theorems
To obtain step-level error labels, we implement
                                                             in the invalid format, we use the “sorry” keyword
wrapper code for step-level verification. Our code
                                                             of Isabelle. The “sorry” keyword serves as a place-
assumes that the other steps are correct when eval-
                                                             holder for incomplete or unproven proofs, allowing
uating the target step.
                                                             the theorem to be accepted by the system without
C.2.1 Formal Statement Generation                            a formal justification. By inserting “sorry” into all
First, we generate formal statements in the for-             generated proof steps, we can isolate and verify
mat compatible with Isabelle (Nipkow et al., 2002).          only the syntactic correctness theorems.
Motivated by prior work (Zhou et al., 2024), we                 For example, in the following proof,
generate formal statements from math word prob-              babysitting_minutes × (Weng_hourly_wage
lems using Qwen 2.5 7B with few-shot prompting.              / 60) contains the symbol ×, which is not a valid
Specifically, we convert informal GSM8K-level                multiplication operator in Isabelle syntax.
math word problems: GSM8K (Cobbe et al., 2021),              theorem example:
                                                                  assumes "(Weng_hourly_wage::real) = 12"
GSM8K-based cases in MetaMathQA (Yu et al.,                            and "(babysitting_minutes::real) = 50"
2024), and math word problems in Big-Math (Al-                         and "(babysitting_hours::real) = babysitting_minutes
                                                                      ,→ / 60"
balak et al., 2025), into formal statements.                           and "(Weng_earnings::real) = Weng_hourly_wage *
                                                                      ,→ babysitting_hours"
                                                                  shows "Weng_earnings = 10"
C.2.2 Formal Proof Generation                                proof -
                                                                  have "Weng_hourly_wage / 60 = 0.20"
We provide an instruction with few-shot examples                       sorry
to generate formal proofs from Qwen 2.5 7B. The                   then have "babysitting_minutes × (Weng_hourly_wage / 60)
                                                                 ,→ = 10"
following is an example of a few-shot demonstra-                       sorry
                                                                  then have "Weng_earnings = 10"
tion for the formal proof generation.                                  sorry
                                                                  thus ?thesis
{                                                                      sorry
   'role': 'user',                                           qed
   'content': '** Formal Statement **
theorem example:
     assumes "(Cabin_cost::nat) = 129000"                    For this input, Isabelle returns the following error.
          and "(Gloria_cash::nat) = 150"
          and "(Cypress_count::nat) = 20"                    Step error: Inner syntax error (line 1)\nat \"? (
          and "(Pine_count::nat) = 600"                      ,→  Weng_hourly_wage / 60 ) = 10\"\nFailed to parse prop\nAt
          and "(Maple_count::nat) = 24"                      ,→  command \"have\" (line 1)
          and "(Cypress_price::nat) = 100"
          and "(Maple_price::nat) = 300"
          and "(Pine_price::nat) = 200"
          and "(After_paying_Alfonso::nat) = Gloria_cash +   Step-level verification. By default, Isabelle halts
         ,→ Cypress_count * Cypress_price + Maple_count *
         ,→ Maple_price + Pine_count * Pine_price -          at the first encountered error and does not provide
         ,→ Cabin_cost"
     shows "After_paying_Alfonso = 200"'                     a step-by-step verification of a proof. To enable
},                                                           independent verification of each step in a multi-
{
   'role': 'assistant',                                      step proof, we insert the “sorry” keyword in all but
one step. This allows Isabelle to type-check and                 models to further improve their capabilities to gen-
parse each step individually, even if other steps are            erate formal solutions and be more suitable for
incomplete or invalid.                                           creating PRM training data using F OV ER.
   The following example is for verifying the third                 Second, we need to make formal verification
step independently. For each theorem, we run Is-                 tools verify step-level correctness. The tools are
abelle once per step.                                            often designed for solution-level verification, so
theorem example:
                                                                 we often need to adapt them for step-level verifica-
     assumes "(wallet_cost::nat) = 100"                          tion, as we did in this paper for creating F OV ER-
          and "(betty_savings::nat) = wallet_cost div 2"
          and "(parent_contribution::nat) = 15"                  40K. When creating PRM training data using more
          and "(grandparent_contribution::nat) = 2 *
         ,→ parent_contribution"
                                                                 complex tasks, we may need to further modify the
          and "(total_savings::nat) = betty_savings +            verification pipeline to support new operations.
         ,→ parent_contribution + grandparent_contribution"
          and "(additional_needed::nat) = wallet_cost -             For example, to keep the verification pipeline
         ,→ total_savings"
     shows "additional_needed = 5"                               simple, we did not use problems that involve as-
proof -                                                          sumptions in the formal logic task (FLDx2), such
     have "betty_savings = wallet_cost div 2"
          sorry                                                  as proofs by contradiction, when creating F OV ER-
     then have "betty_savings = 50"
          sorry                                                  40K. However, we can extend our verification
     have "grandparent_contribution = 2 * parent_contribution"
          by simp
                                                                 pipeline to support such cases. Existing verification
     then have "grandparent_contribution = 30"                   tools are already capable of performing solution-
          sorry
     then have "parent_contribution + grandparent_contribution   level verification for proofs by contradiction, so we
    ,→ = 45"
          sorry                                                  can make use of them to provide step-level verifi-
     then have "total_savings = 95"                              cation. When handling assumptions in our frame-
          sorry
     then have "additional_needed = wallet_cost -                work, the type of mistake that cannot be detected
    ,→ total_savings"
          sorry                                                  through our current step-independent verification
     then have "additional_needed = 5"                           alone is illustrated by the following example, be-
          sorry
     thus ?thesis                                                cause the step-independent verification assumes
          sorry
                                                                 that preceding intermediate results are correct:
D    F OV ER Beyond F OV ER-40K                                  • Premises: fact1: B; fact2: B→C; fact3: C→A;
As the first work towards this direction, we eval-               • Hypothesis: A
uate F OV ER by creating PRM training data using
relatively simple tasks with a minimal pipeline to               • fact1 and fact2 → C; Assume A; A → Hypothe-
keep the evaluation focused and clear. However,                    sis; Therefore, the hypothesis is proved.
F OV ER is not limited to the tasks and tools we
                                                                 In this case, the existing solution-level verifica-
used in this paper and can be extended to create
                                                                 tion will identify this solution as an error because
training data using different types of tasks or more
                                                                 the assumption is not properly discharged. Thus,
complex tasks. When applying F OV ER to create
                                                                 by combining step-independent verification with
PRM training data using more complex tasks, there
                                                                 solution-level verification, we can identify and la-
are two potential challenges: (1) generating formal
                                                                 bel the final step as erroneous.
solutions from LLMs in a valid format compatible
with formal verification tools and (2) verifying step-           E     Implementation Details
level correctness using formal verification tools.
   First, formal solutions should be in a syntacti-              This section provides details of our experiments.
cally valid format compatible with formal verifica-
                                                                 E.1    Input Format and Postprocessing
tion tools we use for verification. Following syntac-
tical rules and formats of some formal verification              F OV ER-PRMs and the baseline PRMs. We cre-
tools can be challenging for LLMs, especially when               ate inputs to LLM-based PRMs by preprocessing
we target more complex problems. Recent LLMs                     step-by-step solutions into a conversation format
are increasingly capable of generating formal solu-              where each input contains a single step, and the
tions in valid formats, showing strong performance               expected output is a single token: “correct” or “in-
in first-order logic (Olausson et al., 2023) and a               correct”. To obtain step-level scores, we extract
growing ability to produce syntactically valid for-              logits for the two words and apply the softmax
mal proofs (Ren et al., 2025). We expect future                  function to compute the prediction probability for
“correct”. This approach follows prior work (Xiong                   8B-Mistral (Xiong et al., 2024), the input format
et al., 2024) that uses LLMs as PRMs. As the base-                   is mostly similar to ours, with the key difference
line PRMs are not fine-tuned, we provide zero-shot                   being the use of “+” and “-” instead of “correct”
instructions about this format.                                      and “incorrect”.2 For these models, we apply our
   First, we describe the input format for F OV ER-                  input format and postprocessing procedures with a
PRMs and the baseline LLM-based PRMs, which                          simple substitution of “correct” with “+”.
are based on Llama 3.1 8B and Qwen 2.5 7B.                           PRMs based on Qwen 2.5 7B. Qwen2.5-Math-
F OV ER-PRMs are trained on F OV ER-40K, so the                      7B-PRM800K (Zheng et al., 2025) and Qwen2.5-
input format has the same format as the training                     Math-PRM-7B (Zhang et al., 2025) are supported
data. The only difference is that we replace all                     by vLLM (Kwon et al., 2023). We follow the input
step-level labels with “correct” in the input. This                  format specified in their respective model descrip-
preprocessing allows us to provide the whole input                   tions and adopt the reward modeling in vLLM.3
once to get the step-level predictions for all steps.                For Qwen2.5-7B-Skywork-PRM (He et al., 2024),
The following is an example input for GSM8K.                         we use a code provided by the authors.4
 [
     {                                                               E.2   Training Settings
         'role': 'user',
         'content': '** Problem **                                   This section provides details of the training settings
            Alice is 7 years older than Beth, who is 5 years older
           ,→ than Erica. What is the difference between the ages    for our F OV ER-PRMs.
           ,→ of Alice and Erica, if Erica is 30 years old?
                                                                     Balanced labels. The last steps of the solutions
           ** Task **
           Your task is to evaluate the accuracy of each step in     in F OV ER-40K includes balanced step-level error
          ,→ the provided solution to the above question. For
          ,→ each step, respond with "correct" if the reasoning
                                                                     labels of 50% of “correct” and “incorrect” labels.
          ,→ is logically valid and mathematically sound, or if      Then, we can perform training on the balanced
          ,→ the step is a general statement or transition that
          ,→ does not contain reasoning. Respond with                label by setting mask_history: True in LLaMA-
          ,→ "incorrect" if the step includes any errors or
          ,→ flawed logic.
                                                                     Factory, which configures the model to use only
                                                                     the last step of each conversation during training.
           ** Sotluion **
           Since Erica is 30 years old, and Beth is 5 years older    Training parameters. We fine-tune all model pa-
          ,→ than Erica, Beth is 30 + 5 = 35 years old.'
      },                                                             rameters and do not use parameter-efficient tech-
      {'role': 'assistant', 'content': 'correct'},
      {'role': 'user', 'content': 'Alice is 7 years older than       niques. We use the AdamW optimizer (Loshchilov
     ,→ Beth, who is 35 years old. '},
      {'role': 'assistant', 'content': 'correct'},
                                                                     and Hutter, 2019) and select the learning rate based
      {'role': 'user', 'content': 'So, Alice is 35 + 7 = 42 years    on the average Best-of-K performance on the val-
     ,→ old.'},
      {'role': 'assistant', 'content': 'correct'},                   idation tasks: Orca-Math (Mitra et al., 2024) and
      {'role': 'user', 'content': "The difference between Alice's
     ,→ age and Erica's age is 42 - 30 = 12 years."},                two tasks in BBH (Suzgun et al., 2023) (Logical De-
      {'role': 'assistant', 'content': 'correct'},                   duction (three objects) and Boolean Expressions).
      {'role': 'user', 'content': 'Therefore, the answer (arabic
     ,→ numerals) is 12.'},                                          We evaluate models trained with the learning rate
      {'role': 'assistant', 'content': 'correct'}
 ]                                                                   1e-6, 2e-6, 5e-6, and 1e-5, and select the model
                                                                     with the best average performance on the valida-
   Next, we describe the postprocessing for                          tion tasks. We use the parameters in Table 9 in all
F OV ER-PRMs and the baseline LLM-based PRMs.                        models, and we did not conduct hyperparameter
                                                                     tuning for these parameters. Please refer to the
Extracting logits. Since we use causal LLMs as
                                                                     configuration files in our code for further details.
PRMs, we extract the model’s predictions for the to-
kens immediately preceding the dummy step-level                      E.3   Evaluation Settings of Best-of-K
labels (e.g., “correct”) in the input.
Computing step-level scores. At each identified                      Benchmarks. Table 10 shows sources of reasoning
position, we extract the logits corresponding to the                 benchmarks evaluated in Best-of-K in Section 4.
tokens “correct” and “incorrect”. We then apply                      Initial generation prompts. Table 11 shows de-
the softmax function over these two logits to com-                      2
                                                                          https://github.com/RLHFlow/
pute the probability assigned to “correct”. This                     RLHF-Reward-Modeling/tree/main/math-rm
probability serves as the step-level score.                             3
                                                                          https://docs.vllm.ai/en/latest/models/
                                                                     pooling_models.html
PRMs based on Llama 3.1 8B. In RLHFlow-                                 4
                                                                          https://github.com/SkyworkAI/
Llama3.1-8B-DeepSeek and RLHFlow-Llama3.1-                           skywork-o1-prm-inference
  Parameter                                  Value      et al., 2023) to generate reward scores.7
  Number of Epochs                           1          Software libraries. For inference, we use
  Batch size                                 32
  Learning Rate Warm up and Decay Strategy   Linear
                                                        vLLM (Kwon et al., 2023) for accelerating
  Learning Rate Warm up Ratio                0.5        LLM inference. For training, we use LLaMA-
                                                        Factory (Zheng et al., 2024) for fine-tuning PRMs.
Table 9: Hyperparameters for training on F OV ER-40K
                                                        F   Ethical Considerations

tailed settings of generating K = 7 responses for       Social impacts. This research does not involve
the Best-of-K evaluation in Section 4. We create        human subjects or private data. This paper pro-
new few-shot examples or modify few-shot demon-         poses a method for improving PRMs, which detect
strations used in prior work to enhance the quality     mistakes in LLM responses. We do not expect any
and to simplify the post-processing procedure. For      harmful impact.
example, we add line breaks between reasoning           Dataset. Our dataset, F OV ER-40K, is created from
steps in all tasks. An example prompt for GSM8K         formal verification tools and logic and mathemati-
is provided in Appendix C.1.1. Please also refer to     cal reasoning datasets. We do not expect that our
our code for further details.                           dataset includes information that uniquely identi-
                                                        fies individual people or offensive content.
E.4   Computational Resources                           The use of Large Language Models. In paper
We use four NVIDIA A100 SXM4 80GB GPUs                  writing, we used LLMs to polish writing. We used
for training and inference. Training each 8B-class      ChatGPT-5 via OpenAI’s web interface.
model on our dataset takes approximately one hour
                                                        G Reproducibility Statement and License
using our training data, F OV ER-40K. Evaluation
takes considerably more time because the Best-of-       The datasets, models, and code are provided
K evaluation requires multiple candidate solutions,     at https://github.com/psunlpgroup/FoVer.
and reproducing all the evaluation in this paper will      We release our dataset under Creative Commons
take approximately three days.                          Attribution 4.0 International and our code under
   Verification using Z3 and Isabelle does not re-      Apache License 2.0. Our dataset and code are
quire GPUs and can be run in parallel on CPU-only       based on the following resources. We consider
servers, enabling efficient and scalable PRM train-     our license to be (one-way) compatible with all
ing data creation. On average, in a single process,     licenses listed below.
Z3 verifies all datasets in less than 10 minutes for    Datasets. F OV ER-40K is based on the following
the formal logic task, and Isabelle verifies each       datasets.
step in approximately 3 seconds for the formal the-
orem proving tasks. For annotation, we run one          • FLDx2 (2024): CC BY 4.08
Z3 process for formal logic and 40 parallel Isabelle    • GSM8K (2021): MIT9
processes for formal theorem proving on AMD
EPYC 7763 64-core processors.                           • MetaMathQA (2024): MIT10
                                                        • Big-Math (2025): Apache License 2.011
E.5   Model Access and Software Libraries
                                                        Code and packages. Our code is partially based
LLMs. We use LLMs from Hugging Face Hub. We             on the following resources.
use meta-llama/Llama-3.1-8B-Instruct and
Qwen/Qwen2.5-7B-Instruct as base models for
                                                           7
                                                             https://docs.vllm.ai/en/latest/
                                                        models/supported_models.html#
our PRMs. We also use these models to gener-            reward-modeling-task-reward
ate initial responses used in creating F OV ER-40K,        8
                                                             https://github.com/hitachi-nlp/FLD-corpus/
and also for generating K = 7 responses in the          blob/neurips_2025/LICENSE
                                                           9
                                                             https://github.com/openai/grade-school-math/
Best-of-K evaluation (§4).                              blob/master/LICENSE
Existing PRMs. Details for the PRMs evaluated in
                                                          10
                                                             https://huggingface.co/datasets/meta-math/
                                                        MetaMathQA/blob/main/README.md
Section 4 are listed in Table 12. We acquire these        11
                                                             https://huggingface.co/datasets/SynthLabsAI/
models at Hugging Face Hub and use vLLM (Kwon           Big-Math-RL-Verified/blob/main/README.md
                              Dataset                                          Source
                           GSM8K                         https://huggingface.co/datasets/openai/gsm8k
                            MATH                               https://github.com/hendrycks/math
                          AQuA-RAT                    https://huggingface.co/datasets/deepmind/aqua_rat
                        AIME (2016-2024)         https://huggingface.co/datasets/di-zhang-fdu/AIME_1983_2024
                              FOLIO                        https://huggingface.co/datasets/yale-nlp/FOLIO
                             LogicNLI                    https://huggingface.co/datasets/tasksource/LogicNLI
                              ANLI                          https://huggingface.co/datasets/facebook/anli
                              HANS                                https://github.com/tommccoy1/hans
                              MMLU              https://huggingface.co/datasets/sam-paech/mmlu-pro-nomath-sml
                               BBH               https://github.com/suzgunmirac/BIG-Bench-Hard/tree/main/bbh


                       Table 10: Reasoning benchmarks evaluated in the Best-of-K experiments.

        Dataset         Few-shot Examples for Initial Generation                                 Answer Matching

        GSM8K                  Kojima et al. (2022) 5                          Exact match after extraction and conversion to integer
        MATH             Lewkowycz et al. (2022, Appendix D.2)                        Lewkowycz et al. (2022, Appendix G)
       AQuA-RAT                 Made by us (3-shot)                                        Exact match after extraction
         AIME                   Made by us (3-shot)                            Exact match after extraction and conversion to integer
        FOLIO                     Made by us (2-shot)                                      Exact match after extraction
       LogicNLI                   Made by us (3-shot)                                      Exact match after extraction
        ANLI                      Made by us (3-shot)                                      Exact match after extraction
        HANS                      Made by us (2-shot)                                      Exact match after extraction
        MMLU                      Made by us (4-shot)                                      Exact match after extraction

         BBH                     Suzgun et al. (2023)6                                     Exact match after extraction


                             Table 11: Detailed settings for Best-of-K downstream evaluation

                      PRMs                                         Source                   Base Datasets         Training Data Creation
       RLHFlow-Llama3.1-8B-DeepSeek (2024)     RLHFlow/Llama3.1-8B-PRM-Deepseek-Data       GSM8K, MATH            Math-Shepherd (2024)
        RLHFlow-Llama3.1-8B-Mistral (2024)      RLHFlow/Llama3.1-8B-PRM-Mistral-Data       GSM8K, MATH            Math-Shepherd (2024)
        Qwen2.5-Math-7B-PRM800K (2025)             Qwen/Qwen2.5-Math-7B-PRM800K                 MATH                Human annotation
                                                                                                                 Math-Shepherd (2024) &
           Qwen2.5-Math-PRM-7B (2025)                    Qwen/Qwen2.5-Math-PRM-7B            Private Data
                                                                                                                    LLM-as-a-Judge
         Qwen2.5-7B-Skywork-PRM (2024)       Skywork/Skywork-o1-Open-PRM-Qwen-2.5-7B            Hidden                    Hidden


                                             Table 12: PRMs we evaluate in Section 4.


• FLD (2024): Apache License 2.012
• Isabelle: BSD-style regulations13
• Neural theorem proving tutorial (2023): MIT14
• DTV (2024): MIT15




  12
     https://github.com/hitachi-nlp/FLD/blob/
neurips_2025/LICENSE
  13
     https://isabelle.in.tum.de/
  14
     https://github.com/wellecks/ntptutorial/blob/
main/LICENSE
  15
     https://github.com/jinpz/dtv/blob/main/
LICENSE
