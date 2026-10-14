                                          VeriScale: Adversarial Test-Suite Scaling for Verifiable Code Generation
                                                     Yifan Bai1 * , Xiaoyang Liu1 * , Zihao Mou2 , Guihong Wang1 , Jian Yu3 ,
                                                  Shuhan Xie4 , Yantao Li5 , Yangyu Zhang6 , Jingwei Liang1,7† , Tao Luo1,7,8†
                                                         1
                                                           School of Mathematical Sciences, Shanghai Jiao Tong University
                                             2
                                               School of Science and Engineering, The Chinese University of Hong Kong, Shenzhen
                                         3
                                           School of Mathematics, Jilin University 4 School of Mathematical Sciences, Tongji University
                                                                    5
                                                                      Zhiyuan College, Shanghai Jiao Tong University
                                                      6
                                                        School of Future Technology, South China University of Technology
                                                            7
                                                              Institute of Natural Sciences, Shanghai Jiao Tong University
                                                            8
                                                              MOE-LSC, CMA-Shanghai, Shanghai Jiao Tong University
                                                               Abstract                       address this reliability challenge, verifiable code
                                                                                                           generation has emerged as a principled paradigm
                                                 As large language models (LLMs) are increas-
arXiv:2605.22368v1 [cs.LG] 21 May 2026




                                                                                                           in which models are required to jointly synthesize
                                                 ingly deployed for software engineering, con-
                                                 structing high-quality benchmarks is crucial              formal specifications, code implementations, and
                                                 for evaluating not just the functional correct-           machine-checkable proofs to establish their con-
                                                 ness, but also the formal verifiability of gen-           sistency (Sun et al., 2024; Ye et al., 2026). By
                                                 erated code. However, existing benchmarks                 integrating machine-checkable correctness guar-
                                                 are limited by the quantity and quality of pos-           antees into the generation process, this paradigm
                                                 itive and negative test cases, leading to an              offers a promising path toward more trustworthy
                                                 overestimation of model capabilities in gen-              LLM-based software development.
                                                 erating specifications and implementations. To
                                                                                                              To rigorously evaluate this emerging paradigm,
                                                 address this, we propose VeriScale, a novel
                                                 framework driven by the adversarial implemen-             recent benchmarks such as C LEVER (Thakur et al.,
                                                 tations. It consists of two stages: test-suite            2026) and V ERINA (Ye et al., 2026) have adopted
                                                 expansion to construct diverse and challeng-              Lean (Moura and Ullrich, 2021) as their core
                                                 ing test cases, and test-suite reduction to distill       verification backend. Unlike verification frame-
                                                 them into compact yet discriminative suites.              works such as Dafny (Leino, 2010) and Verus (Lat-
                                                 While VeriScale is general, we instantiate it             tuada et al., 2023), which heavily leverage SMT
                                                 on V ERINA to construct V ERINA P LUS, which
                                                                                                           solvers (de Moura and Bjørner, 2008) for auto-
                                                 expands the original test suites by over 83×,
                                                 and V ERINA L ITE, a lightweight 14× variant.             mated theorem proving with less explicit proof
                                                 Our experiments across eight state-of-the-art             steps, Lean operates as an interactive theorem
                                                 LLMs demonstrate that V ERINA P LUS exposes               prover (ITP). This distinction enables the con-
                                                 substantial model weaknesses hidden by the                struction of proofs with explicit intermediate steps,
                                                 original benchmark, evidenced by sharp score              thereby facilitating the direct assessment of model
                                                 drops on both SpecGen and CodeGen tasks,                  capabilities in proof generation (ProofGen). For
                                                 whereas V ERINA L ITE maintains this discrimi-            specification generation (SpecGen) and code gener-
                                                 native power at a fraction of the evaluation cost.
                                                                                                           ation (CodeGen), these benchmarks primarily rely
                                                 The enhanced benchmarks and source code are
                                                 publicly available at https://github.com/                 on test cases as the empirical evaluation mecha-
                                                 XiaoyangLiu-sjtu/VeriScale.                               nism (Chen et al., 2021; Ye et al., 2026).
                                                                                                              However, this reliance on test-suite evaluation
                                                                                                           exposes a central limitation: the reliability of the
                                         1       Introduction                                              assessment depends heavily on the quantity and
                                         The rapid advancement of large language models                    quality of the underlying test cases. In current veri-
                                         (LLMs) has reshaped software engineering, par-                    fiable code generation benchmarks, each problem
                                         ticularly in program synthesis and code genera-                   is typically accompanied by only a limited number
                                         tion (Chen et al., 2021; OpenAI et al., 2024). How-               of positive test cases, i.e., expected input-output
                                         ever, LLM-generated programs remain prone to                      pairs. More importantly, high-quality negative
                                         subtle logical errors (Pearce et al., 2025), limit-               test cases are even more limited, including unex-
                                         ing their deployment in high-stakes settings. To                  pected inputs and unexpected outputs that are
                                             * Equal contribution
                                                                                                           essential for testing whether generated specifica-
                                             †
                                             Corresponding author: jingwei.liang@sjtu.edu.cn, luo-         tions correctly reject invalid behaviors. As a result,
                                         tao41@sjtu.edu.cn                                                 models may satisfy the sparse test cases without

                                                                                                       1
                       Test-Suite Expansion                        Adversarial Synthesis              Test-Suite Reduction

                         Seed                  Type-aware                     Problem
                    Generation                     Mutation               Decomposition                                      Reduced
                                                                                                      Reduced               Unexpected
                       GT                                                                         Expected Input               Input
                                              Classification                 SpecGen
                Precondition                                                                          Reduced
                                                                                                  Expected Output             Boundary-
                       Pass?
                                                                      Adversarial                     Reduced                 Preserving
                                                                                                                              Reduction
                                                                    Implementation               Unexpected Output
          Unexpected             Expected Input
            Input
                                 Expected Output         GT Impl
                                                                                                        Adversary-Killing
                                Unexpected Output                                                           Reduction




Figure 1: Overview of the VeriScale framework for adversarial test-suite scaling. Driven by the adversarial
implementations, the framework scales verifiable code generation benchmarks through two core stages: test-suite
expansion to ensure rigorous boundary coverage, and test-suite reduction to optimize evaluation efficiency without
sacrificing discriminative power.


capturing the program intent, allowing incorrect                              V ERINA, resulting in the V ERINA P LUS and V ERI -
implementations or unsound and incomplete speci-                              NA L ITE benchmarks. The empirical results under-
fications to achieve inflated pass rates and leading                          score the necessity of adversarial test scaling. No-
to an overestimate of model capabilities.                                     tably, GPT-5.5 experiences a severe performance
   To bridge this gap, we propose VeriScale, an                               degradation on V ERINA P LUS, plummeting from
adversarial framework that systematically scales                              68.78% to 44.44% on SpecGen and from 96.83%
test-suite evaluation for verifiable code generation.                         to 86.24% on CodeGen. This stark contrast high-
VeriScale first combines LLM-based seed genera-                               lights how the original benchmark significantly
tion with type-aware mutation to construct a large                            overestimates true model capabilities. Furthermore,
pool of candidate inputs. These inputs are then clas-                         model performance on V ERINA L ITE closely mir-
sified as either expected or unexpected according                             rors that on V ERINA P LUS, confirming that our re-
to the ground-truth preconditions. For the former,                            duction strategy successfully eliminates redundant
VeriScale executes the reference implementation to                            test cases while preserving discriminative rigor.
derive the corresponding outputs, thereby forming                                Our main contributions are as follows:
robust expected input-output pairs.                                             1. We propose VeriScale, a framework that lever-
   The core innovation of VeriScale lies in con-                                    ages adversarial implementations to drive both
structing adversarial implementations to drive                                      the systematic expansion and the reduction of
both the construction of unexpected outputs and                                     test suites for verifiable code generation.
the reduction of expected test cases. Instead of                                2. We instantiate VeriScale on V ERINA to con-
directly prompting LLMs to generate arbitrary un-                                   struct V ERINA P LUS, expanding the original
expected outputs, VeriScale synthesizes adversarial                                 test suites by over 83×, alongside V ERI -
implementations designed to exploit weaknesses in                                   NA L ITE , a lightweight 14× variant.
LLM-generated specifications, executing them on                                 3. We show that V ERINA P LUS reveals substan-
expected inputs. Outputs are retained only when                                     tial weaknesses overlooked by the original
they differ from the reference outputs while being                                  benchmark in both SpecGen and CodeGen,
falsely accepted by the generated postconditions,                                   while V ERINA L ITE retains the discriminative
ensuring they are genuinely informative for expos-                                  power at a fraction of the evaluation cost.
ing specification flaws. Finally, VeriScale repur-
                                                                              2        Related Work
