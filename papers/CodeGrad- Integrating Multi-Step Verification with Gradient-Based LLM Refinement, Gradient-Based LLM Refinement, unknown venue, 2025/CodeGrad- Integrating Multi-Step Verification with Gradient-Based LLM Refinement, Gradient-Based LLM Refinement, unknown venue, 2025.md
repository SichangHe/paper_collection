                                         CodeGrad: Integrating Multi-Step Verification with
                                                Gradient-Based LLM Refinement
                                                   Yueke Zhang                       Yifan Zhang                      Kevin Leach                      Yu Huang
                                              Vanderbilt University              Vanderbilt University            Vanderbilt University           Vanderbilt University
                                           yueke.zhang@vanderbilt.edu        yifan.zhang@vanderbilt.edu        kevin.leach@vanderbilt.edu       yu.huang@vanderbilt.edu



                                           Abstract—While Large Language Models (LLMs) have demon-           challenge, therefore, is to develop a principled framework that
                                        strated remarkable capabilities in code generation, they often       synergistically combines the generative power of LLMs with
                                        produce solutions that lack guarantees of correctness, robustness,   the verifiable guarantees of formal methods [19]. Encourag-
                                        and efficiency. This limitation is particularly acute in domains
arXiv:2508.10059v2 [cs.SE] 2 Sep 2025




                                        requiring strict constraints. CodeGrad introduces a principled       ingly, recent studies have demonstrated the potential of using
                                        framework that integrates rigorous verification techniques di-       natural language as a proxy for formal reasoning to guide and
                                        rectly into an iterative LLM-based generation loop. It uniquely      constrain LLM behavior, suggesting a viable path toward this
                                        treats code as a differentiable variable, converting structured      integration [20]–[24].
                                        feedback and mathematical constraints into a textual pseudo-            In this work, we introduce CodeGrad, a novel framework
                                        gradient. This gradient guides the model to iteratively refine
                                        solutions, ensuring they are not only functional but also robust     integrating formal methods into an iterative, LLM-driven
                                        and mathematically justified.                                        generation pipeline. As illustrated in Figure 1, our approach
                                           We evaluate CodeGrad on the HumanEval, HumanEval+, and            treats code as a differentiable variable. This allows us to iter-
                                        LiveCodeBench benchmarks. Our implementation outperforms             atively refine code by generating a textual pseudo-gradient—a
                                        strong baselines, achieving an absolute improvement of up            structured set of corrections—derived from rigorous formal
                                        to 27% on HumanEval and a 41% relative improvement on
                                        the challenging LiveCodeBench V6. StructuredGrad generates           analysis. Rather than a numeric vector, this gradient consists
                                        mathematically justified code that is robust and efficient, paving   of specific, textual edits that steer the code toward an optimal
                                        the way for reliable AI-assisted software development in high-       state. At each iteration, a backward engine, acting as a formal
                                        stakes applications.                                                 critic, evaluates the code against specifications for correctness,
                                           Index Terms—Large Language Model, Software Engineering            efficiency, and constraint compliance. The resulting critique
                                                                                                             is converted into the textual pseudo-gradient, which guides a
                                                              I. I NTRODUCTION                               forward engine to produce an improved candidate. To ensure
                                           Automated code generation is a transformative technology          rigor, a formal methods optimizer augments the update, en-
                                        in software engineering and AI, accelerating development,            forcing explicit invariants. Crucially, it requires each revision
                                        reducing human error, and making programming more acces-             to have a natural language “proof” of its correctness. This
                                        sible [1]–[3]. Large Language Models (LLMs) have demon-              verification ensures solutions are not merely functional but
                                        strated remarkable capabilities in generating code from natural      robust and formally justified, guiding the process toward
                                        language descriptions, solving competitive programming prob-         verifiably correct code. The contributions of this paper are:
                                        lems, and even synthesizing complex algorithms [4]–[6].                 1) We present CodeGrad, the first framework to integrate
                                           Early explorations in LLM-based code synthesis centered on               formal methods to guide an LLM-based code generation
                                        one-shot or few-shot generation [7]–[9], the recent research                loop using textual pseudo-gradients for iterative refine-
                                        has shifted to augmentation with feedback mechanisms like                   ment.
                                        test-driven development and RLHF [10], [11]. Despite these              2) We conduct extensive evaluations on the HumanEval,
                                        methods can produce syntactically correct and functional code,              HumanEval+, and LiveCodeBench benchmarks. Our re-
                                        the resulting code, while often functional, frequently struggles            sults demonstrate the framework’s effectiveness, achiev-
                                        with edge cases, fails to generalize beyond seen examples,                  ing performance increase of up to 27.2% on HumanEval
                                        and lacks mechanisms for systematic improvement [3], [5],                   and a improvement of 40.6% on the lastest Live-
                                        [6], [12]–[14].                                                             CodeBench V6 benchmark over baselines.
                                           Conversely, traditional formal methods in software engineer-         3) We analyze the framework’s performance across vari-
                                        ing provide mathematical rigor and verifiable guarantees of                 ous problem categories and difficulty levels, revealing
                                        correctness. However, their application is often hindered by                its particular efficacy in complex algorithmic domains
                                        their rigidity, the need for specialized expertise, and their poor          where baseline models completely fail.
                                        scalability, particularly for the open-ended, natural-language
                                        tasks where LLMs excel [15], [16]. This fundamental tension                               II. R ELATED W ORK
                                        between the flexibility of LLMs and the rigor of formal                Research into improving the reliability of LLM-generated
                                        methods creates a distinct research gap [17], [18]. The central      code has evolved from enhancing intrinsic reasoning to em-
