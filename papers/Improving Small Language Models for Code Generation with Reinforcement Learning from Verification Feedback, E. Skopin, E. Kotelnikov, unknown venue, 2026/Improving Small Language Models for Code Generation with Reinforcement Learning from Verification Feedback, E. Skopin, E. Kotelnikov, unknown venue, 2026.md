                                                                                                             Записки научных
                                                                                                            семинаров ПОМИ
                                                                                                                Том ..., 2026 г.


                                            E. Skopin, E. Kotelnikov

                                            IMPROVING SMALL LANGUAGE MODELS FOR
                                            CODE GENERATION WITH REINFORCEMENT
                                            LEARNING FROM VERIFICATION FEEDBACK

                                                  Abstract. Reinforcement learning with verifiable rewards (RLVR)
arXiv:2605.30478v1 [cs.SE] 28 May 2026




                                                  trains language models using programmatically checkable signals
                                                  such as unit-test outcomes, enabling direct optimization for func-
                                                  tional correctness in code generation. We conduct an empirical study
                                                  of RLVR for Python code generation on the MBPP benchmark us-
                                                  ing two small models (Qwen3-0.6B and Llama3.2-1B) with LoRA
                                                  fine-tuning. Across multiple reward formulations such as: unit-test-
                                                  only rewards, static-analysis-only shaping via the Ruff linter, and
                                                  a combined reward, we compare group-based policy optimization
                                                  variants (GRPO and GSPO) and evaluate both functional correct-
                                                  ness and behavioral diagnostics. In our experimental setting, RLVR
                                                  improves pass@1 on MBPP test by up to 13 percentage points un-
                                                  der proposed combined reward configuration. However, we find that
                                                  reward shaping can induce systematic behavioral shifts: using only
                                                  static-analysis penalties may bias the policy toward shorter comple-
                                                  tions that reduce lint errors without reliably improving functional
                                                  correctness. In contrast, combined rewards mitigate this degenera-
                                                  tion and yield more stable trade-offs between correctness and style
                                                  constraints. Overall, our results highlight that RLVR effectiveness
                                                  for code generation is highly sensitive to reward design and opti-
                                                  mization granularity, and that diagnostics beyond pass@1, including
                                                  generation length, Ruff severity profiles, and execution error types
                                                  are useful for identifying failure modes.


                                                                       §1. Introduction
                                            Code generation with large language models (LLMs) has become a
                                         widely used paradigm for automating routine programming tasks, assisted
                                         development, and rapid prototyping [10]. Despite strong performance from
                                         instruction-tuned models, achieving high functional correctness remains
                                         challenging because training objectives (e.g., next-token prediction) are
                                         only indirectly aligned with execution behavior. A natural alternative is

                                            Key words and phrases: reinforcement learning and verifiable rewards and code gen-
                                         eration and unit tests and static analysis and MBPP and GRPO and GSPO and LoRA.

                                                                                   1
2                        E. SKOPIN, E. KOTELNIKOV


reinforcement learning with verifiable rewards (RLVR) [3], where rewards
are computed from automatically checkable criteria such as compilation
success, unit tests, or static analysis.
   In the code domain, unit tests provide a particularly compelling reward
signal: they are objective, reproducible, and directly tied to correctness.
However, RLVR is not only an “accuracy improvement” tool; it can also
change generation behavior in non-trivial ways. Reward design and opti-
mization choices can steer models toward undesirable equilibria, for exam-
ple, reward hacking [1].
   In this paper we test the following hypothesis using Mostly Basic Python
Problems (MBPP) dataset: RLVR can substantially improve functional
correctness, but its benefits are reward-sensitive; in particular, static-analysis-
only shaping may degenerate toward shorter solutions, while a combined
unit-test and static-analysis reward yields a more stable trade-off.
   We study RLVR in a controlled small-model setting where full training
runs are feasible. We train LoRA adapters for two architectures (Qwen3-
0.6B and Llama3.2-1B) and compare two group-based policy optimization
variants, GRPO and GSPO, under multiple reward designs: (i) unit-test-
only rewards, (ii) static-analysis-only shaping via Ruff, and (iii) combined
rewards. By analyzing both correctness and behavioral diagnostics, we
characterize when RLVR improves pass@1 and when it instead shifts the
model toward policies that primarily optimize proxy signals.
   Our contributions are as follows:
      • we provide a controlled comparison of GRPO vs. GSPO for RLVR
         on MBPP using small models;
      • we quantify the impact of different reward formulations on pass@1
         and on behavioral indicators (length, Ruff severity, and execution
         error types);
      • we document a reward-induced degeneration mode in our static-
         analysis-only setting and show that combined rewards mitigate
         this effect under the tested weights/normalization.

                           §2. Related Work
