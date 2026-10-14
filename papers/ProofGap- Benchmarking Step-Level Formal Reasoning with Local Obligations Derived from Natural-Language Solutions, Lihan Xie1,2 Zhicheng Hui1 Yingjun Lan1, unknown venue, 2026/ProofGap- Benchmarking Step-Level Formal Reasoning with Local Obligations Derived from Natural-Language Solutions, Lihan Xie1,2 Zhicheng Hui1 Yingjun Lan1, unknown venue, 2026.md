                                         Preprint




                                         P ROOF G AP : B ENCHMARKING S TEP -L EVEL F ORMAL
                                         R EASONING WITH L OCAL O BLIGATIONS D ERIVED
                                         FROM NATURAL -L ANGUAGE S OLUTIONS

                                                                     Lihan Xie1,2 Zhicheng Hui1 Yingjun Lan1
                                                                  Zhehao Li1 Xingzhi Qi1 Siyue Huang1 Jirui Liu1
                                                                    Chuxiao Zeng1 Bohan Zhao1 Qinxiang Cao1,∗
                                                                                1
                                                                                    Shanghai Jiao Tong University
                                                                                 2
                                                                                    Shanghai Innovation Institute
arXiv:2609.29296v1 [cs.PL] 24 Sep 2026




                                                                                          A BSTRACT

                                                      Existing formal mathematics benchmarks, such as miniF2F, ProofNet, and Put-
                                                      namBench, primarily evaluate models on constructing complete formal proofs for
                                                      challenging problems. Because success is measured at the theorem level, these
                                                      benchmarks offer limited insight into models’ step-level formal reasoning. Eval-
                                                      uating this capability separately enables finer-grained diagnosis of model limita-
                                                      tions than theorem-level evaluation alone.
                                                      To fill this evaluation gap, we introduce ProofGap, a fine-grained benchmark for
                                                      step-level formal reasoning. ProofGap is constructed through a natural-language
                                                      proof-processing pipeline that decomposes each reasoning step into one or more
                                                      aligned proof gaps. Applying this pipeline to natural-language solutions to 3,015
                                                      exercises in B. P. Demidovich’s Problems in Mathematical Analysis yields 26,116
                                                      gaps. The benchmark focuses on mathematical analysis, a domain that remains
                                                      challenging for current models. By supplying the local context and target ex-
                                                      plicitly, gap completion isolates local formal proof construction from end-to-end
                                                      proof composition, enabling more precise localization of model failures. Natural-
                                                      language solutions serve as the provenance of these obligations, while the bench-
                                                      mark task itself starts from an already formalized local context and goal. Beyond
                                                      benchmarking, the same pipeline may support future proof-verification systems,
                                                      provided that semantic translation and sequential proof composition are handled
                                                      reliably.


                                         1       I NTRODUCTION
                                         Mathematical reasoning provides a demanding test of whether large language models can perform
                                         rigorous, multi-step inference. Although recent models have achieved impressive performance on
                                         natural-language mathematics, their proofs may still contain subtle logical errors, omitted assump-
                                         tions, or unsupported intermediate claims that are difficult to detect reliably. Formal systems such
                                         as Lean, Rocq, and Isabelle offer a complementary approach by expressing mathematical arguments
                                         in precise languages and mechanically checking the resulting proofs de Moura & Ullrich (2021);
                                         Bertot & Castéran (2013); Nipkow et al. (2002). Building on this verifiable interface, powerful for-
                                         mal theorem-proving systems such as DeepSeek-Prover Ren et al. (2025) and AlphaProof Hubert
                                         et al. (2026) have emerged. In parallel, benchmarks such as miniF2F, ProofNet, and PutnamBench
                                         have provided standardized environments for evaluating statement formalization and formal proof
                                         construction across challenging mathematical problems. Despite differences in their specific tasks
                                         Zheng et al. (2022); Tsoukalas et al. (2024); Azerbayev et al. (2023), these benchmarks largely take
                                         the complete theorem as the basic unit of evaluation.
                                         Yet in many practical settings, what is needed is not formal reasoning over a complete proof, but
                                         fine-grained feedback on individual reasoning steps. During natural-language proof generation, a
                                             ∗
                                                 Corresponding author.


                                                                                                 1
Preprint




critical step can be subjected to local formal verification as soon as it is proposed, allowing unsup-
ported inferences to be detected and revised before their errors propagate through the subsequent
argument. Such feedback can also be used to filter candidate reasoning steps or rank alternative
reasoning trajectories, allowing models to prioritize directions supported by formal evidence. SAFE
exemplifies this use case: it formalizes individual model-generated reasoning steps as Lean state-
ments and combines the resulting proof states with a process reward model to improve Best-of-N
trajectory selection Liu et al. (2025).
Step-level formal feedback is also valuable during training. Prior work has shown that process su-
pervision over intermediate reasoning steps can provide more effective training signals than outcome
supervision based solely on final answers Lightman et al. (2024). FoVer further uses formal veri-
fication tools to generate step-level error labels automatically, demonstrating that formal systems
can provide machine-checkable training data for process reward models Kamoi et al. (2026). Such
feedback can supervise the reasoning process itself, rather than assigning credit solely according to
whether the final answer is correct.
Both settings require formal feedback that is trustworthy, localized, and sufficiently inexpensive to
obtain repeatedly. Whole-proof formalization and proof search provide only a coarse signal and
can be computationally costly when applied to every candidate proof or sampled training trajectory.
A failure at the whole-proof level is also difficult to interpret: the natural-language argument may
contain a logical error, the autoformalization component may translate the proof goal incorrectly, or
the formal proof-generation model may fail even when given an accurately formalized and provable
goal. MA-ProofBench makes this ambiguity concrete in mathematical analysis. Even with expert-
reviewed Lean statements, several models that produce many natural-language proofs judged to
be fully correct nevertheless achieve near-zero formal proof success on the same problems, with
Mathlib hallucinations and incomplete proofs among the dominant failure modes Pu et al. (2026).
Thus, whole-proof verification provides only a coarse signal for applications that require localized
and actionable formal feedback.
For formal feedback to be reliable and actionable, each verification task should correspond to an
identifiable reasoning step in the source natural-language proof, rather than to an arbitrary fragment
of a formal derivation. To this end, we introduce ProofGap, a fine-grained benchmark for step-level
formal reasoning. Using a semantics-aware pipeline for processing natural-language proofs, we
construct ProofGap from 3,015 exercises originating from Demidovich’s Problems in Mathematical
Analysis Demidovich (1969) and their Chinese reference solutions compiled by Fei and Zhou Fei &
Zhou (2012).
ProofGap focuses on mathematical analysis not only because formal proof construction in this do-
main remains challenging for current models Yu et al. (2025); Pu et al. (2026), but also because
many local inferences in analysis solutions depend on domain restrictions, nonzero conditions, sign
conditions, and convergence assumptions that are easily left implicit in natural-language arguments.
These characteristics make mathematical analysis a particularly informative testbed for evaluating
step-level formal reasoning. Moreover, the breadth and diversity of Demidovich’s exercise collection
provide a suitable foundation for the systematic, large-scale construction of such localized formal
reasoning tasks.
To construct ProofGap, we build on a verifiable auto-formalization pipeline based on the Relaxed
and Core Natural Formal Languages. The pipeline first translates a natural-language solution into
an intermediate representation that preserves its stepwise reasoning structure, and then resolves its
ambiguous notation, problem-solving constructs, and implicit variable scopes through a verifiable
elaboration procedure. From the resulting semantically defined proof representation, a proof-gap
generator derives localized verification conditions that expose the assumptions available at each
point and the goal to be established. ProofGap takes the discharge of these conditions as its bench-
mark task.
Our main contributions are as follows:



       • We formulate step-level formal reasoning as a distinct evaluation problem in which models
         discharge local formal proof obligations derived from individual reasoning steps in text-
         book natural-language solutions.


                                                  2
Preprint




          • We construct ProofGap through a natural-language proof-processing procedure, obtaining
            26,116 formal proof gaps from multi-step solutions to 3,015 exercises in mathematical
            analysis, and release both its original and Lean versions.1
          • For the original version, we provide a lightweight checker and a verifier-guided agent work-
            flow to produce executable, checker-validated proofs; for the Lean version, we provide
            ground-truth proofs for exercises and gaps.
          • We systematically evaluate a range of models on ProofGap and conduct fine-grained anal-
            yses to identify their major limitations in formal reasoning for mathematical analysis.
By evaluating models on localized, mechanically checkable proof obligations, ProofGap provides a
fine-grained benchmark for studying formal reasoning beyond theorem-level success. These obliga-
tions may also serve as components of future natural-language proof-verification systems.

2       R ELATED W ORK
Research most closely related to ProofGap lies at the intersection of formal mathematics bench-
marks, step-level mathematical verification, and formal reasoning in mathematical analysis. Table 1
compares representative formal mathematics benchmarks in terms of mathematical scope, target
source, and evaluation granularity.

Table 1: Comparison of formal mathematics benchmarks by mathematical scope, target prove-
nance, and evaluation granularity. Granularity is defined relative to the source problem or reasoning
process; every evaluation target is nevertheless represented as a standalone formal theorem. NL
denotes natural language.
                              Mathematical
Benchmark                                        Target source              Granularity        # Targets
                              scope
miniF2F
                              Multi-domain       Original problem           Theorem-level           488
Zheng et al. (2022)
ProofNet
                              Multi-domain       Original problem           Theorem-level           371
Azerbayev et al. (2023)
PutnamBench
                              Multi-domain       Original problem           Theorem-level           640
Tsoukalas et al. (2024)
FormalMATH
                              Multi-domain       Original problem           Theorem-level         5,560
Yu et al. (2025)
MA-ProofBench                 Mathematical
                                                 Original problem           Theorem-level           200
Pu et al. (2026)              analysis
FormalML                      Machine learning
                                                 Formal proof subgoal       Step-level            4,937
Yang et al. (2025)            theory
FormalStep                                       Model-generated NL
                              Multi-domain                                  Step-level           30,809
Liu et al. (2025)                                reasoning step
                              Mathematical       Original textbook NL
ProofGap                                                                    Step-level           26,116
                              analysis           solution step


Formal Mathematics Benchmarks. Existing benchmarks primarily construct formal evaluation
targets from original mathematical problems. Representative benchmarks include miniF2F Zheng
et al. (2022), ProofNet Azerbayev et al. (2023), PutnamBench Tsoukalas et al. (2024), and For-
malMATH Yu et al. (2025). Despite differences in problem source, domain, and difficulty, these
benchmarks generally derive their formal targets directly from the original problem statements and
report whether models successfully prove them at the problem level. This setting is well suited to
evaluating end-to-end formal proof construction, but provides limited insight into whether a model
can formally justify a particular inference in the corresponding natural-language argument. No-
tably, although ProofNet provides natural-language proofs, it does not decompose their individual
reasoning steps into aligned formal proof obligations.
    1
        Project repository: https://github.com/xielihan/ProofGap-Benchmark


                                                    3
Preprint




Step-Level Mathematical Verification. Step-level reasoning has been studied through process-
supervision datasets that label intermediate natural-language steps (Lightman et al., 2024; Wang
et al., 2024), and through formally grounded settings such as FoVer, FormalML, and SAFE/Formal-
Step (Kamoi et al., 2026; Yang et al., 2025; Liu et al., 2025). ProofGap differs from these works
in the source of its formal targets and in its alignment criterion. FormalML extracts subgoals from
existing Lean developments, while FormalStep autoformalizes model-generated reasoning trajecto-
ries, whose steps may be incorrect, redundant, or self-correcting. In contrast, ProofGap decomposes
coherent textbook reference solutions into local proof obligations aligned with the logical structure
of complete natural-language arguments.

