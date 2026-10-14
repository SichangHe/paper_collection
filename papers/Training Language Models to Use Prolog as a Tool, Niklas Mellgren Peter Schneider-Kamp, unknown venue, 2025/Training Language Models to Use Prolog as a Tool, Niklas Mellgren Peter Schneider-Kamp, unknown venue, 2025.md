                                                           Training Language Models to Use Prolog as a Tool
                                                            Niklas Mellgren                            Peter Schneider-Kamp
                                                     University of Southern Denmark                 University of Southern Denmark
                                                              mell@sdu.dk                              petersk@imada.sdu.dk

                                                                                    Lukas Galke Poech
                                                                               University of Southern Denmark
                                                                                   galke@imada.sdu.dk

                                                               Abstract                          final result as a side effect. However, more and
                                                                                                 more evidence suggests that reasoning traces are
                                             Language models frequently produce plausible
arXiv:2512.07407v3 [cs.CL] 25 Jun 2026




                                                                                                 not always faithful (Lanham et al., 2023; Paul et al.,
                                             yet incorrect reasoning traces that are difficult
                                                                                                 2024), i.e., the reasoning traces do not necessarily
                                             to verify. We investigate fine-tuning models
                                             to use Prolog as an external symbolic reason-       correspond to how the model actually arrives at
                                             ing tool, training Qwen2.5-3B-Instruct with         its final output. This lack of faithfulness renders
                                             Group Relative Policy Optimization (GRPO)           reasoning traces invalid as a robust explanation for
                                             on a cleaned version of GSM8K (which we             the final response or action.
                                             release as gsm8k-prolog-prover). We system-            Being able to trace and audit the reasoning of an
                                             atically vary prompt structure, reward compo-       LLM is crucial in order to validate and justify the
                                             sition (execution, syntax, semantics, structure),
                                                                                                 final decision (cf., EU AI Act). Textual reasoning
                                             and inference protocol (single-try, multiple-try,
                                             and two agentic modes). Our reinforcement
                                                                                                 traces that are potentially unfaithful do not serve
                                             learning approach outperforms supervised fine-      this purpose (Korbak et al., 2025). Thus, we here
                                             tuning on GSM8K, and the resulting 3B model         investigate an alternative way of reasoning, where
                                             achieves zero-shot performance on MMLU-             large language models interact with a symbolic
                                             STEM and MMLU-Pro competitive with 7B               reasoning engine. Symbolic reasoning engines,
                                             few-shot baselines. Most importantly, we iden-      such as implemented in the declarative Prolog pro-
                                             tify an accuracy–auditability trade-off: config-    gramming language, offer precise and auditable
                                             urations tuned for correctness alone learn to
                                                                                                 reasoning traces, i.e., composed of explicit facts
                                             delegate reasoning to natural language and use
                                             Prolog only for the final computation, while        and rules.
                                             configurations rewarded for symbolic structure         Recent studies have shown that prompting LLMs
                                             produce fully auditable programs at a cost in       to emit Prolog code, and then executing it in a sym-
                                             accuracy. We interpret this trade-off as a form     bolic runtime, can dramatically improve accuracy
                                             of reward hacking and discuss its implications      over text-only reasoning (Borazjanizadeh and Pi-
                                             for deploying neurosymbolic systems in safety-      antadosi, 2024; Tan et al., 2024; Yang et al., 2024b).
                                             critical domains.
                                                                                                 These methods currently rely on in-context learn-
                                             The source code for our experiments is avail-       ing prompting or supervised fine-tuning. However,
                                             able under https://github.com/aisilab/              only the most powerful commercial models are ca-
                                             Prolog-as-a-Tool
                                                                                                 pable of the level of in-context learning needed for
                                                                                                 using a niche programming language that likely
                                         1   Introduction
                                                                                                 has not much prevalence in the pre-training data.
                                         Reasoning is the key driver of recent advances in          Motivated by recent findings that reinforcement
                                         large language models (Guo et al., 2025; Muen-          learning may lead to better generalization than su-
                                         nighoff et al., 2025; OpenAI, 2024). With its ori-      pervised fine-tuning (Chu et al., 2025), we inves-
                                         gins in chain-of-thought prompting (Wei et al.,         tigate if we can teach an LLM to use Prolog as
                                         2022) to better handle logic puzzles and mathe-         a tool through reinforcement learning with veri-
                                         matical tasks, reasoning also powers LLM agents,        fiable rewards (RLVR). Specifically, we employ
                                         where reasoning steps are interleaved with tool         group relative policy optimization (GRPO) (Shao
                                         use (Yao et al., 2023). Reasoning traces, i.e., the     et al., 2024) which has led to promising results in
                                         text generated when reasoning is elicited, were ini-    DeepSeek-R1 and its R0 variant, which exclusively
                                         tially considered to yield an explanation for the       uses GRPO as post-training (Guo et al., 2025).
Figure 1: Overview of our training procedure for teaching a language model to produce executable Prolog code
(Inference Protocol 1) and to use Prolog as a tool (Inference Protocol 2).


   To teach a language model how to use Prolog via      inference protocols, revealing that: (a) prompt-
GRPO, we systematically study different system          reward interactions shape program syntax and
prompts, reward suites, and inference strategies.       logic; (b) best-of-N with external verification max-
   Our results will establish that RLVR, and specifi-   imizes in-distribution accuracy; and (c) agentic in-
cally GRPO, is well-suited to teach even a relatively   ference with internal repair yields superior zero-
small language model with only 3B parameters to         shot generalization under distribution shift (from
use Prolog as a tool – as evidenced by strong re-       GSM8k to MMLU).
sults on mathematical and logical reasoning tasks          Third, we identify an accuracy–auditability
(GSM8k, subsets of MMLU) that hit a weight-class        trade-off: configurations tuned for correctness
of LLMs above (i.e., the 3B + Prolog models are         learn to delegate reasoning to natural language,
comparable to 7B models). Moreover, the sym-            while structure-tuned configurations produce fully
bolic reasoning traces are spelled out as crisp log-    symbolic but less accurate programs. This finding
ical rules and derivations processed by Prolog’s        has direct implications for practitioners deploying
(faithful) symbolic reasoning engine. While our         LLM-based neurosymbolic systems.
experiments are currently limited to maths (where          We interpret this trade-off as a form of reward
most work on LLM-based reasoning originates),           hacking: when the reward signal only checks final-
we envision that reasoning traces in Prolog (i.e.,      answer correctness, the model learns to satisfy it by
logical derivations) will be useful more broadly in     delegating reasoning to natural language and using
safety-critical applications (e.g., healthcare, law).   Prolog as a minimal output wrapper, circumventing
                                                        the symbolic-reasoning behavior the reward was
Contributions In contrast to prior work that has        intended to induce.
relied on in-context learning or supervised fine-
tuning to have language models emit Prolog code,        2   Related Work
we use reinforcement learning with verifiable re-
                                                        Our work brings together reasoning and tool use
wards to teach language models to use Prolog as a
                                                        in large language models. Whereas prior work
tool. Our main contributions are three-fold:
                                                        has regarded reasoning and tool use as separate
   First, we demonstrate that reinforcement learn-
                                                        steps (Yao et al., 2023), we hybridize this account
ing with verifiable rewards enables small language
                                                        and investigate using a symbolic reasoning engine
models to use Prolog as an external tool, outper-
                                                        as a tool. We will now lay out the related work on
forming supervised fine-tuning baselines. Criti-
                                                        reasoning and tool use for symbolic reasoning.
cally, our 3B model with agentic inference achieves
zero-shot performance on MMLU benchmarks                Reasoning The idea of reasoning in large lan-
close to few-shot performance of 7B models, show-       guage models has its origins in the chain-of-thought
ing that Prolog tool use can compensate for scale.      prompting strategy (Wei et al., 2022), later used for
   Second, we conduct a systematic investigation        crafting AI agents that interleave tool use and rea-
across prompt structures, reward compositions, and      soning about the tools’ outputs (Yao et al., 2023).
More recently, studies have investigated how rea-      3     Methods
soning can be ingrained into language models
through reinforcement learning with verifiable re-     Our aim is to teach a relatively small language
wards on mathematical reasoning tasks (Shao et al.,    model to use Prolog as a tool. Beyond the tool-
2024; Guo et al., 2025). Specifically, DeepSeek-       calling syntax, the language model must be capable
Math (Shao et al., 2024) has introduced group-         of emitting proper Prolog code that ideally models
relative policy optimization (GRPO), whereby the       the example at hand.
language model generates multiple reasoning traces        Prolog is a declarative programming language in
and final outputs. The final output is compared to     which facts and rules can be described and subse-
the ground truth and the reward is backpropagated      quently processed by a symbolic reasoning engine.
through the reasoning trace that led to a positive     A minimal example of a Prolog program is a. b
outcome. DeepSeek-R1 (Guo et al., 2025) further        :- a. c :- b. ?- c., which would lead the
shows that GRPO as sole post-training method in-       reasoning engine to conclude that c is true. Prolog
duces reflection-like behavior, enabling test-time     fully implements first-order predicate logic.
scaling (Muennighoff et al., 2025).                       The rationale here is that through providing an
   Recent work has questioned the faithfulness of      interface to Prolog’s reasoning engine, we should
chain-of-thought reasoning traces (Lanham et al.,      be able to improve language models’ capabilities to
2023; Paul et al., 2024), motivating our approach      carry out sound reasoning as the logical derivations
of integrating language models with a symbolic         are performed by a symbolic reasoning engine. The
reasoning engine.                                      reasoning process, as executed via Prolog code, is
                                                       therefore verifiable and auditable.
