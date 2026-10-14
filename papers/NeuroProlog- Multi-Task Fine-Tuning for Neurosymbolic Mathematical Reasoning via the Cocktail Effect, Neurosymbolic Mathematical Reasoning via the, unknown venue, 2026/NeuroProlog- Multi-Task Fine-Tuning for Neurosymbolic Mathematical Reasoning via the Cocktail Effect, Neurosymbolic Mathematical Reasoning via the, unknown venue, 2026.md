                                                NeuroProlog: Multi-Task Fine-Tuning for
                                              Neurosymbolic Mathematical Reasoning via the
                                                            Cocktail Effect
                                                                     Pratibha Zunjare                                                     Michael S. Hsiao
                                                          Electrical and Computer Engineering                         Electrical and Computer Engineering
                                                                       Virginia Tech                                               Virginia Tech
                                                                     Blacksburg, USA                                             Blacksburg, USA
                                                                     pratibhaz@vt.edu                                              hsiao@vt.edu
arXiv:2603.02504v3 [cs.AI] 12 Sep 2026




                                                                                                                          Traditional Approach                              NeuroProlog (Ours)
                                            Abstract—We present NeuroProlog, a neurosymbolic frame-
                                         work that compiles math word problems into executable Prolog                      Problem-Solving                      Knowledge                        Problem-
                                                                                                                           Examples Only                          Base                            Solving
                                         programs and trains LLMs to internalize symbolic structure                                                            symbolic                            procedural
                                         rather than apply it post-hoc. Our multi-task Cocktail objective                                                      grounding                             demos


                                         jointly supervises formula-to-rule translation (KB) and natu-                           LLM                                             LLM fθ

                                         ral language-to-program synthesis (SOLVE) within a shared                                   verify      no learning
                                                                                                                                                                 error
                                                                                                                                                               feedback
                                         symbolic space, combining declarative knowledge with proce-                       External Solver                                       Prolog
                                         dural reasoning supervision improves compositional reasoning.                       (post-hoc)                                        Executor σ


                                         At inference, an execution-guided decoding pipeline with a five-
                                                                                                               Fig. 1: Comparison of traditional LLM fine-tuning with Neu-
                                         class error taxonomy enables zero-shot iterative program repair
                                         without correction-specific training.                                 roProlog.
                                            On GSM8K across four model scales (3B–32B), Cocktail FT
                                         yields statistically significant gains for three of four models:      verification tools rather than learned reasoning capabilities.
                                         +5.23% for Qwen-32B, +3.43% for GPT-OSS-20B, and +5.54%               Consequently, LLMs remain weak at systematic generalization
                                         for Llama-3B; GPT-OSS-20B Cocktail FT achieves the highest            to novel problem compositions and struggle to produce verifi-
                                         accuracy among the evaluated configurations at 88.34%. Error          able, executable reasoning traces without external intervention.
                                         analysis reveals scale-associated differences in failure and repair
                                         behavior across the evaluated models. These results demonstrate          Grounded mathematical reasoning, we posit, requires mod-
                                         the potential of combining symbolic knowledge and execution           els to jointly learn three core capabilities: (i) mapping natural
                                         feedback to improve LLM-based mathematical reasoning.                 language to formal logic, (ii) generating executable programs
                                            Index Terms—Large Language Models, Neurosymbolic AI,               that encode structured reasoning, and (iii) aligning symbolic
                                         Mathematical Reasoning, Multi-Task Learning                           outputs with numeric verification. To address this gap, we
                                                                                                               present NeuroProlog, a unified neurosymbolic framework
                                                                I. I NTRODUCTION                               that enforces formal reasoning through multi-task Cocktail
                                            Large Language Models (LLMs) have achieved strong                  training [11] as shown in Fig. 1. Our approach supervises
                                         performance on mathematical reasoning benchmarks such                 LLMs on formula translation, program synthesis, and exe-
                                         as GSM8K [1], aided by techniques like Chain-of-Thought               cution verification simultaneously within a shared symbolic
                                         prompting [2] and Program-of-Thoughts [3]. However, recent            representation space, inducing cross-task transfer and enabling
                                         studies reveal that LLM reasoning often relies on probabilistic       models to internalize systematic reasoning patterns rather than
                                         pattern matching rather than formal logical inference [4], [5].       relying on superficial heuristics.
                                         This leads to brittle behavior: models produce plausible but             We construct a multi-task dataset combining symbolic
                                         incorrect solutions, fail under perturbations, and cannot verify      mathematical knowledge and word problems with executable
                                         intermediate reasoning steps [6].                                     program traces. Symbolic structure paired with semantic align-
                                            Neurosymbolic approaches attempt to address these limi-            ment guides the model to generate interpretable, verifiable
                                         tations by integrating neural models with symbolic represen-          outputs. At inference, an execution-guided decoding pipeline
                                         tations or external solvers, combining neural flexibility with        provides iterative feedback to correct program errors, mea-
                                         symbolic rigor [6]–[8]. However, existing methods typically           suring not only final accuracy but also the model’s ability to
                                         apply symbolic reasoning as a post-hoc correction mechanism           recover from logical mistakes. The main contributions of this
                                         at inference time—validating or refining LLM outputs using            work are as follows:
                                         external theorem provers or logic engines [9], [10]. This                • Multi-Task Neurosymbolic Training: A Cocktail ob-
                                         decoupled design prevents models from internalizing symbolic                jective combining declarative knowledge (formula-to-
                                         structure during training: the symbolic components serve as                 Prolog) with procedural problem-solving (word-problem-
    to-program), inducing cross-task transfer within a unified     TABLE I: Comparison of neurosymbolic reasoning systems
    symbolic representation space.                                 across five design dimensions. ✓ = fully supported; P = partial;
  • Execution-Guided Decoding: An iterative refinement
                                                                   × = absent.
    pipeline with a 5-class error taxonomy enabling zero-




                                                                                                            K-P


                                                                                                                         M




                                                                                                                                                      on
                                                                                                     oT




                                                                                                                                        bg




                                                                                                                                                                 M
    shot execution-guided program repair without correction-




                                                                                                                      icL




                                                                                                                                                  e xi
                                                                                                  L/P


                                                                                                            M8




                                                                                                                                                              SL
                                                                                                                                        f-D
                                                                                                                                 C




                                                                                                                                                                       rs
                                                                                                                             LIN




                                                                                                                                              Refl
                                                                                                                  Log




                                                                                                                                                           Pro
    specific training.




                                                                                                          GS




                                                                                                                                                                     Ou
                                                                                                                                     Sel
                                                                                               PA
                                                                    Dimension
  • Scale-Dependent Error Shift: Empirical discovery
                                                                    KB grounding (train)         ×         ×         ×        ×        ×         ×           P       ✓
    that Cocktail training qualitatively transforms error           Cross-task transfer          ×         ×         ×        ×        ×         ×           ×       ✓
    distributions at large scale (TYPE ERROR → DO-                  5-class error taxonomy       ×         ×         ×        ×        ×         ×           ×       ✓
                                                                    Execution feedback           ×         ×         P        ×        ✓         ✓           ×       ✓
    MAIN ERROR at 32B) but not at small scale (SYNTAX
                                                                    Scale-dependent analysis     ×         ×         ×        ×        ×         ×           ×       ✓
    → TYPE at 8B), revealing a capacity threshold (∼10B
    parameters) for semantic type understanding.                   CodeT5+ [24] jointly trains on code understanding and genera-
  • Comprehensive         Evaluation: Rigorous experiments         tion. Our Cocktail dataset uniquely combines three supervision
    across 12 configurations (4 models × 3 settings) demon-        signals: (i) formula-to-Prolog translation for symbolic ground-
    strating statistically significant gains (+3.43% to +5.54%,    ing, (ii) natural language comments for semantic alignment,
    p<0.05) for 3 of 4 models, with strongest performance          and (iii) program execution for numeric verification, mixing
    (88.34%) exceeding all comparable baselines.                   reasoning modalities rather than task formats.
  • Open Release: Complete dataset (200 KB entries +
                                                                   Program Synthesis and Error Correction. Neural program
    310 SOLVE problems + 7476 updated GSM8K-Prolog
                                                                   synthesis methods include Codex [25], AlphaCode [26], and
    problems), training code, evaluation pipeline, and LoRA
                                                                   CodeLlama [27]. Self-Repair [28] trains on error-correction
    adapters for all 8 fine-tuned configurations.
                                                                   pairs, while Reflexion [29] uses verbal feedback for iterative
                     II. R ELATED W ORK                            improvement. These methods target general-purpose program-
                                                                   ming rather than formal reasoning. We extend execution-
