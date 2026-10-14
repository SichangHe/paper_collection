                                                  Towards Certificate-Driven Software Porting:
                                                      A Self-Improving Agentic Harness
                                                     for Scientific Program Optimization


                                                                 Piyush Jha1,2          Aishik Ghosh2,3            Vijay Ganesh1
                                                          1
                                                        School of Computer Science, Georgia Institute of Technology, USA
arXiv:2609.34069v1 [cs.AI] 28 Sep 2026




                                                            2
                                                              School of Physics, Georgia Institute of Technology, USA
                                                                 3
                                                                   Lawrence Berkeley National Laboratory, USA
                                                    piyush.jha@gatech.edu, aishikghosh@physics.gatech.edu,
                                                                           vganesh@gatech.edu



                                                                                            Abstract

                                                   The upgrade and rewriting of large scientific codebases has traditionally been a
                                                   major challenge. While evolutionary search with large language models (LLMs)
                                                   can port and accelerate legacy code, repair feedback in prompts alone does not
                                                   prevent subsequent candidates from repeating the same errors. We introduce
                                                   Certificate-Driven Evolutionary Search (CDES), which extends evolutionary search
                                                   with enforceable restrictions derived from failed candidates, recorded as certificates
                                                   of assumptions, checker evidence, and justified restrictions. Its control logic
                                                   enforces these restrictions through rejection, backtracking, and targeted repair
                                                   while preserving compatible edits. We apply CDES to CPU-to-GPU translation of
                                                   two particle-simulation functions from the Geant4 toolkit, evaluated with a harness
                                                   that goes beyond unit tests to combine formal checks, numerical comparisons,
                                                   physics checks, and GPU safety tests. Generated implementations achieve 13.78×
                                                   and 23.54× function-level speedups over CPU code, including data conversion
                                                   and transfers; for one function, GPU throughput exceeds an expert implementation
                                                   by 14.9%, reaching 16.1% when complementary components are combined. In
                                                   an ablation over execution settings, certificate feedback increases the fraction of
                                                   candidates passing required correctness checks from 55% to 90%.


                                         1    Introduction

                                         Scientific software is often developed and extended by the community over several decades, making
                                         it challenging to rewrite the entire codebase whenever new hardware acceleration paradigms emerge.
                                         Simulators are of particular interest because they consume a substantial amount of computational
                                         time, for instance in physics and astrophysics research [1–4]. There is therefore great interest in
                                         faster implementations of simulation software that preserve computational and physical specifica-
                                         tions. Geant4 is a particle simulation toolkit widely used for detector simulation in particle physics
                                         experiments and for applications in medical imaging [5–7]. While porting the entirety of Geant4
                                         to GPU-accelerated code is a herculean task, the Celeritas project has taken a significant step by
                                         designing expert-written GPU implementations for particle transport [8]. In this proof-of-concept
                                         study, we explore how automated optimization can complement these efforts by improving existing
                                         implementations and accelerating functions for which no expert-written GPU implementations exist.
                                         For this approach to scale to the entire codebase, we assume that selected functions can be optimized
                                         independently, and that speeding up individual components will reduce overall simulation time. We
                                         evaluate function-level performance here, leaving full-simulation gains to future work.

                                         Preprint. Submitted to the 9th Workshop on Machine Learning and the Physical Sciences (ML4PS 2026).
          AlphaEvolve-style core
                                             Programs + scores

             Seed                                                Relevant restrictions, program and harness feedback



              Program             Parent                                          Evaluation         Failures       Certificate
                                                     Mutator LLM
              database           selection                                         harness                          database


                                                                     Backtrack /
                                             Check                   Restart / Repair
          CDES additions
                                                                                    Retrieve certificates/restrictions
          Undo and targeted repair              Conflict checker and
          using certificates                          analyzer                          Propose new restrictions




Figure 1. CDES extends evolutionary search with certificate-driven control. The certificate database
supplies restrictions and feedback to the mutator LLM and evidence to the conflict checker and
analyzer. CDES enforces validated restrictions during generation and repair. Gold highlights CDES
additions.


