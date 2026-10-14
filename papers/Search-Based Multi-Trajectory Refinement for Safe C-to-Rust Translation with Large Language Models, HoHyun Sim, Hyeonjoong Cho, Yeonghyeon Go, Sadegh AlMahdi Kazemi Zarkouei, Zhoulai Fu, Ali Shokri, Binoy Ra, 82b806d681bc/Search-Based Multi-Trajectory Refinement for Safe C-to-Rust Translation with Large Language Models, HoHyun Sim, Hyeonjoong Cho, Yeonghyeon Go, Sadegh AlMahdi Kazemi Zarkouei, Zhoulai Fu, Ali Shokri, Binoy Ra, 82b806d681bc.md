                                            Search-Based Multi-Trajectory Refinement for Safe C-to-Rust
                                                     Translation with Large Language Models
                                                              HoHyun Sim                                                Hyeonjoong Cho∗                                      Yeonghyeon Go
                                                     tlaghgus0425@korea.ac.kr                                            raycho@korea.ac.kr                               doori74126@korea.ac.kr
                                                          Korea University                                                 Korea University                                  Korea University
                                                        Sejong, South Korea                                              Sejong, South Korea                                Sejong, South Korea

                                                   Sadegh AlMahdi Kazemi                                                       Zhoulai Fu                                        Ali Shokri
                                                          Zarkouei                                                 zhoulai.fu@sunykorea.ac.kr                            ashokri@Central.UH.EDU
                                                 skazemiz@CougarNet.UH.EDU                                                 SUNY Korea                                      University of Houston
                                                                                                                      Incheon, South Korea                                  Houston, TX, USA
arXiv:2505.15858v3 [cs.PL] 6 Apr 2026




                                                     University of Houston
                                                       Houston, TX, USA

                                                                                                                         Binoy Ravindran
                                                                                                                            binoy@vt.edu
                                                                                                                            Virginia Tech.
                                                                                                                         Blacksburg, VA, USA

                                        Abstract                                                                                            a C-to-Rust problem space and have not explored the use of system-
                                        The C programming language has been foundational in building                                        atic search mechanisms to navigate the space of possible refinement
                                        system-level software. However, its manual memory management                                        trajectories. To address these challenges in the C-to-Rust transla-
                                        model frequently leads to memory safety issues. In response, a mod-                                 tion, we propose the MCTS (Monte Carlo Tree Search)-Guided
                                        ern system programming language, Rust, has emerged as a memory-                                     LLM refinement technique for automated C-to-safe-Rust transla-
                                        safe alternative. Moreover, automating the C-to-Rust translation em-                                tion (LAC2R). LAC2R uses MCTS to systematically explore multiple
                                        powered by the rapid advancements of the generative capabilities                                    refinement trajectories and organize the LLM-induced intermediate
                                        of LLMs is gaining growing interest for large volumes of legacy C                                   steps for correct translation. We experimentally demonstrated that
                                        code. Leveraging the LLM capabilities for the C-to-Rust translation                                 LAC2R effectively conducts C-to-Rust translation on large-scale,
                                        introduces distinct challenges, unlike the math or commonsense                                      real-world benchmarks. On GNU coreutils benchmarks (7 programs,
                                        QA domains where the LLM capabilities have been predominantly                                       <15 KLoC), LAC2R achieves an average function-compile rate (FCR)
                                        applied. First, the scarcity of parallel C-to-Rust datasets hinders                                 of 97%, surpassing two major counterparts, such as C2SaferRust
                                        the retrieval of suitable code translation exemplars for in-context                                 (74–80%) and EvoC2Rust (59%); EvoC2Rust, however, passes 0% of
                                        learning. Second, unlike math or commonsense QA problems, the in-                                   behavioral test cases, yielding functionally inequivalent transla-
                                        termediate steps required for C-to-Rust are not well-defined. Third,                                tions due to brace mismatches introduced by LLM code generation
                                        it remains unclear how to organize and cascade these intermediate                                   in macro-heavy functions. On Laertes benchmarks (10 programs,
                                        steps to construct a correct translation trajectory. While existing                                 <96 KLoC), LAC2R achieves an average FCR of 88% with full project
                                        LLM-based approaches have achieved some success, they have re-                                      compilability, while EvoC2Rust, despite reporting the highest aver-
                                        lied on iterative code refinement along a single search trajectory on                               age safety ratio (0.75), fails to produce a project-compilable trans-
                                                                                                                                            lation across all ten benchmarks. Among approaches that yield
                                        ∗ Corresponding author.
                                                                                                                                            valid, executable translations, LAC2R achieves the best safety ratio
                                                                                                                                            on both suites (0.50 vs. 0.32–0.33 for coreutils; 0.54 vs. 0.26–0.29
                                        Authors’ Contact Information: HoHyun Sim, tlaghgus0425@korea.ac.kr, Korea Uni-
                                        versity, Sejong, South Korea; Hyeonjoong Cho, raycho@korea.ac.kr, Korea University,                 for Laertes) and reduces linter warnings by 25–39% compared to
                                        Sejong, South Korea; Yeonghyeon Go, doori74126@korea.ac.kr, Korea University, Se-                   C2SaferRust. On small-scale benchmarks, the TRACTOR Public-
                                        jong, South Korea; Sadegh AlMahdi Kazemi Zarkouei, skazemiz@CougarNet.UH.EDU,                       Tests (Battery-01 + P00_perlin_noise), LAC2R is the only method
                                        University of Houston, Houston, TX, USA; Zhoulai Fu, zhoulai.fu@sunykorea.ac.kr,
                                        SUNY Korea, Incheon, South Korea; Ali Shokri, ashokri@Central.UH.EDU, Univer-                       that simultaneously attains the highest safety ratio (0.95 vs. 0–0.88),
                                        sity of Houston, Houston, TX, USA; Binoy Ravindran, binoy@vt.edu, Virginia Tech.,                   perfect project-level correctness (100% program compilation and
                                        Blacksburg, VA, USA.
                                                                                                                                            100% program pass rate), and the fewest linter warnings among
                                        Permission to make digital or hard copies of all or part of this work for personal or               the compared methods. The results indicate that LAC2R substan-
                                        classroom use is granted without fee provided that copies are not made or distributed               tially improves safety and reliability in program-level C-to-Rust
                                        for profit or commercial advantage and that copies bear this notice and the full citation           translation.
                                        on the first page. Copyrights for components of this work owned by others than the
                                        author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or
                                        republish, to post on servers or to redistribute to lists, requires prior specific permission
                                        and/or a fee. Request permissions from permissions@acm.org.                                         CCS Concepts
                                        © 2018 Copyright held by the owner/author(s). Publication rights licensed to ACM.
                                        ACM 2475-1421/2018/4-ART                                                                            • Computing methodologies → Artificial intelligence; • Soft-
                                        https://doi.org/XXXXXXX.XXXXXXX                                                                     ware and its engineering → General programming languages.
                                                                                                                                        1
Conference’17, July 2017, Washington, DC, USA                                                                                            Trovato et al.


Keywords
Monte Carlo Tree Search, Large Language Model, C-to-Rust


1    Introduction
The C programming language has been foundational for building
system-level software, such as operating systems, embedded sys-
                                                                               Figure 1: The common execution flow of existing LLM-based
tems, and performance-critical applications. Its fine-grained control
                                                                               C-to-Rust translation methods. The dotted connections are
over hardware makes it indispensable in such domains. However,
                                                                               selectively established.
C’s manual memory management model frequently leads to mem-
ory safety issues such as buffer overflows, dangling pointers, and
data races. Industry reports have estimated that 70% of their secu-
rity vulnerabilities stem from these memory safety issues [25, 27]             datasets makes it difficult to retrieve suitable translation exemplars
and the US government recently emphasized the importance of tran-              for in-context learning, which limits the effectiveness of existing
sitioning to safe programming languages [13, 14]. In response, a               multi-step prompting techniques such as few-shot chain-of-thought
modern system programming language, Rust, has emerged as an al-                reasoning [30]. Second, unlike math or commonsense QA problems
ternative that offers memory safety by enforcing a strict ownership            where intermediate steps can be logically defined and easily verified,
and borrowing model at compile time. Rust has been successfully                the intermediate steps required for C-to-Rust are not well-defined.
adopted in several projects, including Mozilla Firefox and AWS                 Third, even if individual intermediate steps for C-to-Rust are given,
Firecracker. However, a large number of legacy C codes still exist             it remains unclear how to organize a promising multi-step trajec-
and manually converting them into Rust requires significant cost,              tory toward a correct C-to-Rust translation. As a result, addressing
which has driven growing interest in automating the C-to-Rust                  the C-to-Rust translation task requires methods that can induce
translation.                                                                   LLMs to generate effective intermediate-step results that facilitate
   Existing automatic C-to-Rust translation techniques are gener-              the C-to-Rust transformation, as well as systematic search mecha-
ally classified into two categories: rule-based and LLM-based ap-              nisms to coordinate those intermediate steps effectively.
proaches. Traditional rule-based approaches, such as C2Rust [15],                  However, existing LLM-based approaches have relied on itera-
aim to preserve equivalence during translation. However, they often            tive refinement along a single search trajectory, leaving the multi-
produce non-idiomatic Rust code that contains unsafe blocks and                trajectory search space unexplored despite its natural formulation
low-level constructs, which undermines both safety and maintain-               as a sequential decision-making problem.
ability. In contrast, LLM-based approaches can generate idiomatic              Contributions. Motivated by these challenges, we propose the
and safer Rust code, as LLMs are trained on the corpora of human-              MCTS-Guided LLM refinement for Automated C-to-safe-Rust trans-
written code. Nevertheless, they lack equivalence guarantees due to            lation (LAC2R). To build a code translation technique capable of
the hallucination problem inherent to LLMs. To address this, recent            systematically planning the intermediate steps for C-to-Rust trans-
approaches combine the generative capabilities of LLMs and the                 lation, we formulate the translation as a sequential decision-making
verifiable determinism of external tools, such as code analyzers and           problem in a code refinement search space. To generate and nav-
validators, to mitigate hallucinations.                                        igate the diverse reasoning trajectories for this task, we propose
   Several LLM-based approaches have been proposed recently,                   using the Monte Carlo Tree Search (MCTS) [3] as a framework