Formal Reasoning in Mathematical Analysis. Mathematical analysis is particularly challenging
for formal reasoning: local inferences often depend on domain restrictions, nonzeroness, differentia-
bility, integrability, convergence assumptions, and library-specific representations of analytic con-
cepts. Recent evaluations confirm this difficulty: FormalMATH reports substantially lower formal
proof success on calculus than on algebra, and MA-ProofBench finds that models still struggle with
mathematical analysis even when they perform much better on the corresponding natural-language
problems. Precisely because end-to-end success remains low in this domain, fine-grained diagnosis
is important: theorem-level failure alone cannot distinguish whether a model fails on analytic side
conditions, local algebraic transformations, limit arguments, or the global proof plan. However,
existing analysis benchmarks remain problem-level, constructing one formal target for each origi-
nal problem. ProofGap complements them by processing reference solutions to 3,015 Demidovich
exercises into 26,116 step-level formal targets, enabling localized evaluation of formal reasoning in
mathematical analysis.


3     T HE P ROOF G AP B ENCHMARK

3.1   TASK D EFINITION

A ProofGap instance is represented as a triple
                                              (Γ, g, m),                                            (1)
where Γ is the well-scoped local context available at the current proof position, g is the target propo-
sition, and m is an optional strategy annotation preserved from the source solution. These compo-
nents correspond to the ASSUM, GOAL, and METHOD fields in the released data.
Given Γ and g, a model must generate a formal derivation accepted by the designated proof checker,
thereby establishing
                                             Γ ⊢ g.                                            (2)
The annotation m is optional metadata rather than part of the proof obligation: it neither affects
checker acceptance nor is provided to models in the reported evaluations. We release it to support
future analyses of proof strategies and strategy-conditioned proving.
Each gap is evaluated independently. Intermediate propositions established earlier in the source
solution are included in Γ and treated as available premises. The source natural-language step is
used during benchmark construction and traceability analysis, but is not part of the model input.
ProofGap therefore evaluates local formal proof completion over obligations derived from natural-
language solutions. It does not directly evaluate natural-language autoformalization or the detection
of invalid natural-language steps. Moreover, because intermediate propositions from earlier steps
are supplied as premises, the task does not evaluate end-to-end proof composition.

3.2   B ENCHMARK C ONSTRUCTION

We construct ProofGap from exercises in B. P. Demidovich’s Problems in Mathematical Analysis
and their Chinese reference solutions compiled by Fei and Zhou. The corpus covers major topics
in mathematical analysis. Before formalization, we remove problems that depend on figures or
unavailable external information, split independent subquestions, and normalize problem–solution
boundaries.


                                                   4
Preprint




Figure 1: Construction pipeline from a boxed natural-language reasoning step to a local ProofGap
instance. Relaxed NFL preserves the original proof structure and method annotation, while Core
NFL makes the implicit universal variables and assumption scopes explicit and normalizes f ′ as
FunDeri(f,1,1), where FunDeri(f,1,1) denotes the first-order derivative of function f with respect to
its first formal argument. The last column shows the emitted ProofGap instance and its correspond-
ing Lean target.




Figure 1 illustrates the construction pipeline. In the first stage, a prompt-based translator con-
verts each problem and solution into Relaxed Natural Formal Language (Relaxed NFL), a parser-
readable intermediate representation that preserves the conditions, goal, proof structure, and method
annotations of the source. The generated representation then undergoes parser validation and
representation-consistency screening, which checks the preservation of the main assumptions, goal,
and proof steps and rejects unsupported intermediate conclusions. Detailed screening criteria are
provided in Appendix A.2.
In the second stage, the Relaxed NFL AST is elaborated into Core NFL, a normalized representation
with explicit proof contexts and variable bindings. The elaboration decomposes compound proposi-
tions, disambiguates context-dependent notation, canonicalizes mathematical operations, and makes
remaining free variables explicit. Most transformations are deterministic; unresolved notation or
scope ambiguities are handled using constrained LLM heuristics followed by programmatic valida-
tion. The resulting Core NFL representation must pass syntax and binding-completeness checks.
In the third stage, the proof-gap generator traverses the Core NFL AST while maintaining the cur-
rent proof state Γ ⊢ g. When a step introduces an intermediate proposition P , the generator emits
the obligation Γ ⊢ P and adds P to the context used to construct subsequent proof states, without
requiring the preceding gap to be solved. Nested and backward proof steps are handled by gener-
ating the corresponding local obligations. Each gap retains a trace link to its source step and Core
NFL node; a single source step may produce multiple gaps when compound or nested reasoning is
decomposed. Formal generation rules are provided in Appendix A.4.
The generator first emits each local obligation in the benchmark-native ProofGap representation. To
support evaluation with existing formal proof assistants, every generated gap is then translated into
a Lean proof obligation using GPT-5.6-sol OpenAI (2026). Local declarations and assumptions are
mapped to Lean binders and theorem premises, while the gap goal is mapped to the theorem conclu-
sion. Each Lean theorem statement is paired with a proof verified by Lean prover. The translations
are audited through a human-in-the-loop cross-review protocol. Multiple independently instantiated
LLM reviewers compare each formalized obligation with the corresponding source problem and so-
lution step. Any case flagged by at least one reviewer for a potential translation error or semantic
ambiguity is escalated to human adjudication and retained only after its semantic fidelity has been
confirmed.


                                                 5
Preprint




3.3     S TATISTICS AND C OVERAGE

The final ProofGap benchmark contains 3,015 mathematical-analysis exercises and 26,116 proof
gaps. Each exercise yields 8.66 gaps on average, with a median of 7. Each gap retains 8.33 assump-
tions on average, with a median of 6. These statistics show that a complete natural-language solution
is typically decomposed into multiple local proof obligations, while each obligation preserves sev-
eral facts available at the corresponding step of the solution.
We group the exercises into seven topics according to the organization of the source material. As
shown in Table 2, ProofGap covers single-variable functions, limits, and continuity; single-variable
differentiation; indefinite and definite integrals; series; multivariable differentiation; parameter inte-
grals; and multiple, line, and surface integrals. Parameter integrals are treated as a separate category
because their proof obligations frequently involve parameter-dependent limits, convergence condi-
tions, and interchanges between limiting operations and integration.



                                  Table 2: Topic coverage of ProofGap.
Topic                                                          Exercises                            Gaps
Functions & Limits                                                   529                            4,033
Single-Var. Differentiation                                          640                            5,019
Indefinite and Definite Integrals                                    620                            4,795
Infinite Series                                                      455                            4,986
Multivariable Differentiation                                        260                            2,380
Parameter Integrals                                                  100                            1,082
Multiple, Line, and Surface Integrals                                411                            3,821



The topic distribution is not uniform, reflecting the composition of the source material. Neverthe-
less, every topic contains at least 100 exercises and more than 1,000 proof gaps. The benchmark
therefore supports both aggregate evaluation and topic-level analysis across major components of
undergraduate mathematical analysis.



4     A L IGHTWEIGHT P ROOF -C HECKING F RAMEWORK FOR P ROOF G AP

For the original version of ProofGap, we provide a lightweight proof-checking interface. Given a
local context Γ and goal g, a model emits a short executable program in an 18-command domain-
specific language (DSL), and a deterministic checker replays it against the evolving proof state. A
program passes the checker only when every generated goal closes, yielding a replayable certificate.
The framework provides deterministic solving through autosolve and access to a 514-entry theo-
rem library. Unsupported solver inputs return unknown, and theorem applications must discharge
all premises and side conditions. A verifier-guided agent uses checker feedback to revise candidate
programs; accepted certificates additionally undergo admit-free root replay and semantic audit. Ap-
pendix B gives the command, checker, and solver specifications, while Appendix B.5 and Figure 2
describe the agent workflow.


Baseline results. Treating autosolve as a lightweight automated theorem prover, we first apply
this DSL command to all 26,116 ProofGap instances and directly close 2,838 gaps (10.87%). We
then run our verifier-guided agent workflow on the remaining instances, using Codex as the agent
and GPT-5.6-sol as its underlying model; the workflow synthesizes checker-validated DSL proofs
for an additional 4,889 gaps. Together, the two stages solve 7,727 gaps (29.59%). Beyond model
scoring, each accepted DSL program is an executable ground-truth solution for the corresponding
gap in the original version of the benchmark.


                                                    6
Preprint




5     E XPERIMENT

5.1     R ESEARCH Q UESTIONS

Our experiments on the Lean version of ProofGap are organized around four research questions.

        • RQ1: To what extent can the evaluated models solve the step-level formal proof obligations
          in ProofGap?
        • RQ2: Under a fixed per-target sampling budget, how does performance on step-level gaps
          compare with performance on their corresponding complete exercise theorems?
        • RQ3: How do specialized formal provers and general-purpose language models compare
          on the balanced ProofGap-280 subset?
        • RQ4: What additional diagnostic information does step-level evaluation provide beyond
          the success or failure of complete theorem proving?

5.2     E XPERIMENTAL S ETUP

Evaluation sets. The complete Lean evaluation set contains 26,116 step-level gaps from 3,015 exer-
cise instances, together with their corresponding 3,015 exercise theorems. Every target is accompa-
nied by a Lean-verified reference proof that is withheld from the evaluated model. For cross-model
comparison, we construct ProofGap-280 by sampling 10 gaps from each of the 28 strata defined by
seven mathematical topics and four length categories. The selected gaps come from 280 distinct
parent exercises, yielding 280 paired gap–exercise targets. Further details on the construction of
ProofGap-280, together with model performance stratified by mathematical topic and proof length,
are provided in Appendices D and E.2.
Models. We evaluate Goedel-Prover-V2-8B Lin et al. (2026), DeepSeek-Prover-V2-7B, and
Kimina-Prover-Distill-8B Wang et al. (2025) on the full paired evaluation set and ProofGap-280.
On ProofGap-280, we additionally evaluate Claude-Opus-4.8 Anthropic (2026), GPT-5.6-sol, Kimi-
K3 Kimi Team (2026), GLM-5.2 GLM-5-Team (2026), and DeepSeek-V4-Pro DeepSeek-AI et al.
(2026). Model configurations are provided in Appendix C.2.
Verification and metrics. We use a budget of eight candidate proofs per target, each capped at
8,192 tokens, and evaluate proof correctness with Lean. We report Pass@k using the standard
estimator of Chen et al. (2021). Gap-level scores assign equal weight to every gap (micro averaging).
For exercise-level diagnosis at Pass@8, we first compute the fraction of solved gaps within each
exercise, then average equally across exercises (macro coverage). Formal definitions are given in
Appendix C.3; full-set Pass@1/3/8 results are provided in Appendix E.1.

5.3     R ESULTS


Table 3: Pass@8 (%) on all 26,116 proof gaps, the 23,191 gaps not solved by the evaluated tactic
portfolio, and the 3,015 corresponding exercise theorems.
                                      All                  Tactic-unsolved                   Exercise
Model                                gaps                        gaps                       theorems
Goedel-V2-8B                         35.39                           27.48                      4.28
DeepSeek-Prover-7B                   33.27                           25.16                      3.32
Kimina-Distill-8B                    31.99                           23.57                      2.92



5.3.1      F ULL -S ET S OLVABILITY (RQ1)
On the complete set of 26,116 proof gaps, Table 3 reports Pass@8 scores of 35.39% for Goedel,
33.27% for DeepSeek, and 31.99% for Kimina. Thus, even the strongest specialized prover leaves
64.61% of the local obligations unsolved. ProofGap therefore remains challenging despite evaluat-
ing individual steps rather than complete proofs.


                                                 7
Preprint




     Table 4: Topic-level Pass@8 (%). Each entry reports gap/exercise-theorem performance.
Topic                                             Goedel               DeepSeek           Kimina
Functions, Limits, and Continuity               44.41 /   8.88        40.32 /   7.56    39.10 /    7.37
Single-Variable Differentiation                 35.11 /   4.69        32.72 /   2.50    32.12 /    2.97
Indefinite and Definite Integrals               32.43 /   1.77        30.57 /   1.45    28.59 /    0.16
Series                                          31.09 /   3.52        29.58 /   3.08    27.20 /    2.86
Multivariable Differentiation                   40.21 /   3.08        38.24 /   2.69    37.73 /    1.92
Parameter Integrals                             20.43 /   1.00        19.50 /   0.00    18.21 /    0.00
Multiple, Line, and Surface Integrals           36.82 /   3.89        35.57 /   3.41    35.15 /    2.68