Symbolic Reasoning Tool use in language mod-              Given a dataset of reasoning tasks and numer-
els originated in ToolFormer (Schick et al., 2023),    ical ground truth values {xi , yi }i<N , we have a
where a language model was trained to use ba-          language model generate G responses for each
sic tools, such as a calculator to help with sim-      xi , i < N . Those responses that lead to the cor-
ple arithmetic. Early approaches on integrating        rect outcome are assigned a positive reward, with
Prolog with language models focus on prompt-           the possibility of combining this main reward func-
ing (Tan et al., 2024) and LoRA finetuning for         tion with extra reward functions, e.g., nudging the
Prolog generation while leveraging permutation         model to produce syntactically correct Prolog code
invariance (Yang et al., 2024b). Borazjanizadeh        and preventing the model from circumventing the
and Piantadosi (2024) introduce a pure zero-shot       task through a print statement.
neurosymbolic Prolog pipeline that prompts a pre-         The standard way to teach a language model
trained LLM to emit Prolog predicates and rules        to use new tools is through supervised fine-
without any fine-tuning – and then executes them in    tuning (Schick et al., 2023), which we consider
SWI-Prolog (a Prolog interpreter). With a multiple-    our baseline. Our key hypothesis is that reinforce-
try inference loop – sampling up to N candidate        ment learning with verifiable rewards may be better
programs and halting on the first one that executes    suited to teach a language model to use Prolog as a
successfully – they achieve substantial gains in ac-   tool than supervised fine-tuning.
curacy: When using GPT-3.5 Turbo + Prolog with            We experiment with four carefully crafted sys-
multiple-try inference, they report 80.4% accuracy     tem prompts (as will be detailed in §3.1), three
versus 57.1% for text-only CoT, and GPT-4 + Pro-       different reward suites (§3.2), and two types of in-
log reaches 95.2% versus 92.0% text-only CoT.          ference protocols: prolog-as-output and prolog-as-
   Concurrently to our work, Pennino et al. (2025)     a-tool, each of which instantiated with two different
also studied using GRPO for teaching a language        concrete protocols (§3.3).
model to use Prolog through a Python bridge
(PySwip). Despite similarities to our work, the        3.1    System Prompts
results and findings are different: Our systematic     We evaluate four system prompts varying in struc-
exploration of combinations of system prompts, re-     tural constraint: SP-Base provides a minimal two-
ward suites, and agentic protocols, has enabled our    part XML template; SP-Struct enforces explicit
approach to challenge larger language models and       code layout with numbered reasoning steps; SP-
revealed an auditability-accuracy trade-off, which     Declare, inspired by Tan et al. (2024), requires
we expect to inform future work in the area.           every numeric constant to be encoded as a named
predicate, ensuring reasoning is captured symbol-      consistent with common practice for reasoning-
ically rather than in natural language; and SP-        focused generation.
Reflect adds a self-correction loop where the model
                                                       Prolog-as-output In both single-try inference
reviews its reasoning before emitting code. Full
                                                       and multiple-try inference protocols, SWI-Prolog
prompts appear in Appendix A.
                                                       is used post hoc as an external tool invoked only
3.2   Reward Composition                               after the LLM produces an answer. The model has
                                                       no visibility into the execution result and cannot
As GRPO is based on reinforcement learning, it
                                                       revise its output in response. This setup reflects
allows us to flexibly define a reward function (that
                                                       a generate-then-verify paradigm, where symbolic
does not need to be differentiable). We experiment
                                                       correctness is assessed retrospectively.
with three different reward suites.
                                                          In the first protocol, Single-Try inference,
   Reward suite 1 (Rwd1) combines four signals:
                                                       we flatten the system prompt and user mes-
correctness (comparing executed output to ground
                                                       sages into one prompt per problem, extract the
truth), Prolog syntax (detecting hallmark constructs
                                                       <answer>...</answer> block, and execute it in
like :- and solve/1), and soft/strict format rewards
                                                       SWI-Prolog. This protocol estimates P (correct |
for XML schema compliance.
                                                       prompt) without retries or feedback.
   Reward suite 2 (Rwd2) adds semantic similar-
                                                          The second prolog-as-output protocol, Multiple-
ity via Sentence-BERT embeddings and predicate-
                                                       Try inference, leverages sampling diversity by
name overlap. The semantic similarity component
                                                       drawing up to N = 20 independent completions
promotes code that corresponds to reference solu-
                                                       per prompt. We halt at the first response that pro-
tions even when surface forms differ, encouraging
                                                       duces an integer or float. We record the number
meaningful use of Prolog.
                                                       of tries until first success. This best-of-N decod-
   Reward suite 3 (Rwd3) introduces curriculum-
                                                       ing converts capability into effective accuracy and
guided weighting that shifts from format to cor-
                                                       mirrors the setup of earlier works (Tan et al., 2024;
rectness as training progresses. Reward suite 3
                                                       Borazjanizadeh and Piantadosi, 2024).
additionally penalizes hard-coded solutions where
solve/1 directly assigns a numeric literal, scaling    Prolog-as-a-tool In both Agentic Internal and
the structure reward by 0.2 to discourage circum-      Agentic Independent, SWI-Prolog acts as an inter-
venting symbolic reasoning. Table 1 summarizes         active, callable engine, transforming the LLM’s
the composition. Full details of the three reward      behavior from passive code generation to tool-
suites are provided in Appendix B.                     augmented reasoning with verification capabilities.
                                                          These protocols treat SWI-Prolog as an inter-
  Reward components            Rwd1   Rwd2    Rwd3     active tool accessible during generation. We de-
  Correctness                   ✓      ✓        ✓      fine a callable function run_prolog() using struc-
  Prolog Syntax                 ✓      ✓        ✓      tured <tool_call> blocks from the Qwen tok-
  Response Format               ✓      ✓        ✓
  XML Tag Count                 ✓      ✓        ✓      enizer’s chat template. The model invokes this
  Semantic Similarity                  ✓        ✓      tool mid-dialogue, receives execution results, and
  Predicate Name Overlap               ✓        ✓      integrates the feedback into subsequent reasoning
  Prolog Structure                              ✓
  prolog_helpers.pl                             ✓      turns, thereby enabling iterative refinement.
  Hard-coding penalty                           ✓         In the Agentic-Internal protocol, we embed a
  Curriculum weighting                          ✓      self-reflective correction loop within a single ses-
  Multi-objective balancing                     ✓
  Normalization and clipping                    ✓      sion of up to 20 turns. After each decode-execute
                                                       step, failures (syntax errors, unbound variables, re-
   Table 1: Composition of different reward suites.    cursion timeouts, or non-numeric outputs) trigger
                                                       targeted feedback and enable the language model
                                                       to iterate.
3.3   Inference Protocols                                 We also “shake” the temperature (multiplying by
We evaluate our Prolog-grounded reasoning              1.15 up to 0.3) if repeated or empty generations oc-
pipeline under four complementary protocols:           cur, and compress older messages into summaries
Single-Try, Multiple-Try, Agentic Internal, and        once the prompt length exceeds 95% of the 2048-
Agentic Independent. Each protocol is run at           token context budget. This design enables in-place
a fixed decoding temperature of 0.2 throughout,        correction and self-verification (Tan et al., 2024).
   In the Agentic-Independent protocol, we treat         Implementation details All experiments use a
each generation-execution-reflection cycle as a          4-bit quantized Qwen2.5-3B-Instruct (Yang et al.,
bounded, self-contained “agentic try”. We allow          2024a) and attach a LoRA (Hu et al., 2022) adapter
up to 20 total turns per problem, but unlike the         for parameter-efficient GRPO training on a 40 GB
Agentic Internal strategy, we discard context and        GPU. After training, we merge the LoRA weights
reset the session entirely whenever we detect signs      into the base checkpoint to obtain a full 16-bit
of persistent failure, e.g., repeated empty gener-       model for downstream evaluation.
ations, invalid numeric outputs, or excessive du-
plicate attempts. Each fresh retry reinitializes the     Hyperparameters We train for one epoch with
conversation with only the original system and user      the AdamW optimizer, a batch size of 8, a learn-
messages, exploring a new trajectory in the model’s      ing rate of 5 · 10−6 , a cosine learning rate sched-
sampling space. This hard-reset policy helps es-         ule, weight decay of 0.1, and gradient clipping to
cape local minima and recursion traps that in-place      0.1. Random seeds are kept fixed. We ran a sys-
correction may reinforce. Within each problem,           tematic sweep over relevant hyperparameters, but
the total retry budget is preserved: the number of       the best configuration did not improve over these
turns used in each session is subtracted from the        manually-optimized ones. Details can be found in
global cap of 20. We continue until either (i) a valid   Appendix F.
numeric result is produced, or (ii) the full budget is   Baselines As our main baseline, we contrast our
exhausted.                                               approach with supervised fine-tuning (SFT) base-
   For both agentic protocols, the system prompt is      line, which employs a standard causal language
extended by a tool declaration that describes how        modeling objective. For perfect comparability, we
the Prolog tool can be invoked. Exact prompts can        use the same data and the same base model as in
be found in Appendix C.                                  our proposed GRPO training strategy. We further
                                                         use the same hyperparameters as those used for our
4   Experimental Setup                                   GRPO training. For reference, we also include the
                                                         performance of larger and more powerful models,
Datasets and pre-processing We build upon the            such as DeepSeekMath-7B-RL, Mistral-7B and
gsm8k-prolog dataset (Yang et al., 2024b), which         Gemma-7B on the official GSM8k test split and on
provides an SWI-Prolog implementation for each           MMLU-STEM/Pro.
GSM8K problem from the original openai/gsm8k             Evaluation Measures For every generated re-
dataset. For every example, we run the reference         sponse, we evaluate three complementary metrics.
Prolog code under CLP(Q) and compare its numeric         First, the main evaluation is accuracy measuring
result to the original openai/gsm8k answer.              whether the output parses as a valid integer or float
   Out of 7473 problems, we found 15 discrepan-          and exactly matches the numeric answer in the
cies: 14 arose from errors in the OpenAI GSM8K           ground truth.
answers (error rate of 0.1874% in the original              Second, structural validity checks whether
dataset), and one from the Prolog references. We         the generated Prolog code includes at least one
manually recomputed and reformatted each correct         user-defined predicate other than solve/1 and
answer to match the official style, then updated         at least one arithmetic constraint enclosed in
both splits and created the cleaned gsm8k-prolog-        {. . . }. This is assessed using the static analyzer
prover dataset, now fully consistent under SWI-          prolog_helpers.pl. This metric captures the
Prolog execution.                                        cases where the LLM reasons mainly in natural lan-
   Throughout our experiments we will use a sub-         guage and only emits a final “solve”-statement to
set of 2,500 examples from this new gsm8k-prolog-        satisfy the Prolog output constraint – which would
prover dataset. We split this subset into 1750 train-    result in low structural validity.
ing examples, 375 validation examples, and hold             Third, semantic similarity quantifies how close
out another 375 examples as a test set. For test-        the generated logic is to the reference Prolog pro-
ing, we also report scores on the official GSM8k         gram using cosine similarity over embeddings. We
test set as well as a zero-shot generalization test on   have devised this metric to measure auditability:
MMLU-Stem (Hendrycks et al., 2021) and MMLU-             Although variable naming is in principle arbitrary
Pro (Wang et al., 2024).                                 and does not change the logic of the program, we
argue that it contributes to auditability when the      four inference methods, GRPO training yields 56%
variable names are semantically related (as mea-        higher accuracy scores than the SFT baseline.
sured by cosine over contextualized embeddings)
to the concepts found in the task description.          Results for the official GSM8k Test Split We
                                                        evaluate both the fully-trained and subset-trained
                                                        variants of the best-performing configuration,