Mathematical Reasoning in LLMs. Recent LLMs achieve
                                                                   guided decoding by leveraging Prolog’s error taxonomy to
strong performance on mathematical benchmarks through
                                                                   guide systematic self-correction.
intermediate reasoning techniques. Chain-of-Thought (CoT)
prompting [2] generates natural language rationales with ex-       Gaps in Prior Work. Table I situates NeuroProlog along
tensions including zero-shot CoT [12] and self-consistency         five dimensions that collectively define the design space of
decoding [13]. Program-Aided Language Models (PAL) [14]            neurosymbolic mathematical reasoning systems.
and Program-of-Thoughts (PoT) [3] delegate computation to             No prior work jointly trains on formula-to-KB translation
Python interpreters, generating executable code as reasoning       or quantifies cross-task transfer between declarative and proce-
traces. However, these approaches operate at inference time        dural symbolic objectives—gaps NeuroProlog addresses, with
through prompting rather than internalizing symbolic reason-       the Cocktail Effect validated empirically in Section IV-G.
ing during training. Studies show LLMs perform probabilistic
pattern matching rather than systematic reasoning [4], [5],                                    III. M ETHODOLOGY
failing under distribution shifts [15]. We address this through
symbolic supervision during fine-tuning, teaching models to           We present N EURO P ROLOG, a neurosymbolic framework
generate verifiable logical programs.                              that enforces executable mathematical reasoning through
Neurosymbolic AI. Neurosymbolic approaches combine neu-            multi-task fine-tuning with Prolog-based symbolic supervi-
ral learning with symbolic logic [16], [17]. Logic-LM [9]          sion. Our approach consists of three core components: (1)
uses external Prolog solvers, Faithful CoT [18] translates         a unified training corpus combining declarative mathematical
reasoning to formal logic for verification, and LINC [10] learns   knowledge with procedural problem-solving demonstrations
neural-symbolic translations through self-supervised refine-       (Section III-A), (2) a multi-task Cocktail training objective that
ment. ProSLM [19] integrates Prolog with language models           induces cross-task transfer through shared symbolic represen-
for explainable, domain-specific question answering. These         tations (Section III-B), and (3) an execution-guided decoding
methods apply symbolic reasoning post-hoc at inference time.       pipeline with iterative error feedback (Section III-C).
Prolog’s declarative semantics suit mathematical reasoning,
and GSM8K-Prolog provides Prolog annotations for GSM8K             A. Dataset Construction
with single-task supervision. We extend this through multi-
task Cocktail training with semantic alignment, internalizing        We construct a unified training corpus designed to enable
symbolic structure during training and enabling self-debugging     neurosymbolic mathematical reasoning through Prolog-based
through execution feedback.                                        representations. Our dataset comprises two complementary
Multi-Task Learning. Multi-task learning improves gener-           components: a Mathematical Knowledge Base (KB) provid-
alization through shared representations [20]. The Cocktail        ing declarative symbolic grounding, and a Problem-Solving
effect [21] produces synergistic gains from complementary          Dataset demonstrating procedural application of mathematical
tasks. FLAN [22] and T0 [23] mix instruction formats, while        concepts.
   Mathematical Knowledge Base: The KB comprises 200             dataset, where xsolve
                                                                                  j    is a word problem and yjsolve is its