Table 5: Mean exercise-level gap coverage, reported over all exercises and conditioned on whether
the corresponding complete theorem is solved at Pass@8.
                                                           Mean gap coverage (%)
                                     All                         Theorem                    Theorem
Model                             exercises                       solved                     failed
Goedel                                  31.15                        75.07                        29.19
DeepSeek                                29.12                        75.94                        27.51
Kimina                                  27.63                        79.12                        26.08



Table 16 in Appendix E.1 examines whether the benchmark can be solved primarily through standard
Lean automation. The strongest individual tactic, aesop, solves 9.67% of the gaps, while the union
of all evaluated tactics solves 11.20%. Moreover, after removing the 2,925 gaps solved by the tactic
union, the learned provers still achieve Pass@8 scores of 23.57–27.48% on the remaining 23,191
gaps. Their performance is therefore not limited to obligations already handled by the evaluated
standard automation.
The topic-level results in Table 4 show that this difficulty is structured rather than uniform. All
three provers perform best on single-variable functions, limits, and continuity (39.10–44.41%) and
worst on parameter integrals (18.21–20.43%). The identical topic ordering across the three provers
suggests that these differences reflect stable properties of the mathematical obligations rather than
an isolated weakness of one model.

5.3.2      E FFECT OF P ROOF G RANULARITY (RQ2)
Under the same eight-candidate budget per target, per-gap Pass@8 is 31.99–35.39%, whereas
complete-theorem Pass@8 is only 2.92–4.28%. This separation is not caused solely by exercises
with many gaps receiving greater weight. After assigning equal weight to each exercise, Table 5
shows that mean exercise-level gap coverage remains 27.63–31.15%, whereas complete-theorem
Pass@8 is only 2.92–4.28%. Thus, step-level evaluation provides a substantial nonzero signal even
when complete-theorem performance is close to the failure floor.
This comparison is conditional on the context supplied to each gap: the local target retains facts
established earlier in the source solution, whereas the complete theorem must be proved from its
original premises. The result therefore does not show that gap completion is an equivalent but easier
theorem-proving task. Instead, it separates local proof construction from the additional demands
of organizing and completing an end-to-end argument. The parameter-integral results make this
distinction particularly visible: the models solve 18.21–20.43% of the local obligations but at most
1.00% of the corresponding complete theorems.

5.3.3      C ROSS -M ODEL C OMPARISON (RQ3)
Table 7 shows a clear model-class separation on ProofGap-280. Every evaluated general-purpose
model outperforms every specialized prover at the gap level. Even GLM-5.2, the weakest general-


                                                      8
Preprint




Table 6: Local progress among exercises whose complete theorem is not solved at Pass@8. All
values are percentages of theorem-failed exercises.
                               Any gap                         At least                     At least
Model                           solved                          half                         75%
Goedel                            78.03                           22.59                         4.99
DeepSeek                          75.88                           20.24                         4.46
Kimina                            72.39                           18.79                         4.68


Table 7: Pass@k results (%) on ProofGap-280 and its 280 corresponding parent exercises. Each
entry reports proof-gap / parent-exercise performance under an 8,192-token generation budget.
                                                      Proof gap / parent exercise
Model                               Pass@1                      Pass@3                   Pass@8
Specialized Formal Provers
Goedel-V2-8B                      29.74 / 3.97                36.35 / 5.64             39.29 / 7.14
DeepSeek-Prover-7B                30.28 / 4.06                36.77 / 5.33             39.64 / 5.71
Kimina-Distill-8B                 30.15 / 2.41                34.69 / 3.42             35.71 / 4.29
Open-Weight General Models
Kimi-K3                           70.71 / 7.14                76.79 / 8.21             81.07 / 8.93
DeepSeek-V4-Pro                   52.50 / 2.86                62.14 / 4.29             67.50 / 5.00
GLM-5.2                           47.86 / 1.79                61.43 / 2.50             65.00 / 3.21
Proprietary General Models
Claude-Opus-4.8                   77.50 / 8.21                83.93 / 13.21            87.86 / 13.93
GPT-5.6-sol                       79.29 / 12.99               84.97 / 17.61            87.86 / 21.43


purpose model at Pass@8, reaches 65.00%, exceeding the strongest specialized prover at 39.64%
by 25.36 percentage points. This result highlights the substantial recent advances in the formal-
reasoning capabilities of general-purpose language models.
The ranking changes substantially on the corresponding parent exercises. GPT-5.6-sol and Claude-
Opus-4.8 retain clear advantages, and Kimi-K3 is numerically higher than the specialized provers,
whereas DeepSeek-V4-Pro and GLM-5.2 are not. Notably, GPT-5.6-sol and Claude-Opus-4.8 tie at
87.86% on the gaps but obtain 21.43% and 13.93%, respectively, on the parent exercises. Similar
gap-level performance can therefore coexist with markedly different end-to-end proof-construction
ability.

5.3.4      D IAGNOSTIC R ESOLUTION (RQ4)
Table 5 shows that gap coverage is strongly associated with complete-theorem success. Exer-
cises whose theorem is solved have mean gap coverage of 75.07–79.12%, compared with 26.08–
29.19% for theorem-failed exercises. Step-level performance is strongly associated with end-to-end
theorem-proving success, while providing a substantially denser diagnostic signal.
At the same time, theorem failure does not imply an absence of local progress. As shown in Table 6,
72.39–78.03% of theorem-failed exercises contain at least one solved gap, 18.79–22.59% have at
least half of their gaps solved, and 4.46–4.99% have at least three quarters solved. ProofGap there-
fore refines a binary theorem failure into a graded account of how many local formal obligations
associated with the underlying argument a model can discharge under the evaluated budget.




                                                  9
Preprint




6   C ONCLUSION
We introduced ProofGap, a fine-grained benchmark for step-level formal reasoning based on local
proof obligations derived from textbook natural-language solutions. It contains 26,116 gaps from
3,015 mathematical analysis exercises. Experiments show that gaps are substantially more tractable
than complete theorems and reveal local progress hidden by theorem-level failure. These findings
establish local formal proof completion as a useful interface for fine-grained evaluation and formally
grounded diagnostic feedback. The benchmark currently covers one textbook in mathematical anal-
ysis; its proof-assistant evaluation is limited to Lean. It evaluates already formalized gaps inde-
pendently and therefore does not directly measure natural-language autoformalization, invalid-step
detection, or end-to-end proof composition. Future work should extend coverage across domains
and proof assistants and evaluate complete pipelines that jointly address semantic translation, local
proof discharge, and sequential proof composition.

R EFERENCES
Anthropic. Claude Opus 4.8 system card. System card, Anthropic, May 2026. URL https://
  www-cdn.anthropic.com/0b4915911bb0d19eca5b5ee635c80fef830a37ea.
  pdf. Model identifier: claude-opus-4-8; accessed 2026-07-28.
Zhangir Azerbayev, Bartosz Piotrowski, Hailey Schoelkopf, Edward W. Ayers, Dragomir Radev,
  and Jeremy Avigad. Proofnet: Autoformalizing and formally proving undergraduate-level math-
  ematics, 2023. URL https://arxiv.org/abs/2302.12433.
Yves Bertot and Pierre Castéran. Interactive theorem proving and program development: Coq’Art:
  the calculus of inductive constructions. Springer Science & Business Media, 2013.
Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde De Oliveira Pinto, Jared
 Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, et al. Evaluating large
 language models trained on code, 2021. URL https://arxiv.org/abs/2107.03374.
Leonardo de Moura and Sebastian Ullrich. The lean 4 theorem prover and programming language.
  In International Conference on Automated Deduction, pp. 625–635. Springer, 2021.
DeepSeek-AI, Anyi Xu, Bangcai Lin, Bing Xue, et al. Deepseek-v4: Towards highly efficient
  million-token context intelligence, 2026. URL https://arxiv.org/abs/2606.19348.
Boris Pavlovich Demidovich. Problems in Mathematical Analysis. Gordon and Breach, New York,
  1969.
Dinghui Fei and Xuesheng Zhou. Solutions to B. P. Demidovich’s Problems in Mathematical Anal-
  ysis. Shandong Science and Technology Press, Jinan, China, 4 edition, 2012. Six volumes, in
  Chinese.
GLM-5-Team. Glm-5: from vibe coding to agentic engineering, 2026. URL https://arxiv.
 org/abs/2602.15763.
Thomas Hubert, Rishi Mehta, Laurent Sartran, Miklós Z Horváth, Goran Žužić, Eric Wieser, Aja
  Huang, Julian Schrittwieser, Yannick Schroecker, Hussain Masoom, et al. Olympiad-level formal
  mathematical reasoning with reinforcement learning. Nature, 651(8106):607–613, 2026.
Ryo Kamoi, Yusen Zhang, Nan Zhang, Sarkar Snigdha Sarathi Das, Ranran Haoran Zhang, Wen-
  peng Yin, and Rui Zhang. Efficient prm training data synthesis via formal verification. In Findings
  of the Association for Computational Linguistics: ACL 2026, pp. 8246–8265, 2026.
Kimi Team. Kimi k3: Open frontier intelligence, 2026. URL https://arxiv.org/abs/
  2607.24653.
Hunter Lightman, Vineet Kosaraju, Yuri Burda, Harrison Edwards, Bowen Baker, Teddy Lee, Jan
  Leike, John Schulman, Ilya Sutskever, and Karl Cobbe. Let’s verify step by step. In The Twelfth
  International Conference on Learning Representations, 2024. URL https://openreview.
  net/forum?id=v8L0pN6EOi.


                                                 10
Preprint




Yong Lin, Shange Tang, Bohan Lyu, Ziran Yang, Jui-Hui Chung, Haoyu Zhao, Lai Jiang, Yihan
  Geng, Jiawei Ge, Jingruo Sun, Jiayun Wu, Jiri Gesi, Ximing Lu, David Acuna, Kaiyu Yang,
  Hongzhou Lin, Yejin Choi, Danqi Chen, Sanjeev Arora, and Chi Jin. Goedel-prover-v2: Scaling
  formal theorem proving with scaffolded data synthesis and self-correction. In The Fourteenth
  International Conference on Learning Representations, 2026. URL https://openreview.
  net/forum?id=j4C0nALrgK.
Chengwu Liu, Ye Yuan, Yichun Yin, Yan Xu, Xin Xu, Zaoyu Chen, Yasheng Wang, Lifeng Shang,
  Qun Liu, and Ming Zhang. Safe: Enhancing mathematical reasoning in large language models
  via retrospective step-aware formal verification. In Proceedings of the 63rd Annual Meeting of
  the Association for Computational Linguistics (Volume 1: Long Papers), pp. 12171–12186, 2025.
Tobias Nipkow, Markus Wenzel, and Lawrence C Paulson. Isabelle/HOL: a proof assistant for
  higher-order logic. Springer, 2002.
OpenAI.    GPT-5.6 system card. System card, OpenAI, July 2026. URL https://
  deploymentsafety.openai.com/gpt-5-6. Includes the gpt-5.6-sol model; ac-
  cessed 2026-07-28.
Lushi Pu, Weiming Zhang, Xinheng Xie, Zixuan Fu, Bingxiang He, Hongya Lyu, Xin Li, Jie Zhou,
  and Yudong Wang. Ma-proofbench: A two-tiered evaluation of llms for theorem proving in
  mathematical analysis, 2026. URL https://arxiv.org/abs/2606.13782.
Z. Z. Ren, Zhihong Shao, Junxiao Song, Huajian Xin, Haocheng Wang, Wanjia Zhao, Liyue
  Zhang, Zhe Fu, Qihao Zhu, Dejian Yang, Z. F. Wu, Zhibin Gou, Shirong Ma, Hongxuan Tang,
  Yuxuan Liu, Wenjun Gao, Daya Guo, and Chong Ruan. Deepseek-prover-v2: Advancing for-
  mal mathematical reasoning via reinforcement learning for subgoal decomposition, 2025. URL
  https://arxiv.org/abs/2504.21801.