Fig. 1. Overview of the Formal-Gradient Code Generation loop on the “maximum-subarray” task. First, the forward model proposes an O(n3 ) triple-loop
solution. The backward model then acts as a formal critic, analyzing the code to identify flaws—in this case, computational inefficiency and a failure to handle
the all-negative numbers edge case. This structured critique is converted into a textual pseudo-gradient that directs refinement. Guided by this gradient and a
formal efficiency invariant, the optimizer produces a new, correct, and highly efficient O(n) solution. The loop terminates under one of two conditions: either
the generated code is accepted upon successful formal verification of its accompanying proof, or the maximum number of iterations is reached.

ploying sophisticated, external feedback loops [25], [26]. Early                 Formally, given a natural language task description T , our
efforts focused on improving the step-by-step reasoning of                       objective is to discover a program P from the space of
models, but recent progress has been made with iterative                         all possible Python programs S that satisfies two primary
refinement [27], [28]. Reflexion established a paradigm where                    conditions.
an agent critiques its own output to guide subsequent im-                           First, the program must be functionally correct. This means
provements [29]. In the code generation domain, this principle                   that for every valid input x from the domain of possible inputs
was adapted into test-driven methods where feedback was                          D, the output of the generated program P (x) must match
derived from unit test outcomes, as seen in CODET and                            the output of the ideal target function fT (x) induced by the
CODERL [30], [31]. More recently, this feedback mechanism                        description T . This can be expressed as:
has been formalized through novel approaches like TextGrad,
which conceptualizes natural language critiques as pseudo-                                               ∀x ∈ D : P (x) = fT (x),                           (1)
gradients [32]. Textgrad use the model toward a correct
                                                                                 where fT is the unknown ground-truth function.
solution by treating textual corrections as differentiable signals
                                                                                    Second, the program must satisfy a set of formal invariants,
within the discrete space of code. Our work builds upon
                                                                                 which represent non-negotiable properties required for the so-
this trajectory, integrating gradient-style feedback with formal
                                                                                 lution to be considered valid. These invariants, denoted as a set
methods.
                                                                                 I = {I1 , . . . , Ik }, can cover requirements such as I/O format,
   While TextGrad formalizes the general feedback mecha-
                                                                                 edge-case handling (Completeness), time/space complexity
nism, a parallel line of research has explored integrating prin-
                                                                                 (Efficiency), and Python syntax validity (Correctness).
