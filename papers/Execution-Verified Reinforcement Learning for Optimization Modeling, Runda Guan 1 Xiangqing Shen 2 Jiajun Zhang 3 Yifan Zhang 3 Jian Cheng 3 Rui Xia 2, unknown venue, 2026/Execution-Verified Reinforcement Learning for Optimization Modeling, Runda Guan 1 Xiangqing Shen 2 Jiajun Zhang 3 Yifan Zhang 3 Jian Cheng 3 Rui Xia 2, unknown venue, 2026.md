                                                Execution-Verified Reinforcement Learning for Optimization Modeling


                                                       Runda Guan 1 Xiangqing Shen 2 Jiajun Zhang 3 Yifan Zhang 3 Jian Cheng 3 Rui Xia 2


                                                                   Abstract                                   ical program—is challenging and highly specialized (Xiao
                                               Automating optimization modeling with LLMs is                  et al., 2025; Ramamonjison et al., 2021). It requires careful
                                               a promising path toward scalable decision intelli-             interpretation of the problem description and precise mathe-
                                               gence, but existing approaches either rely on agen-            matical formalization under solver constraints. As a result,
                                               tic pipelines built on closed-source LLMs with                 reliably generating correct, solver-compatible formulations
arXiv:2604.00442v1 [cs.AI] 1 Apr 2026




                                               high inference latency, or fine-tune smaller LLMs              from natural language remains challenging and often still
                                               using costly process supervision that often over-              requires human experts.
                                               fits to a single solver API. Inspired by reinforce-            Recent advances in large language models
                                               ment learning with verifiable rewards, we pro-                 (LLMs) (Grattafiori et al., 2024) for code generation
                                               pose Execution-Verified Optimization Modeling                  and logical reasoning have opened new avenues for
                                               (EVOM), an execution-verified learning framework               automating optimization modeling. Existing work largely
                                               that treats a mathematical programming solver                  follows two directions. First, prompting-based meth-
                                               as a deterministic, interactive verifier. Given                ods (AhmadiTeshnizi et al., 2024; Xiao et al., 2024) build
                                               a natural-language problem and a target solver,                agentic systems with multi-turn interaction, reflection,
                                               EVOM generates solver-specific code, executes                  and self-correction to improve accuracy and executability.
                                               it in a sandboxed harness, and converts execu-                 While effective, these systems commonly depend on closed-
                                               tion outcomes into scalar rewards, optimized with              source models and incur substantial inference latency due
                                               GRPO and DAPO in a closed-loop generate–                       to multi-round prompting. Second, training-based methods
                                               execute–feedback–update process. This outcome-                 fine-tune smaller LLMs to enable efficient, low-cost
                                               only formulation removes the need for process-                 inference. Yet, to handle harder instances and improve
                                               level supervision, and enables cross-solver gen-               reliability, many of these methods increasingly rely on
                                               eralization by switching the verification environ-             curating or synthesizing datasets with fine-grained process
                                               ment rather than reconstructing solver-specific                supervision—including explicit intermediate steps such as
                                               datasets. Experiments on NL4OPT, MAMO,                         variable definitions, derivations, and reference code (Huang
                                               IndustryOR, and OptiBench across Gurobi,                       et al., 2025a; Wu et al., 2025; Lu et al., 2025).
                                               OR-Tools, and COPT show that EVOM matches
                                               or outperforms process-supervised SFT, supports                Although richer annotations can improve performance,
                                               zero-shot solver transfer, and achieves effective              this paradigm has two major drawbacks. First, process-
                                               low-cost solver adaptation by continuing training              level supervision is expensive, since collecting high-quality
                                               under the target solver backend.                               intermediate-step annotations is difficult. Second, it tends
                                                                                                              to generalize poorly across solvers. In practice, solver APIs
                                                                                                              differ substantially in modeling constructs and programming
                                        1. Introduction                                                       interfaces. Consequently, models trained to imitate refer-
                                                                                                              ence code for a single solver can overfit solver-specific syn-
                                        Operations research is widely used in supply chains, energy           tactic patterns, and may fail when the solver changes (e.g.,
                                        systems, and finance to support decision-making (Eskandar-            migrating from Gurobi to OR-Tools), even if the under-
                                        pour et al., 2015; Skolfield & Escobedo, 2022; Markowitz,             lying mathematical model is essentially the same. Adapting
                                        1952). However, optimization modeling—translating a nat-              to a new solver then typically requires costly solver-specific
                                        ural language, real-world problem into a correct mathemat-            dataset reconstruction and retraining.
                                           1
                                             School of Computer Science and Engineering, Nanjing Uni-         To address these limitations, we draw inspiration from rein-
                                        versity of Science and Technology 2 School of Intelligence Sci-       forcement learning with verifiable rewards (RLVR) (Wen
                                        ence and Technology, Nanjing University 3 Institute of Automa-
                                        tion, Chinese Academy of Sciences. Correspondence to: Rui Xia         et al., 2025), which shows that outcome-level, verifiable
                                        <rxia@nju.edu.cn>.                                                    feedback can elicit complex reasoning without expensive
                                                                                                              process supervision. Optimization modeling naturally fits
                                        Preprint. April 2, 2026.

                                                                                                          1
                              Execution-Verified Reinforcement Learning for Optimization Modeling

                                                             Previous Methods
                             Prompting -based                                                         Training-based

            P                         Rea   soning                                    PPP                        🔥Smaller LLM           Gurobi
                                                             Solver
           Problem                                                                                                                 ❌
                                       Self-correc)on                                                               SFT                OR-Tools
                                                         Execu3on                                LLM Synthesis
                                                                                                                            Process
                              ···       Feedback                             Human Annota*on                                Supervision
           Answer
                                    Rely on closed-source                                             High annotation cost and
                                    powerful LLMs                                                     poor cross-solver generalization

                                              Execution-Verified Optimization Modeling (EVOM)
            Cold-Start SFT                                                                                                Update
          PPP                                                       A group of outputs
                                                                                           ···                   Group-rela=ve Advantages
                                Policy LLM
                                               🔥 Generate         <think>
                                                                  <think>......</think>
                                                                    <think>
                                                                                </think>
                                                                               ... </think>
                                                                  <code>
                                                                  <code>··· </code>
                                                                                 </code>
                                                                    <code>······ </code>                                   Reward Modeling
          P                                                                                                                       Format
                                                                                                       ···
                                                            ...                                                                  Outcome
                             Solver Gurobi COPT OR-Tools                        Execute                      Feedback           Correctness



                      Figure 1. Comparison of Execution-Verified Optimization Modeling with previous methods.


this paradigm because a mathematical programming solver                      adaptation: to target a new solver, we continue the same
is an automated verifier. Generated programs can be de-                      execution-verified learning loop under the target solver back-
terministically evaluated via compilation success, solution                  end, avoiding solver-specific dataset reconstruction while
feasibility, and the correctness of the final objective value.               letting the new solver’s feedback drive rapid adaptation.
This solver-as-verifier property enables closed-loop learning
                                                                             We conduct systematic experiments on NL4OPT (Rama-
from execution feedback, without relying on intermediate-
                                                                             monjison et al., 2021), MAMO (Huang et al., 2025b), In-
step annotations or reference code.
                                                                             dustryOR (Huang et al., 2025a), and OptiBench (Yang
Based on this insight, we propose Execution-Verified Opti-                   et al., 2025). Across three representative solvers—Gurobi,
mization Modeling (EVOM), an execution-verified learning                     OR-Tools, and COPT—we train EVOM with GRPO and
framework that learns optimization modeling from outcome                     DAPO. Our main contributions are summarized as follows:
supervision alone. Given a problem description q and a
target solver s, EVOM generates solver-specific code, ex-                       • EVOM works without process supervision. Using
ecutes it in a sandboxed harness, and converts the execu-                         only outcome supervision, EVOM matches or outper-
tion outcome into a scalar reward. Training then follows                          forms process-supervised SFT across benchmarks.
a simple closed loop: generate–execute–feedback–update
(Figure 1). Crucially, our framework bypasses the need                          • EVOM enables zero-shot solver transfer. Models
for intermediate-step traces or reference programs by uti-                        trained with execution-verified RL on Gurobi trans-
lizing only problem–answer pairs, where solver execution                          fer to OR-Tools in a zero-shot manner and outper-
outcomes serve as reward signals to align natural language                        form SFT-based transfer.
with mathematical logic through trial and error.
                                                                                • EVOM supports low-cost solver adaptation via en-
This paradigm yields two immediate benefits. First, it lowers                     vironment switching. By switching only the execu-
the data barrier by replacing costly process supervision with                     tion backend and performing the same learning loop,
answer-level supervision plus execution feedback. Second,                         EVOM adapts effectively to a new solver without solver-
it provides a practical path to cross-solver generalization                       specific dataset reconstruction, achieving strong per-
and adaptation by treating the solver as part of the verifica-                    formance on the target solver.
tion environment. We distinguish two settings. (i) Zero-shot
solver transfer: a policy trained with execution feedback                    2. Related Work
from a source solver can be directly evaluated on a target
solver by switching only the solver label and execution back-                In recent years, leveraging large language models (LLMs)
end, without any parameter updates. (ii) Low-cost solver                     to automate optimization modeling has become an active
                                                                             research direction (Xiao et al., 2025). Early progress in

                                                                         2
                             Execution-Verified Reinforcement Learning for Optimization Modeling

this line of work was driven by NL4OPT competition (Ra-                  tion environment rather than reconstructing solver-specific
mamonjison et al., 2021; 2022). A series of benchmarks                   datasets. To the best of our knowledge, this is the first work
have since been introduced, including OptiBench (Yang                    to investigate cross-solver generalization under outcome-
et al., 2025) for diverse optimization problem types,                    only, execution-verified training for optimization modeling.
MAMO (Huang et al., 2025b) for evaluating mathemati-
cal modeling ability, and IndustryOR (Huang et al., 2025a)               3. Execution-Verified Learning for
for bringing in industrially grounded scenarios.
                                                                            Solver-Conditioned Optimization Modeling
Existing methods largely fall into two paradigms.
Prompting-based approaches (AhmadiTeshnizi et al., 2024;                 We present Execution-Verified Optimization Modeling
Xiao et al., 2024; Liu et al., 2025; Shi et al., 2025; Wei et al.,       (EVOM), an execution-verified framework for solver-
2022; Madaan et al., 2023; Shinn et al., 2023; Ye et al.,                conditioned optimization modeling. As illustrated in Fig-
2024; Romera-Paredes et al., 2024) build agentic systems on              ure 1, EVOM iterates through a generate–execute–feedback–
top of closed-source LLMs. While effective, their reliance               update loop: given a natural-language problem q and
on closed-source LLMs typically results in high inference                target solver s, the policy first generates a group of
cost. Supervised fine-tuning (SFT) approaches instead train              <think>+<code> responses, which are then executed in
smaller open-source LLMs with intermediate-step traces                   a sandboxed harness to obtain deterministic outcomes. By
that include variable definitions, formula derivations, and              utilizing outcome-only supervision from problem–answer
reference code. ORLM (Huang et al., 2025a) proposed                      pairs (q, a), the framework evaluates both format and cor-
the OR-Instruct data synthesis pipeline, and subsequent                  rectness to assign rewards, subsequently updating the policy
works (Wu et al., 2025; Lu et al., 2025; Jiang et al., 2025;             via group-relative advantages. This closed-loop design en-
Astorga et al., 2025; Zhou et al., 2025) further improve                 ables the model to align natural language with mathematical
dataset construction and training recipes. However, these                logic through trial and error, bypassing the need for interme-
methods face two major challenges: the high cost of process              diate reasoning traces or reference programs. Algorithm 1
supervision and the difficulty of cross-solver generalization.           in Appendix A summarizes the complete training procedure.

RL with verifiable rewards (RLVR) has recently proven ef-                3.1. Solver-Conditioned Objective
fective in tasks with objective verifiable feedback, allowing
training without human preference labels or learned reward               Data and outcomes. Let D = {(q, a)} be a dataset of
models. DeepSeek-R1 (Guo et al., 2025) shows that such                   problem–answer pairs, where q is a natural-language prob-
verifiable signals can elicit stronger multi-step reasoning,             lem and a is the ground-truth outcome. We represent a
and follow-up work (Wen et al., 2025; Jin et al., 2025) fur-             as either (i) a real-valued optimal objective a ∈ R for
ther supports that verifiability implicitly promotes correct             instances with a finite optimum, or (ii) a special symbol
reasoning behaviors. Algorithmically, GRPO (Shao et al.,                 a = ⊥ for non-numeric outcomes such as UNBOUNDED or
2024) performs critic-free optimization via within-group re-             INFEASIBLE.
ward normalization, while DAPO (Yu et al., 2025) mitigates
entropy collapse in long-chain training through asymmetric               Solvers. Let S denote the set of supported solvers (e.g.,
clipping.                                                                Gurobi, OR-Tools, COPT). For each solver s ∈ S,
Inspired by RLVR, a small number of recent efforts have                  let Σs be the finite set of solver status labels exposed by
begun to explore reinforcement learning for optimization                 its standard API, such as OPTIMAL, INFEASIBLE, and
modeling. Solver-Informed RL (Chen et al., 2025) is a rep-               UNBOUNDED.
resentative pioneer that applies RLVR to this setting, intro-
ducing a solver-feedback-driven data synthesis pipeline to               Conditioning context. We formalize optimization mod-
construct high-quality training samples. OR-R1 (Ding et al.,             eling as a solver-conditioned code-generation policy. For a
2025) studies test-time group-relative policy optimization,              target solver s ∈ S, the conditioning context is
improving formulation quality via inference-time policy
updates and achieving strong results with less synthesized                                        x = (q, s).                      (1)
data. In contrast, our work makes two complementary con-
tributions. First, we show that optimization modeling can
be learned from outcome supervision alone without costly                 Policy outputs. A policy πθ (y | x) generates a structured
process-level traces, by treating the solver as an objective             output
verifier through execution feedback. Second, we systemati-                                  y = (ythink , ycode ),                 (2)
cally study cross-solver generalization in this setting, where
adapting to a new solver reduces to switching the verifica-              where ythink is a non-executable reasoning trace and ycode
                                                                         is solver-specific executable code.

                                                                     3
                            Execution-Verified Reinforcement Learning for Optimization Modeling

