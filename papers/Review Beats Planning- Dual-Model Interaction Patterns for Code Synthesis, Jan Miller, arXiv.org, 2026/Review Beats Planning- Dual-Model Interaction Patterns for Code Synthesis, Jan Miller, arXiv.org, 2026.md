                                              Review Beats Planning: Dual-Model Interaction Patterns
                                                               for Code Synthesis
                                                                                   Jan Miller
                                                                                   OPSWAT
                                                                               Hamburg, Germany
                                                                              admin@jan-miller.de
arXiv:2603.03406v1 [cs.SE] 3 Mar 2026




                                                                                     March 2026


                                                                                       Abstract
                                                 How should two language models interact to produce better code than either can alone? The
                                             conventional approach—a reasoning model plans, a code specialist implements—seems natural
                                             but fails: on HumanEval+, plan-then-code degrades performance by 2.4 percentage points
                                             versus the code specialist alone. We show that reversing the interaction changes everything.
                                             When the code specialist generates freely and the reasoning model reviews instead of plans,
                                             the same two models on the same hardware achieve 90.2% pass@1—exceeding GPT-4o (87.2%)
                                             and O1 Preview (89.0%)—on ~$2/hr of commodity GPU. Cross-benchmark validation across
                                             542 problems (HumanEval+ and MBPP+) reveals a moderating variable: review effectiveness
                                             scales with specification richness, yielding 4× more improvement on richly-specified problems
                                             (+9.8pp) than on lean ones (+2.3pp), while remaining net-positive in both cases. The practical
                                             implication is twofold: compose models by their cognitive strengths (reviewers review, coders
                                             code), and invest in specification quality to amplify the returns.


                                        1    Introduction
                                        Large language models have achieved impressive results on code generation benchmarks, with fron-
                                        tier models exceeding 87% pass@1 on HumanEval+ [Liu et al., 2023]. However, these results typ-
                                        ically rely on single large models (70B+ parameters) or proprietary APIs. For on-premise deploy-
                                        ment, practitioners face a fundamental constraint: limited GPU memory forces the use of smaller,
                                        quantized models that individually fall short of state-of-the-art performance.
                                            A natural response is to compose multiple specialized models into a pipeline. The conventional
                                        wisdom—inspired by software engineering practices and chain-of-thought reasoning [Wei et al.,
                                        2022]—is to have a stronger reasoning model plan the solution, then have a code specialist implement
                                        that plan. We call this the “plan-then-code” pattern.
                                            We test this assumption empirically and find it wrong. On HumanEval+, plan-then-code per-
                                        forms worse than the raw code specialist, with the planner’s guidance actively introducing errors
                                        in 15 of 164 problems. The key failure mode: the reasoning model suggests algorithms or identifies
                                        edge cases at a high level, but these suggestions sometimes conflict with the specific implementation
                                        constraints visible only in the code.
                                            This finding motivates a reversal: instead of planning before code generation, we apply the
                                        reasoning model after —as a code reviewer. The “review-then-fix” pattern leverages the same models
                                        and the same compute budget, but changes the interaction direction. The result: a +10.4 percentage


                                                                                           1
point improvement over baseline, achieving 90.2% HumanEval+ with two 4-bit quantized models
on commodity GPUs.

Contributions.

1. Empirical evidence that plan-then-code hurts. We show that guidance from a reasoning
   model can degrade a code specialist’s performance, with a detailed taxonomy of failure modes
   (§4.4).

2. Review-then-fix as an alternative. We propose and evaluate a dual-model pattern where
   the reasoning model reviews (not plans) and the code specialist fixes based on specific feedback
   (§3.2).

3. Adversarial dual-generation. We explore a pattern where both models generate solutions
   independently, which are then cross-validated and synthesized (§3.3).

4. Specification richness as a moderator. Cross-benchmark validation on MBPP+ (378 prob-
   lems) shows review effectiveness scales with specification detail: +9.8pp on rich specs vs +2.3pp
   on lean specs (§4.2).

5. Practical on-premise setup. All results use 4-bit AWQ quantized models on two A10G
   GPUs (~$2/hr total), demonstrating that dual-model composition is a viable path to frontier-
   competitive performance.