ciples from formal methods to better constrain LLM behavior.
A key challenge is the difficulty and low accuracy of having                     B. Formal-Gradient Code Generation (FGCG) Pipeline
LLMs generate code in a strict formal language [20]. Conse-
quently, recent work has focused on using natural language                          Conventional optimization uses a numerical gradient ∂L/∂θ
as a medium for formal reasoning. For instance, Formal-LLM                       to steer parameters θ toward lower loss L. In code generation
has been shown to successfully guide the planning process for                    the surface is discrete, so we approximate this signal with a
agents by preventing the generation of invalid or unsuccessful                   pseudo–gradient g (t) obtained by mapping reviewer feedback
plans [33]. Other approaches have used formal methods to                         to an ordered list of required edits follow the previous in
facilitate the self-monitoring of LLM responses or leveraged                     Textgrad [32]:
LLMs to formulate planning tasks as solvable optimization
                                                                                        g (t) = Parse F (t) −→ {(location, action)}j . (2)
                                                                                                            
problems [23], [25].
                                                                                 Each tuple pinpoints a fragment of P (t) together with the
                         III. M ETHODOLOGY
                                                                                 type of modification (e.g., “replace O(n3 ) loop with linear
A. Problem Definition                                                            scan”). Although expressed in natural language, g (t) functions
  We define our problem as automatically generate a computer                     exactly like a real gradient: following its direction increases the
program that not only fulfills a natural language specification                  likelihood that the next candidate will satisfy the loss template
but also adheres to a set of predefined formal constraints.                      defined below. As figure 1, at each iteration t ∈ {0, . . . , N }
the system maintains a differentiable text variable P (t) and            • HumanEval (HE) [38] is a canonical benchmark for
executes the following four phases:                                        functional correctness, comprising 164 human-authored
  1) Forward Generation (LMfwd ). We prompt a code-                        Python problems with rigorous unit tests. We also use
      centric LLM LMfwd to produce an initial or revised                   its extension, HumanEval+ (HE+) [6], which provides
      program                                                              a more comprehensive test suite to better assess solution
                                                                           robustness.
               P (t) = LMfwd T , P (t−1) , ∇P (t−1) ,
                                                   
                                                                         • LiveCodeBench (LCB V6) [39] is a continuously up-

     where ∇P (t−1) —if available—is textual gradient feed-                dated benchmark for competitive programming, including
     back from the previous step. Conditioned on the task                  problems sourced from active platforms like LeetCode,
     description T and gradient hints from the previous                    AtCoder, and Codeforces. We use V6 in its release
     round, the model emits a candidate implementation P (t) .             version, which include 175 questions from Jan 2025 to
     Intuitively, this component plays the role of a software              May 2025.
     engineer drafting a solution while being aware of earlier                                 IV. R ESULT
     review comments.
  2) Backward Evaluation (LMbwd ). A backward model                                                TABLE I
     reviews the draft. It returns structured textual feedback          PASS @1 PERFORMANCE ACROSS BENCHMARKS . T HE ‘+C ODE ‘ SUFFIX
               (t)     (t)  (t)    (t)                                  INDICATES CODE - ENABLED BACKWARD MODELS . P ERCENTAGES SHOW
     F (t) =[Fcorr , Fio , Feff , Fcomp ], where each element anal-
                                                                             INCREASE OVER THE N ULL BACKWARD MODEL BASELINE .
     yses the program along a specific axis: Correctness
     (corr), Input-Output format (io), Efficiency (eff), and                                   Qwen3-1.7B            GPT4.1-mini
                                                                       Benchmark    Null
     Completeness (comp).                                                                    Base      +Code       Base       +Code
  3) Gradient Propagation. This step converts every com-
                                                                       HE          0.695 0.787↑13% 0.787↑13% 0.811↑17% 0.884↑27%
     ment, suggestion, or error report into a gradient sig-            HE+         0.671 0.713↑6% 0.726↑8% 0.756↑13% 0.817↑22%
     nal ∇P (t) that highlights where and how the code should          LCB V6      0.143 0.166↑16% 0.160↑12% 0.251↑76% 0.201↑41%
     change.
  4) Formal Optimization. We search for an updated pro-                A. RQ1: To what extent does the CodeGrad framework im-
     gram P (t+1) that (i) descends along ∇P (t) and (ii) is           prove code generation performance?
     accompanied by a proof Π(t+1) that each invariant holds:             We first establish a baseline using a forward-only config-
                                                                       uration with the Qwen2.5Coder-3B model and no backward
                 Π(t+1) = LMfwd P (t) , ∇P (t) , I .
                                                       
                                                                (3)    optimization loop (the ”Null” model in Table I). This baseline
     The update is accepted if V ERIFY P (t+1) , Π(t+1) , I =
                                                                      achieves a pass@1 score of 69.5% on HumanEval, 67.1%
     true, else it is discarded. The loop terminates when              on HumanEval+, and 14.3% on the more challenging Live-
                                               (t)
     LMbwd detects no violations (∀i : Fi = “pass”) or after           CodeBench V6. All subsequent results are evaluated relative to
     N iterations. Formally, each iteration seeks a program            this starting point. Introducing the CodeGrad framework yields
     P (t+1) solving the constrained optimization                      substantial improvements. Augmenting the forward model
                                                                       with a lightweight backward model (Qwen3-1.7B) boosts
                                         k
                                        ^                             performance by up to 16% on LiveCodeBench. Employing
          min L P ; T       subject to         Ii (P ) = true,   (4)   a more powerful, albeit code-blind, reviewer (GPT4.1-mini)
         P ∈S
                                         i=1
                                                                       further elevates the scores, with a 17% absolute increase on
     where L is an implicit loss computed by the back-                 HumanEval and a 76% relative increase on LiveCodeBench.
     ward LLM. CodeGrad approximates the solution by                   These collective gains confirm that the CodeGrad framework
     alternating gradient proposals (soft updates) and formal          is an effective mechanism for generating code solutions that
     verification (hard constraints), akin to projected gradient       are more correct and robust.
     descent in continuous optimization.
                                                                       B. RQ2: What is the impact of enabling dynamic code execu-