poses these implementations in a reduction stage,
distilling the expanded cases into compact yet dis-                           Benchmarks for Verifiable Code Generation.
criminative test suites through boundary-preserving                           The evaluation of LLM-generated programs has
and adversary-killing reduction.                                              evolved from functional correctness toward for-
   To evaluate our approach, we apply VeriScale to                            mal verifiability. Early benchmarks such as Hu-

                                                                         2
manEval (Chen et al., 2021), MBPP (Austin et al.,             framework comprises two primary stages, test-suite
2021), APPS (Hendrycks et al., 2021), and Live-               expansion and test-suite reduction, both fundamen-
CodeBench (Jain et al., 2025) primarily assess                tally driven by adversarial implementations.
code generation through unit tests, but do not
evaluate formal specifications or proofs. Re-                 3.1   Test-Suite Expansion
cent verification-oriented benchmarks, including              Formally, each benchmark task is equipped with a
Dafny-Synthesis (Misu et al., 2024), Clover (Sun              problem description, a ground-truth precondition, a
et al., 2024), DafnyBench (Loughridge et al.,                 reference implementation, and existing base inputs.
2025), miniCodeProps (Lohn and Welleck, 2024),                From these components, VeriScale constructs a
FVAPPS (Dougherty and Mehta, 2025), and V E -                 comprehensive test suite encompassing three
RINA (Ye et al., 2026), incorporate formal reason-            types of cases: expected input-output pairs, un-
ing tasks in languages such as Dafny and Lean.                expected inputs, and unexpected outputs. Ex-
   Among these benchmarks, V ERINA provides                   pected input-output pairs support both CodeGen
a comprehensive benchmark for verifiable code                 and SpecGen evaluation by checking intended be-
generation, supporting the evaluation of SpecGen,             haviors, while unexpected inputs and unexpected
CodeGen, and ProofGen. VeriScale is complemen-                outputs test whether generated specifications reject
tary to these efforts: instead of introducing new             invalid inputs and incorrect outputs, respectively.
tasks, it strengthens existing benchmarks by scal-
ing expected input-output pairs, unexpected inputs,           Seed Generation and Type-aware Mutation.
and high-quality unexpected outputs for more dis-             Drawing inspiration from EvalPlus (Liu et al.,
criminative test-suite evaluation.                            2023), VeriScale employs LLMs to synthesize a
                                                              diverse set of initial seed inputs. To construct the
Scaling Test-Suite Evaluation. Test-suite qual-
                                                              generation prompt for each task, we aggregate the
ity is crucial for reliable code generation evaluation,
                                                              problem description, the ground-truth precondition,
as limited unit tests may allow incorrect programs
                                                              input parameter signatures (names and types), and
to pass by missing corner cases. EvalPlus (Liu
                                                              any pre-existing expected and unexpected inputs.
et al., 2023) is a representative effort that augments
                                                              The LLM is then queried to output a specified vol-
HumanEval (Chen et al., 2021) with large-scale
                                                              ume of distinct candidate inputs, establishing a seed
test cases by combining seed generation and type-
                                                              pool for the subsequent type-aware mutation phase.
aware mutation. Mutation-based generation can
                                                              The detailed prompt is shown in Appendix C.
mitigate benchmark leakage, since newly generated
                                                                 To systematically expand the initial seed pool,
tests are less likely to have been memorized dur-
                                                              VeriScale employs an iterative, type-aware muta-
ing training (Xu et al., 2024; Satvaty et al., 2026).
                                                              tion strategy (Park et al., 2021). To preserve task-
Adversarial tests have also proven effective in ex-
                                                              specific semantics during structural perturbation,
posing weaknesses in code generation and program
                                                              we extract an ingredient pool from existing can-
repair systems (Yao et al., 2024; Ye et al., 2025).
                                                              didates, allowing target parameters to stochasti-
   VeriScale is inspired by these methods but tar-
                                                              cally reuse these contextual values (Martinez and
gets verifiable code generation, where evaluation
                                                              Monperrus, 2019). When reuse is not triggered,
requires richer signals than expected input-output
                                                              the framework falls back on type-specific heuristic
pairs alone. In particular, SpecGen evaluation
                                                              perturbations. To construct complex edge cases,
needs unexpected inputs and unexpected outputs
                                                              the mutation engine performs a sequence of mod-
to test whether generated specifications correctly
                                                              ifications by randomly targeting a single param-
reject invalid behaviors. Therefore, VeriScale ex-
                                                              eter per step under a bounded generation budget.
tends test-suite scaling with precondition-guided
                                                              To mathematically capture how a specific value
classification and adversarial implementation syn-
                                                              is perturbed during any given step, we formalize
thesis, producing more informative negative cases
                                                              our type-aware mutation procedure as a five-tuple
to strictly evaluate the SpecGen task.
                                                              M = (T , D, O, p, q).
3   Methodology
                                                                 • T is the set of input types.
In this section, we detail VeriScale, a framework                • D maps each type τ ∈ T to its domain Dτ .
designed to scale test-suite evaluation for verifiable           • O maps each type τ ∈ T to a finite set of mu-
code generation, as illustrated in Figure 1. The                   tation schemas Oτ = {sτ,1 , . . . , sτ,kτ }. Each

                                                          3
     schema sτ,i : Dτ × Θτ,i → Dτ is parameter-              to timeouts or search exhaustion are permanently
     ized by a parameter space Θτ,i .                        excluded from the final test suite.
   • p maps each type τ ∈ T to a probability distri-            Figure 2 illustrates this bidirectional pipeline
     bution pτ over Oτ , specifying how a mutation           in practice. For the isolated expected inputs, we
     schema is selected.                                     execute the reference implementation to compute
   • q maps each pair (τ, i) to a probability dis-           their corresponding outputs. This completes the
     tribution qτ,i over the parameter space Θτ,i ,          expected input-output pairs, establishing a ground
     specifying how the parameters of schema sτ,i            truth for evaluating functional correctness.
     are sampled. In general, this distribution may
     depend on the input value x ∈ Dτ .                        E XAMPLE OF C ANDIDATE I NPUT C LASSIFICATION

  Given an input value x ∈ Dτ , the mutator first              Problem Description: (V ERINA #advanced_7) This
                                                               task requires writing a Lean 4 function that converts a
samples a mutation schema I ∼ pτ , and then sam-               binary number represented as a list of digits (0 or 1) into
ples its parameters according to θ ∼ qτ,I (· | x).             its corresponding decimal value. The list is ordered in
                                                               big-endian format, meaning the most significant digit
The mutated value is then defined as                           comes first. The function should interpret the list as a
                                                               binary number and return its decimal representation as a
               Mτ (x) = sτ,I (x; θ).                           natural number.
                                                               Ground-Truth Precondition:
Since each schema is type-preserving, for any x ∈              def binaryToDecimal_precond (digits : List
                                                               Nat) : Prop := digits.all (fun d => d = 0 ∨
Dτ , i ∈ {1, . . . , kτ }, θ ∈ Θτ,i , we have                  d = 1)

                  sτ,i (x; θ) ∈ Dτ .                           Candidate Input: [1, 2, 1]
                                                               Syntax Filter: #check binaryToDecimal_precond
Therefore, the mutation procedure preserves the                ([1, 2, 1]) Ë Passed
input type by construction:                                    Stage 1: Bidirectional decide
                                                               • #guard decide (binaryToDecimal_precond
                   Mτ (x) ∈ Dτ .                                 ([1, 2, 1])) → Failed (Expression did not evaluate
                                                                 to ‘true’)
                                                               • #guard decide (¬ binaryToDecimal_precond
See Appendix A for more details of these schemas.                ([1, 2, 1])) Ë Passed
                                                               Stage 2: Bidirectional plausible
Precondition-Guided Input Classification. To
                                                               • example: binaryToDecimal_precond