CDES builds on state-of-the-art evolutionary program search, where systems such as FunSearch,
AlphaEvolve, ERA, and MadEvolve repeatedly generate, evaluate, and select programs [9–12]. Our
focus is on how information from failed candidates can be converted into enforceable restrictions on
subsequent search. The certificate database provides feedback to the mutator LLM, but CDES does
not rely on prompt compliance alone. Its control logic separately enforces validated restrictions on
candidate choices, rejecting conflicting choices and guiding the repair process. This design works with
frontier LLMs through API calls and requires neither access to model weights nor additional training.
It draws on symbolic feedback in RLSF [13], constrained reinforcement learning in CDRL [14], and
conflict learning for program construction in Neo [15].
We make two contributions. First, a certificate-driven evolutionary search mechanism converts
conflicts into verified restrictions and enforces them through targeted rejection and repair while
preserving compatible changes. Second, a scientific optimization and evaluation harness integrates
this mechanism with tool selection and correctness checks to translate CPU programs into CUDA,
NVIDIA’s GPU programming platform. The search is self-improving because accumulated certificates
change which future modifications are permitted, without retraining the LLM.


2   Certificate-Driven Evolutionary Search

CDES extends an AlphaEvolve-style core implemented with ShinkaEvolve [16] (Figure 1). A seed
initializes the program database. Parent selection chooses a stored program, and the mutator LLM
proposes code or execution settings. The evaluation harness returns programs and scores to the
program database and failures to the certificate database. CDES adds backtracking, restarting, and
targeted repair.
Detection and certification. The evaluation harness detects requirement violations. The conflict
checker and analyzer reviews unfinished candidates using stored certificates and symbolic checks of
dependencies between code components. A certificate records the conflicting choices, the violated
requirement, and supporting assumptions and evidence. Proposed restrictions are checked before
being used to block the same conflict in later candidates.
Undo and targeted repair. CDES control logic rejects conflicting combinations, adds required
components, and repairs choices while preserving compatible edits. Conflict-driven clause learning
(CDCL) SAT solvers determine whether Boolean choices satisfy logical constraints. They learn
restrictions from conflicts and backjump to earlier decisions [17]. CDES similarly backtracks, restarts,
or repairs candidates, without claiming that no solution exists. Unlike prompt feedback, validated
restrictions are enforced even when the LLM repeats a conflicting proposal.
Related ideas appear in program analysis and synthesis. Prior work uses program summaries and
simplified models to guide search [18, 19], identifies conditions under which rewrites preserve
behavior [20], and aligns states across program executions [21]. Other approaches check unfinished
programs [22] or infer properties preserved across loop iterations [23]. CDES draws on these


                                                            2
directions to guide tool requests and the construction of reusable restrictions, rather than implementing
each method directly.


3   Evaluation Harness

Geant4 source and specifications define expected behavior, with Celeritas as an expert performance
reference where available. An evaluator LLM selects and orders tools, while a fixed policy mandates
checks described below [24]. Each evaluation result records a hash identifying the exact candidate
source code tested. Failed or unresolved mandatory checks block acceptance and enter the certificate
database. Separate validation suites test additional workload sizes, fresh random-number sequences,
and inputs near numerical decision boundaries. Their results are withheld from the corresponding
search runs rather than used to guide proposals.
Formal analysis. The Lean package [25] verifies selected requirements, called contracts, rather
than whole-program equivalence. GPU assignment proofs ensure each input is processed exactly
once and retains its assigned random-sequence identifier. Restricted code generation translates
the GPU work-assignment rules checked in Lean into executable code. CBMC checks C array
indexing within bounded executions [26]. Physlib/HepLean and Mathlib provide reusable physics
and mathematics proofs [27–29]. Alive2 and VOLTA check code-fragment equivalence in separate
demonstrations [30, 31]. These guarantees cover selected requirements and fragments, not complete
GPU programs.
Execution-based validation. Differential tests compare reference and candidate outputs on matching
inputs within fixed numerical tolerances. Where contracts require, they also check exact output
counts and random-number consumption. Physics checks test conservation laws and valid output
ranges. Compute Sanitizer detects GPU memory-access and synchronization errors [32]. Statistical
tests compare selected output distributions from independent samples. Nsight Compute profiles GPU
execution [33]. Acceptance means passing required checks within their stated domains, not universal
program equivalence.


4   Experimental Design