carefully constructed entries formalizing fundamental math-      executable Prolog program. We train fθ to minimize:
ematical concepts as executable Prolog predicates. Each entry
                                                                          Lcocktail (θ) = λkb LKB (θ) + λsolve LSOLVE (θ),    (1)
follows a standardized instruction-input-output format:
                                                                 with each task-specific loss being the standard causal language
 Knowledge Base Entry
                                                                 modeling objective:
 Instruction: [KNOWLEDGE] Generate Prolog code that                                                                      
                                                                                                 |y|
 encodes the given mathematical concept                                                          X
 Input: Natural language description of a mathematical for-           LKB (θ) = −E(x,y)∼DKB         log pθ (yt | x, y<t ) , (2)
                                                                                                 t=1
 mula, concept, or inference rule with semantic explanation                                                             
 and worked examples                                                                            |y|
                                                                                               X
 Output: Executable Prolog program implementing the con-          LSOLVE (θ) = −E(x,y)∼DSOLVE      log pθ (yt | x, y<t ) . (3)
 cept with module imports, natural language comments, type-                                        t=1
 safe predicate definitions, helper predicates for composi-         Task weights satisfy λkb + λsolve = 1. Verified answers aj
 tional reasoning, and a standardized solve/1 interface.         are used only during evaluation to identify logically incorrect
                                                                 executable programs; they are not used during training.
Domain Coverage. The KB entries span 11+ mathematical
                                                                 Training Protocol. We fine-tune using LoRA (without quan-
domains: Basic Statistics (22 entries, 11.0%), Ratio & Propor-
                                                                 tization), injecting low-rank adapters into attention layers
tion (17, 8.5%), Percentage Calculations (17, 8.5%), Number
                                                                 while freezing pretrained weights. Both KB and SOLVE
Theory (11, 5.5%), Propositional Logic (9, 4.5%), Boolean
                                                                 entries are formatted with task-type prefixes ([KNOWLEDGE]
Operations (7, 3.5%), Geometry (12, 6.0%), Linear Equations
                                                                 vs. [SOLVE]) to enable task-conditional generation. All mod-
(6, 3.0%), Sequences & Series (3, 1.5%), and mixed topics
                                                                 els share a common optimization setup (3 epochs, cosine
(96, 48.0%).
                                                                 learning rate schedule with 8% warmup, gradient clipping at
Semantic Alignment Through Comments. A critical design
                                                                 1.0, bfloat16 precision). LoRA rank, learning rate, and regular-
choice distinguishes our KB from conventional code datasets:
                                                                 ization are tuned per model scale, with gradient accumulation
every Prolog predicate includes natural language comments
                                                                 yielding effective batch sizes of 32–64.
that explain its mathematical semantics, enabling the model
                                                                 Cocktail Effect Hypothesis. The Cocktail effect [11] suggests
to bridge informal and formal reasoning.
                                                                 complementary multi-task training yields synergistic gains.
   Problem-Solving Dataset: The second component consists        We hypothesize three transfer mechanisms: (1) Compositional
of 310 problem-solving examples based on the KB, together        Reuse (KB → SOLVE): KB predicates become reusable build-
with 7476 entries from GSM8K-Prolog [30] with executable         ing blocks for SOLVE programs; (2) Contextual Grounding
Prolog programs:                                                 (SOLVE → KB): problem-solving provides usage patterns re-
 Problem-Solving Entry Format                                    inforcing abstract formula semantics; (3) Unified Type System:
                                                                 joint training on Prolog syntax and CLP(Q) constraints induces
 Instruction: [SOLVE] Generate correct Prolog code that
                                                                 shared type-safe representations.
 solves the given math problem
 Input: Mathematical word problem with numeric con-              C. Execution-Guided Decoding with Error Feedback
 straints and a question                                            At inference time, we introduce an iterative pipeline that
 Output: Complete Prolog program that encodes problem            leverages Prolog’s error diagnostics to enable self-debugging
 constraints as predicates, implements the reasoning chain,      through execution-aware generation.
 and produces the numeric answer via solve(Result).                 1) Pipeline Architecture: Fig. 2 illustrates our four-phase
                                                                 pipeline. Given math problem q, fine-tuned LLM fθ generates
Quality Assurance. Each entry underwent multi-stage vali-
                                                                 initial Prolog program P0 . The SWI-Prolog interpreter σ exe-