George Tsoukalas, Jasper Lee, John Jennings, Jimmy Xin, Michelle Ding, Michael Jennings, Ami-
  tayush Thakur, and Swarat Chaudhuri. Putnambench: Evaluating neural theorem-provers on the
  putnam mathematical competition. In The Thirty-eight Conference on Neural Information Pro-
  cessing Systems Datasets and Benchmarks Track, 2024. URL https://openreview.net/
  forum?id=ChKCF75Ocd.
Haiming Wang, Mert Unsal, Xiaohan Lin, Mantas Baksys, Junqi Liu, Marco Dos Santos, Flood
  Sung, Marina Vinyes, Zhenzhe Ying, Zekai Zhu, Jianqiao Lu, Hugues de Saxcé, Bolton Bailey,
  Chendong Song, Chenjun Xiao, Dehao Zhang, Ebony Zhang, Frederick Pu, Han Zhu, Jiawei Liu,
  Jonas Bayer, Julien Michel, Longhui Yu, Léo Dreyfus-Schmidt, Lewis Tunstall, Luigi Pagani,
  Moreira Machado, Pauline Bourigault, Ran Wang, Stanislas Polu, Thibaut Barroyer, Wen-Ding
  Li, Yazhe Niu, Yann Fleureau, Yangyang Hu, Zhouliang Yu, Zihan Wang, Zhilin Yang, Zhengying
  Liu, and Jia Li. Kimina-prover preview: Towards large formal reasoning models with reinforce-
  ment learning, 2025. URL https://arxiv.org/abs/2504.11354.
Peiyi Wang, Lei Li, Zhihong Shao, Runxin Xu, Damai Dai, Yifei Li, Deli Chen, Yu Wu, and Zhifang
  Sui. Math-shepherd: Verify and reinforce llms step-by-step without human annotations. In Pro-
  ceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume
  1: Long Papers), pp. 9426–9439, 2024.
Xiao-Wen Yang, Zihao Zhang, Jianuo Cao, Zhi Zhou, Zenan Li, Lan-Zhe Guo, Yuan Yao, Taolue
  Chen, Yu-Feng Li, and Xiaoxing Ma. Formalml: A benchmark for evaluating formal subgoal
  completion in machine learning theory, 2025. URL https://arxiv.org/abs/2510.
  02335.
Zhouliang Yu, Ruotian Peng, Keyi Ding, Yizhe Li, Zhongyuan Peng, Minghao Liu, Yifan Zhang,
  Zheng Yuan, Huajian Xin, Wenhao Huang, Yandong Wen, Ge Zhang, and Weiyang Liu. For-
  malmath: Benchmarking formal mathematical reasoning of large language models, 2025. URL
  https://arxiv.org/abs/2505.02735.
Kunhao Zheng, Jesse Michael Han, and Stanislas Polu. Minif2f: a cross-system benchmark for
  formal olympiad-level mathematics, 2022. URL https://arxiv.org/abs/2109.00110.



                                              11
Preprint




A     DATASET C ONSTRUCTION D ETAILS
A.1    DATA S OURCES AND P REPROCESSING

The raw corpus for ProofGap comes from the natural-language problems and solutions in B. P.
Demidovich’s Problems in Mathematical Analysis. The book covers topics in mathematical analysis
such as functions and limits, differentiation, integration, series, multivariable analysis, parameter
integrals, and line and surface integrals. Its solutions usually have a clear step-by-step structure,
making them suitable as input to the RNFL pipeline.
Before entering the autoformalization process, the raw text is lightly preprocessed. First, we re-
move problems whose understanding necessarily depends on figures, tables, or external geometric
intuition. Second, we split problems containing multiple mutually independent subquestions into
multiple samples, so that each sample corresponds to a clear problem statement and solution pro-
cess. Finally, we normalize the boundaries between problems and solutions, preventing subsequent
problems or residual formatting artifacts from being mixed into the same sample.
These procedures do not change the mathematical reasoning content of the original solutions. In-
stead, they provide structurally clear input for the subsequent Relaxed NFL translation, elaboration,
and proof-gap generation.

A.2    R ELAXED NFL R EPRESENTATION AND AUTOMATIC T RANSLATION

This section explains how natural-language solutions are first represented as Relaxed NFL. Relaxed
NFL is an intermediate representation between a natural-language solution and Core NFL. It remains
close to natural mathematical writing but has a formal syntax, so it can be read by a parser and
processed further. Its role is not to serve directly as the final verification target, but to provide a
surface language that is easier for large language models to generate while still preserving proof
structure.

           Table 8: Representative natural-language structures preserved by Relaxed NFL.
Natural-language           Relaxed NFL form                   Role
structure

Known condition            GIVEN                              Records problem premises.
Goal to prove              TO PROVE                           Records the current proof goal.
Problem-solving entry      Solve                              Records the object, solution set, or range
                                                              to be found.
Intermediate conclusion    Have P                             Aligns with a natural-language proof step.
Local assumption           Assume P { ...      }              Represents conditional reasoning or a
                                                              nested subproof.
Sufficiency                It suffices to prove P             Represents backward reasoning.
transformation
Local proof of an          We prove that P { ...         }    Generates local proof gaps for P and then
intermediate proposition                                      makes P available as an assumption.
Candidate answer and       Take t as a witness                Records a candidate object and the
checking                   After checking, t                  verification of its constraints.
                           satisfies
                           the constraints
Method annotation          [@method M @]                      Preserves proof-search hints from the
                                                              source solution.

Relaxed NFL resembles natural-language proofs in two main respects. First, it preserves common
reasoning structures in informal proofs, such as stating intermediate conclusions, reasoning under
local assumptions, transforming the goal, and giving method hints. Second, it permits some terms
and propositions to remain not fully elaborated. For example, surface notation such as f ′ , |x|, and
an , as well as variable scopes introduced by expressions such as “take arbitrary x” or “let x,” may
first be preserved in Relaxed NFL and then recovered precisely in later stages.


                                                   12
Preprint




In the ProofGap construction, Relaxed NFL preserves at least the structures shown in Table 8.
A simplified grammar fragment is as follows:

 <program> ::= <assumptions> Prove: <term> Proof: <proof>
             | <assumptions> Solve: <solving_step>
               Solution: <derivation>

 <proof> ::= <derivation> QED

 <derivation> ::= <annotated_step>*

 <annotated_step> ::= ([@method <method> @])? <step>

 <step> ::= Have <term>
          | <action_step>
          | It suffices to prove <term>
          | We prove that <term> { <proof> }
          | Assume <term> { <derivation> }
          | <solving_step> { <derivation> }

 <action_step> ::= Set <term> = <term>
                 | Take <term> as a witness
                 | After checking, <term> satisfies the constraints
                 | After checking, <term> does not satisfy the
   constraints

 <solving_step> ::= Find <term> such that <term>
                  | Find all <term> such that <term>
                  | Find the range of <term> such that <term>


This design makes Relaxed NFL more like a structured natural proof than a language for a particular
proof assistant. It reduces the difficulty of the autoformalization stage while preserving enough
proof-structural information for the subsequent Core NFL elaboration.
Based on the surface language above, natural-language problems and solutions are translated into
Relaxed NFL. We use prompting-based translation: the prompt contains the syntax specification of
Relaxed NFL, target-format requirements, and several examples from natural language to Relaxed
NFL, so that the model learns to preserve proof structure rather than directly generating strict proof
assistant code.
After generation, Relaxed NFL is passed through two types of filtering. The first is parser validation,
which ensures that the generated text satisfies the syntactic constraints of Relaxed NFL and can be
read by downstream programs. The second is representation-consistency screening, which filters
results that are clearly inconsistent with the source solution. The screening focuses on the following
points:

      1. whether the main assumptions in the problem appear in GIVEN or in the corresponding
         local contexts;
      2. whether the original goal is correctly translated as TO PROVE or Solve;
      3. whether the main proof steps in the natural-language solution are represented by Have,
         Assume, We prove that, or It suffices to prove;
      4. whether Relaxed NFL introduces key intermediate conclusions that have no basis in the
         source solution;
      5. whether method annotations are broadly consistent with the corresponding natural-
         language steps.

This screening does not claim to prove that the natural-language solution and Relaxed NFL are
equivalent in full mathematical semantics. Its purpose is closer to sanity checking: filtering structural
errors, syntax errors, and clearly misaligned translations. Full verification does not occur at the


                                                   13
Preprint




Relaxed NFL stage, but is realized through the subsequent Core NFL elaboration and proof-gap
checking.

A.3   C ORE NFL R EPRESENTATION AND V ERIFIABLE E LABORATION

We first give the surface structure of Core NFL and the corresponding organization of proof states.
Core NFL is the normalized representation obtained after elaborating Relaxed NFL. Unlike Relaxed
NFL, which is closer to natural proof writing, Core NFL requires proof steps to eventually be re-
duced to a small number of primitive proof constructors. This allows the proof-gap generator to
maintain proof state uniformly along the proof AST and generate proof gaps. We then describe
several finer-grained elaboration procedures used in the transition from Relaxed NFL to Core NFL.
Abstractly, Core NFL can be viewed as consisting of two syntactic categories:
                                       Term     and    Method,
where Term denotes mathematical expressions or propositions in Core NFL, and Method denotes
proof methods. The special method ?M denotes the empty method.
A proof state consists of the current sequence of assumptions and the current goal:
                                      PState = Term∗ × Term.
If the current assumptions are Γ and the goal is G, the proof state is written as
                                               Γ ⊢ G.

A Core NFL proof consists of a small number of primitive proof constructors:
                                  Proof ::= Forward(M, P, π)
                                             | Backward(M, P, π)
                                             | Subgoal(P, π1 , π2 )
                                             | QED.

The meanings of these constructors and their corresponding Relaxed NFL structures are shown in
Table 9.

           Table 9: Primitive Core NFL proof constructors and their Relaxed NFL origins.
Core NFL constructor           Typical Relaxed NFL             Meaning
                               structure

Forward(M, P, π)               [@method M] Have P              Derives an intermediate proposition P
                                                               from the current proof state using method
                                                               M , and adds P to the subsequent
                                                               assumptions.
Backward(M, P, π)              [@method M] It                  Reduces the current goal to the subgoal P
                               suffices to prove P             using method M , then continues by
                                                               proving P .
Subgoal(P, π1 , π2 )           We prove that P { ...           First proves the intermediate subgoal P
                               }                               with π1 , then uses P as a known fact in π2 .
QED                            QED                             Ends the current proof, indicating that the
                                                               current goal follows from the current
                                                               assumptions.


Thus, a Core NFL program can be regarded as
                                    Program = PState × Proof.

The Core NFL column in Figure 1 of the main paper displays a readable surface form of this structure
in data construction: it has already made variable scopes, local conditions, and context-dependent


                                                  14
Preprint




notation explicit, and can be consumed by the proof-gap generator. Internally, the system does not
treat it as an ordinary text sequence, but parses it into a proof AST consisting of the proof-state
structure and primitive proof constructors described above.
The definitions above explain how the main proof steps in Relaxed NFL are reduced to the core
constructors required by Core NFL. In actual construction, finer-grained elaboration is also needed,
such as recovering implicit variable scopes, eliminating ambiguities in context-dependent notation,
splitting compound propositions, and normalizing derivative and integral notation in mathematical
analysis. These processes are mainly performed by deterministic transformations. In the few places
where the intent of the original natural-language proof must be judged, the system uses constrained
LLM heuristics and requires the output to pass programmatic checks. We give several representative
types of elaboration below.