We study two complementary Geant4 functions as case studies, translating CPU-only C++ functions
rather than the complete simulation. The Compton function computes particle energies and directions
after a photon scatters from an electron. The Fermi function assigns energy and motion to fragments
of an atomic nucleus. Optimization must satisfy the evaluation criteria in Section 3.
We chose Compton because Celeritas has an expert GPU implementation, and Fermi because, to
our knowledge, it has no matching GPU implementation already available. This lets us test both
improving on existing GPU code and generating GPU code where none is provided by Celeritas.
Celeritas therefore serves as our expert reference [8] for the first function. The Fermi case also reduces
reliance on a comparison where the LLM may have seen the Celeritas code during pretraining.
We benchmark the CPU reference, CDES-generated GPU code, and Celeritas where available,
using approximately 250,000 inputs on a 10 GB partition of an NVIDIA H100 GPU. Comparisons
within each table use matching inputs and test programs with repeated measurements. Table 1
sums separately measured data conversion, transfers, and GPU computation. CPU timings include
allocation, whereas GPU timings use preallocated buffers. Table 2 directly measures transfers and
computation in a shared benchmark with different supporting code and launch settings. Its GPU
buffers are also preallocated. Absolute times should therefore be compared within each table. Speedup
is reference time divided by generated-code time, and throughput is inputs processed per second.
Both tables exclude search and evaluation runtime. We use GPT-5.6-Sol with medium reasoning,
with total model-call costs under $10.


5   Results

Performance. CDES-generated GPU code achieves 13.78× and 23.54× speedups over the CPU
versions under the standalone timing protocol (Table 1). In the shared Compton benchmark, GPU


                                                    3
Table 1. Generated CUDA achieves 13.78× and 23.54× speedups over standalone CPU functions
under the stated timing protocol. Times are in milliseconds. GPU times sum separately measured
conversion, transfers, and computation, not full-simulation runtime.
                      Function   Geant4 CPU CDES-generated CUDA Speedup
                      Compton         30.162                        2.189    13.78×
                      Fermi          340.090                       14.447    23.54×


throughput is 14.9% higher than Celeritas, while execution time including transfers is approximately
3.0% lower (Table 2).
Optimization patterns. Generated code reuses earlier calculations and simplifies repeated work. In
Compton, it keeps a value that Celeritas computes inside a helper (Figure 2). In Fermi, it replaces
selected power calculations with multiplication, retaining the original calculation where rounding
could change a decision. Reported speedups measure complete functions, not individual changes.

Celeritas helper                                        CDES-generated code
// Compute from the cosine                              // Reuse an earlier calculation
costheta = 1 - t;                                       if (sint2 < 0) sint2 = 0;
sintheta = sqrt(1 - costheta*costheta);                 sinTeta = sqrt(sint2);

Figure 2. Avoiding repeated work in Compton. Celeritas computes the squared sine inside its helper.
CDES-generated code reuses this quantity from an earlier calculation. The conditional prevents a
negative input to the square root. Snippets are shortened.

Combining with Celeritas. We combine Celeritas’s code for selecting particle energies with our
code for calculating directions and writing outputs. This hybrid increases GPU throughput by 16.1%
over Celeritas (Table 2). It improves GPU throughput over our generated code by 1.2%, measured
as the median gain across six paired timing rounds, showing that the two implementations offer
complementary improvements and an opportunity for human–AI collaboration.

Table 2. Combining Celeritas components with generated code gives the highest GPU throughput.
Times are medians in milliseconds over six paired timing rounds. Throughput gains are medians
of per-round time ratios, not ratios of displayed median times. Execution time directly measures
transfers, computation, and completion waits in the shared benchmark. Settings are selected separately
for each timing metric. Celeritas and the hybrid use a shared direction correction.
                Version           Execution time GPU time          GPU throughput gain
                                                                  vs. Celeritas vs. CDES
                Celeritas                  2.4753        0.5093
                CDES-generated             2.4000        0.4433        14.9%
                Hybrid                     2.3905        0.4387        16.1%          1.2%

Ablation. We compare the evolutionary search with and without certificate feedback, using the same
correctness checks (Table 3). Certificates increase the fraction of proposals that compile and pass
these checks from 55% to 90%. The fraction of proposals that also improve throughput by over
10% increases from 50% to 80%. Search without certificates still produces useful candidates at
lower total API cost, while certificate feedback improves the passing rate and lowers cost per passing
proposal by 10.7%.

