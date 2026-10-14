                                             RePro: Proof-Verified Benchmark Rewriting for Reliable Evaluation of
                                                            LLM Mathematical Problem Solving
                                             Xiyuan Zhou1 * , Zhuoqi Li2 * , Xinlei Wang3 , Yirui He2,4 , Yuhao Wu2 , Yuheng Cheng2 ,
                                                                   Yan Xu1† , Junhua Zhao2,5† , Jinjin Gu3†
                                                 1
                                                  Nanyang Technological University, 2 The Chinese University of Hong Kong, Shenzhen,
                                             3
                                                 INSAIT, Sofia University “St. Kliment Ohridski”, 4 Shenzhen Loop Area Institute, 5 AIRS
                                                             xiyuan002@e.ntu.edu.sg, zhuoqili1@link.cuhk.edu.cn
                                                               xinlei.wang@insait.ai, yiruihe@link.cuhk.edu.cn
                                                          yuhaowu@link.cuhk.edu.cn, yuhengcheng@link.cuhk.edu.cn
                                                      xuyan@ntu.edu.sg, zhaojunhua@cuhk.edu.cn, jinjin.gu@insait.ai
arXiv:2609.00062v1 [cs.CL] 30 Aug 2026




                                                                     Abstract
                                                                                                                                 Original Instances (Problems & Answers)
                                                 Data contamination undermines the reliable
                                                 evaluation of large language models (LLMs)                                                               RePro (Ours)
                                                                                                           Existing Rewriting Methods
                                                 on mathematical problem solving. While                                                              Proof-Verified Rewriting
                                                 rewriting-based evaluation mitigates memo-
                                                 rization, existing methods lack guarantees
                                                                                                                                                   LLM         Proof          ATP
                                                 of problem validity and answer correctness.                 LLM Only            Code
                                                 We propose Proof-Verified Benchmark Rewrit-                         Rewritten                                               Lean
                                                                                                                     Instances                                            Verification
                                                 ing (RePro), the first framework to inte-
                                                 grate Lean-oriented neural automated theo-
                                                 rem provers (ATPs) into benchmark rewrit-                    Rewritten Instances                    Rewritten Instances
                                                 ing, which rewrites problems and regenerates                 Potential Invalid Cases                   Guaranteed
                                                 answers with correctness ensured by Lean-
                                                 verified proofs. Experiments on GSM8K and                 Ill-defined Infeasible Incorrect       Well-defined Feasible     Correct

                                                 MATH show that RePro’s retained rewritten
                                                 instances achieve 100% well-definedness, fea-          Figure 1: Overview of RePro. Existing rewriting meth-
                                                 sibility, and answer correctness, while existing       ods may produce invalid problems or incorrect answers.
                                                 methods still produce invalid or incorrect in-         RePro integrates formal verification to ensure that rewrit-
                                                 stances. Moreover, several models exhibit ac-          ten instances are valid questions and paired with verified
                                                 curacy drops on proof-verified rewritten bench-        answers, enabling reliable LLM evaluation.
                                                 marks, suggesting that their performance is
                                                 sensitive to surface-level and structural vari-
                                                 ations and may partly reflect memorization ef-         including benchmark rewriting, interactive evalu-
                                                 fects. Our source code and data are available at       ation, and multi-agent evaluation, aim to reduce
                                                 https://github.com/AI4Engi/RePro.
                                                                                                        contamination (Chen et al., 2025). However, their
                                         1       Introduction                                           reliance on heuristic rewriting or model-generated
                                                                                                        processes makes it difficult to guarantee problem
                                         Evaluating mathematical capability is essential for            validity and answer correctness.
                                         understanding the reasoning abilities of large lan-               Benchmark reliability remains a concern in ex-
                                         guage models (LLMs) (Shao et al., 2024; Ahn                    isting evaluations, even for influential expert bench-
                                         et al., 2024). However, benchmark reliability is               marks such as GPQA (Rein et al., 2024) and HLE
                                         challenged by data contamination, as training cor-             (Center for AI Safety et al., 2026), which have ad-
                                         pora and evaluation benchmarks often share public              vanced frontier LLM evaluation. HLE-Verified fur-
                                         sources (Chen et al., 2025; Cheng et al., 2025).               ther highlights the importance of answer reliability,
                                         Such overlap may allow models to achieve high                  reporting that within HLE’s mathematical category,
                                         scores through memorization rather than genuine                problem validity exceeds 92% while answer va-
                                         reasoning (Li et al., 2024; Zhou et al., 2026a; Zhao           lidity is 59.6% (Zhai et al., 2026). This suggests
                                         et al., 2025). Recent dynamic evaluation methods,              that benchmark reliability depends on both prob-
                                             * Equal contribution.                                      lem validity and answer correctness, reflecting a
                                             †
                                                 Corresponding authors.                                 broader emphasis on verifier-guided reliability in

                                                                                                    1
LLM systems (Wang et al., 2026). Accordingly,              into a unified verification pipeline, retaining only
RePro focuses on mathematical and formally verifi-         instances with verified reference answers while
able problems, and evaluates rewritten instances by        enforcing problem validity through a three-stage
whether they are well-defined, feasible, and paired        verification process. (2) We introduce reliability-
with a correct reference answer (see Sec. 4).              oriented evaluation criteria for rewritten bench-
   To improve benchmark rewriting reliability, we          marks, covering well-definedness, feasibility, and
introduce deterministic proof verification by incor-       answer correctness. (3) We use proof-verified
porating Lean-oriented neural automated theorem            rewriting to analyze reformulation sensitivity and
provers (ATPs) and proof-assistant checking into           identify potential memorization-related signals.
the rewriting pipeline, replacing heuristic LLM-
based evaluation with machine-verifiable reasoning.        2   Related Work
In RePro, proof search relies on Lean-oriented neu-
ral ATPs such as Goedel-Prover (Lin et al., 2026)          Dynamic Benchmark Generation. Dynamic
and DeepSeek-Prover (Ren et al., 2025). Given a            benchmark methods mitigate data contamination
formalized statement, these models generate Lean           and expand evaluation coverage by automatically
proof scripts, which are treated as candidate proofs       generating new test instances from existing bench-
and accepted only after Lean kernel-level verifi-          marks. A common approach is benchmark rewrit-
cation. Unlike classical ATPs and SMT solvers              ing, which applies semantic or structural transfor-
such as Vampire (Kovács and Voronkov, 2013) and            mations, such as synonym paraphrasing (Ying et al.,
Z3 (De Moura and Bjørner, 2008), which return              2024; Zhu et al., 2024), numerical substitution
sound results within supported logical fragments,          (Qian et al., 2024), and structural perturbation (Cao
neural ATPs may generate scripts with compilation          et al., 2024), to weaken memorization cues while
failures, target mismatches, or tactic-level errors.       reusing existing evaluation resources. Another line
RePro therefore retains only proofs that pass Lean         of work adopts multi-agent or solver-based frame-
kernel-level checking (De Moura et al., 2015).             works for benchmark construction, such as Bench-
   Building on the guarantees provided by formally         mark Self-Evolving (Wang et al., 2025b), BenchA-
verified proofs, we propose RePro (Proof-Verified          gents (Butt et al., 2024), and the CSP-based logic
Benchmark Rewriting), a framework for construct-           puzzle benchmark ZebraLogic (Lin et al., 2025).
ing mathematically rigorous rewritten benchmarks.          Despite improving diversity and coverage, these
As illustrated in Fig. 1, in RePro, LLMs gener-            methods still largely rely on heuristic validation,
ate diverse rewritten problems and perform conser-         including human inspection, LLM-as-a-Judge, or
vative semantic screening, while ATPs search for           agent-based checking. Such validation may still
candidate proofs and proof assistants verify them.         leave semantic drift, incorrect labels, or implicit-
In this way, the rewritten benchmark maintains             assumption violations, limiting deterministic relia-
high diversity while providing verifiable correct-         bility guarantees, see Sec. 4 and Sec. 6.1.
ness guarantees. Only instances whose reference            Formal Verification and Automated Theorem
answers have a formally verified proof are retained,       Proving. Formal reasoning represents mathemat-
ensuring that the released benchmarks contain only         ical statements and proofs in a machine-verifiable
problems with formally verified answers. Detailed          format, enabling rigorous verification of logical cor-
methodology is presented in Sec. 3.                        rectness. Proof assistants such as Lean (De Moura
   Empirical results show that RePro significantly         et al., 2015) and Coq (Bertot and Castéran, 2013)
improves the reliability of rewriting-based evalu-         provide formal languages for mathematical reason-
ation. Compared with existing methods, RePro               ing and verify proofs through kernel-level check-
achieves 100% well-definedness, feasibility, and           ing. Large formal mathematical libraries such
answer correctness among retained rewritten in-            as mathlib support large-scale formalization and
stances on both GSM8K (Cobbe et al., 2021) and             automated reasoning (Yang et al., 2023). Clas-
MATH (Hendrycks et al., 2021), while prior meth-           sical ATPs and SMT solvers, such as Vampire
ods still produce invalid problems or incorrect ref-       (Kovács and Voronkov, 2013) and Z3 (De Moura
erence answers.                                            and Bjørner, 2008), solve formal logical problems
   Our contributions can be summarized as fol-             within supported logics, while hammer systems
lows: (1) We propose RePro, the first benchmark            such as LeanHammer bridge Lean with external
rewriting framework that integrates ATPs and Lean          provers (Zhu et al., 2025). In contrast, recent neu-

                                                       2
        Input              Feasibility Screening               Executable Formalization                  Proof-level Verification                    Output
                                       Retry (Max retries reached at 6 )         Retry (Max retries reached at 8 )


                                                                                Lean                                      Lean
                                    Rewriting                                Formalized                                  Answer
                                    Question                   Formalizer     Question                                    Proof
                           LLM                                                                            ATP
                                                                                 4         5
                       1                                      (Format Check)
                                                                                                                                                     Valid
                                                                             Valid Lean                                                            Rewritten
                                   2                 3   3                   Formalized            6                 7                8
                                                                 LEAN-                                                                             Question
      Original                                                  Interact      Question
                                                                                                                                                       +
      Question                                                                                                                               8
                                                                                 5             6                                                    Verified
                                                              (Semantic Check)                                                                      Answer
                                      Valid
                                                                            Semantically                             Verified Lean
                                    Rewritten                                Consistent                                Answer
                                    Question                                  Question                   LEAN-           Proof
                           LLM                                   LLM                                    Interact                     Match




    *Arrow Notation:                                               Deleted Instances                                                             *Box Notation:
                                         3                                       5                                          8
      Successful                                                       Invalid Lean Format
                                                                                                              Proof Generation Failure            Tool
        Path                  Ill-defined Question                                                                                                       Output
                                                                                                                                                  Used
     Failure Path
                                                                              6
                              Infeasible Question                      Semantic Mismatch                           Incorrect Answer



Figure 2: Framework of the proposed verification pipeline for rewriting-based evaluation. The pipeline progressively
filters rewritten instances to obtain valid questions with verified answers.


ral Lean provers, including DeepSeek-Prover (Ren                                     checks, such as those with ambiguous statements,
et al., 2025) and Goedel-Prover (Lin et al., 2026),                                  missing constraints, or infeasible solutions. The
generate candidate Lean proof scripts that must be                                   remaining candidates are then translated into
checked by Lean before acceptance. RePro oper-                                       executable formal specifications in Lean, providing
ates in this Lean/mathlib setting and uses neural                                    precise and machine-checkable representations
Lean provers with kernel-level verification to en-                                   of the rewritten problems. Finally, an automated
sure answer correctness. While prior work mainly                                     theorem prover (ATP) performs proof search to
studies theorem proving itself, benchmark verifica-                                  generate candidate proofs, whose correctness is
tion remains underexplored.                                                          checked by the Lean proof assistant. Through
                                                                                     this staged process, RePro retains only rewritten
3     RePro                                                                          instances that are well-defined and feasible and
                                                                                     whose answers are supported by formally verified
3.1      Overview
                                                                                     proofs. The prompt templates and implementation
To construct rewritten benchmarks with formally                                      details are provided in Appendix B, and examples
verified reference answers, we propose RePro. Ex-                                    of RePro-generated rewritten instances are
isting rewriting-based approaches typically rely on                                  provided in Appendix G.
heuristic validation mechanisms, such as LLM-as-
a-Judge or rule-based checking, which cannot pro-                                    3.2   Feasibility Screening
vide deterministic guarantees on problem validity                                    Feasibility Screening begins with LLM-based
or answer correctness. To address this limitation,                                   rewriting and subsequently filters invalid candidate
RePro integrates ATPs into the benchmark rewrit-                                     rewrites before executable formalization and proof
ing process, enabling the verification of reference                                  verification. Given an original problem, the LLM
answers through formal proofs while preserving                                       generates a candidate rewrite while preserving its
the diversity of rewritten instances.                                                core mathematical structure, solution logic, diffi-
    RePro follows a progressive verification                                         culty, and answer type. The rewriting process ap-
paradigm. It first prompts an LLM to generate                                        plies strategies including numerical reparameteriza-
candidate rewrites through numerical reparam-                                        tion, logical restructuring, constraint modification,
eterization, logical restructuring, constraint                                       and contextual reconstruction for word problems.
modification, and contextual reconstruction, and                                     The rewriter is instructed not to solve the rewritten
filters out instances that fail basic problem-validity                               problem or generate its new answer.

                                                                               3
   The generated candidate is then screened for               gates this limitation through subsequent proof-level
problem validity. This step removes questions that            verification and final-answer alignment: the ATP-
are ill-defined, ambiguous, internally inconsistent,          generated proof must pass Lean checking, and the
contradictory, unrealistic, or infeasible under basic         extracted answer must match the target quantity
real-world or task-specific constraints. Here, feasi-         requested by the rewritten problem. Therefore,
bility refers to the semantic and constraint consis-          answer correctness is established only after Lean
tency of the rewritten problem, rather than merely            verification and answer alignment, while semantic
whether a target can be formally derived from its             consistency is conservatively screened rather than
premises. Accordingly, candidates with contradic-             formally guaranteed. More details on the semantic
tory premises are rejected regardless of whether the          screening policy and proof-grounded target-answer
target is formally derivable from them. Detailed              matching are provided in Appendices C and D.
rewriting prompts, screening criteria, and imple-
mentation details are provided in Appendix B.                 3.4    Proof-level Verification
   For example, in problems involving population              Proof-level Verification validates the correctness