each with unique features, as listed in Table 6. At a high-level, how-         where the intermediate reasoning steps, such as iterative code re-
ever, they share a similar execution flow as illustrated in Figure 1. In       finement, are systematically structured. MCTS enables a principled
this flow, a preprocessor decomposes the original C code into small            balance between exploration and exploitation by organizing a tree-
snippets and, if necessary, translates them into initial Rust code.            like reasoning structure guided by the Upper Confidence bounds
In parallel, a code analyzer extracts additional information about             applied to Trees (UCT) with reward evaluation. We propose a re-
the original code and provides it to the LLM-based code converter,             ward calculation tailored for C-to-Rust and assess its effectiveness.
validator, or postprocessor, depending on the design choice. When              In addition, we leverage multiple heterogeneous LLMs to gener-
the information is provided in the form of the prompt, the LLM                 ate intermediate refinement steps for C-to-Rust code translation.
converter generates a Rust code snippet and the postprocessor pre-             Leveraging different LLMs enhances diversity in Rust refinement
pares it for validation. Then, the validator checks the correctness            candidates as the heterogeneity of their training datasets encour-
of the generated code in several dimensions, such as compilability             ages their complementary translation.
and equivalence. Based on feedback from the validator, the LLM                     In addition, we experimentally show that LAC2R effectively
converter iteratively refines the Rust code until predefined termina-          conducts C-to-Rust translation on large-scale, real-world bench-
tion conditions are satisfied. This iterative code refinement strategy         marks compared to prior counterparts. On the GNU coreutils bench-
using the external feedback has been successfully applied to several           marks, LAC2R achieves the highest average FCR (97%), surpassing
benchmarks as shown in Table 1.                                                C2SaferRust (74–80%) and EvoC2Rust (59%); however, EvoC2Rust
Challenge. Leveraging the LLM capabilities for the C-to-Rust                   passes 0% of behavioral test cases across all seven benchmarks,
translation introduces distinct challenges, unlike the math or com-            indicating that its translations do not preserve the original pro-
monsense QA domains where the LLM capabilities have been pre-                  gram behavior. On the Laertes benchmarks, LAC2R achieves an
dominantly applied [32]. First, the scarcity of parallel C-to-Rust             average FCR of 88% while maintaining full project compilability;
                                                                           2
Search-Based Multi-Trajectory Refinement for Safe C-to-Rust Translation with Large Language Models                             Conference’17, July 2017, Washington, DC, USA


in contrast, EvoC2Rust, despite reporting the highest safety ratio
(0.75), fails to produce a project-compilable translation in any of the
ten benchmarks, rendering its safety improvement unverifiable in
practice. Among approaches that produce executable, behaviorally
equivalent translations, LAC2R achieves the highest safety ratio
on both suites, 0.50 for coreutils (vs. 0.32–0.33 for C2SaferRust)
and 0.54 for Laertes (vs. 0.26–0.29), and reduces linter warnings by
25–39%. We also evaluate LAC2R on the TRACTOR Public-Tests
benchmark (Battery-01 + P00_perlin_noise). On this benchmark,                          Figure 3: LAC2R’s translation example including a target C
LAC2R outperforms counterparts such as SACTOR, EvoC2Rust, and                          function, its unsafe Rust conversion by C2Rust, and its final
RustAssure across both safety and code quality metrics. Compared                       Rust translation. argmatch_exact() is a sub-function of tail
to C2SaferRust, LAC2R matches the highest project-level correct-                       benchmark in the GNU coreutils suite.
ness (100% program compilation and 100% program pass rate) while
simultaneously attaining a superior safety ratio and substantially                     2.2     Problem Formulation
fewer linter warnings, demonstrating that correctness and safety
                                                                                       We formulate the iterative Rust refinement of a single function as
need not be traded off against one another.
                                                                                       a finite-horizon, constrained sequential decision-making problem
2     Proposed Approach                                                                that aims at maximizing the safety of the Rust result. Formally,
                                                                                       the problem is defined by a tuple (R, A, 𝜏, 𝑆, 𝑐 0 ), where R denotes
                                                                                       a potentially unbounded state space of Rust codes for the target
                                                                                       function, A denotes a set of refinement actions, 𝜏 : R × A → R
                                                                                       denotes the state transition representing the code refinement in
                                                                                       our context, 𝑆 : R → R is a safety evaluation of Rust program, and
                                                                                       𝑐 0 is a target C code.
                                                                                           Given its C2Rust translation 𝑟 0 = C2Rust(𝑐 0 ), the objective is to
                                                                                       obtain a refined Rust program 𝑟 𝑁 after 𝑁 steps that is both safe and
                                                                                       test-equivalent to 𝑐 0 . We denote a fixed test suite by Ttest . We let
                                                                                       Exec(𝑝, 𝑡) be the observable behavior, such as output or exit status,
                                                                                       of program 𝑝 on test 𝑡, and write 𝑝 ≡ Ttest 𝑞 iff Exec(𝑝, 𝑡) = Exec(𝑞, 𝑡)
Figure 2: Overview of LAC2R’s execution flow with an illus-                            for all 𝑡 ∈ Ttest . We also use a validator 𝑉 : R → Z that returns
tration of its key components.                                                         compile/test feedback signals.
                                                                                           We seek a sequence of actions (𝑎 1, ..., 𝑎 𝑁 ) with 𝑟𝑖+1 = 𝜏 (𝑟𝑖 , 𝑎𝑖 ),
                                                                                       formalized as:
2.1     Overview                                                                                           max            𝑆 (𝑟 𝑁 )   s.t. 𝑟 𝑁 ≡ Ttest 𝑐 0 .              (1)
                                                                                                        (𝑎 1 ,...,𝑎 𝑁 )
To address the large scale of legacy C programs and the restricted
context length of LLMs, LAC2R takes an iterative function-wise                         A transition is induced by an LLM-based code refiner 𝐹 and a post-
translation strategy. As illustrated in Figure 2, the execution starts                 processing step Π:
with C2Rust that converts a target C program to an initial unsafe                                       𝜏 (𝑟, 𝑎) = Π 𝐹 prompt𝑎 𝑟, 𝑉 (𝑟 ) .
                                                                                                                                        
                                                                                                                                                      (2)
Rust. This initial compilable Rust program enables focused compile
                                                                                       where 𝑝𝑟𝑜𝑚𝑝𝑡𝑎 denotes a prompt prepared for an action 𝑎. To
check during following function-wise replacement. Then, the Rust
                                                                                       achieve the objective, we propose LAC2R employing MCTS to
program is decomposed into functions and ordered according to
                                                                                       search for an optimal sequence of actions (𝑎 1, ..., 𝑎 𝑁 ).
a dependency graph constructed by a static analyzer. Using this
information, LAC2R repeatedly refines the Rust functions in the
                                                                                       2.3     LAC2R Design
predefined order to generate safer and behaviorally equivalent code.
   To refine a single Rust function, LAC2R searches for the best                       MCTS. LAC2R leverages MCTS to construct promising code re-
refinement trajectory from the initial unsafe Rust function to the                     finement trajectories. MCTS builds a search tree where each node
final candidate using MCTS. MCTS constructs a search tree by                           represents a state of intermediate Rust code and each edge rep-
repeatedly expanding edges until a termination criterion is met,                       resents a refinement transition, enabling principled exploration–
where each expansion corresponds to one iteration comprising LLM-                      exploitation balance via UCT. The detailed procedure is described
based code refinement, program reconstruction using the refined                        in Algorithm 1.
function, and validations. Since MCTS prioritizes the trajectories                     Objective and Reward Functions. LAC2R aims to maximize the
with higher validation scores, it progressively concentrates on the                    safety function 𝑆 as defined in Equation 1. We define 𝑆 to represent
trajectories that produce safer and test-equivalent Rust code.                         the reduction rate in five categories of unsafe Rust constructs, as
   Figure 3 shows an example of LAC2R’s C-to-Rust translation.                         introduced in the prior work [19]. Formally, the 𝑆 is defined as:
                                                                                                                                                         
LAC2R first converts the target C function, argmatch_exact(), to                                                  𝑅𝑃𝐶𝑖 + 𝑅𝑃𝑅𝑖 + 𝐿𝑈𝐶𝑖 + 𝑈𝐶𝐸𝑖 + 𝑈𝑇𝐶𝑖
                                                                                       𝑆 (𝑟𝑖 ) = 𝑚(𝑟𝑖 ) · 𝑚𝑎𝑥 1 −                                          ,0 ,
an unsafe Rust code using C2Rust. Then, LAC2R refines the unsafe                                                  𝑅𝑃𝐶 0 + 𝑅𝑃𝑅0 + 𝐿𝑈𝐶 0 + 𝑈𝐶𝐸 0 + 𝑈𝑇𝐶 0
Rust to the safe one relying on the MCTS framework.                                                                                                      (3)
                                                                                  3
Conference’17, July 2017, Washington, DC, USA                                                                                                    Trovato et al.


where 𝑅𝑃𝐶𝑖 , 𝑅𝑃𝑅𝑖 , 𝐿𝑈𝐶𝑖 , 𝑈𝐶𝐸𝑖 , and 𝑈𝑇𝐶𝑖 denote the numbers of                    are no compile-time or test-case execution errors. It indicates that
raw pointer declaration, raw pointer dereferences, lines of unsafe                  more than 80% of the successfully translated functions achieve
code, unsafe call expressions, and unsafe type casts in the Rust                    this within the first five iterations. Additionally, iterative code re-
program with the function 𝑟𝑖 , respectively. If the Rust program with               finement beyond five iterations tends to be less effective and no
𝑟𝑖 is compilable, 𝑚(𝑟𝑖 ) = 1; otherwise, 𝑚(𝑟𝑖 ) = 0. The indicator                  additional function is successfully translated after 20 iterations,
𝑚(𝑟𝑖 ) is adopted to prioritize compilability over safety and penalize              although the total 𝐹𝑅𝑅 does not reach 100%. To take advantage of
non-compilable code.                                                                the higher 𝐹𝑅𝑅 in the early iterations, LAC2R is designed to gen-
   The compile score 𝐶 (𝑟𝑖 ) is computed as:                                        erate an increased number of initial Rust candidates. In addition,
                                        1                                           to improve the effectiveness of long iterative refinement, LAC2R
                        𝐶 (𝑟𝑖 ) =                ,                 (4)              incorporates diversity using heterogeneous LLMs. Moreover, to
                                  |𝐸𝐶 (𝑟𝑖 )| + 1
                                                                                    reduce the iteration length, we allow each node to spawn multiple