Table 3. Certificate feedback produces more proposals that pass correctness checks and improve
performance. Costs cover this ablation’s Qwen3-Coder-Plus calls.
                                                        Without certificates With certificates
             Proposals passing correctness checks                     55%                90%
             Passing with throughput gain > 10%                       50%                80%
             Passing with throughput gain > 20%                       30%                35%
             Best throughput gain on withheld inputs                66.5%              68.6%
             Model-call cost (USD)                                 $0.0535            $0.0782



                                                    4
6   Conclusion and Future Work
We present a proof-of-concept approach toward reliably and scalably porting large legacy scientific
codebases, demonstrated on two Geant4 functions while enforcing a flexible range of correctness
requirements. The generated code exhibits optimization patterns that improve on expert-written
implementations, and combining it with Celeritas components shows complementary benefits from
human–AI collaboration. CDES connects conflict detection, certificate validation, and enforced
search control for scientific optimization. Future work will test how the cost and correctness benefits
of certificates vary across functions and optimization difficulty, extend evaluation to larger portions
of Geant4, and incorporate requirements needed for projects such as Celeritas.

References
 [1] Georges Aad et al. AtlFast3: The Next Generation of Fast Simulation in ATLAS. Comput.
     Softw. Big Sci., 6(1):7, 2022. doi: 10.1007/s41781-021-00079-7.
 [2] Georges Aad et al. Deep Generative Models for Fast Photon Shower Simulation in ATLAS.
     Comput. Softw. Big Sci., 8(1):7, 2024. doi: 10.1007/s41781-023-00106-9.
 [3] Hao Xu, John H. Wise, Michael L. Norman, Kyungjin Ahn, and Brian W. O’Shea. Galaxy
     properties and uv escape fractions during the epoch of reionization: Results from the renaissance
     simulations. The Astrophysical Journal, 833(1):84, December 2016. ISSN 1538-4357. doi: 10.
     3847/1538-4357/833/1/84. URL http://dx.doi.org/10.3847/1538-4357/833/
     1/84.
 [4] Junze Liu, Aishik Ghosh, Dylan Smith, Pierre Baldi, and Daniel Whiteson. Generalizing to
     new geometries with Geometry-Aware Autoregressive Models (GAAMs) for fast calorimeter
     simulation. JINST, 18(11):P11003, 2023. doi: 10.1088/1748-0221/18/11/P11003.
 [5] S. Agostinelli et al. GEANT4 - A Simulation Toolkit. Nucl. Instrum. Meth. A, 506:250–
     303, 2003. doi: 10.1016/S0168-9002(03)01368-8. URL https://doi.org/10.1016/
     S0168-9002(03)01368-8.
 [6] J. Allison et al. Geant4 developments and applications. IEEE Trans. Nucl. Sci., 53:270, 2006. doi:
     10.1109/TNS.2006.869826. URL https://doi.org/10.1109/tns.2006.869826.
 [7] J. Allison et al. Recent developments in Geant4. Nucl. Instrum. Meth. A, 835:186–225, 2016.
     doi: 10.1016/j.nima.2016.06.125. URL https://doi.org/10.1016/j.nima.2016.
     06.125.
 [8] Seth R. Johnson et al. Celeritas: Accelerating Geant4 with GPUs. EPJ Web Conf., 295:
     11005, 2024. doi: 10.1051/epjconf/202429511005. URL https://doi.org/10.1051/
     epjconf/202429511005.
 [9] Bernardino Romera-Paredes, Mohammadamin Barekatain, Alexander Novikov, Matej Balog,
     M Pawan Kumar, Emilien Dupont, Francisco JR Ruiz, Jordan S Ellenberg, Pengming Wang,
     Omar Fawzi, et al. Mathematical discoveries from program search with large language models.
     Nature, 625(7995):468–475, 2024.