counts or quantity constraints, automatic rewriting           of reference answers through formal proof verifi-
may introduce negative values or other conditions             cation. This stage takes executable formalizations
that violate implicit real-world assumptions (Zhou            as input and retains only instances whose answers
et al., 2026b). Although such outputs may appear              can be successfully proven and verified in Lean,
mathematically expressible, they are considered               forming the final evaluation dataset. Unlike earlier
infeasible under the intended problem semantics               stages, Proof-level Verification is the only stage
and are therefore removed. This stage is intended             that determines answer correctness.
to ensure problem validity rather than answer cor-               At this stage, ATP is used to construct candidate
rectness. Answer correctness is established later             proofs for the formalized problems, which are then
through Proof-level Verification, while the final             verified in Lean. Only instances whose answers
answer-target matching step provides an additional            can be verified by a valid proof are retained, while
target-level consistency check by ensuring that the           those that fail proof verification are discarded and
verified answer corresponds to the specific quantity          regenerated. All correctness guarantees for refer-
requested in the rewritten problem.                           ence answers originate from this stage.
3.3   Executable Formalization                                   As illustrated in Fig. 2, Operation 8 performs
                                                              a constrained answer-alignment step between the
Executable Formalization converts rewritten in-               rewritten problem and the valid proof. It extracts
stances that pass feasibility screening into machine-         a candidate answer from spans that already appear
verifiable formal statements in Lean. This stage              in the proof and checks whether it matches the
consists of a format check and a semantic check.              quantity requested in the problem. No additional
The format check ensures that the generated Lean              computation, normalization, simplification, or in-
code is syntactically valid and can be compiled               ference is allowed at this stage. Only answers that
in Lean. The semantic check performs an LLM-                  exactly match the requested quantity are accepted;
assisted conservative alignment screen between the            intermediate values, answers to a different target,
rewritten natural-language problem and the Lean               and unresolved cases are discarded. This step is
formal statement, comparing key elements such as              used solely to ensure target-answer consistency.
quantities, conditions, logical structure, object type,       Detailed descriptions are provided in Appendix D.
and the requested target.
   We adopt a conservative all-pass policy. For               4     Evaluation Criteria
each compiled formalization, the semantic checker
is queried three times with temperature zero. A can-          A benchmark problem can serve as a reliable eval-
didate is accepted only when all three judgments              uation instance only if the problem itself is valid
return Consistent. Any mismatch, parsing failure,             and its reference answer is correct. The former
or uncertain output causes the candidate to be dis-           requires the problem to be clearly specified, log-
carded and regenerated.                                       ically coherent, and solvable, while the latter en-
   This step should not be interpreted as formal ver-         sures that model outputs are compared against a
ification of natural-language-to-Lean equivalence.            correct ground-truth answer. This is especially im-
It serves only as a pre-proof filter. RePro miti-             portant for rewritten problems, where rewriting

                                                          4
              Rewritten Problem
                                                                                   Original Problem                               Reference Answer
     # Ambiguous              # Missing                                                                                                   2
                                                              A box contains 6 balls, each of which is either red or
     Information             Information
                                                            blue. Among them, 4 are red. How many balls are blue?                Explanation: 6-4 = 2
  A box contains 6         A box contains
  balls, each of which     some balls, each     Rewriting              Rewriting                              Rewriting                       Rewriting
  is either red or blue.   of which is either
  Among them, 2 are        red    or    blue.                                                  Rewritten Problem
  red. The number of       Among them, 4                                                                                  A box contains 5 balls, each of
                                                   A box contains 5 balls, each of    A box contains 5 balls, each of
  red and blue balls       are red. How
                                                   which is either red or blue.       which is either red or blue.        which is either red or blue.
  is the same. How         many balls are
                                                   Among them, 6 are red. How         Among them, 3 are red. How          Among them, 3 are red. How
  many balls are blue?     blue?
                                                   many balls are blue?               many balls are blue?                many balls are blue?
                                                                            Reference Answer

    Unanswerable           Unanswerable                      -1 (Invalid)                         1 (Incorrect)
     Issue: “2 red”          Issue: Total                                                                                           2 (Correct)
   contradicts equal       number of balls         Issue: Negative number of balls.         Issue: Incorrect reference
   red-blue counts.           not given.                                                              answer.

            Ill-defined Problem                         Infeasible Problem                     Incorrect Answer                  Valid Instance

Figure 3: Failure modes of rewriting-based evaluation and our solution. Rewriting may introduce three types of
reliability issues: (1) ill-defined problems caused by ambiguous or missing information, (2) infeasible problems due
to conflicting constraints, and (3) incorrect answers where the reference answer is wrong. A rewritten instance is
valid only if the problem is well-defined, feasible, and paired with a correct reference answer.


may alter not only surface wording but also prob-                                     Answer Correctness. Measures whether the refer-
lem semantics, constraints, or answer consistency.                                    ence answer is formally verified. A reference an-
Recent benchmark verification studies further show                                    swer is correct only if the candidate is successfully
that many evaluation failures arise from ambigu-                                      formalized, verified by a valid proof, and matched
ous statements, missing information, or incorrect                                     to the target quantity. In RePro, all retained candi-
reference answers.                                                                    dates satisfy this requirement. In more general set-
   Motivated by these observations, we evaluate                                       tings, candidates that fail automatic formalization
rewritten problems from two complementary per-                                        should receive human-assisted checking to avoid
spectives: problem validity and answer correct-                                       hallucinated or unverifiable instances.
ness. Problem validity includes two criteria: well-                                      Let N denote the total number of gener-
definedness, requiring the problem to be clear and                                    ated rewritten instances, and Nc the num-
complete, and feasibility, requiring it to admit a                                    ber of instances satisfying criterion c ∈
solution under the given conditions and satisfy ba-                                   {well-definedness, feasibility, answer correctness}.
sic real-world or task-specific constraints. Answer                                   The corresponding rate is computed as Nc /N . To
correctness requires that the reference answer be                                     assess these criteria, we use a verification pipeline
correct. Together, these define three criteria for                                    based on Lean, ATP, and LLM screening, with
a reliable benchmark instance: well-definedness,                                      human assistance for ambiguous cases.
feasibility, and answer correctness. Fig. 3 illus-
trates the corresponding failure modes and a valid
                                                                                      5     Experimental Methodology
rewritten instance. We therefore use three criteria:                                  5.1    Datasets
Well-definedness. Measures whether the problem                                        To evaluate RePro, we select GSM8K (Cobbe
statement provides sufficient and unambiguous in-                                     et al., 2021) and MATH (Hendrycks et al., 2021)
formation to determine the task and its objective.                                    as benchmarks. We also considered harder bench-
A problem is considered not well-defined if it con-                                   marks such as AIME (Dekoninck et al., 2026) and
tains missing conditions, semantic ambiguity, un-                                     Omni-MATH (Gao et al., 2025), but current ATP
clear objects or variables, incomplete constraints,                                   bottlenecks led to very low generation rates; details
or an unspecified solving target.                                                     are provided in Sec. 6.2 and Appendix E. There-
Feasibility. Measures whether a well-defined prob-                                    fore, we focus on GSM8K and MATH, which are
lem admits a valid solution under basic real-world                                    widely used for mathematical reasoning. GSM8K
or task-specific constraints. A problem is consid-                                    provides structured grade-school math problems,
ered infeasible if no valid solution exists or if the                                 while MATH covers five Art of Problem Solving
derived result violates these constraints due to con-                                 (AoPS) difficulty levels (LV1–LV5), ranging from
flicting conditions or inconsistencies.                                               basic high-school exercises to olympiad-level prob-

                                                                                5
Table 1: Comparison of rewriting quality across methods on GSM8K and MATH. Metrics include well-definedness
(Well-defined), feasibility (Feasible), answer correctness (Correct), and generation rate (Gen. Rate). The upper table
reports results on the full set of generated rewritten instances, while the lower table reports results on the subset of
benchmark instances for which RePro successfully generates rewritten problems.

                                                        Full Dataset
                                      GSM8K                                                                                MATH
 Method
                Well-defined ↑ Feasible ↑ Correct ↑ Gen. Rate ↑ Well-defined ↑ Feasible ↑ Correct ↑ Gen. Rate ↑
 Auto-Dataset        99.60         99.19        87.10      100.00                             98.43                  96.23              79.99               100.00
 ITD                100.00         99.19        89.11      100.00                             98.26                  97.85              81.15               100.00
 VarBench            97.98         96.76        95.14       99.60                              96.54                 93.58              87.36                58.76
 RePro (Ours)       100.00        100.00       100.00       88.31                             100.00                 100.00             100.00               59.16

                                           RePro Successful Generation Subset
                                      GSM8K                                                                                MATH
 Method
                Well-defined ↑ Feasible ↑ Correct ↑ Gen. Rate ↑ Well-defined ↑ Feasible ↑ Correct ↑ Gen. Rate ↑
 Auto-Dataset        98.39         97.18        80.65      100.00                             99.53                   99.53             86.88               100.00
 ITD                 97.58         96.77        81.05      100.00                             100.00                  99.07             87.66               100.00
 VarBench            98.79         98.39        96.77      100.00                             95.49                   93.73             89.23                60.53
 RePro (Ours)       100.00        100.00       100.00      100.00                             100.00                 100.00             100.00              100.00



lems. Additional details on dataset selection and                                      100
                                                                                                              92.2                                    DeepSeek-Prover
                                                                                                  88.3
                                                                                                           85.3                                       Kimina-Prover
the data distribution before and after RePro filter-                                           81.9
                                                                                                                                                      Goedel-Prover
                                                                                        80                                 75.8         73.9
                                                                 Generation Rate (%)




ing are provided in Appendix E. The metadata and
                                                                                                                       61.9
fields of the released RePro dataset are described                                      60                                          58.0             57.1

in Appendix F.                                                                                                                                   38.4
                                                                                        40                                                                        33.7

5.2   Models
                                                                                        20                                                                    16.4
                                                                                                                     8.2
We evaluate RePro on a diverse set of open-                                                  4.0         4.6                      6.9          6.5
                                                                                                                                                            2.3
                                                                                         0
source language models from several major                                                    GSM8K         LV1         LV2          LV3          LV4          LV5
model families.        Specifically, we include
Qwen2–0.5B/1.5B, Qwen3–0.6B/1.7B/8B/14B                         Figure 4: Impact of ATPs with varying capabilities on
(Yang et al., 2025a), Llama-3.2–1B/3B (Touvron                  generation success rates.
et al., 2023), DeepSeek-R1–1.5B/7B/14B (Guo
et al., 2025), and Gemma 3–1B/4B (Team et al.,
                                                                the original task structure. Auto-Dataset generates
2025). This selection allows us to compare
                                                                semantically similar questions from existing prob-
contamination-related behaviors across different
                                                                lems. ITD performs semantic-level rewriting while
architectures and training methods while keeping
                                                                preserving the underlying numerical relations and
model scale controlled.
                                                                computation logic. VarBench extracts numerical
   For the RePro generation pipeline, we use
                                                                variables and constructs parameterized problem
Qwen3-MAX (Yang et al., 2025a) for prob-
                                                                templates with executable solution functions, en-
lem rewriting and feasibility screening, Goedel-
                                                                abling new instances through variable resampling.
Formalizer-V2-8B for executable formalization
into Lean 4 statements, and Goedel-Prover-V2-8B                 6                       Results
for ATP-based proof generation (Lin et al., 2026).
The generated proofs are then verified by Lean 4.               6.1                      Rewriting Quality Comparison
                                                                From Table 1, we obtain three key findings.
5.3   Baselines                                                 RePro guarantees reliable retained instances.
We compare our method with several representative               On both GSM8K and MATH, RePro achieves
approaches for automatic benchmark rewriting, in-               100% well-definedness, feasibility, and answer cor-
cluding Auto-Dataset (Ying et al., 2024), ITD (Zhu              rectness. This shows that its verification pipeline
et al., 2024), and VarBench (Qian et al., 2024).                removes ill-defined problems, infeasible instances,
These methods generate new evaluation instances                 and incorrect reference answers from the retained
to mitigate benchmark leakage while preserving                  rewritten set.

                                                            6
                      100                                                                                      100
                                      92.20                                                                                    92.20
                            88.31                                                                                              88.53
                                      81.65                                                                     90 88.31
                                                                                                                     83.87
                       80                       75.80   73.91                                                                  80.28
                            68.55
                                      71.56                                                                     80 76.21               75.80    73.91
Generation rate (%)




                                                                                         Generation rate (%)
                                                                                                                                       71.53    69.57
                       60 58.87                 56.23           57.10                                           70                     66.55
                                                                                                                                                60.87
                                                        48.19                                                   60                                      57.10
                                                        43.48                                                                                           52.84
                                                39.86
                       40                                               33.67                                   50                                      48.86
                                                                31.53
                                                                23.30                                           40
                       20           Qwen3-MAX                                                                                pass@1                              33.67
                                                                                                                                                                 30.99
                                    Qwen3-32B                           9.72
                                                                        7.37                                    30           pass@2                              27.30
                                    Qwen3-8B                                                                                 pass@3
                        0                                                                                       20
                            GSM8K MATH LV1 MATH LV2 MATH LV3 MATH LV4 MATH LV5                                       GSM8K MATH LV1 MATH LV2 MATH LV3 MATH LV4 MATH LV5


             Figure 5: Effect of rewriter on generation rate.                           Figure 6: Effect of ATP call limit on generation rate.


Existing rewriting methods still produce invalid                                     generation success. To study this effect, we keep
or incorrect instances. On the full datasets, Au-                                    all other components unchanged and only replace
toDataset, ITD, and VarBench achieve correctness                                     the ATP. We evaluate three strong ATPs below 15B
rates of 79.99%, 81.15%, and 87.36% on MATH,                                         parameters: DeepSeek-Prover-V2-7B (non-CoT)
and 87.10%, 89.11%, and 95.14% on GSM8K.                                             (Ren et al., 2025), Kimina-Prover-Preview-Distill-
Their feasibility rates also remain below 100% on                                    7B (Wang et al., 2025a), and Goedel-Prover-V2-
both datasets. These results show that existing                                      8B (Lin et al., 2026), denoted as DeepSeek-Prover,
methods can introduce incorrect references or in-                                    Kimina-Prover, and Goedel-Prover, respectively.
valid problems, undermining evaluation reliability.                                  On miniF2F (Zheng et al., 2021), their pass@32
Representative candidate-level failure modes ob-                                     success rates are 68.0%, 63.1%, and 84.6%, respec-
served in our VarBench implementation are further                                    tively (Lin et al., 2026; Wang et al., 2025a).
analyzed in Appendix K.                                                                 Fig. 4 shows that generation success rates gen-
RePro’s gains are not due to subset selection                                        erally increase with stronger ATP capability, while
alone. On the RePro-success subset, baselines still                                  decreasing as problem difficulty increases from
show non-trivial invalidity and incorrectness. Their                                 Level 1 to 5. We also observe that DeepSeek-
correctness rates are 80.65%, 81.05%, and 96.77%                                     Prover performs worse than expected given its
on GSM8K, and 86.88%, 87.66%, and 89.23% on                                          miniF2F performance. Details are in Appendix J.
MATH, respectively. In contrast, RePro remains at                                       This result also highlights a quality-coverage
100% across all criteria, indicating that the gains                                  trade-off. As shown in Table 1, VarBench achieves
mainly come from its verification mechanism rather                                   only 58.76% generation rate on MATH due to
than subset selection.                                                               stricter generation constraints. In contrast, RePro
   As a supplementary reliability check, we inde-                                    maintains a comparable generation rate of 59.16%