classify the candidate inputs, VeriScale operates in              ([1, 2, 1]) := by
alignment with Verina (Ye et al., 2026), evaluating                unfold binaryToDecimal_precond
                                                                   simp_all!
them against the ground-truth precondition using                   plausible
a two-stage verification pipeline. Prior to logical              → Found a counter-example!
evaluation, we enforce a strict syntax filter. Each
                                                               • example: ¬ binaryToDecimal_precond
candidate is rendered as a Lean precondition appli-               ([1, 2, 1]) := by
cation, denoted as <expr>, and validated via the                   unfold binaryToDecimal_precond
                                                                   simp_all!
#check <expr> command. Candidates failing this
                                                                 Ë Passed
step due to missing arguments, type mismatches,
or syntax errors are immediately discarded.                    Final Verdict: Unexpected Input.
   In the first stage, we apply a bidirectional proce-
dure, evaluating both #guard decide <expr> and
                                                             Figure 2: A full trajectory of candidate input classi-
#guard decide (¬ <expr>). An input is classi-
                                                             fication. The input [1,2,1] will be classified as unex-
fied as expected if the positive expression evaluates        pected because #guard descide fails at Stage 1. Ac-
to true (or the negation to false), and unexpected if        cording to our judging process, this example does not
the inverse holds. For these unresolved inputs, we           proceed to Stage 2; it is shown here for illustration only.
construct an example, unfold the precondition, ag-
gressively simplify the goal context via simp_all!,
and execute plausible bidirectionally. Discover-             Adversarial Synthesis of Unexpected Outputs.
ing a counterexample for the negated expression              Beyond verifying basic functionality, evaluating
confirms the input as expected, whereas finding one          the soundness and completeness of formal specifi-
for the positive expression marks it as unexpected.          cations requires high-quality unexpected outputs to
Candidates that still lack a definitive verdict due          serve as negative test cases. Existing approaches

                                                         4
           Problem description: rotate a list of integers to the right by a specified number of positions.
           Specification generated by GPT-5.1:




           l := [1, 2, 3, 4, 5]            [4,5,1,2,3]                  [5,1,2,3,4]
                  n := 7                                                [3,4,5,1,2]                          []

                Expected Input              Expected Output        Unexpected Output (      )    Unexpected Output (   )

Figure 3: Case study of a flawed specification on V ERINA #advanced_3. The generated postcondition success-
fully rejects unexpected outputs from the original dataset, but erroneously accepts our adversarially synthesized
unexpected outputs.


often rely on LLMs to directly hallucinate incor-                          tion and eliminate redundant expected input-output
rect outputs or employ naive random sampling to                            pairs through adversary-killing reduction. Unex-
deviate from the ground truth. However, these triv-                        pected outputs are implicitly filtered alongside their
ially incorrect outputs are usually easily rejected by                     corresponding inputs.
even highly flawed specifications, failing to provide
meaningful diagnostic feedback for underspecifi-                           Boundary-Preserving Reduction. For unex-
cation. As illustrated in Figure 3, a concrete case                        pected inputs, we adopt a boundary-preserving
study demonstrates this limitation.                                        reduction strategy rather than relying solely on
   To synthesize highly discriminative unexpected                          random sampling or feature diversity. We ex-
outputs, VeriScale introduces an adversarial execu-                        tract lightweight structural signatures (e.g., empty
tion paradigm. We first prompt language models                             containers, zero or negative values, mismatched
to perform problem decomposition to reduce task                            lengths, and ordering patterns) to approximate fail-
complexity and clarify structural logic (Liu et al.,                       ure modes. We then prioritize inputs that corre-
2026). Next, we leverage advanced models to gen-                           spond to common boundary violations. For each
erate high-quality formal specifications. Crucially,                       task, we first retain representative examples from
a more capable model acts as a red team (Perez                             these critical boundary buckets, ensuring that fre-
et al., 2022), crafting adversarial implementations                        quent and semantically meaningful unexpected in-
to exploit vulnerabilities within these specifications.                    puts are preserved. If the budget is not exhausted,
As a fallback, if the model fails to generate an ad-                       we further fill the remaining slots with represen-
versarial implementation, we systematically drop                           tative inputs from diverse structural buckets, and
constraints from the ground-truth specification to                         finally use a deterministic priority order as a fall-
expose an attack target, thereby facilitating the suc-                     back. This approach keeps the unexpected input
cessful synthesis of an adversarial implementation.                        set compact while maintaining coverage of typical
                                                                           precondition violations and edge-case behaviors.
   These adversarial implementations are subse-
quently executed on the expected inputs generated                          Adversary-Killing Reduction. We further use
during the previous stage. If an adversarial imple-                        adversary-killing to reduce the set of expected
mentation produces an output that diverges from                            input-output pairs. Specifically, we repurpose the
the ground truth but is still successfully accepted                        adversarial implementations synthesized in the pre-
by the generated postconditions, this mismatched                           vious stage, treating each as a distinct mutant. We
value is formally retained. Because these unex-                            associate each expected pair with the set of adver-
pected outputs stem from systematic specification                          sarial implementations it can kill, formulating test
gaming rather than arbitrary hallucination, they                           reduction as a set-cover problem. We first select
closely mimic realistic logical errors, making them                        expected pairs that cover the largest number of pre-
significantly more effective at exposing specifica-                        viously unkilled mutants using a greedy procedure,
tion unsoundness and incompleteness.                                       ensuring that every implementation detectable by
                                                                           the expanded test suite remains covered by at least
3.2   Test-Suite Reduction                                                 one retained pair. Then, under a fixed per-task bud-
To reduce computational overhead, we filter un-                            get, we add additional pairs that kill the highest
expected inputs via boundary-preserving reduc-                             number of implementations. This strategy avoids

                                                                       5
Table 1: Comparison of test suite volumes. Data is formatted as Mean (Min–Max), accompanied by the relative
growth multiplier compared to the baseline V ERINA.

         Dataset         Expected Input-Output          Unexpected Output               Unexpected Input
         V ERINA               5.89 (2–13)                12.69 (2–34)                     0.65 (0–7)
         V ERINA P LUS   370.07 (5–705) (×62.83)   1114.01 (15–2973) (×87.79)       119.00 (0–684) (×183.08)
         V ERINA L ITE    52.34 (5–61) (×8.89)      202.35 (15–467) (×15.95)         15.80 (0–50) (×24.31)