5   Results
                                                        sp-struct-rwd1, on the official openai/gsm8k
Comparison of System Prompts and Reward                 test split (1320 examples). Each model is tested
Suites We evaluate our GRPO training method             across all four inference strategies. Table 5 shows
on the gsm8k-prolog-prover validation dataset           the results. Although our best GRPO-trained 3B
under all three reward suites and both Single-Try       model surpasses DeepSeekMath-7B-RL on our val-
and Multiple-Try inference protocols. Table 2           idation set with multiple-try inference (89.87% vs.
shows the results. The most accurate model is           86.7%), it scores only 80.21%, below DeepSeek-
sp-struct-multipletry-rwd1, which achieves              Math’s 86.7% on the GSM8K test set.
89.87% accuracy. Reward suite 1 consistently               The full GSM8K test set, containing more varied
yields the highest accuracy across prompt variants.     formulations, favors Agentic-Internal, which accu-
                                                        mulates debugging context across attempts. De-
   Accuracy is highest under SP-Struct system
                                                        spite being trained on only 23.4% of the data, the
prompt with reward suite 1. The best-performing
                                                        subset model is only 1–2 points behind the fully-
models in semantic similarity use the SP-Declare
                                                        trained model.
prompt with reward suite 3. The best model
in terms of structural validity is based on the         Zero-Shot Generalization Test We measure
SP-Declare prompt with reward suite 1. For              cross-dataset generalisation by evaluating the
SP-Struct and SP-Declare, we generally observe          fully–trained model on the multiple-choice datasets
large gains in structure score under reward suite 3.    MMLU-STEM and MMLU-Pro. The STEM
For example, SP-Declare improves from 49.60%            dataset covers physics, chemistry, biology, and en-
(Rwd1) to 94.67% (Rwd3) in structural validity.         gineering disciplines and the Pro dataset covers
The only exception is SP-Base, which consistently       law, finance, medicine, philosophy – contributing
underperforms in structural validity. Moreover, the     375 validation questions each. We keep the original
multiple-try strategy consistently yields substantial   SP-Struct prompt and prompt for the zero-based
accuracy gains over single-try inference.               index of the correct multiple-choice option without
                                                        any in-context examples (zero-shot). Details can
Comparison of Prolog-as-a-Tool Inference Pro-           be found in Appendix E.
tocols Next, we evaluate the agentic internal and          As shown in Table 6, the agentic inference
agentic independent inference protocols with the        protocols, Internal and Independent, consistently
best performing reward suite 1 and all system           outperform Single-Try and Multiple-Try infer-
prompts. As shown in Table 3, the most accu-            ence. Specifically, on MMLU-STEM, our full-
rate results (86.13%) are obtained with the Agentic     data model improves from 53.6% (Multiple-Try) to
Independent protocols combined with either the SP-      58.13% (Agentic Independent). MMLU-Pro shows
Base or the SP-Struct system prompt. However, the       an improvement from 26.67% (Multiple-Try) to
second best results with an accuracy of 84.27% are      30.7% (Agentic Internal). Interestingly, the results
obtained by the agentic internal setting. Notably,      from our models under zero-shot are comparable
the SP-Declare system prompt excels in semantic         to models with a 7B parameter budget from the
similarity and structure.                               DeepSeekMath, Mistral, and Gemma families with
                                                        few-shot prompting with 5 examples available in
GRPO versus SFT Baseline We test whether                the prompt to facilitate in-context learning. Note
our proposed GRPO-based training method outper-         that this evaluation primarily tests generalization of
forms the supervised fine-tuning (SFT) baseline         the tool-augmented language model to other eval-
in a fully controlled environment (same starting        uation benchmarks rather than testing specifically
model, same hyperparameters, same training data).       for more complex symbolic reasoning.
As shown in Table 4, the best GRPO method ex-
ceeds the best SFT method by more than 10 accu-         Qualitative Analysis Analyzing the logfiles for
racy points (90% vs. 79%). On average across the        sp-struct-rwd1 (examples in Appendix D), we
                      Prompt         Training             Inference      Acc ↑   Sem ↑   Struc ↑
                                     GRPO w/ Rwd1         Single-Try     77.87    3.20    0.00
                                     GRPO w/ Rwd2         Single-Try     80.27   17.60    0.27
                                     GRPO w/ Rwd3         Single-Try     82.67   10.13    0.27
                      SP-Base
                                     GRPO w/ Rwd1         Multiple-Try   85.33    2.13    0.27
                                     GRPO w/ Rwd2         Multiple-Try   84.53   20.00    0.27
                                     GRPO w/ Rwd3         Multiple-Try   82.93    9.33    0.00
                                     GRPO w/ Rwd1         Single-Try     85.33    5.60     1.07
                                     GRPO w/ Rwd2         Single-Try     73.60   29.07     3.20
                                     GRPO w/ Rwd3         Single-Try     64.27   29.33    66.93
                      SP-Struct
                                     GRPO w/ Rwd1         Multiple-Try   89.87    8.27     1.60
                                     GRPO w/ Rwd2         Multiple-Try   84.53   32.00     3.20
                                     GRPO w/ Rwd3         Multiple-Try   83.73   40.00    89.60
                                     GRPO w/ Rwd1         Single-Try     34.40   31.20    49.60
                                     GRPO w/ Rwd2         Single-Try     33.07   33.33    46.40
                                     GRPO w/ Rwd3         Single-Try     26.27   26.27    42.40
                      SP-Declare
                                     GRPO w/ Rwd1         Multiple-Try   66.93   59.73    94.67
                                     GRPO w/ Rwd2         Multiple-Try   73.60   62.13    92.53
                                     GRPO w/ Rwd3         Multiple-Try   62.40   62.67    90.40
                                     GRPO w/ Rwd1         Single-Try     74.40    1.60     0.80
                                     GRPO w/ Rwd2         Single-Try     79.73    4.53     0.00
                                     GRPO w/ Rwd3         Single-Try     72.00   22.40    76.27
                      SP-Reflect
                                     GRPO w/ Rwd1         Multiple-Try   88.53    2.93     1.33
                                     GRPO w/ Rwd2         Multiple-Try   88.27    2.93     0.27
                                     GRPO w/ Rwd3         Multiple-Try   87.73   26.13    91.47

Table 2: Validation results of GRPO-trained Qwen-2.5 3B models across prompt variants, reward suites, and
inference strategies. Accuracy (Acc), semantic similarity (Sem), and structure validity (Struc) are averaged over
gsm8k-prolog-prover validation set (375 samples). Best results per metric are marked bold, second best underlined.


 Prompt        Agentic Mode        Acc    Sem     Struc         racy (73.60%). The declarative prompt improves
               Internal           82.93   58.52   0.80          code form further at the cost of accuracy. To test
 SP-Base
               Independent        86.13   58.95   0.27          whether this pattern generalizes beyond individual
               Internal           84.27   55.18   5.07          examples, we next conduct a systematic error anal-
 SP-Struct
               Independent        86.13   56.08   5.87          ysis across the best-performing configurations per
 SP-Declare
               Internal           69.87   81.36   73.07         metric.
               Independent        72.00   80.68   72.53
               Internal           84.27   54.57    9.07         Systematic Error Analysis We select three runs
 SP-Reflect
               Independent        83.47   54.57   10.40         from Table 2, one per evaluation metric: the
                                                                SP-Struct prompt with reward suite 1 for the high-
Table 3: Agentic evaluation on gsm8k-prolog-prover              est accuracy (90%), SP-Declare with reward suite
validation set. For each prompt variant, we report ac-          1 achieves the highest structural validity (95%),
curacy (Acc), semantic similarity (Sem), and structural
                                                                and SP-Declare with reward suite 3 for the high-
correctness (Struc) using reward suite 1.
                                                                est semantic similarity. A systematic error analysis
                                                                reveals a clear auditability-accuracy trade-off (see
observe that the model delegates final computa-                 Figure 2). The SP-Struct run almost never re-
tions to SWI-Prolog via solve/1, but performs                   quires retries (1.08 attempts on average), and when
its intermediate reasoning in natural language.                 it fails it is almost always a generation failure: the
This explains the high accuracy yet poor seman-                 model did not produce valid code, which leads
tic and structural alignment (sem: 8.27%, struc:                to the next attempt. Its dominant failure mode
1.60% in multiple-try). It reaches correct answers              is wrong answers (10% of samples), suggesting
but deviates from the Prolog reference solutions                that the minimal prompt produces code that exe-
of the gsm8k-prolog-prover dataset. In con-                     cutes cleanly but occasionally encodes incorrect
trast, sp-declare-rwd2 emits Prolog code that                   reasoning. The SP-Declare runs show the inverse
matches reference structures and achieves strong                pattern: both require substantially more attempts
semantic similarity (62.13%) and structural cor-                (2.4 and 3.0 on average, up to 17–20) and produce
rectness (92.53%), but at the cost of lower accu-               far more wrong answers (31% and 36%). Their ex-
              Training method        Prompt       Reward        Inference              Acc    Sem     Struc
              SFT (baseline)         SP-Struct    —             Single-try            21.60   20.80   64.27
              SFT (baseline)         SP-Struct    —             Multiple-try          65.07   36.00   66.13
              SFT (baseline)         SP-Struct    —             Agentic Internal      79.20   68.03   49.60
              SFT (baseline)         SP-Struct    —             Agentic Independent   55.46   73.98   52.53
              GRPO (ours)            SP-Struct    Rwd1          Single-try            85.33    5.60    1.07
              GRPO (ours)            SP-Struct    Rwd1          Multiple-try          89.87    8.27    1.60
              GRPO (ours)            SP-Struct    Rwd1          Agentic Internal      84.27   55.18    5.07
              GRPO (ours)            SP-Struct    Rwd1          Agentic Independent   86.13   56.08    5.87

              Table 4: Comparison of GRPO versus SFT on the gsm8k-prolog-prover validation set


                                                                  ecution failures additionally include uninstantiated
 Model                  Inference Protocol         Accuracy       variables (11–16% of failed attempts), which arise
 Qwen2.5-7B-Instruct
                                                                  when the declarative constraint structure is too un-
 (Yang et al., 2024a)                                    91.6     derspecified to ground the answer. Taken together,
 DeepSeekMath-7B                                                  the results suggest that the declarative prompt suc-
 (Shao et al., 2024)                                     86.7
                                                                  cessfully induces structural validity but at the cost
                        Single-Try                    75.28       of introducing more complex constraints that the
 Qwen2.5-3B-Instruct
 SP-Struct RWD1         Multiple-Try                  80.21       model struggles to get right, and that retrying un-
 (7473 examples)
                        Agentic-Internal              78.17       der the same prompt only helps to some extent:
                        Agentic-Independent           77.86       samples that ultimately fail tend to do so because
                        Single-Try                    73.99       the underlying reasoning is wrong, not because the
 Qwen2.5-3B-Instruct
                                                                  code is malformed.
 SP-Struct RWD1         Multiple-Try                  78.24
 (1750 examples)
                        Agentic-Internal              77.20        6   Discussion
                        Agentic-Independent           76.80
                                                                   Our experiments reveal several key insights about