dation: (1) syntactic verification via SWI-Prolog parsing; (2)
                                                                 cutes P0 , producing three possible outcomes: (1) Success with
execution testing of each solve/1 predicate; (3) semantic
                                                                 correct answer (terminate); (2) Success with wrong answer
review by domain experts and researchers.
                                                                 (classify as LOGICAL_ERROR); (3) Error with diagnostic e
                                                                 (classify via taxonomy). On failure, we generate targeted repair
B. Multi-Task Cocktail Training
                                                                 prompt Pe containing the original problem, failed program,
   We formulate neurosymbolic mathematical reasoning as          error type, and fix instructions. The model produces corrected
a multi-task learning problem where models jointly acquire       program Pi+1 = fθ (Pe ), repeating up to k = 3 iterations.
complementary capabilities through shared symbolic represen-        2) Error Taxonomy and Repair Strategies: We distinguish
tations.                                                         five error classes from SWI-Prolog diagnostics: Syntax (mal-
                                                kb 200
Task Formulation. Let DKB = {(xkb          i , yi )}i=1 denote   formed tokens/brackets), Type (arithmetic on non-numeric
                                          kb
the Knowledge Base dataset, where xi is a natural lan-           terms), Domain (runtime violations such as division by zero
guage description and yikb is its Prolog implementation. Let     or negative factorial), Instantiation (variables used before
DSOLVE = {(xsolve
                j  , yjsolve )}7786
                               j=1 denote the Problem-Solving    binding), and Logical (WRONG_ANSWER: program executes
                                                                                                                  GSM8K Accuracy with Prolog-based Reasoning
                         Q: Math Problem q                                            100                                                                                               Base
                                                                                                                                    +3.4%                                               Prolog FT
                                                                                                          +5.2%                      88.3
                                                                                                   85.1    85.5    84.9     86.1                                                        Cocktail FT
                                                                                            80.3
                                                                                       80
                                                                                                                                                            -2.3%
                                                                                                                                             66.8
                                                                                                                                                     63.1   64.5
                                                                                       60




                                                                       Accuracy (%)
                              LLM: LLM fθ


                                     Pi                                                40
                                                                                                                                                                                       +5.5%
                                                                                                                                                                                        27.1
                                                            k≤3                                                                                                     21.5      21.8
                                                                                       20
                             Exec: Executor σ
                                                       Fix: Repair
                                                                                        0
                                                                                              Qwen2.5-Coder               GPT-OSS                   Qwen3                  Llama-3.2
                                                                                                 (32B)                     (20B)                     (8B)                     (3B)


                                    ?           ×
                                                     Err: Classifier
                                                                       Fig. 3: GSM8K accuracy across four models and three config-
                                 Success?
                                                                       urations. Annotations show Cocktail FT improvement over the
                         ✓
                                                    Errors:
                                                    SYNTAX, TYPE,
                                                    DOMAIN, INST.,
                                                                       base model. Qwen3-8B is the only model where fine-tuning
           Out: Answer
                                                    WRONG ANS, ...
                                                                       decreases accuracy, revealing a generation–correction trade-
                                                                       off.
Fig. 2: NeuroProlog execution-guided decoding pipeline with
error feedback.                                                        Cocktail training yields significant gains for three of four
                                                                       models. As shown in Fig. 3, Cocktail training improves accu-
but σ(P ) = a′ ̸= a∗ ). For each error class, a targeted repair        racy by +5.23% (p < 0.01, Qwen-32B), +3.43% (p < 0.01,
prompt is applied to address the corresponding diagnostic              GPT-OSS-20B), and +5.54% (p < 0.05, Llama-3B). In each
category, with class-specific diagnostic codes and prompt              case, Cocktail FT also outperforms single-task Prolog FT
templates used to guide the repair process.                            (e.g., by +2.22% for GPT-OSS). The strongest overall result—
                                                                       88.34% by GPT-OSS-20B Cocktail FT—demonstrates that
D. Evaluation Metrics                                                  multi-task neurosymbolic training can unlock performance
   We measure performance through five complementary met-              in general-purpose models surpassing larger code-specialized
rics: Accuracy (final correct answers after k ≤ 3 iterations);         architectures.
Executability (fraction with at least one valid Prolog execu-          Qwen3-8B reveals a generation–correction trade-off.
tion); initial Success (solved on attempt 1); Correction Rate          Qwen3-8B is the only model where fine-tuning decreases
(fraction of initial failures eventually repaired); and Average        accuracy. The base model achieves 66.79% by compensating
Iterations (mean execution attempts per problem).                      for poor initial generation (7.7% initial execution) through
                                                                       strong iterative repair (70.7% correction). Fine-tuning inverts
                         IV. E XPERIMENTS                              this profile: initial execution success leaps to 69.8% but
  We conduct comprehensive evaluation of NeuroProlog                   correction collapses to 24.1%.
across four LLMs spanning a 10× parameter range (3B–32B).              Generalization to MATH-500
                                                                          To assess out-of-distribution generalization, we evaluate on
