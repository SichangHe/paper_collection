                                        SpecCoder: Specification-Aware Code Generation with
                                           Curriculum Dual-Task Reinforcement Learning
                                        Yixuan Lia , Mingxuan Huanga , Jiajing Wanga , Weidong Yanga,∗, Xinyi Liua , Ben
                                                                      Feib , Lipeng Maa,∗
                                                   a School of Computer Science, Fudan University, Shanghai, 200438, China
arXiv:2609.06041v1 [cs.SE] 5 Sep 2026




                                         b Department of Information Engineering, The Chinese University of Hong Kong, Hong Kong,

                                                                               999077, China




                                        Abstract
                                            Large language models (LLMs) have made substantial progress in code gen-
                                        eration but still struggle with challenging programming tasks that require under-
                                        standing rich natural language requirements. These requirements often specify
                                        problem goals, input/output formats, constraints, examples, edge cases, and im-
                                        plicit assumptions. Overlooking even one of them may produce executable but
                                        functionally incorrect code. Existing training-free methods mainly rely on prompt-
                                        ing or agent-based workflows, while training-based methods typically optimize
                                        final code outputs using supervised or execution-based signals. However, exist-
                                        ing approaches provide limited supervision for learning the intermediate mapping
                                        from raw requirements to structured specification analyses and for grounding such
                                        analyses in concrete implementation behavior. Consequently, models may omit
                                        critical constraints when interpreting raw requirements, and even when an explicit
                                        specification analysis is produced, the resulting implementation may fail to reflect
                                        it consistently. Motivated by this gap, we propose SpecCoder, a specification-
                                        aware two-stage training framework for code generation. SpecCoder first employs
                                        specification-guided Supervised Fine-Tuning (SFT) to train LLMs to derive struc-
                                        tured specification analyses and generate code conditioned on them. It then intro-
                                        duces curriculum dual-task Group Relative Policy Optimization (GRPO), which
                                        jointly optimizes specification-guided generation and discrimination to encour-

                                           ∗ Corresponding authors

                                           Email addresses: yxli24@m.fudan.edu.cn (Yixuan Li),
                                        24307130121@m.fudan.edu.cn (Mingxuan Huang), 25213050375@m.fudan.edu.cn (Jiajing
                                        Wang), wdyang@fudan.edu.cn (Weidong Yang), liuxiny24@m.fudan.edu.cn (Xinyi Liu),
                                        benfei@cuhk.edu.hk (Ben Fei), lpma21@m.fudan.edu.cn (Lipeng Ma)
age stronger correspondence between structured specification analyses and code
behavior. Experiments on APPS, CodeContests, and xCodeEval demonstrate the
effectiveness of specification-aware training, with SpecCoder consistently improv-
ing both standalone code generation and the performance of agent-based work-
flows. Additional evaluations on BigCodeBench-Hard and ClassEval, together
with human evaluation and specification perturbation studies, further support the
effectiveness of structured specification analyses and their role in guiding code
generation and discrimination.
Keywords: Code Generation, Specification-Aware Reasoning, Reinforcement
Learning, Large Language Models


1. Introduction
    Code generation is a fundamental research problem in software engineering.
Large language models (LLMs) have made substantial progress and perform well
on widely used benchmarks such as HumanEval [1] and MBPP [2]. However,
their performance remains limited on more challenging programming benchmarks,
such as APPS [3], CodeContests [4], and xCodeEval [5]. One key difference
is that benchmarks such as HumanEval and MBPP usually provide relatively
simple prompts, such as a function signature or a short instruction, whereas more
challenging tasks often require LLMs to reason over richer raw natural language
requirements. These requirements specify the intended code behavior and may
include problem goals, input and output formats, constraints, examples, edge cases,
and implicit assumptions. Therefore, solving such specification-rich tasks requires
LLMs not only to generate syntactically valid or executable code, but also to form
an explicit understanding of the requirements and ensure that the implementation
satisfies the intended functionality and constraints.
    Existing methods for improving LLM-based code generation can be broadly
categorized into training-free and training-based approaches. Training-free
methods can be further divided into prompt-based methods and agent-based work-
flows. Prompt-based methods [6, 7, 8, 9] guide the generation process through
carefully designed instructions for planning, reasoning, or output repair. They
are lightweight and easy to deploy, but their effectiveness is often limited be-
cause requirement understanding remains implicit and is not directly optimized.
Agent-based methods [10, 11, 12, 13] decompose code generation into multi-step
or multi-role workflows involving requirement analyses, implementation, testing,
and revision. Although effective, these methods typically require repeated inter-

                                        2
actions and iterative execution, leading to substantial inference cost. More impor-
tantly, both prompt-based and agent-based methods mainly improve how LLMs
use prompts or external workflows at inference time, rather than enhancing their
intrinsic ability to align generated code with raw requirements. Training-based
methods [14, 15, 16, 17] optimize LLMs through reinforcement learning or pref-
erence optimization, primarily using execution-based feedback from test cases or
preference signals. However, such feedback often provides sparse reward signals
and does not explicitly supervise how requirements are understood and trans-
lated into structured specification analyses. Consequently, existing training-based
methods provide limited supervision for learning to derive structured specification
analyses from raw requirements and use them to guide code generation.
    Recent studies [18, 19] show that code generation failures often stem from
misunderstanding raw requirements. When requirements such as key concepts,
input and output constraints, or edge cases are overlooked, generated code can
easily deviate from the intended code behavior. However, existing specification-
alignment methods [20, 21] mainly perform alignment, repair, or verification
during inference, rather than improving the intrinsic specification-alignment abil-
ity of LLMs through training. A natural direction is therefore to train LLMs with
explicit specification-aware reasoning capabilities. This direction presents two
challenges. First, building an accurate and structured specification-level under-
standing from raw requirements remains challenging. For complex programming
tasks, requirement understanding should be made explicit before implementation,
as implicit contextual reasoning alone may cause LLMs to omit, misinterpret, or
weaken key constraints. Second, generated code is not always well aligned with
the specification-level understanding. Even when reasonable structured specifica-
tion analyses are produced, the final implementation may still ignore, simplify, or
contradict them, creating a gap between the stated understanding and actual code
behavior. Moreover, execution-based feedback typically provides only outcome-
level signals [22, 23, 16], indicating whether code passes tests but not which
requirement constraints are satisfied or violated. As a result, such feedback pro-
vides limited guidance for training models to follow structured specifications or
compare candidate implementations according to specification satisfaction.
    To address these challenges, we propose SpecCoder, a specification-aware
two-stage training framework for code generation. SpecCoder first conducts
specification-guided Supervised Fine-Tuning (SFT), enabling the LLM to derive
structured specification analyses from raw requirements and generate code con-
ditioned on them. SpecCoder then applies curriculum dual-task Group Relative
Policy Optimization (GRPO). In this stage, the generation task further optimizes

                                        3
specification-guided code generation, while the discrimination task trains the LLM
to select, from paired candidate implementations, the one that better satisfies the
raw requirement under the shared structured specification analysis. For both
GRPO tasks, SpecCoder categorizes training samples into Easy, Medium, and
Hard subsets and organizes them into a three-phase curriculum. The curriculum
first establishes basic associations between structured specification analyses and
code behavior using easier samples, then addresses harder cases requiring com-
plex requirement analysis and implementation comparison, and finally mixes all
difficulty levels to consolidate learned behaviors and mitigate forgetting. By com-
bining these complementary generation and discrimination objectives, SpecCoder
better aligns structured specification analyses with code behavior.
     We evaluate SpecCoder as a standalone code generator and as the backbone
of representative agent-based code generation frameworks. In the standalone set-
ting, SpecCoder achieves strong performance on the in-distribution (ID) APPS and
CodeContests benchmarks, reaching Pass@1/AvgPassRatio scores of 0.186/0.346
and 0.091/0.207, respectively. It achieves the best results among training-free
prompting baselines and is competitive with or superior to training-based base-
lines across almost all metrics. On the out-of-distribution (OOD) xCodeEval
benchmark, SpecCoder obtains a Pass@1 of 0.147 and an AvgPassRatio of 0.324,
outperforming all compared training-free prompting and training-based baselines.
When used as the backbone of agent-based frameworks, SpecCoder consistently
improves all evaluated frameworks across APPS, CodeContests, and xCodeEval,
with gains of up to 11.3 percentage points in Pass@1 and 13.2 percentage points in
AvgPassRatio over the base model. These results demonstrate that SpecCoder im-
proves both standalone code generation and its use as a backbone for agent-based
workflows. Further analyses show that structured specification analyses provide
useful intermediate guidance for code synthesis.
     This paper makes the following contributions.

    • We propose SpecCoder, a specification-aware two-stage training framework
      that combines specification-guided SFT with curriculum dual-task GRPO
      to explicitly learn structured specification analyses from raw requirements
      and use them to guide code generation.
    • We introduce structured specification analyses as a shared intermediate rep-
      resentation for specification-guided generation and implementation discrim-
      ination, allowing the two training objectives to jointly relate requirement
      understanding to concrete code behavior.

                                        4
    • We conduct extensive evaluations of SpecCoder in standalone and agent-
      based settings across ID and OOD benchmarks. Additional analyses on
      intermediate representations, specification dependency, and realistic pro-
      gramming tasks further demonstrate its effectiveness and applicability.


2. Related Work
2.1. Training-Free Methods for LLM-Based Code Generation
    Training-free methods improve LLM-based code generation without updating
model parameters and can be broadly divided into prompt-based methods and
agent-based workflows. Prompt-based methods mainly enhance code generation
through structured reasoning and iterative refinement during inference. Chain-of-
Thought prompting [24] shows that intermediate reasoning can improve LLM per-
formance on complex tasks, motivating structured reasoning approaches for code
generation. Self-Debug [25, 20] and Self-Edit [7] iteratively repair generated code
based on execution feedback, whereas later methods including Self-Planning [8],
SCoT [26], Program of Thoughts [27], ArchCode [28], and 𝜇FiX [21] introduce
structured pre-generation reasoning, explicitly incorporate software requirements,
or integrate specification understanding with execution-based refinement. De-
spite their training-free nature, these methods remain limited because manually
designed prompts are often less robust, and LLMs may struggle to consistently
follow complex instructions or retain critical requirement details.
    Agent-based methods further improve complex code generation by decompos-
ing the development process into multi-step or multi-role workflows. Frameworks
such as MetaGPT [10] and FlowGen [29] simulate software development pro-
cedures through cooperative agents, while Reflexion [30] refines model behavior
through verbal feedback. Recent systems such as Specine [18] and REA-Coder [19]
further address requirement misunderstanding and specification alignment during
inference. These methods can better handle complex requirements by introducing
explicit analysis, feedback, or revision steps, but they usually require repeated
interactions, tool calls, or iterative execution, leading to higher inference cost.
Overall, these prompt-based and agent-based methods treat requirement analysis
as an auxiliary inference-time procedure, without directly optimizing either the
completeness of the derived specification or its consistency with the generated
implementation. Consequently, a model may produce a plausible requirement
analysis while still overlooking critical constraints or generating code that contra-
dicts that analysis.

                                         5
2.2. Training-Based Methods for LLM-Based Code Generation
    Recent training-based methods for LLM-based code generation can be broadly
categorized into feedback-based optimization and training-strategy optimization.
Feedback-driven approaches like CodeRL [22], CodeRL+ [17], CodeDPO [14],
and CodePRM [16] enhance code correctness using execution feedback, preference
signals, or execution-derived process supervision. Meanwhile, training-strategy
optimization methods improve learning efficiency and exploration through pro-
gressive task organization and capability decomposition. For instance, Step-
Coder [31] incrementally increases code-completion difficulty to optimize exe-
cuted segments. RECRL [32] integrates test-driven difficulty estimation with
adaptive curriculum sampling and requirement rewriting. Similarly, FixAudit [33]
sequentially trains models on execution reasoning, code repair, and defect-test
generation. These strategies improve exploration, training efficiency, or iterative
code refinement.
    Despite these advancements, existing learning signals mainly focus on final
implementation outcomes, with limited supervision for accurately understanding
raw requirements. Consequently, models may omit essential constraints during
requirement interpretation, and their final code may fail to consistently reflect
the generated intermediate analyses. SpecCoder explicitly addresses these two
interconnected gaps through a two-stage framework. It first uses specification-
guided SFT to learn structured specification analyses and specification-conditioned
generation. Curriculum dual-task GRPO then jointly optimizes generation and
discrimination to strengthen the correspondence between requirement analysis
and code behavior.

3. Problem Formulation
    SpecCoder trains LLMs to derive structured specification analyses from raw
requirements and generate code aligned with these analyses. We formulate
this objective as two learning tasks: specification-guided code generation and
specification-guided code discrimination. Let P, S, and C denote the spaces of
raw requirements, structured specification analyses, and candidate implementa-
tions, respectively. For each raw requirement 𝑝 ∈ P, let T𝑝 be its test suite. Given
a candidate implementation 𝑐 ∈ C, we define 𝑓 (𝑐, T𝑝 ) ∈ [0, 1] as the fraction
of test cases passed by 𝑐, where 𝑓 (𝑐, T𝑝 ) = 1 means that 𝑐 passes all available
tests. We use T𝑝 as an executable proxy for observable functional correctness
under available tests. Since available tests may not cover all semantic constraints,


                                         6
𝑓 (𝑐, T𝑝 ) is treated as an approximate training and evaluation signal rather than a
complete measure of requirement satisfaction.

3.1. Specification-Guided Code Generation Task
    Directly generating code from raw requirements is challenging because LLMs
may overlook key goals, constraints, edge cases, or implicit assumptions. To make
requirement analysis explicit, SpecCoder generates a structured output in which
a structured specification analysis 𝑠ˆ is produced before the code 𝑐,ˆ so that the
implementation is guided by an explicit intermediate analysis of the requirement.
Formally, let 𝜋𝜃 denote the LLM policy parameterized by 𝜃. The generation
process is defined as:
                                ( 𝑠ˆ, 𝑐)
                                      ˆ ∼ 𝜋𝜃 (· | 𝑝),                          (1)
