                                          KA-TP-23-2026                                                                       September 2026
                                          P3H-26-076




                                                             LLM-Based Form Code Generation with
                                                               Verification-Driven Fine-Tuning
arXiv:2609.23367v1 [hep-ph] 20 Sep 2026




                                                                               Bakar Chargeishvili 1


                                                        Karlsruhe Institute of Technology (KIT), Institut für Theoretische Physik,
                                                                Wolfgang-Gaede-Straße 1, 76131 Karlsruhe, Germany




                                                                                      Abstract
                                              Form is a domain-specific symbolic manipulation language widely used in particle physics for
                                          processing the very large algebraic expressions arising from multi-loop Feynman diagram calcu-
                                          lations. Despite its central role in precision theoretical physics, no artificial-intelligence tooling
                                          exists, to our knowledge, for assisting physicists in writing Form code. We show that contem-
                                          porary large language models (LLMs), including frontier models with hundreds of billions of pa-
                                          rameters, achieve a zero-percent execution pass rate on our instruction-following and tutorial-style
                                          Form tasks without documentation in a single attempt, establishing Form as a genuine zero-shot
                                          language for LLMs at the time of writing. We then present a verification-driven data generation
                                          pipeline that uses the Form binary itself as an execution oracle to produce and validate a corpus of
                                          4,633 training examples spanning deterministic computations, open-ended programs, tutorial code,
                                          and knowledge question–answer pairs. Fine-tuning a compact open-weights model (Qwen3-8B)
                                          with quantized low-rank adaptation (QLoRA) yields a specialist that, evaluated on four comple-
                                          mentary benchmarks (840 tasks, single attempt each), decisively outperforms frontier models with
                                          up to 756B parameters in execution rate and in strict, Form-verified output matching on the larger
                                          benchmarks, and remains statistically indistinguishable from them on the smaller, harder ones.
                                          General reasoning and coding capabilities are preserved within 2.6 percentage points.
                                          Keywords: symbolic algebra, Form, code generation, fine-tuning, QLoRA, domain-specific lan-
                                          guages, particle physics, execution-based verification




                                             1
                                                 bakar.chargeishvili@kit.edu
1    Introduction
Form is a symbolic manipulation system designed for the efficient processing of very large alge-
braic expressions—routinely handling formulae with millions or even billions of terms that arise in
perturbative quantum field theory calculations [1, 2, 3]. Originally developed by Jos Vermaseren
in 1984 as a successor to Schoonschip [4], Form has become an indispensable tool in particle
physics [5], underpinning calculations of multi-loop Feynman amplitudes [6, 7], anomalous di-
mensions, multiple zeta values [8], and many other results in precision QCD and electroweak
physics. Its unique architecture—which stores intermediate expressions on disk rather than in
memory—enables it to process expressions orders of magnitude larger than general-purpose com-
puter algebra systems such as Mathematica or Maple [9, 10].
    Despite its importance, Form remains challenging to learn and use effectively. Its syntax differs
fundamentally from mainstream programming languages: pattern matching uses wildcard symbols
with set-theoretic conditions, the .sort statement controls expression buffering, and tensor oper-
ations require explicit index declarations. The learning curve is long, and there is no ecosystem
of AI-assisted coding tools comparable to what exists for Python, JavaScript, or even specialised
languages like SQL.
    The emergence of large language models (LLMs) trained on code—exemplified by Codex [11]
and its successors—has transformed software development for mainstream languages. However,
Form is a zero-resource language in the LLM training-data sense: it appears negligibly or not at all
in the internet-scale corpora on which modern LLMs are trained. Throughout, zero-resource refers
to this training-data property; we reserve zero-shot for the absence of in-context documentation
or examples (Section 4.2). This raises a fundamental question: can a small language model be
specialised to generate correct Form code, and how does it compare to frontier-scale models?
    In this work, we address this question through three contributions:

1. A verification-driven data generation pipeline that exploits the Form binary as an execution
   oracle. The pipeline generates candidate programs from natural-language instructions using
   a frontier LLM, then verifies each program through a four-stage process: deterministic-word
   checking, syntax validation via the Form binary, non-trivial output confirmation, and semantic
   consistency auditing by an independent LLM. This yields 4,633 verified training examples with
   zero train/test overlap.
2. A parameter-efficient fine-tuning recipe based on QLoRA [12, 13] applied to the 8-billion-
   parameter Qwen3-8B model [14]. The resulting model achieves 97.7% exact-output-match on
   a 664-task deterministic benchmark and 83.0% execution rate on a 100-task open-ended bench-
   mark, outperforming every frontier model studied—including GLM-5.2 and GLM-5.3 (756B
   parameters [15, 16]) and DeepSeek-V4 Flash (304B parameters [17])—with non-overlapping
   95% confidence intervals on both benchmarks. The advantage persists under a strict, Form-
   verified output-match metric (18.0% vs. 5.6% for the best frontier model on 89 of the 100 tasks
   whose output is uniquely determined).
3. A comprehensive evaluation framework comprising four benchmarks, seven baseline models,
   execution-based metrics, anchored LLM judging with a Form-specific factsheet, 95% bootstrap
   confidence intervals, and a strict Form-verified output-match metric that separates genuinely
   solved problems from merely runnable programs. We also demonstrate that general reasoning


                                                 1
    capability is preserved (−2.6 pp on MMLU [18], −1.5 pp on GSM8K [19]), confirming that
    QLoRA fine-tuning does not cause catastrophic forgetting.

     The remainder of this paper is organised as follows. In Section 2 we review the Form symbolic
manipulation system, language models for code generation, and parameter-efficient fine-tuning.
Section 3 describes our verification-driven data generation pipeline and the fine-tuning configu-
ration. In Section 4 we introduce the benchmark suite, baseline models, and evaluation protocol.
Section 5 presents our findings, including the zero-shot result, main benchmark results, ablation
studies, and capability preservation. We discuss why a small fine-tuned model outperforms fron-
tier models, the limitations of the present work, and future directions in Section 6, and conclude in
Section 7.


2     Background
2.1    The Form Symbolic Manipulation System
Form is a domain-specific language (DSL) for symbolic algebra, designed specifically for the kind
of expression manipulation that arises in perturbative quantum field theory. Unlike general-purpose
computer algebra systems, Form is optimised for throughput rather than interactivity: it processes
expressions in a batch-sequential pipeline, writing intermediate results to disk and sorting them
between processing stages via the .sort command [2].
    A typical Form program declares indices, vectors, and tensors; defines a local expression;
applies trace and contraction operations; and prints the result. Figure 1 shows a simple example
that computes the Dirac trace of two gamma matrices contracted with external vectors.

Indices alpha, beta;
Vectors k, l;
Local E = g_(1, alpha, beta) * k(alpha) * l(beta);
Trace4, 1;
contract;
Print;
.end


Figure 1: A simple Form program: declare indices and vectors, define an expression with Dirac
gamma matrices g( 1, α, β), take the trace (Trace4, 1), contract Lorentz indices, and print. The
output is E = 4 k · l, reflecting the trace identity Tr[γα γβ ] = 4 gαβ .

    Key features that make Form challenging for LLMs include:

• Wildcard pattern matching: Wildcard variables must be declared as Symbols and use the ?
  syntax (e.g., id f(x?,y?) = g(x,y)), with optional set conditions (e.g., {>2,<5}).
• Tensor operations: The metric tensor d_, the Levi-Civita symbol e_, and Dirac gamma matri-
  ces g_ require explicit index declarations and dimension settings. The trace operation Trace4
  acts on gamma-matrix chains.


                                                 2