Table 5: Performance of full-data vs. subset-trained               reinforcement learning for integrating symbolic rea-
models on the official openai/gsm8k test split. Best               soning into language models, which we discuss in
and second-best compared 3B variants are highlighted.              the following.
                                                                  Accuracy vs. Auditability Trade-off We find
                                                                  that simple execution-based rewards yield the high-
 Model                      MMLU-Stem            MMLU-Pro
                                                                  est accuracy, but this comes with a trade-off:
                                                                  models learn to emit minimal Prolog that dele-
 Our 3B models with zero-shot prompting
 Single-Try                   50.93                21.33          gates reasoning to natural language. The highest-
 Multiple-Try                 53.60                26.67          accuracy configuration (sp-struct-rwd1, 89.87%)
 Agentic-Internal             56.80                30.67          produces Prolog code with minimal structural va-
 Agentic-Independent          58.13                29.33
                                                                  lidity (1.60%) and low semantic similarity (8.27%).
 7B baseline models with few-shot prompting
 DeepSeekMath-Base 7B         56.50           –
                                                                  Qualitative analysis confirms this model mostly
 Mistral 7B                   51.10         30.90                 reasons in natural language and uses Prolog only as
 Gemma 7B                       –           33.70                 much as needed, i.e., for producing the final output.
                                                                  Reward suites 2 and 3 on SP-Declare achieve up to
Table 6: Zero-shot evaluation of our 3B Qwen-2.5 mod-
                                                                  92.5% structural validity and 62% semantic simi-
els trained with GRPO via SP-Struct-RWD1-full on the
validation set with our four inference protocols. Base-
                                                                  larity, but accuracy drops to 62–74%. When these
line 7B models use few-shot prompting. Our Prolog-                reward signals are omitted, the models discover that
enhanced 3B model can close the gap to 7B models even             reasoning can be deferred to natural language and
without extra examples. Best and second best results are          only a final minimal Prolog code snippet is needed.
highlighted per model size group. MMLU-Pro results                While this trade-off requires further investigation,
for Mistral 7B and Gemma 7B are taken from Wang                   we can so far conclude that richer reward signals
et al. (2024). MMLU-Stem results for DeepSeekMath-                successfully steer models toward more symbolic
Base 7B and Mistral 7B are from Shao et al. (2024).
                                                                  reasoning, but additional structural constraints in-
                                                                  troduce opportunities for error.
                                                        (a) Sample outcomes                                suite 1 outperforms more complex semantic and
                                                   Correct
       Struct rwd1                                 Wrong answer                             90% 10%        structural signals across all prompt variants. In
                                                   Never executed                                          the tool use setup, Agentic-Independent slightly
      Declare rwd1                                                           67%                   31%     outperformed Agentic-Internal, presumably due
                                                                                                           to hard resets to escape local traps. On the full
      Declare rwd3                                                          62%                    36%     openai/GSM8K test set, however, Agentic-Internal
                                           0          20          40         60             80       100   yielded the best results, presumably due to pre-
                                                                 Samples (%)
                                                                                                           serving debugging context for incremental refine-
                                                 (b) Attempt-level error types                             ment. Generally, multiple-try inference suffices for
                                                No code extracted                                          narrow arithmetic problems, whereas interactive
                                     800        Uninstantiated variable
           Failed attempts (count)




                                                Rational number                                            self-repair becomes crucial under distribution shift,
                                                Unevaluated expression
                                                Atom instead of number
                                     600        Timeout                                                    such as on our MMLU generalization tests.
                                                Compound term
                                                Other
                                     400
                                                                                                           Implications for Safety-critical Domains Our
                                     200                                                                   experiments use GSM8K as a controlled testbed,
                                                                                                           yet our results have direct implications for appli-
                                       0
                                               rwd1                  rwd1                   rwd3           cations in domains where auditability is crucial,
                                      Struct               Declare                Declare
                                                                                                           such as in the health domain and the legal do-
                                                                                                           main. The accuracy–auditability trade-off we iden-
                                                                                                           tify suggests practitioners must choose configura-
Figure 2: Error analysis across the best-performing                                                        tions based on whether their application prioritizes
runs per metric. (a) Sample-level outcomes: the Struct                                                     raw performance or auditability.
prompt achieves high execution accuracy (90%) but
at the cost of structural validity, while both Declare                                                     7   Conclusion
variants produce more wrong answers (31–36%). (b)
Distribution of error types across all failed attempts:                                                    We have introduced a training pipeline, including
the majority are generation failures (no code extracted),                                                  concrete system prompts and reward suites, to teach
with uninstantiated variables being the most common                                                        language models to use Prolog as a tool via rein-
execution-level error and disproportionately affecting                                                     forcement learning with verifiable rewards. Our
the more complex Declare prompts.                                                                          findings show that: (1) the interaction between sys-
                                                                                                           tem prompt and reward function shapes the syntac-
   This pattern is a clear instance of reward hack-                                                        tic and logical form of generated Prolog programs;
ing (Skalse et al., 2022): the correctness reward                                                          (2) multiple-try decoding with Prolog verification
is a proxy for “reason symbolically and arrive at                                                          achieves the highest accuracy on in-distribution
the right answer,” but it only checks the latter. The                                                      tasks; and (3) agentic inference with an internal
model discovers that it can maximize the proxy by                                                          repair strategy yields superior zero-shot generaliza-
reasoning in natural language and emitting a mini-                                                         tion across distribution shifts. We further demon-
mal Prolog snippet – behavior that is rewarded just                                                        strate that GRPO training beats an SFT baseline
as much as genuine symbolic reasoning, despite                                                             and that a 3B model with agentic inference can
defeating the purpose of using Prolog in the first                                                         match 7B baselines on MMLU, indicating that sym-
place. Reward suites 2 and 3 attempt to close this                                                         bolic tool use can partially compensate for scale.
gap by adding structural and semantic signals that                                                            Most importantly, our results expose an
more directly specify the intended behavior, and                                                           accuracy–auditability trade-off:        correctness-
they do induce more symbolic programs – but at a                                                           optimized configurations delegate reasoning to
cost in accuracy, likely because the richer reward                                                         natural language and use Prolog only for the
landscape is harder to optimize jointly. Reward                                                            final computation, while structure-rewarded
hacking of this kind has recently been linked to                                                           configurations produce fully symbolic programs
emergent misalignment (Betley et al., 2026; Mac-                                                           that are less accurate. Symbolic grounding alone
Diarmid et al., 2025).                                                                                     does not deliver auditability and the reward design
                                                                                                           must take it into account. Practitioners deploying
Inference Protocol Selection Execution-based                                                               such systems in safety-critical domains should treat
rewards combined with multiple-try inference pro-                                                          the choice of reward composition and inference
duce the best in-distribution accuracy: Reward                                                             protocol as a deliberate position on this trade-off.
8   Limitations                                          Eli Bingham, Jonathan P. Chen, Martin Jankowiak, Fritz
                                                            Obermeyer, Neeraj Pradhan, Theofanis Karaletsos,
This work is limited to elementary arithmetic               Rohit Singh, Paul A. Szerlip, Paul Horsfall, and
reasoning problems (GSM8K), using a single                  Noah D. Goodman. 2019. Pyro: Deep universal
                                                            probabilistic programming. J. Mach. Learn. Res.,
tool (SWI-Prolog), and one reinforcement method
                                                            20:28:1–28:6.
(GRPO). Generalization to richer domains, such as
probabilistic programming (Bingham et al., 2019),        Nasim Borazjanizadeh and Steven Piantadosi. 2024. Re-
remains unexplored, as does integrating multiple           liable reasoning beyond natural language. Preprint,
                                                           arXiv:2407.11373.
tools. Lastly, reward shaping currently follows a
fixed curriculum; future work may benefit from           Tianzhe Chu, Yuexiang Zhai, Jihan Yang, Shengbang
dynamic reward schedules based on validation met-          Tong, Saining Xie, Dale Schuurmans, Quoc V. Le,
                                                           Sergey Levine, and Yi Ma. 2025. SFT memorizes,
rics. Our MMLU evaluation primarily tests the              RL generalizes: A comparative study of foundation
model’s ability to emit well-formed Prolog for en-         model post-training. In ICML, Proceedings of Ma-
coding answer indices.                                     chine Learning Research. PMLR / OpenReview.net.
                                                         Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song,
9   Ethical Considerations                                 Peiyi Wang, Qihao Zhu, Runxin Xu, Ruoyu Zhang,
                                                           Shirong Ma, Xiao Bi, Xiaokang Zhang, Xingkai
Compared to chain-of-thought approaches, our ap-           Yu, Yu Wu, Z. F. Wu, Zhibin Gou, Zhihong Shao,
proach of relying on a symbolic reasoning engine           Zhuoshu Li, Ziyi Gao, Aixin Liu, and 175 oth-
is intended to improve auditability of a language          ers. 2025. Deepseek-R1 incentivizes reasoning
model’s reasoning process. We do not expect that           in LLMs through reinforcement learning. Nat.,
                                                           645(8081):633–638.
our method introduces or exacerbates any risks.
The only caveat here is that, under our basic re-        Dan Hendrycks, Collin Burns, Steven Basart, Andy Zou,
ward suite 1, the system may circumvent reason-            Mantas Mazeika, Dawn Song, and Jacob Steinhardt.
ing via Prolog – as discussed extensively in the           2021. Measuring massive multitask language under-
                                                           standing. In ICLR. OpenReview.net.