pendently audit 2,400 sampled rewritten instances                                    while ensuring both problem validity and answer
across RePro and all baselines. Human judgments                                      correctness through formal verification. Overall,
fully agree with the automatic reliability results.                                  generation success is bounded by current ATP ca-
Details are provided in Appendix H.                                                  pability, and stronger ATPs are expected to further
                                                                                     improve RePro’s coverage.
6.2                         Generation Rate Analysis
We analyze three key factors that affect RePro’s                                     6.2.2                      Effect of Rewriter Capability
generation rate: ATP capability, rewriter capability,                                We further analyze the effect of the rewriter model
and the ATP call limit. Overall, stronger ATPs                                       on RePro’s generation success rate. In this ex-
and rewriters improve generation coverage, while                                     periment, we keep the formalizer, ATP prover,
increasing the ATP call limit brings additional but                                  Lean verification, and answer alignment settings
diminishing gains.                                                                   unchanged, and only replace the model used for
                                                                                     rewriting and feasibility screening.
6.2.1                         Effect of ATP Capability                                 As shown in Fig. 5, the capability of the rewriter
RePro relies on ATPs to generate proofs for formal-                                  model has a clear impact on generation cover-
ized problems, so ATP capability directly affects                                    age. Qwen3-MAX achieves the highest suc-

                                                                                 7
                   (a) Well-definedness                                                                        (b) Feasibility                                                           (c) Answer Correctness
                                                                                                                                                                                                                                                           100


                                                                                                                                                                                                                                                           95
                                                                100                                                                                 100                                                                             100
                                                                                                                                                    99
                                                                 98                                                                                                                                                                 95




                                                                      Percent (%)




                                                                                                                                                          Percent (%)




                                                                                                                                                                                                                                             Percent (%)
                                                                                                                                                    97




                                                                                                                                                                                                                                                                 Percent (%)
                                                                 96                                                                                                                                                                 90                     85
                                                                                                                                                    95
                                                                94                                                                                  93                                                                              85
                                                                92                                                                                  91                                                                              80
                                                                90                                                                                  89                                                                              75                     75
                                                          ReP                                                                               ReP                                                                             ReP
                                                              ro (O                                                                             ro (O                                                                           ro (O
                                                          ITD       urs)                                                                    ITD       urs)                                                                  ITD       urs)
    LV1                                                                                     LV1                                                                                 LV1
           LV2                                 Auto                                               LV2                              Auto                                               LV2                          Auto
                   LV3                              -Data                                                LV3                            -Data                                               LV3                         -Data
            Diff                             VarB         set                                     Diff                           VarB         set                                     Diff                       VarB         set                          65
                icult     LV4                    ench                                                 icult     LV4                   ench                                                icult    LV4                ench
                      y         LV5                                                                        y          LV5                                                                      y          LV5



Figure 7: Rewriting quality comparison across five difficulty levels (LV1–LV5) of the MATH dataset. (a) Proportion
of well-defined problems, (b) proportion of feasible problems, and (c) proportion of correct reference answers.

                                                  (a) Original Accuracy (%)                                                                                             (b) Rewritten Accuracy (%)
              Qwen3-14B               99.5        99.1            97.5              98.0          96.1                100         Qwen3-14B              99.0            97.7           98.5             97.0    98.1               100
        DeepSeek R1-14B               98.5        98.1            98.5              97.0          98.1                      DeepSeek R1-14B              100.0           96.7           96.6             98.0    96.1
               Qwen3-8B               98.5        97.2            96.1              94.6          92.2                80           Qwen3-8B              98.5            95.8           96.6             93.5    94.2               80
        DeepSeek R1-1.5B              97.7        95.1            92.7              93.4          89.3                      DeepSeek R1-1.5B             95.9            93.3           89.0             89.6    83.9
             Qwen3-1.7B               98.6        93.3            95.9              87.7          92.7                           Qwen3-1.7B              99.1            95.1           95.0             94.3    88.8
         DeepSeek R1-7B               95.9        93.8            95.0              90.1          87.3                60     DeepSeek R1-7B              95.0            95.1           90.4             90.1    77.6               60
Model




            Gemma 3 4B                95.9        91.6            95.4              84.4          82.4                          Gemma 3 4B               95.5            92.9           90.9             87.7    82.4
             Qwen3-0.6B               93.6        84.0            86.3              64.2          64.9                40         Qwen3-0.6B              88.1            86.2           82.2             70.8    66.3               40
            Llama-3.2-3B              86.2        75.6            76.7              65.6          65.4                          Llama-3.2-3B             72.0            64.4           61.6             53.3    55.6
            Gemma 3 1B                57.3        51.1            46.1              36.8          22.0                          Gemma 3 1B               62.8            50.7           44.3             34.4    24.4
             Qwen2-1.5B               50.0        35.6            30.1              23.6          20.5                20         Qwen2-1.5B              28.9            23.6           19.6             15.6    15.1               20
            Llama-3.2-1B              28.0        25.3            20.6              16.0          11.7                          Llama-3.2-1B             28.4            24.0           14.6             9.9     10.2
             Qwen2-0.5B               10.6        7.6              8.7              3.3           3.9                            Qwen2-0.5B               7.3            5.3             1.8             1.9     3.9
                                                                                                                      0                                                                                                             0
                                      LV1         LV2              LV3              LV4           LV5                                                     LV1            LV2             LV3             LV4     LV5
                                                                Difficulty                                                                                                            Difficulty
                                                  (c) Absolute Change (pp)                                                                                               (d) Relative Change (%)
              Qwen3-14B            -0.5            -1.4            1.0               -1.0         2.0                 20         Qwen3-14B                -0.5           -1.4            1.0              -1.0    2.1
        DeepSeek R1-14B            1.5             -1.4            -1.9              1.0          -2.0                15   DeepSeek R1-14B                1.5            -1.4            -1.9             1.0     -2.0              60
               Qwen3-8B            0.0             -1.4            0.5               -1.1         2.0                             Qwen3-8B                0.0            -1.4            0.5              -1.2    2.2
        DeepSeek R1-1.5B           -1.8            -1.8            -3.7              -3.8         -5.4                10 DeepSeek R1-1.5B                 -1.8           -1.9            -4.0             -4.1    -6.0              40
             Qwen3-1.7B            0.5             1.8             -0.9              6.6          -3.9                          Qwen3-1.7B                0.5            1.9             -0.9             7.5     -4.2              20
                                                                                                                      5
         DeepSeek R1-7B            -0.9            1.3             -4.6              0.0          -9.7                      DeepSeek R1-7B                -0.9           1.4             -4.8             0.0    -11.1
Model




            Gemma 3 4B             -0.4            1.3             -4.5              3.3          0.0                 0        Gemma 3 4B                 -0.4           1.4             -4.7             3.9     0.0               0
             Qwen3-0.6B            -5.5            2.2             -4.1              6.6          1.4                           Qwen3-0.6B                -5.9           2.6             -4.8            10.3     2.2
            Llama-3.2-3B          -14.2           -11.2           -15.1             -12.3         -9.8                  5      Llama-3.2-3B              -16.5          -14.8           -19.7            -18.7   -15.0                  20
            Gemma 3 1B             5.5             -0.4            -1.8              -2.4         2.4                   10     Gemma 3 1B                 9.6            -0.8            -3.9             -6.5   10.9                   40
             Qwen2-1.5B           -21.1           -12.0           -10.5              -8.0         -5.4                          Qwen2-1.5B               -42.2          -33.7           -34.9            -33.9   -26.3
            Llama-3.2-1B           0.4             -1.3            -6.0              -6.1         -1.5                  15     Llama-3.2-1B               1.4            -5.1           -29.1            -38.1   -12.8                  60
             Qwen2-0.5B            -3.3            -2.3            -6.9              -1.4         0.0                   20      Qwen2-0.5B               -31.1          -30.3           -79.3            -42.4    0.0
                                   LV1             LV2             LV3               LV4          LV5                                                     LV1            LV2             LV3              LV4     LV5
                                                                Difficulty                                                                                                            Difficulty

Figure 8: Impact of problem rewriting on model performance across five difficulty levels. (a) Original accuracy.
(b) Accuracy after rewriting. (c) Absolute accuracy change (percentage points). (d) Relative accuracy change
(percentage). Positive values indicate improvements, while negative values indicate performance drops.


cess rate across all datasets and difficulty levels.                                                                            date that has passed rewriting, feasibility screen-
For example, on GSM8K, Qwen3-MAX reaches                                                                                        ing, and executable formalization. A sample is
88.31%, compared with 68.55% for Qwen3-32B                                                                                      counted as successfully generated if at least one
and 58.87% for Qwen3-8B. A similar trend is ob-                                                                                 proof passes Lean verification and its verified an-
served across MATH difficulty levels, suggesting                                                                                swer matches the target answer.
that stronger rewriters are more likely to produce                                                                                 As shown in Fig. 6, increasing ATP calls consis-
candidates that can be successfully formalized and                                                                              tently improves generation rate. On GSM8K, the
verified. Therefore, we use Qwen3-MAX as the                                                                                    rate increases from 76.21% at pass@1 to 83.87%
default rewriter in the main experiments to obtain                                                                              at pass@2 and 88.31% at pass@3. On MATH
more stable generation coverage.                                                                                                overall, it increases from 50.17% to 55.49% and
                                                                                                                                59.16%, respectively. The same trend holds across
6.2.3              Effect of ATP Call Limit                                                                                     all MATH difficulty levels, showing that additional
We further examine how the ATP call limit affects                                                                               ATP calls can recover part of the failures caused by
RePro’s generation coverage. Here, pass@k allows                                                                                unsuccessful proof generation.
up to k ATP proof-search attempts for each candi-                                                                                    The improvement from pass@2 to pass@3 is

                                                                                                                            8
smaller than that from pass@1 to pass@2, sug-                changes and accuracy drop, and only weak positive
gesting diminishing returns as the ATP call limit            correlations for solution and proof complexity.
increases. We therefore use pass@3 as the default
setting in the main experiments to balance genera-           7   Conclusion
tion coverage and verification cost.
                                                             In this work, we study the reliability of rewriting-
6.3   Impact of Problem Difficulty on Rewriting              based evaluation for contamination-resistant LLM
      Quality                                                benchmarking. Existing rewriting methods can
                                                             reduce memorization effects, but often fail to en-
Fig. 7 shows how rewriting quality changes
                                                             sure problem validity and answer correctness. We
across MATH difficulty levels in terms of well-
                                                             propose RePro, which integrates ATPs and proof-
definedness, feasibility, and answer correctness.
                                                             assistant checking into the rewriting pipeline. Re-
Correctness decreases as problem difficulty in-
                                                             Pro retains only instances that can be successfully
creases. As shown in Fig. 7(c), the correctness
                                                             formalized and verified, ensuring problem validity
of ITD and AutoDataset drops noticeably as diffi-
                                                             and formally supported reference answers. Exper-
culty increases, from around 90% at Level 1-2 to
                                                             iments on MATH and GSM8K show that RePro
about 75%–80% at Level 4-5. This indicates that
                                                             achieves 100% well-defined, feasible, and correct
traditional rewriting methods are more likely to in-
                                                             retained instances, while existing methods still pro-
troduce incorrect reference answers as reasoning
                                                             duce invalid problems or incorrect answers. Further
complexity grows.
                                                             analysis shows that proof-verified rewriting can re-
Well-definedness and feasibility remain stable,
                                                             veal model-specific sensitivity to benchmark refor-
but invalid instances persist. As shown in
                                                             mulation and provide signals of potential memo-
Fig. 7(a)(b), the well-defined and feasible rates of
                                                             rization or benchmark-specific pattern reliance.
AutoDataset, ITD, and VarBench remain between
89% and 100% across all difficulty levels, without           Limitations
clear degradation as difficulty increases. However,
ill-defined or infeasible problems still appear at ev-       While RePro provides the first framework that inte-
ery level, indicating that existing rewriting methods        grates automated theorem proving into benchmark
cannot fully eliminate invalid instances.                    rewriting and constructs evaluation datasets with
                                                             proof-verified reference answers, several limita-
6.4   Rewriting Sensitivity and Potential                    tions remain that we plan to address in future work.
      Memorization                                           Dependence on ATP capability. RePro relies
Fig. 8 compares model accuracy on original MATH              on ATPs to verify candidate solutions during the
problems and their proof-verified rewritten coun-            rewriting. When the underlying ATP fails to find
terparts. Since all retained RePro instances pass            a valid proof, even correct and solvable prob-
validity and answer-correctness verification, this           lems may be filtered out, which can reduce the
paired comparison reduces the influence of invalid           overall generation success rate. This limitation
rewrites or incorrect reference answers. Thus, Re-           mainly reflects the current capability of neural the-
Pro provides a reliable diagnostic tool for analyzing        orem provers rather than the framework itself. As
model sensitivity to benchmark reformulation.                stronger ATP models continue to emerge, the gen-
   The results show that many models, especially             eration coverage of RePro is expected to improve.
smaller ones, lose accuracy after rewriting. For ex-         Formalization constraints. RePro requires rewrit-
ample, Qwen2-1.5B drops by 21.1, 12.0, and 10.5              ten problems to be expressible in the Lean formal
percentage points on Level 1-3, respectively, while          language in order to perform proof verification. As
Llama-3.2-3B drops across all levels, with a maxi-           a result, the current framework mainly applies to
mum drop of 15.1 points. Meanwhile, some mod-                problems that can be rewritten into a Lean represen-
els improve after rewriting, often because rewrit-           tation. Tasks that rely heavily on natural language
ten problems clarify conditions, standardize nota-           semantics or cannot be reasonably formalized in
tion, or reduce diagram-dependent difficulty. These          Lean, such as certain text-based reasoning prob-
mixed effects suggest that proof-verified rewrit-            lems, fall outside the current scope. Nevertheless,
ing reveals model-specific reformulation sensitivity.        ongoing progress in automated formalization and
Appendix I analyzes potential confounds, showing             proof assistants is expected to expand the range of
near-zero correlations between surface or numeric            tasks that can be supported.

                                                         9
Acknowledgements                                                Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian,
                                                                  Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias
This work was supported in part by the Ministry                   Plappert, Jerry Tworek, Jacob Hilton, Reiichiro
of Education and Science of Bulgaria (support for                 Nakano, Christopher Hesse, and John Schulman.
INSAIT, part of the Bulgarian National Roadmap                    2021. Training verifiers to solve math word prob-
                                                                  lems. arXiv preprint arXiv:2110.14168.
for Research Infrastructure), the Shenzhen Insti-
tute of Artificial Intelligence and Robotics for So-            Leonardo De Moura and Nikolaj Bjørner. 2008. Z3:
ciety (AIRS), the Shenzhen Key Laboratory of                      An efficient smt solver. In International conference
                                                                  on Tools and Algorithms for the Construction and
Crowd Intelligence Empowered Low-Carbon En-                       Analysis of Systems, pages 337–340. Springer.
ergy Network (No. ZDSYS20220606100601002),
the National Natural Science Foundation of China                Leonardo De Moura, Soonho Kong, Jeremy Avigad,
(No. 72331009).                                                   Floris Van Doorn, and Jakob von Raumer. 2015. The
                                                                  lean theorem prover (system description). In Inter-
                                                                  national Conference on Automated Deduction, pages
                                                                  378–388. Springer.
References
                                                                Jasper Dekoninck, Nikola Jovanović, Tim Gehrunger,
Janice Ahn, Rishu Verma, Renze Lou, Di Liu, Rui                    Kári Rögnvalddson, Ivo Petrov, Chenhao Sun, and
  Zhang, and Wenpeng Yin. 2024. Large language                     Martin Vechev. 2026. Beyond benchmarks: Math-
  models for mathematical reasoning: Progresses and                arena as an evaluation platform for mathematics with
  challenges. In Proceedings of the 18th Conference                llms. arXiv preprint arXiv:2605.00674.
  of the European Chapter of the Association for Com-
  putational Linguistics: Student Research Workshop,            Bofei Gao, Feifan Song, Zhe Yang, Zefan Cai, Yibo
  pages 225–237, St. Julian’s, Malta. Association for             Miao, Qingxiu Dong, Lei Li, Chenghao Ma, Liang
  Computational Linguistics.                                      Chen, Zhengyang Tang, and 1 others. 2025. Omni-
                                                                  math: A universal olympiad level mathematic bench-
Yves Bertot and Pierre Castéran. 2013. Interactive theo-          mark for large language models. In International
  rem proving and program development: Coq’Art: the               Conference on Learning Representations, volume
  calculus of inductive constructions. Springer Science           2025, pages 100540–100569.
  & Business Media.
                                                                Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song,
Natasha Butt, Varun Chandrasekaran, Neel Joshi, Be-               Peiyi Wang, Qihao Zhu, Runxin Xu, Ruoyu Zhang,
  smira Nushi, and Vidhisha Balachandran. 2024. Ben-              Shirong Ma, Xiao Bi, and 1 others. 2025. Deepseek-
  chagents: Automated benchmark creation with agent               r1 incentivizes reasoning in llms through reinforce-
  interaction. In ICLR 2025 Workshop on Navigat-                  ment learning. Nature, 645(8081):633–638.
  ing and Addressing Data Problems for Foundation
  Models.                                                       Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul
                                                                  Arora, Steven Basart, Eric Tang, Dawn Song, and Ja-
Boxi Cao, Mengjie Ren, Hongyu Lin, Xianpei Han,                   cob Steinhardt. 2021. Measuring mathematical prob-
  Feng Zhang, Junfeng Zhan, and Le Sun. 2024.                     lem solving with the MATH dataset. arXiv preprint
  StructEval: Deepen and broaden large language                   arXiv:2103.03874.
  model assessment via structured evaluation. In Find-
  ings of the Association for Computational Linguistics:        Laura Kovács and Andrei Voronkov. 2013. First-order
  ACL 2024, pages 5300–5318, Bangkok, Thailand. As-               theorem proving and vampire. In International Con-
  sociation for Computational Linguistics.                        ference on Computer Aided Verification, pages 1–35.
                                                                  Springer.
Center for AI Safety, Scale AI, and HLE Contributors
  Consortium. 2026. A benchmark of expert-level aca-            Yucheng Li, Yunhao Guo, Frank Guerin, and Chenghua
  demic questions to assess AI capabilities. Nature,              Lin. 2024. An open-source data contamination report
  649:1139–1146.                                                  for large language models. In Findings of the Associ-
                                                                  ation for Computational Linguistics: EMNLP 2024,
Simin Chen, Yiming Chen, Zexin Li, Yifan Jiang,                   pages 528–541, Miami, Florida, USA. Association
  Zhongwei Wan, Yixin He, Dezhi Ran, Tianle Gu,                   for Computational Linguistics.
  Haizhou Li, Tao Xie, and Baishakhi Ray. 2025.
  Benchmarking large language models under data con-            Bill Yuchen Lin, Ronan Le Bras, Kyle Richardson,
  tamination: A survey from static to dynamic evalu-              Ashish Sabharwal, Radha Poovendran, Peter Clark,
  ation. In Proceedings of the 2025 Conference on                 and Yejin Choi. 2025. Zebralogic: On the scaling
  Empirical Methods in Natural Language Processing,               limits of llms for logical reasoning. arXiv preprint
  pages 10080–10098, Suzhou, China. Association for               arXiv:2502.01100.
  Computational Linguistics.
                                                                Yong Lin, Shange Tang, Bohan Lyu, Ziran Yang,
Yuxing Cheng, Yi Chang, and Yuan Wu. 2025. A survey               Jui-Hui Chung, Haoyu Zhao, Lai Jiang, Yihan
  on data contamination for large language models.                Geng, Jiawei Ge, Jingruo Sun, and 1 others. 2026.
  arXiv preprint arXiv:2502.14425.                                Goedel-prover-v2: Scaling formal theorem proving


                                                           10
  with scaffolded data synthesis and self-correction.         Siyuan Wang, Zhuohan Long, Zhihao Fan, Xuanjing
  2026:11793–11818.                                             Huang, and Zhongyu Wei. 2025b. Benchmark self-
                                                                evolving: A multi-agent framework for dynamic
Chengwu Liu, Jianhao Shen, Huajian Xin, Zhengying               LLM evaluation. In Proceedings of the 31st Inter-
  Liu, Ye Yuan, Haiming Wang, Wei Ju, Chuanyang                 national Conference on Computational Linguistics,
  Zheng, Yichun Yin, Lin Li, and 1 others. 2023. Fimo:          pages 3310–3328, Abu Dhabi, UAE. Association for
  A challenge formal dataset for automated theorem              Computational Linguistics.
  proving. arXiv preprint arXiv:2309.04295.
                                                              Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten
Kun Qian, Shunji Wan, Claudia Tang, Youzhi Wang,                 Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou,
  Xuanming Zhang, Maximillian Chen, and Zhou Yu.                 and 1 others. 2022. Chain-of-thought prompting elic-
  2024. VarBench: Robust language model bench-                   its reasoning in large language models. Advances
  marking through dynamic variable perturbation. In              in neural information processing systems, 35:24824–
  Findings of the Association for Computational Lin-             24837.
  guistics: EMNLP 2024, pages 16131–16161, Miami,
  Florida, USA. Association for Computational Lin-            An Yang, Anfeng Li, Baosong Yang, Beichen Zhang,
  guistics.                                                     Binyuan Hui, Bo Zheng, Bowen Yu, Chang
                                                                Gao, Chengen Huang, Chenxu Lv, and 1 others.
David Rein, Betty Li Hou, Asa Cooper Stickland, Jack-           2025a. Qwen3 technical report. arXiv preprint
  son Petty, Richard Yuanzhe Pang, Julien Dirani, Ju-           arXiv:2505.09388.
  lian Michael, and Samuel R Bowman. 2024. Gpqa:
  A graduate-level google-proof q&a benchmark. In             Kaiyu Yang, Aidan Swope, Alex Gu, Rahul Chala-
  First conference on language modeling.                        mala, Peiyang Song, Shixing Yu, Saad Godil, Ryan J
                                                                Prenger, and Animashree Anandkumar. 2023. Le-
ZZ Ren, Zhihong Shao, Junxiao Song, Huajian Xin,                andojo: Theorem proving with retrieval-augmented
  Haocheng Wang, Wanjia Zhao, Liyue Zhang, Zhe                  language models. Advances in Neural Information
  Fu, Qihao Zhu, Dejian Yang, and 1 others. 2025.               Processing Systems, 36:21573–21612.
  Deepseek-prover-v2: Advancing formal mathemati-
  cal reasoning via reinforcement learning for subgoal        Yuli Yang, Hiroaki Yamada, and Takenobu Tokunaga.
  decomposition. arXiv preprint arXiv:2504.21801.               2025b. Evaluating robustness of LLMs to numer-
                                                                ical variations in mathematical reasoning. In The
Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu,
                                                                Sixth Workshop on Insights from Negative Results
  Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan
                                                                in NLP, pages 171–180, Albuquerque, New Mexico.
  Zhang, YK Li, and 1 others. 2024. Deepseekmath:
                                                                Association for Computational Linguistics.
  Pushing the limits of mathematical reasoning in open
  language models. arXiv preprint arXiv:2402.03300.           Jiahao Ying, Yixin Cao, Yushi Bai, Qianru Sun,
C Spearman. 1904. The proof and measurement of as-               Bo Wang, Wei Tang, Zhaojun Ding, Yizhe Yang,
  sociation between two things. The American Journal             Xuanjing Huang, and Shuicheng YAN. 2024. Au-
  of Psychology, 15(1):72–101.                                   tomating dataset updates towards reliable and timely
                                                                 evaluation of large language models. In The Thirty-
Gemma Team, Aishwarya Kamath, Johan Ferret, Shreya               eight Conference on Neural Information Processing
  Pathak, Nino Vieillard, Ramona Merhej, Sarah Perrin,           Systems Datasets and Benchmarks Track.
  Tatiana Matejovicova, Alexandre Ramé, Morgane
  Rivière, and 1 others. 2025. Gemma 3 technical              Weiqi Zhai, Zhihai Wang, Jinghang Wang, Boyu Yang,
  report. arXiv preprint arXiv:2503.19786.                     Xiaogang Li, Xander Xu, Bohan Wang, Peng Wang,
                                                               Xingzhe Wu, Anfeng Li, and 1 others. 2026. Hle-
Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier          verified: A systematic verification and structured
  Martinet, Marie-Anne Lachaux, Timothée Lacroix,               revision of humanity’s last exam. arXiv preprint
  Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal            arXiv:2602.13964.
  Azhar, and 1 others. 2023. Llama: Open and effi-
  cient foundation language models. arXiv preprint            Yilun Zhao, Guo Gan, Chengye Wang, Chen Zhao, and
  arXiv:2302.13971.                                             Arman Cohan. 2025. Are multimodal LLMs robust
                                                                 against adversarial perturbations? RoMMath: A sys-
Haiming Wang, Mert Unsal, Xiaohan Lin, Mantas                    tematic evaluation on multimodal math reasoning. In
  Baksys, Junqi Liu, Marco Dos Santos, Flood Sung,              Proceedings of the 2025 Conference of the Nations
  Marina Vinyes, Zhenzhe Ying, Zekai Zhu, and 1 oth-             of the Americas Chapter of the Association for Com-
  ers. 2025a. Kimina-prover preview: Towards large               putational Linguistics: Human Language Technolo-
  formal reasoning models with reinforcement learning.           gies (Volume 1: Long Papers), pages 11653–11665,
  arXiv preprint arXiv:2504.11354.                              Albuquerque, New Mexico. Association for Compu-
                                                                 tational Linguistics.
Haoyu Wang, Guangyuan Dong, He Liang, Zijing
  Zhang, Jiachen Luo, Chuang Liu, Chao Xue, and               Kunhao Zheng, Jesse Michael Han, and Stanislas Polu.
  Hao Tang. 2026. Memguard: Persisting verifier sig-            2021. Minif2f: a cross-system benchmark for for-
  nals for llm-agent memory governance. Preprint,               mal olympiad-level mathematics. arXiv preprint
  arXiv:2608.21867.                                             arXiv:2109.00110.


                                                         11
Xiyuan Zhou, Xinlei Wang, Yirui He, Ruixi Zou, Yang
  Wu, Yuheng Cheng, Yulu Xie, Wenxuan Liu, Huan
  Zhao, Yan Xu, and 1 others. 2026a. Engibench: A
  benchmark for evaluating large language models on
  engineering problem solving. In Findings of the As-
  sociation for Computational Linguistics: ACL 2026,
  pages 36308–36334.
Xiyuan Zhou, Ruixi Zou, Xinlei Wang, Yuheng Cheng,
  Yan Xu, Junhua Zhao, and Jinjin Gu. 2026b. Engia-
  gent: Fully connected coordination of LLM agents
  for solving open-ended engineering problems with
  feasible solutions. In Forty-third International Con-
  ference on Machine Learning.
Yue Zhou, Yada Zhu, Diego Antognini, Yoon Kim, and
  Yang Zhang. 2024. Paraphrase and solve: Explor-
  ing and exploiting the impact of surface form on
  mathematical reasoning in large language models.
  In Proceedings of the 2024 Conference of the North
  American Chapter of the Association for Computa-
  tional Linguistics: Human Language Technologies
  (Volume 1: Long Papers), pages 2793–2804, Mexico
  City, Mexico. Association for Computational Lin-
  guistics.
Qin Zhu, Qinyuan Cheng, Runyu Peng, Xiaonan Li,
  Ru Peng, Tengxiao Liu, Xipeng Qiu, and Xuan-
  jing Huang. 2024. Inference-time decontamination:
  Reusing leaked benchmarks for large language model
  evaluation. In Findings of the Association for Com-
  putational Linguistics: EMNLP 2024, pages 9113–
  9129, Miami, Florida, USA. Association for Compu-
  tational Linguistics.
Thomas Zhu, Joshua Clune, Jeremy Avigad, Al-
  bert Qiaochu Jiang, and Sean Welleck. 2025. Premise
  selection for a lean hammer.        arXiv preprint
  arXiv:2506.07477.




                                                          12