• Preprocessor loops: The #do/#enddo and #if constructs enable metaprogramming, but loop
  variables in conditions require backtick syntax (e.g., #if ‘i’ > 2).
• Expression lifecycle: Within a single module, Local F = F + ... redefines rather than ac-
  cumulates; iterative accumulation inside #do loops requires an intervening .sort between loop
  iterations.
• No built-in calculus: Form has no diff_(), Int(), or det() functions. Differentiation, inte-
  gration, and determinant computation must be implemented manually via pattern matching.
    Form has been used in landmark physics calculations including the three-loop QCD anoma-
lous dimensions [6], four-loop massless propagator integrals via the Forcer package [7], and the
systematic computation of multiple zeta values [8]. The 2022 Quanta Magazine article “Crucial
Computer Program for Particle Physics at Risk of Obsolescence” [9] highlighted both Form’s irre-
placeability and its vulnerability as a single-maintainer project; a recent CERN Courier interview
with Form’s past, present and future developers discusses the same sustainability concerns [10].
Our work aims to lower the barrier to Form proficiency by providing an AI coding assistant, thereby
broadening the user base and partially mitigating the knowledge-transfer problem.

2.2    Language Models for Code Generation
The application of LLMs to code generation has been extensively studied for mainstream lan-
guages. The HumanEval benchmark [11] introduced execution-based evaluation with the pass@k
metric, now standard across the field. For low-resource and domain-specific languages, the chal-
lenge is acute: Cassano et al. [20] proposed MultiPL-T, a pipeline for translating high-resource
training data to low-resource languages, demonstrating that fine-tuning on synthetic data can sig-
nificantly improve performance on languages with minimal public code repositories. Mora et
al. [21] introduced “synthetic programming elicitation” for very low-resource languages, using
formal grammar constraints to generate and validate training data.
    Our approach differs from these works in two key respects. First, we benefit from having a
deterministic execution oracle (the Form binary) that provides ground-truth verification of both
syntax and output—a stronger signal than the unit-test-based verification used in MultiPL-T [20]
or the grammar-based validation in [21]. Second, Form is not merely a low-resource language but
a zero-shot language: as we demonstrate in Section 5, all tested LLMs (up to 756B parameters)
produce zero syntactically-valid Form programs without documentation context on Instruct-100,
and the same holds on Tutorial-44 for the base model and the frontier models evaluated there
without documentation (Section 5.1 details the no-documentation coverage).
    Our generation-and-verification pipeline is conceptually related to the Ralph Wiggum Loop
(RWL) [22], an agentic design pattern in which an LLM repeatedly generates candidate solutions,
an external verifier evaluates them, and the LLM reflects on the feedback to produce improved
candidates. In the RWL framework—named after the Simpsons character for its persistent trial-
and-error behaviour—the agent alternates between generation and external validation until the
solution passes all checks or a maximum iteration count is reached. Our pipeline instantiates this
pattern with the Form binary as the external verifier: candidate programs are generated by a frontier
LLM, validated through execution, and the error output is fed back for repair attempts. The key
difference is that our pipeline collects only the successfully verified outputs as training data, rather
than using the iterative refinement to improve the generator itself.

                                                   3
                             Verification-Driven Data Generation Pipeline

          Feature            LLM Generation
         Taxonomy          (DeepSeek-V4 Flash
       (16 features)          304B, T=0.8)             repair loop




                           1. Deterministic-word                     2. FORM Binary
                                   Check                              Syntax Check




                                                                      3. Non-trivial    4. GLM-5.2 Consistency
                                                                      Output Check           Audit (T=0.1)




       Open-ended                     Tutorial                            Knowledge        Verified Deterministic
       Code (1,113)                    (43)                               Q&A (1,075)              (2,465)



                                       Final Training Set: 4,633 examples



Figure 2: Verification-driven data generation pipeline. Candidate programs are generated from
natural-language instructions by a frontier LLM (DeepSeek-V4 Flash, temperature 0.8), then pass
through a four-stage verification process before inclusion in the training set.

2.3   Parameter-Efficient Fine-Tuning
Full supervised fine-tuning (SFT) of an 8B-parameter model must keep the full parameter set, gra-
dients, and optimizer states in memory—on the order of 70–80 GB with AdamW—which is feasi-
ble on modern hardware but risks catastrophic forgetting of pre-trained capabilities. QLoRA [12]
addresses both concerns by quantising the base model to 4-bit precision and training only low-rank
adapter matrices (LoRA [13]) on top of the frozen weights. This reduces the number of trainable
parameters by ∼99% while preserving performance comparable to full fine-tuning.


3     Method
3.1   Verification-Driven Data Generation
Our data generation pipeline is built on the principle that every training example must be verified
by executing the generated Form program through the actual Form binary. This ensures that the
model learns only from syntactically valid, semantically consistent examples. The pipeline consists
of four stages, illustrated in Figure 2.




                                                       4
Feature Taxonomy
We define a taxonomy of 16 Form features, each with three complexity levels (basic, intermedi-
ate, advanced), yielding 48 feature-complexity cells. The features include: symbol and expression
arithmetic, index and tensor operations, gamma-matrix traces, Levi-Civita contractions, wildcard
pattern matching, preprocessor loops (#do/#if), expression manipulation (repeat/while), the
count function, the discard/keep mechanism, nested function substitution, and polynomial op-
erations.

Generation
For each feature–complexity cell, we generate candidate programs by prompting DeepSeek-V4
Flash (304B parameters [17]) at temperature 0.8 with instructions in plain English. The instructions
specify the exact symbols, expressions, and operations to use, ensuring deterministic outputs. This
produces ∼10,000 candidate programs across all cells.

Four-Stage Verification
Each candidate program passes through the following verification chain:

1. Deterministic-word check: The instruction is scanned for non-deterministic words (“think”,
   “appropriate”, “suitable”) that could lead to variable outputs. Candidates containing such words
   are rejected.
2. Form binary syntax validation: The program is executed through the Form binary (FORM 5.0,
   April 2025). Programs that fail to compile or run are rejected. Importantly, Form writes error
   messages to standard output (not standard error) with exit code 1, which we capture for the
   repair loop.
3. Non-trivial output check: Programs that produce empty or trivially simple output (e.g., 0 or
   1) are rejected to ensure training signal richness.
4. LLM consistency audit: An independent LLM (GLM-5.2, 756B parameters [15], tempera-
   ture 0.1; low temperature since auditing is deterministic classification, not creative generation—
   cf. the LLM judge of Section 4.3) evaluates whether the generated program is semantically con-
   sistent with the instruction. This catches cases where the program runs but does not implement
   the requested computation. The auditor is given a Form factsheet—a curated list of real Form
   built-in functions and common pitfalls—to prevent hallucinated capabilities from inflating audit
   scores.

    After verification, duplicate programs are removed via exact-match and normalised-text dedu-
plication. The final deterministic training set contains 2,465 verified examples.

Multi-Source Data Composition
Beyond deterministic tasks, we supplement the training set with three additional data categories:




                                                 5
• Open-ended code generation (1,050 training examples): Instructions that specify a goal but
  leave implementation details open. These are generated from seed programs in the Form refer-
  ence manual and the “Form for Pedestrians” tutorial [23], then GLM-5.2-audited for instruction–
  code consistency (63 of the 1,113 generated examples are held out for validation).
• Tutorial programs (43 examples): Verbatim programs extracted from the “Form for Pedestri-
  ans” book [23], paired with natural-language instructions. These provide canonical idioms that
  reflect how Form is actually used in practice. The 43 training programs are exact-match-disjoint
  from the 44 Tutorial-44 test tasks.
• Knowledge question–answer pairs (1,075 examples): Conceptual questions about Form syn-
  tax and semantics (e.g., “What does the .sort statement do?”), generated by an LLM and
  audited by an independent LLM judge.
• Documentation-in-context slice (355 rows): A variant subset of the training data—counted
  within the categories above, not in addition to them—where the first 6,000 characters of a Form
  syntax guide are prepended to the instruction (applied to 10% of the code rows), teaching the
  model to use documentation at inference time.

    The final training set therefore comprises 2,465 deterministic + 1,050 open-ended + 43 tuto-
rial + 1,075 question–answer examples = 4,633 examples with a 314-example validation split.
Test sets are generated before training data to prevent data leakage; we verify zero exact-match
contamination between train and test instructions.

3.2   Fine-Tuning Configuration
We fine-tune Qwen3-8B [14], a dense model with 8 billion parameters, using QLoRA with the
configuration in Table 1.
   We train two model variants to study the effect of data composition:

   • FORM-8B (det-only), hereafter v3b: 2,465 deterministic examples only. This model serves
     as a negative control: it demonstrates what happens when the training data is verified but
     compositionally narrow (deterministic tasks with fully specified instructions and known out-
     puts).

   • FORM-8B (full mix), hereafter v3c: 4,633 examples including deterministic tasks, open-
     ended code generation, tutorial programs, knowledge Q&A pairs, and the documentation-
     in-context slice. This is our primary model. The label “v3c” reflects the third iteration of our
     data pipeline, incorporating audited multi-source data.

The rationale for training two variants is to isolate the effect of data composition from data veri-
fication: both v3b and v3c use verified data, but v3b contains only deterministic tasks while v3c
includes diverse open-ended, tutorial, and knowledge components. As we show in Section 5.4, this
difference in composition is the single most important factor for open-ended capability.
    Training loss curves are shown in Figure 3. Both variants converge smoothly. The det-only
model achieves lower validation loss (0.289) due to the narrower output distribution, while the
full-mix model stabilises at ∼0.59, reflecting the broader task variety.


                                                 6
                         Table 1: QLoRA fine-tuning hyperparameters.
                   Parameter              Value
                   Base model             Qwen3-8B (4-bit NF4 quantisation)
                   LoRA rank (r)          16
                   LoRA alpha (α)         32
                   LoRA dropout           0.05
                   Target modules         All linear layers
                   Learning rate          2 × 10−4
                   LR schedule            Cosine, warmup 5%
                   Epochs                 5
                   Effective batch size   32 (8 per device × 4 grad. accum.)
                   Max sequence length    2,048 tokens
                   Optimizer              AdamW (paged)
                   Framework              Unsloth [24] + TRL [25]
                   Training time          ∼35 minutes (1× A100-40GB)


    We disable Qwen3’s hybrid thinking mode during both training and inference, such that the
model directly emits Form code without producing an intermediate reasoning trace. This is a delib-
erate design choice: the training data contains only code (no chain-of-thought), and we prioritise
fast, deterministic code generation over explainability. The model has nevertheless internalised
Form syntax conventions—for example, it consistently uses Trace4 for Dirac traces, respects the
redefinition semantics of Local, and applies .sort before cross-expression references— suggest-
ing that these patterns are learned as tacit knowledge rather than explicit reasoning steps.


4     Evaluation
4.1   Benchmark Suite
We evaluate on four benchmarks, designed to cover different aspects of Form code generation:

1. B1: 664-Deterministic (664 tasks). Fully-specified computations with known expected out-
   puts. Metric: exact output match after running the generated program through the Form binary.
   This is the primary benchmark; its large size (664) yields tight confidence intervals.
2. B2: Instruct-100 (100 tasks). Open-ended instructions that specify a computation goal without
   prescribing the exact implementation. Metric: syntax pass (the generated program compiles and
   runs without error in the Form binary), plus a strict Form-verified output-match rate on the 89


                                                 7
                                      (a) Training Loss                                                                          (b) Validation Loss
                3.0                                                                                    0.60
                                                                                                       0.55
                2.5
                                                                                                       0.50




                                                                                     Validation Loss
Training Loss



                2.0
                                                                                                       0.45
                1.5                                                                                    0.40
                1.0                                                                                    0.35
                0.5                                                                                    0.30
                0.0                                                                                    0.25
                      0   100   200     300    400       500      600       700                               0    100       200        300    400      500   600   700
                                        Training Step                                                                                   Training Step

                                                     FORM-8B (full mix, 4,633 ex.)                      FORM-8B (det-only, 2,465 ex.)


Figure 3: Training (left) and validation (right) loss curves for the two model variants: v3b (det-
only, 2,465 examples) and v3c (full mix, 4,633 examples). The v3c model converges to a higher
validation loss due to task diversity but achieves substantially better performance on open-ended
benchmarks (see Section 5).

                output-determined tasks (eleven references print no result expression; Section 5.3); the latter is
                a conservative lower bound because many instructions underspecify the target computation.
3. B3: Tutorial-44 (44 tasks). Programs extracted from the “Form for Pedestrians” tutorial [23],
   with instructions re-written in plain English. This benchmark is completely independent of the
   training pipeline and tests generalisation to canonical Form idioms. Metric: syntax pass, plus
   the same strict Form-verified output-match rate on the 41 adjudicable tasks (three references
   print no result expression).
4. B4: Open-32 (32 tasks). Complex, multi-step Form tasks (e.g., “Compute the SU(3) Casimir
   operator and verify its eigenvalue”). Metric: PASS/PARTIAL/FAIL verdict from an anchored
   LLM judge (GLM-5.2, temperature 0.1) that scores each task on 2–6 verifiable requirements,
   with a Form-specific factsheet in the system prompt to prevent hallucinated capabilities. The
   judge ceiling is verified at 100% (32/32 reference solutions judged PASS). In addition, the 22
   output-determined tasks are graded by strict Form-verified output matching (Section 5.3).

    All benchmarks use a zero-shot, single-attempt protocol: the model receives the instruction
(with no few-shot examples) and produces exactly one generation, which is then evaluated. This is
the strictest fair-evaluation protocol. The single-attempt design is a deliberate choice of eval target:
real coding practice is of course iterative, but agentic loops measure tool orchestration as much as
language competence, are strongly sensitive to system prompts and tooling, and are run-to-run
stochastic. A single attempt at temperature 0 measures the one competence every such loop still
requires—first-shot generation from a problem statement alone—in a way that is deterministic and
exactly reproducible. We demonstrate the specialist inside a realistic agentic workflow separately
(Section 5.6); a fair cross-model agentic benchmark is beyond the scope of this work.



                                                                                     8
Table 2: Baseline models. “Docs” indicates that the first 6,000 characters of a Form syntax guide
are prepended to the instruction. Without documentation, all evaluated frontier models score 0%
on Instruct-100, and the base model, DeepSeek-V4 Flash, GPT-OSS-120B and Gemma 4 likewise
score 0% on Tutorial-44 (Open-32, whose rubric judge credits partial solutions, is the one excep-
tion; see Section 5.1). GLM-5.3 shares the GLM-5.2 base model (756B total, 40B active); its gains
over GLM-5.2 are post-training only [16].
           Model                       Params    Active     Type               Context
           Qwen3-8B (base) [14]             8B        8B    Dense              Zero-shot
           FORM-8B (ours)                   8B        8B    Dense + QLoRA      Zero-shot
           Qwen3.8-27B [26]               27B        27B    Dense              +Docs
           Gemma 4 [27]                   33B        33B    Dense              +Docs
           GPT-OSS-120B [28]             117B        5.1B   MoE                +Docs
           DeepSeek-V4 Flash [17]        304B        13B    MoE                +Docs
           GLM-5.2 [15]                  756B        40B    MoE                +Docs
           GLM-5.3 [16]                  756B        40B    MoE                +Docs


4.2   Baseline Models
We compare against seven baseline models, representing a range of scales and architectures (Ta-
ble 2). “Docs” indicates that the first 6,000 characters of a Form syntax guide are prepended to the
instruction. Without documentation, every frontier model we evaluated produces zero valid pro-
grams on Instruct-100, and on Tutorial-44 the base model, DeepSeek-V4 Flash, GPT-OSS-120B
and Gemma 4 likewise produce zero (Section 5.1 gives the Open-32 exception).
    All frontier models are evaluated with documentation (the first 6,000 characters of a curated
Form syntax guide prepended to the instruction), because without it they score 0%—a finding we
report in Section 5. This provides frontier models with a significant advantage: our fine-tuned
model is evaluated zero-shot (no documentation), while frontier models receive documentation
that covers most of the syntax needed for the benchmarks.

4.3   Metrics and Statistical Analysis
For the deterministic benchmark (B1), we use exact output match: the generated program is exe-
cuted through the Form binary, and its stdout is compared against the expected output.
    For syntax-pass benchmarks (B2, B3), we check whether the generated program compiles and
runs without error in the Form binary.
    For the open-ended benchmark (B4), we use an anchored LLM judge (GLM-5.2, tempera-
ture 0.1) that scores each task on 2–6 verifiable criteria (e.g., “correct Levi-Civita sign”, “proper
Trace4 usage”). The judge is sampled at a deliberately low temperature rather than the vendor
default (≈0.6, tuned for conversational diversity): rubric scoring is a deterministic classification
task, where sampling noise only adds verdict variance. The only other parameters overridden are
a generation-length cap and disabling the model’s thinking mode; all remaining sampling parame-


                                                 9
ters use the server defaults. The judge’s accuracy does not rely on creative diversity—its reference
ceiling is 32/32 (all reference solutions judged PASS), and its verdicts are largely confirmed by the
Form-verified ground truth on the output-determined tasks (11 of 11 rubric passes for our model;
Section 5.3). The score is the fraction of criteria met (0–1), with the verdict derived as follows:

• PASS ⇔ score =1.0,
• PARTIAL ⇔ 0 < score < 1,
• FAIL ⇔ score =0 or no valid run.

The judge’s system prompt includes a Form factsheet listing real built-in functions and com-
mon pitfalls (e.g., Form has no diff_() or det() function; e_ contraction yields +24 in
FORM’s convention), preventing the judge from crediting hallucinated capabilities. The ex-
act factsheet text used for the published rubric verdicts is archived in the benchmark release
(judge_factsheet_v1.txt); the accumulation pitfall it encodes is discussed, in corrected form,
in Section 2.
     We report 95% bootstrap confidence intervals (10,000 resamples) for all benchmarks. Signif-
icance between models is assessed by checking for non-overlapping confidence intervals—a con-
servative criterion. For zero-count entries the bootstrap percentile interval is degenerate at zero;
we substitute the one-sided 95% Clopper–Pearson upper bound. As a complementary and more
powerful criterion we additionally compare models pairwise with the exact version of McNemar’s
test [29]. Because all models attempt the same tasks, the comparison reduces to the discordant
pairs—tasks solved by one model but not the other—whose split is tested against a fair-coin null
hypothesis with an exact two-sided binomial test. Pairing controls for task difficulty, which CI
overlap does not; its cost is that discordant pairs alone carry the signal, so tiny benchmarks yield
little power. We use it to check which of the differences suggested by Table 3 are statistically real.
     In addition to these execution-based metrics, we report a strict output-match rate for B2–B4:
the generated program is re-executed and its result expressions must reproduce the reference out-
put, with equality verified by Form itself (Section 5.3 gives the full procedure). This separates
programs that run from programs that solve the stated problem, and is the correctness metric em-
phasised in Table 3.


5     Results
5.1    Form is a True Zero-Shot Language
Our first finding is that Form is a zero-shot language for all the LLMs evaluated without documen-
tation: every model—from the 8B base model to the 756B GLM-5.2—produces zero syntactically-
valid Form programs without documentation on Instruct-100, and likewise on Tutorial-44 for
every model evaluated there (base, DeepSeek-V4 Flash, GPT-OSS-120B and Gemma 4). The
rubric-judged Open-32 benchmark is the one exception: without documentation, the largest fron-
tier models still complete a non-trivial fraction of its tasks (GLM-5.3 46.9%, GLM-5.2 40.6%,
DeepSeek-V4 Flash 37.5%; GPT-OSS-120B 12.5% and Gemma 4 6.2% remain near zero). Strict
Form-verified adjudication (Section 5.3) confirms that this competence is genuine rather than an
artefact of the rubric judge: without documentation, GLM-5.3, GLM-5.2 and DeepSeek-V4 Flash


                                                 10
                                                                       Strict FORM-verified correctness with 95% bootstrap confidence intervals
                                                                                                                                                            FORM-8B          DeepSeek-V4        Gemma 4
                                                                                                                                                            (ours)           Flash (304B)       (33B)
                                                                                                                                                            GLM-5.3          GPT-OSS            Qwen3.8



                                         98%
                               100%                                                                                                                         GLM-5.2          (117B)             (27B)
                                                                                                                                                            (756B)
Solved (strict output match)



                               80%

                                                     76%
                                               68%



                                                           62%




                                                                                                                                                                      59%
                               60%




                                                                                                                                                                                  55%
                                                                                                                                                                50%



                                                                                                                                                                            50%
                                                                       48%
                                                                 46%
                               40%




                                                                                                                              22%
                                                                                                                        20%




                                                                                                                                                                                        18%
                                                                                  18%
                               20%




                                                                                                                  15%




                                                                                                                                    15%




                                                                                                                                                                                              14%
                                                                                                                                                12%
                                                                                                                                          10%



                                                                                                                                                      10%
                                                                                        6%

                                                                                             6%
                                0%
                                                       664-Det                               Instruct-100                      Tutorial-44                                    Open-32
                                                       (n=664)                               strict (n=89)                    strict (n=41)                                 strict (n=22)


 Figure 4: Strict Form-verified correctness rates (Table 3, “Strict” columns; B1 is output match by
 construction) with 95% bootstrap confidence intervals. Our fine-tuned 8B model (blue) dominates
 on B1 and on the output-determined B2 tasks; on B3 and B4 the small adjudicable samples (41,
 22) produce wide CIs with overlap.

 genuinely solve 7, 8 and 9 of the 22 output-determined Open-32 tasks, respectively. The contrast
 with the Instruct-100 and Tutorial-44 benchmarks is explained by task shape: Open-32 problems
 are fully self-contained and closer to generic symbolic programming, whereas B2/B3 hinge on
 Form-specific idioms. Taken together, the near-zero no-docs performance indicates that Form
 appears negligibly in the training corpora of contemporary LLMs, placing it in the category of
 zero-resource languages as defined by Cassano et al. [20]. All frontier-model results reported sub-
 sequently are with documentation context, providing them with a substantial advantage over our
 zero-shot fine-tuned model.

 5.2                                  Main Results
 Table 3 presents the results across all four benchmarks. For B2–B4 each benchmark occupies
 two columns: the execution rate (syntax pass; rubric-judged for B4’s free-choice tasks) and the
 strict Form-verified correctness rate described in Section 5.3, which is the metric we emphasise.
 Figure 4 visualises the strict rates with confidence intervals.
     For zero-count entries the bootstrap percentile interval is degenerate at zero, so we substitute
 the one-sided 95% Clopper–Pearson upper bound (3.3%, 7.1% and 12.7% for the denominators
 89, 41 and 22).
     The key findings are:

 1. On the 664-Deterministic benchmark, FORM-8B achieves 97.7% [96.5, 98.8], outperforming
    GLM-5.2 (756B, 75.5% [72.3, 78.6]) by 22.2 pp, GLM-5.3 (67.8% [64.3, 71.4]) by 29.9 pp
    and DeepSeek-V4 Flash (304B, 62.3% [58.7, 66.1]) by 35.4 pp. GPT-OSS-120B (45.6% [41.9,
    49.4]) and Gemma 4 (47.6% [43.8, 51.4]) score even lower, while the Qwen3-8B base model
    scores 0.0%—it cannot generate a single valid Form program without fine-tuning or documen-
    tation. Qwen3.8-27B is instructive: it produces syntactically valid programs for 18.8% of tasks

                                                                                                             11
Table 3: Main results across the four benchmarks, reported as execution rate (“Exec.”: syntax
pass for B2/B3, rubric score for B4) and Form-verified strict output-match rate (“Strict”). B1 is
strict output match by construction (n=664). The B2 strict rate is computed on the 89 output-
determined tasks and is a conservative lower bound (Section 5.3); the B4 strict rate on the 22
output-determined tasks (for GPT-OSS-120B and Gemma 4 it is based on the no-docs runs); the
B3 strict rate on the 41 adjudicable tasks (three references print no result expression and cannot
be verified by output matching). Frontier models are evaluated with documentation; our model is
zero-shot. Bold indicates the best score per column. 95% bootstrap CIs for the correctness metrics
(B1 and all Strict columns). All entries are single-attempt generations at temperature 0.
Model                                B1          B2: Instruct-100            B3: Tutorial-44         B4: Open-32
                                  (n=664)        Exec.          Strict      Exec.      Strict      Rubric      Strict
                                                (n=100)        (n=89)       (n=44)    (n=41)       (n=32)     (n=22)
This work (zero-shot, no docs)
FORM-8B                             97.7         83.0           18.0         43.2       14.6        56.2       50.0
                                 [96.5, 98.8]                [10.1, 25.8]            [4.9, 26.8]            [27.3, 68.2]
Frontier baselines (with documentation)
GLM-5.3 [16]                        67.8         65.0            5.6         54.5       19.5        65.6       59.1
                                 [64.3, 71.4]                [1.1, 11.2]             [7.3, 31.7]            [36.4, 77.3]
GLM-5.2 (756B) [15]                 75.5         55.0            5.6         31.8       22.0        31.2       50.0
                                 [72.3, 78.6]                [1.1, 11.2]             [9.8, 34.1]            [27.3, 72.7]
DeepSeek-V4 Flash (304B) [17]       62.3         48.0            3.4         25.0       14.6        53.1       54.5
                                 [58.7, 66.1]                 [0.0, 7.9]             [4.9, 26.8]            [31.8, 72.7]
GPT-OSS-120B (117B) [28]            45.6         39.0            3.4         20.5       9.8         12.5       18.2
                                 [41.9, 49.4]                 [0.0, 7.9]             [2.4, 19.5]            [4.5, 36.4]
Gemma 4 (33B) [27]                  47.6         11.0            0.0         11.4       12.2        15.6        4.5
                                 [43.8, 51.4]                 [0.0, 3.3]             [2.4, 22.0]            [0.0, 13.6]
Qwen3.8-27B [26]                     0.6          8.0            0.0         11.4       9.8         9.4        13.6
                                  [0.2, 1.2]                  [0.0, 3.3]             [2.4, 19.5]            [0.0, 27.3]
Qwen3-8B base [14]                   0.0          0.0            0.0         0.0        0.0         6.2         0.0
                                  [0.0, 0.5]                  [0.0, 3.3]             [0.0, 7.1]             [0.0, 12.7]




                                                        12
   yet matches the expected output on only 0.6%—the same runs-are-not-solutions gap that Sec-
   tion 5.3 quantifies on the tutorial benchmark. The confidence intervals between FORM-8B and
   all frontier models do not overlap, confirming statistical significance.
2. On the Instruct-100 benchmark, FORM-8B leads on both metrics: 83.0% [75.0, 90.0] exe-
   cution rate versus 65.0% [56.0, 74.0] for the strongest frontier model (GLM-5.3), with non-
   overlapping CIs, and 18.0% [10.1, 25.8] versus 5.6% [1.1, 11.2] on the strict Form-verified
   output-match rate. The strict rate is a conservative lower bound—a manual audit found that
   many Instruct-100 instructions underspecify the target computation, so a correct-in-spirit pro-
   gram can still fail the check (Section 5.3)—but the same grading is applied to all models, and
   the near-disjoint intervals (overlap of 1.1 pp) make the ordering robust. Part of this advantage
   may reflect our model’s familiarity with the reference-generation conventions (Section 5.3).
3. On the Open-32 benchmark, GLM-5.3 leads on the strict metric with 59.1% [36.4, 77.3] of the
   22 output-determined tasks versus FORM-8B’s 50.0% [27.3, 68.2] and DeepSeek-V4 Flash’s
   54.5% [31.8, 72.7]—together with Tutorial-44, the only benchmarks where a frontier model
   outperforms our model on the strict metric, although the CIs overlap heavily on this small
   sample. Section 5.3 shows that this lead is genuine rather than a rubric artefact: GLM-5.3
   converts 13 of its 14 rubric passes on the output-determined tasks into Form-verified solutions,
   while our model converts 11 of 11. GLM-5.2 (50.0%), GPT-OSS-120B (18.2%) and Gemma
   4 (4.5%) score substantially lower. Our v3cn variant (Section 5.4) ties GLM-5.3 at 59.1%, and
   v3c with documentation reaches 63.6%.
4. On the Tutorial-44 benchmark, the strict metric reshuffles the ranking: GLM-5.3’s apparent
   dominance under syntax pass (54.5% vs. our 43.2%) largely evaporates—it converts only 33%
   of its passed tasks into genuine solutions, reflecting fluency in writing runnable Form rather
   than superior problem solving. The strict rates are statistically indistinguishable across all
   strong models (GLM-5.2 22.0% [9.8, 34.1], GLM-5.3 19.5% [7.3, 31.7], FORM-8B 14.6%
   [4.9, 26.8], DeepSeek-V4 Flash 14.6%), and no model solves even a quarter of the 41 adjudi-
   cable tasks: B3-style tutorial transfer remains hard for everyone.

5.3    Runs Are Not Solutions: Strict Output Match
The execution metric used for B2 and B3 counts a program as passed when it merely compiles
and runs without error—it does not check what the program computes. (B4’s rubric judge grades
stated criteria, but it is an LLM assessment rather than an execution check.) The “Strict” columns
of Table 3 grade correctness instead: we re-execute each generated program, extract its result ex-
pressions, and compare them against the reference solution. Equality is verified by Form itself
through a difference-to-zero check, Local Z = (ref) - (gen);, which is invariant to term or-
dering, factor ordering, and algebraic rearrangement (e.g. b*b vs. bˆ2, or sin(a)*(1-cos(a)ˆ2)
vs. sin(a)-sin(a)*cos(a)ˆ2)). Since instructions do not pin declaration types, the declaration
sets of the reference and the generated program are tried in turn. A task is solved only if every ref-
erence expression is reproduced (extra expressions in the generated output are tolerated, so printing
auxiliary results is harmless). Tasks whose reference prints no named result expression cannot be
adjudicated this way and are excluded (three on B3, eleven on B2); references reproduce their own
stored outputs on all remaining tasks, validating the metric.


                                                 13
Table 4: Execution success vs. genuine solutions on Tutorial-44. “Exec.” is the syntax-pass rate of
Table 3 (n=44); “Solved” is the strict Form-verified output-match rate on the 41 adjudicable tasks
(three references print no result expression). The final column is the fraction of a model’s passed
tasks that are genuine solutions.
                 Model                         Exec. passed    Solved     Solved/Exec.
                 GLM-5.2                       14 (31.8%)     9 (22.0%)      64%
                 GLM-5.3                       24 (54.5%)     8 (19.5%)      33%
                 FORM-8B                       19 (43.2%)     6 (14.6%)      32%
                 DeepSeek-V4 Flash             11 (25.0%)     6 (14.6%)      55%
                 Gemma 4                        5 (11.4%)     5 (12.2%)      100%
                 Qwen3.8-27B                    5 (11.4%)     4 (9.8%)       80%
                 GPT-OSS-120B                   9 (20.5%)     4 (9.8%)       44%
                 v3b (ablation, Section 5.4)   10 (22.7%)     4 (9.8%)       40%


Instruct-100 instructions are often underspecified. Applying strict matching to B2 required
a manual audit of the 89 adjudicable tasks, and it exposed a benchmark property worth stating
explicitly: many instructions underspecify the target computation, so the reference output is not
uniquely determined by the instruction alone. In one task the reference multiplies the contraction
by a symbol never mentioned in the instruction; in another, “apply pattern matching rules to re-
place them with simpler expressions” does not state the rules; elsewhere “extract the coefficient of
a specific term” does not say which term, and “contract pairs of indices” admits several valid read-
ings. A solver that writes a correct, working program for a reasonable reading of the instruction
can therefore still fail the check. The B2 strict column in Table 3 is thus a conservative lower bound
on correctness, and the large exec-to-strict gap (e.g. 83.0% to 18.0% for our model) mixes genuine
errors with unmatchable specifications. Two remarks qualify our model’s B2 strict lead. The same
grading is applied to every model, so the ordering remains informative, but our training data was
generated by the same pipeline family as the B2 references, so our model may have learned some
of their arbitrary conventions (e.g. which symbol to carry through a contraction); part of its 18.0%
vs. 5.6% lead over the best frontier model may reflect this familiarity rather than raw skill.
    On Tutorial-44, where every task is fully specified by its reference program, the exec-to-strict
conversion is shown in Table 4—and it is sobering for every model: across the board, only a mi-
nority of programs that run also produce the expected result. Two observations stand out. First,
GLM-5.3’s apparent lead on B3 largely evaporates: it converts only 33% of its passes into gen-
uine solutions, so its strict rate (19.5%) is statistically indistinguishable from GLM-5.2’s (22.0%)
and from ours (14.6%, CIs all overlapping). Its high syntax-pass rate reflects fluency in writing
runnable Form, not superior problem solving. Second, models differ markedly in their “runs-but-
wrong” fraction—from Gemma 4’s 0% (it passes rarely, but almost always correctly) to 67% for
GLM-5.3 and 68% for our own model, the lowest conversion among the strong models—so syntax-
pass alone is a poor proxy for correctness at the individual-model level. We report both metrics for
full transparency, including for our own model. The strict metric also narrows the absolute spread
between all models to 9.8–22.0% of the 41 adjudicable tasks, confirming that B3-style tutorial
transfer remains hard for everyone.

                                                   14
Open-32 under the strict metric. Ten of the 32 Open-32 tasks ask the model to define a poly-
nomial “with at least four terms” of its choosing; their expected output is undetermined and
execution-based grading is impossible by construction—this is why B4 uses a rubric judge. On
the remaining 22 output-determined tasks we applied the same Form-verified adjudication (the
reference programs reproduce their own outputs on all 22, validating the metric). The rubric judge
turns out to be accurate here: GLM-5.3 converts 13 of its 14 rubric passes on the output-determined
tasks into genuine solutions, DeepSeek-V4 Flash 12 of 13, and our model 11 of 11. GLM-5.3’s
Open-32 lead is therefore largely genuine—unlike its Tutorial-44 lead—although the strict rates
(GLM-5.3 59.1% [36.4, 77.3] vs. FORM-8B 50.0% [27.3, 68.2], n=22) again have overlapping
CIs, and our ablation variants are on par (v3cn 59.1%, v3c with documentation 63.6%). For GPT-
OSS-120B and Gemma 4 the B4 strict column of Table 3 is based on the no-docs runs, since the
exact generations behind their published rubric scores were not retained.

Paired significance. Exact McNemar tests on the per-task verdicts (Section 4.3) confirm what
the overlapping CIs already suggest. Our Instruct-100 strict lead is significant against every frontier
model: 16/89 solved versus 5/89 for GLM-5.3 and GLM-5.2 gives p = 0.007, and versus 3/89 for
DeepSeek-V4 Flash and GPT-OSS-120B gives p < 0.001. On the small benchmarks no pairwise
comparison among the leading models reaches significance: on B3, FORM-8B (6/41) vs. GLM-
5.2 (9/41) gives p = 0.375 and GLM-5.2 vs. GLM-5.3 (8/41) gives p = 1.0; on B4, FORM-8B
(11/22) vs. GLM-5.3 (13/22) gives p = 0.727 and v3cn vs. GLM-5.3 (13/22 each) gives p = 1.0.
With 41 and 22 tasks, the entire gap between the best and worst strong model amounts to one or
two discordant tasks, which these sample sizes cannot resolve: B3 and B4 can establish that every
model is far from solving them, but not that any model leads.

5.4    Ablation Studies
Data Composition. Figure 5 shows the effect of data composition across benchmarks. The
v3b model (2,465 verified deterministic examples) achieves excellent deterministic perfor-
mance (96.1%) but collapses on open-ended tasks (29.0% on Instruct-100), demonstrating that
deterministic-only training narrowly specialises the model and destroys its ability to generate
code from open-ended instructions. Adding audited open-ended code, tutorial programs, and
knowledge Q&A (v3c, 4,633 examples) recovers open-ended capability (83.0% on Instruct-100)
while improving deterministic performance (97.7%). A further variant, v3cn, trained on the same
4,633 examples with the documentation-in-context prefixes removed, is marginally stronger on
B2 (88.0%) and B4 (68.8%) but slightly weaker on B1 (97.0%) and B3 (29.5%); we retain the
documentation slice in the released model because it matches deployment conditions in which
users may paste reference material into the prompt.

Data Scaling. Figure 6 shows the effect of dataset size and composition on Instruct-100 pass
rate (all numbers in this paragraph were measured on an earlier snapshot of the benchmark; model
rankings are unchanged). We compare two data-generation strategies: (1) the v1 pipeline (the
first, unverified iteration of our data pipeline: code-only data), which scales from 770 to 3,079
examples and reaches 90.1% at 75% of the data, and (2) the v3c pipeline (verified, diverse data),
which scales from 0 to 4,633 examples. The v3c ablation reveals a steep learning curve: the
base model scores 0.0%, but with just 1,158 verified examples (25%), pass rate jumps to 76.2%,

                                                  15
                                          Ablation: Effect of Data Composition
                                  97.7%                                                       v3b
                   100%   96.1%                                                               Det-only
                                                                                              (2,465 ex.)
                                                     83.0%                                    v3c
                                                                                              Full mix
                   80%                                                                        (4,633 ex.)
       Pass Rate


                   60%                                                                        56.2%
                                                                           43.2%
                   40%                                                                34.4%
                                             29.0%
                                                                   22.7%
                   20%

                    0%
                            664-Det       Instruct-100 (n=100)   Tutorial-44 (n=44)   Open-Ended 32

Figure 5: Ablation: effect of data composition. The v3b model (deterministic-only data, 2,465
examples) collapses open-ended capability. The v3c model (full mix, 4,633 examples) recovers it
while maintaining deterministic performance.

and with 2,316 examples (50%) it reaches 83.2%—nearly matching the full model’s 84.2% on
the same benchmark. The v3b model (2,465 verified deterministic-only examples) scores only
26.7%, demonstrating that data composition matters more than raw quantity: 2,316 diverse verified
examples (83.2%) dramatically outperform 2,465 deterministic-only verified examples (26.7%).
This confirms that verified multi-source data is the key driver of performance.

Documentation in Context. Because frontier baselines are evaluated with a syntax guide in
context (Section 4.2), one might suspect that our main-table advantage is a documentation artefact.
It is not: evaluated with the same guide that the frontier models receive, our top models barely
move (v3c 83.0→88.0%, v3cn 88.0→85.0% on the 100-task benchmark), whereas weak models
are rescued substantially (v3b 29.0→62.0%; the un-fine-tuned base 0.0→34.0%). Fine-tuning
subsumes the information carried by the documentation; documentation alone cannot substitute
for it at the level of our best models, though it explains part of the spread among weaker baselines.

5.5   Capability Preservation
A key concern with fine-tuning is catastrophic forgetting of pre-trained capabilities. We verify
that QLoRA fine-tuning preserves general reasoning by evaluating on three standard benchmarks
(Table 5 and Figure 7):
    The minimal degradation (≤ 2.6 pp on all three benchmarks) confirms that QLoRA—which
trains only 0.5% of the total parameters—effectively prevents catastrophic forgetting. This is con-
sistent with the literature [12, 13].




                                                         16
                                  100%
                                                Data Scaling: Effect of Dataset Size and Composition

                                  80%                                                             v3c: verified, diverse
         Instruct-100 Pass Rate                                                                   data recovers capability

                                  60%
                                                                                     v3b: det-only data
                                                                                     collapses open-ended
                                                                                     capability
                                  40%


                                  20%
                                                                                                       v1 (unverified, code-only)
                                                                                                       v3c (verified, full mix)
                                   0%                                                                  v3b (verified, det-only)
                                         0          1000           2000            3000                     4000
                                                                 Training Examples

Figure 6: Data scaling: effect of dataset size and composition. The v1 scaling curve (purple,
dashed) shows improvement with more unverified code-only data. The v3c curve (blue, solid)
shows the effect of verified, diverse data at 25%/50%/75%/100% of the full dataset. The v3b point
(orange square) shows that verified but deterministic-only data collapses open-ended capability
despite having more examples than the 50% v3c subset.

Table 5: General capability preservation. Changes relative to Qwen3-8B base. MMLU: full 9,183-
question test set; GSM8K: 200-problem subsample; HumanEval: all 164 problems.
                                  Benchmark                                 Base         FORM-8B                     ∆
                                  MMLU (5-shot) [18]                       76.5%             73.9%              −2.6 pp
                                  GSM8K (0-shot, flexible-extract) [19]    92.0%             90.5%              −1.5 pp
                                  HumanEval (0-shot) [11]                  63.4%             62.8%              −0.6 pp


5.6   Agentic Workflow Modification
The benchmarks in the previous sections evaluate single-turn code generation: one instruction, one
program, one verdict. In practice, however, physicists use Form as part of multi-file computational
workflows that include diagram generation (e.g., Qgraf [30]), shell orchestration scripts, and hand-
written Form procedures. A practically useful AI assistant must therefore operate in an agentic
mode: given a repository of undocumented code, it must read files, understand the calculation
pipeline, and rewrite it to accomplish a modified physics goal.
   Robust comparison of different LLMs in agentic mode is difficult for several reasons. First,
each model benefits from a different system prompt and tool-use style; a prompt optimised for one
model may disadvantage another. Second, agentic runs are inherently stochastic—the same model
may take different code paths across runs—so many repetitions are needed for reliable statistics.
Third, the evaluation metric (“did the rewritten workflow produce the correct physics?”) requires
running the full pipeline and comparing output files, making it expensive and task-specific. These
obstacles make a fair, large-scale agentic benchmark beyond the scope of this work.

                                                                    17
                 Capability Preservation: FORM Specialisation vs General Benchmarks
                                                              FORM
                                                           Instruct-100


                            MMLU

                                                                                    100%
                                                                              80%
                                                                        60%
                                                                  40%
                                                            20%
                                                                                       FORM
                                                                                      664-Det




                            GSM8K


                                                           HumanEval
                                    Qwen3-8B (base)         FORM-8B (fine-tuned)


Figure 7: Capability radar: the fine-tuned model (blue) gains dramatically on Form benchmarks
while retaining general capabilities (MMLU, GSM8K, HumanEval) close to the base model (grey).

    Nevertheless, to illustrate the practical value of our fine-tuned model, we report a representative
user experience using the Pi agent harness [31]—a minimal, extensible terminal-based coding
agent. In this demonstration, an agent is given an undocumented Form codebase that computes the
tree-level squared matrix element for gg → tt¯, along with the Qgraf configuration for amplitude
generation and an orchestrating bash script. The agent is tasked with extending the workflow to
compute the virtual NLO correction—specifically, the interference between the Born and one-loop
amplitudes, 2 Re(M(0)∗ M(1) ).
    We compare two configurations of the agent:

• Smart-routed: The agent uses Qwen3.8-27B as the primary model, with a routing rule that
  directs any request involving Form code to our fine-tuned 8B model. Non-Form tasks (editing
  bash scripts, modifying Qgraf configurations, writing documentation) are handled by the 27B
  model. No Form documentation is included in the context.
• Frontier with docs: The agent uses a single frontier model (GLM-5.2, 756B parameters) for all
  tasks, with the first 6,000 characters of the Form syntax guide prepended to every prompt.

    Both configurations are given the same repository and the same natural-language goal, with
no additional skills or extensions enabled in the harness. The smart-routed configuration success-
fully completes the task in fewer agent steps and with substantially fewer total input/output tokens,
because the fine-tuned model generates correct Form code without needing to consult documen-
tation on every turn. The frontier-with-docs configuration, by contrast, requires multiple repair
attempts on the Form portions of the workflow, increasing both token consumption and wall-clock

                                                      18
time. While this is a single demonstration rather than a controlled study, it illustrates the practical
advantage of domain-specialised models in agentic physics calculations: routing Form-related sub-
tasks to a small specialist avoids the overhead of injecting documentation into every frontier-model
prompt, while achieving higher code quality.


6     Discussion
6.1    Why Does an 8B Model Outperform 756B?
The result that an 8B fine-tuned model outperforms a 756B model by >20 pp may seem surprising.
The explanation lies in the zero-resource nature of Form: the 756B model has never seen Form
code during pre-training, and even with 6,000 characters of syntax documentation, it must infer
Form’s syntax from a brief description. The fine-tuned 8B model, by contrast, has been trained on
4,633 verified examples and has internalised Form’s syntax, idioms, and common patterns. This
demonstrates a key insight for scientific domain-specific languages: verified task-specific data
trumps raw parameter count when the target language is absent from pre-training corpora.

6.2    Absence of Proprietary API Models
A natural question is why we do not include results for proprietary API models such as Chat-
GPT (GPT-4/5), Claude, or Gemini. Our evaluation pipeline—which executes generated programs
through the Form binary and compares outputs—is fully compatible with any model that accepts a
text prompt and returns a text completion. However, evaluating these models requires paid API ac-
cess, and the scale of our benchmark suite (664 + 100 + 44 + 32 = 840 single-attempt evaluations
per model) would incur significant cost. Moreover, proprietary models frequently update their
weights without version pinning, making results non-reproducible. We therefore restrict our base-
line comparisons to open-weights models that can be self-hosted, version-pinned, and evaluated
with identical hardware and software configurations, ensuring full reproducibility.

6.3    Limitations
We identify several limitations of the current work:

1. Loosely-specified and small open-ended test sets: The strict output-match metric is well-
   defined only for a subset of the open-ended benchmarks (89 of 100 B2 tasks; 22 of 32 B4 tasks),
   and a manual audit found that many B2 instructions underspecify the target computation, so the
   B2 strict rate is a lower bound. The adjudicable subsets are also small (41 tasks for B3, 22 for
   B4): confidence interval half-widths reach ±20 pp, so results there are suggestive rather than
   significant. Expanding the open-ended test sets to 100+ fully-specified tasks would strengthen
   these claims.
2. No human evaluation: We do not conduct a user study with physicists. Execution-based
   metrics provide objective signal, but a human evaluation would validate the practical utility of
   the model.



                                                  19
3. Single base model: We fine-tune only Qwen3-8B. Results may differ for other base models
   (e.g., Qwen3-Coder, Llama).
4. Author-constructed benchmarks: The evaluation benchmarks and the fine-tuned model were
   developed by the same author, which inevitably introduces a potential bias: the benchmark
   tasks may inadvertently reflect the author’s own programming style and expectations, and may
   align with the training data used to fine-tune the model. In the absence of a community-
   established benchmark for Form code generation—a gap that reflects the zero-resource status
   of the language—constructing an in-house benchmark was the only viable option. We try to
   mitigate this concern by grounding all benchmark tasks in the official Form documentation and
   real physics use cases and by relying on execution-based metrics against the Form binary rather
   than subjective assessment. Releasing the suite as a public benchmark (Section 7) allows the
   community to audit and extend it.
5. Correctness, not runtime performance: All metrics verify whether generated code produces
   the correct output, not how fast it runs. Optimising Form runtime (statement ordering, .sort
   placement, dollar variables, pattern constraints) is a distinct expert skill in its own right; the
   training corpus carries no runtime-optimality signal and the benchmarks measure none. A
   runtime-aware extension (e.g., rewarding programs that beat a reference implementation’s wall-
   clock time on large expressions) is a natural follow-up.

6.4   Future Work
Several directions are promising for future work:

1. Reinforcement Learning from Verifiable Rewards (RLVR): The Form binary provides a
   deterministic reward signal (does the program run and produce the expected output?). This
   makes it a natural fit for GRPO (Group Relative Policy Optimization [32]), which has shown
   +9–16 pp improvements for code models (cf. [33]).
2. Expanded open-ended test set: Increasing the Open-32 and Tutorial-44 benchmarks to 100+
   tasks would reduce confidence interval widths and enable more definitive comparisons on open-
   ended generation.
3. Human evaluation: A study with 2–3 physicists evaluating 50 generated programs would
   validate practical utility.
4. Generalisation to other scientific DSLs: The verification-driven pipeline is applicable to any
   language with a deterministic execution environment (e.g., Cadabra [34], Redberry [35], and
   REDUCE [36]).


7     Conclusion
We have demonstrated that a small (8B) language model, fine-tuned with QLoRA on 4,633
verification-driven examples, can generate semantically correct Form symbolic algebra code at a
level that significantly exceeds frontier-scale models (up to 756B parameters) on the benchmarks
large enough to decide the comparison. The key insight is that for zero-resource domain-specific

                                                 20
languages, verified task-specific training data is more valuable than raw parameter count. Our
verification-driven pipeline—which uses the Form binary as an execution oracle—ensures that
every training example is syntactically valid and semantically consistent, producing high-quality
data without human annotation.
    The resulting model achieves 97.7% exact output match on 664 deterministic tasks and an
83.0% execution rate on 100 open-ended tasks, with non-overlapping 95% confidence intervals
against GLM-5.3, GLM-5.2 (756B) and DeepSeek-V4 Flash (304B) on these benchmarks. The
advantage persists under strict Form-verified output matching: on the output-determined Instruct-
100 subset (the 89 tasks with uniquely determined outputs) our model solves 18.0% versus 5.6%
for the best frontier model, and exact paired McNemar tests confirm the gap against every frontier
model (p ≤ 0.007). On the small Tutorial-44 and Open-32 benchmarks, where no model solves
even a quarter of the tasks, differences of the size observed between the leading models are statis-
tically unresolvable (p ≥ 0.375): these benchmarks show that everyone struggles, but not that any
model leads. General reasoning capability is preserved to within 2.6 pp on MMLU, GSM8K, and
HumanEval, confirming that QLoRA fine-tuning does not cause catastrophic forgetting.
    This work provides a template for bringing AI-assisted coding to niche scientific languages:
identify a deterministic execution oracle, generate and verify training data through it, and fine-tune
a small model with parameter-efficient methods. As Form continues to underpin precision calcu-
lations in particle physics [3], AI tooling that lowers the barrier to its use becomes increasingly
important for the community.
    The fine-tuned model weights and the complete benchmark suite—840 tasks with instructions,
references, evaluation harness, and per-task verdicts for all evaluated models—are publicly avail-
able on HuggingFace: the FORM-8B model [37] and the FORM-bench benchmark suite [38], each
with a persistent Digital Object Identifier. The training corpus is available from the author upon
request.

Acknowledgements
The author thanks Gudrun Heinrich, Adam Kardos, Marco Klann, Vitaly Magerya and Sven-Olaf
Moch for discussions and comments on the manuscript.
   The work of B.C. was supported by the Deutsche Forschungsgemeinschaft (DFG) under grant
396021762 — TRR 257 “Particle Physics Phenomenology after the Higgs Discovery”.


A     Representative Inference Examples
The following examples are drawn from the Instruct-100 benchmark and were generated by the
v3c model (FORM-8B) in a single attempt at temperature 0.0. Each example shows the natural-
language instruction, the generated Form program, and the actual Form binary output. All pro-
grams were verified by running through FORM 5.0.




                                                 21
Indices mu, nu;
Vectors p, q;
Dimension 4;
Local E = g_(1, mu) * g_(1, nu) * p(mu) * q(nu);
Trace4, 1;
contract;
Print;
.end


Figure 8: Example A1: Dirac trace with momentum contraction. Instruction: “Compute the
trace of a product of gamma matrices contracted with two external vectors, and simplify the result
using the metric tensor in four dimensions.” The model correctly uses Trace4 for the Dirac trace,
contract for Lorentz index contraction, and sets Dimension 4. FORM output: E = 4*p.q,
reflecting the trace identity Tr[γµ γν ] = 4 gµν .

Indices mu, nu, rho, sig;
Set ind: mu, nu, rho, sig;
CTensor g;
Local E = g(mu, nu) * g(nu, rho)
           * g(rho, sig) * g(sig, mu);
id g(mu?, nu?) = d_(mu, nu);
contract;
Print;
.end


Figure 9: Example A2: Wildcard pattern matching for metric contraction. Instruction: “Con-
tract pairs of indices from a declared index set using the metric tensor, then print the resulting
simplified scalar expression.” The model uses the wildcard pattern g(mu?, nu?) to replace the
symbolic tensor g with the metric d_ and then contracts. FORM output: E = 4, the correct result
for a chain of four metric contractions in four dimensions.
Symbols a, b, c;
Functions f (symmetric), g (antisymmetric);
Local E = f(a,b) + g(a,b) + f(b,a) + g(b,a);
id f(a,b) = a + b;
id g(a,b) = a - b;
Print;
.end


Figure 10: Example A3: Symmetric and antisymmetric function properties. Instruction: “De-
clare a symmetric function and an antisymmetric function, then apply pattern matching rules to
replace them with simpler expressions and print the result.” The model correctly declares the
symmetry properties, so that f(b,a) is automatically identified with f(a,b) and g(b,a) with
-g(a,b). FORM output: E = 2*b + 2*a, corresponding to 2(a + b) + (a − b) + (b − a) = 2a + 2b.

                                               22
Symbols x;
Local E = 0;
#do i = 1, 5
     Local E = E + x^‘i’;
#enddo
Print +f;
.end


Figure 11: Example A4: Preprocessor loop and the module-lifecycle pitfall. Instruction: “Use
a preprocessor loop to build a sum of powers of a symbol, then print the resulting polynomial.”
The model correctly uses the #do/#enddo preprocessor loop with backtick variable substitution,
and the program runs without error. The resulting output is nevertheless not the requested sum:
because the Local statement redefines E within a single module (there is no .sort between loop
iterations), each iteration discards the previous partial sum, and the final output is E = x5 rather
than x + x2 + x3 + x4 + x5 . We deliberately present this as an instructive failure example: the missing
.sort is exactly the subtle Form idiom discussed in Section 2.




Symbols p2, m2, A, B, C;
Vectors p, q;
Indices mu, nu;
CTensor g;
Local F = g(mu,nu)*A + p(mu)*p(nu)*B
           + q(mu)*q(nu)*C;
id g(mu,nu) = d_(mu,nu);
id p(mu)*p(nu) = p2*g(mu,nu);
id q(mu)*q(nu) = m2*g(mu,nu);
contract;
Print +f;
.end


Figure 12: Example A5: Tensor decomposition with metric substitution. Instruction: “Decom-
pose a rank-2 tensor integral with two Lorentz indices into scalar integrals by contracting with
the metric tensor and momentum vectors, then simplifying the result.” The model constructs a
general rank-2 tensor decomposition, then applies id rules to replace tensor structures with scalar
coefficients. FORM output: d_(mu,nu)*A + g(mu,nu)*m2*C + g(mu,nu)*p2*B.




                                                  23
References
 [1] J. Vermaseren, New features of FORM, arXiv preprint math-ph/0010025 (2000)
     [math-ph/0010025].

 [2] J. Kuipers, T. Ueda, J. Vermaseren and J. Vollinga, FORM version 4.0, Computer Physics
     Communications 184 (2013) 653 [arXiv:1203.6543].

 [3] J. Davies, T. Kaneko, C. Marinissen, T. Ueda and J. Vermaseren, FORM version 5.0, arXiv
     preprint 2601.19982 (2026) [arXiv:2601.19982].

 [4] J. Vermaseren, The FORM project, arXiv preprint 0806.4080 (2008) [arXiv:0806.4080].

 [5] A. von Manteuffel, E.W.N. Glover, E. Laenen, F. Herzog, G. Heinrich, J. Vermaseren et al.,
     Computer algebra for precision calculations in particle physics: the FORM project, Input to
     the European Strategy for Particle Physics — 2026 update, 2025.

 [6] S. Larin, P. Nogueira, T. van Ritbergen and J. Vermaseren, The 3-loop QCD calculation of
     the moments of deep inelastic structure functions, Nuclear Physics B 492 (1997) 338
     [hep-ph/9605317].

 [7] B. Ruijl, T. Ueda and J. Vermaseren, Forcer, a FORM program for the parametric reduction
     of four-loop massless propagator-type integrals to master integrals, Computer Physics
     Communications 253 (2020) 107198 [arXiv:1704.06650].

 [8] J. Blümlein, D. Broadhurst and J. Vermaseren, The multiple zeta value data mine, Computer
     Physics Communications 181 (2010) 582 [arXiv:0907.2557].

 [9] M. von Hippel, Crucial computer program for particle physics at risk of obsolescence,
     Quanta Magazine, 2022.

[10] D. De Biasio, The most important tool you’ve never heard of, CERN Courier, 2026.

[11] M. Chen et al., Evaluating large language models trained on code, arXiv preprint
     2107.03374 (2021) [arXiv:2107.03374].

[12] T. Dettmers, A. Pagnoni, A. Holtzman and L. Zettlemoyer, QLoRA: Efficient finetuning of
     quantized LLMs, in Advances in Neural Information Processing Systems (NeurIPS), 2023.
     arXiv:2305.14314.

[13] E. Hu, Y. Shen, P. Wallis, Z. Allen-Zhu, Y. Li, S. Wang et al., LoRA: Low-rank adaptation of
     large language models, in International Conference on Learning Representations (ICLR),
     2022. arXiv:2106.09685.

[14] A. Yang et al., Qwen3 technical report, arXiv preprint 2505.09388 (2025)
     [arXiv:2505.09388].

[15] A. Zeng et al., GLM-5: From vibe coding to agentic engineering, arXiv preprint 2602.15763
     (2026) [arXiv:2602.15763].


                                               24
[16] GLM-5-Team, GLM-5.3 model card, Hugging Face,
     https://huggingface.co/zai-org/GLM-5.3, 2026.

[17] A. Xu et al., DeepSeek-V4: Towards highly efficient million-token context language models,
     arXiv preprint 2606.19348 (2026) [arXiv:2606.19348].

[18] D. Hendrycks, C. Burns, S. Basart, A. Zou, M. Mazeika, D. Song et al., Measuring massive
     multitask language understanding, in International Conference on Learning
     Representations (ICLR), 2021. arXiv:2009.03300.

[19] K. Cobbe, V. Kosaraju, M. Bavarian et al., Training verifiers to solve math word problems,
     arXiv preprint 2110.14168 (2021) [arXiv:2110.14168].

[20] F. Cassano, J. Gouwar, D. Nguyen, S. Andersen, K. Ferry, E. Mast et al., Knowledge
     transfer from high-resource to low-resource programming languages for code LLMs, ACM
     Transactions on Software Engineering and Methodology (2024) [arXiv:2308.09895].

[21] F. Mora, J. Wong, H. Lepe, S. Verma, N. Polikarpova, D. Sorin et al., Synthetic programming
     elicitation for text-to-code in very low-resource programming and formal languages, in
     Advances in Neural Information Processing Systems (NeurIPS), 2024. arXiv:2406.03636.

[22] Z. Xu, N. Martelaro and C. McComb, Supervising Ralph Wiggum: Exploring a
     metacognitive co-regulation agentic AI loop for engineering design, arXiv preprint
     2603.24768 (2026) [arXiv:2603.24768].

[23] A. Heck, FORM for Pedestrians. NIKHEF, 2000.

[24] Unsloth, Unsloth: Fast fine-tuning for large language models, https://unsloth.ai,
     2024.

[25] Hugging Face, TRL: Transformer reinforcement learning,
     https://github.com/huggingface/trl, 2024.

[26] Qwen Team, Qwen3.8-Max: A new bar for coding and cowork,
     https://qwen.ai/blog?id=qwen3.8; model card at
     https://huggingface.co/Qwen/Qwen3.8-27B, 2026.

[27] Google DeepMind, Gemma 4 technical report, arXiv preprint 2607.02770 (2026)
     [arXiv:2607.02770].

[28] S. Agarwal et al., gpt-oss-120b & gpt-oss-20b model card, arXiv preprint 2508.10925
     (2025) [arXiv:2508.10925].

[29] Q. McNemar, Note on the sampling error of the difference between correlated proportions
     or percentages, Psychometrika 12 (1947) 153.

[30] P. Nogueira, Abusing QGRAF, Nuclear Instruments and Methods in Physics Research A 559
     (2006) 220.



                                               25
[31] earendil-works, Pi: A minimal agent harness for coding,
     https://github.com/earendil-works/pi, 2025.

[32] Z. Shao, P. Wang, Q. Zhu et al., DeepSeekMath: Pushing the limits of mathematical
     reasoning in open language models, arXiv preprint 2402.03300 (2024)
     [arXiv:2402.03300].

[33] D. Guo et al., DeepSeek-R1: Incentivizing reasoning capability in LLMs via reinforcement
     learning, arXiv preprint 2501.12948 (2025) [arXiv:2501.12948].

[34] K. Peeters, A field-theory motivated approach to symbolic computer algebra, Computer
     Physics Communications 176 (2007) 550 [cs/0608005].

[35] D. Bolotin and S. Poslavsky, Introduction to Redberry: a computer algebra system designed
     for tensor manipulation, arXiv preprint 1302.1219 (2013) [arXiv:1302.1219].

[36] A.C. Hearn, REDUCE: A User-Oriented Interactive System for Algebraic Simplification, in
     Proceedings of the Second ACM Symposium on Symbolic and Algebraic Manipulation,
     SYMSAC ’71, (New York, NY, USA), p. 128, ACM, 1971. DOI.

[37] B. Chargeishvili, FORM-8B (revision 41eac88), Hugging Face model card,
     doi:10.57967/hf/10525, 2026.

[38] B. Chargeishvili, FORM-bench (revision 6a33568), Hugging Face dataset card,
     doi:10.57967/hf/10524, 2026.




                                              26