Discussion. However, this lack-of-faithfulness con-
cern equally applies to natural-language reasoning       Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan
traces, and one of our contributions lies in identify-     Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and
                                                           Weizhu Chen. 2022. LoRA: Low-rank adaptation of
ing an accuracy–auditability trade-off in neurosym-        large language models. In ICLR. OpenReview.net.
bolic reasoning systems.
                                                         Tomek Korbak, Mikita Balesni, Elizabeth Barnes,
Acknowledgments                                            Yoshua Bengio, Joe Benton, Joseph Bloom, Mark
                                                           Chen, Alan Cooney, Allan Dafoe, Anca Dragan,
This research was supported in part by the MIST            Scott Emmons, Owain Evans, David Farhi, Ryan
                                                           Greenblatt, Dan Hendrycks, Marius Hobbhahn, Evan
project, funded by the Novo Nordisk foundation             Hubinger, Geoffrey Irving, Erik Jenner, and 22 oth-
under grant reference number NNF25OC0103204.               ers. 2025. Chain of thought monitorability: A new
The research was further supported in part by the          and fragile opportunity for AI safety. Preprint,
Danish Foundation Models project, funded by the            arXiv:2507.11473.
Danish government. Part of the computation done          Tamera Lanham, Anna Chen, Ansh Radhakrishnan,
for this project was performed on the UCloud in-           Benoit Steiner, Carson Denison, Danny Hernan-
teractive HPC system managed by the eScience               dez, Dustin Li, Esin Durmus, Evan Hubinger, Jack-
Center at the University of Southern Denmark.              son Kernion, and 1 others. 2023. Measuring faith-
                                                           fulness in chain-of-thought reasoning. Preprint,
                                                           arXiv:2307.13702.

References                                               Monte MacDiarmid, Benjamin Wright, Jonathan Ue-
                                                          sato, Joe Benton, Jonathan Kutasov, Sara Price, Naia
Samy Bengio, Oriol Vinyals, Navdeep Jaitly, and Noam      Bouscal, Samuel R. Bowman, Trenton Bricken, Alex
  Shazeer. 2015. Scheduled sampling for sequence pre-     Cloud, Carson Denison, Johannes Gasteiger, Ryan
  diction with recurrent neural networks. In NeurIPS,     Greenblatt, Jan Leike, Jack Lindsey, Vladimir Miku-
  pages 1171–1179.                                        lik, Ethan Perez, Alex Rodrigues, Drake Thomas,
                                                          and 3 others. 2025. Natural emergent misalignment
Jan Betley, Niels Warncke, Anna Sztyber-Betley, Daniel    from reward hacking in production RL. Preprint,
   Tan, Xuchan Bao, Martín Soto, Megha Srivastava,        arXiv:2511.18397.
   Nathan Labenz, and Owain Evans. 2026. Training
   large language models on narrow tasks can lead to     Niklas Muennighoff, Zitong Yang, Weijia Shi, Xi-
   broad misalignment. Nat., 649(8097):584–589.            ang Lisa Li, Li Fei-Fei, Hannaneh Hajishirzi, Luke
  Zettlemoyer, Percy Liang, Emmanuel Candès, and         An Yang, Baosong Yang, Beichen Zhang, Binyuan Hui,
  Tatsunori Hashimoto. 2025. s1: Simple test-time          Bo Zheng, Bowen Yu, Chengyuan Li, Dayiheng Liu,
  scaling. In EMNLP, pages 20275–20321.                    Fei Huang, Haoran Wei, Huan Lin, Jian Yang, Jian-
                                                           hong Tu, Jianwei Zhang, Jianxin Yang, Jiaxi Yang,
OpenAI. 2024. OpenAI o1 system card. Preprint,             Jingren Zhou, Junyang Lin, Kai Dang, and 22 oth-
  arXiv:2412.16720.                                        ers. 2024a. Qwen2.5 technical report. Preprint,
                                                           arXiv:2412.15115.
Razvan Pascanu, Tomás Mikolov, and Yoshua Bengio.
  2013. On the difficulty of training recurrent neural   Xiaocheng Yang, Bingsen Chen, and Yik-Cheung Tam.
  networks. In ICML, pages 1310–1318. JMLR.org.            2024b. Arithmetic reasoning with LLM: Prolog gen-
                                                           eration & permutation. In Proceedings of the 2024
Debjit Paul, Robert West, Antoine Bosselut, and Boi        Conference of the North American Chapter of the
  Faltings. 2024. Making reasoning matter: Measur-         Association for Computational Linguistics: Human
  ing and improving faithfulness of chain-of-thought       Language Technologies (Volume 2: Short Papers),
  reasoning. In EMNLP Findings, pages 15012–15032.         pages 699–710.

Federico Pennino, Bianca Raimondi, Massimo Rondelli,     Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak
  Andrea Gurioli, and Maurizio Gabbrielli. 2025. From      Shafran, Karthik Narasimhan, and Yuan Cao. 2023.
  reasoning to code: GRPO optimization for underrep-       ReAct: Synergizing reasoning and acting in language
  resented languages. Preprint, arXiv:2506.11027.          models. In ICLR. OpenReview.net.

Timo Schick, Jane Dwivedi-Yu, Roberto Dessì, Roberta     Appendix
  Raileanu, Maria Lomeli, Eric Hambro, Luke Zettle-
  moyer, Nicola Cancedda, and Thomas Scialom. 2023.      A   System Prompts in Detail
  Toolformer: Language models can teach themselves
  to use tools. In NeurIPS.                              SP Base: Minimal Prompt for Symbolic Ground-
                                                         ing The SP Base system prompt establishes
Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu,          a minimal yet effective template for aligning
  Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan         LLMs with symbolic execution engines like Pro-
  Zhang, Yongan Li, Yantao Wu, and Daya Guo. 2024.
  DeepSeekMath: Pushing the limits of mathemati-         log. It defines a fixed two-part XML schema: a
  cal reasoning in open language models. Preprint,       <reasoning> section for short, structured step-
  arXiv:2402.03300.                                      by-step logic, and an <answer> section that
                                                         emits Prolog code with a single constraint-solving
Joar Skalse, Nikolaus H. R. Howe, Dmitrii Krashenin-
                                                         clause (solve(X)). The Prolog code always in-
  nikov, and David Krueger. 2022. Defining and char-
  acterizing reward gaming. In NeurIPS.                  cludes :- use_module(library(clpq))., ensur-
                                                         ing compatibility with constraint logic program-
Charlie Victor Snell, Jaehoon Lee, Kelvin Xu, and Avi-   ming (CLP(Q)). SP Base is also consistent with
  ral Kumar. 2025. Scaling LLM test-time compute         Tan et al. (2024), who demonstrate that lightweight
  optimally can be more effective than scaling parame-
  ters for reasoning. In ICLR. OpenReview.net.           Prolog-based prompts form an effective baseline
                                                         for CoT-based arithmetic reasoning, when paired
Xiaoyu Tan, Yongxin Deng, Xihe Qiu, Weidi Xu, Chao       with strict symbolic evaluation.
  Qu, Wei Chu, Yinghui Xu, and Yuan Qi. 2024.
  Thought-Like-Pro: Enhancing reasoning of large              You are a Prolog assistant specialized
  language models through self-driven Prolog-based            in solving math problems.
  chain-of-thought. Preprint, arXiv:2407.14562.
                                                              Provide your solution       strictly    in
                                                              this XML format:
Yubo Wang, Xueguang Ma, Ge Zhang, Yuansheng Ni,
  Abhranil Chandra, Shiguang Guo, Weiming Ren,               <reasoning>
  Aaran Arulraj, Xuan He, Ziyan Jiang, and 1 others.         - Give concise step-by-step reasoning
  2024. MMLU-Pro: A more robust and challenging               here.
  multi-task language understanding benchmark. In            </reasoning>
  NeurIPS, pages 95266–95290.                                <answer>
                                                              :- use_module(library(clpq)).
Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten
   Bosma, Fei Xia, Ed Chi, Quoc V Le, and Denny              solve(X) :-
                                                             {X = final numeric answer}.
   Zhou. 2022. Chain-of-thought prompting elicits rea-
                                                             </answer>
   soning in large language models. In NeurIPS, pages
   24824–24837.
                                                         SP Struct: Structured Output with Explicit
Will Brown. 2025. grpo_demo.py. GitHub Gist. Last        Code Layout The SP Struct prompt incentivizes
  accessed: April 18, 2026.                              alignment with symbolic programming language
by enforcing a fixed internal structure within each    You    are   a    specialized  Prolog
output section. The <reasoning> block guides the       code-generating assistant that must
                                                       follow a strict structured format to
model to decompose the task into ordered, num-         solve math problems.
bered logical steps. The <answer> block is explic-
itly formatted: code must start with the CLP(Q)        Your task is to solve math problems
                                                       by providing an answer in two clearly
import, define constants or intermediate predicates    defined sections:
(if needed), and conclude with a solve/1 clause
                                                       1. <reasoning>
written entirely using curly-brace constraints. This   - Provide a clear, concise, step-by-step
prompt incentivizes breaking complex tasks into         explanation of your solution.
simpler subtasks and building modular prompts          - Explain how each numeric constant
                                                        from the problem is represented by a
that produce more predictable structured outputs.       predicate.
                                                       - Do not include unnecessary calculations
     You    are   a    specialized      Prolog
                                                        using    literal    numbers;     instead,
     code-generating assistant.
                                                        reference the predicates you define.
     Your task is to solve math problems by
                                                        2. <answer>
     providing a structured answer in two
                                                       - Provide executable Prolog code using
     clearly defined sections:
                                                        constraint logic programming (CLP) to
                                                        compute the numeric answer.
    1. <reasoning>
                                                       -     Always    start    with:       ’:-
    - Provide a clear, concise step-by-step
                                                        use_module(library(clpq)).’
    explanation of how you arrive at the
                                                       - For every numeric constant mentioned
    solution.
                                                        in the problem, define a predicate with
                                                        a descriptive name.
    2. <answer>
                                                        For example, if the problem states that
    - Provide executable Prolog code using
                                                       James carries 10 bags per trip, include:
    constraint logic programming to compute
                                                        bags_per_trip(james, 10).
    the numeric answer.
                                                        Similarly, define predicates for other
    -    Always     start    with:        ’:-
                                                        constants (e.g., trips_per_day(james,
    use_module(library(clpq)).’
                                                        20). days(5).)
    - Define any necessary numeric constants
                                                       - In the solve predicate, retrieve each
    or intermediate values using predicates.
                                                       value by querying its predicate and
    - Final answer should be unified
                                                        use these values in your arithmetic
    explicitly in solve(X) using curly-brace
                                                        constraints.
    constraints, without printing commands.
                                                       - Use curly-brace constraints (e.g.,
                                                       {Total = Bags * Trips * Days}) to
     Use this XML format strictly:
                                                        compute the final answer.
     <reasoning>
                                                       - The final answer must be explicitly
     (Your step-by-step reasoning here)
                                                        unified in the solve predicate (e.g.,
     </reasoning>
                                                        solve(Total_bags) :- ...).
     <answer>
     :- use_module(library(clpq)).
                                                       Ensure your answer strictly follows
                                                       this XML format:
     (Any    predicates/constants      defined
                                                       <reasoning>
     here)
                                                       Your detailed, step-by-step reasoning
                                                       here, with references to the predicates
    solve(X) :-
                                                       defined for numeric constants.
    (Intermediate computations using curly
                                                       </reasoning>
    braces)
                                                       <answer>
    {X = final constraint logic}.
                                                       :- use_module(library(clpq)).
    </answer>
                                                       Define numeric constants as predicates:
SP Declare: Declarative Abstraction and                bags_per_trip(james, 10).
Predicate-Level Alignment Inspired by prior            trips_per_day(james, 20).
                                                       days(5).
work, where reasoning traces are translated into
predicates (Tan et al., 2024), the third system        solve(Total_bags) :-
prompt, SP Declare, requires the model to en-          bags_per_trip(james, Bags),
                                                       trips_per_day(james, Trips),
code every numeric constant mentioned in the           days(Days),
problem statement as a named predicate (e.g.,          {Total_bags = Bags * Trips * Days}.
bags_per_trip(james, 10).). These constants            </answer>
must be queried and referenced symbolically in-        Do not shortcut the process by
side the final solve/1 clause, and never embedded      embedding direct numeric literals in
directly as literals.                                  the solve predicate.
     Every numeric constant must be defined            B     Reward Suites in Detail
     via a predicate and then referenced in
     the arithmetic computations.

                                                       Here, we describe the three developed reward suites
SP Reflect: Reflexive Reasoning and Self-              in detail. Each consecutive suite reward builds on
Correction The SP Reflect prompt extends SP            top of the previous reward suite.
Struct by adding a built-in meta-cognitive loop. Af-
ter the model completes its initial <reasoning>, it
reviews its own logic to check for potential flaws.
                                                       B.1    Details of Reward Suite 1: Structural
If issues are found, it should retry the reasoning
                                                              Execution Shaping
step and only then emit the final Prolog code in
<answer>. This embedded “reflection” mechanism
enables error-checking and self-correction.            In developing our first reward-shaping scheme, we
                                                       build directly on the GRPO reward functions from
                                                       Will Brown (2025), using them as a baseline to cre-
     You    are   a    specialized      Prolog
     code-generating assistant.                        ate a suite that nudges the model toward generating
                                                       correct, executable Prolog code. The components
     Your task is to solve math problems by            of Reward Suite 1 are described below. Figure 3
     providing a structured answer in two
     clearly defined sections:                         shows the progression of the correctness reward
                                                       over training steps.
    1. <reasoning>
    - Provide a clear, concise step-by-step               Correctness Reward: We extract the model’s
    explanation of how you arrive at the
    solution.                                          <answer>...</answer> block, execute it using
    - Review the reasoning at the end of the           SWI-Prolog, and compare the numeric output to
    <reasoning> section to ensure that all             the ground truth. Exact matches receive a score of
    computations and logical deductions are
    correct.                                           2.0; incorrect but numeric outputs earn 1.0; and any
    - If something is not correct, then                executable attempt, even with unbound variables
    try again: Provide a clear, concise
    step-by-step explanation of how you
                                                       or failures, earns 0.5.
    arrive at the solution.
                                                          Prolog Syntax Reward: Inspired by neurosym-
    2. <answer>                                        bolic scaffolding (Borazjanizadeh and Piantadosi,
    - Provide executable Prolog code using             2024), we award 0.2 points (up to 1.0) for detect-
    constraint logic programming to compute
    the numeric answer.                                ing hallmark Prolog constructs: directives like :-
    -    Always     start    with:        ’:-          use_module, the solve/1 clause, and clause termi-
    use_module(library(clpq)).’
    - Define any necessary numeric constants
                                                       nators (.). This rewards syntactic validity without
    or intermediate values using predicates.           a strict all-or-nothing reward.
    - Final answer should be unified
    explicitly in solve(X) using curly-brace              Soft- and Strict-Format Rewards We provide
    constraints, without printing commands.
                                                       both soft and strict format incentives. The soft for-
    Use this XML format strictly:                      mat reward assigns 0.5 points if the output contains
    <reasoning>                                        both a <reasoning>...</reasoning> block and
    - Your step-by-step reasoning here
    - Your review of the reasoning here
                                                       a subsequent <answer>...</answer> block. The
    - Your potential further step-by-step              strict format reward grants an additional 0.5 only
    reasoning here                                     when the entire completion exactly matches a line-
    </reasoning>
    <answer>                                           by-line XML regular expression.
    :- use_module(library(clpq)).
                                                          XML-Count Heuristic: To support fine-
     (Any    predicates/constants      defined         grained compliance, we add a continuous schema-
     here)
                                                       adherence score: each correctly placed XML
    solve(X) :-                                        tag (<reasoning>, </reasoning>, <answer>,
    (Intermediate computations using curly             </answer>) contributes 0.125, with a small per-
    braces)
    {X = final constraint logic}.                      character penalty applied to trailing text after
    </answer>                                          </answer>.
Figure 3: Correctness reward progression during train-
ing across different system prompts under Reward Suite
1. By isolating the execution-based signal, we see that
SP-Base, SP-Struct, and SP-Reflect reach the highest
correctness reward levels. This indicates that mini-
mal scaffolding plus executable output dominate perfor-
mance on downstream tasks.



                                                           Figure 4: (Top): Semantic similarity reward across dif-
                                                           ferent prompt variants under Reward Suite 2. (Bottom):
                                                           Correctness reward progression during training across
B.2   Details of Reward Suite 2: Semantic                  different system prompts under Reward Suite 2.
      Similarity
                                                              Figure 4 reveals clear trends in semantic align-
                                                           ment across prompt variants. The sp-declare
Having ensured that outputs are executable and             prompt consistently achieves the highest average
conform to the XML schema, we now introduce a              semantic similarity, indicating that its predicate-
reward that promotes code which corresponds to             level abstraction leads to closer alignment with
the reference code even when surface forms differ.         reference Prolog programs. Other prompts such as
In addition to the components of reward suite 1, we        sp-struct and sp-base converge to moderately
additionally employ semantic similarity.                   high similarity, while sp-reflect underperforms.
                                                           This confirms that Reward Suite 2’s embedding-
                                                           based feedback meaningfully shapes model behav-
   The semantic similarity score Ssem ∈ [0, 1]
                                                           ior toward semantically aligned and structurally
combines two complementary signals. First, we
                                                           consistent code.
extract the contents of the <answer>-block from
both the model output and the ground-truth data.           B.3   Details of Reward Suite 3:
Each code snippet is then embedded using the                     Curriculum-Guided Structural
Sentence-BERT model all-MiniLM-L6-v2, and                        Optimization
cosine similarity is computed between the result-
                                                           Our third reward suite builds on top of the semantic
ing vectors, yielding cos ∈ [0, 1]. In parallel,
                                                           similarity and format shaping of Reward Suite 2
we calculate predicate-name overlap by identify-
                                                           by adding Prolog-structure-sensitive rewards and