A. Experimental Setup                                                  a 239-problem subset of MATH-500 covering problems with
Models. We evaluate four models: (i) Qwen2.5-Coder-                    real numeric answers; problems requiring imaginary numbers,
32B-Instruct (code-specialized), (ii) GPT-OSS-20B (general-            symbolic equation generation, or geometric constructions are
purpose), (iii) Qwen3-8B (mid-scale general), and (iv) Llama-          excluded due to SWI-Prolog CLP(Q) scope. The evaluation
3.2-3B-Instruct (compact instruction-tuned).                           protocol is held constant with GSM8K: identical base models,
Training Configurations. For each model we compare                     LoRA hyperparameters, and three-condition structure (Base,
three settings: Base (zero-shot), Prolog FT (fine-tuned on             Prolog FT, Cocktail FT). No MATH-500 data was observed
GSM8K-Prolog), and Cocktail FT (fine-tuned on our unified              during training.
KB+SOLVE dataset per Eq. 1). Both fine-tuned configurations               The combined KB+SOLVE training configuration improves
use identical LoRA hyperparameters and train for the same              accuracy over the corresponding single-task Prolog FT config-
number of epochs.                                                      uration on three of four models, indicating that incorporating
Decoding and Evaluation. We use greedy decoding                        complementary symbolic supervision can provide additional
(temperature= 0) for deterministic results. The pipeline runs          benefits.
with k=3 maximum correction iterations on the full GSM8K
test set (n=1,319). Significance is assessed via McNemar’s             C. Effect of Model Scale
test.                                                                     Fig. 4 plots initial execution success against correction rate
                                                                       for all twelve configurations, revealing four distinct regimes.
B. Overall Performance                                                 Large code models (32B): Clean generation, emergent
  Table II presents evaluation across all twelve model-                correction. Qwen-32B achieves near-perfect initial success
configuration pairs. Fig. 3 summarizes accuracy visually.              (96.4%) but weak correction (17.0%). Cocktail training in-
TABLE II: GSM8K evaluation with Prolog-based code generation. Bold = best per model; underline = overall best. ∆ rows
show absolute change from the base model. †: p < 0.05; ‡: p < 0.01 by McNemar’s test against the same-model base
configuration.
           Model                    Config          Acc. (%)   Exec. (%)                             Initial Exec (%)                                Corr. (%)                                          Avg Iter                           Sig.
            Large-Scale Code Model (32B)
           Qwen2.5-Coder-32B Base                    80.29       97.04                                           96.4                                        17.0                                            1.07                               —
                               Prolog FT             85.14       99.24                                           98.7                                        41.2                                            1.02                               ‡
                               Cocktail FT           85.52       99.32                                           90.7                                        92.7                                            1.11                               ‡
                               ∆Prolog               +4.85       +2.20                                           +2.3                                       +24.2                                           −0.05
                               ∆Cocktail             +5.23       +2.28                                           −5.7                                       +75.7                                           +0.04
            General-Purpose Model (20B)
           GPT-OSS-20B         Base                  84.91       89.99                                           45.0                                        81.8                                           1.75                                —
                               Prolog FT             86.12       91.00                                           55.0                                        69.2                                            1.61                               †
                               Cocktail FT           88.34       93.00                                           60.0                                        70.8                                           1.52                                ‡
                               ∆Prolog               +1.21       +1.01                                           +10.0                                      −12.6                                           −0.14
                               ∆Cocktail             +3.43       +3.01                                           +15.0                                      −11.0                                           −0.23
            Mid-Scale General Model (8B)
           Qwen3-8B            Base                  66.79       72.93                                            7.7                                        70.7                                            2.43                               —
                               Prolog FT             63.15       75.96                                           69.2                                        27.7                                            1.60                               †
                               Cocktail FT           64.51       77.10                                           69.8                                        24.1                                            1.54
                               ∆Prolog               −3.64       +3.03                                           +61.5                                      −43.0                                           −0.83
                               ∆Cocktail             −2.28       +4.17                                           +62.1                                      −46.6                                           −0.89
            Small-Scale Model (3B)
           Llama-3B-Instruct    Base                 21.53       66.49                                            47.5                                       36.2                                           1.90                                —
                                Prolog FT            21.83       42.08                                            23.4                                       24.4                                           2.36
                                Cocktail FT          27.07       57.92                                            53.8                                        8.9                                           1.89                                †
                                ∆Prolog              +0.30      −24.41                                           −24.1                                      −11.8                                           +0.46
                                ∆Cocktail            +5.54      −8.57                                            +6.3                                       −27.3                                           −0.01


TABLE III: Cocktail FT accuracy (%) on MATH-500 subset                                                                                         Final Error Distribution after 3 Correction Attempts