Execution environment. For each solver s, an execution                 • c ∈ {0, 1} is the execution flag, equal to 1 iff the pro-
environment Es deterministically executes ycode and returns              gram is successfully interpreted and runs to completion
an observation:                                                          without raising exceptions (including syntax, import,
                     o = Es (ycode ).                   (3)              and runtime errors).

Execution-verified objective. We learn πθ by maximiz-                  • σ ∈ Σs is the solver status returned by solver s (e.g.,
ing the expected reward computed from execution feedback                 OPTIMAL, INFEASIBLE, UNBOUNDED).
and outcome supervision:                                               • v ∈ R ∪ {⊥} is the objective value, where v = ⊥ if
                                    h          i                        no valid numeric objective is produced (e.g., infeasi-
    max E(q,a)∼D Es∼p(s) Ey∼πθ (·|x) R y, o; a , (4)                     ble/unbounded, missing objective, or parse failure).
     θ

where x = (q, s), o = Es (ycode ), p(s) is the solver sam-             • ℓ is the raw execution log (stdout/stderr and solver
pling distribution (uniform over S unless otherwise stated),             logs), retained for debugging and error analysis.
and R(·) is defined in Section 3.4.
                                                                     This standardization makes reward computation determin-
3.2. Solver-Conditioned Output Protocol                              istic and solver-agnostic. Moreover, it induces a natural
                                                                     execution hierarchy (runs → status informative → numeric
To make execution signals reliable, we enforce a strict,
                                                                     value available), which we exploit in our reward design and
machine-parseable output schema. Each model response
                                                                     policy optimization (Section 3.5).
must contain exactly one <think> block followed by ex-
actly one <code> block:
                                                                     3.4. Execution-Verified Reward
            y ≡ <think> ythink </think>                              Given the standardized execution observation o from Sec-
                                                          (5)
                 <code> ycode </code>.                               tion 3.3, we define a scalar reward that combines (i) a
                                                                     lightweight format regularization term to stabilize parsing
At runtime, a deterministic parser extracts only the unique          and execution, and (ii) an outcome-only supervision term
<code> block and executes it; the <think> block is never             grounded in solver verification:
executed and does not affect execution outcomes. Outputs
that violate the schema (e.g., missing tags, multiple blocks,                    R(y, o; a) = rfmt (y) + rans (o; a).         (7)
or wrong order) are treated as non-executable and receive
no credit from execution-based rewards.                              Here, rfmt depends only on the raw model output y and is
                                                                     evaluated prior to execution, while rans depends solely on
As illustrated in Figure 5, the prompt specifies the target
                                                                     the solver-verified outcome o and the ground-truth answer
solver via the placeholder {solver}, which is instantiated
                                                                     a. Crucially, no intermediate reasoning traces or reference
as a plain string identifier such as Gurobi, OR-Tools, or
                                                                     programs are used in reward computation.
COPT. Importantly, the prompt provides no solver-specific
exemplars, step-by-step modeling templates, or reference
                                                                     3.4.1. F ORMAT R EWARD
codes. Thus, the model must infer solver-appropriate API
usage through interaction with the execution environment.            The format reward rfmt enforces the solver-conditioned
For fair comparison, we use the same output protocol, pars-          output protocol in Eq. (5), ensuring that model outputs are
ing rules, and prompt format for all methods.                        reliably parseable and executable. We combine a soft tag-
                                                                     count check with a hard regular-expression match:
3.3. Sandboxed Execution Harness                                                       X
                                                                            rfmt (y) =     wt · I[count(t, y) = 1]
We evaluate each candidate program by executing it in a
                                                                                       t∈T                                   (8)
sandboxed harness that maps heterogeneous solver behav-
iors to a unified, machine-readable observation. Given the                             + wm · I[Match(y, pattern)],
extracted code ycode and the designated solver s, the har-
                                                                     where T = {<think>, </think>, <code>, </code>},
ness runs ycode under strict resource constraints (10 seconds
                                                                     wt , wm ≥ 0 are fixed weights, and pattern validates
timeout; 2 GB memory cap) and invokes solver s via its
                                                                     proper ordering and closure of the blocks. The soft
standard Python interface. It captures standard output/error
                                                                     tag-count term provides a dense learning signal during early
and solver logs, and consolidates them into a structured
                                                                     training, while the hard regex constraint strictly enforces
observation
                                                                     the required structure. Together, they substantially reduce
                      o = (c, σ, v, ℓ),                    (6)
                                                                     malformed outputs and stabilize downstream execution
where:                                                               across solvers.

                                                                 4
                            Execution-Verified Reinforcement Learning for Optimization Modeling

3.4.2. O UTCOME C ORRECTNESS R EWARD                                where µR , σR are the empirical mean/std over the group and
                                                                    δA is a small constant. The GRPO objective is
The outcome reward is the core supervision signal derived                                         "    G
solely from solver-verified outcomes. Let a denote the                                              1 X
ground-truth outcome. Following Section 3.1, a is either (i)                 JGRPO (θ) = Ex,{yi }         (min(ρi Ai ,
                                                                                                    G i=1
a numeric optimal objective a ∈ R, or (ii) a discrete status                                                               (12)
label a ∈ Σ (e.g., INFEASIBLE or UNBOUNDED).                                           clip(ρi , 1 − ϵ, 1 + ϵ)Ai )
                                                                                       −β DKL (πθ ∥ πref ))] ,
Numerical closeness. For numeric outcomes, we define a              where ρi = πθ (yi | x)/πθold (yi | x).
tolerance-based predicate:
                                                                    3.5.2. D ECOUPLED C LIPPING AND DYNAMIC
  IsClose(v, a) ⇐⇒          |v − a| < ϵabs
                                                                          S AMPLING (DAPO)
                                                      (9)
                                                  
                                   |v − a|                          DAPO (Yu et al., 2025) removes the KL penalty, uses asym-
                            ∨                < ϵrel ,
                                 max(|a|, δ)                        metric clipping to mitigate entropy collapse, and applies
                                                                    dynamic sampling to skip uninformative groups (e.g., all
                                                                    failures):
with ϵabs = ϵrel = 10−4 and δ = 10−12 to avoid division                                           "
by zero.                                                                                               G
                                                                                                    1 X        
                                                                             JDAPO (θ) = Ex,{yi }          min ρi Âi ,
                                                                                                    G i=1                 (13)
Reward. Let Σnums    ⊆ Σs denote solver statuses un-                                                                 i
der which a valid numeric objective is returned (e.g.,                                 clip(ρi , 1 − ϵl , 1 + ϵh )Âi ,
OPTIMAL). We define:
                                                                    where ϵh > ϵl and Âi is computed analogously to Ai under
                                                                   DAPO’s sampling rule.
                 c = 1 ∧ a ∈ R ∧ σ ∈ Σnum
                                       s   ∧ v ̸= ⊥
              1,
              
                   ∧ IsClose(v, a),
              
                                                                   3.6. Cross-Solver Adaptation and Transfer
 rans (o; a) = 1, c = 1 ∧ a ∈ Σ ∧ σ = a,
              
              
              
                                                                   A key advantage of EVOM is its ability to generalize across
              0, otherwise.                                        different solver backends without requiring solver-specific
                                                         (10)       reference datasets. We study this generalization from two
This design rewards the model only when it generates ex-            perspectives:
ecutable code whose solver-verified outcome matches the
ground truth. While rans is intentionally sparse, we mitigate       Zero-shot transfer. We evaluate the policy’s ability to
sparsity using group-based relative advantages and dynamic          transfer to a target solver stgt without any additional train-
sampling in policy optimization (Section 3.5).                      ing. This setting examines whether the models trained with
                                                                    execution-verified feedback capture universal mathemati-
3.5. Critic-Free Policy Optimization with Execution                 cal modeling principles that generalize beyond the specific
     Rewards                                                        syntactic requirements of the source solver ssrc .

We instantiate the “update” step of the generate–execute–           Low-cost adaptation via environment switching. Our
feedback–update loop by optimizing πθ with critic-free pol-         framework also supports rapid adaptation to new solvers
icy optimization. Given deterministic execution rewards             through environment switching. By transitioning the
R(y, o; a), we avoid training a separate value model, which         generate–execute–feedback–update loop to a target envi-
is well-suited to sparse, verifiable signals from sandboxed         ronment Estgt , the policy can be fine-tuned directly against
execution.                                                          the feedback of stgt . This avoids the need for constructing
                                                                    new solver-specific reference datasets, allowing the policy to
3.5.1. G ROUP R ELATIVE P OLICY O PTIMIZATION                       align with the target solver’s specific APIs and error modes
       (GRPO)                                                       using only outcome supervision.
GRPO (Shao et al., 2024) standardizes rewards within a
group. For each x = (q, s), we sample {yi }G
                                           i=1 ∼ πθold (· |         4. Experiments
x), execute them, and obtain {Ri }G
                                  i=1 . Group-relative ad-
vantages are                                                        4.1. Experimental Settings

                            Ri − µR                                 Datasets. We construct the training set D based on OR-
                     Ai =           ,                   (11)        Instruct-3K from ORLM (Huang et al., 2025a), which
                            σR + δA

                                                                5
                              Execution-Verified Reinforcement Learning for Optimization Modeling

                       Table 1. Performance comparison on optimization modeling benchmarks using Gurobi.

                 Model                   OptiBench      NL4OPT         MAMO-E         MAMO-C       IndustryOR      Avg.
                 Prompting-based Models
                 DeepSeek-R1-0528       76.21             86.12            79.45        74.88          54.00       73.73
                 OpenAI o1              71.40             87.10            87.60        72.10          40.00       71.64
                 GPT-4o (Standard)      42.30             70.30            84.30        58.80          27.00       56.54
                 GPT-4o (CoT)           42.00             71.60            84.80        59.90          29.00       57.46
                 GPT-4o (CoE)           43.20             76.40            85.70        64.00          34.00       60.66
                 OptiMUS                45.80             82.00            85.10        64.90          34.00       62.36
                 Training-based Models (Qwen2.5-7B)
                 Base Model             41.19       55.10                  65.95        28.43          21.00       42.33
                 ORLM (SFT)             60.96       84.89                  88.34        35.71          27.00       59.38
                 EVOM (GRPO)            62.95       84.08                  88.19        34.28          31.00       60.10


contains 3,000 optimization problems. To align with                        Implementation Details. Following the solver-as-verifier
our outcome-only formulation, we retain only the natural-                  paradigm, we utilize three representative mathematical pro-
language descriptions q and extract the ground-truth out-                  gramming solvers: Gurobi (Gurobi Optimization, LLC,
comes a (optimal objective values) by executing the original               2024), OR-Tools (Perron & Furnon, 2024), and COPT (Ge
reference programs. All intermediate process-level anno-                   et al., 2023). Our main experiments focus on Gurobi and
tations (e.g., variable derivations and reference code) are                OR-Tools, while results for COPT are reported in the con-
discarded during training. We evaluate EVOM across four                    text of cold-start adaptation (see Appendix I). For training-
representative benchmarks: NL4OPT (Ramamonjison et al.,                    based models, we use Qwen2.5-7B (Yang et al., 2024) as
2021), MAMO (Huang et al., 2025b), IndustryOR (Huang                       the base policy πθ , and report additional small-scale experi-
et al., 2025a), and OptiBench (Yang et al., 2025). Notably,                ments in the Appendix G.
for the MAMO ComplexLP subset, we identified and cor-
rected erroneous reference answers in several Traveling                    4.2. Main Results
Salesman Problem instances where the original programs
provided sub-optimal results.                                              Table 1 demonstrates the effectiveness of outcome-only su-
                                                                           pervision in optimization modeling. By utilizing the solver-
Baseline Methods. We compare EVOM against two dis-                         as-verifier paradigm, EVOM achieves competitive perfor-
tinct paradigms. Prompting-based Models include state-of-                  mance across all benchmarks, matching or even surpassing
the-art closed-source reasoning models such as DeepSeek-                   the ORLM (SFT) baseline that was trained on process-level
R1 (Guo et al., 2025) and OpenAI o1 (OpenAI, 2024), as                     annotations. Notably, our framework exhibits an advan-
well as various strategies applied to GPT-4o (Hurst et al.,                tage on more challenging datasets, such as IndustryOR
2024), including Standard Prompting, Chain-of-Thought                      and OptiBench. These results suggest that, in addition to
(CoT) (Wei et al., 2022), Chain-of-Experts (CoE) (Xiao                     process-level supervision, Execution-Verified Optimization
et al., 2024), and the agentic system OptiMUS (Ahma-                       Modeling represents a promising direction for optimiza-
diTeshnizi et al., 2024). We compare against ORLM (Huang                   tion modeling, especially in domains where objective and
et al., 2025a), which represents the process-level supervi-                deterministic feedback is available to guide the alignment
sion paradigm via supervised fine-tuning (SFT) on the full                 of natural language with mathematical logic. We further
OR-Instruct dataset.                                                       conduct a human evaluation on 500 OptiBench samples to
                                                                           assess reasoning and implementation quality, with details
                                                                           provided in Appendix E.
Evaluation Metric. We report Accuracy, defined as the
fraction of test instances where the predicted outcome v
from the execution observation o matches the ground-truth a.               4.3. Ablation Study
Following previous work (Huang et al., 2025a), a prediction                This ablation study investigates the effect of explicit rea-
v is counted as correct if it satisfies a relative tolerance ϵeval :       soning in outcome-supervised learning. Specifically, we
                                                                           examine whether outcome supervision suffices for a direct
                       |v − a|
                                  ≤ ϵeval ,                   (14)         problem-to-code mapping, or if an explicit reasoning step
                      max(|a|, δ)                                          is essential for successful alignment. To this end, we com-