ing all functors of the form name( using a reg-
                                                           a curriculum-driven schedule that gradually shifts
ular expression. Let Pmodel and Pref denote the
                                                           the model from broad exploration toward focused
sets of predicate names extracted from the model
                                                           exploitation as training progresses.
and reference programs, respectively. The nor-
                                  |Pmodel ∩Pref |
malized intersection is: pred = max(1,|P    ref |)
                                                   . The   Prolog Structure Reward Each reference Pro-
final semantic similarity score is the average of          log code:
these two signals: Ssem = 21 (cos + pred) ∈ [0, 1].        1. Loads      arithmetic     constraints      with
If either code block is missing or empty, we as-              :- use_module(library(clpq)).;
sign Ssem = 0. To align with the other reward              2. States problem facts as one-line clauses; and
                               score to [0.5, 2.0]:
scales, we rescale the semantic                            3. Defines exactly one public predicate, solve/1,
reward = max 0.5, 2 × Ssem .                                  whose single argument is the final result.
A typical example:                                      Curriculum-Based Weight Scheduling Instead
: - use_module ( library ( clpq )).                     of using a static mix of sub-rewards, we dynami-
                                                        cally adjust weight allocations based on training
sell_clips ( natalia , april , 48).
                                                        progress t ∈ [0, 1]—defined as the fraction of
solve ( Total ) :-                                      prompts seen—via a logistic function:
    sell_clips ( natalia , april , April ),
    { May      = April / 2 },
    { Total = April + May }.
                                                                            1
                                                            σ(t) =                    ,    k = 12, τ = 0.5.
                                                                     1 + e−k (t−τ )
prolog_helpers.pl. The    helper  script
prolog_helpers.pl analyzes any candidate                This sigmoid-shaped trajectory has proven effective
program and prints:                                     in curriculum learning (Bengio et al., 2015).
 PREDICATE_COUNT — user predicates other than           Multi-Objective Balancing We let early[k] and
                  solve                                 late[k] be the weight for sub-reward k at the be-
  CONSTRAINT_COUNT — goals inside { ... }               ginning and end of training, respectively. We in-
$ swipl -q -f prolog_helpers . pl \
  -g " analyze_code (' prog .pl ',P ,C), halt ."        terpolate between them using the same sigmoid
PREDICATE_COUNT : 1                                     σ(t):
CONSTRAINT_COUNT : 2
                                                                                                
  A program is marked structurally valid                weights[k] = early[k] + late[k]−early[k] ×σ(t).
whenever PREDICATE_COUNT           ≥      1 and
CONSTRAINT_COUNT ≥ 1.
  We convert the same counts into a scalar reward             Reward            Early Weight   Late Weight
S ∈ [0, 2]:
                                                              Semantic              0.35          0.10
  sp = min(0.25 × PREDICATE_COUNT, 0.75)                      XML Format            0.25          0.10
                                                              Syntax                0.10          0.10
  sc = min(0.30 × CONSTRAINT_COUNT, 0.90)                     Correctness           0.15          0.45
                                                              Structure             0.15          0.25
Sraw = sp + sc
Hard-coding penalty. If solve/1 contains a lit-         Table 7: Early and late-stage reward weights used for
eral numeric assignment—detected via the pattern:       curriculum interpolation in Reward Suite 3. These de-
        solve(...) :- ... = <number>. or                fine the endpoints of the training schedule, with se-
        solve(...) :- { ... = <number> }.               mantic and formatting objectives emphasized early, and
                                                        correctness and structural reasoning prioritized late.
then the score is scaled by 0.2:
                 S = 0.2 × Sraw .
                                                          While Table 7 defines the curriculum endpoints,
  Otherwise, S = Sraw . The final value                 Figure 5 shows how weights evolve over time under
is clipped to [0, 2] and returned as the                our sigmoid interpolation, confirming the gradual
prolog_structure_reward.                                shift in learning priorities.
Rationale and percentage mapping. Each aux-
iliary predicate adds 0.25 up to a cap of 0.75 (three
helpful helpers), and each arithmetic constraint
adds 0.30 up to 0.90 (three useful constraints). Be-
yond these caps, further clauses no longer raise the
reward, preventing inflation through repetition. The
maximum attainable Sraw = 0.75 + 0.90 = 1.65 is
linearly mapped to a 0–100 % structural score:
                                 
                                S
          Struct% = min 1, 1.65      × 100.
                                                        Figure 5: Interpolated reward weights over training
A program that reaches the caps and avoids hard-        steps, driven by the sigmoid progression schedule. Each
coding therefore receives 100% structural credit,       curve shows how a specific sub-reward (e.g., structure,
whereas a hard-coded answer is immediately re-          correctness) increases or decreases in emphasis as train-
duced to 20 % of the score it would otherwise earn.     ing progresses.
Reward Normalization and Clipping To avoid                  C.2    Agentic Internal Context Feedback
dominance effects due to scale mismatches across                  The code failed to produce a numeric
reward components, we normalize and clip all sub-                 result.
                                                                  Let’s fix it:
rewards into a shared range. This prevents the                    1. Reflect on what went wrong.
“winner-takes-all” dynamic.                                       2. Recalculate
                                                                  3. Adjust your answer to:
Final Aggregation For each example, we nor-                       <answer>
malize and weight the five signals—Semantic,                      :- use_module(library(clpq)).
                                                                  solve(X) :-
Correctness, Structure, Syntax, and For-                          {X = final_number}.
mat—then sum the weighted values and scale the                    </answer>
                                                                  ...
result into [0, 2]:
                                  5
                                  X                         D     Inference Examples
         final_reward = 2.0 ×           wk · r k
                                  k=1
                                                            D.1    SP-Struct-RWD1 Example
                                                                  <reasoning>
This final scaling preserves the [0, 2] reward range              To determine how many more cakes Louise
established in Suite 1 (where a perfect program                   needs to bake, we can break down the
                                                                  problem step by step.
earned 2.0), maintains compatibility with GRPO’s
learning rate and gradient magnitudes, and ensures                1. Louise needs a total of 60 cakes.
comparability across all three reward suites.                     2. She has already baked half of 60
   Over time, this curriculum drives the model from               cakes, which is 30 cakes.
                                                                  3. She has 60 - 30 = 30 cakes left to
early-format scaffolding toward producing concise,                bake.
logically rich, and syntactically robust Prolog code.             4.    Today, she bakes half of the
                                                                  remaining 30 cakes, which is 30 / 2 =
                                                                  15 cakes.
                                                                  5. After baking 15 cakes, she has 30 -
                                                                  15 = 15 cakes left to bake.
                                                                  6. The next day, she bakes a third of
                                                                  the remaining 15 cakes, which is 15 / 3
                                                                  = 5 cakes.
                                                                  7. After baking 5 cakes, she has 15 - 5
                                                                  = 10 cakes left to bake.

                                                                  Therefore, Louise needs to bake 10 more
                                                                  cakes.
                                                                  </reasoning>
Figure 6: Prolog structure reward progression for each            <answer>
                                                                  :- use_module(library(clpq)).
prompt variant in Reward Suite 3. As scheduled weights
shift toward structural fidelity, models like sp-declare
and sp-struct learn to emit programs with diverse                 solve(C) :-
                                                                  C = 10.
predicates and logically well-formed constraint blocks.           </answer>
sp-base exhibits a delayed but eventual increase, fol-
lowing the sigmoid schedule’s shift from format to struc-   D.2    SP-Declare-RWD1 Example
ture.
                                                                  <reasoning>
                                                                  - Walter works 5 days a week in a
  Figure 6 shows how structural competence                         fast-food chain and earns $5 per hour.
emerges as a function of the curriculum weights.                  - He works 4 hours a day, so his daily
                                                                   earning is 4 * $5 = $20.
                                                                  - He works 5 days a week, so his weekly
C     Agentic Prompts                                              earning is 5 * $20 = $100.
                                                                  - Walter allocates 3/4 of his weekly
C.1    System Prompt for Agentic Internal and                      earning for his schooling.
       Agentic Independent                                        - We need to find 3/4 of $100.
                                                                  </reasoning>
      You have one tool:
                                                                  <answer>
      <tools>
                                                                   :- use_module(library(clpq)).
      {"name":    "run_prolog", "arguments":
      [{"code": "string"}]}
      </tools>                                                    working_days(Walter, 5).
      - Use the "run_prolog" tool to execute                      hours_per_day(Walter, 4).
      your answer in the <answer> section.                        hourly_wage(Walter, 5).
      schooling_fraction(Walter, 3/4).                  The code failed to produce a numeric
                                                        result.
      solve(School_allocation) :-
      working_days(Walter, Days),                       Let’s fix it:
      hours_per_day(Walter, Hours),
      hourly_wage(Walter, Wage),                        1. Reflect on what went wrong.
      schooling_fraction(Walter, Fraction),             2. Recalculate
      {School_allocation = Fraction * (Days *           3. Adjust your answer to:
      Hours * Wage)}.                                   <answer>
      </answer>                                         :- use_module(library(clpq)).

                                                        solve(X) :-
D.3    SP-Struct-RWD1-Agentic-Internal                  {X = final_number}.
       Example                                          </answer>
      — TURN 1 —
      (USER) <reasoning>                                <tool_call>{
      To find out how many bunnies Michael has,         "name": "run_prolog",
      we can first calculate the number of              "arguments": {
      dogs and cats he has, and then subtract           "code":                             ":-
      that total from the total number of pets.         use_module(library(clpq)).\n\nsolve(X)
                                                        :- {X = final_number}."
      1.    Calculate the number of dogs:               }
      25% of 36 pets.                                   }
      2. Calculate the number of cats: 50% of
      36 pets.                                          [TOKENS:post-feedback] used=731 (38.7%)
      3. Subtract the sum of dogs and cats              | rem=1159 | budget=1890
      from the total number of pets to find             [TOKENS:pre-gen] used=731 (38.7%) |
      the number of bunnies.                            rem=1159 | budget=1890

      Let’s denote the total number of                  — TURN 2 —
      pets as 36. The number of dogs is 0.25
      * 36, and the number of cats is 0.50 *            (ASSISTANT) <reasoning>
      36. The number of bunnies is then 36 -            The previous code had a logical error in
      (0.25 * 36 + 0.50 * 36).                          the definition of the helper predicates.
                                                        The helper predicates should directly
      <answer>                                          compute the number of dogs, cats, and
      :- use_module(library(clpq)).                     bunnies without needing to be called
                                                        separately. We can simplify the process
      number_of_dogs(Pets, Dogs) :-                     by directly calculating the number of
      Dogs is 0.25 * Pets.                              dogs and cats and then subtracting from
                                                        the total number of pets to find the
      number_of_cats(Pets, Cats) :-                     number of bunnies.
      Cats is 0.50 * Pets.
                                                        1.    Calculate the number of dogs:
      number_of_bunnies(Pets,   Dogs,    Cats,          25% of 36 pets.
      Bunnies) :-                                       2. Calculate the number of cats: 50% of
      Bunnies is Pets - (Dogs + Cats).                  36 pets.
                                                        3. Subtract the sum of dogs and cats
      number_of_bunnies(36,     Dogs,    Cats,          from the total number of pets to find
      Bunnies) :-                                       the number of bunnies.
      number_of_dogs(36, Dogs),
      number_of_cats(36, Cats),                         Let’s directly compute the       number
      number_of_bunnies(36,     Dogs,    Cats,          of bunnies as a single step.
      Bunnies).
                                                        <answer>
      solve(X) :-                                       :- use_module(library(clpq)).
      number_of_bunnies(36,     Dogs,    Cats,
      Bunnies),                                         solve(X) :-
      {X = Bunnies}.                                    {X = 36 - (0.25 * 36 + 0.50 * 36)}.
      </answer>                                         </answer>

      [TOKENS:post-gen]    used=622    (32.9%)          [TOKENS:post-gen]    used=926    (49.0%)
      | rem=1268 | budget=1890                          | rem=964 | budget=1890
      »> WARNING: Potential infinite recursion          »> run_prolog→ 9
      detected in Prolog code
      »> run_prolog→ None                         D.4    SP-Struct-RWD1 Agentic-Independent
      [TOKENS:pre-feedback] used=622 (32.9%)
      | rem=1268 | budget=1890
                                                         Example
                                                        QUESTION 54: Please generate a piece
      »> FEEDBACK INJECTED:                             of Prolog code to solve the given math
problem.                                    1.     Reflect briefly on what     went
Jenny wants to know whether bone meal or    wrong.
cow manure makes better fertilizer. The     2. Recalculate
control plant with no fertilizer grows      3. Adjust your answer to:
36 inches high, the plant with bone         <answer>
meal grows to 125% of the height of the     :- use_module(library(clpq)).
control plant, and the cow manure plant
grows to 200% of the height of the bone     solve(X) :-
meal plant. How tall is the cow manure      {X = final_number}.
plant in inches?                            </answer>

»> INDEPENDENT AGENTIC_TRY #1               <tool_call>{
[TOKENS:pre-gen] used=332 (17.6%)       |   "name": "run_prolog",
rem=1558 | budget=1890                      "arguments": {
                                            "code":                             ":-
— TURN: 1/20 —                              use_module(library(clpq)).\n\nsolve(X)
(Assume the height of the plant with        :- {X = final_number}."
bone meal is 125% of 36 inches, and the     }
height of the cow manure plant is 200%      }
of the height of the bone meal plant.)
(USER) <reasoning>                          [TOKENS:post-feedback] used=763 (40.4%)
To determine the height of the cow          | rem=1127 | budget=1890
manure plant, we need to follow these       [TOKENS:pre-gen] used=763 (40.4%) |
steps:                                      rem=1127 | budget=1890