C. Experimental Setup                                                  tion within the backward model?
   To evaluate the effectiveness of CodeGrad, we estab-                   Our approach builds upon the established principle of using
lish a comprehensive experimental setup. We employ Qwen                partial execution for self-debugging, as demonstrated in prior
2.5Coder-3B as our Forward Model [34]. For the Back-                   work [30], [31], which demonstrates that even minimal, sand-
ward Model, we evaluate two distinct models to analyze                 boxed probes substantially enhance reviewer effectiveness.
the impact of critic capability: the lightweight, open-source          This research question examines the performance difference
Qwen3-1.7B [35] and the more powerful, proprietary GPT4.1-             when the backward model is granted the ability to execute
mini [36]. All open-source models were deployed using the              code probes. We compare pairs of architecturally identical re-
vLLM inference engine on an NVIDIA A6000 GPU [37]. For                 viewers—with and without the sandboxed execution capability
all experiments, we fixed the number of max refinement iter-           (denoted by the +Code suffix in Table II while holding the
ations at two. We assess performance on two complementary              forward model constant). The results presented in Table II
benchmarks:                                                            reveal that the benefit of code execution is highly contingent
                                                             TABLE II
                     PASS @1 BY A LGORITHMIC C ATEGORY, FOR F ORWARD M ODEL WITH DIFFERENT BACKWARD MODEL .

          Model                      Array     DP     Graph Greedy Hash Map           Math      Simulation      String
          Null                       0.412    0.000   0.000    0.000     0.231        0.119        0.071        0.333
                           Base  0.471↑14% 0.083      0.062    0.154   0.385↑67% 0.262↑120% 0.179↑152% 0.444↑33%
          GPT4.1-mini
                           +Code    0.412  0.083      0.062    0.154   0.385↑67% 0.167↑40% 0.143↑101% 0.444↑33%
                           Base  0.353↓14% 0.000      0.062    0.000   0.308↑33%    0.214↑80%    0.107↑51% 0.278↓17%
          Qwen3-1.7B
                           +Code 0.294↓29% 0.000      0.125    0.000   0.154↓33%    0.167↑40%   0.143↑101%    0.333

                            TABLE III                              fails to produce a single correct solution (0.0% pass@1).