(239 problems). ∆ denotes change from Base.                                                   39
                                                                                                      Qwen-32B                                   OSS-20B                                                     Qwen3-8B                                      Llama-3B
                                                                                                                                                                                                                                                              764
                                                                                                                                                    183                                         357
                                                                                                                             175                                                     350                                                  700
                                                                                         35                                                                                                                      319
     Model                  Base      Cocktail FT       ∆                                30                                  150
                                                                                                                                                                       154
                                                                                                                                                                                     300
                                                                                                                                                                                                                              302
                                                                                                                                                                                                                                          600
                                                                                                                                                                                                                                                                        555
                                                                                                                                     132
                                                                                                                             125                                                     250                                                  500
                                                                                         25
     Qwen2.5-Coder-32B      40.17        42.68        +2.51
                                                                     Final Error Count




                                                                                                                                                                                                                                                    442

                                                                                         20                                  100                                                     200                                                  400
     GPT-OSS-20B            49.37        51.46        +2.09                                                                   75                                                     150                                                  300
                                                                                         15
     Llama-3B-Instruct       9.10        10.04        +0.94                              10
                                                                                                         10
                                                                                                                     9
                                                                                                                              50                                                     100                                                  200
     Qwen3-8B               30.96        21.34        −9.62                               5                                   25                                                      50                                                  100

                                                                                          0                                    0                                                       0                                                    0
                                                                                              Base      Prolog    Cocktail           Base          Prolog            Cocktail                   Base            Prolog      Cocktail                Base     Prolog   Cocktail
                                                                                                                             SYNTAX_OPERATOR       DOMAIN_ERROR                 INSTANTIATION          UNEXPECTED_EOF    EXEC_EXCEPTION
                                                                                                                             TYPE_ERROR            UNDEF_PREDICATE              SYNTAX_ERROR           UNKNOWN




                                                                      Fig. 5: Final error distribution after k=3 correction attempts,
                                                                      by Prolog error type.

                                                                      20B compensates for moderate initial success (45.0%) with
                                                                      strong correction (81.8%). Cocktail training shifts toward first-
                                                                      attempt resolution (45% → 60%) while maintaining correction
                                                                      quality.


                                                                      Mid-scale models (8B): Generation–correction trade-off.
                                                                      Qwen3-8B Base has low initial success (7.7%) but strong
                                                                      correction (70.7%). Fine-tuning boosts initial success by 9×
                                                                      but sharply reduces correction, lowering overall accuracy
Fig. 4: Initial success vs. correction rate across all 12 config-     (p = 0.08).
urations, revealing four distinct behavioral regimes.

duces a qualitative shift: initial success decreases to 90.7%         Small models (3B): Capacity-limited. Llama-3B-Instruct re-
while correction improves to 92.7% (p < 0.01).                        mains in the lower-left region regardless of configuration. The
                                                                      27.07% Cocktail FT accuracy ceiling confirms 3B parameters
Medium general models (20B): Error tolerance. GPT-OSS-                are insufficient for reliable compositional Prolog generation.
D. Execution-Guided Error Recovery                                                                                Qwen3-8B shows the largest efficiency gain (+61.5%) despite
Cocktail FT trades inital success perfection for robust cor-                                                      accuracy loss, as reduced iterations (2.43 → 1.54) and
rection (Qwen-32B). Cocktail training reduces Qwen-32B’s                                                          improved executability outweigh accuracy decline for latency-
initial success accuracy from 96.4% to 90.7% but enables                                                          sensitive applications. Fig. 6 identifies two Pareto-optimal
92.7% error repair, yielding only 9 final failures versus 39                                                      points: GPT-OSS-20B Cocktail for accuracy (88.34%) and
for the base model (77% reduction).                                                                               Qwen-32B Prolog FT for efficiency.
GPT-OSS-20B: Monotonic pipeline improvement. Fine-
tuning monotonically improves all pipeline metrics: initial                                                       G. Ablation Studies
success (45% → 60%), average iterations (1.75 → 1.52),                                                               TABLE IV: Effect of Additional Symbolic Supervision
and accuracy (84.91% → 88.34%). The Cocktail configuration
requires 13.1% fewer total iterations than the base while                                                          Model           Prolog FT     Cocktail FT   ∆Acc.     ∆Exec.
achieving +3.43% higher accuracy.                                                                                  Qwen-32B              85.14         85.52    +0.38     +0.08
Correction degrades at sub-10B scale. Qwen3-8B and                                                                 GPT-OSS-20B           86.12         88.34    +2.22     +2.00
Llama-3B-Instruct exhibit sharp declines in correction rates                                                       Qwen3-8B              63.15         64.51    +1.36     +1.14
after fine-tuning (70.7%→24.1% and 36.2%→8.9%, respec-                                                             Llama-3B              21.83         27.07    +5.24    +15.84
tively), indicating that models below ∼10B parameters lack                                                         Mean                  64.06         66.36    +2.30     +4.77
sufficient capacity to jointly learn code generation and
execution-based error diagnosis.                                                                                  KB Integration. Table IV compares the single-task Prolog FT
                                                                                                                  configuration with the combined KB+SOLVE configuration.
E. Error Analysis                                                                                                 The addition of KB supervision improves accuracy across all
Scale-dependent error shift—the key mechanistic finding.                                                          four models, with gains ranging from +0.38% to +5.24%.
The most informative result from Fig. 5 is the opposite error                                                     Execution-Guided Decoding. Taxonomy-based feedback
transformations at different model capacities. At 32B, base                                                       adds +4.82% over greedy decoding. Qwen-32B Cocktail
model errors are 87.2% TYPE_ERROR—semantic failures                                                               achieves 90.7% initial success success, with 92.7% correction
fixable only 12% of the time. After Cocktail training, errors                                                     rate demonstrating effective execution-guided repair without
shift to 55.6% DOMAIN_ERROR (repaired at 96%). Total                                                              correction-specific training.
errors drop from 39 to 9.                                                                                         TABLE V: Effect of execution-guided repair on Qwen-32B
   At 8B, the inverse occurs: Qwen3-8B base errors are 89.4%                                                      performance.
SYNTAX_OPERATOR_EXPECTED. After Cocktail training,
the dominant error becomes 69.5% TYPE_ERROR with only                                                                           Initial success(%)   Final accuracy(%)      ∆
5% fixability. Fine-tuning successfully teaches Prolog syntax                                                     Prolog FT             98.7               85.14          −13.6
but introduces the same semantic failure that the 32B model                                                       Cocktail FT           90.7               85.52          −5.2
resolves, suggesting semantic type understanding requires ca-                                                     ∆ (KB)                −8.0               +0.38            —
pacity beyond 8B parameters.
                                                                                                                     Table V compares initial generation performance with final