2.1. Code Generation Benchmarks. The evaluation of functional cor-
rectness in code generation is commonly performed using execution-based
benchmarks such as HumanEval [7] and Mostly Basic Python Problems
(MBPP) [13]. These benchmarks provide programming tasks paired with
unit tests, allowing to track objective metrics such as pass@k. For RLVR,
    IMPROVING SMALL LLMS FOR CODE GENERATION WITH RLVR                    3


these datasets are a natural fit because the evaluation signal (unit-test
outcomes) matches the reward family used during training, enabling a di-
rect assessment of whether reward optimization transfers to held-out tasks.
Execution-based evaluation yields structured failure signals (e.g., syntax
vs. runtime vs. assertion failures), and these error modes are informative
for diagnosing reward-induced shifts.
2.2. RL for Code. Several works have demonstrated that incorporating
execution feedback into reinforcement learning can improve functional cor-
rectness compared to purely supervised training. For example, CodeRL [4]
combines a pretrained code model with reinforcement learning driven by
unit test outcomes and introduces critic-based mechanisms to mitigate
reward sparsity. Subsequent studies have extended this line of work by de-
signing richer feedback signals. For example, StepCoder introduces curriculum-
style reinforcement learning with compiler/unit-test feedback [15]. CodeRL+
further pushes this direction by introducing execution semantics align-
ment, adding variable-level execution trajectory signals so that optimiza-
tion is guided by how the generated program behaves during execution [3].
However, RL with verifiable rewards is sensitive to reward shaping: aux-
iliary terms can introduce proxy objectives that are only loosely coupled
to semantic correctness. Recent work has emphasized reward hacking as
a practical concern in code-oriented RL environments and has proposed
benchmarks and taxonomies for detecting reward exploits [2].
2.3. Group-Based Policy Optimization. Group Relative Policy Opti-
mization (GRPO) was introduced in the DeepSeekMath work as a variant
of Proximal Policy Optimization (PPO) that eliminates the separate critic
using instead the baseline from group scores [5]. It has since been adopted
in large-scale LLM reinforcement learning, including DeepSeek-R1, for op-
timizing reasoning and other verifiable tasks.
   A complementary formulation, Group Sequence Policy Optimization
(GSPO), applies the group-relative objective at the sequence level rather
than at the token level [8]. Both objectives are relevant for reinforcement
learning with verifiable rewards (RLVR), where rewards are computed pro-
grammatically such as from unit tests.

                     §3. Method Description
3.1. Problem Setup. We study Python code generation from natural-
language specifications. Given a programming task described in text, the
4                          E. SKOPIN, E. KOTELNIKOV


model must produce a Python implementation of the required function
such that it satisfies a held-out set of unit tests. We use the Mostly Basic
Python Problems dataset, where each instance consists of (i) a short prob-
lem statement and (ii) reference tests that specify the desired behavior.
   Formally, for each task i we have a prompt xi (problem description,
optionally augmented with a signature hint) and a candidate program yi
generated by the model. Correctness is defined by execution: yi is consid-
ered correct if it compiles and passes all provided tests under the evaluation
harness. A typical MBPP task asks for a small utility function, e.g “Write
a python function to find the first repeated character in a given string”
   The expected output is a self-contained Python function definition that
can be executed by the test runner, for example:
           assert first_repeated_char("abcabc") == "a"
3.2. Base models. We conduct experiments with two small LLMs: (i)
Qwen3-0.6B [14] and (ii) Llama3.2-1B-Instruct [12]. Both models are
used in their instruct variants. All training is performed with parameter-
efficient adapters (LoRA) [11], while the underlying base model parameters
remain frozen.
3.3. Prompting. Each MBPP task provides a natural language problem
statement and reference tests. During generation, the model is prompted
with the problem description and the example of test case. It is important
to note that we provide only one example of test case and not the entire list
to avoid leaking potential solutions to the model. Example of the prompt
is shown in Figure 1. We post-process model outputs by extracting Python
code blocks and normalizing them into an executable module containing
the target function.
3.4. Reward Design. We consider three reward formulations:
     • Static-Analysis-Only Reward
     • Unit-Test-Only Reward
     • Combined Reward
3.4.1. Static-Analysis-Only Reward. In the first RLVR configuration, re-
wards are derived exclusively from static analysis feedback produced by
the Ruff linter 1. No unit test execution signal is used in this setting. The
objective is to encourage syntactically correct and stylistically clean code
1https://docs.astral.sh/ruff/
     IMPROVING SMALL LLMS FOR CODE GENERATION WITH RLVR                    5


      User: Please generate a python function for my problem. Do
      not provide any explanations, write only python code.

      Here is my problem:
      Write a python function to find the first repeated character
       in a given string.
      Test case example:
      assert first_repeated_char("abcabc") == "a"



        Figure 1. Example of generation prompt used in training
        process.