where 𝑠ˆ serves as an intermediate specification-level representation rather than a
unique ground-truth analysis. The output is structured so that 𝑠ˆ is generated before
ˆ making code generation conditioned on the raw requirement 𝑝 and the preceding
𝑐,
specification analysis 𝑠ˆ in the autoregressive context.

3.2. Specification-Guided Code Discrimination Task
    To strengthen the alignment between structured specification analyses and code
behavior, we introduce a specification-guided discrimination task in which the
LLM compares two candidate implementations under the same raw requirement
and structured specification analysis. For each pair of candidate implementations,
we construct (𝑐+ , 𝑐− ) such that:

                                 𝑓 (𝑐+ , T𝑝 ) > 𝑓 (𝑐− , T𝑝 ),                          (2)

where 𝑐+ achieves a higher test pass rate than 𝑐− , indicating that it better satisfies the
requirements under the available tests. To reduce position bias, the two candidates
are randomly ordered as (𝑐 𝐴 , 𝑐 𝐵 ), and the LLM analyses them with respect to the
shared specification to output a binary decision 𝑦 ∈ {𝐴, 𝐵}.

4. Methodology
    Figure 1 illustrates the overall pipeline of SpecCoder, which contains one data
construction stage and two training stages. SpecCoder uses structured specifica-
tion analyses as an intermediate interface between raw requirements and candidate
implementations. In the data construction stage, we build a specification-guided


                                             7
generation dataset Dgen with tuples ( 𝑝, 𝑠, 𝑐) and a specification-guided discrimi-
nation dataset Ddisc with tuples ( 𝑝, 𝑠, 𝑐 𝐴 , 𝑐 𝐵 , 𝑦), where 𝑦 indicates the candidate
implementation with the higher test pass rate under the shared raw requirement and
structured specification analysis. In the first training stage, SpecCoder performs
specification-guided SFT on Dgen to initialize the LLM’s ability to derive struc-
tured specification analyses and generate code conditioned on them. In the second
training stage, SpecCoder applies curriculum dual-task GRPO to jointly optimize
specification-guided generation and discrimination, further aligning specification-
level understanding with code behavior. The following sections describe data
construction in Section 4.1, specification-guided SFT in Section 4.2.1, and cur-
riculum dual-task GRPO in Section 4.2.2.

4.1. Data Construction Pipeline
    As shown in Stage 1 of Figure 1, the data construction pipeline builds two
datasets, namely the specification-guided code generation dataset Dgen and the
specification-guided code discrimination dataset Ddisc . Both datasets are con-
structed from APPS and CodeContests. For APPS, we use the original training set
for data construction and further split the original test set into two non-overlapping
subsets: one used only for additional data construction and the other reserved for
evaluation, thereby preventing overlap between construction and evaluation. In
contrast, CodeContests uses only its complete training set.

4.1.1. Specification-Guided Code Generation Dataset Dgen
    The dataset Dgen provides verified triplets for specification-guided code gen-
eration training and is constructed through multi-path generation and bidirectional
verification.
    Multi-Path Generation. For each raw requirement 𝑝, we use GPT-4o (gpt-
4o-2024-08-06) with a sampling temperature of 𝜏 = 0.7. By independently
querying the model 𝑀 times, we generate a set of structured specification analy-
ses 𝑠 (1) , 𝑠 (2) , . . . , 𝑠 (𝑀) , where 𝑀 = 3 in our implementation. Each specification
analysis follows a seven-dimensional structure consisting of problem background,
functional requirements, input requirements, output requirements, test cases, exter-
nal dependencies, and additional notes, as summarized in Table 1. The structure
is adapted from common software requirement specification practices [34, 35]
and tailored to programming tasks, enabling raw requirements to be organized
into explicit specification-level analyses for code generation. For each generated
structured specification analysis 𝑠 (𝑚) , GPT-4o further generates a corresponding


                                           8
   Stage 1 Data Construction                                      Stage 2 Specification-Guided SFT
         Raw Requirement                                                                                           Structured Output:
                                                                            𝓓𝒈𝒆𝒏
     (from APPS, CodeContests)            Base                                                          SFT        • <ANALYZE> specification
                                                                                                                     analysis </ANALYZE>
                                          Model                    SFT                                 Model       • <CODE> code snippet </CODE>
                        GPT
  Spec1   Code1        Forward
                      Verification
                                                                 Stage 3 Curriculum Dual-Task GRPO                                        E: Easy
                      Backward                                                                                                            M: Medium
                      Verification
                                          SFT Model                                                                                       H: Hard
                  …                                                          Phase 1 Initial Alignment
 Specm    Codem        Forward                                               E            E               E          E
                      Verification                                    𝓓𝒈𝒆𝒏           𝓓𝒅𝒊𝒔𝒄         𝓓𝒈𝒆𝒏         𝓓𝒅𝒊𝒔𝒄
                      Backward
                      Verification
                                                                       Phase 2 Difficulty Adaptation
                                                                             M            M               H           H
                                                                      𝓓𝒈𝒆𝒏           𝓓𝒅𝒊𝒔𝒄         𝓓𝒈𝒆𝒏          𝓓𝒅𝒊𝒔𝒄
                     Dataset
                      𝓓𝒈𝒆𝒏
                                                                            Phase 3 Full Consolidation
     Specification           Raw                                        E         E    M     M    H     H
      Analysis (s)      Requirement (p)                          𝓓𝒈𝒆𝒏        𝓓𝒅𝒊𝒔𝒄 𝓓𝒈𝒆𝒏 𝓓𝒅𝒊𝒔𝒄 𝓓𝒈𝒆𝒏 𝓓𝒅𝒊𝒔𝒄
  Buggy Code                              Final Model

                                                                                    Inference
                                          Raw Requirement                    Specification Analysis                           Code
                                          Write a method to             •        Problem Background: …        def padovan(n: int) -> int:
                                          return the i-th                                                        # Handle base cases directly
                                                                        •        Functional Requirements: …      if n in (0, 1, 2):
                                          Padovan number
                                                                        •        Input Requirements: …               return 1
                                          where                                                                  # Space-optimized dynamic programming
                     Dataset              P(0)=P(1)=P(2)=1 andSpecCoder •        Output Requirements: …
                                                                        •        Test Cases: …                   p0, p1, p2 = 1, 1, 1
                      𝓓𝒅𝒊𝒔𝒄               P(n)=P(n-2)+P(n-3)…                                                    for _ in range(3, n + 1):
                                                                        •        External Dependencies: …            p0, p1, p2 = p1, p2, p0 + p1
                                          Better Understand & Generate  •        Additional Notes: …             return p2




Figure 1: Overview of the SpecCoder pipeline. The methodology consists of a data construction
stage followed by two training stages. Stage 1 constructs the specification-guided generation dataset
Dgen through forward execution-based verification and backward semantic verification, and builds
the specification-guided discrimination dataset Ddisc from paired candidate implementations under
shared problems and specification analyses. Stage 2 performs supervised fine-tuning on Dgen to
teach the LLM to derive structured specification analyses and generate code conditioned on them.
Stage 3 applies curriculum dual-task GRPO to jointly optimize specification-guided generation
and discrimination, progressively moving from easier samples to harder cases and then to a full
mixture for consolidation. During inference, the trained model first analyses the raw requirement
into a structured specification analysis and then uses it to guide final code generation.


candidate implementation 𝑐 (𝑚) conditioned on both 𝑝 and 𝑠 (𝑚) , forming a candidate
triplet ⟨𝑝, 𝑠 (𝑚) , 𝑐 (𝑚) ⟩.
    Bidirectional Verification. For the candidate triplets generated above, we ap-
ply two verification steps to ensure both executable correctness and specification
consistency. Forward verification evaluates functional correctness by executing
each candidate implementation against the available test suite T𝑝 . Only triplets
whose candidate implementation satisfies 𝑓 (𝑐 (𝑚) , T𝑝 ) = 1 are retained. Back-
ward verification further examines whether the structured specification analysis is
consistent with the raw requirement and whether the generated code follows the


                                                                  9
specification analysis. Although a candidate implementation may pass all avail-
able tests, it may still only partially reflect the specification analysis or rely on
assumptions not explicitly captured by it. To reduce this risk, we use DeepSeek-
V3-0324 [36] as an evaluator to assess each forward-verified triplet ⟨𝑝, 𝑠 (𝑚) , 𝑐 (𝑚) ⟩.
For space considerations, we evaluate each triplet from three aspects: semantic
completeness, algorithmic traceability, and expression clarity, with detailed crite-
ria provided in Appendix A.2. Triplets satisfying the backward verification criteria
are retained. If multiple verified triplets remain for a problem, we randomly se-
lect one, while problems without any verified triplet are entirely discarded. The
resulting triplets form the final specification-guided code generation dataset Dgen .

   Dimension                            Objective and Description
   Problem            Summarizes the task context, overall objective, and necessary
   Background               background to clarify the purpose of the problem.
   Functional        Defines the required program behavior, including the problem
   Requirements               objective and key operations to be performed.
   Input             Details the expected input data types, structure, format, ranges,
   Requirements                          and validation constraints.
   Output             Defines the expected output data type, format, and conditions
   Requirements                   that the generated output must satisfy.
   Test               Extracts available examples or test cases to illustrate expected
   Cases                            behavior and boundary conditions.
   External          Identifies required external libraries, frameworks, or APIs and
   Dependencies                     their usage constraints. (Optional)
   Additional            Captures edge cases, implicit assumptions, exceptional
   Notes             conditions, and other constraints not covered above. (Optional)

                  Table 1: Dimensions of Structured Specification Analyses.


4.1.2. Specification-Guided Code Discrimination Dataset Ddisc
    The dataset Ddisc provides training instances for specification-guided code dis-
crimination. For each verified triplet ⟨𝑝, 𝑠, 𝑐⟩ in Dgen , we use the raw requirement
𝑝 and structured specification analysis 𝑠 as the shared context and prompt Qwen2.5-
Coder-32B-Instruct to sample ten candidate implementations conditioned on them.
Each candidate is executed on T𝑝 to obtain its test pass rate, and candidate im-
plementations with syntax errors or compilation failures are discarded. From the
remaining candidates, we construct pairwise samples with different pass rates.
Each pair is denoted as (𝑐+ , 𝑐− ), where 𝑓 (𝑐+ , T𝑝 ) > 𝑓 (𝑐− , T𝑝 ). During training,

                                             10
the two candidate implementations are randomly ordered as (𝑐 𝐴 , 𝑐 𝐵 ) to reduce
position bias, forming an instance ( 𝑝, 𝑠, 𝑐 𝐴 , 𝑐 𝐵 , 𝑦), where 𝑦 labels the candidate
implementation with the higher test pass rate after random ordering.
     To support curriculum learning, each discrimination sample is assigned a
difficulty label according to the pass-rate gap Δ between the higher-performing
and lower-performing candidates. (1) Easy samples correspond to Δ ∈ (0.6, 1.0]
where the programs differ substantially in their test pass rates. (2) Medium
samples feature Δ ∈ (0.3, 0.6] representing a moderate gap that often indicates
partial functional differences. (3) Hard samples involve Δ ∈ (0.0, 0.3] with a
small pass-rate gap requiring much more fine-grained comparison. These difficulty
labels subsequently guide the curriculum reinforcement learning strategy.

4.2. Two-Stage Training Paradigm
    After data construction, SpecCoder proceeds with two-stage training, corre-
sponding to Stage 2 and Stage 3 in Figure 1. The first stage warm-starts the
LLM through specification-guided SFT, and the second stage further improves
both generation and discrimination through curriculum dual-task GRPO. The fol-
lowing subsections detail these two stages.

4.2.1. Specification-Guided SFT
    As the first training stage, specification-guided SFT initializes the LLM’s
ability to derive structured specification analyses from raw requirements and use
them to guide code generation. For each training tuple ⟨𝑝𝑖 , 𝑠𝑖 , 𝑐𝑖 ⟩ ∈ Dgen , we
construct an autoregressive training sequence 𝑋𝑖 with an input part and a target
part. The input part contains the raw requirement 𝑝𝑖 , enclosed by <REQ> and
</REQ>. The target part contains the structured specification analysis 𝑠𝑖 , enclosed
by <ANALYZE> and </ANALYZE>, followed by the implementation 𝑐𝑖 , enclosed
by <CODE> and </CODE>. Under this format, the LLM learns to first produce a
structured specification analysis and then generate code conditioned on both the
raw requirement and the generated analysis. We optimize the LLM by minimizing
the following loss:
                                                             |𝑋𝑖 |
                  1              ∑︁                   1      ∑︁
       LSFT = −                                  Í|𝑋𝑖 |              𝑚𝑖, 𝑗 log 𝜋𝜃 (𝑋𝑖, 𝑗 | 𝑋𝑖,< 𝑗 ),   (3)
                |Dgen |
                          ⟨𝑝 𝑖 ,𝑠𝑖 ,𝑐 𝑖 ⟩∈Dgen     𝑗=1 𝑚 𝑖, 𝑗 𝑗=1

Here, 𝑋𝑖, 𝑗 denotes the 𝑗-th token of 𝑋𝑖 , and 𝑋𝑖,< 𝑗 denotes its preceding context.
The mask 𝑚𝑖, 𝑗 ∈ {0, 1} determines whether each token contributes to the loss.


                                                    11
We set 𝑚𝑖, 𝑗 = 0 for input tokens corresponding to the raw requirement and its
delimiters, and set 𝑚𝑖, 𝑗 = 1 for target tokens corresponding to the structured
specification analysis, the implementation, and their target-side delimiters. Thus,
the loss is applied only to the model-generated part of the sequence. The resulting
SFT policy provides a stable initialization for the subsequent curriculum dual-task
GRPO stage, where the LLM is further optimized with task-specific reward signals.

4.2.2. Curriculum Dual-Task GRPO
    After specification-guided SFT, the LLM learns to follow the analysis-before-
code generation format. However, SFT alone provides limited optimization for
strengthening the correspondence between structured specifications and code be-
havior across generation and implementation discrimination. Therefore, Spec-
Coder applies curriculum dual-task GRPO to jointly optimize specification-guided
generation and discrimination using task-specific outcome rewards.