where |𝐸𝐶 | is the number of compile errors.
                                                                                    child nodes as presented in [21].
   To select a promising node for tree expansion, MCTS uses the
                                                                                    Algorithm. LAC2R employs an MCTS-based search strategy as
UCT that is updated based on a reward. LAC2R defines the node
                                                                                    presented in Algorithm 1. Each rollout performs four standard
reward 𝑅 based on both the compile score and the safety of the Rust
                                                                                    MCTS phases (Lines 6–10): UCT-guided selection to a promising
code. Formally, the 𝑅 is computed as:
                                                                                    leaf, expansion via Expand (Algorithm 2), greedy simulation to
   𝑅 = 𝑅𝑉 + 𝑤 · 𝑅𝑆 = 𝐶 (𝑟𝑖 ) − 𝐶 (𝑟𝑖 −1 ) + 𝑤 · (𝑆 (𝑟𝑖 ) − 𝑆 (𝑟𝑖 −1 )),   (5)       a terminal node, and backpropagation of rewards along the full
    where 𝑅𝑉 denotes a reward computed using validation feedbacks                   path. The process repeats for num_rollouts iterations, and the
and 𝑅𝑆 denotes a reward computed using safety metrics. The scalar                   final solution is selected from the constructed tree (Line 4).
𝑤 is a weighting factor that balances the contributions of two                          Expansion, one of LAC2R’s core phases, is described in detail
reward terms.                                                                       in Algorithm 2. When expanding the root (Init) node, multiple
    Since the reward is defined as the increment from each node to                  Gen children are created using heterogeneous LLMs (Lines 2–3),
its child, the cumulative reward along a trajectory corresponds to                  exploiting the higher success rates in the early iterations observed
the total improvement from the root to the terminal node. Thus,                     in Figure 4. During non-root expansions, the LLM generates a
the MCTS policy of maximizing the expected accumulated reward                       candidate translation using the conversation history and any prior
steers the search toward both reducing compilation errors and                       feedback, which is then inserted into the full program (Lines 4–5).
increase the safety score. When compilation succeeds, the search                    If compilation succeeds, the node reward is computed based on
effectively maximizes the objective function.                                       the safety score and compile status (Line 7). When test suites are
Transition Action with Heterogeneous LLMs. To obtain diverse                        available, they are executed: if all tests pass, a Success child is added
intermediate refinements, LAC2R uses heterogeneous LLMs, whose                      to the node (Line 10); otherwise, Fix children are added with test-
distinct training datasets encourage complementary refinement                       execution errors as feedback (Line 11). If no test suites are available,
effects.                                                                            a successful compilation alone is sufficient to add a Success child
    LAC2R allows two types of actions for transitions, such as code                 (Line 12). When compilation fails, Fix children are added with
refinement with validator feedback and without feedback, denoted                    compiler error messages as feedback (Line 13). This feedback-driven
by (𝑓 𝑒𝑒𝑑𝑏𝑎𝑐𝑘, 𝐿𝐿𝑀𝐾 ) and (𝑛𝑢𝑙𝑙, 𝐿𝐿𝑀𝑘 ), respectively. 𝑘 ∈ {1, ..., 𝐾 }             error repair enables LAC2R to progressively converge to correct
indexes available LLMs where 𝐾 is the total number. For the ac-                     translations (Lines 4–13).
tion with feedback, the LLM prompt incorporates feedback from                       Prompt. Figure 5 presents the main prompt for LAC2R. The prompt
validators, such as a compiler and a testcase executor for code                     largely follows a prior work, C2SaferRust’s prompt except for line
refinement.                                                                         1-6 that explicitly clarifies the translation direction. The prompt
                                                                                    defines four placeholders in line 9-12. {unsafe_rust} is for the
                                                                                    target Rust code, {call_sites} is for the list of call sites calling the
                                                                                    target Rust function, {global} is for global variables, and {import}
                                                                                    is for import information. The prompt instructs LLMs to produce the
                                                                                    translation results within <FUNC> and <\FUNC>. In addition to the
                                                                                    main prompt, LAC2R employs two more prompts, one for correcting
                                                                                    compile errors and another for addressing testcase execution errors.
                                                                                    Both prompts follow the C2SaferRust prompts.
Figure 4: The FRR distribution of C2SaferRust’s iterative
Rust refinement over iterations.
                                                                                    3 Experiments
Tree Configuration. As shown in Table 6, most existing LLM-                         3.1 Experimental Setup
based C-to-Rust translation methods, including C2SaferRust, rely                    Baseline and Benchmarks. For experimental comparison, we
on sequential, iterative code refinement based on external feedback.                selected C2SaferRust as our baseline, as its open implementa-
When running C2SaferRust on the seven coreutil benchmarks as                        tion has been empirically shown to support large-scale, real-world
in [19], the distribution of function-replacement rate (𝐹𝑅𝑅) over                   benchmarks, as shown in Table 1. C2SaferRust supports two types
iterations is visualized in Figure 4, where a function translation is               of decompositions: function-wise and unit-wise, where a unit can
counted as successful (i.e., 𝐹𝑅𝑅 = 1 for that function) when there                  be smaller than a function. In their experiments, the unit-wise
                                                                                4
 Search-Based Multi-Trajectory Refinement for Safe C-to-Rust Translation with Large Language Models                     Conference’17, July 2017, Washington, DC, USA


   Algorithm 1: High-level procedure of LAC2R’s MCTS                                        Algorithm 2: High-level procedure of Expand()
   Input: 𝑓 𝑢𝑛𝑐: target Rust function; 𝑝𝑟𝑜𝑔𝑟𝑎𝑚: full Rust                                 Input: 𝑛𝑜𝑑𝑒: MCTS node; 𝑝𝑟𝑜𝑔𝑟𝑎𝑚: full Rust program; 𝑇 𝑡𝑒𝑠𝑡 :
          program;                                                                               test suite (may be ∅)
          𝑁𝑟𝑜𝑙𝑙𝑜𝑢𝑡 : number of MCTS rollouts;                                           1 Types: Init (root), Gen (initial translation), Fix (error repair),
          𝑆 (·): safety ratio function (fraction of safe code in a                         Success (valid solution);
   Rust snippet);                                                                       2 Func Expand(𝑛𝑜𝑑𝑒, 𝑝𝑟𝑜𝑔𝑟𝑎𝑚):
          𝑄 (𝑛): accumulated reward of node 𝑛                                           3    if 𝑛𝑜𝑑𝑒.𝑡𝑦𝑝𝑒 = Init // root: spawn diverse initial
   Output: 𝑏𝑒𝑠𝑡_𝑛𝑜𝑑𝑒: highest-reward solution node found                                      candidates then
 0 Node structure: each node 𝑛 holds 𝑛.𝑟𝑢𝑠𝑡 (translated Rust
                                                                                        4        create multiple Gen children of 𝑛𝑜𝑑𝑒 using
    snippet), 𝑛.𝑝𝑟𝑜𝑔𝑟𝑎𝑚 (full Rust program with 𝑛.𝑟𝑢𝑠𝑡
                                                                                                   heterogeneous LLMs;
    substituted), 𝑛.𝑡𝑦𝑝𝑒 ∈ {Init, Gen, Fix, Success};
                                                                                        5    else
 1 Func MCTS_Search(𝑓 𝑢𝑛𝑐, 𝑝𝑟𝑜𝑔𝑟𝑎𝑚):
                                                                                        6        𝑟𝑒𝑠𝑝 ← LLM(𝑛𝑜𝑑𝑒.𝑐𝑜𝑛𝑣𝑒𝑟𝑠𝑎𝑡𝑖𝑜𝑛);            // translate
 2    𝑟𝑜𝑜𝑡 ← Create_Node(𝑓 𝑢𝑛𝑐, type=Init); // root node;
                                                                                                   using conversation history and prior
        no LLM call yet                                                                            feedback
 3    for 𝑖 ← 1 to 𝑁𝑟𝑜𝑙𝑙𝑜𝑢𝑡 do                                                          7        insert 𝑟𝑒𝑠𝑝 into 𝑝𝑟𝑜𝑔𝑟𝑎𝑚;
 4         MCTS_Rollout(𝑟𝑜𝑜𝑡, 𝑖, 𝑝𝑟𝑜𝑔𝑟𝑎𝑚);
                                                                                        8        if compile(𝑝𝑟𝑜𝑔𝑟𝑎𝑚) succeeds then
 5     return Find_Best_Solution(𝑟𝑜𝑜𝑡);                                                 9            𝑛𝑜𝑑𝑒.𝑟𝑒𝑤𝑎𝑟𝑑 ← compute_reward(𝑝𝑟𝑜𝑔𝑟𝑎𝑚);
 6 Func MCTS_Rollout(𝑟𝑜𝑜𝑡, 𝑖, 𝑝𝑟𝑜𝑔𝑟𝑎𝑚):                                                                // based on safety score and compile
 7    𝑝𝑎𝑡ℎ𝑠 ← Select(𝑟𝑜𝑜𝑡, 𝑖); // UCT-guided path to a                                                 status
        leaf                                                                           10             if |𝑇 𝑡𝑒𝑠𝑡 | > 0 then
 8    𝑙𝑒𝑎𝑓 ← 𝑝𝑎𝑡ℎ𝑠 .last();                                                            11                  if run_tests(𝑝𝑟𝑜𝑔𝑟𝑎𝑚, 𝑇 𝑡𝑒𝑠𝑡 ) passes then
 9    Expand(𝑙𝑒𝑎𝑓 , 𝑝𝑟𝑜𝑔𝑟𝑎𝑚); // generate children; see                                12                       add Success child to 𝑛𝑜𝑑𝑒; // solution
       Alg. 2                                                                                                     candidate found
10    𝑝𝑎𝑡ℎ𝑟 ← Simulate(𝑙𝑒𝑎𝑓 ); // greedy rollout from                                  13                  else
        leaf to terminal                                                               14                       add Fix children to 𝑛𝑜𝑑𝑒 with test-run