while evaluating how such shaping influences downstream functional cor-
rectness. For each generated completion y, we invoke Ruff in JSON-output
mode:
    ruff check --stdin-filename tmp.py --output-format=json
The generated source code is passed via standard input. Ruff returns a list
of issues E(y), where each issue contains a rule identifier and diagnostic
message.
   Each finding is mapped to a severity level:
                 severity(e) ∈ {error, high, normal, low},
using a predefined rule-to-severity mapping. If a rule identifier is not di-
rectly mapped, we attempt a fallback mapping using tokens extracted
from the diagnostic message. Unmapped errors or warnings default to the
normal severity level. Each severity level is associated with a fixed scalar
penalty:
w(error) = −10.0,     w(high) = −5.0,       w(normal) = −1.0,    w(low) = −0.2.
  Let Ns (y) denote the number of findings of severity s in completion y.
The total Ruff-based reward is defined as
                                 X
              Rruff (y) =                    w(s) · Ns (y).
                          s∈{error,high,normal,low}

  If Ruff produces no issues (i.e., E(y) = ∅) the reward is set to 0.
  This severity-to-penalty mapping is heuristic rather than learned or
tuned exhaustively. Its purpose is to encode an ordinal preference over
Ruff findings, assigning larger penalties to more severe issues while keeping
6                      E. SKOPIN, E. KOTELNIKOV


low-severity style violations weakly penalized. In this work, we use it as
a simple and interpretable shaping signal rather than claiming it is the
uniquely correct weighting scheme.

3.4.2. Length-Normalized Static-Analysis Reward. During the design of
the static-analysis-only reward, we identified a potential failure mode: the
model may reduce the total penalty simply by generating shorter and sim-
pler code, without actually improving correctness. Because Ruff penalties
are accumulated over the generated program, longer completions can re-
ceive larger negative rewards even when they represent reasonable solution
attempts.
   To mitigate this length bias, we introduce a normalized variant of the
static-analysis reward. Let
                                   X
                R̃ruff (y) =                     w(s) · Ns (y)
                          s∈{error,high,normal,low}

denote the unnormalized Ruff penalty, and let L(y) denote the number of
generated lines in completion y. We define the normalized reward as
                                                         !
                                       R̃ruff (y)
               Rruff-norm (y) = clip              , −1, 0 .
                                     max(1, L(y))
   Thus, the normalized static-analysis reward remains penalty-only: com-
pletions with no Ruff findings receive reward 0, while completions with
more or more severe findings receive negative reward. Normalization re-
duces sensitivity to output length and discourages degenerate behavior in
which the model minimizes penalties primarily by producing overly short
code.

3.4.3. Unit-Test-Only Reward. In the second RLVR configuration, rewards
are derived exclusively from functional correctness measured via unit test
execution. No static-analysis penalties are used in this setting. The objec-
tive is to directly optimize behavioral correctness under the MBPP evalu-
ation protocol.
   For each generated completion y, we extract the Python function imple-
mentation and evaluate it using the HumanEval-style execution harness.
Each completion is paired with the corresponding list of MBPP tests, in-
cluding both standard and challenge tests.
   Following prior work such as CodeRL [4], we employ a graded reward
mapping that differentiates between distinct failure modes. The execution
     IMPROVING SMALL LLMS FOR CODE GENERATION WITH RLVR                    7


result for each completion is categorized into one of the following outcome
classes:
      • Passed: all tests pass.
      • Assertion Error: test assertions fail or execution times out.
      • Runtime Error: runtime exceptions (e.g., TypeError, IndexError,
         ValueError, etc.).
      • Interpreter Error: syntax or interpreter-level failures (e.g., SyntaxError,
         NameError, IndentationError).
      • Other: uncategorized failures.
   Each outcome category is mapped to a scalar reward:
                      
                      
                        1.0, if Passed,
                      
                      −0.3, if Assertion Error,
          Runit (y) =
                      
                      
                       −0.6, if Runtime Error,
                        −1.0, if Interpreter Error or otherwise.
                      

   This design introduces graded penalties rather than a purely binary
reward. Interpreter-level failures receive the strongest penalty, reflecting
complete invalidity of the program. Runtime errors receive intermediate
penalties, while assertion failures incur milder penalties since the program
structure is valid but functionally incorrect.