We set ϵeval = 0.05 for all results in the main paper, and                 pare the standard EVOM against a reasoning-free variant that
more stringent evaluations (ϵeval = 10−4 ) are provided in                 bypasses the <think> block and generates code directly.
Appendix F, Appendix L and Appendix G.

                                                                       6
                                                     Execution-Verified Reinforcement Learning for Optimization Modeling

Table 2. Zero-Shot Solver Transfer to OR-Tools. Accuracy of models evaluated on the target solver (stgt : OR-Tools) after being
trained on the source solver (ssrc : Gurobi). Unlike process-supervised SFT (ORLM), which overfits to source-specific syntax and leads
to performance collapse, EVOM (GRPO) maintains robust transferability.

                                   Model                       Supervision                  OptiBench       NL4OPT                       MAMO-E              MAMO-C         IndusOR
                                   Base (Qwen2.5-7B)                  —                        40.86          59.18                           53.83             18.48         20.00
                                   ORLM (SFT)                      P ROCESS                     3.49          4.89                             0.00             1.42          6.00
                                   EVOM (GRPO)                     A NSWER                     54.31          77.55                           84.81             22.27         24.00
                                   Difference (∆)                                              +50.82        +72.66                           +84.81           +20.85        +18.00

Table 3. Adaptive specialization across diverse solver environments. EVOM drives significant performance gains by aligning the policy
with the designated solver’s feedback loop.

                                         Solver                                 OptiBench          NL4OPT           MAMO-E                       MAMO-C              IndustryOR
                                         Gurobi
                                           Qwen2.5-7B                              41.19            55.10                       65.95              28.43                 21.00
                                           After EVOM (GRPO)                       62.95            84.08                       88.19              34.28                 31.00
                                           Absolute Gain (∆)                      +21.76            +28.98                     +22.24              +5.85                +10.00
                                         OR-Tools
                                           Qwen2.5-7B                             40.86              59.18                      53.83                  18.48             20.00
                                           After EVOM (GRPO)                      52.49              77.14                      82.82                  16.11             31.00
                                           Absolute Gain (∆)                      +11.63            +17.96                     +28.99                  -2.37            +11.00



                                                                        Base (w/ think)
                                                                                                                               80                                                             GRPO
                  80                                                    Base (w/o think)
                                                                                                                                                                                              DAPO
                                                                        RL (w/ think)
                                                                                                                Accuracy (%)




                                                                        RL (w/o think)                                         60
                  60
   Accuracy (%)




                                                                                                                               40

                  40                                                                                                           20

                                                                                                                                0
                  20
                                                                                                                                           nch            PT         -  E        -C               OR
                                                                                                                                      tiB
                                                                                                                                          e             4O        MO          MO           stry
                                                                                                                                    Op             NL           MA          MA        Ind
                                                                                                                                                                                          u
                  0
                               h          PT          E         C            OR               g.             Figure 3. GRPO vs. DAPO under identical training setup. Accu-
                           enc        4O          MO
                                                     -
                                                            MO
                                                               -                           Av
                       tiB          NL                                   stry
                  Op                           MA         MA        Ind
                                                                        u                                    racy curves across benchmarks are nearly identical, indicating low
                                                                                                             sensitivity to the optimizer choice in execution-verified training.
Figure 2. Impact of explicit reasoning on EVOM performance
across different benchmarks.

                                                                                                             4.4. Analysis of Cross-Solver Generalization
                                                                                                             We evaluate the cross-solver generalization of EVOM from
As shown in Figure 2, removing the reasoning block triggers
                                                                                                             two perspectives as defined in Section 3.6: zero-shot solver
a significant performance collapse across most benchmarks.
                                                                                                             transfer and low-cost adaptation via environment switching.
This degradation is particularly acute on logically demand-
ing tasks such as IndustryOR and MAMO-C, indicating that
                                                                                                             4.4.1. Z ERO -S HOT S OLVER T RANSFER
a direct mapping from problem descriptions to code often
fails to capture complex optimization logic. In contrast,                                                    To examine whether EVOM elicits universal mathematical
on the simpler MAMO-E subset, the absence of reasoning                                                       modeling principles, we evaluate a policy trained exclusively
yields a marginal performance gain, suggesting that explicit                                                 on Gurobi (ssrc ) by directly switching the execution back-
reasoning might introduce unnecessary overhead or “over-                                                     end to OR-Tools (stgt ) without any parameter updates.
thinking” for trivial instances. These results affirm that                                                   This setting tests the model’s ability to decouple underlying
within the RLVR framework, the <think> block acts not                                                        mathematical logic from solver-specific syntactic require-
just as a post-hoc explanation, but as an essential internal                                                 ments. As shown in Table 2, EVOM demonstrates superior
workspace: outcome-level rewards optimize code genera-                                                       zero-shot transferability compared to the SFT-based base-
tion indirectly by reinforcing the intermediate logical steps                                                line. While the process-supervised ORLM suffers from a
that are necessary to reach a verifiable solution.                                                           near-complete collapse on the target solver (e.g., dropping

                                                                                                        7
                             Execution-Verified Reinforcement Learning for Optimization Modeling

to 0.00% accuracy on MAMO-E), EVOM not only preserves                                                                                             50
but often enhances its performance across all benchmarks.
                                                                                       1100
This stark contrast suggests that process-level supervision                                                                                       40




                                                                                                                                                       Accuracy (%)
                                                                        Token Length
often forces the model to mimic specific solver APIs and
code patterns present in the training traces, leading to brittle,                      1000
                                                                                                                                                  30
syntax-dependent policies. In contrast, by optimizing for
outcome-level correctness through verifiable rewards, EVOM                              900                                        Think Length   20
learns to prioritize invariant mathematical structures. This                                                                       Code Length
                                                                                                                                   Accuracy
allows the model to function as a “plug-and-play” optimizer
capable of cross-interface generalization without requiring                                   0        10       20          30      40
specialized fine-tuning for every new solver environment.                                                      Training Step

                                                                        (a) Thinking length increases while code length decreases as accu-
4.4.2. A DAPTATION VIA E NVIRONMENT S WITCHING                          racy improves.
We next evaluate low-cost solver adaptation via environ-                                0.5
ment switching. Starting from the same the Base Model, we
run the identical generate–execute–feedback–update loop                                 0.4
under different verification environments Es . Concretely,



                                                                                Score
switching the solver amounts to changing only the execution                             0.3
backend and the induced observation o = (c, σ, v, ℓ), while
keeping the training data as outcome-only pairs (q, a) and
                                                                                        0.2                                        Soft Format
without constructing solver-specific reference programs.                                                                           Hard Format
                                                                                                                                   Answer Score
Table 3 compares performance before and after execution-
                                                                                              0        10       20          30      40
verified training within each solver environment. We ob-
                                                                                                               Training Step
serve consistent gains across solvers, and the improvement
is particularly pronounced when the base policy is weaker               (b) Format reward saturates early, whereas correctness reward rises
under the target backend. For instance, under EOR-Tools , the           gradually.
policy improves by +28.99% on MAMO-E, indicating that                                  Figure 4. Training dynamics of execution-verified learning.
deterministic execution feedback provides a strong learn-
ing signal for rapidly specializing the code generator to the
target solver’s interface and failure modes. These results              rectness.
support our central claim: adapting to a new solver can be
realized by switching the verification environment, rather
than rebuilding solver-specific supervised datasets.                    5. Conclusion
                                                                        We studied execution-verified learning for solver-
4.5. Sensitivity Analysis of Optimization Algorithms                    conditioned optimization modeling, with the goal of
We test whether EVOM depends on the specific RL optimizer               reducing reliance on expensive process-level supervision
by replacing our default GRPO update with DAPO, keeping                 and improving robustness across solver backends. We
the same data, harness, and training budget. Figure 3 shows             proposed Execution-Verified Optimization Modeling
nearly identical performance across NL4OPT, OptiBench,                  (EVOM), which learns from outcome-only supervision
and MAMO, with only a minor gap on IndustryOR. Thus,                    by treating the solver as a deterministic verifier in a
in execution-verified optimization modeling, the dominant               closed-loop generate–execute–feedback–update process.
factor is solver-verified modeling competence rather than               Across representative benchmarks, EVOM matches or sur-
optimizer choice; GRPO is sufficient in our setting.                    passes process-supervised SFT baselines while producing
                                                                        solver-executable programs under sandboxed verification.
                                                                        We further show that solver changes can be handled via
4.6. Analysis of Training Dynamics
                                                                        environment switching: a policy trained with execution feed-
We analyze how outputs and rewards evolve during training.              back exhibits non-trivial zero-shot transfer to a new solver,
Figure 4(a) shows that thinking length increases while code             and can be effectively adapted by continuing the same
length decreases, suggesting the model shifts budget toward             execution-verified loop under the target backend, avoiding
planning and emits more concise programs. Figure 4(b)                   solver-specific dataset reconstruction. Overall, our results
shows that format rewards saturate early whereas correct-               indicate that deterministic execution feedback provides
ness rewards improve gradually, indicating rapid interface              a practical supervision signal for scalable optimization
compliance followed by slower gains in solver-verified cor-             modeling and lightweight cross-solver transfer.

                                                                    8
                           Execution-Verified Reinforcement Learning for Optimization Modeling

Impact Statement                                                   Grattafiori, A., Dubey, A., Jauhri, A., Pandey, A., Kadian,
                                                                     A., Al-Dahle, A., Letman, A., Mathur, A., Schelten, A.,
This paper introduces EVOM, a framework for automating               Vaughan, A., Yang, A., Fan, A., Goyal, A., Hartshorn,
optimization modeling through execution-verified reinforce-          A., Yang, A., Mitra, A., Sravankumar, A., Korenev,
ment learning. Our work aims to improve the efficiency and           A., Hinsvark, A., Rao, A., Zhang, A., Rodriguez, A.,
scalability of decision intelligence by reducing the cost of         Gregerson, A., Spataru, A., Roziere, B., Biron, B., Tang,
process-level supervision. There are many potential societal         B., Chern, B., Caucheteux, C., Nayak, C., Bi, C., Marra,
consequences of our work, none of which we feel must be              C., McConnell, C., Keller, C., Touret, C., Wu, C., Wong,
specifically highlighted here.                                       C., Ferrer, C. C., Nikolaidis, C., Allonsius, D., Song, D.,
                                                                     Pintz, D., Livshits, D., Wyatt, D., Esiobu, D., Choudhary,
References                                                           D., Mahajan, D., Garcia-Olano, D., Perino, D., Hupkes,
                                                                     D., Lakomkin, E., AlBadawy, E., Lobanova, E., Dinan,
AhmadiTeshnizi, A., Gao, W., and Udell, M. Optimus: Scal-
                                                                     E., Smith, E. M., Radenovic, F., Guzmán, F., Zhang, F.,
  able optimization modeling with (MI)LP solvers and large
                                                                     Synnaeve, G., Lee, G., Anderson, G. L., Thattai, G., Nail,
  language models. In Forty-first International Confer-
                                                                     G., Mialon, G., Pang, G., Cucurell, G., Nguyen, H., Ko-
  ence on Machine Learning, ICML 2024, Vienna, Austria,
                                                                     revaar, H., Xu, H., Touvron, H., Zarov, I., Ibarra, I. A.,
  July 21-27, 2024. OpenReview.net, 2024. URL https:
                                                                     Kloumann, I., Misra, I., Evtimov, I., Zhang, J., Copet, J.,
 //openreview.net/forum?id=YT1dtdLvSN.
                                                                     Lee, J., Geffert, J., Vranes, J., Park, J., Mahadeokar, J.,
Astorga, N., Liu, T., Xiao, Y., and van der Schaar, M. Auto-         Shah, J., van der Linde, J., Billock, J., Hong, J., Lee, J.,
  formulation of mathematical optimization models using              Fu, J., Chi, J., Huang, J., Liu, J., Wang, J., Yu, J., Bitton,
  llms. In Forty-second International Conference on Ma-              J., Spisak, J., Park, J., Rocca, J., Johnstun, J., Saxe, J., Jia,
  chine Learning, ICML 2025, Vancouver, BC, Canada,                  J., Alwala, K. V., Prasad, K., Upasani, K., Plawiak, K., Li,
  July 13-19, 2025. OpenReview.net, 2025. URL https:                 K., Heafield, K., Stone, K., El-Arini, K., Iyer, K., Malik,
  //openreview.net/forum?id=33YrT1j0O0.                              K., Chiu, K., Bhalla, K., Lakhotia, K., Rantala-Yeary,
                                                                     L., van der Maaten, L., Chen, L., Tan, L., Jenkins, L.,
Burkard, R., Dell’Amico, M., and Martello, S. Assign-                Martin, L., Madaan, L., Malo, L., Blecher, L., Landzaat,
  ment Problems. Society for Industrial and Applied                  L., de Oliveira, L., Muzzi, M., Pasupuleti, M., Singh,
  Mathematics, 2012. doi: 10.1137/1.9781611972238.                   M., Paluri, M., Kardas, M., Tsimpoukelli, M., Oldham,
  URL https://epubs.siam.org/doi/abs/10.                             M., Rita, M., Pavlova, M., Kambadur, M., Lewis, M.,
  1137/1.9781611972238.                                              Si, M., Singh, M. K., Hassan, M., Goyal, N., Torabi, N.,
                                                                     Bashlykov, N., Bogoychev, N., Chatterji, N., Zhang, N.,