2     Experimental Setup
2.1   Models


                        Table 1: Model configurations used in all experiments.
 Role                     Model                          Params      Quant.        GPU       VRAM
 Code specialist          Qwen2.5-Coder-14B-Instruct       14B      AWQ 4-bit    A10G #1      ~8 GB
 Reasoning generalist     Qwen3-32B                        32B      AWQ 4-bit    A10G #2      ~18 GB

   Both models are served via vLLM [Kwon et al., 2023] using the OpenAI Chat Completions API
format. We use greedy decoding (temperature = 0) for deterministic, reproducible results.

Qwen3 thinking mode. Qwen3-32B supports an explicit reasoning mode that emits internal
reasoning tokens before the response. For raw benchmarking, we disable thinking to avoid output
pollution. For pipeline configurations where the model performs analysis or review, we enable
thinking to leverage the model’s reasoning capability.

2.2   Benchmark
We use two benchmarks from the EvalPlus framework [Liu et al., 2023]:

• HumanEval+: 164 Python problems with rich specifications—function signatures, detailed doc-
  strings, type annotations, and doctest examples. Augmented with 80× more tests than the orig-
  inal HumanEval [Chen et al., 2021].

                                                  2
• MBPP+: 378 Python problems with lean specifications—typically a one-line description and a
  single assertion. Augmented test suite from EvalPlus.

This pair provides a natural experiment in specification richness: same evaluation framework, same
models, but dramatically different specification detail. We report pass@1 on the augmented suites
(“HumanEval+” and “MBPP+”) with greedy decoding.

2.3   Code Extraction and Validation
Model outputs are post-processed to extract function bodies from potentially verbose responses,
handling markdown fence stripping, repeated signature removal, indentation normalization, and
trailing text truncation. Each extraction step includes compile-time verification.
    Pipeline variants with retry include an eval-retry loop: generated code is compiled, executed,
and tested against docstring examples visible in the prompt. On failure, the error message is fed
back for correction (up to 3 retries). Importantly, this uses only tests visible in the prompt—not
the hidden EvalPlus augmented tests—preventing any form of test leakage.


3     Pipeline Architectures
Figure 1 contrasts the two primary interaction patterns.

         (a) Plan-then-code         75.6%      worse than baseline

                                                     plan
                          Planner                                                  Coder
                            32B                                                     14B

                                       abstract guidance can mislead coder

         (b) Review-then-fix        87.8%       beats GPT-4o

                                     code                                    fix
                  Coder                              Planner                               Coder
                   14B                                 32B                                  14B

                               specific bug reports coder fixes with targeted feedback


Figure 1: Two dual-model interaction patterns. (a) Plan-then-code: the reasoning model plans
upfront, but its abstract guidance can mislead the coder (75.6%). (b) Review-then-fix: the coder
generates freely, the reasoning model reviews for bugs, and the coder fixes—achieving 87.8% without
retry.




                                                         3
3.1    Plan-Then-Code
The planner receives the function signature and docstring, produces a natural-language analysis
(algorithm, edge cases, complexity), and the coder implements with this analysis as context. This
is the conventional “chain-of-thought delegation” pattern.

3.2    Review-Then-Fix
The key insight: instead of telling the code specialist how to solve the problem (which can mislead),
let it solve the problem naturally, then use the reasoning model to find bugs. The code specialist
then receives specific, actionable feedback (“line X does Y, but should do Z”) rather than abstract
algorithmic guidance.
    The pipeline proceeds as:
    1. Coder generates a solution (identical prompt to raw baseline)

    2. Planner reviews the solution against the specification

    3. If bugs found, coder receives the review and fixes (single pass)
    This core pipeline uses exactly 2–3 LLM calls per problem: one generation, one review, and op-
tionally one fix. No test execution, no retry loop—a fair comparison against single-shot leaderboard
entries.
    We additionally evaluate a variant review-then-fix + retry that adds an eval-retry loop: after
the review-fix pass, the solution is compiled and tested against docstring examples visible in the
prompt. On failure, the error is fed back for correction (up to 3 retries). This variant is reported
separately to isolate the contribution of review from the contribution of test feedback.
    Additional context provided to the coder includes an import inventory (explicitly stating allowed
imports).