11    Backpropagate(𝑝𝑎𝑡ℎ𝑠 ++ 𝑝𝑎𝑡ℎ𝑟 );      // update 𝑄 and                                                        errors as feedback;
       visit counts along full path                                                    15                else
12    if 𝑝𝑎𝑡ℎ𝑟 ≠ ∅ then return 𝑝𝑎𝑡ℎ𝑟 .last();                                          16                    add Success child to 𝑛𝑜𝑑𝑒; // no tests:
13    else return 𝑙𝑒𝑎𝑓 ;                                                                                      compile pass is sufficient
14 Func Find_Best_Solution(𝑟𝑜𝑜𝑡):                                                      17             else
15    S ← {𝑛 ∈ tree(𝑟𝑜𝑜𝑡) | 𝑛.𝑡𝑦𝑝𝑒 = Success};      // all                             18                 add Fix children to 𝑛𝑜𝑑𝑒 with compile errors as
       test-passing nodes                                                                                  feedback;
16    if S ≠ ∅ then
17        return arg max𝑛∈ S 𝑆 (𝑛.𝑟𝑢𝑠𝑡); // highest safety
           ratio among valid solutions
18    else                                                                              For comparison on small-scale benchmarks, we conducted exper-
19        return 𝑟𝑜𝑜𝑡;      // no valid solution found;                                 iments on the TRACTOR Public-Tests [6] benchmark, which com-
           return original input                                                        prises Battery-01 (B01_organic: 38 programs and B01_synthetic:
                                                                                        85 programs) and one project-level program (P00_perlin_noise),
                                                                                        for a total of 124 programs. TRACTOR Public-Tests was planned,
                                                                                        curated, and created by MIT Lincoln Laboratory, the independent
                                                                                        test and evaluation (T&E) organization for the DARPA TRACTOR
 translation tended to outperform the other. We conduct our experi-                     program, and was designed to objectively evaluate the artifacts pro-
 ments using both variants of C2SaferRust. Notably, LAC2R adopts                        duced by participating performer teams. Battery-01 in total contains
 function-wise decomposition and can be easily extended to support                      150 benchmarks, of which 123 are public and 27 are reserved as hid-
 the unit-wise translation. In addition to C2SaferRust, we selected                     den test cases for independent evaluation. P00_perlin_noise is an
 EvoC2Rust as another counterpart. Unlike both C2SaferRust and                          independent project-level benchmark outside the Battery-01 suite,
 LAC2R, EvoC2Rust adopts a skeleton-guided translation strategy                         included in this work to broaden the evaluation to project-scale
 and does not rely on conventional transpiler-based preprocessing.                      translation.
    For comparison on large-scale, repository-level benchmarks, we                         Metrics. We primarily measure the counts of five unsafe Rust
 conducted experiments on two datasets: seven C programs collected                      constructs, such as 𝑅𝑃𝐷 1 , 𝑅𝑃𝐷 2 , 𝐿𝑈𝐶, 𝑈𝐶𝐸, and 𝑈𝑇𝐶, as intro-
 from GNU coreutils and ten C programs used by a prior transpiler,                      duced in [19]. We then compute the Safety Ratio (𝑆𝑅) as a function
 Laertes [8], that C2SaferRust introduced. The maximum LoCs                             of these five counts using Equation 3. We also compute the Function-
 in these two benchmark datasets are 14K and 96K, respectively.                         level Compile Rate (𝐹𝐶𝑅), defined as the number of functions that
                                                                                   5
Conference’17, July 2017, Washington, DC, USA                                                                                                        Trovato et al.


           Table 1: Prior LLM-based approaches for C-to-Rust translation with their benchmarks and primary metrics.

  Name                   Benchmarks (LoC)                                                         Primary metrics

  VERT [31]              TransCoder-IR dataset(<100), 14 PM prog.1 (<500)                         success rates, runtime
  FLOURINE [9]           libopenaptx (<200), opl (<500)                                           success rates, linter warnings
  SPECTRA [20]           CodeNet dataset                                                          success rates
  SYZYGY [24]            Zopfli (<3K), urlparser (<500)                                           success rates, slow down
  C2SaferRust [19]       coreutils dataset (<15K), Laertes dataset (<96K)                         unsafe constructs2 , success rates
                         TransCoder-IR dataset(<100), CodeNet dataset(<500),
  SACTOR [33]                                                                                     success rates, cost in tokens, linter warnings
                         avl-tree (<500), urlparser (<500)
  SafeTrans [10]         2,653 C programs of CodeNet dataset (<500)                               success rates, coverages, memory safety
  LLMigrate [18]         Three Linux kernel modules: math, sort, ramfs (<900)                     success rates, safe code ratio, laziness, C-BLEU
  EvoC2Rust [29]         Vivo-Bench (<1K), C2R-Bench (<4K)                                        success rates, translation accuracy, memory-safe rate
  RustAssure [2]         libcsv(<500), urlparser(<500), optipng(<3.1K), libbmp(<300), u8c(<400)   compile rate, unsafe code rate, semantic similarity score
                         HumanEval dataset(<500), urlparser, libtree (<2K), json.h(<3.5K),
  Rustify [28]                                                                                    pass rate, compile rate, unsafe ratio, codeBLEU
                         quadtree(<500), buffer(<500), rgba(<500), binn(<4.5K), private (<10K)
  RustMap [5]            RosettaCode dataset, bzip2 (<45K)                                        coverage, unsafe code blocks, cognitive complexity
  1) PM stands for Pointer Manipulation programs.
  2) The unsafe constructs include raw pointer declarations, raw pointer dereferences, unsafe lines, unsafe type casts, and unsafe calls in Rust codes.


                                                                                  measure the number of Linter Warnings in the final translation us-
                                                                                  ing Clippy [22], which checks the idiomaticity and quality of Rust
                                                                                  code. Clippy supports multiple lint levels to help catch various
                                                                                  mistakes, so that the number of linter warnings is not necessarily
                                                                                  proportional to the number of unsafe Rust constructs. In addition,
                                                                                  to assess the translation costs, we measure the average number
                                                                                  of tokens consumed by LLMs and the number of LLM queries for
                                                                                  translating a function of a given benchmark.
                                                                                      For small-scale code datasets, we measure Program-level Compile
                                                                                  Rate (𝑃𝐶𝑅), defined as the number of programs that compile suc-
                                                                                  cessfully after translation divided by the total number of programs
                                                                                  in a given dataset. In addition, We also measure the Program Pass
                                                                                  Rate (𝑃𝑃𝑅), defined as the number of programs that pass all tests
                                                                                  after translation divided by the total number of programs.
                                                                                      LLMs. For comparison, counterpart approaches use GPT-4o,
                                                                                  whereas LAC2R, leverages the pair of GPT-4o and DeepSeek V3 [7]
                                                                                  for LAC2R. LLM capability is often correlated to its scale, although
Figure 5: Main prompt used in LAC2R. When compilation or                          architecture and training also matter. The estimated numbers of
test-run errors occur, the error messages are appended to the                     parameters for GPT-4o and DeepSeek V3 are 200B and 671B [1, 7].
conversation history and passed back to the LLM as feedback                           MCTS Configuration. LAC2R runs 𝑁𝑟𝑜𝑙𝑙𝑜𝑢𝑡 = 10 rollouts per
for the next Fix-node expansion.                                                  function with a UCT exploration constant of 𝐶 = 1.5 (Algorithm 1).
                                                                                  The maximum tree depth is set to 𝐷 = 5. The root Init node gener-
                                                                                  ates four Gen children (two from GPT-4o and two from DeepSeek
                                                                                  V3) as in Algorithm 2. The reward weight is set to 𝑤 = 2, giving
compile successfully after translation divided by the total number                twice the emphasis to safety improvement over compile success.
of functions in a given benchmark. We next measure the Function                       Machine and Running Time for Experiments. We ran all
Replacement Rate (𝐹𝑅𝑅), defined as the proportion of functions                    experiments on a workstation equipped with Intel Xeon Gold 6434
successfully translated in a given benchmark, where a translation                 (32 cores), 512GB memory, and Ubuntu 22.04.4 LTS. These spec-
is considered successful when there are no compile-time or test-                  ifications are reported for reproducibility, not as a requirement.
case execution errors. We also measure the Test Pass Rate (𝑇 𝑃𝑅),                 CPU/memory utilization remained modest in our experiments. The
defined as the number of passed test cases divided by the total                   longest benchmark of coreutils is tail, for which LAC2R completed
number of test cases. For additional code quality evaluation, we                  its translation in approximately 14 hours. In the Laertes dataset, the
                                                                              6
Search-Based Multi-Trajectory Refinement for Safe C-to-Rust Translation with Large Language Models                           Conference’17, July 2017, Washington, DC, USA


longest benchmark is optipng. LAC2R completed its translation
in 48 hours. Between the two variants of C2SaferRust, the one
with the unit-wise decomposition runs longer time than the other.
C2SaferRust with 150 LoC-unit size translated optipng in approx-
imately 120 hours. Elapsed time was largely driven by refinement
iterations and external LLM latency. EvoC2Rust translated tail in
approximately 1.4 hours and optipng in approximately 2.7 hours.                        Figure 7: Function Compile Rate: visualization of the 𝐹𝐶𝑅
                                                                                       column in Table 2 for GNU coreutils benchmarks.
3.2     Results
Comparative Evaluation on large-scale Benchmarks. We eval-
uated LAC2R against the counterparts on two large-scale bench-
marks, such as the coreutils and Laertes. Table 2 shows the results
on the coreutils dataset in several metrics, such as 𝑆𝑅, 𝐹𝐶𝑅, 𝐹𝑅𝑅,
𝑇 𝑃𝑅, LLM costs, and linter warnings. On most coreutil benchmarks,
LAC2R outperforms the counterparts by a large margin. Figure 6
and 7 visualize the results. To normalize Linter warnings, we define                   Figure 8: Idiomaticity: visualization of 𝐼 computed using the
a linter-based idiomaticity score 𝐼 as:                                                Linter warnings in Table 2 for GNU coreutils benchmarks.
                                               
                                      𝑁𝐿 (𝑟𝑖 )
                   𝐼 (𝑟𝑖 ) = 𝑚𝑎𝑥 1 −             ,0 ,             (6)
                                      𝑁𝐿 (𝑟 0 )                                        shows that LAC2R incurs more queries and higher token consump-