Chen, Y., Xia, J., Shao, S., Ge, D., and Ye, Y. Solver-              Duchenne, O., Çelebi, O., Alrassy, P., Zhang, P., Li, P.,
  informed RL: grounding large language models for au-               Vasic, P., Weng, P., Bhargava, P., Dubal, P., Krishnan,
  thentic optimization modeling. CoRR, abs/2505.11792,               P., Koura, P. S., Xu, P., He, Q., Dong, Q., Srinivasan,
  2025. doi: 10.48550/ARXIV.2505.11792. URL https:                   R., Ganapathy, R., Calderer, R., Cabral, R. S., Stojnic,
  //doi.org/10.48550/arXiv.2505.11792.                               R., Raileanu, R., Maheswari, R., Girdhar, R., Patel, R.,
                                                                     Sauvestre, R., Polidoro, R., Sumbaly, R., Taylor, R., Silva,
Ding, Z., Tan, Z., Zhang, J., and Chen, T. OR-R1: au-                R., Hou, R., Wang, R., Hosseini, S., Chennabasappa, S.,
  tomating modeling and solving of operations research               Singh, S., Bell, S., Kim, S. S., Edunov, S., Nie, S., Narang,
  optimization problem via test-time reinforcement learn-            S., Raparthy, S., Shen, S., Wan, S., Bhosale, S., Zhang,
  ing. CoRR, abs/2511.09092, 2025. doi: 10.48550/ARXIV.              S., Vandenhende, S., Batra, S., Whitman, S., Sootla, S.,
  2511.09092. URL https://doi.org/10.48550/                          Collot, S., Gururangan, S., Borodinsky, S., Herman, T.,
  arXiv.2511.09092.                                                  Fowler, T., Sheasha, T., Georgiou, T., Scialom, T., Speck-
                                                                     bacher, T., Mihaylov, T., Xiao, T., Karn, U., Goswami, V.,
Eskandarpour, M., Dejax, P., Miemczyk, J.,
                                                                     Gupta, V., Ramanathan, V., Kerkez, V., Gonguet, V., Do,
  and Péton, O.        Sustainable supply chain net-
                                                                     V., Vogeti, V., Albiero, V., Petrovic, V., Chu, W., Xiong,
  work design:      An optimization-oriented review.
                                                                     W., Fu, W., Meers, W., Martinet, X., Wang, X., Wang,
  Omega, 54:11–32, 2015.              ISSN 0305-0483.
                                                                     X., Tan, X. E., Xia, X., Xie, X., Jia, X., Wang, X., Gold-
  doi:     https://doi.org/10.1016/j.omega.2015.01.006.
                                                                     schlag, Y., Gaur, Y., Babaei, Y., Wen, Y., Song, Y., Zhang,
  URL       https://www.sciencedirect.com/
                                                                     Y., Li, Y., Mao, Y., Coudert, Z. D., Yan, Z., Chen, Z.,
  science/article/pii/S0305048315000080.
                                                                     Papakipos, Z., Singh, A., Srivastava, A., Jain, A., Kelsey,
Ge, D., Huangfu, Q., Wang, Z., Wu, J., and                           A., Shajnfeld, A., Gangidi, A., Victoria, A., Goldstand,
 Ye, Y.       Cardinal Optimizer (COPT) user guide.                  A., Menon, A., Sharma, A., Boesenberg, A., Baevski, A.,
  https://guide.coap.online/copt/en-doc, 2023.                       Feinstein, A., Kallet, A., Sangani, A., Teo, A., Yunus, A.,

                                                               9
                         Execution-Verified Reinforcement Learning for Optimization Modeling

Lupu, A., Alvarado, A., Caples, A., Gu, A., Ho, A., Poul-            S., Remez, T., Glaser, T., Best, T., Koehler, T., Robinson,
ton, A., Ryan, A., Ramchandani, A., Dong, A., Franco,                T., Li, T., Zhang, T., Matthews, T., Chou, T., Shaked,
A., Goyal, A., Saraf, A., Chowdhury, A., Gabriel, A.,                T., Vontimitta, V., Ajayi, V., Montanez, V., Mohan, V.,
Bharambe, A., Eisenman, A., Yazdan, A., James, B.,                   Kumar, V. S., Mangla, V., Ionescu, V., Poenaru, V., Mi-
Maurer, B., Leonhardi, B., Huang, B., Loyd, B., Paola,               hailescu, V. T., Ivanov, V., Li, W., Wang, W., Jiang, W.,
B. D., Paranjape, B., Liu, B., Wu, B., Ni, B., Hancock,              Bouaziz, W., Constable, W., Tang, X., Wu, X., Wang, X.,
B., Wasti, B., Spence, B., Stojkovic, B., Gamido, B.,                Wu, X., Gao, X., Kleinman, Y., Chen, Y., Hu, Y., Jia, Y.,
Montalvo, B., Parker, C., Burton, C., Mejia, C., Liu, C.,            Qi, Y., Li, Y., Zhang, Y., Zhang, Y., Adi, Y., Nam, Y., Yu,
Wang, C., Kim, C., Zhou, C., Hu, C., Chu, C.-H., Cai, C.,            Wang, Zhao, Y., Hao, Y., Qian, Y., Li, Y., He, Y., Rait,
Tindal, C., Feichtenhofer, C., Gao, C., Civin, D., Beaty,            Z., DeVito, Z., Rosnbrick, Z., Wen, Z., Yang, Z., Zhao,
D., Kreymer, D., Li, D., Adkins, D., Xu, D., Testuggine,             Z., and Ma, Z. The llama 3 herd of models, 2024. URL
D., David, D., Parikh, D., Liskovich, D., Foss, D., Wang,            https://arxiv.org/abs/2407.21783.
D., Le, D., Holland, D., Dowling, E., Jamil, E., Mont-
gomery, E., Presani, E., Hahn, E., Wood, E., Le, E.-T.,            Guo, D., Yang, D., Zhang, H., Song, J., Wang, P., Zhu, Q.,
Brinkman, E., Arcaute, E., Dunbar, E., Smothers, E., Sun,           Xu, R., Zhang, R., Ma, S., Bi, X., Zhang, X., Yu, X., Wu,
F., Kreuk, F., Tian, F., Kokkinos, F., Ozgenel, F., Cag-            Y., Wu, Z. F., Gou, Z., Shao, Z., Li, Z., Gao, Z., Liu, A.,
gioni, F., Kanayet, F., Seide, F., Florez, G. M., Schwarz,          Xue, B., Wang, B., Wu, B., Feng, B., Lu, C., Zhao, C.,
G., Badeer, G., Swee, G., Halpern, G., Herman, G., Sizov,            Deng, C., Ruan, C., Dai, D., Chen, D., Ji, D., Li, E., Lin,
G., Guangyi, Zhang, Lakshminarayanan, G., Inan, H.,                  F., Dai, F., Luo, F., Hao, G., Chen, G., Li, G., Zhang, H.,
Shojanazeri, H., Zou, H., Wang, H., Zha, H., Habeeb, H.,            Xu, H., Ding, H., Gao, H., Qu, H., Li, H., Guo, J., Li,
Rudolph, H., Suk, H., Aspegren, H., Goldman, H., Zhan,              J., Chen, J., Yuan, J., Tu, J., Qiu, J., Li, J., Cai, J. L., Ni,
H., Damlaj, I., Molybog, I., Tufanov, I., Leontiadis, I.,           J., Liang, J., Chen, J., Dong, K., Hu, K., You, K., Gao,
Veliche, I.-E., Gat, I., Weissman, J., Geboski, J., Kohli,           K., Guan, K., Huang, K., Yu, K., Wang, L., Zhang, L.,
J., Lam, J., Asher, J., Gaya, J.-B., Marcus, J., Tang, J.,           Zhao, L., Wang, L., Zhang, L., Xu, L., Xia, L., Zhang,
Chan, J., Zhen, J., Reizenstein, J., Teboul, J., Zhong, J.,          M., Zhang, M., Tang, M., Zhou, M., Li, M., Wang, M.,
Jin, J., Yang, J., Cummings, J., Carvill, J., Shepard, J.,           Li, M., Tian, N., Huang, P., Zhang, P., Wang, Q., Chen,
McPhie, J., Torres, J., Ginsburg, J., Wang, J., Wu, K., U,           Q., Du, Q., Ge, R., Zhang, R., Pan, R., Wang, R., Chen,
K. H., Saxena, K., Khandelwal, K., Zand, K., Matosich,               R. J., Jin, R. L., Chen, R., Lu, S., Zhou, S., Chen, S., Ye,
K., Veeraraghavan, K., Michelena, K., Li, K., Jagadeesh,             S., Wang, S., Yu, S., Zhou, S., Pan, S., Li, S. S., Zhou, S.,
K., Huang, K., Chawla, K., Huang, K., Chen, L., Garg,               Wu, S., Yun, T., Pei, T., Sun, T., Wang, T., Zeng, W., Liu,
L., A, L., Silva, L., Bell, L., Zhang, L., Guo, L., Yu, L.,         W., Liang, W., Gao, W., Yu, W., Zhang, W., Xiao, W. L.,
Moshkovich, L., Wehrstedt, L., Khabsa, M., Avalani, M.,             An, W., Liu, X., Wang, X., Chen, X., Nie, X., Cheng,
Bhatt, M., Mankus, M., Hasson, M., Lennie, M., Reso,                X., Liu, X., Xie, X., Liu, X., Yang, X., Li, X., Su, X.,
M., Groshev, M., Naumov, M., Lathi, M., Keneally, M.,                Lin, X., Li, X. Q., Jin, X., Shen, X., Chen, X., Sun, X.,
Liu, M., Seltzer, M. L., Valko, M., Restrepo, M., Patel,            Wang, X., Song, X., Zhou, X., Wang, X., Shan, X., Li,
M., Vyatskov, M., Samvelyan, M., Clark, M., Macey,                  Y. K., Wang, Y. Q., Wei, Y. X., Zhang, Y., Xu, Y., Li, Y.,
M., Wang, M., Hermoso, M. J., Metanat, M., Rastegari,                Zhao, Y., Sun, Y., Wang, Y., Yu, Y., Zhang, Y., Shi, Y.,
M., Bansal, M., Santhanam, N., Parks, N., White, N.,                Xiong, Y., He, Y., Piao, Y., Wang, Y., Tan, Y., Ma, Y.,
Bawa, N., Singhal, N., Egebo, N., Usunier, N., Mehta,                Liu, Y., Guo, Y., Ou, Y., Wang, Y., Gong, Y., Zou, Y.,
N., Laptev, N. P., Dong, N., Cheng, N., Chernoguz, O.,               He, Y., Xiong, Y., Luo, Y., You, Y., Liu, Y., Zhou, Y.,
Hart, O., Salpekar, O., Kalinli, O., Kent, P., Parekh, P.,           Zhu, Y. X., Huang, Y., Li, Y., Zheng, Y., Zhu, Y., Ma, Y.,
Saab, P., Balaji, P., Rittner, P., Bontrager, P., Roux, P.,         Tang, Y., Zha, Y., Yan, Y., Ren, Z. Z., Ren, Z., Sha, Z.,
Dollar, P., Zvyagina, P., Ratanchandani, P., Yuvraj, P.,             Fu, Z., Xu, Z., Xie, Z., Zhang, Z., Hao, Z., Ma, Z., Yan,
Liang, Q., Alao, R., Rodriguez, R., Ayub, R., Murthy, R.,            Z., Wu, Z., Gu, Z., Zhu, Z., Liu, Z., Li, Z., Xie, Z., Song,
Nayani, R., Mitra, R., Parthasarathy, R., Li, R., Hogan,             Z., Pan, Z., Huang, Z., Xu, Z., Zhang, Z., and Zhang,
R., Battey, R., Wang, R., Howes, R., Rinott, R., Mehta,              Z. Deepseek-r1 incentivizes reasoning in llms through
S., Siby, S., Bondu, S. J., Datta, S., Chugh, S., Hunt, S.,          reinforcement learning. Nat., 645(8081):633–638, 2025.
Dhillon, S., Sidorov, S., Pan, S., Mahajan, S., Verma,               doi: 10.1038/S41586-025-09422-Z. URL https://
S., Yamamoto, S., Ramaswamy, S., Lindsay, S., Lindsay,               doi.org/10.1038/s41586-025-09422-z.
S., Feng, S., Lin, S., Zha, S. C., Patil, S., Shankar, S.,
                                                                   Gurobi Optimization, LLC. Gurobi Optimizer Reference
Zhang, S., Zhang, S., Wang, S., Agarwal, S., Sajuyigbe,
                                                                     Manual, 2024. URL https://www.gurobi.com.
S., Chintala, S., Max, S., Chen, S., Kehoe, S., Satter-
field, S., Govindaprasad, S., Gupta, S., Deng, S., Cho,            Huang, C., Tang, Z., Hu, S., Jiang, R., Zheng, X.,
S., Virk, S., Subramanian, S., Choudhury, S., Goldman,               Ge, D., Wang, B., and Wang, Z. Orlm: A cus-

                                                              10
                           Execution-Verified Reinforcement Learning for Optimization Modeling

  tomizable framework in training large models for au-                 2503.09516. URL https://doi.org/10.48550/
  tomated optimization modeling. Operations Research,                  arXiv.2503.09516.
  73(6):2986–3009, nov 2025a. doi: 10.1287/opre.2024.
  1233.    URL https://pubsonline.informs.                           Liu, H., Wang, J., Cai, Y., Han, X., Kuang, Y., and HAO,
  org/doi/10.1287/opre.2024.1233.                                      J. Optitree: Hierarchical thoughts generation with tree
                                                                       search for LLM optimization modeling. In The Thirty-