3.4.4. Combined Reward: Unit Tests + Normalized Ruff Penalty. In the
third RLVR configuration, we combine execution-based unit test rewards
with a normalized, penalty-only static analysis signal from Ruff. The unit
test component remains identical to the unit-test-only setting (3.4.3), while
the Ruff signal is normalized to reduce sensitivity to output length. In
addition, we apply a small anti-shortcut penalty to discourage degenerate
“empty” generations.
   Let E(y) denote the set of Ruff issues for completion y and let Ns (y) be
the number of issues assigned to severity level s ∈ {error, high, normal, low}
(using the same severity mapping as in the Ruff-only setting). We first
compute the raw Ruff penalty as a weighted sum:
                                    X
                         Rraw (y) =     w(s) Ns (y),
                                     s

If Ruff produces no findings, Rraw (y) = 0. If Ruff fails (e.g., invalid JSON
output), we assign a mild penalty of −0.5.
8                         E. SKOPIN, E. KOTELNIKOV


   Because Rraw (y) scales with the number of lines and may introduce a
length bias, we normalize it by the number of lines:
                                           Rraw (y)
                           Rline (y) =                ,
                                         max(1, L(y))

where L(y) is the number of lines in y.
  Finally, we clip the normalized penalty into a bounded interval to pre-
vent rare bursts of violations from dominating the reward:
                                                 
           Rruff (y) = clip Rline (y), [cmin , 0] , cmin = −1.0,

so that Rruff (y) ∈ [−1, 0].
   To discourage trivial completions that avoid both unit test failures and