[10] Alexander Novikov, Ngân Vũ, Marvin Eisenberger, Emilien Dupont, Po-Sen Huang, Adam Zsolt
     Wagner, Sergey Shirobokov, Borislav Kozlovskii, Francisco J. R. Ruiz, Abbas Mehrabian,
     M. Pawan Kumar, Abigail See, Swarat Chaudhuri, George Holland, Alex Davies, Sebastian
     Nowozin, Pushmeet Kohli, and Matej Balog. AlphaEvolve: A coding agent for scientific and
     algorithmic discovery, 2025. URL https://arxiv.org/abs/2506.13131.
[11] Eser Aygün, Anastasiya Belyaeva, Gheorghe Comanici, Marc Coram, Hao Cui, et al. An AI
     system to help scientists write expert-level empirical software. Nature, 654(8120):909–916,
     2026. ISSN 1476-4687. doi: 10.1038/s41586-026-10658-6. URL https://doi.org/10.
     1038/s41586-026-10658-6.
[12] Tianyi Li, Shihui Zang, and Moritz Münchmeyer. MadEvolve: evolutionary optimization of
     cosmological algorithms with large language models. Mach. Learn. Sci. Tech., 7(4):045026,
     2026. doi: 10.1088/2632-2153/ae7e3b.


                                                  5
[13] Piyush Jha, Prithwish Jana, Pranavkrishna Suresh, Arnav Arora, and Vijay Ganesh. RLSF:
     Fine-tuning LLMs via Symbolic Feedback. In ECAI 2025, volume 413 of Frontiers in Artificial
     Intelligence and Applications, pages 1687–1694. IOS Press, 2025. ISBN 9781643686318. doi:
     10.3233/faia250996. URL https://arxiv.org/abs/2405.16661.
[14] Piyush Jha, Jake Rudolph, Victoria Knapp-Pérez, Max Fieg, Aishik Ghosh, and Vijay Ganesh.
     CDRL: Certification-Driven Reinforcement Learning for Neutrino Flavor Model Discovery,
     2026. URL https://arxiv.org/abs/2608.20686.
[15] Yu Feng, Ruben Martins, Osbert Bastani, and Isil Dillig. Program synthesis using conflict-driven
     learning. In Proceedings of the 39th ACM SIGPLAN Conference on Programming Language
     Design and Implementation, PLDI ’18, pages 420–435. ACM, 2018. doi: 10.1145/3192366.
     3192382. URL https://www.cs.utexas.edu/~isil/pldi18-neo.pdf.
[16] Robert Tjarko Lange, Yuki Imajuku, and Edoardo Cetin. ShinkaEvolve: Towards Open-Ended
     And Sample-Efficient Program Evolution. arXiv preprint arXiv:2509.19349, 2025. URL
     https://arxiv.org/abs/2509.19349.
[17] Joao Marques-Silva, Ines Lynce, and Sharad Malik. Conflict-Driven Clause Learn-
     ing SAT Solvers.      In Handbook of Satisfiability, pages 131–153. IOS Press,
     2009. doi: 10.3233/978-1-58603-929-5-131. URL https://doi.org/10.3233/
     978-1-58603-929-5-131.
[18] Xinyu Wang, Greg Anderson, Isil Dillig, and K. L. McMillan. Learning Abstractions for
     Program Synthesis. In Computer Aided Verification, volume 10981 of Lecture Notes in Computer
     Science, pages 407–426. Springer, 2018. doi: 10.1007/978-3-319-96145-3_22. URL https:
     //arxiv.org/abs/1804.04152.
[19] Xinyu Wang, Isil Dillig, and Rishabh Singh. Program synthesis using abstraction refinement.
     Proceedings of the ACM on Programming Languages, 2(POPL):63:1–63:30, 2018. doi: 10.
     1145/3158151. URL https://arxiv.org/abs/1710.07740.
[20] David Menendez and Santosh Nagarakatte. Alive-Infer: data-driven precondition inference
     for peephole optimizations in LLVM. In Proceedings of the 38th ACM SIGPLAN Conference
     on Programming Language Design and Implementation, pages 49–63. ACM, 2017. doi:
     10.1145/3062341.3062372. URL https://people.cs.rutgers.edu/~santosh.
     nagarakatte/papers/pldi2017-alive-infer.pdf.
[21] Berkeley Churchill, Oded Padon, Rahul Sharma, and Alex Aiken. Semantic program align-
     ment for equivalence checking. In Proceedings of the 40th ACM SIGPLAN Conference
     on Programming Language Design and Implementation, pages 1027–1040. ACM, 2019.
     doi: 10.1145/3314221.3314596. URL https://www.berkeleychurchill.com/
     research/pldi2019.pdf.