where 𝑁𝐿 (𝑟𝑖 ) denotes the number of linter warnings for Rust code                     tion than its counterpart due to its MCTS-based structure.
𝑟𝑖 . The comparison in 𝐼 is presented in Figure 8, that shows that                        For bzip2 in Table 3, LAC2R produces more linter warnings
LAC2R generally scores higher and LAC2R produces Rust code                             than C2Rust, including an additional 234 instances of the "deref
with better idiomaticity compared to its counterparts.                                 which would be done by auto-deref" warning. This reflects cases
     As in Table 2, LAC2R achieves an average 𝑆𝑅 of 0.50 across
coreutil benchmarks, compared to 0.33 for C2SaferRust(U), 0.32                         Table 2: Comparative results on coreutils in detail.
for C2SaferRust(F), and 0.24 for EvoC2Rust, a gain of up to 52%                        C2SaferRust(U) and C2SaferRust(F) denote two versions
over the strongest safety baseline. This consistent advantage reflects                 of C2SaferRust: the former uses unit-wise decomposition,
LAC2R’s safety-aware reward design (Algorithm 2): by weighting                         and the latter employs function-wise decomposition. Bold
safety improvement 𝑅𝑆 twice as heavily as compile success 𝑅𝑉 , UCT                     highlights the best performance across the approaches.
selection (Algorithm 1) preferentially explores refinement paths that
reduce unsafe constructs rather than merely achieving compilation.                       Benchmark
                                                                                                                              FCR      FRR     TPR
                                                                                                                                                      Linter    Ave.    Ave.
                                                                                                        Methods       SR
                                                                                           (LoC)                                                      Warns    Query   Tokens
Translations that compile but retain raw-pointer operations receive
                                                                                                         C2Rust         0       -        -     100%    546       -        -
lower rewards, steering the search toward safer code across ten                                      C2SaferRust(u)   0.14   70.89%   38.70%   100%    436     3.12    5,414
                                                                                            split    C2SaferRust(f)   0.20   80.19%   71.98%   100%    393     2.32    2,961
rollouts.                                                                                 (13,848)     EvoC2Rust      0.17   61.10%   61.10%    0%      -      1.01    3,125
                                                                                                         LAC2R                                 100%            18.82   40,536
     Table 2 also shows the translation cost, including the number of                                                 0.39   95.16%   89.37%           268
                                                                                                         C2Rust         0       -        -     100%    369       -        -
LLM queries and tokens consumed. LAC2R incurs more queries and                                       C2SaferRust(u)   0.43   78.95%   77.63%   100%    223     2.55    3,842
                                                                                           pwd       C2SaferRust(f)   0.41   78.74%   75.59%   100%    222     2.59    4,045
higher token consumption than its counterpart, which is expected                          (5,859)      EvoC2Rust      0.40   67.60%   67.60%    0%      -      1.00    3,068
                                                                                                         LAC2R                                 100%            17.10   50,170
given that LAC2R leverages the MCTS framework to search for                                                           0.77   98.43%   97.63%           74
                                                                                                         C2Rust         0       -        -     100%    414       -        -
better decision trajectories over a candidate population generated                                   C2SaferRust(u)   0.39   79.51%   76.59%   100%    113     2.37    3,763
                                                                                            cat      C2SaferRust(f)   0.38   87.35%   83.73%   100%    262     2.42    3,554
by LLMs.                                                                                  (7,460)      EvoC2Rust      0.28    61.2%    61.2%    0%      -      1.51    4,182
                                                                                                         LAC2R        0.49   98.19%   95.18%   100%    174     14.26   28,851
                                                                                                         C2Rust         0       -        -     100%    385       -        -
                                                                                                     C2SaferRust(u)   0.32   72.94%   68.24%   100%    245     2.63    4,595
                                                                                          truncate   C2SaferRust(f)   0.27   85.48%   80.65%   100%    242     2.69    4,264
                                                                                           (7,181)     EvoC2Rust      0.24    63.9%    63.9%    0%      -      1.02    3,036
                                                                                                         LAC2R        0.33   97.58%   92.74%   100%    176     15.25   36,963
                                                                                                         C2Rust         0       -        -     100%    469       -        -
                                                                                                     C2SaferRust(u)   0.32   74.18%   71.36%   100%    327     2.59    4,738
                                                                                           uniq      C2SaferRust(f)   0.32   80.24%   76.65%   100%    318     2.48    3,541
                                                                                          (8,299)      EvoC2Rust      0.30   61.00%   61.00%    0%      -      1.01    3,103
                                                                                                         LAC2R        0.38   96.41%   94.61%   100%    195     15.91   30,742
                                                                                                         C2Rust         0       -        -     100%    717       -        -
                                                                                                     C2SaferRust(u)   0.36   72.29%   69.43%   100%    449     2.50    4,707
Figure 6: Safety Ratio: visualization of the 𝑆𝑅 column in Ta-                               tail     C2SaferRust(f)   0.31   75.19%   71.80%   100%    434     2.51    3,768
                                                                                          (14,423)     EvoC2Rust      0.19    48.5%    48.5%    0%      -      1.02    3,170
ble 2 for GNU coreutils benchmarks.                                                                      LAC2R        0.60   95.11%   93.60%   100%    248     16.65   42,187
                                                                                                         C2Rust         0       -        -     100%    409       -        -
                                                                                                     C2SaferRust(u)   0.35   70.47%   66.84%   100%    280     2.67    4,523
                                                                                           head      C2SaferRust(f)   0.35   75.16%   70.59%   100%    267
   On most Laertes benchmarks, LAC2R outperforms the coun-                                (8,047)      EvoC2Rust      0.22    56.2%    56.2%    0%      -
                                                                                                                                                               2.60
                                                                                                                                                               1.02
                                                                                                                                                                       4,220
                                                                                                                                                                       4,234
                                                                                                         LAC2R                                 100%            15.94   35,988
terparts in the metrics including 𝑆𝑅, 𝐹𝐶𝑅, 𝐹𝑅𝑅, 𝑇 𝑃𝑅 and linter                                                       0.53   96.73%   92.15%           171
                                                                                          Average        C2Rust         0       -        -     100%    472       -        -
warnings as in Table 3. These results indicate that LAC2R more                                       C2SaferRust(u)   0.33   74.17%   66.97%   100%    296     2.63    4,512
                                                                                                     C2SaferRust(f)   0.32   80.33%   75.85%   100%    305     2.51    3,765
effectively reduces the unsafe Rust constructs than its counterpart                                    EvoC2Rust      0.24   58.90%   58.90%    0%      -      1.02    3,220
                                                                                                         LAC2R                                 100%            16.27   37,920
during translation without sacrificing 𝐹𝑅𝑅 or 𝑇 𝑃𝑅. Table 3 also                                                      0.50   96.80%   93.61%           186


                                                                                  7
Conference’17, July 2017, Washington, DC, USA                                                                                                               Trovato et al.


where the LLM does not leverage Rust’s automatic dereferencing                                  covers specific features of the C language and the more challeng-
mechanism when translating C-style unsafe code to safe Rust, and                                ing aspects of translating C. P00_perlin_noise is a single larger,
instead emits explicit dereference operations in otherwise safe code.                           project-scale program. In total, these subsets contain 2,620 lines
These warnings are not part of the five categories of unsafe con-                               of code for B01_organic, 3,562 for B01_synthetic, and 512 for
structs. Rather, they occur in safe but non-idiomatic Rust. Moreover,                           P00_perlin_noise, for an overall total of 6,694 lines of code. For
C2SaferRust(U) yields more linter warnings than C2Rust, driven                                  C2SaferRust and LAC2R, we provide TRACTOR test cases during
by 417 instances of the "unnecessary unsafe block" warning, indi-                               translation, since both methods are built to support test-guided
cating the insertion of redundant unsafe blocks.                                                refinement. RustAssure and EvoC2Rust are evaluated using their
                                                                                                default pipelines, which do not consume test-vector feedback dur-