A     The Use of Large Language Models                          Problem rewriting prompt. The rewriting
                                                                prompt asks the model to generate a new prob-
    In this work, LLMs were used in four main ways:             lem while preserving the underlying mathematical
                                                                structure, solution logic, and answer type. It explic-
    1. Benchmark rewriting and feasibility                      itly forbids solving the problem or computing the
       screening. LLMs were used to generate                    new answer.
       rewritten problem instances from existing            1 You are a top-level exam question design expert. Your goal
       benchmarks and to perform preliminary                          is to rewrite the given question while preserving its
                                                                      core mathematical structure, solution logic, and
       feasibility screening by identifying obviously                 difficulty, but making it entirely new in form,
                                                                      wording, and surface meaning.
       invalid, ambiguous, or infeasible rewritten          2
       instances.                                           3 General requirements:
                                                            4 1. The rewritten question remains solvable and maintains a
                                                                      similar level of difficulty.
                                                            5 2. The underlying mathematical relationships, reasoning
    2. Semantic consistency checking during for-                      method, and solution logic remain equivalent.
                                                            6 3. The rewritten question is valid and logically consistent.
       malization. LLMs were used to assess                 7 4. The rewritten question is entirely different from the
       whether rewritten natural-language problems                    original in surface form, wording, and semantics.
                                                            8 5. No part of the original phrasing, expressions, or
       are semantically consistent with their corre-                  narrative should be reused.
                                                            9 6. If a previous rewrite is provided, the new rewrite must
       sponding Lean formal statements. This check                    be significantly different from it.
       serves only as a conservative pre-proof filter      10
                                                           11 For word problems:
       and does not provide formal verification of         12 1. Completely change the story context or scenario.
                                                           13 2. Change the time, place, characters, identities, and
       natural-language-to-Lean equivalence.                          physical quantities involved.
                                                           14 3. Use realistic and physically possible situations.
                                                           15 4. Choose a target unknown that is clearly well-defined and
    3. Answer extraction and target-answer                            not semantically ambiguous.
                                                           16
       matching. LLMs were used to extract candi-          17    For pure mathematical problems:
                                                           18    1. Keep the rewritten question purely mathematical.
       date final answers from Lean-verified proofs        19    2. Do not introduce a story or real-world context.
       and check whether the extracted spans match         20
                                                           21    Rewriting strategies:
       the quantities requested by the rewritten prob-     22    - Numerical reparameterization.
                                                           23    - Logical restructuring.
       lems. Candidate answers were restricted to          24    - Constraint modification.
       spans that appear verbatim in the verified Lean     25    - Contextual reconstruction for word problems.
                                                           26
       proof, and no additional computation, simpli-       27    Answer-type preservation:
                                                           28    The rewritten problem must preserve the type of the expected
       fication, or reasoning was allowed.                              answer from the original problem, such as integer,
                                                                       rational number, interval, or finite set. Do not solve
                                                                        the problem or compute the answer. Enforce answer-
    4. Figure and language assistance. AI tools                        type preservation structurally, for example by using
                                                                       linear expressions, proportional relationships, or
       were used to generate some visual icons in                      factorizable polynomials when the original answer is
                                                                       rational or integral.
       Fig. 1 and Fig. 2, where applicable, other          29
                                                           30 Return valid JSON only:
       illustrative icons used in the figures. AI tools    31 {
       were also used for grammar checking and lan-        32   "rewritten_question": "<the rewritten question as a string
                                                                      >"
       guage refinement during the writing of this         33 }

       paper. All scientific claims, experimental re-
                                                                  The runtime user input is:
       sults, and analyses were reviewed and verified
       by the authors.                                      1 Original question:
                                                            2 <original problem>


B Prompt Templates and Implementation                           Feasibility screening prompt. Feasibility
  Details                                                       screening is used as an early filter. Its purpose is
                                                                to reject rewritten questions that are ill-defined,
This appendix reports the main prompt templates
                                                                infeasible, ambiguous, internally inconsistent, or
and implementation details used in RePro. We in-
                                                                unrealistic. It does not establish reference-answer
clude the prompts for problem rewriting, feasibility
                                                                correctness; answer correctness is established later
screening, semantic alignment screening, proof-
                                                                through Lean verification.
grounded answer extraction, and final-answer clas-
                                                            1 You are an expert in mathematics and careful problem
sification. The templates are lightly formatted for                   interpretation.
readability. The released code contains the exact           2
                                                            3 Your task is not only to check whether the problem is
runtime prompts and parsing logic.                                    mathematically solvable, but to judge whether it is



                                                          13
           well-defined, unambiguous, and valid under strict            rather than a formal proof of natural-language-to-
           interpretation.
4                                                                       Lean equivalence.
5 First classify the problem into one of two categories:
6                                                                   1 You are an expert in analyzing semantic consistency between
7 (A) Pure mathematical problem:                                              a natural language math problem and its formal
8 - No real-world story or physical interpretation is involved                representation in Lean 4.
           .                                                        2
9 - Examples include solving equations, finding domains,            3 Your task is to judge whether the formal statement matches
           simplifying expressions, algebraic manipulation, and               the natural language problem semantically.
           function properties.                                     4
10                                                                  5 You must not solve the problem, compute any values, or
11 (B) Real-world or applied problem:                                         verify the correctness of the result. Your task is
12 - The problem refers to people, objects, money, measurements               purely semantic.
           , experiments, physical processes, or real-world         6
           actions.                                                 7 A formalization is considered Consistent if and only if:
13                                                                  8 1. The same quantities are being referred to.
14    Then apply the corresponding verification standard.           9 2. The same conditions are imposed.
15                                                                 10 3. The same logical structure is preserved.
16 Your tasks:                                                     11 4. The same type of object is being reasoned about, such as
17 1. Solve the problem.                                                    discrete vs continuous, individual vs aggregate, or
18 2. Classify it as either (A) pure mathematical or (B) real-              instance vs range.
         world/applied.                                            12 5. The same target quantity is being characterized.
19 3. Judge whether the problem statement and the final            13
         numerical answer are valid under the appropriate          14 Judge the formalization as Inconsistent if any of the
         strict standard.                                                     following occurs:
20                                                                 15 A. Logical structure mismatch.
21    For pure mathematical problems, check:                       16 B. Wrong target quantity.
22    - Uniqueness.                                                17 C. Quantitative mismatch in numbers, constraints, arithmetic
23    - Mathematical clarity.                                                   relationships, units, or constants.
24    - Answer-type and format consistency.                        18    D. Missing condition.
25    - Mathematical reasonableness.                               19    E. Extra condition.
26                                                                 20
27    For real-world or applied problems, check:                   21    Special warning about rounding, ceiling, and floor:
28    - Uniqueness.                                                22    If the natural language problem requires a rounding
29    - Semantic clarity.                                                      convention, such as "must buy whole items" or "round
30    - Real-world executability.                                              up", and the Lean formalization fails to encode that
31    - Unit and meaning consistency.                                          convention correctly, then it is inconsistent.
32    - Reasonableness.                                            23
33                                                                 24 The natural-language meaning must match exactly. Even a
34    For both categories:                                                    small mismatch means Inconsistent.
35    If there is any ambiguity, vagueness, underspecification,    25
            incompatible condition, or mismatch between the        26    Return valid JSON only:
            mathematical answer and the required interpretation    27    {
            standard, the verdict must be "no".                    28       "judgment": "Consistent",
36                                                                 29       "explanation": "<reason>"
37 Return valid JSON only:                                         30    }
38 {                                                               31    or
39   "analysis": "<solution and checks>",                          32    {
40   "verdict": "yes/no"                                           33       "judgment": "Inconsistent",
41 }                                                               34       "explanation": "<reason>"
                                                                   35    }

       The runtime user input is:                                         The runtime user input is:
1 Question:
2 <rewritten problem>
                                                                    1    Natural language problem:
                                                                    2    <rewritten problem>
                                                                    3
                                                                    4    Lean 4 formal statement:
     Formalization and proof-generation prompts.                    5    <Lean theorem statement>

     The formalizer and prover are called through back-                    For each compiled Lean statement, the semantic
     end models with short task instructions. The gener-                checker is queried three times. The candidate is
     ated Lean statement must compile before semantic                   retained only when all three responses return Co
     screening. A generated proof is accepted only if it                nsistent. Any Inconsistent response, parsing
     passes Lean checking and does not contain sorry.                   failure, malformed output, or uncertain response
1 Formalize the following question in Lean 4:                           leads to rejection and regeneration.
2 <rewritten problem>

                                                                        Proof-grounded answer extraction prompt.
1 Prove the following statement in Lean 4 without using 'sorry
           ':
                                                                        After a proof passes Lean verification, RePro ex-
2 <Lean formal statement>                                               tracts an answer candidate from the verified proof.
                                                                        The extractor is read-only: it may only copy spans
     Semantic alignment screening prompt. The se-                       that already appear in the Lean proof text.
     mantic alignment prompt checks whether a com-                  1    You are a strict answer extractor for Lean 4 proof text.
                                                                    2
     piled Lean statement appears to encode the same                3    You are given:
     task as the rewritten natural-language problem.                4    - The natural-language problem.
                                                                    5    - The Lean 4 proof text.
     This step is an LLM-assisted conservative screen               6




                                                                  14
7 Your job:                                                           7
8 - Identify the exact final numeric answer or answers                8 The candidate may contain multiple requested quantities
           requested by the natural-language problem.                            separated by commas at top level.
 9   - You must not compute anything.                                 9
10   - You must not simplify anything.                               10 Your job:
11   - You must not evaluate arithmetic expressions.                 11 Do not compute or simplify anything. Decide whether the
12   - You must only copy answer candidates that literally appear                candidate is one of the following:
            in the Lean text.                                        12
13                                                                   13 final:
14 If the natural-language problem asks for multiple quantities      14 Exactly the quantity or quantities asked, with no further
          , then extract all of them and output them in one                      computation, simplification, or evaluation needed.
          string separated by top-level commas.                      15
15                                                                   16 intermediate:
16 Allowed:                                                          17 An unfinished form that would require computation,
17 - Copy existing expressions from the Lean text as-is.                         simplification, or evaluation.
18 - Select the expressions that match the quantity asked by         18
          the problem.                                               19 wrong_target:
19                                                                   20 A valid statement or value, but not the quantity requested
20   Not allowed:                                                                by the problem.
21   - Arithmetic.                                                   21
22   - Evaluation of powers or factorials.                           22 unknown:
23   - Symbolic simplification.                                      23 No unique final answer can be determined from the provided
24   - Cancellation, expansion, or fraction reduction.                           text or candidate, or the proof determines only part
25   - Any inference requiring a new step.                                       of the requested quantities.
26   - Using results from interactive commands such as #eval, #      24
           reduce, #check, or #print.                                25 Strict rules:
27                                                                   26 - Any candidate containing an unexecuted arithmetic operator
28   Return valid JSON only:                                                      or evaluation, such as +, -, *, /, ^, or !, should be
29   {                                                                            treated as intermediate unless the problem explicitly
30     "answer": "<string>",                                                      asks for that exact expression form.
31     "evidence": "<snippet copied from Lean text>"                 27    - Any candidate relying on #eval, #reduce, #check, or #print
32   }                                                                            is unknown.
33                                                                   28    - If the problem asks for multiple quantities but the
34   If no unique literal answer candidate can be found, or if                   candidate provides fewer, classify it as unknown.
           the proof determines only part of the requested           29    - Do not invent semantic conversions.
           quantities, return:                                       30    - Do not evaluate products or powers.
35   {                                                               31
36     "answer": "unknown",                                          32 Return valid JSON only:
37     "evidence": "unknown"                                         33 {
38   }                                                               34   "answer": "<string>",
                                                                     35   "status": "final|intermediate|wrong_target|unknown",
                                                                     36   "explanation": "<short reason>"
       The runtime user input is:                                    37 }

1    Natural language problem:
2    <rewritten problem>                                                      The runtime user input is:
3
4    Lean 4 proof text:                                               1    Natural language problem:
5    <Lean proof>                                                     2    <rewritten problem>
6                                                                     3
7    Task:                                                            4    Lean 4 proof text:
8    Identify the requested quantity or quantities and extract        5    <Lean proof>
           the answer candidate only by copying from the Lean         6
           text. Do not compute or simplify. Do not use #eval, #      7    Extracted candidate:
           reduce, #check, or #print results.                         8    <candidate answer>
                                                                      9
                                                                     10    Evidence snippets:
        In addition to the prompt, RePro applies string-             11    <snippets copied from Lean text>
     level checks to ensure that every comma-separated               12
                                                                     13    Now classify the candidate under the strict rules and output
     part of the extracted answer appears in the Lean                             JSON only.
     proof text. Candidates that appear only near inter-
                                                                             Only candidates classified as final are accepted
     active commands such as #eval, #reduce, #chec
                                                                          as reference answers. Candidates classified as i
     k, or #print are rejected.
                                                                          ntermediate, wrong_target, or unknown are re-
     Final-answer classification prompt. Literal ex-                      jected, and the corresponding rewritten instance is
     traction alone is insufficient because a verified                    not retained.
     proof may contain intermediate values or values for
     a different target. RePro therefore uses a second                    C     Semantic Alignment Screening and
     classifier to determine whether the extracted candi-                       Target-Answer Matching
     date is the final answer requested by the rewritten                  During executable formalization, RePro adopts a
     problem.                                                             layered validation design to reduce the risk of se-
1 You are a strict classifier for extracted answers from Lean             mantic mismatch between the rewritten natural-
          4 proof text.
2                                                                         language problem and the Lean formal statement.
3    You are given:
4    - The natural-language problem.                                      This design contains two complementary steps.
5    - The Lean proof text.                                               First, before proof search, an LLM-assisted seman-
6    - An extracted answer candidate string that appears in the
           Lean text.                                                     tic alignment screen filters out Lean statements

                                                                    15
that are syntactically valid but appear semantically            During answer extraction, the candidate answer
inconsistent with the rewritten problem. Second,             must be copied from literal spans that already ap-
after Lean verification, a proof-grounded target-            pear in the verified proof. The extractor is not
answer matching step checks whether the extracted            allowed to perform additional computation, nor-
answer corresponds to the final quantity requested           malization, simplification, or inference. Candidates
by the rewritten problem.                                    that appear only in interactive commands such as
                                                             #eval, #reduce, #check, or #print are rejected.
Semantic alignment screen. After a generated                    During answer classification, RePro determines
Lean statement passes compilation, RePro ap-                 whether the copied candidate is the final answer,
plies a conservative semantic alignment screen.              an intermediate value, a wrong-target value, an
The checker receives only the rewritten natural-             unresolved expression, or unknown. A rewritten
language problem and the generated Lean 4 state-             instance is retained only when the candidate is clas-
ment. It does not receive the original problem,              sified as final and matches the target quantity
the final answer, or the proof, and is explicitly in-        requested by the rewritten problem.
structed not to solve the problem, compute any
value, or judge answer correctness. Instead, it              Reliability scope. The semantic alignment
checks whether the Lean statement preserves the              screen is not a formal proof of natural-language-
same quantities, conditions, logical structure, ob-          to-Lean equivalence. Instead, it serves as a con-
ject type, and target quantity as the rewritten prob-        servative pre-proof filter to reduce apparent se-
lem.                                                         mantic drift before formal verification. RePro
   A formalization is rejected if the checker detects        does not rely on a single LLM judgment to es-