Dual-Task GRPO Reward and Advantage Design. SpecCoder jointly optimizes
specification-guided generation and discrimination in the GRPO stage. Since the
two tasks have different output formats and reward structures, we define task-
specific rewards and normalize advantages separately within each task type. For a
                                                      (𝑞)
training instance of task type 𝑞 ∈ {gen, disc}, let {𝑜𝑖,𝑘 }𝐺𝑘=1 denote the 𝐺 sampled
                                                   (𝑞)
outputs from the current policy, and let 𝑅𝑞 (𝑜𝑖,𝑘 ) denote the corresponding task-
specific reward. The normalized advantage is computed as:
                                                                        
                             (𝑞)                 (𝑞)               (𝑞)
                        𝑅𝑞 (𝑜𝑖,𝑘 ) − mean 𝑅𝑞 (𝑜𝑖,1 ), . . . , 𝑅𝑞 (𝑜𝑖,𝐺 )
                  (𝑞)
               𝐴ˆ 𝑖,𝑘 =                                              .     (4)
                                        (𝑞)               (𝑞)       (𝑞)
                        max std 𝑅𝑞 (𝑜𝑖,1 ), . . . , 𝑅𝑞 (𝑜𝑖,𝐺 ) , 𝜎min

        (𝑞)
Here, 𝜎min is a task-specific variance floor, which is set to 10−3 for both generation
and discrimination. This task-wise normalization compares sampled outputs only
within the same task type and training instance, preventing reward-scale differences
between generation and discrimination from dominating policy updates. We define
the task-specific rewards 𝑅gen and 𝑅disc as follows.
    For the generation task, let 𝑜 𝑔 denote a sampled output and let 𝑐 𝑔 be the
implementation extracted from its code section. The generation reward combines
format compliance, compilation success, and execution-based correctness:
                               gen         gen                       gen
               𝑅gen (𝑜 𝑔 ) = 𝛼𝑟 format + 𝛾𝑟 compile + (1 − 𝛼 − 𝛾)𝑟 correct ,      (5)


                                           12
                                                             gen
where 𝛼 = 0.2 and 𝛾 = 0.2. The format reward 𝑟 format is 1.0 when both the
structured specification analysis section and the code section are present, 0.75
when only the code section is present, 0.25 when only the structured specification
                                                                         gen