A.3.1      N OTATION D ISAMBIGUATION
A common source of ambiguity in natural mathematical writing is notation overloading: the same
symbol may denote different mathematical objects. A simple example is |x|. Depending on the
meaning of x, it may denote either the absolute value of a real number or the cardinality of a set.
Therefore, the surface notation |x| in Relaxed NFL cannot by itself be automatically fixed as a
particular Core NFL term.
To perform notation disambiguation, the system preserves overloaded notation in the term language
of Relaxed NFL while introducing unambiguous forms and auxiliary annotations:

 <term> ::= ...
          | |<term>|
          | IsReal(<term>)
          | IsSet(<term>)
          | Abs(<term>)
          | Card(<term>)


Here, |.| is overloaded surface notation, while Abs(.) and Card(.) are unambiguous forms
that can be deterministically translated to Core NFL. The annotations IsReal(.) and IsSet(.)
record whether a term is regarded as a real number or as a set. They are not a static type system for
Relaxed NFL, but annotations used to guide the interpretation of overloaded notation.
The elaborator performs static analysis over Relaxed NFL and maintains an environment recording
these annotations. The annotations may come from two sources. The first is information explic-
itly preserved by the model during the initial autoformalization stage; for example, “for every real
number t” introduces IsReal(t). The second is constraint propagation performed by the system
according to operator signatures; for example, when an operator requires a set argument, an IsSet
annotation is generated for the corresponding object. When the environment determines a unique
interpretation, the system directly replaces the overloaded notation:
                                      |t| 7→ Abs(t) if IsReal(t),
                                      |t| 7→ Card(t) if IsSet(t).
If multiple candidate interpretations remain after static constraints are applied, the system gives the
model only the local proof context and a finite candidate set, asks it to select the intended interpre-
tation, and then checks whether the choice is consistent with the current constraint environment.
The same disambiguation mechanism is also used for other context-dependent notation in mathe-
matical analysis. For example, f ′ must be interpreted as a function derivative or some other derived
object; an may denote the n-th term of a sequence, or a partial derivative of a function or multi-
variate object with respect to n; and f −1 may denote an inverse function, a matrix inverse, or an
ordinary power of −1. The system selects the interpretation using the local object category, operator
signatures, and contextual constraints, and uses constrained candidate selection when needed.

A.3.2      S PLITTING C HAINED E QUALITIES AND C OMPOUND P ROPOSITIONS
Natural-language proofs often compress several atomic relations into a single compound proposi-
tion, such as a chained inequality, a chained equality, or a conjunction. Relaxed NFL may pre-


                                                  15
Preprint




serve this writing style.However, when generating proof gaps, a compound proposition that is too
large mixes multiple local inferences into the same goal, making it difficult to obtain fine-grained
step-level obligations. Therefore, elaboration normalizes such compound structures into smaller
verification units:


                   Have a < b < c ⇝ Have a < b, Have b < c,             Have a < c,
                   Have a = b = c ⇝ Have a = b, Have b = c,             Have a = c,
                     Have P ∧ Q ⇝ Have P, Have Q.
This transformation does not perform proof search, nor does it try to prove the individual subproposi-
tions. It only unfolds surface-level compound propositions into more explicit Core NFL steps. After
expansion, each subproposition can generate an independent proof gap under the current proof state.
This preserves the locality of the original proof step while making error localization more precise.

A.3.3      R ECOVERING I MPLICIT VARIABLE S COPE
Relaxed NFL permits temporarily unbound variables to appear in proof steps. For example, Have
P(x) only states that the current step claims P (x), but it does not yet specify whether x is an
arbitrary real number, a fixed object, or a variable satisfying some local conditions. Core NFL needs
such implicit scopes to be made explicit; otherwise, the generated proof gap lacks complete context.
For this purpose, the system first marks free variables in propositions with [@free ... @], and
then marks the implicit scope these variables should inhabit with [@scope ... @]. The scope
annotation is then eliminated and converted into explicit quantifiers and conditions in Core NFL.
For example:

 Free-variable annotation:
 [@free x @] Have P(x)

 Scope annotation:
 [@scope [forall x] [x in Real] @] {
   Have P(x)
 }

 After scope elimination:
 Have forall (x), x in Real =>
   P(x)


Here, [@free x @] indicates that x has not yet been explicitly bound by the current proposition,
while [@scope [forall x] [x in Real] @] indicates that the step should be interpreted
as holding “for every real number x.” The model output for this step must pass a deterministic
checker: all annotated free variables must fall within matching scopes, and apart from adding and
eliminating scope annotations, no other part of the proof may be modified.

A.3.4      C ANONICALIZING D ERIVATIVES AND I NDEFINITE I NTEGRALS
Because ProofGap targets mathematical analysis, it also needs a unified internal canonical form for
derivatives and indefinite integrals. The goal here is not to execute differentiation or integration, but
to translate surface notation in natural writing into semantically explicit Core NFL terms without
free variables.
Derivatives are uniformly represented as
                                            FunDeri(f, g, n),
denoting the n-th derivative of function f with respect to function g. In this way, ordinary deriva-
tives, partial derivatives, higher-order derivatives, and derivatives with respect to a composite func-
tion can all be placed in the same canonical form. For example, the derivative of sin(x) with respect
to cos(x),
                                                d(sin x)
                                                         ,
                                                d(cos x)

                                                   16
Preprint




is written in Core NFL as
                                  FunDeri(λx. sin x, λx. cos x, 1).

As another example, for the second-order partial derivative of a binary function f (x, y) with respect
to y, the natural notation
                                            ∂ 2 f (x, y)
                                                ∂y 2
can first be represented as
                                     FunDeri(f, λx, y. y, 2).
Since λx, y. y selects only the second formal parameter, this representation can also be written in a
more readable form:
                                    FunDeri(λx, y. f (x, y), 2, 2).
These two Core NFL terms have the same semantics; the latter only displays “differentiate with
respect to the second formal parameter” more concisely.
The canonicalization of indefinite integrals is based on another consideration: an indefinite integral
denotes a family of antiderivatives, not a single function value. For example, the natural notation
                                         Z
                                             2x dx = x2 + C

is represented in Core NFL as an equality between two sets of functions:
          { F | ∀x, FunDeri(F, 1, 1)(x) = 2x } = { F | ∃C ∈ R, ∀x, F (x) = x2 + C }.
                                           R
This treatment is necessary: the result of 2x dx is not a fixed function, but the set of all functions
satisfying F ′ (x) = 2x; the right-hand side x2 + C also denotes a family of functions parameterized
by an arbitrary real constant C. Thus, in Core NFL, an equality of indefinite integrals is naturally
represented as an equality between two sets of functions.

A.4   P ROOF -G AP G ENERATION AND C HECKING

After verifiable elaboration, the semantics of Core NFL is given by proof-gap generation. That is,
we do not interpret a Core NFL program directly as a complete proof object; instead, we interpret
it as a process that generates verification conditions. If all generated proof gaps are successfully
proved, then the Core NFL program is regarded as verified.
A proof gap consists of a proof state and a method:
                                     Gap = PState × Method.
If the proof state is Γ ⊢ G and the method annotation is M , the gap is written as
                                              Γ ⊢M G.
It means: under assumptions Γ, prove the goal G. The method M is a hint preserved from the
natural-language solution and does not change the formal validity of the proof obligation.
The proof-gap generator PGG is defined recursively according to the structure of the Core NFL
proof. Let Γ; P denote appending proposition P to the end of the assumption sequence. The gener-
ation rules are:
             PGG(Γ ⊢ G, Forward(M, P, π)) = { Γ ⊢M P } ∪ PGG(Γ; P ⊢ G, π),
           PGG(Γ ⊢ G, Backward(M, P, π)) = { Γ; P ⊢M G } ∪ PGG(Γ ⊢ P, π),
            PGG(Γ ⊢ G, Subgoal(P, π1 , π2 )) = PGG(Γ ⊢ P, π1 ) ∪ PGG(Γ; P ⊢ G, π2 ),
                       PGG(Γ ⊢ G, QED) = { Γ ⊢?M G }.

This definition explains why ProofGap is a local benchmark: every gap comes from a proof con-
structor in Core NFL rather than from an arbitrary subgoal extracted from a complete theorem. An
intermediate step in the natural-language solution corresponds to a proof-state transition in Core
NFL and is then expanded into a local proof obligation.


                                                 17
Preprint




Furthermore, we define
                                  CheckGap : Gap → {false, true},
and                                                    ^
                         CheckProgram(σ, π) =                  CheckGap(H).
                                                  H∈PGG(σ,π)

In this benchmark, CheckGap can be implemented through two compatible interfaces: the proof-
checking framework over the lightweight ProofGap representation, and the corresponding Lean the-
orem skeleton. During evaluation, a model must generate, for each proof gap, a formal derivation
accepted by the selected interface.

A.5   P ROOF G AP DATA F IELDS AND L EAN S KELETON E XPORT

A released ProofGap instance expands the sequent form above into data fields:

 ASSUM:
   Gamma

 GOAL:
   G

 METHOD:
   M


The METHOD field is optional. It records strategy hints from the source natural-language solution,
such as “differentiate both sides,” “by monotonicity,” or “compare coefficients.” It is withheld in all
reported evaluations and released for future analyses of strategy-conditioned proving.
Since each ProofGap sample already contains explicit local assumptions and a goal, it can be ex-
ported relatively directly as a Lean theorem skeleton. The Lean version and the lightweight Proof-
Gap representation are two compatible interfaces for the same local proof obligation: the former
supports manual inspection, reuse, and connection to the ecosystem of existing interactive theorem
provers, while the latter provides a compact benchmark-native representation.
For example, the following ProofGap:

 ASSUM:
 DiffableFunc(f)
 forall x, EvenFunc(f) => f(x)=f(-x)

 GOAL:
 forall x, EvenFunc(f)
   => FunDeri(f,1,1)(x)= -FunDeri(f,1,1)(-x)

 METHOD:
 differentiate both sides


can be exported as the following Lean theorem skeleton:




                                                  18
Preprint




 theorem gap2
     (f : Real -> Real)
     (h1 : Differentiable Real f)
     (h2 : forall x : Real, Function.Even f
       -> f x = f (-x)) :
     forall x : Real, Function.Even f ->
       deriv f x = -deriv f (-x) := by
   sorry


This export is mainly structural: ProofGap has already split the local proof obligation into ASSUM
and GOAL, so exporting a Lean skeleton only requires translating each assumption into a theorem
parameter and placing the goal in the conclusion position of the theorem. In the example above,
DiffableFunc(f) is exported as the differentiability premise h1, the local fact forall x,
EvenFunc(f) => f(x)=f(-x) is exported as premise h2, and GOAL becomes the theorem
conclusion. Thus, the Lean form and the lightweight ProofGap form are not different tasks, but two
representations and checking interfaces for the same proof-gap instance.

A.6   Q UALITY C ONTROL AND T RACEABILITY

Before a sample enters the final benchmark, it must pass several layers of programmatic checks:

      1. the boundaries of the natural-language problem and solution are clear, and the sample does
         not depend on unrecoverable graphical information;
      2. Relaxed NFL can be parsed by the parser;
      3. Relaxed NFL has basic proof-structure consistency with the source solution;
      4. elaboration from Relaxed NFL to Core NFL completes successfully;
      5. free-variable annotations and scope annotations have been eliminated, and the binding-
         completeness check passes;
      6. Core NFL can generate nonempty, parseable ASSUM and GOAL fields.

These checks cannot guarantee that the autoformalized result is absolutely correct in full mathemat-
ical semantics, but they keep the construction process controlled and verifiable. Relaxed NFL serves
as an intermediate representation aligned with natural language, Core NFL provides a semantically
explicit proof-state structure, and proof gaps turn the correctness of a complete proof into a set of
locally checkable verification conditions. It is important to emphasize that the entire construction
process operates on syntax trees generated by the parser: elaboration transforms the Relaxed NFL
AST, while the proof-gap generator maintains proof state and generates proof obligations along the
Core NFL proof AST. Therefore, each proof gap preserves its generation position in the proof AST
and can be mapped back to the corresponding local proof step in the source solution.