F. Pipeline Efficiency                                                                                            accuracy after execution-guided repair for Qwen-32B. The
                                                                                                                  results show that the Cocktail configuration exhibits a smaller
                                                         Accuracy Efficiency Trade-off
                                    Low Eff.
                                                                                                                  gap between initial and final performance than Prolog FT. This
                           90       High Acc.
                                                                                                                  comparison characterizes the interaction between generation
                                                                              OSS-20B
                           80                                               (Cocktail FT)    Qwen-32B
                                                                                            (Cocktail FT)
                                                                                                                  quality and subsequent repair, but does not establish a causal
                           70
                                                                                                                  effect of KB supervision on repair.
       Best Accuracy (%)




                           60                               Qwen3-8B
                                                             (Base)
                                                                                                                                         V. C ONCLUSION
                           50
                                                                                                                     We presented NeuroProlog, a neurosymbolic framework
                           40
                                                                                                                  that combines multi-task symbolic supervision with execution-
                           30                                                                                     guided program repair for mathematical reasoning. The com-
                           20         Llama-3B
                                    (Cocktail FT)
                                                                                                High Eff.
                                                                                                Low Acc.
                                                                                                                  bined KB+SOLVE training improves GSM8K accuracy over
                                0                   20                 40             60      80
                                                                                                                  single-task Prolog fine-tuning for the evaluated models, with
                                                             Pipeline Efficiency Score                            gains of up to 5.54%, while MATH-500 results indicate gen-
Fig. 6: Accuracy vs. Efficiency tradeoff across all configura-                                                    eralization to unseen problems. Error analysis reveals scale-
tions.                                                                                                            associated differences in repair behavior, with larger models
                                                                                                                  showing greater improvements in handling semantic errors.
  We define pipeline efficiency as:                                                                               These results demonstrate the potential of combining symbolic
                                                         Accuracy × Execution Rate                                knowledge and execution feedback for improving LLM-based
                           Efficiency =                                            .                        (4)   mathematical reasoning.
                                                             Average Iterations
  Limitations and future work include scaling the KB to                         [18] Q. Lyu, S. Havaldar, A. Stein, L. Zhang, D. Rao, E. Wong, M. Apid-
1000+ entries for advanced mathematics, comparative studies                          ianaki, and C. Callison-Burch. Faithful chain-of-thought reasoning.
                                                                                     In Proceedings of the 13th International Joint Conference on Natural