3.3    Adversarial Dual-Generation
This architecture eliminates “guidance contamination” entirely:
    1. Both models generate solutions independently (in parallel)

    2. Cross-validate both against docstring tests

    3. If exactly one passes, use it; if both pass, adversarial review selects the better one

    4. If neither passes, the planner reviews both; the coder synthesizes a third solution informed by
       both failures and their reviews


4     Results
4.1    Main Results
4.2    Cross-Benchmark Validation: Specification Richness
To understand when review helps, we replicated our key comparison on MBPP+ (378 problems)—a
benchmark with substantially leaner specifications than HumanEval+. Where HumanEval+ pro-
vides function signatures, detailed docstrings, type annotations, and doctest examples, MBPP+
typically offers a one-line natural language description and a single assertion.

                                                     4
   Table 2: Pass@1 results on HumanEval and HumanEval+ (greedy decoding, 164 problems).
          Configuration                 HumanEval        HumanEval+        ∆ vs baseline
          raw-coder (14B AWQ)              81.1%             78.0%              —
          raw-planner (32B AWQ)            89.0%             84.1%            +6.1pp
          Plan-then-code                   80.5%             75.6%            −2.4pp
          Review-then-fix (no retry)       89.6%             87.8%            +9.8pp
          Review-then-fix (+retry)         93.3%             90.2%            +12.2pp
          Adversarial debate               91.5%             86.6%            +8.6pp


Table 3: Review effectiveness scales with specification richness. Comparison of review-then-fix (no
retry) across benchmarks.
                                 HumanEval+ (rich specs)          MBPP+ (lean specs)
         Configuration           Pass@1              ∆            Pass@1           ∆
         raw-coder (baseline)     78.0%            —               67.5%          —
         Review-then-fix          87.8%          +9.8pp            69.8%        +2.3pp
         Enriched review          88.4%          +10.4pp           69.8%        +2.3pp


    The same review pipeline that yields +9.8pp on HumanEval+ yields only +2.3pp on MBPP+—
a 4× reduction in review impact. We attribute this to the reviewer’s ability to assess correctness:
with rich specifications (examples, types, edge cases), the reviewer has clear criteria against which
to judge the code. With lean specifications, the reviewer must infer intent from a brief description,
increasing the chance of both missed bugs and false positives.
    Crucially, review is still net-positive on both benchmarks. We tested two mitigations for the
lean-spec gap:

• Spec-gated review: Selectively skip review for lean specifications. Performed worse than un-
  conditional review (84.1% HumanEval+, 69.0% MBPP+)—the modest false-positive rate on lean
  specs is offset by the genuine bugs review catches.

• Spec-enriched review: Use the reasoning model to generate additional examples, types, and
  edge cases before review. Marginal gain on HumanEval+ (+0.6pp) and no gain on MBPP+
  (69.8% vs 69.8%), at the cost of an additional LLM call per problem.

Neither mitigation closes the gap (Figure 4). The practical implication: unconditional review is the
right default, specification richness is a fundamental moderator that cannot be cheaply synthesized,
and investment in upstream specification quality is the most effective lever for improving review
outcomes.

4.3   Leaderboard Context
4.4   Failure Mode Analysis
Of 164 problems, plan-then-code produced 15 regressions where the pipeline broke tasks the raw
coder solved, against only 14 improvements. We categorize the regressions (Figure 5):



                                                 5
                                              Pipeline Configurations on HumanEval+
            Coder alone                            78.0%
             (14B AWQ)

         Plan-then-code                   75.6%

          Planner alone                                                84.1%
             (32B AWQ)

      Adversarial debate                                                       86.6%

         Review-then-fix                                                              87.8%
              (no retry)
         Review-then-fix                                                                      90.2%
               (+retry)
                                                                                        GPT-4oO1 Preview
                           70                 75                80               85                  90
                                                        HumanEval+ pass@1 (%)