Huang, X., Shen, Q., Hu, Y., Gao, A., and Wang, B.                     ninth Annual Conference on Neural Information Pro-
  Llms for mathematical modeling: Towards bridging the                 cessing Systems, 2025. URL https://openreview.
  gap between natural and mathematical languages. In                   net/forum?id=Ej20yjWMCj.
  Chiruzzo, L., Ritter, A., and Wang, L. (eds.), Find-
  ings of the Association for Computational Linguistics:             Lu, H., Xie, Z., Wu, Y., Ren, C., Chen, Y., and Wen, Z. Opt-
 NAACL 2025, Albuquerque, New Mexico, USA, April                       math: A scalable bidirectional data synthesis framework
 29 - May 4, 2025, volume NAACL 2025 of Find-                          for optimization modeling. In Forty-second International
  ings of ACL, pp. 2678–2710. Association for Compu-                   Conference on Machine Learning, ICML 2025, Vancou-
  tational Linguistics, 2025b. doi: 10.18653/V1/2025.                  ver, BC, Canada, July 13-19, 2025. OpenReview.net,
  FINDINGS-NAACL.146. URL https://doi.org/                             2025. URL https://openreview.net/forum?
 10.18653/v1/2025.findings-naacl.146.                                  id=9P5e6iE4WK.

Hurst, A., Lerer, A., Goucher, A. P., Perelman, A., Ramesh,          Madaan, A., Tandon, N., Gupta, P., Hallinan, S., Gao, L.,
  A., Clark, A., Ostrow, A., Welihinda, A., Hayes, A.,                Wiegreffe, S., Alon, U., Dziri, N., Prabhumoye, S., Yang,
  Radford, A., Madry, A., Baker-Whitcomb, A., Beutel,                 Y., Gupta, S., Majumder, B. P., Hermann, K., Welleck,
  A., Borzunov, A., Carney, A., Chow, A., Kirillov, A.,               S., Yazdanbakhsh, A., and Clark, P. Self-refine: Iterative
  Nichol, A., Paino, A., Renzin, A., Passos, A. T., Kir-              refinement with self-feedback. In Oh, A., Naumann,
  illov, A., Christakis, A., Conneau, A., Kamali, A., Jabri,          T., Globerson, A., Saenko, K., Hardt, M., and Levine,
  A., Moyer, A., Tam, A., Crookes, A., Tootoonchian, A.,              S. (eds.), Advances in Neural Information Processing
  Kumar, A., Vallone, A., Karpathy, A., Braunstein, A.,               Systems 36: Annual Conference on Neural Information
  Cann, A., Codispoti, A., Galu, A., Kondrich, A., Tul-               Processing Systems 2023, NeurIPS 2023, New Orleans,
  loch, A., Mishchenko, A., Baek, A., Jiang, A., Pelisse,             LA, USA, December 10 - 16, 2023, 2023. URL https:
  A., Woodford, A., Gosalia, A., Dhar, A., Pantuliano,                //openreview.net/forum?id=S37hOerQLB.
  A., Nayak, A., Oliver, A., Zoph, B., Ghorbani, B., Le-
                                                                     Markowitz, H. Portfolio selection. The Journal of Finance,
  imberger, B., Rossen, B., Sokolowsky, B., Wang, B.,
                                                                      7(1):77–91, 1952. ISSN 00221082, 15406261. URL
  Zweig, B., Hoover, B., Samic, B., McGrew, B., Spero,
                                                                      http://www.jstor.org/stable/2975974.
  B., Giertler, B., Cheng, B., Lightcap, B., Walkin, B.,
  Quinn, B., Guarraci, B., Hsu, B., Kellogg, B., Eastman,            Meng, L., Zhang, C., Ren, Y., Zhang, B., and Lv, C.
  B., Lugaresi, C., Wainwright, C. L., Bassin, C., Hudson,            Mixed-integer linear programming and constraint
  C., Chu, C., Nelson, C., Li, C., Shern, C. J., Conger, C.,          programming formulations for solving distributed
  Barette, C., Voss, C., Ding, C., Lu, C., Zhang, C., Beau-           flexible job shop scheduling problem. Computers &
  mont, C., Hallacy, C., Koch, C., Gibson, C., Kim, C.,               Industrial Engineering, 142:106347, 2020. ISSN 0360-
  Choi, C., McLeavey, C., Hesse, C., Fischer, C., Winter, C.,         8352. doi: https://doi.org/10.1016/j.cie.2020.106347.
  Czarnecki, C., Jarvis, C., Wei, C., Koumouzelis, C., and            URL         https://www.sciencedirect.com/
  Sherburn, D. Gpt-4o system card. CoRR, abs/2410.21276,              science/article/pii/S0360835220300814.
  2024. doi: 10.48550/ARXIV.2410.21276. URL https:
 //doi.org/10.48550/arXiv.2410.21276.                                OpenAI. Introducing Openai o1. https://openai.
                                                                       com/o1/, 2024.
Jiang, C., Shu, X., Qian, H., Lu, X., Zhou, J., Zhou, A., and
   Yu, Y. LLMOPT: learning to define and solve general op-           Perron, L. and Furnon, V. Or-tools, 2024. URL https:
   timization problems from scratch. In The Thirteenth Inter-          //developers.google.com/optimization/.
   national Conference on Learning Representations, ICLR
   2025, Singapore, April 24-28, 2025. OpenReview.net,               Ramamonjison, R., Yu, T. T. L., Li, R., Li, H.,
   2025. URL https://openreview.net/forum?                             Carenini, G., Ghaddar, B., He, S., Mostajabdaveh,
   id=9OMvtboTJg.                                                      M., Banitalebi-Dehkordi, A., Zhou, Z., and Zhang, Y.
                                                                       Nl4opt competition: Formulating optimization prob-
Jin, B., Zeng, H., Yue, Z., Wang, D., Zamani, H.,                      lems based on their natural language descriptions. In
   and Han, J. Search-r1: Training llms to reason and                  Ciccone, M., Stolovitzky, G., and Albrecht, J. (eds.),
   leverage search engines with reinforcement learning.                NeurIPS 2022 Competition Track, November 28 - De-
   CoRR, abs/2503.09516, 2025. doi: 10.48550/ARXIV.                    cember 9, 2022, Online, volume 220 of Proceedings

                                                                11
                          Execution-Verified Reinforcement Learning for Optimization Modeling

  of Machine Learning Research, pp. 189–203. PMLR,                   ing methodologies and applications. European Journal
  2021. URL https://proceedings.mlr.press/                           of Operational Research, 300(2):387–404, 2022. ISSN
  v220/ramamonjison22a.html.                                         0377-2217. doi: https://doi.org/10.1016/j.ejor.2021.10.
                                                                     003. URL https://www.sciencedirect.com/
Ramamonjison, R., Li, H., Yu, T. T. L., He, S., Rengan, V.,          science/article/pii/S0377221721008481.
  Banitalebi-Dehkordi, A., Zhou, Z., and Zhang, Y. Aug-
  menting operations research with auto-formulation of             Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B.,
  optimization models from problem descriptions. In Li, Y.          Xia, F., Chi, E. H., Le, Q. V., and Zhou, D. Chain-of-
  and Lazaridou, A. (eds.), Proceedings of the 2022 Con-            thought prompting elicits reasoning in large language
  ference on Empirical Methods in Natural Language Pro-             models. In Koyejo, S., Mohamed, S., Agarwal, A., Bel-
  cessing: EMNLP 2022 - Industry Track, Abu Dhabi, UAE,             grave, D., Cho, K., and Oh, A. (eds.), Advances in Neu-
  December 7 - 11, 2022, pp. 29–62. Association for Com-            ral Information Processing Systems 35: Annual Con-
  putational Linguistics, 2022. doi: 10.18653/V1/2022.              ference on Neural Information Processing Systems 2022,
  EMNLP-INDUSTRY.4. URL https://doi.org/                            NeurIPS 2022, New Orleans, LA, USA, November 28 - De-
  10.18653/v1/2022.emnlp-industry.4.                                cember 9, 2022, 2022. URL https://openreview.
Romera-Paredes, B., Barekatain, M., Novikov, A., Ba-                net/forum?id=_VjQlMeSB_J.
  log, M., Kumar, M. P., Dupont, E., Ruiz, F. J. R.,
                                                                   Wen, X., Liu, Z., Zheng, S., Xu, Z., Ye, S., Wu, Z.,
  Ellenberg, J. S., Wang, P., Fawzi, O., Kohli, P., and
                                                                    Liang, X., Wang, Y., Li, J., Miao, Z., Bian, J., and
  Fawzi, A. Mathematical discoveries from program search
                                                                    Yang, M. Reinforcement learning with verifiable rewards
  with large language models. Nature, 625(7995):468–
                                                                    implicitly incentivizes correct reasoning in base llms.
  475, January 2024. ISSN 1476-4687. doi: 10.1038/
                                                                    CoRR, abs/2506.14245, 2025. doi: 10.48550/ARXIV.
  s41586-023-06924-6. URL https://doi.org/10.
                                                                    2506.14245. URL https://doi.org/10.48550/
  1038/s41586-023-06924-6.
                                                                    arXiv.2506.14245.
Shao, Z., Wang, P., Zhu, Q., Xu, R., Song, J., Zhang, M.,
  Li, Y. K., Wu, Y., and Guo, D. Deepseekmath: Pushing             Wu, Y., Zhang, Y., Wu, Y., Wang, Y., Zhang, J., and
  the limits of mathematical reasoning in open language             Cheng, J. Training LLMs for optimization model-
  models. CoRR, abs/2402.03300, 2024. doi: 10.48550/                ing via iterative data synthesis and structured vali-
  ARXIV.2402.03300. URL https://doi.org/10.                         dation. In Christodoulopoulos, C., Chakraborty, T.,
  48550/arXiv.2402.03300.                                           Rose, C., and Peng, V. (eds.), Findings of the Asso-
                                                                    ciation for Computational Linguistics: EMNLP 2025,
Shi, Y., Zhou, J., Song, W., Bi, J., Wu, Y., and Zhang, J.          pp. 12880–12896, Suzhou, China, November 2025. As-
  Generalizable heuristic generation through large language         sociation for Computational Linguistics. ISBN 979-8-
  models with meta-optimization. CoRR, abs/2505.20881,              89176-335-7. doi: 10.18653/v1/2025.findings-emnlp.
  2025. doi: 10.48550/ARXIV.2505.20881. URL https:                  691. URL https://aclanthology.org/2025.
  //doi.org/10.48550/arXiv.2505.20881.                              findings-emnlp.691/.
Shinn, N., Cassano, F., Gopinath, A., Narasimhan, K., and          Xiao, Z., Zhang, D., Wu, Y., Xu, L., Wang, Y. J., Han, X., Fu,
  Yao, S. Reflexion: language agents with verbal reinforce-          X., Zhong, T., Zeng, J., Song, M., and Chen, G. Chain-
  ment learning. In Oh, A., Naumann, T., Globerson, A.,              of-experts: When llms meet complex operations research
  Saenko, K., Hardt, M., and Levine, S. (eds.), Advances             problems. In The Twelfth International Conference on
  in Neural Information Processing Systems 36: Annual                Learning Representations, ICLR 2024, Vienna, Austria,
  Conference on Neural Information Processing Systems                May 7-11, 2024. OpenReview.net, 2024. URL https:
  2023, NeurIPS 2023, New Orleans, LA, USA, December                 //openreview.net/forum?id=HobyL1B9CZ.
  10 - 16, 2023, 2023. URL https://openreview.
  net/forum?id=vAElhFcKW6.                                         Xiao, Z., Xie, J., Xu, L., Guan, S., Zhu, J., Han, X.,
Singh, A.      An overview of the optimization mod-                  Fu, X., Yu, W., Wu, H., Shi, W., Kang, Q., Duan, J.,
  elling applications.      Journal of Hydrology, 466-               Zhong, T., Yuan, M., Zeng, J., Wang, Y., Chen, G.,
  467:167–182, 2012.          ISSN 0022-1694.     doi:               and Zhang, D. A survey of optimization modeling
  https://doi.org/10.1016/j.jhydrol.2012.08.004.                     meets llms: Progress and future directions. In Pro-
  URL         https://www.sciencedirect.com/                         ceedings of the Thirty-Fourth International Joint Con-
  science/article/pii/S0022169412006683.                             ference on Artificial Intelligence, IJCAI 2025, Montreal,
                                                                     Canada, August 16-22, 2025, pp. 10742–10750. ijcai.org,
Skolfield, J. K. and Escobedo, A. R. Operations research             2025. doi: 10.24963/IJCAI.2025/1192. URL https:
  in optimal power flow: A guide to recent and emerg-                //doi.org/10.24963/ijcai.2025/1192.

                                                              12
                            Execution-Verified Reinforcement Learning for Optimization Modeling

Yang, A., Yang, B., Zhang, B., Hui, B., Zheng, B., Yu, B.,
  Li, C., Liu, D., Huang, F., Wei, H., Lin, H., Yang, J., Tu,
  J., Zhang, J., Yang, J., Yang, J., Zhou, J., Lin, J., Dang,
  K., Lu, K., Bao, K., Yang, K., Yu, L., Li, M., Xue, M.,
  Zhang, P., Zhu, Q., Men, R., Lin, R., Li, T., Xia, T., Ren,
  X., Ren, X., Fan, Y., Su, Y., Zhang, Y., Wan, Y., Liu, Y.,
  Cui, Z., Zhang, Z., and Qiu, Z. Qwen2.5 technical report.
  CoRR, abs/2412.15115, 2024. doi: 10.48550/ARXIV.
  2412.15115. URL https://doi.org/10.48550/
  arXiv.2412.15115.
Yang, Z., Wang, Y., Huang, Y., Guo, Z., Shi, W., Han, X.,
  Feng, L., Song, L., Liang, X., and Tang, J. Optibench
  meets resocratic: Measure and improve llms for optimiza-
  tion modeling. In The Thirteenth International Confer-
  ence on Learning Representations, ICLR 2025, Singapore,
  April 24-28, 2025. OpenReview.net, 2025. URL https:
  //openreview.net/forum?id=fsDZwS49uY.