1.     Calculate the height of the          — TURN: 2/20 —
plant with bone meal, which is 125% of
the height of the control plant.            (ASSISTANT) <reasoning>
2. Calculate the height of the cow          Upon reviewing the previous code,
manure plant, which is 200% of the          it appears that the issue might
height of the bone meal plant.              be related to the way the height
                                            of the bone meal plant and the cow
The height of      the   control   plant    manure plant are calculated and unified.
is 36 inches.
                                            1.      Calculate the height of the
1.    Height of the bone meal plant          bone meal plant:
= 125% of 36 inches = 1.25 * 36 inches.     - Height of the bone meal plant = 1.25 *
2. Height of the cow manure plant = 200%     36 inches.
of the height of the bone meal plant =
2.00 * (1.25 * 36 inches).                   2.     Calculate the height of the
</reasoning>                                 cow manure plant:
<answer>                                    - Height of the cow manure plant = 2.00
:- use_module(library(clpq)).               * (1.25 * 36 inches).

height_control_plant(36).                   To ensure the final height is correctly
                                            computed and unified, we need to
height_bone_meal(B) :-                      make sure the intermediate steps are
B is 1.25 * height_control_plant(36).       correctly defined and the final height
                                            is directly computed and unified in one
height_cow_manure(C) :-                     step.
C is 2.00 * height_bone_meal(B).
                                            Let’s redefine the solve predicate
solve(C) :-                                 to directly compute the height of the
height_cow_manure(C).                       cow manure plant and unify it with the
</answer>                                   variable X.
                                            </reasoning>
[TOKENS:post-gen]    used=653    (34.6%)    <answer>
| rem=1237 | budget=1890                    :- use_module(library(clpq)).
»> WARNING: Potential infinite recursion
detected in Prolog code                     solve(X) :-
»> run_prolog→ None                         X = 2.00 * 1.25 * 36.
[TOKENS:pre-feedback] used=653 (34.6%)      </answer>
| rem=1237 | budget=1890
                                            [TOKENS:post-gen]    used=973  (51.5%)
»> FEEDBACK INJECTED:                       | rem=917 | budget=1890
The code failed to produce a numeric        »> run_prolog→ 2.0*1.25*36
result.                                     [TOKENS:pre-feedback] used=973 (51.5%)
                                            | rem=917 | budget=1890
Let’s fix it:
                                            »> FEEDBACK INJECTED:
The code failed to produce a numeric      context for a new independent try
result.                                   »> Total steps used: 3/20
                                          »> TRY RESULT → pred=None, steps=3, took
Let’s fix it:                             23.05s
                                          »> Bailed — no valid numeric answer;
1.     Reflect briefly on what     went   retrying with fresh context
wrong.
2. Recalculate                            »> INDEPENDENT AGENTIC_TRY #2
3. Adjust your answer to:                 [TOKENS:pre-gen] used=332 (17.6%)     |
<answer>                                  rem=1558 | budget=1890
:- use_module(library(clpq)).
                                          — TURN: 4/20 —
solve(X) :-                               (Assume all growth is in whole inches.)
{X = final_number}.                       (USER) <reasoning>
</answer>                                 To determine the height of the cow
                                          manure plant, we need to follow these
<tool_call>{                              steps:
"name": "run_prolog",
"arguments": {                            1.    The control plant grows to 36
"code":                             ":-   inches.
use_module(library(clpq)).\n\nsolve(X)    2. The bone meal plant grows to 125% of
:- {X = final_number}."                   the control plant’s height.
}                                         3. The cow manure plant grows to 200%
}                                         of the bone meal plant’s height.

[TOKENS:post-feedback]        used=1083   First, we calculate the height of
(57.3%) | rem=807 | budget=1890           the bone meal plant:
[TOKENS:pre-gen] used=1083 (57.3%) |      [Height of bone meal plant] = 36 × 1.25
rem=807 | budget=1890
                                          Next, we calculate the height of
— TURN: 3/20 —                            the cow manure plant:
                                          [Height of cow manure plant] = [Height
(ASSISTANT)                               of bone meal plant] × 2
(ASSISTANT) <reasoning>
Upon reviewing the previous code, it      Finally, we need to find the height of
appears that the issue might be related   the cow manure plant.
to the way the height of the cow manure   </reasoning>
plant is directly computed and unified.   <answer>
                                          :- use_module(library(clpq)).
The height of the cow manure plant
is 2.00 * (1.25 * 36 inches). We can      height_of_bone_meal_plant(Height)
simplify this to:                         :-
                                          Height is 36 * 1.25.
- Height of the bone meal plant =
1.25 * 36 inches.                         height_of_cow_manure_plant(CowManureHeight)
- Height of the cow manure plant = 2.00   :-
* (1.25 * 36 inches) = 2.00 * B, where    height_of_bone_meal_plant(BoneMealHeight),
B is the height of the bone meal plant.   CowManureHeight is BoneMealHeight * 2.

To directly compute and unify the         solve(CowManureHeight) :-
final height, we can simplify the         height_of_cow_manure_plant(CowManureHeight).
expression and directly compute the
final height in one step.                 CowManureHeight = CowManureHeight.
                                          </answer>
Let’s redefine the solve predicate
to directly compute the height of the     [TOKENS:post-gen]    used=619    (32.8%)
cow manure plant and unify it with the    | rem=1271 | budget=1890
variable X.                               »> WARNING: Potential infinite recursion
</reasoning>                              detected in Prolog code
<answer>                                  »> run_prolog→ 90.0
:- use_module(library(clpq)).             »> Total steps used: 4/20
                                          »> TRY RESULT → pred=’90.0’, steps=1,
solve(X) :-                               took 8.58s
X = 2.00 * 1.25 * 36.
</answer>                                 Q#54 | Pred: 90.0 | Gold: 90.0

[TOKENS:post-gen] used=1306 (69.1%) |
rem=584 | budget=1890
»> run_prolog→ 2.0*1.25*36
»> Aborting this attempt—resetting
E    System Prompt for SP-Struct                       We selected our search ranges based on estab-
     Zero-Shot MMLU Evaluation                      lished best practices and recent findings. First, the
                                                    learning rate is sampled log-uniformly between
 You are a specialized Prolog code-generating
 assistant.                                         5 × 10−6 and 1 × 10−4 . For LoRA capacity, we re-
 You have one tool:                                 strict the rank r to {32,64} and α to {64}, as gains
                                                    beyond r ≈ 64 diminish at the 3B-parameter scale
 <tools>
 {"name":"run_prolog",                              (Hu et al., 2022). We use per-device batch sizes of
 "arguments":[{"code":"string"}]}                   8 or 16 to balance throughput against gradient sta-
 </tools>
                                                    bility. The number of rollouts (num_generations)
 Your task is to choose the correct option index    is set to either 4 or 8, since additional generations
 for a multiple-choice question, and present        reduce policy-gradient variance (Snell et al., 2025).
 your work in two clearly defined sections:
                                                    Gradient clipping (max_grad_norm) is drawn uni-
1. <reasoning>                                      formly from [0.1,1.0] to prevent exploding gradi-
- Provide a clear, concise step-by-step             ents (Pascanu et al., 2013), and weight decay is
 explanation of how you determine which option
 is correct.                                        chosen from {0.01,0.1,0.2}.
- Refer to the correct option by its zero-based
 index.

 2. <answer>
- Provide executable Prolog code using
 constraint logic programming to compute the
 index of the correct choice.
-      Always      start      with:          ’:-
 use_module(library(clpq)).’
- Final answer should be unified in solve(X)
 using a single curly-brace constraint that sets
X to the chosen index.

 Use this XML format strictly:
 <reasoning>
 (Your step-by-step reasoning here)                 Figure 7: Parallel coordinates plot of 12 hyperparameter
 </reasoning>                                       trials from Bayesian optimization. Each line represents
 <answer>                                           one sweep, colored by validation correctness reward
 :- use_module(library(clpq)).                      (eval/rewards/correctness_reward_func).
 solve(X) :-
 {X = correct_index}.
 </answer>

- Use the "run_prolog" tool to          execute
 your answer in the <answer> section.


F    Hyperparameter Tuning
                                                      The best configuration found, denoted
Because sp-struct-rwd1 achieved the highest         sp-struct-rwd1-hyper (section F), was then
validation accuracy among our tested variants,      evaluated on the gsm8k-prolog-prover test split.
we ran Bayesian hyper-parameter optimisation to     Table 8 compares its accuracy to our original
see whether it could be pushed further on the       sp-struct-rwd1 model:
GSM8K-Prolog-Prover task.
   Using a Weights & Biases sweep with
"method": "bayes", the system fits a Gaus-
sian Process surrogate model P (y | x)
that estimates validation reward y (specifically,    Model                     Mode                  Acc
eval/rewards/correctness_reward_func) as a           SP-Struct-RWD1            Multiple-Try          89.87
function of the hyperparameter configuration x:      SP-Struct-RWD1-Hyper      Multiple-Try          89.07

          learning_rate, r, lora_alpha,
                                       
                                                    Table 8: Test accuracy on GSM8k-Prolog-Prover. Hy-
    x =  batch_size, num_generations,             perparameter tuning did not surpass the original base-
                                                    line.
          max_grad_norm, weight_decay
Figure 8: Bar chart of hyperparameter importances com-
puted by W&B’s fANOVA analysis on our sweep.

  Although the tuned variant fell 0.8 percent-
age points short of the non-tuned baseline (Ta-
ble 8), fANOVA analysis (Figure 8) shows that
only learning_rate, max_grad_norm, and, more
weakly, num_generations influence the reward.
The remaining variables either contribute mini-
mally or degrade performance.
Best configuration The configuration that scored
the highest in correctness for the evaluation dataset
was:
   learning_rate: 0.00001821
   lora_alpha: 64
   max_grad_norm: 0.4359
   num_generations: 8
   per_device_train_batch_size: 16
   r: 64
   weight_decay: 0.2
   eval/rewards/correctness_reward_func: 1.859

G    Use of AI Assistants
Claude Opus 4.5 assisted in revising the write-up
and proofreading for initial submission. Opus 4.6
and Sonnet 4.6 assisted in drafting an initial script
for the systematic error analysis. Opus 4.7 assisted
with proofreading the camera-ready version.