[22] Nadia Polikarpova, Ivan Kuraj, and Armando Solar-Lezama. Program synthesis from poly-
     morphic refinement types. In Proceedings of the 37th ACM SIGPLAN Conference on
     Programming Language Design and Implementation, pages 522–538. ACM, 2016. doi:
     10.1145/2908080.2908093. URL https://cseweb.ucsd.edu/~npolikarpova/
     publications/pldi16.pdf.
[23] P. Ezudheen, Daniel Neider, Deepak D’Souza, Pranav Garg, and P. Madhusudan. Horn-ICE
     learning for synthesizing invariants and contracts. Proceedings of the ACM on Programming
     Languages, 2(OOPSLA):131:1–131:25, 2018. doi: 10.1145/3276501. URL https://madhu.
     cs.illinois.edu/HornICELearning-OOPSLA18.pdf.
[24] Subbarao Kambhampati, Karthik Valmeekam, Lin Guan, Mudit Verma, Kaya Stechly, Siddhant
     Bhambri, Lucas Saldyt, and Anil Murthy. LLMs Can’t Plan, But Can Help Planning in
     LLM-Modulo Frameworks, 2024. URL https://arxiv.org/abs/2402.01817.
[25] Leonardo de Moura and Sebastian Ullrich. The Lean 4 Theorem Prover and Programming
     Language. In Automated Deduction – CADE 28: 28th International Conference on Automated
     Deduction, Virtual Event, July 12–15, 2021, Proceedings, pages 625–635, Berlin, Heidelberg,
     2021. Springer-Verlag. ISBN 978-3-030-79875-8. doi: 10.1007/978-3-030-79876-5_37. URL
     https://lean-lang.org/doc/reference/latest/.


                                                 6
[26] Edmund Clarke, Daniel Kroening, and Flavio Lerda. A Tool for Checking ANSI-C Programs.
     In Kurt Jensen and Andreas Podelski, editors, Tools and Algorithms for the Construction and
     Analysis of Systems (TACAS 2004), volume 2988 of Lecture Notes in Computer Science, pages
     168–176. Springer, 2004. ISBN 3-540-21299-X. URL https://diffblue.github.io/
     cbmc/.
[27] The Physlib community. Physlib: The Lean Physics Library. https://github.com/
     leanprover-community/physlib, 2024.
[28] Joseph Tooby-Smith. HepLean: Digitalising high energy physics. Comput. Phys. Commun.,
     308:109457, 2025. doi: 10.1016/j.cpc.2024.109457. URL https://arxiv.org/abs/
     2405.08863.
[29] The mathlib Community. The Lean mathematical library. In Proceedings of the 9th ACM
     SIGPLAN International Conference on Certified Programs and Proofs, POPL ’20, pages 367–
     381. ACM, 2020. doi: 10.1145/3372885.3373824. URL https://arxiv.org/abs/
     1910.09336.
[30] Nuno P. Lopes, Juneyoung Lee, Chung-Kil Hur, Zhengyang Liu, and John Regehr. Alive2:
     Bounded Translation Validation for LLVM. In Proc. of the 42nd ACM SIGPLAN International
     Conference on Programming Language Design and Implementation (PLDI), 2021. doi: 10.1145/
     3453483.3454030. URL https://web.ist.utl.pt/nuno.lopes/pubs.php?id=
     alive2-pldi21.
[31] Benjamin Driscoll, Kshitij Dubey, Anjiang Wei, Neeraj Kayal, Rahul Sharma, and Alex Aiken.
     Equivalence Checking of ML GPU Kernels, 2025. URL https://arxiv.org/abs/
     2511.12638.
[32] Compute Sanitizer. NVIDIA Corporation, 2026. URL https://docs.nvidia.com/
     compute-sanitizer/ComputeSanitizer/index.html. Documentation updated
     July 20, 2026.
[33] Nsight Compute Profiling Guide. NVIDIA Corporation, 2026. URL https://docs.
     nvidia.com/nsight-compute/ProfilingGuide/index.html. Documentation
     updated July 15, 2026.




                                               7