Ye, H., Wang, J., Cao, Z., Berto, F., Hua, C., Kim, H., Park,
  J., and Song, G. Reevo: Large language models as hyper-
  heuristics with reflective evolution. In Globersons, A.,
  Mackey, L., Belgrave, D., Fan, A., Paquet, U., Tomczak,
  J. M., and Zhang, C. (eds.), Advances in Neural Infor-
  mation Processing Systems 38: Annual Conference on
  Neural Information Processing Systems 2024, NeurIPS
  2024, Vancouver, BC, Canada, December 10 - 15, 2024,
  2024. URL https://openreview.net/forum?
  id=483IPG0HWL.
Yu, Q., Zhang, Z., Zhu, R., Yuan, Y., Zuo, X., Yue, Y., Fan,
  T., Liu, G., Liu, L., Liu, X., Lin, H., Lin, Z., Ma, B.,
  Sheng, G., Tong, Y., Zhang, C., Zhang, M., Zhang, W.,
  Zhu, H., Zhu, J., Chen, J., Chen, J., Wang, C., Yu, H., Dai,
  W., Song, Y., Wei, X., Zhou, H., Liu, J., Ma, W., Zhang,
  Y., Yan, L., Qiao, M., Wu, Y., and Wang, M. DAPO: an
  open-source LLM reinforcement learning system at scale.
  CoRR, abs/2503.14476, 2025. doi: 10.48550/ARXIV.
  2503.14476. URL https://doi.org/10.48550/
  arXiv.2503.14476.
Zhou, C., Xu, T., Lin, J., and Ge, D. Steporlm: A
  self-evolving framework with generative process su-
  pervision for operations research language models.
  CoRR, abs/2509.22558, 2025. doi: 10.48550/ARXIV.
  2509.22558. URL https://doi.org/10.48550/
  arXiv.2509.22558.




                                                                 13
                             Execution-Verified Reinforcement Learning for Optimization Modeling

A. Algorithm

Algorithm 1 Execution-Verified Optimization Modeling Training via Generate–Execute–Feedback–Update
Require: Dataset D = {(q, a)}; solver set S; policy πθ ; solver sampler p(s); batch size B; group size G.
Require: Harness Es (·) with resource limits (timeout 10s, memory 2GB).
Require: Rewards rfmt (·) (Eq. (5)), rans (·; ·) (Eq. (10)).
Require: GRPO params (ϵ, β, πref , δA ) or DAPO params (ϵl , ϵh , δA ).
 1: while not converged do
 2:   Sample {(qj , aj )}B                    B
                           j=1 ∼ D and {sj }j=1 ∼ p(s).
 3:   Freeze πθold ← πθ .
 4:   for j = 1 to B do
 5:     xj ← (qj , sj ).
 6:     Sample {yj,k }G  k=1 ∼ πθold (· | xj ).
 7:     for k = 1 to G do
             fmt
 8:         rj,k  ← rfmt (yj,k ).
 9:         Parse the unique <code> block from yj,k (Sec. 3.2).
10:         if parsing fails (schema violation) then
11:            oj,k ← (0, ERROR, ⊥, ℓ)                                                                       // non-executable
12:         else
                                                   code
13:            Execute in sandbox: oj,k ← Esj (yj,k     )                                                           (Sec. 3.3)
14:         end if
              ans
15:         rj,k  ← rans (oj,k ; aj ).
                       fmt      ans
16:         Rj,k ← rj,k    + rj,k                                                                                    (Eq. (7))
17:      end for
18:      Compute group stats µR , σR over {Rj,k }G   k=1 .
                   Rj,k − µR
19:      Aj,k ←                  for k = 1..G.
                    σR + δ A
20:      if using DAPO then
21:         Optionally skip uninformative groups (e.g., all failures) per DAPO sampling rule.
22:      end if
23:   end for
24:   Update θ with GRPO objective (Eq. (12)) or DAPO objective (Eq. (13)).
25: end while


Algorithm 1 provides the complete pseudocode for Execution-Verified Optimization Modeling training. The procedure
follows a generate–execute–feedback–update loop that iteratively improves the solver-conditioned policy πθ via deterministic
execution feedback.

Sampling and context construction. At each iteration, we sample a batch of problem–answer pairs {(qj , aj )}B     j=1 from D
and assign each instance a target solver sj ∼ p(s). The conditioning context is then constructed as xj = (qj , sj ), matching
the solver-conditioned objective in Eq. (4).

Group rollout generation. For each context xj , we sample a group of G candidate outputs {yj,k }G  k=1 ∼ πθold (· | xj ).
Group sampling enables within-group normalization to compute group-relative advantages, which is particularly important
under sparse, execution-verified rewards.

Parsing, sandboxed execution, and observation standardization. Each output yj,k is first checked against the required
output protocol (Sec. 3.2) and deterministically parsed to extract the unique <code> block. Outputs that violate the
schema (e.g., missing tags, multiple blocks, or wrong order) are treated as non-executable and directly mapped to a failure
observation. Otherwise, the extracted program is executed in the sandboxed harness under strict resource constraints
(10 seconds timeout; 2 GB memory cap), invoking solver sj via its standard Python interface (Sec. 3.3). The harness
consolidates heterogeneous solver behaviors into a unified observation o = (c, σ, v, ℓ), consisting of the execution flag,
solver status, objective value (or ⊥), and raw logs.

Execution-verified reward computation. For each sample, we compute the total reward Rj,k = rfmt (yj,k ) +
rans (oj,k ; aj ), where rfmt enforces protocol compliance (Eq. (5)) and rans verifies outcome correctness using only solver-
verified outcomes (Eq. (10)). Crucially, no intermediate reasoning traces or reference programs are used.

                                                                 14
                              Execution-Verified Reinforcement Learning for Optimization Modeling


    Below is an Operations Research question. Build a mathematical model and corresponding Python code using {solver} to
    address the question.
    In the Python code, please include a final logic block as follows: if the problem has an optimal or feasible solution, print “Just
    print the best solution: {solution value}”; otherwise, print “No Best Solution”.
   The response consists of two parts. The reasoning process (including the mathematical model) and the Python code must be
   enclosed within <think>...</think> and <code>...</code> tags, respectively:
    <think>
    reasoning process here, including mathematical model...
    </think>
    <code>
    your response here, including Python code...
    </code>
    Here is the question:
    {Question}


            Figure 5. Solver-conditioned prompt template with a fixed two-block output format for parsing and execution.


Advantage estimation and policy update. Advantages are computed via within-group standardization Aj,k = (Rj,k −
µR )/(σR + δA ), producing group-relative rankings for policy optimization. We then update θ using GRPO (Eq. 12) or
DAPO (Eq. 13); when using DAPO, asymmetric clipping and dynamic sampling (e.g., skipping uninformative all-failure
groups) help stabilize learning and improve sample efficiency. The loop repeats until convergence, as measured by validation
performance or reward saturation.

B. Training Prompt Template
Figure 5 presents the solver-conditioned prompt template used throughout training and evaluation. The template is designed
with three key properties:

Solver Conditioning. The placeholder {solver} is dynamically instantiated with the target solver identifier (e.g.,
Gurobi, OR-Tools, COPT) at runtime. This design enables a single model to handle multiple solvers by conditioning on
the solver name, without requiring few-shot examples. The model must learn solver-specific API usage and idioms purely
from execution feedback.

Structured Output Protocol. The template enforces a strict two-block output format: a <think> block for reasoning
and mathematical modeling, followed by a <code> block for executable Python code. This machine-parseable structure
ensures reliable extraction of the code component for execution and enables automatic format validation through the format
reward rfmt .

Standardized Output Convention. The template specifies a uniform output convention requiring the model to print the
optimal objective value in a fixed format (Just print the best solution: {value}) or indicate infeasibility
or unboundedness (No Best Solution). This standardization simplifies answer extraction and enables consistent
reward computation across different solvers and problem types.
Notably, the prompt provides no solver-specific exemplars, step-by-step solution templates, or reference programs. All
solver-specific knowledge must be acquired through interaction with the execution environment, making the approach purely
outcome-supervised.

C. Datasets
  • OptiBench (Yang et al., 2025) is an end-to-end optimization problem-solving benchmark designed for human-readable
    inputs and outputs. It encompasses both linear and nonlinear programming problems, including scenarios with and
    without tabular data. A distinctive feature is that LLMs are required to call code solvers to provide precise numerical
    answers, ensuring accuracy through computational verification rather than approximation.

                                                                   15
                                Execution-Verified Reinforcement Learning for Optimization Modeling

   • NL4OPT (Ramamonjison et al., 2021) is a benchmark originating from the NeurIPS 2022 competition that focuses on
     translating natural language descriptions into linear programming formulations. It contains 289 linear programming
     problems in its test set and addresses two sub-tasks: (1) recognizing and labeling semantic entities corresponding
     to optimization problem components, and (2) generating meaning representations (i.e., logical forms) from detected
     problem entities.

   • MAMO (Huang et al., 2025b) proposes a process-oriented framework to assess the mathematical modeling capabilities
     of LLMs. It contains 1,209 problems spanning ordinary differential equations, linear programming, and mixed-integer
     linear programming. The benchmark distinguishes between EasyLP (652 problems) and ComplexLP (211 problems)
     categories. Unlike conventional result-oriented assessments, MAMO focuses on the modeling process itself by utilizing
     solvers and comparing outputs with ground truth.

   • IndustryOR (Huang et al., 2025a) is the first industrial-scale benchmark specifically designed to evaluate LLMs on
     solving real-world operations research problems. It comprises 100 problems sourced from 13 different industries,
     covering 5 types of questions across 3 levels of difficulty, bridging the gap between academic optimization problems
     and practical industrial applications.

D. Implementation Details
Base Models. We conduct experiments using the Qwen2.5 model family (Yang et al., 2024) across multiple scales,
including 0.5B, 1.5B, 3B, and 7B parameter variants. For fair comparison, we also reproduce the ORLM baseline (Huang
et al., 2025a) using Qwen2.5-7B as the backbone and follow its original supervised fine-tuning (SFT) protocol.

Training Infrastructure. All model training is conducted on 4 NVIDIA A800 GPUs using the verl1 reinforcement
learning framework. Unless otherwise specified, we use the following default hyperparameters: learning rate of 1 × 10−6 ,
batch size of 64, group size G = 8 for rollout sampling, clipping parameter ϵclip = 0.2, KL coefficient β = 0.001, and 1
training epoch. We use a maximum sequence length of 8,192 tokens. For the format reward rfmt , we set wt = 0.125 for
all tags in T and wm = 0.5 for the regex match term. Experiment-specific configurations, if different, are detailed in the
corresponding sections.

Evaluation Protocol. We evaluate model performance using answer accuracy under two tolerance levels: ϵ = 0.05 (5%
relative error) and ϵ = 10−4 (strict matching). The accuracy is computed as the proportion of test instances where the
model-generated code successfully executes, produces a feasible solution, and yields an optimal value within ϵ of the ground
truth. All evaluations use greedy decoding with temperature 0.

E. Human Evaluation on Reasoning and Implementation
                            Table 4. Human evaluation accuracy on reasoning quality and code implementation.

                                                          Constraints          Objective Function
                                        Model
                                                       Reasoning     Code      Reasoning   Code
                                        Qwen2.5-7B        24.6          58.3     74.2       81.4
                                        ORLM (SFT)        23.4          78.7     65.4       78.7
                                        GRPO              26.4          59.7     77.1       87.8


To deeply investigate the underlying mechanisms of model performance improvement, specifically to verify whether the
model has truly mastered operations research modeling logic, we randomly sampled 500 samples from the OptiBench
benchmark for fine-grained human evaluation. The evaluation focused on the two most critical dimensions in operations
research modeling: Constraints and Objective Function. For these two dimensions, we established differentiated evaluation
criteria: for constraints, we adopted dual metrics of “correctness” and “completeness,” examining both whether the generated
constraints conform to mathematical logic and strictly verifying whether the model missed key implicit restrictions in the
problem; for the objective function, we primarily assessed the “correctness” of its mathematical expression. To ensure the
   1
       https://github.com/verl-project/verl

                                                                   16
                           Execution-Verified Reinforcement Learning for Optimization Modeling

professionalism and fairness of the evaluation, we invited two mathematics graduate students to conduct back-to-back blind
annotation, with a third senior researcher responsible for adjudicating scoring discrepancies. Ultimately, the annotation
results demonstrated extremely high inter-annotator agreement, with Cohen’s κ coefficient exceeding 0.85, ensuring the
reliability of the evaluation conclusions.
The experimental results are shown in Table 4. We compare three models: the base Qwen2.5-7B, ORLM trained with process-
supervised SFT, and our GRPO method trained with execution-verified RL. The results reveal distinct improvement patterns
across different dimensions. First, in constraint modeling, GRPO achieves the highest reasoning accuracy, outperforming
both the base model and ORLM. Notably, ORLM’s reasoning score is even lower than the base model, suggesting that process
supervision may lead to overfitting on specific constraint patterns rather than enhancing general reasoning capabilities. For
constraint code, ORLM achieves the highest accuracy, benefiting from its exposure to reference code during SFT, while
GRPO shows modest improvement over the base model. Second, in objective function construction, GRPO demonstrates
clear advantages across both reasoning and code dimensions compared to the base model. In contrast, ORLM shows
degraded performance in both metrics, falling below even the base model. This suggests that while process supervision with
reference code can boost constraint implementation, it may inadvertently impair the model’s ability to independently reason
about objective formulation. Overall, these results demonstrate that outcome-only supervision through execution feedback
not only optimizes code generation but also drives genuine improvements in mathematical reasoning, enabling the model to
achieve more robust performance across both constraint understanding and objective definition.