PASS @1 BY D IFFICULTY L EVEL FOR F ORWARD MODEL WITH DIFFERENT    In contrast, the full CodeGrad approach successfully solves
                        BACKWARD MODEL
                                                                   problems in these areas, demonstrating its ability to navigate
                        Qwen3-1.7B             GPT4.1-mini         complex logic and constraints. The largest relative gains are
 Difficulty Null
                    Base        +Code        Base      +Code
                                                                   observed in Simulation (+101%), Math (+40%), and Hash
                                                                   map (+66%), where iterative refinement and formal checks
 Easy      0.558    0.558      0.558    0.791↑42% 0.628↑13%
 Medium    0.019 0.077↑305% 0.058↑205% 0.115↑505% 0.135↑611%       are critical for correctness.
 Hard      0.000    0.013      0.013       0.050     0.025            The analysis by difficulty level in Table III reinforces this
                                                                   finding. While CodeGrad offers a respectable 12.5% improve-
                                                                   ment on ”Easy” problems, its impact is transformative for
on the capability of the backward model and the nature of the      more challenging tasks. It boosts performance on ”Medium”
evaluation benchmark. For the more powerful GPT4.1-mini            difficulty problems by over 610% relative to the baseline and
reviewer, enabling execution on the HumanEval benchmarks           successfully generates correct solutions for ”Hard” problems
yields improvements. The pass@1 score on HumanEval rises           where the baseline fails completely.
from 0.811 to 0.884, a gain of 7.3 percentage points, and on
HumanEval+, it increases from 0.756 to 0.817. This demon-                        V. I MPLICATION AND F UTURE W ORK
strates that a sophisticated reviewer can effectively leverage
                                                                      While our results demonstrate the effectiveness of the
execution to identify and correct flaws in standard, function-
                                                                   CodeGrad framework, there are several directions for future
based programming tasks. The effect is less pronounced for
                                                                   exploration. First, we will enhance the efficiency of the itera-
the smaller Qwen3-1.7B model, which sees a modest 1.3%
                                                                   tive refinement process. We plan to replace the current fixed-
gain on HumanEval+ and no change on the base HumanEval
                                                                   iteration method with a dynamic, search-based approach that
benchmark.
                                                                   identifies the most cost-effective path to an optimal solution.
   Conversely, the data from Table I shows a performance
                                                                   Second, we aim to translate our research prototype into a
degradation on LiveCodeBench V6 when execution is enabled.
                                                                   practical, developer-centric tool. This involves designing a
The GPT4.1-mini (Code) configuration scores 5.0% lower than
                                                                   robust framework that enables software engineers to directly
its non-executing counterpart, and the Qwen3-1.7B (Code)
                                                                   apply CodeGrad to their own development workflows, poten-
model shows a slight decrease of 0.6%. This reversal high-
                                                                   tially as an integrated development environment (IDE) plugin
lights a key challenge. LiveCodeBench problems involve com-
                                                                   or a standalone library. Finally, we will explore extending
plex constraints, such as communication via stdin/stdout and
                                                                   the core principles of CodeGrad beyond code generation.
strict efficiency requirements, which are difficult to replicate
                                                                   The concept of using formal feedback as a textual pseudo-
faithfully with isolated code snippets. While execution probes
                                                                   gradient is highly generalizable. We plan to investigate its
can catch simple runtime errors, they may generate misleading
                                                                   application in related domains such as automated program
pseudo-gradients in this context.
                                                                   repair, where formal invariants could guide the fixing of bugs,
C. RQ3: How does the performance of CodeGrad vary across           and interactive proof generation, where the framework could
different problem categories and difficulty levels?                help refine mathematical or logical arguments expressed in
                                                                   natural language.
   To understand the conditions under which CodeGrad is most
beneficial, we analyze its performance on problems grouped
                                                                                         VI. C ONCLUSION