static analysis findings by producing almost no code, we apply a length-
based penalty:
                          (
                             −0.5, if chars(y) < 30 or L(y) < 3,
            Rshort (y) =
                              0,   otherwise.

   We combine unit test reward Runit (y) (3.4.3) with Ruff and anti-shortcut
signals using a pass-gated weighting scheme. The final reward is:
             (
              Runit (y) + λpass Rruff (y) + Rshort (y), if Runit (y) = 1.0 (Passed),
Rcomb (y) =
              Runit (y) + λfail Rruff (y) + Rshort (y), otherwise,

where λpass , λfail are specified constants introduced to regulate “ruff“ com-
ponent importance.
   This “gate” prevents Ruff penalties from dominating optimization on
failing solutions (where functional correctness has not yet been achieved),
while still encouraging cleaner code among already-correct solutions.

3.5. Group policy optimization. Given a prompt x, we sample a group
of G candidate completions {yi }G
                                i=1 from the current policy and compute
scalar rewards {Ri }. We form a group-relative advantage (TRL default is
a simple group baseline; optionally normalized):
                G
             1 X                                                  Ai
      R̄ =         Rj ,     Ai = Ri − R̄      (optionally Ai ← std(R)+ϵ ).   (1)
             G j=1
     IMPROVING SMALL LLMS FOR CODE GENERATION WITH RLVR                             9


Let yi = (ai,1 , . . . , ai,Ti ) and denote the token-level likelihood ratio (im-
portance weight) between the new policy πθ and the sampling policy πθold :
                                          πθ (ai,t | x, ai,<t )
                            ri,t (θ) =                            .               (2)
                                         πθold (ai,t | x, ai,<t )
Token-level GRPO (TRL). GRPO applies a PPO-style clipped policy-
gradient objective at the token level, using the same scalar group advantage
Ai for all tokens of a sampled completion:
                       G     Ti
                   1 X 1 X                                                
    LGRPO (θ) =                  min ri,t Ai , clip(ri,t , 1 − ε, 1 + ε)Ai
                   G i=1 Ti t=1                                                  (3)
                                                   
                   − β KL πθ (· | x) ∥ πref (· | x) .
where ε is the clip range and β controls KL regularization to a reference
policy πref .
Sequence-level GSPO (GRPO variation in TRL):. GSPO uses the same
group-relative advantage, but moves the importance weighting to the se-
quence level by aggregating log-probability ratios across the entire com-
pletion:
                              Ti
         πθ (yi | x)        X                                                         
ri (θ) =               = exp     log πθ (ai,t | x, ai,<t )−log πθold (ai,t | x, ai,<t ) .
        πθold (yi | x)       t=1
                                                                                 (4)
The clipped objective is then applied once per completion:
                             G
                         1 X                                              
           LGSPO (θ) =         min ri (θ)Ai , clip(ri (θ), 1 − ε, 1 + ε)Ai
                         G i=1                                                   (5)
                                                         
                         − β KL πθ (· | x) ∥ πref (· | x) ,
Compared to token-level GRPO, GSPO assigns a single importance weight
to each sampled completion, which changes the credit assignment and can
yield different length/entropy dynamics under the same reward.

                                §4. Experiments
4.1. Dataset. We use the Mostly Basic Python Problems (MBPP) bench-
mark [13], which consists of short Python programming tasks paired with
reference solutions and unit tests. MBPP provides predefined splits; we
use MBPP train for RLVR training and report primary results on the
MBPP test split.
10                    E. SKOPIN, E. KOTELNIKOV


  In addition, we perform a stricter external evaluation using EvalPlus
benchmarks (MBPP-Plus and HumanEval-Plus) [9], described in Section 4.6.
  We do not modify tasks or tests; all comparisons use the same evaluation
harness. There are 974 tasks in total:
     • 374 in train split,
     • 500 in test split,
     • 90 in validation split,
     • 10 in “prompt“ split (used for few-shot prompts)
4.2. Metrics. We report pass@1 on MBPP test, i.e., the fraction of tasks
for which the first sampled solution passes all tests [7].
   For failing tasks, we record the dominant failure mode from execution
traces (e.g., AssertionError, TypeError, NameError, SyntaxError) and
report category frequencies.
   We report the average number of Ruff findings per task, stratified by
severity levels.
   We report mean generated tokens per run and study its correlation with
pass@1 and reward configurations.
4.3. Training Details. All RLVR training is performed using LoRA
adapters [11]. We keep base weights frozen and optimize only adapter
parameters. We use:
     • Number of generations per sample = 8,
     • Batch Size (Prompts per Update) = 1,
     • Gradient Accumulation Steps = 1,
     • learning rate = 1 × 10−5 ,
     • epochs = 5,
     • sampling temperature = 0.9
     • max tokens = 768,
     • LoraRank = 32,
     • Loraα = 64,
     • KL coefficient β = 0.0 (no refernce model loaded),
     • ϵ = 0.2 (for clipping),
     • λpass = 0.3,
     • λf ail = 0.1,
     • Random State = 42
For LoRa adapter we target several modules such as:
     • Self-Attention projections:
          – q_proj - Query projection WQ
       IMPROVING SMALL LLMS FOR CODE GENERATION WITH RLVR                11


         – k_proj - Key projection WK
         – v_proj - Value projection WV
         – o_proj - Attention output projection WO
     • Feed-Forward (MLP) projections:
         – up_proj - Expansion projection Wup
         – gate_proj - Gating projection Wgate
         – down_proj - Contraction projection Wdown
We evaluate the following methods (matching the labels used in figures):
     • normal: base model inference with the same decoding parameters
       (no RLVR).
     • grpo-unit, gspo-unit: RLVR with unit-test rewards only.
     • grpo-ruff, gspo-ruff : RLVR with Ruff shaping only.
     • grpo-combined, gspo-combined: combined reward.
4.4. Test evaluation. After fine-tuning with RLVR to evaluate the model’s
quality we make several runs. For each run we take MBPP test split, gen-
erate solutions for each task, using same methods as in training process
we extract code, add test cases (both from basic test list and challenge
test list) and evaluate the solution. We report pass@1 for each run and
provide mean ± SD for each method. We use decoding with sampling with
temperature T = 0.6 and max token count max_tokens = 768.
   Our primary baseline is the corresponding normal pretrained model for
each architecture using the same prompt formatting and decoding settings.
4.5. Implementation. Training and evaluation scripts were done with
Python 3.12.12, using Transformers v4.57.6 [16], TRL 0.24 [17], Unsloth
2026.1.4 [18] with Pytorch 2.10. For code and test execution we utilize
OpenAI human-eval python module 2. Static analysis feedback was pro-
vided by using Ruff 0.14.11 3 with default ruleset (Flake8’s F rules, along
with a subset of the E rules).
   All training runs were done on rented GPU-server with Nvidia RTX
3090 (24GB VRAM), while test evaluations were performed on PC with
Nvidia RTX 5060Ti (16GB VRAM).
4.6. EvalPlus evaluation. To complement the main MBPP test evalua-
tion, we additionally evaluate selected reward configurations using EvalPlus
[9] on MBPP+ and HumanEval+, which provide a stricter hidden-test
2https://github.com/openai/human-eval
3
    https://docs.astral.sh/ruff
12                      E. SKOPIN, E. KOTELNIKOV


benchmark for functional correctness. For this evaluation, we retrain each
reward configuration with two random seeds (101 and 202) and report per-
seed pass@1 results. Inference is performed with an OpenAI-compatible
vLLM backend (v0.17.0) [6] using greedy decoding. We evaluate on both
the base and the additional hidden tests provided by EvalPlus.


                    §5. Results and Discussion
5.1. Overall Performance. For each combination of model and method
we ran 10 test evaluations. Table 1 reports mean pass@1 on MBPP test set
and p-value. We compute the p-value with a paired randomization (sign-
flip) test over tasks: we repeatedly flip the sign of each task’s method base-
line score difference at random to simulate the null hypothesis of “no effect“
and report the fraction of simulations where the resulting mean difference
is at least as extreme as the observed one. We observe consistent gains from
RLVR with unit-test only and combined rewards across both model fam-
ilies, with the best combined-reward configuration of Qwen3-0.6B model
using Combined Reward improving pass@1 by up to 13 percent points
over the baseline. Across the reported settings, neither GRPO nor GSPO
consistently dominates the other. A plausible explanation is that MBPP
and HumanEval consist of relatively short, self-contained tasks with short
prompts and completions, so the benefit of sequence-level optimization is
less pronounced than it might be in longer-horizon settings.

5.2. Error Analysis. Figure 2 shows the distribution of execution out-
comes. For combined and unit-test only we can see reduction of Asser-
tionErrors and an increase in the fraction of passed solutions. We also
observe method-specific shifts among runtime and interpreter errors (e.g.,
NameError, TypeError), suggesting that different objectives may prioritize
distinct correctness improvements (semantic vs. syntactic robustness).

5.3. Static Analysis Effects. Figure 3 reports Ruff findings by severity.
Static-analysis shaping substantially changes the distribution of findings,
but these improvements do not always translate proportionally into higher
pass@1. This highlights a key RLVR tradeoff: optimizing a proxy reward
(style/quality signals) can steer generation away from test-passing correct-
ness if not calibrated carefully.
    IMPROVING SMALL LLMS FOR CODE GENERATION WITH RLVR                          13


  Model              Method               pass@1        ∆ vs normal   p-value
                   gspo-combined       0.417 ± 0.016      +0.144      5.0e-6
                   grpo-combined        0.415 ± 0.010     +0.142      5.0e-6
                     gspo-unit          0.412 ± 0.010     +0.139      5.0e-6
                     grpo-unit          0.388 ± 0.012     +0.115      5.0e-6
  Qwen3-0.6B
                       normal           0.273 ± 0.007        –           –
                grpo-ruff-normalized    0.253 ± 0.006     -0.020      5.0e-6
                      grpo-ruff         0.252 ± 0.009     -0.021      2.6e-2
                gspo-ruff-normalized    0.249 ± 0.008     -0.024      5.0e-6
                      gspo-ruff         0.232 ± 0.008     -0.041      3.5e-4
                   grpo-combined       0.389 ± 0.008      +0.040      9.5e-4
                   gspo-combined        0.383 ± 0.009     +0.034      4.9e-3
                     grpo-unit          0.379 ± 0.010     +0.030      1.8e-3
  Llama3.2-1B        gspo-unit          0.375 ± 0.014     +0.026      4.7e-3
                       normal           0.349 ± 0.010        –           –
                      grpo-ruff         0.313 ± 0.011     -0.036      4.5e-4
                      gspo-ruff         0.312 ± 0.010     -0.037      3.5e-5
                grpo-ruff-normalized    0.294 ± 0.010     -0.055      5.0e-6
                gspo-ruff-normalized    0.287 ± 0.011     -0.062      5.0e-6


        Table 1. MBPP test pass@1 (mean ± SD over runs). ∆ in-
        dicates absolute improvement over the corresponding nor-
        mal baseline.


5.4. Length Degeneration. Figure 4 plots mean number of generated
tokens vs pass rate across runs. We can observe that Ruff-dominant config-
uration tend to produce shorter output while having lower pass rate. This
static-analysis only configuration skews model into reward-driven degen-
eration which incentives simple code that reduces style violations without
improving functional correctness. While unit-test configuration tend to
produce longer outputs with bigger pass rates. These findings motivate
reporting behavioral diagnostics alongside pass@1 for RLVR-trained code
models.

5.5. External Validation with EvalPlus. So far, the previous results
were based on the MBPP test split and its associated diagnostics. To as-
sess whether these patterns transfer to a stricter hidden-test setting, we
additionally evaluate independently retrained adapters on EvalPlus bench-
marks (MBPP+ and HumanEval+). Table 2 reports per-seed results for
both model families.
14                E. SKOPIN, E. KOTELNIKOV




     Figure 2. Execution outcome distribution on MBPP test
     (mean over runs).
IMPROVING SMALL LLMS FOR CODE GENERATION WITH RLVR              15




  Figure 3. Ruff finding severity distribution (average find-
  ings per task).
16                 E. SKOPIN, E. KOTELNIKOV




     Figure 4. Run-level mean generated tokens vs MBPP pass
     rate.
    IMPROVING SMALL LLMS FOR CODE GENERATION WITH RLVR                                17


   The overall pattern remains similar to the main MBPP analysis. Static-
analysis-only methods remain unstable and often weak, while the unit-test-
only and combined reward families are generally stronger. However, under
stricter evaluation, the combined reward is competitive in some settings
but does not provide a consistent improvement over the unit-test-only
reward across both models and both benchmarks. These results suggest
that the benefits of reward shaping are sensitive to evaluation protocol
and do not always transfer uniformly to stronger hidden-test settings.

                              Qwen3-0.6B                      Llama-3.2-1B
                        MBPP+         HumanEval+        MBPP+         HumanEval+
    Method            101      202     101    202      101     202     101    202
    Base              0.405   0.405   0.384   0.384   0.407   0.407   0.311   0.311
    Ruff GRPO         0.405   0.267   0.256   0.244   0.429   0.399   0.299   0.293
    Ruff GSPO         0.265   0.344   0.244   0.268   0.429   0.302   0.287   0.305
    Ruff-norm GRPO    0.357   0.302   0.299   0.268   0.386   0.399   0.341   0.317
    Ruff-norm GSPO    0.399   0.312   0.280   0.274   0.376   0.407   0.323   0.329
    Unit-tests GRPO   0.508   0.526   0.396   0.396   0.434   0.437   0.341   0.354
    Unit-tests GSPO   0.460   0.537   0.323   0.366   0.450   0.447   0.335   0.335
    Combined GRPO     0.484   0.503   0.402   0.396   0.442   0.452   0.360   0.348
    Combined GSPO     0.526   0.505   0.372   0.396   0.471   0.450   0.439   0.348


        Table 2. Per-seed EvalPlus results for independently re-
        trained adapters.



                              §6. Limitations
   Currently all the experiments were done with test split of MBPP dataset
and EvalPlus benchmark. These benchmarks consist of short, mostly self-
contained Python programming tasks with relatively small test suites. As
a result, conclusions may not transfer to long-horizon code generation set-
tings
   Our reward formulations include several heuristic design decisions:
      • a graded unit-test reward mapping,
      • a Ruff-derived penalty,
      • a line-normalized and clipped Ruff reward in the combined setting
These choices were motivated by stability and practical considerations,
but they introduce additional hyperparameters (e.g., clipping threshold,
18                     E. SKOPIN, E. KOTELNIKOV


weighting (λ) coefficients, length thresholds) that may affect outcomes.
We did not perform exhaustive tests over these parameters, and alternative
normalizations or weight schedules could yield different trade-offs.
    We evaluate two small models (Qwen3-0.6B and Llama3.2-1B), which
still leaves open whether the same reward-shaping effects hold for larger
models or for models trained with different instruction-tuning schemes.


                            §7. Conclusion
    We presented a study of reinforcement learning with verifiable rewards
(RLVR) for Python code generation on MBPP using two small language
models, Qwen3-0.6B and Llama3.2-1B. Across both architectures, RLVR
improves functional correctness, with the best configuration achieving up
to +13 percent points in pass@1 over the corresponding baseline. Re-
garding the optimization variants, we do not observe a universal winner
between token-level GRPO and sequence-level GSPO. Both variants are
capable of improving performance under suitable reward design, and nei-
ther is uniformly dominant across any tests. A more decisive comparison
between GRPO and GSPO may require longer-horizon code-generation
benchmarks, where sequence-level credit assignment is expected to matter
more strongly than in short benchmark tasks such as MBPP and Hu-
manEval. Our analysis also shows that reward design induce behavioral
shifts. First, unit-test-driven RLVR substantially changes the failure pro-
file, we can observe not only reduction in Assertion Errors (failing unit
tests), but also with Type and Name Errors. Second, static-analysis re-
wards affects code quality diagnostics but does not necessarily translate
into higher pass@1: Ruff-optimized runs shift severity distributions toward
fewer “error“-level severity issues, yet can underperform in functional cor-
rectness when the static penalty dominates the learning signal. Third, we
find that static-analysis penalties interact strongly with output length.
According to our tests, Ruff-heavy objectives tend to produce shorter gen-
erations, whereas combined rewards shift the model toward longer com-
pletions that correlate with higher pass@1. Overall, the results emphasize
that RLVR for code should be evaluated with diagnostics beyond pass@1,
including execution error categories, static-analysis profiles, and length
statistics.
    Future work includes more extensive reward-weight sweeps, training-
dynamics analysis (KL/reward curves), systematic sensitivity analysis of
     IMPROVING SMALL LLMS FOR CODE GENERATION WITH RLVR                                 19


the Ruff severity weights, including alternative scaling schemes and sever-
ity groupings and extending the approach to additional datasets and lan-
guages.

                                    References
 1. Zhang, K., Zuo, Y., He, B., Sun, Y., Liu, R., Jiang, et al., A Survey of Reinforcement
    Learning for Large Reasoning Models. (2025), https://arxiv.org/abs/2509.08827
 2. Darshan Deshpande and Anand Kannappan and Rebecca Qian, Benchmarking
    Reward Hack Detection in Code Environments via Contrastive Analysis, 2026.
    https://arxiv.org/abs/2601.20103
 3. Jiang, X., Dong, Y., Liu, M., Deng, H., Wang, T., T, et al., CodeRL+: Improving
    Code Generation via Reinforcement with Execution Semantics Alignment. (2025),
    https://arxiv.org/abs/2510.18471
 4. Hung Le, Yue Wang, Akhilesh Deepak Gotmare, Silvio Savarese, and Steven C. H.
    Hoi, CodeRL: Mastering Code Generation through Pretrained Models and Deep
    Reinforcement Learning, arXiv preprint arXiv:2207.01780, 2022.
 5. Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, et al., DeepSeek-
    Math: Pushing the Limits of Mathematical Reasoning in Open Language Models,
    arXiv preprint arXiv:2402.03300, 2024.
 6. Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng, Cody Hao
    Yu, Joseph E. Gonzalez, Hao Zhang, and Ion Stoica, Efficient Memory Management
    for Large Language Model Serving with PagedAttention, In Proceedings of the ACM
    SIGOPS 29th Symposium on Operating Systems Principles, 2023.
 7. Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde de Oliveira
    Pinto, Jared Kaplan, et al., Evaluating Large Language Models Trained on Code,
    arXiv preprint arXiv:2107.03374, 2021.
 8. Chujie Zheng, Shixuan Liu, Mingze Li, Xiong-Hui Chen, Bowen Yu, et al., Group
    Sequence Policy Optimization (GSPO) for Verifiable Rewards, arXiv preprint
    arXiv:2507.18071, 2025.
 9. Liu, J., Xia, C. S., Wang, Y., and Zhang, L., Is Your Code Generated by ChatGPT
    Really Correct? Rigorous Evaluation of Large Language Models for Code Genera-
    tion, Thirty-seventh Conference on Neural Information Processing Systems, 2023,
    https://openreview.net/forum?id=1qvx610Cu7
10. Jiang, J., Wang, F., Shen, J., Kim, S. & Kim, S. A Survey on Large Language
    Models for Code Generation. ACM Transactions On Software Engineering And
    Methodology. 35, 1-72 (2026,1), http://dx.doi.org/10.1145/3747588
11. Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean
    Wang, and Weizhu Chen, LoRA: Low-Rank Adaptation of Large Language Models,
    arXiv preprint arXiv:2106.09685, 2021.
12. Meta      AI.     Llama-3.2-1B-Instruct       (model       card).    Hugging      Face,
    https://huggingface.co/meta-llama/Llama-3.2-1B-Instruct, 2024.
13. Jacob Austin, Augustus Odena, Maxwell Nye, Maarten Bosma, Henryk
    Michalewski, David Dohan, et al., Program Synthesis with Large Language Models,
    2021.
14. Team, Q. Qwen3 Technical Report. (2025), https://arxiv.org/abs/2505.09388
20                         E. SKOPIN, E. KOTELNIKOV


15. Dou, S., Liu, Y., Jia, H., Xiong, L., Zhou, E., et al., StepCoder: Improve
    Code Generation with Reinforcement Learning from Compiler Feedback. (2024),
    https://arxiv.org/abs/2402.01391
16. Wolf, T., Debut, L., Sanh, V., Chaumond, J., Delangue, C., , et al., Transformers:
    State-of-the-Art Natural Language Processing. Proceedings Of The 2020 Conference
    On Empirical Methods In Natural Language Processing: System Demonstrations.
    pp. 38-45 (2020,10), https://www.aclweb.org/anthology/2020.emnlp-demos.6
17. Werra, L., Belkada, Y., Tunstall, L., Beeching, E., Thrush, T., Lambert, N., Huang,
    S., Rasul, K. & Gallouédec, Q. TRL: Transformers Reinforcement Learning. (2020),
    https://github.com/huggingface/trl
18. Daniel Han, M. & Team, U. Unsloth. (2023), https://github.com/unslothai/unsloth
                                                            Поступило 1 March 2026

                                                 (E. Skopin) Vyatka State University
                                                E-mail: eclipsingstasr00@gmail.com

                               (E. Kotelnikov) European University at St. Petersburg
                                                  E-mail: kotelnikov.ev@gmail.com