Figure 2: Pipeline configurations on HumanEval+. Plan-then-code (red) performs worse than the
raw coder baseline. Review-then-fix (green) exceeds both GPT-4o and O1 Preview. Dashed line:
coder baseline; dotted lines: proprietary model reference points.

      Table 4: Comparison with published HumanEval+ results from the EvalPlus leaderboard.
        Model                                           HumanEval+                      Notes
        O1 Preview                                          89.0%          Proprietary reasoning model
        Our pipeline (14B+32B AWQ)                          90.2%               2× A10G, ~$2/hr
        Qwen2.5-Coder-32B (FP16)                            87.2%          Single model, full precision
        GPT-4o                                              87.2%                  Proprietary
        DeepSeek-V3                                         86.6%                  Proprietary
                                Full review-then-fix run on all 164 problems (not merged).


• Missing imports (7): Planner suggests using Counter, math.factorial, etc. Coder follows
  the suggestion but omits the import.
• Variable name “correction” (1): Problem uses intentional misspelling (delimeter). Planner
  “fixes” it to delimiter, causing signature mismatch.
• Algorithm mismatch (5): Planner’s high-level approach is correct but coder introduces subtle
  bugs during translation.
• Over-engineering (2): Planner identifies edge cases that don’t exist, adding unnecessary com-
  plexity.


4.5     Why Review Beats Planning
We hypothesize three mechanisms:

                                                            6
                 95
                      Review Effectiveness Scales with Specification Richness
                          HumanEval+ (rich specs)
                          MBPP+ (lean specs)
                 90                            +9.8pp             +10.4pp
                                               87.8%               88.4%
                 85
    pass@1 (%)




                 80                                                                      4x gap
                                                                                         persists
                 75     78.0%

                 70                                     +2.3pp              +2.3pp
                                                        69.8%               69.8%
                 65             67.5%

                 60
                         Coder alone          Review-then-fix      Enriched review

Figure 3: Review effectiveness scales with specification richness. The 4× gap between rich specs
(HumanEval+, +9.8pp) and lean specs (MBPP+, +2.3pp) persists even with spec enrichment.
Green: HumanEval+ (rich); gray: MBPP+ (lean).


    1. Specificity of feedback. Planning produces abstract suggestions; review produces specific
       bug reports. Specific feedback is easier to act on.

    2. Preserved code autonomy. The coder first solves in its natural style, then receives
       corrections—its internal consistency is preserved.

    3. Asymmetric strengths. The 32B generalist excels at finding bugs (reasoning); the 14B
       specialist excels at generating code. Review-then-fix aligns each model with its strength.


5        Related Work
Self-repair. Chen et al. [2023] and Olausson et al. [2024] study single-model code repair using
execution feedback. Our work differs by using a separate reasoning model for review, introducing
genuine model diversity.

Multi-agent code generation. ChatDev [Qian et al., 2024] and MetaGPT [Hong et al., 2024] use
multi-agent systems for software development, but typically role-play with the same base model. We
use genuinely different models (specialist vs generalist) and show that interaction direction matters
more than role assignment.

LLM composition. Speculative decoding, routing, and mixture-of-experts combine models for
efficiency. Our work composes models for quality—achieving results neither model reaches alone.


                                                        7
                              Mitigation Attempts: Neither Gating nor Enriching Beats Unconditional Review

                 92
                             HumanEval+ (rich specs)                                           73
                                                                                                               MBPP+ (lean specs)
                 90                                                                            72
                         87.8%                        88.4%
                 88                                                                            71
                 86                                                                                    69.8%                        69.8%
    pass@1 (%)




                                                                                  pass@1 (%)
                                                                                               70
                                        84.1%                                                                         69.0%
                 84                                                                            69
                 82                                                                            68                                           baseline (67.5%)
                 80
                                                               baseline (78.0%)                67
                 78
                                                                                               66
                 76
                                                                                               65
                      Unconditional   Spec-gated   Spec-enriched                                    Unconditional   Spec-gated   Spec-enriched
                         review         review        review                                           review         review        review


Figure 4: Mitigation attempts for the spec-richness gap. Left: HumanEval+ (rich specs). Right:
MBPP+ (lean specs). Neither spec-gated review (purple) nor spec-enriched review (blue) outper-
forms unconditional review (green). Dashed line: coder-alone baseline.


6          Discussion and Limitations
Benchmark scope. HumanEval+ tests single-function problems, not real-world multi-file devel-
opment.
    Eval-retry uses visible tests. The docstring test validation is a lightweight correctness signal,