by algorithmic category (Table II) and difficulty (Table III).
We analyze the problems from the LiveCodeBench dataset                This work introduced CodeGrad, a framework that success-
along two dimensions: their predefined difficulty level and        fully integrates gradient-based iterative refinement with for-
their algorithmic category, which we assign based on the           mal verification for LLM-based code generation. Our results
classification from LeetCode [40]. The breakdown by category       demonstrate that this hybrid approach enhances performance,
reveals that the framework’s advantages are most pronounced        achieving substantial gains on challenging benchmarks like
in complex algorithmic domains. For categories like Dynamic        LiveCodeBench. The framework proves particularly effective
Programming (DP), Graph, and Greedy, the baseline model            for complex problems requiring deep reasoning and strict
constraint adherence, demonstrating a viable path toward gen-                     [20] J. Cao, Y. Lu, M. Li, H. Ma, H. Li, M. He, C. Wen, L. Sun, H. Zhang,
erating more reliable, robust, and formally justified AI-assisted                      S. Qin et al., “From informal to formal–incorporating and evaluating
                                                                                       llms on natural language requirements to verifiable formal proofs,” arXiv
software for high-stakes applications.                                                 preprint arXiv:2501.16207, 2025.
                                                                                  [21] A. Ospanov, F. Farnia, and R. Yousefzadeh, “Apollo: Automated llm
                              R EFERENCES                                              and lean collaboration for advanced formal reasoning,” arXiv preprint
                                                                                       arXiv:2505.05758, 2025.
 [1] A. Svyatkovskiy, S. K. Deng, S. Fu, and N. Sundaresan, “Intellicode          [22] M. Hassan, S. Ahmadi-Pour, K. Qayyum, C. K. Jha, and R. Drechsler,
     compose: Code generation using transformer,” in Proceedings of the                “Llm-guided formal verification coupled with mutation testing,” in 2024
     28th ACM joint meeting on European software engineering conference                Design, Automation & Test in Europe Conference & Exhibition (DATE).
     and symposium on the foundations of software engineering, 2020, pp.               IEEE, 2024, pp. 1–2.
     1433–1443.                                                                   [23] S. Jha, S. K. Jha, P. Lincoln, N. D. Bastian, A. Velasquez, and S. Neema,
 [2] B. A. Becker, P. Denny, J. Finnie-Ansley, A. Luxton-Reilly, J. Prather,           “Dehallucinating large language models using formal methods guided
     and E. A. Santos, “Programming is hard-or at least it used to be:                 iterative prompting,” in 2023 IEEE International Conference on Assured
     Educational opportunities and challenges of ai code generation,” in               Autonomy (ICAA). IEEE, 2023, pp. 149–152.
     Proceedings of the 54th ACM Technical Symposium on Computer                  [24] T. Morishita, G. Morio, A. Yamaguchi, and Y. Sogawa, “Enhancing
     Science Education V. 1, 2023, pp. 500–506.                                        reasoning capabilities of llms via principled synthetic logic corpus,” Ad-
 [3] Y. Li, D. Choi, J. Chung, N. Kushman, J. Schrittwieser, R. Leblond,               vances in Neural Information Processing Systems, vol. 37, pp. 73 572–
     T. Eccles, J. Keeling, F. Gimeno, A. Dal Lago et al., “Competition-               73 604, 2024.
     level code generation with alphacode,” Science, vol. 378, no. 6624, pp.      [25] S. Hao, Y. Gu, H. Luo, T. Liu, X. Shao, X. Wang, S. Xie, H. Ma,
     1092–1097, 2022.                                                                  A. Samavedhi, Q. Gao et al., “Llm reasoners: New evaluation, library,
 [4] Q. Gu, “Llm-based code generation method for golang compiler testing,”            and analysis of step-by-step reasoning with large language models,”
     in Proceedings of the 31st ACM Joint European Software Engineering                arXiv preprint arXiv:2404.05221, 2024.
     Conference and Symposium on the Foundations of Software Engineering,         [26] Y. Zhang, S. Mao, T. Ge, X. Wang, A. de Wynter, Y. Xia, W. Wu,
     2023, pp. 2201–2203.                                                              T. Song, M. Lan, and F. Wei, “Llm as a mastermind: A survey
 [5] J. Wang and Y. Chen, “A review on code generation with llms:                      of strategic reasoning with large language models,” arXiv preprint
     Application and evaluation,” in 2023 IEEE International Conference on             arXiv:2404.01230, 2024.
     Medical Artificial Intelligence (MedAI). IEEE, 2023, pp. 284–289.
                                                                                  [27] Z. Zhou, J. Song, K. Yao, Z. Shu, and L. Ma, “Isr-llm: Iterative self-
 [6] J. Liu, C. S. Xia, Y. Wang, and L. Zhang, “Is your code generated by
                                                                                       refined large language model for long-horizon sequential task planning,”
     chatgpt really correct? rigorous evaluation of large language models for
                                                                                       in 2024 IEEE International Conference on Robotics and Automation
     code generation,” Advances in Neural Information Processing Systems,
                                                                                       (ICRA). IEEE, 2024, pp. 2081–2088.
     vol. 36, pp. 21 558–21 572, 2023.
                                                                                  [28] Y. Abbasi Yadkori, I. Kuzborskij, A. György, and C. Szepesvari, “To
 [7] C. Xiong, C. Liu, H. Li, and X. Li, “Hlspilot: Llm-based high-
                                                                                       believe or not to believe your llm: Iterative prompting for estimating
     level synthesis,” in Proceedings of the 43rd IEEE/ACM International
                                                                                       epistemic uncertainty,” Advances in Neural Information Processing
     Conference on Computer-Aided Design, 2024, pp. 1–9.
                                                                                       Systems, vol. 37, pp. 58 077–58 117, 2024.
 [8] T. Ye, Y. Du, T. Ma, L. Wu, X. Zhang, S. Ji, and W. Wang, “Uncovering
     llm-generated code: A zero-shot synthetic code detector via code rewrit-     [29] N. Shinn, F. Cassano, A. Gopinath, K. Narasimhan, and S. Yao, “Reflex-
     ing,” in Proceedings of the AAAI Conference on Artificial Intelligence,           ion: Language agents with verbal reinforcement learning,” Advances in
     vol. 39, no. 1, 2025, pp. 968–976.                                                Neural Information Processing Systems, vol. 36, pp. 8634–8652, 2023.
 [9] Z. Ságodi, I. Siket, and R. Ferenc, “Methodology for code synthesis         [30] H. Le, Y. Wang, A. D. Gotmare, S. Savarese, and S. C. H. Hoi,
     evaluation of llms presented by a case study of chatgpt and copilot,”             “Coderl: Mastering code generation through pretrained models and deep
     Ieee Access, 2024.                                                                reinforcement learning,” Advances in Neural Information Processing