analysis section is present, and 0 otherwise. The compilation reward 𝑟 compile is
1 if the extracted implementation compiles successfully and 0 otherwise. The
correctness reward is based on the test pass rate:
                           (
                  gen        𝑓 (𝑐 𝑔 , T𝑝 ),    if 𝑑𝑔 = Easy,
                𝑟 correct = √︁                                                 (6)
                                𝑓 (𝑐 𝑔 , T𝑝 ), if 𝑑𝑔 ∈ {Medium, Hard},

where 𝑑𝑔 denotes the difficulty of the generation instance.
    For the discrimination task, let 𝑜 𝑑 denote a sampled output and let 𝑦ˆ be the fi-
nal decision extracted from 𝑜 𝑑 . Given a discrimination instance ( 𝑝, 𝑠, 𝑐 𝐴 , 𝑐 𝐵 , 𝑦) ∈
Ddisc , the discrimination reward combines a format reward and a decision correct-
ness reward:
                                          disc              disc
                        𝑅disc (𝑜 𝑑 ) = 𝜆𝑟 format + (1 − 𝜆)𝑟 decision ,                 (7)
We set 𝜆 = 0.3. The format reward 𝑟 format disc is 1.0 when both the comparison
analysis and final decision are present, 0.5 when only one of them is present, and
0 otherwise. The decision correctness reward is defined as:
                                    disc
                                  𝑟 decision = I[ 𝑦ˆ = 𝑦],                            (8)

where 𝑦 ∈ {𝐴, 𝐵} denotes the candidate implementation with the higher test
pass rate after random ordering. Detailed training hyperparameters are reported
in Appendix D.

Progressive Curriculum Learning Strategy. In the curriculum dual-task GRPO
stage, directly mixing all difficulty levels from the beginning may lead to unsta-
ble optimization, because easy samples provide dense but limited learning signals,
whereas harder samples require more complex requirement analysis, specification-
guided code generation, and fine-grained implementation comparison. SpecCoder
therefore adopts a progressive curriculum that organizes training samples accord-
ing to task type and difficulty level.
    For the generation task, each instance is assigned a difficulty label 𝑑𝑔 ∈
{Easy, Medium, Hard} according to the benchmark-provided difficulty annota-
tions. For the discrimination task, difficulty is determined by the pass rate gap Δ
between the higher-performing and lower-performing candidate implementations,
as defined in Section 4.1.2. To avoid unequal sample exposure, we keep a fixed

                                            13
sample-level update budget across the GRPO stage, so that the curriculum changes
the training order and phase composition rather than the total exposure of each
sample. The curriculum consists of three sequential phases:

    • Phase 1 (Initial Alignment): uses Easy samples from both generation
      and discrimination tasks to establish basic associations between structured
      specification analyses and code behavior.

    • Phase 2 (Difficulty Adaptation): focuses on Medium and Hard samples
      from both tasks to improve complex requirement analysis, specification-
      guided code generation, and fine-grained implementation comparison.

    • Phase 3 (Full Consolidation): mixes all task types and difficulty levels
      to consolidate learned behaviors across the full training distribution and
      mitigate forgetting of easier cases.

    Detailed training data configurations and optimization procedures are provided
in Appendix Appendix D, while the complete training process is summarized in
Algorithm 1.

5. Experimental Design
5.1. Datasets
    We evaluate SpecCoder on three widely adopted competitive code generation
benchmarks: APPS [3], CodeContests [4], and xCodeEval [5]. Following the
pipeline in Section 4.1, we construct the specification-guided generation and dis-
crimination datasets for training. Table 2 summarizes the final training and testing
data distributions, while further dataset details and difficulty classifications are
provided in Appendix B.

                 Training Phase                                   Evaluation Phase
    Dataset      Phase                                Size   Dataset       Phase           Size
                 SFT (𝑇1 : 𝑇2 = 1 : 0)               6,039   APPS          Testing         500
    APPS
                 GRPO (𝑇1 : 𝑇2 = 2 : 1)              5,110   CodeContests Testing          165
                 SFT (𝑇1 : 𝑇2 = 1 : 0)               7,493   xCodeEval     Testing         300
    CodeContests
                 GRPO (𝑇1 : 𝑇2 = 2 : 1)              5,110   -             -                -
Table 2: Statistics of the datasets. Note: 𝑇1 and 𝑇2 denote the Specification-Guided Code Generation
task and the Specification-Guided Code Discrimination task, respectively.




                                                14
5.2. Evaluation Metrics
    Following studies [8, 21], we employ Pass@1 and AvgPassRatio to evaluate
the performance of SpecCoder, capturing both exact and partial correctness. To
quantify uncertainty, we report 95% confidence intervals estimated via bootstrap
resampling with 10,000 iterations over the test set [37].
    Pass@1. We focus on Pass@1 as it mirrors real-world scenarios where devel-
opers typically rely on the first generated solution [25, 9, 16]. For an evaluation set
of 𝑁 tasks, the model generates a single code instance per problem with a decoding
temperature of 0.2. Let the indicator function I𝑖 = 1 if the 𝑖-th task passes all test
cases, and I𝑖 = 0 otherwise. The metric is defined as:
                                                  𝑁
                                               1 ∑︁
                                𝑃𝑎𝑠𝑠@1 =             I𝑖                            (9)
                                               𝑁 𝑖=1

    AvgPassRatio. To provide a complementary view of partial correctness, Avg-
PassRatio measures the average fraction of passed test cases across the same 𝑁
tasks. For the 𝑖-th task, let 𝑇𝑖 denote the total number of evaluation test cases, and
𝑡𝑖 denote the number of test cases passed by the generated instance:
                                                      𝑁
                                           1 ∑︁ 𝑡𝑖
                            𝐴𝑣𝑔𝑃𝑎𝑠𝑠𝑅𝑎𝑡𝑖𝑜 =                                        (10)
                                           𝑁 𝑖=1 𝑇𝑖

5.3. Baselines
    To compare SpecCoder with representative code generation methods, we con-
sider two broad categories of baselines: training-free and training-based methods.
The training-free baselines include prompt-based approaches, such as SCoT [26],
Self-Planning [8], 𝜇FiX [21] and ArchCode [28]. The training-based baselines
include CodeRL+ [17], CodeDPO [14], CodePRM [16], and FixAudit [33] which
optimize code generation through reinforcement learning, preference optimiza-
tion, or reward modeling. To further evaluate the generalization and compatibility
of SpecCoder as a backbone model, we extend our study to four representative
training-free agent-based frameworks: AgentCoder [11], MetaGPT [10], Pair-
Coder [13], and Specine [18]. This setting allows us to examine whether the
specification-aware generation capability learned by SpecCoder can benefit down-
stream agent workflows across different agent architectures. More details on these
approaches can be found in their papers.



                                          15
5.4. Implementation Details
    All training and evaluation tasks are executed on two NVIDIA A100 SXM4
GPUs with 80GB memory. SpecCoder follows a two-stage training scheme. In
the first stage, we perform SFT on Qwen2.5-7B-Coder-Instruct [38] with LoRA
fine tuning [39] using LLaMA Factory [40]. In the second stage, we perform
curriculum dual-task GRPO [41] using SkyRL [42]. For fair comparison, all
trainable methods use the same backbone model, training split, evaluation pro-
tocol, hardware, and comparable optimization budget. Training-free baselines,
including prompt-based and agent-based methods, use the same backbone model
and decoding settings without parameter updates. Training-based baselines are
trained on the same programming problems and test suites, with training signals
following their original designs. Detailed data distributions, hardware statistics,
and hyperparameter configurations are provided in Appendix D.

                                         ID                                           OOD
Technique                  APPS                    CodeContests                     xCodeEval
                   P@1            Avg.P          P@1         Avg.P               P@1        Avg.P
Training-free Prompting Baselines
Zero-shot      0.166 ± 0.033 0.271 ± 0.033   0.030 ± 0.027   0.145 ± 0.037   0.100 ± 0.032   0.204 ± 0.038
SCoT           0.168 ± 0.033 0.298 ± 0.033   0.036 ± 0.027   0.114 ± 0.037   0.097 ± 0.032   0.250 ± 0.038
Self-Planning 0.168 ± 0.030 0.278 ± 0.031    0.049 ± 0.033   0.109 ± 0.040   0.083 ± 0.030   0.233 ± 0.037
𝜇Fix           0.170 ± 0.031 0.299 ± 0.032   0.055 ± 0.033   0.157 ± 0.037   0.133 ± 0.025   0.279 ± 0.030
ArchCode       0.174 ± 0.031 0.274 ± 0.032   0.067 ± 0.025   0.145 ± 0.041   0.103 ± 0.032   0.189 ± 0.036
Training-based Fine-tuning Baselines
CodeRL+        0.182 ± 0.039 0.339 ± 0.036   0.049 ± 0.033   0.105 ± 0.039   0.093 ± 0.028   0.175 ± 0.034
CodeDPO        0.178 ± 0.035 0.332 ± 0.034   0.061 ± 0.033   0.144 ± 0.044   0.073 ± 0.031   0.171 ± 0.035
CodePRM        0.186 ± 0.033 0.340 ± 0.033   0.073 ± 0.037   0.166 ± 0.035   0.103 ± 0.033   0.207 ± 0.039
FixAudit       0.184 ± 0.035 0.254 ± 0.032   0.091 ± 0.042   0.162 ± 0.046   0.143 ± 0.040   0.279 ± 0.044
Ours
SpecCoder      0.186 ± 0.028 0.346 ± 0.030   0.091 ± 0.023   0.207 ± 0.033   0.147 ± 0.026   0.324 ± 0.033

Table 3: Performance comparison of various code generation techniques utilizing the base
Qwen2.5-7B-Coder-Instruct, measured by Pass@1 and AvgPassRatio. Results are reported with
95% confidence intervals, where P@1 and Avg.P denote Pass@1 and AvgPassRatio, respectively.



6. Results and Analysis
6.1. Effectiveness of the SpecCoder Framework
    Setup. To establish a unified experimental foundation, we use the open-
source Qwen2.5-7B-Coder-Instruct as the baseline backbone. In this subsection,

                                                  16
we evaluate standalone code generation by assessing ID performance on APPS
and CodeContests along with OOD generalization on xCodeEval. Across these
evaluations, we compare SpecCoder against a standard Zero-shot approach and
the previously introduced training-free and training-based baselines. All methods
generate a single solution with a decoding temperature of 0.2. All metric scores
are reported with 95% bootstrap confidence intervals estimated over test instances.
    Results and Analysis. Table 3 summarizes the performance of standalone
code generation methods across the three datasets. For ID evaluation, SpecCoder
achieves strong performance on both APPS and CodeContests. On APPS, Spec-
Coder obtains a Pass@1 of 0.186 and an AvgPassRatio of 0.346. Compared with
the strongest baseline CodePRM which achieves 0.186 and 0.340, SpecCoder
matches its Pass@1 while further improving AvgPassRatio. On CodeContests,
SpecCoder and FixAudit achieve the same Pass@1 of 0.091, while SpecCoder
achieves a higher AvgPassRatio of 0.207 compared with 0.162 for FixAudit. For
OOD evaluation on xCodeEval, SpecCoder achieves a Pass@1 of 0.147, compared
with 0.143 for FixAudit and 0.133 for 𝜇Fix. Furthermore, SpecCoder achieves
the highest AvgPassRatio of 0.324, delivering an improvement of 4.5 percentage
points over the best baseline.
Conclusion 1: SpecCoder achieves competitive or superior standalone code
generation performance across the evaluated ID and OOD benchmarks, sup-
porting the effectiveness of the proposed specification-aware two-stage training
framework.

6.2. Generalization as an Agent Backbone
    Setup. To evaluate whether SpecCoder can generalize beyond standalone
code generation, we use it as the backbone model of representative training-free
agent-based workflows, including AgentCoder, MetaGPT, PairCoder, and Specine.
Specifically, we replace the original Qwen2.5-7B-Coder-Instruct backbone in each
workflow with the LLM trained by SpecCoder. We evaluate agent performance in
both ID and OOD settings over five interactive rounds.
    Results and Analysis. As Table 4 shows, SpecCoder consistently improves
agent-based workflows on both ID and OOD benchmarks. On APPS, PairCoder
achieves the largest gain, with Pass@1 increasing by 6.1 percentage points over the
original backbone. On the more challenging CodeContests benchmark, replacing
the backbone with SpecCoder improves Pass@1 and AvgPassRatio by up to 10.9
and 12.3 percentage points, respectively. On xCodeEval, SpecCoder also shows
strong OOD generalization, with Specine reaching 28.3% Pass@1 and 36.8%

                                        17
                   APPS                     CodeContests                 xCodeEval
                       SpecCoder                    SpecCoder                   SpecCoder




                       AgentCoder                   AgentCoder                  AgentCoder




                       SpecCoder                    SpecCoder                   SpecCoder




                          MetaGPT                   MetaGPT                     MetaGPT




                       SpecCoder                    SpecCoder                   SpecCoder




                          PairCoder                 PairCoder                   PairCoder




                        SpecCoder                   SpecCoder                   SpecCoder




                           Specine                   Specine                     Specine




Figure 2: Performance trends in terms of Pass@1 of agent-based code generation methods over five
iterations across three datasets. Each row corresponds to a specific agent framework, comparing
the base Qwen2.5-7B-Coder-Instruct with its SpecCoder-enhanced variant.


AvgPassRatio, corresponding to gains of 11.3 and 12.5 percentage points. The
results after five iterations consistently show higher performance for SpecCoder-
based agents than for their corresponding base-model counterparts across the
evaluated frameworks. These results demonstrate that SpecCoder serves as an
effective backbone for diverse agent architectures.
    Figure 2 further shows that SpecCoder-based agents consistently achieve higher
Pass@1 than agents using the original LLM at each refinement round, while
also showing gradual performance improvements across iterations. This observa-

                                              18
                                                ID                                      OOD
      Technique                  APPS                   CodeContests                 xCodeEval
                         P@1           Avg.P         P@1           Avg.P         P@1           Avg.P
           Base      0.270 ± 0.039 0.501 ± 0.033 0.115 ± 0.048 0.236 ± 0.052 0.210 ± 0.045 0.431 ± 0.043
AgentCoder
           SpecCoder 0.338 ± 0.041 0.541 ± 0.034 0.146 ± 0.052 0.328 ± 0.056 0.310 ± 0.052 0.563 ± 0.041
           Base      0.208 ± 0.036 0.393 ± 0.033 0.067 ± 0.039 0.204 ± 0.048 0.160 ± 0.042 0.375 ± 0.041
 MetaGPT
           SpecCoder 0.268 ± 0.039 0.486 ± 0.033 0.115 ± 0.048 0.293 ± 0.052 0.210 ± 0.047 0.469 ± 0.041
           Base      0.291 ± 0.041 0.481 ± 0.036 0.091 ± 0.045 0.254 ± 0.052 0.237 ± 0.048 0.423 ± 0.046
 PairCoder
           SpecCoder 0.352 ± 0.042 0.574 ± 0.033 0.200 ± 0.064 0.377 ± 0.061 0.277 ± 0.050 0.542 ± 0.041
           Base      0.596 ± 0.042 0.700 ± 0.036 0.376 ± 0.073 0.426 ± 0.071 0.170 ± 0.043 0.243 ± 0.043
  Specine
           SpecCoder 0.656 ± 0.041 0.749 ± 0.033 0.424 ± 0.073 0.456 ± 0.073 0.283 ± 0.050 0.368 ± 0.048

Table 4: Performance comparison of different agent-based techniques using Qwen2.5-7B-Coder-
Instruct at iteration 5, measured by Pass@1 and AvgPassRatio. Results are reported with 95%
confidence intervals, where P@1 and Avg.P denote Pass@1 and AvgPassRatio, respectively.


tion confirms that the performance lead of SpecCoder is consistently maintained
throughout the entire multi round interactive process.
Conclusion 2: SpecCoder provides a stronger backbone for training-free agent-
based code generation workflows across both ID and OOD benchmarks. he
experimental results confirm that replacing the base model with SpecCoder
directly elevates the final performance of various multi-step agent workflows
without requiring any modifications to their external workflow design.

6.3. Ablation Study
    To verify the contribution of each design in SpecCoder we conduct ablation
experiments across both ID and OOD benchmarks by dividing the variants into
three main groups training component, optimization strategy and intermediate
representation. Unless stated otherwise all variants share the same base model
data splits evaluation protocols and compute budgets.

6.3.1. Training Component
    Setup. This section evaluates whether the main training components in the
specification-aware two-stage training framework are necessary for effective code
generation. The specific ablation designs are as follows:
    • Variant I (w/o SFT) removes the specification-guided SFT stage and applies
      curriculum dual-task GRPO directly to the base model.
    • Variant II (w/o GRPO) removes the curriculum dual-task GRPO stage and
      relies only on specification-guided SFT.

                                                  19
Figure 3: Ablation study results of SpecCoder in terms of Pass@1 and AvgPassRatio across three
benchmarks. The red shaded areas and arrows quantify the performance drop of each variant
relative to the full model. Configuration labels: I w/o SFT, II w/o GRPO, III w/o discrimination
task, IV w/o curriculum, V generation-first sequential, VI discrimination-first sequential.


    • Variant III (w/o Discrimination Task) removes the specification-guided
      code discrimination task and optimizes only the generation task during
      GRPO.
    Results and Analysis. The overall ablation results are illustrated in Fig-
ure 3. The training component ablation reveals that removing any of the three key
components leads to noticeable performance degradation. Specifically, Variant
I applies GRPO directly without supervised initialization, reducing Pass@1 on
CodeContests from 0.091 to 0.043. This severe 52.7 percent drop suggests the

                                              20
model relies on supervised fine tuning to learn how to format and utilize struc-
tured specification analyses. Conversely, Variant II removes GRPO and causes
a 34.1 percent decrease in Pass@1. This mutual degradation confirms that SFT
provides the essential structural initialization, while GRPO further optimizes gen-
eration quality beyond supervised data. Variant III verifies the importance of
the specification-guided code discrimination task. When this task is removed,
GRPO optimizes only the generation objective, resulting in weaker performance.
This indicates that generation alone does not explicitly train the LLM to judge
whether an implementation follows the stated specification-level understanding.
By comparing candidate implementations under the same raw requirement and
structured specification analysis, the discrimination task helps the model associate
specification satisfaction with concrete code behavior.
Conclusion 3: Each training component contributes to the overall effectiveness
of SpecCoder, as removing any component leads to performance degradation.
Specification-guided SFT initializes the capacity of the model to derive struc-
tured specification analyses and generate code conditioned on them. Dual-task
GRPO provides the essential initialization for structured generation while the
discrimination task acts as a powerful auxiliary signal during dual task GRPO to
further maximize overall code quality.

6.3.2. Optimization Strategy
    Setup. This experiment examines how the difficulty based curriculum schedul-
ing and the task optimization order affect dual task GRPO. We design three variants
to modify the curriculum schedule or the task optimization order:

    • Variant IV (w/o Curriculum) removes the difficulty-based curriculum and
      trains on samples from all difficulty levels simultaneously.

    • Variant V (Gen-First Sequential) replaces joint dual-task optimization
      with sequential training, where the generation task is optimized before the
      discrimination task.

    • Variant VI (Disc-First Sequential) replaces joint dual-task optimization
      with sequential training, where the discrimination task is optimized before
      the generation task.

   Results and Analysis. Figure 3 illustrates the results of the optimization strat-
egy ablation. For Variant IV removing the curriculum reduces Pass@1 on Code-
Contests from 0.091 to 0.079 which reveals a drop on more complex benchmarks.

                                        21
This demonstrates that curriculum learning provides a stable optimization path
by establishing reliable initial signals before introducing complex requirements.
Variant V and Variant VI replace joint dual-task optimization with sequential
training. Both variants underperform the full model, indicating that optimizing
generation and discrimination separately is less effective than jointly optimizing
them. Sequential training may overemphasize one task before the other has estab-
lished a stable learning signal. In contrast, joint optimization allows generation
and discrimination to reinforce each other throughout GRPO. The generation task
improves the model’s ability to construct and use structured specification analyses
for code synthesis, while the discrimination task strengthens its ability to relate
specification-level understanding to concrete code behavior.
Conclusion 4: The optimization strategy ablation demonstrates that both cur-
riculum learning and joint dual-task optimization are important for the overall
performance of SpecCoder. The difficulty based curriculum provides SpecCoder
with a stable and progressive optimization path for complex coding requirements
while joint training ensures the generation and discrimination tasks mutually
reinforce the specification-aware learning process.

6.3.3. Intermediate Representation
    Setup. This experiment further investigates whether the proposed structured
specifications provide advantages over other intermediate representations under
matched training conditions. We select three representative baselines, and all
intermediate representations are generated by GPT-4o for the same training prob-
lems. Then apply the same LLM filtering rules used by SpecCoder to construct
high-quality training data. During GRPO, these three variants optimize only the
generation task and use the same generation rewards and training budget as the
generation-only SpecCoder variant (w/o Disc), corresponding to Variant III in
Section 6.3.1. The three baseline representations are defined as follows:

    • Code-Only directly formats the training data to translate raw requirements
      into code without any intermediate representation, serving as the standard
      direct generation baseline [1].

    • Free-Form structures the training data to include an unconstrained natural-
      language rationale prior to code generation, inspired by conventional Chain-
      of-Thought [24]. This examines whether the gains arise from adding general
      reasoning before code generation.



                                        22
                    APPS                                       xCodeEval


Figure 4: Performance comparison in terms of Pass@1 and AvgPassRatio on APPS and xCodeEval,
across Easy, Medium, and Hard difficulty levels.


    • Planning-CoT formats the training sequences to first formulate a stepwise
      implementation plan and subsequently generate the code [8], controlling for
      the benefits of structured intermediate planning.

     Results and Analysis. We report Pass@1 and average output length in tokens
for standalone generation in Table 5 alongside Pass@1 over five Specine iterations
in Figure 5.
     As shown in Table 5, SpecCoder (w/o Disc) achieves the best or tied-best per-
formance among all generation-only variants. On the ID benchmarks, it achieves
0.172 on APPS and 0.061 on CodeContests, outperforming or matching the three
baselines. Its advantage is more evident on the OOD xCodeEval benchmark where
it achieves 0.127 and outperforms Code Only Free Form and Planning CoT by 4.7
2.4 and 3.4 percentage points respectively. Building upon this generation foun-
dation the full SpecCoder further elevates the scores to 0.186 on APPS 0.091 on
CodeContests and 0.147 on xCodeEval through joint generation and discrimination
training Since different intermediate representations produce outputs of different
lengths, we also report their average token counts. SpecCoder (w/o Disc) generates
only 126.5 and 155.7 more tokens than Free-Form and Planning-CoT, respectively,
but improves Pass@1 on xCodeEval by 2.4 and 3.4 percentage points. The full

                                            23
                                          ID                      OOD
 IR                                                                            Avg. Tokens
                              APPS             CodeContests     xCodeEval
 Code-Only                0.166 ± 0.029        0.055 ± 0.033   0.080 ± 0.032      277.9
 Free-Form                0.170 ± 0.033        0.060 ± 0.039   0.103 ± 0.035      568.2
 Planning-CoT             0.168 ± 0.031        0.061 ± 0.039   0.093 ± 0.033      539.0
 SpecCoder (w/o Disc)     0.172 ± 0.032        0.061 ± 0.030   0.127 ± 0.028      694.7
 SpecCoder                0.186 ± 0.028        0.091 ± 0.023   0.147 ± 0.026      709.4

Table 5: Performance comparison of different intermediate representations in terms of Pass@1
and average output tokens. Results are reported with 95% confidence interval


SpecCoder adds only 14.7 tokens and further improves performance by 1.4, 3.0,
and 2.0 percentage points across the three datasets. These results show that the
gains do not come solely from longer outputs, but mainly from organizing require-
ment constraints through structured specifications and aligning requirements with
code through two-stage training.
    To further examine the role of different intermediate representations in multi-
round code generation, we select Specine, a representative code generation agent
framework, and evaluate it with all five representation variants as backbones. As
shown in Figure 5, the Pass@1 of all models increases across iterations. However,
the later gains of Code-Only, Free-Form, and Planning-CoT gradually slow down,
while the models using structured specifications maintain higher performance.
At Iter 5, the full SpecCoder outperforms the best non-structured representation
by 5.2, 6.0, and 5.3 percentage points on APPS, CodeContests, and xCodeEval,
respectively. SpecCoder (w/o Disc) also leads by 2.6, 2.4, and 2.0 percentage
points. These results show that structured specifications explicitly organize func-
tional requirements and constraints, providing a consistent reference for iterative
generation, checking, and repair. The further advantage of the full SpecCoder
suggests that two-stage training strengthens the alignment between specifications
and code behavior, allowing the agent to use iterative feedback more effectively.
Conclusion 5: Under matched training conditions, structured specifications
achieve better overall standalone and agent-based performance than Code-Only,
Free-Form, and Planning-CoT representations. These results suggest that explic-
itly organizing requirement information provides more effective intermediate
guidance for code generation.




                                               24
               Code-Only     Free-Form      Planning-CoT    SpecCoder(w/o Disc)       SpecCoder




                APPS                         CodeContests                         xCodeEval

Figure 5: Performance comparison in terms of Pass@1 for different intermediate representations
across three datasets over iterations 1–5. All variants are based on the Qwen2.5-7B-Coder-Instruct
model.


7. In-depth Analysis
7.1. Performance across Problem Difficulties
    Training-based Standalone Model Performance. Figure 4 evaluates stan-
dalone code generation performance across different problem difficulties on APPS
and xCodeEval. As task difficulty increases, all methods show performance degra-
dation, while SpecCoder maintains stronger overall robustness, especially in Avg-
PassRatio. Specifically, on Easy tasks, SpecCoder clearly outperforms baselines
on xCodeEval, achieving a Pass@1 of 0.247 and an AvgPassRatio of 0.461. On
Medium tasks, SpecCoder obtains the highest AvgPassRatio of 0.171, although
its Pass@1 of 0.043 is slightly lower than CodePRM’s 0.057. This indicates that
SpecCoder improves broader test-case coverage by aligning structured specifica-
tion analyses with code behavior, even when fewer generated code implementations
pass all tests. On Hard tasks, where Pass@1 approaches zero for most methods,
SpecCoder still achieves the leading AvgPassRatio of 0.186 on APPS. These re-
sults suggest that specification-aware training helps the LLM better preserve partial
requirement satisfaction under increasing task complexity.
    Training-free Agent-based Performance. Figure 6 further evaluates Spec-
Coder as the backbone of a training-free agent-based self-repair framework over
five interaction rounds. Compared with the vanilla backbone, SpecCoder consis-
tently yields larger Pass@1 gains across iterations. For example, on CodeContests
Easy tasks, the net improvement increases from 0.010 in the first round to 0.080
in the fifth round, while xCodeEval Easy tasks obtain a fifth-round gain of 0.143.
This trend also holds on harder tasks. APPS Hard tasks improve from 0.440 to
0.530, yielding a net gain of 0.090, and xCodeEval Hard tasks increase from 0.174


                                                25
Figure 6: Heatmap of Pass@1 improvement achieved by replacing the base Qwen2.5-7B-Coder-
Instruct with SpecCoder within the Specine framework across iterations 1–5 for different difficulty
levels of each dataset.


to 0.261. These results indicate that SpecCoder provides a stronger specification-
aware backbone, enabling training-free agent-based workflows to start from better
intermediate outputs and achieve more effective iterative repair.
Conclusion 6: SpecCoder maintains stronger specification-aware code gener-
ation across problem difficulties and provides a more effective backbone for
training-free agent-based workflows, suggesting that the proposed specification-
aware training strategy benefits both standalone generation and iterative self-
repair.

7.2. Specification Alignment and Dependency Analysis
    This section systematically examines the role of structured specifications in
SpecCoder from multiple perspectives. First, we conduct a human evaluation to
assess their coverage of the original requirements and their consistency with the
generated code. Since consistency alone is insufficient to establish that the model
actually relies on the specification during inference, we further conduct controlled
perturbation experiments to examine the dependence of both code generation and
code discrimination on specification semantics.

7.2.1. Specification Alignment Evaluation
    Setup. To assess specification quality and its alignment with generated code,
we manually evaluate intermediate reasoning on 150 stratified samples from the
three benchmarks while preserving their original difficulty distributions. For each


                                               26
         IR                     Requirement Coverage        Spec-Code Consistency
         Free-form                    3.42 ± 0.15                 3.35 ± 0.18
         Planning-CoT                 3.68 ± 0.14                 3.52 ± 0.16
         SpecCoder (Ours)             4.55 ± 0.12                 4.48 ± 0.14

Table 6: Human evaluation results for specification alignment based on a 5-point Likert scale,
reported as mean values with 95% confidence intervals.


sample, two software engineering researchers independently assess the interme-
diate reasoning and corresponding code generated by Free-form, Planning-CoT,
and SpecCoder, with method labels hidden and outputs randomly ordered. The
evaluation focuses on semantic content rather than output format and follows the
seven-dimensions. Requirement Coverage measures how completely the inter-
mediate reasoning captures the original problem requirements, while Spec-Code
Consistency measures how well the generated code aligns with the requirements,
logic, and constraints expressed in the intermediate reasoning. Detailed scoring
rubrics are provided in Appendix C.
    Results and Analysis. As shown in Table 6, the human evaluation shows
substantial inter-rater agreement, with weighted Cohen’s 𝜅 values of 0.81 and 0.77
for Requirement Coverage and Spec-Code Consistency, respectively. SpecCoder
achieves the highest scores of 4.55 and 4.48 on the two metrics, while Free-form
and Planning-CoT score between 3.3 and 3.7. The 95% confidence intervals further
show a clear performance gap. These results indicate that structured specifications
capture the original requirements more completely and exhibit stronger consistency
with the generated code.

7.2.2. Dependency in Code Generation
    Setup. To investigate whether code generation depends on the structured
specification, we conduct inference-time perturbation experiments across three
benchmarks. For each problem, we perturb the generated specification while
keeping the original problem, model parameters, prompt template, and decoding
configurations unchanged. The perturbed specification is provided within the
<ANALYZE> tags as fixed context for generation from the <CODE> tag. The settings
are as follows:


    • Empty: Removes all specification content while retaining the format tags.

    • Removed: Randomly removes one dimension from the original specification

                                             27
      while preserving the remaining dimension.

    • Shuffled: Replaces the original specification with one from another problem
      of comparable length.

    • Corrupted: Alters selected semantic constraints, such as numerical bound-
      aries or I/O requirements, while leaving the remaining content unchanged.

    • Standard: Uses the original specification without modification.

    Results and Analysis. As shown in Figure 7, the Standard setting consistently
achieves the best performance, while all perturbation settings lead to degradation.
Notably, Empty generally outperforms the other perturbations, indicating that
missing specification information is less harmful than providing incomplete or
incorrect information. Among these perturbations, Shuffled causes the largest
overall degradation, as illustrated by xCodeEval Pass@1 dropping from 0.147 un-
der Standard to 0.014. Corrupted also generally performs worse than Removed
and falls below Empty in most cases, with APPS Pass@1 decreasing from 0.170
to 0.132. These results show that the benefit of structured specifications depends
critically on their semantic correctness and alignment with the original problem.
This further suggests that SpecCoder has learned to condition code generation on
specification semantics, as misleading specifications can be more detrimental than
the absence of specification information.

7.2.3. Dependency in Code Discrimination
    Setup. To examine whether code discrimination relies on specification infor-
mation, we sample 200 test instances and follow the procedure in Section 4.1.2 to
construct a fixed candidate pair (𝑐+ , 𝑐− ) for each instance, representing correct and
defective implementations, respectively. We then evaluate discrimination accuracy
under the same specification perturbations defined in Section 7.2.2. The candidate
code pairs are kept identical across all settings, so differences in discrimination
accuracy can be primarily attributed to changes in the specification context.
    Results and Analysis. Under the Standard specification, the model achieves
91% discrimination accuracy, which drops to 68% when the specification content
is removed under Empty. The corresponding accuracies under Removed, Shuf-
fled, and Corrupted are 60%, 43%, and 49%, respectively. All three content
perturbations fall below Empty, with Shuffled and Corrupted yielding the lowest
accuracies, further highlighting the importance of complete and semantically cor-
rect specification information for code discrimination. These results indicate that

                                          28
  Pass@1
  AvgPassRatio




Figure 7: Performance impact of inference-time specification perturbations on code generation
using Qwen2.5-7B-Coder-Instruct. Pass@1 and AvgPassRatio are reported with 95% confidence
intervals, comparing four perturbation strategies against the Standard baseline.


code discrimination relies on the semantic correspondence between the structured
specification and the candidate implementations.
Conclusion 7: The perturbation experiments provide further evidence that Spec-
Coder relies on structured specifications during both code generation and dis-
crimination. Performance degradation under removed, shuffled, or corrupted
specifications indicates that the model responds to the semantic content of the
specification rather than merely its structured format.

7.3. Evaluation on Realistic Benchmarks
    To further evaluate code generation capabilities in realistic programming sce-
narios, we conduct additional experiments on BigCodeBench-Hard [43] and Clas-
sEval [44] using the official evaluation scripts. The former focuses on the ability
to call complex third-party libraries, while the latter assesses model performance
in object-oriented and context-dependent scenarios at both the function and class
levels. All results are reported using Pass@1 under greedy decoding.
    As shown in Figure 8, SpecCoder achieves the best performance across all
evaluated settings. On BigCodeBench-Hard, SpecCoder reaches 0.34, compared
with 0.29 for the base model and 0.32 for CodePRM. On ClassEval function-level
tasks, SpecCoder achieves 0.692, outperforming CodePRM at 0.673 and FixAudit
at 0.664. On class-level tasks, SpecCoder improves the base model Pass@1 from


                                             29
            Base     CodeRL+      CodeDPO       CodePRM       FixAudit    SpecCoder




               (a)                            (b)                             (c)


Figure 8: Performance comparison in terms of Pass@1 for SpecCoder against the base Qwen2.5-7B-
Coder-Instruct and four reinforcement learning baselines. (a) BigCodeBench-Hard; (b) ClassEval
function-level; (c) ClassEval class-level.

0.182 to 0.230. These results show that SpecCoder extends its performance gains
to more realistic code generation settings involving third-party libraries, object-
oriented programming, and class-level implementation.

7.4. Case Studies
     To qualitatively examine specification-aware behavior during iterative code
refinement, we select a constrained partition problem from APPS (test_1482)
as the case study. The task requires partitioning 𝑛 × 𝑘 elements into 𝑘 disjoint
subsets, each of size 𝑛, where the 𝑖-th subset must contain the preferred element
𝑎𝑖 . This problem is suitable for analysis because correct solutions must preserve
strict capacity constraints and element dependencies throughout implementation.
     As shown in Figure 9, the base LLM undergoes five refinement iterations, but
its test case pass rate remains at 40%. In the first iteration, it removes the preferred
elements and inserts them using a static global stride 𝑖 × 𝑛, which causes index
drift. Although later iterations attempt to reconstruct the solution with slicing, the
LLM eventually reverts to the earlier flawed framework and changes the insertion
position to 𝑖 × 𝑛 − 1. This behavior indicates that the generated specification-
level constraints are not consistently reflected in the implementation, leading to a
persistent mismatch between requirement understanding and code behavior.
     In contrast, SpecCoder reaches a test case pass rate of 100% in three iterations,
as shown in Figure 10. It first separates the preferred elements from the remaining
pool and then adopts a sliding-window consumption strategy, using segments[]
for dynamic padding and truncating the residual pool to avoid index offset errors.


                                             30
               Raw Requirement
          Given two integers, n and k. A set containing all integers from 1 to n × k needs to be partitioned into k disjoint subsets, where
          each subset has a size of exactly n. You are also given an array a of length k, where all elements are distinct and satisfy 1 ≤ a_i
          ≤ n × k. The constraint is that the i-th subset must contain the element a_i.
          Input Format
          The first line contains two integers n and k (1 ≤ n, k ≤ 30). And, the second line contains k distinct space-separated integers
          a_1, a_2, ..., a_k (1 ≤ a_i ≤ n × k).
          Output Format
          Print n × k space-separated integers. The first n integers represent the elements of the 1st subset, the next n integers
          represent the elements of the 2nd subset, and so on.
                                                             Code             • Purpose: Split n × k segments into k disjoint subsets of size n, ensuring group i
                 def divide_orange(n, k, a):
                   segments = list(range(1, n * k + 1))                         contains element a_i.
                   for i in range(k):                                         • Inputs: Two integers n and k (1 to 30), and a list of k distinct requested
                      segments.remove(a[i])           Pass Rate 0.40            elements a_i.
 Iteration 1




                      segments.insert(i * n, a[i])                            • Outputs: A sequence of n × k integers where each consecutive block of n items
                   return segments                                              represents the assigned subsets in order.
                                                                              • Constraints: Parameters n and k are bounded within 30, all a_i are distinct and
                 n, k = map(int, input().split())                               valid, and a solution always exists.
                 a = list(map(int, input().split()))                          • Edge Cases: Handles k = 1 where one child gets all segments, and n = 1 where
                 print(" ".join(map(str, divide_orange(n, k, a))))              each child receives only their requested a_i.             Specification Analysis

                                                             Code
                 def divide_orange(n, k, a):                                  •   Purpose: Assist Ms. Swan in partitioning n × k orange segments into k disjoint
                   segments = list(range(1, n * k + 1))                           subsets of size n, guaranteeing that group i contains the specific requested
                   result = []                                                    element a_i.
                   for ai in a:                       Pass Rate 0.40          •   Inputs: Two integers n and k (1 ≤ n, k ≤ 30), and a list of k distinct target
                      index = segments.index(ai)                                  integers a_i.
 Iteration 2




                                                                              •   Outputs: A sequence of n × k integers where each consecutive block of n
                      segments.pop(index)
                                                                                  items represents the assigned subsets in order.
                      segments.insert(0, ai)
                                                                              •   Constraints: Parameters n and k are bounded within 30, all a_i are distinct,
                      result.extend(segments[:n])
                                                                                  and a solution always exists.
                      segments = segments[n:]
                                                                              •   Edge Cases: Handles special boundaries such as k = 1 where all elements go
                   return result[:n*k]                                            to the only child, and n = 1 where each child receives exactly and only their
                 n, k = map(int, input().split())                                 requested item a_i.
                 a = list(map(int, input().split()))                          •   Example Scenarios: Targets "4 1" with n = 2, k = 2 outputs "2 4 1 3", while
                 print(" ".join(map(str, divide_orange(n, k, a))))                target "2" with n = 3, k = 1 outputs "3 2 1".            Specification Analysis

                                                             Code
                 def divide_orange(n, k, a):                                  • Purpose: Divide n × k orange segments into k disjoint groups of size n,
                    segments = list(range(1, n * k + 1))                        ensuring group i contains element a_i.
                    result = [[] for _ in range(k)]                           • Key Concepts: Includes unique segment numbering from 1 to n × k, satisfying
                    for i in range(k):                   Pass Rate 0.40         individual preferences, equal sizing, and a guaranteed valid distribution.
 Iteration 3




                       index = segments.index(a[i])                           • Inputs: Two integers n and k (1 ≤ n, k ≤ 30), and a list of k distinct target
                       result[i].append(segments.pop(index))                    integers a_i.
                       for j in range(n - 1):                                 • Outputs: A sequence of n × k integers where each consecutive block of n
                          if segments:                                          items represents the assigned subsets in order.
                             result[i].append(segments.pop(0))                • Constraints: Parameters n and k are bounded within 30, all a_i are distinct
                    return [item for sublist in result for item in sublist]     and valid, and a solution always exists.
                 n, k = map(int, input().split())                             • Edge Cases: Covers single-child allocation (k = 1), single-element matching (n
                 a = list(map(int, input().split()))                            = 1), max-bound processing (n = k = 30), and accepting any valid configuration
                                                                                if multiple solutions exist.                              Specification Analysis
                 print(*divide_orange(n, k, a))
                                            …                                                                         …
                                                             Code
                 def divide_orange(n, k, a):                                  • Purpose: Split n × k segments into k groups of size n, where group i must
                   segments = list(range(1, n * k + 1))                         contain element a_i.
                   result = []                                                • Key Concepts: Involves a 1 to n × k numbering pool, distinct individual
                   for i in range(k):                 Pass Rate 0.40            preferences, equal sizing, and a guaranteed valid distribution.
                                                                              • Edge Cases: Handles k = 1 (single child takes all), n = 1 (direct matching to
 Iteration 5




                      result.append(segments.pop(a[i] - 1))
                   for i in range(n - k):                                       input array), and multi-child group isolation.
                      result.append(segments.pop())                           • Inputs: Two integers n and k (1 ≤ n, k ≤ 30), and a list of k distinct target
                                                                                integers a_i.
                   return result
                                                                              • Outputs: A flat sequence of n × k integers where each consecutive block of n
                 n, k = map(int, input().split())                               items represents the assigned subset in order.
                 a = list(map(int, input().split()))                          • Constraints: Parameters n and k are bounded within 30, all a_i are distinct,
                 print(*divide_orange(n, k, a))                                 and a solution always exists.                              Specification Analysis

                         The error corrections merely addressed superficial symptoms rather than demonstrating a true
                                    comprehension of the requirements necessary to synthesize correct code.

Figure 9: Case study of the base Qwen2.5-7B-Coder-Instruct model on APPS test_1482. Within
the Specine framework, the figure illustrates the detailed interaction and evolution of code and
specifications across five iterations.

                                                                                  31
This update preserves both subset capacity and preferred-element constraints,
raising the pass rate to 100%. The final iteration further simplifies the code while
maintaining the correct partitioning logic. Meanwhile, the generated structured
specification analysis covers relevant edge cases and implementation constraints,
providing more stable guidance for refinement. This case suggests that SpecCoder
can better preserve raw requirement constraints during iterative refinement by
aligning structured specification analyses with concrete code behavior. While
this qualitative example does not replace systematic quantitative evaluation, it
illustrates how specification-aware training can reduce the gap between stated
specification-level understanding and generated code behavior.

8. Discussion
8.1. Cost Analysis
    The data construction pipeline contains two API-dependent stages: multi-path
generation using GPT-4o (gpt-4o-2024-08-06) and backward verification using
DeepSeek-V3-0324 [36], while forward verification relies on local execution and
incurs no API fees. Starting from 20,000 seed problems, we query GPT-4o three
times per seed, resulting in 60,000 candidate solutions. Each query contains an
average of 880 input tokens and 713 output tokens, corresponding to approximately
$0.028 per seed problem and a total generation cost of $559.8. Among these can-
didates, 88.7% pass forward verification, leaving 53,220 candidates for backward
verification. Each DeepSeek-V3-0324 query consumes an average of 1,592 input
tokens and 244 output tokens, resulting in approximately $0.000698 per candidate
and $37.16 in total. After bidirectional filtering, 13,532 high-quality triplets are
retained for Dgen . The total API expenditure is therefore approximately $596.96,
of which generation and backward verification account for 93.8% and 6.2%, re-
spectively. This corresponds to an amortized API cost of approximately $0.044
per retained sample, showing that the proposed pipeline maintains a relatively low
API cost despite the stringent filtering process.

8.2. Limitations and Future Work
    Although SpecCoder shows effectiveness in challenging code generation tasks,
this study has limitations to address in future work. First, data construction
process relies heavily on external teacher models. This ensures high quality
training data but introduces additional API costs. More importantly, the ability
of our model to understand specifications is limited by the capabilities of these
teacher models. Future work will explore ways to automatically synthesize high

                                        32
               Raw Requirement
         Given two integers, n and k. A set containing all integers from 1 to n × k needs to be partitioned into k disjoint subsets, where
         each subset has a size of exactly n. You are also given an array a of length k, where all elements are distinct and satisfy 1 ≤ a_i
         ≤ n × k. The constraint is that the i-th subset must contain the element a_i.
         Input Format
         The first line contains two integers n and k (1 ≤ n, k ≤ 30). And, the second line contains k distinct space-separated integers
         a_1, a_2, ..., a_k (1 ≤ a_i ≤ n × k).
         Output Format
         Print n × k space-separated integers. The first n integers represent the elements of the 1st subset, the next n integers
         represent the elements of the 2nd subset, and so on.
                                                                     Code                • Purpose: Partition n × k orange segments into k disjoint groups of size n,
                     def divide_orange(n, k, a):
                       segments = list(range(1, n * k + 1))                                ensuring group i contains element a_i.
                       for i in range(k): List Insert                                    • Inputs: Two integers, n and k, representing the segment count per child and the
                          segments.remove(a[i])           Pass Rate 0.40                   number of children, alongside a list a of k distinct desired segment numbers.
 Iteration 1




                          segments.insert(i * n, a[i])                                   • Outputs: A sequence of n * k integers where each consecutive block of n
                       return segments                                                     numbers represents the final segments allocated to each child in order.
                                                                                         • Constraints: Parameters n and k are bounded within 30, all a_i are distinct and
                     n, k = map(int, input().split())                                      valid, and a solution always exists.
                     a = list(map(int, input().split()))                                 • Edge Cases: Handles single-group distribution and single-element matching
                     print(" ".join(map(str, divide_orange(n, k, a))))                     where output order matches input list a.                  Specification Analysis

                                                                     Code                 • Purpose: Split n × k segments into k disjoint subsets of size n, where the i-th
                     n, k = map(int, input().split())                                       subset must contain element a_i.
                     a = [int(x) for x in input().split()]                                • Inputs: Two integers n and k (1 ≤ n, k ≤ 30), and a list of k distinct integers a_i.
 Iteration 2




                     s = set(range(1, n * k + 1))              Pass Rate 0.60             • Outputs: A sequence of n × k integers where each consecutive block of n
                     for x in a:                                                            items represents the segments assigned to each child in order.
                        s.remove(x)                                                       • Constraints: Parameters n and k are bounded within 30, all requested a_i are
                     for i in range(k):                                                     distinct and valid, and a solution always exists.
                        print(" ".join(map(str, [a[i]] + list(s)[i * (n - 1) : (i +       • Edge Cases: If k = 1, the single child gets all segments; if n = 1, each child gets
                     1) * (n - 1)]))) Set Slice                                             only their chosen a_i; if n = k, each child receives a_i plus an equal share of the
                                                                                            remaining pool.                                           Specification Analysis

                                                           Code
                                                                                          • Purpose: Split n × k segments into k disjoint subsets of size n, where the i-th
                 def distribute_segments(n, k, desired_segments):                           subset must contain element a_i.
                   # Create a list of segments from 1 to n*k                              • Inputs: Two integers n and k (1 ≤ n, k ≤ 30), and a list of k distinct integers a_i
                   segments = list(range(1, n * k + 1)) Pass Rate 1.00                      (1 ≤ a_i ≤ n × k).
                   for segment in desired_segments:                                       • Outputs: A sequence of n × k integers where each consecutive block of n
                      segments.remove(segment) Pool Extract                                 items represents the segments assigned to each child in order.
                   result = []                                                            • Constraints: Parameters n and k are bounded within 30, all requested a_i are
 Iteration 3




                   for i in range(k):                                                       distinct and valid, and a solution always exists.
                      result.append(desired_segments[i])                                  • Edge Cases: Special conditions include k = 1 (all to one child), n = 1 (each child
                      # Add the next n-1                                                    gets only a_i), and n = k (equal grid distribution).
                      result.extend(segments[:n-1])                                       • Examples: Input "2 2" with targets "2 4" outputs "2 4 1 3" (Groups: [2,4], [1,3]);
                      # Update the remaining segments                                       input "3 1" with target "3" outputs "3 2 1" (Group: [3,2,1]).
                      segments = segments[n-1:]                                           • Usage Scenarios: This problem models constrained resource allocation
                                                                                            scenarios where individual preferences must be satisfied within strict capacity
                 s




                   for i in range(0, len(result), n):
                      print(*result[i:i+n])                                                 limits.
                                                                                          • Limitations: The specification assumes a valid distribution is always
                 n, k = map(int, input().split())
                                                                                            mathematically possible, ignoring real-world feasibility checks for arbitrary
                 desired_segments = list(map(int, input().split()))
                                                                                            inputs.                                                 Specification Analysis
                 distribute_segments(n, k, desired_segments)

                       Version                   Approach                               Fixed Previous Issue?                            Core Status / Conclusion
                      Iteration 1          In-place List Insertion                                 ----                              ❌ Failed (Index Drift alignment bug)
                      Iteration 2             Static Set Slicing             Yes (Separated mandatory elements to fix drift)      ❌ Failed (Group Overflow depletion bug)
                      Iteration 3      Consumable Sliding Window               Yes (Corrected slice length to fix overflow)                      🎉 Success !

Figure 10: Case study of the Qwen2.5-7B-Coder-Instruct model trained with SpecCoder on APPS
test_1482. Within the Specine framework, the figure illustrates the interaction and evolution of
code and specifications, reaching a 100 percent test case pass rate within three iterations.


quality data without relying on closed source models. We plan to achieve this
through mechanisms like self-play [45, 46] and weak to strong generalization.
Second, executable test cases have limitations as reward signals. During the


                                                                                             33
reinforcement learning stage, we use the pass rate on test cases as an approximate
signal to measure whether the code meets the specification. However, existing
test suites are often incomplete. They mainly verify input and output correctness
through black box testing. They struggle to cover all extreme edge cases and cannot
directly check if the code follows specific internal logic or external constraints.
Future research will leverage static code analysis or process reward models for
multidimensional specification feedback beyond basic execution results.

9. Conclusion
    In this paper, we propose SpecCoder, a specification-aware two-stage training
framework for improving LLM-based code generation on challenging program-
ming tasks with complex natural language requirements. SpecCoder introduces
structured specification analyses as an intermediate interface between raw require-
ments and source code, and combines specification-guided SFT with curriculum
dual-task GRPO to optimize both code generation and code discrimination. This
design enables LLMs to explicitly derive structured specification analysis from
raw requirements, generate code conditioned on them, and strengthen the corre-
spondence between specification-level understanding and generated code behavior.
Experiments on APPS, CodeContests, and xCodeEval show that SpecCoder con-
sistently improves standalone and agent-based code generation, while additional
evaluations on BigCodeBench-Hard and ClassEval demonstrate its effectiveness
in more realistic programming scenarios. Ablation studies, human evaluation, and
specification perturbation analyses further show that the proposed training com-
ponents contribute to overall performance and that the model relies on structured
specification semantics during code generation and discrimination.




                                        34
Appendix A. Data Construction Prompts and Verification
Appendix A.1. Multi-Path Generation and Verification Prompts
    To improve reproducibility, we provide the prompt templates used in the con-
struction of Dgen . As shown in Figure A.11 part(a), the multi-path generation
prompt instructs GPT-4o (version: gpt-4o-2024-08-06) to produce structured
specification analyses according to the seven predefined dimensions, while the
bidirectional verification prompt instructs DeepSeek-V3-0324 to evaluate the se-
mantic consistency of each triplet ⟨𝑝, 𝑠, 𝑐⟩ before it is retained for training.
     # System Role                                                              # System Role
     You are an experienced programming specialist and requirement              You are an expert Software Engineering Evaluator and Code Generation Quality Analyst. Your task is to evaluate whether a
     analyst. Your task is to analyze a natural-language programming            generated structured requirement specification is semantically consistent with the original programming problem and whether the
     problem and generate a structured requirement specification that can       candidate code faithfully follows the specification.
     be used as a reliable intermediate representation for code generation.
                                                                                # Input Data
     # Input Data                                                               • Original Programming Problem: {{problem}}
     • Programming Problem: {{problem}}                                         • Generated Structured Specification: {{specification}}
                                                                                • Candidate Code: {{code}}
     # Task Description
     Given the programming problem, produce a concise and faithful              # Evaluation Context
     structured specification. The specification should summarize the           The candidate code has already passed the currently available executable test cases. However, passing these tests does not
     requirements of the original problem without generating any source         necessarily guarantee that the specification fully captures the original problem or that the code faithfully follows the specification.
     code or solution implementation. It should preserve the task objective,    Your task is to perform backward semantic verification for the triplet consisting of the original problem, the generated specification,
     input-output formats, constraints, boundary conditions, examples,          and the candidate code. A triplet should be accepted only if all three dimension scores are at least 4. Otherwise, it should be
     and any special cases that may affect program correctness.                 rejected.
     The generated specification must not introduce unsupported
     assumptions, additional requirements, or implementation details that       # Multi-Dimensional Scoring
     are not implied by the original problem. If some information is not        Evaluate the triplet using the following three dimensions. Each dimension should be rated on a five-point scale, where a higher
     provided in the problem statement, do not invent it. The total length of   score indicates better quality.
     the specification should be kept within 500 words.
                                                                                ## Dimension 1: Semantic Completeness
     # Specification Dimensions                                                 -Definition: Measures whether the specification adequately covers the key requirements in the original problem.
     1. Problem Background: Describe the development context,                   • 5: Fully covers the task objective, input-output formats, constraints, boundary conditions, and special cases.
         applicable scenario, and necessary background information for          • 4: Covers the main requirements with only minor omissions that do not affect the core semantics.
         understanding the purpose of the problem.                              • 3: Generally usable but misses some noticeable requirements or boundary conditions.
     2. Functional Requirements: Describe the primary functionality             • 2: Misses multiple important requirements or partially misinterprets the problem.
         required by the problem, including the key operations or the           • 1: Severely incomplete, misleading, or inconsistent with the original problem.
         specific task to be solved.
     3. Input Requirements: Describe the expected input types, structure,       ## Dimension 2: Algorithmic Traceability
         format, data ranges, constraints, and validation rules.                -Definition: Measures whether the implementation logic of the candidate code can be reasonably traced back to the specification.
     4. Output Requirements: Describe the expected output type, format,         • 5: The code faithfully implements the functionality, constraints, and expected behaviors described in the specification.
         and correctness conditions that the output must satisfy.               • 4: The main logic is consistent with the specification, with only minor unsupported details.
     5. Test Cases: Extract the sample test cases or examples provided          • 3: The code is partially consistent with the specification but contains noticeable gaps or assumptions.
         in the problem statement to illustrate the expected behavior. If no    • 2: The code relies on important assumptions or logic not supported by the specification.
         test case is provided, return "NONE".                                  • 1: The implementation is largely inconsistent with or unrelated to the specification.
     6. External Dependencies: List any required libraries, frameworks,
         APIs, or environmental assumptions if explicitly specified. If none    ## Dimension 3: Expression Clarity
         are required, return "NONE".                                           -Definition: Measures whether the specification is clear, specific, and suitable as a conditioning signal for code generation.
     7. Additional Notes: Provide any additional constraints, edge cases,       • 5: Clear, explicit, well structured, and free of ambiguity or irrelevant content.
         implementation considerations, or special rules that are important     • 4: Mostly clear and actionable, with only minor wording or formatting issues.
         for correctly solving the problem. If none are provided, return        • 3: Understandable but contains vague, generic, or partially ambiguous descriptions.
         "NONE".                                                                • 2: Contains substantial ambiguity, placeholders, contradictions, or irrelevant content.
                                                                                • 1: Unclear, non-actionable, internally inconsistent, or largely unusable.
     # Output Format
     Strictly output a JSON object with no markdown formatting:                 # Output Format
     {                                                                          Strictly output a JSON object with no markdown formatting:
     "structured_specification": {                                              {
     "overall_analysis": "",                                                    "quality_evaluation": {
     "problem_background": "",                                                  "semantic_completeness_score": ,
     "functional_requirements": "",                                             "algorithmic_traceability_score": ,
     "input_requirements": "",                                                  "expression_clarity_score": ,
     "output_requirements": "",                                                 "reasoning": "Brief justification for the assigned scores"
     "test_cases": "",                                                          },
     "external_dependencies": "",                                               "acceptance_decision": {
     "additional_notes": ""                                                     "accepted": ,
     }                                                                          "reason": "Brief explanation of why the triplet is accepted or rejected"
     }                                                                          }
               (a) Multi-Path Generation Prompt                                 }                                         (b) Bidirectional Verification Prompt




Figure A.11: Prompt templates used in the SpecCoder data construction pipeline. Subfigure (a)
shows the multi-path specification generation prompt, which guides GPT-4o (version: gpt-4o-
2024-08-06) to generate structured specification analyses from raw requirements. Subfigure (b)
shows the bidirectional verification prompt, which guides DeepSeek-V3-0324 to evaluate each
triplet along semantic completeness, algorithmic traceability, and expression clarity.


Appendix A.2. Bidirectional Verification Evaluation Rubrics and Prompt
    This section describes the evaluation rubrics used in the backward verification
stage of the data construction pipeline. After forward execution-based verification,

                                                                                                         35
a candidate implementation may pass all available test cases, but its correspond-
ing structured specification analysis may still omit key requirements, introduce
unsupported assumptions, or fail to faithfully reflect the implemented behavior.
Therefore, for each triplet ⟨𝑝, 𝑠, 𝑐⟩, where 𝑝 is the raw requirement, 𝑠 is the gen-
erated structured specification analysis, and 𝑐 is the candidate implementation, we
use DeepSeek-V3-0324 [36] as an automatic evaluator to assess semantic consis-
tency before adding the triplet to Dgen . Backward verification is conducted along
three dimensions:

    • Semantic Completeness. This dimension evaluates whether the structured
      specification analysis 𝑠 preserves the key requirement information in the
      raw requirement 𝑝, including the task objective, input and output formats,
      constraints, boundary conditions, and special cases.

    • Algorithmic Traceability. This dimension evaluates whether the imple-
      mentation logic of the candidate code 𝑐 can be reasonably traced back to the
      structured specification analysis 𝑠, including the core algorithm, input/output
      handling, state updates, and boundary-case processing.

    • Expression Clarity. This dimension evaluates whether the structured spec-
      ification analysis 𝑠 is clear, specific, and suitable as a conditioning signal
      for code generation, without vague placeholders, ambiguous descriptions,
      contradictions, or irrelevant content.

    Each dimension is rated on a five-point scale, as detailed in Figure A.11 (b).
A triplet is retained in Dgen only if it receives a score of at least 4 in all three di-
mensions. Unlike forward verification, which focuses on executable correctness,
backward verification provides a fine-grained assessment of the semantic consis-
tency among the raw requirement, structured specification analysis, and generated
implementation. This process filters out triplets that pass the available tests but
contain incomplete, inconsistent, or unclear specification analyses.
    To assess the reliability of the automatic evaluation, we conduct a manual
audit of 400 triplets randomly sampled from the 13,532 triplets accepted by the
automatic evaluator. According to Cochran’s formula [47], this sample size corre-
sponds to a 95% confidence level with an approximate margin of error of 4.83%
under the conservative maximum-variance assumption. Two researchers with ex-
pertise in software engineering and program analysis independently evaluate the
sampled triplets using the same three dimensions and five-point scoring criteria.


                                          36
Both annotators are blind to the scores assigned by the automatic evaluator. Dis-
agreements are resolved through discussion, with a third annotator consulted when
necessary.
    The two annotators achieve a Cohen’s Kappa of 𝜅 = 0.79, indicating substantial
inter-annotator agreement [48]. After resolving disagreements, 88% of the auto-
matically accepted triplets also satisfy the human acceptance criterion, requiring
a score of at least 4 in all three dimensions. This human-validated acceptance rate
provides empirical support for using automatic backward verification to construct
high-quality specification-guided generation data at scale.

Appendix B. Expanded Descriptions of Benchmark Datasets
   To evaluate SpecCoder, we adopt three competitive code generation bench-
marks: APPS [3], CodeContests-raw [4], and xCodeEval [5]. To construct the
required specification-based generation and discrimination tasks, the data is pro-
cessed via bidirectional filtering. The subsequent subsections provide detailed
descriptions and difficulty classifications for each dataset.

Appendix B.1. APPS
     This dataset collects programming problems from various online platforms
such as Codeforces and LeetCode. It contains 5,000 training samples and 5,000
test samples. For convenience, we denote the three difficulty levels of introductory,
interview, and competition as easy, medium, and hard respectively. In the training
phase, we utilize all training data. To obtain richer training resources, we also
select 3,000 samples from the test set for data generation according to the original
difficulty distribution. In the testing phase, following previous work [21, 19], we
sample 500 problems from the test set for our experiments to balance evaluation
cost and statistical representation. This sub-sample strictly maintains the original
difficulty distribution across easy, medium, and hard levels.

Appendix B.2. CodeContests
    It is introduced by Google DeepMind to evaluate the ability of models to solve
competitive programming problems. The dataset consists of 13,610 training prob-
lems and 165 test problems. Based on the platform rating score 𝑅, the problems
are divided into three levels, where easy represents 800 ≤ 𝑅 ≤ 1400, medium
represents 1400 < 𝑅 ≤ 1900, and hard represents 𝑅 > 1900. In the training phase,
we utilize all 13,610 training problems as base data for data construction during the
generation stage. In the testing phase, we use the complete test sets for evaluation.

                                         37
Appendix B.3. xCodeEval
    It is a large-scale competitive code generation benchmark that contains about
7,500 programming problems. The problems are divided into three levels based
on the difficulty value 𝐷, where easy represents 𝐷 ≤ 1400, medium represents
1400 < 𝐷 ≤ 2000, and hard represents 𝐷 > 2000. In the training phase, this
dataset does not participate in the construction of the training data to ensure a
fair evaluation. In the testing phase, we use it purely as a test set to check the
robustness of the models. Following the settings of previous work [21, 19], we
sample a subset of 300 problems from this benchmark to evaluate our method and
the baseline models.

Appendix C. Human Evaluation Rubrics
    To ensure a fair and consistent assessment across different intermediate rep-
resentations, the human evaluation employs a 5-point Likert scale. The seven
predefined specification dimensions in Table 1 are used only as a semantic refer-
ence rather than as separately scored items or required output fields. Evaluators
examine whether the intermediate reasoning captures the requirement information
represented by these dimensions, regardless of how such information is organized
or expressed. Based on this assessment, Requirement Coverage measures the
overall completeness of the captured requirements, while Spec-Code Consistency
evaluates how consistently the generated code follows the requirements, logic, and
constraints expressed in the intermediate reasoning. Detailed scoring criteria are
provided in Figure C.12.

Appendix D. Implementation and Hyperparameter Configurations
    We conduct the two-stage training of SpecCoder on two NVIDIA A100-SXM4
GPUs using a random seed of 42 for training and evaluation. The correspond-
ing hyperparameter configurations are provided in Table C.7. The supervised
fine-tuning stage uses 13,532 samples and takes 1.50 hours, with a peak memory
usage of 73,058 MB per GPU. The curriculum dual-task GRPO stage uses 10,220
samples, including 6,811 generation samples and 3,409 discrimination samples,
which are further partitioned into easy, medium, and hard subsets. Within each
curriculum stage, generation and discrimination samples from the designated dif-
ficulty subsets are randomly interleaved, with a peak memory usage of 76,445 MB
per GPU. As illustrated in Figure 1 and Table C.8, the three curriculum stages
require 13.17 hours for easy warmup, 25.67 hours for hard focus, and 18.38 hours

                                       38
 Part I: Requirement Coverage Rubric
 p 5 (Perfect): Comprehensively and accurately covers all core problem elements (task goals, I/O formats,
   implicit and explicit constraints, and edge cases). Contains no missing key information or hallucinated facts.
 p 4 (Good): Covers the vast majority of key requirements. Any omissions are extremely minor and do not
   impact the complete derivation of the core logic.
 p 3 (Fair): Extracts the primary task objectives but omits explicit constraints or edge cases, or contains a small
   amount of hallucinated information irrelevant to the original problem.
 p 2 (Poor): Omits multiple key requirements or demonstrates a severe misunderstanding of the core intent.
   Unreliable as a foundation for code generation.
 p 1 (Fail): Severely lacks critical information or completely fails to reFlect the intent of the original problem.

 Part II: Speci7ication-Code Consistency Rubric
 p 5 (Perfect): The code logic perfectly maps to the intermediate text. Explicit algorithm choices, boundary
   handling, and constraints in the text are directly and rigorously reFlected in the code.
 p 4 (Good): The main code logic follows the intermediate text. It deviates only in a few non-core
   implementation details, but the overall code architecture remains highly consistent with the speciFication.
 p 3 (Fair): The code only partially follows the text. There are obvious disconnections, such as missing key
   constraints in the code or implementing core logic completely unmentioned in the text.
 p 2 (Poor): A substantial disconnection exists between the code logic and the intermediate text. Most of the
   implementation deviates from the established plan.
 p 1 (Fail): The code completely contradicts the intermediate text, showing no adherence to the plan.


           Figure C.12: The 5-point Likert rubric for evaluating specification alignment.
     Specification-Guide SFT Stage (Model: Qwen2.5-7B-Coder-Instruct-base)
   Hyperparameter          Value     Hyperparameter             Value
   LR Scheduler            Cosine    Cutoff Length               4096
   Learning Rate         1.0 × 10−4 Precision                    BF16
   Epochs                    3.0     LoRA Rank                     8
   Warmup Ratio              0.1     LoRA Target             all modules
   Curriculum Dual-task GRPO Stage (Model: Qwen2.5-7B-Coder-Instruct-SFT)
   Hyperparameter          Value     Hyperparameter             Value
   Parallel Strategy       FSDP2     Max Prompt Length           2048
   Policy Learning Rate 1.0 × 10−6 Max Generate Length           1024
   Samples per Prompt         8      Inference Engine           vLLM
   Train Batch Size          16      Epochs                        3

           Table C.7: Hyperparameter settings for the two-stage training of SpecCoder.


for full consolidation. Each stage initializes the model from the checkpoint of the
preceding stage while resetting the optimizer state. As formalized in Algorithm 1,
easy samples are processed twice in the first stage and once in the third, whereas
medium and hard samples are processed twice in the second stage and once in the
third. Thus, each sample is seen exactly three times, matching the total sample
exposure of a standard three-epoch training scheme.


                                                        39
                          Task Types               Curriculum Dual-task GRPO Stage
  Difficulty
                  Generation Discrimination        Phase 1 Phase 2       Phase 3
       Easy         2,408          1,695            ✓✓                     ✓
      Medium        2,701          1,004                     ✓✓            ✓
       Hard         1,702           710                      ✓✓            ✓

Table C.8: Data distribution and epoch allocation across the three GRPO phases. Each checkmark
(✓) represents one training epoch for the corresponding subset.



 Algorithm 1: SpecCoder Two-Stage Training
 1 Specification-Guide SFT Stage
   Input: Pre-trained policy 𝜋𝜃 init ; Generation dataset Dgen
 2 𝜃 ← 𝜃 init ;
 3 for epoch = 1 to 𝐸 SFT do
 4     BSFT ← Shuffle(Dgen );
 5     for mini-batch 𝐵 ⊂ BSFT do
 6         𝜃 ← 𝜃 − 𝜂∇LSFT
 7    𝜃 SFT ← 𝜃
 8 Curriculum Dual-task GRPO Stage
   Input: SFT policy 𝜋𝜃 SFT ; Subsets {(𝑆 𝑘 , 𝐸 𝑘 )}3𝑘=1 containing easy, medium,
           and hard partitions of Dgen ∪ Ddisc
 9 𝜃 0 ← 𝜃 SFT ;
10 for phase 𝑘 = 1, 2, 3 do
11     𝜃 ← 𝜃 𝑘−1 Reset optimizer state;
12     B𝑘 ← Shuffle(𝑆 𝑘 )
13     for epoch = 1 to 𝐸 𝑘 do
14         for mini-batch 𝐵 ⊂ B𝑘 do
15              for prompt 𝑥𝑖 ∈ 𝐵 do
                                            (𝑔)
16                  Sample 𝐺 responses {𝑦𝑖 }𝐺    𝑔=1 ∼ 𝜋 𝜃 (· | 𝑥𝑖 );
                                             (𝑔)
 17                   Compute rewards {𝑟𝑖 }𝐺𝑔=1 via execution or spec
                       matching;
                                                           (𝑔)
 18                   Compute group-relative advantages 𝐴ˆ 𝑖 ;
 19                𝜃 ← 𝜃 + 𝜂∇LGRPO
20       𝜃𝑘 ← 𝜃
      Output: Final optimized policy 𝜋𝜃 3



                                             40
Appendix E. Reproducibility and Artifact Availability
    We use a random seed of 42 for the main training and evaluation exper-
iments. The exact training and evaluation samples, together with their task
identifiers, are publicly released to reproduce the data splits used in our ex-
periments. The code and more information are publicly available at https:
//github.com/yixuanli1230/SpecCoder.




                                      41
References
 [1] M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. D. O. Pinto, J. Kaplan, H. Edwards,
     Y. Burda, N. Joseph, G. Brockman, et al., Evaluating large language models
     trained on code, arXiv preprint arXiv:2107.03374 (2021).

 [2] J. Austin, A. Odena, M. Nye, M. Bosma, H. Michalewski, D. Dohan, E. Jiang,
     C. Cai, M. Terry, Q. Le, et al., Program synthesis with large language models,
     arXiv preprint arXiv:2108.07732 (2021).

 [3] D. Hendrycks, S. Basart, S. Kadavath, M. Mazeika, A. Arora, E. Guo,
     C. Burns, S. Puranik, H. He, D. Song, et al., Measuring coding challenge
     competence with apps, in: Thirty-fifth Conference on Neural Information
     Processing Systems Datasets and Benchmarks Track (Round 2), 2021.

 [4] Y. Li, D. Choi, J. Chung, N. Kushman, J. Schrittwieser, R. Leblond, T. Eccles,
     J. Keeling, F. Gimeno, A. Dal Lago, et al., Competition-level code generation
     with alphacode, Science 378 (6624) (2022) 1092–1097.

 [5] M. A. M. Khan, M. S. Bari, X. L. Do, W. Wang, M. R. Parvez, S. Joty,
     Xcodeeval: An execution-based large scale multilingual multitask bench-
     mark for code understanding, generation, translation and retrieval, in: Pro-
     ceedings of the 62nd Annual Meeting of the Association for Computational
     Linguistics (Volume 1: Long Papers), 2024, pp. 6766–6805.

 [6] T. X. Olausson, J. P. Inala, C. Wang, J. Gao, A. Solar-Lezama, Is self-repair
     a silver bullet for code generation?, arXiv preprint arXiv:2306.09896 (2023).

 [7] K. Zhang, Z. Li, J. Li, G. Li, Z. Jin, Self-edit: Fault-aware code editor for code
     generation, in: Proceedings of the 61st Annual Meeting of the Association
     for Computational Linguistics (Volume 1: Long Papers), 2023, pp. 769–787.

 [8] X. Jiang, Y. Dong, L. Wang, Z. Fang, Q. Shang, G. Li, Z. Jin, W. Jiao, Self-
     planning code generation with large language models, ACM Transactions on
     Software Engineering and Methodology 33 (7) (2024) 1–30.

 [9] Y. Dong, X. Jiang, Z. Jin, G. Li, Self-collaboration code generation via
     chatgpt, ACM Transactions on Software Engineering and Methodology 33 (7)
     (2024) 1–38.



                                         42
[10] S. Hong, M. Zhuge, J. Chen, X. Zheng, Y. Cheng, J. Wang, C. Zhang,
     Z. Wang, S. K. S. Yau, Z. Lin, et al., Metagpt: Meta programming for a multi-
     agent collaborative framework, in: The Twelfth International Conference on
     Learning Representations, 2023.

[11] D. Huang, J. M. Zhang, M. Luck, Q. Bu, Y. Qing, H. Cui, Agentcoder:
     Multi-agent-based code generation with iterative testing and optimisation,
     arXiv preprint arXiv:2312.13010 (2023).

[12] N. S. Mathews, M. Nagappan, Test-driven development and llm-based code
     generation, in: Proceedings of the 39th IEEE/ACM International Conference
     on Automated Software Engineering, 2024, pp. 1583–1594.

[13] H. Zhang, W. Cheng, Y. Wu, W. Hu, A pair programming framework for code
     generation via multi-plan exploration and feedback-driven refinement, in:
     Proceedings of the 39th IEEE/ACM International Conference on Automated
     Software Engineering, 2024, pp. 1319–1331.

[14] K. Zhang, G. Li, Y. Dong, J. Xu, J. Zhang, J. Su, Y. Liu, Z. Jin, Codedpo:
     Aligning code models with self generated and verified source code, in: Pro-
     ceedings of the 63rd Annual Meeting of the Association for Computational
     Linguistics (Volume 1: Long Papers), 2025, pp. 15854–15871.

[15] Y. Wang, Y. Wang, D. Guo, J. Chen, R. Zhang, Y. Ma, Z. Zheng, Rl-
     coder: Reinforcement learning for repository-level code completion, in:
     2025 IEEE/ACM 47th International Conference on Software Engineering
     (ICSE), IEEE, 2025, pp. 1140–1152.

[16] Q. Li, X. Dai, X. Li, W. Zhang, Y. Wang, R. Tang, Y. Yu, Codeprm: Execution
     feedback-enhanced process reward model for code generation, in: Findings
     of the Association for Computational Linguistics: ACL 2025, 2025, pp.
     8169–8182.

[17] X. Jiang, Y. Dong, M. Liu, H. Deng, T. Wang, Y. Tao, R. Cao, B. Li, Z. Jin,
     W. Jiao, et al., Coderl+: Improving code generation via reinforcement with
     execution semantics alignment, arXiv preprint arXiv:2510.18471 (2025).

[18] Z. Tian, J. Chen, Aligning requirement for large language model’s code
     generation, arXiv preprint arXiv:2509.01313 (2025).



                                       43
[19] J. Li, R. Bai, Y. Luo, Y. Zhang, W. Yang, Z. Sun, T. Zhao, D. Jin, L. Li,
     Z. Jin, Bridging the gap between user intent and llm: A requirement alignment
     approach for code generation, arXiv preprint arXiv:2604.16198 (2026).

[20] X. Chen, Z. Tao, K. Zhang, C. Zhou, X. Zhang, W. Gu, Y. He, M. Zhang,
     X. Cai, H. Zhao, et al., Revisit self-debugging with self-generated tests
     for code generation, in: Proceedings of the 63rd Annual Meeting of the
     Association for Computational Linguistics (Volume 1: Long Papers), 2025,
     pp. 18003–18023.

[21] Z. Tian, J. Chen, X. Zhang, Fixing large language models’ specification
     misunderstanding for better code generation, in: 2025 IEEE/ACM 47th In-
     ternational Conference on Software Engineering (ICSE), IEEE Computer
     Society, 2025, pp. 645–645.

[22] H. Le, Y. Wang, A. D. Gotmare, S. Savarese, S. C. H. Hoi, Coderl: Mas-
     tering code generation through pretrained models and deep reinforcement
     learning, Advances in Neural Information Processing Systems 35 (2022)
     21314–21328.

[23] J. Liu, Y. Zhu, K. Xiao, Q. Fu, X. Han, W. Yang, D. Ye, Rltf: Reinforcement
     learning from unit test feedback, arXiv preprint arXiv:2307.04349 (2023).

[24] J. Wei, X. Wang, D. Schuurmans, M. Bosma, F. Xia, E. Chi, Q. V. Le,
     D. Zhou, et al., Chain-of-thought prompting elicits reasoning in large lan-
     guage models, Advances in neural information processing systems 35 (2022)
     24824–24837.

[25] X. Chen, M. Lin, N. Schärli, D. Zhou, Teaching large language models to
     self-debug, in: International Conference on Learning Representations, Vol.
     2024, 2024, pp. 8746–8825.

[26] J. Li, G. Li, Y. Li, Z. Jin, Structured chain-of-thought prompting for code
     generation, ACM Transactions on Software Engineering and Methodology
     34 (2) (2025) 1–23.

[27] W. Chen, X. Ma, X. Wang, W. W. Cohen, Program of thoughts prompting:
     Disentangling computation from reasoning for numerical reasoning tasks,
     arXiv preprint arXiv:2211.12588 (2022).



                                       44
[28] H. Han, J. Kim, J. Yoo, Y. Lee, S.-w. Hwang, Archcode: Incorporating
     software requirements in code generation with large language models, in:
     Proceedings of the 62nd Annual Meeting of the Association for Computa-
     tional Linguistics (Volume 1: Long Papers), 2024, pp. 13520–13552.

[29] F. Lin, D. J. Kim, T.-H. Chen, Soen-101: Code generation by emulating soft-
     ware process models using large language model agents, in: 2025 IEEE/ACM
     47th International Conference on Software Engineering (ICSE), IEEE, 2025,
     pp. 1527–1539.

[30] N. Shinn, F. Cassano, A. Gopinath, K. Narasimhan, S. Yao, Reflexion: Lan-
     guage agents with verbal reinforcement learning, Advances in neural infor-
     mation processing systems 36 (2023) 8634–8652.

[31] S. Dou, Y. Liu, H. Jia, E. Zhou, L. Xiong, J. Shan, C. Huang, X. Wang,
     X. Fan, Z. Xi, et al., Stepcoder: improving code generation with reinforce-
     ment learning from compiler feedback, in: Proceedings of the 62nd Annual
     Meeting of the Association for Computational Linguistics (Volume 1: Long
     Papers), 2024, pp. 4571–4585.

[32] S. Yin, Z. Tian, J. Chen, S. Guo, Improving llm code generation
     via requirement-aware curriculum reinforcement learning, arXiv preprint
     arXiv:2605.00433 (2026).

[33] L. Tang, M. Ye, Z. Chu, X. Ren, Z. Liu, L. Bao, H. Ye, An iterative
     test-and-repair framework for competitive code generation, arXiv preprint
     arXiv:2604.05560 (2026).

[34] ISO/IEC/IEEE 29148:2018 Systems and Software Engineering – Life Cycle
     Processes – Requirements Engineering (2018).

[35] IEEE Recommended Practice for Software Requirements Specifications
     (1998).

[36] DeepSeek-AI,      Deepseek-v3-0324, https://huggingface.co/
     deepseek-ai/DeepSeek-V3-0324, model checkpoint, accessed 15
     June 2026 (2025).

[37] T. J. DiCiccio, B. Efron, Bootstrap confidence intervals, Statistical science
     11 (3) (1996) 189–228.


                                       45
[38] B. Hui, J. Yang, Z. Cui, J. Yang, D. Liu, L. Zhang, T. Liu, J. Zhang,
     B. Yu, K. Lu, et al., Qwen2. 5-coder technical report, arXiv preprint
     arXiv:2409.12186 (2024).

[39] E. J. Hu, Y. Shen, P. Wallis, Z. Allen-Zhu, Y. Li, S. Wang, L. Wang,
     W. Chen, Lora: Low-rank adaptation of large language models, arXiv
     preprint arXiv:2106.09685 (2021).

[40] Y. Zheng, R. Zhang, J. Zhang, Y. Ye, Z. Luo, Z. Feng, Y. Ma, Llamafactory:
     Unified efficient fine-tuning of 100+ language models, in: Proceedings of
     the 62nd Annual Meeting of the Association for Computational Linguistics
     (Volume 3: System Demonstrations), Association for Computational Lin-
     guistics, Bangkok, Thailand, 2024.
     URL http://arxiv.org/abs/2403.13372

[41] Z. Shao, P. Wang, Q. Zhu, R. Xu, J. Song, X. Bi, H. Zhang, M. Zhang, Y. Li,
     et al., Deepseekmath: Pushing the limits of mathematical reasoning in open
     language models, arXiv preprint arXiv:2402.03300 (2024).

[42] S. Liu, S. Hegde, S. Cao, A. Zhu, D. Li, T. Griggs, E. Tang, A. Malik,
     K. Hakhamaneshi, R. Liaw, P. Moritz, M. Zaharia, J. E. Gonzalez, I. Stoica,
     Skyrl-sql: Matching gpt-4o and o4-mini on text2sql with multi-turn rl (2025).

[43] T. Y. Zhuo, M. C. Vu, J. Chim, H. Hu, W. Yu, R. Widyasari, I. N. B. Yusuf,
     H. Zhan, J. He, I. Paul, et al., Bigcodebench: Benchmarking code generation
     with diverse function calls and complex instructions, in: International Con-
     ference on Learning Representations, Vol. 2025, 2025, pp. 66602–66656.

[44] X. Du, M. Liu, K. Wang, H. Wang, J. Liu, Y. Chen, J. Feng, C. Sha, X. Peng,
     Y. Lou, Classeval: A manually-crafted benchmark for evaluating llms on
     class-level code generation, arXiv preprint arXiv:2308.01861 (2023).

[45] W. Yuan, R. Y. Pang, K. Cho, X. Li, S. Sukhbaatar, J. Xu, J. Weston,
     Self-rewarding language models, in: Proceedings of the 41st International
     Conference on Machine Learning, 2024, pp. 57905–57923.

[46] S. Zhang, X. Liu, X. Zhang, J. Liu, Z. Luo, S. Huang, Y. Gong, Process-
     based self-rewarding language models, in: Findings of the Association for
     Computational Linguistics: ACL 2025, 2025, pp. 18097–18110.

[47] W. G. Cochran, Sampling techniques, john wiley & sons, 1977.

                                       46
[48] J. R. Landis, G. G. Koch, The measurement of observer agreement for
     categorical data, biometrics (1977) 159–174.




                                  47