Table 3: Comparative results on Laertes benchmarks in detail.                                   ing translation. RustAssure keeps improving the translations by
C2SaferRust(U) and C2SaferRust(F) denote two versions                                           feeding compiler error messages back to the LLM and, once the
of C2SaferRust: the former uses unit-wise decomposition,                                        code compiles, runs symbolic tests on both versions to ensure be-
and the latter employs function-wise decomposition. Bold                                        havioral equivalence between the original C and the resulting Rust
highlights the best performance across the approaches.                                          code. On the other hand, EvoC2Rust fixes errors by relying on
                                                                                                the compiler, using its feedback alongside static analysis to gen-
  Benchmark                                        Project       Linter    Ave.    Ave.         erate possible patches and keep adjusting them, without needing
                   Methods       SR      FCR
    (LoC)                                        Compilability   Warns    Query   Tokens
                                                                                                pre-written tests to validate changes. For SACTOR, we skip tests
                    C2Rust         0       -          ✓           458       -        -
     bzip2
                C2SaferRust(u)   0.23   61.75%        ✓           813     2.75    9,749         during translation to evaluate both library and executable forms
                C2SaferRust(f)   0.35   62.50%        ✓           442     2.91    11,452
    (43,374)
                  EvoC2Rust      0.33   79.50%        ×            -      1.01    3,271         the same way, since SACTOR’s verification setup isn’t compatible
                    LAC2R                                         544     18.99   85,380
                                 0.70   85.16%        ✓
                                                                                                with how TRACTOR handles library testing. The choice of the LLM
                    C2Rust         0       -          ✓           114       -         -
    genann
                C2SaferRust(u)   0.31   62.86%        ✓           129     2.27     5,473        used varies across methods and affects performance. C2SaferRust,
                C2SaferRust(f)   0.31   59.38%        ✓           142     2.89     13,185
    (2,084)
                  EvoC2Rust      0.72   63.00%        ×            -      1.02     4,482        EvoC2Rust, SACTOR, and RustAssure all rely on GPT-4o, while
                    LAC2R        0.61                                     19.33   105,465
                                        93.75%        ✓           113
                                                                                                in our LAC2R work, we leverage both DeepSeek-V3 and GPT-4o.
                    C2rust         0       -          ✓           419       -        -
       lil
                C2SaferRust(u)   0.06   27.50%        ✓           390     2.93    5,976            We first evaluated the original C2Rust translations on the same
                C2SaferRust(f)   0.20   35.00%        ✓           442     3.25    8,067
    (5,400)
                  EvoC2Rust      0.06   27.10%        ×            -      1.03    4,899         124 programs as a baseline, and we computed 𝑃𝐶𝑅 and 𝑃𝑃𝑅 over
                    LAC2R                                                 22.09   78,088
                                 0.30   74.38%        ✓           221
                                                                                                this full set instead of only counting the ones that compiled. These
                    C2Rust         0       -          ✓           94        -         -
   urlparser
                C2SaferRust(u)   0.20   52.00%        ✓           93      3.08     8,400        translations achieved 100% compile and test pass rates under the
                C2SaferRust(f)   0.34   50.00%        ✓           64      3.45     13,772
    (1,118)
                  EvoC2Rust      0.83   85.7%         ×            -      1.00     4,267        TRACTOR evaluation harness. C2SaferRust and LAC2R matched
                    LAC2R        0.50   81.81%                            17.33   122,033
                                                      ✓           63
                                                                                                this on both metrics. This is expected, since both methods start
                    C2Rust         0       -          ✓           45        -        -
     grabc
                C2SaferRust(u)   0.19   71.43%        ✓           35      2.40    8,272         from C2Rust translations and refine them incrementally, so they
                C2SaferRust(f)   0.20   71.43%        ✓           36      2.60    3,744
    (1,046)
                  EvoC2Rust      0.70   45.8%         ×            -      1.00    3,854         can always fall back on the original if a chunk fails.
                    LAC2R        0.61    100%         ✓           24      22.00   56,913
                                                                                                   Table 4 demonstrates that LAC2R is the only method that achieves
                    C2Rust         0       -          ✓           806       -        -
     tulip-     C2SaferRust(u)   0.13   81.82%        ✓           574     2.75    13,239        the highest safety ratio (0.95), perfect project-level correctness (100%
   indicators   C2SaferRust(f)   0.11   81.20%        ✓           608     2.38    7,263
    (44,486)      EvoC2Rust      0.54    71.9%        ×            -      1.06    4,367         𝑃𝐶𝑅 and 100% 𝑃𝑃𝑅), and the fewest linter warnings (439) on TRAC-
                    LAC2R        0.23   91.03%        ✓           591     15.41   60,995
                                                                                                TOR Public-Tests, whereas every other method fails to achieve
                    C2Rust         0       -          ✓          5270       -         -
    optipng
                C2SaferRust(u)   0.45   50.41%        ✓          7,184    2.34     4,355        parity on at least one metric. These results reveal two distinct gaps.
                C2SaferRust(f)   0.11   48.78%        ✓          5164     2.75     10,361
    (95,560)
                  EvoC2Rust      0.90    64.8%        ×            -      1.73     5,733        First, methods that do not incorporate test-run feedback, namely
                    LAC2R        0.33   89.57%        ✓          3,609    21.47   118,386
                    C2Rust         0       -          ✓            5        -        -
                                                                                                RustAssure (2.4% 𝑃𝑃𝑅) and EvoC2Rust (18% 𝑃𝑃𝑅), substantially
     qsort
                C2SaferRust(u)   0.72   66.67%        ✓            4      2.50    3,442         underperform relative to the perfect correctness attained by LAC2R
                C2SaferRust(f)    1      100%         ✓            1      1.67    1,552
      (41)
                  EvoC2Rust      1.00    100%         ×            -      1.00    5,107         and C2SaferRust, which both integrate test run feedback. This
                    LAC2R         1      100%         ✓            0      15.00   22,534
                    C2Rust         0       -          ✓           268       -         -
                                                                                                finding confirms that compiler feedback alone is insufficient to
   snudown
                C2SaferRust(u)   0.16   34.26%        ✓           294     3.19     11,613       detect semantic discrepancies between a translation that merely
                C2SaferRust(f)   0.13   34.78%        ✓           241     3.34     10,378
    (6,521)
                  EvoC2Rust      0.63   68.6%         ×            -      1.03     4,559        compiles and one that is functionally equivalent to the original C
                    LAC2R        0.38   67.39%        ✓           186     24.55   107,903
                    C2Rust         0       -          ✓           99        -         -
                                                                                                code. Second, among the methods that incorporate test-run feed-
    xzoom
                C2SaferRust(u)   0.14   57.69%        ✓           93      2.87     9,350        back, LAC2R attains a higher 𝑆𝑅 (0.95) than C2SaferRust (0.88)
                C2SaferRust(f)   0.14   63.64%        ✓           92      2.71     13,614
    (2,524)
                  EvoC2Rust      0.95   64.00%        ×            -      1.02     3,072        while maintaining equivalent correctness, with C2SaferRust also
                    LAC2R        0.72    100%         ✓           64      23.64   108,709
   Average          C2Rust         0       -          ✓          757.80     -        -
                                                                                                exhibiting inferior code quality. This additional gain in safety and
                C2SaferRust(u)   0.26   56.63%        ✓          960.90   2.70    7,987         code quality is attributable to LAC2R’s MCTS-based search: the
                C2SaferRust(f)   0.29   60.67%        ✓          724.40   2.79    9,339
                  EvoC2Rust      0.75    65.8%        ×            -      1.07    4,354         safety-aware reward in Algorithm 2 directs tree exploration toward
                    LAC2R        0.54   88.30%        ✓          541.50   19.98   86,641
                                                                                                translations with fewer unsafe constructs, thereby surpassing what
                                                                                                iterative refinement alone can achieve. The primary tradeoff of
   Comparative Evaluation on small-scale Benchmarks. Ta-                                        LAC2R is inference cost, as it requires the most queries and, to-
ble 4 breaks down the results on the TRACTOR benchmark for                                      gether with EvoC2Rust, ranks among the most token intensive
three subsets of the Public-Tests dataset: B01_organic (38 cases),                              methods.
B01_synthetic (85 cases), and P00_perlin_noise (1 case). Each                                      The Effectiveness of Heterogeneous LLMs. Leveraging het-
covers a different kind of input. B01_organic includes programs                                 erogeneous LLMs is based on the expectation that diverse code
drawn from real codebases that rely on external libraries. B01_synthetic
                                                                                            8
Search-Based Multi-Trajectory Refinement for Safe C-to-Rust Translation with Large Language Models                                                      Conference’17, July 2017, Washington, DC, USA


Table 4: Comparative results on the TRACTOR Public-Tests.                                                                   whose full definitions were absent from the prompt. Without these
Bold highlights the best performance across the approaches.                                                                 structural facts, LAC2R cannot determine field types, aliasing, or
                                                                                                                            lifetimes, and MCTS fails to find a safe refinement. Incorporating
                                                                               Linter       Ave.             Ave.
        Dataset                 Methods          SR         PCR        PPR
                                                                              Warnings     Queries          Tokens          richer structural context is an important future direction.
                                C2Rust             0        100%       100%     14,399           -                -
 TRACTOR Public-Tests
                            C2SaferRust(u)       0.88       100%       100%     13,727         5.24            6,652
                               SACTOR             0.8        83%        63%      3,064         6.54            10,092
                              EvoC2Rust          0.04        42%        18%     49,316         14.74           53,249
                             RustAssure          0.72        74%       2.4%      1,026         7.86            7,254
                                LAC2R            0.95       100%       100%       439           25             51,788




refinements produced by different LLMs have complementary ef-
fects leading to improved translation. To evaluate this hypothe-
sis, we compared three variants of LAC2R, such as LAC2R using
GPT-4o only, LAC2R using Deepseek V3 only, and the proposed
LAC2R using heterogeneous LLMs. Table 5 shows that LAC2R us-
ing heterogeneous LLMs outperforms both variants regardless of                                                              Figure 9: Function Replacement Rates (𝐹𝑅𝑅) across the
which individual LLM is used. It implies that the LLM heterogeneity                                                         function-length distribution of the GNU coreutils.
contributes to consistent performance improvement. However, as
shown in Table 5, the heterogeneous LLMs incurs high cost in terms
of LLM tokens and queries.

Table 5: The evaluation of LAC2R’s heterogeneous LLMs on
coreutils. Three variants of LAC2R, such as LAC2R using
GPT-4o only, LAC2R using Deepseek V3 only, and the pro-
posed LAC2R using heterogeneous LLMs are compared.
                                                                                                                                 Figure 10: Failure case 1 of tail on GNU coreutils.
  Benchmark                                        Ave.             Ave.                                Linter
                      Methods         Safety                                   FRR       TPR
    (LoC)                                         Queries          Tokens                              Warnings
     split         LAC2R (GPT-4o)         0.29     14.78          31,168.08   86.47%     100%            293
   (13848)        LAC2R (Deepseek)        0.31     20.98          40,134.07   80.68%     100%            305
     pwd           LAC2R (GPT-4o)         0.75     15.38          38,000.59   94.48%     100%            98
    (5859)        LAC2R (Deepseek)        0.46     16.83          33,315.71   90.55%     100%            182
      cat          LAC2R (GPT-4o)         0.44     13.92          27,796.37   93.97%     100%            173
    (7460)        LAC2R (Deepseek)        0.40     14.23          25,934.54   89.75%     100%            187
   truncate        LAC2R (GPT-4o)         0.43     14.76          31,949.39   90.32%     100%            201
    (7181)        LAC2R (Deepseek)        0.25     16.88           32,916.3   90.32%     100%            192
     uniq          LAC2R (GPT-4o)         0.35      15.4          29,458.98   92.21%     100%            224
    (8299)        LAC2R (Deepseek)        0.33     16.61          32,671.07   89.22%     100%            238
     tail          LAC2R (GPT-4o)         0.56     15.41          42861.54    88.34%     100%            189
   (14423)        LAC2R (Deepseek)        0.48     16.25          36,371.38   88.68%     100%            261
     head          LAC2R (GPT-4o)         0.55     15.65          39,706.32   91.50%     100%            195
    (8047)        LAC2R (Deepseek)        0.50     15.77          38,414.13   86.92%     100%            190
                   LAC2R (GPT-4o )    0.4945       15.04       34,420.17      91.04%     100%           196.14
  Average
                  LAC2R (Deepseek)    0.3927       16.79       34,251.02      88.01%     100%           222.14
                   LAC2R (Hetero.)     0.50        16.27       37,920.17      93.61%     100%           186.57


                                                                                                                                 Figure 11: Failure case 2 of tail on GNU coreutils.