[10] W. Shen and C. Zhang, “Policy filtration in rlhf to fine-tune llm for code        Systems, vol. 35, pp. 21 314–21 328, 2022.
     generation,” arXiv preprint arXiv:2409.06957, 2024.                          [31] B. Chen, F. Zhang, A. Nguyen, D. Zan, Z. Lin, J.-G. Lou, and
[11] J. Gehring, K. Zheng, J. Copet, V. Mella, Q. Carbonneaux, T. Cohen,               W. Chen, “Codet: Code generation with generated tests,” arXiv preprint
     and G. Synnaeve, “Rlef: Grounding code llms in execution feedback                 arXiv:2207.10397, 2022.
     with reinforcement learning,” arXiv preprint arXiv:2410.02089, 2024.         [32] M. Yuksekgonul, F. Bianchi, J. Boen, S. Liu, Z. Huang, C. Guestrin, and
[12] F. Liu, Y. Liu, L. Shi, H. Huang, R. Wang, Z. Yang, L. Zhang, Z. Li,              J. Zou, “Textgrad: Automatic” differentiation” via text,” arXiv preprint
     and Y. Ma, “Exploring and evaluating hallucinations in llm-powered                arXiv:2406.07496, 2024.
     code generation,” arXiv preprint arXiv:2404.00971, 2024.                     [33] Z. Li, W. Hua, H. Wang, H. Zhu, and Y. Zhang, “Formal-llm: Integrating
[13] Z. Zhang, C. Wang, Y. Wang, E. Shi, Y. Ma, W. Zhong, J. Chen,                     formal language and natural language for controllable llm-based agents,”
     M. Mao, and Z. Zheng, “Llm hallucinations in practical code generation:           arXiv preprint arXiv:2402.00798, 2024.
     Phenomena, mechanism, and mitigation,” Proceedings of the ACM on             [34] B. Hui, J. Yang, Z. Cui, J. Yang, D. Liu, L. Zhang, T. Liu, J. Zhang,
     Software Engineering, vol. 2, no. ISSTA, pp. 481–503, 2025.                       B. Yu, K. Lu et al., “Qwen2. 5-coder technical report,” arXiv preprint