across SMT solvers and Lean, controlled scaling experiments                          Language Processing and the 3rd Conference of the Asia-Pacific Chapter
(1B–70B), and evaluation on MATH and TheoremQA bench-                                of the Association for Computational Linguistics (Volume 1: Long
marks.                                                                               Papers), pages 305–329, Nusa Dua, Bali, November 2023. Association
                                                                                     for Computational Linguistics.
                                                                                [19] P. Vakharia, A. Kufeldt, M. Meyers, I. Lane, and L. H. Gilpin. ProSLM:
                             R EFERENCES                                             A prolog synergized language model for explainable domain specific
 [1] K. Cobbe, V. Kosaraju, M. Bavarian, M. Chen, H. Jun, L. Kaiser,                 knowledge based question answering. In Proceedings of the 2024
     M. Plappert, J. Tworek, J. Hilton, R. Nakano, C. Hesse, and J. Schul-           International Conference on Neural-Symbolic Learning and Reasoning
     man. Training verifiers to solve math word problems. arXiv preprint             (NeSy), pages 291–304, 2024.
     arXiv:2110.14168, 2021.                                                    [20] R. Caruana. Multitask learning. Machine Learning, 28(1):41–75, 1997.
 [2] J. Wei, X. Wang, D. Schuurmans, M. Bosma, B. Ichter, F. Xia, E. H. Chi,    [21] Y. Li, Z. Liu, and E. Xing. Data mixing optimization for supervised
     Q. V. Le, and D. Zhou. Chain-of-thought prompting elicits reasoning in          fine-tuning of large language models. In Proceedings of the 42nd Inter-
     large language models. In Advances in Neural Information Processing             national Conference on Machine Learning, volume 267 of Proceedings
     Systems, volume 35, pages 24824–24837, 2022.                                    of Machine Learning Research, pages 35419–35437. PMLR, 2025.
 [3] W. Chen, X. Ma, X. Wang, and W. W. Cohen. Program of thoughts              [22] J. Wei, M. Bosma, V. Y. Zhao, K. Guu, A. W. Yu, B. Lester, N. Du, A. M.
     prompting: Disentangling computation from reasoning for numerical               Dai, and Q. V. Le. Finetuned language models are zero-shot learners.
     reasoning tasks. Transactions on Machine Learning Research, 2023.               In International Conference on Learning Representations, 2022.
 [4] Q. Lyu, S. Havaldar, A. Stein, L. Zhang, D. Rao, E. Wong, M. Apid-         [23] V. Sanh, A. Webson, C. Raffel, et al. Multitask prompted training enables
     ianaki, and C. Callison-Burch. Faithful chain-of-thought reasoning. In          zero-shot task generalization. In International Conference on Learning
     Proceedings of the 13th International Joint Conference on Natural Lan-          Representations, 2022.
     guage Processing and the 3rd Conference of the Asia-Pacific Chapter of     [24] Y. Wang, H. Le, A. D. Gotmare, N. D. Q. Bui, J. Li, and S. C. H. Hoi.
     the Association for Computational Linguistics (Volume 1: Long Papers),          CodeT5+: Open code large language models for code understanding and
     pages 305–329, Nusa Dua, Bali, 2023. Association for Computational              generation. In Proceedings of the 2023 Conference on Empirical Meth-
     Linguistics.                                                                    ods in Natural Language Processing, pages 1069–1088. Association for
 [5] K. Valmeekam, A. Olmo, S. Sreedharan, and S. Kambhampati. Large                 Computational Linguistics, 2023.
     language models still can’t plan (a benchmark for llms on planning and     [25] M. Chen, J. Tworek, H. Jun, et al. Evaluating large language models
     reasoning about change). arXiv preprint arXiv:2206.10498, 2022.                 trained on code. CoRR, abs/2107.03374, 2021.
 [6] A. Creswell, M. Shanahan, and I. Higgins. Selection-inference: Ex-         [26] Y. Li, D. Choi, J. Chung, N. Kushman, J. Schrittwieser, R. Leblond,
     ploiting large language models for interpretable logical reasoning. In          T. Eccles, J. Keeling, F. Gimeno, A. Dal Lago, et al. Competition-level
     International Conference on Learning Representations, 2023.                     code generation with alphacode. Science, 378(6624):1092–1097, 2022.
 [7] V. Singh, D. Cassel, N. Weir, N. Feng, and S. Bayless. VERGE: Formal       [27] B. Rozière et al. Code llama: Open foundation models for code. arXiv
     refinement and guidance engine for verifiable LLM reasoning. arXiv              preprint arXiv:2308.12950, 2023.
     preprint arXiv:2601.20055, 2026.                                           [28] X. Chen, M. Lin, N. Schärli, and D. Zhou. Teaching large language
 [8] M. K. Chen. A comparative study of neurosymbolic ai approaches to               models to self-debug. In International Conference on Learning Repre-
     interpretable logical reasoning. In Proceedings of NeSy 2025, 2025.             sentations, 2024.
 [9] L. Pan, A. Albalak, X. Wang, and W. Wang. Logic-LM: Empowering             [29] N. Shinn, F. Cassano, E. Berman, A. Gopinath, K. Narasimhan, and
     large language models with symbolic solvers for faithful logical rea-           S. Yao. Reflexion: Language agents with verbal reinforcement learning.
     soning. In Findings of the Association for Computational Linguistics:           In Advances in Neural Information Processing Systems, volume 36,
     EMNLP 2023, pages 3806–3824, Singapore, 2023. Association for                   2023.
     Computational Linguistics.                                                 [30] X. Yang, B. Chen, and Y.-C. Tam. Arithmetic reasoning with llm: Prolog
[10] T. X. Olausson, A. Gu, B. Lipkin, C. E. Zhang, A. Solar-Lezama, J. B.           generation & permutation. In Proceedings of the 2024 Conference of the
     Tenenbaum, and R. Levy. LINC: A neurosymbolic approach for logical              North American Chapter of the Association for Computational Linguis-
     reasoning by combining language models with first-order logic provers.          tics: Human Language Technologies (Volume 2: Short Papers), pages
     In Proceedings of the 2023 Conference on Empirical Methods in Natural           699–710, Mexico City, Mexico, 2024. Association for Computational
     Language Processing, pages 5153–5176. Association for Computational             Linguistics.
     Linguistics, 2023.
[11] M. Brief, O. Ovadia, G. Shenderovitz, N. Ben Yoash, R. Lemberg, and
     E. Sheetrit. Mixing it up: The cocktail effect of multi-task fine-tuning
     on llm performance – a case study in finance, 2024.
[12] T. Kojima, S. S. Gu, M. Reid, Y. Matsuo, and Y. Iwasawa. Large
     language models are zero-shot reasoners. In Advances in Neural
     Information Processing Systems, volume 35, pages 22199–22213, 2022.
[13] X. Wang, J. Wei, D. Schuurmans, Q. V. Le, E. H. Chi, S. Narang,
     A. Chowdhery, and D. Zhou. Self-consistency improves chain of thought
     reasoning in language models. In International Conference on Learning
     Representations, 2023.
[14] L. Gao, A. Madaan, S. Zhou, U. Alon, P. Liu, Y. Yang, J. Callan, and
     G. Neubig. PAL: Program-aided language models. In Proceedings of
     the 40th International Conference on Machine Learning, volume 202
     of Proceedings of Machine Learning Research, pages 10764–10799.
     PMLR, 2023.
[15] Y. Razeghi, R. L. IV Logan, M. Gardner, and S. Singh. Impact
     of pretraining term frequencies on few-shot numerical reasoning. In
     Findings of the Association for Computational Linguistics: EMNLP
     2022, pages 840–854. Association for Computational Linguistics, 2022.
[16] A. d. Garcez, M. Gori, L. C. Lamb, L. Serafini, M. Spranger, and
     S. N. Tran. Neural-symbolic computing: An effective methodology for
     principled integration of machine learning and reasoning. Journal of
     Applied Logics, 6(4):611–632, 2019.
[17] H. Kautz. The third ai summer: Aaai robert s. engelmore memorial
     lecture. AI Magazine, 43(1):105–125, 2022.