3.3          Limitations
The seven coreutils benchmarks include 1,210 functions, which can
be classified using their LoCs. As Figure 9 shows, most functions are                                                       4   Discussion
0-50 LoC long and LAC2R’s 𝐹𝑅𝑅 for the functions is 97% whereas                                                              LLM Cost. MCTS-based search substantially increases LLM in-
C2SaferRust’s 𝐹 𝑅𝑅 are around 80%. As the function length in-                                                               ference costs relative to single-trajectory refinement: LAC2R con-
creases, the 𝐹 𝑅𝑅 of all methods decrease. The trend suggests that                                                          sumes on average 6–9× more queries and tokens per function than
LLMs struggle to comprehend and translate the entire context of                                                             C2SaferRust (Tables 2 and 3), as each tree expansion requires a full
such lengthy functions.                                                                                                     LLM call for code refinement followed by compilation and test vali-
   Figure 10 shows an unsafe Rust function ximalloc (<50 LoC)                                                               dation. Two complementary strategies can mitigate this overhead.
from tail, where LAC2R failed to refine. Its body invokes external                                                          At the tree level, heuristic pruning [23] and rollout-free MCTS [26]
functions whose signatures and behavioral contracts are unavail-                                                            can limit redundant node expansions without degrading solution
able in the prompt context, preventing LAC2R from determining                                                               quality. At the inference level, token-budget-aware reasoning [11]
ownership semantics; MCTS thus fails to find a safe, compilable                                                             can dynamically cap generation length per call, reducing per-query
refinement within the search budget.                                                                                        cost while preserving output quality. Integrating these techniques
   Figure 11 shows a failure where the target function depends on                                                           into LAC2R’s MCTS structure is a promising direction for reducing
the precise layout and invariants of Hash_table and Hash_tuning,                                                            inference overhead while retaining its safety gains.
                                                                                                                        9
Conference’17, July 2017, Washington, DC, USA                                                                                                                    Trovato et al.


               Table 6: LLM-based approaches for C-to-Rust translation. Bold highlights the distinct feature of LAC2R.

                                                                       Validator
   Name            Translation strategy                                                                Code analyzer                          Preprocessor
                                                                       (success check)
   VERT            Oracle-guided iterative translation                 Bolero [4], Kani [16]           Generating an oracle Rust using Wasm                  -
                   Iterative translation validated by cross-language
   Flourine                                                            fuzzing-based                   Fuzzing                                               -
                   differential fuzzing
   SpecTra         Specification-augmented translation                 using test cases                Generating specification                              -
                                                                                                       Dynamic analysis
   Syzygy          Dynamic analysis-guided iterative refinement        fuzzing-based                                                          Decomposition
                                                                                                       Fuzzing
   C2SaferRust     Iterative refinement of C2Rust output               using test cases                Static analysis                        Decomposition, C2Rust
   SACTOR          Iterative refinement with two-step translation      using test cases                Static analysis                        Decomposition
   SafeTrans       Iterative refinement with few-shot learning         using test cases                                   -                                  -
                   Context-aware function-level decomposition
   LLMigrate                                                           Manual test                     Static analysis                        Decomposition, C2Rust
                   and assembly
                                                                                                       Feature mapping
   EvoC2Rust       Skeleton-guided iterative translation               using test cases                                                       Skeleton construction
                                                                                                       Static analysis
                                                                                                                                              header file preprocessor
                   Iterative translation guided by function-level
   RustAssure                                                          Differential symbolic testing   -                                      struct transpiler
                   semantic equivalence validation
                                                                                                                                              struct field usage analyzer
                   Predefined workflow-based multi-agent                                                                                      Decomposition
   Rustify                                                             using test cases                Static analysis
                   iterative translation                                                                                                      Node merging heuristic
                   Dependency-guided scaffolding                                                                                              Project-scaffolding
   RustMap                                                             using test cases                Static and dynamic analysis
                   for project-scale translation                                                                                              C preprocessor
   LAC2R (ours)    MCTS-based structural refinement                    using test cases                Static analysis                        Decomposition, C2Rust



Correctness Checks. LAC2R relies on test case-based equivalence                               5   Related Work
checks, consistent with recent approaches [19, 33]. While conve-                              Verified Equivalent Rust Transpilation (VERT) combines a rule-
nient and scalable, test-based validation is bounded by the represen-                         based transpilation path with an LLM-generated code candidate [31].
tativeness of the test suite: passing all provided tests does not guar-                       VERT compiles the C program to WebAssembly and lifts it to Rust
antee semantic equivalence on unseen inputs, as our TRACTOR                                   using rWasm, producing a semantically correct but often non-
results confirm (Table 4). Fuzzing-based differential checks [12]                             idiomatic oracle reference, against which LLM-generated candi-
can complement this by exploring inputs beyond the fixed test                                 dates are verified through property-based testing and formal model
suite, though they depend on harness quality and seed corpus                                  checking. Flourine proposed cross-language differential fuzzing
diversity. Symbolic validation [31] offers stronger path-level guar-                          to compare the I/O behavior of source and translated programs
antees but faces path explosion at the scale of real programs. Incor-                         without relying on pre-existing test cases [9]. SpecTra enhances
porating lightweight differential fuzzing into MCTS rollout scor-                             code translation by incorporating static specifications, input/output
ing—penalizing translations that fail on automatically generated                              test cases, and natural language descriptions individually into the
inputs—could improve correctness coverage without the scalabil-                               prompt to guide multi-candidate generation [20]. Syzygy combines
ity penalty of full symbolic verification, and represents a natural                           LLMs with dynamic analysis to extract semantic information such
extension of LAC2R.                                                                           as aliasing behavior and heap allocation sizes for iterative refine-
Benchmark Suite. We evaluate on the seven coreutil and ten                                    ment of real-world libraries [24]. C2SaferRust initiates transla-
Laertes benchmarks, the largest program-level, real-world suites                              tion from C2Rust output and applies slice-wise iterative refine-
currently used in this domain [19], supplemented by TRACTOR                                   ment driven by static analysis [19]. SACTOR introduces a two-step
Public-Tests as a small-scale benchmark. As Table 1 shows, prior                              pipeline of unidiomatic and idiomatic conversions, where static
works have relied on heterogeneous benchmark sets with lim-                                   analysis informs the LLM about pointer semantics and code depen-
ited overlap, making cross-method comparison difficult. CRUST-                                dencies in both stages [33]. SafeTrans employs few-shot guided re-
Bench [17], a recently introduced dataset of 100 C repositories                               pair by supplying the LLM with contextual information and related
paired with manually-written Rust function signatures and test                                code snippets, and evaluates whether potential C vulnerabilities are
cases, is a promising candidate for a unified evaluation platform.                            properly resolved in the translated Rust [10]. LLMigrate addresses
Standardizing on such a benchmark and extending coverage to                                   the laziness problem—where LLMs omit significant portions of a
larger programs would enable more rigorous comparison across                                  target code during translation—through function-level decomposi-
the rapidly growing set of C-to-Rust translation methods.                                     tion and static analysis [18]. EvoC2Rust augments an LLM with
                                                                                              safety-preserving mappings between the core linguistic features of
                                                                                              C and Rust, constructing a compilable skeleton and incrementally
                                                                                              translating individual functions to enable project-scale translation

                                                                                         10
Search-Based Multi-Trajectory Refinement for Safe C-to-Rust Translation with Large Language Models                                 Conference’17, July 2017, Washington, DC, USA


without conventional transpiler preprocessing [29]. RustAssure                                     project-scale c-to-rust migration via program analysis and llm. In International
performs iterative translation guided by function-level semantic                                   Conference on Engineering of Complex Computer Systems. Springer, 283–302.
                                                                                               [6] DARPA TRACTOR Program. 2026. PUBLIC Test Corpus. https://github.com/
equivalence validation using differential symbolic testing, with                                   DARPA-TRACTOR-Program/PUBLIC-Test-Corpus. Accessed: 2026-03-26.
dedicated preprocessors for header files, structs, and struct field us-                        [7] DeepSeek-AI. 2024. DeepSeek-V3 Technical Report. arXiv:2412.19437 [cs.CL]
                                                                                                   doi:10.48550/arXiv.2412.19437 arXiv:2412.19437.
ages [2]. Rustify employs a predefined workflow-based multi-agent                              [8] Mehmet Emre, Ryan Schroeder, Kyle Dewey, and Ben Hardekopf. 2021. Translat-
framework that iteratively refines translations using static analy-                                ing C to safer Rust. Proc. ACM Program. Lang. 5, OOPSLA, Article 121 (oct 2021),
sis and a node-merging heuristic for function decomposition [28].                                  29 pages. doi:10.1145/3485498
                                                                                               [9] Hasan Ferit Eniser, Hanliang Zhang, Cristina David, Meng Wang, Maria Chris-
RustMap adopts dependency-guided scaffolding for project-scale                                     takis, Brandon Paulsen, Joey Dodds, and Daniel Kroening. 2024. Towards
translation, leveraging both static and dynamic analysis along with                                Translating Real-World Code with LLMs: A Study of Translating to Rust.
a C preprocessor [5].                                                                              arXiv:2405.11514 [cs.SE] https://arxiv.org/abs/2405.11514
                                                                                              [10] Muhammad Farrukh, Smeet Shah, Baris Coskun, and Michalis Polychron-
   These existing methods share a similar execution flow at a high-                                akis. 2025.        SafeTrans: LLM-assisted Transpilation from C to Rust.
level as illustrated in Figure 1, and all rely on iterative code re-                               arXiv:2505.10708 [cs.CR] https://arxiv.org/abs/2505.10708
                                                                                              [11] Tingxu Han, Zhenting Wang, Chunrong Fang, Shiyu Zhao, Shiqing
finement along a single search trajectory. Their detailed structural                               Ma, and Zhenyu Chen. 2025.              Token-Budget-Aware LLM Reasoning.
distinctions are summarized in Table 6. In contrast, LAC2R formu-                                  arXiv:2412.18547 [cs.CL] https://arxiv.org/abs/2412.18547
lates C-to-Rust translation as a sequential decision-making problem                           [12] Adrian Herrera, Hendra Gunadi, Shane Magrath, Michael Norrish, Mathias Payer,
                                                                                                   and Antony L. Hosking. 2021. Seed selection for successful fuzzing. In Proceed-