the coverage loss caused by purely diversity-based            E XAMPLE OF A DVERSARY-K ILLING R EDUCTION
or random reduction, allowing the lightweight test            Problem Description: (V ERINA #advanced_16) Imple-
suite to substantially reduce its size while preserv-         ment the insertion sort algorithm in Lean 4. The function
ing its ability to distinguish flawed specifications.         takes a single list of integers as input and returns a new
                                                              list that contains the same integers in ascending order.
4     Experiments
                                                              Candidate Expected Input: [0, -1, -2, -3, -4]
4.1    The Augmented Benchmarks                               Expected Output: [-4, -3, -2, -1, 0]
We instantiate VeriScale on the V ERINA dataset (Ye           Adversary-Killing Count
et al., 2026) to construct the augmented bench-               • def insertionSort (xs : List Int) :
                                                                 List Int := xs.reverse
marks V ERINA P LUS and V ERINA L ITE. During
                                                                Output: [-4, -3, -2, -1, 0] → Same as expected
the expansion stage, we employ GPT-5.3-Codex
for seed generation, problem decomposition, and               • def insertionSort (xs : List Int) :
                                                                 List Int := match xs with
adversarial implementation synthesis. To obtain                   | [] => []
                                                                  | x :: _ => List.replicate xs.length x
highly diverse candidate specifications, we utilize
an array of widely adopted prior models: Claude-                Output: [0, 0, 0, 0, 0] Ë Different
Haiku-4.5, Claude-Sonnet-4.5, GPT-5.1, GPT-4.1,               • def insertionSort (xs : List Int) :
                                                                 List Int := List.replicate xs.length 0
Qwen3-Max, and DeepSeek-V3.2. Detailed hy-
                                                                Output: [0, 0, 0, 0, 0] Ë Different
perparameter configurations of the expansion and
                                                              • def insertionSort (xs : List Int) :
reduction stages are provided in Appendix B. In                  List Int := (List.range xs.length).map
total, the API cost incurred during the benchmark                   (fun n => Int.ofNat n)
expansion phase was $58.89.                                     Output: [0, 1, 2, 3, 4] Ë Different
   As demonstrated in Table 1, V ERINA P LUS sig-             • def insertionSort (xs : List Int) :
nificantly scales up the test volume by over 83×                 List Int := []
compared to the original baseline to ensure rigor-              Output: [] Ë Different
ous boundary coverage, whereas V ERINA L ITE op-              • def insertionSort (xs : List Int) :
timizes computational overhead via the aforemen-                 List Int := xs
tioned reduction strategies to provide a lightweight            Output: [0, -1, -2, -3, -4] Ë Different
14× variant. Notably, the augmented benchmarks                • def insertionSort (xs : List Int) : List
                                                                    Int :=
also consistently maintain 100% code coverage.                    match xs with
                                                                  | [] => []
4.2    Evaluation Setup                                           | x :: _ => [x]

We evaluate eight state-of-the-art LLMs, includ-                Output: [0] Ë Different
ing Claude-Sonnet-4.6, Claude-Opus-4.7, GPT-5.3-
                                                              Adversary-Killing Count: 6 / 7.
Codex, GPT-5.5, Gemini-3.1-Flash-Lite-Preview,
Gemini-3.1-Pro-Preview, Qwen3.6-Max-Preview,
and DeepSeek-V4-Pro. These models are assessed              Figure 4: An example of adversary-killing reduction.
across the V ERINA, V ERINA P LUS, and V ERI -              Given an expected input, an adversarial implementation
                                                            is considered "killed" if its output differs from the ex-
NA L ITE benchmarks, focusing on the SpecGen and
                                                            pected output. The illustrated case kills six out of seven
CodeGen tasks. To ensure a rigorous assessment,             adversarial implementations, making it a high-quality
we employ the official evaluation harness provided          case. For simplicity, we ignore any preconditions in
by V ERINA (Ye et al., 2026) to compute and re-             these adversarial implementations.
port the pass@1 scores. However, we intentionally
remove the original 2-shot setting to facilitate the
evaluation of the entire dataset.

                                                        6
                                Claude-Sonnet-4.6                                  Claude-Opus-4.7                               GPT-5.3-Codex                     GPT-5.5
                                Gemini-3.1-Flash-Lite-Preview                      Gemini-3.1-Pro-Preview                        Qwen3.6-Max-Preview               Deepseek-V4-Pro


                                                                                                       Code Score
100                                                                                   96.83
                                                           91.01                                                                          89.42                                                     Verina
                                   86.77                                                      86.24 88.36
                                                                   79.37 82.01                                                                    79.37 81.48                                       VerinaPlus
 80
        73.02                              75.13 77.78                                                                                                                                              VerinaLite
                                                                                                                                                                  67.72
                63.49 65.08                                                                                                                                                               64.02
                                                                                                                                                                          60.32 61.38
 60                                                                                                                56.61                                                                          56.61 58.20
                                                                                                                           49.74 50.79

 40



 20



  0

                                                                                     Spec Sound&Complete Score
100
                                                                                                                                                                                                    Verina
                                                                                                                                                                                                    VerinaPlus
                                   71.16                                                                                                  69.05
 80
                                                           66.40                      68.78                                                                                                         VerinaLite
        60.32                                                                                                                                                     60.32
                                                                                                                                                                                                    Error bar
 60                                                53.97
                        50.00              47.88                           50.00                      47.88                                               48.41
                44.97                                              47.09                      44.44                                               44.71                           44.97   47.62
                                                                                                                   42.33                                                  41.27
                                                                                                                                                                                                          37.83
 40                                                                                                                        31.75 33.07                                                            34.92


 20



  0




Figure 5: Performance comparison of eight models on V ERINA, V ERINA P LUS, and V ERINA L ITE. The top
panel shows the Code Score, while the bottom panel displays the Spec Sound&Complete Score. For the specification
evaluation, we include error bars indicating the lower bound (treating unknown cases as not holding) and upper
bound (treating unknown cases as holding).


  All experiments are implemented using Lean                                                                      vulnerabilities, providing a much more rigorous
v4.24.0. The evaluation was conducted on a server                                                                 evaluation of the SpecGen and CodeGen tasks.
equipped with dual Intel Xeon Platinum 8380                                                                          Furthermore, a closer examination of the Spec-
CPUs, providing a total of 80 physical cores.                                                                     Gen evaluation reveals a striking reduction in evalu-
                                                                                                                  ation uncertainty, as evidenced by the significantly
4.3   Evaluation Results                                                                                          narrowed error bars on the augmented benchmarks.
To systematically interpret our findings, we or-                                                                  In the original V ERINA baseline, the scarcity of
ganize the evaluation results across three critical                                                               test cases frequently leads to indeterminate veri-
dimensions: the effectiveness of the augmented                                                                    fication outcomes, resulting in wide margins be-
benchmarks in exposing hidden model vulnerabili-                                                                  tween the upper and lower bounds. For exam-
ties, the profound robustness gap between SpecGen                                                                 ple, Claude-Opus-4.7 exhibits a substantial gap of
and CodeGen, and the computational efficiency of                                                                  13.23% (77.78% vs. 64.55%) on the baseline. How-
our test-suite reduction strategy.                                                                                ever, under the rigorous scrutiny of V ERINA P LUS,
                                                                                                                  this ambiguity is effectively resolved, drastically
Effectiveness of the Augmented Benchmarks.
                                                                                                                  shrinking the gap for the same model to merely
As illustrated in Figure 5, all models exhibit signifi-
                                                                                                                  4.76% (50.26% vs. 45.50%). This consistent com-
cant performance degradation across both Spec-
                                                                                                                  pression of error margins across all evaluated mod-
Gen and CodeGen tasks on V ERINA P LUS and
                                                                                                                  els demonstrates that our adversarial scaling not
V ERINA L ITE compared to the V ERINA baseline.
                                                                                                                  only exposes model flaws, but also transforms a pre-
For instance, the top-performing model, GPT-5.5,
                                                                                                                  viously ambiguous evaluation into a highly defini-
achieves a code score of 96.83 and a specification
                                                                                                                  tive and statistically reliable assessment.
soundness and completeness score of 68.78 on the
baseline, which drop sharply to 86.24 and 44.44                                                                   Robustness Gap between SpecGen and Code-
on V ERINA P LUS, respectively. This consistent de-                                                               Gen. While the augmented benchmarks univer-
cline across all models demonstrates that the orig-                                                               sally depress scores, this degradation is far from
inal benchmark overestimates model capabilities                                                                   uniform: the decline in CodeGen is drastically out-
due to underspecified test cases. By addressing this                                                              paced by a precipitous drop in SpecGen. Taking
critical limitation, our adversarial expansions suc-                                                              the top-performing GPT-5.5 as a representative ex-
cessfully systematically expose previously hidden                                                                 ample again, the model experiences a moderate

                                                                                                              7
Table 2: Evaluation time on V ERINA, V ERINA P LUS, and V ERINA L ITE. We report wall-clock time in seconds,
with the average row additionally highlighting the relative time multipliers compared to the V ERINA baseline.

                                               SpecGen                                    CodeGen
  Model
                                  V ERINA V ERINA P LUS V ERINA L ITE V ERINA V ERINA P LUS V ERINA L ITE
  Claude-Sonnet-4.6                 996       1772                1280        268         356            241
  Claude-Opus-4.7                  1324       2758                2102        250         394            269
  GPT-5.3-Codex                    1018       1839                1395        252         413            327
  GPT-5.5                          1191       2100                1669        264         413            284
  Gemini-3.1-Flash-Lite-Preview     790       1333                1053        190         305            205
  Gemini-3.1-Pro-Preview           1214       2081                1645        254         396            267
  Qwen3.6-Max-Preview               962       1732                1333        212         329            227
  DeepSeek-V4-Pro                   757       1261                 935        260         311            217
  Average                          1032    1860 (×1.80)       1427 (×1.38)    244     365 (×1.50)    255 (×1.05)



relative decline of roughly 10.59% in CodeGen                 sue without sacrificing evaluative rigor. It drasti-
when moving from the V ERINA baseline to V ERI -              cally reduces the time overhead to merely 1.38 and
NA P LUS , yet suffers a staggering 24.34% relative           1.05 times the original baseline. More importantly,
reduction in its specification soundness and com-             while achieving this efficiency, V ERINA L ITE si-
pleteness score. This consistent disparity, observed          multaneously maintains a performance degradation
across all evaluated LLMs, strongly indicates that            profile highly similar to the full V ERINA P LUS suite
synthesizing sound and complete specifications is             (as evidenced in Figure 5). This optimal balance
fundamentally more challenging than generating                proves that our reduction strategies successfully
functional code.                                              prune redundant cases while fully retaining the
   This stark contrast highlights a fundamental limi-         essential diagnostic power, thereby establishing
tation in the current state-of-the-art models. Thanks         V ERINA L ITE as a highly practical benchmark for
to vast exposure to standard software repositories            evaluations of verifiable code generation.
during pre-training, advanced LLMs have devel-
oped a remarkable proficiency for synthesizing                5    Conclusion and Future Work
functional programming logic. However, this em-
                                                              In this paper, we proposed VeriScale, an adversarial
pirical success is heavily reliant on statistical pat-
                                                              framework that systematically expands and reduces
tern matching and does not seamlessly transfer to
                                                              test suites to rigorously evaluate verifiable code
the rigorous domain of formal verification. Synthe-
                                                              generation. We instantiated VeriScale on the origi-
sizing sound and complete specifications demands
                                                              nal V ERINA benchmark to construct V ERINA P LUS
strict mathematical reasoning and a global aware-
                                                              (expanded by over 83×) and V ERINA L ITE (a 14×
ness of constraints. Consequently, when tasked
                                                              variant). Our evaluations demonstrate that V ERI -
with formalizing properties that defend against ad-
                                                              NA P LUS uncovers substantial weaknesses in state-
versarial edge cases, the reasoning capabilities of
                                                              of-the-art LLMs across both SpecGen and Code-
these models remain highly fragile.
                                                              Gen tasks that original benchmarks fail to detect,
Efficiency of Test-Suite Reduction Strategy.                  while V ERINA L ITE achieves the same discrimina-
Beyond evaluation rigor, the practical utility of             tive power with significantly reduced evaluation
a benchmark heavily depends on its computational              cost. Together, these augmented benchmarks pro-
overhead. As detailed in Table 2, exhaustively eval-          vide a crucial, highly reliable standard for advanc-
uating models on the expanded V ERINA P LUS in-               ing LLM-based verifiable code generation.
curs a substantial computational penalty due to the              Future work will evolve VeriScale into a closed-
sheer volume of test cases. Specifically, this ex-            loop repair system, using the discovered counterex-
haustive approach multiplies the average time over-           amples to guide models in iteratively patching
head to 1.80 and 1.50 times the baseline for the              flawed specifications. Furthermore, recognizing
SpecGen and CodeGen tasks, respectively. Such                 that SpecGen is fundamentally an autoformaliza-
pronounced time constraints can significantly hin-            tion task severely bottlenecked by data scarcity, we
der the widespread utilization of the benchmark.              plan to leverage VeriScale as an adversarial data
   Crucially, our minimized benchmark, V ERI -                engine. By synthesizing large-scale, high-quality
NA L ITE , effectively resolves this scalability is-          training corpora, we aim to train a dedicated model

                                                          8
capable of robust autoformalization. Finally, gener-          Quinn Dougherty and Ronak Mehta. 2025. Proving the
alizing VeriScale to other formal verification frame-           coding interview: A benchmark for formally verified
                                                                code generation. Preprint, arXiv:2502.05714.
works, such as Dafny, remains a critical step toward
verifiable code generation.                                   Dan Hendrycks, Steven Basart, Saurav Kadavath, Man-
                                                                tas Mazeika, Akul Arora, Ethan Guo, Collin Burns,
Limitations                                                     Samir Puranik, Horace He, Dawn Song, and Jacob
                                                                Steinhardt. 2021. Measuring coding challenge com-
                                                                petence with APPS. In Thirty-fifth Conference on
While VeriScale significantly advances the rigor-
                                                                Neural Information Processing Systems Datasets and
ous evaluation of verifiable code generation, it has            Benchmarks Track (Round 2).
several limitations. First, the pipeline relies funda-
mentally on the availability of ground-truth precon-          Naman Jain, King Han, Alex Gu, Wen-Ding Li, Fanjia
                                                                Yan, Tianjun Zhang, Sida Wang, Armando Solar-
ditions and the reference implementations. Second,              Lezama, Koushik Sen, and Ion Stoica. 2025. Live-
the quality of the generated unexpected outputs is              codebench: Holistic and contamination free evalua-
inherently bounded by the reasoning and formal-                 tion of large language models for code. In The Thir-
ization capabilities of the LLM acting as the red               teenth International Conference on Learning Repre-
                                                                sentations.
team. If the model struggles with the strict typing
constraints of Lean 4, it may fail to synthesize so-          Andrea Lattuada, Travis Hance, Chanhee Cho, Matthias
phisticated adversarial implementations. Third, the             Brun, Isitha Subasinghe, Yi Zhou, Jon Howell, Bryan
construction phase of the expanded test suites re-              Parno, and Chris Hawblitzel. 2023. Verus: Verifying
                                                                rust programs using linear ghost types. Proc. ACM
mains highly compute-intensive, requiring massive               Program. Lang., 7(OOPSLA1).
LLM sampling and Lean executions.
                                                              K. Rustan M. Leino. 2010. Dafny: An automatic pro-
Acknowledgments                                                 gram verifier for functional correctness. In Logic for
                                                                Programming, Artificial Intelligence, and Reasoning,
                                                                pages 348–370, Berlin, Heidelberg. Springer Berlin
This work is sponsored by the National Key R&D                  Heidelberg.
Program of China Grant No. 2022YFA1008200 (T.
L.). We also thank Shanghai Institute for Mathe-              Jiawei Liu, Chunqiu Steven Xia, Yuyao Wang, and Ling-
matics and Interdisciplinary Sciences (SIMIS) for                ming Zhang. 2023. Is your code generated by chat-
                                                                 GPT really correct? rigorous evaluation of large lan-
their financial support. This research was funded                guage models for code generation. In Thirty-seventh
by SIMIS under grant number SIMIS-ID-2025-ST.                    Conference on Neural Information Processing Sys-
The authors are grateful for the resources and facil-            tems.
ities provided by SIMIS, which were essential for
                                                              Xiaoyang Liu, Zineng Dong, Yifan Bai, Yantao Li,
the completion of this work.                                    Yuntian Liu, and Tao Luo. 2026. Decompose,
                                                                structure, and repair: A neuro-symbolic framework
                                                                for autoformalization via operator trees. Preprint,
References                                                      arXiv:2604.19000.

Jacob Austin, Augustus Odena, Maxwell Nye, Maarten            Evan Lohn and Sean Welleck. 2024. minicodeprops: a
   Bosma, Henryk Michalewski, David Dohan, Ellen                minimal benchmark for proving code properties. In
   Jiang, Carrie Cai, Michael Terry, Quoc Le, and               Neurips Safe Generative AI Workshop 2024.
   Charles Sutton. 2021. Program synthesis with large
   language models. Preprint, arXiv:2108.07732.               Chloe R Loughridge, Qinyi Sun, Seth Ahrenbach, Fed-
                                                                erico Cassano, Chuyue Sun, Ying Sheng, Anish Mu-
                                                                dide, Md Rakib Hossain Misu, Nada Amin, and Max
Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan,               Tegmark. 2025. Dafnybench: A benchmark for for-
 Henrique Ponde de Oliveira Pinto, Jared Kaplan,                mal software verification. Transactions on Machine
 Harri Edwards, Yuri Burda, Nicholas Joseph, Greg               Learning Research.
 Brockman, Alex Ray, Raul Puri, Gretchen Krueger,
 Michael Petrov, Heidy Khlaaf, Girish Sastry, Pamela          Matias Martinez and Martin Monperrus. 2019. Astor:
 Mishkin, Brooke Chan, Scott Gray, and 39 others.              Exploring the design space of generate-and-validate
 2021. Evaluating large language models trained on             program repair beyond genprog. J. Syst. Softw.,
 code. Preprint, arXiv:2107.03374.                             151(C):65–80.

Leonardo de Moura and Nikolaj Bjørner. 2008. Z3: An           Md Rakib Hossain Misu, Cristina V. Lopes, Iris Ma, and
  efficient smt solver. In Tools and Algorithms for the        James Noble. 2024. Towards ai-assisted synthesis
  Construction and Analysis of Systems, pages 337–             of verified dafny methods. Proc. ACM Softw. Eng.,
  340, Berlin, Heidelberg. Springer Berlin Heidelberg.         1(FSE).


                                                          9
Leonardo de Moura and Sebastian Ullrich. 2021. The               inferred program intent. Proc. ACM Softw. Eng.,
  lean 4 theorem prover and programming language.                2(ISSTA).
  In Automated Deduction – CADE 28, pages 625–635,
  Cham. Springer International Publishing.                     Zhe Ye, Zhengxu Yan, Jingxuan He, Timothe Kas-
                                                                 riel, Kaiyu Yang, and Dawn Song. 2026. VERINA:
OpenAI, Josh Achiam, Steven Adler, Sandhini Agarwal,             Benchmarking verifiable code generation. In The
  Lama Ahmad, Ilge Akkaya, Florencia Leoni Ale-                  Fourteenth International Conference on Learning
  man, Diogo Almeida, Janko Altenschmidt, Sam Alt-               Representations.
  man, Shyamal Anadkat, Red Avila, Igor Babuschkin,
  Suchir Balaji, Valerie Balcom, Paul Baltescu, Haim-
  ing Bao, Mohammad Bavarian, Jeff Belgum, and
  262 others. 2024. Gpt-4 technical report. Preprint,
  arXiv:2303.08774.
Jiwon Park, Dominik Winterer, Chengyu Zhang, and
   Zhendong Su. 2021. Generative type-aware mutation
   for testing smt solvers. Proc. ACM Program. Lang.,
   5(OOPSLA).
Hammond Pearce, Baleegh Ahmad, Benjamin Tan,
  Brendan Dolan-Gavitt, and Ramesh Karri. 2025.
  Asleep at the keyboard? assessing the security of
  github copilot’s code contributions. Commun. ACM,
  68(2):96–105.
Ethan Perez, Saffron Huang, Francis Song, Trevor Cai,
  Roman Ring, John Aslanides, Amelia Glaese, Nat
  McAleese, and Geoffrey Irving. 2022. Red teaming
  language models with language models. In Proceed-
  ings of the 2022 Conference on Empirical Methods
  in Natural Language Processing, pages 3419–3448,
  Abu Dhabi, United Arab Emirates. Association for
  Computational Linguistics.
Ali Satvaty, Suzan Verberne, and Fatih Turkmen. 2026.
  Undesirable memorization in large language models:
  A survey. Preprint, arXiv:2410.02650.
Chuyue Sun, Ying Sheng, Oded Padon, and Clark Bar-
  rett. 2024. Clover: Closed-loop verifiable code gen-
  eration. In AI Verification: First International Sym-
  posium, SAIV 2024, Montreal, QC, Canada, July
  22–23, 2024, Proceedings, page 134–155, Berlin,
  Heidelberg. Springer-Verlag.
Amitayush Thakur, Jasper Lee, George Tsoukalas,
 Meghana Sistla, Matthew Zhao, Stefan Zetzsche,
 Greg Durrett, Yisong Yue, and Swarat Chaudhuri.
 2026. CLEVER: A curated benchmark for formally
 verified code generation. In The Thirty-ninth An-
 nual Conference on Neural Information Processing
 Systems Datasets and Benchmarks Track.
Ruijie Xu, Zengzhi Wang, Run-Ze Fan, and Pengfei Liu.
  2024. Benchmarking benchmark leakage in large
  language models. Preprint, arXiv:2404.18824.
Kaichun Yao, Hao Wang, Chuan Qin, Hengshu Zhu,
  Yanjun Wu, and Libo Zhang. 2024. Carl: Unsu-
  pervised code-based adversarial attacks for program-
  ming language models via reinforcement learning.
  ACM Trans. Softw. Eng. Methodol., 34(1).
He Ye, Aidan Z.H. Yang, Chang Hu, Yanlin Wang, Tao
  Zhang, and Claire Le Goues. 2025. Adverintent-
  agent: Adversarial reasoning for repair based on


                                                          10
A   Detailed Type-aware Mutation Rules
When ingredient pool reuse is not triggered, we apply type-specific mutations for the following Lean input
types: Int, Nat, List Int, Array Int, List Nat, Array Nat, and List Char, String.
Integers.   When τ = Int, the domain is Dτ = Z. We define mutation-schema set as
                                               Oτ ≜ {sτ,1 , sτ,2 }
where
                    sτ,1 (x, δ) = x + δ,                          Θτ,1 = {−2, −1, 0, 1, 2} ,
                    sτ,2 (x, δ) = δx,                             Θτ,2 = {−2, −1, 0, 1, 2} .
When ingredient pool reuse is disabled, both the mutation schema and its parameters are sampled
uniformly. Therefore,
                                   1
                          pτ (i) = , i ∈ {1, 2} ,
                                   2
                                   1
                         qτ,i (δ) = , i ∈ {1, 2} , δ ∈ {−2, −1, 0, 1, 2} .
                                   5
Natural numbers. When τ = Nat, the domain is Dτ = N. We obtain the mutation schemas by
applying the integer schemas and clipping the result to the natural-number domain. Formally, let
clip(z) = max(0, z), we define
                                        Oτ ≜ {sτ,1 , sτ,2 } ,
where
                  sτ,1 (x; δ) = clip(x + δ),                        Θτ,1 = {−2, −1, 0, 1, 2},
                  sτ,2 (x; δ) = clip(δx),                           Θτ,2 = {−2, −1, 0, 1, 2}.
The clipping operation ensures that every mutated value remains in Dτ = N. When ingredient pool reuse
is disabled, both the mutation schema and its parameters are sampled uniformly:
                                   1
                          pτ (i) = , i ∈ {1, 2},
                                   2
                                   1
                         qτ,i (δ) = , i ∈ {1, 2}, δ ∈ {−2, −1, 0, 1, 2}.
                                   5
Integer lists and arrays. When τ ∈ {List Int, Array Int}, we model both lists and arrays as finite
sequences. Thus,                                       !
                                                  [
                                     Dτ = Z∗ ≜       Zn .
                                                            n∈N
We define the mutation-schema set as
                                        Oτ ≜ {sτ,1 , sτ,2 , sτ,3 , sτ,4 } ,
corresponding to element modification, appending, deletion, and reversal. For a sequence x, let |x| denote
its length, xj its j-th element, replace(x, j, v) the sequence obtained by replacing xj with v, and del(x, j)
the sequence obtained by deleting xj . The schemas are defined as
                                               (
                                                replace(x, j, sInt,i (xj ; δ)) , |x| > 0,
                           sτ,1 (x; j, i, δ) =
                                                x,                               |x| = 0,
                            sτ,2 (x; v) = x ++ [v],
                                          (
                                            del(x, j), |x| > 0,
                            sτ,3 (x; j) =
                                            x,         |x| = 0,
                               sτ,4 (x) = rev(x).


                                                       11
The corresponding parameter spaces are

                            Θτ,1 (x) = {0, . . . , |x| − 1} × {1, 2} × {−2, −1, 0, 1, 2},
                               Θτ,2 = {−5, −4, . . . , 5},
                            Θτ,3 (x) = {0, . . . , |x| − 1},
                               Θτ,4 = ∅.

When |x| = 0, the index-dependent schemas are interpreted as the identity function, so the mutation
remains well-defined. When ingredient pool reuse is disabled, the schema distribution is uniform:
                                                   1
                                           pτ (i) = ,       i ∈ {1, 2, 3, 4}.
                                                   4
The parameter distributions are uniform over their corresponding finite parameter spaces. In particular,
                         1 1 1
     qτ,1 (j, i, δ | x) =    · · ,           j ∈ {0, . . . , |x| − 1},     i ∈ {1, 2},   δ ∈ {−2, −1, 0, 1, 2},
                        |x| 2 5
                         1
             qτ,2 (v) = ,                    v ∈ {−5, −4, . . . , 5},
                        11
                         1
         qτ,3 (j | x) =     ,                j ∈ {0, . . . , |x| − 1},
                        |x|
             qτ,4 (∗) = 1.

Natural-number lists and arrays. When τ ∈ {List Nat, Array Nat}, domain of the two types are
both                                                 !
                                              [
                                          ∗        n
                                 Dτ = N ≜        N .
                                                                n∈N
The mutation schemas are analogous to those for integer lists and arrays, except that every newly generated
element is clipped to the natural-number domain. Let clip(z) = max(0, z). We define

                                            Oτ ≜ {sτ,1 , sτ,2 , sτ,3 , sτ,4 } ,

where
                                           (
                                            replace(x, j, clip(sInt,i (xj ; δ))) , |x| > 0,
                       sτ,1 (x; j, i, δ) =
                                            x,                                     |x| = 0,
                             sτ,2 (x; v) = x ++ [clip(v)],
                                           (
                                             del(x, j), |x| > 0,
                             sτ,3 (x; j) =
                                             x,         |x| = 0,
                             sτ,4 (x; ∗) = rev(x).

The parameter spaces are

                            Θτ,1 (x) = {0, . . . , |x| − 1} × {1, 2} × {−2, −1, 0, 1, 2},
                               Θτ,2 = {−5, −4, . . . , 5},
                            Θτ,3 (x) = {0, . . . , |x| − 1},
                               Θτ,4 = ∅.

For empty lists or arrays, we again interpret index-dependent mutations as identity transformations. When
ingredient pool reuse is disabled,
                                                   1
                                           pτ (i) = ,       i ∈ {1, 2, 3, 4}.
                                                   4

                                                           12
The parameters are sampled uniformly:
                         1 1 1
     qτ,1 (j, i, δ | x) =    · · ,        j ∈ {0, . . . , |x| − 1},    i ∈ {1, 2},    δ ∈ {−2, −1, 0, 1, 2},
                        |x| 2 5
                         1
             qτ,2 (v) = ,                 v ∈ {−5, −4, . . . , 5},
                        11
                         1
         qτ,3 (j | x) =     ,             j ∈ {0, . . . , |x| − 1},
                        |x|
             qτ,4 (∗) = 1.

As before, when |x| = 0, we use a singleton dummy parameter space for the index-dependent schemas.
Character lists.     When τ = List Char, the domain is
                                                                           !
                                                            [
                                       Dτ =      Σ∗char ≜         Σnchar       ,
                                                            n∈N

where Σchar denotes the finite set of allowable characters. We define

                                        Oτ ≜ {sτ,1 , sτ,2 , sτ,3 , sτ,4 } ,

corresponding to character modification, appending, deletion, and reversal:
                                              (
                                               replace(x, j, c), |x| > 0,
                             sτ,1 (x; j, c) =
                                               x,                |x| = 0,
                                  sτ,2 (x; c) = x ++ [c],
                                                (
                                                  del(x, j), |x| > 0,
                                  sτ,3 (x; j) =
                                                  x,         |x| = 0,
                                  sτ,4 (x; ∗) = rev(x).

The parameter spaces are

                                    Θτ,1 (x) = {0, . . . , |x| − 1} × Σchar ,
                                       Θτ,2 = Σchar ,
                                    Θτ,3 (x) = {0, . . . , |x| − 1},
                                       Θτ,4 = ∅.

When ingredient pool reuse is disabled, the schema is sampled uniformly:
                                                1
                                        pτ (i) = ,      i ∈ {1, 2, 3, 4}.
                                                4
The parameter distributions are uniform:
                                 1         1
              qτ,1 (j, c | x) =      ·       ,                j ∈ {0, . . . , |x| − 1},   c ∈ Σchar ,
                                |x| |Σchar |
                                    1
                     qτ,2 (c) =          ,                    c ∈ Σchar ,
                                |Σchar |
                                 1
                 qτ,3 (j | x) =     ,                         j ∈ {0, . . . , |x| − 1},
                                |x|
                     qτ,4 (∗) = 1.

For |x| = 0, the index-dependent schemas use a singleton dummy parameter space and reduce to the
identity transformation.

                                                       13
Strings. When τ = String, we model the domain in the same way as List Char, namely as the set of
all finite character sequences:
                                        Dτ = Σ∗char .
Unlike List Char, however, we define the mutation-schema set as

                                               Oτ ≜ {sτ,1 , sτ,2 , sτ,3 } ,

where

                             sτ,1 (x) = ϵ,                                       Θτ,1 = ∅,
                             sτ,2 (x) = rev(x),                                  Θτ,2 = ∅,
                           sτ,3 (x; c) = x ++ c,                                 Θτ,3 = Σsp .

Here, ϵ denotes the empty string, rev reverses a string, and Σsp is the set of special characters. When
ingredient pool reuse is disabled, the schema is sampled uniformly:
                                                     1
                                             pτ (i) = ,        i ∈ {1, 2, 3}.
                                                     3
The parameter distributions are

                                           qτ,1 (∗) = 1,
                                           qτ,2 (∗) = 1,
                                                            1
                                             qτ,3 (c) =          ,   c ∈ Σsp .
                                                          |Σsp |

B    Hyperparameter Settings
Table 3 provides the detailed hyperparameter configurations used across the test-suite expansion and
reduction stages of the VeriScale pipeline.

                        Table 3: Detailed hyperparameter settings for the VeriScale pipeline.

    Parameter                              Value     Description
    Test-Suite Expansion
    Seed Generation
    –rounds                                   1      Number of LLM generation rounds for each task
    –candidates_per_round                     40     Number of candidates generated per round for each task
    –example_limit                            5      Maximum number of accept/reject examples in prompt
    Type-aware Mutation
    –max_mutations_per_input                 15      Upper limit of mutation samples per seed input
    –mutation_multi_step_size                 5      Maximum number of consecutive steps per mutation
    –mutation_ingredient_prob                0.3     Probability of ingredient reuse during mutation
    Adversarial Implementation Synthesis
    –max_adver_impl                           5      Maximum number of adversarial implementations per specification
    Test-Suite Reduction
    Boundary-Preserving Reduction
    –MAX_REJECT_INPUTS_PER_TASK               50     Maximum number of unexpected inputs retained per task
    –KEEP_PER_CRITICAL_BUCKET                  1     Number of unexpected inputs retained from each boundary bucket
    Adversary-Killing Reduction
    –MAX_ACCEPT_TEST_CASES_PER_TASK           50     Maximum number of expected input-output pairs retained per task




                                                             14
C      Prompt Templates
This appendix provides the detailed prompt templates utilized across the expansion stage of the VeriScale
pipeline. We present the exact instructions formulated for tasks including seed generation, problem
decomposition, specification generation, and adversarial implementation synthesis.
    Prompt Template for Seed Generation

    You are an expert at generating diverse candidate inputs for Lean4 code verification tasks.

    Return ONLY a JSON array. Each element must strictly follow:
    {"input": {"param1": value1, "param2": value2, ...}}

    Rules:
    1. Do not output markdown, prose, comments, or code fences.
    2. Keys in each `input` object must exactly match the function parameter names: no missing keys, no extra keys.
    3. Values must be JSON−serializable and type−compatible with the declared Lean parameter types.
    4. Treat the ground−truth precondition as the valid−input boundary: generate both valid and invalid inputs, especially
    boundary cases.
    5. Include both likely−valid and likely−invalid inputs. Treat likely−invalid as semantically violating the precondition, not
    malformed JSON.
    6. Generate diverse and challenging edge−case candidates. Return exactly the number of candidates requested by the
    user.

    Generate candidate inputs for this Lean4 programming verification task.
    Task description:
    {description}

    Ground−truth precondition:
    {precond}

    Use of precondition:
    − It defines the semantic boundary of valid inputs.
    − Generate both inputs that satisfy it and inputs that violate it.
    − Focus on hard boundary/edge cases around this condition.
    − "likely−invalid" means: still valid JSON and type−compatible, but likely violates the precondition.
    Validity mix target:
    − total candidates: {candidate_count}
    − likely−invalid target: {invalid_target}
    − likely−valid target: {valid_target}
    − If constraints make exact ratio hard, prioritize exact total count and boundary coverage.

    Function parameters (JSON):
    {parameters}

    Example likely−valid inputs:
    {test_examples}

    Example likely−invalid inputs (maybe no examples available, but generate if possible):
    {reject_examples}

    Output format MUST be exactly a JSON array of objects:
    [{{"input": {{"param": value, ...}}}}, ...]




                                                                15
Prompt Template for Problem Decomposition

### Role
You are a mathematical modeling expert. Your task is to analyze a programming problem description and produce a
structured mathematical model that captures its formal meaning.

### Input
− **Problem Description**: A natural language description of a programming problem.

### Instructions
1. Identify the Input information:
   a. contents (decleration of the input variables)
   b. constraints of the input
      − type/data structure of the input variables
      − properties of the input variables must satisfy, mark each property with one of the following two keywords
         (E: Explicit, properties that are stated explicitly in the problem descripition)
         (H: Hypothesis, properties that may be included in the constraints)
2. Identify the Output information:
   a. contents (decleration of the output variables, you can declare them as `res1, res2, ...`)
   b. constraints of the output
      − type/data structure of the output variables
      − properties of the output variables must satisfy, the relationship between the input and the output (eg. elements/
ordering preserving, elements inclusion, etc.)
3. A detailed description of the type of input and output:
  − Figure out the data struture, consider list/tuples and etc.
  − Consider the type of the variables, for example, real numbers, integers, string and etc.
4. A detailed description of the relationship between the input and the output. You may think through:
  − Does every element of the output originate from the input?
  − Does the output preserve any ordering from the input?
  − Does the output contain all elements from the input that meet some conditions?
5. Unless explicitly stated, do NOT mark non−empty, integer−only, positivity, uniqueness, sortedness and etc. with `E`.
6. Do not add any explanations of the constraints.

### Output Format
You MUST structure your response strictly as follows:

Input:
  a. {contents}
  b. {constraints}
     − {constraints1}
     − {constraints2}
     − ...
Output:
  a. {contents}
  b. {constraints}
     − {constraints1}
     − {constraints2}
     − ...

### Now perform the following task:
− **Problem Description**:
{problem_description}




                                                           16
Prompt Template for Specification Generation

### Role
You are an expert in Lean4 programming. Your task is to analyze a programming problem description and produce the
Lean4 code of its precondition and postcondition.

### Input
− **Problem Description**: A natural language description of a programming problem.
− **Input**: Input of the problem, and constraints on the input.
− **Output**: Output of the problem, and constraints on the output.
− **Precondition Function Signature**: Function signature of the precondition.
− **Postcondition Function Signature**: Function signature of the postcondition.

### Instructions
1. Generate the Lean4 code for the precondition and postcondition according to the Input and Output information. Both
the Input and Output have two parts: contents and constraints. Note that you should include all the information provided
for you.
2. You should carefully analyze the problem description to help you identify gaps and omissions, thereby capturing any
missing details within the Input and Output.
3. Define the Lean4 precondition and postcondition by using the provided function signature.
4. Only translate the constraints of the precondition marked with 'E'. Neglect the constraints marked with 'H'.
5. If auxiliary functions are needed, put them directly before the precondition and postcondition.

### Output Format
You MUST structure your response strictly as follows:
```lean
−− Precondition Implementation
{precondition auxiliary functions, if any. precondition implementation}

−− Postcondition Implementation
{postcondition auxiliary functions, if any. postcondition implementation}
```

### Now perform the task below:
− **Problem Description**:
{problem_description}
− **Input**:
{input}
− **Output**:
{output}
− **Precondition Function Signature**:
{precond_signature}
− **Postcondition Function Signature**:
{postcond_signature}




                                                           17
Prompt Template for Adversarial Implementation Synthesis

### Role
You are an expert Red Teamer in formal verification and a "lazy" code hacker. Your objective is to perform "
Specification Gaming": identify underspecification loopholes within a given `post−condition` in Lean4, and write
degenerate code to exploit these vulnerabilities.

### Input
− **Problem Description**: A natural language description of a programming problem.
− **Pre−condition**: Defines valid inputs. Assume inputs always pass this.
− **Post−condition**: The flawed contract your output MUST satisfy.
− **Implementation Signatures**: The function signature of the adversarial functions.

### Instructions
1. You MUST NOT write a genuine algorithmic solution to the `Problem Description`. **If your code actually solves
the true problem perfectly, you have FAILED your mission.** Your code MUST produce fundamentally WRONG
outputs according to the natural language problem, BUT these wrong outputs must magically trick the `post−condition`
into evaluating to `True` (or being provable).
2. Carefully analyze the `post−condition`. What crucial constraints from the `Problem Description` did it forget to
check? You may consider
  − Did it check `List.length` but forget to check elements?
  − Did it check `List.Sorted` but forget to ensure elements belong to the original list?
  − Did it use `∃` without bounding the witness?
  − Did it use `∀ x ∈ xs` but forget the empty−list case is vacuously true?
3. Here are some adversarial strategies you may consider:
  − *Constant Return*: Return meaningless constants (`0`, `#[]`, `[]`, `""`, `#[0, 0]`, `false`, `none`) if the post−
condition fails to bind the output to the input.
  − *Input Echoing*: Return the input parameters directly unmodified (e.g., `fun xs => xs`).
  − *Trivial Synthesis*: Return `List.replicate n 0`, `List.range n`, `Array.mkArray n 0`, or entirely fabricated data
that satisfies the shape/type/length constraints.
  − *Malicious Deletion/Modification*: If the post−condition only checks for the absence of something (e.g., "no
duplicates", "no negative elements"), delete everything and return `[]` / `#[]`.
  − *Edge Case Exploitation*: Force empty or trivial states (e.g., empty list, `0`, `none`) that make universally
quantified checks (`∀ x ∈ []`, ...) vacuously true.
4. Your adversarial functions MUST be pure and total Lean4 functions. You MUST NOT:
  − declare new `axiom`s, use `sorry`, or introduce `opaque` definitions to bypass verification
  − use `unsafe`, `partial`, or non−terminating recursion to avoid producing a real value
  − use `@[implemented_by ...]`, `@[extern ...]`, or any attribute that replaces the compiled behavior of a function
  − register new `instance`s that shadow or override existing typeclass resolution for standard types (`Eq`, `LE`, `LT`,
 `Decidable`, `Ord`, `BEq`, `Hashable`, etc.)
  − rely on `IO`, `ST`, `IO.Ref`, or any monadic side effects that persist outside the function call
  − use noncomputable definitions or use `choose`, `choose_spec` to define the adversarial functions
  If any strategy requires modifying the ambient environment, DO NOT use it.
5. You MUST NOT use type−level / typeclass / coercion tricks to fake post−condition satisfaction. In particular, DO
NOT:
  − define custom `structure`s / `inductive` types as outputs purely so that a custom `DecidableEq`, `LE`, `LT`, or `
BEq` instance makes the post−condition trivially true
  − override or re−declare instances such as `BEq`, `DecidableEq`, `LE`, `LT`, `Ord`, `HAdd`, `HSub`, `
Membership`, `GetElem` for standard types
  − return proxy/wrapper/sentinel values (e.g., via `Subtype` with a bogus proof, or a wrapper with a custom equality)
that are not semantically valid outputs
  − exploit `Decidable` instances whose `decide` always returns `isTrue`
  Outputs must be plain values of the exact types expected by the specification (`Nat`, `Int`, `String`, `List α`, `Array
 α`, `Option α`, tuples of these, etc.).
6. You must generate exactly **5** different adversarial implementations. Try to use a *different* adversarial strategy
from the list above for each one to probe different potential loopholes.
7. The function signatures of your adversarial implementations MUST match the implementation signature provided.
Distinguish each adversarial function by appending the suffix `i` to its name, where i denotes the index of the i−th
adversarial implementation.
8. DO NOT add any explanations.

### Output Format
You MUST structure your response strictly as follows. Do not include any explanations, and you must provide **5**
adversarial implementations.

```lean
−− Adversarial Implementation 1
{adversatial function 1}




                                                           18
−− Adversarial Implementation 2
{adversatial function 2}

−− Adversarial Implementation 3
{adversatial function 3}

−− Adversarial Implementation 4
{adversatial function 4}

−− Adversarial Implementation 5
{adversatial function 5}
```

### Now perform the task below:
− **Problem Description**:
{problem_description}
− **Pre−condition**:
```lean
{pre_condition}
```
− **Post−condition**:
```lean
{post_condition}
```
− **Implementation Signatures**:
```lean
{impl_signature}
```




                                   19