mismatched constants, arithmetic relations, units,           tablish retained-instance reliability. Instead, it uses
constraints, variable domains, logical connectives,          multiple automated safeguards to reduce false ac-
target quantity, or required discrete operations such        ceptance: Lean compilation, conservative seman-
as rounding, ceiling, or floor behavior. Missing             tic screening, ATP-generated proof verification by
conditions and extra conditions are also treated as          Lean, proof-grounded answer extraction, and strict
semantic mismatches.                                         target-answer matching. The strongest formal guar-
                                                             antee applies to the Lean-verified proof for the ac-
Conservative all-pass policy. To reduce false                cepted formal statement, while natural-language-
acceptance, we adopt a conservative all-pass pol-            to-Lean alignment and final answer-target align-
icy. For each compiled Lean statement, the                   ment are supported by conservative LLM-assisted
semantic checker is queried three times using                screening, proof-grounded extraction constraints,
Qwen3-Max with temperature zero. A candidate                 and strict classification.
passes semantic screening only if all three calls re-
turn Consistent. Any Inconsistent judgment,                  D    Obtaining the Final Answer from
JSON parsing failure, malformed output, or uncer-                 Verified Proofs
tain response leads to rejection and regeneration.
This policy makes the screen intentionally conser-           Design goal. After a formally verified proof is
vative: it may discard some valid formalizations,            obtained, the system must recover the final an-
but it reduces the chance that an apparent semantic          swer corresponding to the quantity requested in
mismatch enters proof search.                                the rewritten problem. A key requirement is that
                                                             this post-proof stage must not introduce any new
Target-answer matching after Lean verification.              reasoning beyond the verified proof itself.
Semantic screening checks whether the Lean state-               A naive design would directly generate the final
ment appears to encode the same task as the rewrit-          answer from the proof. However, this would allow
ten problem, but it is not used to verify answer             post-hoc computation, simplification, or selection
correctness. Therefore, RePro applies a separate             among intermediate results, effectively turning an-
target-answer matching step after proof-level ver-           swer reporting into a second solving process. Such
ification. This step consists of two strictly con-           behavior would weaken the RePro guarantee and re-
strained substeps: extracting an answer candidate            duce reproducibility. To avoid this issue, post-proof
from the Lean-verified proof and then checking               answer recovery is divided into two constrained
whether the candidate is the final quantity requested        steps: literal answer extraction and final-answer
by the rewritten problem.                                    checking.

                                                        16
Literal answer extraction. The first step is                 ing, while also matching the current capability
purely read-only. It extracts spans that appear              range of Lean-oriented neural ATPs. GSM8K con-
verbatim in the verified proof and does not allow            tains structured grade-school math word problems
computation, normalization, inference, or rewrit-            with a relatively convergent solution space, making
ing. Thus, the procedure may copy text from the              it suitable for controlled rewriting. MATH cov-
proof, but may not derive new text.                          ers five AoPS difficulty levels, ranging from basic
   For example, if the proof contains have h : x             high-school exercises to olympiad-level problems,
= 17 := by ..., then 17 can be extracted. If the             enabling evaluation across different reasoning com-
proof contains 2 + 3, outputting 5 is not allowed. If        plexities.
the proof contains {3}, outputting 3 is not allowed             We also considered harder benchmarks such as
unless 3 also appears explicitly.                            AIME and Omni-MATH. However, our prelim-
   For problems with multiple target quantities, all         inary experiment on 30 AIME 2025 problems
corresponding spans are returned, separated by               (Dekoninck et al., 2026) yields a RePro genera-
commas, without reordering or reformatting.                  tion success rate of 0%, suggesting that current
   For instance, if the proof contains a = 2 and b           ATP-based verification may still be insufficient
= 5, the extractor may output 2, 5, but not (2,5)            for reliably constructing rewritten instances at
unless that exact form appears in the proof.                 this difficulty level. This observation is also con-
                                                             sistent with recent results on high-difficulty for-
Final-answer checking. Literal extraction alone              mal proof generation benchmarks such as FIMO
does not guarantee that the extracted span corre-            (Liu et al., 2023) and DeepSeek-ProverBench (Ren
sponds to the quantity requested in the problem,             et al., 2025), which are relevant to olympiad-style
since a verified proof may contain intermediate              formal reasoning. Under pass@32, current 7B-8B
values, auxiliary constants, or witness terms.               Lean-oriented prover models achieve only 3.35-
   Therefore, a second step checks whether the ex-           7.05% on FIMO and 0.31-1.53% on DeepSeek-
tracted candidate matches the target quantity speci-         ProverBench, as summarized in Table 2 (Lin et al.,
fied in the rewritten problem. Importantly, this step        2026). Therefore, we focus on the relatively
is restricted to target alignment only: it does not          more tractable GSM8K and MATH benchmarks in
generate a new answer, perform additional compu-             this work, and leave broader evaluation on harder
tation, or replace the extracted span with a derived         benchmarks such as AIME and Omni-MATH to
result.                                                      future work as ATP capabilities improve.
   For example, if the problem asks for x + y and
the proof contains x = 3, y = 4, and x + y =                  Model                   FIMO DeepSeek-ProverBench
7, then 3 and 4 are proof-grounded but not final,             DeepSeek-Prover-V2-7B    5.70            0.31
while 7 is both proof-grounded and final.                     Kimina-Prover-7B         3.35            1.38
   If the problem asks for both a and b, and the              Goedel-Prover-V2-8B      7.05            1.53
proof contains a = 2, b = 5, and a+b = 7, then 2,
                                                             Table 2: Pass@32 success rates of recent Lean-oriented
5 is final, whereas 7 is not.                                prover models on high-difficulty formal proof genera-
                                                             tion benchmarks. The low scores indicate a substantial
Summary. This design guarantees (1) traceabil-
                                                             ATP bottleneck for harder olympiad-style benchmarks.
ity to the verified proof, (2) no answer generation
after proof verification, and (3) alignment with the
                                                             Sampling protocol. Specifically, we adopt a re-
quantity requested in the problem.
                                                             jection sampling procedure: candidate problems
   As a result, the final reported answer remains
                                                             are randomly drawn from the source datasets and
proof-grounded, query-aligned, and free of post-
                                                             passed through the RePro pipeline. Only instances
hoc reasoning, which preserves the RePro princi-
                                                             that satisfy all verification criteria are retained. This
ple.
                                                             process continues until the number of valid rewrit-
E Dataset Selection and Data Distribution                    ten instances reaches around 200 for each subset.
                                                             Full dataset. The full dataset refers to all sampled
Dataset selection. We select GSM8K and MATH                  candidate problems before filtering. As shown in
for systematic evaluation because they remain                Fig. 9, the number of sampled candidates varies
widely used benchmarks for mathematical reason-              across subsets because rejection sampling contin-
ing, contamination analysis, and benchmark rewrit-           ues until approximately 200 verified instances are

                                                        17
obtained for each subset. Consequently, harder                                                           verified proof. Only instances that pass the RePro
levels such as LV4 and LV5 require substantially                                                         verification pipeline are retained.
more sampled candidates due to their lower reten-                                                          Each instance contains the following fields:
tion rates.
                                                                                                            • original_question – Original problem state-
RePro successful generation subset. The final
                                                                                                              ment sampled from the source benchmark.
evaluation set consists only of instances that pass
RePro verification. Due to the rejection sam-                                                               • original_answer – Ground-truth answer to
pling process, the resulting subset exhibits a nearly                                                         the original problem.
uniform distribution, with approximately 200 in-
stances per difficulty level.                                                                               • rewritten_question – Rewritten version of
Retention-rate analysis. As shown in Fig. 9, the                                                              the original problem generated by the rewrit-
retention rate decreases substantially as problem                                                             ing pipeline.
difficulty increases. Specifically, RePro retains                                                           • new_answer – Reference answer correspond-
88.3% of sampled GSM8K candidates, while the                                                                  ing to the rewritten problem.
retention rates on MATH are 92.2%, 75.8%, 73.9%,
57.1%, and 33.7% for LV1–LV5, respectively. This                                                            • lean_proof – Formal proof in Lean that veri-
pattern reveals a clear difficulty-dependent selec-                                                           fies the correctness of the rewritten problem
tion effect: under current formalization and prov-                                                            and its answer.
ing capabilities, harder problems are less likely to                                                     G Representative Successful RePro Cases
pass the full verification pipeline. Consequently,
although rejection sampling produces a nearly                                                            This section presents representative successful gen-
balanced final subset with approximately 200 in-                                                         eration cases from RePro. Each case includes the
stances per difficulty level, this retained subset does                                                  original problem, the rewritten problem, the Lean
not preserve the original difficulty distribution of                                                     formal statement, the verified answer, and a short
MATH. This observation further highlights that the                                                       explanation of why the instance passes the RePro
current coverage of RePro is constrained by the                                                          verification pipeline. To avoid LaTeX compila-
capabilities of the underlying formalizer and ATP.                                                       tion issues with Unicode symbols, we display Lean
Reproducibility. All generated datasets, includ-                                                         statements in ASCII form. The complete Lean
ing rewritten problems and their formally verified                                                       proofs are included in the released dataset.
proofs, are publicly released to facilitate repro-                                                       Case 1. GSM8K word problem with unit con-
ducibility and further research.                                                                         version. Original problem. James buys 2 note-
                                                                                                         books with 50 pages each. He pays $5. How many
                                                                                        597
                      600          Full Dataset                                                          cents did each page cost?
                                   RePro Subset
                      500
                                                                                                           Rewritten problem. A student purchases 4
Number of Instances




                                                                                                         sketchbooks, each containing 80 sheets of paper,
                      400
                                                                            352                          for a total of $16. What is the cost per sheet in
                      300
                            248
                                                    281         276                                      cents?
                                  219   218               213
                      200
                                              201                     204         201         201          Verified answer. 5
                                                                                                           Lean formal statement.
                      100
                                                                                                     1 theorem cost_per_sheet :
                        0                                                                            2   let total_cost_cents : Rat := 16 * 100
                            GSM8K        LV1         LV2         LV3         LV4         LV5         3   let total_sheets : Rat := 4 * 80
                                                Dataset / Difficulty Level                           4   total_cost_cents / total_sheets = 5 := by


Figure 9: Data distribution before and after RePro filter-
                                                                                                             Verification outcome. The ATP-generated
ing.                                                                                                     proof is accepted by Lean. The proof establishes
                                                                                                         that the total cost is 1600 cents, the total number of
                                                                                                         sheets is 320, and the unit cost is 5 cents per sheet.
F                      RePro Dataset Metadata                                                                Why this instance passes RePro. The rewrit-
                                                                                                         ten problem is well-defined because the requested
Each instance in the RePro dataset corresponds to a                                                      quantity, cost per sheet in cents, is explicit. It is
rewritten problem derived from GSM8K or MATH,                                                            feasible because the monetary and counting quan-
together with its reference answer and a formally                                                        tities are realistic and internally consistent. The

                                                                                                    18
 Lean statement preserves the same unit-conversion              Case 4. MATH optimization problem with a
 structure as the natural-language problem. The fi-             minimum value. Original problem. Square
 nal answer is extracted from the verified proof and            A and Square B are both 2009 by 2009 squares.
 corresponds to the requested quantity.                         Square A has both its length and width increased
                                                                by an amount x, while Square B has both its length
 Case 2. MATH inverse-function problem with                     and width decreased by the same amount x. What
 a set-valued answer. Original problem. Define                  is the minimum value of x such that the difference
 f (x) = 3x − 8. If f −1 is the inverse of f , find the         in area between the two new squares is at least as
 value or values of x for which f (x) = f −1 (x).               great as the area of a 2009 by 2009 square?
    Rewritten problem. Let g(x) = 5x − 12. If                      Rewritten problem. Two identical square plots
 g −1 denotes the inverse function of g, determine              of land each measure 1873 meters on a side. One
 all real numbers x such that g(x) = g −1 (x).                  plot is expanded by adding y meters to both its
    Verified answer. {3}                                        length and width, while the other is reduced by
    Lean formal statement.                                      subtracting y meters from both its length and width.
1 theorem g_inverse :                                           What is the smallest positive value of y such that
2   let g : Real -> Real := fun x => 5 * x - 12                 the absolute difference in area between the two
3   let g_inv : Real -> Real := fun x => (x + 12) / 5
4   {x : Real | g x = g_inv x} = ({3} : Set Real) := by         modified plots is at least equal to the area of one
                                                                original plot?
    Verification outcome. The ATP-generated
                                                                   Verified answer. 1873/4
 proof is accepted by Lean. The proof verifies the
                                                                   Lean formal statement.
 equality between the solution set of g(x) = g −1 (x)
                                                            1 theorem minimum_area_difference :
 and the singleton set {3}.                                 2   let original_side : Real := 1873
    Why this instance passes RePro. The rewrit-             3   let expanded_area : Real -> Real :=
                                                            4     fun y => (original_side + y)^2
 ten problem has a clear target: the full set of real       5   let reduced_area : Real -> Real :=
                                                            6     fun y => (original_side - y)^2
 solutions. The formal statement encodes the func-          7   let original_area : Real := original_side^2
                                                            8   let area_difference : Real -> Real :=
 tion, its inverse, and the requested solution set. The     9     fun y => abs (expanded_area y - reduced_area y)
 proof verifies set equality rather than merely show-      10   let condition : Real -> Prop :=
                                                           11     fun y => And (y > 0) (original_area <= area_difference y
 ing that one candidate solution works. This en-                      )
                                                           12     Exists (fun y : Real =>
 sures that the retained answer is proof-grounded          13       And (y = original_side / 4)
 and target-aligned.                                       14         (And (condition y)
                                                           15           (forall z : Real, condition z -> y <= z))) := by

 Case 3. MATH symbolic factorization problem.                      Verification outcome. The ATP-generated
 Original problem. Factor 36 − 4x2 completely.                  proof is accepted by Lean. The proof verifies that
   Rewritten problem. Factor 81 − 9y 2 com-                     y = 1873/4 satisfies the area-difference condition
 pletely.                                                       and that every positive value satisfying the condi-
   Verified answer. 9(3 − y)(3 + y)                             tion is at least 1873/4.
   Lean formal statement.                                          Why this instance passes RePro. This case
1 theorem factor_81_minus_9y2 (y : Real) :
                                                                demonstrates a more complex successful rewrite.
2   81 - 9 * y^2 = 9 * (3 - y) * (3 + y) := by                  The rewritten problem changes the numerical pa-
                                                                rameter and real-world context while preserving
    Verification outcome. The ATP-generated
                                                                the optimization structure. The Lean statement en-
 proof is accepted by Lean. The proof verifies the
                                                                codes the positivity condition, the area inequality,
 algebraic identity between the original expression
                                                                and the minimality requirement. Therefore, the
 and the factored expression.
                                                                pipeline does not merely verify that the answer sat-
    Why this instance passes RePro. This case
                                                                isfies the inequality; it also verifies that it is the
 shows that RePro supports symbolic answers, not
                                                                smallest valid value.
 only numerical answers. The rewritten problem
 asks for a factored expression, and the Lean state-            Summary. These cases illustrate different types
 ment verifies the equivalence between the expanded             of retained RePro instances. Case 1 shows a real-
 and factored forms. The answer extraction step                 world arithmetic problem with unit conversion.
 accepts the expression because the requested tar-              Case 2 shows a set-valued algebraic answer. Case
 get is a symbolic factorization and the answer is              3 shows a symbolic expression answer. Case 4
 grounded in the verified proof.                                shows an optimization problem requiring a mini-

                                                          19