B     V ERIFICATION F RAMEWORK AND AGENT BASELINE
This appendix expands the compact framework description in the main paper. It records the com-
plete DSL command inventory, the checker’s operational trust boundary, explicit solver coverage,
theorem-instantiation protocol, and the controller used by the verifier-guided baseline. The pur-
pose is to make successful certificates replayable and the system’s failure modes explicit without
enlarging the main-paper presentation.

B.1   DSL C OMMAND I NVENTORY

The DSL contains 18 commands, grouped in Table 10. Its granularity lies between an end-to-end
formal proof and an unconstrained natural-language step: one instruction performs a recognizable
reasoning operation, while the checker validates its exact effect. In particular, autosolve is itself
a DSL command rather than an external preprocessing step. Automation can receive either every
local hypothesis or an explicit model-selected subset; explicit selection records the dependencies of
a step and limits accidental reliance on irrelevant context.


                                                 19
Preprint




        Table 10: The 18 DSL commands, organized by their role in proof-gap completion.
Command family       Commands                               Effect on the proof state

Discharge            autosolve, apply                       Close the goal with a solver or reduce it to
                                                            the unmatched premises of an applicable
                                                            hypothesis.
Fact management      get prop, use condition,               Instantiate a hypothesis or theorem,
                     assert, destruct and                   eliminate implication premises, establish a
                                                            checked local claim, or decompose a
                                                            conjunction.
Quantifiers and      exists, get exists,                    Provide witnesses, open quantified
implications         get forall, get condition              hypotheses or goals, and move an
                                                            antecedent from a goal into the local
                                                            context.
Rewriting and        autoreplace, not normalize,            Perform checked transformations, including
normalization        rewrite, rewrite in limit,             binder-aware rewriting under limits, sums,
                     rewrite in sum, rewrite in             and set comprehensions.
                     setdesc
Branching            case analysis, or intro                Split on a disjunctive hypothesis or select a
                                                            side of a disjunctive goal.



Surface syntax. Programs are line-oriented; formulas are enclosed in braces, hypotheses carry
explicit indices, and a hash mark starts a comment. The following schematic forms summarize the
complete command surface. Here source and result are a hypothesis or the goal, dir is a
rewrite direction, and ellipses denote repeated binders or hypotheses rather than unchecked text.

 autoreplace <scope>; from <term> to <term>; from <source> to <result>
 not_normalize from (GOAL: {...}) to (GOAL: {...})
 autosolve all_hypothesis
 autosolve (hypothesis <i>: {...}) ...
 get_prop (<hypothesis-or-theorem>) (<x> := {...}) ... as (hypothesis
   <j>: {...})
 exists (<x> := {...}) ...
 destruct_and (hypothesis <i>: {...}) as (hypothesis <j>: {...}) ...
 rewrite (<dir>, <equation-or-iff>) (hypothesis <i>: {...}); from
   <source> to <result>
 rewrite_in limit (<dir>, equation) (hypothesis <i>: {...}); from
   <source> to <result>
 rewrite_in sum (<dir>, equation) (hypothesis <i>: {...}); from
   <source> to <result>
 rewrite_in setdesc (<dir>, equation) (hypothesis <i>: {...}) (<x> :=
   {...}); from <source> to <result>
 apply (hypothesis <i>: {...})
 use_condition (<condition>) ... in (hypothesis <i>: {...}) as
   (hypothesis <j>: {...})
 get_exists (hypothesis <i>: {...}) (<x> := {...}) ...
 get_forall (GOAL: {...}) (<x> := {...}) ...
 get_condition (hypothesis <j>: {...}) ... in (GOAL: {...})
 assert (hypothesis <j>: {...}) [by proof { ... }]
 case_analysis (hypothesis <i>: {...})
 or_intro <left-or-right>



Command-level semantics.       The checker assigns the following precise state transition to each
command.

      1. autoreplace. Recompute a supported local transformation in a hypothesis or the goal,
         using no hypotheses, all hypotheses, or an explicit subset. The command states the replaced


                                                20
Preprint




          term, its replacement, the complete source formula, and the claimed result; an arbitrary
          user-written substitution is not trusted.
       2. not normalize. Replace only the goal, and only when the old and new forms have
          α-equivalent fully unfolded negation normal forms. The command rejects a no-op and
          invokes neither general automation nor linear arithmetic.
       3. autosolve. Close the current goal only when the deterministic solver portfolio certifies
          it from all hypotheses or the explicitly selected subset. Thus autosolve is an ordinary
          DSL instruction whose success can be replayed.
       4. get prop. Instantiate outer universal binders of a hypothesis or a named library theo-
          rem and add the checked instance as a new hypothesis. The checker requires enough outer
          binders, performs capture-avoiding simultaneous substitution and beta reduction, and com-
          pares the supplied result modulo α-equivalence.
       5. exists. Supply witnesses for one or more consecutive outer existential binders of the
          goal. The stated binder names must match those binders, and the residual goal is recom-
          puted by the checker.
       6. destruct and. Recursively flatten a conjunctive hypothesis. The number and order of
          explicitly named output hypotheses must exactly match all flattened conjuncts.
       7. rewrite. Apply a directed equation or biconditional from a hypothesis to a goal or
          hypothesis. It checks the complete before and after formulas and does not cross a protected
          binder. A rewrite rule still wrapped in an outer quantifier must first be instantiated.
       8. rewrite in limit. Rewrite one selected limit body using a hypothesis with exactly
          one outer universal binder and an equation conclusion. A conditional rule must hold even-
          tually in the relevant punctured, one-sided, or infinite neighborhood.
       9. rewrite in sum. Rewrite one selected summand with the same single-binder equation
          form, after proving the rule condition for every index in the entire finite or supported infinite
          summation range.
      10. rewrite in setdesc. Rewrite within one selected set comprehension using an ex-
          plicit map from the rule binder to the set binder. The side condition may use unaffected
          local set conditions but not the very condition being rewritten.
      11. apply. Close a matching goal or reduce it to the unmatched prefix of premises of an
          implication chain. Any resulting premises remain explicit proof obligations.
      12. use condition. Discharge an ordered prefix of an implication hypothesis and add the
          residual implication or conclusion as a new hypothesis. Each premise is supplied by a
          matching hypothesis or by an obvious fact that is itself checked.
      13. get exists. Open consecutive outer existentials in a hypothesis using fresh names and
          update that hypothesis in place.
      14. get forall. Open consecutive outer universal binders of the goal using fresh names and
          replace the goal with the checked body.
      15. get condition. Move an ordered prefix of goal antecedents into the local context under
          explicitly assigned fresh hypothesis indices.
      16. assert. Add an intermediate proposition only after it is discharged either by automa-
          tion or by a nonempty nested DSL proof. The nested proof receives a copy of the outer
          assumptions; hypotheses made inside it cannot leak into the outer state.
      17. case analysis. Split a disjunctive hypothesis into one active proof gap for each recur-
          sively exposed disjunct. Acceptance requires every resulting branch to close.
      18. or intro. Select the left or right side of a binary disjunctive goal and replace the goal by
          that selected proposition.

B.2    C HECKER S EMANTICS AND T RUST B OUNDARY

The checker implements the operational semantics of these commands as deterministic proof-state
transitions. Commands that transform a formula state both the source and intended result; the
source must match the current state, and the checker recomputes or validates the claimed change.


                                                    21
Preprint




Quantifier instantiation uses capture-avoiding substitution and compares expressions modulo α-
equivalence. Fresh-variable and hypothesis-index constraints make the execution trace unambigu-
ous. The assert command may contain a nested DSL program, but facts created inside that local
proof do not escape; only its checked conclusion is added to the outer state. Acceptance requires
every active goal to close, so a program cannot leave a case-analysis branch or local assertion unfin-
ished.
Rewriting beneath implicit binders receives additional checks. Ordinary rewrite is binder pro-
tecting; the three rewrite in commands are explicit, scoped exceptions. Their rule must be a
hypothesis with exactly one outer universal binder and an equation conclusion. Before substitution,
conflicting binders are α-renamed, and a candidate rule instance that depends on a binder introduced
locally by the rule is rejected. Every unchanged sibling, binder, limit point, summation bound, and
set condition must remain α-equivalent, so algebraic normalization cannot be hidden as an addi-
tional rewrite. Equality must hold eventually in the relevant neighborhood for a limit, at every
index—including initial indices—for a sum, or under the unaffected local conditions of a set com-
prehension. Excluding the condition currently being rewritten prevents a circular, self-justifying set
rewrite. These checks are particularly important in analysis, where an otherwise plausible rewrite
may capture a variable or omit a domain condition.
The parser, checker, and solver have distinct failure contracts. A parse error produces no proof
state; an illegal transition leaves the current state unaccepted; and a solver that cannot establish its
obligation produces no certificate. In particular, unsupported solver input is reported as unknown.
Execution reports the first failed command together with the remaining local context and goal. Thus
syntax failures, unsupported automation, unfinished branches, and mathematically invalid transi-
tions remain separable in downstream analysis.

B.3    S OLVER P ORTFOLIO AND C APABILITY B OUNDARIES

The DSL command autosolve invokes a portfolio of specialized, deterministic solvers over the
selected hypotheses. Selected backends may also be requested explicitly; for example, the interface
exposes LimitCalcSolver. An unsupported expression is reported as unknown; an unresolved
side condition or exhausted bounded search likewise produces no certificate. This conservative
contract permits composition without turning an unsupported expression into a proof.

Table 11: Major solver families and their supported fragments; the table does not claim completeness
for the corresponding mathematical theories.
Capability family       Representative solvers                 Supported reasoning

Logical and structural EqbSolver, Reflexivity,                 Hypothesis matching modulo
                       NotUnfoldSolver,                        α-equivalence, reflexive relations,
                       FunctionApplySolver                     negation normalization, beta reduction,
                                                               definition unfolding, and deterministic
                                                               piecewise-function evaluation.
Domains and             ConstTypeSolver,                       Membership in standard number sets,
constants               DomainTypeSolver, shared               closure under contextual type facts, and
                        exact-numeric analysis                 exact evaluation of closed constants
                                                               subject to definedness checks.
Algebra and             PolyRatSolver,                         Polynomial and rational identities, root
inequalities            RootFracSolver,                        and fraction normalization, sign
                        RootPowerSolver,                       propagation, linear arithmetic, interval
                        SgnPureSolver/SgnSolver,               reasoning, and bound propagation.
                        IntervalSolver,
                        SqueezeSolver, SmtLraSolver
Calculus and analysis   DerivSolver,                           Symbolic derivatives, elementary
                        ContinuousFuncSolver,                  continuity, integrability on finite closed
                        IntegrableFuncSolver,                  intervals, antiderivative verification,
                        IntegralSolver,                        endpoint evaluation, and conservative
                        EvalBarSolver,                         finite-point or positive-infinity limits.
                        LimitCalcSolver



                                                  22
Preprint




Logical reduction and domain analysis. EqbSolver matches a goal against an assumption
modulo α-equivalence, while the separate reflexivity backend handles relations such as equality and
subset inclusion. FunctionApplySolver performs capture-avoiding simultaneous beta reduc-
tion, unfolds admissible nonrecursive closed definitions, and selects a piecewise point value only
when the selected guard is proved and every preceding guard is disproved. ConstTypeSolver
is restricted to number-set membership of closed constant terms; concrete primality is checked only
up to 106 . DomainTypeSolver instead propagates contextual membership through compound
expressions while retaining nonzero, root, and power conditions.

Algebra and inequalities. Polynomial and rational normalization, root–fraction normaliza-
tion, and root–power conversion are separated into specialized backends. Sign solvers propa-
gate positive, negative, zero, and nonzero information through supported expression structure.
IntervalSolver performs interval-constraint propagation and distinguishes defined, undefined,
and unknown closed expressions. SqueezeSolver uses explicit comparison and sign facts in a
bounded local search; it neither invokes another solver to manufacture a side condition nor performs
unrestricted algebraic expansion. Linear real arithmetic is available through a separate backend
rather than being silently assumed by every transformation.