F. Stringent Evaluation of Generalization Across Different Solvers
Table 5 presents the model’s performance trained under different solver settings with a more stringent evaluation threshold
(ϵeval = 10−4 ). Compared to the standard threshold of ϵeval = 0.05 used in the main text, this stricter setting can more
accurately detect modeling errors, especially errors related to variable type declarations. Under the looser threshold, some
integer variables that were not correctly declared might be mistakenly considered correct due to minor numerical differences;
the stricter threshold effectively exposes such hidden modeling flaws.
The experimental results demonstrate that despite the significantly tightened evaluation criteria, execution-verified rein-
forcement learning still shows robust improvement across both solver environments. Notably, while the absolute accuracy
of each benchmark generally decreases under the stricter evaluation standard, the relative gains brought by RL training
remain substantial. This indicates that execution verification feedback effectively guides the model to learn correct variable
type declarations and constraint formulations, thereby maintaining competitiveness even under more rigorous evaluation
conditions.

                                      Table 5. Training with different solvers (ϵ = 10−4 ).

            Solver                  OptiBench NL4OPT MAMO EasyLP MAMO ComplexLP IndustryOR
            Gurobi (before RL)          34.05      48.97            82.82                  13.27        22.00
            Gurobi (after RL)           58.30      76.32            87.42                  29.85        23.00
            ∆ (after – before)         +24.25      +27.35           +4.60                 +16.58        +1.00
            OR-Tools (before RL)       24.25        37.14           44.93                  4.26         17.00
            OR-Tools (after RL)        31.56        44.48           72.08                  2.36         26.00
            ∆ (after – before)         +7.31        +7.34           +27.15                -1.90         +9.00



G. Evaluation of the Capabilities of Small-Scale Models
This section evaluates the applicability of execution-verified reinforcement learning on small-scale models of the Qwen2.5
series (0.5B, 1.5B, and 3B parameters). Table 6 and Table 7 report performance under relaxed (ϵeval = 0.05) and stringent
(ϵeval = 10−4 ) evaluation thresholds, respectively.

Results under Relaxed Evaluation (ϵeval = 0.05). As shown in Table 6, model scale significantly affects baseline
capabilities. The 0.5B model achieves zero accuracy across all benchmarks, indicating insufficient capacity for optimization
modeling. However, the 1.5B and 3B models demonstrate substantial improvements after GRPO training, with significant
gains observed across multiple benchmarks. These results demonstrate that execution-verified RL exhibits a pronounced

                                                               17
                           Execution-Verified Reinforcement Learning for Optimization Modeling

amplification effect on small-scale models.

Results under Stringent Evaluation (ϵeval = 10−4 ). As shown in Table 7, reinforcement learning maintains robust
improvements even under the stricter evaluation criterion for both the 1.5B and 3B models. Notably, while absolute accuracy
decreases compared to the relaxed evaluation, the relative gains from RL training remain substantial or even larger, indicating
that execution feedback effectively guides small-scale models toward more precise modeling strategies.

Summary. These results validate that execution-verified RL is highly effective for enhancing small-scale models. After
training, the 3B model’s performance on several benchmarks approaches or exceeds the 7B base model, providing a feasible
path for deploying optimization modeling systems in resource-constrained scenarios.

                           Table 6. Performance of small-scale models (ϵ = 0.05, %). Higher is better.

                                                                    MAMO      MAMO
                       Model            OptiBench     NL4OPT                                 IndustryOR
                                                                    EasyLP   ComplexLP
                                                    Base models (Qwen2.5)
                       Qwen2.5-0.5B         0.00        0.00       0.00           0.00           0.00
                       Qwen2.5-1.5B        35.44       48.57      43.35           4.73           9.00
                       Qwen2.5-3B          28.40       26.12      77.14           8.53           7.00
                                                    GRPO-trained models
                       GRPO-0.5B            0.00        0.00       0.00           0.00           0.00
                       GRPO-1.5B           47.00       66.53      78.98          12.79          12.00
                       GRPO-3B             55.81       77.55      84.66          22.27          16.00



H. Execution-Verified Optimization Modeling for A Under-covered Solver: COPT
For under-covered solvers with scarce pretraining exposure and near-zero initial generation success (e.g., niche or regional
solvers like COPT), direct RL training suffers from a cold-start problem: the model rarely produces executable code,
resulting in sparse positive feedback and slow convergence. To address this, we propose a two-stage cold-start strategy
combining cross-solver data construction with cold-start SFT.

Cross-Solver Data Construction via LLM Translation. The key idea is to leverage labeled data from a well-supported
source solver ssrc (e.g., Gurobi) and use a strong general-purpose LLM to translate solver-specific code to the target
solver stgt . Concretely, given a problem description q and its reference code ysrc under the source solver, we prompt a
capable LLM (e.g., GPT-4o) together with the target solver’s API documentation to rewrite the code:
                                                       LLM Translation
                                      (q, ssrc , ysrc ) −−−−−−−−−−−→ (q, stgt , ytgt ).                                   (15)

This procedure is essentially a cross-solver syntactic transformation: it preserves the mathematical modeling logic (decision
variables, constraints, objectives) while adapting only the underlying API calls, import statements, and solver-specific
idioms. To ensure quality, we execute each translated program ytgt in the target solver environment Estgt and retain only
samples that produce correct outputs matching the ground-truth answer. This execution-based filtering removes translation
errors and API misuse, yielding a clean cold-start dataset.

Cold-Start SFT followed by Execution-Verified RL. Using the constructed dataset, we first run a brief SFT stage to
instantiate minimal API priors for the target solver, including import conventions, variable declaration patterns, and common
constraint/objective templates. Starting from this cold-start policy, we then switch to execution-verified RL in Estgt using
the same generate–execute–feedback–update loop described in Algorithm 1. This allows solver-specific executability and
verified correctness to improve rapidly without requiring a large-scale solver-specific dataset.
We emphasize that this cold-start procedure is not required in the default outcome-only setting for well-supported solvers;
it is used only to reduce cold-start friction for solvers with poor pretraining coverage. As shown in Appendix J, a small
amount of cold-start data (100–300 samples) combined with RL training is often more effective than large-scale SFT alone,
as excessive SFT may cause overfitting and reduce subsequent RL effectiveness.

                                                               18
                               Execution-Verified Reinforcement Learning for Optimization Modeling

                             Table 7. Performance of small-scale models (ϵ = 10−4 , %). Higher is better.

                                                                                    MAMO      MAMO
                         Model                         OptiBench       NL4OPT                                     IndustryOR
                                                                                    EasyLP   ComplexLP
                                                                     Base models (Qwen2.5)
                         Qwen2.5-0.5B                       0.00         0.00       0.00            0.00             0.00
                         Qwen2.5-1.5B                      22.46        31.02      38.34            0.47             7.00
                         Qwen2.5-3B                        20.59        20.00      74.69            2.36             6.00
                                                                     GRPO-trained models
                         GRPO-0.5B                          0.00         0.00       0.00            0.00             0.00
                         GRPO-1.5B                         30.23        39.18      69.01            1.42             9.00
                         GRPO-3B                           52.32        71.83      83.74           21.32            14.00



I. Cold Start Experiment on COPT


                                                              Base     SFT cold start     RL with SFT cold start
                                           100

                                            75
                            Accuracy (%)




                                            50

                                            25

                                             0

                                                        nch           PT        syL
                                                                                   P
                                                                                              xL
                                                                                                P
                                                                                                            ryO
                                                                                                               R
                                                      Be          4O          a           ple             st
                                                 Opti           NL         OE           om            ndu
                                                                        A M           C              I
                                                                       M         A MO
                                                                               M

Figure 6. Cold-start experiment on COPT solver comparing Base, SFT cold start, and RL with SFT cold start across different benchmarks.



Figure 6 presents the cold-start experiment results on the COPT solver, a regional commercial solver with limited coverage in
LLM pretraining corpora. We compare three settings: (1) Base model with zero-shot prompting, (2) Base model fine-tuned
with cold-start SFT data, and (3) SFT model further trained with execution-verified RL.


Experimental Setup. The cold-start SFT dataset consists of only 100 randomly sampled problem-code pairs, constructed
via LLM translation from Gurobi reference programs as described in Appendix H. This minimal data scale demonstrates
the efficiency of our cold-start strategy.


Results and Analysis. The results demonstrate the effectiveness of our cold-start approach. With only 100 samples, SFT
successfully bootstraps the base model to learn COPT API usage, achieving substantial improvements over the zero-shot
baseline across all benchmarks. This confirms that minimal syntactic supervision is sufficient to overcome the cold-start
barrier for unfamiliar solvers, significantly reducing the data construction cost.
More importantly, execution-verified RL training further enhances performance on the majority of benchmarks. On
OptiBench, NL4OPT, and IndustryOR, RL training after SFT yields consistent performance gains, demonstrating that
execution feedback continues to refine modeling capabilities beyond static supervision. These results validate that the
generate–execute–feedback–update loop remains effective even for solvers with limited pretraining coverage.

                                                                               19
                                     Execution-Verified Reinforcement Learning for Optimization Modeling

                            OptiBench                                        NL4OPT                                       MAMO EasyLP
                                                               0.80
                                                                                                               0.88
            0.55                                               0.75
 Accuracy




                                                    Accuracy




                                                                                                    Accuracy
                                                                                                               0.86
            0.50                                               0.70

                                                                                                               0.84
                                                               0.65
            0.45
                                                                                                               0.82
                     0     1000      2000    3000                     0   1000       2000    3000                     0   1000       2000    3000
                          Training Samples                                Training Samples                                Training Samples

                         MAMO ComplexLP                                     IndustryOR

                                                               0.24
               0.3
    Accuracy




                                                    Accuracy
                                                               0.22                                                       SFT Cold Start
               0.2                                             0.20                                                       GRPO After Cold Start

                                                               0.18
               0.1
                     0     1000      2000    3000                     0   1000       2000    3000
                          Training Samples                                Training Samples

Figure 7. Accuracy as a function of cold-start SFT data size on Gurobi. Curves compare SFT-only and SFT+RL training with varying data
scales from 60 to 3000 samples.




J. Analysis of Cold-Start Data Scale Impact on Gurobi
Figure 7 illustrates the impact of different SFT data scales on model performance during cold-start experiments with the
Gurobi solver. We systematically explored cold-start data ranging from 60 to 3,000 samples and tested two settings: SFT
training only and SFT followed by RL training.
The experimental results reveal a counter-intuitive phenomenon: more cold-start data is not necessarily better, and excessive
SFT data may actually harm subsequent reinforcement learning effectiveness. Using only a small number of cold-start
samples for SFT, combined with RL training, achieves performance comparable to or even exceeding large-scale SFT on
multiple benchmarks. This indicates that a small number of high-quality examples is sufficient to help the model establish
basic knowledge of the target solver’s API. However, when the cold-start data exceeds a certain scale, the effectiveness
of subsequent RL training noticeably decreases, with performance degradation observed on some benchmarks. Through
manual analysis of model outputs, we identified three typical problems in models trained with large-scale SFT: models
tend to overfit specific variable definition patterns in the SFT data, leading to incorrect variable type selection; large-scale
SFT causes models to generate longer, more complex code, introducing more potential syntax errors and logical flaws;
additionally, models tend to attempt more complex constraint expressions during RL training, but due to lack of correct
understanding of the underlying logic, this actually increases the proportion of infeasible solutions.
Based on the experimental results, we recommend prioritizing a strategy of using a small amount of cold-start data combined
with RL training for unfamiliar solvers to avoid overfitting caused by large-scale SFT. If high-quality translated data is
unavailable, one may also consider pure RL training starting from the zero-shot base model, using execution verification
feedback to explore solver syntax from scratch, although this approach has slower convergence.
We speculate that the potential mechanisms behind the decreased RL effectiveness after large-scale SFT training may involve
multiple aspects. Excessive SFT data may disrupt the general reasoning capabilities learned during pretraining, making
the model overly reliant on memorization rather than logical reasoning. Meanwhile, large-scale SFT causes the model to
converge prematurely to locally suboptimal strategies, making it more prone to reward hacking behavior in subsequent RL
training. Furthermore, SFT training reinforces specific code generation patterns, reducing the entropy of the policy and
making it difficult for the model to effectively explore new modeling paths during the RL phase. These findings provide
important guidance for designing cross-solver cold-start strategies, emphasizing the importance of combining moderate

                                                                             20
                             Execution-Verified Reinforcement Learning for Optimization Modeling

supervision with reinforcement exploration.

K. Evaluation of Sequential Transfer

Table 8. Appendix: Detailed Sequential Transfer Learning Dynamics. We evaluate model stability on the source solver (Gurobi) and
transferability to the target solver (OR-Tools) throughout the training stages. Results show that Sequential GRPO progressively improves
performance without sacrificing the original solver’s capabilities.

        Evaluation Suite     Training Stage                 OptiBench      NL4OPT        MAMO-E        MAMO-C        IndusOR
                             0. Base Model                     41.19         55.10         65.95          28.43         21.00
        On Gurobi            1. After Stage 1 (Gurobi)         59.96         80.81         85.58          36.01         31.00
                             2. After Stage 2 (OR-Tools)       60.46         81.22         87.57          30.80         23.00
                             Overall Gain (∆)                 +19.27         +26.12       +21.62         +2.37         +2.00
                             0. Base Model                     40.86         59.18         53.83          18.48         20.00
                             1. After Stage 1 (Gurobi)         54.15         78.77         81.59          27.48         24.00
        On OR-Tools
                             2. After Stage 2 (OR-Tools)       54.31         77.55         84.81          22.27         24.00
                             Transfer Gain (∆)                 +13.45        +18.37       +30.98         +3.79         +4.00


We further evaluate the Sequential Transfer strategy to verify the hypothesis that modeling competence is largely solver-
agnostic and can be disentangled from solver-specific syntax. In this experiment, we transfer a model trained exclusively in
EGurobi (ssrc ) to the OR-Tools environment (stgt ).
The results in Table 8 reveal a clear two-stage transfer pattern that supports our hypothesis. Initially, we observe a
significant “zero-shot” performance boost on the target solver: after training solely on Gurobi, the model’s accuracy on
OR-Tools benchmarks rises dramatically across all benchmarks. This empirical evidence confirms that the modeling
competence—specifically the ability to formulate optimization constraints and objectives—transfers effectively even before
the model encounters the target solver’s specific feedback. Subsequently, when the model is cold-started and trained in
EOR-Tools , performance further stabilizes. This second phase focuses the optimization on resolving residual API mismatches,
thereby substantially reducing the exploration cost compared to training on the target solver from scratch.