not a substitute for comprehensive testing.
    Cost trade-off. Review-then-fix requires 2–7 LLM calls per problem vs 1 for single-model
generation.
    Model specificity. Results are specific to Qwen2.5-Coder-14B + Qwen3-32B; other combina-
tions may differ.
    Specification enrichment does not close the gap. Since review effectiveness scales with
specification richness, a natural mitigation is using the reasoning model to enrich lean specifications
before review—generating examples, types, and edge cases from brief descriptions. We tested this
(“enriched review”: coder generates, planner enriches spec, planner reviews against enriched spec,
coder fixes). On HumanEval+ (already rich specs), enrichment yields a marginal +0.6pp (88.4% vs
87.8% unconditional review). On MBPP+ (lean specs), enrichment shows no improvement (69.8%
vs 69.8%). The auto-generated enrichment does not substitute for genuine specification detail,
suggesting that the specification richness gap is a fundamental property of the problem, not an
artifact of missing context that can be synthesized.


7          Conclusion
We demonstrate that dual-model composition can achieve frontier-competitive code synthesis (90.2%
HumanEval+) using two 4-bit quantized open models on commodity GPUs. The critical finding
is that interaction pattern selection—specifically, using the reasoning model for code review rather
than upfront planning—is the primary driver of quality improvement. Plan-then-code degrades
performance; review-then-fix dramatically improves it. Cross-benchmark validation on MBPP+
reveals a second finding: review effectiveness scales with specification richness, yielding 4× more


                                                                             8
                             Why Planning Hurts: 15 Regressions in Plan-then-code
                             (tasks the coder solved alone but failed with guidance)
                                                              Name
                                                              "correction"
                                                                             Over-
                                                          1                  engineering
                                                                  2
                                Import
                          contamination     7

                                                                  5
                                                                             Algorithm
                                                                             mismatch




Figure 5: Breakdown of 15 regressions in plan-then-code: tasks the coder solved alone but failed
with planner guidance. Import contamination dominates—the planner suggests libraries the coder
then uses without importing.


improvement on richly-specified problems (+9.8pp on HumanEval+) than on lean ones (+2.3pp on
MBPP+), while remaining net-positive in both cases. This suggests that in dual-model systems,
models should be composed according to their cognitive strengths rather than following the human
metaphor of plan-then-implement, and that investment in specification quality amplifies the returns
of code review.


References
Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Pondé de Oliveira Pinto, Jared
 Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, et al. Evaluating large
 language models trained on code. arXiv preprint arXiv:2107.03374, 2021.

Xinyun Chen, Maxwell Lin, Nathanael Schärli, and Denny Zhou. Teaching large language models
  to self-debug. arXiv preprint arXiv:2304.05128, 2023.

Sirui Hong, Mingchen Zhuge, Jonathan Chen, Xiawu Zheng, Yuheng Cheng, Ceyao Zhang, Jinlin
  Wang, Zili Wang, Steven Ka Shing Yau, Zijuan Lin, et al. MetaGPT: Meta programming for a
  multi-agent collaborative framework. In ICLR, 2024.

Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Ying, Ying Lian, Kangmin Cho, Hao Zhuang,
 Joseph E Gonzalez, Ion Stoica, and Eric P Xing. Efficient memory management for large language
 model serving with PagedAttention. In SOSP, 2023.

Jiawei Liu, Chunqiu Steven Xia, Yuyao Wang, and Lingming Zhang. Is your code generated by
  ChatGPT really correct? rigorous evaluation of large language models for code generation. In
  NeurIPS, 2023.

Theo X Olausson, Jeevana Priya Inala, Chenglong Wang, Jianfeng Gao, and Armando Solar-
  Lezama. Is self-repair a silver bullet for code generation? ICLR, 2024.



                                                      9
Chen Qian, Xin Cong, Cheng Yang, Weize Chen, Yusheng Su, Juyuan Xu, Zhiyuan Liu, and
  Maosong Sun. Communicative agents for software development. In ACL, 2024.

Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia, Ed Chi, Quoc
  Le, and Denny Zhou. Chain-of-thought prompting elicits reasoning in large language models. In
  NeurIPS, 2022.




                                              10