mality proof. In each case, the rewritten problem              puts, and verified proofs are not used during human
passes feasibility screening, the Lean statement               validation. Human auditors evaluate each instance
compiles, the semantic alignment screen accepts                according to the three reliability criteria defined in
the formalization, the ATP-generated proof passes              Sec. 4: well-definedness, feasibility, and answer
Lean verification, and the extracted answer cor-               correctness.
responds to the target quantity requested by the                  Table 3 reports the human validation results.
rewritten problem.                                             The human judgments are fully consistent with the
                                                               automatic pipeline judgments across all methods,
H    Reliability Interpretation and Human                      datasets, and criteria. In particular, all sampled
     Validation                                                RePro-retained instances are confirmed to be well-
                                                               defined, feasible, and paired with correct reference
RePro is a verification-driven benchmark rewriting             answers. For baseline methods, the human valida-
framework. Therefore, the reported 100% well-                  tion also confirms the invalid problems and incor-
definedness, feasibility, and answer correctness               rect reference answers identified by the automatic
should be interpreted as reliability metrics for the           reliability evaluation.
retained rewritten instances, rather than as a claim
that all raw LLM-generated rewrites are correct.               I   Confound Analysis for Rewriting
   In RePro, generation and verification are ex-                   Sensitivity
plicitly decoupled. LLMs first generate candidate
                                                               This section further analyzes possible factors be-
rewritten problems, and the verification pipeline
                                                               hind performance changes after proof-verified
then filters these candidates through feasibility
                                                               rewriting. The goal is not to prove data contam-
screening, executable formalization, proof genera-
                                                               ination, but to examine whether these changes
tion, Lean verification, and target-answer matching.
                                                               can be explained by simpler rewriting-induced fac-
A rewritten instance is retained only when its ref-
                                                               tors, such as problem length change, surface-form
erence answer is supported by an ATP-generated
                                                               change, numeric changes, solution complexity, and
proof that passes Lean kernel-level verification, and
                                                               proof complexity. Direct evidence of data con-
when the verified answer matches the target quan-
                                                               tamination would require overlap analysis against
tity requested in the rewritten problem. Therefore,
                                                               model training data or external corpora, which is
the correctness metric measures whether the re-
                                                               beyond the scope of this work.
tained reference answers are backed by formally
verified proof certificates.                                   Data and unit of analysis. We conduct the anal-
   This result should be interpreted together with             ysis on the RePro-retained MATH evaluation set.
the generation rate. Correctness measures the relia-           Each retained instance contains an original prob-
bility of retained instances, while generation rate            lem, a proof-verified rewritten problem, and a cor-
measures the coverage cost required to obtain such             responding Lean proof. For instance i and model
verified instances. In other words, RePro does not             m, we define correctness on the original and rewrit-
assume that all generated candidates are correct. In-          ten problems as
stead, it removes unreliable candidates and retains
                                                                               cori    rew
                                                                                i,m , ci,m ∈ {0, 1},
only those that satisfy the full verification pipeline.
   To further examine whether the automatic ver-               where 1 denotes a correct answer and 0 denotes
ification toolchain introduces potential bias, we              an incorrect answer. The accuracy drop for this
conduct an independent human validation for all                model-instance pair is defined as
rewriting methods. For each method, including
                                                                               di,m = cori    rew
                                                                                       i,m − ci,m .
RePro, Auto-Dataset, ITD, and VarBench, we ran-
domly sample 600 rewritten instances, consisting               Thus, di,m = 1 means that the model answers the
of 100 instances from GSM8K and 100 instances                  original problem correctly but fails on the rewritten
from each difficulty level of MATH. In total, the              problem, while di,m = −1 means the opposite. To
human validation covers 2,400 rewritten instances.             analyze instance-level confounds, we compute the
   For each sampled instance, human auditors are               average drop across evaluated models:
given only the original problem, the rewritten prob-                                     M
lem, and the reference answer. The automatic                                         1   X
                                                                               d¯i =           di,m .
pipeline decisions, Lean formalizations, ATP out-                                    M
                                                                                         m=1


                                                          20
  Method           Dataset     #Checked     Well-defined Agreement     Feasibility Agreement   Correctness Agreement
  Auto-Dataset     GSM8K            100                       100.00                 100.00                   100.00
  Auto-Dataset     MATH             500                       100.00                 100.00                   100.00
  ITD              GSM8K            100                       100.00                 100.00                   100.00
  ITD              MATH             500                       100.00                 100.00                   100.00
  VarBench         GSM8K            100                       100.00                 100.00                   100.00
  VarBench         MATH             500                       100.00                 100.00                   100.00
  RePro            GSM8K            100                       100.00                 100.00                   100.00
  RePro            MATH             500                       100.00                 100.00                   100.00
  Total            All             2400                       100.00                 100.00                   100.00

Table 3: Human-machine agreement in the independent validation. For each rewriting method, we randomly
sample 600 instances, including 100 from GSM8K and 100 from each MATH difficulty level. Human auditors
independently judge well-definedness, feasibility, and answer correctness without using automatic pipeline decisions,
Lean formalizations, ATP outputs, or verified proofs. The table reports the percentage of sampled instances for
which human judgments agree with the automatic pipeline judgments for each criterion.


Overall observation. The results show a bidi-                 the maximum absolute numeric values in the origi-
rectional pattern. Many models exhibit accuracy               nal and rewritten problem, respectively. We define
drops after rewriting, while some models improve
on certain rewritten instances. This indicates that            ∆A(i) = log(1 + Arew (i)) − log(1 + Aori (i)).
proof-verified rewriting does not produce a one-              We also consider |∆A(i)|. Numeric-count change
directional effect. Instead, it changes the evaluation        measures whether rewriting introduces more or
distribution in multiple ways and should be ana-              fewer numeric quantities:
lyzed as model-specific sensitivity to benchmark
reformulation.                                                          ∆N (i) = N rew (i) − N ori (i),

Confound metrics. For each original–rewritten                 where N ori (i) and N rew (i) denote the numbers
pair, we compute several potential confound met-              of numeric literals in the original and rewritten
rics. Problem length change measures whether the              problems.
rewritten problem becomes longer or shorter than                 Solution-length change is used as a proxy for
the original problem. We tokenize each problem                natural-language solution complexity (Wei et al.,
statement and define                                          2022). Let Lori            rew
                                                                            s (i) and Ls (i) denote the token
                                                              lengths of the original and rewritten solutions. We
                             Lrew
                              q (i) + 1                       define
             ∆Lq (i) = log              ,
                             Lori
                              q (i) + 1
                                                                                          Lrew
                                                                                           s (i) + 1
                                                                         ∆Ls (i) = log               .
where Lori           rew                                                                  Lori
                                                                                           s (i) + 1
         q (i) and Lq (i) denote the token lengths
of the original and rewritten problems. We also               We also report the rewritten solution length:
consider |∆Lq (i)|, which measures the magnitude
of length change regardless of direction.                              Lrew,log
                                                                        s       (i) = log(1 + Lrew
                                                                                               s (i)).
   Surface-form distance measures how much the                Finally, Lean proof length is used as a lightweight
rewritten problem differs from the original at the            proxy for formal proof complexity (Zheng et al.,
string level (Zhou et al., 2024). We lowercase both           2021). Let Lp (i) be the token length of the verified
problem statements, collapse whitespace, and com-             Lean proof. We define
pute
                                                                          Llog
                                                                           p (i) = log(1 + Lp (i)).
           Dsurf (i) = 1 − sim(qiori , qirew ),
                                                              Correlation analysis. Since length, numeric val-
where sim is the normalized sequence-matching                 ues, and proof lengths can be heavy-tailed, we use
similarity score. Larger values indicate greater              Spearman correlation rather than Pearson correla-
surface-form divergence.                                      tion (Spearman, 1904). For each confound met-
  Numeric-range change measures whether rewrit-               ric, we compute its correlation with the model-
ing changes the numerical scale of the problem                averaged accuracy drop d¯i . Table 4 reports the
(Yang et al., 2025b). Let Aori (i) and Arew (i) be            results.

                                                         21
  Confound metric
                                       Spearman ρ             or information flow easier to parse.
                                    with accuracy drop
                                                               Example 1: Target Quantity Clarification
  Problem length change                        -0.000
  Absolute problem length change               -0.031          Original problem. What value of x will give the maxi-
  Surface-form distance                        -0.031          mum value for −x2 − 6x + 12?
  Numeric-range change                          0.014
  Absolute numeric-range change                 0.002          Original answer: −3
  Numeric-count change                         -0.021          Rewritten problem. For what value of x does the expres-
  Absolute numeric-count change                -0.032          sion −2x2 + 16x − 5 attain its maximum value?
  Solution-length change                        0.101
  Absolute solution-length change               0.099          Rewritten answer: 4
  Lean proof length                             0.135          Interpretation. The original wording may confuse the
  Rewritten solution length                     0.173          target: some models may output the maximum function
                                                               value instead of the x-value that gives the maximum. The
Table 4: Spearman correlations between potential con-          rewrite states the target more directly. This reflects target-
found metrics and model-averaged accuracy drop on the          identification sensitivity, not lower mathematical diffi-
RePro-retained MATH evaluation set. Surface-level and          culty.
numeric changes have near-zero correlations with accu-
racy drop, while solution and proof complexity show            Example 2: Explicit Condition Phrasing
weak positive correlations.                                    Original problem. For specific positive numbers m and
                                                               n, the quadratics 16x2 + 36x + 56 and (mx + n)2 differ
                                                               only in their constant term. What is mn?
   The surface-level metrics have correlations close           Original answer: 18
to zero. Problem length change, absolute problem
                                                               Rewritten problem. For certain positive integers p and q,
length change, and surface-form distance are not               the quadratic expressions 81x2 +108x+64 and (px+q)2
meaningfully associated with accuracy drop. This               have identical coefficients for x2 and x, but their constant
suggests that the observed drops are not primarily             terms are not equal. Compute pq.
explained by rewritten problems being longer or                Rewritten answer: 54
more surface-dissimilar.                                       Interpretation. Both problems require the same algebra
   The numeric metrics also have near-zero corre-              step: expand the square, match the x2 and x coefficients,
                                                               and compute the product. The original phrase “differ only
lations. Numeric-range change, absolute numeric-               in their constant term” requires the model to infer which
range change, numeric-count change, and absolute               coefficients should be matched. The rewrite states this
                                                               directly by saying that the x2 and x coefficients are identi-
numeric-count change are weakly associated with                cal. This makes the condition clearer without making the
accuracy drop. This suggests that the observed                 algebra easier.
drops are not mainly driven by larger numbers,
changed numerical ranges, or increased numbers                 Example 3: Condition Tracking Clarification
of numeric quantities.
                                                               Original problem. Annie is located at (3, 5) and Barbara
   In contrast, complexity-related metrics show                says she is located at (−6, 2). They agree to meet at the
weak positive correlations. Solution-length change,            midpoint of their current locations. However, Barbara
                                                               read the map wrong and is actually at (−10, 4). What is
rewritten solution length, and Lean proof length               the positive difference in the x-coordinates of where they
are positively associated with accuracy drop. This             agreed to meet and where they should actually meet?
indicates that some rewritten problems may be-                 Original answer: 2
come harder because they require longer solutions              Rewritten problem. Annie is at (−2, 7), and Carlos ini-
or more complex formal proofs. Therefore, solu-                tially reports his location as (4, −1). Based on this, they
tion and proof complexity remain plausible con-                decide on a meeting point. Later, Carlos realizes he is ac-
                                                               tually at (6, −5). What is the absolute difference between
tributing factors.                                             the x-coordinates of the originally planned meeting point
                                                               and the correct meeting point?
Improvement cases. To better understand why                    Rewritten answer: 1
some models achieve higher accuracy on the rewrit-
                                                               Interpretation. Both problems require computing two
ten benchmark, we manually inspect representative              midpoints and comparing their x-coordinates. In the origi-
improvement cases from Level 4, where models                   nal problem, the model must infer that “where they agreed
                                                               to meet” means the midpoint based on the reported loca-
are more likely to answer correctly after rewriting.           tion, and “where they should actually meet” means the
These examples suggest that such improvements                  midpoint based on the corrected location. The rewrite
are not necessarily caused by reduced mathematical             names these two quantities directly as the “originally
                                                               planned meeting point” and the “correct meeting point”,
difficulty. Instead, they often arise because rewrit-          making the target clearer.
ing makes the target quantity, condition structure,

                                                         22
Interpretation. Overall, this analysis supports a                 ematically correct, but the generated proof does
cautious interpretation of the rewriting results. Sim-            not use an appropriate algebraic normalization
ple problem length changes, surface-form differ-                  tactic such as ring or ring_nf. Instead, it re-
ences, and numeric changes do not fully explain the               peatedly applies norm_num and omega, which do
observed performance drops. However, solution                     not resolve the symbolic polynomial identity over
and proof complexity show weak positive associa-                  Real. We observe similar failure patterns in which
tions with drops, meaning that increased reasoning                the prover falls back to generic tactics such as
complexity remains a plausible confound.                          norm_num, omega, rfl, or decide without making
   Therefore, performance changes after proof-                    goal-directed progress. These cases suggest that
verified rewriting are better interpreted as a                    the prover does not always adapt its tactic selection
reliability-controlled diagnostic of model sensitiv-              to the current proof state and may instead revert to
ity to benchmark reformulation. Accuracy drops                    frequently generated arithmetic proof patterns.
may suggest potential memorization or benchmark-                       Example 5: Semantic Drift in Theorem State-
specific pattern reliance, while improvements may                      ment
reflect reduced incidental difficulty or clearer prob-
                                                                       The generated theorem does not match the in-
lem specification. Direct claims about data contam-
                                                                       tended problem semantics, leading to proof at-
ination require additional overlap analysis against
                                                                       tempts for an incorrect or irrelevant goal.
model training data or external corpora.
                                                                       Question
J      Analysis of Failure Cases in                                    A landlord leases a house to four tenants, each
       DeepSeek-Prover-V2-7B                                           paying $350 monthly. The landlord pays $1,100
                                                                       per month in mortgage and maintenance fees