[14] S. Ouyang, J. M. Zhang, M. Harman, and M. Wang, “Llm is like a                    arXiv:2409.12186, 2024.
     box of chocolates: the non-determinism of chatgpt in code generation,”       [35] A. Yang, A. Li, B. Yang, B. Zhang, B. Hui, B. Zheng, B. Yu, C. Gao,
     arXiv e-prints, pp. arXiv–2308, 2023.                                             C. Huang, C. Lv et al., “Qwen3 technical report,” arXiv preprint
[15] S. Liu and R. Adams, “Limitations of formal methods and an approach to            arXiv:2505.09388, 2025.
     improvement,” in Proceedings 1995 Asia Pacific Software Engineering          [36] OpenAI, “Introducing GPT-4.1, GPT-4.1 Mini, and GPT-4.1 Nano,”
     Conference. IEEE, 1995, pp. 498–507.                                              https://openai.com/index/gpt-4-1/, 2025, accessed: July 7, 2025.
[16] J. Woodcock, P. G. Larsen, J. Bicarregui, and J. Fitzgerald, “Formal         [37] W. Kwon, Z. Li, S. Zhuang, Y. Sheng, L. Zheng, C. H. Yu, J. E.
     methods: Practice and experience,” ACM computing surveys (CSUR),                  Gonzalez, H. Zhang, and I. Stoica, “Efficient memory management for
     vol. 41, no. 4, pp. 1–36, 2009.                                                   large language model serving with pagedattention,” in Proceedings of
[17] A. Agarwal, A. Chan, S. Chandel, J. Jang, S. Miller, R. Z. Moghaddam,             the ACM SIGOPS 29th Symposium on Operating Systems Principles,
     Y. Mohylevskyy, N. Sundaresan, and M. Tufano, “Copilot evaluation                 2023.
     harness: Evaluating llm-guided software programming,” arXiv preprint         [38] M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. de Oliveira Pinto, J. Kaplan,
     arXiv:2402.14261, 2024.                                                           H. Edwards, Y. Burda, N. Joseph, G. Brockman, A. Ray, R. Puri,
[18] S. Fakhoury, A. Naik, G. Sakkas, S. Chakraborty, and S. K. Lahiri, “Llm-          G. Krueger, M. Petrov, H. Khlaaf, G. Sastry, P. Mishkin, B. Chan,
     based test-driven interactive code generation: User study and empirical           S. Gray, N. Ryder, M. Pavlov, A. Power, L. Kaiser, M. Bavarian,
     evaluation,” IEEE Transactions on Software Engineering, 2024.                     C. Winter, P. Tillet, F. P. Such, D. Cummings, M. Plappert, F. Chantzis,
[19] Y. Zhang, Y. Cai, X. Zuo, X. Luan, K. Wang, Z. Hou, Y. Zhang,                     E. Barnes, A. Herbert-Voss, W. H. Guss, A. Nichol, A. Paino, N. Tezak,
     Z. Wei, M. Sun, J. Sun et al., “The fusion of large language models and           J. Tang, I. Babuschkin, S. Balaji, S. Jain, W. Saunders, C. Hesse,
     formal methods for trustworthy ai agents: A roadmap,” arXiv preprint              A. N. Carr, J. Leike, J. Achiam, V. Misra, E. Morikawa, A. Radford,
     arXiv:2412.06512, 2024.                                                           M. Knight, M. Brundage, M. Murati, K. Mayer, P. Welinder, B. McGrew,
     D. Amodei, S. McCandlish, I. Sutskever, and W. Zaremba, “Evaluating
     large language models trained on code,” 2021.
[39] A. G. W.-D. L. F. Y. T. Z. S. W. A. S.-L. K. S. I. S. Naman Jain,
     King Han, “Livecodebench: Holistic and contamination free evaluation
     of large language models for code,” arXiv preprint, 2024.
[40] LeetCode, “Problemset,” https://leetcode.com/problemset/, 2025, ac-
     cessed: 2025-07-11.
