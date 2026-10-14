                                                        Evaluation of LLMs for Mathematical Formalization in Lean


                                         Tyson Klingner * 1 Drew Bladek * 1 Escher Crawford * 1 Bohao Chen 1 Ariel Fu 1 Kaira Nair 1 Jarod Alper 1
                                                                             Giovanni Inchiostro 1 Vasily Ilin 1


                                                                  Abstract                                 DeepMind, 2025). However, it is currently difficult to verify
                                                                                                           the correctness of a natural language proof in an automated
                                               Within the past few years, the ability of Large Lan-
                                                                                                           way (Lightman et al., 2024).
                                               guage Models (LLMs) to generate formal mathe-
                                               matical proofs has improved drastically. We pro-            Alternatively, we can task LLMs to produce a formal lan-
arXiv:2606.05632v1 [cs.AI] 4 Jun 2026




                                               vide a comparison of various LLMs’ effective-               guage proof (Zhou et al., 2025). Formalization of mathe-
                                               ness in producing formal proofs in Lean 4 with              matical proofs gives an objective metric to confirm a proof’s
                                               the goal of assisting those seeking to use LLMs             correctness. Namely, we can use a formal theorem proving
                                               to support their own projects. We utilize both              system such as Lean 4 (Moura & Ullrich, 2021). LLMs have
                                               pass@k and refine@k metrics as the benchmark                recently shown strong improvements in formal proof gener-
                                               for our comparison and evaluate on subsets of               ation in Lean 4 (Han et al., 2025; Polu et al., 2023). Most
                                               both miniF2F and miniCTX datasets. Our testing              notably, Google’s AlphaProof achieved a silver-medal per-
                                               shows that overall, Gemini 3.1 Pro and Claude               formance in the 2024 IMO when producing formal proofs
                                               Opus 4.7 perform best. Gemini 3.1 Pro achieved              in Lean 4 (Hubert et al., 2025).
                                               a 92% success rate on miniF2F via refine@32
                                                                                                           With an abundance of readily available LLMs it is natural to
                                               whereas Opus 4.7 achieved a 86% success rate on
                                                                                                           ask which LLM is the best at formal proof generation. The
                                               miniCTX via refine@32. When taking cost into
                                                                                                           current options span from general-purpose frontier models,
                                               account, NVIDIA Nemotron 3 Super and GPT-
                                                                                                           e.g. Google Gemini 3.1 Pro, to Lean specialized models, e.g.
                                               OSS 120B were the most efficient, with competi-
                                                                                                           Goedel-Prover V2 (Lin et al., 2026) and Mistral’s Leanstral
                                               tive accuracies and average costs of < $0.01 per
                                                                                                           (AI, 2026). Moreover, for the general mathematician, there
                                               correct proof.
                                                                                                           are many real world factors to consider before selecting a
                                                                                                           model for formal proof generation, including cost and access
                                                                                                           to computing power. In this paper, we compare several
                                        1. Introduction                                                    general and special purpose LLMs’ capability in formal
                                        Proving mathematical theorems often requires a complex             proof generation. More specifically, we fix an n = 50 size
                                        chain of arguments, logical deductions, and involves tedious       subset of both miniF2F (Zheng et al., 2022) and miniCTX
                                        computations. As such, the ability to prove theorems is            (Hu et al., 2025) datasets and utilize both the Pass@k (Chen
                                        emblematic of human intelligence and reasoning. Hence,             et al., 2021) and Refine@k (Xu et al., 2026) methodologies
                                        evaluating a Large Language Model’s (LLMs) ability to              for k = 32. See Table 2.1 for a complete list of models
                                        produce mathematical proofs provides an important bench-           considered. Beyond measuring proof success rates, we also
                                        mark to measure a given model’s reasoning ability (Liu             analyze computational cost. Our goal is to provide a clear
                                        et al., 2025). A natural starting point in this direction is       and practical comparison of different models and strategies,
                                        getting LLMs to produce natural language proofs (Zhang             to help identify which approaches are most effective under
                                        et al., 2026). For example, advanced versions of Google’s          real-world resource constraints.
                                        Deep Think achieved a gold-medal level performance in the          Our contributions are as follows:
                                        2025 International Mathematical Olympiad (IMO) (Google
                                           1                                                                 1. A comprehensive standardized evaluation of a wide
                                            Math AI Lab, University of Washington, Seattle, WA, USA.
                                        Correspondence to: Tyson Klingner <tysonk4@uw.edu>,                     array of LLMs for formal proof generation.
                                        Drew Bladek <abladek@uw.edu>,            Escher Crawford             2. An extensive analysis of the cost efficiency.
                                        <ecraw4d@uw.edu>, Bohao Chen <bohaoc@uw.edu>, Ariel Fu
                                        <xinyuf3@uw.edu>, Kaira Nair <kaira@uw.edu>, Jarod Alper             3. A detailed comparison between the pass@k and
                                        <alper@uw.edu>, Giovanni Inchiostro <ginchios@uw.edu>,                  refine@k methods.
                                        Vasily Ilin <vilin@uw.edu>.
                                                                                                             4. A thorough categorization of error trends between mod-
                                        Preprint. June 5, 2026.                                                 els.

                                                                                                       1
                                  Evaluation of LLMs for Mathematical Formalization in Lean

2. Methodology                                                         To ensure that minor deviations from the requested format-
                                                                       ting do not produce false negatives, our extraction pipeline
In this section, we explain every step and procedure in order          utilizes a cascading fallback strategy: it prioritizes the re-
so that the reader can reproduce our results. See https:               quested FINAL templating, next checking for generic Lean
//github.com/uw-math-ai/LLMsLean for the ex-                           tags (e.g., lean4), and ultimately locates theorem or lemma
plicit code used.                                                      keywords if the model embeds the code in plain text.

2.1. Datasets                                                          We used a temperature of 0.5 in order to have enough varia-
                                                                       tion in responses for the pass@k metric to be useful, while
We construct our benchmark upon two complementary eval-                maintaining enough consistency so that the refine@k strat-
uation datasets: miniF2F (Zheng et al., 2022), which evalu-            egy would depend mostly on prompt feedback as opposed
ates mathematical reasoning on isolated, competition-level             to randomness. See Section 2.5 for the definition of pass@k
problems (e.g., IMO, AMC, AIME), and miniCTX (Hu                       and refine@k. The exception to this is Opus 4.7, for which
et al., 2025), which tests the model’s ability to operate within       the API did not accept a temperature setting. The models
a heavily-imported theorem structures intended to mimic                were allowed a token budget of 16384 for reasoning, which
real-world mathematical work.                                          was chosen to limit time and cost if the model got stuck in a
Evaluating frontier LLMs over the entirety of both datasets            loop while still allowing adequate tokens for thinking and
is expensive. To evaluate the models in a more cost-effective          output.
manner, we instead work over a subset of size n = 50 for
both miniF2F and miniCTX. To limit selection bias we em-               2.4. Verification Protocols
ploy sampling strategies based on the datasets structure. For          To prevent models bypassing the verification, our module
miniF2F, we utilize proportional stratified sampling. We               sanitizes responses before compilation. Specifically, we
categorized problems into explicit strata (e.g., imo, amc12,           filter out outputs containing sorry, admit, or omitted macros,
aime, algebra, induction, numbertheory), and randomly sam-             which are tactics that bypass proofs but satisfy the compiler.
pled from each stratum in exact proportion to its frequency            A generated proof is labeled as a Pass precisely when it
in the whole dataset. On the other hand, for miniCTX the               compiles cleanly in the Lean 4 environment without errors or
problem domain is generally homogeneous and lacks ex-                  bypass statements, ensuring machine-checkable correctness.
plicit categorical distinctions, so we take a simple random
sample across the total dataset. This approach ensures that            Furthermore, to prevent models from altering theorem
both subsets remain statistically representative snapshots of          premises, we enforce strict structural extraction. Our
their respective original benchmarks.                                  pipeline isolates the proof body from the model’s response
                                                                       and then combines it with the datasets formal statement.
2.2. Models                                                            This structural safeguard guarantees that the Lean verifier
                                                                       evaluates the exact target theorem, neutralizing any halluci-
We evaluate a comprehensive suite of models, structurally              nated modifications to the problem definition. Evaluation
categorized by their purpose and availability: Proprietary             was performed using LeanInteract to interface between our
Frontier Models, Open-Weight General-Purpose, and Lean-                pipeline and the Lean Kernel.
Specialized Provers. Table 2.1 lists the models considered
and API endpoints utilized to ensure benchmark repro-                  2.5. Evaluation: Pass@k and Refine@k
ducibility. For Goedel, both models were run on NVIDIA
H200 GPUs with 2 for 32B and 1 for 8B. We used 2 GPUs                  We evaluate the models under two distinct generation meth-
for 32B since initial testing showed 1 GPU had insufficient            ods, choosing a maximum of k = 32 to balance computa-
VRAM.                                                                  tional costs with generating accurate and reliable data. Our
                                                                       methods are as follows:
2.3. Prompting and Model Settings
                                                                          • Pass@k: We generate n = 32 independent proofs
To ensure a fair comparison across a diverse field of LLMs,                 for each theorem at a temperature of t = 0.5. The
our framework uses a standardized zero-shot prompting                       Pass@k metric estimates the probability that at least
paradigm. The agent is minimally contextualized and in-                     one out of k independent samples successfully verified
structed to output the proof within a designated markdown                   in the Lean environment. (Chen et al., 2021). Taking
block, assuming all Mathlib dependencies are pre-imported.                  the average over the given dataset gives an unbiased
We deliberately avoid model-specific prompt engineering                     expected value
or complex few-shot scaffolding, in order to evaluate the                                               "           #
                                                                                                                n−c
intrinsic formalization capability of the models. See Figures                                                    k
A.5, and A.6 for the specific prompts.                                                 pass@k := E        1− n                 (1)
                                                                                                     Problems
                                                                                                                    k


                                                                   2
                                Evaluation of LLMs for Mathematical Formalization in Lean

                              Table 2.1. List of every general and special purpose LLM evaluated

          Category                  Model Family           Specific Target / API Identifier
                                                           Gemini 3.1 Pro (gemini-3.1-pro-preview),
          Proprietary Frontier      Google Gemini          Gemini 3 Flash (gemini-3-flash-preview),
                                                           Gemini 3.1 Flash-Lite (gemini-3.1-flash-lite-preview)
                                                           GPT-5.4 (gpt-5.4), GPT-5.4 Mini (gpt-5.4-mini),
                                    Open AI GPT
                                                           GPT-5.4 Nano (gpt-5.4-nano)
                                    Anthropic Claude       Claude Opus 4.7 (global.anthropic.claude-opus-4-7)
          Open-Weight               Qwen                   Qwen 3.5 (Qwen3.5-397B-A17B)
          General-Purpose           Nemotron               Nemotron 3 Super (nemotron-3-super-120b-a12b)
                                    Open AI OSS            GPT-OSS-120B (gpt-oss-120b)
                                    Deepseek               DeepSeek 3.2 (DeepSeek-V3.2)
                                                           Goedel-Prover V2 (Goedel-Prover-V2-32B),
          Lean Specialized          Goedel
                                                           (Goedel-Prover-V2-8B)
                                    Mistral Labs           Leanstral (labs-leanstral-2603)


    where c is the number of correct samples out of the                    Table 2.2. LLMs pricing $USD / million tokens
    n = 32 generations and k is the number of solutions
    intended to be checked. See Figure A.3 for a flowchart           Model                     Input Cost      Output Cost
    visual.                                                          Opus 4.7                        5              25
                                                                     Nemotron                       0.3             0.9
  • Refine@k: To evaluate agentic formalization capabili-
                                                                     Deepseek 3.2                   0.3            0.45
    ties, we introduce an interactive refinement sequence
                                                                     Qwen 3.5                       0.6             3.6
    akin to. If an initial generation fails, the exact trace
                                                                     GPT 5.4                        2.5             15
    from the Lean verifier is extracted. The model is re-
                                                                     GPT 5.4-mini                  0.75            4.5
    prompted with its previous faulty proof alongside this
                                                                     GPT 5.4-nano                   0.2            1.25
    specific compiler feedback, iterating for up to k turns.
                                                                    Gemini 3.1 Pro                  2              12
                     
                       LLM (Prompt, FTS) i = 1                      Gemini 3 Flash                 0.5              3
                                                                     Gemini 3.1 Flash-Lite         0.25            1.5
                     
                     LLM (Prompt,
      Responsei :=                                                   GPT-OSS                       0.15             0.6
                       FTS, Responsei−1 ,
                                                                     Leanstral                       0               0
                     
                     
                        Feedbacki−1 )           1<i≤k
                     
                                                          (2)
    where FTS := Formal Theorem Statement. We define
    refine@k as the percentage of theorems that are correct         3. Results
    after k iterations, normalized to [0,1]. See Figure A.4         3.1. Accuracy
    for a flowchart visual.
                                                                    Considering Figure 3.1, which presents the accuracy vs. k
2.6. Model Costs                                                    curves for pass/refine@k on each dataset and for all models
                                                                    evaluated. We see that Gemini 3.1 Pro and Claude Opus
To determine model pricing, we use two different methods.
                                                                    4.7, both frontier models, were the two best-performing
For models that have a dedicated API endpoint, we calculate
                                                                    models for both pass@32 and refine@32 on both datasets.
the price based on the recorded input and output tokens
                                                                    Nemotron and Qwen 3.5 performed well on miniF2F, achiev-
consumed for each API call. For the models without a
                                                                    ing 3rd and 4th respectively, but struggled with miniCTX
dedicated API endpoint we ran the experiments using a
                                                                    (∼ 20% worse than the best model). On the other hand,
local HPC Cluster, which cost $0.90/ GPU hr. However,
                                                                    GPT 5.4 and GPT-OSS were roughly average on miniF2F,
to replicate the experiments the reader may have to pay
                                                                    but ranked right behind Gemini and Opus in miniCTX.
market rate e.g., (Vast.ai, 2026) which is approximately
$3.48/ GPU hr. All prices were obtained in May 2026, with           In addition, the specialized models (Leanstral, Goedel)
model providers and prices indicated in Table 2.2.                  performed reasonably well on miniF2F, with Goedel 32B

                                                                3
                                     Evaluation of LLMs for Mathematical Formalization in Lean




                                               (a) MiniCTX Accuracy vs. k (Pass and Refine)




                                                (b) MiniF2F Accuracy vs. k (Pass and Refine)
Figure 3.1. Each graph presents the pass@k/refine@k for 1 ≤ k ≤ 32 of all models on miniF2F and miniCTX. Each curve is increasing,
with the exception of the Goedel models for pass@k, which did not increase. This is likely due to homogeneity in responses In general,
accuracies on miniCTX were lower, with the exception of the frontier models (Gemini Pro etc.) and GPT-OSS. The curves for pass@k
are smoother since the pass@k function is given by a binomial expression (1), whereas refine@k has discrete interval values. For k near
32, Gemini 3.1 Pro was the top performing model on all but refine@k on miniCTX, where it is outperformed by Opus 4.7. On the other
hand, Goedel 8B had the lowest pass@k and refine@k on miniCTX, Gemini 3.1 Flash-Lite had the lowest pass@k on miniF2F, and GPT
5.4-mini had the lowest refine@k on miniF2F.


and Leanstral performing above average via refine@32, as                      This also helps explain why general-purpose models have a
shown in Figure A.1. However, these models underper-                          smaller difference in accuracy between the two datasets.
formed on miniCTX by a significant margin, trailing the
                                                                              When considering the most practical model, it is also impor-
next worst model by over 20% on pass@32, with the Goedel
                                                                              tant to compare performances at low k, since many users
models performing the worst1 , as indicated by Figure A.2.
                                                                              may not want to waste time and money regenerating a proof
This may be due to overfitting for datasets like miniF2F that
                                                                              dozens of times. From Figure 3.1, we can see that GPT-OSS
provide little to no context prior to the formal statement of
                                                                              performs almost as well as the top models on miniCTX, for
the theorem needing proof. In order to challenge this strat-
                                                                              k ∈ {1, 2}. However, this is not the case for miniF2F, in
egy, the miniCTX dataset first formalizes new definitions
                                                                              which GPT-OSS performed below the median for low k.
and lemmas before giving a formal statement that depends
on them (Hu et al., 2025). Thus, it requires a greater abil-
ity to generalize, as seen in models like Gemini and Opus.                    3.2. Error Analysis

   1                                                                          First, we discuss generation errors of different models. One
     It is worth noting that the pass@k lines for both Goedel mod-
els are horizontal, indicating a lack of diversity in responses, likely       thing to note is that Nemotron, Qwen 3.5, and Deepseek 3.2
caused by our temperature of t = 0.5 not being properly applied.              all have high proportions of generation failures, partially


                                                                          4
                                   Evaluation of LLMs for Mathematical Formalization in Lean




Figure 3.2. Error category distribution per model. See Appendix A.1 for a description of each error type and specific values. The top
4 categories (in order) are tactical errors (improper use of Lean tactics such as ‘rw’, ‘simp’, etc.), syntactical errors (incorrect Lean
syntax), unsolved goals (incomplete proofs), and generation failures (use of ‘sorry’/‘admit’, failed API calls). Cumulatively, these 4
categories make up 54.7% of errors.


due to the API used returning an empty string when going               statement in miniCTX, which lends itself to a higher
over the token limit. However, most theorems take fewer                chance of improper syntax use. Hallucination errors
than our 214 token limit to solve, which indicates that these          are also more prevalent in responses on miniCTX, likely
models are more prone to runaway responses. Opus also has              for similar reasons: models make up plausible sound-
a very high proportion of generation failures, mostly from             ing lemmas (such as ‘Padic.valuation nonneg’ and
the usage of ‘sorry’ and ‘admit’. This indicates that                  ‘Int.toNat add of nonneg’, both of which are not
Opus tends to admit defeat more readily than other models              real Mathlib Lemmas) based off of the context that miniCTX
on difficult proofs. Taking into account Opus’s overall high           provides.
performance and its distribution of other error categories,
it is also likely that Opus is very effective at mitigating            3.3. Cost Efficiency
strategical errors.
                                                                       When choosing a model, cost is often a major limiting fac-
Next, we analyze the prevalence of tactical errors through-            tor. As shown in Figures 3.3a and 3.3b, model cost per
out the models. GPT 5.4-nano has the smallest proportion               theorem is correlated with improvements to effectiveness on
of tactical errors, however, it also has the largest propor-           miniF2F, with R2 s of 0.453 and 0.528. For miniCTX, the
tion of unsolved goals, implying that it tends to end proofs           relation is much less strongly correlated, with R2 s of 0.108
prematurely rather than make tactical mistakes. GPT 5.4                and 0.225 (not shown). However, when we neglect the spe-
and Gemini 3 Flash also have a relatively large proportion             cialized models, which as discussed above did especially
of tactical errors while also having minimal generation er-            poorly on miniCTX, the R2 s increase to 0.604 and 0.55.
rors. This means that these models rarely use ‘sorry’,                 Together, these trends suggest the emergent phenomenon of
and prefer to make an attempt at solving the given problem             the formalization capability: larger, more expensive general-
no matter their confidence. Looking at Gemini 3 Flash in               purpose models exhibit good generalization to formal proof
particular, it has the largest proportion of ‘no goals’ errors,        generation, better than small specialized models.
in which it continues to write tactics even after all goals            With that in mind, to determine the most cost-efficient
have already been solved. This suggests that Gemini 3 Flash            model, we identified the degree of overperformance from
does not always know when it is correct.                               expected by calculating the residuals of each plot and then
Regarding syntax errors, one interesting result is the dis-            ordering them. Table A.6 presents these residuals. The best
parity of syntax errors between miniCTX and miniF2F.                   performer for miniF2F was Nemotron, which outperformed
Per A.4 and A.5, we can see that syntax errors make                    expected by 24% for pass@32 and 23% for refine@32. For
up 10.7% more of the errors on miniCTX as com-                         miniCTX however, Nemotron underperformed and GPT-
pared to miniF2F. This is likely because of the many                   OSS was the most effective, over-performing expected by
lemmas and definitions introduced before each problem                  12% for pass@32 and 18% for refine@32. In addition, both


                                                                   5
                                   Evaluation of LLMs for Mathematical Formalization in Lean




           (a) Accuracy vs. Cost for miniF2F pass@32                           (b) Accuracy vs. Cost for miniF2F refine@32




          (c) Accuracy vs. Cost for miniCTX pass@32                            (d) Accuracy vs. Cost for miniCTX refine@32
Figure 3.3. These plots show accuracy vs. average cost per attempt for miniF2F and miniCTX pass/refine@32. Accuracy scales linearly
with average cost, with an increase of over 3% per $0.01 increase in cost per attempt. Most models are clustered below $0.03 per attempt
excluding most frontier models. Interestingly, GPT 5.4, which despite its frontier status used relatively few tokens. Refine@k is also
consistently marginally more expensive than pass@k, likely due to the increased input size.


these models cost around $0.01 per attempt, making them                miniF2F and miniCTX, sorted from greatest to least by
ideal candidates for mathematicians on a budget.                       miniCTX ∆32 . On the miniF2F data subset, all but two of
                                                                       the models (Deepseek and GPT 5.4-nano) have a positive
3.4. Refine Effectiveness                                              ∆32 , with average ∆32 = +7.7%. However, on the miniCTX
                                                                       data subset, only 9 of the 14 models had a positive ∆32 , with
It is important to analyze the per-model difference between            the average being ∆32 = -1.4%. Despite this, the models
the pass@k and refine@k metrics. For this, we define the               performed better on average with the iterative refinement
difference metric                                                      method, with an overall average improvement of +3.14%.
                ∆k := refine@k − pass@k.                               On the miniCTX dataset, most of the models that performed
                                                                       better on refine@32 are frontier models (Gemini, GPT,
Hence, a positive ∆k means the model performed better                  Claude) that have very large context windows. We suspect
with the iterative refine pipeline compared to the expected            this to be the primary limitation of this strategy—smaller
value of generating k independent responses. On the other              models that lack the ability to store enough context begin
hand, a negative ∆k says the opposite.                                 to lose information on errors from previous attempts, espe-
Table 3.1 presents the ∆32 values of all models on both                cially due to the verbosity of some Lean 4 error messages,

                                                                   6
                                 Evaluation of LLMs for Mathematical Formalization in Lean

 Table 3.1. Model ∆32 on miniF2F and miniCTX benchmarks.             models via pass@k on various datasets with high k. For
                                                                     example, Goedel-Prover V2 has been tested on the Putnam-
          Model             miniF2F     miniCTX                      Bench up to pass@184 (Lin et al., 2026), and Kimina-Prover
          Opus 4.7               8.0         22.0                    has been tested on miniF2F up to pass@8192 (Wang et al.,
          Nemotron               6.0          8.0                    2025). While higher k can capture the models full poten-
          Goedel 32B            16.0          8.0                    tial for auto-formalization and increase accuracy for lower
          Goedel 8B              8.0          6.0                    k measurements, it risks obfuscating the actual capabili-
          GPT 5.4-mini           2.0          6.0                    ties of a model when in use. Importantly, lower k values
          GPT 5.4                8.0          2.0                    better reflect real-world usage, where repeatedly sampling
          Leanstral             28.0          2.0                    hundreds of outputs is often impractical, especially for high-
          Gemini Lite           12.0          0.0                    cost models. However, a larger amount of samples would
          GPT-OSS                0.0          0.0                    increase confidence for k = 32 and improve accuracy of
          Deepseek              −4.0         −8.0                    our measurements.
          Gemini Pro             6.0         −8.0
          GPT 5.4-nano          −8.0        −12.0                    4.2.2. DATA S UBSETS
          Qwen 3.5               6.0        −22.0
                                                                     Though we have taken care to make sure the subsets we
          Gemini Flash          20.0        −24.0
                                                                     used were as close to representative of the original datasets
          Average                 7.7         −1.4                   as possible, it is possible that there were some nuances, such
                                                                     as particularly difficult or easy problems that were over- or
                                                                     under-included.
and thus are less likely to remedy the error in their next
response. This issue would be further exacerbated by the             4.2.3. S TANDARDIZED P ROMPT
complexity of the problems in the miniCTX dataset, many
                                                                     The standardized prompt may misrepresent some models’
of which require longer formal problem statements that de-
                                                                     true accuracy. Indeed, prompt engineering has been shown
fine theorems and lemmas necessary to solve the problem.
                                                                     to vastly improve results in other benchmarks, and the ideal
This disparity in complexity between miniF2F and miniCTX
                                                                     prompt varies from model to model (He et al., 2024). For
likely explains why the iterative refinement strategy was less
                                                                     example, both Goedel-Prover V2 8B and 32B are designed
effective on the latter.
                                                                     on a specialized prompt, and achieved 84.6% and 88.1%
                                                                     on miniF2F via pass@32 respectively (Lin et al., 2026).
4. Conclusion                                                        However, using a standardized prompt normalizes the re-
                                                                     sults. Further, it better represents a model’s capabilities
4.1. Summary
                                                                     when integrated into an agentic workflow, where prompts
We evaluated a multitude of models on unbiased size n = 50           are nonstandard and can include large amounts of tooling
subsets of both the miniCTX and miniF2F datasets, where              specific to the agentic tool (Zhou et al., 2026).
we compared the overall effectiveness, cost-effectiveness
and iterative refinement capabilities of each model. Based           4.2.4. R EFINE @k IS NOT S TATISTICAL
on these evaluations, we have identified Gemini 3.1 Pro
                                                                     While pass@k provides an expected value for the accuracy
and Claude Opus 4.7 as the current best models for formal
                                                                     of each model when prompted k times, refine@k only pro-
proof generation in Lean 4. However, these models incurred
                                                                     vides a snapshot of what is possible with an iterative refine-
a significant cost, up to an average of $0.075 per attempt.
                                                                     ment strategy. However, when considering the miniF2F
In contrast, we have identified Nemotron and GPT-OSS
                                                                     dataset, given the consistent improvement most models
as budget-friendly alternatives that still provide significant
                                                                     showed over Pass@k, it is likely that an iterative refinement
theorem proving capabilities, while reducing costs by up to
                                                                     strategy does in general improve results over repeated single
96%. Across all models, iterative refinement consistently
                                                                     attempt generation. This is consistent with previous work
outperforms repeated independent attempts, indicating that
                                                                     evaluating LLMs’ reasoning ability with competitive pro-
feedback-driven reasoning loops are a key factor in improv-
                                                                     gramming contests via both pass@k and refine@k bench-
ing formal proof generation.
                                                                     marks (Xu et al., 2026). On the other hand, when treating
                                                                     the miniCTX dataset, refine@k underperformed pass@k on
4.2. Limitations                                                     GPT 5.4-nano, Gemini 3.1 Pro, and Qwen 3.5, see Figure
4.2.1. L IMITED S CALING                                             A.2. We were not able to re-perform the experiments for
                                                                     financial reasons and this observation reveals the need for a
Our evaluations are limited to pass@32 and refine@32                 statistical refine@k.
benchmarks. In previous works, authors have evaluated

                                                                 7
                                Evaluation of LLMs for Mathematical Formalization in Lean

4.3. Future Work                                                    He, J., Rungta, M., Koleczek, D., Sekhon, A., Wang, F. X.,
                                                                      and Hasan, S. Does prompt formatting have any impact
The natural extension of our work is evaluating more LLMs.
                                                                      on llm performance?, 2024. URL https://arxiv.
While we covered many well-known models, budgetary con-
                                                                      org/abs/2411.10541. https://arxiv.org/
straints limited our capabilities, and we were not able to
                                                                      abs/2411.10541.
test every model we initially considered. Additionally, as
newer models are released, capabilities will change. Hence,         Hu, J., Zhu, T., and Welleck, S. miniCTX: Neural the-
a website that compiles all the data and regularly updates            orem proving with (long-)contexts. In The Thirteenth
similar to https://llm-stats.com/ would be a wor-                    International Conference on Learning Representations,
thy endeavor. Furthermore, as models improve, our current             2025. URL https://openreview.net/forum?
datasets will become saturated, even with a lower k value.            id=KIgaAqEFHW.
Thus, extending this work to other datasets could yield new
insights on how well LLMs handle actual mathematical                Hubert, T. et al. Olympiad-level formal mathemat-
work. One candidate dataset for evaluation is RLMEval                 ical reasoning with reinforcement learning. Na-
(Poiroux et al., 2025), which focuses on formal research-             ture, 2025. URL https://www.nature.com/
level mathematical problems collected from a variety of               articles/s41586-025-09833-y.
mathematical topics. Another direction could be evaluating
                                                                    Lightman, H., Kosaraju, V., Burda, Y., Edwards, H., Baker,
refine@k in a statistical method. One method to accomplish
                                                                      B., Lee, T., Leike, J., Schulman, J., Sutskever, I., and
this could be to choose a lower k, such as k = 4 or k = 8,
                                                                      Cobbe, K. Let’s verify step by step. In The Twelfth
and evaluate that n times as in pass@k. This would provide
                                                                      International Conference on Learning Representations,
a statistical look at refine@k while keeping inference costs
                                                                      2024. URL https://openreview.net/forum?
manageable.
                                                                      id=v8L0pN6EOi.

Acknowledgments                                                     Lin, Y. et al. Goedel-prover-v2: Scaling formal theorem
                                                                      proving with scaffolded data synthesis and self-correction.
CPU and GPU computing, LLM inference and data storage                 In The Fourteenth International Conference on Learning
were in part done using AWS credits from the UW eScience              Representations, 2026. URL https://openreview.
School and UW IT. GPU computing was in part done on                   net/forum?id=j4C0nALrgK.
UWIT’s GPU cluster Tillicum. GPU computing and model
inference were in part done using TokenFactory.                     Liu, J. et al. Combibench: Benchmarking llm capability
                                                                      for combinatorial mathematics, 2025. URL https://
                                                                      arxiv.org/abs/2505.03171.
References
                                                                    Moura, L. d. and Ullrich, S. The lean 4 theorem prover
AI, M. Leanstral: Open-source foundation for trustworthy
                                                                     and programming language. In Automated Deduction
  vibe-coding, March 2026. URL https://mistral.
                                                                     CADE 28: 28th International Conference on Automated
  ai/news/leanstral. https://mistral.ai/
                                                                     Deduction, Virtual Event, July 1215, 2021, Proceed-
  news/leanstral.
                                                                     ings, pp. 625635, Berlin, Heidelberg, 2021. Springer-
Chen, M. et al. Evaluating large language models trained             Verlag. ISBN 978-3-030-79875-8. doi: 10.1007/
  on code. CoRR, abs/2107.03374, 2021. URL https:                    978-3-030-79876-5 37. URL https://doi.org/
  //arxiv.org/abs/2107.03374.                                        10.1007/978-3-030-79876-5_37.

                                                                    Poiroux, A., Bosselut, A., and Kunčak, V. RLMEval:
Google DeepMind. Advanced version of Gemini with                      Evaluating research-level neural theorem proving. In
  Deep Think officially achieves gold-medal stan-                     Christodoulopoulos, C., Chakraborty, T., Rose, C.,
  dard at the International Mathematical Olympiad.                    and Peng, V. (eds.), Findings of the Association
  https://deepmind.google/blog/advanced-version-of-                   for Computational Linguistics: EMNLP 2025, pp.
  gemini-with-deep-think-officially-achieves-gold-medal-              10946–10957, Suzhou, China, November 2025. Asso-
  standard-at-the-international-mathematical-olympiad/,               ciation for Computational Linguistics. ISBN 979-8-
  2025.                                                               89176-335-7. doi: 10.18653/v1/2025.findings-emnlp.
                                                                      581. URL https://aclanthology.org/2025.
Han, S., Hur, T., Hur, Y., Sangkyung Lee, K., Lee, M.,                findings-emnlp.581/.
  and Lim, H. Simplifying formal proof-generating models
  with chatgpt and basic searching techniques. In Intelligent       Polu, S., Han, J. M., Zheng, K., Baksys, M., Babuschkin, I.,
  Computing-Proceedings of the Computing Conference,                  and Sutskever, I. Formal mathematics statement curricu-
  pp. 205–222. Springer, 2025.                                        lum learning. In The Eleventh International Conference

                                                                8
                                  Evaluation of LLMs for Mathematical Formalization in Lean

  on Learning Representations, 2023. URL https://
  openreview.net/forum?id=-P7G-8dmSh4.
Vast.ai. Rent h200 gpus on vast.ai. https://vast.ai/
  pricing/gpu/H200, 2026. https://vast.ai/
  pricing/gpu/H200.
Wang, H. et al.   Kimina-prover preview: Towards
 large formal reasoning models with reinforcement
 learning, 2025. URL https://arxiv.org/abs/
 2504.11354. https://arxiv.org/abs/2504.
 11354.
Xu, S., Yiwen, H., Min, Y., Chen, Z., Zhao, X., and
 Wen, J.-R. ICPC-eval: Probing the frontiers of LLM
  reasoning with competitive programming contests. In
 The Thirty-ninth Annual Conference on Neural Informa-
  tion Processing Systems Datasets and Benchmarks Track,
  2026. URL https://openreview.net/forum?
  id=rRrswElWIW.

Zhang, Z., Xu, J., He, Z., Liang, T., Liu, Q., Li, Y., Song, L.,
  Liang, Z., Zhang, Z., Wang, R., Tu, Z., Mi, H., and Yu,
  D. Deeptheorem: Advancing LLM reasoning for theo-
  rem proving through natural language and reinforcement
  learning, 2026. URL https://openreview.net/
  forum?id=0OUkySEAf0.
Zheng, K., Han, J. M., and Polu, S. minif2f: a cross-system
  benchmark for formal olympiad-level mathematics. In
  International Conference on Learning Representations,
  2022. URL https://openreview.net/forum?
  id=9ZPegFuFTFv.

Zhou, H., Wan, X., Sun, R., Palangi, H., Iqbal, S.,
  Vuli, I., Korhonen, A., and Ark, S. . Multi-agent
  design: Optimizing agents with better prompts and
  topologies, 2026. URL https://arxiv.org/abs/
  2502.02533. https://arxiv.org/abs/2502.
  02533.
Zhou, Y. et al. Solving formal math problems by decom-
  position and iterative reflection, 2025. URL https:
  //arxiv.org/abs/2507.15225.               https://
  arxiv.org/abs/2507.15225.




                                                                   9
                                       Evaluation of LLMs for Mathematical Formalization in Lean

A. Additional Materials
A.1. Additional Information on Error Classifications

                                                Table A.1. Error categories and their descriptions.

            Category                           Description

            generation                         Model produced a non-runnable proof: used sorry/admit, returned
                                               an empty string, or the API call failed.
            timeout                            The Lean server exceeded its heartbeat limit during verification.
            syntax                             Output is not parseable Lean (unexpected tokens, import statements,
                                               unterminated blocks).
            unsolved goals                     Proof terminates with open goals remaining, including incomplete case
                                               splits.
            no goals                           Proof continues after all goals have been closed.
            tactic                             A specific tactic failed: rewrite/rw found no matching pattern,
                                               simp/simp all made no progress, introN/rcases/ext failed, or
                                               similar.
            arithmetic                         A decision procedure (omega, linarith, norm num, ring) could
                                               not close the goal.
            type mismatch                      Explicit type mismatch, bad anonymous constructor, or application type
                                               mismatch.
            elaboration                        Typeclass synthesis failure, and other errors that occur in the Lean 4
                                               elaboration phase
            hallucination                      Unknown identifier, constant, or tactic — the model referenced a name
                                               that does not exist in scope.
            other                              Uncategorized residual (5.0%).


                                Table A.2. Per-model error profile (fraction of that model’s failure entries).

               Model                    gen.     timeout   no goals   unsolved    halluc.   arith.   tactic    type   elab.   syntax   other

               Nemotron                0.354      0.032      0.084      0.072      0.091    0.025    0.124    0.081   0.046   0.045    0.047
               Qwen 3.5                0.287      0.025      0.078      0.058      0.041    0.026    0.089    0.057   0.029   0.289    0.024
               Opus 4.7                0.269      0.049      0.011      0.026      0.038    0.031    0.168    0.025   0.040   0.289    0.054
               Deepseek 3.2            0.213      0.106      0.099      0.163      0.069    0.024    0.097    0.070   0.056   0.061    0.041
               Goedel 32B              0.174      0.027      0.019      0.152      0.025    0.018    0.120    0.045   0.130   0.238    0.051
               Gemini 3.1 Flash-Lite   0.153      0.041      0.129      0.109      0.098    0.023    0.205    0.110   0.061   0.028    0.042
               Gemini 3.1 Pro          0.127      0.093      0.053      0.090      0.065    0.035    0.117    0.057   0.045   0.281    0.037
               GPT 5.4-nano            0.060      0.075      0.032      0.295      0.047    0.013    0.054    0.112   0.057   0.187    0.066
               Leanstral               0.089      0.047      0.084      0.144      0.132    0.068    0.175    0.054   0.061   0.117    0.029
               GPT-OSS                 0.014      0.005      0.052      0.195      0.151    0.022    0.098    0.278   0.082   0.023    0.080
               GPT 5.4                 0.007      0.061      0.025      0.162      0.087    0.101    0.220    0.166   0.068   0.046    0.057
               Gemini 3 Flash          0.018      0.040      0.191      0.080      0.087    0.023    0.164    0.095   0.060   0.210    0.032
               GPT 5.4-mini            0.046      0.030      0.032      0.148      0.090    0.098    0.205    0.141   0.040   0.066    0.103
               Goedel 8B               0.061      0.022      0.020      0.081      0.044    0.110    0.174    0.088   0.138   0.230    0.033




A.2. Additional Accuracy Information




                                                                             10
                                 Evaluation of LLMs for Mathematical Formalization in Lean

                                            Table A.3. Overall error category distribution.

                                        Category                    Count      % of failures

                                        tactic                         8,128            14.4
                                        syntax                         7,987            14.2
                                        unsolved goals                 7,519            13.3
                                        generation                     7,243            12.8
                                        type mismatch                  5,706            10.1
                                        hallucination                  4,366              7.7
                                        elaboration                    3,807              6.7
                                        no goals                       3,727              6.6
                                        arithmetic                     2,592              4.6
                                        timeout                        2,540              4.5
                                        other                          2,828              5.0

Table A.4. miniCTX error distribution (total fails: 32,559).               Table A.5. miniF2F error distribution (total fails: 23,884).

         Category                  Count         %                                 Category                   Count        %

         generation                 3,325     10.2                                 generation                  3,918     16.4
         timeout                    2,021       6.2                                timeout                       519      2.2
         no goals                   1,424       4.4                                no goals                    2,303      9.6
         unsolved goals             3,207       9.8                                unsolved goals              4,312     18.1
         hallucination              3,017       9.3                                hallucination               1,349      5.6
         arithmetic                   190       0.6                                arithmetic                  2,402     10.1
         tactic                     5,381     16.5                                 tactic                      2,747     11.5
         type mismatch              2,974       9.1                                type mismatch               2,732     11.4
         elaboration                3,131       9.6                                elaboration                   676      2.8
         syntax                     6,074     18.7                                 syntax                      1,913      8.0
         other                      1,815       5.6                                other                       1,013      4.2




      Figure A.1. Model pass@32 and refine@32 on miniF2F               Figure A.2. Model pass@32 and refine@32 on miniCTX


                                                                  11
                               Evaluation of LLMs for Mathematical Formalization in Lean

A.3. Additional Cost Information
                                                Table A.6. Model Cost Residuals

          Model                      F2F Pass@32        F2F Refine@32        CTX Pass@32        CTX Refine@32
          Nemotron                          0.24               0.23               -0.08                0.05
          Deepseek 3.2                      0.18               0.08               -0.04                -0.07
          Qwen 3.5                          0.12               0.09               -0.03                -0.21
          GPT 5.4-nano                      0.08              -0.06                0.07                0.01
          Opus 4.7                          0.07               0.06               -0.07                0.11
          Gemini 3.1 Pro                    0.02              -0.03                0.07                -0.04
          GPT-OSS                           -0.01             -0.07                0.13                0.18
          Leanstral                         -0.01              0.21                N/A                  N/A
          GPT 5.4                           -0.04             -0.03               -0.01                0.06
          Gemini 3 Flash                    -0.04              0.08                0.06                -0.15
          GPT mini                          -0.15             -0.19               -0.10                0.02
          Goedel v2 8b                      -0.15             -0.14                N/A                  N/A
          Gemini 3.1 Flash-Lite             -0.16             -0.10               -0.01                0.05
          Goedel v2 32b                     -0.17             -0.10                N/A                  N/A

A.4. Flowcharts for Pass@k and Refine@k




         Figure A.3. Flowchart for pass@k
                                                                          Figure A.4. Flowchart for refine@k




                                                              12
               Evaluation of LLMs for Mathematical Formalization in Lean

A.5. Prompts




                             Figure A.5. Prompt for pass@k




                             Figure A.6. Prompt for refine@k




                                           13
                           Evaluation of LLMs for Mathematical Formalization in Lean

B. List of Problems used in the Datasets
B.1. MiniF2F
                                    Table B.1. MiniF2F problems used in subset

               amc12b 2020 p21                            amc12b 2021 p3
               amc12a 2021 p9                             amc12 2000 p6
               amc12a 2019 p12                            amc12a 2009 p25
               amc12a 2021 p25                            amc12b 2002 p3
               amc12a 2003 p1                             mathd algebra 419
               mathd algebra 33                           mathd algebra 362
               mathd algebra 181                          mathd algebra 144
               mathd algebra 24                           mathd algebra 332
               mathd algebra 192                          mathd algebra 412
               mathd algebra 270                          mathd algebra 288
               mathd algebra 323                          algebra manipexpr apbeq2cceqiacpbceqm2
               mathd algebra 756                          mathd algebra 156
               algebra amgm sumasqdivbsqgeqsumbdiva       algebra manipexpr 2erprsqpesqeqnrpnesq
               mathd algebra 432                          aime 1997 p11
               aime 1983 p1                               aime 1988 p8
               mathd numbertheory 109                     mathd numbertheory 84
               mathd numbertheory 301                     mathd numbertheory 34
               mathd numbertheory 690                     mathd numbertheory 185
               mathd numbertheory 236                     mathd numbertheory 342
               mathd numbertheory 521                     mathd numbertheory 33
               mathd numbertheory 765                     mathd numbertheory 345
               mathd numbertheory 237                     mathd numbertheory 149
               induction sum 1oktkp1                      induction ineq nsqlefactn
               imo 1982 p1                                imo 1965 p2
               imo 2006 p3                                imo 1964 p2




                                                       14
                     Evaluation of LLMs for Mathematical Formalization in Lean

B.2. MiniCTX
                              Table B.2. MinCTX problems used in subset

               PowerSeries.invOneSubPow inv zero eq one
               PadicInt.valuation mul
               List.reduceOption eq nil iff
               Condensed.hasExactLimitsOfShape
               ZLattice.volume image eq volume div covolume
               SetLike.covBy iff
               Polynomial.hilbertPoly mul one sub pow add
               AddValuation.ofValuation toValuation
               isBigO deriv ofReal cpow const atTop
               PowerSeries.invOneSubPow add
               HomologicalComplex.homologyπ extendHomologyIso hom
               IsCoatom.lt top
               Complex.deriv cpow const
               ZLattice.covolume.tendsto card le div”
               ComplexShape.Embedding.op boundaryLE iff
               HomologicalComplex.extendHomologyIso hom homologyι
               HomologicalComplex.extendHomologyIso hom naturality
               PadicInt.valuation pow
               AddValuation.ofValuation apply
               Submodule.span range update add smul
               ZLattice.covolume.tendsto card div pow”
               Valuation.ofAddValuation symm eq
               HomologicalComplex.pOpcycles extendOpcyclesIso inv
               CanonicallyOrderedAdd.pow pos
               PadicInt.valuation coe nonneg
               HomologicalComplex.homologyπ extendHomologyIso inv
               isTheta deriv ofReal cpow const atTop
               IsAtom.bot lt
               PadicInt.norm eq zpow neg valuation
               ComplexShape.Embedding.op boundaryGE iff
               Polynomial.coeff mul invOneSubPow eq hilbertPoly eval
               List.reduceOption eq concat iff
               Set.pairwiseDisjoint pair insert
               Polynomial.natDegree hilbertPoly of ne zero
               Complex.deriv ofReal cpow const
               Valuation.ofAddValuation apply
               Valuation.ofAddValuation toAddValuation
               Matrix.det updateCol add self
               DifferentiableAt.ofReal cpow const
               Valuation.val mrange zero
               Polynomial.hilbertPoly X pow succ
               StrictConvexSpace.of strictConvex unitClosedBall
               Subsemiring.coe toNonUnitalSubsemiring
               Matrix.det updateCol sum
               IsApproximateSubgroup.pow inter pow covBySMul sq inter sq
               CharacterModule.dual injective iff surjective
               Polynomial.hilbertPoly smul
               ZLattice.volume image eq volume div covolume’
               hasDerivAt ofReal cpow const
               HomologicalComplex.extend.leftHomologyData.lift d comp eq zero iff’

                                                 15