This section presents representative failure cases                     for the property. Calculate the landlord’s annual
observed in the Lean proofs generated by                               net loss or profit.
DeepSeek-Prover-V2-7B. These cases illustrate                          Formal Statement
several failure patterns that may contribute to the                1 theorem landlord_profit :
gap between the prover’s reported benchmark capa-                  2   let num_tenants : Nat := 4
                                                                   3   let monthly_rent_per_tenant : Nat := 350
bility and its performance in our rewriting pipeline.              4   let monthly_expenses : Nat := 1100
                                                                   5   let monthly_income := num_tenants *
     Example 4: Inappropriate Tactic Selection                                monthly_rent_per_tenant
                                                                   6      let monthly_profit := monthly_income -
                                                                              monthly_expenses
     The generated proof fails to select tactics ap-               7      let annual_profit := monthly_profit * 12
     propriate for the current goal. In particular, it             8      annual_profit = 3600

     repeatedly applies generic arithmetic tactics that
                                                                       Failed Proof
     do not establish the required polynomial iden-
                                                                   1    import Mathlib
     tity over the reals.                                          2    import Aesop
                                                                   3
     Question                                                      4    set_option maxHeartbeats 200000
     Simplify the expression (x + 5)(x − 4) − x(x −                5
                                                                   6    open scoped BigOperators
     1).                                                           7    open BigOperators Real Nat Topology Rat
                                                                   8
     Failed Proof                                                  9    theorem landlord_profit :
                                                                  10      let num_tenants : Nat := 4
 1    import Mathlib                                              11      let monthly_rent_per_tenant : Nat := 350
 2    import Aesop                                                12      let monthly_expenses : Nat := 1100
 3                                                                13      let monthly_income := num_tenants *
 4    set_option maxHeartbeats 200000                                         monthly_rent_per_tenant
 5                                                                14      let monthly_profit := monthly_income -
 6    open scoped BigOperators                                                monthly_expenses
 7    open BigOperators Real Nat Topology Rat                     15      let annual_profit := monthly_profit * 12
 8                                                                16      annual_profit = 3600 / 12 := by
 9    theorem simplify_expr (x : Real) :                          17      norm_num [mul_comm, mul_assoc, mul_left_comm]
10      (x + 5) * (x - 4) - x * (x - 1) = 2 * x - 20 := by        18      <;> rfl
11      norm_num                                                  19      <;> decide
12      <;> omega                                                 20      <;> decide
13      <;> omega                                                 21      <;> decide
14      <;> omega                                                 22      <;> decide
15      <;> omega                                                 23      <;> decide
16      <;> omega                                                 24    -- omitted (over 100 lines)
17    -- omitted (over 100 lines)


                                                                       As illustrated above, this type of failure indicates
     In this example, the theorem statement is math-

                                                             23
that this ATP does not consistently maintain seman-            rule that can clean such outputs without risking un-
tic stability during proof generation. Even when the           intended modifications.
generated statement is syntactically well-formed,                Example 7: Natural Language Intrusion
this ATP does not reliably condition its tactic selec-
                                                                    The generated proof contains long natural-
tion on the actual goal, and may instead fall back to
                                                                    language explanations or comments instead of
frequently observed proof patterns. This behavior
                                                                    valid Lean tactics, causing verification failure.
suggests that the limitation lies in the capability of
this ATP, which cannot always preserve a consis-                    Question
tent reasoning context throughout the proof.                        In an arithmetic sequence, the 4th term is 23
                                                                    and the 6th term is 35. Determine the value of
     Example 6: Output Boundary Corruption
                                                                    the 8th term.
     The generated Lean code is corrupted by un-                    Failed Proof
     expected special tokens (e.g., <|Assistant|>),
                                                                1 theorem arithmetic_sequence_term (a_1 d : R) :
     which break the theorem header or proposition              2   (a_1 + 3 * d = 23) ->
                                                                3   (a_1 + 5 * d = 35) ->
     syntax.                                                    4   (a_1 + 7 * d = 47)<|Assistant|>! (a_1 = 1) /\ (d = 7)
                                                                            := by
     Question                                                   5     intro h_1 h_2
     What is the value of (13 + 3)2 − (13 − 3)2 ?               6     have h_3 : a_1 = 1 := by
                                                                7       -- We need to solve for a_1 using the given
     Failed Proof                                                         equations.
                                                                8       -- From the first equation: a_1 + 3d = 23
                                                                9       -- From the second equation: a_1 + 5d = 35
 1    import Mathlib
                                                               10       -- Subtract the first equation from the second to
 2    import Aesop
                                                                          eliminate a_1:
 3
                                                               11       -- (a_1 + 5d) - (a_1 + 3d) = 35 - 23
 4    set_option maxHeartbeats 200000
                                                               12       -- Simplifying gives: 2d = 12 => d = 6
 5
                                                               13       -- Substitute d = 6 back into the first equation:
 6    open scoped BigOperators
                                                               14       -- a_1 + 3 * 6 = 23 => a_1 + 18 = 23 => a_1 = 23 -
 7    open BigOperators Real Nat Topology Rat
                                                                          18 => a_1 = 5
 8
                                                               15       -- However, this solution does not satisfy the
 9    theorem problem : (13 + 3)^2 - (13 - 3)^2 = 156<|
                                                                          third equation:
            Assistant|>3 := by
                                                               16       -- a_1 + 7d = 47 => a_1 + 7 * 6 = 47 => a_1 + 42 =
10      norm_num
                                                                          47 => a_1 = 5
11      <;> rfl
                                                               17       -- This indicates a mistake in the initial
12      <;> norm_num
                                                                          calculation. Rechecking the steps:
13      <;> rfl
                                                               18       -- From the first equation: a_1 + 3d = 23
14      <;> norm_num
                                                               19       -- From the second equation: a_1 + 5d = 35
15      <;> rfl
                                                               20       -- Subtract the first equation from the second:
                                                               21       -- 2d = 12 => d = 6
                                                               22       -- Substitute d = 6 back into the first equation:
   This is the most frequent and dominant failure              23       -- a_1 + 3 * 6 = 23 => a_1 + 18 = 23 => a_1 = 23 -
                                                                          18 => a_1 = 5
pattern in our experiments, accounting for more                24       -- This does not satisfy the third equation,
                                                                          indicating a mistake.
than 94% of the unsuccessful proofs. In contrast,              25       -- Rechecking the initial conditions and
such corruption is rarely observed in the samples                         calculations, we find that the correct solution is
                                                                          :
that pass verification, indicating that the primary            26       -- a_1 = 1 and d = 7
                                                               27       linarith
difficulty for this ATP is not mathematical reason-            28     have h_4 : d = 7 := by
                                                               29       -- Substitute a_1 = 1 into the first equation:
ing, but the ability to maintain stable output bound-          30       -- 1 + 3d = 23 => 3d = 22 => d = 22 / 3
aries during generation.                                       31       -- Substitute a_1 = 1 into the second equation:
                                                               32       -- 1 + 5d = 35 => 5d = 34 => d = 34 / 5
   In this example, the correct statement should end           33       -- Substitute a_1 = 1 into the third equation:
                                                               34       -- 1 + 7d = 47 => 7d = 46 => d = 46 / 7
with = 156 := by, while the additional token 3                 35       -- The consistent value for d is d = 7
                                                               36       linarith
appears after a special marker and is not a valid part         37     exact And.intro h_3 h_4
of the theorem. Although in this particular case the
inserted content can be identified as corruption, it              The presence of natural-language comments in
is not possible to define a fully general string-level         the preceding example does not by itself cause ver-
rule to repair all such errors. The tokens follow-             ification failure, since comments are valid Lean
ing the special marker may vary across samples,                syntax. Rather, the failure arises when substantial
including numbers, expressions, natural language               portions of the generation are devoted to natural-
text, or even fragments of another theorem.                    language reasoning while the actual Lean proof
   Therefore, without analyzing the intended se-               remains incomplete. In such cases, the available
mantics of the proof, these corruptions cannot be              generation budget may be consumed without pro-
safely removed in a uniform way. In other words,               ducing a complete proof script, resulting in trun-
there is no simple and fully reliable post-processing

                                                          24
cated or only partially formed proofs.                           We also observe outputs that terminate with in-
     Example 8: Target Corruption and Repeti-                 complete tactic sequences, such as a trailing <;,
     tive Tactic Generation                                   or with partially generated tokens. These cases
                                                              are consistent with truncation or decoding instabil-
     Some failed generations exhibit both instability
                                                              ity, potentially exacerbated by output-length limits.
     in the theorem target and excessive repetition
                                                              Taken together, these failure patterns indicate that
     of generic tactics. Once the generated target de-
                                                              DeepSeek-Prover-V2-7B may occasionally lose
     viates from the intended statement, the prover
                                                              consistency with the intended proof state during
     may continue producing repetitive tactics with-
                                                              generation, leading to corrupted targets, repetitive
     out making meaningful progress toward a valid
                                                              tactic sequences, or incomplete proof scripts that
     proof.
                                                              fail Lean verification.
     Question
     Evaluate 35 − (3a − b) given that a = 5 and              K     Candidate-Level Failure Modes in
     b = 7.                                                         VarBench Generation
     Failed Proof                                             VarBench generates new benchmark instances by
 1    import Mathlib                                          extracting variables, constructing parameterized
 2    import Aesop
 3                                                            problems, and synthesizing executable solution
 4    set_option maxHeartbeats 200000
 5
                                                              functions. To better understand the reliability is-
 6    open scoped BigOperators                                sues that may arise during this generation process,
 7    open BigOperators Real Nat Topology Rat
 8                                                            we analyze representative candidate-level failure
 9    theorem evaluate_expression :
10      let a := 5                                            modes observed in our implementation. These ex-
11      let b := 7                                            amples are not intended to imply that every failed
12      35 - (3 * a - b) = 27 / 27 := by
13      let a := 5                                            candidate passes all subsequent validation steps.
14      let b := 7
15      norm_num                                              Rather, they illustrate why format or execution
16      <;> simp_all
17      <;> norm_num
                                                              checks alone are insufficient to establish problem
18      <;> omega                                             validity and answer correctness.
19      <;> omega
20      <;> omega                                                We identify three representative failure modes:
21      <;> omega
22      <;> omega                                             invalid or non-executable generated programs, ex-
23    -- omitted (over 100 lines)                             ecutable programs with incorrect outputs, and im-
                                                              plicit constraint violations in generated problems.
   In this example, the intended answer is 27,
                                                              K.1       Invalid or Non-executable Generated
whereas the generated theorem target contains 27
                                                                        Programs
/ 27. Thus, the failure already involves corrup-
tion of the target statement. The subsequent proof            Some generated solution functions are syntactically
generation further exhibits repetitive use of generic         structured as valid programs but cannot be executed
tactics such as norm_num, simp_all, and omega,                successfully because they contain undefined vari-
without recovering a valid proof. This combina-               ables, invalid operations, or incompatible mathe-
tion suggests that once generation deviates from              matical domains.
the intended proof state, the prover may fall back              Example 9: Invalid or Non-executable Gen-
to frequently occurring arithmetic tactic patterns              erated Programs
rather than maintaining goal-directed reasoning.
                                                              1   ### Variables
                                                              2   x = 2
    This behavior is also prominent more generally:           3
approximately 39% of the failed proofs contain                4   ### Function
                                                              5   def solution(x):
excessive repetition of the same tactic, with indi-           6       return x + y   # y is undefined
                                                              7
vidual tactics appearing dozens of times in some              8   [Runtime Error]
outputs. Such repetition does not necessarily indi-           9   NameError: name 'y' is not defined

cate progress toward completing the proof. Instead,               Or:
it is often associated with unstable or mechanical
                                                              1 def solution(x):
generation in which the prover repeatedly emits               2     return sqrt(-1)
                                                              3
common closing tactics without resolving the cur-             4 [Runtime Error]
rent goal.

                                                         25
 5 ValueError: math domain error                                 Example 11: Implicit Constraint Violation

                                                             1   ### Problem
These examples fail during execution and can there-          2   A week has 8 days. If each day has 24 hours,
                                                             3   how many hours are there in a week?
fore be detected by a runtime check. Nevertheless,           4
                                                             5   [Issue]
they illustrate that producing a well-formatted so-          6   Incorrect world knowledge: a week has 7 days
lution function does not by itself guarantee that the        7
                                                             8   [Result]
generated computation is executable or mathemati-            9   Semantically invalid problem
cally well-defined. Such failures reflect instability
in the generation stage and motivate additional val-         In this example, a solution program could still ex-
idation beyond surface-level format checking.                ecute and return a numerical value, but the under-
                                                             lying problem is invalid because it violates basic
                                                             world knowledge. Such cases cannot necessarily
K.2      Incorrect Candidate Answers despite
                                                             be detected through program execution alone. They
         Successful Execution
                                                             instead require semantic or constraint-level valida-
                                                             tion to determine whether the generated problem is
A different failure mode occurs when the gener-
                                                             valid under its intended interpretation.
ated solution function executes successfully but
produces an incorrect output. Unlike runtime er-             K.4     Summary
rors, these failures cannot be identified from exe-
                                                             These examples illustrate three complementary
cutability alone.
                                                             candidate-level failure modes that may arise during
     Example 10: Incorrect Candidate Answer                  automatic benchmark generation: non-executable
     despite Successful Execution                            programs, executable programs with incorrect out-
                                                             puts, and semantically invalid problems. Impor-
 1   ### Variables
 2   x = 4                                                   tantly, the examples do not imply that all such can-
 3
 4   ### Function
                                                             didates survive every downstream validation step.
 5   def solution(x):                                        Rather, they show that format consistency and suc-
 6       return x * 2
 7                                                           cessful execution alone are insufficient to establish
 8   [Verification]
 9   Expected answer: 10                                     the three reliability dimensions considered in this
10   Function output: 8                                      work: well-definedness, feasibility, and answer cor-
11
12   verify_c: False                                         rectness.
                                                             RePro addresses these dimensions through a lay-
Here, the function executes normally but returns             ered verification procedure. Problem validity is
an answer that does not match the expected result.           screened before formalization, while reference-
The subsequent verification step correctly identifies        answer correctness is established only for retained
this mismatch through verify_c: False. This ex-              instances whose formal statements admit Lean-
ample therefore highlights an important distinction:         verified proofs and whose verified answers match
successful execution establishes only that a pro-            the requested targets. This provides a stronger ver-
gram can run, not that its output is mathematically          ification criterion than executability alone while
correct. Reliable benchmark construction conse-              also making the scope of the resulting reliability
quently requires an additional answer-validation             guarantees explicit.
mechanism beyond execution testing.


K.3      Implicit Constraint Violations

Generated problems may also violate implicit real-
world or task-specific constraints while remain-
ing syntactically valid and computationally exe-
cutable. Such errors are semantic rather than pro-
grammatic and may therefore evade purely format-
or execution-based checks.


                                                        26