Calculus and analysis. The calculus backends certify restricted, explicit fragments rather than
invoking a general computer-algebra oracle. DerivSolver evaluates FunDeri expressions from
lambdas or admissible nonrecursive definitions and supports higher and mixed partials; it does not
invent derivatives for unknown symbolic functions. Conditional derivative and pointwise-continuity
definitions must hold on a real open neighborhood of the evaluation point, not merely at that point.
ContinuousFuncSolver handles resolved unary lambdas, arithmetic closure, and supported
elementary compositions subject to their natural domains. IntegrableFuncSolver automat-
ically proves integrability only on finite closed intervals, using continuity as a sufficient condi-
tion. IntegralSolver verifies a normalized antiderivative family by differentiation and requires
an explicit, unconstrained real integration constant; it does not synthesize an indefinite integral.
EvalBarSolver checks finite endpoint evaluation of an explicit lambda after validating division,
powers, logarithms, roots, and tangent at both endpoints. LimitCalcSolver supports continuity-
based finite substitution and conservative positive-infinity rational or growth-order cases, but not
negative-infinity and general one-sided limits, L’Hopital’s rule, or general asymptotic equivalence.

Definedness and exactness. Solver obligations retain their domain information. Division requires
a nonzero denominator, logarithms require admissible arguments and bases, even roots require non-
negative radicands, and a piecewise branch is selected only under the guarded conditions above.
Substitution is binder-aware, preventing a fact about a free variable from being reused for a shad-
owing bound variable. Rational expressions are evaluated exactly when possible, while constants
such as e and π use certified rational intervals for comparisons rather than ordinary floating-point
approximation. Unknown precision or an unsupported construct is never silently converted into a
proof.


B.4   T HEOREM L IBRARY

Many proof gaps require named mathematical knowledge beyond computation and decision proce-
dures. We therefore provide a theorem library in the same formal language as the proof states. The
packaged solutions use the included theorem-library snapshot, which contains 514 consecutively in-
dexed DSL entries. They cover sets, binary relations, functions, cardinality, countability, and induc-
tion; limits, continuity, differentiation, integration, sequences, and series; algebraic, trigonometric,
exponential, logarithmic, hyperbolic, inverse-trigonometric, and complex identities; and reusable
definitions for intervals, extrema, function and sequence properties, and multivariable differential
operators. The snapshot contains high-level results such as the mean-value and squeeze theorems,
definition-expansion and bridge lemmas for short local steps, and alpha-compatible variants of fre-
quently used declarations.
Table 12 gives a descriptive organization by index range. These ranges summarize the bundled
sequence; they are not additional types trusted by the checker.


                                                  23
Preprint




           Table 12: Descriptive coverage of the bundled 514-entry theorem-library snapshot.
 Indices Count Descriptive coverage

   1–75         75   Sets and binary relations
 76–109         34   Functions, cardinality, and natural numbers
110–147         38   Core analysis results and proof rules
148–241         94   Algebraic, trigonometric, exponential, and complex identities
242–277         36   Auxiliary mathematical operators and definitions
278–352         75   Function properties, continuity, differentiability, sequences, and series
353–494        142   Executable bridge lemmas for analysis reasoning
495–514         20   Alpha-variable compatibility entries



Each entry pairs a stable numeric identifier and a human-readable title with a formal DSL statement.
Titles are not assumed to be globally unique, so the numbered identifier is the primary reference.
Library entries and proof gaps pass through the same semantic parser, so intervals, indexed sums,
and set comprehensions receive the same AST-level interpretation. To use an entry, a DSL program
invokes get prop, quotes the entry, optionally supplies explicit substitutions for a subset of its
outer universal binders, and states the resulting hypothesis. The checker resolves the numbered
entry, performs capture-avoiding instantiation and beta reduction, and accepts the hypothesis only
when it is α-equivalent to the recomputed instance. Its premises must then be discharged explicitly.
A model therefore cannot cite a nonexistent theorem or silently discard its side conditions, and
missing library knowledge remains an observable failure mode.
This 514-entry theorem snapshot is included in the final artifact and used to replay its packaged
solutions. Among the 7,727 accepted programs, 569 cite at least one numbered library entry; they
contain 1,053 references spanning 180 distinct theorem identifiers. The library is thus used selec-
tively alongside solver- and context-driven certificates.

B.5   U NIFIED V ERIFIER -G UIDED AGENT W ORKFLOW

The verifier-guided baseline integrates complementary mechanisms explored by four workflow im-
plementations behind one task and checker interface; it does not assume that every implementation
contains every mechanism. The language model proposes and revises DSL programs, whereas a
deterministic controller atomically claims gaps, pins the checker and theorem-library versions, as-
signs budgets, and executes each candidate in an isolated work area. Attempts retain their DSL, first
failure, residual state, and terminal decision, enabling replay and recovery. Figure 2 summarizes the
workflow.

                                      Deterministic
                                                                    FAST route                      DEEP route
       Input and control                screening
                                                                 short hypothesis,               targeted retrieval;
      (Γ, g); atomic claim;        source and terminal                                stall
                                                                  witness, binder,                smallest bridge;
        pinned versions;              checks; cheap
                                                                 theorem, rewrite,                decompose and
         budget and log             autosolve; pass to
                                                                   or solver plan                 backfill subgaps
                                   gate or enter FAST
                                                       direct pass
           Audited reusable          Audited outcome                 Dual accep-
               knowledge             accepted certificate             tance gate              Model–checker loop
            proof/reference          or typed diagnosis:          closed, admit-free             plan, emit, and
            bank; validated           invalid, capabil-         root replay; semantic            revise DSL ↔
           failure experience           ity, limitation,        audit: scope, domain,           isolated checker
             for later gaps            bug, or blocker            and dependencies            with failure evidence


Figure 2: Verifier-guided agent baseline. Darker nodes denote model-directed work, while dashed
arrows denote reuse. Stalled FAST attempts escalate to targeted DEEP search; acceptance requires
an admit-free root replay and semantic audit before outcomes can guide later gaps.



                                                        24
Preprint




Screening and FAST search. Screening performs source and terminal-evidence checks and first
tests a cheap candidate such as autosolve all hypothesis. Unresolved gaps enter bounded
FAST search over short hypothesis, witness, binder, theorem, rewrite, assertion, and solver routes.
For each attempt, the checker returns the first failed instruction, compact local evidence, and the
residual proof state. A retry is justified only when it changes the route or proof state; a repeated
failure signature or exhausted budget triggers escalation rather than another equivalent solver per-
mutation.

DEEP search and subgaps. DEEP search retrieves a small set of relevant theorems, solver cards,
recipes, or verified examples, then identifies the smallest bridge between the current state and target.
It may organize that bridge as local assertions or recursive subgaps. Search-time placeholders can
expose those subgaps, but they are never accepted as evidence: every subgap must be backfilled, and
the complete root program must be replayed with zero admits.

Acceptance and typed diagnoses. A machine pass remains provisional. Acceptance additionally
requires a closed, admit-free root proof and semantic checks of theorem instantiation, quantifier
scope, rewriting, domain conditions, dependencies, and possible inconsistent assumptions. Other
runs receive evidence-backed diagnoses such as invalid data, missing theorem or backend capability,
known limitation, bug, or a localized unresolved blocker. Audited certificates populate the proof
bank, while validated recurring failures populate the experience bank used for subsequent routing
and retrieval.

Audited reuse. Atomic claims allow workers to process disjoint gaps concurrently, while publica-
tion into shared state is serialized. A successful proof enters the reference bank only after machine
and semantic gates pass and duplicate content is removed. Repeated failure signatures first become
experience candidates; they influence later routing only after mechanical regression evidence or re-
view validates the proposed recovery rule. Retrieval is deliberately targeted, exposing a small ranked
set rather than the complete history.

B.6     O RIGINAL -V ERSION BASELINE AND R EPORTING P ROTOCOL

Treating autosolve as a lightweight automated theorem prover inside the DSL, we first apply it
to all 26,116 instances; it closes 2,838 gaps. The remaining 23,278 instances are then processed by
our verifier-guided agent workflow, using Codex as the agent and gpt-5.6-sol as its underlying
model. Under the same checker and theorem-library snapshot, the workflow produces accepted DSL
proofs for a further 4,889 gaps. The complete accounting is shown in Table 13.


Table 13: Checker-accepted certificates for the original ProofGap version. “Share of all” is measured
over 26,116 gaps; the workflow stage rate is measured over its 23,278-instance residual input.
Stage                                                   Inputs Newly closed Share of all Stage rate

Direct autosolve                                        26,116          2,838        10.9%       10.9%
Verifier-guided workflow                                23,278          4,889        18.7%       21.0%

Combined coverage                                       26,116          7,727        29.6%           —


Stage attribution prevents successes found by autosolve from being credited to the agent work-
flow. Operationally, a direct certificate consists of exactly one nonempty command, after removal of
an optional numeric step prefix, and that command begins with autosolve; every other accepted
program is assigned to the workflow stage. We report the workflow as a single baseline rather than
attributing completions to its internal FAST or DEEP routes.
Every accepted DSL program is replayable under the checker and therefore provides an executable
ground-truth solution for the corresponding gap in the original version of the benchmark. This is a
solution-level notion of ground truth: multiple distinct DSL programs may validly certify the same
local obligation. The remaining 18,389 gaps have no packaged certificate and are not treated as false
or unprovable.


                                                  25
Preprint




B.7   C ERTIFICATE PACKAGE AND I NDEPENDENT V ERIFICATION

The final original-version artifact contains one canonical directory for each of the 26,116 gaps.
Exactly 7,727 directories contain both the gap and an accepted DSL program, while 18,389 contain
the gap only. Seven secondary solutions for already represented canonical pairs are excluded, so the
reported count is over unique exercise–gap pairs. A 26,116-row manifest records the canonical pair,
whether a program is present, provenance, and a SHA-256 digest for every gap and every available
program. A machine-readable build summary records the aggregate counts and component digests.
The artifact also contains the 514-entry theorem snapshot used during replay.
The final artifact includes its packaged verifiers for 64-bit Linux and Windows together with a
Python-standard-library verification driver. The driver executes only cases that contain a DSL pro-
gram; gap-only cases are counted and skipped. It uses isolated temporary settings, result, and log
locations for each case and normalizes UTF-8 byte-order marks, line endings, and blank lines in
a temporary copy, leaving the submitted gap unchanged. Parallelism is configurable (default eight
workers), as is the per-case timeout (default 120 seconds). A full replay is launched with python3
check.py; command-line options can select the platform, worker count, and timeout. Running
the driver produces per-case execution and error logs, an aggregate tabular report, and a machine-
readable summary.
A packaged case passes only when all of the following conditions hold:

      1. the verifier process exits with status zero;
      2. the structured result uses schema test dsl structured v2;
      3. final status is finish;
      4. both proof finished and proof verified are true;
      5. both admit count and split gap count are zero; and
      6. standard output contains the terminal marker dsl proof finished.

The driver itself exits successfully only when every packaged DSL case passes all of these checks.
Consequently, a merely parsable program, an unfinished case branch, an admitted subgap, or a
process that exits cleanly without the structured proof evidence is not classified as passing by the
replay driver.

C     E VALUATION P ROTOCOL
The Lean evaluation uses two paired target types. A proof-gap target asks the model to prove
one local theorem with the context accumulated from earlier steps of the reference solution. Its
parent-exercise target asks the model to prove the corresponding complete exercise theorem from
the original premises. The complete evaluation contains 26,116 proof gaps from 3,015 exercises and
their corresponding 3,015 parent-exercise theorems. The same set of exercises is used for paired
gap–exercise and macro-coverage analyses. The reference proof is withheld in both settings.

C.1   P ROMPT AND V ERIFICATION I NTERFACE