and employs MCTS to systematically explore multiple refinement                                     ings of the 30th ACM SIGSOFT International Symposium on Software Testing and
trajectories, enabling principled exploration–exploitation balance                                 Analysis (Virtual, Denmark) (ISSTA 2021). Association for Computing Machinery,
via UCT-guided search.                                                                             New York, NY, USA, 230–243. doi:10.1145/3460319.3464795
                                                                                              [13] The White House. 2024. Back to the Building Blocks: A Path toward Secure
                                                                                                   and Measurable Software. https://bidenwhitehouse.archives.gov/wp-content/
                                                                                                   uploads/2024/02/Final-ONCD-Technical-Report.pdf.
6    Conclusion                                                                               [14] The White House. 2024.           National Cybersecurity Strategy Implementa-
To address the challenges of C-to-Rust code translation leveraging                                 tion Plan. https://bidenwhitehouse.archives.gov/wp-content/uploads/2024/05/
                                                                                                   National-Cybersecurity-Strategy-Implementation-Plan-Version-2.pdf.
emerging LLM capabilities, we introduced an MCTS-Guided LLM                                   [15] Immunant, Inc. 2024. C2Rust Manual. https://c2rust.com/manual/.
refinement technique for code translation, LAC2R. These efforts are                           [16] Kani Developers. 2025. The Kani Rust Verifier. https://model-checking.github.
motivated by the observation that the intermediate steps required                                  io/kani/ Accessed: 2025-10-10.
                                                                                              [17] Anirudh Khatry, Robert Zhang, Jia Pan, Ziteng Wang, Qiaochu Chen, Greg
for C-to-Rust are not well-defined and there is limited study on how                               Durrett, and Isil Dillig. 2025. CRUST-Bench: A Comprehensive Benchmark for
to organize these intermediate steps to construct a correct trans-                                 C-to-safe-Rust Transpilation. arXiv:2504.15254 [cs.SE] https://arxiv.org/abs/
                                                                                                   2504.15254
lation trajectory. LAC2R systematically organizes LLM-generated                               [18] Yuchen Liu, Junhao Hu, Yingdi Shan, Ge Li, Yanzhen Zou, Yihong Dong, and Tao
intermediate steps and improves the possibility of producing a cor-                                Xie. 2025. LLMigrate: Transforming "Lazy" Large Language Models into Efficient
rect translation. Our experimental evaluation on two large-scale,                                  Source Code Migrators. arXiv:2503.23791 [cs.PL] https://arxiv.org/abs/2503.23791
                                                                                              [19] Vikram Nitin, Rahul Krishna, Luiz Lemos do Valle, and Baishakhi Ray. 2025.
real-world datasets and a small-scale benchmark demonstrates that                                  C2SaferRust: Transforming C Projects into Safer Rust with NeuroSymbolic Tech-
LAC2R outperforms its counterparts across several metrics, indi-                                   niques. arXiv:2501.14257 [cs.SE] https://arxiv.org/abs/2501.14257
cating a high likelihood of safe translation.                                                 [20] Vikram Nitin, Rahul Krishna, and Baishakhi Ray. 2024. SpecTra: Enhancing
                                                                                                   the Code Translation Ability of Language Models by Generating Multi-Modal
                                                                                                   Specifications. arXiv:2405.18574 [cs.SE] https://arxiv.org/abs/2405.18574
                                                                                              [21] Zhenting Qi, Mingyuan Ma, Jiahang Xu, Li Lyna Zhang, Fan Yang, and Mao
Data-Availability Statement                                                                        Yang. 2024. Mutual Reasoning Makes Smaller LLMs Stronger Problem-Solvers.
The GNU coreutils benchmark originates from the GNU Project                                        arXiv:2408.06195 [cs.CL] https://arxiv.org/abs/2408.06195
                                                                                              [22] Rust Project Developers. 2024. Clippy (rust-clippy). https://github.com/rust-
(https://www.gnu.org/software/coreutils/). The Laertes benchmark                                   lang/rust-clippy
suite is publicly available at https://doi.org/10.5281/zenodo.5442253.                        [23] Julian Schrittwieser, Ioannis Antonoglou, Thomas Hubert, Karen Simonyan,
The TRACTOR Public-Tests benchmark is available at https://github.                                 Laurent Sifre, Simon Schmitt, Arthur Guez, Edward Lockhart, Demis Hassabis,
                                                                                                   Thore Graepel, Timothy P. Lillicrap, and David Silver. 2019. Mastering Atari, Go,
com/DARPA-TRACTOR-Program/PUBLIC-Test-Corpus. The ex-                                              Chess and Shogi by Planning with a Learned Model. CoRR abs/1911.08265 (2019).
perimental scripts and tool accompanying this paper are available                                  arXiv:1911.08265 http://arxiv.org/abs/1911.08265
                                                                                              [24] Manish Shetty, Naman Jain, Adwait Godbole, Sanjit A. Seshia, and Koushik Sen.
at https://doi.org/10.5281/zenodo.19247427.                                                        2024. Syzygy: Dual Code-Test C to (safe) Rust Translation using LLMs and
                                                                                                   Dynamic Analysis. arXiv:2412.14234 [cs.SE] https://arxiv.org/abs/2412.14234
                                                                                              [25] Jeff Vander Stoep and Chong Zhang. 2019. Queue the Hardening Enhancements.
References                                                                                         https://security.googleblog.com/2019/05/queue-hardening-enhancements.html.
 [1] Asma Ben Abacha, Wen wai Yim, Yujuan Fu, Zhaoyi Sun, Meliha Yetisgen, Fei                [26] Maciej Swiechowski, Konrad Godlewski, Bartosz Sawicki, and Jacek Mandziuk.
     Xia, and Thomas Lin. 2025. MEDEC: A Benchmark for Medical Error Detection                     2021. Monte Carlo Tree Search: A Review of Recent Modifications and Applica-
     and Correction in Clinical Notes. arXiv:2412.19260 [cs.CL] https://arxiv.org/abs/             tions. CoRR abs/2103.04931 (2021). arXiv:2103.04931 https://arxiv.org/abs/2103.
     2412.19260                                                                                    04931
 [2] Yubo Bai and Tapti Palit. 2025. RustAssure: Differential Symbolic Testing for            [27] Microsoft MSRC Team. 2019. We need a safer systems programming lan-
     LLM-Transpiled C-to-Rust Code. In 2025 40th IEEE/ACM International Conference                 guage. https://msrc.microsoft.com/blog/2019/07/we-need-a-safer-systems-
     on Automated Software Engineering (ASE). 534–546. doi:10.1109/ASE63991.2025.                  programming-language/.
     00051                                                                                    [28] Chen Wang, Yujun Huang, Peng Li, Lina Gong, and Fei Wu. 2026. Rustify:
 [3] Cameron B. Browne, Edward Powley, Daniel Whitehouse, Simon M. Lucas, Pe-                      Towards Repository-Level C to Safer Rust via Workflow-Guided Multi-Agent
     ter I. Cowling, Philipp Rohlfshagen, Stephen Tavener, Diego Perez, Spyridon                   Transpiler. https://openreview.net/forum?id=tjZHVvgmZt
     Samothrakis, and Simon Colton. 2012. A Survey of Monte Carlo Tree Search                 [29] Chaofan Wang, Tingrui Yu, Jie Wang, Dong Chen, Wenrui Zhang, Yuling
     Methods. IEEE Transactions on Computational Intelligence and AI in Games 4, 1                 Shi, Xiaodong Gu, and Beijun Shen. 2025. EVOC2RUST: A Skeleton-guided
     (2012), 1–43. doi:10.1109/TCIAIG.2012.2186810                                                 Framework for Project-Level C-to-Rust Translation. arXiv:2508.04295 [cs.SE]
 [4] Cameron Bytheway. 2024. Bolero Book: Fuzzing and Property Testing for Rust.                   https://arxiv.org/abs/2508.04295
     https://camshaft.github.io/bolero/ Accessed: 2025-10-10.                                 [30] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei
 [5] Xuemeng Cai, Jiakun Liu, Xiping Huang, Yijun Yu, Haitao Wu, Chunmiao Li,                      Xia, Ed H. Chi, Quoc V. Le, and Denny Zhou. 2022. Chain-of-thought prompting
     Bo Wang, Imam Nur Bani Yusuf, and Lingxiao Jiang. 2025. Rustmap: Towards                      elicits reasoning in large language models. In Proceedings of the 36th International
                                                                                         11
Conference’17, July 2017, Washington, DC, USA                                                                                                                     Trovato et al.


     Conference on Neural Information Processing Systems (New Orleans, LA, USA)                 Reasoning to Language Agents. ACM Comput. Surv. 57, 8, Article 206 (March
     (NIPS ’22). Curran Associates Inc., Red Hook, NY, USA, Article 1800, 14 pages.             2025), 39 pages. doi:10.1145/3719341
[31] Aidan Z. H. Yang, Yoshiki Takashima, Brandon Paulsen, Josiah Dodds, and               [33] Tianyang Zhou, Haowen Lin, Somesh Jha, Mihai Christodorescu, Kirill Levchenko,
     Daniel Kroening. 2024. VERT: Verified Equivalent Rust Transpilation with                   and Varun Chandrasekaran. 2025. LLM-Driven Multi-step Translation from C to
     Large Language Models as Few-Shot Learners. arXiv:2404.18852 [cs.PL] https:                Rust using Static Analysis. arXiv:2503.12511 [cs.SE] https://arxiv.org/abs/2503.
     //arxiv.org/abs/2404.18852                                                                 12511
[32] Zhuosheng Zhang, Yao Yao, Aston Zhang, Xiangru Tang, Xinbei Ma, Zhiwei He,
     Yiming Wang, Mark Gerstein, Rui Wang, Gongshen Liu, and Hai Zhao. 2025.               Received 20 February 2007; revised 12 March 2009; accepted 5 June 2009
     Igniting Language Intelligence: The Hitchhiker’s Guide from Chain-of-Thought




                                                                                      12