L. Experiment Results of Multi-Solver Generalization with Joint Training
This section presents comprehensive results of multi-solver joint training, where the model is trained simultaneously on
both Gurobi and OR-Tools environments. Table 9 and Table 10 report performance under relaxed (ϵeval = 0.05) and
stringent (ϵeval = 10−4 ) evaluation thresholds, respectively.

Results under Relaxed Evaluation (ϵeval = 0.05). As shown in Table 9, joint training yields consistent improvements
across both solvers. For OR-Tools, which has lower pretraining coverage, the gains are particularly pronounced across
all benchmarks. For Gurobi, the model also maintains strong performance with notable improvements across multiple
benchmarks. These results demonstrate that joint training effectively enables a single model to generalize across multiple
solvers without sacrificing solver-specific performance.

Results under Stringent Evaluation (ϵeval = 10−4 ). The stringent threshold more accurately detects modeling errors,
particularly incorrect variable type declarations. As shown in Table 10, execution-verified RL maintains robust improvements
even under this stricter criterion for both Gurobi and OR-Tools across all benchmarks. Importantly, while absolute
accuracy decreases compared to the relaxed evaluation, the relative gains from RL training remain substantial, indicating
that execution feedback guides the model toward more precise modeling strategies.

Summary. These results validate that multi-solver joint training is an effective strategy for building solver-agnostic
optimization modeling capabilities. The consistent improvements across both evaluation thresholds and both solvers confirm
that the execution-verified framework successfully captures transferable modeling competence rather than solver-specific
syntactic patterns.

                                                                  21
                             Execution-Verified Reinforcement Learning for Optimization Modeling

                               Table 9. Multi-solver generalization with joint training (ϵeval = 0.05).

            Solver                     OptiBench NL4OPT MAMO EasyLP MAMO ComplexLP IndustryOR
            Gurobi (before RL)            41.19       55.10           65.95                  28.43             21.00
            Gurobi (after RL)             61.79       82.04           84.96                  32.70             31.00
            ∆ (after – before)           +20.60       +26.94          +19.01                 +4.27            +10.00
            OR-Tools (before RL)          40.86       59.18           53.83                  18.48             20.00
            OR-Tools (after RL)           52.99       78.36           82.51                  20.38             27.00
            ∆ (after – before)           +12.13       +19.18          +28.68                 +1.90            +7.00

                                Table 10. Multi-solver generalization with joint training (ϵ = 10−4 ).

            Solver                     OptiBench NL4OPT MAMO EasyLP MAMO ComplexLP IndustryOR
            Gurobi (before RL)            34.05       48.97           82.82                  13.27            22.00
            Gurobi (after RL)             57.14       78.77           84.20                  30.33            23.00
            ∆ (after – before)           +23.09       +29.80          +1.38                 +17.06            +1.00
            OR-Tools (before RL)         24.25        37.14           44.93                   4.26            17.00
            OR-Tools (after RL)          32.55        45.71           71.62                   6.16            20.00
            ∆ (after – before)           +8.30        +8.57           +26.69                 +1.90            +3.00



M. Error Analysis
Table 11. Fine-grained error analysis on 500 sampled instances from OptiBench. Error types are categorized by human annotators before
and after RL training.

                                         Error Type       Before RL      After RL        Diff
                                      Implement Error       10.85%         7.17%       -3.68%
                                       Objective Error      12.98%        12.60%       -0.39%
                                      Constraint Error      18.02%        16.09%       -1.94%
                                       Variable Error        6.59%         0.78%       -5.81%
                                        Fully Correct       51.55%        63.37%      +11.82%


To gain a deeper understanding of the specific improvements that execution-verified reinforcement learning brings to
model capabilities, we conducted a fine-grained error classification analysis on the 500 samples from the human evaluation.
Figure 8 and Table 11 present the distribution changes of various error types before and after RL training.
We categorize the errors in model outputs into five types: Implementation Error includes code-level syntax errors, API call
errors, or runtime exceptions, reflecting the model’s mastery of solver interfaces; Objective Error encompasses mathematical
expression errors in the objective function, such as incorrect optimization direction, missing terms, or coefficient errors;
Constraint Error refers to logical errors, omissions, or redundancies in constraint conditions, which is the most common and
critical error type in operations research optimization modeling; Variable Error includes variable definition errors, such as
failing to correctly declare integer variables or incorrect variable bound settings; Fully Correct indicates no obvious errors in
both modeling logic and code implementation, yielding correct solution results.
Significant trends can be observed from Figure 8 and Table 11. Implementation errors decreased significantly, indicating that
RL training effectively reduced code-level syntax errors, with execution feedback successfully guiding the model to learn
correct API call patterns, directly improving code executability. Variable errors showed the largest improvement among all
error types. RL training, through solver feedback, enabled the model to correctly select variable types based on problem
characteristics, such as integer variables for discrete decisions and continuous variables for resource allocation, which has a
critical impact on solution quality. Constraint errors also decreased, though a notable fraction of samples still exhibited
such errors after RL training, reflecting the inherent difficulty of converting natural language constraints into mathematical
logic. Objective function errors showed only a marginal improvement, possibly because objective functions are typically
simpler and the base model already possesses strong understanding capabilities. The fully correct rate increased significantly,
validating the overall effectiveness of the execution verification framework.

                                                                 22
                            Execution-Verified Reinforcement Learning for Optimization Modeling

                                                                                                         2.1%




                               13.6%
                  22.4%                                                                       19.6%



                                                                                                                      43.9%

                                       37.2%
                 26.8%                                                                       34.4%




                         Before RL                                                                   After RL



                           Implement Error         Objective Error        Constraint Error           Variable Error


              Figure 8. Error type distribution before and after RL training on 500 sampled instances from OptiBench.




Table 11 reports the proportion of each error type over all 500 samples, while Figure 8 shows the proportion within the
erroneous subset only (i.e., excluding fully correct samples). The two perspectives reveal complementary insights. From the
table, the overall error rate drops substantially after RL training. From the figure, the relative composition of errors shifts
noticeably after RL training: implementation errors and variable errors decrease as a share of all errors, whereas constraint
errors and objective errors become more dominant. This compositional shift indicates that RL training preferentially
eliminates errors that are directly diagnosable through execution feedback (syntax and type errors), while the residual error
distribution becomes increasingly dominated by deeper semantic errors (constraints and objectives) that require logical
reasoning beyond what execution signals alone can provide.
Through fine-grained error analysis, we found that execution-verified reinforcement learning exhibits notably different
improvement effects across different dimensions. For error types that can be directly determined through execution feedback,
such as implementation errors and variable errors, RL training shows the most significant improvements; whereas for
error types requiring deep logical reasoning, such as constraint errors, improvements are relatively limited. This finding
points to directions for future method improvements, such as introducing more refined hierarchical reward mechanisms or
incorporating process hints for a small number of key constraints to further enhance the model’s capabilities in complex
constraint modeling.

N. Case Study
This section presents four representative successful cases covering different types of optimization problems: geometric
optimization, integer programming, resource allocation linear programming, and complex nonlinear programming. These
cases demonstrate the model’s capabilities in problem understanding, mathematical model construction, and executable
code generation.

   Case 1: Geometric Optimization (Nonlinear Programming)

   Problem: Of all rectangles of area 100, which has the smallest perimeter?

   Reasoning Process:


                                                                 23
                           Execution-Verified Reinforcement Learning for Optimization Modeling


To solve this problem, we need to find the rectangle with the smallest perimeter given that its area is 100. Let’s denote the length of
the rectangle by l and the width by w. The area of the rectangle is given by: l × w = 100. The perimeter P of the rectangle is
given by: P = 2l + 2w.
Our goal is to minimize the perimeter P subject to the constraint l × w = 100.

Generated Code:
 1   import gurobipy as gp
 2   from gurobipy import GRB
 3
 4   m = gp.Model("rectangle_optimization")
 5
 6   l = m.addVar(name="length", lb=0, ub=GRB.INFINITY)
 7   w = m.addVar(name="width", lb=0, ub=GRB.INFINITY)
 8
 9   m.setObjective(2*l + 2*w, GRB.MINIMIZE)
10   m.addConstr(l * w == 100)
11   m.optimize()
12
13   if m.status == GRB.OPTIMAL:
14       print(f"Just print the best solution: {m.objVal}")



Execution Result: 40.0        (Ground Truth: 40.0)     Correct




Case 2: Transportation Planning (Integer Programming)

Problem: A golf course is hosting an event and can transport guests using either golf carts or pull carts. A golf cart
can take 4 guests while a pull cart can take 1 guest. Since golf carts take up a lot of space, at most 60% of carts can be
golf carts. If the golf course needs to transport at least 80 guests, how many of each cart should be used to minimize
the total number of carts needed?

Reasoning Process:
Let x be the number of golf carts and y be the number of pull carts.
Objective: Minimize x + y
Constraints:
• Guest capacity: 4x + y ≥ 80
• Golf cart ratio: x ≤ 0.6(x + y) ⇒ y ≥ 23 x
• Non-negativity: x, y ≥ 0 and integer

Generated Code:
 1   import gurobipy as gp
 2   from gurobipy import GRB
 3
 4   m = gp.Model("golf_carts")
 5
 6   x = m.addVar(name="golf_carts", vtype=GRB.INTEGER, lb=0)
 7   y = m.addVar(name="pull_carts", vtype=GRB.INTEGER, lb=0)
 8
 9   m.setObjective(x + y, GRB.MINIMIZE)
10   m.addConstr(4*x + y >= 80, "guest_constraint")
11   m.addConstr(y >= (2/3)*x, "cart_constraint")
12   m.optimize()
13
14   if m.status == GRB.OPTIMAL:
15       print(f"Just print the best solution: {m.objVal}")



Execution Result: 29.0        (Ground Truth: 29.0)     Correct




                                                                  24
                          Execution-Verified Reinforcement Learning for Optimization Modeling

Case 3: Resource Allocation (Linear Programming)

Problem: There are two ways to extract a metal from mined ores. Process J can extract 5 units of metal using 8 units
of water and produces 3 units of pollution. Process P can extract 9 units of metal using 6 units of water and produces 5
units of pollution. There can be at most 1500 units of water and 1350 units of pollution. How many of each type of
processes should be performed to maximize the amount of metal extracted?

Reasoning Process:
Let x be the number of times process J is used, and y be the number of times process P is used.
Objective: Maximize 5x + 9y (total metal extracted)
Constraints:
• Water constraint: 8x + 6y ≤ 1500
• Pollution constraint: 3x + 5y ≤ 1350
• Non-negativity: x, y ≥ 0

Generated Code:
 1   import gurobipy as gp
 2   from gurobipy import GRB
 3
 4   m = gp.Model("metal_extraction")
 5
 6   x = m.addVar(name="x", vtype=GRB.INTEGER)
 7   y = m.addVar(name="y", vtype=GRB.INTEGER)
 8
 9   m.setObjective(5 * x + 9 * y, GRB.MAXIMIZE)
10   m.addConstr(8 * x + 6 * y <= 1500, "water_constraint")
11   m.addConstr(3 * x + 5 * y <= 1350, "pollution_constraint")
12   m.optimize()
13
14   if m.status == GRB.OPTIMAL:
15       print(f"Just print the best solution: {m.objVal}")



Execution Result: 2250.0        (Ground Truth: 2250.0)      Correct



Case 4: Agricultural Planning with Labor Optimization (Nonlinear Programming)

Problem: A farmer is planning to plant three types of crops: Wheat, Corn, and Soybeans. The farmer needs to decide
how many acres to allocate to each crop, as well as how many hours of labor to invest in each crop per acre.
                                    Crop         Yield/Acre     Price/Kg    Labor Cost/Hr
                                    Wheat          500 kg         $0.20           $10
                                    Corn           700 kg         $0.15           $12
                                    Soybeans       400 kg         $0.25            $8
The farmer has 100 acres and 500 labor hours available. At least 30 acres must be for Wheat. Labor per acre for each crop should
be at least 1 hour. Maximize net profit.

Reasoning Process:
Decision Variables:
• W, C, S: acres allocated to Wheat, Corn, Soybeans
• LW , LC , LS : labor hours per acre for each crop
Objective: Maximize (100W + 105C + 100S) − (10W LW + 12CLC + 8SLS )
Constraints: W + C + S ≤ 100, LW W + LC C + LS S ≤ 500, W ≥ 30, LW , LC , LS ≥ 1

Generated Code:
1    import gurobipy as gp
2    from gurobipy import GRB
3
4    m = gp.Model("crop_planning")
5
6    W = m.addVar(name="W", lb=30); C = m.addVar(name="C", lb=0); S = m.addVar(name="S", lb=0)




                                                                25
                         Execution-Verified Reinforcement Learning for Optimization Modeling


 7   L_W = m.addVar(name="L_W", lb=1); L_C = m.addVar(name="L_C", lb=1); L_S = m.addVar(name="L_S", lb=1)
 8
 9   m.setObjective(100*W + 105*C + 100*S - 10*W*L_W - 12*C*L_C - 8*S*L_S, GRB.MAXIMIZE)
10   m.addConstr(W + C + S <= 100, "total_acres")
11   m.addConstr(L_W*W + L_C*C + L_S*S <= 500, "total_labor")
12   m.optimize()
13
14   if m.status == GRB.OPTIMAL:
15       print(f"Just print the best solution: {m.objVal}")



Execution Result: 9210.0     (Ground Truth: 9210.0)   Correct




                                                          26