For a proof-gap target, the prompt contains the original imports, definitions, helper declarations,
statements of preceding gap theorems, and the exact target statement. Every gap proof body is
replaced by a marker or an omission comment, and later declarations are excluded. Earlier theorem
statements remain available because they form part of the local context represented by the gap. For a
parent-exercise target, the prompt contains the imports, definitions, and complete exercise statement,
but no intermediate gap theorem or reference proof. In both cases, the model returns a JSON object
whose proof field is a complete replacement for the target’s by block.
The returned proof is inserted into the original module, with all other source text unchanged, and
checked in a fresh process. The pinned environment uses Lean v4.29.0-rc6 and Mathlib re-
vision 5c8398df528176d9c87ccd9226ba8f7c8852d59c. A candidate is accepted only if
the reconstructed module compiles and a recursive assert no sorry check confirms that the
target has no dependency on sorryAx. The checker also rejects proof escapes and declarations


                                                 26
Preprint




that could change the trusted environment, including sorry, admit, axiom, constant, and
run tac. Candidate checks are isolated so that generated files and process state cannot be reused
across targets.

C.2   M ODELS AND C ANDIDATE B UDGET

The full paired evaluation uses Goedel-Prover-V2-8B, DeepSeek-Prover-V2-7B, and Kimina-
Prover-Distill-8B. ProofGap-280 additionally includes Kimi-K3, DeepSeek-V4-Pro, GLM-5.2,
Claude-Opus-4.8, and GPT-5.6-sol. Each model receives the same target-specific prompt interface
and generates eight candidate proofs per target. Each generation is capped at 8,192 output tokens.
We use temperature 0.6 and nucleus-sampling parameter top p = 0.95. The comparison is therefore
controlled at the target level: one proof gap and one complete exercise theorem each receive eight
candidates. It is not an exercise-level compute comparison, because an exercise containing multiple
gaps induces multiple independently evaluated local targets.

C.3   PASS @k AND E XERCISE -L EVEL C OVERAGE

For fixed-n runs, let T be the number of targets, n = 8 the number of checked candidates per target,
and ci the number of accepted candidates for target i. For k ≤ n, we use the standard unbiased
estimator of Chen et al. (2021)
                                                 T         n−ci
                                                                !
                                             1X              k
                                  \
                                 Pass@k =            1− n          ,
                                             T i=1           k

with the ratio interpreted as zero when n − ci < k. At k = 8, this reduces exactly to the fraction of
targets with at least one accepted candidate. All reported Lean evaluation runs have eight checked
candidates per target and use this estimator. Malformed, timed-out, prohibited, or noncompiling
returned candidates count as failures.
For the full proof-gap set, micro averaging assigns equal weight to each gap. The exercise-level
diagnostic analyses use Pass@8. Let N be the number of paired exercises, ni the number of gaps in
                 (8)
exercise i, and yij ∈ {0, 1} indicate whether at least one checked candidate solves its j-th gap under
the eight-candidate budget. At this budget, micro-averaged gap performance and macro-averaged
exercise coverage are
                             PN Pni (8)                                        N       ni
                                i=1   j=1 yij                              1 X 1 X          (8)
       GapPassmicro @8 =          PN          ,       GapCovmacro @8 =                     yij .
                                    i=1 ni
                                                                          N       n
                                                                              i=1 i j=1

Micro averaging weights all gaps equally; macro coverage first computes the fraction of solved gaps
within each exercise and then weights all exercises equally. The reported exercise-level means and
conditional analyses use all 3,015 paired exercises.

D     P ROOF G AP -280 C ONSTRUCTION
ProofGap-280 is a reduced-cost, balanced subset for cross-model comparison. Its construction
jointly controls mathematical topic and the length of the Lean reference proof. Reference-proof
length is used only as reproducible sampling metadata: the reference proof itself, its length, and its
hash are not included in the model prompt, and line count is not assumed to be a complete measure
of mathematical difficulty.

D.1   L ENGTH S TRATA AND T OPIC M APPING

The benchmark catalog parses the exact by proof body of each gap and counts its physical lines
after removing trailing whitespace. The four strata are
                            T INY :   1–2        gold-proof lines,
                            S HORT :  3–5        gold-proof lines,
                            M EDIUM : 6–15       gold-proof lines,
                            L ONG :   16 or more gold-proof lines.

                                                 27
Preprint




The seven topics follow the source-area mapping used in the main paper: functions, limits, and
continuity; single-variable differentiation; indefinite and definite integrals; series; multivariable dif-
ferentiation; parameter integrals; and multiple, line, and surface integrals.

D.2     BALANCED S AMPLING P ROCEDURE

We form the Cartesian product of seven topics and four length strata, producing 28 sampling
cells. Each cell contributes exactly ten gaps, giving 40 gaps per topic, 70 per length stratum,
and 280 in total. Within each cell, eligible catalog entries are shuffled by Python’s deterministic
random.Random(20260727) generator and selected subject to at most one gap from each base
exercise number. The latter rule also prevents variants such as two separately indexed subquestions
of the same numbered exercise from both entering the subset. Consequently, the 280 gaps have 280
distinct parent-exercise targets. After selection, rows are sorted by exercise number, exercise variant,
and gap number to give a stable evaluation order.


                Table 14: ProofGap-280 allocation across the 28 topic-by-length cells.
Topic                                                              Tiny Short Medium Long Total

Functions, limits, and continuity                                     10     10         10      10     40
Single-variable differentiation                                       10     10         10      10     40
Indefinite and definite integrals                                     10     10         10      10     40
Series                                                                10     10         10      10     40
Multivariable differentiation                                         10     10         10      10     40
Parameter integrals                                                   10     10         10      10     40
Multiple, line, and surface integrals                                 10     10         10      10     40

Total                                                                 70     70         70      70    280

The released subset manifest records the seed, strategy, cell counts, stable subset position, exercise
identifier, source topic, length stratum, reference proof line count, gap identifier, and paired original-
exercise identifier for every selected row. It therefore permits exact regeneration of the subset and
direct alignment of every gap result with its parent-exercise result.




                                                   28
Preprint




E     A DDITIONAL R ESULTS AND A NALYSIS
E.1     F ULL -S ET PASS @k

Table 15 gives the complete Pass@1, Pass@3, and Pass@8 results for the three specialized provers.
The proof-gap columns use all 26,116 local targets, and the parent-exercise columns use their 3,015
corresponding complete theorems.


        Table 15: Full-set Pass@k (%) for proof gaps and complete parent-exercise theorems.
                                       All proof gaps                            Parent exercises
Model                         Pass@1      Pass@3        Pass@8       Pass@1          Pass@3         Pass@8
Goedel-Prover-V2-8B            26.60        32.85        35.39            2.17             3.36        4.28
DeepSeek-Prover-V2-7B          26.12        31.84        33.27            1.92             2.67        3.32
Kimina-Prover-Distill-8B       25.56        30.77        31.99            1.74             2.42        2.92

The standard-tactic union solves 2,925 gaps, or 11.20% of the full set. Removing these leaves
23,191 tactic-unsolved gaps (88.80%). As shown in Table 17, the learned provers retain substantial
performance on this residual set; their results are not explained only by obligations already solved
by the evaluated tactic portfolio.


Table 16: Solve rates of standard Lean tactics on 26,116 proof gaps. The union succeeds if any
evaluated tactic succeeds.
                  Tactic                                                 Solve rate (%)
                  assumption                                                        1.78
                  simp                                                              1.88
                  aesop                                                             9.67
                  norm num                                                          2.45
                  linarith                                                          2.75
                  nlinarith                                                         2.85
                  ring                                                              1.08
                  omega                                                             0.17
                  Union                                                            11.20



        Table 17: Performance (%) on the 23,191 gaps not solved by the standard-tactic union.
Model                                  Pass@1                Pass@8                        Solved at Pass@8
Goedel-Prover-V2-8B                      18.61                   27.48                                6,374
DeepSeek-Prover-V2-7B                    17.81                   25.16                                5,834
Kimina-Prover-Distill-8B                 17.07                   23.57                                5,467




                                                 29
Preprint




E.2     P ROOF G AP -280 B REAKDOWN

The main paper reports overall Pass@1, Pass@3, and Pass@8 for all models on ProofGap-280.
The following tables give Pass@8 breakdowns for the five general-purpose models. Each entry in
Tables 18 and 19 reports proof gap / parent exercise. Topic cells have denominator 40 and length
cells have denominator 70.

Table 18: ProofGap-280 Pass@8 (%) by mathematical topic. Each entry is proof-gap / parent-
exercise performance.
                          Functions                 Single-var.             Indef./def.
Model                                                                                           Series
                           & limits                    diff.                 integrals
GPT-5.6-sol               95.0 /    55.0            90.0 / 20.0             90.0 /    2.5      90.0 / 17.5
Claude-Opus-4.8           87.5 /    37.5            87.5 / 17.5             92.5 /    2.5      92.5 / 10.0
Kimi-K3                   85.0 /    27.5            80.0 / 12.5             90.0 /    0.0      80.0 / 5.0
DeepSeek-V4-Pro           65.0 /    10.0            57.5 / 5.0              77.5 /    0.0      65.0 / 5.0
GLM-5.2                   65.0 /     5.0            57.5 / 2.5              72.5 /    0.0      67.5 / 0.0


                          Multivar.              Parameter             Multiple/line/
Model                                                                                           Overall
                           diff.                  integrals           surface integrals
GPT-5.6-sol              90.0 / 25.0             77.5 /    7.5              82.5 / 22.5        87.9 / 21.4
Claude-Opus-4.8          90.0 / 10.0             82.5 /    2.5              82.5 / 17.5        87.9 / 13.9
Kimi-K3                  82.5 / 5.0              75.0 /    2.5              75.0 / 10.0        81.1 / 8.9
DeepSeek-V4-Pro          65.0 / 5.0              67.5 /    2.5              75.0 / 7.5         67.5 / 5.0
GLM-5.2                  60.0 / 5.0              65.0 /    2.5              67.5 / 7.5         65.0 / 3.2



Table 19: ProofGap-280 Pass@8 (%) by the reference proof length of the selected gap. Each entry is
proof-gap / parent-exercise performance. The parent-exercise column is grouped by its paired gap’s
stratum, not by the length of a parent-exercise reference proof.
Model                   Tiny                Short             Medium                 Long       Overall
GPT-5.6-sol          100.0 / 22.9          98.6 / 24.3        92.9 / 22.9        60.0 / 15.7   87.9 / 21.4
Claude-Opus-4.8       98.6 / 12.9          98.6 / 18.6        88.6 / 14.3        65.7 / 10.0   87.9 / 13.9
Kimi-K3               98.6 / 8.6           98.6 / 11.4        92.9 / 10.0        34.3 / 5.7    81.1 / 8.9
DeepSeek-V4-Pro      100.0 / 7.1           91.4 / 8.6         65.7 / 2.9         12.9 / 1.4    67.5 / 5.0
GLM-5.2               97.1 / 4.3           87.1 / 5.7         64.3 / 1.4         11.4 / 1.4    65.0 / 3.2


Length sensitivity. All five models solve at least 97.1% of Tiny gaps, whereas Long-gap Pass@8
ranges from 65.7% for Claude-Opus-4.8 to 11.4% for GLM-5.2. Much of the cross-model separation
is therefore concentrated in longer local derivations. Reference-proof line count remains a coverage
proxy rather than a complete measure of intrinsic difficulty.

Local versus end-to-end reasoning. GPT-5.6-sol and Claude-Opus-4.8 tie at 87.9% on gaps but
reach 21.4% and 13.9%, respectively, on the paired exercises. Even in the Tiny stratum, parent-
exercise Pass@8 is only 4.3–22.9%. The parent rows are grouped by the paired gap’s length, not by
parent-theorem proof length.

Topic sensitivity. Parent exercises are easiest in functions and limits for every model. Indefinite
and definite integral gaps reach 72.5–92.5%, but the paired exercise score is 2.5% for GPT-5.6-sol
and Claude-Opus-4.8 and zero for the other models; parameter integrals are also difficult end to end.
Local success therefore leaves substantial work in lemma selection, analytic side conditions, and
proof composition.



                                                      30
